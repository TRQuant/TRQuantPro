# -*- coding: utf-8 -*-
"""
韬睿量化 - 多因子策略 (PTrade V2)
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
STOCK_POOL = '000300.XSHG'  # 沪深300
HOLD_NUM = 30               # 持仓数量
WEIGHTS = {'EP': 0.3, 'ROE': 0.3, 'Reversal': 0.4}


def initialize(context):
    """
    初始化函数 (必选)
    在策略开始运行时执行一次
    """
    # 设置基准 - PTrade API
    set_benchmark('000300.XSHG')
    
    # 定时执行 - PTrade API: run_daily(func, time)
    # 每天09:35执行检查是否需要调仓
    run_daily(check_rebalance, '09:35')
    
    # 初始化变量
    context.last_rebalance_month = -1
    context.stock_pool_initialized = False
    
    log.info('='*50)
    log.info('多因子策略初始化完成')
    log.info('股票池: %s' % STOCK_POOL)
    log.info('持仓数量: %d' % HOLD_NUM)
    log.info('='*50)


def handle_data(context, data):
    """
    行情处理函数 (必选)
    每个交易bar执行一次
    """
    pass


def check_rebalance(context):
    """
    检查是否需要月度调仓
    """
    # 获取当前日期
    current_date = get_trading_day(context)
    current_month = current_date.month
    
    # 判断是否是新的月份
    if current_month != context.last_rebalance_month:
        log.info('='*50)
        log.info('月度调仓日: %s' % current_date)
        
        # 执行调仓
        rebalance(context)
        
        # 更新记录
        context.last_rebalance_month = current_month
        log.info('='*50)


def rebalance(context):
    """
    执行月度调仓
    """
    # 获取当前日期
    current_date = get_trading_day(context)
    date_str = current_date.strftime('%Y-%m-%d')
    
    # 获取股票池
    stocks = get_stock_pool(date_str)
    log.info('股票池数量: %d' % len(stocks))
    
    if len(stocks) == 0:
        log.warn('股票池为空，跳过调仓')
        return
    
    # 计算复合因子得分
    scores = calculate_composite_score(stocks, date_str, context)
    
    if scores is None or len(scores) == 0:
        log.warn('因子计算失败，跳过调仓')
        return
    
    # 选择得分最高的股票
    scores = scores.dropna().sort_values(ascending=False)
    target_stocks = scores.head(HOLD_NUM).index.tolist()
    log.info('目标持仓: %d只' % len(target_stocks))
    
    # 执行调仓
    execute_rebalance(context, target_stocks)


def get_trading_day(context):
    """获取当前交易日"""
    return context.blotter.current_dt.date()


def get_stock_pool(date_str):
    """获取股票池"""
    # PTrade API: get_index_stocks(index_code)
    stocks = get_index_stocks(STOCK_POOL)
    
    # 过滤ST股票
    filtered = []
    for stock in stocks:
        try:
            # PTrade API: get_stock_name(stock_code)
            name = get_stock_name(stock)
            if name and ('ST' not in name and '*ST' not in name):
                filtered.append(stock)
        except:
            continue
    
    return filtered


def calculate_composite_score(stocks, date_str, context):
    """计算复合因子得分"""
    try:
        # 计算各因子
        ep_factor = calculate_ep_factor(stocks, date_str)
        roe_factor = calculate_roe_factor(stocks, date_str)
        reversal_factor = calculate_reversal_factor(stocks, date_str, context)
        
        # 合并因子
        df = pd.DataFrame({
            'EP': ep_factor,
            'ROE': roe_factor,
            'Reversal': reversal_factor
        })
        
        log.info('因子计算完成: EP=%d, ROE=%d, Reversal=%d' % 
                 (len(ep_factor.dropna()), len(roe_factor.dropna()), len(reversal_factor.dropna())))
        
        # 标准化
        for col in df.columns:
            df[col] = zscore_normalize(df[col])
        
        # 加权组合
        score = pd.Series(0.0, index=df.index)
        for factor, weight in WEIGHTS.items():
            if factor in df.columns:
                score = score + df[factor].fillna(0) * weight
        
        return score
        
    except Exception as e:
        log.error('因子计算异常: %s' % str(e))
        return None


def calculate_ep_factor(stocks, date_str):
    """
    计算EP因子 (盈利收益率 = 1/PE)
    使用PTrade API: get_fundamentals
    """
    ep_values = {}
    
    for stock in stocks:
        try:
            # PTrade API: get_fundamentals(stock, start_date, end_date, fields)
            df = get_fundamentals(stock, date_str, date_str, fields='pe_ratio')
            if df is not None and len(df) > 0 and 'pe_ratio' in df.columns:
                pe = df['pe_ratio'].iloc[-1]
                if pe is not None and pe > 0 and pe < 500:
                    ep_values[stock] = 1.0 / pe
        except:
            continue
    
    return pd.Series(ep_values)


def calculate_roe_factor(stocks, date_str):
    """
    计算ROE因子 (净资产收益率)
    使用PTrade API: get_fundamentals
    """
    roe_values = {}
    
    for stock in stocks:
        try:
            # PTrade API: get_fundamentals(stock, start_date, end_date, fields)
            df = get_fundamentals(stock, date_str, date_str, fields='roe')
            if df is not None and len(df) > 0 and 'roe' in df.columns:
                roe = df['roe'].iloc[-1]
                if roe is not None:
                    roe_values[stock] = roe
        except:
            continue
    
    return pd.Series(roe_values)


def calculate_reversal_factor(stocks, date_str, context):
    """
    计算反转因子 (过去20日收益率的负值)
    使用PTrade API: get_history
    """
    reversal = {}
    
    for stock in stocks:
        try:
            # PTrade API: get_history(count, frequency, field, security_list, fq, include)
            df = get_history(21, '1d', 'close', stock, fq='pre', include=False)
            if df is not None and len(df) >= 20:
                close_prices = df[stock] if stock in df.columns else df['close']
                if len(close_prices) >= 20:
                    ret = (close_prices.iloc[-1] / close_prices.iloc[0]) - 1
                    reversal[stock] = -ret  # 反转：收益率取负
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
    """
    执行调仓
    使用PTrade交易API
    """
    # 获取当前持仓 - PTrade API: get_position(stock)
    current_positions = []
    for stock in context.portfolio.positions:
        pos = get_position(stock)
        if pos is not None and pos.amount > 0:
            current_positions.append(stock)
    
    # 计算需要卖出的股票
    to_sell = [s for s in current_positions if s not in target_stocks]
    
    # 计算需要买入的股票
    to_buy = [s for s in target_stocks if s not in current_positions]
    
    log.info('调仓: 卖出%d只, 买入%d只' % (len(to_sell), len(to_buy)))
    
    # 先卖出 - PTrade API: order_target(stock, amount)
    for stock in to_sell:
        try:
            order_target(stock, 0)
            log.info('卖出: %s' % stock)
        except Exception as e:
            log.error('卖出失败 %s: %s' % (stock, str(e)))
    
    # 计算每只股票的目标金额
    if len(target_stocks) == 0:
        return
    
    total_value = context.portfolio.portfolio_value
    target_value = total_value * 0.95 / len(target_stocks)
    
    # 买入 - PTrade API: order_target_value(stock, value)
    for stock in target_stocks:
        try:
            current_value = 0
            pos = get_position(stock)
            if pos is not None:
                current_value = pos.amount * pos.last_price
            
            # 偏离超过10%才调整
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info('买入: %s, 目标金额: %.0f' % (stock, target_value))
        except Exception as e:
            log.error('买入失败 %s: %s' % (stock, str(e)))


def before_trading_start(context, data):
    """
    盘前处理函数 (可选)
    每天开盘前执行一次
    """
    # 在盘前设置股票池（不能在initialize中调用get_index_stocks）
    if not context.stock_pool_initialized:
        try:
            stocks = get_index_stocks(STOCK_POOL)
            set_universe(stocks)
            log.info('股票池设置完成: %d只' % len(stocks))
            context.stock_pool_initialized = True
        except Exception as e:
            log.error('设置股票池失败: %s' % str(e))


def after_trading_end(context, data):
    """
    盘后处理函数 (可选)
    每天收盘后执行一次
    """
    pass

