#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
S2加速期策略 - 严格筛选版V2

针对之前版本的问题进行优化：
1. 排除一次性利润暴增（限制利润增速上限300%）
2. 要求营收同步增长（营收增速>20%）
3. 排除更多周期性行业（农林牧渔、医疗器械等）
4. 要求ROE更高（>15%）
5. 缩短持有期（1年）+ 更宽松止损（-15%）
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
# 配置
# ============================================================

# 排除行业（扩展版）
EXCLUDE_INDUSTRIES = [
    '有色金属', '钢铁', '化工', '采掘', '建筑材料',
    '建筑装饰', '房地产', '交通运输', '公用事业',
    '农林牧渔',  # 周期性强
    '医药生物',  # 防疫类一次性利润
]

CONFIG = {
    # 筛选条件（更严格）
    'min_mcap': 50,            # 最小市值
    'max_mcap': 300,           # 最大市值（缩小）
    'min_profit_growth': 0.25, # 最小利润增速
    'max_profit_growth': 3.0,  # 最大利润增速（新增：排除一次性暴增）
    'min_revenue_growth': 0.20,# 最小营收增速（新增）
    'min_roe': 0.15,           # 最小ROE（提高）
    'max_peg': 1.0,            # 最大PEG
    'max_pe': 60,              # 最大PE（降低）
    
    # 仓位
    'bull_position': 1.0,
    'volatile_position': 0.3,  # 降低震荡市仓位
    'bear_position': 0.0,
    
    # 风控
    'stop_loss': -0.15,        # 止损放宽到-15%
    'hold_days': 252,          # 持有期缩短到1年
}


# ============================================================
# 市场环境
# ============================================================

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


# ============================================================
# 严格S2识别器
# ============================================================

class StrictS2Identifier:
    """严格版S2识别器"""
    
    def identify(self, market_cap: float, profit_growth: float, revenue_growth: float,
                 roe: float, pe: float, industry: str = '') -> Tuple[bool, float, str]:
        
        # 行业排除
        if industry and any(ind in industry for ind in EXCLUDE_INDUSTRIES):
            return False, 0, "排除行业"
        
        # 市值
        if not (CONFIG['min_mcap'] <= market_cap <= CONFIG['max_mcap']):
            return False, 0, "市值不符"
        
        # 利润增速（设置上限，排除一次性暴增）
        if profit_growth < CONFIG['min_profit_growth']:
            return False, 0, "利润增速不足"
        if profit_growth > CONFIG['max_profit_growth']:
            return False, 0, "利润增速异常（可能一次性）"
        
        # 营收增速（新增：确保业务真正增长）
        if revenue_growth < CONFIG['min_revenue_growth']:
            return False, 0, "营收增速不足"
        
        # ROE
        if roe < CONFIG['min_roe']:
            return False, 0, "ROE不足"
        
        # PE
        if pe <= 0 or pe > CONFIG['max_pe']:
            return False, 0, "PE不符"
        
        # PEG
        peg = pe / (profit_growth * 100) if profit_growth > 0.1 else 99
        if peg > CONFIG['max_peg']:
            return False, 0, f"PEG过高({peg:.2f})"
        
        # 计算得分
        score = 50
        
        # 利润与营收匹配度加分
        if 0.8 <= profit_growth / max(revenue_growth, 0.01) <= 2.0:
            score += 15  # 利润与营收增速匹配
        
        # ROE加分
        if roe >= 0.25:
            score += 15
        elif roe >= 0.20:
            score += 10
        else:
            score += 5
        
        # PEG加分
        if peg < 0.5:
            score += 15
        elif peg < 0.8:
            score += 10
        else:
            score += 5
        
        # 市值加分
        if 80 <= market_cap <= 200:
            score += 10
        elif 50 <= market_cap <= 300:
            score += 5
        
        reason = f"利润+{profit_growth*100:.0f}%, 营收+{revenue_growth*100:.0f}%, ROE{roe*100:.0f}%"
        return True, min(score, 100), reason


# ============================================================
# 数据获取
# ============================================================

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
    """获取收益率和止损情况"""
    try:
        end = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=days+30)
        
        price = jq.get_price(code, start_date=start_date, end_date=end.strftime('%Y-%m-%d'),
                             frequency='daily', fields=['close'], panel=False)
        
        if price is None or len(price) < 10:
            return None
        
        prices = price['close'].values
        entry_price = prices[0]
        
        # 检查止损
        for i, p in enumerate(prices):
            ret = (p - entry_price) / entry_price
            if ret <= CONFIG['stop_loss']:
                return ret, "止损"
        
        # 持有到期
        final_idx = min(days, len(prices) - 1)
        final_ret = (prices[final_idx] - entry_price) / entry_price
        return final_ret, "到期"
        
    except:
        return None


