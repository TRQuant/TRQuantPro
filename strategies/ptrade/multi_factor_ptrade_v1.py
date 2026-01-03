# -*- coding: utf-8 -*-
"""
韬睿量化 - 多因子策略 (PTrade版)
================================

因子: EP(价值), ROE(质量), Reversal(动量反转)
股票池: 沪深300
持仓数量: 30只
调仓频率: 月度

适配PTrade平台API
"""

import pandas as pd
import numpy as np

# ==================== 策略参数 ====================
STOCK_POOL = '000300.XSHG'  # 沪深300
HOLD_NUM = 30               # 持仓数量
WEIGHTS = {'EP': 0.3, 'ROE': 0.3, 'Reversal': 0.4}  # 因子权重


def initialize(context):
    """初始化函数"""
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置交易时间 - 每月第一个交易日调仓
    run_monthly(rebalance, 1, '09:35')
    
    # 记录日志
    log.info('多因子策略初始化完成')
    log.info('股票池: %s' % STOCK_POOL)
    log.info('持仓数量: %d' % HOLD_NUM)


def rebalance(context, bar_dict):
    """月度调仓"""
    log.info('='*50)
    log.info('开始月度调仓')
    
    # 获取当前日期
    date = context.now.strftime('%Y-%m-%d')
    
    # 获取股票池
    stocks = get_stock_pool(date)
    log.info(f'股票池数量: {len(stocks)}')
    
    if len(stocks) == 0:
        log.warn('股票池为空，跳过调仓')
        return
    
    # 计算复合因子得分
    scores = calculate_composite_score(stocks, date)
    
    if scores is None or len(scores) == 0:
        log.warn('因子计算失败，跳过调仓')
        return
    
    # 选择得分最高的股票
    scores = scores.dropna().sort_values(ascending=False)
    target_stocks = scores.head(HOLD_NUM).index.tolist()
    log.info(f'目标持仓: {len(target_stocks)}只')
    
    # 执行调仓
    execute_rebalance(context, target_stocks)
    
    log.info('调仓完成')
    log.info('='*50)


def get_stock_pool(date):
    """获取股票池"""
    # 获取指数成分股
    stocks = get_index_stocks(STOCK_POOL, date)
    
    # 过滤ST和停牌股票
    stocks = filter_stocks(stocks, date)
    
    return stocks


def filter_stocks(stocks, date):
    """过滤股票"""
    filtered = []
    for stock in stocks:
        try:
            # 获取股票信息
            info = get_stock_info(stock)
            if info is None:
                continue
            # 过滤ST
            name = info.get('name', '')
            if 'ST' in name or '*ST' in name:
                continue
            filtered.append(stock)
        except:
            continue
    return filtered


def calculate_composite_score(stocks, date):
    """计算复合因子得分"""
    try:
        # 计算各因子
        ep_factor = calculate_ep_factor(stocks, date)
        roe_factor = calculate_roe_factor(stocks, date)
        reversal_factor = calculate_reversal_factor(stocks, date)
        
        # 合并因子
        df = pd.DataFrame({
            'EP': ep_factor,
            'ROE': roe_factor,
            'Reversal': reversal_factor
        })
        
        # 标准化
        for col in df.columns:
            df[col] = zscore_normalize(df[col])
        
        # 加权组合
        score = pd.Series(0, index=df.index)
        for factor, weight in WEIGHTS.items():
            if factor in df.columns:
                score += df[factor].fillna(0) * weight
        
        return score
        
    except Exception as e:
        log.error(f'因子计算异常: {e}')
        return None


def calculate_ep_factor(stocks, date):
    """计算EP因子 (盈利收益率 = 1/PE)"""
    try:
        ep_values = {}
        
        for stock in stocks:
            try:
                # 获取市盈率
                df = get_fundamentals(stock, date, date, fields=['pe_ratio'])
                if df is not None and len(df) > 0:
                    pe = df['pe_ratio'].iloc[-1]
                    if pe and pe > 0 and pe < 500:
                        ep_values[stock] = 1.0 / pe
            except:
                continue
        
        return pd.Series(ep_values)
        
    except Exception as e:
        log.error('EP因子计算失败: %s' % str(e))
        return pd.Series()


def calculate_roe_factor(stocks, date):
    """计算ROE因子 (净资产收益率)"""
    try:
        roe_values = {}
        
        for stock in stocks:
            try:
                # 获取ROE
                df = get_fundamentals(stock, date, date, fields=['roe'])
                if df is not None and len(df) > 0:
                    roe = df['roe'].iloc[-1]
                    if roe is not None:
                        roe_values[stock] = roe
            except:
                continue
        
        return pd.Series(roe_values)
        
    except Exception as e:
        log.error('ROE因子计算失败: %s' % str(e))
        return pd.Series()


def calculate_reversal_factor(stocks, date):
    """计算反转因子 (过去20日收益率的负值)"""
    try:
        reversal = {}
        
        for stock in stocks:
            try:
                # PTrade获取历史价格
                df = get_price(stock, count=21, end_date=date, frequency='1d', fields=['close'])
                if df is not None and len(df) >= 20:
                    ret = (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
                    reversal[stock] = -ret  # 反转：收益率取负
            except:
                continue
        
        return pd.Series(reversal)
        
    except Exception as e:
        log.error('反转因子计算失败: %s' % str(e))
        return pd.Series()


def zscore_normalize(series):
    """Z-score标准化"""
    series = series.dropna()
    if len(series) == 0:
        return series
    mean = series.mean()
    std = series.std()
    if std == 0:
        return series - mean
    return (series - mean) / std


def execute_rebalance(context, target_stocks):
    """执行调仓"""
    # 获取当前持仓
    current_positions = list(context.portfolio.positions.keys())
    
    # 计算需要卖出的股票
    to_sell = [s for s in current_positions if s not in target_stocks]
    
    # 计算需要买入的股票
    to_buy = [s for s in target_stocks if s not in current_positions]
    
    log.info('卖出: %d只, 买入: %d只' % (len(to_sell), len(to_buy)))
    
    # 先卖出
    for stock in to_sell:
        position = context.portfolio.positions.get(stock)
        if position and position.sellable > 0:
            order_target(stock, 0)
            log.info('卖出: %s' % stock)
    
    # 计算每只股票的目标金额
    if len(target_stocks) == 0:
        return
        
    total_value = context.portfolio.portfolio_value
    target_value = total_value * 0.95 / len(target_stocks)
    
    # 买入
    for stock in target_stocks:
        current_value = 0
        position = context.portfolio.positions.get(stock)
        if position:
            current_value = position.value
        
        if current_value < target_value * 0.9:  # 偏离超过10%才调整
            order_target_value(stock, target_value)
            log.info('买入: %s, 目标金额: %.0f' % (stock, target_value))


def handle_data(context, bar_dict):
    """每日运行（可选）"""
    pass

