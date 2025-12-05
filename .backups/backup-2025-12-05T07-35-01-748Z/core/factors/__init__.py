# -*- coding: utf-8 -*-
"""
韬睿量化因子库
=============

根据Alpha因子模块集成方案设计及补充建议，提供完整的量化因子计算功能：

因子类别：
- 价值因子：EP, BP, SP, 股息率
- 成长因子：营收增速, 利润增速, ROE变化
- 质量因子：ROE, 毛利率, 周转率, 杠杆
- 动量因子：价格动量, 反转, 相对强弱
- 资金流因子：北向资金, 主力资金
- 规模因子：市值、对数市值（新增）
- 波动率因子：波动率、Beta（新增）
- 流动性因子：换手率、成交额、非流动性（新增）

功能模块：
- 因子计算：BaseFactor, FactorResult
- 因子管理：FactorManager
- 因子验证：FactorEvaluator, ICResult, GroupBacktestResult
- 因子存储：FactorStorage (MongoDB + 文件存储)
- 因子中性化：FactorNeutralizer（新增）
- 因子相关性分析：FactorCorrelationAnalyzer（新增）
- 换手率分析：TurnoverAnalyzer（新增）
- 自动化流水线：FactorPipeline（新增）
- 候选池集成：FactorPoolIntegration

所有因子均可直接用于PTrade实盘策略。
"""

from .base_factor import BaseFactor, FactorResult
from .factor_manager import FactorManager
from .factor_evaluator import (
    FactorEvaluator, ICResult, GroupBacktestResult, FactorPerformance,
    create_factor_evaluator
)
from .factor_storage import FactorStorage, create_factor_storage
from .factor_neutralizer import (
    FactorNeutralizer, FactorCorrelationAnalyzer, TurnoverAnalyzer,
    create_factor_neutralizer, create_correlation_analyzer, create_turnover_analyzer
)
from .factor_pipeline import FactorPipeline, create_factor_pipeline
from .factor_pool_integration import FactorPoolIntegration, StockSignal, create_factor_pool_integration

# 价值因子
from .value_factors import (
    EPFactor, BPFactor, SPFactor, DividendYieldFactor,
    CompositeValueFactor
)
# 成长因子
from .growth_factors import (
    RevenueGrowthFactor, ProfitGrowthFactor, ROEChangeFactor,
    CompositeGrowthFactor
)
# 质量因子
from .quality_factors import (
    ROEFactor, GrossMarginFactor, AssetTurnoverFactor, LeverageFactor,
    CompositeQualityFactor
)
# 动量因子
from .momentum_factors import (
    PriceMomentumFactor, ReversalFactor, RelativeStrengthFactor,
    CompositeMomentumFactor
)
# 资金流因子
from .flow_factors import (
    NorthboundFlowFactor, MainForceFlowFactor, MarginBalanceFactor,
    CompositeFlowFactor
)
# 扩展因子（规模/波动率/流动性）
from .extended_factors import (
    SizeFactor, MarketCapFactor,
    VolatilityFactor, BetaFactor,
    TurnoverFactor, AmountFactor, IlliquidityFactor,
    CompositeSizeFactor, CompositeVolatilityFactor, CompositeLiquidityFactor
)

__all__ = [
    # 基类
    'BaseFactor',
    'FactorResult',
    'FactorManager',
    
    # 因子验证
    'FactorEvaluator',
    'ICResult',
    'GroupBacktestResult',
    'FactorPerformance',
    'create_factor_evaluator',
    
    # 因子存储
    'FactorStorage',
    'create_factor_storage',
    
    # 因子中性化与分析
    'FactorNeutralizer',
    'FactorCorrelationAnalyzer',
    'TurnoverAnalyzer',
    'create_factor_neutralizer',
    'create_correlation_analyzer',
    'create_turnover_analyzer',
    
    # 自动化流水线
    'FactorPipeline',
    'create_factor_pipeline',
    
    # 候选池集成
    'FactorPoolIntegration',
    'StockSignal',
    'create_factor_pool_integration',
    
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
    
    # 规模因子
    'SizeFactor',
    'MarketCapFactor',
    'CompositeSizeFactor',
    
    # 波动率因子
    'VolatilityFactor',
    'BetaFactor',
    'CompositeVolatilityFactor',
    
    # 流动性因子
    'TurnoverFactor',
    'AmountFactor',
    'IlliquidityFactor',
    'CompositeLiquidityFactor',
]

__version__ = '2.1.0'  # 添加扩展因子、中性化、流水线等模块

