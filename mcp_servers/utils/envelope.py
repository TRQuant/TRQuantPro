#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP工具响应统一Envelope包装器
=============================

提供统一的响应格式包装，确保所有MCP工具返回一致的envelope结构：
{
    "ok": bool,
    "data": Any,
    "error": Optional[Dict],
    "meta": {
        "server": str,
        "tool": str,
        "version": str,
        "timestamp": str,
        "trace_id": str
    }
}
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union
from pathlib import Path


def generate_trace_id(prefix: str = "trace") -> str:
    """生成trace_id"""
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


def wrap_success_response(
    data: Any,
    server_name: str,
    tool_name: str,
    version: str = "1.0.0",
    trace_id: Optional[str] = None
) -> Dict[str, Any]:
    """包装成功响应为统一envelope格式
    
    Args:
        data: 业务数据
        server_name: 服务器名称
        tool_name: 工具名称
        version: 服务器版本
        trace_id: 追踪ID（如果为None则自动生成）
    
    Returns:
        统一envelope格式的响应
    """
    if trace_id is None:
        trace_id = generate_trace_id()
    
    return {
        "ok": True,
        "data": data,
        "error": None,
        "meta": {
            "server": server_name,
            "tool": tool_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "trace_id": trace_id
        }
    }


def wrap_error_response(
    error_code: str,
    error_message: str,
    server_name: str,
    tool_name: str,
    version: str = "1.0.0",
    error_details: Optional[Dict[str, Any]] = None,
    error_hint: Optional[str] = None,
    trace_id: Optional[str] = None
) -> Dict[str, Any]:
    """包装错误响应为统一envelope格式
    
    Args:
        error_code: 错误码（必须在白名单内）
        error_message: 错误消息
        server_name: 服务器名称
        tool_name: 工具名称
        version: 服务器版本
        error_details: 错误详情
        error_hint: 错误提示（如何修复）
        trace_id: 追踪ID（如果为None则自动生成）
    
    Returns:
        统一envelope格式的错误响应
    """
    if trace_id is None:
        trace_id = generate_trace_id()
    
    error = {
        "code": error_code,
        "message": error_message,
        "details": error_details or {},
        "hint": error_hint or "请检查输入参数或联系管理员"
    }
    
    return {
        "ok": False,
        "data": None,
        "error": error,
        "meta": {
            "server": server_name,
            "tool": tool_name,
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "trace_id": trace_id
        }
    }


def extract_trace_id_from_request(params: Dict[str, Any]) -> Optional[str]:
    """从请求参数中提取trace_id
    
    Args:
        params: MCP请求参数
    
    Returns:
        trace_id或None
    """
    # 尝试从arguments中提取
    arguments = params.get("arguments", {})
    if isinstance(arguments, dict):
        trace_id = arguments.get("trace_id")
        if trace_id:
            return trace_id
    
    # 尝试从params顶层提取
    trace_id = params.get("trace_id")
    if trace_id:
        return trace_id
    
    return None


def wrap_mcp_tool_response(
    result: Any,
    server_name: str,
    tool_name: str,
    version: str = "1.0.0",
    request_params: Optional[Dict[str, Any]] = None,
    is_error: bool = False,
    error_code: Optional[str] = None,
    error_message: Optional[str] = None
) -> Dict[str, Any]:
    """包装MCP工具响应（自动判断成功/错误）
    
    Args:
        result: 工具执行结果
        server_name: 服务器名称
        tool_name: 工具名称
        version: 服务器版本
        request_params: 请求参数（用于提取trace_id）
        is_error: 是否为错误响应
        error_code: 错误码（错误时必需）
        error_message: 错误消息（错误时必需）
    
    Returns:
        统一envelope格式的响应
    """
    trace_id = None
    if request_params:
        trace_id = extract_trace_id_from_request(request_params)
    
    if is_error:
        if not error_code or not error_message:
            error_code = "INTERNAL_ERROR"
            error_message = str(result) if result else "未知错误"
        
        return wrap_error_response(
            error_code=error_code,
            error_message=error_message,
            server_name=server_name,
            tool_name=tool_name,
            version=version,
            error_details={"raw_error": str(result)} if result else None,
            trace_id=trace_id
        )
    else:
        return wrap_success_response(
            data=result,
            server_name=server_name,
            tool_name=tool_name,
            version=version,
            trace_id=trace_id
        )


# 装饰器：自动包装工具响应
def with_envelope(server_name: str, version: str = "1.0.0"):
    """装饰器：自动为工具函数添加envelope包装
    
    使用示例:
        @with_envelope("trquant-spec", "1.0.0")
        async def call_tool(name: str, arguments: dict, request_params: dict = None):
            # 工具逻辑
            return result
    """
    def decorator(func):
        async def wrapper(name: str, arguments: dict, request_params: dict = None, *args, **kwargs):
            try:
                result = await func(name, arguments, *args, **kwargs)
                return wrap_mcp_tool_response(
                    result=result,
                    server_name=server_name,
                    tool_name=name,
                    version=version,
                    request_params=request_params or {"arguments": arguments},
                    is_error=False
                )
            except Exception as e:
                return wrap_mcp_tool_response(
                    result=str(e),
                    server_name=server_name,
                    tool_name=name,
                    version=version,
                    request_params=request_params or {"arguments": arguments},
                    is_error=True,
                    error_code="INTERNAL_ERROR",
                    error_message=str(e)
                )
        return wrapper
    return decorator













