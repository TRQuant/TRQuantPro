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









