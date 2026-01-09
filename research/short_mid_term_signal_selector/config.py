from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SelectorConfig:
    """
    多因子选股/选ETF配置（短-中期）
    """

    # ---------- 基本参数 ----------
    as_of_date: str | None = None  # None => 使用今天（JQData支持的最近交易日）
    lookback_days: int = 160  # 拉取历史K线窗口（用于计算1m/3m动量、波动等）

    # ---------- Universe 过滤 ----------
    min_listed_days: int = 180  # 新股过滤
    min_avg_turnover: float = 2e7  # 近20日平均成交额过滤（人民币）

    # ---------- 输出 ----------
    top_n_stocks: int = 30
    top_n_etfs: int = 20

    # ---------- 因子权重（横截面zscore后加权）----------
    # 动量/趋势（短-中期）
    w_mom_20: float = 0.25
    w_mom_60: float = 0.30
    w_trend_ma: float = 0.15
    w_week_mom_4: float = 0.15   # 周线4周动量（短线）
    w_week_mom_12: float = 0.15  # 周线12周动量（中线）
    w_trend_quality: float = 0.20  # 回归斜率×R²（趋势强度×稳定度）

    # 风险与回撤（惩罚项）
    w_vol_20: float = -0.15
    w_mdd_60: float = -0.15

    # 流动性（奖励项）
    w_liquidity: float = 0.10

    # 可选：成长性（如果能取到财务字段就启用，否则自动跳过）
    enable_growth_factor: bool = False
    w_growth: float = 0.20

