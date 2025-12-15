# -*- coding: utf-8 -*-
"""
回测模块
========
提供三层回测架构：
1. 快速验证层 (Fast) - 向量化回测
2. 标准回测层 (Standard) - 事件驱动
3. 精确回测层 (Precise) - BulletTrade/QMT

使用方式：
    from core.backtest import UnifiedBacktestManager, quick_backtest
    
    # 快速回测
    result = quick_backtest(
        securities=["000001.XSHE", "600000.XSHG"],
        start_date="2024-01-01",
        end_date="2024-03-01",
        strategy="momentum"
    )
    print(result.summary())
"""

# 统一回测管理器
from core.backtest.unified_backtest_manager import (
    UnifiedBacktestManager,
    UnifiedBacktestConfig,
    UnifiedBacktestResult,
    BacktestLevel,
    DataFrequency,
    BacktestEngine,
    BaseStrategy,
    MomentumStrategy,
    MeanReversionStrategy,
    quick_backtest,
)

# 快速回测引擎
from core.backtest.fast_backtest_engine import (
    FastBacktestEngine,
    BacktestConfig,
    BacktestResult,
    quick_backtest as fast_quick_backtest,
)

# 事件引擎
from core.backtest.event_engine import (
    EventEngine,
    EventType,
    Event,
    BarData,
    OrderData,
    TradeData,
    PositionData,
)

# 批量回测
from core.backtest.batch_backtest_manager import BatchBacktestManager

# 信号转换
from core.backtest.signal_converter import convert_strategy_to_signals

# 策略比较
from core.backtest.strategy_comparator import StrategyComparator

__all__ = [
    # 统一管理器
    "UnifiedBacktestManager",
    "UnifiedBacktestConfig",
    "UnifiedBacktestResult",
    "BacktestLevel",
    "DataFrequency",
    "BacktestEngine",
    "BaseStrategy",
    "MomentumStrategy",
    "MeanReversionStrategy",
    "quick_backtest",
    # 快速引擎
    "FastBacktestEngine",
    "BacktestConfig",
    "BacktestResult",
    "fast_quick_backtest",
    # 事件引擎
    "EventEngine",
    "EventType",
    "Event",
    "BarData",
    "OrderData",
    "TradeData",
    "PositionData",
    # 批量回测
    "BatchBacktestManager",
    # 工具
    "convert_strategy_to_signals",
    "StrategyComparator",
]
