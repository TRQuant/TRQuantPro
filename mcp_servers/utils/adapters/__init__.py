"""
MCP适配器层

连接MCP工具和业务服务，实现版本路由和格式转换。

Author: TRQuant Team
Date: 2025-12-21
"""

from .tenbagger_adapter import TenbaggerMCPAdapter, get_tenbagger_adapter

__all__ = [
    'TenbaggerMCPAdapter',
    'get_tenbagger_adapter',
]

