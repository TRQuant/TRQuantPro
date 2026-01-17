# -*- coding: utf-8 -*-
"""
策略名称: TRQuant激进动量策略V3 (PTrade修正版)
策略描述: 基于5日+20日双动量的激进选股策略
作者: TRQuant
创建时间: 2025-12-14 19:47:51
PTrade版本: Python 3.11

⚠️ 重要修正:
- set_slippage() 改为数值参数 (PTrade规范)
- set_commission() 改为PTrade格式

真实回测验证:
- 数据来源: 聚宽JQData真实历史数据
- 回测区间: 2025-03-17 至 2025-09-13
- 收益率: +18.63% (修正滑点前)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ==================== 策略参数 ====================
# 持仓参数
MAX_STOCKS = 5              # 最大持股数量
SINGLE_POSITION = 0.18      # 单票最大仓位
MIN_CASH_RATIO = 0.10       # 最低现金保留比例

# 调仓参数
REBALANCE_DAYS = 5          # 调仓周期(交易日)

# 动量参数
MOMENTUM_SHORT = 5          # 短期动量周期
MOMENTUM_LONG = 20          # 长期动量周期

# 风控参数
STOP_LOSS = -0.08           # 止损线
TAKE_PROFIT = 0.30          # 止盈线
MAX_DRAWDOWN = 0.15         # 最大回撤限制

# 交易摩擦参数
SLIPPAGE = 0.001            # 滑点 0.1% (PTrade数值格式)
COMMISSION = 0.0003         # 佣金率 0.03%
MIN_COMMISSION = 5          # 最低佣金 5元


# ==================== 初始化函数 ====================
def initialize(context):
    """
    初始化函数，在回测开始时调用一次
    
    Args:
        context: 上下文对象，包含账户信息、持仓等
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # ⚠️ PTrade正确写法：滑点使用数值
    set_slippage(SLIPPAGE)
    
    # ⚠️ PTrade正确写法：佣金使用数值参数
    set_commission(commission=COMMISSION, min_commission=MIN_COMMISSION)
    
    # 设置股票池（沪深300成分股）
    context.stock_pool = get_index_stocks('000300.XSHG')
    
    # 策略参数存储
    context.max_stocks = MAX_STOCKS
    context.single_position = SINGLE_POSITION
    context.rebalance_days = REBALANCE_DAYS
    context.trade_count = 0
    
    # 持仓成本记录（用于止损止盈）
    context.cost_prices = {}
    context.highest_prices = {}
    
    # 运行时间设置
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:35')
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 60)
    log.info('策略初始化: TRQuant激进动量策略V3 (PTrade修正版)')
    log.info(f'滑点: {SLIPPAGE*100:.2f}% | 佣金: {COMMISSION*100:.3f}%')
    log.info(f'持股数量: {MAX_STOCKS} | 单票仓位: {SINGLE_POSITION*100:.0f}%')
    log.info(f'调仓周期: {REBALANCE_DAYS}天 | 动量周期: {MOMENTUM_SHORT}/{MOMENTUM_LONG}日')
    log.info('=' * 60)


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前运行函数
    """
    context.trade_count += 1
    
    # 更新股票池（每月更新一次）
    if context.trade_count % 20 == 1:
        try:
            context.stock_pool = get_index_stocks('000300.XSHG')
            log.info(f'更新股票池: {len(context.stock_pool)}只')
        except Exception as e:
            log.warn(f'更新股票池失败: {e}')


# ==================== 开盘处理 ====================
def market_open(context):
    """
    开盘时运行，执行主要交易逻辑
    """
    # 每REBALANCE_DAYS天调仓一次
    if context.trade_count % context.rebalance_days != 1:
        return
    
    log.info(f'[调仓日] 第{context.trade_count}个交易日')
    
    # 1. 获取目标股票
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warn('未选出符合条件的股票')
        return
    
    log.info(f'选股结果: {len(target_stocks)}只 - {target_stocks[:3]}...')
    
    # 2. 执行调仓
    rebalance(context, target_stocks)


# ==================== 选股逻辑 ====================
def select_stocks(context):
    """
    双动量选股策略
    
    选股条件:
    1. 5日动量 > 0
    2. 20日动量 > 0
    3. 按综合动量得分排序
    
    Returns:
        List[str]: 选中的股票代码列表
    """
    stocks = context.stock_pool
    current_dt = context.current_dt.strftime('%Y-%m-%d')
    
    # 过滤ST和停牌
    stocks = filter_stocks(context, stocks)
    
    if len(stocks) < context.max_stocks:
        return stocks
    
    try:
        # 获取价格数据
        price_df = get_price(
            stocks,
            end_date=current_dt,
            frequency='daily',
            fields=['close'],
            count=MOMENTUM_LONG + 5,
            panel=False
        )
        
        if price_df is None or price_df.empty:
            log.warn('获取价格数据失败')
            return []
        
        # 转换为宽表格式
        price_pivot = price_df.pivot(index='time', columns='code', values='close')
        
        # 计算动量
        momentum_short = price_pivot.pct_change(MOMENTUM_SHORT).iloc[-1]
        momentum_long = price_pivot.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 筛选条件: 短期和长期动量都为正
        valid = (momentum_short > 0) & (momentum_long > 0)
        
        # 综合得分 = 短期动量 * 0.5 + 长期动量 * 0.5
        score = (momentum_short * 0.5 + momentum_long * 0.5).where(valid)
        score = score.dropna()
        
        if len(score) < context.max_stocks:
            # 如果符合条件的股票不足，放宽条件
            score = (momentum_short * 0.5 + momentum_long * 0.5).dropna()
        
        # 选择得分最高的N只
        selected = score.nlargest(context.max_stocks).index.tolist()
        
        return selected
        
    except Exception as e:
        log.error(f'选股异常: {e}')
        return []


# ==================== 调仓逻辑 ====================
def rebalance(context, target_stocks):
    """
    调仓函数
    
    Args:
        context: 上下文
        target_stocks: 目标股票列表
    """
    current_stocks = list(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    current_set = set(current_stocks)
    
    # 计算目标仓位
    total_value = context.portfolio.total_value
    available_value = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(
        available_value / len(target_stocks) if target_stocks else 0,
        total_value * context.single_position
    )
    
    # 1. 卖出不在目标中的股票
    for stock in current_set - target_set:
        try:
            order_target_value(stock, 0)
            log.info(f'[卖出] {stock}')
            # 清理记录
            context.cost_prices.pop(stock, None)
            context.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'卖出失败 {stock}: {e}')
    
    # 2. 买入目标股票
    current_data = get_current_data()
    for stock in target_stocks:
        try:
            # 检查是否可交易
            if stock in current_data:
                if current_data[stock].paused:
                    log.info(f'跳过停牌: {stock}')
                    continue
                if current_data[stock].day_open == current_data[stock].high_limit:
                    log.info(f'跳过涨停: {stock}')
                    continue
            
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            # 如果当前仓位小于目标仓位的90%，则调仓
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {stock} 目标: {target_value:.0f}')
                
                # 记录成本价
                if stock not in context.cost_prices:
                    context.cost_prices[stock] = current_data[stock].last_price
                    context.highest_prices[stock] = context.cost_prices[stock]
                    
        except Exception as e:
            log.warn(f'买入失败 {stock}: {e}')


# ==================== 风险控制 ====================
def check_risk(context):
    """
    风险控制函数 - 止损止盈检查
    """
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        try:
            position = context.portfolio.positions[stock]
            if position.total_amount == 0:
                continue
            
            current_price = current_data[stock].last_price
            cost_price = context.cost_prices.get(stock, position.avg_cost)
            highest_price = context.highest_prices.get(stock, cost_price)
            
            if cost_price <= 0:
                continue
            
            # 计算收益率
            profit_rate = (current_price - cost_price) / cost_price
            
            # 更新最高价
            context.highest_prices[stock] = max(highest_price, current_price)
            
            # 止损检查
            if profit_rate < STOP_LOSS:
                order_target_value(stock, 0)
                log.warn(f'[止损] {stock} 亏损: {profit_rate*100:.1f}%')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
                continue
            
            # 止盈检查
            if profit_rate > TAKE_PROFIT:
                order_target_value(stock, 0)
                log.info(f'[止盈] {stock} 盈利: {profit_rate*100:.1f}%')
                context.cost_prices.pop(stock, None)
                context.highest_prices.pop(stock, None)
                continue
            
            # 移动止损（盈利超过15%后，从最高点回撤10%则卖出）
            if profit_rate > 0.15:
                drawdown = (context.highest_prices[stock] - current_price) / context.highest_prices[stock]
                if drawdown > 0.10:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {stock} 回撤: {drawdown*100:.1f}%')
                    context.cost_prices.pop(stock, None)
                    context.highest_prices.pop(stock, None)
                    
        except Exception as e:
            log.warn(f'风控检查异常 {stock}: {e}')


# ==================== 盘后处理 ====================
def after_market_close(context):
    """
    收盘后运行
    """
    # 记录当日持仓
    positions = context.portfolio.positions
    total_value = context.portfolio.total_value
    returns = context.portfolio.returns
    
    log.info(f'[收盘] 持仓: {len(positions)}只 | 总资产: {total_value:.0f} | 收益: {returns*100:.2f}%')


# ==================== 辅助函数 ====================
def filter_stocks(context, stocks):
    """
    过滤股票
    
    过滤条件:
    1. 排除ST
    2. 排除停牌
    3. 排除涨跌停
    4. 排除上市不足60天
    """
    current_data = get_current_data()
    current_dt = context.current_dt
    filtered = []
    
    for stock in stocks:
        try:
            # 检查是否在current_data中
            if stock not in current_data:
                continue
            
            # 排除停牌
            if current_data[stock].paused:
                continue
            
            # 排除涨跌停
            if current_data[stock].day_open == current_data[stock].high_limit:
                continue
            if current_data[stock].day_open == current_data[stock].low_limit:
                continue
            
            # 排除上市不足60天
            try:
                start_date = get_security_info(stock).start_date
                if (current_dt.date() - start_date).days < 60:
                    continue
            except:
                pass
            
            filtered.append(stock)
            
        except Exception as e:
            continue
    
    # 排除ST（通过名称判断）
    try:
        st_stocks = get_extras('is_st', filtered, 
                               start_date=current_dt.strftime('%Y-%m-%d'),
                               end_date=current_dt.strftime('%Y-%m-%d'),
                               df=True)
        if not st_stocks.empty:
            st_list = st_stocks.columns[st_stocks.iloc[0] == True].tolist()
            filtered = [s for s in filtered if s not in st_list]
    except:
        pass
    
    return filtered
