#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量回测验证器 - 支持多时间段和多市场环境回测
==============================================

功能：
1. 多时间段回测（滚动窗口、固定窗口、自定义时间段）
2. 市场环境标签（预留接口，等待算法确认后实现）
3. 回测结果汇总和对比分析
4. HTML/CSV报告生成
5. 稳定性和一致性验证
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import threading

import pandas as pd
import numpy as np

from .parallel_backtest_runner import (
    ParallelBacktestRunner,
    ParallelBacktestResult,
    BatchBacktestSummary,
    BacktestTask
)
from .bullettrade_strategy_generator import StrategyConfig
from .data_preloader import DataPreloader

logger = logging.getLogger(__name__)


class WindowType(Enum):
    """时间窗口类型"""
    ROLLING = "rolling"      # 滚动窗口（如每月滚动半年）
    FIXED = "fixed"          # 固定窗口（如每季度）
    CUSTOM = "custom"        # 自定义时间段


class MarketEnvironment(Enum):
    """市场环境类型（预留，等待算法确认）"""
    BULL = "bull"            # 牛市
    BEAR = "bear"            # 熊市
    SIDEWAYS = "sideways"    # 震荡市
    UNKNOWN = "unknown"      # 未知


@dataclass
class BacktestPeriod:
    """回测时间段"""
    start_date: str
    end_date: str
    label: str = ""
    market_env: MarketEnvironment = MarketEnvironment.UNKNOWN
    description: str = ""
    
    def __post_init__(self):
        if not self.label:
            self.label = f"{self.start_date}_{self.end_date}"
    
    @property
    def days(self) -> int:
        """回测天数"""
        start = datetime.strptime(self.start_date, "%Y-%m-%d")
        end = datetime.strptime(self.end_date, "%Y-%m-%d")
        return (end - start).days
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "label": self.label,
            "market_env": self.market_env.value,
            "description": self.description,
            "days": self.days
        }


@dataclass
class ValidationResult:
    """验证结果"""
    period: BacktestPeriod
    backtest_result: ParallelBacktestResult
    passed_criteria: Dict[str, bool] = field(default_factory=dict)
    score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period.to_dict(),
            "backtest_result": self.backtest_result.to_dict(),
            "passed_criteria": self.passed_criteria,
            "score": self.score
        }


