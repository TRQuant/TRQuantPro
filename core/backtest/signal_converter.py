# -*- coding: utf-8 -*-
"""
策略信号转换器
=============
将策略参数转换为可用于向量化回测的信号矩阵
"""

import logging
from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class StrategyParams:
    """策略参数"""
    strategy_type: str = "momentum"  # momentum, value, trend, multi_factor
    # 动量参数
    momentum_short: int = 5
    momentum_long: int = 20
    # 通用参数
    max_stocks: int = 10
    rebalance_days: int = 5
    # 风控参数
    stop_loss: float = 0.08
    take_profit: float = 0.20


class SignalConverter:
    """
    信号转换器
    
    将策略逻辑转换为信号矩阵，供向量化回测使用
    """
    
    def __init__(self):
        self._converters = {
            "momentum": self._momentum_signals,
            "value": self._value_signals,
            "trend": self._trend_signals,
            "multi_factor": self._multi_factor_signals
        }
    
    def convert(self, 
                price_data: pd.DataFrame,
                params: StrategyParams) -> pd.DataFrame:
        """
        转换为信号矩阵
        
        Args:
            price_data: 价格数据（pivot格式，index=日期，columns=股票）
            params: 策略参数
            
        Returns:
            信号矩阵（index=日期，columns=股票，values=权重0-1）
        """
        converter = self._converters.get(params.strategy_type, self._momentum_signals)
        return converter(price_data, params)
    
    def _momentum_signals(self, price_data: pd.DataFrame, params: StrategyParams) -> pd.DataFrame:
        """动量策略信号"""
        # 计算动量
        mom_short = price_data.pct_change(params.momentum_short)
        mom_long = price_data.pct_change(params.momentum_long)
        
        # 综合得分
        score = 0.5 * mom_short + 0.5 * mom_long
        
        # 生成信号
        signals = pd.DataFrame(0.0, index=price_data.index, columns=price_data.columns)
        
        for i, date in enumerate(price_data.index):
            if i < params.momentum_long:
                continue
            
            # 是否是调仓日
            if i % params.rebalance_days != 0:
                # 保持前一天的信号
                if i > 0:
                    signals.iloc[i] = signals.iloc[i-1]
                continue
            
            # 选股
            row_score = score.iloc[i].dropna()
            # 只选正动量的
            positive_score = row_score[row_score > 0]
            
            if len(positive_score) >= params.max_stocks:
                top_stocks = positive_score.nlargest(params.max_stocks).index
            elif len(positive_score) > 0:
                top_stocks = positive_score.index
            else:
                # 没有正动量股票，选得分最高的
                top_stocks = row_score.nlargest(params.max_stocks).index
            
            # 等权分配
            weight = 1.0 / len(top_stocks) if len(top_stocks) > 0 else 0
            signals.loc[date, top_stocks] = weight
        
        return signals
    
    def _trend_signals(self, price_data: pd.DataFrame, params: StrategyParams) -> pd.DataFrame:
        """趋势策略信号"""
        fast_ma = price_data.rolling(5).mean()
        slow_ma = price_data.rolling(20).mean()
        
        # 金叉信号
        trend_up = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
        
        signals = pd.DataFrame(0.0, index=price_data.index, columns=price_data.columns)
        
        for i, date in enumerate(price_data.index):
            if i < 20:
                continue
            
            if i % params.rebalance_days != 0:
                if i > 0:
                    signals.iloc[i] = signals.iloc[i-1]
                continue
            
            # 选择趋势向上的股票
            up_stocks = price_data.columns[fast_ma.iloc[i] > slow_ma.iloc[i]]
            
            if len(up_stocks) > params.max_stocks:
                # 按动量排序
                mom = price_data.pct_change(params.momentum_short).iloc[i]
                up_stocks = mom[up_stocks].nlargest(params.max_stocks).index
            
            weight = 1.0 / len(up_stocks) if len(up_stocks) > 0 else 0
            for stock in up_stocks:
                signals.loc[date, stock] = weight
        
        return signals
    
    def _value_signals(self, price_data: pd.DataFrame, params: StrategyParams) -> pd.DataFrame:
        """价值策略信号（简化版：用价格低位代替PE）"""
        # 计算52周相对位置
        rolling_high = price_data.rolling(252, min_periods=20).max()
        rolling_low = price_data.rolling(252, min_periods=20).min()
        relative_pos = (price_data - rolling_low) / (rolling_high - rolling_low + 1e-10)
        
        signals = pd.DataFrame(0.0, index=price_data.index, columns=price_data.columns)
        
        for i, date in enumerate(price_data.index):
            if i < 20:
                continue
            
            if i % params.rebalance_days != 0:
                if i > 0:
                    signals.iloc[i] = signals.iloc[i-1]
                continue
            
            # 选择相对位置低的（价值股）
            pos = relative_pos.iloc[i].dropna()
            low_stocks = pos.nsmallest(params.max_stocks).index
            
            weight = 1.0 / len(low_stocks) if len(low_stocks) > 0 else 0
            signals.loc[date, low_stocks] = weight
        
        return signals
    
    def _multi_factor_signals(self, price_data: pd.DataFrame, params: StrategyParams) -> pd.DataFrame:
        """多因子策略信号"""
        # 动量因子
        mom = price_data.pct_change(params.momentum_long)
        
        # 波动因子（低波动优先）
        vol = price_data.pct_change().rolling(20).std()
        
        # 综合得分（动量正向，波动负向）
        mom_rank = mom.rank(axis=1, pct=True)
        vol_rank = vol.rank(axis=1, pct=True, ascending=False)  # 低波动高分
        
        score = 0.6 * mom_rank + 0.4 * vol_rank
        
        signals = pd.DataFrame(0.0, index=price_data.index, columns=price_data.columns)
        
        for i, date in enumerate(price_data.index):
            if i < params.momentum_long + 5:
                continue
            
            if i % params.rebalance_days != 0:
                if i > 0:
                    signals.iloc[i] = signals.iloc[i-1]
                continue
            
            row_score = score.iloc[i].dropna()
            top_stocks = row_score.nlargest(params.max_stocks).index
            
            weight = 1.0 / len(top_stocks) if len(top_stocks) > 0 else 0
            signals.loc[date, top_stocks] = weight
        
        return signals


def convert_strategy_to_signals(price_data: pd.DataFrame,
                                strategy_type: str = "momentum",
                                **kwargs) -> pd.DataFrame:
    """
    快捷函数：将策略转换为信号
    
    Args:
        price_data: 价格数据（pivot格式）
        strategy_type: 策略类型
        **kwargs: 策略参数
        
    Returns:
        信号矩阵
    """
    params = StrategyParams(strategy_type=strategy_type, **kwargs)
    converter = SignalConverter()
    return converter.convert(price_data, params)
