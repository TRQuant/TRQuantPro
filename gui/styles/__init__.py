# -*- coding: utf-8 -*-
"""
韬睿量化专业版 - 样式模块
"""
from .theme import (
    Colors,
    Typography,
    Spacing,
    BorderRadius,
    GLOBAL_STYLE,
    ButtonStyles,
    CardStyles,
    LabelStyles,
    BadgeStyles,
    apply_theme,
)

# 向后兼容
DARK_THEME = GLOBAL_STYLE
COLORS = Colors

__all__ = [
    'Colors',
    'Typography',
    'Spacing',
    'BorderRadius',
    'GLOBAL_STYLE',
    'ButtonStyles',
    'CardStyles',
    'LabelStyles',
    'BadgeStyles',
    'apply_theme',
    'DARK_THEME',
    'COLORS',
]
