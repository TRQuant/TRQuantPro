#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据检查脚本 - 诊断为什么筛不出股票
"""

import sys
sys.path.insert(0, '/home/taotao/.cursor/worktrees/TRQuant/ope')

import pandas as pd
import numpy as np
from datetime import datetime
import jqdatasdk as jq
from jqdata.auth import authenticate

print("="*60)
print("数据诊断")
print("="*60)

authenticate()

date_str = datetime.now().strftime('%Y-%m-%d')
print(f"\n检查日期: {date_str}")

# 获取股票
all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
valid = all_stocks[
    ~all_stocks['display_name'].str.contains('ST|退', na=False) &
    ~all_stocks.index.str.startswith('688') &
    ~all_stocks.index.str.startswith('8')
]
print(f"有效股票: {len(valid)} 只")

# 获取财务数据
codes = valid.index.tolist()[:500]  # 先检查500只

q = jq.query(
    jq.valuation.code,
    jq.valuation.market_cap,
    jq.valuation.pe_ratio,
    jq.indicator.roe,
    jq.indicator.inc_revenue_year_on_year,
    jq.indicator.inc_net_profit_year_on_year,
).filter(jq.valuation.code.in_(codes))

df = jq.get_fundamentals(q, date=date_str)
print(f"\n财务数据样本: {len(df)} 条")

if not df.empty:
    df = df.set_index('code')
    
    # 统计各指标分布
    print("\n指标分布:")
    print("-"*40)
    
    # 市值
    mcap = df['market_cap'].dropna()
    print(f"\n市值（亿）:")
    print(f"  范围: {mcap.min():.0f} - {mcap.max():.0f}")
    print(f"  中位数: {mcap.median():.0f}")
    print(f"  20-800亿: {len(mcap[(mcap >= 20) & (mcap <= 800)])} 只")
    
    # 利润增速
    pg = df['inc_net_profit_year_on_year'].dropna() / 100
    print(f"\n利润增速:")
    print(f"  有数据: {len(pg)} 只")
    print(f"  >10%: {len(pg[pg > 0.10])} 只")
    print(f"  >20%: {len(pg[pg > 0.20])} 只")
    print(f"  >30%: {len(pg[pg > 0.30])} 只")
    
    # 营收增速
    rg = df['inc_revenue_year_on_year'].dropna() / 100
    print(f"\n营收增速:")
    print(f"  有数据: {len(rg)} 只")
    print(f"  >8%: {len(rg[rg > 0.08])} 只")
    print(f"  >15%: {len(rg[rg > 0.15])} 只")
    
    # ROE
    roe = df['roe'].dropna() / 100
    print(f"\nROE:")
    print(f"  有数据: {len(roe)} 只")
    print(f"  >8%: {len(roe[roe > 0.08])} 只")
    print(f"  >12%: {len(roe[roe > 0.12])} 只")
    
    # PE
    pe = df['pe_ratio'].dropna()
    pe_valid = pe[(pe > 0) & (pe < 100)]
    print(f"\nPE:")
    print(f"  0<PE<100: {len(pe_valid)} 只")
    
    # 组合条件
    print("\n" + "="*60)
    print("组合条件筛选")
    print("="*60)
    
    # 条件1：基础筛选
    cond1 = (
        (df['market_cap'] >= 20) & (df['market_cap'] <= 800)
    )
    print(f"\n市值20-800亿: {cond1.sum()} 只")
    
    # 条件2：增长
    cond2 = (
        cond1 &
        (df['inc_net_profit_year_on_year'] > 10) &  # >10%
        (df['inc_revenue_year_on_year'] > 8)        # >8%
    )
    print(f"+ 利润>10%, 营收>8%: {cond2.sum()} 只")
    
    # 条件3：质量
    cond3 = (
        cond2 &
        (df['roe'] > 8)  # >8%
    )
    print(f"+ ROE>8%: {cond3.sum()} 只")
    
    # 条件4：估值
    cond4 = (
        cond3 &
        (df['pe_ratio'] > 0) & (df['pe_ratio'] < 100)
    )
    print(f"+ 0<PE<100: {cond4.sum()} 只")
    
    # 显示符合条件的股票
    if cond4.sum() > 0:
        result = df[cond4].copy()
        result['profit_growth'] = result['inc_net_profit_year_on_year']
        result['revenue_growth'] = result['inc_revenue_year_on_year']
        
        print(f"\n符合基础条件的股票:")
        for code in result.index[:10]:
            r = result.loc[code]
            name = valid.loc[code, 'display_name'] if code in valid.index else code
            print(f"  {code} {name}: 市值{r['market_cap']:.0f}亿, "
                  f"利润+{r['profit_growth']:.0f}%, 营收+{r['revenue_growth']:.0f}%, "
                  f"ROE{r['roe']:.0f}%, PE{r['pe_ratio']:.0f}")
    else:
        print("\n⚠️ 没有符合基础条件的股票！")
        print("\n检查数据质量...")
        
        # 检查NaN比例
        print(f"\n缺失值比例:")
        print(f"  market_cap: {df['market_cap'].isna().mean()*100:.1f}%")
        print(f"  pe_ratio: {df['pe_ratio'].isna().mean()*100:.1f}%")
        print(f"  roe: {df['roe'].isna().mean()*100:.1f}%")
        print(f"  inc_net_profit_year_on_year: {df['inc_net_profit_year_on_year'].isna().mean()*100:.1f}%")
        print(f"  inc_revenue_year_on_year: {df['inc_revenue_year_on_year'].isna().mean()*100:.1f}%")
else:
    print("⚠️ 未获取到财务数据！")
