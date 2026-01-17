from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd


@dataclass
class JQSessionInfo:
    authed: bool
    spare_queries: Optional[int] = None
    as_of_date: Optional[str] = None


def _try_auth_jqdata() -> JQSessionInfo:
    """
    复用项目现有的 config/config_manager.py 进行认证。
    不与现有框架耦合，但允许复用配置文件与账号信息。
    """
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager

        cfg = get_config_manager().get_config("jqdata")
        if cfg:
            jq.auth(cfg.get("username"), cfg.get("password"))
        authed = bool(jq.is_auth())
        spare = None
        if authed:
            try:
                perm = jq.get_query_count()
                spare = perm.get("spare")
            except Exception:
                spare = None
        return JQSessionInfo(authed=authed, spare_queries=spare)
    except Exception:
        return JQSessionInfo(authed=False)


def ensure_jqdata(as_of_date: Optional[str] = None) -> JQSessionInfo:
    """
    确保已认证，并返回一个“可用日期”（最近交易日）。
    """
    info = _try_auth_jqdata()
    if not info.authed:
        return info

    import jqdatasdk as jq

    if as_of_date is None:
        # 用今天回退到最近交易日
        today = datetime.now().strftime("%Y-%m-%d")
        trade_days = jq.get_trade_days(end_date=today, count=10)
        as_of_date = trade_days[-1].strftime("%Y-%m-%d")

    info.as_of_date = as_of_date
    return info


def get_all_stocks(as_of_date: str) -> pd.DataFrame:
    """
    返回 A 股股票列表（过滤掉已退市的）。
    """
    import jqdatasdk as jq

    df = jq.get_all_securities(types=["stock"], date=as_of_date)
    df = df.reset_index().rename(columns={"index": "code"})
    # JQ字段：display_name, start_date, end_date, type, ...
    return df


def get_all_etfs(as_of_date: str) -> pd.DataFrame:
    """
    返回 ETF 列表。
    """
    import jqdatasdk as jq

    df = jq.get_all_securities(types=["etf"], date=as_of_date)
    df = df.reset_index().rename(columns={"index": "code"})
    return df


def get_price_panel(
    code: str,
    start_date: str,
    end_date: str,
    fields: Optional[list[str]] = None,
) -> pd.DataFrame:
    """
    拉取单标的日频价格数据（包含成交量与成交额）。
    """
    import jqdatasdk as jq

    if fields is None:
        fields = ["open", "high", "low", "close", "volume", "money"]
    df = jq.get_price(code, start_date=start_date, end_date=end_date, frequency="daily", fields=fields)
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.reset_index()
    if "index" in df.columns:
        df = df.rename(columns={"index": "date"})
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df


def calc_start_date(as_of_date: str, lookback_days: int) -> str:
    """
    粗略回退自然日，避免交易日计算过重；后续用实际数据长度兜底。
    """
    dt = datetime.strptime(as_of_date, "%Y-%m-%d")
    start = dt - timedelta(days=int(lookback_days * 1.8))
    return start.strftime("%Y-%m-%d")

