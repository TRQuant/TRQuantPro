# -*- coding: utf-8 -*-
"""
TRQuant 主线趋势轮动策略 V2 - 改进版
====================================
基于用户专业分析的完整改进版本

关键改进：
1. 分批获取价格数据（不再只取前50只）
2. 改进兜底策略（基于流动性排序）
3. 使用真实成本价（pos.avg_cost）
4. 周频调仓（降低换手）
5. 自适应风控（ATR/波动）
6. 指数趋势判断控制仓位
7. 主线行业/概念过滤（可配置）
"""

from jqdata import *
import numpy as np
import pandas as pd

# ==================== 策略参数 ====================
BENCH = '000300.XSHG'

MAX_STOCKS = 10
BUFFER = 5                 # 保留缓冲：持仓若仍在前 MAX+BUFFER，不卖（降低抖动）
MIN_CASH_RATIO = 0.08
SINGLE_POSITION = 0.18     # 单票上限

REBALANCE_WEEKDAY = 1      # 周几调仓：1=周一（聚宽：0=周一，1=周二...）
MOM_S = 5                  # 短动量（周）
MOM_L = 20                 # 长动量（月）

# 指数趋势参数（风险开关）
INDEX_MA_FAST = 20
INDEX_MA_SLOW = 60
RISK_ON_POS = 1.00         # 风险开：满仓
RISK_MID_POS = 0.50        # 风险中：半仓
RISK_OFF_POS = 0.00        # 风险关：空仓/极低仓

# 风控：自适应（ATR倍数/波动倍数）
ATR_N = 14
STOP_ATR = 2.2             # 止损：跌破成本 - STOP_ATR*ATR
TRAIL_ATR = 2.8            # 移动止损：从最高价回撤超过 TRAIL_ATR*ATR 触发
TAKE_PROFIT_R = 4.0        # 可选：盈利超过 TAKE_PROFIT_R*ATR 触发减仓

# 主线过滤方式（可配置）
USE_INDUSTRY_FILTER = False  # 需要配置行业代码
INDUSTRY_CODES = []          # 示例：['801750', '801080'] 等

USE_CONCEPT_FILTER = False   # 需要预处理概念标签
CONCEPT_KEYWORDS = ['人工智能', '算力', '半导体', '信创', '国产替代']


# ==================== 初始化 ====================
def initialize(context):
    """策略初始化"""
    set_benchmark(BENCH)
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    context.stock_pool = []
    context.cost = {}            # 成本（用 pos.avg_cost 同步）
    context.highest = {}         # 持仓以来最高价
    context.risk_state = 'OFF'   # OFF/MID/ON
    context.target_gross = 0.0   # 目标总仓位（0~1）
    
    # 任务调度
    run_daily(before_market_open, time='09:00')
    run_daily(market_open, time='09:35')
    run_daily(check_risk, time='14:50')
    run_daily(after_market_close, time='15:30')
    
    log.info('=' * 50)
    log.info('TRQuant 主线趋势轮动策略 V2 - 改进版')
    log.info(f'持股: {MAX_STOCKS}只 | 仓位: {SINGLE_POSITION*100:.0f}%')
    log.info(f'调仓: 周频(周{REBALANCE_WEEKDAY+1}) | 动量: {MOM_S}/{MOM_L}日')
    log.info('=' * 50)


# ==================== 盘前 ====================
def before_market_open(context):
    """盘前准备"""
    # 1) 更新股票池
    try:
        context.stock_pool = get_index_stocks(BENCH)
        log.info(f'[盘前] 更新股票池: {len(context.stock_pool)}只')
    except Exception as e:
        log.warn(f'[盘前] 获取指数成分股失败: {e}')
        try:
            context.stock_pool = get_all_securities(['stock']).index.tolist()[:300]
            log.info(f'[盘前] 使用全市场股票池: {len(context.stock_pool)}只')
        except:
            context.stock_pool = []
    
    # 2) 更新风险状态（指数趋势->目标仓位）
    context.risk_state, context.target_gross = judge_market_risk(context)
    
    # 3) 同步真实成本（避免用 last_price 伪成本）
    sync_cost_prices(context)
    
    log.info(f'[盘前] risk={context.risk_state} target_gross={context.target_gross:.2f}')


