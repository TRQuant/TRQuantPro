from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


def _safe_pct_change(series: pd.Series, periods: int) -> float:
    if series is None or series.empty or len(series) <= periods:
        return float("nan")
    a = float(series.iloc[-1])
    b = float(series.iloc[-1 - periods])
    if b == 0:
        return float("nan")
    return (a / b) - 1.0


def _max_drawdown(close: pd.Series) -> float:
    if close is None or close.empty:
        return float("nan")
    arr = close.astype(float).values
    peak = np.maximum.accumulate(arr)
    dd = (arr / peak) - 1.0
    return float(dd.min())


def _realized_vol(close: pd.Series, window: int = 20) -> float:
    if close is None or close.empty or len(close) < window + 1:
        return float("nan")
    r = close.astype(float).pct_change().dropna()
    if len(r) < window:
        return float("nan")
    return float(r.tail(window).std() * np.sqrt(252))


def _trend_ma(close: pd.Series, fast: int = 5, slow: int = 20) -> float:
    """
    趋势强度：fast/slow 均线比值-1
    """
    if close is None or close.empty or len(close) < slow:
        return float("nan")
    fast_ma = close.rolling(fast).mean().iloc[-1]
    slow_ma = close.rolling(slow).mean().iloc[-1]
    if slow_ma == 0 or np.isnan(fast_ma) or np.isnan(slow_ma):
        return float("nan")
    return float(fast_ma / slow_ma - 1.0)


def _trend_quality_regression(close: pd.Series, window: int = 60) -> float:
    """
    趋势质量：回归斜率 × R²（对数价格）
    - 斜率体现趋势强度
    - R²体现趋势“干净程度/噪音大小”
    参考思路：趋势强度趋势质量综合评估（斜率表征趋势强度，R²表征趋势质量）
    """
    if close is None or close.empty or len(close) < window:
        return float("nan")
    y = np.log(close.astype(float).tail(window).values)
    x = np.arange(len(y), dtype=float)
    if len(y) < 10:
        return float("nan")
    # 线性回归 y = a*x + b
    a, b = np.polyfit(x, y, 1)
    y_hat = a * x + b
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    r2 = float(np.clip(r2, 0.0, 1.0))
    # 把斜率近似转成“年化”尺度（252交易日）
    slope_ann = float(a * 252.0)
    return slope_ann * r2


@dataclass
class FactorRow:
    code: str
    name: str
    asset_type: str  # "stock" | "etf"

    mom_20: float
    mom_60: float
    week_mom_4: float
    week_mom_12: float
    trend_quality: float
    vol_20: float
    mdd_60: float
    trend_ma: float

    liquidity: float  # avg turnover (money)

    growth: Optional[float] = None


def compute_factors_for_price_df(
    code: str,
    name: str,
    asset_type: str,
    price_df: pd.DataFrame,
) -> FactorRow:
    """
    仅基于价格数据计算（无需财务字段），保证可用性与可迁移性。
    """
    close = price_df["close"] if "close" in price_df.columns else pd.Series(dtype=float)
    money = price_df["money"] if "money" in price_df.columns else pd.Series(dtype=float)

    mom_20 = _safe_pct_change(close, 20)
    mom_60 = _safe_pct_change(close, 60)

    # 周线数据（周五收盘）
    if "date" in price_df.columns:
        dt = pd.to_datetime(price_df["date"])
        tmp = price_df.copy()
        tmp["date"] = dt
        tmp = tmp.set_index("date").sort_index()
        w = tmp.resample("W-FRI").agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
                "money": "sum",
            }
        ).dropna(subset=["close"])
        w_close = w["close"]
    else:
        w_close = pd.Series(dtype=float)

    week_mom_4 = _safe_pct_change(w_close, 4)
    week_mom_12 = _safe_pct_change(w_close, 12)

    trend_quality = _trend_quality_regression(close, window=60)
    vol_20 = _realized_vol(close, 20)
    mdd_60 = _max_drawdown(close.tail(60)) if len(close) >= 60 else _max_drawdown(close)
    trend_ma = _trend_ma(close, 5, 20)

    liquidity = float(money.tail(20).mean()) if len(money) >= 5 else float("nan")

    return FactorRow(
        code=code,
        name=name,
        asset_type=asset_type,
        mom_20=mom_20,
        mom_60=mom_60,
        week_mom_4=week_mom_4,
        week_mom_12=week_mom_12,
        trend_quality=trend_quality,
        vol_20=vol_20,
        mdd_60=mdd_60,
        trend_ma=trend_ma,
        liquidity=liquidity,
        growth=None,
    )

