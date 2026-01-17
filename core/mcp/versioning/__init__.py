"""
版本管理模块

提供版本注册、路由和兼容性管理功能。

Author: TRQuant Team
Date: 2025-12-21
"""

from .version_manager import VersionManager, get_version_manager

__all__ = [
    'VersionManager',
    'get_version_manager',
]

