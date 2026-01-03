# -*- coding: utf-8 -*-
"""
韬睿量化 - 多因子策略
======================

因子: EP, ROE, Reversal
股票池: 000300.XSHG
持仓数量: 30
调仓频率: monthly

由韬睿量化系统自动生成
"""

import pandas as pd
import numpy as np
from jqdatasdk import *

# ==================== 因子计算函数 ====================


# EP因子 - 盈利收益率
def calculate_ep_factor(stocks, date):
    """
    计算EP因子
    
    Args:
        stocks: 股票列表
        date: 计算日期
    
    Returns:
        pd.Series: EP因子值
    """
    from jqdatasdk import query, valuation, get_fundamentals
    import numpy as np
    
    q = query(
        valuation.code,
        valuation.pe_ratio
    ).filter(valuation.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    
    # EP = 1/PE，处理异常值
    df['EP'] = np.where(
        (df['pe_ratio'] > 0) & (df['pe_ratio'] < 500),
        1.0 / df['pe_ratio'],
        np.nan
    )
    
    return df.set_index('code')['EP']

# ROE因子
def calculate_roe_factor(stocks, date):
    """计算ROE因子"""
    from jqdatasdk import query, indicator, get_fundamentals
    
    q = query(
        indicator.code,
        indicator.roe
    ).filter(indicator.code.in_(stocks))
    
    df = get_fundamentals(q, date=date)
    df['ROE'] = df['roe'].clip(-20, 50)
    
    return df.set_index('code')['ROE']

# 短期反转因子
def calculate_reversal_factor(stocks, date, lookback_days=5):
    """
    计算短期反转因子
    
    短期下跌越多，反弹预期越强
    """
    from jqdatasdk import get_price
    import numpy as np
    import pandas as pd
    
    prices = get_price(
        stocks,
        end_date=date,
        count=lookback_days + 5,
        fields=['close'],
        panel=False
    )
    
    reversal_dict = {}
    
    for stock in stocks:
        stock_prices = prices[prices['code'] == stock]['close']
        
        if len(stock_prices) < lookback_days + 1:
            reversal_dict[stock] = np.nan
            continue
        
        current_price = stock_prices.iloc[-1]
        past_price = stock_prices.iloc[-(lookback_days + 1)]
        
        if past_price > 0:
            # 取负值：下跌越多，反转因子越大
            reversal_dict[stock] = -(current_price - past_price) / past_price
        else:
            reversal_dict[stock] = np.nan
    
    return pd.Series(reversal_dict).clip(-0.5, 0.5)


# ==================== 辅助函数 ====================

def zscore(series):
    """Z-score标准化"""
    mean = series.mean()
    std = series.std()
    if std > 0:
        return (series - mean) / std
    return series - mean

def winsorize_mad(series, n=5):
    """MAD法去极值"""
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0:
        return series
    upper = median + n * 1.4826 * mad
    lower = median - n * 1.4826 * mad
    return series.clip(lower, upper)

def filter_stocks(stocks, date):
    """过滤ST和停牌股票"""
    # 过滤ST
    st_stocks = get_extras('is_st', stocks, end_date=date, count=1).iloc[0]
    stocks = [s for s in stocks if not st_stocks.get(s, True)]
    
    # 过滤停牌
    paused = get_price(stocks, end_date=date, count=1, fields=['paused'], panel=False)
    paused_stocks = paused[paused['paused'] == 1]['code'].tolist()
    stocks = [s for s in stocks if s not in paused_stocks]
    
    return stocks

# ==================== 策略主体 ====================

def initialize(context):
    """初始化"""
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点和手续费
    set_slippage(FixedSlippage(0.02))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    # 策略参数
    context.stock_pool = '000300.XSHG'
    context.hold_num = 30
    context.factor_weights = {'EP': 0.3, 'ROE': 0.3, 'Reversal': 0.4}
    
    # 设置调仓
    run_monthly(rebalance, 1, time='open')

def calculate_composite_factor(stocks, date):
    """计算复合因子"""
    weights = {'EP': 0.3, 'ROE': 0.3, 'Reversal': 0.4}
    
    factors = {}
    
    # 计算各因子
    factors['EP'] = calculate_ep_factor(stocks, date)
    factors['ROE'] = calculate_roe_factor(stocks, date)
    factors['Reversal'] = calculate_reversal_factor(stocks, date)

    
    # 标准化并组合
    df = pd.DataFrame(factors)
    
    composite = pd.Series(0, index=df.index)
    for name, weight in weights.items():
        if name in df.columns:
            factor_values = winsorize_mad(df[name].fillna(0))
            composite += zscore(factor_values) * weight
    
    return zscore(composite)

def rebalance(context):
    """调仓"""
    date = context.current_dt.strftime('%Y-%m-%d')
    
    # 获取股票池
    stocks = get_index_stocks(context.stock_pool)
    
    # 过滤
    stocks = filter_stocks(stocks, date)
    
    if len(stocks) == 0:
        log.warning("股票池为空")
        return
    
    # 计算因子
    factor = calculate_composite_factor(stocks, date)
    
    # 选股
    target_stocks = factor.nlargest(context.hold_num).index.tolist()
    
    # 卖出不在目标中的股票
    for stock in list(context.portfolio.positions.keys()):
        if stock not in target_stocks:
            order_target(stock, 0)
    
    # 买入目标股票
    if len(target_stocks) > 0:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_value(stock, context.portfolio.total_value * weight)
    
    log.info(f"调仓完成: 持仓 {len(target_stocks)} 只股票")
