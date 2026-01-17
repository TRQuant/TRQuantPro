#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advisor V4.0 - Vectorized Fast Validate
======================================

用途：
- 走 UnifiedBacktestManager 的 Fast 层（向量化回测），用于“秒级”快速验证
- 数据口径：JQData（禁用mock、禁用AKShare初始化）

示例：
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python scripts/v4_vectorized_fast_validate.py --start 2025-09-01 --end 2025-12-31
"""

from __future__ import annotations

import argparse
import time
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.advisor_v4.backtest_engine import BacktestEngine  # noqa: E402
from core.advisor_v4.trading_strategy import TradingConfig  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--cash", type=float, default=1_000_000)
    parser.add_argument("--max_positions", type=int, default=8)
    parser.add_argument("--position_size", type=float, default=0.20)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    trading_cfg = TradingConfig(
        max_positions=int(args.max_positions),
        position_size=float(args.position_size),
    )

    engine = BacktestEngine(
        predictor=None,  # Fast层会自动走 fast_mode（不依赖模型/因子），用于速度验证
        trading_config=trading_cfg,
        initial_capital=float(args.cash),
        verbose=bool(args.verbose),
        use_unified_backtest=True,
    )

    t0 = time.time()
    result = engine.run(
        start_date=args.start,
        end_date=args.end,
        rebalance_freq="weekly",
        backtest_levels=["fast"],
    )
    dt = time.time() - t0

    print("\n=== V4 Vectorized Fast Validate Result ===")
    print(f"duration_seconds: {dt:.3f}")
    print(f"total_return: {result.total_return:+.2%}")
    print(f"annualized_return: {result.annualized_return:+.2%}")
    print(f"sharpe_ratio: {result.sharpe_ratio:.3f}")
    print(f"max_drawdown: {result.max_drawdown:.2%}")
    print(f"total_trades: {result.total_trades}")
    print(f"win_rate: {result.win_rate:.2%}")


if __name__ == "__main__":
    main()

