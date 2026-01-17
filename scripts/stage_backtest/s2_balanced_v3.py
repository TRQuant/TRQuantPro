#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期策略 - 平衡版V3

平衡筛选条件：
1. 利润增速：20%-500%（排除极端暴增，但保留高增长）
2. 营收增速：>15%（略放宽）
3. ROE：>12%
4. 只排除强周期行业
5. 持有期1年，止损-15%
"""

import sys
import os

PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate


# 只排除强周期行业
EXCLUDE_INDUSTRIES = [
    '有色金属', '钢铁', '采掘', '建筑材料',
    '农林牧渔',  # 养殖周期
]

CONFIG = {
    'min_mcap': 30,
    'max_mcap': 500,
    'min_profit_growth': 0.20,  # 放宽到20%
    'max_profit_growth': 5.0,   # 放宽到500%
    'min_revenue_growth': 0.15, # 放宽到15%
    'min_roe': 0.12,            # 放宽到12%
    'max_peg': 1.5,             # 放宽到1.5
    'max_pe': 80,
    
    'bull_position': 1.0,
    'volatile_position': 0.5,
    'bear_position': 0.0,
    
    'stop_loss': -0.15,
    'hold_days': 252,
}


def get_market_regime(date_str: str) -> str:
    try:
        end_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=100)
        price = jq.get_price('000300.XSHG', start_date=start_date.strftime('%Y-%m-%d'),
                             end_date=date_str, frequency='daily', fields=['close'], panel=False)
        if price is None or len(price) < 60:
            return "VOLATILE"
        close = price['close']
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        current = close.iloc[-1]
        if current > ma20 > ma60:
            return "BULL"
        elif current < ma20 < ma60:
            return "BEAR"
        return "VOLATILE"
    except:
        return "VOLATILE"


class BalancedS2Identifier:
    def identify(self, market_cap: float, profit_growth: float, revenue_growth: float,
                 roe: float, pe: float, industry: str = '') -> Tuple[bool, float, str]:
        
        if industry and any(ind in industry for ind in EXCLUDE_INDUSTRIES):
            return False, 0, "排除行业"
        
        if not (CONFIG['min_mcap'] <= market_cap <= CONFIG['max_mcap']):
            return False, 0, "市值不符"
        
        if profit_growth < CONFIG['min_profit_growth']:
            return False, 0, "利润增速不足"
        if profit_growth > CONFIG['max_profit_growth']:
            return False, 0, "利润增速异常"
        
        if revenue_growth < CONFIG['min_revenue_growth']:
            return False, 0, "营收增速不足"
        
        if roe < CONFIG['min_roe']:
            return False, 0, "ROE不足"
        
        if pe <= 0 or pe > CONFIG['max_pe']:
            return False, 0, "PE不符"
        
        peg = pe / (profit_growth * 100) if profit_growth > 0.1 else 99
        if peg > CONFIG['max_peg']:
            return False, 0, f"PEG过高"
        
        score = 50
        
        # 利润与营收匹配度
        ratio = profit_growth / max(revenue_growth, 0.01)
        if 0.5 <= ratio <= 3.0:
            score += 10
        
        # 利润增速
        if 0.30 <= profit_growth <= 1.0:
            score += 15  # 最佳区间
        elif profit_growth > 1.0:
            score += 10
        else:
            score += 5
        
        # ROE
        if roe >= 0.20:
            score += 15
        elif roe >= 0.15:
            score += 10
        else:
            score += 5
        
        # PEG
        if peg < 0.5:
            score += 15
        elif peg < 1.0:
            score += 10
        else:
            score += 5
        
        reason = f"利润+{profit_growth*100:.0f}%,营收+{revenue_growth*100:.0f}%,ROE{roe*100:.0f}%"
        return True, min(score, 100), reason


def get_stocks_with_industry(date_str: str) -> pd.DataFrame:
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &
        ~all_stocks.index.str.startswith('8')
    ]
    codes = valid.index.tolist()
    industries = jq.get_industry(codes, date=date_str)
    valid = valid.copy()
    valid['industry'] = ''
    for code in codes:
        if code in industries:
            ind_info = industries[code]
            if 'sw_l1' in ind_info and 'industry_name' in ind_info['sw_l1']:
                valid.loc[code, 'industry'] = ind_info['sw_l1']['industry_name']
    return valid


def get_fundamentals(codes: List[str], date_str: str) -> pd.DataFrame:
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
        df = jq.get_fundamentals(q, date=date_str)
        if df is not None and not df.empty:
            all_dfs.append(df)
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True).set_index('code')
    return pd.DataFrame()


def get_return(code: str, start_date: str, days: int) -> Optional[Tuple[float, str]]:
    try:
        end = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=days+30)
        price = jq.get_price(code, start_date=start_date, end_date=end.strftime('%Y-%m-%d'),
                             frequency='daily', fields=['close'], panel=False)
        if price is None or len(price) < 10:
            return None
        prices = price['close'].values
        entry_price = prices[0]
        for i, p in enumerate(prices):
            ret = (p - entry_price) / entry_price
            if ret <= CONFIG['stop_loss']:
                return ret, "止损"
        final_idx = min(days, len(prices) - 1)
        final_ret = (prices[final_idx] - entry_price) / entry_price
        return final_ret, "到期"
    except:
        return None


@dataclass
class StockResult:
    code: str
    name: str
    industry: str
    market_cap: float
    profit_growth: float
    revenue_growth: float
    roe: float
    score: float
    return_pct: float = 0
    reason: str = ""


def screen_stocks(date_str: str, stocks_df: pd.DataFrame) -> List[StockResult]:
    identifier = BalancedS2Identifier()
    codes = stocks_df.index.tolist()
    fundamentals = get_fundamentals(codes, date_str)
    results = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            
            industry = stocks_df.loc[code, 'industry'] if code in stocks_df.index else ''
            is_s2, score, reason = identifier.identify(market_cap, profit_growth, revenue_growth, roe, pe, industry)
            
            if is_s2:
                name = stocks_df.loc[code, 'display_name'] if code in stocks_df.index else code
                results.append(StockResult(
                    code=code, name=name, industry=industry,
                    market_cap=market_cap, profit_growth=profit_growth,
                    revenue_growth=revenue_growth, roe=roe, score=score
                ))
        except:
            continue
    
    return sorted(results, key=lambda x: x.score, reverse=True)


def run_backtest():
    print("="*80)
    print("S2加速期策略 - 平衡版V3")
    print("="*80)
    print("\n筛选条件：")
    print(f"  利润增速：{CONFIG['min_profit_growth']*100:.0f}%-{CONFIG['max_profit_growth']*100:.0f}%")
    print(f"  营收增速：>{CONFIG['min_revenue_growth']*100:.0f}%")
    print(f"  ROE：>{CONFIG['min_roe']*100:.0f}%")
    print(f"  PEG：<{CONFIG['max_peg']}")
    print(f"  排除行业：有色金属、钢铁、采掘、建筑材料、农林牧渔")
    print(f"  持有期：{CONFIG['hold_days']}天，止损：{CONFIG['stop_loss']*100:.0f}%")
    print()
    
    authenticate()
    
    screen_dates = ['2020-06-01', '2021-06-01', '2022-06-01', '2023-06-01', '2024-06-01']
    all_results = []
    yearly_stats = []
    
    for screen_date in screen_dates:
        print(f"\n{'='*70}")
        print(f"筛选日期: {screen_date}")
        
        regime = get_market_regime(screen_date)
        print(f"市场环境: {regime}")
        print("="*70)
        
        stocks_df = get_stocks_with_industry(screen_date)
        print(f"有效股票: {len(stocks_df)} 只")
        
        candidates = screen_stocks(screen_date, stocks_df)
        print(f"S2阶段股票: {len(candidates)} 只")
        
        if regime == "BEAR":
            print(f"熊市空仓")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': len(candidates),
                               'trades': 0, 'avg_return': None, 'win_rate': None, 'stop_loss': 0})
            continue
        
        if not candidates:
            print("无候选股票")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': 0,
                               'trades': 0, 'avg_return': None, 'win_rate': None, 'stop_loss': 0})
            continue
        
        position = CONFIG['bull_position'] if regime == "BULL" else CONFIG['volatile_position']
        top_n = max(5, int(10 * position))
        selected = candidates[:top_n]
        
        print(f"选取{len(selected)}只（仓位{position*100:.0f}%）:")
        for s in selected[:5]:
            print(f"  {s.code} {s.name}: 得分{s.score}, {s.industry}")
        
        print("计算收益...")
        returns = []
        stop_loss_count = 0
        
        for s in selected:
            result = get_return(s.code, screen_date, CONFIG['hold_days'])
            if result:
                s.return_pct, s.reason = result
                returns.append(s.return_pct)
                all_results.append(s)
                if s.reason == "止损":
                    stop_loss_count += 1
        
        if returns:
            avg_ret = np.mean(returns)
            win_rate = sum(1 for r in returns if r > 0) / len(returns)
            print(f"\n结果: 平均收益{avg_ret*100:.1f}%, 胜率{win_rate*100:.0f}%, 止损{stop_loss_count}次")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': len(candidates),
                               'trades': len(returns), 'avg_return': avg_ret, 'win_rate': win_rate,
                               'stop_loss': stop_loss_count})
    
    # 汇总
    print("\n" + "="*80)
    print("5年汇总（平衡版V3）")
    print("="*80)
    
    print("\n年度表现:")
    print("-"*90)
    print(f"{'年份':<6} {'环境':<10} {'候选':<8} {'交易':<8} {'平均收益':<12} {'胜率':<10} {'止损':<8}")
    print("-"*90)
    
    for stat in yearly_stats:
        if stat['trades'] > 0:
            print(f"{stat['year']:<6} {stat['regime']:<10} {stat['candidates']:<8} {stat['trades']:<8} "
                  f"{stat['avg_return']*100:>8.1f}%    {stat['win_rate']*100:>6.0f}%    {stat['stop_loss']:<8}")
        else:
            print(f"{stat['year']:<6} {stat['regime']:<10} {stat['candidates']:<8} {'空仓':<8}")
    
    if all_results:
        all_results_sorted = sorted(all_results, key=lambda x: x.return_pct, reverse=True)
        
        double = [s for s in all_results_sorted if s.return_pct > 1.0]
        high = [s for s in all_results_sorted if s.return_pct > 0.5]
        
        print(f"\n翻倍股票（>100%）: {len(double)} 只")
        for s in double:
            print(f"  {s.code} {s.name}: +{s.return_pct*100:.1f}% ({s.industry})")
            print(f"    利润+{s.profit_growth*100:.0f}%, 营收+{s.revenue_growth*100:.0f}%, ROE{s.roe*100:.0f}%")
        
        print(f"\n高回报（>50%）: {len(high)} 只")
        for s in high[:10]:
            print(f"  {s.code} {s.name}: +{s.return_pct*100:.1f}% ({s.industry})")
        
        all_returns = [s.return_pct for s in all_results]
        print(f"\n整体统计:")
        print(f"  总交易: {len(all_returns)} 笔")
        print(f"  平均收益: {np.mean(all_returns)*100:.2f}%")
        print(f"  胜率: {sum(1 for r in all_returns if r>0)/len(all_returns)*100:.1f}%")
        print(f"  最高: +{np.max(all_returns)*100:.1f}%")
        print(f"  最低: {np.min(all_returns)*100:.1f}%")
        
        # 高回报特征分析
        if high:
            print(f"\n高回报股票特征分析（>50%）:")
            print(f"  平均市值: {np.mean([s.market_cap for s in high]):.0f} 亿")
            print(f"  平均利润增速: {np.mean([s.profit_growth for s in high])*100:.0f}%")
            print(f"  平均营收增速: {np.mean([s.revenue_growth for s in high])*100:.0f}%")
            print(f"  平均ROE: {np.mean([s.roe for s in high])*100:.0f}%")
            
            from collections import Counter
            industries = [s.industry for s in high if s.industry]
            if industries:
                ind_count = Counter(industries)
                print(f"  行业分布:")
                for ind, cnt in ind_count.most_common(5):
                    print(f"    {ind}: {cnt} 只")
    
    # 保存
    if all_results:
        df = pd.DataFrame([{
            'code': s.code, 'name': s.name, 'industry': s.industry,
            'market_cap': s.market_cap, 'profit_growth': s.profit_growth,
            'revenue_growth': s.revenue_growth, 'roe': s.roe,
            'score': s.score, 'return_pct': s.return_pct, 'reason': s.reason
        } for s in all_results])
        output = f'{PROJECT_ROOT}/results/s2_balanced_v3_results.csv'
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {output}")


if __name__ == '__main__':
    run_backtest()
