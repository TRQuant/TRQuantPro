# -*- coding: utf-8 -*-
"""
TRQuant激进动量策略V3 - PTrade原生版
====================================
完全使用PTrade原生API，不依赖jqdata

PTrade API参考：
- get_history(): 获取历史行情
- get_snapshot(): 获取当前快照
- get_index_stocks(): 获取指数成分股
- set_slippage(float): 设置滑点
- set_commission(): 设置佣金
"""

# ==================== 策略参数 ====================
MAX_STOCKS = 5              # 最大持股数量
SINGLE_POSITION = 0.18      # 单票最大仓位
MIN_CASH_RATIO = 0.10       # 最低现金保留

REBALANCE_DAYS = 5          # 调仓周期
MOMENTUM_SHORT = 5          # 短期动量
MOMENTUM_LONG = 20          # 长期动量

STOP_LOSS = -0.08           # 止损线
TAKE_PROFIT = 0.30          # 止盈线

BENCHMARK = '000300.XSHG'   # 基准指数


# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    # 设置基准
    set_benchmark(BENCHMARK)
    
    # 设置滑点（PTrade直接使用数值）
    set_slippage(0.001)
    
    # 设置佣金（PTrade格式）
    set_commission(commission=0.0003, min_commission=5)
    
    # 初始化全局变量
    g.trade_count = 0
    g.stock_pool = []
    g.cost_prices = {}
    g.highest_prices = {}
    
    # 定时任务
    run_daily(before_market_open, '09:00')
    run_daily(market_open, '09:35')
    run_daily(check_risk, '14:50')
    run_daily(after_market_close, '15:30')
    
    log.info('=' * 50)
    log.info('策略初始化: TRQuant激进动量V3 (PTrade原生版)')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info('=' * 50)


def before_market_open(context):
    """盘前准备"""
    g.trade_count += 1
    
    # 每20天更新股票池
    if g.trade_count % 20 == 1:
        try:
            g.stock_pool = get_index_stocks(BENCHMARK)
            log.info(f'[盘前] 股票池更新: {len(g.stock_pool)}只')
        except Exception as e:
            log.error(f'[盘前] 获取指数成分股失败: {e}')
            # 兜底：使用全市场
            try:
                all_stocks = list(get_all_securities('stock').index)
                g.stock_pool = all_stocks[:300]
                log.info(f'[盘前] 使用全市场股票池: {len(g.stock_pool)}只')
            except:
                g.stock_pool = []


def market_open(context):
    """开盘交易"""
    if g.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{g.trade_count}个交易日')
    
    # 选股
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warn('[调仓] 未选出股票，保持当前持仓')
        return
    
    log.info(f'[调仓] 目标股票: {target_stocks}')
    
    # 执行调仓
    rebalance(context, target_stocks)


def select_stocks(context):
    """选股逻辑"""
    stocks = g.stock_pool
    if not stocks:
        log.warn('[选股] 股票池为空')
        return []
    
    log.info(f'[选股] 开始选股，股票池: {len(stocks)}只')
    
    # 过滤股票
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {len(stocks)}只')
    
    if len(stocks) == 0:
        return fallback_select(context)
    
    try:
        # 限制数量避免超时
        test_stocks = stocks[:30] if len(stocks) > 30 else stocks
        
        # PTrade获取历史数据
        # get_history(count, unit, security_list, fields, skip_paused, fq)
        prices = get_history(
            MOMENTUM_LONG + 5, 
            '1d', 
            test_stocks, 
            ['close'],
            skip_paused=False, 
            fq='pre'
        )
        
        if prices is None or len(prices) == 0:
            log.warn('[选股] 获取历史数据为空')
            return fallback_select(context)
        
        # prices是dict格式: {'close': DataFrame}
        close_df = prices.get('close')
        if close_df is None or close_df.empty:
            log.warn('[选股] 收盘价数据为空')
            return fallback_select(context)
        
        log.info(f'[选股] 价格数据: {len(close_df)}行 x {len(close_df.columns)}列')
        
        # 计算动量
        mom_short = close_df.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = close_df.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 三级选股条件
        # 严格条件：两个动量都>0
        valid_strict = (mom_short > 0) & (mom_long > 0)
        score_strict = (mom_short * 0.5 + mom_long * 0.5).where(valid_strict).dropna()
        
        # 宽松条件：至少一个动量>0
        valid_loose = (mom_short > 0) | (mom_long > 0)
        score_loose = (mom_short * 0.5 + mom_long * 0.5).where(valid_loose).dropna()
        
        # 综合得分
        score_all = (mom_short * 0.5 + mom_long * 0.5).dropna()
        
        # 选择合适的条件
        if len(score_strict) >= MAX_STOCKS:
            score = score_strict
            log.info(f'[选股] 使用严格条件: {len(score)}只符合')
        elif len(score_loose) >= MAX_STOCKS:
            score = score_loose
            log.info(f'[选股] 使用宽松条件: {len(score)}只符合')
        elif len(score_all) > 0:
            score = score_all
            log.info(f'[选股] 使用综合得分: {len(score)}只')
        else:
            log.warn('[选股] 无有效得分')
            return fallback_select(context)
        
        # 选出得分最高的股票
        selected = score.nlargest(MAX_STOCKS).index.tolist()
        log.info(f'[选股] 选股成功: {len(selected)}只')
        
        return selected
        
    except Exception as e:
        import traceback
        log.error(f'[选股] 异常: {e}')
        log.error(traceback.format_exc())
        return fallback_select(context)


