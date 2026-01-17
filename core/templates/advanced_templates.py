# -*- coding: utf-8 -*-
"""
高级策略模板
===========
轮动、套利、配对交易等高级策略模板
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TemplateParam:
    """模板参数"""
    name: str
    type: str  # int, float, str, list
    default: any
    description: str
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class BaseTemplate:
    """策略模板基类"""
    
    name: str = "base"
    description: str = "基础模板"
    params: List[TemplateParam] = []
    
    def generate_code(self, params: Dict) -> str:
        raise NotImplementedError
    
    def validate_params(self, params: Dict) -> bool:
        return True


class RotationTemplate(BaseTemplate):
    """
    行业/风格轮动策略模板
    根据动量或相对强弱在不同资产类别间轮动
    """
    
    name = "rotation"
    description = "行业/风格轮动策略"
    params = [
        TemplateParam("rotation_period", "int", 20, "轮动周期（天）", 5, 60),
        TemplateParam("top_n", "int", 3, "选择前N个资产", 1, 10),
        TemplateParam("lookback", "int", 20, "回看周期", 5, 120),
        TemplateParam("asset_type", "str", "industry", "资产类型: industry/style/etf"),
    ]
    
    def generate_code(self, params: Dict) -> str:
        rotation_period = params.get("rotation_period", 20)
        top_n = params.get("top_n", 3)
        lookback = params.get("lookback", 20)
        asset_type = params.get("asset_type", "industry")
        
        return f'''# -*- coding: utf-8 -*-
"""
行业/风格轮动策略
================
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
轮动周期: {rotation_period}天
选择数量: {top_n}个
"""

# ==================== 参数 ====================
ROTATION_PERIOD = {rotation_period}
TOP_N = {top_n}
LOOKBACK = {lookback}
ASSET_TYPE = "{asset_type}"

# 行业ETF映射
INDUSTRY_ETFS = {{
    "银行": "512800.XSHG",
    "证券": "512880.XSHG", 
    "医药": "512010.XSHG",
    "消费": "159928.XSHE",
    "科技": "515000.XSHG",
    "新能源": "516160.XSHG",
    "军工": "512660.XSHG",
    "半导体": "512480.XSHG",
}}

# ==================== 初始化 ====================
def initialize(context):
    set_benchmark("000300.XSHG")
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    set_slippage(FixedSlippage(0.001))
    
    g.rotation_day = 0
    g.assets = list(INDUSTRY_ETFS.values())
    
    run_daily(rotation_check, time="09:35")

# ==================== 轮动检查 ====================
def rotation_check(context):
    g.rotation_day += 1
    if g.rotation_day % ROTATION_PERIOD != 0:
        return
    
    # 计算动量
    momentum_scores = {{}}
    for asset in g.assets:
        try:
            prices = get_price(asset, end_date=context.current_dt, 
                             frequency="daily", fields=["close"], count=LOOKBACK)
            if len(prices) >= LOOKBACK:
                momentum = (prices["close"].iloc[-1] / prices["close"].iloc[0]) - 1
                momentum_scores[asset] = momentum
        except:
            pass
    
    # 选择前N个
    sorted_assets = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    selected = [a[0] for a in sorted_assets[:TOP_N]]
    
    # 调仓
    current_holdings = set(context.portfolio.positions.keys())
    target_holdings = set(selected)
    
    # 卖出不在目标中的
    for stock in current_holdings - target_holdings:
        order_target(stock, 0)
    
    # 买入目标
    if selected:
        weight = 1.0 / len(selected)
        for stock in selected:
            order_target_value(stock, context.portfolio.total_value * weight * 0.95)
    
    log.info(f"轮动调仓: {{selected}}")
'''


class PairTradingTemplate(BaseTemplate):
    """
    配对交易策略模板
    基于协整关系进行统计套利
    """
    
    name = "pair_trading"
    description = "配对交易（统计套利）策略"
    params = [
        TemplateParam("stock_a", "str", "600519.XSHG", "股票A代码"),
        TemplateParam("stock_b", "str", "000858.XSHE", "股票B代码"),
        TemplateParam("lookback", "int", 60, "回看周期", 20, 252),
        TemplateParam("entry_threshold", "float", 2.0, "开仓阈值（标准差倍数）", 1.0, 3.0),
        TemplateParam("exit_threshold", "float", 0.5, "平仓阈值", 0.0, 1.0),
    ]
    
    def generate_code(self, params: Dict) -> str:
        stock_a = params.get("stock_a", "600519.XSHG")
        stock_b = params.get("stock_b", "000858.XSHE")
        lookback = params.get("lookback", 60)
        entry = params.get("entry_threshold", 2.0)
        exit_t = params.get("exit_threshold", 0.5)
        
        return f'''# -*- coding: utf-8 -*-
"""
配对交易策略
===========
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
配对: {stock_a} vs {stock_b}
"""

import numpy as np

# ==================== 参数 ====================
STOCK_A = "{stock_a}"
STOCK_B = "{stock_b}"
LOOKBACK = {lookback}
ENTRY_THRESHOLD = {entry}
EXIT_THRESHOLD = {exit_t}

# ==================== 初始化 ====================
def initialize(context):
    set_benchmark("000300.XSHG")
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    set_slippage(FixedSlippage(0.001))
    
    g.position_type = None  # "long_spread" or "short_spread"
    
    run_daily(pair_trading, time="09:35")

# ==================== 配对交易 ====================
def pair_trading(context):
    # 获取价格数据
    prices_a = get_price(STOCK_A, end_date=context.current_dt, 
                        frequency="daily", fields=["close"], count=LOOKBACK)
    prices_b = get_price(STOCK_B, end_date=context.current_dt,
                        frequency="daily", fields=["close"], count=LOOKBACK)
    
    if len(prices_a) < LOOKBACK or len(prices_b) < LOOKBACK:
        return
    
    # 计算价差（简化版：对数价格差）
    log_a = np.log(prices_a["close"])
    log_b = np.log(prices_b["close"])
    spread = log_a.values - log_b.values
    
    # 计算z-score
    mean_spread = spread.mean()
    std_spread = spread.std()
    if std_spread == 0:
        return
    
    current_spread = spread[-1]
    z_score = (current_spread - mean_spread) / std_spread
    
    # 交易逻辑
    if g.position_type is None:
        if z_score > ENTRY_THRESHOLD:
            # 做空价差：卖A买B
            order_target_value(STOCK_A, -context.portfolio.total_value * 0.45)
            order_target_value(STOCK_B, context.portfolio.total_value * 0.45)
            g.position_type = "short_spread"
            log.info(f"开仓做空价差 z={{z_score:.2f}}")
            
        elif z_score < -ENTRY_THRESHOLD:
            # 做多价差：买A卖B
            order_target_value(STOCK_A, context.portfolio.total_value * 0.45)
            order_target_value(STOCK_B, -context.portfolio.total_value * 0.45)
            g.position_type = "long_spread"
            log.info(f"开仓做多价差 z={{z_score:.2f}}")
    
    else:
        # 平仓检查
        if abs(z_score) < EXIT_THRESHOLD:
            order_target(STOCK_A, 0)
            order_target(STOCK_B, 0)
            log.info(f"平仓 z={{z_score:.2f}}")
            g.position_type = None
'''


class MeanReversionTemplate(BaseTemplate):
    """
    均值回归策略模板
    """
    
    name = "mean_reversion"
    description = "均值回归策略"
    params = [
        TemplateParam("lookback", "int", 20, "回看周期", 5, 60),
        TemplateParam("entry_std", "float", 2.0, "开仓标准差", 1.0, 3.0),
        TemplateParam("exit_std", "float", 0.5, "平仓标准差", 0.0, 1.5),
        TemplateParam("max_stocks", "int", 10, "最大持股数", 5, 30),
    ]
    
    def generate_code(self, params: Dict) -> str:
        lookback = params.get("lookback", 20)
        entry_std = params.get("entry_std", 2.0)
        exit_std = params.get("exit_std", 0.5)
        max_stocks = params.get("max_stocks", 10)
        
        return f'''# -*- coding: utf-8 -*-
"""
均值回归策略
===========
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import numpy as np

