#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP工具工件（Artifact）存储与索引规范
====================================

提供统一的工件存储、检索和预览功能，避免大JSON导致Broken pipe。

工件路径规范：
    .taorui/artifacts/{artifact_type}/{date}/artifact_{timestamp}_{shortid}.json

工件指针结构：
    {
        "artifact_id": "artifact_20251209_123456_abc123",
        "artifact_path": ".taorui/artifacts/reports/report_20251209_123456.json",
        "artifact_type": "report",
        "preview": {...},
        "size_bytes": 1024000,
        "expires_at": "2025-12-10T12:00:00Z"
    }

使用方式:
    from mcp_servers.utils.artifacts import artifact_write, artifact_preview, get_artifact
    
    # 写入工件
    pointer = artifact_write(data, "report", trace_id)
    
    # 读取工件
    data = get_artifact(pointer["artifact_id"])
"""

import json
import hashlib
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Union

# 工件存储根目录
ARTIFACTS_ROOT = Path(".taorui/artifacts")

# 默认过期时间（天）
DEFAULT_EXPIRES_DAYS = 30

# 强制使用pointer的阈值（字节）
FORCE_POINTER_THRESHOLD = 256 * 1024  # 256KB


def _ensure_artifacts_dir(artifact_type: str) -> Path:
    """确保工件目录存在"""
    date_str = datetime.now().strftime("%Y%m%d")
    artifact_dir = ARTIFACTS_ROOT / artifact_type / date_str
    artifact_dir.mkdir(parents=True, exist_ok=True)
    return artifact_dir


def _generate_artifact_id() -> str:
    """生成工件ID"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_id = uuid.uuid4().hex[:8]
    return f"artifact_{timestamp}_{short_id}"


def artifact_write(
    payload: Any,
    artifact_type: str,
    trace_id: Optional[str] = None,
    expires_days: int = DEFAULT_EXPIRES_DAYS
) -> Dict[str, Any]:
    """
    写入工件并返回指针
    
    Args:
        payload: 要存储的数据（会被JSON序列化）
        artifact_type: 工件类型（如：report, code, factor_detail等）
        trace_id: 追踪ID
        expires_days: 过期天数
    
    Returns:
        工件指针结构
    """
    # 确保目录存在
    artifact_dir = _ensure_artifacts_dir(artifact_type)
    
    # 生成工件ID和文件名
    artifact_id = _generate_artifact_id()
    filename = f"{artifact_id}.json"
    artifact_path = artifact_dir / filename
    
    # 序列化并写入
    json_str = json.dumps(payload, ensure_ascii=False, indent=2)
    artifact_path.write_text(json_str, encoding='utf-8')
    
    # 计算大小
    size_bytes = len(json_str.encode('utf-8'))
    
    # 生成预览
    preview = artifact_preview(payload, artifact_type)
    
    # 计算过期时间
    expires_at = (datetime.now() + timedelta(days=expires_days)).isoformat() + "Z"
    
    # 构建指针
    # 使用绝对路径，然后转换为相对路径（如果可能）
    try:
        artifact_path_rel = str(artifact_path.relative_to(Path.cwd()))
    except ValueError:
        # 如果不在当前工作目录下，使用绝对路径
        artifact_path_rel = str(artifact_path)
    
    pointer = {
        "artifact_id": artifact_id,
        "artifact_path": artifact_path_rel,
        "artifact_path_absolute": str(artifact_path.absolute()),
        "artifact_type": artifact_type,
        "preview": preview,
        "size_bytes": size_bytes,
        "expires_at": expires_at
    }
    
    if trace_id:
        pointer["trace_id"] = trace_id
    
    return pointer


def artifact_preview(payload: Any, artifact_type: str) -> Dict[str, Any]:
    """
    生成工件预览（摘要）
    
    Args:
        payload: 数据
        artifact_type: 工件类型
    
    Returns:
        预览信息
    """
    preview = {
        "type": artifact_type,
        "summary": "数据已存储为工件"
    }
    
    # 根据类型生成特定预览
    if artifact_type == "report":
        if isinstance(payload, dict):
            preview.update({
                "summary": payload.get("summary", "回测报告"),
                "total_return": payload.get("total_return"),
                "sharpe_ratio": payload.get("sharpe_ratio"),
                "max_drawdown": payload.get("max_drawdown")
            })
    elif artifact_type == "code":
        if isinstance(payload, dict):
            preview.update({
                "summary": f"代码文件: {payload.get('file', 'unknown')}",
                "lines": payload.get("lines", 0),
                "language": payload.get("language", "python")
            })
    elif artifact_type == "factor_detail":
        if isinstance(payload, dict):
            preview.update({
                "summary": f"因子: {payload.get('name', 'unknown')}",
                "category": payload.get("category"),
                "description": payload.get("description", "")[:100]
            })
    elif artifact_type == "strategy":
        if isinstance(payload, dict):
            preview.update({
                "summary": f"策略: {payload.get('name', 'unknown')}",
                "factors_count": len(payload.get("factors", [])),
                "description": payload.get("description", "")[:100]
            })
    
    return preview


def get_artifact(artifact_id: str) -> Optional[Dict[str, Any]]:
    """
    读取工件
    
    Args:
        artifact_id: 工件ID
    
    Returns:
        工件数据，如果不存在或已过期则返回None
    """
    # 查找工件文件（可能在多个日期目录中）
    for date_dir in ARTIFACTS_ROOT.glob("*/20*"):
        artifact_file = date_dir / f"{artifact_id}.json"
        if artifact_file.exists():
            try:
                data = json.loads(artifact_file.read_text(encoding='utf-8'))
                return data
            except Exception:
                return None
    
    return None


def should_use_artifact(payload: Any, artifact_policy: str = "inline") -> bool:
    """
    判断是否应该使用工件（而不是内联返回）
    
    Args:
        payload: 数据
        artifact_policy: 用户请求的策略
    
    Returns:
        是否应该使用工件
    """
    # 如果用户明确要求pointer，使用工件
    if artifact_policy == "pointer":
        return True
    
    # 如果用户要求inline，但数据超过阈值，强制使用工件
    if artifact_policy == "inline":
        try:
            json_str = json.dumps(payload, ensure_ascii=False)
            size_bytes = len(json_str.encode('utf-8'))
            if size_bytes > FORCE_POINTER_THRESHOLD:
                return True
        except Exception:
            # 如果序列化失败，使用工件更安全
            return True
    
    return False


def create_artifact_if_needed(
    payload: Any,
    artifact_type: str,
    artifact_policy: str,
    trace_id: Optional[str] = None
) -> Union[Dict[str, Any], Any]:
    """
    根据策略创建工件或返回原始数据
    
    Args:
        payload: 数据
        artifact_type: 工件类型
        artifact_policy: 输出策略
        trace_id: 追踪ID
    
    Returns:
        如果应该使用工件，返回指针；否则返回原始数据
    """
    if should_use_artifact(payload, artifact_policy):
        pointer = artifact_write(payload, artifact_type, trace_id)
        # 添加元数据说明
        pointer["_meta"] = {
            "note": "forced_pointer_due_to_size" if artifact_policy == "inline" else "user_requested_pointer"
        }
        return pointer
    return payload