def judge_market_risk(context):
    """
    用指数均线判断风险开关：
    - MA20 > MA60：风险开（满仓）
    - MA20 介于/接近 MA60：风险中（半仓）
    - MA20 < MA60：风险关（空仓）
    """
    end = context.current_dt.strftime('%Y-%m-%d')
    try:
        df = get_price(BENCH, end_date=end, frequency='daily', 
                      fields=['close'], count=INDEX_MA_SLOW+5, panel=False)
        if df is None or df.empty:
            return 'MID', RISK_MID_POS
        
        close = df['close'].values
        if len(close) < INDEX_MA_SLOW:
            return 'MID', RISK_MID_POS
        
        ma_fast = pd.Series(close).rolling(INDEX_MA_FAST).mean().iloc[-1]
        ma_slow = pd.Series(close).rolling(INDEX_MA_SLOW).mean().iloc[-1]
        
        if ma_fast > ma_slow * 1.005:
            return 'ON', RISK_ON_POS
        elif ma_fast < ma_slow * 0.995:
            return 'OFF', RISK_OFF_POS
        else:
            return 'MID', RISK_MID_POS
    except Exception as e:
        log.warn(f'[风险判断] 异常: {e}')
        return 'MID', RISK_MID_POS


# ==================== 开盘：周频调仓 ====================
def market_open(context):
    """开盘交易"""
    if context.target_gross <= 0.01:
        # 风险关：清仓
        liquidate_all(context, reason='RISK_OFF')
        return
    
    # 周频调仓：只在特定 weekday 执行
    # 聚宽：0=周一, 1=周二, ..., 6=周日
    wd = context.current_dt.weekday()
    if wd != REBALANCE_WEEKDAY:
        return
    
    log.info(f'[调仓日] 周{wd+1}')
    
    candidates = build_universe(context)
    targets = select_stocks(context, candidates)
    
    if not targets:
        log.warn('[调仓] 选不出票，按风险状态控制仓位')
        return
    
    log.info(f'[调仓] 选股结果: {len(targets)}只候选')
    rebalance(context, targets)


def build_universe(context):
    """组合股票池 + 主线过滤 + 基础过滤"""
    stocks = context.stock_pool[:]
    stocks = basic_filter(context, stocks)
    
    if USE_INDUSTRY_FILTER and INDUSTRY_CODES:
        stocks = industry_filter(context, stocks, INDUSTRY_CODES)
    
    if USE_CONCEPT_FILTER and CONCEPT_KEYWORDS:
        stocks = concept_filter_by_keywords(context, stocks, CONCEPT_KEYWORDS)
    
    return stocks


def basic_filter(context, stocks):
    """基础过滤：停牌/ST/新股/涨跌停"""
    current_data = get_current_data()
    now = context.current_dt.date()
    res = []
    
    for s in stocks:
        try:
            d = current_data[s]
            if getattr(d, 'paused', False):
                continue
            
            # 新股过滤（60天）
            try:
                info = get_security_info(s)
                if (now - info.start_date).days < 60:
                    continue
            except:
                pass
            
            # 涨跌停过滤（用 last_price 更稳）
            hl = getattr(d, 'high_limit', None)
            ll = getattr(d, 'low_limit', None)
            lp = getattr(d, 'last_price', None)
            if hl and lp and lp >= hl * 0.999:
                continue
            if ll and lp and lp <= ll * 1.001:
                continue
            
            res.append(s)
        except:
            continue
    
    # ST过滤：务必全量/分批，不要只取前100
    res = filter_st_flags(context, res)
    return res


def filter_st_flags(context, stocks, batch=200):
    """ST过滤：分批处理，确保全覆盖"""
    if not stocks:
        return stocks
    day = context.current_dt.strftime('%Y-%m-%d')
    keep = []
    for i in range(0, len(stocks), batch):
        part = stocks[i:i+batch]
        try:
            st = get_extras('is_st', part, start_date=day, end_date=day, df=True)
            if st is None or st.empty:
                keep += part
            else:
                st_list = st.columns[st.iloc[0] == True].tolist()
                keep += [s for s in part if s not in st_list]
        except:
            keep += part
    return keep


def industry_filter(context, stocks, industry_codes):
    """行业过滤：交集过滤"""
    allow = set()
    for code in industry_codes:
        try:
            allow |= set(get_industry_stocks(code))
        except:
            pass
    if not allow:
        return stocks
    return [s for s in stocks if s in allow]


def concept_filter_by_keywords(context, stocks, keywords):
    """
    概念过滤：需要预处理概念标签
    TODO: 在韬睿系统预处理：给每只股票打 concept 标签，然后在这里读取
    """
    # 当前版本：返回原列表（需要你实现概念标签读取）
    return stocks


