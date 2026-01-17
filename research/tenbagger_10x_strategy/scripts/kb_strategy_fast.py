#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速版知识库策略 - 一次性缓存所有数据"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def run_kb_strategy():
    print("="*70)
    print("📚 知识库策略快速版 - 两年5倍目标")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    initial = 1_000_000
    
    # === 第一步：批量筛选高增速小市值股票 ===
    print("\n📊 第一步：批量筛选候选股...")
    
    from jqdatasdk import query, valuation, indicator
    
    # 筛选查询
    q = query(
        valuation.code,
        valuation.pe_ratio,
        valuation.market_cap,
        indicator.roe,
        indicator.gross_profit_margin,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year
    ).filter(
        # 科创板+创业板
        (valuation.code.like('688%') | valuation.code.like('300%')),
        # 小市值
        valuation.market_cap < 1e10,  # <100亿
        valuation.market_cap > 1.5e9,   # >15亿
        # 高增速
        indicator.inc_net_profit_year_on_year > 50,  # 利润>50%
        indicator.inc_revenue_year_on_year > 30,      # 营收>30%
        # 盈利
        indicator.roe > 5,
        # PE合理
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 100
    ).limit(50)
    
    df = jq.get_fundamentals(q, date=start_date)
    print(f"   筛选出 {len(df)} 只符合条件的股票")
    
    if len(df) == 0:
        print("❌ 没有符合条件的股票，放宽条件重试...")
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.market_cap,
            indicator.roe,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year
        ).filter(
            (valuation.code.like('688%') | valuation.code.like('300%')),
            valuation.market_cap < 2e10,
            indicator.inc_net_profit_year_on_year > 30,
            indicator.roe > 0
        ).limit(100)
        df = jq.get_fundamentals(q, date=start_date)
        print(f"   放宽后筛选出 {len(df)} 只股票")
    
    if len(df) == 0:
        print("❌ 仍无符合条件股票")
        return
    
    # 评分排序
    df['score'] = (
        df['inc_net_profit_year_on_year'].clip(0, 200) * 0.4 +
        df['inc_revenue_year_on_year'].clip(0, 100) * 0.3 +
        df['roe'].clip(0, 30) * 2 +
        (100 - df['market_cap']/1e8).clip(0, 100) * 0.3
    )
    df = df.sort_values('score', ascending=False)
    
    # 显示候选
    print("\n🏆 TOP 10 候选股:")
    print(f"{'代码':<15} {'利润增速':<10} {'营收增速':<10} {'ROE':<8} {'市值(亿)':<10} {'评分':<8}")
    print("-"*70)
    for _, row in df.head(10).iterrows():
        print(f"{row['code']:<15} {row['inc_net_profit_year_on_year']:>6.0f}% {row['inc_revenue_year_on_year']:>6.0f}% {row['roe']:>6.1f}% {row['market_cap']/1e8:>8.0f} {row['score']:>6.0f}")
    
    # === 第二步：获取TOP股票的价格数据 ===
    top_stocks = df['code'].head(10).tolist()
    print(f"\n📈 第二步：加载TOP {len(top_stocks)} 股票价格...")
    
    price_data = {}
    for stock in top_stocks:
        try:
            prices = jq.get_price(stock, start_date=start_date, end_date=end_date, fields=['close'])
            if prices is not None and len(prices) > 0:
                price_data[stock] = prices['close']
        except:
            pass
    print(f"   成功加载 {len(price_data)} 只")
    
    if not price_data:
        print("❌ 无价格数据")
        return
    
    # === 第三步：模拟交易 ===
    print("\n📊 第三步：回测交易...")
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    
    # 选择评分最高的2只
    selected = [s for s in top_stocks[:2] if s in price_data]
    
    if not selected:
        print("❌ 选中股票无价格数据")
        return
    
    print(f"   选中: {selected}")
    
    # 简化交易：等权持有，12%止损，80%止盈
    cash = initial
    positions = {}
    
    # 初始买入
    per_stock = initial * 0.95 / len(selected)
    first_day = str(trade_days[0])
    
    for stock in selected:
        if first_day in price_data[stock].index:
            price = price_data[stock].loc[first_day]
            shares = int(per_stock / price / 100) * 100
            if shares > 0:
                positions[stock] = {'shares': shares, 'cost': price}
                cash -= shares * price
                print(f"   初始买入 {stock} @{price:.2f} x{shares}")
    
    # 每日更新
    equity_curve = []
    for i, td in enumerate(trade_days):
        date_str = str(td)
        
        portfolio_value = cash
        for stock, pos in list(positions.items()):
            if stock in price_data and date_str in price_data[stock].index:
                price = price_data[stock].loc[date_str]
                value = pos['shares'] * price
                portfolio_value += value
                
                # 止损/止盈
                ret = price / pos['cost'] - 1
                
                if ret <= -0.12:
                    cash += pos['shares'] * price
                    print(f"⛔ [{date_str}] 止损 {stock} 亏损:{ret*100:.1f}%")
                    del positions[stock]
                elif ret >= 0.80:
                    cash += pos['shares'] * price
                    print(f"🎯 [{date_str}] 止盈 {stock} 盈利:{ret*100:.1f}%")
                    del positions[stock]
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        # 月度进度
        if i % 20 == 0:
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
    
    # 最大回撤
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
    
    # 两年5倍评估
    factor = 1 + total_ret/100
    two_year = factor ** (2/years) if years > 0 else factor
    
    print("\n🎯 两年5倍目标评估:")
    print(f"   {years:.1f}年倍数: {factor:.2f}x")
    print(f"   两年预测: {two_year:.2f}x")
    print(f"   目标: 5.0x | 进度: {two_year/5*100:.1f}%")


if __name__ == "__main__":
    run_kb_strategy()
