from __future__ import annotations

from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def _df_to_html_table(df: pd.DataFrame, max_rows: int = 50) -> str:
    if df is None or df.empty:
        return "<p><em>(empty)</em></p>"
    show = df.head(max_rows).copy()
    return show.to_html(index=False, escape=False)


def render_html_report(
    *,
    title: str,
    as_of_date: str,
    cfg_dict: Dict,
    stocks_top: pd.DataFrame,
    etfs_top: pd.DataFrame,
    factor_weights: Dict[str, float],
    notes: Optional[str] = None,
) -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def fmt_weights(d: Dict[str, float]) -> str:
        rows = [{"factor": k, "weight": v} for k, v in d.items()]
        return _df_to_html_table(pd.DataFrame(rows), max_rows=200)

    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Microsoft YaHei", sans-serif; background:#0b1220; color:#e5e7eb; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
    h1,h2,h3 {{ margin: 12px 0; }}
    .card {{ background:#0f1a30; border:1px solid #1f2a44; border-radius: 12px; padding: 16px 18px; margin: 14px 0; }}
    .muted {{ color:#9ca3af; }}
    table {{ width:100%; border-collapse: collapse; }}
    th, td {{ border:1px solid #22304f; padding: 8px 10px; font-size: 13px; }}
    th {{ background:#111c33; }}
    code {{ background:#111c33; padding:2px 6px; border-radius:6px; }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
    <p class="muted">生成时间：{ts} ｜ 截止交易日：<code>{as_of_date}</code></p>

    <div class="card">
      <h2>策略定位</h2>
      <ul>
        <li><strong>目标</strong>：短期-中期跟随近期上涨行情，输出候选<strong>个股</strong>与<strong>ETF</strong>清单</li>
        <li><strong>方式</strong>：多因子横截面标准化（zscore）后加权打分</li>
        <li><strong>参考</strong>：日线+周线趋势共振过滤噪音，捕捉主升浪（见内部参考文档）</li>
        <li><strong>说明</strong>：当前仅做“信号选股/选ETF”，暂不包含持仓期/止损/仓位等交易规则</li>
      </ul>
      {f"<p><strong>备注</strong>：{notes}</p>" if notes else ""}
    </div>

    <div class="card">
      <h2>产业热点/主线（结构位，后续可深化）</h2>
      <p class="muted">
        这里优先展示 <strong>ETF Top榜</strong> 作为“行业/主题强度”的代理；
        后续可加入：行业轮动、ETF成分股映射、政策/景气度因子等。
      </p>
      <ul>
        <li><strong>日周共振</strong>：报告表中 <code>day_week_resonance</code> = True 表示日线与周线动量同向</li>
        <li><strong>趋势质量</strong>：<code>trend_quality</code> 使用回归斜率×R²，偏好“强且稳”的趋势</li>
      </ul>
    </div>

    <div class="card">
      <h2>配置参数</h2>
      {_df_to_html_table(pd.DataFrame([cfg_dict]), max_rows=1)}
    </div>

    <div class="card">
      <h2>因子权重（对 zscore 后的因子）</h2>
      {fmt_weights(factor_weights)}
      <p class="muted">负权重表示惩罚项（如波动、回撤）。</p>
    </div>

    <div class="card">
      <h2>Top 个股（候选）</h2>
      {_df_to_html_table(stocks_top, max_rows=50)}
    </div>

    <div class="card">
      <h2>Top ETF（候选）</h2>
      {_df_to_html_table(etfs_top, max_rows=50)}
    </div>

    <div class="card">
      <h2>下一步建议（后续开发）</h2>
      <ul>
        <li><strong>风控</strong>：基于标的波动/回撤/行业属性设置差异化仓位上限与止损</li>
        <li><strong>交易规则</strong>：加入持仓期（T+5/T+20）、趋势破坏退出、盈利保护</li>
        <li><strong>成长增强</strong>：接入财务成长（营收/利润增速）作为可选因子，并做行业中性化</li>
      </ul>
    </div>
  </div>
</body>
</html>
"""
    return html


def save_report(html: str, filename: str) -> Path:
    out_dir = Path("output") / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / filename
    path.write_text(html, encoding="utf-8")
    return path

