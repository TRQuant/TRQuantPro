from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Tuple

import pandas as pd

from research.short_mid_term_signal_selector.config import SelectorConfig
from research.short_mid_term_signal_selector.factors import FactorRow, compute_factors_for_price_df
from research.short_mid_term_signal_selector.jqdata_io import calc_start_date


def compute_factor_table_bulk(
    universe_df: pd.DataFrame,
    as_of_date: str,
    cfg: SelectorConfig,
) -> pd.DataFrame:
    """
    批量拉取价格数据（panel=False），按 code 分组计算因子。
    """
    if universe_df.empty:
        return pd.DataFrame()

    import jqdatasdk as jq

    codes = universe_df["code"].tolist()
    start_date = calc_start_date(as_of_date, cfg.lookback_days)

    px = jq.get_price(
        codes,
        start_date=start_date,
        end_date=as_of_date,
        fields=["open", "high", "low", "close", "volume", "money"],
        frequency="daily",
        panel=False,
    )
    if px is None or px.empty:
        return pd.DataFrame()

    px = px.sort_values(["code", "time"])
    px = px.rename(columns={"time": "date"})

    meta = universe_df.set_index("code")[["name", "asset_type", "liquidity_20d"]].to_dict("index")

    rows: List[Dict] = []
    for code, g in px.groupby("code"):
        g = g.reset_index(drop=True)
        m = meta.get(code, {})
        row = compute_factors_for_price_df(
            code=code,
            name=m.get("name", ""),
            asset_type=m.get("asset_type", ""),
            price_df=g,
        )
        d = asdict(row)
        d["liquidity_20d"] = float(m.get("liquidity_20d")) if m.get("liquidity_20d") is not None else d.get("liquidity")
        rows.append(d)

    df = pd.DataFrame(rows)
    # 用 universe 的 liquidity_20d 覆盖（更快、与过滤一致）
    if "liquidity_20d" in universe_df.columns:
        df = df.merge(universe_df[["code", "liquidity_20d"]], on="code", how="left", suffixes=("", "_u"))
        df["liquidity"] = df["liquidity_20d_u"].fillna(df["liquidity"])
        df = df.drop(columns=["liquidity_20d_u"])
    return df

