"""
Rotation - 行业/主题轮动模块
============================

实现A股行业轮动与主题ETF轮动的共振分析
"""

from core.rotation.sector_resonance import (
    SectorResonanceEngine,
    SectorScore,
    ThemeETFScore,
)

__all__ = [
    "SectorResonanceEngine",
    "SectorScore",
    "ThemeETFScore",
]
