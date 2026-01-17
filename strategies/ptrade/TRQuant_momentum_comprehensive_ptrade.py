# -*- coding: utf-8 -*-
"""
PTrade策略 - 由BulletTrade/聚宽策略转换生成
转换时间: 2025-12-15 06:59:04
转换工具: TRQuant Comprehensive Strategy Converter

注意事项:
---------
1. 请检查所有API调用是否符合PTrade规范
2. 确认股票代码格式是否正确
3. 测试数据获取和交易执行功能
4. 检查日志输出是否正常

转换变更:
---------
- 删除jqdata导入
- get_price转换为get_history
- get_current_data()转换为get_snapshot(filtered)
- get_security_info转换为get_instrument

"""

# -*- coding: utf-8 -*-
"""
TRQuant激进动量策略V3 - 统一版本
================================
同时兼容 PTrade 和 BulletTrade 的策略代码

兼容性说明：
- 使用 PerTrade 设置佣金（两个平台都支持）
- 使用 FixedSlippage 设置滑点（两个平台都支持）
- 选股逻辑使用三级条件放宽机制
- 完整的日志输出便于调试

使用方法：
1. PTrade: 直接复制此文件到PTrade
2. BulletTrade: 在文件开头添加 ""

作者: TRQuant系统自动生成
版本: V3.0 (统一版)
"""

# ==================== 策略参数 ====================
MAX_STOCKS = 5              # 最大持股数量
SINGLE_POSITION = 0.18      # 单票最大仓位（18%）
MIN_CASH_RATIO = 0.10       # 最低现金保留（10%）

REBALANCE_DAYS = 5          # 调仓周期（天）
MOMENTUM_SHORT = 5          # 短期动量周期
MOMENTUM_LONG = 20          # 长期动量周期

STOP_LOSS = -0.08           # 止损线（-8%）
TAKE_PROFIT = 0.30          # 止盈线（30%）
TRAILING_STOP = 0.10        # 移动止损回撤（10%）

BENCHMARK = '000300.XSHG'   # 基准指数


# ==================== 初始化函数 ====================
def initialize(context):
    """
    策略初始化
    - 设置基准、滑点、佣金
    - 初始化全局变量
    - 设置定时任务
    """
    # 设置基准
    set_benchmark(BENCHMARK)
    
    # ⚠️ 关键：使用FixedSlippage设置滑点（PTrade和BulletTrade都支持）
    set_slippage(FixedSlippage(0.001))
    
    # ⚠️ 关键：使用PerTrade设置佣金（PTrade和BulletTrade都支持）
    # buy_cost: 买入佣金率 0.03%
    # sell_cost: 卖出佣金率 0.03% + 印花税 0.1% = 0.13%
    # min_cost: 最低佣金 5元
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
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
    
    log.info('=' * 60)
    log.info('策略初始化: TRQuant激进动量V3 (统一版)')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info(f'止损: {STOP_LOSS*100:.0f}% | 止盈: {TAKE_PROFIT*100:.0f}%')
    log.info('=' * 60)


# ==================== 盘前处理 ====================
def before_market_open(context):
    """
    盘前准备
    - 更新股票池
    """
    g.trade_count += 1
    
    # 每20天更新股票池
    if g.trade_count % 20 == 1:
        try:
            g.stock_pool = get_index_stocks(BENCHMARK)
            log.info(f'[盘前] 股票池更新: {len(g.stock_pool)}只')
        except Exception as e:
            log.error(f'[盘前] 获取指数成分股失败: {e}')
            try:
                all_stocks = list(get_all_securities('stock').index)
                g.stock_pool = all_stocks[:300]
                log.info(f'[盘前] 使用全市场股票池: {len(g.stock_pool)}只')
            except:
                g.stock_pool = []


# ==================== 开盘交易 ====================
def market_open(context):
    """
    开盘交易
    - 判断是否为调仓日
    - 执行选股和调仓
    """
    if g.trade_count % REBALANCE_DAYS != 1:
        return
    
    log.info(f'[调仓日] 第{g.trade_count}个交易日')
    
    target_stocks = select_stocks(context)
    
    if not target_stocks:
        log.warn('[调仓] 未选出股票，保持当前持仓')
        return
    
    log.info(f'[调仓] 目标股票: {target_stocks}')
    rebalance(context, target_stocks)


# ==================== 选股逻辑 ====================
def select_stocks(context):
    """
    选股逻辑（三级条件放宽机制）
    1. 严格条件：5日和20日动量都>0
    2. 宽松条件：5日或20日动量>0
    3. 兜底条件：综合得分排序
    """
    stocks = g.stock_pool
    if not stocks:
        log.warn('[选股] 股票池为空')
        return []
    
    log.info(f'[选股] 开始选股，股票池: {len(stocks)}只')
    
    stocks = filter_stocks(context, stocks)
    log.info(f'[选股] 过滤后: {len(stocks)}只')
    
    if len(stocks) == 0:
        return fallback_select(context)
    
    try:
        test_stocks = stocks[:30] if len(stocks) > 30 else stocks
        
        # 获取历史数据（兼容PTrade和BulletTrade）
        try:
            prices = get_history(MOMENTUM_LONG + 5, '1d', test_stocks, ['close'], 
                               skip_paused=False, fq='pre')
            if isinstance(prices, dict):
                close_df = prices.get('close')
            else:
                close_df = prices
        except:
            current_dt = context.current_dt.strftime('%Y-%m-%d')
            prices = get_history(20, '1d', test_stocks, ['close'], skip_paused=False, fq='pre')
            if 'time' in prices.columns and 'code' in prices.columns:
                close_df = prices.pivot(index='time', columns='code', values='close')
            else:
                close_df = prices
        
        if close_df is None or close_df.empty:
            log.warn('[选股] 获取历史数据为空')
            return fallback_select(context)
        
        log.info(f'[选股] 价格数据: {len(close_df)}行 x {len(close_df.columns)}列')
        
        # 计算动量
        mom_short = close_df.pct_change(MOMENTUM_SHORT).iloc[-1]
        mom_long = close_df.pct_change(MOMENTUM_LONG).iloc[-1]
        
        # 三级选股条件
        valid_strict = (mom_short > 0) & (mom_long > 0)
        score_strict = (mom_short * 0.5 + mom_long * 0.5).where(valid_strict).dropna()
        
        valid_loose = (mom_short > 0) | (mom_long > 0)
        score_loose = (mom_short * 0.5 + mom_long * 0.5).where(valid_loose).dropna()
        
        score_all = (mom_short * 0.5 + mom_long * 0.5).dropna()
        
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
    
    filtered = filter_stocks(context, stocks[:50])
    selected = filtered[:MAX_STOCKS]
    
    if selected:
        log.info(f'[选股] 兜底选股: {selected}')
    
    return selected


