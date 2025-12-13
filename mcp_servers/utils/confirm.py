#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP写操作双确认机制
==================

提供confirm_token的生成和校验功能，确保写操作的安全性。

Token格式：
    {tool_name}_{args_hash}_{trace_id}_{expires_at}

Token校验规则：
    1. tool_name必须匹配
    2. args_hash必须匹配（排除confirm_token本身）
    3. trace_id必须匹配
    4. expires_at必须未过期

使用方式:
    from mcp_servers.utils.confirm import build_confirm_payload, verify_confirm_token
    
    # 生成token（在evidence.record或secrets.get_token中）
    token = build_confirm_payload("factor.create", arguments, trace_id)
    
    # 校验token（在执行侧）
    ok, err_code = verify_confirm_token(token, "factor.create", arguments, trace_id)
"""

import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional


def _compute_args_hash(arguments: Dict[str, Any]) -> str:
    """
    计算参数哈希（排除confirm_token本身）
    
    Args:
        arguments: 工具参数
    
    Returns:
        16位哈希值
    """
    # 复制参数并排除confirm_token
    args_copy = {k: v for k, v in arguments.items() if k != "confirm_token"}
    
    # 排序后序列化
    args_str = json.dumps(args_copy, sort_keys=True, ensure_ascii=False)
    
    # 计算SHA256并取前16位
    hash_obj = hashlib.sha256(args_str.encode('utf-8'))
    return hash_obj.hexdigest()[:16]


def build_confirm_payload(
    tool_name: str,
    arguments: Dict[str, Any],
    trace_id: str,
    expires_minutes: int = 30
) -> str:
    """
    构建confirm_token
    
    Args:
        tool_name: 工具名称（如：factor.create）
        arguments: 工具参数（会自动排除confirm_token）
        trace_id: 追踪ID
        expires_minutes: 过期时间（分钟）
    
    Returns:
        confirm_token字符串
    """
    # 计算参数哈希（排除confirm_token）
    args_hash = _compute_args_hash(arguments)
    
    # 计算过期时间（使用时间戳，避免ISO格式中的特殊字符）
    expires_at = int((datetime.now() + timedelta(minutes=expires_minutes)).timestamp())
    
    # 构建token（使用|作为分隔符，避免tool_name和trace_id中的下划线冲突）
    token = f"{tool_name}|{args_hash}|{trace_id}|{expires_at}"
    
    return token


def verify_confirm_token(
    token: str,
    tool_name: str,
    arguments: Dict[str, Any],
    trace_id: str
) -> Tuple[bool, Optional[str]]:
    """
    校验confirm_token
    
    Args:
        token: confirm_token字符串
        tool_name: 工具名称
        arguments: 工具参数
        trace_id: 追踪ID
    
    Returns:
        (是否有效, 错误码)
        错误码：None表示有效，INVALID_TOKEN表示无效，TOKEN_EXPIRED表示过期
    """
    if not token:
        return False, "INVALID_TOKEN"
    
    try:
        # 解析token（使用|作为分隔符）
        parts = token.split("|")
        if len(parts) != 4:
            return False, "INVALID_TOKEN"
        
        # 格式：tool_name|args_hash|trace_id|expires_at
        token_tool = parts[0]
        token_args_hash = parts[1]
        token_trace_id = parts[2]
        expires_str = parts[3]
        
        # 解析expires_at（时间戳格式）
        try:
            expires_timestamp = int(expires_str)
            expires_at = datetime.fromtimestamp(expires_timestamp)
        except (ValueError, OSError):
            # 解析失败
            return False, "INVALID_TOKEN"
        
        # 校验1: tool_name必须匹配
        if token_tool != tool_name:
            return False, "INVALID_TOKEN"
        
        # 校验2: args_hash必须匹配
        expected_args_hash = _compute_args_hash(arguments)
        if token_args_hash != expected_args_hash:
            return False, "INVALID_TOKEN"
        
        # 校验3: trace_id必须匹配
        if token_trace_id != trace_id:
            return False, "INVALID_TOKEN"
        
        # 校验4: 过期时间必须未过期
        if datetime.now() > expires_at:
            return False, "TOKEN_EXPIRED"
        
        return True, None
        
    except Exception as e:
        # 解析失败
        return False, "INVALID_TOKEN"


def extract_token_components(token: str) -> Optional[Dict[str, str]]:
    """
    提取token的各个组件（用于调试）
    
    Args:
        token: confirm_token字符串
    
    Returns:
        包含tool_name, args_hash, trace_id, expires_at的字典
    """
    try:
        parts = token.split("|")
        if len(parts) != 4:
            return None
        
        # 格式：tool_name|args_hash|trace_id|expires_at
        return {
            "tool_name": parts[0],
            "args_hash": parts[1],
            "trace_id": parts[2],
            "expires_at": parts[3]
        }
    except Exception:
        return None

