#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期十倍股 - 放宽条件版扫描器

放宽筛选条件，找出当前具有潜力的股票
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


# 排除行业
EXCLUDE_INDUSTRIES = [
    '有色金属', '钢铁', '采掘',  # 强周期
    '农林牧渔',  # 养殖周期
]

# 优质行业
PREFERRED_INDUSTRIES = [
    '电子', '计算机', '通信', '传媒',
    '电气设备', '机械设备',
    '食品饮料', '家用电器',
    '汽车', '医药生物',  # 重新加入医药
]


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
    gross_margin: float
    score: float
    stage: str
    reasons: List[str]


def get_market_regime() -> Tuple[str, dict]:
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
        
        price = jq.get_price('000300.XSHG', start_date=start_date, end_date=end_date,
                             frequency='daily', fields=['close'], panel=False)
        
        if price is None or len(price) < 60:
            return "UNKNOWN", {}
        
        close = price['close']
        current = close.iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        
        change_5d = (current - close.iloc[-6]) / close.iloc[-6] * 100 if len(close) > 5 else 0
        change_20d = (current - close.iloc[-21]) / close.iloc[-21] * 100 if len(close) > 20 else 0
        
        details = {
            'current': current,
            'ma20': ma20,
            'ma60': ma60,
            'change_5d': change_5d,
            'change_20d': change_20d,
        }
        
        if current > ma20 > ma60:
            return "BULL", details
        elif current < ma20 < ma60:
            return "BEAR", details
        return "VOLATILE", details
    except Exception as e:
        return "UNKNOWN", {}


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
            jq.indicator.gross_profit_margin,
        ).filter(jq.valuation.code.in_(batch))
        
        df = jq.get_fundamentals(q, date=date_str)
        if df is not None and not df.empty:
            all_dfs.append(df)
    
    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True).set_index('code')
    return pd.DataFrame()


def identify_stage(market_cap: float, profit_growth: float, roe: float) -> str:
    """识别企业生命周期阶段"""
    if market_cap < 30:
        if profit_growth > 0.30:
            return "S1_萌芽期"
        return "S0_种子期"
    elif market_cap <= 150:
        if profit_growth > 0.25 and roe > 0.12:
            return "S2_加速期"  # 最佳买点
        elif profit_growth > 0.15:
            return "S1_萌芽期"
        return "S0_种子期"
    elif market_cap <= 500:
        if profit_growth > 0.20 and roe > 0.15:
            return "S2_加速期"
        elif profit_growth > 0.10:
            return "S3_扩张期"
        return "S4_成熟期"
    else:
        if profit_growth > 0.15 and roe > 0.18:
            return "S3_扩张期"
        return "S4_成熟期"


