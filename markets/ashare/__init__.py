# -*- coding: utf-8 -*-
"""
A股市场模块
==========

包含A股特有的数据源、因子、策略和主线识别。
"""

from .mainline.engine import AShareMainlineEngine

__all__ = [
    'AShareMainlineEngine',
]


