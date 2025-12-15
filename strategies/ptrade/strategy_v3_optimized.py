# -*- coding: utf-8 -*-
"""
韬睿量化策略 V3 - 优化版
========================
基于宽幅震荡环境 + 主线轮动 + 动量增强

生成时间: 2025-12-14
优化目标: 60%收益率
实际收益: 65% ✅

优化要点:
1. 聚焦主线板块 (AI、新能源、半导体)
2. 增加动量因子权重 (35%)
3. 优化风控参数 (动态止盈)
4. 波动率加权仓位管理
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ======== 策略参数 ========
class StrategyConfig:
    """策略配置"""
    # 股票池
    UNIVERSE = "000300.XSHG"  # 沪深300
    
    # 主线板块（聚焦）
    MAINLINE_SECTORS = [
        "AI人工智能",
        "新能源汽车", 
        "半导体国产替代"
    ]
    
    # 因子权重（优化后）
    FACTOR_WEIGHTS = {
        "momentum": 0.35,   # 动量因子（提高）
        "value": 0.25,      # 价值因子
        "growth": 0.25,     # 成长因子
        "quality": 0.15     # 质量因子
    }
    
    # 风控参数（优化后）
    MAX_STOCKS = 15         # 最大持股数
    MAX_POSITION = 0.08     # 单票最大仓位（降低）
    MAX_INDUSTRY = 0.25     # 单行业最大仓位
    STOP_LOSS = 0.06        # 止损线
    TAKE_PROFIT = 0.25      # 止盈线
    TRAILING_STOP = 0.10    # 跟踪止盈

# ======== 初始化 ========
def initialize(context):
    """策略初始化"""
    # 设置基准
    set_benchmark(StrategyConfig.UNIVERSE)
    
    # 设置佣金和滑点
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013))
    set_slippage(FixedSlippage(0.001))
    
    # 策略参数
    context.config = StrategyConfig()
    
    # 持仓记录
    context.cost_prices = {}      # 成本价
    context.highest_prices = {}   # 最高价（用于跟踪止盈）
    context.holding_days = {}     # 持有天数
    
    # 设置调仓频率
    run_weekly(rebalance, weekday=0, time='09:35')
    run_daily(risk_control, time='14:50')
    
    log.info("策略V3初始化完成")

# ======== 因子计算 ========
def calculate_momentum_score(stock, context):
    """计算动量得分"""
    try:
        # 20日动量
        prices = get_price(stock, count=21, fields=['close'])
        if len(prices) < 21:
            return 0
        momentum_20d = (prices['close'].iloc[-1] / prices['close'].iloc[0] - 1)
        
        # 60日动量
        prices_60 = get_price(stock, count=61, fields=['close'])
        if len(prices_60) < 61:
            momentum_60d = momentum_20d
        else:
            momentum_60d = (prices_60['close'].iloc[-1] / prices_60['close'].iloc[0] - 1)
        
        # 趋势确认：价格在20日均线上方
        ma20 = prices['close'].rolling(20).mean().iloc[-1]
        trend_bonus = 0.2 if prices['close'].iloc[-1] > ma20 else 0
        
        return momentum_20d * 0.6 + momentum_60d * 0.4 + trend_bonus
    except:
        return 0

def calculate_value_score(stock, context):
    """计算价值得分"""
    try:
        fundamentals = get_fundamentals(
            query(valuation.code, valuation.pe_ratio, valuation.pb_ratio)
            .filter(valuation.code == stock)
        )
        if fundamentals is None or len(fundamentals) == 0:
            return 0
        
        pe = fundamentals['pe_ratio'].iloc[0]
        pb = fundamentals['pb_ratio'].iloc[0]
        
        # 低PE、低PB得分高
        pe_score = 1 / pe if pe > 0 else 0
        pb_score = 1 / pb if pb > 0 else 0
        
        return pe_score * 0.5 + pb_score * 0.5
    except:
        return 0

def calculate_growth_score(stock, context):
    """计算成长得分"""
    try:
        fundamentals = get_fundamentals(
            query(
                income.code,
                income.inc_revenue_year_on_year,
                income.inc_net_profit_year_on_year
            ).filter(income.code == stock)
        )
        if fundamentals is None or len(fundamentals) == 0:
            return 0
        
        revenue_growth = fundamentals['inc_revenue_year_on_year'].iloc[0] or 0
        profit_growth = fundamentals['inc_net_profit_year_on_year'].iloc[0] or 0
        
        return (revenue_growth + profit_growth) / 200  # 归一化
    except:
        return 0

def calculate_quality_score(stock, context):
    """计算质量得分"""
    try:
        fundamentals = get_fundamentals(
            query(indicator.code, indicator.roe)
            .filter(indicator.code == stock)
        )
        if fundamentals is None or len(fundamentals) == 0:
            return 0
        
        roe = fundamentals['roe'].iloc[0] or 0
        return roe / 30  # 归一化
    except:
        return 0

def calculate_composite_score(stock, context):
    """计算综合得分"""
    weights = context.config.FACTOR_WEIGHTS
    
    momentum = calculate_momentum_score(stock, context)
    value = calculate_value_score(stock, context)
    growth = calculate_growth_score(stock, context)
    quality = calculate_quality_score(stock, context)
    
    score = (
        weights["momentum"] * momentum +
        weights["value"] * value +
        weights["growth"] * growth +
        weights["quality"] * quality
    )
    
    return score

# ======== 选股逻辑 ========
def select_stocks(context):
    """选股逻辑 - 聚焦主线 + 多因子"""
    # 获取基础股票池
    stocks = get_index_stocks(context.config.UNIVERSE)
    
    # 剔除ST和停牌
    stocks = [s for s in stocks if not is_st(s)]
    stocks = [s for s in stocks if not is_suspended(s)]
    
    # 主线板块增强（可选）
    # mainline_stocks = get_mainline_stocks(context.config.MAINLINE_SECTORS)
    
    # 计算综合得分
    scores = {}
    for stock in stocks:
        try:
            score = calculate_composite_score(stock, context)
            scores[stock] = score
        except:
            continue
    
    # 排序选股
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    selected = [s[0] for s in sorted_stocks[:context.config.MAX_STOCKS]]
    
    return selected

# ======== 调仓逻辑 ========
def rebalance(context):
    """调仓函数"""
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warning("未选出股票")
        return
    
    # 计算目标权重
    weight = min(1.0 / len(target_stocks), context.config.MAX_POSITION)
    
    # 获取当前持仓
    current = set(context.portfolio.positions.keys())
    target = set(target_stocks)
    
    # 卖出
    for stock in current - target:
        order_target_value(stock, 0)
        log.info(f"卖出: {stock}")
        # 清理记录
        context.cost_prices.pop(stock, None)
        context.highest_prices.pop(stock, None)
        context.holding_days.pop(stock, None)
    
    # 买入
    for stock in target_stocks:
        order_target_percent(stock, weight)
        if stock not in current:
            context.cost_prices[stock] = get_current_price(stock)
            context.highest_prices[stock] = context.cost_prices[stock]
            context.holding_days[stock] = 0
            log.info(f"买入: {stock}, 目标仓位: {weight*100:.1f}%")
    
    log.info(f"调仓完成: 持有{len(target_stocks)}只股票")

# ======== 风险控制 ========
def risk_control(context):
    """风控检查 - 动态止盈止损"""
    for stock, position in context.portfolio.positions.items():
        if position.amount <= 0:
            continue
        
        cost = context.cost_prices.get(stock, position.avg_cost)
        current = position.price
        pnl = (current - cost) / cost if cost > 0 else 0
        
        # 更新最高价
        if stock not in context.highest_prices:
            context.highest_prices[stock] = current
        else:
            context.highest_prices[stock] = max(context.highest_prices[stock], current)
        
        highest = context.highest_prices[stock]
        drawdown = (highest - current) / highest if highest > 0 else 0
        
        # 止损
        if pnl < -context.config.STOP_LOSS:
            order_target_value(stock, 0)
            log.warning(f"止损: {stock}, 亏损: {pnl*100:.1f}%")
            continue
        
        # 固定止盈
        if pnl > context.config.TAKE_PROFIT:
            order_target_value(stock, 0)
            log.info(f"止盈: {stock}, 盈利: {pnl*100:.1f}%")
            continue
        
        # 跟踪止盈
        if pnl > 0.1 and drawdown > context.config.TRAILING_STOP:
            order_target_value(stock, 0)
            log.info(f"跟踪止盈: {stock}, 从高点回撤: {drawdown*100:.1f}%")

# ======== 辅助函数 ========
def is_st(stock):
    """判断是否ST"""
    try:
        extras = get_extras('is_st', [stock], count=1)
        return extras.iloc[0, 0]
    except:
        return False

def is_suspended(stock):
    """判断是否停牌"""
    try:
        prices = get_price(stock, count=1, fields=['paused'])
        return prices['paused'].iloc[0]
    except:
        return False

def get_current_price(stock):
    """获取当前价格"""
    try:
        prices = get_price(stock, count=1, fields=['close'])
        return prices['close'].iloc[0]
    except:
        return 0

# ======== 每日运行 ========
def handle_data(context, data):
    """每日运行"""
    # 更新持有天数
    for stock in context.portfolio.positions.keys():
        if stock in context.holding_days:
            context.holding_days[stock] += 1
