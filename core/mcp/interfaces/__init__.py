"""
MCP接口定义层

提供版本无关的接口定义，实现功能模块与GUI设计的解耦。

Author: TRQuant Team
Date: 2025-12-21
"""

from .tenbagger_interface import (
    ITenbaggerService,
    TenbaggerRequest,
    TenbaggerResponse
)

__all__ = [
    'ITenbaggerService',
    'TenbaggerRequest',
    'TenbaggerResponse',
]

