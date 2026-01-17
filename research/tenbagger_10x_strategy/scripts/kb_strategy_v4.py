#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""知识库策略V4 - 修复NaN和替补逻辑"""

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
    print("📚 知识库策略V4 - 稳健版")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    initial = 1_000_000
    max_holdings = 5  # 分散持仓
    stop_loss = -0.12  # 止损
    
    trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
    from jqdatasdk import query, valuation, indicator
    
    # 筛选高成长股票
    print("\n📊 筛选候选股...")
    q = query(
        valuation.code,
        valuation.market_cap,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year,
        indicator.roe
    ).filter(
        (valuation.code.like('688%') | valuation.code.like('300%')),
        valuation.market_cap < 200,
        valuation.market_cap > 15,
        indicator.inc_net_profit_year_on_year > 30,
        indicator.inc_revenue_year_on_year > 10,
        indicator.roe > 5
    ).limit(100)
    
    df = jq.get_fundamentals(q, date=start_date)
    print(f"   筛选出 {len(df)} 只候选股")
    
    if len(df) < 5:
        print("候选股不足，放宽条件")
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year,
            indicator.roe
        ).filter(
            (valuation.code.like('688%') | valuation.code.like('300%')),
            valuation.market_cap < 500,
            indicator.inc_net_profit_year_on_year > 20
        ).limit(100)
        df = jq.get_fundamentals(q, date=start_date)
    
    # 评分
    df['score'] = (
        df['inc_net_profit_year_on_year'].clip(0, 200).fillna(0) * 0.5 +
        df['inc_revenue_year_on_year'].clip(0, 150).fillna(0) * 0.3 +
        df['roe'].clip(0, 40).fillna(0) * 1.5
    )
    df = df.sort_values('score', ascending=False)
    
    print("\n🏆 TOP 10:")
    for _, row in df.head(10).iterrows():
        print(f"   {row['code']} 利润:{row['inc_net_profit_year_on_year']:.0f}% 营收:{row['inc_revenue_year_on_year']:.0f}% 市值:{row['market_cap']:.0f}亿")
    
    # 获取价格数据（只获取有完整数据的股票）
    candidates = df['code'].head(30).tolist()
    print(f"\n📈 加载价格...")
    
    price_data = {}
    for stock in candidates:
        try:
            prices = jq.get_price(stock, start_date=start_date, end_date=end_date, 
                                 fields=['close'], skip_paused=True)
            if prices is not None and len(prices) > 400:  # 要求几乎完整的数据
                price_data[stock] = prices['close']
        except:
            pass
    print(f"   成功加载 {len(price_data)} 只（完整数据）")
    
    if len(price_data) < 3:
        print("❌ 可用股票不足")
        return
    
    # 选择有完整数据的TOP股票
    selected = [s for s in candidates if s in price_data][:max_holdings]
    print(f"\n📊 选中: {selected}")
    
    # 回测
    cash = initial
    positions = {}
    equity_curve = []
    stopped_stocks = set()  # 记录已止损的股票，避免重复买入
    
    print("\n📊 回测:")
    print("-"*70)
    
    # 初始等权买入
    per_stock = initial * 0.95 / len(selected)
    first_day = str(trade_days[0])
    
    for stock in selected:
        if first_day in price_data[stock].index:
            price = price_data[stock].loc[first_day]
            shares = int(per_stock / price / 100) * 100
            if shares > 0:
                positions[stock] = {'shares': shares, 'cost': price}
                cash -= shares * price
                print(f"🔥 [{first_day}] 买入 {stock} @{price:.2f}")
    
    for i, td in enumerate(trade_days):
        date_str = str(td)
        
        # 计算持仓市值
        portfolio_value = cash
        valid = True
        
        for stock, pos in list(positions.items()):
            if stock in price_data:
                if date_str in price_data[stock].index:
                    price = price_data[stock].loc[date_str]
                    if pd.isna(price):
                        continue
                    
                    portfolio_value += pos['shares'] * price
                    
                    # 止损检查
                    ret = price / pos['cost'] - 1
                    if ret <= stop_loss:
                        cash += pos['shares'] * price
                        print(f"⛔ [{date_str}] 止损 {stock} 亏损:{ret*100:.1f}%")
                        stopped_stocks.add(stock)
                        del positions[stock]
                    elif ret >= 1.0:
                        cash += pos['shares'] * price
                        print(f"🎯 [{date_str}] 止盈 {stock} 盈利:{ret*100:.1f}%")
                        del positions[stock]
        
        # 安全检查
        if pd.isna(portfolio_value) or portfolio_value <= 0:
            portfolio_value = cash
            for s, p in positions.items():
                if s in price_data and date_str in price_data[s].index:
                    pv = price_data[s].loc[date_str]
                    if not pd.isna(pv):
                        portfolio_value += p['shares'] * pv
        
        # 如果持仓不足，补充买入
        if len(positions) < max_holdings and i % 20 == 0:
            for backup in candidates:
                if backup not in positions and backup not in stopped_stocks and backup in price_data:
                    if date_str in price_data[backup].index:
                        bp = price_data[backup].loc[date_str]
                        if pd.isna(bp) or bp <= 0:
                            continue
                        bs = int(portfolio_value * 0.2 / bp / 100) * 100
                        if bs > 0 and cash >= bs * bp:
                            positions[backup] = {'shares': bs, 'cost': bp}
                            cash -= bs * bp
                            print(f"🔄 [{date_str}] 补仓 {backup} @{bp:.2f}")
                            break
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        if i % 20 == 0:
            ret_pct = (portfolio_value / initial - 1) * 100
            print(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}% 持仓:{len(positions)}只")
    
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
    eq_df['equity'] = eq_df['equity'].replace([np.inf, -np.inf], np.nan).fillna(method='ffill')
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