# ==================== 选股：动量 + 流动性/波动 ====================
def select_stocks(context, stocks):
    """选股逻辑 - 改进版：分批取价 + 波动惩罚"""
    if len(stocks) < MAX_STOCKS:
        return stocks[:MAX_STOCKS]
    
    end = context.current_dt.strftime('%Y-%m-%d')
    
    # 关键改进：分批获取价格数据，不再只取前50只
    close = batch_get_price_pivot(stocks, end, fields=['close'], count=MOM_L+5, batch=120)
    if close is None or close.shape[0] < MOM_L:
        log.warn('[选股] 价格数据不足，使用兜底策略')
        return fallback_liquidity(context, stocks)
    
    close = close.sort_index()
    
    # 有效交易天数比例过滤
    valid_ratio = close.tail(MOM_L).notna().mean()
    close = close.loc[:, valid_ratio >= 0.8]
    if close.shape[1] < MAX_STOCKS:
        log.warn('[选股] 有效股票不足，使用兜底策略')
        return fallback_liquidity(context, stocks)
    
    # 计算动量
    mom_s = close.pct_change(MOM_S).iloc[-1]
    mom_l = close.pct_change(MOM_L).iloc[-1]
    
    # 质量/稳定：用波动惩罚（防止全买"最疯的"导致回撤巨大）
    ret1 = close.pct_change(1)
    vol = ret1.tail(MOM_L).std()  # 简易波动
    vol = vol.replace(0, np.nan)
    
    # 综合打分：趋势为主，波动惩罚
    score = (0.7*mom_l + 0.3*mom_s) / (vol ** 0.5)
    score = score.dropna()
    
    # 只保留"至少一个动量为正"
    score = score[(mom_l > 0) | (mom_s > 0)].dropna()
    if len(score) < MAX_STOCKS:
        # 不够就放宽
        score = ((0.7*mom_l + 0.3*mom_s).dropna()).nlargest(MAX_STOCKS + BUFFER)
    
    # 选出候选池（含 buffer，给 rebalance 做"保留机制"）
    pick = score.nlargest(MAX_STOCKS + BUFFER).index.tolist()
    log.info(f'[选股] 选股成功: {len(pick)}只候选')
    return pick


def batch_get_price_pivot(stocks, end, fields, count, batch=120):
    """
    关键改进：分批获取价格数据，确保覆盖全部候选股票
    """
    frames = []
    for i in range(0, len(stocks), batch):
        part = stocks[i:i+batch]
        try:
            df = get_price(part, end_date=end, frequency='daily', 
                          fields=fields, count=count, panel=False)
            if df is None or df.empty:
                continue
            frames.append(df)
        except Exception as e:
            log.warn(f'[分批取价] 批次 {i//batch+1} 失败: {e}')
            continue
    
    if not frames:
        return None
    
    try:
        df = pd.concat(frames, axis=0, ignore_index=True)
        if 'time' in df.columns and 'code' in df.columns:
            return df.pivot(index='time', columns='code', values=fields[0])
        return df
    except Exception as e:
        log.error(f'[分批取价] 合并失败: {e}')
        return None


def fallback_liquidity(context, stocks):
    """
    改进兜底策略：按近20日成交额排序（比 stocks[:N] 强得多）
    """
    end = context.current_dt.strftime('%Y-%m-%d')
    try:
        df = get_price(stocks[:400], end_date=end, frequency='daily', 
                      fields=['money'], count=20, panel=False)
        if df is None or df.empty:
            log.warn('[兜底] 成交额数据获取失败，使用原顺序')
            return stocks[:MAX_STOCKS + BUFFER]
        money = df.groupby('code')['money'].sum().sort_values(ascending=False)
        selected = money.index[:MAX_STOCKS + BUFFER].tolist()
        log.info(f'[兜底] 按流动性选股: {len(selected)}只')
        return selected
    except Exception as e:
        log.warn(f'[兜底] 异常: {e}，使用原顺序')
        return stocks[:MAX_STOCKS + BUFFER]


# ==================== 调仓：保留机制 + 风险仓位控制 ====================
def rebalance(context, target_ranked):
    """
    调仓逻辑：保留机制 + 风险仓位控制
    target_ranked: 包含 MAX+BUFFER 个候选
    """
    current = list(context.portfolio.positions.keys())
    cur_set = set(current)
    
    # 1) 确定"最终目标持仓"：先保留现有，再补足
    target_pool = target_ranked[:]  # MAX+BUFFER
    keep = [s for s in current if s in target_pool]
    
    # 优先级：保留现有，再用排名靠前的补足
    final = keep[:]
    for s in target_ranked:
        if len(final) >= MAX_STOCKS:
            break
        if s not in final:
            final.append(s)
    
    final_set = set(final)
    
    # 2) 风险状态决定总仓位
    total_value = context.portfolio.total_value
    gross_cap = total_value * context.target_gross
    investable = gross_cap * (1 - MIN_CASH_RATIO)
    
    # 单票目标（并受 SINGLE_POSITION 约束）
    per_value = investable / max(1, len(final))
    per_value = min(per_value, total_value * SINGLE_POSITION)
    
    log.info(f'[调仓] risk={context.risk_state} target={len(final)} per={per_value:.0f}')
    
    # 3) 先卖：不在 final 的卖出（但注意跌停可能卖不掉）
    current_data = get_current_data()
    for s in list(cur_set - final_set):
        if can_sell(current_data, s):
            order_target_value(s, 0)
            context.cost.pop(s, None)
            context.highest.pop(s, None)
            log.info(f'[卖出] {s}')
        else:
            log.warn(f'[卖出跳过] {s} 可能跌停/不可卖')
    
    # 4) 再买/调：final 内调到目标市值
    for s in final:
        if not can_buy(current_data, s):
            log.info(f'[买入跳过] {s} 可能涨停/停牌')
            continue
        order_target_value(s, per_value)
        log.info(f'[调仓到] {s} -> {per_value:.0f}')


