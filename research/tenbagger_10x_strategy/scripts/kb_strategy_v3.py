#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""知识库策略V3 - 修复市值单位"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def run_strategy():
    print("="*70)
    print("📚 知识库策略V3 - 市值单位修复版")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    initial = 1_000_000
    max_holdings = 3
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    from jqdatasdk import query, valuation, indicator
    
    # 预先筛选所有符合基本条件的股票
    print("\n📊 预筛选高成长股票...")
    q = query(
        valuation.code,
        valuation.market_cap,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
        indicator.roe
    ).filter(
        # 科创板+创业板
        (valuation.code.like('688%') | valuation.code.like('300%')),
        # 小市值 (JQData market_cap单位是亿元)
        valuation.market_cap < 150,  # <150亿
        valuation.market_cap > 10,   # >10亿
        # 高增速
        indicator.inc_net_profit_year_on_year > 30,  # 利润>30%
        indicator.inc_revenue_year_on_year > 10,     # 营收>10%
        # 盈利
        indicator.roe > 5
    ).limit(100)
    
    df = jq.get_fundamentals(q, date=start_date)
    print(f"   筛选出 {len(df)} 只候选股")
    
    if len(df) > 0:
        df['score'] = (
            df['inc_net_profit_year_on_year'].clip(0, 150) * 0.5 +
            df['inc_revenue_year_on_year'].clip(0, 100) * 0.3 +
            df['roe'].clip(0, 30) * 1.5 +
            (150 - df['market_cap']).clip(0, 100) * 0.2
        )
        df = df.sort_values('score', ascending=False)
        
        print("\n🏆 TOP 10 候选:")
        print(f"{'代码':<15} {'利润增速':<10} {'营收增速':<10} {'ROE':<8} {'市值':<10} {'评分':<8}")
        print("-"*70)
        for _, row in df.head(10).iterrows():
            print(f"{row['code']:<15} {row['inc_net_profit_year_on_year']:>6.0f}% {row['inc_revenue_year_on_year']:>6.0f}% {row['roe']:>6.1f}% {row['market_cap']:>6.0f}亿 {row['score']:>6.0f}")
    else:
        print("❌ 无候选股票，放宽条件...")
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year,
            indicator.roe
        ).filter(
            (valuation.code.like('688%') | valuation.code.like('300%')),
            valuation.market_cap < 300,
            indicator.inc_net_profit_year_on_year > 20
        ).limit(100)
        df = jq.get_fundamentals(q, date=start_date)
        print(f"   放宽后筛选出 {len(df)} 只")
        
        if len(df) > 0:
            df['score'] = df['inc_net_profit_year_on_year'].fillna(0) * 0.5
            df = df.sort_values('score', ascending=False)
    
    if len(df) == 0:
        print("❌ 仍无候选股")
        return
    
    # 获取价格数据
    candidates = df['code'].head(20).tolist()
    print(f"\n📈 加载TOP {len(candidates)} 股票价格...")
    
    price_data = {}
    for stock in candidates:
        try:
            prices = jq.get_price(stock, start_date=start_date, end_date=end_date, fields=['close'])
            if prices is not None and len(prices) > 50:
                price_data[stock] = prices['close']
        except:
            pass
    print(f"   成功加载 {len(price_data)} 只")
    
    if not price_data:
        print("❌ 无价格数据")
        return
    
    # 选择TOP 3
    selected = [s for s in candidates if s in price_data][:max_holdings]
    print(f"\n📊 选中: {selected}")
    
    # 回测
    cash = initial
    positions = {}
    equity_curve = []
    
    print("\n📊 回测交易:")
    print("-"*70)
    
    # 初始买入
    first_day = str(trade_days[0])
    per_stock = initial * 0.95 / len(selected)
    
    for stock in selected:
        if first_day in price_data[stock].index:
            price = price_data[stock].loc[first_day]
            shares = int(per_stock / price / 100) * 100
            if shares > 0:
                positions[stock] = {'shares': shares, 'cost': price}
                cash -= shares * price
                print(f"🔥 [{first_day}] 买入 {stock} @{price:.2f} x{shares}")
    
    for i, td in enumerate(trade_days):
        date_str = str(td)
        
        portfolio_value = cash
        for stock, pos in list(positions.items()):
            if stock in price_data and date_str in price_data[stock].index:
                price = price_data[stock].loc[date_str]
                portfolio_value += pos['shares'] * price
                
                ret = price / pos['cost'] - 1
                
                if ret <= -0.15:
                    cash += pos['shares'] * price
                    print(f"⛔ [{date_str}] 止损 {stock} 亏损:{ret*100:.1f}%")
                    del positions[stock]
                    
                    # 止损后用备选股票替补
                    for backup in candidates:
                        if backup not in positions and backup in price_data and date_str in price_data[backup].index:
                            bp = price_data[backup].loc[date_str]
                            bs = int(portfolio_value * 0.3 / bp / 100) * 100
                            if bs > 0 and cash >= bs * bp:
                                positions[backup] = {'shares': bs, 'cost': bp}
                                cash -= bs * bp
                                print(f"🔄 [{date_str}] 替补买入 {backup} @{bp:.2f}")
                                break
                
                elif ret >= 1.0:
                    cash += pos['shares'] * price
                    print(f"🎯 [{date_str}] 止盈 {stock} 盈利:{ret*100:.1f}%")
                    del positions[stock]
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        if i % 20 == 0:
            ret_pct = (portfolio_value / initial - 1) * 100
            print(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}% 持仓:{len(positions)}只")
    
    # 最终清算
    final_value = cash
    for stock, pos in positions.items():
        if stock in price_data:
            final_value += pos['shares'] * price_data[stock].iloc[-1]
    
    total_ret = (final_value / initial - 1) * 100
    years = len(trade_days) / 250
    annual_ret = ((final_value / initial) ** (1/years) - 1) * 100 if years > 0 else 0
    
    eq_df = pd.DataFrame(equity_curve)
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
    print(f"   目标: 5.0x | 进度: {two_year/5*100:.1f}%")
    
    return {'total_return': total_ret, 'annual_return': annual_ret, 'two_year_factor': two_year}


if __name__ == "__main__":
    run_strategy()
