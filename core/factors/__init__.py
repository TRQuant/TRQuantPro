#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Factors Module - 因子模块
========================

提供聚宽因子库和风险模型整合：
1. CNE5/CNE6风格因子
2. 聚宽因子库
3. Alpha101/Alpha191
4. 技术指标
5. 风险分解
"""

from .jqdata_factor_engine import (
    JQDataFactorEngine,
    get_jqdata_factor_engine,
    FactorExposure,
    FactorReturn,
    RiskDecomposition,
    CNE5_FACTORS,
    CNE6_FACTORS,
    JQFACTOR_CATEGORIES
)

__all__ = [
    'JQDataFactorEngine',
    'get_jqdata_factor_engine',
    'FactorExposure',
    'FactorReturn',
    'RiskDecomposition',
    'CNE5_FACTORS',
    'CNE6_FACTORS',
    'JQFACTOR_CATEGORIES'
]
