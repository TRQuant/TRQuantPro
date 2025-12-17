# -*- coding: utf-8 -*-
"""
批量回测管理器
==============
Phase 3 Task 3.2.2: 批量回测管理器

特性:
1. 并行回测（多进程/多线程）
2. 参数网格（自动生成参数组合）
3. 结果对比（自动生成对比报告）
"""

import logging
import time
import asyncio
from itertools import product
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any, Tuple
from datetime import datetime
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ==================== 参数网格 ====================

@dataclass
class ParameterGrid:
    """参数网格定义"""
    name: str
    values: List[Any]
    
    def __len__(self):
        return len(self.values)


@dataclass
class GridSearchConfig:
    """网格搜索配置"""
    parameters: List[ParameterGrid] = field(default_factory=list)
    
    def add_parameter(self, name: str, values: List[Any]) -> "GridSearchConfig":
        """添加参数"""
        self.parameters.append(ParameterGrid(name=name, values=values))
        return self
    
    def get_combinations(self) -> List[Dict[str, Any]]:
        """获取所有参数组合"""
        if not self.parameters:
            return [{}]
        
        param_names = [p.name for p in self.parameters]
        param_values = [p.values for p in self.parameters]
        
        combinations = []
        for combo in product(*param_values):
            combinations.append(dict(zip(param_names, combo)))
        
        return combinations
    
    @property
    def total_combinations(self) -> int:
        """总组合数"""
        if not self.parameters:
            return 0
        total = 1
        for p in self.parameters:
            total *= len(p)
        return total


# ==================== 批量回测结果 ====================

@dataclass
class BatchBacktestResult:
    """批量回测结果"""
    task_id: str
    params: Dict[str, Any]
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    calmar_ratio: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    duration_seconds: float = 0.0
    success: bool = False
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "params": self.params,
            "total_return": round(self.total_return * 100, 2),
            "annual_return": round(self.annual_return * 100, 2),
            "sharpe_ratio": round(self.sharpe_ratio, 2),
            "max_drawdown": round(self.max_drawdown * 100, 2),
            "calmar_ratio": round(self.calmar_ratio, 2),
            "win_rate": round(self.win_rate * 100, 2),
            "total_trades": self.total_trades,
            "duration_seconds": round(self.duration_seconds, 2),
            "success": self.success,
            "error": self.error,
        }


