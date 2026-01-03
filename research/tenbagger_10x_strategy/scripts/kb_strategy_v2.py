#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""知识库策略V2 - 修复止损后重新买入"""

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
    print("📚 知识库策略V2 - 动态轮动版")
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
    
    # 预加载大池价格
    print("\n📈 预加载股票池价格...")
    from jqdatasdk import query, valuation, indicator
    
    # 获取科创板+创业板所有股票
    all_stocks = list(jq.get_all_securities('stock', date=start_date).index)
    growth_stocks = [s for s in all_stocks if s.startswith('688') or s.startswith('300')][:200]
    
    price_data = {}
    for stock in growth_stocks:
        try:
            df = jq.get_price(stock, start_date=start_date, end_date=end_date, fields=['close'])
            if df is not None and len(df) > 100:
                price_data[stock] = df['close']
        except:
            pass
    print(f"   加载 {len(price_data)} 只股票")
    
    def screen_stocks(date: str) -> list:
        """每次筛选TOP股票"""
        q = query(
            valuation.code,
            valuation.pe_ratio,
            valuation.market_cap,
            indicator.inc_net_profit_year_on_year,
            indicator.inc_revenue_year_on_year,
            indicator.roe
        ).filter(
            (valuation.code.like('688%') | valuation.code.like('300%')),
            valuation.market_cap < 1.5e10,  # <150亿
            valuation.market_cap > 1e9,     # >10亿
            indicator.inc_net_profit_year_on_year > 30,  # 利润>30%
            indicator.inc_revenue_year_on_year > 10,     # 营收>10%（必须正增长）
            indicator.roe > 5,
            valuation.pe_ratio > 0,
            valuation.pe_ratio < 100
        ).limit(50)
        
        df = jq.get_fundamentals(q, date=date)
        
        if df is None or len(df) == 0:
            return []
        
        # 评分
        df['score'] = (
            df['inc_net_profit_year_on_year'].clip(0, 150) * 0.5 +
            df['inc_revenue_year_on_year'].clip(0, 100) * 0.3 +
            df['roe'].clip(0, 30) * 1.5 +
            (150 - df['market_cap']/1e8).clip(0, 100) * 0.2
        )
        
        # 只选有价格数据的
        df = df[df['code'].isin(price_data.keys())]
        df = df.sort_values('score', ascending=False)
        
        return df['code'].head(max_holdings * 2).tolist()
    
    # 回测状态
    cash = initial
    positions = {}
    equity_curve = []
    rebalance_interval = 20  # 每20天轮动
    
    print("\n📊 回测交易...")
    print("-"*70)
    
    for i, td in enumerate(trade_days):
        date_str = str(td)
        
        # 计算持仓市值
        portfolio_value = cash
        for stock, pos in list(positions.items()):
            if stock in price_data and date_str in price_data[stock].index:
                price = price_data[stock].loc[date_str]
                portfolio_value += pos['shares'] * price
                
                # 止损/止盈
                ret = price / pos['cost'] - 1
                
                if ret <= -0.12:
                    cash += pos['shares'] * price
                    logger.info(f"⛔ [{date_str}] 止损 {stock} @{price:.2f} 亏损:{ret*100:.1f}%")
                    del positions[stock]
                
                elif ret >= 1.0:
                    cash += pos['shares'] * price
                    logger.info(f"🎯 [{date_str}] 止盈 {stock} @{price:.2f} 盈利:{ret*100:.1f}%")
                    del positions[stock]
        
        # 定期轮动或空仓时重新选股
        if i % rebalance_interval == 0 or len(positions) < max_holdings:
            candidates = screen_stocks(date_str)
            
            if candidates and len(positions) < max_holdings:
                # 清仓不在候选中的
                for stock in list(positions.keys()):
                    if stock not in candidates:
                        if stock in price_data and date_str in price_data[stock].index:
                            price = price_data[stock].loc[date_str]
                            ret = price / positions[stock]['cost'] - 1
                            cash += positions[stock]['shares'] * price
                            if ret > 0:
                                logger.info(f"📤 [{date_str}] 轮动卖出 {stock} 盈利:{ret*100:.1f}%")
                            else:
                                logger.info(f"📤 [{date_str}] 轮动卖出 {stock} 亏损:{ret*100:.1f}%")
                        del positions[stock]
                
                # 买入新股
                available_slots = max_holdings - len(positions)
                if available_slots > 0:
                    per_stock = (portfolio_value * 0.95 / max_holdings)
                    for stock in candidates[:available_slots]:
                        if stock not in positions and stock in price_data:
                            if date_str in price_data[stock].index:
                                price = price_data[stock].loc[date_str]
                                shares = int(per_stock / price / 100) * 100
                                if shares > 0 and cash >= shares * price:
                                    positions[stock] = {'shares': shares, 'cost': price}
                                    cash -= shares * price
                                    logger.info(f"🔥 [{date_str}] 买入 {stock} @{price:.2f} x{shares}")
        
        equity_curve.append({'date': date_str, 'equity': portfolio_value})
        
        # 月度进度
        if i % 20 == 0:
            ret_pct = (portfolio_value / initial - 1) * 100
            logger.info(f"💰 [{date_str}] 净值:{portfolio_value:,.0f} 收益:{ret_pct:+.1f}% 持仓:{len(positions)}只")
    
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
    
    if two_year >= 5:
        print("   ✅ 达到两年5倍目标！")


if __name__ == "__main__":
    run_strategy()
