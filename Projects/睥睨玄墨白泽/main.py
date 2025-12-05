# -*- coding: utf-8 -*-
"""
睥睨玄墨白泽 - 智能多因子量化策略
=====================================

创建时间: 2025/12/3 17:42:50
回测区间: 2024-09-03 至 2025-09-03
基准指数: 000300.XSHG (沪深300)

平台兼容:
---------
- 聚宽(JoinQuant): 策略研究和回测验证
- PTrade: 实盘交易（需少量API适配）

策略特色:
---------
本策略基于韬睿量化(TRQuant)工作流系统，自动获取并整合：
1. 市场趋势分析 → 仓位管理
2. 投资主线识别 → 选股方向
3. 因子权重推荐 → 动态配置

工作流数据驱动:
--------------
- 牛市: 增加动量/成长因子权重，提升仓位
- 熊市: 增加价值/质量因子权重，降低仓位  
- 震荡: 均衡配置，注重波动控制

迁移到PTrade:
-------------
1. get_price -> get_history
2. get_current_data -> get_snapshot  
3. order_target_value -> order_target_percent
4. 添加 on_bar() 入口函数
"""

import numpy as np
import pandas as pd
from datetime import datetime

# ============================================================
# 工作流数据配置（根据TRQuant分析结果动态调整）
# ============================================================

# 市场状态：risk_on(牛市)/risk_off(熊市)/neutral(震荡)
# 由TRQuant工作流Step2(市场趋势分析)提供
MARKET_REGIME = 'risk_on'

# 当前热门主线（由TRQuant工作流Step3投资主线识别提供）
# 格式: [主线名称, 关联行业代码]
HOT_MAINLINES = [
    ('AI人工智能', ["半导体","软件","通信"]),
    ('新能源汽车', ["汽车","电池","充电桩"]),
    ('医药创新', ["创新药","医疗器械","CXO"]),
    ('高端制造', ["机械","工控","机器人"]),
    ('消费复苏', ["白酒","免税","餐饮"]),
]

# 因子权重配置（由TRQuant工作流Step5因子推荐提供）
# 根据市场状态自动调整
FACTOR_WEIGHTS_BY_REGIME = {
    'risk_on': {      # 牛市配置
        'value': 0.10,
        'growth': 0.30,
        'quality': 0.15,
        'momentum': 0.35,
        'volatility': 0.10,
    },
    'risk_off': {     # 熊市配置
        'value': 0.35,
        'growth': 0.10,
        'quality': 0.30,
        'momentum': 0.10,
        'volatility': 0.15,
    },
    'neutral': {      # 震荡市配置
        'value': 0.25,
        'growth': 0.20,
        'quality': 0.25,
        'momentum': 0.20,
        'volatility': 0.10,
    },
}

# 仓位配置（根据市场状态调整）
POSITION_BY_REGIME = {
    'risk_on': {
        'max_total_position': 0.95,    # 总仓位上限
        'single_stock_max': 0.12,      # 单票上限
        'min_cash': 0.05,              # 最低现金
    },
    'risk_off': {
        'max_total_position': 0.60,    # 熊市降仓
        'single_stock_max': 0.08,
        'min_cash': 0.40,
    },
    'neutral': {
        'max_total_position': 0.80,
        'single_stock_max': 0.10,
        'min_cash': 0.20,
    },
}

# ============================================================
# 全局参数配置
# ============================================================

PARAMS = {
    # 基础参数
    'stock_num': 10,              # 持仓股票数量
    'select_pool': 'hs300',       # 选股池: hs300/zz500/zz1000
    'benchmark': '000300.XSHG',   # 基准指数
    
    # 动态因子权重（根据市场状态自动选择）
    'factor_weights': FACTOR_WEIGHTS_BY_REGIME.get(MARKET_REGIME, FACTOR_WEIGHTS_BY_REGIME['neutral']),
    
    # 动态仓位（根据市场状态自动选择）
    'position_config': POSITION_BY_REGIME.get(MARKET_REGIME, POSITION_BY_REGIME['neutral']),
    
    # 风控参数
    'stop_loss': -0.08,           # 止损线 (工作流可覆盖)
    'take_profit': 0.20,          # 止盈线
    'trailing_stop': 0.05,        # 移动止损
    
    # 调仓参数
    'rebalance_days': 20,         # 调仓周期（交易日）
    'use_mainline_filter': True,  # 是否使用主线过滤
}


# ============================================================
# 聚宽策略入口
# ============================================================