@dataclass
class BatchBacktestSummary:
    """批量回测汇总"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_time_seconds: float = 0.0
    results: List[BatchBacktestResult] = field(default_factory=list)
    best_result: Optional[BatchBacktestResult] = None
    
    def add_result(self, result: BatchBacktestResult):
        self.results.append(result)
        self.completed_tasks += 1
        if not result.success:
            self.failed_tasks += 1
        
        # 更新最佳结果（按夏普比率）
        if result.success:
            if self.best_result is None or result.sharpe_ratio > self.best_result.sharpe_ratio:
                self.best_result = result
    
    def to_dataframe(self) -> pd.DataFrame:
        """转为 DataFrame"""
        rows = [r.to_dict() for r in self.results]
        return pd.DataFrame(rows)
    
    def get_ranking(self, metric: str = "sharpe_ratio", top_n: int = 10) -> pd.DataFrame:
        """获取排名"""
        df = self.to_dataframe()
        if df.empty:
            return df
        
        df_success = df[df["success"] == True]
        if df_success.empty:
            return df_success
        
        # 按指标排序
        ascending = metric in ["max_drawdown", "duration_seconds"]
        return df_success.sort_values(metric, ascending=ascending).head(top_n)


# ==================== 批量回测管理器 ====================

class BatchBacktestManager:
    """批量回测管理器"""
    
    def __init__(
        self,
        max_workers: int = 4,
        use_multiprocessing: bool = True
    ):
        """
        初始化
        
        Args:
            max_workers: 最大并行数
            use_multiprocessing: 使用多进程（否则用多线程）
        """
        self.max_workers = max_workers
        self.use_multiprocessing = use_multiprocessing
        self._progress_callback: Optional[Callable] = None
        
        logger.info(f"✅ 批量回测管理器初始化: max_workers={max_workers}, multiprocessing={use_multiprocessing}")
    
    def set_progress_callback(self, callback: Callable[[float, str], None]):
        """设置进度回调"""
        self._progress_callback = callback
    
    def _report_progress(self, progress: float, message: str):
        if self._progress_callback:
            self._progress_callback(progress, message)
        logger.info(f"[{progress*100:.0f}%] {message}")
    
    def run_grid_search(
        self,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_type: str,
        grid_config: GridSearchConfig,
        level: str = "fast",
        use_mock: bool = True
    ) -> BatchBacktestSummary:
        """
        运行参数网格搜索
        
        Args:
            securities: 股票列表
            start_date: 开始日期
            end_date: 结束日期
            strategy_type: 策略类型
            grid_config: 网格配置
            level: 回测层级
            use_mock: 使用模拟数据
            
        Returns:
            批量回测汇总
        """
        start_time = time.time()
        combinations = grid_config.get_combinations()
        total = len(combinations)
        
        summary = BatchBacktestSummary(total_tasks=total)
        
        self._report_progress(0.0, f"开始网格搜索: {total} 个参数组合")
        
        if total == 0:
            return summary
        
        # 准备任务
        tasks = []
        for i, params in enumerate(combinations):
            task_id = f"grid_{i:04d}"
            tasks.append((task_id, securities, start_date, end_date, strategy_type, params, level, use_mock))
        
        # 并行执行
        Executor = ProcessPoolExecutor if self.use_multiprocessing else ThreadPoolExecutor
        
        # 由于跨进程序列化问题，使用线程池
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for task in tasks:
                future = executor.submit(_run_single_backtest, *task)
                futures[future] = task[0]  # task_id
            
            completed = 0
            for future in as_completed(futures):
                task_id = futures[future]
                try:
                    result = future.result()
                    summary.add_result(result)
                except Exception as e:
                    logger.error(f"任务 {task_id} 执行异常: {e}")
                    summary.add_result(BatchBacktestResult(
                        task_id=task_id,
                        params={},
                        success=False,
                        error=str(e)
                    ))
                
                completed += 1
                progress = completed / total
                self._report_progress(progress, f"完成 {completed}/{total}")
        
        summary.total_time_seconds = time.time() - start_time
        
        self._report_progress(1.0, f"网格搜索完成: {summary.completed_tasks}/{total}，耗时 {summary.total_time_seconds:.2f}秒")
        
        return summary
    
    def run_batch(
        self,
        backtest_configs: List[Dict[str, Any]],
        level: str = "fast"
    ) -> BatchBacktestSummary:
        """
        运行批量回测
        
        Args:
            backtest_configs: 回测配置列表
            level: 回测层级
            
        Returns:
            批量回测汇总
        """
        start_time = time.time()
        total = len(backtest_configs)
        summary = BatchBacktestSummary(total_tasks=total)
        
        self._report_progress(0.0, f"开始批量回测: {total} 个任务")
        
        # 并行执行
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for i, config in enumerate(backtest_configs):
                task_id = f"batch_{i:04d}"
                future = executor.submit(
                    _run_single_backtest,
                    task_id,
                    config.get("securities", []),
                    config.get("start_date"),
                    config.get("end_date"),
                    config.get("strategy_type", "momentum"),
                    config.get("params", {}),
                    level,
                    config.get("use_mock", True)
                )
                futures[future] = task_id
            
            completed = 0
            for future in as_completed(futures):
                task_id = futures[future]
                try:
                    result = future.result()
                    summary.add_result(result)
                except Exception as e:
                    logger.error(f"任务 {task_id} 执行异常: {e}")
                    summary.add_result(BatchBacktestResult(
                        task_id=task_id,
                        params={},
                        success=False,
                        error=str(e)
                    ))
                
                completed += 1
                self._report_progress(completed / total, f"完成 {completed}/{total}")
        
        summary.total_time_seconds = time.time() - start_time
        return summary
    
    def generate_comparison_report(
        self,
        summary: BatchBacktestSummary,
        output_path: str = None,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        生成对比报告
        
        Args:
            summary: 批量回测汇总
            output_path: 输出路径
            top_n: 显示前N个结果
            
        Returns:
            报告数据
        """
        df = summary.to_dataframe()
        
        if df.empty:
            return {"error": "无回测结果"}
        
        df_success = df[df["success"] == True]
        
        report = {
            "summary": {
                "total_tasks": summary.total_tasks,
                "completed_tasks": summary.completed_tasks,
                "failed_tasks": summary.failed_tasks,
                "total_time_seconds": round(summary.total_time_seconds, 2),
                "avg_time_per_task": round(summary.total_time_seconds / max(summary.total_tasks, 1), 2),
            },
            "statistics": {},
            "best_results": {},
            "top_n": [],
        }
        
        if not df_success.empty:
            # 统计信息
            for metric in ["total_return", "annual_return", "sharpe_ratio", "max_drawdown", "win_rate"]:
                report["statistics"][metric] = {
                    "mean": round(df_success[metric].mean(), 2),
                    "std": round(df_success[metric].std(), 2),
                    "min": round(df_success[metric].min(), 2),
                    "max": round(df_success[metric].max(), 2),
                }
            
            # 最佳结果
            report["best_results"] = {
                "by_sharpe": df_success.loc[df_success["sharpe_ratio"].idxmax()].to_dict() if not df_success.empty else None,
                "by_return": df_success.loc[df_success["total_return"].idxmax()].to_dict() if not df_success.empty else None,
                "by_drawdown": df_success.loc[df_success["max_drawdown"].idxmax()].to_dict() if not df_success.empty else None,
            }
            
            # Top N
            ranking = summary.get_ranking("sharpe_ratio", top_n)
            report["top_n"] = ranking.to_dict(orient="records")
        
        # 保存报告
        if output_path:
            import json
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"报告已保存: {output_path}")
        
        return report


