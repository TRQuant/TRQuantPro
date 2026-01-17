#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期十倍股 - 修复版扫描器

修复数据获取问题
"""

import sys
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate


# 排除行业
EXCLUDE_INDUSTRIES = ['有色金属', '钢铁', '采掘', '农林牧渔']

# 优质行业
PREFERRED_INDUSTRIES = ['电子', '计算机', '通信', '电气设备', '机械设备', '食品饮料', '家用电器', '汽车', '医药生物']


@dataclass
class StockCandidate:
    code: str
    name: str
    industry: str
    market_cap: float
    pe: float
    peg: float
    roe: float
    profit_growth: float
    revenue_growth: float
    score: float
    stage: str
    reasons: List[str]


def get_market_regime() -> str:
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
        price = jq.get_price('000300.XSHG', start_date=start_date, end_date=end_date,
                             frequency='daily', fields=['close'], panel=False)
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


def get_fundamentals_fixed(codes: List[str], date_str: str) -> pd.DataFrame:
    """修复版：分别查询估值和指标数据"""
    batch_size = 500
    all_data = []
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i+batch_size]
        
        try:
            # 查询估值数据
            q_val = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
            ).filter(jq.valuation.code.in_(batch))
            
            df_val = jq.get_fundamentals(q_val, date=date_str)
            
            if df_val is None or df_val.empty:
                continue
            
            # 查询指标数据
            q_ind = jq.query(
                jq.indicator.code,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
            ).filter(jq.indicator.code.in_(batch))
            
            df_ind = jq.get_fundamentals(q_ind, date=date_str)
            
            if df_ind is None or df_ind.empty:
                continue
            
            # 合并
            df_merged = df_val.merge(df_ind, on='code', how='inner')
            all_data.append(df_merged)
            
        except Exception as e:
            print(f"  批次{i//batch_size}获取失败: {e}")
            continue
    
    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        return result.set_index('code')
    return pd.DataFrame()


def identify_stage(market_cap: float, profit_growth: float, roe: float) -> str:
    if market_cap < 30:
        return "S1_萌芽期" if profit_growth > 0.20 else "S0_种子期"
    elif market_cap <= 200:
        if profit_growth > 0.20 and roe > 0.10:
            return "S2_加速期"
        return "S1_萌芽期" if profit_growth > 0.10 else "S0_种子期"
    elif market_cap <= 500:
        if profit_growth > 0.15 and roe > 0.12:
            return "S2_加速期"
        return "S3_扩张期" if profit_growth > 0.08 else "S4_成熟期"
    else:
        return "S3_扩张期" if profit_growth > 0.10 else "S4_成熟期"


def run_scanner():
    print("="*80)
    print("S2加速期十倍股 - 当前市场扫描")
    print("="*80)
    print(f"\n扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    authenticate()
    
    # 市场环境
    regime = get_market_regime()
    print(f"\n市场环境: {regime}")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    print(f"筛选日期: {date_str}")
    
    # 获取股票
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &
        ~all_stocks.index.str.startswith('8')
    ]
    print(f"有效股票: {len(valid)} 只")
    
    # 行业
    codes = valid.index.tolist()
    industries = jq.get_industry(codes, date=date_str)
    valid = valid.copy()
    valid['industry'] = ''
    for code in codes:
        if code in industries and 'sw_l1' in industries[code]:
            valid.loc[code, 'industry'] = industries[code]['sw_l1'].get('industry_name', '')
    
    # 财务数据（修复版）
    print("获取财务数据...")
    fundamentals = get_fundamentals_fixed(codes, date_str)
    print(f"财务数据: {len(fundamentals)} 只")
    
    if fundamentals.empty:
        print("\n⚠️ 无法获取财务数据")
        return
    
    # 筛选条件（放宽）
    CONFIG = {
        'min_mcap': 20, 'max_mcap': 800,
        'min_profit_growth': 0.10,
        'min_revenue_growth': 0.05,
        'min_roe': 0.05,
        'max_pe': 150,
        'max_peg': 2.5,
    }
    
    candidates = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            industry = valid.loc[code, 'industry'] if code in valid.index else ''
            name = valid.loc[code, 'display_name'] if code in valid.index else code
            
            # 排除行业
            if any(ind in industry for ind in EXCLUDE_INDUSTRIES):
                continue
            
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            
            # 数据有效性
            if pd.isna(market_cap) or market_cap <= 0:
                continue
            
            # 筛选
            if not (CONFIG['min_mcap'] <= market_cap <= CONFIG['max_mcap']):
                continue
            if profit_growth < CONFIG['min_profit_growth']:
                continue
            if revenue_growth < CONFIG['min_revenue_growth']:
                continue
            if roe < CONFIG['min_roe']:
                continue
            if pe <= 0 or pe > CONFIG['max_pe']:
                continue
            
            peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 99
            if peg > CONFIG['max_peg']:
                continue
            
            stage = identify_stage(market_cap, profit_growth, roe)
            if stage not in ["S1_萌芽期", "S2_加速期"]:
                continue
            
            # 评分
            score = 50
            reasons = []
            
            if stage == "S2_加速期":
                score += 15
                reasons.append("S2加速期")
            else:
                score += 5
                reasons.append("S1萌芽期")
            
            if any(ind in industry for ind in PREFERRED_INDUSTRIES):
                score += 10
                reasons.append("优质行业")
            
            if profit_growth >= 0.40:
                score += 15
                reasons.append(f"高增长+{profit_growth*100:.0f}%")
            elif profit_growth >= 0.25:
                score += 10
            else:
                score += 5
            
            if roe >= 0.18:
                score += 10
                reasons.append(f"高ROE{roe*100:.0f}%")
            elif roe >= 0.12:
                score += 5
            
            if peg < 0.8:
                score += 10
                reasons.append(f"低PEG{peg:.2f}")
            elif peg < 1.2:
                score += 5
            
            if 30 <= market_cap <= 150:
                score += 5
                reasons.append("最佳市值")
            
            candidates.append(StockCandidate(
                code=code, name=name, industry=industry,
                market_cap=market_cap, pe=pe, peg=peg, roe=roe,
                profit_growth=profit_growth, revenue_growth=revenue_growth,
                score=min(score, 100), stage=stage, reasons=reasons
            ))
        except:
            continue
    
    candidates.sort(key=lambda x: x.score, reverse=True)
    print(f"\n筛选出早期潜力股: {len(candidates)} 只")
    
    if candidates:
        s2 = [c for c in candidates if c.stage == "S2_加速期"]
        s1 = [c for c in candidates if c.stage == "S1_萌芽期"]
        
        print("\n" + "="*80)
        print(f"🌟 S2加速期股票（最佳买点）: {len(s2)} 只")
        print("="*80)
        
        for i, s in enumerate(s2[:20], 1):
            print(f"\n{i}. {s.code} {s.name} 【得分: {s.score}】")
            print(f"   {s.industry} | 市值{s.market_cap:.0f}亿 | PE{s.pe:.0f} | PEG{s.peg:.2f}")
            print(f"   利润+{s.profit_growth*100:.0f}% | 营收+{s.revenue_growth*100:.0f}% | ROE{s.roe*100:.0f}%")
            print(f"   ✅ {', '.join(s.reasons)}")
        
        print("\n" + "="*80)
        print(f"🌱 S1萌芽期股票: {len(s1)} 只（显示Top10）")
        print("="*80)
        
        for i, s in enumerate(s1[:10], 1):
            print(f"{i}. {s.code} {s.name}: 得分{s.score}, {s.industry}, 利润+{s.profit_growth*100:.0f}%")
        
        # 保存
        df = pd.DataFrame([{
            'code': s.code, 'name': s.name, 'stage': s.stage,
            'industry': s.industry, 'market_cap': s.market_cap,
            'pe': s.pe, 'peg': s.peg, 'roe': s.roe,
            'profit_growth': s.profit_growth, 'revenue_growth': s.revenue_growth,
            'score': s.score, 'reasons': '|'.join(s.reasons)
        } for s in candidates])
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f'/home/taotao/.cursor/worktrees/TRQuant/ope/results/s2_candidates_{timestamp}.csv'
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {output}")
        
        # 投资建议
        print("\n" + "="*80)
        print("💡 投资建议")
        print("="*80)
        
        print(f"\n市场环境: {regime}")
        if regime == "BULL":
            print("✅ 牛市环境，可积极配置")
        else:
            print("⚠️ 非牛市，建议控制仓位")
        
        print("\n重点关注（S2阶段Top5）:")
        for s in s2[:5]:
            print(f"  📌 {s.code} {s.name} - {s.industry}, 利润+{s.profit_growth*100:.0f}%")
    else:
        print("\n⚠️ 未找到符合条件的股票")
    
    return candidates


if __name__ == '__main__':
    run_scanner()
