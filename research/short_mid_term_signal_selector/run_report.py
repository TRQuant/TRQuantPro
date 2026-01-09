from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

import pandas as pd

from research.short_mid_term_signal_selector.config import SelectorConfig
from research.short_mid_term_signal_selector.jqdata_io import ensure_jqdata
from research.short_mid_term_signal_selector.pipeline import compute_factor_table_bulk
from research.short_mid_term_signal_selector.report import render_html_report, save_report
from research.short_mid_term_signal_selector.scoring import score_universe, split_top_lists
from research.short_mid_term_signal_selector.universe import build_universe


def main() -> None:
    cfg = SelectorConfig()

    info = ensure_jqdata(as_of_date=cfg.as_of_date)
    if not info.authed or not info.as_of_date:
        raise RuntimeError("JQData 未认证或无法获取有效交易日，请检查 config/jqdata 配置。")

    as_of_date = info.as_of_date
    print(f"✅ JQData 已连接，剩余查询: {info.spare_queries}")
    print(f"📅 截止交易日: {as_of_date}")

    print("🔎 构建 universe（股票+ETF）...")
    stocks_u, etfs_u = build_universe(cfg, as_of_date=as_of_date)
    universe = pd.concat([stocks_u, etfs_u], ignore_index=True)
    print(f"   股票数: {len(stocks_u)} | ETF数: {len(etfs_u)} | 合计: {len(universe)}")

    print("🧮 计算因子（批量）...")
    factors_df = compute_factor_table_bulk(universe, as_of_date=as_of_date, cfg=cfg)
    if factors_df.empty:
        raise RuntimeError("因子计算失败：未获取到价格数据。")

    print("🏁 横截面打分...")
    scored = score_universe(factors_df, cfg)
    tops = split_top_lists(scored, cfg)

    keep_cols = [
        "code",
        "name",
        "asset_type",
        "score_total",
        "mom_20",
        "mom_60",
        "week_mom_4",
        "week_mom_12",
        "trend_quality",
        "trend_ma",
        "vol_20",
        "mdd_60",
        "liquidity",
        "day_week_resonance",
        "score_mom_20",
        "score_mom_60",
        "score_week_mom_4",
        "score_week_mom_12",
        "score_trend_quality",
        "score_trend_ma",
        "score_liquidity",
        "score_vol_20",
        "score_mdd_60",
    ]
    stocks_top = tops["stocks"][keep_cols].copy() if not tops["stocks"].empty else tops["stocks"]
    etfs_top = tops["etfs"][keep_cols].copy() if not tops["etfs"].empty else tops["etfs"]

    title = "A股短-中期多因子信号选股/ETF筛选（开发版）"
    html = render_html_report(
        title=title,
        as_of_date=as_of_date,
        cfg_dict=asdict(cfg),
        stocks_top=stocks_top,
        etfs_top=etfs_top,
        factor_weights=scored.factor_weights,
        notes="当前版本优先保证可跑与可解释；风控/持仓规则会在下一阶段补齐。",
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = save_report(html, filename=f"short_mid_term_selector_{ts}.html")
    print(f"✅ 报告已生成: {path}")


if __name__ == "__main__":
    main()

