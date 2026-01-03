# -*- coding: utf-8 -*-
"""
TRQuant 数据库模块
==================

提供数据库访问、优化和备份功能
"""

from .db_optimizer import (
    DatabaseOptimizer,
    get_optimizer,
    optimize_database,
    COLLECTION_CONFIGS,
    CollectionConfig,
    IndexSpec
)

from .backup_manager import (
    BackupManager,
    BackupInfo,
    get_backup_manager
)

__all__ = [
    # 优化器
    "DatabaseOptimizer",
    "get_optimizer",
    "optimize_database",
    "COLLECTION_CONFIGS",
    "CollectionConfig",
    "IndexSpec",
    # 备份管理器
    "BackupManager",
    "BackupInfo",
    "get_backup_manager"
]
