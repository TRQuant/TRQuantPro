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

# 新增模块
from .optimizer import (
    StrategyOptimizer,
    OptimizeConfig,
    OptimizeParam,
    OptimizeResult,
    optimize_strategy,
)
from .reporter import (
    ReportGenerator,
    ReportConfig,
    ReportResult,
    generate_report,
)
from .live_engine import (
    LiveTradingEngine,
    LiveEngineConfig,
    LiveEngineStatus,
    BrokerType as LiveBrokerType,
    QMTServerManager,
    Position,
    Trade,
    AccountInfo,
)
from .risk_control import (
    RiskControlEngine,
    RiskConfig,
    RiskEvent,
    RiskStatus,
    RiskLevel,
    RiskAction,
    create_default_risk_config,
)
from .snapshot_manager import (
    SnapshotManager,
    DailySnapshot,
    PositionRecord,
    TradeRecord,
    create_snapshot,
)
from .ai_daily_report import (
    AIReportGenerator,
    DailyReportData,
)

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
    # 参数优化
    "StrategyOptimizer",
    "OptimizeConfig",
    "OptimizeParam",
    "OptimizeResult",
    "optimize_strategy",
    # 报告生成
    "ReportGenerator",
    "ReportConfig",
    "ReportResult",
    "generate_report",
    # 实盘交易
    "LiveTradingEngine",
    "LiveEngineConfig",
    "LiveEngineStatus",
    "LiveBrokerType",
    "QMTServerManager",
    "Position",
    "Trade",
    "AccountInfo",
    # 风控
    "RiskControlEngine",
    "RiskConfig",
    "RiskEvent",
    "RiskStatus",
    "RiskLevel",
    "RiskAction",
    "create_default_risk_config",
    # 快照管理
    "SnapshotManager",
    "DailySnapshot",
    "PositionRecord",
    "TradeRecord",
    "create_snapshot",
    # AI日报
    "AIReportGenerator",
    "DailyReportData",
]