def initialize(context):
    """策略初始化 (聚宽)"""
    # 基准指数
    set_benchmark(PARAMS['benchmark'])
    
    # 滑点和手续费
    set_slippage(PriceRelatedSlippage(0.002))
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,       # 印花税 0.1%
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5
        ),
        type='stock'
    )
    
    # 真实价格模式
    set_option('use_real_price', True)
    set_option('order_volume_ratio', 0.25)
    
    # 初始化全局变量
    g.params = PARAMS
    g.trade_days = 0
    g.hold_days = {}
    g.cost_prices = {}
    g.highest_prices = {}  # 用于移动止损
    
    # 市场状态（从工作流获取）
    g.market_regime = MARKET_REGIME
    g.hot_mainlines = HOT_MAINLINES
    
    # 定时任务
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:30')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 60)
    log.info('📊 策略初始化: 睥睨玄墨白泽')
    log.info(f'📅 回测区间: 2024-09-03 ~ 2025-09-03')
    log.info(f'🎯 市场状态: {g.market_regime}')
    log.info(f'⚖️ 因子权重: {g.params["factor_weights"]}')
    log.info('=' * 60)


def before_market_open(context):
    """开盘前准备"""
    g.trade_days += 1
    current_dt = context.current_dt.strftime('%Y-%m-%d')
    
    # 获取停牌和ST股票
    g.paused_stocks = get_paused_stocks(current_dt)
    g.st_stocks = get_st_stocks(current_dt)
    
    # 动态调整市场状态（可选：每周更新一次）
    if g.trade_days % 5 == 1:
        update_market_regime(context)
    
    log.info(f'[{current_dt}] 交易日 #{g.trade_days} | 市场: {g.market_regime}')


def market_open(context):
    """盘中交易"""
    # 1. 风控检查（含移动止损）
    risk_control(context)
    
    # 2. 调仓判断
    if g.trade_days % g.params['rebalance_days'] == 1:
        log.info('[调仓日] 执行智能调仓')
        smart_rebalance(context)


def after_market_close(context):
    """收盘后记录"""
    # 更新持仓天数和最高价
    current_data = get_current_data()
    for stock in context.portfolio.positions:
        g.hold_days[stock] = g.hold_days.get(stock, 0) + 1
        price = current_data[stock].last_price
        g.highest_prices[stock] = max(g.highest_prices.get(stock, price), price)
    
    # 记录收益
    ret = context.portfolio.returns * 100
    log.info(f'[收盘] 资产: {context.portfolio.total_value:.0f} | 收益: {ret:.2f}%')


# ============================================================
# 智能选股（整合工作流数据）
# ============================================================

def smart_rebalance(context):
    """智能调仓 - 整合工作流数据"""
    # 1. 多因子选股
    target_stocks = select_stocks_with_mainline(context)
    
    if not target_stocks:
        log.warn('⚠️ 未选出股票')
        return
    
    log.info(f'[选股] 选出 {len(target_stocks)} 只: {target_stocks[:3]}...')
    
    # 2. 获取当前持仓
    current_stocks = list(context.portfolio.positions.keys())
    
    # 3. 卖出不在目标中的
    for stock in current_stocks:
        if stock not in target_stocks:
            log.info(f'[卖出] {stock}')
            order_target_value(stock, 0)
            clean_stock_records(stock)
    
    # 4. 根据市场状态计算仓位
    pos_config = g.params['position_config']
    total_value = context.portfolio.total_value
    available_value = total_value * pos_config['max_total_position']
    
    target_value = min(
        available_value / len(target_stocks),
        total_value * pos_config['single_stock_max']
    )
    
    # 5. 买入目标股票
    for stock in target_stocks:
        if stock in g.paused_stocks or stock in g.st_stocks:
            continue
        
        current_pos = context.portfolio.positions.get(stock, None)
        current_value = current_pos.value if current_pos else 0
        
        if current_value < target_value * 0.9:
            log.info(f'[买入] {stock} 目标: {target_value:.0f}')
            order_target_value(stock, target_value)
            
            if stock not in g.cost_prices:
                g.cost_prices[stock] = get_current_data()[stock].last_price
                g.highest_prices[stock] = g.cost_prices[stock]


