# -*- coding: utf-8 -*-
"""
五维评分独立Tab组件

每个维度有独立的Tab页面，便于可视化和工具扩展
热度维度使用现有的heatmap_panel.py
"""

from .funds_tab import FundsDimensionTab
from .momentum_tab import MomentumDimensionTab
from .policy_tab import PolicyDimensionTab
from .leader_tab import LeaderDimensionTab
from .composite_tab import CompositeDimensionTab

__all__ = [
    "FundsDimensionTab",
    "MomentumDimensionTab",
    "PolicyDimensionTab",
    "LeaderDimensionTab",
    "CompositeDimensionTab",
]
