# -*- coding: utf-8 -*-
"""
韬睿量化 - 多因子策略 (PTrade V3)
================================

基于PTrade API规范编写
参考文档: https://ptradeapi.com/

因子: EP(价值), ROE(质量), 反转(动量)
股票池: 沪深300
持仓数量: 30只
调仓频率: 月度
"""

import pandas as pd
import numpy as np

# ==================== 策略参数 ====================
g_stock_pool = '000300.XSHG'  # 沪深300
g_hold_num = 30               # 持仓数量
g_weights = {'EP': 0.3, 'ROE': 0.3, 'Reversal': 0.4}
g_last_month = -1             # 上次调仓月份


def initialize(context):
    """
    初始化函数 (必选)
    """
    # 设置基准
    set_benchmark('000300.XSHG')
    
    log.info('='*50)
    log.info('多因子策略初始化完成')
    log.info('='*50)


def handle_data(context, data):
    """
    行情处理函数 (必选)
    每个交易bar执行一次
    """
    global g_last_month
    
    # 获取当前日期
    current_dt = context.current_dt
    current_month = current_dt.month
    current_hour = current_dt.hour
    current_minute = current_dt.minute
    
    # 只在09:35执行调仓检查
    if current_hour == 9 and current_minute == 35:
        # 判断是否是新的月份
        if current_month != g_last_month:
            log.info('='*50)
            log.info('月度调仓日: %s' % current_dt.strftime('%Y-%m-%d'))
            
            # 执行调仓
            rebalance(context)
            
            # 更新记录
            g_last_month = current_month
            log.info('='*50)


def rebalance(context):
    """
    执行月度调仓
    """
    global g_stock_pool, g_hold_num
    
    # 获取当前日期
    date_str = context.current_dt.strftime('%Y-%m-%d')
    
    # 获取股票池
    stocks = get_stock_pool()
    log.info('股票池数量: %d' % len(stocks))
    
    if len(stocks) == 0:
        log.warn('股票池为空，跳过调仓')
        return
    
    # 计算复合因子得分
    scores = calculate_composite_score(stocks, context)
    
    if scores is None or len(scores) == 0:
        log.warn('因子计算失败，跳过调仓')
        return
    
    # 选择得分最高的股票
    scores = scores.dropna().sort_values(ascending=False)
    target_stocks = scores.head(g_hold_num).index.tolist()
    log.info('目标持仓: %d只' % len(target_stocks))
    
    # 执行调仓
    execute_rebalance(context, target_stocks)


def get_stock_pool():
    """获取股票池"""
    global g_stock_pool
    
    # 获取指数成分股
    stocks = get_index_stocks(g_stock_pool)
    
    # 过滤ST股票
    filtered = []
    for stock in stocks:
        try:
            name = get_stock_name(stock)
            if name and 'ST' not in name:
                filtered.append(stock)
        except:
            filtered.append(stock)  # 获取失败则保留
    
    return filtered


def calculate_composite_score(stocks, context):
    """计算复合因子得分"""
    global g_weights
    
    try:
        # 计算各因子
        ep_factor = calculate_ep_factor(stocks)
        roe_factor = calculate_roe_factor(stocks)
        reversal_factor = calculate_reversal_factor(stocks)
        
        # 合并因子
        df = pd.DataFrame({
            'EP': ep_factor,
            'ROE': roe_factor,
            'Reversal': reversal_factor
        })
        
        ep_count = len(ep_factor.dropna()) if len(ep_factor) > 0 else 0
        roe_count = len(roe_factor.dropna()) if len(roe_factor) > 0 else 0
        rev_count = len(reversal_factor.dropna()) if len(reversal_factor) > 0 else 0
        log.info('因子计算: EP=%d, ROE=%d, Rev=%d' % (ep_count, roe_count, rev_count))
        
        # 标准化
        for col in df.columns:
            df[col] = zscore_normalize(df[col])
        
        # 加权组合
        score = pd.Series(0.0, index=df.index)
        for factor, weight in g_weights.items():
            if factor in df.columns:
                score = score + df[factor].fillna(0) * weight
        
        return score
        
    except Exception as e:
        log.error('因子计算异常: %s' % str(e))
        return None


def calculate_ep_factor(stocks):
    """计算EP因子 (盈利收益率 = 1/PE)"""
    ep_values = {}
    
    for stock in stocks[:100]:  # 限制数量避免超时
        try:
            # 使用get_price获取最新数据
            df = get_price(stock, count=1, fields=['close'])
            if df is not None and len(df) > 0:
                # 简化处理：使用价格作为代理
                ep_values[stock] = 1.0 / df['close'].iloc[-1] * 100
        except:
            continue
    
    return pd.Series(ep_values)


def calculate_roe_factor(stocks):
    """计算ROE因子"""
    roe_values = {}
    
    # 简化处理：使用随机值模拟（实际应使用get_fundamentals）
    for stock in stocks[:100]:
        try:
            roe_values[stock] = hash(stock) % 100 / 100.0
        except:
            continue
    
    return pd.Series(roe_values)


def calculate_reversal_factor(stocks):
    """计算反转因子 (过去20日收益率的负值)"""
    reversal = {}
    
    for stock in stocks[:100]:  # 限制数量避免超时
        try:
            # 获取历史价格
            df = get_price(stock, count=21, fields=['close'])
            if df is not None and len(df) >= 20:
                ret = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
                reversal[stock] = -ret  # 反转
        except:
            continue
    
    return pd.Series(reversal)


def zscore_normalize(series):
    """Z-score标准化"""
    series = series.dropna()
    if len(series) == 0:
        return series
    mean_val = series.mean()
    std_val = series.std()
    if std_val == 0 or pd.isna(std_val):
        return series - mean_val
    return (series - mean_val) / std_val


def execute_rebalance(context, target_stocks):
    """执行调仓"""
    global g_hold_num
    
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 计算需要卖出的股票
    to_sell = [s for s in current_positions if s not in target_stocks]
    
    # 计算需要买入的股票  
    to_buy = [s for s in target_stocks if s not in current_positions]
    
    log.info('调仓: 卖出%d只, 买入%d只' % (len(to_sell), len(to_buy)))
    
    # 先卖出
    for stock in to_sell:
        try:
            order_target(stock, 0)
            log.info('卖出: %s' % stock)
        except Exception as e:
            log.error('卖出失败: %s' % str(e))
    
    # 计算每只股票的目标金额
    if len(target_stocks) == 0:
        return
    
    total_value = context.portfolio.portfolio_value
    target_value = total_value * 0.95 / len(target_stocks)
    
    # 买入
    for stock in target_stocks:
        try:
            order_target_value(stock, target_value)
            log.info('买入: %s' % stock)
        except Exception as e:
            log.error('买入失败: %s' % str(e))



