#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
早期识别系统 - 优化版回测验证

根据初次验证结果，优化阶段识别参数：
1. 放宽S2加速期条件（profit_growth 0.30→0.25, roe 0.15→0.12）
2. 调整阶段权重配置（S1:15%, S2:40%, S3:35%, S0:10%）
3. 排除周期性行业的假阳性
"""

import sys
import os

# 工作目录：/home/taotao/.cursor/worktrees/TRQuant/ope
# 项目根目录：/home/taotao/.cursor/worktrees/TRQuant/ope
PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate

from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerStage, TenbaggerCriteria
)


# ============================================================
# 优化后的阶段识别器
# ============================================================

class OptimizedStageIdentifier:
    """优化后的阶段识别器
    
    调整阈值：
    - S2加速期：profit_growth >= 0.25 (原0.30), roe >= 0.12 (原0.15)
    - S3扩张期：market_cap < 800亿 (原1000亿)
    """
    
    def identify_stage(self, market_cap: float, revenue_growth: float,
                       profit_growth: float, roe: float) -> TenbaggerStage:
        """识别所处阶段（优化版）"""
        
        # 衰退期判断
        if profit_growth < -0.10 and revenue_growth < 0:
            return TenbaggerStage.S5_DECLINE
        
        # 根据市值和增速判断阶段
        if market_cap < 30:
            return TenbaggerStage.S0_SEED
        elif market_cap < 100:
            # 放宽S1条件
            if profit_growth >= 0.20 or revenue_growth >= 0.20:
                return TenbaggerStage.S1_EMERGENCE
            else:
                return TenbaggerStage.S0_SEED
        elif market_cap < 300:
            # 放宽S2条件：profit_growth 0.30→0.25, roe 0.15→0.12
            if profit_growth >= 0.25 and roe >= 0.12:
                return TenbaggerStage.S2_ACCELERATION
            elif profit_growth >= 0.15:
                return TenbaggerStage.S1_EMERGENCE
            else:
                return TenbaggerStage.S0_SEED
        elif market_cap < 800:  # 原1000
            if profit_growth >= 0.15:
                return TenbaggerStage.S3_EXPANSION
            else:
                return TenbaggerStage.S4_MATURITY
        else:
            if profit_growth >= 0.10:
                return TenbaggerStage.S4_MATURITY
            else:
                return TenbaggerStage.S5_DECLINE


# ============================================================
# 优化后的策略
# ============================================================

class OptimizedStageWeightStrategy:
    """优化后的阶段权重策略
    
    权重调整：S1:15%, S2:40%, S3:35%, S0:10%
    """
    
    def __init__(self):
        self.name = "优化阶段权重"
        self.weights = {
            TenbaggerStage.S0_SEED: 0.10,
            TenbaggerStage.S1_EMERGENCE: 0.15,
            TenbaggerStage.S2_ACCELERATION: 0.40,
            TenbaggerStage.S3_EXPANSION: 0.35,
        }
    
    def select_stocks(self, screened):
        result = []
        for stage, stage_weight in self.weights.items():
            stocks = screened.get(stage, [])[:10]
            if stocks:
                stock_weight = stage_weight / len(stocks)
                for s in stocks:
                    result.append((s['code'], stock_weight))
        return result


class TopScoreStrategy:
    """高得分优先策略：选择得分最高的股票"""
    
    def __init__(self, top_n: int = 20):
        self.name = f"高得分Top{top_n}"
        self.top_n = top_n
    
    def select_stocks(self, screened):
        candidates = []
        for stage in [TenbaggerStage.S0_SEED, TenbaggerStage.S1_EMERGENCE,
                      TenbaggerStage.S2_ACCELERATION, TenbaggerStage.S3_EXPANSION]:
            candidates.extend(screened.get(stage, []))
        
        candidates.sort(key=lambda x: x['score'], reverse=True)
        top = [c for c in candidates[:self.top_n] if c['score'] >= 55]
        
        if not top:
            return []
        
        weight = 1.0 / len(top)
        return [(c['code'], weight) for c in top]


# ============================================================
# 优化后的筛选器
# ============================================================

class OptimizedScreener:
    """优化后的筛选器"""
    
    def __init__(self):
        self.identifier = OptimizedStageIdentifier()
        authenticate()
    
    def screen_at_date(self, screen_date: str) -> Dict[TenbaggerStage, List[dict]]:
        """筛选股票"""
        print(f"\n{'='*60}")
        print(f"优化版筛选 - {screen_date}")
        print(f"{'='*60}")
        
        # 获取所有A股
        all_stocks = jq.get_all_securities(types=['stock'], date=screen_date)
        
        # 过滤
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|退', na=False) &
            ~all_stocks.index.str.startswith('688') &
            ~all_stocks.index.str.startswith('8')
        ]
        print(f"有效股票: {len(valid_stocks)} 只")
        
        # 获取基本面数据
        codes = valid_stocks.index.tolist()
        fundamentals = self._get_fundamentals(codes, screen_date)
        
        # 识别阶段
        results = {stage: [] for stage in TenbaggerStage}
        
        for code in fundamentals.index:
            try:
                fund = fundamentals.loc[code]
                
                market_cap = fund.get('market_cap', 0)
                revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
                profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
                roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
                pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
                
                # 基本过滤
                if market_cap < 20 or market_cap > 2000:
                    continue
                if pe <= 0 or pe > 200:
                    continue
                
                # 识别阶段
                stage = self.identifier.identify_stage(market_cap, revenue_growth, profit_growth, roe)
                
                # 计算简化得分
                score = self._calculate_score(revenue_growth, profit_growth, roe, market_cap, pe)
                
                name = valid_stocks.loc[code, 'display_name'] if code in valid_stocks.index else code
                
                results[stage].append({
                    'code': code,
                    'name': name,
                    'stage': stage,
                    'score': score,
                    'market_cap': market_cap,
                    'revenue_growth': revenue_growth,
                    'profit_growth': profit_growth,
                    'roe': roe,
                    'pe': pe
                })
                
            except Exception:
                continue
        
        # 按得分排序
        for stage in results:
            results[stage].sort(key=lambda x: x['score'], reverse=True)
        
        # 打印统计
        print(f"\n优化后阶段分布:")
        for stage, stocks in results.items():
            print(f"  {stage.value}: {len(stocks)} 只")
        
        return results
    
    def _get_fundamentals(self, codes: List[str], date: str) -> pd.DataFrame:
        """获取基本面数据"""
        batch_size = 1000
        all_dfs = []
        
        for i in range(0, len(codes), batch_size):
            batch = codes[i:i+batch_size]
            q = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
            ).filter(jq.valuation.code.in_(batch))
            
            df = jq.get_fundamentals(q, date=date)
            if df is not None and not df.empty:
                all_dfs.append(df)
        
        if all_dfs:
            df = pd.concat(all_dfs, ignore_index=True)
            return df.set_index('code')
        return pd.DataFrame()
    
    def _calculate_score(self, revenue_growth, profit_growth, roe, market_cap, pe):
        """计算简化得分"""
        score = 50  # 基础分
        
        # 成长性 (最高30分)
        if profit_growth > 0.50:
            score += 20
        elif profit_growth > 0.30:
            score += 15
        elif profit_growth > 0.15:
            score += 10
        
        if revenue_growth > 0.30:
            score += 10
        elif revenue_growth > 0.15:
            score += 5
        
        # 质量 (最高15分)
        if roe > 0.20:
            score += 10
        elif roe > 0.15:
            score += 7
        elif roe > 0.10:
            score += 3
        
        if market_cap < 100:
            score += 5  # 小市值加分
        
        # 估值 (最高5分)
        peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 10
        if 0 < peg < 1:
            score += 5
        elif peg < 1.5:
            score += 3
        
        return min(score, 100)


# ============================================================
# 回测运行
# ============================================================

def run_backtest(stock_weights, start_date, end_date, strategy_name):
    """运行回测"""
    if not stock_weights:
        return {'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0, 'count': 0}
    
    codes = [s[0] for s in stock_weights]
    weights = {s[0]: s[1] for s in stock_weights}
    
    price_df = jq.get_price(
        codes,
        start_date=start_date,
        end_date=end_date,
        frequency='daily',
        fields=['close'],
        panel=False
    )
    
    if price_df is None or price_df.empty:
        return {'total_return': 0, 'sharpe': 0, 'max_dd': 0, 'win_rate': 0, 'count': 0}
    
    # 计算各股票收益
    stock_returns = {}
    for code in codes:
        sd = price_df[price_df['code'] == code]
        if len(sd) >= 2:
            stock_returns[code] = (sd['close'].iloc[-1] - sd['close'].iloc[0]) / sd['close'].iloc[0]
        else:
            stock_returns[code] = 0
    
    # 组合收益
    portfolio_return = sum(stock_returns.get(c, 0) * w for c, w in weights.items())
    
    # 日收益率
    dates = price_df['time'].unique()
    daily_returns = []
    portfolio_values = [1.0]
    
    for i in range(1, len(dates)):
        day_data = price_df[price_df['time'] == dates[i]]
        prev_data = price_df[price_df['time'] == dates[i-1]]
        
        day_return = 0
        for code, weight in weights.items():
            curr = day_data[day_data['code'] == code]['close']
            prev = prev_data[prev_data['code'] == code]['close']
            if len(curr) > 0 and len(prev) > 0 and prev.iloc[0] > 0:
                day_return += (curr.iloc[0] - prev.iloc[0]) / prev.iloc[0] * weight
        
        daily_returns.append(day_return)
        portfolio_values.append(portfolio_values[-1] * (1 + day_return))
    
    # 最大回撤
    max_dd = 0
    peak = portfolio_values[0]
    for v in portfolio_values:
        if v > peak:
            peak = v
        dd = (peak - v) / peak
        if dd > max_dd:
            max_dd = dd
    
    # 夏普比率
    if daily_returns and np.std(daily_returns) > 0:
        sharpe = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(252)
    else:
        sharpe = 0
    
    # 胜率
    win_rate = sum(1 for r in stock_returns.values() if r > 0) / len(stock_returns) if stock_returns else 0
    
    print(f"{strategy_name}: 收益={portfolio_return*100:.2f}%, 夏普={sharpe:.2f}, 回撤={max_dd*100:.2f}%, 胜率={win_rate*100:.1f}%")
    
    return {
        'total_return': portfolio_return,
        'sharpe': sharpe,
        'max_dd': max_dd,
        'win_rate': win_rate,
        'count': len(codes)
    }


# ============================================================
# 主程序
# ============================================================

def main():
    SCREEN_DATE = '2024-06-01'
    START_DATE = '2024-06-03'
    END_DATE = datetime.now().strftime('%Y-%m-%d')
    
    print("="*70)
    print("优化版早期识别系统回测验证")
    print("="*70)
    print(f"筛选日期: {SCREEN_DATE}")
    print(f"回测区间: {START_DATE} 至 {END_DATE}")
    
    # 筛选
    screener = OptimizedScreener()
    screened = screener.screen_at_date(SCREEN_DATE)
    
    # 策略
    strategies = [
        ("S2单阶段", lambda s: [(x['code'], 1.0/len(s[TenbaggerStage.S2_ACCELERATION][:20])) 
                                for x in s[TenbaggerStage.S2_ACCELERATION][:20]] if s[TenbaggerStage.S2_ACCELERATION] else []),
        ("S1单阶段", lambda s: [(x['code'], 1.0/len(s[TenbaggerStage.S1_EMERGENCE][:20]))
                                for x in s[TenbaggerStage.S1_EMERGENCE][:20]] if s[TenbaggerStage.S1_EMERGENCE] else []),
        ("优化阶段权重", OptimizedStageWeightStrategy().select_stocks),
        ("高得分Top20", TopScoreStrategy(20).select_stocks),
        ("高得分Top30", TopScoreStrategy(30).select_stocks),
    ]
    
    # 回测
    print(f"\n{'='*70}")
    print("策略回测结果")
    print("="*70)
    
    results = []
    for name, select_func in strategies:
        stock_weights = select_func(screened)
        result = run_backtest(stock_weights, START_DATE, END_DATE, name)
        result['name'] = name
        results.append(result)
    
    # 汇总
    print(f"\n{'='*70}")
    print("策略对比汇总")
    print("="*70)
    
    df = pd.DataFrame(results)
    df = df.sort_values('total_return', ascending=False)
    df['total_return'] = df['total_return'].apply(lambda x: f"{x*100:.2f}%")
    df['sharpe'] = df['sharpe'].apply(lambda x: f"{x:.2f}")
    df['max_dd'] = df['max_dd'].apply(lambda x: f"{x*100:.2f}%")
    df['win_rate'] = df['win_rate'].apply(lambda x: f"{x*100:.1f}%")
    
    print(df[['name', 'total_return', 'sharpe', 'max_dd', 'win_rate', 'count']].to_string(index=False))
    
    # 最佳策略
    best = max(results, key=lambda x: x['total_return'] if isinstance(x['total_return'], float) else 0)
    print(f"\n最佳策略: {best['name']}")


if __name__ == '__main__':
    main()
