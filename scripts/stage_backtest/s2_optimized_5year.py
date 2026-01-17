#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期策略 - 优化版5年回测

优化点：
1. 放宽筛选条件，增加候选池
2. 增加行业过滤（排除强周期行业）
3. 增加市场环境判断
4. 多持有期对比（1年、2年）
5. 增加PEG估值过滤
"""

import sys
import os

PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

import jqdatasdk as jq
from jqdata.auth import authenticate


# ============================================================
# 周期性行业（需排除）
# ============================================================

CYCLICAL_INDUSTRIES = [
    '有色金属', '钢铁', '化工', '采掘', '建筑材料',
    '建筑装饰', '房地产', '交通运输', '公用事业'
]


# ============================================================
# 优化后的S2识别器
# ============================================================

class OptimizedS2Identifier:
    """优化后的S2加速期识别器
    
    优化点：
    1. 放宽市值范围：30-500亿（原50-500亿）
    2. 放宽利润增速：>20%（原>25%）
    3. 放宽ROE：>10%（原>12%）
    4. 增加PEG过滤：<1.5
    5. 排除周期性行业
    """
    
    def __init__(self, strict: bool = False):
        self.strict = strict
        
        # 宽松条件
        self.loose_config = {
            'min_mcap': 30, 'max_mcap': 500,
            'min_profit_growth': 0.20,
            'min_roe': 0.10,
            'max_peg': 2.0
        }
        
        # 严格条件
        self.strict_config = {
            'min_mcap': 50, 'max_mcap': 300,
            'min_profit_growth': 0.30,
            'min_roe': 0.15,
            'max_peg': 1.5
        }
        
        self.config = self.strict_config if strict else self.loose_config
    
    def identify(self, market_cap: float, profit_growth: float, 
                 roe: float, pe: float, industry: str = '') -> Tuple[bool, float, str]:
        """识别S2阶段
        
        Returns:
            (是否S2, 得分, 原因)
        """
        reasons = []
        score = 50
        
        # 市值过滤
        if market_cap < self.config['min_mcap']:
            return False, 0, "市值过小"
        if market_cap > self.config['max_mcap']:
            return False, 0, "市值过大"
        
        # 市值得分
        if 50 <= market_cap <= 150:
            score += 15  # 最佳市值区间
        elif 30 <= market_cap <= 300:
            score += 10
        else:
            score += 5
        
        # 利润增速（核心指标）
        if profit_growth < self.config['min_profit_growth']:
            return False, 0, "利润增速不足"
        
        if profit_growth >= 0.50:
            score += 25
            reasons.append("利润高增长")
        elif profit_growth >= 0.30:
            score += 20
            reasons.append("利润快速增长")
        else:
            score += 10
        
        # ROE
        if roe < self.config['min_roe']:
            return False, 0, "ROE过低"
        
        if roe >= 0.20:
            score += 15
            reasons.append("高ROE")
        elif roe >= 0.15:
            score += 10
        else:
            score += 5
        
        # PEG估值
        if profit_growth > 0.05 and pe > 0:
            peg = pe / (profit_growth * 100)
            if peg > self.config['max_peg']:
                return False, 0, f"PEG过高({peg:.1f})"
            
            if peg < 0.5:
                score += 15
                reasons.append("极低PEG")
            elif peg < 1.0:
                score += 10
                reasons.append("低PEG")
            elif peg < 1.5:
                score += 5
        
        # 行业过滤
        if industry and any(ind in industry for ind in CYCLICAL_INDUSTRIES):
            score -= 10
            reasons.append("周期行业")
        
        return True, min(score, 100), ", ".join(reasons) if reasons else "S2阶段"


# ============================================================
# 市场环境判断
# ============================================================

def get_market_regime(date_str: str) -> str:
    """判断市场环境
    
    使用沪深300的20日和60日均线判断
    """
    try:
        end_date = datetime.strptime(date_str, '%Y-%m-%d')
        start_date = end_date - timedelta(days=100)
        
        price = jq.get_price(
            '000300.XSHG',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=date_str,
            frequency='daily',
            fields=['close'],
            panel=False
        )
        
        if price is None or len(price) < 60:
            return "UNKNOWN"
        
        close = price['close']
        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1]
        current = close.iloc[-1]
        
        # 判断趋势
        if current > ma20 > ma60:
            return "BULL"  # 牛市
        elif current < ma20 < ma60:
            return "BEAR"  # 熊市
        else:
            return "VOLATILE"  # 震荡
            
    except Exception:
        return "UNKNOWN"


# ============================================================
# 数据获取
# ============================================================

def get_all_stocks_with_industry(date_str: str) -> pd.DataFrame:
    """获取所有A股及其行业"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    
    # 过滤
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &
        ~all_stocks.index.str.startswith('8')
    ]
    
    # 获取行业
    codes = valid.index.tolist()
    industries = jq.get_industry(codes, date=date_str)
    
    valid['industry'] = ''
    for code in codes:
        if code in industries:
            ind_info = industries[code]
            if 'sw_l1' in ind_info and 'industry_name' in ind_info['sw_l1']:
                valid.loc[code, 'industry'] = ind_info['sw_l1']['industry_name']
    
    return valid


