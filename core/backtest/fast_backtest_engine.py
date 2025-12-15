# -*- coding: utf-8 -*-
"""
快速回测引擎（增强版）
===================
基于向量化计算，支持模拟数据和真实数据
目标：5秒内完成1周回测
"""

import logging
from typing import List, Dict, Optional, Callable
from datetime import datetime
import pandas as pd
import numpy as np
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)


@dataclass
class BacktestConfig:
    """回测配置"""
    start_date: str
    end_date: str
    initial_capital: float = 1000000.0
    commission_rate: float = 0.0003
    stamp_tax: float = 0.001
    slippage: float = 0.001
    benchmark: str = "000300.XSHG"
    max_positions: int = 10
    single_position_limit: float = 0.2


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    daily_returns: Optional[pd.Series] = None
    duration_seconds: float = 0.0


class FastBacktestEngine:
    """快速回测引擎"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self._price_pivot: Optional[pd.DataFrame] = None
        self._returns_data: Optional[pd.DataFrame] = None
        self._progress_callback: Optional[Callable] = None
    
    def set_progress_callback(self, callback: Callable[[float, str], None]):
        self._progress_callback = callback
    
    def _report_progress(self, progress: float, message: str):
        if self._progress_callback:
            self._progress_callback(progress, message)
        logger.debug(f"[{progress*100:.0f}%] {message}")
    
    def load_data(self, securities: List[str], use_mock: bool = True) -> bool:
        """加载数据"""
        self._report_progress(0.1, "加载数据...")
        
        try:
            from core.data.unified_data_provider import get_data_provider, DataRequest
            provider = get_data_provider(use_mock=use_mock)
            
            request = DataRequest(
                securities=securities,
                start_date=self.config.start_date,
                end_date=self.config.end_date,
                frequency="daily",
                fields=["close"],
                use_mock=use_mock
            )
            response = provider.get_data(request)
            
            if not response.success or response.data is None:
                logger.error(f"数据加载失败: {response.error}")
                return False
            
            # 转换为pivot格式
            data = response.data
            if "time" in data.columns and "code" in data.columns:
                self._price_pivot = data.pivot(index="time", columns="code", values="close")
            else:
                self._price_pivot = data
            
            # 计算收益率
            self._returns_data = self._price_pivot.pct_change()
            
            self._report_progress(0.3, f"数据加载完成，{len(self._price_pivot)}天，{len(self._price_pivot.columns)}只股票")
            return True
            
        except Exception as e:
            logger.error(f"数据加载异常: {e}")
            return False
    
    def run(self, signals: pd.DataFrame) -> BacktestResult:
        """运行向量化回测"""
        start_time = time.time()
        self._report_progress(0.4, "开始回测...")
        
        result = BacktestResult()
        
        try:
            if self._returns_data is None:
                logger.error("请先load_data")
                return result
            
            # 对齐数据
            common_dates = signals.index.intersection(self._returns_data.index)
            common_stocks = signals.columns.intersection(self._returns_data.columns)
            
            if len(common_dates) == 0:
                logger.error("信号和收益率无重叠日期")
                return result
            
            signals_aligned = signals.loc[common_dates, common_stocks]
            returns_aligned = self._returns_data.loc[common_dates, common_stocks]
            
            self._report_progress(0.5, f"回测 {len(common_dates)}天 x {len(common_stocks)}股票")
            
            # 向量化计算
            # 使用前一天的信号计算今天的收益
            portfolio_returns = (signals_aligned.shift(1) * returns_aligned).sum(axis=1)
            
            # 交易成本
            turnover = signals_aligned.diff().abs().sum(axis=1) / 2
            cost = turnover * (self.config.commission_rate + self.config.slippage)
            portfolio_returns = portfolio_returns - cost
            
            # 去除NaN
            portfolio_returns = portfolio_returns.dropna()
            
            if len(portfolio_returns) == 0:
                logger.error("计算收益为空")
                return result
            
            self._report_progress(0.7, "计算绩效指标...")
            
            # 绩效指标
            cumulative = (1 + portfolio_returns).cumprod()
            result.total_return = float(cumulative.iloc[-1] - 1)
            
            days = len(portfolio_returns)
            result.annual_return = float((1 + result.total_return) ** (252 / max(days, 1)) - 1)
            
            std = portfolio_returns.std()
            if std > 0:
                result.sharpe_ratio = float(portfolio_returns.mean() / std * np.sqrt(252))
            
            running_max = cumulative.cummax()
            drawdown = (cumulative - running_max) / running_max
            result.max_drawdown = float(drawdown.min())
            
            result.win_rate = float((portfolio_returns > 0).sum() / max(len(portfolio_returns), 1))
            result.total_trades = int(turnover.sum() * len(common_stocks))
            result.daily_returns = portfolio_returns
            result.duration_seconds = time.time() - start_time
            
            self._report_progress(1.0, f"回测完成，耗时{result.duration_seconds:.2f}秒")
            
        except Exception as e:
            logger.error(f"回测异常: {e}")
            result.duration_seconds = time.time() - start_time
        
        return result
    
    def get_price_pivot(self) -> Optional[pd.DataFrame]:
        """获取价格pivot数据（用于信号生成）"""
        return self._price_pivot


def quick_backtest(securities: List[str],
                   start_date: str,
                   end_date: str,
                   strategy: str = "momentum",
                   use_mock: bool = True,
                   **kwargs) -> BacktestResult:
    """
    快速回测入口
    
    Args:
        securities: 股票列表
        start_date: 开始日期
        end_date: 结束日期
        strategy: 策略类型
        use_mock: 使用模拟数据
        **kwargs: 策略参数
        
    Returns:
        回测结果
    """
    config = BacktestConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=kwargs.get("initial_capital", 1000000),
        max_positions=kwargs.get("max_stocks", 10)
    )
    
    engine = FastBacktestEngine(config)
    
    # 加载数据
    if not engine.load_data(securities, use_mock=use_mock):
        return BacktestResult()
    
    # 获取价格数据
    price_pivot = engine.get_price_pivot()
    if price_pivot is None or price_pivot.empty:
        return BacktestResult()
    
    # 生成信号
    from core.backtest.signal_converter import convert_strategy_to_signals
    signals = convert_strategy_to_signals(
        price_pivot,
        strategy_type=strategy,
        momentum_short=kwargs.get("mom_short", 5),
        momentum_long=kwargs.get("mom_long", 20),
        max_stocks=kwargs.get("max_stocks", 10),
        rebalance_days=kwargs.get("rebalance_days", 5)
    )
    
    # 运行回测
    return engine.run(signals)
