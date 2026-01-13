#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场趋势月度预测（优化版）
=======================

使用集成模型预测本周及未来一个月的市场趋势。
优化：减少预测频率、添加进度监控、使用缓存。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

from core.ensemble_market_trend import EnsembleMarketTrendAnalyzer, TrendDirection
import jqdatasdk as jq
from config.config_manager import get_config_manager

# 尝试导入tqdm，如果没有则使用简单进度显示
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("⚠️ 未安装tqdm，使用简单进度显示。建议安装: pip install tqdm")

# 初始化JQData
cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])

INDEX_CODE = "000300.XSHG"  # 沪深300

# 预测频率：每N个交易日预测一次（减少计算量）
PREDICTION_INTERVAL = 3  # 每3个交易日预测一次


def get_trading_dates(start_date: str, end_date: str, interval: int = 1) -> List[str]:
    """获取交易日列表（支持采样）"""
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    sampled_days = [d.strftime('%Y-%m-%d') for d in trade_days[::interval]]
    return sampled_days


def predict_market_trend(
    analyzer: EnsembleMarketTrendAnalyzer,
    dates: List[str],
    show_progress: bool = True
) -> List[Dict]:
    """预测多个日期的市场趋势（带进度显示）"""
    results = []
    total = len(dates)
    start_time = time.time()
    
    # 使用tqdm或简单进度显示
    if HAS_TQDM and show_progress:
        date_iter = tqdm(dates, desc="预测进度", unit="日期")
    else:
        date_iter = dates
    
    for idx, date_str in enumerate(date_iter):
        try:
            # 显示进度（如果没有tqdm）
            if not HAS_TQDM and show_progress:
                elapsed = time.time() - start_time
                avg_time = elapsed / (idx + 1) if idx > 0 else 0
                remaining = avg_time * (total - idx - 1)
                progress = (idx + 1) / total * 100
                print(f"\r[{progress:.1f}%] 预测 {date_str} ({idx+1}/{total}) "
                      f"已用: {elapsed:.1f}s 预计剩余: {remaining:.1f}s", end='', flush=True)
            
            result = analyzer.analyze(INDEX_CODE, date_str)
            if result:
                results.append({
                    'date': date_str,
                    'trend': result.final_trend.value,
                    'confidence': result.final_confidence,
                    'consistency': result.consistency,
                    'bull_score': result.bull_score,
                    'bear_score': result.bear_score,
                    'sideways_score': result.sideways_score,
                    'agreement_ratio': result.agreement_ratio,
                    'model_predictions': [
                        {
                            'model': p.model_name,
                            'trend': p.trend.value,
                            'confidence': p.confidence
                        }
                        for p in result.model_predictions
                    ]
                })
        except Exception as e:
            if show_progress:
                print(f"\n⚠️ 预测 {date_str} 失败: {e}")
            continue
    
    if not HAS_TQDM and show_progress:
        print()  # 换行
    
    total_time = time.time() - start_time
    if show_progress:
        print(f"✅ 预测完成，共 {len(results)} 个结果，耗时 {total_time:.1f}秒")
    
    return results


