#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSPI概念股票动量分析

分析指定股票的动量因子，并基于短期动量策略给出投资建议。

作者: TRQuant Team
日期: 2026-01-10
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 确保项目路径
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq


def init_jqdata():
    """初始化JQData连接"""
    try:
        cm = get_config_manager()
        cfg = cm.get_config('jqdata')
        jq.auth(cfg['username'], cfg['password'])
        
        if jq.is_auth():
            print("✅ JQData连接成功")
            return True
        else:
            print("❌ JQData认证失败")
            return False
    except Exception as e:
        print(f"❌ JQData初始化失败: {e}")
        return False


def calculate_momentum(stocks, date=None):
    """计算动量因子"""
    if date is None:
        trade_days = jq.get_trade_days(end_date=datetime.now(), count=5)
        date = trade_days[-1].strftime('%Y-%m-%d')
    
    # 获取历史数据
    start_date = (pd.to_datetime(date) - timedelta(days=120)).strftime('%Y-%m-%d')
    
    print(f"📥 获取价格数据: {start_date} ~ {date}")
    
    price_data = jq.get_price(
        stocks,
        start_date=start_date,
        end_date=date,
        frequency='daily',
        fields=['close', 'volume'],
        skip_paused=True,
        fq='post',
        panel=False
    )
    
    if price_data is None or price_data.empty:
        return pd.DataFrame()
    
    # 标准化列名
    if 'time' in price_data.columns:
        price_data = price_data.rename(columns={'time': 'date'})
    
    price_data['date'] = pd.to_datetime(price_data['date']).dt.strftime('%Y-%m-%d')
    
    # 计算每只股票的动量
    results = []
    for code in price_data['code'].unique():
        stock_data = price_data[price_data['code'] == code].sort_values('date')
        
        if len(stock_data) < 60:
            continue
        
        latest = stock_data.iloc[-1]
        
        # 计算动量
        close_5d_ago = stock_data.iloc[-6]['close'] if len(stock_data) >= 6 else latest['close']
        close_20d_ago = stock_data.iloc[-21]['close'] if len(stock_data) >= 21 else latest['close']
        close_60d_ago = stock_data.iloc[-61]['close'] if len(stock_data) >= 61 else latest['close']
        
        mom_5d = (latest['close'] / close_5d_ago - 1) * 100 if close_5d_ago > 0 else 0
        mom_20d = (latest['close'] / close_20d_ago - 1) * 100 if close_20d_ago > 0 else 0
        mom_60d = (latest['close'] / close_60d_ago - 1) * 100 if close_60d_ago > 0 else 0
        
        results.append({
            'code': code,
            'close': latest['close'],
            'volume': latest['volume'],
            'mom_5d': mom_5d,
            'mom_20d': mom_20d,
            'mom_60d': mom_60d,
            'date': latest['date']
        })
    
    return pd.DataFrame(results)


def calculate_strategy_score(row, strategy):
    """计算策略评分"""
    score = 50.0  # 基础分
    
    if strategy == 'strong_breakout':
        # 强动量突破: mom_5d >= 15%
        if row['mom_5d'] >= 15:
            score += min(row['mom_5d'] - 15, 20) * 2
            if row['mom_20d'] > 20:
                score += 10
            if row['mom_5d'] > row['mom_20d'] / 4:
                score += 5
    
    elif strategy == 'accelerated_breakout':
        # 加速突破: mom_5d > 10% AND mom_20d > 30%
        if row['mom_5d'] > 10 and row['mom_20d'] > 30:
            score += min(row['mom_5d'] - 10, 15) * 1.5
            score += min(row['mom_20d'] - 30, 30) * 0.5
            if row['mom_60d'] > 30:
                score += 5
    
    elif strategy == 'pullback_rebound':
        # 回调反弹: mom_5d < 0 AND mom_20d > 15%
        if row['mom_5d'] < 0 and row['mom_20d'] > 15:
            score += min(row['mom_20d'] - 15, 30) * 1
            if -5 < row['mom_5d'] < 0:
                score += 10
            if row['mom_60d'] > 20:
                score += 5
    
    return min(max(score, 0), 100)


def get_recommendation(score):
    """根据评分给出推荐"""
    if score >= 80:
        return "★★★ 强烈推荐"
    elif score >= 65:
        return "★★ 推荐"
    elif score >= 50:
        return "★ 观望"
    else:
        return "- 不推荐"


