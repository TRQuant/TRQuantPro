"""
MCP服务器工具模块
"""

from .performance import (
    MCPCache,
    get_cache,
    cached,
    get_monitor,
    PerformanceMonitor
)

from .redis_cache import (
    RedisCache,
    get_redis_cache
)

from .workflow_storage import (
    WorkflowStorage
)

from .system_registry import (
    SystemRegistry,
    get_registry
)

from .enhancements import (
    retry_on_failure,
    with_timeout,
    track_detailed,
    get_metrics,
    get_warmer,
    CacheWarmer,
    PerformanceMetrics
)

# M1工具
try:
    from .workflow_context import get_context, clear_context, WorkflowContext
    from .data_snapshot import get_snapshot_manager, DataSnapshot
    from .experiment import get_experiment_tracker, ExperimentConfig, ExperimentMetrics
    from .m1_tools import M1_TOOLS, call_m1_tool, get_m1_tool_names
except ImportError:
    M1_TOOLS = []

# M3.1工具
try:
    from .rawdoc import get_rawdoc_store, create_doc, RawDoc
    from .event_extractor import get_event_extractor, Event, EventType
    from .m31_tools import M31_TOOLS, call_m31_tool, get_m31_tool_names
except ImportError:
    M31_TOOLS = []

# M3.2工具
try:
    from .stage_machine import get_stage_machine, Stage, StageRecord
    from .scorecard import get_scorecard_engine, ScoreCard
    from .m32_tools import M32_TOOLS, call_m32_tool, get_m32_tool_names
except ImportError:
    M32_TOOLS = []

# M3.3工具
try:
    from .candidate_pool import get_candidate_pool, LayeredCandidatePool, PoolLevel, FilterCriteria
    from .industry_chain import get_industry_chain, IndustryChainGraph
    from .m33_tools import M33_TOOLS, M33_HANDLERS
except ImportError:
    M33_TOOLS = []
    M33_HANDLERS = {}

__all__ = [
    # Performance
    "MCPCache", "get_cache", "cached", "get_monitor", "PerformanceMonitor",
    # Redis
    "RedisCache", "get_redis_cache",
    # Workflow
    "WorkflowStorage",
    # Registry
    "SystemRegistry", "get_registry",
    # Enhancements
    "retry_on_failure", "with_timeout", "track_detailed",
    "get_metrics", "get_warmer", "CacheWarmer", "PerformanceMetrics",
    # M1
    "M1_TOOLS", "call_m1_tool", "get_m1_tool_names",
    # M3.1
    "M31_TOOLS", "call_m31_tool", "get_m31_tool_names",
    # M3.2
    "M32_TOOLS", "call_m32_tool", "get_m32_tool_names",
    # M3.3
    "M33_TOOLS", "M33_HANDLERS",
    "get_candidate_pool", "LayeredCandidatePool", "PoolLevel", "FilterCriteria",
    "get_industry_chain", "IndustryChainGraph",
]

# Strategy Pack工具
try:
    from .strategy_pack import (
        get_strategy_registry, StrategyRegistry,
        BaseStrategy, StrategyConfig, StrategyType, StrategyStatus,
        FactorStrategy, TenbaggerStrategy, MomentumStrategy
    )
    from .strategy_tools import STRATEGY_TOOLS, STRATEGY_HANDLERS
except ImportError:
    STRATEGY_TOOLS = []
    STRATEGY_HANDLERS = {}

# 更新导出
__all__.extend([
    "get_strategy_registry", "StrategyRegistry",
    "BaseStrategy", "StrategyConfig", "StrategyType", "StrategyStatus",
    "STRATEGY_TOOLS", "STRATEGY_HANDLERS"
])

# Tier2 AltData工具
try:
    from .altdata_tier2 import (
        get_bid_store, get_job_store, get_signal_generator,
        BidDataStore, JobDataStore, Tier2SignalGenerator,
        BidRecord, JobRecord, TrendSignal
    )
    from .altdata_tools import ALTDATA_TOOLS, ALTDATA_HANDLERS
except ImportError:
    ALTDATA_TOOLS = []
    ALTDATA_HANDLERS = {}

__all__.extend([
    "get_bid_store", "get_job_store", "get_signal_generator",
    "BidDataStore", "JobDataStore", "Tier2SignalGenerator",
    "ALTDATA_TOOLS", "ALTDATA_HANDLERS"
])

# Tenbagger评估工具
try:
    from .tenbagger_evaluator import (
        get_evaluator, TenbaggerEvaluator,
        TenbaggerReport, EvalDimension, EvalLevel
    )
    from .tenbagger_tools import TENBAGGER_TOOLS, TENBAGGER_HANDLERS
except ImportError:
    TENBAGGER_TOOLS = []
    TENBAGGER_HANDLERS = {}

__all__.extend([
    "get_evaluator", "TenbaggerEvaluator",
    "TenbaggerReport", "EvalLevel",
    "TENBAGGER_TOOLS", "TENBAGGER_HANDLERS"
])

# Portfolio组合管理工具
try:
    from .portfolio_manager import (
        get_portfolio, PortfolioManager,
        Position, Order, StrategyAllocation, RiskConfig, RiskManager
    )
    from .portfolio_tools import PORTFOLIO_TOOLS, PORTFOLIO_HANDLERS
except ImportError:
    PORTFOLIO_TOOLS = []
    PORTFOLIO_HANDLERS = {}

__all__.extend([
    "get_portfolio", "PortfolioManager",
    "Position", "Order", "StrategyAllocation",
    "PORTFOLIO_TOOLS", "PORTFOLIO_HANDLERS"
])

# DataSource数据源工具
try:
    from .datasource_manager import (
        get_datasource_manager, DataSourceManager,
        DataRequest, DataResponse, DataCategory, DataSourceType,
        MockDataProvider, JQDataProvider
    )
    from .datasource_tools import DATASOURCE_TOOLS, DATASOURCE_HANDLERS
except ImportError:
    DATASOURCE_TOOLS = []
    DATASOURCE_HANDLERS = {}

__all__.extend([
    "get_datasource_manager", "DataSourceManager",
    "DataRequest", "DataCategory", "DataSourceType",
    "DATASOURCE_TOOLS", "DATASOURCE_HANDLERS"
])

# JQData增强版
try:
    from .jqdata_enhanced import get_jqdata_enhanced, JQDataEnhanced
    from .datasource_manager import register_jqdata_provider
except ImportError:
    pass
