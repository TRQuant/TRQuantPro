# -*- coding: utf-8 -*-
"""
韬睿量化因子库
=============

提供完整的量化因子计算功能，支持：
- 价值因子：EP, BP, SP, 股息率
- 成长因子：营收增速, 利润增速, ROE变化
- 质量因子：ROE, 毛利率, 周转率, 杠杆
- 动量因子：价格动量, 反转, 相对强弱
- 资金流因子：北向资金, 主力资金

所有因子均可直接用于PTrade实盘策略。
"""

from .base_factor import BaseFactor, FactorResult
from .factor_manager import FactorManager
from .value_factors import (
    EPFactor, BPFactor, SPFactor, DividendYieldFactor,
    CompositeValueFactor
)
from .growth_factors import (
    RevenueGrowthFactor, ProfitGrowthFactor, ROEChangeFactor,
    CompositeGrowthFactor
)
from .quality_factors import (
    ROEFactor, GrossMarginFactor, AssetTurnoverFactor, LeverageFactor,
    CompositeQualityFactor
)
from .momentum_factors import (
    PriceMomentumFactor, ReversalFactor, RelativeStrengthFactor,
    CompositeMomentumFactor
)
from .flow_factors import (
    NorthboundFlowFactor, MainForceFlowFactor, MarginBalanceFactor,
    CompositeFlowFactor
)

__all__ = [
    # 基类
    'BaseFactor',
    'FactorResult',
    'FactorManager',
    
    # 价值因子
    'EPFactor',
    'BPFactor', 
    'SPFactor',
    'DividendYieldFactor',
    'CompositeValueFactor',
    
    # 成长因子
    'RevenueGrowthFactor',
    'ProfitGrowthFactor',
    'ROEChangeFactor',
    'CompositeGrowthFactor',
    
    # 质量因子
    'ROEFactor',
    'GrossMarginFactor',
    'AssetTurnoverFactor',
    'LeverageFactor',
    'CompositeQualityFactor',
    
    # 动量因子
    'PriceMomentumFactor',
    'ReversalFactor',
    'RelativeStrengthFactor',
    'CompositeMomentumFactor',
    
    # 资金流因子
    'NorthboundFlowFactor',
    'MainForceFlowFactor',
    'MarginBalanceFactor',
    'CompositeFlowFactor',
]

__version__ = '1.0.0'

