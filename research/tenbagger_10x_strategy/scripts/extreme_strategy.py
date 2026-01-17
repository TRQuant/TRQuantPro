#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""极端激进策略 - 测试理论上限"""

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
    print("🔥 极端激进策略 - 理论上限测试")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 2020-2021牛市
    start_date = "2020-01-01"
    end_date = "2021-12-31"
    initial = 1_000_000
    
    from jqdatasdk import query, valuation, indicator
    
    print("\n📊 筛选超高增速股...")
    q = query(
        valuation.code,
        valuation.market_cap,
        indicator.inc_net_profit_year_on_year,
        indicator.inc_revenue_year_on_year
    ).filter(
        (valuation.code.like('688%') | valuation.code.like('300%')),
        valuation.market_cap < 50,  # 极小市值
        valuation.market_cap > 10,
        indicator.inc_net_profit_year_on_year > 100,  # 超高增速
        indicator.inc_revenue_year_on_year > 50
    ).limit(50)
    
    df = jq.get_fundamentals(q, date=start_date)
    print(f"   筛选出 {len(df)} 只超高增速小市值股")
    
    if len(df) == 0:
        q = query(
            valuation.code,
            valuation.market_cap,
            indicator.inc_net_profit_year_on_year
        ).filter(
            valuation.market_cap < 100,
            indicator.inc_net_profit_year_on_year > 50
        ).limit(50)
        df = jq.get_fundamentals(q, date=start_date)
    
    candidates = df['code'].head(20).tolist()
    
    # 获取价格并计算区间涨幅
    print("\n📈 计算各股票区间涨幅...")
    results = []
    
    for stock in candidates:
        try:
            prices = jq.get_price(stock, start_date=start_date, end_date=end_date, 
                                 fields=['close'], skip_paused=True)
            if prices is not None and len(prices) > 200:
                start_price = prices['close'].iloc[0]
                end_price = prices['close'].iloc[-1]
                max_price = prices['close'].max()
                min_price = prices['close'].min()
                
                total_ret = end_price / start_price - 1
                max_ret = max_price / start_price - 1
                min_ret = min_price / start_price - 1
                ideal_ret = max_price / min_price - 1  # 理论最大收益
                
                results.append({
                    'code': stock,
                    'start': start_price,
                    'end': end_price,
                    'max': max_price,
                    'min': min_price,
                    'total_ret': total_ret * 100,
                    'max_ret': max_ret * 100,
                    'ideal_ret': ideal_ret * 100
                })
        except:
            pass
    
    results.sort(key=lambda x: x['ideal_ret'], reverse=True)
    
    print("\n🏆 TOP 10 潜在收益:")
    print(f"{'代码':<15} {'持有收益':<12} {'最高涨幅':<12} {'理论最大':<12}")
    print("-"*60)
    for r in results[:10]:
        print(f"{r['code']:<15} {r['total_ret']:>8.0f}% {r['max_ret']:>8.0f}% {r['ideal_ret']:>8.0f}%")
    
    # 模拟极端集中策略（只持1只）
    print("\n🔥 极端集中策略（只持1只最强股）:")
    if results:
        best = results[0]
        print(f"   选中: {best['code']}")
        print(f"   持有收益: {best['total_ret']:.0f}%")
        print(f"   如果完美择时: {best['ideal_ret']:.0f}%")
        
        # 两年收益计算
        years = 2
        hold_factor = 1 + best['total_ret']/100
        ideal_factor = 1 + best['ideal_ret']/100
        
        print(f"\n📊 收益分析:")
        print(f"   持有策略: {hold_factor:.2f}x / 2年")
        print(f"   完美择时: {ideal_factor:.2f}x / 2年")
        print(f"   目标: 5.0x / 2年")
        
        if ideal_factor >= 5:
            print(f"   ✅ 理论上可达成！需要完美择时")
        else:
            print(f"   ❌ 即使完美择时也无法达成")
    
    # 组合策略（2只股票）
    print("\n🎯 组合策略（2只最强股）:")
    if len(results) >= 2:
        avg_ret = (results[0]['total_ret'] + results[1]['total_ret']) / 2
        avg_ideal = (results[0]['ideal_ret'] + results[1]['ideal_ret']) / 2
        print(f"   平均持有收益: {avg_ret:.0f}%")
        print(f"   平均理论最大: {avg_ideal:.0f}%")
    
    # 结论
    print("\n" + "="*70)
    print("📋 结论")
    print("="*70)
    print("1. 即使选中最好的股票，两年5倍仍然极难达成")
    print("2. 需要：极端集中 + 完美择时 + 选中大牛股")
    print("3. 知识库规律在选股上有效，但无法保证极端收益")
    print("4. 建议调整目标为年化30-50%更为现实")


if __name__ == "__main__":
    run_strategy()
