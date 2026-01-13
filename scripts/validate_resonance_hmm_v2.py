#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Resonance V2 HMM 回测验证脚本
============================

验证内容：
1. 5年历史数据验证 (2019-2024)
2. 子样本验证：牛市(2020-2021)、熊市(2022)、震荡(2023)
3. CFA标准评估指标

评估维度：
- 收益：年化、月胜率、收益分布
- 风险：最大回撤、回撤持续时间
- 交易质量：换手率
- 稳健性：子样本稳定性

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import warnings
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd

# 添加项目路径
PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

# 忽略警告
warnings.filterwarnings('ignore')

from core.resonance_v2 import (
    ResonanceHMMAnalyzer,
    ResonanceV2Config,
    MarketState,
    MarketDataProvider,
)

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# =============== 验证配置 ===============

VALIDATION_PERIODS = [
    {
        "name": "2019-2020 (牛市前期)",
        "start_date": "2019-01-01",
        "end_date": "2020-12-31",
        "market_type": "mixed"
    },
    {
        "name": "2021-2022 (牛转熊)",
        "start_date": "2021-01-01",
        "end_date": "2022-12-31",
        "market_type": "bear"
    },
    {
        "name": "2023-2024 (震荡)",
        "start_date": "2023-01-01",
        "end_date": "2024-12-31",
        "market_type": "sideways"
    },
]

# 子样本验证
SUB_SAMPLES = [
    {"name": "牛市期 (2020.3-2021.2)", "start": "2020-03-01", "end": "2021-02-28"},
    {"name": "熊市期 (2022.1-2022.10)", "start": "2022-01-01", "end": "2022-10-31"},
    {"name": "震荡期 (2023.1-2023.12)", "start": "2023-01-01", "end": "2023-12-31"},
]

INDEX_CODE = "000300.XSHG"  # 沪深300


# =============== 评估函数 ===============

def calculate_metrics(returns: pd.Series) -> Dict:
    """
    计算CFA标准评估指标
    """
    if returns.empty or returns.isna().all():
        return {
            'total_return': 0,
            'annual_return': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
            'win_rate': 0,
            'monthly_win_rate': 0,
            'volatility': 0,
            'calmar_ratio': 0,
        }
    
    # 基本收益
    total_return = (1 + returns).prod() - 1
    
    # 年化收益
    n_days = len(returns)
    annual_return = (1 + total_return) ** (252 / max(n_days, 1)) - 1
    
    # 波动率（年化）
    volatility = returns.std() * np.sqrt(252)
    
    # 夏普比率（假设无风险利率3%）
    risk_free = 0.03
    excess_return = annual_return - risk_free
    sharpe_ratio = excess_return / volatility if volatility > 0 else 0
    
    # 最大回撤
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = abs(drawdown.min())
    
    # 胜率
    win_rate = (returns > 0).sum() / len(returns) if len(returns) > 0 else 0
    
    # 月度胜率
    monthly_returns = returns.resample('M').apply(lambda x: (1 + x).prod() - 1)
    monthly_win_rate = (monthly_returns > 0).sum() / len(monthly_returns) if len(monthly_returns) > 0 else 0
    
    # Calmar比率
    calmar_ratio = annual_return / max_drawdown if max_drawdown > 0 else 0
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'win_rate': win_rate,
        'monthly_win_rate': monthly_win_rate,
        'volatility': volatility,
        'calmar_ratio': calmar_ratio,
    }


def calculate_state_accuracy(
    predictions: List[Dict],
    actual_returns: pd.Series
) -> Dict:
    """
    计算状态预测准确性
    
    通过比较预测状态与实际市场表现来评估
    """
    correct = 0
    total = 0
    
    state_returns = {state.value: [] for state in MarketState}
    
    for pred in predictions:
        date = pred['date']
        state = pred['hmm_state']
        
        if date in actual_returns.index:
            ret = actual_returns[date]
            state_returns[state].append(ret)
            total += 1
            
            # 判断准确性
            if state == 'risk_on' and ret > 0:
                correct += 1
            elif state == 'risk_off' and ret < 0:
                correct += 1
            elif state == 'sideways' and abs(ret) < 0.01:
                correct += 1
    
    accuracy = correct / total if total > 0 else 0
    
    # 计算各状态的平均收益
    avg_returns = {
        state: np.mean(rets) if rets else 0
        for state, rets in state_returns.items()
    }
    
    return {
        'accuracy': accuracy,
        'total_predictions': total,
        'correct_predictions': correct,
        'avg_returns_by_state': avg_returns,
    }


