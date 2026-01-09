#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BulletTrade 快速验证入口（V4 Fast Validate）

特点：
- 走 BulletTrade 引擎（聚宽API兼容）
- 默认关闭报告生成（避免慢 & 避免 akshare/py_mini_racer 相关 warning 链路）
- 默认短周期（用户可改参数）
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.bullettrade import BulletTradeEngine, BTConfig


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--cash", type=float, default=1_000_000)
    parser.add_argument("--benchmark", default="000300.XSHG")
    parser.add_argument("--strategy", default="strategies/bullettrade/TRQuant_v4_fast_validate.py")
    parser.add_argument("--output", default="backtest_results/bullettrade_v4_fast_validate")
    parser.add_argument("--report", action="store_true", help="生成HTML/CSV报告（会变慢）")
    args = parser.parse_args()

    strategy_path = Path(args.strategy)
    if not strategy_path.exists():
        raise FileNotFoundError(f"Strategy not found: {strategy_path}")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = BTConfig(
        start_date=args.start,
        end_date=args.end,
        initial_capital=args.cash,
        benchmark=args.benchmark,
        data_provider="jqdata",
        frequency="day",
        output_dir=str(out_dir),
        generate_html=bool(args.report),
        generate_csv=bool(args.report),
        generate_images=False,
    )

    engine = BulletTradeEngine(cfg)
    result = engine.run_backtest(strategy_path=str(strategy_path))

    print("\n=== BulletTrade Fast Validate Result ===")
    print(f"total_return: {result.total_return:.2f}%")
    print(f"annual_return: {result.annual_return:.2f}%")
    print(f"sharpe_ratio: {result.sharpe_ratio:.2f}")
    print(f"max_drawdown: {result.max_drawdown:.2f}%")
    print(f"win_rate: {result.win_rate:.2f}%")
    print(f"total_trades: {result.total_trades}")
    print(f"output_dir: {out_dir}")


if __name__ == "__main__":
    main()

