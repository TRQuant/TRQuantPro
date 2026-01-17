# -*- coding: utf-8 -*-
"""
TRQuant Research Module
=======================

研究模块：向量化回测、因子计算、信号生成

子模块：
- data_provider: 统一数据提供器（缓存+标准化矩阵输出）
- factors: 因子计算（JQData因子库 + GPU自定义）
- signals: 信号引擎（向量化选股条件）
- vbt_backtest: vectorbt回测封装
"""

from .data_provider import ResearchDataProvider, DataMatrices
from .factors import FactorCalculator, FactorMatrices
from .signals import SignalEngine, SignalParams, SignalMatrices
from .vbt_backtest import (
    VBTBacktest,
    BacktestResult,
    PositionTracker,
    calculate_composite_score,
    run_vbt_backtest,
)

__all__ = [
    # 数据层
    "ResearchDataProvider",
    "DataMatrices",
    # 因子层
    "FactorCalculator",
    "FactorMatrices",
    # 信号层
    "SignalEngine",
    "SignalParams",
    "SignalMatrices",
    # 回测层
    "VBTBacktest",
    "BacktestResult",
    "PositionTracker",
    "calculate_composite_score",
    "run_vbt_backtest",
]
