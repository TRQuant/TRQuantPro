# -*- coding: utf-8 -*-
"""
回测优化系统 (Backtest Optimizer System)

功能：
1. 历史回测验证：验证筛选算法的有效性
2. 多周期收益评估：周/月/季/年/五年
3. 因子权重自动优化：基于回测表现
4. 市场环境自适应：不同环境不同策略
5. 防过拟合机制：交叉验证+正则化
"""

from .backtest_engine import BacktestEngine
from .factor_optimizer import FactorOptimizer
from .market_regime_adapter import MarketRegimeAdapter
from .final_selector import FinalSelector

__all__ = [
    'BacktestEngine',
    'FactorOptimizer', 
    'MarketRegimeAdapter',
    'FinalSelector'
]
