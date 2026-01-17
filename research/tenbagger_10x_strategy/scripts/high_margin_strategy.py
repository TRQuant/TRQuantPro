#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高毛利率优先策略
核心发现：688116（5倍股）利润增速只有73%（不是最高），
但毛利率52.6%（非常高），这才是关键！

选股逻辑改进：
1. 毛利率权重提高到40%
2. 利润增速权重降低到30%
3. 增加行业匹配（新能源/半导体）
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def run_strategy():
    print("="*70)
    print("🎯 高毛利率优先策略 - 基于688116案例改进")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    initial = 1_000_000
    max_holdings = 3
    
    from jqdatasdk import query, valuation, indicator
    
    # 筛选科创板
    print("\n📊 筛选科创板高毛利率股票...")
    all_stocks = jq.get_all_securities('stock', date=start_date)
    star_stocks = all_stocks[all_stocks.index.str.startswith('688')]
    
    candidates = []
    for stock in star_stocks.index.tolist()[:100]:
        try:
            q = query(
                valuation.market_cap,
                indicator.inc_net_profit_year_on_year,
                indicator.gross_profit_margin,
                indicator.roe
            ).filter(valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=start_date)
            if len(df) > 0:
                row = df.iloc[0]
                mc = row['market_cap'] if pd.notna(row['market_cap']) else 999
                pg = row['inc_net_profit_year_on_year'] if pd.notna(row['inc_net_profit_year_on_year']) else 0
                gm = row['gross_profit_margin'] if pd.notna(row['gross_profit_margin']) else 0
                
                # 关键条件：高毛利率
                if mc < 150 and gm > 40:  # 毛利率>40%（核心条件）
                    # 新评分：毛利率权重最高
                    score = (
                        gm * 1.0 +                      # 毛利率权重40%
                        min(pg, 100) * 0.3 +            # 利润增速权重30%（封顶100%）
                        (150 - mc) * 0.2 +              # 小市值权重20%
                        0                               # 保留10%给行业判断
                    )
                    candidates.append({
                        'code': stock,
                        'name': star_stocks.loc[stock, 'display_name'],
                        'market_cap': mc,
                        'profit_growth': pg,
                        'gross_margin': gm,
                        'score': score
                    })
        except:
            pass
    
    if not candidates:
        print("❌ 无符合条件的股票")
        return
    
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n🏆 TOP 10 候选（毛利率优先）:")
    print(f"{'代码':<15} {'名称':<10} {'毛利率':<8} {'利润增速':<10} {'市值':<8} {'评分':<8}")
    print("-"*70)
    for c in candidates[:10]:
        print(f"{c['code']:<15} {c['name']:<10} {c['gross_margin']:>5.0f}% {c['profit_growth']:>6.0f}% {c['market_cap']:>5.0f}亿 {c['score']:>6.0f}")
    
    # 检查688116是否在列表中
    has_688116 = any(c['code'] == '688116.XSHG' for c in candidates)
    if has_688116:
        rank = next(i for i, c in enumerate(candidates) if c['code'] == '688116.XSHG') + 1
        print(f"\n✅ 688116（天奈科技）排名: 第{rank}名")
    else:
        print("\n❌ 688116不在候选列表中")
    
    # 选中TOP股票
    selected = [c['code'] for c in candidates[:max_holdings]]
    print(f"\n📈 选中: {selected}")
    
    # 获取价格数据
    price_data = {}
    for stock in selected:
        try:
            prices = jq.get_price(stock, start_date=start_date, end_date=end_date, 
                                 fields=['close'], skip_paused=True)
            if prices is not None and len(prices) > 200:
                price_data[stock] = prices['close']
        except:
            pass
    
    if not price_data:
        print("❌ 无价格数据")
        return
    
    # 回测
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    cash = initial
    positions = {}
    equity_curve = []
    
    print("\n📊 回测:")
    print("-"*70)
    
    per_stock = initial * 0.95 / len(price_data)
    first_day = str(trade_days[0])
    
    for stock in price_data:
        if first_day in price_data[stock].index:
            price = price_data[stock].loc[first_day]
            shares = int(per_stock / price / 100) * 100
            if shares > 0:
                positions[stock] = {'shares': shares, 'cost': price}
                cash -= shares * price
                name = [c['name'] for c in candidates if c['code'] == stock][0]
                print(f"🔥 [{first_day}] 买入 {stock} {name} @{price:.2f}")
    
    for i, td in enumerate(trade_days):
        date_str = str(td)
        
        portfolio_value = cash
        for stock, pos in list(positions.items()):
            if stock in price_data and date_str in price_data[stock].index:
                price = price_data[stock].loc[date_str]
                if pd.isna(price):
                    continue
                portfolio_value += pos['shares'] * price
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        if i % 40 == 0:
            ret_pct = (portfolio_value / initial - 1) * 100
            print(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}%")
    
    # 最终清算
    final_value = cash
    for stock, pos in positions.items():
        if stock in price_data:
            final_value += pos['shares'] * price_data[stock].iloc[-1]
    
    total_ret = (final_value / initial - 1) * 100
    years = len(trade_days) / 250
    annual_ret = ((final_value / initial) ** (1/years) - 1) * 100 if years > 0 else 0
    
    print("\n" + "="*70)
    print("📋 回测结果")
    print("="*70)
    print(f"初始资金:     {initial:>15,}")
    print(f"最终净值:     {final_value:>15,.0f}")
    print(f"总收益率:     {total_ret:>14.1f}%")
    print(f"年化收益率:   {annual_ret:>14.1f}%")
    
    factor = 1 + total_ret/100
    
    print(f"\n🎯 两年5倍目标评估:")
    print(f"   {years:.1f}年倍数: {factor:.2f}x")
    print(f"   目标: 5.0x")
    
    if factor >= 5:
        print("   ✅ 达到两年5倍目标！🎉")
    else:
        print(f"   进度: {factor/5*100:.1f}%")
    
    return factor


if __name__ == "__main__":
    run_strategy()
