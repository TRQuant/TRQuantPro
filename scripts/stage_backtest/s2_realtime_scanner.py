#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期十倍股 - 实时筛选器

基于回测优化后的参数，筛选当前具有十倍股潜力的S2加速期股票
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


# ============================================================
# 优化后的筛选参数（基于5年回测）
# ============================================================

# 排除行业（回测验证无效的行业）
EXCLUDE_INDUSTRIES = [
    '有色金属', '钢铁', '采掘', '建筑材料',  # 强周期
    '农林牧渔',  # 养殖周期
    '医药生物',  # 防疫一次性利润
    '房地产',    # 政策影响大
]

# 优质行业（回测验证有效的行业）
PREFERRED_INDUSTRIES = [
    '电子', '计算机', '通信', '传媒',  # 科技
    '电气设备', '机械设备',  # 制造升级
    '食品饮料', '家用电器',  # 消费
    '汽车',  # 新能源车
]

CONFIG = {
    # 市值范围（亿）
    'min_mcap': 30,
    'max_mcap': 500,
    
    # 增长指标
    'min_profit_growth': 0.20,   # 利润增速 >20%
    'max_profit_growth': 5.0,    # 利润增速 <500%
    'min_revenue_growth': 0.15,  # 营收增速 >15%
    
    # 质量指标
    'min_roe': 0.12,
    'max_pe': 80,
    'max_peg': 1.5,
}


# ============================================================
# 市场环境判断
# ============================================================

def get_market_regime() -> Tuple[str, dict]:
    """判断当前市场环境"""
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
        
        price = jq.get_price('000300.XSHG', start_date=start_date, end_date=end_date,
                             frequency='daily', fields=['close'], panel=False)
        
        if price is None or len(price) < 60:
            return "UNKNOWN", {}
        
        close = price['close']
        current = close.iloc[-1]
        ma5 = close.rolling(5).mean().iloc[-1]
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        
        # 计算涨跌幅
        change_5d = (current - close.iloc[-6]) / close.iloc[-6] * 100 if len(close) > 5 else 0
        change_20d = (current - close.iloc[-21]) / close.iloc[-21] * 100 if len(close) > 20 else 0
        
        details = {
            'current': current,
            'ma5': ma5,
            'ma20': ma20,
            'ma60': ma60,
            'change_5d': change_5d,
            'change_20d': change_20d,
        }
        
        if current > ma20 > ma60:
            return "BULL", details
        elif current < ma20 < ma60:
            return "BEAR", details
        else:
            return "VOLATILE", details
            
    except Exception as e:
        return "UNKNOWN", {'error': str(e)}


# ============================================================
# S2阶段识别器
# ============================================================

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
    reasons: List[str]
    risk_factors: List[str]