# ==================== 辅助函数 ====================

def _run_single_backtest(
    task_id: str,
    securities: List[str],
    start_date: str,
    end_date: str,
    strategy_type: str,
    params: Dict[str, Any],
    level: str,
    use_mock: bool
) -> BatchBacktestResult:
    """运行单个回测（用于并行）"""
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    start_time = time.time()
    
    result = BatchBacktestResult(
        task_id=task_id,
        params=params
    )
    
    try:
        from core.backtest.unified_backtest_manager import (
            UnifiedBacktestManager,
            UnifiedBacktestConfig,
            BacktestLevel,
        )
        
        config = UnifiedBacktestConfig(
            start_date=start_date,
            end_date=end_date,
            securities=securities,
            use_mock=use_mock,
        )
        
        manager = UnifiedBacktestManager(config)
        
        # 运行回测
        backtest_results = manager.run_full_pipeline(
            strategy_type=strategy_type,
            strategy_params=params,
            levels=[BacktestLevel(level)]
        )
        
        bt_result = backtest_results.get(level)
        
        if bt_result and bt_result.success:
            result.success = True
            result.total_return = bt_result.total_return
            result.annual_return = bt_result.annual_return
            result.sharpe_ratio = bt_result.sharpe_ratio
            result.max_drawdown = bt_result.max_drawdown
            result.calmar_ratio = bt_result.calmar_ratio
            result.win_rate = bt_result.win_rate
            result.total_trades = bt_result.total_trades
        else:
            result.error = bt_result.error if bt_result else "回测失败"
        
    except Exception as e:
        logger.error(f"任务 {task_id} 回测异常: {e}")
        result.error = str(e)
    
    result.duration_seconds = time.time() - start_time
    return result


# ==================== 便捷函数 ====================

def grid_search(
    securities: List[str],
    start_date: str,
    end_date: str,
    strategy_type: str = "momentum",
    parameter_ranges: Dict[str, List[Any]] = None,
    max_workers: int = 4,
    use_mock: bool = True
) -> BatchBacktestSummary:
    """
    快速网格搜索
    
    Args:
        securities: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        strategy_type: 策略类型
        parameter_ranges: 参数范围 {"lookback": [10, 20, 30], "top_n": [5, 10]}
        max_workers: 并行数
        use_mock: 使用模拟数据
        
    Returns:
        批量回测汇总
    """
    parameter_ranges = parameter_ranges or {}
    
    # 构建网格配置
    grid_config = GridSearchConfig()
    for name, values in parameter_ranges.items():
        grid_config.add_parameter(name, values)
    
    # 运行网格搜索
    manager = BatchBacktestManager(max_workers=max_workers)
    return manager.run_grid_search(
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        strategy_type=strategy_type,
        grid_config=grid_config,
        use_mock=use_mock
    )


def batch_backtest(
    configs: List[Dict[str, Any]],
    max_workers: int = 4
) -> BatchBacktestSummary:
    """
    快速批量回测
    
    Args:
        configs: 回测配置列表
        max_workers: 并行数
        
    Returns:
        批量回测汇总
    """
    manager = BatchBacktestManager(max_workers=max_workers)
    return manager.run_batch(configs)


# ==================== 导出 ====================

__all__ = [
    "ParameterGrid",
    "GridSearchConfig",
    "BatchBacktestResult",
    "BatchBacktestSummary",
    "BatchBacktestManager",
    "grid_search",
    "batch_backtest",
]