# ==================== 参数 ====================
LOOKBACK = {lookback}
ENTRY_STD = {entry_std}
EXIT_STD = {exit_std}
MAX_STOCKS = {max_stocks}

# ==================== 初始化 ====================
def initialize(context):
    set_benchmark("000300.XSHG")
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    set_slippage(FixedSlippage(0.001))
    
    g.stock_pool = get_index_stocks("000300.XSHG")
    
    run_daily(mean_reversion, time="09:35")
    run_daily(check_exit, time="14:50")

# ==================== 均值回归选股 ====================
def mean_reversion(context):
    # 计算所有股票的z-score
    candidates = []
    
    for stock in g.stock_pool[:100]:  # 限制计算量
        try:
            prices = get_price(stock, end_date=context.current_dt,
                             frequency="daily", fields=["close"], count=LOOKBACK+5)
            if len(prices) < LOOKBACK:
                continue
            
            close = prices["close"]
            ma = close.rolling(LOOKBACK).mean().iloc[-1]
            std = close.rolling(LOOKBACK).std().iloc[-1]
            
            if std > 0:
                z_score = (close.iloc[-1] - ma) / std
                if z_score < -ENTRY_STD:  # 超跌
                    candidates.append((stock, z_score))
        except:
            pass
    
    # 选择最超跌的
    candidates.sort(key=lambda x: x[1])
    selected = [c[0] for c in candidates[:MAX_STOCKS]]
    
    # 调仓
    current = set(context.portfolio.positions.keys())
    target = set(selected)
    
    # 卖出
    for stock in current - target:
        order_target(stock, 0)
    
    # 买入
    if selected:
        weight = 0.9 / len(selected)
        for stock in selected:
            order_target_value(stock, context.portfolio.total_value * weight)

