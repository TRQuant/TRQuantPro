# -*- coding: utf-8 -*-
"""
TRQuant V4 Fast Validate (BulletTrade / 聚宽兼容)
==============================================

目标：
- 用 BulletTrade 在“聚宽研究环境口径”下做 **快速验证**（分钟级），不追求最终最优收益
- 核心思路：小股票池 + 周频调仓 + 简单动量打分 + 指数风险开关

说明：
- BulletTrade 与聚宽 API 兼容（from jqdata import *）
- 为了速度：stock_pool 默认使用 HS300 成分股的前 N 只
"""

from jqdata import *
import numpy as np
import pandas as pd

BENCH = "000300.XSHG"

# ====== 速度优先参数 ======
MAX_UNIVERSE = 60          # 股票池上限（越小越快）
MAX_POSITIONS = 8          # 最大持仓数
REBALANCE_WEEKDAY = 0      # 0=周一（Python weekday）

# 动量参数
MOM_S = 5
MOM_L = 20

# 风控：指数趋势开关（简化）
INDEX_FAST = 20
INDEX_SLOW = 60
RISK_ON = 1.0
RISK_MID = 0.5
RISK_OFF = 0.0

# 交易成本
SLIPPAGE = 0.001


def initialize(context):
    set_benchmark(BENCH)
    set_slippage(FixedSlippage(SLIPPAGE))
    set_order_cost(
        OrderCost(
            open_tax=0,
            close_tax=0.001,
            open_commission=0.0003,
            close_commission=0.0003,
            min_commission=5,
        ),
        type="stock",
    )
    set_option("use_real_price", True)

    context.stock_pool = []
    context.target_gross = 0.0
    context.risk_state = "MID"

    run_daily(before_market_open, time="09:00")
    run_daily(market_open, time="09:35")

    log.info(f"[V4_FAST] init: universe={MAX_UNIVERSE} pos={MAX_POSITIONS} mom={MOM_S}/{MOM_L} weekly")


def before_market_open(context):
    # 1) 股票池（为了速度，默认只取HS300前N）
    # 必须传递当前日期，确保获取历史成分股
    current_date = context.current_dt.strftime('%Y-%m-%d') if hasattr(context, 'current_dt') and context.current_dt else None
    if current_date is None:
        log.error('[V4_FAST] 无法获取当前日期，无法更新股票池')
        context.stock_pool = []
        return
    
    try:
        pool = get_index_stocks(BENCH, date=current_date)
        if not pool or len(pool) == 0:
            log.error(f'[V4_FAST] 获取指数成分股失败: 返回空列表，日期={current_date}')
            context.stock_pool = []
        else:
            context.stock_pool = pool[:MAX_UNIVERSE]
            log.info(f'[V4_FAST] 获取指数成分股成功: {len(context.stock_pool)}只，日期={current_date}')
    except Exception as e:
        log.error(f'[V4_FAST] get_index_stocks失败: {e}，日期={current_date}')
        raise  # 不兜底，明确报错

    # 2) 风险开关
    context.risk_state, context.target_gross = judge_market_risk(context)
    log.info(f"[V4_FAST] pre: pool={len(context.stock_pool)} risk={context.risk_state} gross={context.target_gross:.2f}")


def judge_market_risk(context):
    end = context.current_dt.strftime("%Y-%m-%d")
    try:
        df = get_price(
            BENCH,
            end_date=end,
            frequency="daily",
            fields=["close"],
            count=INDEX_SLOW + 5,
            panel=False,
        )
        if df is None or df.empty:
            return "MID", RISK_MID

        close = df["close"].values
        if len(close) < INDEX_SLOW:
            return "MID", RISK_MID

        s = pd.Series(close)
        ma_fast = s.rolling(INDEX_FAST).mean().iloc[-1]
        ma_slow = s.rolling(INDEX_SLOW).mean().iloc[-1]

        if ma_fast > ma_slow * 1.005:
            return "ON", RISK_ON
        if ma_fast < ma_slow * 0.995:
            return "OFF", RISK_OFF
        return "MID", RISK_MID
    except Exception as e:
        log.warn(f"[V4_FAST] risk judge err: {e}")
        return "MID", RISK_MID


def market_open(context):
    if context.target_gross <= 0.01:
        # 风险关：清仓
        for s in list(context.portfolio.positions.keys()):
            order_target_value(s, 0)
        return

    # 周频调仓
    if context.current_dt.weekday() != REBALANCE_WEEKDAY:
        return

    stocks = basic_filter(context, context.stock_pool)
    if len(stocks) == 0:
        log.warn("[V4_FAST] universe empty after filter")
        return

    targets = select_by_momentum(context, stocks)
    if not targets:
        log.warn("[V4_FAST] selection empty")
        return

    rebalance(context, targets)


def basic_filter(context, stocks):
    current_data = get_current_data()
    res = []
    for s in stocks:
        try:
            d = current_data[s]
            if getattr(d, "paused", False):
                continue
            name = getattr(d, "name", "")
            if "ST" in name:
                continue
            res.append(s)
        except Exception:
            continue
    return res


def select_by_momentum(context, stocks):
    end = context.current_dt.strftime("%Y-%m-%d")
    need = MOM_L + 5
    try:
        df = get_price(
            stocks,
            end_date=end,
            frequency="daily",
            fields=["close"],
            count=need,
            panel=False,
        )
        if df is None or df.empty:
            return []
        # BulletTrade/JQ兼容环境下，get_price 可能返回多种形态：
        # 1) long-form: columns=[time, code, close]
        # 2) wide-form: columns=[code1, code2, ...]
        # 3) MultiIndex columns: [('close','000001.XSHE'), ...] 或 [('000001.XSHE','close'), ...]
        if isinstance(getattr(df, "columns", None), pd.MultiIndex):
            lv0 = df.columns.get_level_values(0)
            lv1 = df.columns.get_level_values(1)
            if "close" in set(lv0):
                px = df["close"].copy()
            elif "close" in set(lv1):
                px = df.xs("close", axis=1, level=1).copy()
            else:
                px = df.copy()
        elif "time" in df.columns and "code" in df.columns and "close" in df.columns:
            px = df.pivot(index="time", columns="code", values="close")
        else:
            px = df.copy()

        # 兜底：如果 columns 还是 MultiIndex，取最后一层作为 code（避免出现 ('close', code) 这类 tuple）
        if isinstance(getattr(px, "columns", None), pd.MultiIndex):
            px.columns = px.columns.get_level_values(-1)

        if len(px) < MOM_L + 1:
            return []

        mom_s = px.iloc[-1] / px.iloc[-1 - MOM_S] - 1
        mom_l = px.iloc[-1] / px.iloc[-1 - MOM_L] - 1
        score = 0.5 * mom_s + 0.5 * mom_l
        score = score.replace([np.inf, -np.inf], np.nan).dropna()
        score = score[score > 0]  # 只要上升动量
        if score.empty:
            return []

        top = score.nlargest(min(MAX_POSITIONS, len(score))).index.tolist()
        log.info(f"[V4_FAST] picks: {top[:5]} ... n={len(top)}")
        return top
    except Exception as e:
        log.warn(f"[V4_FAST] momentum err: {e}")
        return []


def rebalance(context, targets):
    # 卖出非目标
    for s in list(context.portfolio.positions.keys()):
        if s not in targets:
            order_target_value(s, 0)

    # 等权买入
    weight = context.target_gross / len(targets)
    weight = min(weight, 0.20)
    total_value = context.portfolio.total_value
    for s in targets:
        order_target_value(s, total_value * weight)