class S2Scanner:
    """S2加速期股票扫描器"""
    
    def __init__(self):
        self.config = CONFIG
    
    def scan(self, date_str: str = None) -> List[StockCandidate]:
        """扫描S2阶段股票"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        print(f"\n扫描日期: {date_str}")
        print("="*70)
        
        # 获取所有股票
        all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
        
        # 基础过滤
        valid = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|退', na=False) &
            ~all_stocks.index.str.startswith('688') &  # 排除科创板（门槛高）
            ~all_stocks.index.str.startswith('8')      # 排除北交所
        ]
        
        print(f"有效股票池: {len(valid)} 只")
        
        # 获取行业
        codes = valid.index.tolist()
        industries = jq.get_industry(codes, date=date_str)
        
        valid = valid.copy()
        valid['industry'] = ''
        for code in codes:
            if code in industries:
                ind_info = industries[code]
                if 'sw_l1' in ind_info and 'industry_name' in ind_info['sw_l1']:
                    valid.loc[code, 'industry'] = ind_info['sw_l1']['industry_name']
        
        # 获取财务数据
        fundamentals = self._get_fundamentals(codes, date_str)
        print(f"获取财务数据: {len(fundamentals)} 只")
        
        # 筛选
        candidates = []
        
        for code in fundamentals.index:
            try:
                fund = fundamentals.loc[code]
                industry = valid.loc[code, 'industry'] if code in valid.index else ''
                name = valid.loc[code, 'display_name'] if code in valid.index else code
                
                result = self._evaluate_stock(code, name, industry, fund)
                if result:
                    candidates.append(result)
            except:
                continue
        
        # 按得分排序
        candidates.sort(key=lambda x: x.score, reverse=True)
        
        print(f"筛选出S2阶段股票: {len(candidates)} 只")
        
        return candidates
    
    def _get_fundamentals(self, codes: List[str], date_str: str) -> pd.DataFrame:
        """获取财务数据"""
        batch_size = 1000
        all_dfs = []
        
        for i in range(0, len(codes), batch_size):
            batch = codes[i:i+batch_size]
            q = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin,
                jq.indicator.net_profit_margin,
            ).filter(jq.valuation.code.in_(batch))
            
            df = jq.get_fundamentals(q, date=date_str)
            if df is not None and not df.empty:
                all_dfs.append(df)
        
        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True).set_index('code')
        return pd.DataFrame()
    
    def _evaluate_stock(self, code: str, name: str, industry: str, 
                        fund: pd.Series) -> Optional[StockCandidate]:
        """评估单只股票"""
        
        reasons = []
        risk_factors = []
        score = 50
        
        # 提取数据
        market_cap = fund.get('market_cap', 0)
        pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
        roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
        revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
        profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
        gross_margin = fund.get('gross_profit_margin', 0) / 100 if pd.notna(fund.get('gross_profit_margin')) else 0
        
        # ===== 硬性过滤 =====
        
        # 行业过滤
        if industry and any(ind in industry for ind in EXCLUDE_INDUSTRIES):
            return None
        
        # 市值过滤
        if not (self.config['min_mcap'] <= market_cap <= self.config['max_mcap']):
            return None
        
        # 利润增速过滤
        if profit_growth < self.config['min_profit_growth']:
            return None
        if profit_growth > self.config['max_profit_growth']:
            risk_factors.append("利润增速异常高（可能一次性）")
            return None
        
        # 营收增速过滤（核心！）
        if revenue_growth < self.config['min_revenue_growth']:
            return None
        
        # ROE过滤
        if roe < self.config['min_roe']:
            return None
        
        # PE过滤
        if pe <= 0 or pe > self.config['max_pe']:
            return None
        
        # PEG过滤
        peg = pe / (profit_growth * 100) if profit_growth > 0.1 else 99
        if peg > self.config['max_peg']:
            return None
        
        # ===== 评分 =====
        
        # 优质行业加分
        if industry and any(ind in industry for ind in PREFERRED_INDUSTRIES):
            score += 10
            reasons.append(f"优质行业({industry})")
        
        # 市值评分
        if 50 <= market_cap <= 150:
            score += 10
            reasons.append("最佳市值区间")
        elif 30 <= market_cap <= 300:
            score += 5
        
        # 利润增速评分
        if 0.30 <= profit_growth <= 1.0:
            score += 15
            reasons.append(f"高增长({profit_growth*100:.0f}%)")
        elif profit_growth > 1.0:
            score += 10
            reasons.append(f"超高增长({profit_growth*100:.0f}%)")
        else:
            score += 5
        
        # 营收增速评分
        if revenue_growth >= 0.30:
            score += 10
            reasons.append(f"营收高增长({revenue_growth*100:.0f}%)")
        elif revenue_growth >= 0.20:
            score += 5
        
        # 利润与营收匹配度
        if revenue_growth > 0.01:
            ratio = profit_growth / revenue_growth
            if 0.5 <= ratio <= 2.0:
                score += 5
                reasons.append("利润营收匹配")
            elif ratio > 3.0:
                risk_factors.append("利润增速远超营收")
        
        # ROE评分
        if roe >= 0.25:
            score += 15
            reasons.append(f"高ROE({roe*100:.0f}%)")
        elif roe >= 0.18:
            score += 10
        else:
            score += 5
        
        # PEG评分
        if peg < 0.5:
            score += 15
            reasons.append(f"极低PEG({peg:.2f})")
        elif peg < 0.8:
            score += 10
            reasons.append(f"低PEG({peg:.2f})")
        else:
            score += 5
        
        # 毛利率评分
        if gross_margin >= 0.40:
            score += 5
            reasons.append(f"高毛利({gross_margin*100:.0f}%)")
        elif gross_margin < 0.15:
            risk_factors.append("毛利率偏低")
        
        # ===== 风险因素 =====
        
        if pe > 60:
            risk_factors.append("估值偏高")
        
        if market_cap > 300:
            risk_factors.append("市值较大，涨幅空间有限")
        
        return StockCandidate(
            code=code,
            name=name,
            industry=industry,
            market_cap=market_cap,
            pe=pe,
            peg=peg,
            roe=roe,
            profit_growth=profit_growth,
            revenue_growth=revenue_growth,
            gross_margin=gross_margin,
            score=min(score, 100),
            reasons=reasons,
            risk_factors=risk_factors
        )


# ============================================================
# 主程序
# ============================================================

def run_realtime_scan():
    """运行实时扫描"""
    
    print("="*80)
    print("S2加速期十倍股 - 实时筛选")
    print("="*80)
    print(f"\n扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 认证
    authenticate()
    
    # 市场环境
    regime, details = get_market_regime()
    print(f"\n市场环境: {regime}")
    if details and 'current' in details:
        print(f"  沪深300: {details['current']:.2f}")
        print(f"  5日涨跌: {details.get('change_5d', 0):.2f}%")
        print(f"  20日涨跌: {details.get('change_20d', 0):.2f}%")
    
    # 投资建议
    if regime == "BULL":
        print("\n📈 牛市环境 - 建议：积极配置，可满仓操作")
        position_advice = "80-100%"
    elif regime == "BEAR":
        print("\n📉 熊市环境 - 建议：谨慎观望，轻仓或空仓")
        position_advice = "0-20%"
    else:
        print("\n📊 震荡环境 - 建议：精选个股，控制仓位")
        position_advice = "30-50%"
    
    # 扫描
    scanner = S2Scanner()
    candidates = scanner.scan()
    
    if not candidates:
        print("\n⚠️ 未找到符合条件的S2阶段股票")
        print("建议：等待市场出现新的机会，或适当放宽条件")
        return
    
    # 输出结果
    print("\n" + "="*80)
    print(f"筛选结果：{len(candidates)} 只S2阶段潜力股")
    print("="*80)
    
    print(f"\n建议仓位：{position_advice}")
    
    # Top 10
    print("\n" + "-"*80)
    print("🌟 Top 10 推荐")
    print("-"*80)
    
    for i, s in enumerate(candidates[:10], 1):
        print(f"\n{i}. {s.code} {s.name} 【得分: {s.score}】")
        print(f"   行业: {s.industry}")
        print(f"   市值: {s.market_cap:.0f}亿 | PE: {s.pe:.1f} | PEG: {s.peg:.2f}")
        print(f"   ROE: {s.roe*100:.1f}% | 毛利率: {s.gross_margin*100:.1f}%")
        print(f"   利润增速: +{s.profit_growth*100:.0f}% | 营收增速: +{s.revenue_growth*100:.0f}%")
        
        if s.reasons:
            print(f"   ✅ 优势: {', '.join(s.reasons)}")
        if s.risk_factors:
            print(f"   ⚠️ 风险: {', '.join(s.risk_factors)}")
    
    # 按行业分组
    print("\n" + "-"*80)
    print("📊 行业分布")
    print("-"*80)
    
    from collections import Counter
    industries = [s.industry for s in candidates if s.industry]
    ind_count = Counter(industries)
    
    for ind, cnt in ind_count.most_common(10):
        stocks = [s for s in candidates if s.industry == ind]
        avg_score = np.mean([s.score for s in stocks])
        print(f"  {ind}: {cnt} 只 (平均得分: {avg_score:.0f})")
        for s in stocks[:3]:
            print(f"    - {s.code} {s.name}: 得分{s.score}")
    
    # 保存结果
    df = pd.DataFrame([{
        'code': s.code,
        'name': s.name,
        'industry': s.industry,
        'market_cap': s.market_cap,
        'pe': s.pe,
        'peg': s.peg,
        'roe': s.roe,
        'profit_growth': s.profit_growth,
        'revenue_growth': s.revenue_growth,
        'gross_margin': s.gross_margin,
        'score': s.score,
        'reasons': '|'.join(s.reasons),
        'risk_factors': '|'.join(s.risk_factors)
    } for s in candidates])
    
    output_path = f'{PROJECT_ROOT}/results'
    os.makedirs(output_path, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f'{output_path}/s2_realtime_{timestamp}.csv'
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n结果已保存: {output_file}")
    
    # 投资建议总结
    print("\n" + "="*80)
    print("💡 投资建议")
    print("="*80)
    
    if regime == "BEAR":
        print("\n⚠️ 当前为熊市环境，建议观望")
        print("  - 即使有优质标的，也建议等待市场企稳")
        print("  - 可先建立观察仓（5-10%）跟踪")
    else:
        print(f"\n推荐关注（Top 5）:")
        for s in candidates[:5]:
            print(f"  📌 {s.code} {s.name}")
            print(f"     理由: {', '.join(s.reasons[:3])}")
        
        print("\n操作建议:")
        print("  1. 分批建仓，不要一次性买入")
        print("  2. 设置止损位（-15%）")
        print("  3. 持有周期建议1-2年")
        print("  4. 定期复盘，关注业绩变化")
    
    return candidates


if __name__ == '__main__':
    run_realtime_scan()