@dataclass
class ValidationSummary:
    """验证汇总"""
    total_periods: int = 0
    passed_periods: int = 0
    failed_periods: int = 0
    avg_return: float = 0.0
    avg_sharpe: float = 0.0
    avg_max_drawdown: float = 0.0
    consistency_score: float = 0.0  # 一致性得分
    stability_score: float = 0.0    # 稳定性得分
    results: List[ValidationResult] = field(default_factory=list)
    criteria_pass_rates: Dict[str, float] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_result(self, result: ValidationResult):
        """添加验证结果"""
        self.results.append(result)
        self._update_statistics()
    
    def _update_statistics(self):
        """更新统计信息"""
        if not self.results:
            return
        
        self.total_periods = len(self.results)
        
        # 统计成功的回测
        successful_results = [r for r in self.results if r.backtest_result.success]
        
        if successful_results:
            returns = [r.backtest_result.total_return for r in successful_results]
            sharpes = [r.backtest_result.sharpe_ratio for r in successful_results]
            drawdowns = [r.backtest_result.max_drawdown for r in successful_results]
            
            self.avg_return = np.mean(returns)
            self.avg_sharpe = np.mean(sharpes)
            self.avg_max_drawdown = np.mean(drawdowns)
            
            # 计算一致性得分（收益率方差的倒数）
            return_std = np.std(returns)
            self.consistency_score = 1.0 / (1.0 + return_std * 10) if return_std > 0 else 1.0
            
            # 计算稳定性得分（夏普比率的稳定性）
            sharpe_std = np.std(sharpes)
            self.stability_score = 1.0 / (1.0 + sharpe_std) if sharpe_std > 0 else 1.0
        
        # 统计通过的时间段
        self.passed_periods = sum(1 for r in self.results if r.score >= 0.6)
        self.failed_periods = self.total_periods - self.passed_periods
        
        # 统计各指标的通过率
        all_criteria = set()
        for r in self.results:
            all_criteria.update(r.passed_criteria.keys())
        
        for criterion in all_criteria:
            passed_count = sum(1 for r in self.results if r.passed_criteria.get(criterion, False))
            self.criteria_pass_rates[criterion] = passed_count / self.total_periods if self.total_periods > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_periods": self.total_periods,
            "passed_periods": self.passed_periods,
            "failed_periods": self.failed_periods,
            "avg_return": round(self.avg_return, 2),  # 已经是百分比形式，不需要再乘以100
            "avg_sharpe": round(self.avg_sharpe, 2),
            "avg_max_drawdown": round(self.avg_max_drawdown, 2),  # 已经是百分比形式，不需要再乘以100
            "consistency_score": round(self.consistency_score, 2),
            "stability_score": round(self.stability_score, 2),
            "criteria_pass_rates": {k: round(v * 100, 2) for k, v in self.criteria_pass_rates.items()},
            "generated_at": self.generated_at,
            "results": [r.to_dict() for r in self.results]
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """转为DataFrame"""
        rows = []
        for r in self.results:
            row = {
                "时间段": r.period.label,
                "开始日期": r.period.start_date,
                "结束日期": r.period.end_date,
                "天数": r.period.days,
                "市场环境": r.period.market_env.value,
                "总收益率(%)": round(r.backtest_result.total_return, 2),  # 已经是百分比形式
                "年化收益(%)": round(r.backtest_result.annual_return, 2),  # 已经是百分比形式
                "夏普比率": round(r.backtest_result.sharpe_ratio, 2),
                "最大回撤(%)": round(r.backtest_result.max_drawdown, 2),  # 已经是百分比形式
                "胜率(%)": round(r.backtest_result.win_rate, 2),  # win_rate已经是百分比形式（来自ParallelBacktestResult）
                "交易次数": r.backtest_result.total_trades,
                "验证得分": round(r.score, 2),
                "是否通过": "是" if r.score >= 0.6 else "否"
            }
            rows.append(row)
        return pd.DataFrame(rows)


@dataclass
class ValidationCriteria:
    """验证标准"""
    min_sharpe: float = 0.5           # 最低夏普比率
    max_drawdown: float = 25.0        # 最大允许回撤（百分比，如25.0表示25%）
    min_win_rate: float = 0.35        # 最低胜率
    min_total_return: float = -0.10   # 最低总收益率
    min_trades: int = 5               # 最少交易次数
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "min_sharpe": self.min_sharpe,
            "max_drawdown": self.max_drawdown,
            "min_win_rate": self.min_win_rate,
            "min_total_return": self.min_total_return,
            "min_trades": self.min_trades
        }


