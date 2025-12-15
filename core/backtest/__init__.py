"""快速回测模块"""
from .fast_backtest_engine import FastBacktestEngine, BacktestConfig, BacktestResult, quick_backtest
from .batch_backtest_manager import BatchBacktestManager, StrategyConfig, BatchBacktestResult
from .signal_converter import SignalConverter, StrategyParams, convert_strategy_to_signals
from .strategy_comparator import StrategyComparator, ComparisonResult, compare_all_strategies