# ============================================================
# 回测
# ============================================================

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
    identifier = StrictS2Identifier()
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
    print("S2加速期策略 - 严格筛选版V2")
    print("="*80)
    print("\n核心优化：")
    print(f"  1. 利润增速：{CONFIG['min_profit_growth']*100:.0f}% - {CONFIG['max_profit_growth']*100:.0f}%（排除一次性暴增）")
    print(f"  2. 营收增速：>{CONFIG['min_revenue_growth']*100:.0f}%（确保业务真正增长）")
    print(f"  3. ROE：>{CONFIG['min_roe']*100:.0f}%")
    print(f"  4. 排除行业：农林牧渔、医药生物、周期股")
    print(f"  5. 持有期：{CONFIG['hold_days']}天，止损：{CONFIG['stop_loss']*100:.0f}%")
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
        
        # 仓位决策
        if regime == "BEAR":
            position = CONFIG['bear_position']
            print(f"熊市空仓")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': len(candidates),
                               'trades': 0, 'avg_return': None, 'win_rate': None})
            continue
        elif regime == "VOLATILE":
            position = CONFIG['volatile_position']
        else:
            position = CONFIG['bull_position']
        
        if not candidates:
            print("无候选股票")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': 0,
                               'trades': 0, 'avg_return': None, 'win_rate': None})
            continue
        
        # 选股
        top_n = max(3, int(10 * position))
        selected = candidates[:top_n]
        
        print(f"选取{len(selected)}只（仓位{position*100:.0f}%）:")
        for s in selected[:5]:
            print(f"  {s.code} {s.name}: 得分{s.score}, 利润+{s.profit_growth*100:.0f}%, 营收+{s.revenue_growth*100:.0f}%")
        
        # 计算收益
        print("计算收益...")
        entry_date = screen_date  # 简化处理
        
        returns = []
        for s in selected:
            result = get_return(s.code, entry_date, CONFIG['hold_days'])
            if result:
                s.return_pct, s.reason = result
                returns.append(s.return_pct)
                all_results.append(s)
        
        if returns:
            avg_ret = np.mean(returns)
            win_rate = sum(1 for r in returns if r > 0) / len(returns)
            print(f"\n结果: 平均收益{avg_ret*100:.1f}%, 胜率{win_rate*100:.0f}%")
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': len(candidates),
                               'trades': len(returns), 'avg_return': avg_ret, 'win_rate': win_rate})
        else:
            yearly_stats.append({'year': screen_date[:4], 'regime': regime, 'candidates': len(candidates),
                               'trades': 0, 'avg_return': None, 'win_rate': None})
    
    # 汇总
    print("\n" + "="*80)
    print("5年汇总（严格筛选版V2）")
    print("="*80)
    
    print("\n年度表现:")
    print("-"*80)
    for stat in yearly_stats:
        if stat['trades'] > 0:
            print(f"{stat['year']} {stat['regime']:<10} 候选{stat['candidates']:<4} 交易{stat['trades']:<4} "
                  f"收益{stat['avg_return']*100:>6.1f}%  胜率{stat['win_rate']*100:>5.0f}%")
        else:
            print(f"{stat['year']} {stat['regime']:<10} 候选{stat['candidates']:<4} {'空仓/无候选':<20}")
    
    # 高回报股票
    if all_results:
        all_results_sorted = sorted(all_results, key=lambda x: x.return_pct, reverse=True)
        
        high_return = [s for s in all_results_sorted if s.return_pct > 0.5]
        double = [s for s in all_results_sorted if s.return_pct > 1.0]
        
        print(f"\n翻倍股票: {len(double)} 只")
        for s in double:
            print(f"  {s.code} {s.name}: +{s.return_pct*100:.1f}% ({s.industry})")
        
        print(f"\n高回报（>50%）: {len(high_return)} 只")
        for s in high_return[:10]:
            print(f"  {s.code} {s.name}: +{s.return_pct*100:.1f}%")
        
        # 整体统计
        all_returns = [s.return_pct for s in all_results]
        print(f"\n整体统计:")
        print(f"  总交易: {len(all_returns)} 笔")
        print(f"  平均收益: {np.mean(all_returns)*100:.2f}%")
        print(f"  胜率: {sum(1 for r in all_returns if r>0)/len(all_returns)*100:.1f}%")
        print(f"  最高: +{np.max(all_returns)*100:.1f}%")
        print(f"  最低: {np.min(all_returns)*100:.1f}%")
    
    # 保存
    if all_results:
        df = pd.DataFrame([{
            'code': s.code, 'name': s.name, 'industry': s.industry,
            'market_cap': s.market_cap, 'profit_growth': s.profit_growth,
            'revenue_growth': s.revenue_growth, 'roe': s.roe,
            'score': s.score, 'return_pct': s.return_pct, 'reason': s.reason
        } for s in all_results])
        
        output = f'{PROJECT_ROOT}/results/s2_strict_v2_results.csv'
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存: {output}")


if __name__ == '__main__':
    run_backtest()
