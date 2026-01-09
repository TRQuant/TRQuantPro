#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
并行回测运行器 - 利用缓存数据和GPU加速执行回测
==============================================

功能：
1. 从本地缓存加载数据（避免重复API调用）
2. GPU加速因子计算（利用现有 gpu_accelerator.py）
3. 并行执行多个回测任务
4. 实时进度显示
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import pandas as pd
import numpy as np
from tqdm import tqdm

from .data_preloader import DataPreloader, PreloadResult, preload_6month_data
from .bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig
from .bullettrade_backtest import BulletTradeBacktest
from core.bullettrade.config import BTConfig
from core.bullettrade.result import BTResult

# GPU加速器
try:
    from .gpu_accelerator import GPUTechnicalIndicatorCalculator, USE_GPU
except ImportError:
    GPUTechnicalIndicatorCalculator = None
    USE_GPU = False

logger = logging.getLogger(__name__)


@dataclass
class BacktestTask:
    """回测任务"""
    task_id: str
    start_date: str
    end_date: str
    strategy_config: StrategyConfig
    initial_capital: float = 1000000.0
    description: str = ""


@dataclass
class ParallelBacktestResult:
    """并行回测结果"""
    task_id: str
    start_date: str
    end_date: str
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    calmar_ratio: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    report_path: str = ""
    duration_seconds: float = 0.0
    success: bool = False
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_return": round(self.total_return * 100, 2),
            "annual_return": round(self.annual_return * 100, 2),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "win_rate": round(self.win_rate * 100, 2),
            "total_trades": self.total_trades,
            "report_path": self.report_path,
            "duration_seconds": round(self.duration_seconds, 2),
            "success": self.success,
            "error": self.error
        }


