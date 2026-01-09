#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
验证优化后的参数效果
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 优化后的参数（从优化过程中获取）
OPTIMIZED_CONFIG = {
    "weights": {"trend": 0.77, "hmm": 0.23},
    "indicator_weights": {
        "ma": 0.213, "macd": 0.253, "rsi": 0.116, "bb": 0.154,
        "vol": 0.121, "kdj": 0.065, "adx": 0.108, "flow": 0.190,
    },
    "factor_group_weights": {
        "trend": 0.348, "oscillator": 0.324, "volatility": 0.202, "volume": 0.126,
    },
    "scoring_style": "legacy",
}

# 基线参数
BASELINE_CONFIG = {
    "weights": {"trend": 0.8, "hmm": 0.2},
    "indicator_weights": {
        "ma": 0.20, "macd": 0.18, "rsi": 0.10, "bb": 0.10,
        "vol": 0.12, "kdj": 0.10, "adx": 0.10, "flow": 0.10,
    },
    "factor_group_weights": {
        "trend": 0.45, "oscillator": 0.25, "volatility": 0.15, "volume": 0.15,
    },
    "scoring_style": "smooth_grouped",
}


def init_jqdata():
    import jqdatasdk as jq
    from config.config_manager import get_config_manager
    config_mgr = get_config_manager()
    jq_config = config_mgr.get_config('jqdata')
    if jq_config:
        jq.auth(jq_config.get('username'), jq_config.get('password'))
        return jq.is_auth()
    return False


def get_trading_dates(start_date, end_date):
    import jqdatasdk as jq
    dates = jq.get_trade_days(start_date=start_date, end_date=end_date)
    return [d.strftime("%Y-%m-%d") for d in dates]


def get_returns(dates):
    import jqdatasdk as jq
    if not dates:
        return pd.DataFrame()
    start_dt = datetime.strptime(dates[0], "%Y-%m-%d") - timedelta(days=10)
    df = jq.get_price("000300.XSHG", start_date=start_dt.strftime("%Y-%m-%d"),
                      end_date=dates[-1], frequency='daily', fields=['close'])
    if df is None or df.empty:
        return pd.DataFrame()
    df = df.reset_index()
    df.columns = ['date', 'close']
    df['date'] = df['date'].dt.strftime("%Y-%m-%d")
    df['fwd_ret_5d'] = df['close'].shift(-5) / df['close'] - 1
    return df


def evaluate_config(config_dict, dates, returns_df, sample_interval=7):
    """评估一组配置参数"""
    from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
    
    config = MarketTrendAnalyzerConfig(
        scoring_style=config_dict["scoring_style"],
        weights=config_dict["weights"],
        indicator_weights=config_dict["indicator_weights"],
        factor_group_weights=config_dict["factor_group_weights"],
        active_periods=["week", "month", "quarter"],
    )
    analyzer = MarketTrendAnalyzer(config)
    
    sample_dates = dates[::sample_interval]
    signals = []
    
    for date in sample_dates:
        try:
            signal = analyzer.analyze("000300.XSHG", as_of_date=date)
            if signal:
                signals.append({
                    "date": date,
                    "score": signal.ensemble_score,
                    "position": signal.workflow_params.position_target,
                })
        except:
            pass
    
    if len(signals) < 5:
        return {"ic": 0, "direction_acc": 0.5}
    
    signals_df = pd.DataFrame(signals)
    merged = signals_df.merge(returns_df[['date', 'fwd_ret_5d']], on='date', how='left')
    merged = merged.dropna()
    
    if len(merged) < 5:
        return {"ic": 0, "direction_acc": 0.5}
    
    ic = merged['score'].corr(merged['fwd_ret_5d'])
    if pd.isna(ic):
        ic = 0
    
    merged['pred'] = merged['score'].apply(lambda x: 1 if x > 10 else (-1 if x < -10 else 0))
    merged['actual'] = merged['fwd_ret_5d'].apply(lambda x: 1 if x > 0.005 else (-1 if x < -0.005 else 0))
    directional = merged[merged['pred'] != 0]
    direction_acc = (directional['pred'] == directional['actual']).mean() if len(directional) > 0 else 0.5
    
    return {"ic": ic, "direction_acc": direction_acc, "signals": len(merged)}


def main():
    print("=" * 60)
    print("参数优化效果验证")
    print("=" * 60)
    
    if not init_jqdata():
        print("JQData初始化失败")
        return
    
    # 获取数据
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    
    print(f"\n验证周期: {start_date} ~ {end_date}")
    
    dates = get_trading_dates(start_date, end_date)
    returns_df = get_returns(dates)
    
    print(f"交易日数: {len(dates)}")
    
    # 评估基线
    print("\n评估基线配置...")
    baseline_result = evaluate_config(BASELINE_CONFIG, dates, returns_df)
    
    # 评估优化后
    print("评估优化配置...")
    optimized_result = evaluate_config(OPTIMIZED_CONFIG, dates, returns_df)
    
    # 对比结果
    print("\n" + "=" * 60)
    print("对比结果")
    print("=" * 60)
    print(f"\n{'指标':<20} {'基线':<15} {'优化后':<15} {'改进':<10}")
    print("-" * 60)
    
    for metric in ["ic", "direction_acc"]:
        base_val = baseline_result.get(metric, 0)
        opt_val = optimized_result.get(metric, 0)
        improvement = opt_val - base_val
        
        if metric == "direction_acc":
            print(f"{metric:<20} {base_val:.2%}{'':<10} {opt_val:.2%}{'':<10} {improvement:+.2%}")
        else:
            print(f"{metric:<20} {base_val:.4f}{'':<10} {opt_val:.4f}{'':<10} {improvement:+.4f}")
    
    print(f"\n基线信号数: {baseline_result.get('signals', 0)}")
    print(f"优化信号数: {optimized_result.get('signals', 0)}")
    
    print("\n" + "=" * 60)
    
    if optimized_result.get("ic", 0) > baseline_result.get("ic", 0):
        print("✅ 优化后IC有所提升")
    else:
        print("⚠️ 优化后IC无明显改善")


if __name__ == "__main__":
    main()
