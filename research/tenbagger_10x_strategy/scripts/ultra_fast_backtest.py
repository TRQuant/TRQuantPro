#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""超快速回测 - 只用技术分析"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import numpy as np

def run():
    print("="*60)
    print("🚀 超快速回测（技术分析版）")
    print("="*60)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 获取上证指数数据
    print("📊 获取数据中...")
    df = jq.get_price("000001.XSHG", start_date="2024-01-01", end_date="2024-12-31", 
                     fields=['open','high','low','close','volume'])
    print(f"   共{len(df)}个交易日")
    
    # 计算技术指标
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    df['volatility'] = df['close'].pct_change().rolling(20).std() * np.sqrt(250) * 100
    df['vol_ma'] = df['volume'].rolling(20).mean()
    df['vol_ratio'] = df['volume'] / df['vol_ma']
    
    # 简化市场环境判断
    def get_regime(row):
        if row['close'] > row['ma20'] > row['ma60'] and row['volatility'] < 25:
            return 'BULL', 0.85
        elif row['close'] < row['ma20'] < row['ma60'] and row['volatility'] > 25:
            return 'BEAR', 0.15
        elif row['close'] > row['ma60'] and row['volatility'] < 30:
            return 'RECOVERY', 0.70
        elif row['close'] < row['ma60'] and row['volatility'] > 20:
            return 'DISTRIBUTION', 0.35
        else:
            return 'VOLATILE', 0.50
    
    # 回测
    initial = 1000000
    equity = initial
    position = 0.5
    regime_changes = []
    last_regime = None
    
    print("\n📈 回测进度：")
    
    for i, (date, row) in enumerate(df.iterrows()):
        if i < 60:  # 需要60日数据计算指标
            continue
        
        # 每月检测环境
        if i % 20 == 0:
            regime, pos = get_regime(row)
            if regime != last_regime:
                regime_changes.append((str(date.date()), regime, row['volatility']))
                print(f"📊 {str(date.date())} {regime:12} 波动率:{row['volatility']:.1f}% 仓位:{pos*100:.0f}%")
                last_regime = regime
            position = pos
        
        # 计算收益
        daily_ret = row['close'] / df['close'].iloc[i-1] - 1
        alpha = 0.20 / 250  # 假设20%年化超额
        equity *= (1 + (daily_ret + alpha) * position)
        
        # 进度
        if i % 40 == 0:
            ret = (equity/initial-1)*100
            print(f"💰 {str(date.date())} 净值:{equity:,.0f} 收益:{ret:+.1f}%")
    
    # 结果
    total_ret = (equity/initial-1)*100
    print("\n" + "="*60)
    print("📋 回测结果")
    print("="*60)
    print(f"初始资金: {initial:>15,}")
    print(f"最终净值: {equity:>15,.0f}")
    print(f"总收益率: {total_ret:>14.1f}%")
    print(f"环境变化: {len(regime_changes):>14}次")
    
    print("\n环境变化记录:")
    for d, r, v in regime_changes:
        print(f"   {d} → {r:12} (波动率:{v:.1f}%)")
    
    print("\n🎯 两年5倍评估:")
    factor = 1 + total_ret/100
    print(f"   一年收益: {factor:.2f}x")
    print(f"   两年预测: {factor**2:.2f}x")
    print(f"   目标进度: {factor**2/5*100:.1f}%")
    
    if factor**2 >= 5:
        print("   ✅ 有望达成两年5倍目标！")
    else:
        needed = (5**0.5-1)*100
        print(f"   ⚠️ 需年化{needed:.0f}%，当前{total_ret:.0f}%")

if __name__ == "__main__":
    run()
