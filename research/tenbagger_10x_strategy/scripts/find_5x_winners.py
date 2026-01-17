#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
寻找历史上两年内涨幅超过5倍的股票
分析它们的共同特征，构建预测模型
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def find_5x_stocks():
    print("="*70)
    print("🔍 寻找历史5倍股案例")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 检查多个时间窗口
    windows = [
        # (start, end, description)
        ("2019-01-01", "2021-01-01", "2019-2020牛市"),
        ("2020-03-01", "2022-03-01", "疫情后反弹"),
        ("2022-10-01", "2024-10-01", "近两年"),
    ]
    
    all_winners = []
    
    for start, end, desc in windows:
        print(f"\n📅 检查 {desc} ({start} ~ {end})")
        
        # 获取股票池
        try:
            stocks = list(jq.get_all_securities('stock', date=start).index)[:500]
        except:
            stocks = list(jq.get_index_stocks('000300.XSHG'))
        
        winners = []
        
        # 批量检查
        for stock in stocks[:200]:  # 检查前200只
            try:
                df = jq.get_price(stock, start_date=start, end_date=end, 
                                 fields=['close'], skip_paused=True)
                if df is not None and len(df) >= 100:
                    start_price = df['close'].iloc[0]
                    end_price = df['close'].iloc[-1]
                    max_price = df['close'].max()
                    
                    total_ret = end_price / start_price - 1
                    max_ret = max_price / start_price - 1
                    
                    if max_ret >= 4.0:  # 最高涨幅>=400%（5倍）
                        winners.append({
                            'code': stock,
                            'period': desc,
                            'start': start,
                            'end': end,
                            'total_return': total_ret * 100,
                            'max_return': max_ret * 100,
                            'factor': 1 + max_ret
                        })
            except:
                pass
        
        print(f"   找到 {len(winners)} 只5倍股")
        all_winners.extend(winners)
    
    if not all_winners:
        print("\n❌ 未找到5倍股案例")
        return
    
    # 排序
    all_winners.sort(key=lambda x: x['max_return'], reverse=True)
    
    print("\n" + "="*70)
    print("🏆 5倍股排行榜（最高涨幅）")
    print("="*70)
    print(f"{'代码':<15} {'时期':<15} {'最高涨幅':<12} {'倍数':<8}")
    print("-"*70)
    
    for w in all_winners[:20]:
        print(f"{w['code']:<15} {w['period']:<15} {w['max_return']:>8.0f}% {w['factor']:>6.1f}x")
    
    # 分析最佳案例的买入时机
    if all_winners:
        best = all_winners[0]
        print(f"\n🔥 最佳案例分析: {best['code']}")
        print(f"   时期: {best['period']}")
        print(f"   最高涨幅: {best['max_return']:.0f}%")
        print(f"   倍数: {best['factor']:.1f}x")
        
        # 获取详细数据
        df = jq.get_price(best['code'], start_date=best['start'], end_date=best['end'],
                         fields=['close', 'volume'])
        if df is not None:
            # 计算最佳买入点
            cummax = df['close'].cummax()
            drawdown = df['close'] / cummax - 1
            
            # 找到最低点后的反弹
            min_idx = df['close'].idxmin()
            print(f"   最低点: {min_idx.date()} @{df['close'].loc[min_idx]:.2f}")
            
            # 找到突破20日均线的点
            df['ma20'] = df['close'].rolling(20).mean()
            breakout = df[df['close'] > df['ma20']].index
            if len(breakout) > 0:
                first_breakout = breakout[0]
                print(f"   首次突破MA20: {first_breakout.date()} @{df['close'].loc[first_breakout]:.2f}")
    
    return all_winners


if __name__ == "__main__":
    find_5x_stocks()
