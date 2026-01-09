#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场趋势分析模块回测验证脚本
==============================

验证 MarketTrendAnalyzer 的信号准确率和预测效果

功能:
1. 过去1年日频信号生成
2. 对比14种阶段分布与实际涨跌
3. 仓位建议与实际收益相关性
4. 输出准确率和信噪比

使用方法:
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python scripts/validate_market_trend_v3.py

版本: 1.0
日期: 2026-01-07
"""

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import logging
import argparse
from collections import Counter

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_jqdata() -> bool:
    """初始化JQData"""
    try:
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        
        if jq_config:
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            if jq.is_auth():
                logger.info("JQData认证成功")
                return True
        
        logger.warning("JQData认证失败")
        return False
    except Exception as e:
        logger.error(f"JQData初始化异常: {e}")
        return False


def get_trading_dates(start_date: str, end_date: str) -> List[str]:
    """获取交易日列表"""
    try:
        import jqdatasdk as jq
        dates = jq.get_trade_days(start_date=start_date, end_date=end_date)
        return [d.strftime("%Y-%m-%d") for d in dates]
    except Exception as e:
        logger.error(f"获取交易日失败: {e}")
        return []


def get_index_returns(index_code: str, dates: List[str]) -> pd.DataFrame:
    """获取指数收益率数据"""
    try:
        import jqdatasdk as jq
        
        if not dates:
            return pd.DataFrame()
        
        start_date = dates[0]
        end_date = dates[-1]
        
        # 获取价格数据（多取一些用于计算收益率）
        start_dt = datetime.strptime(start_date, "%Y-%m-%d") - timedelta(days=10)
        
        df = jq.get_price(
            index_code,
            start_date=start_dt.strftime("%Y-%m-%d"),
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            skip_paused=False,
            fq='pre',
        )
        
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.reset_index()
        df.columns = ['date', 'close']
        df['date'] = df['date'].dt.strftime("%Y-%m-%d")
        
        # 计算各期收益率
        df['ret_1d'] = df['close'].pct_change(1)
        df['ret_5d'] = df['close'].pct_change(5)
        df['ret_10d'] = df['close'].pct_change(10)
        df['ret_20d'] = df['close'].pct_change(20)
        
        # 计算未来收益率（用于评估预测效果）
        df['fwd_ret_1d'] = df['close'].shift(-1) / df['close'] - 1
        df['fwd_ret_5d'] = df['close'].shift(-5) / df['close'] - 1
        df['fwd_ret_10d'] = df['close'].shift(-10) / df['close'] - 1
        df['fwd_ret_20d'] = df['close'].shift(-20) / df['close'] - 1
        
        return df
    except Exception as e:
        logger.error(f"获取指数数据失败: {e}")
        return pd.DataFrame()


def run_backtest_signals(
    dates: List[str],
    sample_interval: int = 5,  # 每N天采样一次
) -> Tuple[List[Dict], pd.DataFrame]:
    """
    运行回测生成信号
    
    Args:
        dates: 交易日列表
        sample_interval: 采样间隔
        
    Returns:
        (signals_list, returns_df)
    """
    from core.market_trend_analyzer import (
        MarketTrendAnalyzer,
        MarketTrendAnalyzerConfig,
    )
    from core.resonance_state_model import MarketSwitchSpec, ResonanceConfig
    
    # 初始化分析器
    config = MarketTrendAnalyzerConfig(
        scoring_style="smooth_grouped",
        active_periods=["week", "month", "quarter"],
    )
    analyzer = MarketTrendAnalyzer(config)
    
    # 获取收益率数据
    returns_df = get_index_returns("000300.XSHG", dates)
    if returns_df.empty:
        logger.error("无法获取收益率数据")
        return [], pd.DataFrame()
    
    # 采样日期
    sample_dates = dates[::sample_interval]
    logger.info(f"采样日期数: {len(sample_dates)} (每{sample_interval}天)")
    
    signals = []
    confirm_history = {}
    
    for i, date in enumerate(sample_dates):
        try:
            # 使用共振分析
            signal = analyzer.analyze_composite(
                as_of_date=date,
                confirm_history=confirm_history,
            )
            
            if signal:
                # 获取诊断信息
                diag = analyzer.get_diagnostic_details(signal)
                
                # 构建信号记录
                record = {
                    "date": date,
                    "ensemble_score": signal.ensemble_score,
                    "direction": signal.ensemble_direction.value,
                    "market_phase": signal.market_phase.value if signal.market_phase else "",
                    "market_phase_name": signal.market_phase.name if signal.market_phase else "",
                    "position_cap": signal.position_cap,
                    "market_phase_position": signal.market_phase_position,
                    "resonance_phase": signal.resonance_phase.value,
                    "confirm_streak": signal.confirm_streak,
                    "strategy_mode": signal.strategy_mode.value,
                    "hmm_state": signal.hmm_signal.state.value if signal.hmm_signal else "",
                    "hmm_confidence": signal.hmm_signal.confidence if signal.hmm_signal else 0,
                    "week_score": signal.period_signals.get("week").score if "week" in signal.period_signals else 0,
                    "month_score": signal.period_signals.get("month").score if "month" in signal.period_signals else 0,
                    "quarter_score": signal.period_signals.get("quarter").score if "quarter" in signal.period_signals else 0,
                }
                
                signals.append(record)
                confirm_history[date] = signal.confirm_streak
                
                if (i + 1) % 20 == 0:
                    logger.info(f"已处理 {i + 1}/{len(sample_dates)} 个日期")
                    
        except Exception as e:
            logger.warning(f"处理日期 {date} 失败: {e}")
    
    logger.info(f"生成信号数: {len(signals)}")
    return signals, returns_df


def analyze_signal_accuracy(
    signals: List[Dict],
    returns_df: pd.DataFrame,
    forward_days: int = 5,
) -> Dict[str, Any]:
    """
    分析信号准确率
    
    Args:
        signals: 信号列表
        returns_df: 收益率DataFrame
        forward_days: 评估未来N日收益
        
    Returns:
        分析结果字典
    """
    if not signals or returns_df.empty:
        return {"error": "数据不足"}
    
    signals_df = pd.DataFrame(signals)
    
    # 合并收益率数据
    fwd_col = f"fwd_ret_{forward_days}d"
    if fwd_col not in returns_df.columns:
        fwd_col = "fwd_ret_5d"  # 默认
    
    merged = signals_df.merge(
        returns_df[['date', fwd_col]],
        on='date',
        how='left'
    )
    merged = merged.dropna(subset=[fwd_col])
    
    if merged.empty:
        return {"error": "合并后无数据"}
    
    results = {
        "total_signals": len(merged),
        "forward_days": forward_days,
    }
    
    # 1. 方向准确率
    # 看多（score>10）且实际上涨 或 看空（score<-10）且实际下跌
    merged['pred_direction'] = merged['ensemble_score'].apply(
        lambda x: 1 if x > 10 else (-1 if x < -10 else 0)
    )
    merged['actual_direction'] = merged[fwd_col].apply(
        lambda x: 1 if x > 0.005 else (-1 if x < -0.005 else 0)
    )
    
    # 只看有明确方向的信号
    directional = merged[merged['pred_direction'] != 0]
    if len(directional) > 0:
        correct_direction = (directional['pred_direction'] == directional['actual_direction']).sum()
        results['direction_accuracy'] = correct_direction / len(directional)
        results['directional_signals'] = len(directional)
    else:
        results['direction_accuracy'] = 0
        results['directional_signals'] = 0
    
    # 2. 按市场阶段分析
    phase_stats = {}
    for phase in merged['market_phase'].unique():
        if not phase:
            continue
        phase_data = merged[merged['market_phase'] == phase]
        phase_stats[phase] = {
            "count": len(phase_data),
            "avg_return": phase_data[fwd_col].mean(),
            "win_rate": (phase_data[fwd_col] > 0).mean(),
            "avg_score": phase_data['ensemble_score'].mean(),
        }
    results['phase_stats'] = phase_stats
    
    # 3. 分组收益相关性
    # 按评分分组，看与实际收益的单调性
    merged['score_group'] = pd.qcut(
        merged['ensemble_score'],
        q=5,
        labels=['Very_Low', 'Low', 'Medium', 'High', 'Very_High'],
        duplicates='drop'
    )
    
    group_returns = merged.groupby('score_group')[fwd_col].mean()
    results['group_returns'] = group_returns.to_dict()
    
    # 计算IC（信息系数）
    ic = merged['ensemble_score'].corr(merged[fwd_col])
    results['information_coefficient'] = ic
    
    # 4. 仓位建议与收益相关性
    position_ic = merged['position_cap'].corr(merged[fwd_col])
    results['position_return_corr'] = position_ic
    
    # 5. 各周期信号质量
    for period in ['week', 'month', 'quarter']:
        col = f"{period}_score"
        if col in merged.columns:
            period_ic = merged[col].corr(merged[fwd_col])
            results[f'{period}_ic'] = period_ic
    
    # 6. 市场阶段分布
    results['phase_distribution'] = dict(Counter(merged['market_phase']))
    
    return results


def print_analysis_report(results: Dict[str, Any]):
    """打印分析报告"""
    print("\n" + "=" * 70)
    print("市场趋势分析模块回测验证报告")
    print("=" * 70)
    
    if "error" in results:
        print(f"\n错误: {results['error']}")
        return
    
    print(f"\n【基本统计】")
    print(f"  总信号数: {results['total_signals']}")
    print(f"  评估周期: 未来{results['forward_days']}日")
    print(f"  方向性信号数: {results.get('directional_signals', 0)}")
    print(f"  方向准确率: {results.get('direction_accuracy', 0):.1%}")
    print(f"  信息系数(IC): {results.get('information_coefficient', 0):.3f}")
    print(f"  仓位-收益相关性: {results.get('position_return_corr', 0):.3f}")
    
    # 各周期IC
    print(f"\n【各周期信息系数】")
    for period in ['week', 'month', 'quarter']:
        ic = results.get(f'{period}_ic', 0)
        print(f"  {period}: {ic:.3f}")
    
    # 分组收益
    print(f"\n【评分分组平均收益】")
    group_returns = results.get('group_returns', {})
    for group, ret in group_returns.items():
        print(f"  {group}: {ret*100:+.2f}%")
    
    # 市场阶段统计
    print(f"\n【14种市场阶段统计】")
    phase_stats = results.get('phase_stats', {})
    sorted_phases = sorted(phase_stats.items(), key=lambda x: x[1]['avg_return'], reverse=True)
    
    print(f"  {'阶段':<25} {'次数':<6} {'平均收益':<10} {'胜率':<8} {'平均评分':<10}")
    print("-" * 70)
    for phase, stats in sorted_phases:
        print(f"  {phase:<25} {stats['count']:<6} {stats['avg_return']*100:+.2f}%{'':<4} "
              f"{stats['win_rate']:.1%}{'':<4} {stats['avg_score']:+.1f}")
    
    # 阶段分布
    print(f"\n【市场阶段分布】")
    phase_dist = results.get('phase_distribution', {})
    total = sum(phase_dist.values())
    sorted_dist = sorted(phase_dist.items(), key=lambda x: x[1], reverse=True)
    for phase, count in sorted_dist:
        pct = count / total if total > 0 else 0
        print(f"  {phase}: {count} ({pct:.1%})")
    
    print("\n" + "=" * 70)
    
    # 总结
    ic = results.get('information_coefficient', 0)
    dir_acc = results.get('direction_accuracy', 0)
    
    print("\n【结论】")
    if ic > 0.05 and dir_acc > 0.55:
        print("  ✅ 信号质量良好: IC > 0.05 且 方向准确率 > 55%")
    elif ic > 0.03 or dir_acc > 0.52:
        print("  ⚠️ 信号质量一般: 有一定预测能力但需进一步优化")
    else:
        print("  ❌ 信号质量不足: 需要审查模型参数或数据质量")
    
    print("")


def main():
    parser = argparse.ArgumentParser(description='市场趋势分析模块回测验证')
    parser.add_argument('--days', type=int, default=250, help='回测天数')
    parser.add_argument('--interval', type=int, default=5, help='采样间隔')
    parser.add_argument('--forward', type=int, default=5, help='评估未来N日收益')
    parser.add_argument('--output', type=str, default='', help='输出CSV路径')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("市场趋势分析模块回测验证")
    print("=" * 60)
    
    # 初始化JQData
    if not init_jqdata():
        print("JQData初始化失败，退出")
        sys.exit(1)
    
    # 获取交易日
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    
    print(f"\n日期范围: {start_date} ~ {end_date}")
    print(f"采样间隔: 每{args.interval}天")
    print(f"评估周期: 未来{args.forward}日")
    
    dates = get_trading_dates(start_date, end_date)
    print(f"交易日数: {len(dates)}")
    
    if not dates:
        print("无交易日数据，退出")
        sys.exit(1)
    
    # 运行回测
    print("\n正在生成信号...")
    signals, returns_df = run_backtest_signals(dates, sample_interval=args.interval)
    
    if not signals:
        print("无信号生成，退出")
        sys.exit(1)
    
    # 分析结果
    print("\n正在分析结果...")
    results = analyze_signal_accuracy(signals, returns_df, forward_days=args.forward)
    
    # 打印报告
    print_analysis_report(results)
    
    # 导出数据
    if args.output:
        signals_df = pd.DataFrame(signals)
        signals_df.to_csv(args.output, index=False, encoding='utf-8-sig')
        print(f"\n信号数据已导出: {args.output}")
    
    print("验证完成!")


if __name__ == "__main__":
    main()
