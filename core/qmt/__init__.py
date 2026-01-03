# -*- coding: utf-8 -*-
"""
QMT模块
=======
提供QMT/xtquant回测和交易接口

使用方式：
    from core.qmt import QMTEngine, QMTConfig, run_qmt_backtest
    
    result = run_qmt_backtest(
        strategy_code=my_strategy,
        start_date="2024-01-01",
        end_date="2024-03-01",
        stock_pool=["000001.SZ", "600000.SH"]
    )
"""

from core.qmt.config import QMTConfig, QMTOptimizeConfig
from core.qmt.result import QMTResult, QMTOptimizeResult
from core.qmt.engine import QMTEngine
from core.qmt.backtest_workflow import (
    QMTBacktestWorkflow,
    QMTBacktestConfig,
    QMTBacktestResult,
    QMTDataPeriod,
    QMTOrderType,
    run_qmt_backtest,
)

__all__ = [
    # 配置
    "QMTConfig",
    "QMTOptimizeConfig",
    "QMTBacktestConfig",
    # 结果
    "QMTResult",
    "QMTOptimizeResult",
    "QMTBacktestResult",
    # 引擎
    "QMTEngine",
    "QMTBacktestWorkflow",
    # 枚举
    "QMTDataPeriod",
    "QMTOrderType",
    # 便捷函数
    "run_qmt_backtest",
]