def fallback_select(context):
    """兜底选股策略"""
    log.info('[选股] 使用兜底策略')
    
    stocks = g.stock_pool
    if not stocks:
        return []
    
    # 简单返回前N只股票
    filtered = filter_stocks(context, stocks[:50])
    selected = filtered[:MAX_STOCKS]
    
    if selected:
        log.info(f'[选股] 兜底选股: {selected}')
    
    return selected


def filter_stocks(context, stocks):
    """过滤股票"""
    filtered = []
    
    # 获取当前快照
    try:
        snapshots = get_snapshot(stocks[:100])
    except:
        snapshots = {}
    
    for stock in stocks:
        try:
            # 排除ST（通过名称判断）
            try:
                info = get_instrument(stock)
                if info and hasattr(info, 'name'):
                    name = info.name
                    if 'ST' in name or '*ST' in name:
                        continue
            except:
                pass
            
            # 排除涨跌停
            if stock in snapshots:
                snap = snapshots[stock]
                if hasattr(snap, 'open') and hasattr(snap, 'up_limit'):
                    if snap.open == snap.up_limit:
                        continue
                if hasattr(snap, 'open') and hasattr(snap, 'down_limit'):
                    if snap.open == snap.down_limit:
                        continue
                # 排除停牌
                if hasattr(snap, 'paused') and snap.paused:
                    continue
            
            filtered.append(stock)
        except:
            continue
    
    return filtered


def rebalance(context, target_stocks):
    """调仓"""
    if not target_stocks:
        return
    
    current_stocks = set(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    log.info(f'[调仓] 目标仓位: {target_value:.0f}/只')
    
    # 卖出不在目标列表的股票
    sell_count = 0
    for stock in current_stocks - target_set:
        try:
            order_target_value(stock, 0)
            log.info(f'[卖出] {stock}')
            sell_count += 1
            g.cost_prices.pop(stock, None)
            g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[卖出失败] {stock}: {e}')
    
    if sell_count > 0:
        log.info(f'[调仓] 卖出: {sell_count}只')
    
    # 买入目标股票
    buy_count = 0
    for stock in target_stocks:
        try:
            # 获取当前持仓
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            # 需要调整仓位
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {stock} 目标:{target_value:.0f}')
                buy_count += 1
                
                # 记录成本
                if stock not in g.cost_prices:
                    try:
                        snap = get_snapshot([stock])
                        if stock in snap and hasattr(snap[stock], 'last_px'):
                            g.cost_prices[stock] = snap[stock].last_px
                            g.highest_prices[stock] = g.cost_prices[stock]
                    except:
                        pass
        except Exception as e:
            log.warn(f'[买入失败] {stock}: {e}')
    
    if buy_count > 0:
        log.info(f'[调仓] 买入: {buy_count}只')
    else:
        log.warn('[调仓] 未执行任何买入')


def check_risk(context):
    """风控检查"""
    for stock in list(context.portfolio.positions.keys()):
        try:
            pos = context.portfolio.positions[stock]
            if pos.total_amount == 0:
                continue
            
            # 获取当前价格
            try:
                snap = get_snapshot([stock])
                current_price = snap[stock].last_px if stock in snap else pos.price
            except:
                current_price = pos.price
            
            cost = g.cost_prices.get(stock, pos.avg_cost)
            highest = g.highest_prices.get(stock, cost)
            
            if cost <= 0:
                continue
            
            profit = (current_price - cost) / cost
            g.highest_prices[stock] = max(highest, current_price)
            
            # 止损
            if profit < STOP_LOSS:
                order_target_value(stock, 0)
                log.warn(f'[止损] {stock} {profit*100:.1f}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            
            # 止盈
            elif profit > TAKE_PROFIT:
                order_target_value(stock, 0)
                log.info(f'[止盈] {stock} {profit*100:.1f}%')
                g.cost_prices.pop(stock, None)
                g.highest_prices.pop(stock, None)
            
            # 移动止损（盈利15%后回撤10%止损）
            elif profit > 0.15:
                dd = (g.highest_prices[stock] - current_price) / g.highest_prices[stock]
                if dd > 0.10:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {stock} 回撤{dd*100:.1f}%')
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

