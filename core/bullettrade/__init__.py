# -*- coding: utf-8 -*-
"""
BulletTrade 深度集成模块

提供BulletTrade回测引擎的Python API封装，支持:
- Python API调用（而非命令行）
- MCP服务器集成
- 工作流自动化
- 批量回测
- 参数优化
- 结果持久化

使用示例:
    from core.bullettrade import BulletTradeEngine, BTConfig, BTResult

    # 创建配置
    config = BTConfig(
        start_date="2024-01-01",
        end_date="2024-12-31",
        initial_capital=1000000,
        data_provider="jqdata"
    )

    # 创建引擎
    engine = BulletTradeEngine(config)

    # 执行回测
    result = engine.run_backtest(
        strategy_path="strategies/bullettrade/my_strategy.py"
    )

    # 获取结果
    print(f"总收益率: {result.total_return:.2f}%")
    print(f"夏普比率: {result.sharpe_ratio:.2f}")
"""

from .config import BTConfig, BTOptimizeConfig
from .result import BTResult, BTOptimizeResult
from .engine import BulletTradeEngine, run_backtest_simple

__all__ = [
    # 配置类
    "BTConfig",
    "BTOptimizeConfig",
    # 结果类
    "BTResult",
    "BTOptimizeResult",
    # 引擎类
    "BulletTradeEngine",
    # 便捷函数
    "run_backtest_simple",
]

__version__ = "1.0.0"

