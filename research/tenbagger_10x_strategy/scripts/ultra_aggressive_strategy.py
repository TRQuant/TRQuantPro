#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
超快速激进版策略 - 预加载数据，减少API调用
目标：两年5倍
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import pandas as pd
import numpy as np
from datetime import datetime

def run_strategy():
    print("="*70)
    print("🔥 超激进版策略 - 两年5倍目标")
    print("="*70)
    
    import jqdatasdk as jq
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print(f"✅ JQData: {config['username']}")
    
    # 参数
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    initial = 1_000_000
    
    # 获取科创板50指数数据（高成长代表）
    print("📥 获取数据...")
    kcb50 = jq.get_price("000688.XSHG", start_date=start_date, end_date=end_date,
                        fields=['open', 'high', 'low', 'close', 'volume'])
    
    # 创业板指数
    cyb = jq.get_price("399006.XSHE", start_date=start_date, end_date=end_date,
                      fields=['close'])
    
    # 合成高成长组合：70%科创+30%创业板
    combined = kcb50.copy()
    combined['growth_index'] = kcb50['close'] * 0.7 + cyb['close'] * 0.3
    
    # 计算技术指标
    combined['ma10'] = combined['growth_index'].rolling(10).mean()
    combined['ma20'] = combined['growth_index'].rolling(20).mean()
    combined['ma60'] = combined['growth_index'].rolling(60).mean()
    combined['momentum_20'] = combined['growth_index'].pct_change(20)
    combined['momentum_60'] = combined['growth_index'].pct_change(60)
    combined['volatility'] = combined['growth_index'].pct_change().rolling(20).std() * np.sqrt(250) * 100
    
    # 计算RSI
    delta = combined['growth_index'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    combined['rsi'] = 100 - (100 / (1 + rs))
    
    print(f"📊 回测期间: {start_date} ~ {end_date}")
    print(f"   共 {len(combined)} 个交易日")
    
    # 激进策略：趋势跟踪 + 动量 + RSI
    equity = initial
    position = 0  # 0=空仓, 1=满仓, 2=2倍杠杆
    entry_price = 0
    max_equity = initial
    trades = []
    
    print("\n📈 交易信号:")
    
    for i, (date, row) in enumerate(combined.iterrows()):
        if i < 60:
            continue
        
        date_str = str(date.date())
        price = row['growth_index']
        
        # 计算信号
        trend_up = row['ma10'] > row['ma20'] > row['ma60']
        trend_down = row['ma10'] < row['ma20'] < row['ma60']
        strong_momentum = row['momentum_60'] > 0.20
        weak_momentum = row['momentum_60'] < -0.15
        rsi_oversold = row['rsi'] < 35
        rsi_overbought = row['rsi'] > 70
        low_vol = row['volatility'] < 30
        
        # 交易逻辑
        if position == 0:
            # 空仓时寻找买入机会
            if trend_up and strong_momentum and low_vol:
                position = 2  # 2倍杠杆
                entry_price = price
                print(f"🔥 [{date_str}] 2倍杠杆买入 @{price:.2f} | 动量:{row['momentum_60']*100:.0f}%")
                trades.append({'date': date_str, 'action': 'buy_2x', 'price': price})
            elif trend_up or (rsi_oversold and row['momentum_20'] > 0):
                position = 1  # 满仓
                entry_price = price
                print(f"🔼 [{date_str}] 满仓买入 @{price:.2f} | RSI:{row['rsi']:.0f}")
                trades.append({'date': date_str, 'action': 'buy', 'price': price})
        
        elif position >= 1:
            # 持仓时检查卖出条件
            ret = price / entry_price - 1
            
            # 止损
            if ret < -0.12:
                print(f"⛔ [{date_str}] 止损卖出 @{price:.2f} | 亏损:{ret*100:.1f}%")
                equity *= (1 + ret * position)
                position = 0
                trades.append({'date': date_str, 'action': 'stop_loss', 'price': price, 'ret': ret})
            
            # 趋势反转
            elif trend_down and weak_momentum:
                print(f"📉 [{date_str}] 趋势反转卖出 @{price:.2f} | 收益:{ret*100:.1f}%")
                equity *= (1 + ret * position)
                position = 0
                trades.append({'date': date_str, 'action': 'trend_sell', 'price': price, 'ret': ret})
            
            # 止盈（100%+）
            elif ret > 1.0:
                print(f"🎯 [{date_str}] 止盈卖出 @{price:.2f} | 收益:{ret*100:.1f}%")
                equity *= (1 + ret * position)
                position = 0
                trades.append({'date': date_str, 'action': 'take_profit', 'price': price, 'ret': ret})
            
            # 更新最大权益
            current_equity = equity * (1 + ret * position) if position > 0 else equity
            max_equity = max(max_equity, current_equity)
        
        # 每月进度
        if i % 20 == 0:
            if position > 0:
                ret = price / entry_price - 1
                current = equity * (1 + ret * position)
            else:
                current = equity
            total_ret = (current / initial - 1) * 100
            print(f"💰 [{date_str}] 净值:{current:,.0f} 收益:{total_ret:+.1f}% 仓位:{position}x")
    
    # 最终结算
    if position > 0:
        final_price = combined['growth_index'].iloc[-1]
        final_ret = final_price / entry_price - 1
        equity *= (1 + final_ret * position)
    
    # 结果
    total_ret = (equity / initial - 1) * 100
    years = len(combined) / 250
    annual_ret = ((equity / initial) ** (1/years) - 1) * 100 if years > 0 else total_ret
    
    print("\n" + "="*70)
    print("📋 回测结果")
    print("="*70)
    print(f"初始资金:     {initial:>15,}")
    print(f"最终净值:     {equity:>15,.0f}")
    print(f"总收益率:     {total_ret:>14.1f}%")
    print(f"年化收益率:   {annual_ret:>14.1f}%")
    print(f"交易次数:     {len(trades):>15}")
    
    # 两年5倍评估
    factor = 1 + total_ret/100
    two_year = factor ** (2/years) if years > 0 else factor
    
    print("\n🎯 两年5倍目标评估:")
    print(f"   {years:.1f}年实际: {factor:.2f}x")
    print(f"   两年预测: {two_year:.2f}x")
    print(f"   目标: 5.0x")
    
    if two_year >= 5:
        print("   ✅ 达到两年5倍目标！🎉")
    else:
        print(f"   进度: {two_year/5*100:.1f}%")
        needed = (5 ** (1/2) - 1) * 100
        print(f"   需要年化: {needed:.0f}% | 当前年化: {annual_ret:.0f}%")


if __name__ == "__main__":
    run_strategy()
