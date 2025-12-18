# -*- coding: utf-8 -*-
"""
TRQuant_momentum_v4 - PTrade策略
由TRQuant自动生成 @ 2025-12-15 06:17:30

策略风格: 动量成长
使用因子: momentum_20d, ROE_ttm
"""


# ==================== 策略参数 ====================
MAX_STOCKS = 5              # 最大持股数量
SINGLE_POSITION = 0.18       # 单票最大仓位
MIN_CASH_RATIO = 0.10                  # 最低现金保留

REBALANCE_DAYS = 5                     # 调仓周期
MOMENTUM_SHORT = 5                     # 短期动量
MOMENTUM_LONG = 20                     # 长期动量

STOP_LOSS = -0.08               # 止损线
TAKE_PROFIT = 0.3            # 止盈线

BENCHMARK = '000300.XSHG'              # 基准指数
FACTORS = ['momentum_20d', 'ROE_ttm']                    # 使用因子


# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    set_benchmark(BENCHMARK)
    set_slippage(0.001)
    set_commission(commission=0.0003, min_commission=5)
    
    g.trade_count = 0
    g.stock_pool = []
    g.cost_prices = {}
    g.highest_prices = {}
    
    run_daily(before_market_open, '09:00')
    run_daily(market_open, '09:35')
    run_daily(check_risk, '14:50')
    run_daily(after_market_close, '15:30')
    
    log.info('=' * 50)
    log.info(f'策略初始化: {BENCHMARK}')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info('=' * 50)


def before_market_open(context):
    """盘前准备"""
    g.trade_count += 1
    
    if g.trade_count % 20 == 1:
        try:
            g.stock_pool = get_index_stocks(BENCHMARK)
            log.info(f'[盘前] 股票池更新: {len(g.stock_pool)}只')
        except Exception as e:
            log.error(f'[盘前] 获取指数成分股失败: {e}')
            try:
                all_stocks = list(get_all_securities('stock').index)
                g.stock_pool = all_stocks[:300]
            except:
                g.stock_pool = []


def market_open(context):
    """开盘交易"""
    if g.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{g.trade_count}个交易日')
    
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warn('[调仓] 未选出股票')
        return
    
    log.info(f'[调仓] 目标股票: {target_stocks}')
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑"""
    stocks = g.stock_pool
    if not stocks:
        return []
    
    log.info(f'[选股] 开始选股，股票池: {len(stocks)}只')
    
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {len(stocks)}只')
    
    if len(stocks) == 0:
        return fallback_select(context)
    
    try:
        test_stocks = stocks[:30] if len(stocks) > 30 else stocks
        
        prices = get_history(MOMENTUM_LONG + 5, '1d', test_stocks, ['close'], skip_paused=False, fq='pre')
        
        if prices is None:
            return fallback_select(context)
        
        close_df = prices['close']
        
        if close_df is None or close_df.empty:
            return fallback_select(context)
        
        # 计算动量
        mom_short = close_df.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = close_df.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 三级选股
        valid_strict = (mom_short > 0) & (mom_long > 0)
        score_strict = (mom_short * 0.5 + mom_long * 0.5).where(valid_strict).dropna()
        
        valid_loose = (mom_short > 0) | (mom_long > 0)
        score_loose = (mom_short * 0.5 + mom_long * 0.5).where(valid_loose).dropna()
        
        score_all = (mom_short * 0.5 + mom_long * 0.5).dropna()
        
        if len(score_strict) >= MAX_STOCKS:
            score = score_strict
        elif len(score_loose) >= MAX_STOCKS:
            score = score_loose
        elif len(score_all) > 0:
            score = score_all
        else:
            return fallback_select(context)
        
        selected = score.nlargest(MAX_STOCKS).index.tolist()
        log.info(f'[选股] 选股成功: {len(selected)}只')
        return selected
        
    except Exception as e:
        log.error(f'[选股] 异常: {e}')
        return fallback_select(context)


def fallback_select(context):
    """兜底选股"""
    stocks = g.stock_pool
    if not stocks:
        return []
    
    filtered = filter_stocks(context, stocks[:50])
    selected = filtered[:MAX_STOCKS]
    
    if selected:
        log.info(f'[选股] 兜底: {selected}')
    
    return selected


def rebalance(context, target_stocks):
    """调仓"""
    if not target_stocks:
        return
    
    current_stocks = set(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    # 卖出
    for stock in current_stocks - target_set:
        try:
            order_target_value(stock, 0)
            log.info(f'[卖出] {stock}')
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[卖出失败] {stock}: {e}')
    
    # 买入
    for stock in target_stocks:
        try:
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {stock} 目标:{target_value:.0f}')
        except Exception as e:
            log.warn(f'[买入失败] {stock}: {e}')


def check_risk(context):
    """风控检查"""
    for stock in list(context.portfolio.positions.keys()):
        try:
            pos = context.portfolio.positions[stock]
            if pos.total_amount == 0:
                continue
            
            current_price = pos.price
            cost = g.cost_prices.get(stock, pos.avg_cost)
            highest = g.highest_prices.get(stock, cost)
            
            if cost <= 0:
                continue
            
            profit = (current_price - cost) / cost
            g.highest_prices[stock] = max(highest, current_price)
            
            if profit < STOP_LOSS:
                order_target_value(stock, 0)
                log.warn(f'[止损] {stock} {profit*100:.1f}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            elif profit > TAKE_PROFIT:
                order_target_value(stock, 0)
                log.info(f'[止盈] {stock} {profit*100:.1f}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            elif profit > 0.15:
                dd = (g.highest_prices[stock] - current_price) / g.highest_prices[stock]
                if dd > 0.10:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {stock}')
                    g.cost_prices.pop(stock, None)
                    g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[风控异常] {stock}: {e}')


def after_market_close(context):
    """收盘统计"""
    pos_count = len([p for p in context.portfolio.positions.values() if p.total_amount > 0])
    total = context.portfolio.total_value
    ret = context.portfolio.returns
    log.info(f'[收盘] 持仓:{pos_count}只 资产:{total:.0f} 收益:{ret*100:.2f}%')


def filter_stocks(context, stocks):
    """过滤股票"""
    filtered = []
    
    try:
        snapshots = get_snapshot(stocks[:100])
    except:
        snapshots = {}
    
    for stock in stocks:
        try:
            # 排除ST
            try:
                info = get_instrument(stock) if 'ptrade' in 'ptrade' else get_security_info(stock)
                if info and hasattr(info, 'name'):
                    if 'ST' in info.name or '*ST' in info.name:
                        continue
            except:
                pass
            
            filtered.append(stock)
        except:
            continue
    
    return filtered
