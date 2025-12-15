#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
错误处理工具
============

提供统一的异常到错误码映射，确保所有MCP服务器返回一致的错误格式。
"""

from typing import Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


def map_exception_to_error_code(exception: Exception) -> Tuple[str, str, str]:
    """
    映射异常到错误码、消息和提示
    
    Args:
        exception: 异常对象
    
    Returns:
        (error_code, error_message, error_hint) 元组
    """
    exception_type = type(exception).__name__
    error_message = str(exception)
    
    # ValueError -> VALIDATION_ERROR
    if isinstance(exception, ValueError):
        return (
            "VALIDATION_ERROR",
            error_message,
            "请检查输入参数是否符合工具Schema要求"
        )
    
    # FileNotFoundError, OSError -> NOT_FOUND
    if isinstance(exception, (FileNotFoundError, OSError)):
        if "No such file" in error_message or "not found" in error_message.lower():
            return (
                "NOT_FOUND",
                error_message,
                "请检查资源是否存在"
            )
        return (
            "NOT_FOUND",
            error_message,
            "请检查文件或目录路径是否正确"
        )
    
    # RuntimeError (依赖相关) -> DEPENDENCY_ERROR
    if isinstance(exception, RuntimeError):
        if "不可用" in error_message or "unavailable" in error_message.lower() or "not available" in error_message.lower():
            return (
                "DEPENDENCY_ERROR",
                error_message,
                "请检查依赖是否已安装和配置正确"
            )
        if "import" in error_message.lower() or "module" in error_message.lower():
            return (
                "DEPENDENCY_ERROR",
                error_message,
                "请检查依赖模块是否已安装"
            )
    
    # PermissionError -> PERMISSION_DENIED
    if isinstance(exception, PermissionError):
        return (
            "PERMISSION_DENIED",
            error_message,
            "请检查文件或目录权限配置"
        )
    
    # KeyError, AttributeError -> NOT_FOUND (资源不存在)
    if isinstance(exception, (KeyError, AttributeError)):
        return (
            "NOT_FOUND",
            error_message,
            "请检查资源是否存在或属性是否正确"
        )
    
    # TypeError -> VALIDATION_ERROR
    if isinstance(exception, TypeError):
        if "required" in error_message.lower() or "missing" in error_message.lower():
            return (
                "VALIDATION_ERROR",
                error_message,
                "请检查必需参数是否已提供"
            )
        return (
            "VALIDATION_ERROR",
            error_message,
            "请检查参数类型是否正确"
        )
    
    # 其他异常 -> INTERNAL_ERROR
    return (
        "INTERNAL_ERROR",
        error_message,
        "服务器内部错误，请查看日志或联系管理员"
    )


def get_error_details(exception: Exception) -> Dict[str, Any]:
    """
    获取错误详情
    
    Args:
        exception: 异常对象
    
    Returns:
        错误详情字典
    """
    return {
        "exception_type": type(exception).__name__,
        "exception_message": str(exception),
        "exception_module": exception.__class__.__module__ if hasattr(exception, '__class__') else None
    }


def wrap_exception_response(
    exception: Exception,
    server_name: str,
    tool_name: str,
    version: str = "1.0.0",
    trace_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    将异常包装为统一的错误响应格式
    
    Args:
        exception: 异常对象
        server_name: 服务器名称
        tool_name: 工具名称
        version: 服务器版本
        trace_id: 追踪ID
    
    Returns:
        统一envelope格式的错误响应
    """
    from mcp_servers.utils.envelope import wrap_error_response, generate_trace_id
    
    if trace_id is None:
        trace_id = generate_trace_id()
    
    error_code, error_message, error_hint = map_exception_to_error_code(exception)
    error_details = get_error_details(exception)
    
    # 记录异常日志
    logger.exception(f"工具调用失败: {server_name}.{tool_name}")
    
    return wrap_error_response(
        error_code=error_code,
        error_message=error_message,
        server_name=server_name,
        tool_name=tool_name,
        version=version,
        error_details=error_details,
        error_hint=error_hint,
        trace_id=trace_id
    )











# ============================================================================
# 新的错误码体系（模块_类型_编号格式）
# ============================================================================

class MCPError(Exception):
    """MCP工具基础异常类"""
    
    def __init__(self, code: str, message: str, details: Dict[str, Any] = None, trace_id: Optional[str] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        self.trace_id = trace_id
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "code": self.code,
            "message": self.message,
            "type": self._get_error_type(),
            "module": self._get_module(),
            "trace_id": self.trace_id,
            "details": self.details
        }
    
    def _get_error_type(self) -> str:
        """从错误码中提取错误类型"""
        parts = self.code.split('_')
        if len(parts) >= 2:
            return parts[1]
        return "UNKNOWN"
    
    def _get_module(self) -> str:
        """从错误码中提取模块名"""
        parts = self.code.split('_')
        if len(parts) >= 1:
            return parts[0]
        return "UNKNOWN"


class MCPParameterError(MCPError):
    """参数错误"""
    pass


class MCPSystemError(MCPError):
    """系统错误"""
    pass


class MCPBusinessError(MCPError):
    """业务错误"""
    pass


class MCPDataError(MCPError):
    """数据错误"""
    pass


def create_error_response(
    error: MCPError,
    server_name: str,
    tool_name: str,
    version: str = "1.0.0"
) -> Dict[str, Any]:
    """
    创建标准错误响应
    
    Args:
        error: MCP错误对象
        server_name: 服务器名称
        tool_name: 工具名称
        version: 服务器版本
    
    Returns:
        标准错误响应字典
    """
    from mcp_servers.utils.trace_manager import TraceManager
    
    trace_id = error.trace_id or TraceManager.get_trace_id()
    
    return {
        "error": error.to_dict(),
        "server": server_name,
        "tool": tool_name,
        "version": version,
        "trace_id": trace_id
    }


# 错误码常量定义
class ErrorCodes:
    """错误码常量"""
    
    # 参数错误
    PARAM_MISSING = "_PARAM_001"
    PARAM_TYPE_ERROR = "_PARAM_002"
    PARAM_FORMAT_ERROR = "_PARAM_003"
    PARAM_RANGE_ERROR = "_PARAM_004"
    PARAM_VALIDATION_FAILED = "_PARAM_005"
    
    # 系统错误
    SYSTEM_INTERNAL = "_SYSTEM_001"
    SYSTEM_UNAVAILABLE = "_SYSTEM_002"
    SYSTEM_TIMEOUT = "_SYSTEM_003"
    SYSTEM_RESOURCE = "_SYSTEM_004"
    SYSTEM_CONFIG = "_SYSTEM_005"
    
    # 业务错误
    BUSINESS_NOT_FOUND = "_BUSINESS_001"
    BUSINESS_FORBIDDEN = "_BUSINESS_002"
    BUSINESS_CONFLICT = "_BUSINESS_003"
    BUSINESS_RULE_VIOLATION = "_BUSINESS_004"
    BUSINESS_OPERATION_FAILED = "_BUSINESS_005"
    
    # 数据错误
    DATA_NOT_FOUND = "_DATA_001"
    DATA_FORMAT_ERROR = "_DATA_002"
    DATA_VALIDATION_FAILED = "_DATA_003"
    DATA_ACCESS_FAILED = "_DATA_004"
    
    @staticmethod
    def build_code(module: str, error_type: str) -> str:
        """
        构建错误码
        
        Args:
            module: 模块名（如KB, DATA）
            error_type: 错误类型常量（如PARAM_MISSING）
        
        Returns:
            完整错误码
        """
        return f"{module}{error_type}"