@dataclass
class BatchBacktestSummary:
    """批量回测汇总"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_duration_seconds: float = 0.0
    results: List[ParallelBacktestResult] = field(default_factory=list)
    best_result: Optional[ParallelBacktestResult] = None
    worst_result: Optional[ParallelBacktestResult] = None
    
    def add_result(self, result: ParallelBacktestResult):
        """添加结果"""
        self.results.append(result)
        self.completed_tasks += 1
        if not result.success:
            self.failed_tasks += 1
        
        # 更新最佳/最差结果
        if result.success:
            if self.best_result is None or result.sharpe_ratio > self.best_result.sharpe_ratio:
                self.best_result = result
            if self.worst_result is None or result.sharpe_ratio < self.worst_result.sharpe_ratio:
                self.worst_result = result
    
    def to_dataframe(self) -> pd.DataFrame:
        """转为DataFrame"""
        rows = [r.to_dict() for r in self.results]
        return pd.DataFrame(rows)
    
    def get_statistics(self) -> Dict[str, float]:
        """获取统计信息"""
        if not self.results:
            return {}
        
        successful_results = [r for r in self.results if r.success]
        if not successful_results:
            return {}
        
        returns = [r.total_return for r in successful_results]
        sharpes = [r.sharpe_ratio for r in successful_results]
        drawdowns = [r.max_drawdown for r in successful_results]
        
        return {
            "avg_return": np.mean(returns),
            "std_return": np.std(returns),
            "avg_sharpe": np.mean(sharpes),
            "std_sharpe": np.std(sharpes),
            "avg_drawdown": np.mean(drawdowns),
            "max_drawdown": max(drawdowns),
            "win_count": sum(1 for r in returns if r > 0),
            "loss_count": sum(1 for r in returns if r <= 0)
        }


class ParallelBacktestRunner:
    """并行回测运行器"""
    
    def __init__(
        self,
        cache_dir: str = "data/cache",
        output_dir: str = "output/advisor_v4/parallel_backtest",
        use_gpu: bool = True,
        max_workers: int = 3,
        verbose: bool = True
    ):
        """
        初始化并行回测运行器
        
        Args:
            cache_dir: 数据缓存目录
            output_dir: 输出目录
            use_gpu: 是否使用GPU加速
            max_workers: 最大并行工作数
            verbose: 是否显示详细输出
        """
        self.cache_dir = Path(cache_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.use_gpu = use_gpu and USE_GPU
        self.max_workers = max_workers
        self.verbose = verbose
        
        # 数据预加载器
        self.data_preloader = DataPreloader(
            max_workers=max_workers,
            cache_dir=str(cache_dir),
            verbose=verbose
        )
        
        # GPU计算器
        self.gpu_calculator = None
        if self.use_gpu and GPUTechnicalIndicatorCalculator:
            try:
                self.gpu_calculator = GPUTechnicalIndicatorCalculator(batch_size=100, use_gpu=True)
                if self.verbose:
                    print(f"✅ GPU加速已启用")
            except Exception as e:
                logger.warning(f"GPU初始化失败，使用CPU: {e}")
                self.use_gpu = False
        
        # 进度追踪
        self._progress_lock = threading.Lock()
        self._current_progress = 0.0
    
    def ensure_data_cached(
        self,
        start_date: str,
        end_date: str,
        force_refresh: bool = False
    ) -> PreloadResult:
        """
        确保数据已缓存（优先使用MongoDB）
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            force_refresh: 强制刷新
        
        Returns:
            PreloadResult
        """
        if self.verbose:
            print(f"\n🔍 检查数据缓存...")
        
        period_key = self.data_preloader._get_period_key(start_date, end_date)
        
        # 优先检查MongoDB存储
        if self.data_preloader.use_mongodb and self.data_preloader.mongodb_storage:
            # 检查MongoDB中是否已有数据
            if not force_refresh:
                prices_df = self.data_preloader.mongodb_storage.load_daily_prices(period_key=period_key)
                if prices_df is not None and not prices_df.empty:
                    if self.verbose:
                        print(f"   ✅ 数据已从MongoDB加载: {len(prices_df)}条")
                    return PreloadResult(
                        success=True,
                        cache_paths={"prices": "mongodb"},
                        total_stocks=len(prices_df["code"].unique()) if "code" in prices_df.columns else 0,
                        data_size_mb=0.0  # MongoDB不计算文件大小
                    )
        
        # 检查文件缓存
        prices_cache = self.cache_dir / "daily_prices" / f"{period_key}_prices.parquet"
        if prices_cache.exists() and not force_refresh:
            if self.verbose:
                print(f"   ✅ 文件缓存已存在: {prices_cache}")
            return PreloadResult(
                success=True,
                cache_paths={"prices": prices_cache},
                data_size_mb=prices_cache.stat().st_size / (1024 * 1024)
            )
        
        # 需要下载数据（DataPreloader会自动保存到MongoDB）
        if self.verbose:
            print(f"   📥 开始下载数据...")
        
        result = self.data_preloader.preload_market_data(
            start_date=start_date,
            end_date=end_date,
            force_refresh=force_refresh
        )
        
        # 下载指数数据
        index_paths = self.data_preloader.preload_index_data(
            start_date=start_date,
            end_date=end_date,
            force_refresh=force_refresh
        )
        result.cache_paths.update(index_paths)
        
        return result
    
    def run_single_backtest(
        self,
        task: BacktestTask
    ) -> ParallelBacktestResult:
        """
        执行单个回测任务
        
        Args:
            task: 回测任务
        
        Returns:
            ParallelBacktestResult
        """
        result = ParallelBacktestResult(
            task_id=task.task_id,
            start_date=task.start_date,
            end_date=task.end_date
        )
        
        start_time = time.time()
        
        try:
            # 配置BulletTrade
            bt_config = BTConfig(
                start_date=task.start_date,
                end_date=task.end_date,
                initial_capital=task.initial_capital,
                benchmark="000300.XSHG",
                frequency="day",
                data_provider="jqdata",
                output_dir=str(self.output_dir / task.task_id),
                generate_html=True,
                generate_csv=True
            )
            
            # 创建回测实例
            backtest = BulletTradeBacktest(
                strategy_config=task.strategy_config,
                bt_config=bt_config,
                output_dir=str(self.output_dir / task.task_id),
                cache_dir=str(self.cache_dir) if self.cache_dir else None
            )
            
            # 执行回测
            bt_result = backtest.run_backtest(
                start_date=task.start_date,
                end_date=task.end_date,
                initial_capital=task.initial_capital
            )
            
            # 提取结果
            result.total_return = bt_result.total_return
            result.annual_return = bt_result.annual_return
            result.sharpe_ratio = bt_result.sharpe_ratio
            result.max_drawdown = bt_result.max_drawdown
            result.win_rate = bt_result.win_rate
            result.total_trades = bt_result.total_trades
            result.report_path = bt_result.report_path
            
            # 计算Calmar比率
            if result.max_drawdown != 0:
                result.calmar_ratio = result.annual_return / abs(result.max_drawdown)
            
            result.success = True
            
        except Exception as e:
            result.success = False
            result.error = str(e)
            logger.error(f"回测任务 {task.task_id} 失败: {e}")
        
        result.duration_seconds = time.time() - start_time
        return result
    
    def run_backtest_with_cache(
        self,
        start_date: str,
        end_date: str,
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0,
        task_id: str = None
    ) -> ParallelBacktestResult:
        """
        使用缓存数据执行回测
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            strategy_config: 策略配置
            initial_capital: 初始资金
            task_id: 任务ID
        
        Returns:
            ParallelBacktestResult
        """
        if task_id is None:
            task_id = f"backtest_{start_date}_{end_date}"
        
        if strategy_config is None:
            strategy_config = StrategyConfig()
        
        # 确保数据已缓存
        cache_result = self.ensure_data_cached(start_date, end_date)
        if not cache_result.success:
            return ParallelBacktestResult(
                task_id=task_id,
                start_date=start_date,
                end_date=end_date,
                success=False,
                error="数据缓存失败"
            )
        
        # 创建任务并执行
        task = BacktestTask(
            task_id=task_id,
            start_date=start_date,
            end_date=end_date,
            strategy_config=strategy_config,
            initial_capital=initial_capital
        )
        
        return self.run_single_backtest(task)
    
    def run_parallel_backtests(
        self,
        periods: List[Tuple[str, str]],
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0
    ) -> BatchBacktestSummary:
        """
        并行执行多个时间段的回测
        
        Args:
            periods: 时间段列表 [(start, end), ...]
            strategy_config: 策略配置
            initial_capital: 初始资金
        
        Returns:
            BatchBacktestSummary
        """
        if strategy_config is None:
            strategy_config = StrategyConfig()
        
        summary = BatchBacktestSummary(total_tasks=len(periods))
        start_time = time.time()
        
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🚀 并行回测运行器 - 开始执行")
            print(f"{'='*60}")
            print(f"   任务数: {len(periods)}")
            print(f"   并行数: {self.max_workers}")
            print(f"   GPU加速: {'是' if self.use_gpu else '否'}")
        
        # 首先确保所有数据都已缓存
        if self.verbose:
            print(f"\n📥 预加载所有时间段的数据...")
        
        for start_date, end_date in periods:
            self.ensure_data_cached(start_date, end_date)
        
        # 创建任务列表
        tasks = []
        for i, (start_date, end_date) in enumerate(periods):
            task = BacktestTask(
                task_id=f"period_{i}_{start_date}_{end_date}",
                start_date=start_date,
                end_date=end_date,
                strategy_config=strategy_config,
                initial_capital=initial_capital,
                description=f"{start_date} ~ {end_date}"
            )
            tasks.append(task)
        
        # 并行执行回测
        if self.verbose:
            print(f"\n🔄 执行回测...")
        
        # 由于BulletTrade可能有资源限制，使用线程池而非进程池
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(tasks))) as executor:
            futures = {
                executor.submit(self.run_single_backtest, task): task
                for task in tasks
            }
            
            with tqdm(total=len(tasks), desc="执行回测", disable=not self.verbose) as pbar:
                for future in as_completed(futures):
                    task = futures[future]
                    try:
                        result = future.result()
                        summary.add_result(result)
                        
                        if self.verbose and result.success:
                            pbar.set_postfix({
                                "任务": task.task_id[:20],
                                "收益": f"{result.total_return:.2%}",
                                "夏普": f"{result.sharpe_ratio:.2f}"
                            })
                    except Exception as e:
                        logger.error(f"任务 {task.task_id} 执行失败: {e}")
                        summary.add_result(ParallelBacktestResult(
                            task_id=task.task_id,
                            start_date=task.start_date,
                            end_date=task.end_date,
                            success=False,
                            error=str(e)
                        ))
                    pbar.update(1)
        
        summary.total_duration_seconds = time.time() - start_time
        
        # 输出汇总
        if self.verbose:
            self._print_summary(summary)
        
        # 保存汇总结果
        self._save_summary(summary)
        
        return summary
    
    def _print_summary(self, summary: BatchBacktestSummary):
        """打印汇总信息"""
        print(f"\n{'='*60}")
        print(f"📊 回测汇总")
        print(f"{'='*60}")
        print(f"   总任务数: {summary.total_tasks}")
        print(f"   完成数: {summary.completed_tasks}")
        print(f"   失败数: {summary.failed_tasks}")
        print(f"   总耗时: {summary.total_duration_seconds:.1f} 秒")
        
        stats = summary.get_statistics()
        if stats:
            print(f"\n📈 绩效统计:")
            print(f"   平均收益率: {stats['avg_return']*100:.2f}% (±{stats['std_return']*100:.2f}%)")
            print(f"   平均夏普比率: {stats['avg_sharpe']:.2f} (±{stats['std_sharpe']:.2f})")
            print(f"   平均最大回撤: {stats['avg_drawdown']*100:.2f}%")
            print(f"   盈利/亏损: {stats['win_count']}/{stats['loss_count']}")
        
        if summary.best_result:
            print(f"\n🏆 最佳表现:")
            print(f"   时间段: {summary.best_result.start_date} ~ {summary.best_result.end_date}")
            print(f"   收益率: {summary.best_result.total_return*100:.2f}%")
            print(f"   夏普比率: {summary.best_result.sharpe_ratio:.2f}")
        
        if summary.worst_result:
            print(f"\n⚠️  最差表现:")
            print(f"   时间段: {summary.worst_result.start_date} ~ {summary.worst_result.end_date}")
            print(f"   收益率: {summary.worst_result.total_return*100:.2f}%")
            print(f"   夏普比率: {summary.worst_result.sharpe_ratio:.2f}")
    
    def _save_summary(self, summary: BatchBacktestSummary):
        """保存汇总结果"""
        import json
        
        summary_path = self.output_dir / "batch_summary.json"
        
        summary_data = {
            "total_tasks": summary.total_tasks,
            "completed_tasks": summary.completed_tasks,
            "failed_tasks": summary.failed_tasks,
            "total_duration_seconds": summary.total_duration_seconds,
            "statistics": summary.get_statistics(),
            "results": [r.to_dict() for r in summary.results],
            "generated_at": datetime.now().isoformat()
        }
        
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        if self.verbose:
            print(f"\n💾 汇总结果已保存: {summary_path}")
        
        # 保存为CSV
        df = summary.to_dataframe()
        csv_path = self.output_dir / "batch_results.csv"
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        
        if self.verbose:
            print(f"   CSV结果: {csv_path}")


def run_6month_baseline_backtest(
    start_date: str = "2024-07-01",
    end_date: str = "2024-12-31",
    initial_capital: float = 1000000.0,
    cache_dir: str = "data/cache",
    output_dir: str = "output/advisor_v4/baseline"
) -> ParallelBacktestResult:
    """
    执行半年基准回测的便捷函数
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
        cache_dir: 缓存目录
        output_dir: 输出目录
    
    Returns:
        ParallelBacktestResult
    """
    print(f"\n{'='*70}")
    print(f"🎯 半年基准回测")
    print(f"{'='*70}")
    print(f"   时间段: {start_date} ~ {end_date}")
    print(f"   初始资金: {initial_capital:,.0f}")
    
    # 创建运行器
    runner = ParallelBacktestRunner(
        cache_dir=cache_dir,
        output_dir=output_dir,
        use_gpu=True,
        max_workers=3,
        verbose=True
    )
    
    # 使用默认策略配置
    strategy_config = StrategyConfig(
        max_stocks=10,
        single_position_max=0.20,
        stop_loss=-0.08,
        take_profit=0.30,
        trailing_stop=0.15,
        time_stop_days=20,
        min_total_score=30.0  # 降低阈值确保有股票通过筛选
    )
    
    # 执行回测
    result = runner.run_backtest_with_cache(
        start_date=start_date,
        end_date=end_date,
        strategy_config=strategy_config,
        initial_capital=initial_capital,
        task_id="6month_baseline"
    )
    
    # 打印结果
    print(f"\n{'='*70}")
    print(f"📊 回测结果")
    print(f"{'='*70}")
    
    if result.success:
        print(f"   ✅ 回测成功")
        print(f"   总收益率: {result.total_return*100:.2f}%")
        print(f"   年化收益: {result.annual_return*100:.2f}%")
        print(f"   夏普比率: {result.sharpe_ratio:.2f}")
        print(f"   最大回撤: {result.max_drawdown*100:.2f}%")
        print(f"   卡玛比率: {result.calmar_ratio:.2f}")
        print(f"   胜率: {result.win_rate*100:.2f}%")
        print(f"   总交易次数: {result.total_trades}")
        print(f"   报告路径: {result.report_path}")
        print(f"   耗时: {result.duration_seconds:.1f} 秒")
    else:
        print(f"   ❌ 回测失败: {result.error}")
    
    return result


if __name__ == "__main__":
    # 执行半年基准回测
    result = run_6month_baseline_backtest(
        start_date="2024-07-01",
        end_date="2024-12-31",
        initial_capital=1000000.0
    )
