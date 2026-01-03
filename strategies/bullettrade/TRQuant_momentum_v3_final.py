# -*- coding: utf-8 -*-
"""
TRQuant激进动量策略V3 - BulletTrade最终优化版
======================================
基于3日+15日双动量的选股策略（最终优化版）

优化点:
1. 更激进的参数设置（目标年化60%+）
2. 更宽松的选股条件
3. 增强的错误处理和兜底策略
4. 优化的风控参数
"""

from jqdata import *
import numpy as np
import pandas as pd

# ==================== 策略参数 ====================
MAX_STOCKS = 10             # 最大持股数量（增加）
SINGLE_POSITION = 0.22      # 单票最大仓位（增加）
MIN_CASH_RATIO = 0.05       # 最低现金保留（降低）

REBALANCE_DAYS = 2          # 调仓周期（更频繁）
MOMENTUM_SHORT = 3          # 短期动量
MOMENTUM_LONG = 15          # 长期动量

STOP_LOSS = -0.05           # 止损线（更紧）
TAKE_PROFIT = 0.20          # 止盈线（降低）
TRAILING_STOP = 0.08        # 移动止损（回撤8%）

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
    log.info('策略初始化: TRQuant激进动量V3 (最终优化版)')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info(f'调仓周期: {REBALANCE_DAYS}天 | 动量: {MOMENTUM_SHORT}/{MOMENTUM_LONG}日')
    log.info('=' * 50)


def before_market_open(context):
    """盘前准备"""
    context.trade_count += 1
    
    if context.trade_count % 20 == 1:
        try:
            context.stock_pool = get_index_stocks('000300.XSHG')
            log.info(f'[盘前] 更新股票池: {len(context.stock_pool)}只')
        except Exception as e:
            log.warn(f'[盘前] 获取指数成分股失败: {e}')
            try:
                all_stocks = get_all_securities(['stock']).index.tolist()
                context.stock_pool = all_stocks[:300]
                log.info(f'[盘前] 使用全市场股票池: {len(context.stock_pool)}只')
            except:
                context.stock_pool = []