def analyze_pspi_stocks():
    """分析PSPI概念股票"""
    
    # PSPI概念股票列表（转换为聚宽代码格式）
    pspi_stocks = {
        '688323.XSHG': '瑞华泰',      # 688323 - 科创板
        '000859.XSHE': '国风新材',    # 000859
        '600458.XSHG': '时代新材',    # 600458
        '300054.XSHE': '鼎龙股份',    # 300054
        '002643.XSHE': '万润股份',    # 002643
        '002254.XSHE': '泰和新材',    # 002254
        '300429.XSHE': '强力新材',    # 300429
    }
    
    print("="*80)
    print("PSPI概念股票动量分析")
    print("="*80)
    print(f"\n分析日期: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"股票数量: {len(pspi_stocks)}\n")
    
    # 初始化JQData
    if not init_jqdata():
        return
    
    # 获取最新交易日
    trade_days = jq.get_trade_days(end_date=datetime.now(), count=5)
    latest_date = trade_days[-1].strftime('%Y-%m-%d')
    
    print(f"最新交易日: {latest_date}\n")
    
    # 计算动量
    print("📊 计算动量因子...")
    momentum_df = calculate_momentum(list(pspi_stocks.keys()), latest_date)
    
    if momentum_df.empty:
        print("❌ 无法获取动量数据")
        return
    
    # 合并股票名称
    momentum_df['name'] = momentum_df['code'].map(pspi_stocks)
    momentum_df = momentum_df[momentum_df['name'].notna()]
    
    # 显示所有股票的完整信息
    print("\n" + "="*80)
    print("📈 PSPI概念股票动量因子详情")
    print("="*80)
    print(f"{'股票代码':<12} {'名称':<10} {'收盘价':>8} {'5日动量':>8} {'20日动量':>8} {'60日动量':>8}")
    print("-"*80)
    
    for _, row in momentum_df.iterrows():
        print(f"{row['code']:<12} {row['name']:<10} {row['close']:>8.2f} "
              f"{row['mom_5d']:>7.2f}% {row['mom_20d']:>7.2f}% {row['mom_60d']:>7.2f}%")
    
    # 应用三种策略筛选
    strategies = {
        'strong_breakout': ('强动量突破', lambda r: r['mom_5d'] >= 15),
        'accelerated_breakout': ('加速突破', lambda r: (r['mom_5d'] > 10) & (r['mom_20d'] > 30)),
        'pullback_rebound': ('回调反弹', lambda r: (r['mom_5d'] < 0) & (r['mom_20d'] > 15))
    }
    
    strategy_results = []
    
    for strategy_key, (strategy_name, condition_func) in strategies.items():
        filtered = momentum_df[condition_func(momentum_df)].copy()
        
        if not filtered.empty:
            filtered['score'] = filtered.apply(
                lambda r: calculate_strategy_score(r, strategy_key), axis=1
            )
            filtered['recommendation'] = filtered['score'].apply(get_recommendation)
            filtered['strategy'] = strategy_name
            
            for _, row in filtered.iterrows():
                strategy_results.append({
                    'code': row['code'],
                    'name': row['name'],
                    'strategy': row['strategy'],
                    'mom_5d': row['mom_5d'],
                    'mom_20d': row['mom_20d'],
                    'score': row['score'],
                    'recommendation': row['recommendation']
                })
    
    # 显示符合策略的股票
    if strategy_results:
        print("\n" + "="*80)
        print("✅ 符合短期动量策略的股票")
        print("="*80)
        print(f"{'股票代码':<12} {'名称':<10} {'策略':<12} {'5日动量':>8} {'20日动量':>8} {'评分':>6} {'推荐'}")
        print("-"*80)
        
        # 按评分排序
        results_df = pd.DataFrame(strategy_results)
        results_df = results_df.sort_values('score', ascending=False)
        
        for _, row in results_df.iterrows():
            print(f"{row['code']:<12} {row['name']:<10} {row['strategy']:<12} "
                  f"{row['mom_5d']:>7.2f}% {row['mom_20d']:>7.2f}% {row['score']:>5.0f} {row['recommendation']}")
    else:
        print("\n⚠️  暂无股票符合三大策略的筛选条件")
    
    # 综合分析和建议
    print("\n" + "="*80)
    print("💡 投资建议")
    print("="*80)
    
    # 按5日动量排序
    momentum_df_sorted = momentum_df.sort_values('mom_5d', ascending=False)
    
    print("\n📊 按5日动量排序:")
    for idx, (_, row) in enumerate(momentum_df_sorted.iterrows(), 1):
        hints = []
        if row['mom_5d'] >= 15:
            hints.append("强动量突破★★★")
        elif row['mom_5d'] >= 10 and row['mom_20d'] > 30:
            hints.append("加速突破★★★")
        elif row['mom_5d'] < 0 and row['mom_20d'] > 15:
            hints.append("回调反弹★★")
        
        hint_str = f" → {', '.join(hints)}" if hints else ""
        
        print(f"{idx}. {row['name']}({row['code']}): "
              f"5日={row['mom_5d']:.2f}%, 20日={row['mom_20d']:.2f}%, 60日={row['mom_60d']:.2f}%"
              f"{hint_str}")
    
    # 按20日动量排序
    momentum_df_sorted_20d = momentum_df.sort_values('mom_20d', ascending=False)
    
    print("\n📊 按20日动量排序（中期趋势）:")
    for idx, (_, row) in enumerate(momentum_df_sorted_20d.iterrows(), 1):
        print(f"{idx}. {row['name']}({row['code']}): "
              f"20日={row['mom_20d']:.2f}%, 5日={row['mom_5d']:.2f}%")
    
    # 综合评分
    print("\n📊 综合评分（基于三大策略）:")
    
    for _, row in momentum_df.iterrows():
        scores = []
        
        # 强动量突破策略评分
        if row['mom_5d'] >= 15:
            score1 = 50 + min(row['mom_5d'] - 15, 20) * 2
            if row['mom_20d'] > 20:
                score1 += 10
            scores.append(('强动量突破', score1))
        
        # 加速突破策略评分
        if row['mom_5d'] > 10 and row['mom_20d'] > 30:
            score2 = 50 + min(row['mom_5d'] - 10, 15) * 1.5 + min(row['mom_20d'] - 30, 30) * 0.5
            scores.append(('加速突破', score2))
        
        # 回调反弹策略评分
        if row['mom_5d'] < 0 and row['mom_20d'] > 15:
            score3 = 50 + min(row['mom_20d'] - 15, 30) * 1
            if -5 < row['mom_5d'] < 0:
                score3 += 10
            scores.append(('回调反弹', score3))
        
        if scores:
            max_score = max(scores, key=lambda x: x[1])[1]
            best_strategy = max(scores, key=lambda x: x[1])[0]
            recommendation = "★★★" if max_score >= 80 else "★★" if max_score >= 65 else "★"
            print(f"  {row['name']}({row['code']}): {best_strategy}, 评分={max_score:.0f} {recommendation}")
    
    # 最终建议
    print("\n" + "="*80)
    print("🎯 最终投资建议")
    print("="*80)
    
    # 找出最强的股票
    top_by_5d = momentum_df_sorted.iloc[0]
    top_by_20d = momentum_df_sorted_20d.iloc[0]
    
    print(f"\n【最强短期动量】{top_by_5d['name']}({top_by_5d['code']})")
    print(f"   5日动量: {top_by_5d['mom_5d']:.2f}%")
    print(f"   20日动量: {top_by_5d['mom_20d']:.2f}%")
    print(f"   建议: {'适用强动量突破策略★★★' if top_by_5d['mom_5d'] >= 15 else '动量尚未完全启动，继续观察'}")
    
    print(f"\n【最强中期趋势】{top_by_20d['name']}({top_by_20d['code']})")
    print(f"   20日动量: {top_by_20d['mom_20d']:.2f}%")
    print(f"   5日动量: {top_by_20d['mom_5d']:.2f}%")
    print(f"   建议: {'中期趋势强劲，适合关注★★★' if top_by_20d['mom_20d'] > 30 else '中期趋势温和，需观察'}")
    
    print("\n⚠️  风险提示:")
    print("   1. 以上分析基于历史数据，不构成投资建议")
    print("   2. 建议设置止损位: -8%")
    print("   3. 建议止盈位: +30%")
    print("   4. 持仓周期: 5个交易日")
    print("   5. 单票仓位: ≤ 10%")


if __name__ == '__main__':
    analyze_pspi_stocks()