def select_stocks_with_mainline(context):
    """整合主线的多因子选股"""
    # 1. 获取基础股票池
    pool = g.params['select_pool']
    if pool == 'hs300':
        stocks = get_index_stocks('000300.XSHG')
    elif pool == 'zz500':
        stocks = get_index_stocks('000905.XSHG')
    elif pool == 'zz1000':
        stocks = get_index_stocks('000852.XSHG')
    else:
        stocks = get_index_stocks('000300.XSHG')
    
    # 2. 主线加权（如果启用）
    mainline_boost = {}
    if g.params.get('use_mainline_filter') and g.hot_mainlines:
        for mainline_name, industry_codes in g.hot_mainlines:
            try:
                # 获取主线相关股票
                for code in industry_codes:
                    mainline_stocks = get_industry_stocks(code)
                    for s in mainline_stocks:
                        if s in stocks:
                            mainline_boost[s] = mainline_boost.get(s, 0) + 0.15
            except:
                pass
    
    log.info(f'[选股] 初始池: {len(stocks)}, 主线加权: {len(mainline_boost)}只')
    
    # 3. 过滤
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {len(stocks)}')
    
    if len(stocks) < g.params['stock_num']:
        return stocks
    
    # 4. 计算因子得分（动态权重）
    scores = calc_factor_scores_dynamic(context, stocks, mainline_boost)
    
    # 5. 排序选股
    sorted_stocks = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_stocks[:g.params['stock_num']]]


def calc_factor_scores_dynamic(context, stocks, mainline_boost=None):
    """动态权重因子评分"""
    current_dt = context.current_dt.strftime('%Y-%m-%d')
    weights = g.params['factor_weights']
    
    # 获取财务数据
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
        indicator.gross_profit_margin,
        indicator.inc_revenue_year_on_year,
        indicator.inc_net_profit_year_on_year,
    ).filter(valuation.code.in_(stocks))
    
    df = get_fundamentals(q, date=current_dt).set_index('code')
    
    # 获取行情数据
    price_df = get_price(stocks, end_date=current_dt, frequency='daily',
                         fields=['close'], count=60, panel=False)
    
    scores = {}
    
    for stock in stocks:
        if stock not in df.index:
            continue
        
        score = 0
        
        # 价值因子
        pe = df.loc[stock, 'pe_ratio']
        pb = df.loc[stock, 'pb_ratio']
        if not pd.isna(pe) and 0 < pe < 200:
            score += weights['value'] * (1 / min(pe, 100)) * 50
        if not pd.isna(pb) and 0 < pb < 50:
            score += weights['value'] * (1 / min(pb, 20)) * 50
        
        # 成长因子
        rev_g = df.loc[stock, 'inc_revenue_year_on_year']
        profit_g = df.loc[stock, 'inc_net_profit_year_on_year']
        if not pd.isna(rev_g):
            score += weights['growth'] * min(max(rev_g, -50), 100) / 100 * 50
        if not pd.isna(profit_g):
            score += weights['growth'] * min(max(profit_g, -50), 100) / 100 * 50
        
        # 质量因子
        roe = df.loc[stock, 'roe']
        gpm = df.loc[stock, 'gross_profit_margin']
        if not pd.isna(roe):
            score += weights['quality'] * min(max(roe, 0), 50) / 50 * 60
        if not pd.isna(gpm):
            score += weights['quality'] * min(max(gpm, 0), 80) / 80 * 40
        
        # 动量因子
        stock_prices = price_df[price_df['code'] == stock]['close'].values
        if len(stock_prices) >= 20:
            mom = (stock_prices[-1] / stock_prices[-20] - 1)
            score += weights['momentum'] * min(max(mom, -0.3), 0.5) * 100
        
        # 波动因子（低波动得高分）
        if len(stock_prices) >= 20:
            vol = np.std(np.diff(stock_prices) / stock_prices[:-1])
            score += weights['volatility'] * (1 - min(vol * 10, 1)) * 100
        
        # 主线加权
        if mainline_boost and stock in mainline_boost:
            score *= (1 + mainline_boost[stock])
        
        scores[stock] = score
    
    return scores


# ============================================================
# 风险控制（增强版）
# ============================================================