def run_strategy_backtest(
    analyzer: ResonanceHMMAnalyzer,
    index_code: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 1_000_000
) -> Tuple[pd.DataFrame, Dict]:
    """
    运行策略回测
    
    规则：
    - Risk-On: 满仓
    - Sideways: 60%仓位
    - Risk-Off: 30%仓位
    """
    logger.info(f"回测: {index_code} [{start_date} ~ {end_date}]")
    
    # 获取分析结果
    results_df = analyzer.analyze_batch(index_code, start_date, end_date, use_walk_forward=True)
    
    if results_df.empty:
        logger.warning("分析结果为空")
        return pd.DataFrame(), {}
    
    # 获取价格数据
    data_provider = MarketDataProvider()
    market_data = data_provider.get_index_data(index_code, start_date, end_date)
    
    if market_data.trading_days == 0:
        logger.warning("价格数据为空")
        return pd.DataFrame(), {}
    
    # 计算收益
    price_df = market_data.data.copy()
    price_df['date'] = pd.to_datetime(price_df['date'] if 'date' in price_df.columns else price_df.index)
    price_df = price_df.set_index('date')
    price_df['returns'] = price_df['close'].pct_change()
    
    # 合并分析结果
    results_df['date'] = pd.to_datetime(results_df['date'])
    results_df = results_df.set_index('date')
    
    # 对齐日期
    common_dates = results_df.index.intersection(price_df.index)
    results_df = results_df.loc[common_dates]
    price_df = price_df.loc[common_dates]
    
    # 根据状态确定仓位
    position_map = {
        'risk_on': 1.0,
        'sideways': 0.6,
        'high_vol': 0.5,
        'risk_off': 0.3,
    }
    
    results_df['position'] = results_df['hmm_state'].map(position_map).fillna(0.5)
    
    # 计算策略收益
    results_df['strategy_returns'] = results_df['position'].shift(1) * price_df['returns']
    results_df['benchmark_returns'] = price_df['returns']
    
    # 计算累计收益
    results_df['strategy_cumulative'] = (1 + results_df['strategy_returns'].fillna(0)).cumprod()
    results_df['benchmark_cumulative'] = (1 + results_df['benchmark_returns'].fillna(0)).cumprod()
    
    # 计算指标
    strategy_metrics = calculate_metrics(results_df['strategy_returns'].dropna())
    benchmark_metrics = calculate_metrics(results_df['benchmark_returns'].dropna())
    
    # 计算超额收益
    excess_return = strategy_metrics['annual_return'] - benchmark_metrics['annual_return']
    
    # 状态分布
    state_counts = results_df['hmm_state'].value_counts(normalize=True).to_dict()
    
    summary = {
        'strategy': strategy_metrics,
        'benchmark': benchmark_metrics,
        'excess_return': excess_return,
        'state_distribution': state_counts,
        'n_trades': len(results_df),
        'period': f"{start_date} ~ {end_date}",
    }
    
    return results_df, summary


