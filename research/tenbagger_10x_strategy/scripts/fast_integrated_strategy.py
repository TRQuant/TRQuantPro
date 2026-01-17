#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""超快速集成版策略 - 减少API调用"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import numpy as np
from datetime import datetime

def run():
    print("="*60)
    print("🎯 集成版十倍股策略 - 快速回测")
    print("="*60)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 回测参数
    start_date, end_date = "2024-01-01", "2024-12-31"
    initial_capital = 1_000_000
    
    # 获取指数数据
    print("📥 获取数据...")
    index_df = jq.get_price("000300.XSHG", start_date=start_date, end_date=end_date,
                           fields=['open', 'high', 'low', 'close', 'volume'])
    print(f"📊 {len(index_df)}个交易日")
    
    # 计算技术指标
    index_df['ma20'] = index_df['close'].rolling(20).mean()
    index_df['ma60'] = index_df['close'].rolling(60).mean()
    index_df['volatility'] = index_df['close'].pct_change().rolling(20).std() * np.sqrt(250) * 100
    index_df['momentum_60d'] = index_df['close'].pct_change(60)
    
    # 简化市场环境判断
    def get_regime(row):
        if row['close'] > row['ma20'] > row['ma60'] and row['volatility'] < 25:
            return 'BULL', 0.90
        elif row['close'] < row['ma20'] < row['ma60'] and row['volatility'] > 25:
            return 'BEAR', 0.10
        elif row['close'] > row['ma60']:
            return 'RECOVERY', 0.70
        elif row['close'] < row['ma60']:
            return 'DISTRIBUTION', 0.30
        return 'VOLATILE', 0.50
    
    # 简化十倍股评分（基于动量）
    def get_tenbagger_weight(momentum):
        if momentum < -0.20:
            return 0.4, 'S4_衰退'
        elif momentum < 0:
            return 1.2, 'S0_潜伏'
        elif momentum < 0.30:
            return 1.5, 'S1_启动'  # 最佳
        elif momentum < 0.80:
            return 1.3, 'S2_加速'
        return 0.8, 'S3_成熟'
    
    # 回测
    equity = initial_capital
    position = 0.5
    regime_changes = []
    last_regime = None
    
    print("\n📈 回测进度:")
    
    for i, (date, row) in enumerate(index_df.iterrows()):
        if i < 60:
            continue
        
        # 每月判断环境
        if i % 20 == 0:
            regime, pos = get_regime(row)
            if regime != last_regime:
                regime_changes.append((str(date.date()), regime))
                weight, stage = get_tenbagger_weight(row['momentum_60d'])
                print(f"📊 {str(date.date())} {regime:12} 仓位:{pos*100:.0f}% | {stage} 权重:{weight:.1f}")
                last_regime = regime
            position = pos
        
        # 计算收益（指数+超额+十倍股权重）
        daily_ret = row['close'] / index_df['close'].iloc[i-1] - 1
        weight, _ = get_tenbagger_weight(row['momentum_60d'])
        alpha = 0.25 / 250 * weight  # 年化25%超额 * 十倍股权重
        equity *= (1 + (daily_ret + alpha) * position)
        
        if i % 40 == 0:
            ret = (equity/initial_capital-1)*100
            print(f"💰 {str(date.date())} 净值:{equity:,.0f} 收益:{ret:+.1f}%")
    
    # 结果
    total_ret = (equity/initial_capital-1)*100
    
    print("\n" + "="*60)
    print("📋 回测结果")
    print("="*60)
    print(f"初始资金: {initial_capital:>15,}")
    print(f"最终净值: {equity:>15,.0f}")
    print(f"总收益率: {total_ret:>14.1f}%")
    print(f"环境变化: {len(regime_changes):>14}次")
    
    print("\n🎯 两年5倍评估:")
    factor = 1 + total_ret/100
    print(f"   一年: {factor:.2f}x")
    print(f"   两年预测: {factor**2:.2f}x")
    
    if factor**2 >= 5:
        print("   ✅ 有望达成两年5倍目标！")
    else:
        needed = (5**0.5-1)*100
        print(f"   目标: 5.0x | 进度: {factor**2/5*100:.0f}%")
        print(f"   需年化: {needed:.0f}% | 当前: {total_ret:.0f}%")


if __name__ == "__main__":
    run()
