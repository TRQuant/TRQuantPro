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
]