def market_open(context):
    """开盘交易"""
    if context.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{context.trade_count}个交易日')
    
    target_stocks = select_stocks(context)
    if not target_stocks:
        log.warn('[调仓] 未选出股票，保持空仓')
        return
    
    log.info(f'[调仓] 选股结果: {len(target_stocks)}只 - {target_stocks[:3]}...')
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑 - 最终优化版"""
    stocks = context.stock_pool
    if not stocks:
        log.warn('[选股] 股票池为空')
        return []
    
    current_dt = context.current_dt.strftime('%Y-%m-%d')
    log.info(f'[选股] 开始选股，股票池: {len(stocks)}只')
    
    # 过滤股票
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {len(stocks)}只')
    
    if len(stocks) < MAX_STOCKS:
        log.warn(f'[选股] 股票数量不足: {len(stocks)} < {MAX_STOCKS}')
        if stocks:
            return stocks[:MAX_STOCKS]
        return []
    
    try:
        # 限制股票数量，避免数据获取超时
        test_stocks = stocks[:50] if len(stocks) > 50 else stocks
        log.info(f'[选股] 获取价格数据: {len(test_stocks)}只股票')
        
        prices = get_price(test_stocks, end_date=current_dt, frequency='daily',
                          fields=['close'], count=MOMENTUM_LONG+5, panel=False)
        
        if prices is None or prices.empty:
            log.warn('[选股] 获取价格数据为空，使用兜底策略')
            return fallback_select(context, stocks)
        
        log.info(f'[选股] 价格数据: {len(prices)}条记录')
        
        # 处理数据格式
        if 'time' in prices.columns and 'code' in prices.columns:
            price_pivot = prices.pivot(index='time', columns='code', values='close')
        elif isinstance(prices, pd.DataFrame) and len(prices.columns) > 0:
            price_pivot = prices
        else:
            log.warn(f'[选股] 价格数据格式异常: {type(prices)}')
            return fallback_select(context, stocks)
        
        if price_pivot.empty or len(price_pivot) < MOMENTUM_LONG:
            log.warn(f'[选股] 价格数据不足: {len(price_pivot)} < {MOMENTUM_LONG}')
            return fallback_select(context, stocks)
        
        # 计算动量
        mom_short = price_pivot.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = price_pivot.pct_change(MOMENTUM_LONG).iloc[-1]
        
        log.info(f'[选股] 动量计算完成: 短期{len(mom_short.dropna())}只, 长期{len(mom_long.dropna())}只')
        
        # 最终优化：更宽松的选股条件
        # 方案1: 至少一个动量>0（最宽松）
        valid1 = (mom_short > 0) | (mom_long > 0)
        score1 = (mom_short * 0.6 + mom_long * 0.4).where(valid1).dropna()
        
        # 方案2: 两个动量都>0（严格）
        valid2 = (mom_short > 0) & (mom_long > 0)
        score2 = (mom_short * 0.6 + mom_long * 0.4).where(valid2).dropna()
        
        # 优先使用严格条件，不足时使用宽松条件
        if len(score2) >= MAX_STOCKS:
            score = score2
            log.info(f'[选股] 使用严格条件: {len(score)}只符合')
        elif len(score1) >= MAX_STOCKS:
            score = score1
            log.info(f'[选股] 使用宽松条件: {len(score)}只符合')
        else:
            # 如果还是不够，使用综合得分（不限制符号，选择动量最强的）
            score = (mom_short * 0.6 + mom_long * 0.4).dropna()
            log.info(f'[选股] 使用综合得分: {len(score)}只')
        
        if len(score) == 0:
            log.warn('[选股] 无符合条件的股票，使用兜底策略')
            return fallback_select(context, stocks)
        
        selected = score.nlargest(MAX_STOCKS).index.tolist()
        log.info(f'[选股] 选股成功: {len(selected)}只 - {selected}')
        return selected
        
    except Exception as e:
        import traceback
        log.error(f'[选股] 选股异常: {e}')
        log.error(traceback.format_exc())
        return fallback_select(context, stocks)


def fallback_select(context, stocks):
    """兜底选股策略"""
    log.info('[选股] 使用兜底策略: 直接选择前N只')
    if stocks:
        selected = stocks[:MAX_STOCKS]
        log.info(f'[选股] 最终兜底: {len(selected)}只')
        return selected
    return []


def rebalance(context, target_stocks):
    """调仓"""
    current_stocks = list(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    current_set = set(current_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    log.info(f'[调仓] 目标仓位: {target_value:.0f}/只, 共{len(target_stocks)}只')
    
    # 卖出
    sell_count = 0
    for stock in current_set - target_set:
        try:
            order_target_value(stock, 0)
            log.info(f'[卖出] {stock}')
            sell_count += 1
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[卖出失败] {stock}: {e}')
    
    if sell_count > 0:
        log.info(f'[调仓] 卖出完成: {sell_count}只')
    
    # 买入
    buy_count = 0
    current_data = get_current_data()
    for stock in target_stocks:
        try:
            if stock in current_data:
                data = current_data[stock]
                if hasattr(data, 'paused') and data.paused:
                    log.info(f'[跳过] {stock} 停牌')
                    continue
                try:
                    open_price = getattr(data, 'open', None) or getattr(data, 'day_open', None)
                    high_limit = getattr(data, 'high_limit', None)
                    if open_price and high_limit and open_price == high_limit:
                        log.info(f'[跳过] {stock} 涨停')
                        continue
                except:
                    pass
            
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {stock} 目标:{target_value:.0f}')
                buy_count += 1
                
                if stock not in context.cost_prices:
                    if stock in current_data:
                        context.cost_prices[stock] = current_data[stock].last_price
                        context.highest_prices[stock] = context.cost_prices[stock]
        except Exception as e:
            log.warn(f'[买入失败] {stock}: {e}')
    
    if buy_count > 0:
        log.info(f'[调仓] 买入完成: {buy_count}只')
    else:
        log.warn('[调仓] 未执行任何买入')


def check_risk(context):
    """风控检查"""
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        try:
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
            
            # 止损
            if profit < STOP_LOSS:
                order_target_value(stock, 0)
                log.warn(f'[止损] {stock} {profit*100:.1f}%')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
            # 止盈
            elif profit > TAKE_PROFIT:
                order_target_value(stock, 0)
                log.info(f'[止盈] {stock} {profit*100:.1f}%')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
            # 移动止损
            elif profit > 0.10:
                dd = (context.highest_prices[stock] - current_price) / context.highest_prices[stock]
                if dd > TRAILING_STOP:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {stock} 回撤{dd*100:.1f}%')
                    context.cost_prices.pop(stock, None)
                    context.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[风控检查异常] {stock}: {e}')


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
        try:
            if stock not in current_data:
                continue
            
            data = current_data[stock]
            
            if hasattr(data, 'paused') and data.paused:
                continue
            
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
        except:
            continue
    
    try:
        st = get_extras('is_st', filtered[:100], 
                       start_date=current_dt.strftime('%Y-%m-%d'),
                       end_date=current_dt.strftime('%Y-%m-%d'), df=True)
        if not st.empty:
            st_list = st.columns[st.iloc[0] == True].tolist()
            filtered = [s for s in filtered if s not in st_list]
    except:
        pass
    
    return filtered

