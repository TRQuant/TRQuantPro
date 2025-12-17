# -*- coding: utf-8 -*-
"""
MCP 服务器工具库
================
提供统一的工具类和规范实现

Phase 2 实现:
- mcp_standard: 标准化工具 (命名/参数/trace_id/错误码)
- performance: 性能优化 (缓存/监控/连接池)
- logging_config: 日志和告警
"""

# MCP 标准化工具 (Phase 2.1)
from mcp_servers.utils.mcp_standard import (
    # 错误码
    ErrorCode,
    # trace_id
    TraceManager,
    TraceContext,
    # 参数验证
    ParamValidator,
    # 响应格式
    MCPResponse,
    wrap_success,
    wrap_error,
    # 基类
    MCPStandard,
    # 装饰器
    mcp_tool,
    # 命名规范
    NamingConvention,
)

# 性能优化 (Phase 2.2.1)
from mcp_servers.utils.performance import (
    MCPCache,
    get_cache,
    cached,
    PerformanceMonitor,
    get_monitor,
    monitored,
    ConnectionPool,
    BatchProcessor,
    PerformanceContext,
)

# 监控和日志 (Phase 2.2.2)
from mcp_servers.utils.logging_config import (
    StructuredFormatter,
    HumanReadableFormatter,
    MCPLoggerAdapter,
    setup_logging,
    get_mcp_logger,
    AlertManager,
    get_alert_manager,
)

# 旧版兼容
from mcp_servers.utils.trace_manager import (
    generate_trace_id,
    TraceManager as LegacyTraceManager,
    extract_trace_id_from_args,
    add_trace_id_to_args,
    get_trace_id_from_args_or_context,
)

from mcp_servers.utils.error_handler import (
    map_exception_to_error_code,
    get_error_details,
    wrap_exception_response,
    MCPError,
    MCPParameterError,
    MCPSystemError,
    MCPBusinessError,
    MCPDataError,
    create_error_response,
    ErrorCodes,
)

from mcp_servers.utils.parameter_validator import (
    ParameterValidationError,
    ParameterValidator as LegacyParameterValidator,
    validate_mcp_tool_params,
)

__all__ = [
    # Phase 2.1: 标准化
    "ErrorCode",
    "TraceManager",
    "TraceContext",
    "ParamValidator",
    "MCPResponse",
    "wrap_success",
    "wrap_error",
    "MCPStandard",
    "mcp_tool",
    "NamingConvention",
    # Phase 2.2.1: 性能
    "MCPCache",
    "get_cache",
    "cached",
    "PerformanceMonitor",
    "get_monitor",
    "monitored",
    "ConnectionPool",
    "PerformanceContext",
    # Phase 2.2.2: 日志
    "StructuredFormatter",
    "get_mcp_logger",
    "setup_logging",
    "AlertManager",
    "get_alert_manager",
    # 旧版兼容
    "generate_trace_id",
    "MCPError",
    "MCPParameterError",
    "validate_mcp_tool_params",
]
