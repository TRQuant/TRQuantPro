#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP工具Schema拼装器
==================

提供可复用的Schema拼装功能，确保所有工具都包含统一的跨工具字段：
- trace_id: 链路追踪
- mode: 操作模式（read/dry_run/execute）
- artifact_policy: 输出策略（inline/pointer）
- confirm_token: 确认令牌（mode=execute时需要）

使用方式:
    from mcp_servers.utils.schema import base_args_schema, merge_schema
    
    # 获取基础Schema
    base = base_args_schema()
    
    # 合并到工具特定Schema
    tool_schema = merge_schema(base, {
        "type": "object",
        "properties": {
            "factor_id": {"type": "string", "description": "因子ID"}
        },
        "required": ["factor_id"]
    })
"""

from typing import Dict, Any, Optional


def base_args_schema(mode: str = "read") -> Dict[str, Any]:
    """
    返回基础跨工具字段的Schema定义
    
    Args:
        mode: 默认模式，影响required字段（execute时需要confirm_token）
    
    Returns:
        包含trace_id, mode, artifact_policy, confirm_token的properties定义
    """
    base_properties = {
        "trace_id": {
            "type": "string",
            "description": "追踪ID（可选，用于E2E链路追踪）"
        },
        "mode": {
            "type": "string",
            "enum": ["read", "dry_run", "execute"],
            "description": "操作模式：read(只读), dry_run(模拟执行不落盘), execute(真实执行，需要confirm_token)",
            "default": "read"
        },
        "artifact_policy": {
            "type": "string",
            "enum": ["inline", "pointer"],
            "description": "输出策略：inline(内联返回), pointer(返回工件指针，避免大JSON)",
            "default": "inline"
        }
    }
    
    # 如果mode是execute，confirm_token是必需的
    if mode == "execute":
        base_properties["confirm_token"] = {
            "type": "string",
            "description": "确认令牌（mode=execute时必需，由evidence.record或secrets.get_token生成）"
        }
        required = ["confirm_token"]
    else:
        base_properties["confirm_token"] = {
            "type": "string",
            "description": "确认令牌（mode=execute时必需）"
        }
        required = []
    
    return {
        "properties": base_properties,
        "required": required
    }


def merge_schema(base: Dict[str, Any], specific: Dict[str, Any]) -> Dict[str, Any]:
    """
    合并基础Schema和工具特定Schema
    
    Args:
        base: 基础Schema（来自base_args_schema()）
        specific: 工具特定的Schema定义
    
    Returns:
        合并后的完整Schema
    """
    if "type" not in specific:
        specific["type"] = "object"
    
    if "properties" not in specific:
        specific["properties"] = {}
    
    # 合并properties
    specific["properties"].update(base["properties"])
    
    # 合并required（去重）
    base_required = set(base.get("required", []))
    specific_required = set(specific.get("required", []))
    specific["required"] = list(specific_required | base_required)
    
    return specific


def build_tool_schema(
    tool_name: str,
    description: str,
    specific_properties: Dict[str, Any],
    required_fields: Optional[list] = None,
    default_mode: str = "read"
) -> Dict[str, Any]:
    """
    构建完整的工具Schema（便捷方法）
    
    Args:
        tool_name: 工具名称
        description: 工具描述
        specific_properties: 工具特定的properties
        required_fields: 工具特定的required字段
        default_mode: 默认模式
    
    Returns:
        完整的工具Schema
    """
    base = base_args_schema(mode=default_mode)
    
    schema = {
        "type": "object",
        "properties": specific_properties,
        "required": required_fields or []
    }
    
    return merge_schema(base, schema)


def validate_mode(mode: str, operation_type: str = "read") -> bool:
    """
    验证mode是否允许执行指定操作
    
    Args:
        mode: 操作模式
        operation_type: 操作类型（read/write/execute）
    
    Returns:
        是否允许
    """
    if operation_type == "read":
        return mode in ["read", "dry_run", "execute"]
    elif operation_type == "write":
        return mode in ["dry_run", "execute"]
    elif operation_type == "execute":
        return mode == "execute"
    return False


def requires_confirm_token(mode: str) -> bool:
    """
    判断是否需要confirm_token
    
    Args:
        mode: 操作模式
    
    Returns:
        是否需要confirm_token
    """
    return mode == "execute"













