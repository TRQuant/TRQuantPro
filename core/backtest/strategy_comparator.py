# -*- coding: utf-8 -*-
"""
策略对比器
=========
批量回测多个策略并对比结果
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
import pandas as pd
import time

logger = logging.getLogger(__name__)


@dataclass
class ComparisonResult:
    """对比结果"""
    strategy_name: str
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    duration_seconds: float


class StrategyComparator:
    """策略对比器"""
    
    def __init__(self):
        self.results: List[ComparisonResult] = []
    
    def compare_strategies(self,
                          securities: List[str],
                          start_date: str,
                          end_date: str,
                          strategies: List[str] = None,
                          use_mock: bool = True) -> pd.DataFrame:
        """
        对比多个策略
        
        Args:
            securities: 股票列表
            start_date: 开始日期
            end_date: 结束日期
            strategies: 策略名称列表，默认所有
            use_mock: 使用模拟数据
            
        Returns:
            DataFrame: 对比结果表
        """
        from core.backtest.fast_backtest_engine import quick_backtest
        from core.templates import list_all_templates
        
        if strategies is None:
            strategies = list_all_templates()
        
        self.results = []
        
        for strategy_name in strategies:
            logger.info(f"回测策略: {strategy_name}")
            start_time = time.time()
            
            try:
                result = quick_backtest(
                    securities=securities,
                    start_date=start_date,
                    end_date=end_date,
                    strategy=strategy_name,
                    use_mock=use_mock
                )
                
                comparison = ComparisonResult(
                    strategy_name=strategy_name,
                    total_return=result.total_return,
                    annual_return=result.annual_return,
                    sharpe_ratio=result.sharpe_ratio,
                    max_drawdown=result.max_drawdown,
                    win_rate=result.win_rate,
                    total_trades=result.total_trades,
                    duration_seconds=time.time() - start_time
                )
                self.results.append(comparison)
                
            except Exception as e:
                logger.warning(f"策略 {strategy_name} 回测失败: {e}")
                self.results.append(ComparisonResult(
                    strategy_name=strategy_name,
                    total_return=0,
                    annual_return=0,
                    sharpe_ratio=0,
                    max_drawdown=0,
                    win_rate=0,
                    total_trades=0,
                    duration_seconds=time.time() - start_time
                ))
        
        return self.to_dataframe()
    
    def to_dataframe(self) -> pd.DataFrame:
        """转换为DataFrame"""
        if not self.results:
            return pd.DataFrame()
        
        data = []
        for r in self.results:
            data.append({
                "策略": r.strategy_name,
                "总收益": f"{r.total_return*100:.2f}%",
                "年化收益": f"{r.annual_return*100:.2f}%",
                "夏普比率": f"{r.sharpe_ratio:.2f}",
                "最大回撤": f"{r.max_drawdown*100:.2f}%",
                "胜率": f"{r.win_rate*100:.1f}%",
                "交易次数": r.total_trades,
                "耗时(s)": f"{r.duration_seconds:.2f}"
            })
        
        df = pd.DataFrame(data)
        return df
    
    def rank_by(self, metric: str = "sharpe_ratio") -> pd.DataFrame:
        """按指标排名"""
        if not self.results:
            return pd.DataFrame()
        
        sorted_results = sorted(
            self.results,
            key=lambda x: getattr(x, metric, 0),
            reverse=True
        )
        
        data = []
        for i, r in enumerate(sorted_results, 1):
            data.append({
                "排名": i,
                "策略": r.strategy_name,
                metric: getattr(r, metric, 0),
                "总收益": f"{r.total_return*100:.2f}%"
            })
        
        return pd.DataFrame(data)
    
    def get_best_strategy(self, metric: str = "sharpe_ratio") -> str:
        """获取最佳策略"""
        if not self.results:
            return ""
        
        best = max(self.results, key=lambda x: getattr(x, metric, 0))
        return best.strategy_name


def compare_all_strategies(securities: List[str],
                          start_date: str,
                          end_date: str,
                          use_mock: bool = True) -> pd.DataFrame:
    """
    对比所有策略的快捷函数
    """
    comparator = StrategyComparator()
    return comparator.compare_strategies(
        securities=securities,
        start_date=start_date,
        end_date=end_date,
        use_mock=use_mock
    )