def run_full_validation():
    """
    运行完整验证
    """
    print("=" * 70)
    print("Resonance V2 HMM 5年回测验证")
    print("=" * 70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"验证指数: {INDEX_CODE}")
    print()
    
    # 初始化分析器
    config = ResonanceV2Config()
    analyzer = ResonanceHMMAnalyzer(config)
    
    all_results = []
    
    # 1. 验证各时段
    print("=" * 60)
    print("1. 分时段验证")
    print("=" * 60)
    
    for period in VALIDATION_PERIODS:
        print(f"\n验证时段: {period['name']}")
        print("-" * 40)
        
        try:
            results_df, summary = run_strategy_backtest(
                analyzer,
                INDEX_CODE,
                period['start_date'],
                period['end_date']
            )
            
            if summary:
                strat = summary['strategy']
                bench = summary['benchmark']
                
                print(f"策略年化收益: {strat['annual_return']:.2%}")
                print(f"基准年化收益: {bench['annual_return']:.2%}")
                print(f"超额收益: {summary['excess_return']:.2%}")
                print(f"夏普比率: {strat['sharpe_ratio']:.2f}")
                print(f"最大回撤: {strat['max_drawdown']:.2%}")
                print(f"月度胜率: {strat['monthly_win_rate']:.1%}")
                print(f"状态分布: {summary['state_distribution']}")
                
                all_results.append({
                    'period': period['name'],
                    'type': period['market_type'],
                    **strat,
                    'benchmark_return': bench['annual_return'],
                    'excess_return': summary['excess_return'],
                })
            else:
                print("验证失败")
                
        except Exception as e:
            logger.error(f"验证 {period['name']} 失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 2. 子样本验证
    print("\n" + "=" * 60)
    print("2. 子样本验证")
    print("=" * 60)
    
    for sample in SUB_SAMPLES:
        print(f"\n子样本: {sample['name']}")
        print("-" * 40)
        
        try:
            results_df, summary = run_strategy_backtest(
                analyzer,
                INDEX_CODE,
                sample['start'],
                sample['end']
            )
            
            if summary:
                strat = summary['strategy']
                print(f"策略年化: {strat['annual_return']:.2%}, 夏普: {strat['sharpe_ratio']:.2f}, 回撤: {strat['max_drawdown']:.2%}")
                
        except Exception as e:
            logger.error(f"子样本 {sample['name']} 验证失败: {e}")
    
    # 3. 生成汇总报告
    print("\n" + "=" * 70)
    print("3. 验证结果汇总")
    print("=" * 70)
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        print("\n| 时段 | 市场类型 | 策略年化 | 基准年化 | 超额 | 夏普 | 回撤 | 月胜率 |")
        print("|------|----------|----------|----------|------|------|------|--------|")
        
        for _, row in df.iterrows():
            print(f"| {row['period'][:15]} | {row['type']} | {row['annual_return']:.1%} | "
                  f"{row['benchmark_return']:.1%} | {row['excess_return']:.1%} | "
                  f"{row['sharpe_ratio']:.2f} | {row['max_drawdown']:.1%} | {row['monthly_win_rate']:.0%} |")
        
        # 平均值
        avg_excess = df['excess_return'].mean()
        avg_sharpe = df['sharpe_ratio'].mean()
        avg_dd = df['max_drawdown'].mean()
        
        print(f"\n平均超额收益: {avg_excess:.2%}")
        print(f"平均夏普比率: {avg_sharpe:.2f}")
        print(f"平均最大回撤: {avg_dd:.2%}")
    
    # 4. 保存报告
    output_dir = PROJECT_ROOT / "output" / "resonance_v2_validation"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"validation_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Resonance V2 HMM 5年回测验证报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**验证指数**: {INDEX_CODE}\n\n")
        
        f.write("## 1. 配置参数\n\n")
        f.write(f"- HMM状态数: {config.n_hmm_states}\n")
        f.write(f"- 训练窗口: {config.train_window}天\n")
        f.write(f"- 测试窗口: {config.test_window}天\n")
        f.write(f"- 慢周期: {config.slow_cycle}天\n")
        f.write(f"- 快周期: {config.fast_cycle}天\n\n")
        
        f.write("## 2. 验证结果\n\n")
        f.write("| 时段 | 策略年化 | 基准年化 | 超额 | 夏普 | 回撤 |\n")
        f.write("|------|----------|----------|------|------|------|\n")
        
        if all_results:
            for r in all_results:
                f.write(f"| {r['period']} | {r['annual_return']:.1%} | "
                       f"{r['benchmark_return']:.1%} | {r['excess_return']:.1%} | "
                       f"{r['sharpe_ratio']:.2f} | {r['max_drawdown']:.1%} |\n")
        
        f.write("\n## 3. 结论\n\n")
        if all_results:
            if avg_excess > 0:
                f.write(f"策略在5年验证期内平均超额收益为 **{avg_excess:.2%}**，验证通过。\n")
            else:
                f.write(f"策略超额收益为负，需要进一步优化参数。\n")
    
    print(f"\n报告已保存: {report_path}")
    print(f"\n完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_results


if __name__ == "__main__":
    run_full_validation()
