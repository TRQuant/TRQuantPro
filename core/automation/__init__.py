# -*- coding: utf-8 -*-
"""
自动化模块
=========
包含浏览器自动化、Agent等功能

模块:
- browser_agent: 浏览器自动化工具
- openmanus_agent: OpenManus智能Agent
- performance: 性能优化工具
"""

from .browser_agent import BrowserAgent
from .openmanus_agent import OpenManusAgent
from .performance import (
    RequestCache, 
    BrowserPool, 
    ParallelExecutor,
    PerformanceMonitor,
    cached,
    get_global_cache,
    get_global_monitor
)

__all__ = [
    'BrowserAgent', 
    'OpenManusAgent',
    'RequestCache',
    'BrowserPool',
    'ParallelExecutor',
    'PerformanceMonitor',
    'cached',
    'get_global_cache',
    'get_global_monitor'
]
