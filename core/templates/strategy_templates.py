# -*- coding: utf-8 -*-
"""
策略模板库
=========
提供多种预定义策略模板，可直接使用或自定义参数
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json


@dataclass
class StrategyTemplate(ABC):
    """策略模板基类"""
    name: str
    description: str
    category: str
    params: Dict[str, Any] = field(default_factory=dict)
    
    @abstractmethod
    def get_default_params(self) -> Dict[str, Any]:
        """获取默认参数"""
        pass
    
    @abstractmethod
    def generate_code(self, params: Dict[str, Any] = None) -> str:
        """生成策略代码"""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> bool:
        """验证参数"""
        return True


@dataclass
class MomentumTemplate(StrategyTemplate):
    """动量策略模板"""
    name: str = "动量策略"
    description: str = "基于价格动量选股，追涨杀跌"
    category: str = "momentum"
    
    def get_default_params(self) -> Dict[str, Any]:
        return {
            "short_period": 5,
            "long_period": 20,
            "max_stocks": 10,
            "rebalance_days": 5,
            "stop_loss": 0.08,
            "take_profit": 0.20
        }
    
    def generate_code(self, params: Dict[str, Any] = None) -> str:
        p = {**self.get_default_params(), **(params or {})}
        return f'''# -*- coding: utf-8 -*-
"""动量策略 - 自动生成"""
from jqdata import *

# 参数
SHORT_PERIOD = {p["short_period"]}
LONG_PERIOD = {p["long_period"]}
MAX_STOCKS = {p["max_stocks"]}
REBALANCE_DAYS = {p["rebalance_days"]}
STOP_LOSS = {p["stop_loss"]}
TAKE_PROFIT = {p["take_profit"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, 
                            open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.trade_count = 0
    run_daily(rebalance, time='09:35')

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    stocks = get_index_stocks('000300.XSHG')
    df = get_price(stocks, end_date=context.current_dt, frequency='daily', fields=['close'], count=LONG_PERIOD+5, panel=False)
    pivot = df.pivot(index='time', columns='code', values='close')
    
    mom_short = pivot.pct_change(SHORT_PERIOD).iloc[-1]
    mom_long = pivot.pct_change(LONG_PERIOD).iloc[-1]
    score = (mom_short * 0.5 + mom_long * 0.5)
    score = score[(mom_short > 0) & (mom_long > 0)].dropna()
    
    targets = score.nlargest(MAX_STOCKS).index.tolist()
    
    # 卖出不在目标的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    # 买入目标
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
'''


@dataclass
class ValueTemplate(StrategyTemplate):
    """价值策略模板"""
    name: str = "价值策略"
    description: str = "基于估值因子选股，低估买入"
    category: str = "value"
    
    def get_default_params(self) -> Dict[str, Any]:
        return {
            "pe_max": 20,
            "pb_max": 2,
            "max_stocks": 10,
            "rebalance_days": 20
        }
    
    def generate_code(self, params: Dict[str, Any] = None) -> str:
        p = {**self.get_default_params(), **(params or {})}
        return f'''# -*- coding: utf-8 -*-
"""价值策略 - 自动生成"""
from jqdata import *

PE_MAX = {p["pe_max"]}
PB_MAX = {p["pb_max"]}
MAX_STOCKS = {p["max_stocks"]}
REBALANCE_DAYS = {p["rebalance_days"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    g.trade_count = 0
    run_daily(rebalance, time='09:35')

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    q = query(valuation.code, valuation.pe_ratio, valuation.pb_ratio
        ).filter(valuation.pe_ratio > 0, valuation.pe_ratio < PE_MAX,
                 valuation.pb_ratio > 0, valuation.pb_ratio < PB_MAX
        ).order_by(valuation.pe_ratio.asc()).limit(MAX_STOCKS)
    
    df = get_fundamentals(q)
    targets = df['code'].tolist()
    
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
'''


@dataclass
class TrendTemplate(StrategyTemplate):
    """趋势策略模板"""
    name: str = "趋势策略"
    description: str = "基于均线趋势交易"
    category: str = "trend"
    
    def get_default_params(self) -> Dict[str, Any]:
        return {
            "fast_period": 5,
            "slow_period": 20,
            "max_stocks": 10
        }
    
    def generate_code(self, params: Dict[str, Any] = None) -> str:
        p = {**self.get_default_params(), **(params or {})}
        return f'''# -*- coding: utf-8 -*-
"""趋势策略 - 自动生成"""
from jqdata import *
import pandas as pd

FAST = {p["fast_period"]}
SLOW = {p["slow_period"]}
MAX_STOCKS = {p["max_stocks"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    run_daily(rebalance, time='09:35')

def rebalance(context):
    stocks = get_index_stocks('000300.XSHG')[:100]
    
    signals = []
    for stock in stocks:
        df = get_price(stock, end_date=context.current_dt, count=SLOW+5, fields=['close'])
        if len(df) < SLOW:
            continue
        ma_fast = df['close'].rolling(FAST).mean().iloc[-1]
        ma_slow = df['close'].rolling(SLOW).mean().iloc[-1]
        if ma_fast > ma_slow:
            signals.append((stock, ma_fast / ma_slow))
    
    signals.sort(key=lambda x: x[1], reverse=True)
    targets = [s[0] for s in signals[:MAX_STOCKS]]
    
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
'''


@dataclass
class MultiFactorTemplate(StrategyTemplate):
    """多因子策略模板"""
    name: str = "多因子策略"
    description: str = "综合多个因子选股"
    category: str = "multi_factor"
    
    def get_default_params(self) -> Dict[str, Any]:
        return {
            "factors": ["momentum", "value", "quality"],
            "weights": [0.4, 0.3, 0.3],
            "max_stocks": 10,
            "rebalance_days": 10
        }
    
    def generate_code(self, params: Dict[str, Any] = None) -> str:
        p = {**self.get_default_params(), **(params or {})}
        return f'''# -*- coding: utf-8 -*-
"""多因子策略 - 自动生成"""
from jqdata import *
import pandas as pd

FACTORS = {p["factors"]}
WEIGHTS = {p["weights"]}
MAX_STOCKS = {p["max_stocks"]}
REBALANCE_DAYS = {p["rebalance_days"]}

def initialize(context):
    set_benchmark('000300.XSHG')
    g.trade_count = 0
    run_daily(rebalance, time='09:35')

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    stocks = get_index_stocks('000300.XSHG')
    scores = pd.Series(0.0, index=stocks)
    
    # 动量因子
    if "momentum" in FACTORS:
        idx = FACTORS.index("momentum")
        df = get_price(stocks, end_date=context.current_dt, count=20, fields=['close'], panel=False)
        pivot = df.pivot(index='time', columns='code', values='close')
        mom = pivot.pct_change(20).iloc[-1]
        scores += mom.rank(pct=True) * WEIGHTS[idx]
    
    # 价值因子
    if "value" in FACTORS:
        idx = FACTORS.index("value")
        q = query(valuation.code, valuation.pe_ratio).filter(valuation.code.in_(stocks))
        fund = get_fundamentals(q)
        pe_rank = fund.set_index('code')['pe_ratio'].rank(pct=True, ascending=True)
        for stock in pe_rank.index:
            if stock in scores.index:
                scores[stock] += pe_rank[stock] * WEIGHTS[idx]
    
    targets = scores.nlargest(MAX_STOCKS).index.tolist()
    
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
'''


# 模板注册表
_TEMPLATES: Dict[str, StrategyTemplate] = {
    "momentum": MomentumTemplate(),
    "value": ValueTemplate(),
    "trend": TrendTemplate(),
    "multi_factor": MultiFactorTemplate()
}


def get_template(name: str) -> Optional[StrategyTemplate]:
    """获取策略模板"""
    return _TEMPLATES.get(name)


def list_templates() -> List[Dict[str, Any]]:
    """列出所有模板"""
    return [
        {
            "name": t.name,
            "category": t.category,
            "description": t.description,
            "default_params": t.get_default_params()
        }
        for t in _TEMPLATES.values()
    ]