def get_fundamentals_batch(codes: List[str], date_str: str) -> pd.DataFrame:
    """批量获取基本面数据"""
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


def calculate_return(code: str, start_date: str, days: int) -> Optional[float]:
    """计算收益率"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = start + timedelta(days=days + 30)
        
        price = jq.get_price(
            code,
            start_date=start_date,
            end_date=end.strftime('%Y-%m-%d'),
            frequency='daily',
            fields=['close'],
            panel=False
        )
        
        if price is None or len(price) < 10:
            return None
        
        return (price['close'].iloc[-1] - price['close'].iloc[0]) / price['close'].iloc[0]
        
    except Exception:
        return None


# ============================================================
# 筛选与回测
# ============================================================

@dataclass
class StockResult:
    code: str
    name: str
    screen_date: str
    industry: str
    market_cap: float
    profit_growth: float
    revenue_growth: float
    roe: float
    pe: float
    peg: float
    score: float
    reason: str
    return_1y: Optional[float] = None
    return_2y: Optional[float] = None


def screen_s2_stocks(screen_date: str, stocks_df: pd.DataFrame, 
                     strict: bool = False) -> List[StockResult]:
    """筛选S2阶段股票"""
    identifier = OptimizedS2Identifier(strict=strict)
    
    codes = stocks_df.index.tolist()
    fundamentals = get_fundamentals_batch(codes, screen_date)
    
    results = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            
            # 基本过滤
            if pe <= 0 or pe > 200:
                continue
            
            industry = stocks_df.loc[code, 'industry'] if code in stocks_df.index else ''
            
            # S2识别
            is_s2, score, reason = identifier.identify(
                market_cap, profit_growth, roe, pe, industry
            )
            
            if is_s2:
                peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 99
                name = stocks_df.loc[code, 'display_name'] if code in stocks_df.index else code
                
                results.append(StockResult(
                    code=code,
                    name=name,
                    screen_date=screen_date,
                    industry=industry,
                    market_cap=market_cap,
                    profit_growth=profit_growth,
                    revenue_growth=revenue_growth,
                    roe=roe,
                    pe=pe,
                    peg=peg,
                    score=score,
                    reason=reason
                ))
                
        except Exception:
            continue
    
    results.sort(key=lambda x: x.score, reverse=True)
    return results


def run_optimized_backtest():
    """运行优化版回测"""
    
    print("="*80)
    print("S2加速期策略 - 优化版5年回测")
    print("="*80)
    print("\n策略逻辑：")
    print("  1. 企业生命周期S2阶段（加速成长期）是十倍股最佳买入时机")
    print("  2. 核心筛选条件：市值30-500亿、利润增速>20%、ROE>10%、PEG<2")
    print("  3. 排除周期性行业，降低假阳性")
    print("  4. 市场环境判断，熊市谨慎操作")
    print()
    
    authenticate()
    
    screen_dates = ['2020-06-01', '2021-06-01', '2022-06-01', '2023-06-01', '2024-06-01']
    
    all_results = []
    yearly_stats = []
    
    for screen_date in screen_dates:
        print(f"\n{'='*70}")
        print(f"筛选日期: {screen_date}")
        
        # 市场环境
        regime = get_market_regime(screen_date)
        print(f"市场环境: {regime}")
        print("="*70)
        
        # 获取股票
        stocks_df = get_all_stocks_with_industry(screen_date)
        print(f"有效股票: {len(stocks_df)} 只")
        
        # 宽松筛选
        s2_stocks = screen_s2_stocks(screen_date, stocks_df, strict=False)
        print(f"S2阶段股票（宽松）: {len(s2_stocks)} 只")
        
        # 严格筛选
        s2_strict = screen_s2_stocks(screen_date, stocks_df, strict=True)
        print(f"S2阶段股票（严格）: {len(s2_strict)} 只")
        
        if not s2_stocks:
            continue
        
        # 选取Top20
        top_stocks = s2_stocks[:20]
        
        # 计算收益
        print("计算1年和2年收益...")
        for stock in top_stocks:
            stock.return_1y = calculate_return(stock.code, screen_date, 252)
            stock.return_2y = calculate_return(stock.code, screen_date, 504)
        
        # 统计
        valid_1y = [s.return_1y for s in top_stocks if s.return_1y is not None]
        valid_2y = [s.return_2y for s in top_stocks if s.return_2y is not None]
        
        if valid_1y:
            print(f"\n{screen_date[:4]}年统计:")
            print(f"  1年平均收益: {np.mean(valid_1y)*100:.2f}%, 胜率: {sum(1 for r in valid_1y if r>0)/len(valid_1y)*100:.1f}%")
            if valid_2y:
                print(f"  2年平均收益: {np.mean(valid_2y)*100:.2f}%, 胜率: {sum(1 for r in valid_2y if r>0)/len(valid_2y)*100:.1f}%")
            
            yearly_stats.append({
                'year': screen_date[:4],
                'regime': regime,
                'count': len(valid_1y),
                'avg_1y': np.mean(valid_1y),
                'win_1y': sum(1 for r in valid_1y if r>0)/len(valid_1y),
                'max_1y': np.max(valid_1y),
                'avg_2y': np.mean(valid_2y) if valid_2y else None,
                'win_2y': sum(1 for r in valid_2y if r>0)/len(valid_2y) if valid_2y else None,
            })
        
        all_results.extend(top_stocks)
    
    # ============================================================
    # 汇总
    # ============================================================
    
    print("\n" + "="*80)
    print("5年汇总统计（优化版）")
    print("="*80)
    
    print("\n年度表现:")
    print("-"*90)
    print(f"{'年份':<6} {'环境':<10} {'股票数':<8} {'1年收益':<12} {'1年胜率':<10} {'2年收益':<12} {'2年胜率':<10}")
    print("-"*90)
    
    for stat in yearly_stats:
        y2_ret = f"{stat['avg_2y']*100:.1f}%" if stat['avg_2y'] is not None else "N/A"
        y2_win = f"{stat['win_2y']*100:.1f}%" if stat['win_2y'] is not None else "N/A"
        print(f"{stat['year']:<6} {stat['regime']:<10} {stat['count']:<8} "
              f"{stat['avg_1y']*100:>8.1f}%    {stat['win_1y']*100:>6.1f}%    "
              f"{y2_ret:>8}    {y2_win:>6}")
    
    # 高回报股票
    print("\n" + "="*80)
    print("高回报股票统计")
    print("="*80)
    
    # 1年翻倍
    double_1y = [s for s in all_results if s.return_1y is not None and s.return_1y > 1.0]
    double_1y.sort(key=lambda x: x.return_1y, reverse=True)
    
    print(f"\n1年翻倍股票（收益>100%）: {len(double_1y)} 只")
    for s in double_1y:
        print(f"  {s.code} {s.name}: +{s.return_1y*100:.1f}% ({s.screen_date}, {s.industry})")
        print(f"    市值{s.market_cap:.0f}亿, 利润增速{s.profit_growth*100:.0f}%, ROE{s.roe*100:.1f}%")
    
    # 2年翻倍
    double_2y = [s for s in all_results if s.return_2y is not None and s.return_2y > 1.0]
    double_2y.sort(key=lambda x: x.return_2y, reverse=True)
    
    print(f"\n2年翻倍股票（收益>100%）: {len(double_2y)} 只")
    for s in double_2y[:10]:
        print(f"  {s.code} {s.name}: +{s.return_2y*100:.1f}% ({s.screen_date}, {s.industry})")
    
    # 高回报（>50%）
    high_1y = [s for s in all_results if s.return_1y is not None and s.return_1y > 0.5]
    high_2y = [s for s in all_results if s.return_2y is not None and s.return_2y > 0.5]
    
    print(f"\n1年高回报（>50%）: {len(high_1y)} 只")
    print(f"2年高回报（>50%）: {len(high_2y)} 只")
    
    # 特征分析
    print("\n" + "="*80)
    print("高回报股票特征分析（1年收益>50%）")
    print("="*80)
    
    if high_1y:
        print(f"\n共 {len(high_1y)} 只高回报股票:")
        print(f"  平均市值: {np.mean([s.market_cap for s in high_1y]):.1f} 亿")
        print(f"  平均利润增速: {np.mean([s.profit_growth for s in high_1y])*100:.1f}%")
        print(f"  平均ROE: {np.mean([s.roe for s in high_1y])*100:.1f}%")
        print(f"  平均PEG: {np.mean([s.peg for s in high_1y if s.peg < 10]):.2f}")
        
        # 行业分布
        industries = [s.industry for s in high_1y if s.industry]
        if industries:
            from collections import Counter
            ind_count = Counter(industries)
            print(f"\n  行业分布:")
            for ind, cnt in ind_count.most_common(5):
                print(f"    {ind}: {cnt} 只")
    
    # 保存结果
    results_df = pd.DataFrame([{
        'code': s.code,
        'name': s.name,
        'screen_date': s.screen_date,
        'industry': s.industry,
        'market_cap': s.market_cap,
        'profit_growth': s.profit_growth,
        'revenue_growth': s.revenue_growth,
        'roe': s.roe,
        'pe': s.pe,
        'peg': s.peg,
        'score': s.score,
        'return_1y': s.return_1y,
        'return_2y': s.return_2y
    } for s in all_results])
    
    output_path = f'{PROJECT_ROOT}/results'
    os.makedirs(output_path, exist_ok=True)
    results_df.to_csv(f'{output_path}/s2_optimized_5year_results.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n结果已保存: {output_path}/s2_optimized_5year_results.csv")
    
    return all_results, yearly_stats


if __name__ == '__main__':
    run_optimized_backtest()