def risk_control(context):
    """增强风控：止盈止损 + 移动止损"""
    current_data = get_current_data()
    
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        current_price = current_data[stock].last_price
        cost_price = g.cost_prices.get(stock, pos.avg_cost)
        highest_price = g.highest_prices.get(stock, cost_price)
        
        if cost_price <= 0:
            continue
        
        profit = (current_price - cost_price) / cost_price
        drawdown_from_high = (highest_price - current_price) / highest_price if highest_price > 0 else 0
        
        # 止损
        if profit < g.params['stop_loss']:
            log.warn(f'🛑 [止损] {stock} {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
        
        # 止盈
        elif profit > g.params['take_profit']:
            log.info(f'🎯 [止盈] {stock} {profit*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)
        
        # 移动止损（盈利超过10%后启用）
        elif profit > 0.10 and drawdown_from_high > g.params.get('trailing_stop', 0.05):
            log.info(f'📉 [移动止损] {stock} 回撤 {drawdown_from_high*100:.1f}%')
            order_target_value(stock, 0)
            clean_stock_records(stock)


def clean_stock_records(stock):
    """清理股票记录"""
    g.hold_days.pop(stock, None)
    g.cost_prices.pop(stock, None)
    g.highest_prices.pop(stock, None)


# ============================================================
# 动态市场状态更新
# ============================================================

def update_market_regime(context):
    """
    动态更新市场状态（简化版）
    
    完整版应调用TRQuant工作流API获取实时市场分析
    """
    try:
        # 获取指数数据
        index_code = '000300.XSHG'
        end_dt = context.current_dt.strftime('%Y-%m-%d')
        
        prices = get_price(index_code, end_date=end_dt, frequency='daily',
                          fields=['close'], count=60)
        
        if prices.empty or len(prices) < 20:
            return
        
        close = prices['close']
        ma5 = close.rolling(5).mean().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20
        current = close.iloc[-1]
        
        # 简单趋势判断
        if current > ma5 > ma20 > ma60:
            new_regime = 'risk_on'
        elif current < ma5 < ma20:
            new_regime = 'risk_off'
        else:
            new_regime = 'neutral'
        
        # 状态变化时更新参数
        if new_regime != g.market_regime:
            g.market_regime = new_regime
            g.params['factor_weights'] = FACTOR_WEIGHTS_BY_REGIME[new_regime]
            g.params['position_config'] = POSITION_BY_REGIME[new_regime]
            log.info(f'🔄 [市场状态更新] {new_regime} | 因子权重已调整')
    
    except Exception as e:
        log.warn(f'市场状态更新失败: {e}')


# ============================================================
# 辅助函数
# ============================================================

def filter_stocks(context, stocks):
    """过滤股票"""
    current_data = get_current_data()
    filtered = []
    
    for stock in stocks:
        if stock in g.paused_stocks or stock in g.st_stocks:
            continue
        if current_data[stock].day_open == current_data[stock].high_limit:
            continue
        if current_data[stock].day_open == current_data[stock].low_limit:
            continue
        
        start_date = get_security_info(stock).start_date
        if (context.current_dt.date() - start_date).days < 60:
            continue
        
        filtered.append(stock)
    
    return filtered


def get_paused_stocks(date):
    """获取停牌股票"""
    current_data = get_current_data()
    return set(s for s in get_all_securities(['stock']).index if current_data[s].paused)


def get_st_stocks(date):
    """获取ST股票"""
    df = get_extras('is_st', get_all_securities(['stock']).index.tolist(), 
                    start_date=date, end_date=date, df=True)
    if df.empty:
        return set()
    return set(df.columns[df.iloc[0] == True].tolist())


# ============================================================
# PTrade 适配层 (实盘时取消注释)
# ============================================================

'''
# PTrade 入口函数
def on_bar(context, bar_dict):
    """PTrade K线触发函数"""
    market_open(context)


# PTrade API 映射
def order_target_value_ptrade(stock, value):
    """PTrade下单适配"""
    if value == 0:
        order_target_percent(stock, 0)
    else:
        total_value = context.portfolio.total_value
        percent = value / total_value
        order_target_percent(stock, percent)
'''


# ============================================================
# 策略使用说明
# ============================================================

"""
🚀 快速开始:
1. 直接在聚宽平台运行回测
2. 观察不同市场阶段的因子权重自动调整
3. 根据回测结果微调参数

🔧 参数调优建议:
- 牛市(risk_on): 可进一步提高momentum权重至0.40
- 熊市(risk_off): 可降低stock_num至5-8只,集中持仓优质标的
- 震荡市(neutral): 可缩短rebalance_days至10天,快进快出

📊 工作流整合:
本策略设计与TRQuant工作流深度整合:
- Step2 市场趋势 → MARKET_REGIME
- Step3 投资主线 → HOT_MAINLINES
- Step5 因子推荐 → FACTOR_WEIGHTS_BY_REGIME

🎯 PTrade迁移:
1. 取消注释底部PTrade适配层
2. 将order_target_value替换为order_target_value_ptrade
3. 在PTrade模拟盘充分测试后再实盘

⚠️ 风险提示:
本策略仅供学习研究，不构成投资建议。
投资有风险，入市需谨慎。

更新日志:
2025/12/3 17:42:50 - 智能版，整合TRQuant工作流数据
"""
