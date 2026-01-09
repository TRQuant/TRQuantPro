from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import pandas as pd

from research.short_mid_term_signal_selector.config import SelectorConfig


def zscore(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    m = s.mean()
    std = s.std()
    if std == 0 or np.isnan(std):
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - m) / std


@dataclass
class ScoredUniverse:
    df: pd.DataFrame
    factor_weights: Dict[str, float]


def score_universe(factors_df: pd.DataFrame, cfg: SelectorConfig) -> ScoredUniverse:
    """
    横截面标准化后加权得到综合得分：
    - 正向因子：mom_20, mom_60, trend_ma, liquidity
    - 负向因子：vol_20, mdd_60
    """
    df = factors_df.copy()

    # 处理缺失值：先用列中位数填充（避免因缺失导致被直接剔除）
    for col in [
        "mom_20",
        "mom_60",
        "week_mom_4",
        "week_mom_12",
        "trend_quality",
        "trend_ma",
        "liquidity",
        "vol_20",
        "mdd_60",
    ]:
        if col not in df.columns:
            df[col] = np.nan
        med = float(df[col].median()) if df[col].notna().any() else 0.0
        df[col] = df[col].astype(float).fillna(med)

    df["z_mom_20"] = zscore(df["mom_20"])
    df["z_mom_60"] = zscore(df["mom_60"])
    df["z_week_mom_4"] = zscore(df["week_mom_4"])
    df["z_week_mom_12"] = zscore(df["week_mom_12"])
    df["z_trend_quality"] = zscore(df["trend_quality"])
    df["z_trend_ma"] = zscore(df["trend_ma"])
    df["z_liquidity"] = zscore(np.log1p(df["liquidity"].clip(lower=0)))
    df["z_vol_20"] = zscore(df["vol_20"])
    df["z_mdd_60"] = zscore(df["mdd_60"])

    weights = {
        "z_mom_20": cfg.w_mom_20,
        "z_mom_60": cfg.w_mom_60,
        "z_week_mom_4": cfg.w_week_mom_4,
        "z_week_mom_12": cfg.w_week_mom_12,
        "z_trend_quality": cfg.w_trend_quality,
        "z_trend_ma": cfg.w_trend_ma,
        "z_liquidity": cfg.w_liquidity,
        "z_vol_20": cfg.w_vol_20,
        "z_mdd_60": cfg.w_mdd_60,
    }

    # 贡献项（便于可解释性）
    df["score_mom_20"] = df["z_mom_20"] * weights["z_mom_20"]
    df["score_mom_60"] = df["z_mom_60"] * weights["z_mom_60"]
    df["score_week_mom_4"] = df["z_week_mom_4"] * weights["z_week_mom_4"]
    df["score_week_mom_12"] = df["z_week_mom_12"] * weights["z_week_mom_12"]
    df["score_trend_quality"] = df["z_trend_quality"] * weights["z_trend_quality"]
    df["score_trend_ma"] = df["z_trend_ma"] * weights["z_trend_ma"]
    df["score_liquidity"] = df["z_liquidity"] * weights["z_liquidity"]
    df["score_vol_20"] = df["z_vol_20"] * weights["z_vol_20"]
    df["score_mdd_60"] = df["z_mdd_60"] * weights["z_mdd_60"]

    df["score_total"] = (
        df["score_mom_20"]
        + df["score_mom_60"]
        + df["score_week_mom_4"]
        + df["score_week_mom_12"]
        + df["score_trend_quality"]
        + df["score_trend_ma"]
        + df["score_liquidity"]
        + df["score_vol_20"]
        + df["score_mdd_60"]
    )

    # 日周共振标记：日线动量/周线动量同向为 True（用于报告解释，不直接额外加分）
    df["day_week_resonance"] = (df["mom_20"] > 0) & (df["week_mom_4"] > 0)

    df = df.sort_values("score_total", ascending=False)
    return ScoredUniverse(df=df, factor_weights=weights)


def split_top_lists(scored: ScoredUniverse, cfg: SelectorConfig) -> Dict[str, pd.DataFrame]:
    df = scored.df
    stocks = df[df["asset_type"] == "stock"].head(cfg.top_n_stocks).copy()
    etfs = df[df["asset_type"] == "etf"].head(cfg.top_n_etfs).copy()
    return {"stocks": stocks, "etfs": etfs}

