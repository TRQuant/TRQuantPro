# -*- coding: utf-8 -*-
"""
韬睿量化 - 数据源管理模块
==========================

提供统一的数据源管理，支持多数据源切换和本地缓存。

数据源：
- JQData（聚宽）- 主数据源
- AKShare - 备用数据源
- QMT桥接 - 实时数据源（需要Windows虚拟机）
- PTrade桥接 - 交易数据源

缓存：
- MongoDB - 本地数据缓存
"""

from .cache_manager import MongoDBCache
from .data_source_manager import DataSourceManager
from .jqdata_source import JQDataSource
from .akshare_source import AKShareSource

__all__ = [
    'MongoDBCache',
    'DataSourceManager', 
    'JQDataSource',
    'AKShareSource',
]





