# -*- coding: utf-8 -*-
"""
韬睿量化 - 核心框架层
====================

市场无关的核心抽象，支持多市场扩展。
"""

from .base_market import BaseMarket, MarketType
from .base_mainline import BaseMainlineEngine

__all__ = [
    'BaseMarket',
    'MarketType',
    'BaseMainlineEngine',
]