class BatchBacktestValidator:
    """
    批量回测验证器
    
    支持多时间段和多市场环境回测，用于验证策略的稳定性和一致性。
    """
    
    def __init__(
        self,
        cache_dir: str = "data/cache",
        output_dir: str = "output/advisor_v4/batch_validation",
        use_gpu: bool = True,
        max_workers: int = 3,
        verbose: bool = True
    ):
        """
        初始化批量回测验证器
        
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
        
        self.use_gpu = use_gpu
        self.max_workers = max_workers
        self.verbose = verbose
        
        # 并行回测运行器
        self.runner = ParallelBacktestRunner(
            cache_dir=str(cache_dir),
            output_dir=str(output_dir),
            use_gpu=use_gpu,
            max_workers=max_workers,
            verbose=verbose
        )
        
        # 数据预加载器
        self.data_preloader = DataPreloader(
            max_workers=max_workers,
            cache_dir=str(cache_dir),
            verbose=verbose
        )
        
        # 验证标准
        self.criteria = ValidationCriteria()
        
        # 市场环境识别器（预留，等待用户确认算法后实现）
        self._market_env_detector: Optional[Callable] = None
    
    def set_criteria(self, criteria: ValidationCriteria):
        """设置验证标准"""
        self.criteria = criteria
    
    def set_market_env_detector(self, detector: Callable[[str, str], MarketEnvironment]):
        """
        设置市场环境识别器
        
        Args:
            detector: 识别函数，输入(start_date, end_date)，输出MarketEnvironment
        
        注意：这是预留接口，等待用户确认算法后使用。
        """
        self._market_env_detector = detector
    
    # ==================== 时间段生成 ====================
    
    def generate_rolling_periods(
        self,
        start_date: str,
        end_date: str,
        window_months: int = 6,
        step_months: int = 1
    ) -> List[BacktestPeriod]:
        """
        生成滚动窗口时间段
        
        Args:
            start_date: 整体开始日期
            end_date: 整体结束日期
            window_months: 窗口大小（月）
            step_months: 滚动步长（月）
        
        Returns:
            时间段列表
        """
        periods = []
        
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        current_start = start_dt
        window_delta = timedelta(days=window_months * 30)  # 近似月数
        step_delta = timedelta(days=step_months * 30)
        
        idx = 0
        while current_start + window_delta <= end_dt:
            window_end = current_start + window_delta
            
            period = BacktestPeriod(
                start_date=current_start.strftime("%Y-%m-%d"),
                end_date=window_end.strftime("%Y-%m-%d"),
                label=f"rolling_{idx}_{current_start.strftime('%Y%m')}",
                description=f"滚动窗口 {idx+1}"
            )
            
            # 识别市场环境（如果有识别器）
            if self._market_env_detector:
                period.market_env = self._market_env_detector(
                    period.start_date, period.end_date
                )
            
            periods.append(period)
            current_start += step_delta
            idx += 1
        
        return periods
    
    def generate_weekly_rolling_periods(
        self,
        start_date: str,
        end_date: str,
        window_weeks: int = 12,  # 3个月约12周
        step_weeks: int = 1
    ) -> List[BacktestPeriod]:
        """
        生成按周滚动的时间段
        
        Args:
            start_date: 整体开始日期
            end_date: 整体结束日期
            window_weeks: 窗口大小（周）
            step_weeks: 滚动步长（周）
        
        Returns:
            时间段列表
        """
        periods = []
        
        try:
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            # 初始化JQData
            if not jq.is_auth():
                config_mgr = get_config_manager()
                jq_config = config_mgr.get_config('jqdata')
                jq.auth(jq_config.get('username'), jq_config.get('password'))
            
            # 获取所有交易日（优先从MongoDB/cache读取）
            all_trade_days = None
            
            # 尝试从MongoDB加载
            if self.data_preloader and self.data_preloader.use_mongodb and self.data_preloader.mongodb_storage:
                period_key = self.data_preloader._get_period_key(start_date, end_date)
                trade_days_list = self.data_preloader.mongodb_storage.load_trade_days(
                    period_key=period_key,
                    start_date=start_date,
                    end_date=end_date
                )
                if trade_days_list:
                    # 转换为datetime对象
                    from datetime import datetime
                    all_trade_days = [datetime.strptime(d, '%Y-%m-%d') for d in trade_days_list]
                    if self.verbose:
                        logger.info(f"从MongoDB加载交易日: {len(all_trade_days)} 天")
            
            # 如果MongoDB没有，尝试从JQData获取
            if all_trade_days is None or len(all_trade_days) == 0:
                try:
                    import jqdatasdk as jq
                    if not jq.is_auth():
                        # 尝试认证（如果环境变量已设置）
                        import os
                        jq_user = os.environ.get("JQDATA_USER")
                        jq_password = os.environ.get("JQDATA_PASSWORD")
                        if jq_user and jq_password:
                            jq.auth(jq_user, jq_password)
                    
                    if jq.is_auth():
                        all_trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
                        if all_trade_days and len(all_trade_days) > 0:
                            # 保存到MongoDB（如果可用）
                            if self.data_preloader and self.data_preloader.use_mongodb and self.data_preloader.mongodb_storage:
                                period_key = self.data_preloader._get_period_key(start_date, end_date)
                                trade_days_str = [d.strftime('%Y-%m-%d') for d in all_trade_days]
                                self.data_preloader.mongodb_storage.save_trade_days(
                                    trade_days=trade_days_str,
                                    period_key=period_key,
                                    start_date=start_date,
                                    end_date=end_date
                                )
                                if self.verbose:
                                    logger.info(f"交易日已保存到MongoDB: {len(trade_days_str)} 天")
                except Exception as e:
                    logger.warning(f"从JQData获取交易日失败: {e}")
            
            if all_trade_days is None or len(all_trade_days) == 0:
                logger.error(f"无法获取交易日: {start_date} ~ {end_date} (MongoDB和JQData都失败)")
                return periods
            
            # 转换为字符串列表
            trade_days_str = [d.strftime('%Y-%m-%d') for d in all_trade_days]
            
            # 按周分组（自然周：周一到周日）
            weeks = []
            current_week = []
            current_weekday = None
            
            for date_str in trade_days_str:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                weekday = dt.weekday()  # 0=周一, 6=周日
                
                # 如果是周一或新的一周开始
                if weekday == 0 or (current_weekday is not None and weekday < current_weekday):
                    if current_week:
                        weeks.append(current_week)
                    current_week = [date_str]
                else:
                    current_week.append(date_str)
                
                current_weekday = weekday
            
            # 添加最后一周
            if current_week:
                weeks.append(current_week)
            
            if not weeks:
                logger.warning("无法生成周时间段")
                return periods
            
            if self.verbose:
                logger.info(f"共生成 {len(weeks)} 周，窗口大小: {window_weeks} 周")
            
            # 生成滚动窗口
            idx = 0
            max_start_idx = len(weeks) - window_weeks + 1
            if max_start_idx <= 0:
                logger.warning(f"周数不足: 总周数={len(weeks)}, 窗口大小={window_weeks}, 无法生成滚动窗口")
                return periods
            
            for i in range(0, max_start_idx, step_weeks):
                # 窗口内的所有周
                window_weeks_list = weeks[i:i + window_weeks]
                
                if not window_weeks_list:
                    continue
                
                # 窗口的开始和结束日期
                window_start = window_weeks_list[0][0]  # 第一周的第一个交易日
                window_end = window_weeks_list[-1][-1]  # 最后一周的最后一个交易日
                
                period = BacktestPeriod(
                    start_date=window_start,
                    end_date=window_end,
                    label=f"weekly_rolling_{idx}_W{i+1}",
                    description=f"按周滚动窗口 {idx+1} (第{i+1}周开始, {len(window_weeks_list)}周)"
                )
                
                # 识别市场环境（如果有识别器）
                if self._market_env_detector:
                    period.market_env = self._market_env_detector(
                        period.start_date, period.end_date
                    )
                
                periods.append(period)
                idx += 1
            
            if self.verbose:
                logger.info(f"生成了 {len(periods)} 个按周滚动时间段")
            
        except Exception as e:
            logger.error(f"生成按周滚动时间段失败: {e}")
            import traceback
            traceback.print_exc()
        
        return periods
    
    def generate_quarterly_periods(
        self,
        start_year: int,
        end_year: int
    ) -> List[BacktestPeriod]:
        """
        生成季度时间段
        
        Args:
            start_year: 开始年份
            end_year: 结束年份
        
        Returns:
            时间段列表
        """
        periods = []
        
        quarter_dates = [
            ("01-01", "03-31", "Q1"),
            ("04-01", "06-30", "Q2"),
            ("07-01", "09-30", "Q3"),
            ("10-01", "12-31", "Q4")
        ]
        
        for year in range(start_year, end_year + 1):
            for q_start, q_end, q_label in quarter_dates:
                period = BacktestPeriod(
                    start_date=f"{year}-{q_start}",
                    end_date=f"{year}-{q_end}",
                    label=f"{year}{q_label}",
                    description=f"{year}年{q_label}"
                )
                
                if self._market_env_detector:
                    period.market_env = self._market_env_detector(
                        period.start_date, period.end_date
                    )
                
                periods.append(period)
        
        return periods
    
    def generate_yearly_periods(
        self,
        start_year: int,
        end_year: int
    ) -> List[BacktestPeriod]:
        """
        生成年度时间段
        
        Args:
            start_year: 开始年份
            end_year: 结束年份
        
        Returns:
            时间段列表
        """
        periods = []
        
        for year in range(start_year, end_year + 1):
            period = BacktestPeriod(
                start_date=f"{year}-01-01",
                end_date=f"{year}-12-31",
                label=f"Y{year}",
                description=f"{year}年全年"
            )
            
            if self._market_env_detector:
                period.market_env = self._market_env_detector(
                    period.start_date, period.end_date
                )
            
            periods.append(period)
        
        return periods
    
    def generate_custom_periods(
        self,
        period_defs: List[Tuple[str, str, str]]
    ) -> List[BacktestPeriod]:
        """
        生成自定义时间段
        
        Args:
            period_defs: [(start_date, end_date, label), ...]
        
        Returns:
            时间段列表
        """
        periods = []
        
        for start_date, end_date, label in period_defs:
            period = BacktestPeriod(
                start_date=start_date,
                end_date=end_date,
                label=label,
                description=label
            )
            
            if self._market_env_detector:
                period.market_env = self._market_env_detector(
                    period.start_date, period.end_date
                )
            
            periods.append(period)
        
        return periods
    
    # ==================== 验证执行 ====================
    
    def _evaluate_result(self, result: ParallelBacktestResult) -> Tuple[Dict[str, bool], float]:
        """
        评估单个回测结果
        
        Args:
            result: 回测结果
        
        Returns:
            (passed_criteria, score)
        """
        passed = {}
        
        if not result.success:
            return {}, 0.0
        
        # 评估各指标
        passed["sharpe"] = result.sharpe_ratio >= self.criteria.min_sharpe
        passed["drawdown"] = abs(result.max_drawdown) <= self.criteria.max_drawdown
        passed["win_rate"] = result.win_rate >= self.criteria.min_win_rate
        passed["return"] = result.total_return >= self.criteria.min_total_return
        passed["trades"] = result.total_trades >= self.criteria.min_trades
        
        # 计算得分
        score = sum(1 for v in passed.values() if v) / len(passed) if passed else 0.0
        
        return passed, score
    
    def run_validation(
        self,
        periods: List[BacktestPeriod],
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0,
        preload_data: bool = True
    ) -> ValidationSummary:
        """
        运行批量验证
        
        Args:
            periods: 时间段列表
            strategy_config: 策略配置
            initial_capital: 初始资金
            preload_data: 是否预加载数据
        
        Returns:
            ValidationSummary
        """
        if strategy_config is None:
            strategy_config = StrategyConfig()
        
        summary = ValidationSummary()
        
        if self.verbose:
            print(f"\n{'='*70}")
            print(f"🔍 批量回测验证器 - 开始验证")
            print(f"{'='*70}")
            print(f"   时间段数: {len(periods)}")
            print(f"   初始资金: {initial_capital:,.0f}")
            print(f"   GPU加速: {'是' if self.use_gpu else '否'}")
            print(f"   验证标准:")
            print(f"      - 最低夏普比率: {self.criteria.min_sharpe}")
            print(f"      - 最大回撤: {self.criteria.max_drawdown:.1f}%")
            print(f"      - 最低胜率: {self.criteria.min_win_rate:.0%}")
            print(f"      - 最低收益率: {self.criteria.min_total_return:.0%}")
            print(f"      - 最少交易次数: {self.criteria.min_trades}")
        
        # 1. 预加载所有时间段的数据
        if preload_data:
            if self.verbose:
                print(f"\n📥 预加载数据...")
            
            for period in periods:
                self.runner.ensure_data_cached(
                    start_date=period.start_date,
                    end_date=period.end_date
                )
        
        # 2. 逐个执行回测和验证
        if self.verbose:
            print(f"\n🔄 执行回测...")
        
        for i, period in enumerate(periods):
            if self.verbose:
                print(f"\n   [{i+1}/{len(periods)}] {period.label}: {period.start_date} ~ {period.end_date}")
            
            # 执行回测
            backtest_result = self.runner.run_backtest_with_cache(
                start_date=period.start_date,
                end_date=period.end_date,
                strategy_config=strategy_config,
                initial_capital=initial_capital,
                task_id=f"validate_{period.label}"
            )
            
            # 评估结果
            passed_criteria, score = self._evaluate_result(backtest_result)
            
            validation_result = ValidationResult(
                period=period,
                backtest_result=backtest_result,
                passed_criteria=passed_criteria,
                score=score
            )
            
            summary.add_result(validation_result)
            
            if self.verbose:
                if backtest_result.success:
                    status = "✅ 通过" if score >= 0.6 else "⚠️ 未通过"
                    print(f"      收益: {backtest_result.total_return:.2f}%, "
                          f"夏普: {backtest_result.sharpe_ratio:.2f}, "
                          f"得分: {score:.2f} {status}")
                else:
                    print(f"      ❌ 回测失败: {backtest_result.error}")
        
        # 3. 保存结果
        self._save_validation_results(summary)
        
        # 4. 打印汇总
        if self.verbose:
            self._print_summary(summary)
        
        return summary
    
    def run_rolling_validation(
        self,
        start_date: str,
        end_date: str,
        window_months: int = 6,
        step_months: int = 1,
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0
    ) -> ValidationSummary:
        """
        运行滚动窗口验证
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            window_months: 窗口大小（月）
            step_months: 滚动步长（月）
            strategy_config: 策略配置
            initial_capital: 初始资金
        
        Returns:
            ValidationSummary
        """
        periods = self.generate_rolling_periods(
            start_date=start_date,
            end_date=end_date,
            window_months=window_months,
            step_months=step_months
        )
        
        return self.run_validation(
            periods=periods,
            strategy_config=strategy_config,
            initial_capital=initial_capital
        )
    
    def run_weekly_rolling_validation(
        self,
        start_date: str,
        end_date: str,
        window_weeks: int = 12,  # 3个月约12周
        step_weeks: int = 1,
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0
    ) -> ValidationSummary:
        """
        运行按周滚动窗口验证
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            window_weeks: 窗口大小（周）
            step_weeks: 滚动步长（周）
            strategy_config: 策略配置
            initial_capital: 初始资金
        
        Returns:
            ValidationSummary
        """
        periods = self.generate_weekly_rolling_periods(
            start_date=start_date,
            end_date=end_date,
            window_weeks=window_weeks,
            step_weeks=step_weeks
        )
        
        return self.run_validation(
            periods=periods,
            strategy_config=strategy_config,
            initial_capital=initial_capital
        )
    
    def run_quarterly_validation(
        self,
        start_year: int,
        end_year: int,
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0
    ) -> ValidationSummary:
        """
        运行季度验证
        
        Args:
            start_year: 开始年份
            end_year: 结束年份
            strategy_config: 策略配置
            initial_capital: 初始资金
        
        Returns:
            ValidationSummary
        """
        periods = self.generate_quarterly_periods(
            start_year=start_year,
            end_year=end_year
        )
        
        return self.run_validation(
            periods=periods,
            strategy_config=strategy_config,
            initial_capital=initial_capital
        )
    
    def run_yearly_validation(
        self,
        start_year: int,
        end_year: int,
        strategy_config: Optional[StrategyConfig] = None,
        initial_capital: float = 1000000.0
    ) -> ValidationSummary:
        """
        运行年度验证
        
        Args:
            start_year: 开始年份
            end_year: 结束年份
            strategy_config: 策略配置
            initial_capital: 初始资金
        
        Returns:
            ValidationSummary
        """
        periods = self.generate_yearly_periods(
            start_year=start_year,
            end_year=end_year
        )
        
        return self.run_validation(
            periods=periods,
            strategy_config=strategy_config,
            initial_capital=initial_capital
        )
    
    # ==================== 结果输出 ====================
    
    def _print_summary(self, summary: ValidationSummary):
        """打印验证汇总"""
        print(f"\n{'='*70}")
        print(f"📊 验证汇总")
        print(f"{'='*70}")
        
        print(f"\n📈 整体统计:")
        print(f"   总时间段数: {summary.total_periods}")
        if summary.total_periods > 0:
            print(f"   通过: {summary.passed_periods} ({summary.passed_periods/summary.total_periods*100:.1f}%)")
            print(f"   未通过: {summary.failed_periods}")
        else:
            print(f"   ⚠️  没有生成任何时间段，请检查日期范围")
            return
        
        print(f"\n📉 绩效统计:")
        print(f"   平均收益率: {summary.avg_return:.2f}%")  # avg_return已经是百分比形式(9.87表示9.87%)
        print(f"   平均夏普比率: {summary.avg_sharpe:.2f}")
        print(f"   平均最大回撤: {summary.avg_max_drawdown:.2f}%")  # max_drawdown已经是百分比形式(-1.60表示-1.60%)
        
        print(f"\n🎯 稳定性指标:")
        print(f"   一致性得分: {summary.consistency_score:.2f} (越高越稳定)")
        print(f"   稳定性得分: {summary.stability_score:.2f} (越高越稳定)")
        
        if summary.criteria_pass_rates:
            print(f"\n✅ 各指标通过率:")
            for criterion, rate in summary.criteria_pass_rates.items():
                print(f"   {criterion}: {rate:.1f}%")
        
        # 找出最好和最差的时间段
        successful_results = [r for r in summary.results if r.backtest_result.success]
        if successful_results:
            best = max(successful_results, key=lambda x: x.backtest_result.sharpe_ratio)
            worst = min(successful_results, key=lambda x: x.backtest_result.sharpe_ratio)
            
            print(f"\n🏆 最佳时间段:")
            print(f"   {best.period.label}: 收益 {best.backtest_result.total_return:.2f}%, "
                  f"夏普 {best.backtest_result.sharpe_ratio:.2f}")
            
            print(f"\n⚠️  最差时间段:")
            print(f"   {worst.period.label}: 收益 {worst.backtest_result.total_return:.2f}%, "
                  f"夏普 {worst.backtest_result.sharpe_ratio:.2f}")
    
    def _save_validation_results(self, summary: ValidationSummary):
        """保存验证结果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存JSON
        json_path = self.output_dir / f"validation_summary_{timestamp}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(summary.to_dict(), f, indent=2, ensure_ascii=False)
        
        if self.verbose:
            print(f"\n💾 验证结果已保存: {json_path}")
        
        # 保存CSV
        csv_path = self.output_dir / f"validation_results_{timestamp}.csv"
        df = summary.to_dataframe()
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        
        if self.verbose:
            print(f"   CSV: {csv_path}")
        
        # 生成HTML报告
        html_path = self._generate_html_report(summary, timestamp)
        if html_path and self.verbose:
            print(f"   HTML: {html_path}")
    
    def _generate_html_report(self, summary: ValidationSummary, timestamp: str) -> Optional[Path]:
        """生成HTML报告"""
        try:
            html_path = self.output_dir / f"validation_report_{timestamp}.html"
            
            df = summary.to_dataframe()
            
            # 构建HTML
            html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>批量回测验证报告 - {timestamp}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
        }}
        h1 {{
            color: #1a1a2e;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .card-value {{
            font-size: 2em;
            font-weight: bold;
            color: #16213e;
        }}
        .card-label {{
            color: #666;
            margin-top: 5px;
        }}
        .card.success {{
            background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        }}
        .card.warning {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        .card.warning .card-value, .card.warning .card-label {{
            color: white;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            font-size: 14px;
        }}
        th, td {{
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #e0e0e0;
        }}
        th {{
            background: #1a1a2e;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .pass {{
            color: #27ae60;
            font-weight: bold;
        }}
        .fail {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .positive {{
            color: #27ae60;
        }}
        .negative {{
            color: #e74c3c;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 批量回测验证报告</h1>
        
        <div class="summary-cards">
            <div class="card">
                <div class="card-value">{summary.total_periods}</div>
                <div class="card-label">总时间段数</div>
            </div>
            <div class="card success">
                <div class="card-value">{summary.passed_periods}</div>
                <div class="card-label">通过数</div>
            </div>
            <div class="card {'warning' if summary.failed_periods > 0 else ''}">
                <div class="card-value">{summary.failed_periods}</div>
                <div class="card-label">未通过数</div>
            </div>
            <div class="card">
                <div class="card-value">{summary.avg_return:.1f}%</div>
                <div class="card-label">平均收益率</div>
            </div>
            <div class="card">
                <div class="card-value">{summary.avg_sharpe:.2f}</div>
                <div class="card-label">平均夏普比率</div>
            </div>
            <div class="card">
                <div class="card-value">{summary.avg_max_drawdown:.1f}%</div>
                <div class="card-label">平均最大回撤</div>
            </div>
            <div class="card">
                <div class="card-value">{summary.consistency_score:.2f}</div>
                <div class="card-label">一致性得分</div>
            </div>
            <div class="card">
                <div class="card-value">{summary.stability_score:.2f}</div>
                <div class="card-label">稳定性得分</div>
            </div>
        </div>
        
        <h2>📈 详细结果</h2>
        <table>
            <thead>
                <tr>
                    <th>时间段</th>
                    <th>开始日期</th>
                    <th>结束日期</th>
                    <th>天数</th>
                    <th>总收益率</th>
                    <th>年化收益</th>
                    <th>夏普比率</th>
                    <th>最大回撤</th>
                    <th>胜率</th>
                    <th>交易次数</th>
                    <th>得分</th>
                    <th>结果</th>
                </tr>
            </thead>
            <tbody>
"""
            
            for _, row in df.iterrows():
                return_class = "positive" if row['总收益率(%)'] > 0 else "negative"
                pass_class = "pass" if row['是否通过'] == "是" else "fail"
                
                html_content += f"""
                <tr>
                    <td>{row['时间段']}</td>
                    <td>{row['开始日期']}</td>
                    <td>{row['结束日期']}</td>
                    <td>{row['天数']}</td>
                    <td class="{return_class}">{row['总收益率(%)']:.2f}%</td>
                    <td class="{return_class}">{row['年化收益(%)']:.2f}%</td>
                    <td>{row['夏普比率']:.2f}</td>
                    <td>{row['最大回撤(%)']:.2f}%</td>
                    <td>{row['胜率(%)']:.2f}%</td>
                    <td>{row['交易次数']}</td>
                    <td>{row['验证得分']:.2f}</td>
                    <td class="{pass_class}">{row['是否通过']}</td>
                </tr>
"""
            
            html_content += f"""
            </tbody>
        </table>
        
        <div class="footer">
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>Investment Advisor V4.0 - 批量回测验证器</p>
        </div>
    </div>
</body>
</html>
"""
            
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            return html_path
        
        except Exception as e:
            logger.error(f"生成HTML报告失败: {e}")
            return None


# ==================== 便捷函数 ====================

def run_quick_validation(
    start_date: str = "2024-01-01",
    end_date: str = "2024-12-31",
    window_months: int = 3,
    step_months: int = 1,
    cache_dir: str = "data/cache",
    output_dir: str = "output/advisor_v4/batch_validation"
) -> ValidationSummary:
    """
    快速运行滚动窗口验证
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        window_months: 窗口大小（月）
        step_months: 滚动步长（月）
        cache_dir: 缓存目录
        output_dir: 输出目录
    
    Returns:
        ValidationSummary
    """
    validator = BatchBacktestValidator(
        cache_dir=cache_dir,
        output_dir=output_dir,
        use_gpu=True,
        max_workers=3,
        verbose=True
    )
    
    return validator.run_rolling_validation(
        start_date=start_date,
        end_date=end_date,
        window_months=window_months,
        step_months=step_months
    )


if __name__ == "__main__":
    # 测试
    summary = run_quick_validation(
        start_date="2024-01-01",
        end_date="2024-12-31",
        window_months=3,
        step_months=1
    )
    
    print(f"\n验证完成!")
    if summary.total_periods > 0:
        print(f"  通过率: {summary.passed_periods / summary.total_periods * 100:.1f}%")
    else:
        print(f"  ⚠️  没有生成任何时间段")