def generate_prediction_report(results: List[Dict], start_date: str, end_date: str):
    """生成预测报告"""
    output_dir = PROJECT_ROOT / "output" / "market_predictions"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"market_trend_prediction_{timestamp}.md"
    
    # 统计趋势分布
    trend_counts = {}
    for r in results:
        trend = r['trend']
        trend_counts[trend] = trend_counts.get(trend, 0) + 1
    
    total = len(results)
    bull_pct = trend_counts.get('bull', 0) / total * 100 if total > 0 else 0
    bear_pct = trend_counts.get('bear', 0) / total * 100 if total > 0 else 0
    sideways_pct = trend_counts.get('sideways', 0) / total * 100 if total > 0 else 0
    
    avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
    avg_consistency = sum(r['consistency'] for r in results) / total if total > 0 else 0
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 市场趋势预测报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**预测指数**: {INDEX_CODE} (沪深300)\n")
        f.write(f"**预测期间**: {start_date} ~ {end_date}\n")
        f.write(f"**预测样本数**: {total} 个交易日\n\n")
        
        f.write("## 1. 执行摘要\n\n")
        f.write(f"**整体趋势判断**: ")
        
        if bull_pct >= 50:
            f.write("**偏牛市** 📈\n")
        elif bear_pct >= 50:
            f.write("**偏熊市** 📉\n")
        else:
            f.write("**震荡市** ➡️\n")
        
        f.write(f"\n**平均置信度**: {avg_confidence:.1%}\n")
        f.write(f"**平均一致性**: {avg_consistency:.1%}\n\n")
        
        f.write("### 趋势分布\n\n")
        f.write("| 趋势 | 占比 | 交易日数 |\n")
        f.write("|------|------|----------|\n")
        f.write(f"| 牛市 | {bull_pct:.1f}% | {trend_counts.get('bull', 0)} |\n")
        f.write(f"| 熊市 | {bear_pct:.1f}% | {trend_counts.get('bear', 0)} |\n")
        f.write(f"| 震荡 | {sideways_pct:.1f}% | {trend_counts.get('sideways', 0)} |\n\n")
        
        f.write("## 2. 详细预测\n\n")
        
        # 按周分组
        current_week = None
        week_results = []
        
        for r in results:
            date_dt = pd.to_datetime(r['date'])
            week_num = date_dt.isocalendar()[1]
            
            if current_week != week_num:
                if week_results:
                    # 输出上一周的结果
                    f.write(f"### 第{current_week}周 ({week_results[0]['date']} ~ {week_results[-1]['date']})\n\n")
                    f.write("| 日期 | 趋势 | 置信度 | 一致性 | 投票得分 |\n")
                    f.write("|------|------|--------|--------|----------|\n")
                    
                    for wr in week_results:
                        trend_emoji = "📈" if wr['trend'] == 'bull' else ("📉" if wr['trend'] == 'bear' else "➡️")
                        f.write(f"| {wr['date']} | {trend_emoji} {wr['trend']} | {wr['confidence']:.1%} | {wr['consistency']:.1%} | "
                               f"牛:{wr['bull_score']:.2f} 熊:{wr['bear_score']:.2f} 震:{wr['sideways_score']:.2f} |\n")
                    
                    # 统计本周趋势
                    week_trends = [wr['trend'] for wr in week_results]
                    week_bull = week_trends.count('bull')
                    week_bear = week_trends.count('bear')
                    week_sideways = week_trends.count('sideways')
                    
                    if week_bull > week_bear and week_bull > week_sideways:
                        week_summary = "**本周整体: 偏牛市** 📈"
                    elif week_bear > week_bull and week_bear > week_sideways:
                        week_summary = "**本周整体: 偏熊市** 📉"
                    else:
                        week_summary = "**本周整体: 震荡市** ➡️"
                    
                    f.write(f"\n{week_summary}\n\n")
                
                current_week = week_num
                week_results = []
            
            week_results.append(r)
        
        # 输出最后一周
        if week_results:
            f.write(f"### 第{current_week}周 ({week_results[0]['date']} ~ {week_results[-1]['date']})\n\n")
            f.write("| 日期 | 趋势 | 置信度 | 一致性 | 投票得分 |\n")
            f.write("|------|------|--------|--------|----------|\n")
            
            for wr in week_results:
                trend_emoji = "📈" if wr['trend'] == 'bull' else ("📉" if wr['trend'] == 'bear' else "➡️")
                f.write(f"| {wr['date']} | {trend_emoji} {wr['trend']} | {wr['confidence']:.1%} | {wr['consistency']:.1%} | "
                       f"牛:{wr['bull_score']:.2f} 熊:{wr['bear_score']:.2f} 震:{wr['sideways_score']:.2f} |\n")
            
            week_trends = [wr['trend'] for wr in week_results]
            week_bull = week_trends.count('bull')
            week_bear = week_trends.count('bear')
            week_sideways = week_trends.count('sideways')
            
            if week_bull > week_bear and week_bull > week_sideways:
                week_summary = "**本周整体: 偏牛市** 📈"
            elif week_bear > week_bull and week_bear > week_sideways:
                week_summary = "**本周整体: 偏熊市** 📉"
            else:
                week_summary = "**本周整体: 震荡市** ➡️"
            
            f.write(f"\n{week_summary}\n\n")
        
        f.write("## 3. 模型预测详情（最新日期）\n\n")
        if results:
            latest = results[-1]
            f.write(f"**预测日期**: {latest['date']}\n\n")
            f.write("| 模型 | 预测趋势 | 置信度 |\n")
            f.write("|------|----------|--------|\n")
            
            for pred in latest['model_predictions']:
                trend_emoji = "📈" if pred['trend'] == 'bull' else ("📉" if pred['trend'] == 'bear' else "➡️")
                f.write(f"| {pred['model']} | {trend_emoji} {pred['trend']} | {pred['confidence']:.1%} |\n")
            
            f.write(f"\n**集成预测**: {latest['trend']} (置信度: {latest['confidence']:.1%})\n")
            f.write(f"**一致性**: {latest['consistency']:.1%}\n")
            f.write(f"**模型同意率**: {latest['agreement_ratio']:.1%}\n")
        
        f.write("\n## 4. 投资建议\n\n")
        
        if bull_pct >= 50:
            f.write("### 偏牛市环境\n\n")
            f.write("- ✅ **建议**: 可以适当增加仓位，关注主线板块\n")
            f.write("- ⚠️ **注意**: 保持风险控制，设置止损\n")
            f.write("- 📊 **策略**: 关注技术指标和市场宽度的确认信号\n")
        elif bear_pct >= 50:
            f.write("### 偏熊市环境\n\n")
            f.write("- ⚠️ **建议**: 降低仓位，保持谨慎\n")
            f.write("- 🛡️ **注意**: 加强风险控制，避免追高\n")
            f.write("- 📊 **策略**: 等待市场底部信号，关注情绪指标反转\n")
        else:
            f.write("### 震荡市环境\n\n")
            f.write("- ➡️ **建议**: 保持中性仓位，高抛低吸\n")
            f.write("- ⚠️ **注意**: 避免追涨杀跌，控制交易频率\n")
            f.write("- 📊 **策略**: 关注个股机会，精选标的\n")
        
        f.write(f"\n**重要提示**: 本预测基于历史数据和技术分析，仅供参考，不构成投资建议。\n")
        f.write(f"实际投资请结合自身风险承受能力和市场实际情况。\n")
    
    return report_path