def can_buy(current_data, stock):
    """判断是否可以买入"""
    try:
        d = current_data[stock]
        if getattr(d, 'paused', False):
            return False
        hl = getattr(d, 'high_limit', None)
        lp = getattr(d, 'last_price', None)
        if hl and lp and lp >= hl * 0.999:
            return False
        return True
    except:
        return False


def can_sell(current_data, stock):
    """判断是否可以卖出"""
    try:
        d = current_data[stock]
        if getattr(d, 'paused', False):
            return False
        ll = getattr(d, 'low_limit', None)
        lp = getattr(d, 'last_price', None)
        if ll and lp and lp <= ll * 1.001:
            return False
        return True
    except:
        return False


def liquidate_all(context, reason=''):
    """清仓"""
    current_data = get_current_data()
    for s in list(context.portfolio.positions.keys()):
        if can_sell(current_data, s):
            order_target_value(s, 0)
            context.cost.pop(s, None)
            context.highest.pop(s, None)
    log.warn(f'[清仓] {reason}')


# ==================== 风控：ATR/波动自适应 ====================
def check_risk(context):
    """风控检查：ATR/波动自适应"""
    current_data = get_current_data()
    day = context.current_dt.strftime('%Y-%m-%d')
    
    for s in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[s]
        if pos.total_amount <= 0:
            continue
        
        lp = current_data[s].last_price
        cost = context.cost.get(s, pos.avg_cost)
        if cost <= 0:
            continue
        
        # 更新最高价
        hi = context.highest.get(s, lp)
        hi = max(hi, lp)
        context.highest[s] = hi
        
        # 计算 ATR（简化：用 high/low/close）
        atr = calc_atr(s, day, ATR_N)
        if atr is None or atr <= 0:
            continue
        
        # 1) 自适应止损：跌破成本 - STOP_ATR*ATR
        stop_price = cost - STOP_ATR * atr
        if lp < stop_price:
            if can_sell(current_data, s):
                order_target_value(s, 0)
                log.warn(f'[ATR止损] {s} lp={lp:.2f} stop={stop_price:.2f}')
                context.cost.pop(s, None)
                context.highest.pop(s, None)
            continue
        
        # 2) 移动止损：从最高价回撤超过 TRAIL_ATR*ATR
        trail_price = hi - TRAIL_ATR * atr
        if lp < trail_price and (hi - cost) > 1.0 * atr:  # 先要求有一定浮盈再启用
            if can_sell(current_data, s):
                order_target_value(s, 0)
                log.info(f'[ATR移动止损] {s} lp={lp:.2f} trail={trail_price:.2f}')
                context.cost.pop(s, None)
                context.highest.pop(s, None)
            continue


def calc_atr(stock, end_date, n=14):
    """计算ATR（平均真实波幅）"""
    try:
        df = get_price(stock, end_date=end_date, frequency='daily',
                      fields=['high', 'low', 'close'], count=n+2, panel=False)
        if df is None or df.empty or len(df) < n+1:
            return None
        
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values
        prev_close = np.roll(close, 1)
        prev_close[0] = close[0]
        
        tr = np.maximum(high - low, 
                       np.maximum(np.abs(high - prev_close), 
                                 np.abs(low - prev_close)))
        atr = pd.Series(tr).rolling(n).mean().iloc[-1]
        return float(atr) if atr == atr else None
    except Exception as e:
        return None


def sync_cost_prices(context):
    """
    关键改进：同步真实成本（用 pos.avg_cost，不用 last_price）
    """
    for s, pos in context.portfolio.positions.items():
        if pos.total_amount > 0:
            context.cost[s] = pos.avg_cost
            context.highest[s] = max(context.highest.get(s, pos.price), pos.price)


# ==================== 收盘记录 ====================
def after_market_close(context):
    """收盘记录"""
    pos_count = len(context.portfolio.positions)
    total = context.portfolio.total_value
    ret = context.portfolio.returns
    log.info(f'[收盘] risk={context.risk_state} pos={pos_count} total={total:.0f} returns={ret*100:.2f}%')
