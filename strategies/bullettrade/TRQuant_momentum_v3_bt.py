# -*- coding: utf-8 -*-
"""
TRQuant激进动量策略V3 - BulletTrade版本
======================================
基于5日+20日双动量的选股策略

数据源: 聚宽JQData
回测引擎: BulletTrade

策略逻辑:
1. 5日动量 > 0
2. 20日动量 > 0
3. 按综合动量得分排序
4. 选择TOP5买入
"""

from jqdata import *
import numpy as np
import pandas as pd

# ==================== 策略参数 ====================
MAX_STOCKS = 5              # 最大持股数量
SINGLE_POSITION = 0.18      # 单票最大仓位
MIN_CASH_RATIO = 0.10       # 最低现金保留

REBALANCE_DAYS = 5          # 调仓周期
MOMENTUM_SHORT = 5          # 短期动量
MOMENTUM_LONG = 20          # 长期动量

STOP_LOSS = -0.08           # 止损线
TAKE_PROFIT = 0.30          # 止盈线


# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    context.stock_pool = []
    context.trade_count = 0
    context.cost_prices = {}
    context.highest_prices = {}
    
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:35')
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 50)
    log.info('策略初始化: TRQuant激进动量V3')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info('=' * 50)


def before_market_open(context):
    """盘前准备"""
    context.trade_count += 1
    
    if context.trade_count % 20 == 1:
        try:
            context.stock_pool = get_index_stocks('000300.XSHG')
            log.info(f'更新股票池: {len(context.stock_pool)}只')
        except:
            context.stock_pool = get_all_securities(['stock']).index.tolist()[:300]


