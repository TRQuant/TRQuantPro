# -*- coding: utf-8 -*-
"""
TRQuant Shared Library
======================

共享库层 - 桌面系统和扩展件共用的核心接口

设计原则：
1. 定义统一的API接口
2. 自动检测运行环境（完整版/独立部署）
3. 提供适配器模式切换实现

使用方式：
    from shared import get_api
    api = get_api()
    
    # 统一调用，无论是桌面还是扩展
    result = api.analyze_market_trend()
    mainlines = api.get_mainlines()
"""

from .api import TRQuantAPI, get_api

__all__ = ['TRQuantAPI', 'get_api']
__version__ = '1.0.0'






















































