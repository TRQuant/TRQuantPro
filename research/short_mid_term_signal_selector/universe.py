from __future__ import annotations

from datetime import datetime
from typing import Tuple

import pandas as pd

from research.short_mid_term_signal_selector.config import SelectorConfig
from research.short_mid_term_signal_selector.jqdata_io import (
    calc_start_date,
    get_all_etfs,
    get_all_stocks,
)


def _parse_date(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d")


def build_universe(cfg: SelectorConfig, as_of_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    构建 universe：
    - 股票：剔除 ST（基于名称包含ST的弱过滤）、剔除新股、剔除低流动性
    - ETF：做基础流动性过滤

    返回：
    - stocks_df: code, display_name, start_date, liquidity_20d
    - etfs_df: code, display_name, start_date, liquidity_20d
    """
    stocks = get_all_stocks(as_of_date)
    etfs = get_all_etfs(as_of_date)

    # 基础字段：JQ 同时有 display_name（中文名）与 name（简称/拼音缩写）。
    # 为避免 rename 造成重复列，这里统一：
    # - name_cn: display_name
    # - name: 原始 name（通常是简称/拼音）
    stocks = stocks.rename(columns={"display_name": "name_cn"})
    etfs = etfs.rename(columns={"display_name": "name_cn"})
    if "name" not in stocks.columns:
        stocks["name"] = stocks.get("name_cn", "")
    if "name" not in etfs.columns:
        etfs["name"] = etfs.get("name_cn", "")

    # 1) ST过滤（弱过滤：名称包含ST/退；用中文名更稳）
    name_for_filter = stocks["name_cn"] if "name_cn" in stocks.columns else stocks["name"]
    stocks = stocks[~name_for_filter.astype(str).str.contains(r"ST|\\*ST|退", regex=True)].copy()

    # 2) 新股过滤（上市天数）
    if "start_date" in stocks.columns:
        listed_days = (_parse_date(as_of_date) - pd.to_datetime(stocks["start_date"])).dt.days
        stocks = stocks[listed_days >= cfg.min_listed_days].copy()

    if "start_date" in etfs.columns:
        listed_days = (_parse_date(as_of_date) - pd.to_datetime(etfs["start_date"])).dt.days
        etfs = etfs[listed_days >= 30].copy()  # ETF上市30天后才参与

    # 3) 流动性过滤（近20日平均成交额）
    # 性能关键：使用 get_price 批量拉取 panel=False，然后 groupby 计算均值
    start_date = calc_start_date(as_of_date, cfg.lookback_days)
    import jqdatasdk as jq

    def add_liquidity_bulk(df: pd.DataFrame, asset_type: str) -> pd.DataFrame:
        codes = df["code"].tolist()
        if not codes:
            out = df.copy()
            out["asset_type"] = asset_type
            out["liquidity_20d"] = float("nan")
            return out

        px = jq.get_price(
            codes,
            start_date=start_date,
            end_date=as_of_date,
            fields=["money"],
            frequency="daily",
            panel=False,
        )
        if px is None or px.empty:
            out = df.copy()
            out["asset_type"] = asset_type
            out["liquidity_20d"] = float("nan")
            return out

        px = px.sort_values(["code", "time"])
        liq = (
            px.groupby("code")["money"]
            .apply(lambda s: float(s.tail(20).mean()))
            .rename("liquidity_20d")
            .reset_index()
        )

        out = df.merge(liq, on="code", how="left")
        out["asset_type"] = asset_type
        return out

    stocks = add_liquidity_bulk(stocks, "stock")
    etfs = add_liquidity_bulk(etfs, "etf")

    stocks = stocks[stocks["liquidity_20d"].fillna(0) >= cfg.min_avg_turnover].copy()
    etfs = etfs[etfs["liquidity_20d"].fillna(0) >= cfg.min_avg_turnover].copy()

    return stocks, etfs

