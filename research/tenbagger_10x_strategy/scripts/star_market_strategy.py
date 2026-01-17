#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
科创板新股高增速策略
核心规律（基于688116案例）：
1. 科创板新股（上市<2年）
2. 小市值（<100亿）
3. 利润增速>50%
4. 高毛利率>40%
5. 新能源/半导体/AI行业
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
    print("🚀 科创板新股高增速策略 - 基于688116案例")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 2020-2021新能源牛市
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    initial = 1_000_000
    max_holdings = 3  # 集中持仓
    
    from jqdatasdk import query, valuation, indicator
    
    # 筛选科创板新股
    print("\n📊 筛选科创板新股...")
    all_stocks = jq.get_all_securities('stock', date=start_date)
    
    # 科创板 + 上市不到2年
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    cutoff_date = (start_dt - timedelta(days=730)).strftime("%Y-%m-%d")  # 2年前
    
    star_new = all_stocks[
        (all_stocks.index.str.startswith('688')) &
        (all_stocks['start_date'] >= cutoff_date)
    ]
    print(f"   科创板新股（上市<2年）: {len(star_new)} 只")
    
    # 筛选高增速
    candidates = []
    for stock in star_new.index.tolist()[:50]:
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
                
                # 688116特征：市值75亿，利润增速73%，毛利率52.6%
                if mc < 150 and pg > 30 and gm > 30:
                    score = pg * 0.5 + gm * 0.3 + (150 - mc) * 0.2
                    candidates.append({
                        'code': stock,
                        'name': star_new.loc[stock, 'display_name'],
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
    
    print(f"\n🏆 TOP 10 候选:")
    print(f"{'代码':<15} {'名称':<10} {'市值':<8} {'利润增速':<10} {'毛利率':<8} {'评分':<8}")
    print("-"*70)
    for c in candidates[:10]:
        print(f"{c['code']:<15} {c['name']:<10} {c['market_cap']:>5.0f}亿 {c['profit_growth']:>6.0f}% {c['gross_margin']:>6.0f}% {c['score']:>6.0f}")
    
    # 获取价格数据
    selected = [c['code'] for c in candidates[:max_holdings]]
    print(f"\n📈 选中: {selected}")
    
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
    
    # 等权买入
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
                
                # 止损/止盈
                ret = price / pos['cost'] - 1
                if ret <= -0.20:
                    cash += pos['shares'] * price
                    print(f"⛔ [{date_str}] 止损 {stock} 亏损:{ret*100:.1f}%")
                    del positions[stock]
                elif ret >= 3.0:  # 300%止盈
                    cash += pos['shares'] * price
                    print(f"🎯 [{date_str}] 止盈 {stock} 盈利:{ret*100:.1f}%")
                    del positions[stock]
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        if i % 40 == 0:
            ret_pct = (portfolio_value / initial - 1) * 100
            print(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}%")
    
    # 最终清算
    final_value = cash
    for stock, pos in positions.items():
        if stock in price_data:
            last_price = price_data[stock].iloc[-1]
            if not pd.isna(last_price):
                final_value += pos['shares'] * last_price
    
    total_ret = (final_value / initial - 1) * 100
    years = len(trade_days) / 250
    annual_ret = ((final_value / initial) ** (1/years) - 1) * 100 if years > 0 else 0
    
    eq_df = pd.DataFrame(equity_curve)
    eq_df['equity'] = eq_df['equity'].replace([np.inf, -np.inf], np.nan).ffill()
    max_dd = ((eq_df['equity'] / eq_df['equity'].cummax()) - 1).min() * 100
    
    print("\n" + "="*70)
    print("📋 回测结果")
    print("="*70)
    print(f"初始资金:     {initial:>15,}")
    print(f"最终净值:     {final_value:>15,.0f}")
    print(f"总收益率:     {total_ret:>14.1f}%")
    print(f"年化收益率:   {annual_ret:>14.1f}%")
    print(f"最大回撤:     {max_dd:>14.1f}%")
    
    factor = 1 + total_ret/100
    two_year = factor ** (2/years) if years > 0 else factor
    
    print("\n🎯 两年5倍目标评估:")
    print(f"   {years:.1f}年倍数: {factor:.2f}x")
    print(f"   两年预测: {two_year:.2f}x")
    print(f"   目标: 5.0x")
    
    if two_year >= 5:
        print("   ✅ 达到两年5倍目标！🎉")
    else:
        print(f"   进度: {two_year/5*100:.1f}%")
    
    return {'total_return': total_ret, 'annual_return': annual_ret, 'two_year_factor': two_year}


if __name__ == "__main__":
    run_strategy()