# ==================== 股票过滤 ====================
def filter_stocks(context, stocks):
    """
    过滤股票
    - 排除ST股票
    - 排除涨跌停
    - 排除停牌
    """
    filtered = []
    
    try:
        current_data = get_snapshot(filtered[:100]) if len(filtered) > 0 else {}
    except:
        current_data = {}
    
    for stock in stocks:
        try:
            # 排除ST
            try:
                info = get_instrument(stock)
                if info and hasattr(info, 'name'):
                    name = info.name
                    if 'ST' in name or '*ST' in name:
                        continue
            except:
                pass
            
            if stock in current_data:
                data = current_data[stock]
                
                if hasattr(data, 'paused') and data.paused:
                    continue
                
                try:
                    open_price = getattr(data, 'open', None) or getattr(data, 'day_open', None)
                    high_limit = getattr(data, 'high_limit', None) or getattr(data, 'up_limit', None)
                    low_limit = getattr(data, 'low_limit', None) or getattr(data, 'down_limit', None)
                    
                    if open_price and high_limit and open_price == high_limit:
                        continue
                    if open_price and low_limit and open_price == low_limit:
                        continue
                except:
                    pass
            
            filtered.append(stock)
        except:
            continue
    
    return filtered


# ==================== 调仓执行 ====================
def rebalance(context, target_stocks):
    """
    执行调仓
    """
    if not target_stocks:
        return
    
    current_stocks = set(context.portfolio.positions.keys())
    target_set = set(target_stocks)
    
    total_value = context.portfolio.total_value
    available = total_value * (1 - MIN_CASH_RATIO)
    target_value = min(available / len(target_stocks), total_value * SINGLE_POSITION)
    
    log.info(f'[调仓] 目标仓位: {target_value:.0f}/只')
    
    # 卖出
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
    
    # 买入
    buy_count = 0
    try:
        current_data = get_snapshot(list(context.portfolio.positions.keys())[:100]) if len(context.portfolio.positions) > 0 else {}
    except:
        current_data = {}
    
    for stock in target_stocks:
        try:
            current_value = 0
            if stock in context.portfolio.positions:
                current_value = context.portfolio.positions[stock].value
            
            if current_value < target_value * 0.9:
                order_target_value(stock, target_value)
                log.info(f'[买入] {stock} 目标:{target_value:.0f}')
                buy_count += 1
                
                if stock not in g.cost_prices:
                    try:
                        if stock in current_data:
                            price = getattr(current_data[stock], 'last_price', None) or \
                                   getattr(current_data[stock], 'last_px', None)
                            if price:
                                g.cost_prices[stock] = price
                                g.highest_prices[stock] = price
                    except:
                        pass
        except Exception as e:
            log.warn(f'[买入失败] {stock}: {e}')
    
    if buy_count > 0:
        log.info(f'[调仓] 买入: {buy_count}只')
    else:
        log.warn('[调仓] 未执行任何买入')


# ==================== 风控检查 ====================
def check_risk(context):
    """
    风控检查
    - 止损：亏损超过8%
    - 止盈：盈利超过30%
    - 移动止损：盈利15%后回撤10%
    """
    try:
        current_data = get_snapshot(list(context.portfolio.positions.keys())[:100]) if len(context.portfolio.positions) > 0 else {}
    except:
        current_data = {}
    
    for stock in list(context.portfolio.positions.keys()):
        try:
            pos = context.portfolio.positions[stock]
            if pos.total_amount == 0:
                continue
            
            current_price = pos.price
            if stock in current_data:
                try:
                    current_price = getattr(current_data[stock], 'last_price', None) or \
                                   getattr(current_data[stock], 'last_px', current_price)
                except:
                    pass
            
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
                if dd > TRAILING_STOP:
                    order_target_value(stock, 0)
                    log.info(f'[移动止损] {stock} 回撤{dd*100:.1f}%')
                    g.cost_prices.pop(stock, None)
                    g.highest_prices.pop(stock, None)
        except Exception as e:
            log.warn(f'[风控异常] {stock}: {e}')


# ==================== 收盘统计 ====================
def after_market_close(context):
    """
    收盘统计
    """
    pos_count = len([p for p in context.portfolio.positions.values() if p.total_amount > 0])
    total = context.portfolio.total_value
    ret = context.portfolio.returns
    
    log.info(f'[收盘] 持仓:{pos_count}只 资产:{total:.0f} 收益:{ret*100:.2f}%')
