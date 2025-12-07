"""BulletTrade 集成模块

基于 BulletTrade 框架实现策略回测验证与实盘交易部署
兼容聚宽 (JoinQuant) API，支持策略无缝迁移

官方网站: https://bullettrade.cn/

四步从准备到实盘:
1. 安装: pip install bullet-trade
2. 研究: bullet-trade lab
3. 回测: bullet-trade backtest strategy.py --start 2025-01-01 --end 2025-06-01
4. 实盘: bullet-trade live strategy.py --broker qmt
"""

from .bt_engine import BulletTradeEngine, BTConfig, BrokerType, BTMode
from .config import (
    BulletTradeConfig,
    setup_bullet_trade_env,
    check_bullet_trade_installation,
)
from .jqdata_compat import (
    JQDataCompat,
    Context,
    Portfolio,
    order,
    order_value,
    order_target,
    order_target_value,
    get_price,
    history,
    attribute_history,
    set_benchmark,
    set_commission,
    set_slippage,
    run_daily,
)
from .data_provider_adapter import DataProviderAdapter, DataProviderType

__all__ = [
    # 引擎
    "BulletTradeEngine",
    "BTConfig",
    "BrokerType",
    "BTMode",
    # 配置
    "BulletTradeConfig",
    "setup_bullet_trade_env",
    "check_bullet_trade_installation",
    # 聚宽API兼容
    "JQDataCompat",
    "Context",
    "Portfolio",
    "order",
    "order_value",
    "order_target",
    "order_target_value",
    "get_price",
    "history",
    "attribute_history",
    "set_benchmark",
    "set_commission",
    "set_slippage",
    "run_daily",
    # 数据适配器
    "DataProviderAdapter",
    "DataProviderType",
]