# ==================== 检查平仓 ====================
def check_exit(context):
    for stock in list(context.portfolio.positions.keys()):
        try:
            prices = get_price(stock, end_date=context.current_dt,
                             frequency="daily", fields=["close"], count=LOOKBACK)
            close = prices["close"]
            ma = close.mean()
            std = close.std()
            
            if std > 0:
                z_score = (close.iloc[-1] - ma) / std
                if z_score > EXIT_STD:  # 回归均值，平仓
                    order_target(stock, 0)
                    log.info(f"{{stock}} 回归均值平仓 z={{z_score:.2f}}")
        except:
            pass
'''


class BreakoutTemplate(BaseTemplate):
    """
    突破策略模板
    """
    
    name = "breakout"
    description = "价格突破策略"
    params = [
        TemplateParam("channel_period", "int", 20, "通道周期", 10, 60),
        TemplateParam("atr_period", "int", 14, "ATR周期", 5, 30),
        TemplateParam("atr_multiplier", "float", 2.0, "ATR倍数止损", 1.0, 4.0),
        TemplateParam("max_stocks", "int", 5, "最大持股数", 3, 20),
    ]
    
    def generate_code(self, params: Dict) -> str:
        channel = params.get("channel_period", 20)
        atr_period = params.get("atr_period", 14)
        atr_mult = params.get("atr_multiplier", 2.0)
        max_stocks = params.get("max_stocks", 5)
        
        return f'''# -*- coding: utf-8 -*-
"""
价格突破策略（唐奇安通道）
=======================
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import numpy as np

# ==================== 参数 ====================
CHANNEL_PERIOD = {channel}
ATR_PERIOD = {atr_period}
ATR_MULTIPLIER = {atr_mult}
MAX_STOCKS = {max_stocks}

# ==================== 初始化 ====================
def initialize(context):
    set_benchmark("000300.XSHG")
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    set_slippage(FixedSlippage(0.001))
    
    g.stock_pool = get_index_stocks("000300.XSHG")
    g.stop_prices = {{}}
    
    run_daily(breakout_entry, time="09:35")
    run_daily(trailing_stop, time="14:50")

# ==================== 突破入场 ====================
def breakout_entry(context):
    if len(context.portfolio.positions) >= MAX_STOCKS:
        return
    
    for stock in g.stock_pool[:50]:
        if stock in context.portfolio.positions:
            continue
        
        try:
            prices = get_price(stock, end_date=context.current_dt,
                             frequency="daily", 
                             fields=["open", "high", "low", "close"],
                             count=CHANNEL_PERIOD + 5)
            
            if len(prices) < CHANNEL_PERIOD:
                continue
            
            # 唐奇安通道
            high_n = prices["high"].iloc[:-1].rolling(CHANNEL_PERIOD).max().iloc[-1]
            current_price = prices["close"].iloc[-1]
            
            if current_price > high_n:
                # 计算ATR止损
                tr = np.maximum(
                    prices["high"] - prices["low"],
                    np.abs(prices["high"] - prices["close"].shift(1)),
                    np.abs(prices["low"] - prices["close"].shift(1))
                )
                atr = tr.rolling(ATR_PERIOD).mean().iloc[-1]
                stop_price = current_price - ATR_MULTIPLIER * atr
                
                # 买入
                weight = 0.9 / MAX_STOCKS
                order_target_value(stock, context.portfolio.total_value * weight)
                g.stop_prices[stock] = stop_price
                log.info(f"{{stock}} 突破买入, 止损={{stop_price:.2f}}")
                
                if len(context.portfolio.positions) >= MAX_STOCKS:
                    break
        except:
            pass

# ==================== 移动止损 ====================
def trailing_stop(context):
    for stock in list(context.portfolio.positions.keys()):
        try:
            prices = get_price(stock, end_date=context.current_dt,
                             frequency="daily",
                             fields=["high", "low", "close"],
                             count=ATR_PERIOD + 1)
            
            current_price = prices["close"].iloc[-1]
            
            # 更新止损
            tr = np.maximum(
                prices["high"] - prices["low"],
                np.abs(prices["high"] - prices["close"].shift(1)),
                np.abs(prices["low"] - prices["close"].shift(1))
            )
            atr = tr.rolling(ATR_PERIOD).mean().iloc[-1]
            new_stop = current_price - ATR_MULTIPLIER * atr
            
            if stock in g.stop_prices:
                g.stop_prices[stock] = max(g.stop_prices[stock], new_stop)
                
                if current_price < g.stop_prices[stock]:
                    order_target(stock, 0)
                    del g.stop_prices[stock]
                    log.info(f"{{stock}} 触发止损")
        except:
            pass
'''


# 模板注册
ADVANCED_TEMPLATES = {
    "rotation": RotationTemplate(),
    "pair_trading": PairTradingTemplate(),
    "mean_reversion": MeanReversionTemplate(),
    "breakout": BreakoutTemplate(),
}


def get_advanced_template(name: str) -> BaseTemplate:
    """获取高级模板"""
    return ADVANCED_TEMPLATES.get(name)


def list_advanced_templates() -> List[str]:
    """列出所有高级模板"""
    return list(ADVANCED_TEMPLATES.keys())