def market_open(context):
    """开盘交易"""
    if context.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{context.trade_count}天')
    
    target_stocks = select_stocks(context)
    if not target_stocks:
        log.warn('未选出股票')
        return
    
    log.info(f'选股: {target_stocks[:3]}...')
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑"""
    stocks = context.stock_pool
    if not stocks:
        log.warn('股票池为空')
        return []
    
    current_dt = context.current_dt.strftime('%Y-%m-%d')
    
    stocks = filter_stocks(context, stocks)
    log.info(f'过滤后股票数: {len(stocks)}')
    
    if len(stocks) < MAX_STOCKS:
        log.warn(f'股票数量不足: {len(stocks)} < {MAX_STOCKS}')
        return stocks[:MAX_STOCKS] if stocks else []
    
    try:
        # 限制股票数量，避免数据获取超时
        test_stocks = stocks[:50] if len(stocks) > 50 else stocks
        
        prices = get_price(test_stocks, end_date=current_dt, frequency='daily',
                          fields=['close'], count=MOMENTUM_LONG+5, panel=False)
        
        if prices is None or prices.empty:
            log.warn('获取价格数据为空')
            return []
        
        # 处理不同的数据格式
        if 'time' in prices.columns and 'code' in prices.columns:
            price_pivot = prices.pivot(index='time', columns='code', values='close')
        elif isinstance(prices, pd.DataFrame) and len(prices.columns) > 0:
            # 如果已经是宽表格式
            price_pivot = prices
        else:
            log.warn(f'价格数据格式异常: {type(prices)}')
            return []
        
        if price_pivot.empty or len(price_pivot) < MOMENTUM_LONG:
            log.warn('价格数据不足')
            return []
        
        # 计算动量
        mom_short = price_pivot.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = price_pivot.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 筛选条件
        valid = (mom_short > 0) & (mom_long > 0)
        score = (mom_short * 0.5 + mom_long * 0.5).where(valid).dropna()
        
        if len(score) < MAX_STOCKS:
            # 放宽条件
            score = (mom_short * 0.5 + mom_long * 0.5).dropna()
        
        if len(score) == 0:
            log.warn('无符合条件的股票')
            return []
        
        selected = score.nlargest(MAX_STOCKS).index.tolist()
        log.info(f'选股成功: {len(selected)}只')
        return selected
        
    except Exception as e:
        import traceback
        log.error(f'选股异常: {e}')
        log.error(traceback.format_exc())
        return []


def rebalance(context, target_stocks):
    """调仓"""
    current_stocks = list(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    current_set = set(current_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    # 卖出
    for stock in current_set - target_set:
        order_target_value(stock, 0)
        log.info(f'[卖出] {stock}')
        context.cost_prices.pop(stock, None)
        context.highest_prices.pop(stock, None)
    
    # 买入
    current_data = get_current_data()
    for stock in target_stocks:
        if stock in current_data:
            data = current_data[stock]
            # 检查停牌
            if hasattr(data, 'paused') and data.paused:
                continue
            # 检查涨停 (BulletTrade兼容)
            try:
                open_price = getattr(data, 'open', None) or getattr(data, 'day_open', None)
                high_limit = getattr(data, 'high_limit', None)
                if open_price and high_limit and open_price == high_limit:
                    continue
            except:
                pass
        
        current_value = 0
        if stock in context.portfolio.positions:
            current_value = context.portfolio.positions[stock].value
        
        if current_value < target_value * 0.9:
            order_target_value(stock, target_value)
            log.info(f'[买入] {stock} 目标:{target_value:.0f}')
            
            if stock not in context.cost_prices:
                context.cost_prices[stock] = current_data[stock].last_price
                context.highest_prices[stock] = context.cost_prices[stock]


def check_risk(context):
    """风控检查"""
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost = context.cost_prices.get(stock, pos.avg_cost)
        highest = context.highest_prices.get(stock, cost)
        
        if cost <= 0:
            continue
        
        profit = (current_price - cost) / cost
        context.highest_prices[stock] = max(highest, current_price)
        
        if profit < STOP_LOSS:
            order_target_value(stock, 0)
            log.warn(f'[止损] {stock} {profit*100:.1f}%')
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
        elif profit > TAKE_PROFIT:
            order_target_value(stock, 0)
            log.info(f'[止盈] {stock} {profit*100:.1f}%')
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
        elif profit > 0.15:
            dd = (context.highest_prices[stock] - current_price) / context.highest_prices[stock]
            if dd > 0.10:
                order_target_value(stock, 0)
                log.info(f'[移动止损] {stock} 回撤{dd*100:.1f}%')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)


def after_market_close(context):
    """收盘记录"""
    pos_count = len(context.portfolio.positions)
    total = context.portfolio.total_value
    ret = context.portfolio.returns
    log.info(f'[收盘] 持仓:{pos_count}只 资产:{total:.0f} 收益:{ret*100:.2f}%')


def filter_stocks(context, stocks):
    """过滤股票"""
    current_data = get_current_data()
    current_dt = context.current_dt
    filtered = []
    
    for stock in stocks:
        if stock not in current_data:
            continue
        
        data = current_data[stock]
        
        # 检查停牌
        if hasattr(data, 'paused') and data.paused:
            continue
        
        # 检查涨跌停 (BulletTrade使用open而非day_open)
        try:
            open_price = getattr(data, 'open', None) or getattr(data, 'day_open', None)
            high_limit = getattr(data, 'high_limit', None)
            low_limit = getattr(data, 'low_limit', None)
            
            if open_price and high_limit and open_price == high_limit:
                continue
            if open_price and low_limit and open_price == low_limit:
                continue
        except:
            pass
        
        try:
            info = get_security_info(stock)
            if (current_dt.date() - info.start_date).days < 60:
                continue
        except:
            pass
        
        filtered.append(stock)
    
    try:
        st = get_extras('is_st', filtered, 
                       start_date=current_dt.strftime('%Y-%m-%d'),
                       end_date=current_dt.strftime('%Y-%m-%d'), df=True)
        if not st.empty:
            st_list = st.columns[st.iloc[0] == True].tolist()
            filtered = [s for s in filtered if s not in st_list]
    except:
        pass
    
    return filtered