def main():
    """主函数"""
    print("=" * 80)
    print("市场趋势月度预测（优化版）")
    print("=" * 80)
    
    # 初始化集成分析器
    print("\n初始化集成分析器...")
    analyzer = EnsembleMarketTrendAnalyzer()
    
    # 计算日期范围
    today = datetime.now()
    
    # 本周（从本周一开始）
    days_since_monday = today.weekday()
    week_start = today - timedelta(days=days_since_monday)
    week_end = week_start + timedelta(days=6)
    
    # 未来一个月（从今天开始）
    month_start = today
    month_end = today + timedelta(days=30)
    
    # 获取交易日（采样，减少计算量）
    print(f"\n获取交易日列表...")
    week_dates = get_trading_dates(
        week_start.strftime('%Y-%m-%d'),
        week_end.strftime('%Y-%m-%d'),
        interval=1  # 本周每天预测
    )
    
    month_dates = get_trading_dates(
        month_start.strftime('%Y-%m-%d'),
        month_end.strftime('%Y-%m-%d'),
        interval=PREDICTION_INTERVAL  # 未来一个月每N天预测一次
    )
    
    # 合并日期（去重并排序）
    all_dates = sorted(list(set(week_dates + month_dates)))
    
    print(f"预测期间: {all_dates[0]} ~ {all_dates[-1]}")
    print(f"预测交易日数: {len(all_dates)} (采样间隔: 本周每天，未来每月{PREDICTION_INTERVAL}天)")
    print(f"\n开始预测...\n")
    
    # 执行预测（带进度显示）
    results = predict_market_trend(analyzer, all_dates, show_progress=True)
    
    if not results:
        print("\n❌ 预测失败，没有获取到任何结果")
        return 1
    
    # 生成报告
    print(f"\n生成预测报告...")
    report_path = generate_prediction_report(
        results,
        all_dates[0],
        all_dates[-1]
    )
    
    # 打印摘要
    print("\n" + "=" * 80)
    print("预测摘要")
    print("=" * 80)
    
    trend_counts = {}
    for r in results:
        trend = r['trend']
        trend_counts[trend] = trend_counts.get(trend, 0) + 1
    
    total = len(results)
    bull_pct = trend_counts.get('bull', 0) / total * 100 if total > 0 else 0
    bear_pct = trend_counts.get('bear', 0) / total * 100 if total > 0 else 0
    sideways_pct = trend_counts.get('sideways', 0) / total * 100 if total > 0 else 0
    
    avg_confidence = sum(r['confidence'] for r in results) / total if total > 0 else 0
    
    print(f"\n整体趋势分布:")
    print(f"  牛市: {bull_pct:.1f}% ({trend_counts.get('bull', 0)} 个交易日)")
    print(f"  熊市: {bear_pct:.1f}% ({trend_counts.get('bear', 0)} 个交易日)")
    print(f"  震荡: {sideways_pct:.1f}% ({trend_counts.get('sideways', 0)} 个交易日)")
    print(f"\n平均置信度: {avg_confidence:.1%}")
    
    if bull_pct >= 50:
        print(f"\n📈 整体判断: 偏牛市")
    elif bear_pct >= 50:
        print(f"\n📉 整体判断: 偏熊市")
    else:
        print(f"\n➡️ 整体判断: 震荡市")
    
    print(f"\n详细报告已保存: {report_path}")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
