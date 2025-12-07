"""回测模块

基于 BulletTrade 的策略回测执行和结果处理
"""

from .backtest_config import BacktestConfig, BacktestFrequency
from .bt_run import BacktestRunner, run_backtest
from .backtest_result import BacktestResult, BacktestMetrics

__all__ = [
    "BacktestConfig",
    "BacktestFrequency",
    "BacktestRunner",
    "run_backtest",
    "BacktestResult",
    "BacktestMetrics",
]