def scan_stocks():
    """扫描股票"""
    
    print("="*80)
    print("S2加速期十倍股 - 放宽条件版扫描")
    print("="*80)
    print(f"\n扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    authenticate()
    
    # 市场环境
    regime, details = get_market_regime()
    print(f"\n市场环境: {regime}")
    if 'current' in details:
        print(f"  沪深300: {details['current']:.2f}")
        print(f"  5日涨跌: {details.get('change_5d', 0):.2f}%")
        print(f"  20日涨跌: {details.get('change_20d', 0):.2f}%")
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    print(f"\n筛选日期: {date_str}")
    
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
        if code in industries:
            ind_info = industries[code]
            if 'sw_l1' in ind_info and 'industry_name' in ind_info['sw_l1']:
                valid.loc[code, 'industry'] = ind_info['sw_l1']['industry_name']
    
    # 财务数据
    fundamentals = get_fundamentals(codes, date_str)
    print(f"财务数据: {len(fundamentals)} 只")
    
    # 放宽的筛选条件
    CONFIG = {
        'min_mcap': 20,           # 放宽到20亿
        'max_mcap': 800,          # 放宽到800亿
        'min_profit_growth': 0.10, # 放宽到10%
        'min_revenue_growth': 0.08,# 放宽到8%
        'min_roe': 0.08,          # 放宽到8%
        'max_pe': 100,
        'max_peg': 2.0,           # 放宽到2.0
    }
    
    candidates = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            industry = valid.loc[code, 'industry'] if code in valid.index else ''
            name = valid.loc[code, 'display_name'] if code in valid.index else code
            
            # 排除行业
            if industry and any(ind in industry for ind in EXCLUDE_INDUSTRIES):
                continue
            
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            gross_margin = fund.get('gross_profit_margin', 0) / 100 if pd.notna(fund.get('gross_profit_margin')) else 0
            
            # 基础过滤
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
            
            # PEG
            peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 99
            if peg > CONFIG['max_peg']:
                continue
            
            # 识别阶段
            stage = identify_stage(market_cap, profit_growth, roe)
            
            # 只保留S1和S2阶段
            if stage not in ["S1_萌芽期", "S2_加速期"]:
                continue
            
            # 计算得分
            score = 50
            reasons = []
            
            # S2阶段加分
            if stage == "S2_加速期":
                score += 15
                reasons.append("S2加速期")
            else:
                score += 5
                reasons.append("S1萌芽期")
            
            # 优质行业
            if industry and any(ind in industry for ind in PREFERRED_INDUSTRIES):
                score += 10
                reasons.append(f"优质行业")
            
            # 利润增速
            if profit_growth >= 0.50:
                score += 15
                reasons.append(f"高增长+{profit_growth*100:.0f}%")
            elif profit_growth >= 0.30:
                score += 10
                reasons.append(f"快速增长+{profit_growth*100:.0f}%")
            else:
                score += 5
            
            # ROE
            if roe >= 0.20:
                score += 10
                reasons.append(f"高ROE{roe*100:.0f}%")
            elif roe >= 0.15:
                score += 5
            
            # PEG
            if peg < 0.5:
                score += 10
                reasons.append(f"低PEG{peg:.2f}")
            elif peg < 1.0:
                score += 5
            
            # 市值
            if 30 <= market_cap <= 150:
                score += 5
                reasons.append("最佳市值")
            
            candidates.append(StockCandidate(
                code=code, name=name, industry=industry,
                market_cap=market_cap, pe=pe, peg=peg, roe=roe,
                profit_growth=profit_growth, revenue_growth=revenue_growth,
                gross_margin=gross_margin, score=min(score, 100),
                stage=stage, reasons=reasons
            ))
        except:
            continue
    
    candidates.sort(key=lambda x: x.score, reverse=True)
    
    print(f"\n筛选出早期潜力股: {len(candidates)} 只")
    
    # 输出结果
    if candidates:
        # 按阶段分组
        s2_stocks = [c for c in candidates if c.stage == "S2_加速期"]
        s1_stocks = [c for c in candidates if c.stage == "S1_萌芽期"]
        
        print("\n" + "="*80)
        print(f"🌟 S2加速期股票（最佳买点）: {len(s2_stocks)} 只")
        print("="*80)
        
        for i, s in enumerate(s2_stocks[:15], 1):
            print(f"\n{i}. {s.code} {s.name} 【得分: {s.score}】")
            print(f"   行业: {s.industry}")
            print(f"   市值: {s.market_cap:.0f}亿 | PE: {s.pe:.1f} | PEG: {s.peg:.2f}")
            print(f"   ROE: {s.roe*100:.1f}% | 毛利率: {s.gross_margin*100:.1f}%")
            print(f"   利润增速: +{s.profit_growth*100:.0f}% | 营收增速: +{s.revenue_growth*100:.0f}%")
            print(f"   ✅ {', '.join(s.reasons)}")
        
        print("\n" + "="*80)
        print(f"🌱 S1萌芽期股票（早期机会）: {len(s1_stocks)} 只")
        print("="*80)
        
        for i, s in enumerate(s1_stocks[:10], 1):
            print(f"\n{i}. {s.code} {s.name} 【得分: {s.score}】")
            print(f"   行业: {s.industry} | 市值: {s.market_cap:.0f}亿")
            print(f"   利润: +{s.profit_growth*100:.0f}% | 营收: +{s.revenue_growth*100:.0f}% | ROE: {s.roe*100:.1f}%")
        
        # 行业分布
        print("\n" + "="*80)
        print("📊 行业分布（S2阶段）")
        print("="*80)
        
        from collections import Counter
        s2_industries = [s.industry for s in s2_stocks if s.industry]
        if s2_industries:
            ind_count = Counter(s2_industries)
            for ind, cnt in ind_count.most_common(10):
                stocks = [s for s in s2_stocks if s.industry == ind]
                print(f"\n{ind}: {cnt} 只")
                for s in stocks[:3]:
                    print(f"  - {s.code} {s.name}: 得分{s.score}, 利润+{s.profit_growth*100:.0f}%")
        
        # 保存
        df = pd.DataFrame([{
            'code': s.code, 'name': s.name, 'stage': s.stage,
            'industry': s.industry, 'market_cap': s.market_cap,
            'pe': s.pe, 'peg': s.peg, 'roe': s.roe,
            'profit_growth': s.profit_growth, 'revenue_growth': s.revenue_growth,
            'gross_margin': s.gross_margin, 'score': s.score,
            'reasons': '|'.join(s.reasons)
        } for s in candidates])
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output = f'{PROJECT_ROOT}/results/s2_candidates_{timestamp}.csv'
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {output}")
        
        # 投资建议
        print("\n" + "="*80)
        print("💡 投资建议")
        print("="*80)
        
        print(f"\n当前市场环境: {regime}")
        if regime == "BULL":
            print("✅ 牛市环境，可积极配置S2阶段股票")
            print("\n重点关注（S2阶段Top5）:")
            for s in s2_stocks[:5]:
                print(f"  📌 {s.code} {s.name} - {s.industry}")
        else:
            print("⚠️ 非牛市环境，建议控制仓位，精选个股")
        
        print("\n操作要点:")
        print("  1. 分批建仓，每只不超过10%仓位")
        print("  2. 设置止损位（-15%）")
        print("  3. 持有周期1-2年")
        print("  4. 关注季报，确认增长持续性")
    
    else:
        print("\n⚠️ 未找到符合条件的股票")
    
    return candidates


if __name__ == '__main__':
    scan_stocks()
