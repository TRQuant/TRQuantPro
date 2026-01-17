#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试聚宽情绪因子API
==================

测试聚宽是否提供情绪因子的直接API，或需要自己计算。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

import jqdatasdk as jq
from config.config_manager import get_config_manager

# 初始化JQData
cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])

print("=" * 80)
print("测试聚宽情绪因子API")
print("=" * 80)

# 测试1: get_factor_values (CNE5/CNE6风格因子)
print("\n1. 测试 get_factor_values (CNE5/CNE6风格因子)...")
try:
    factors = jq.get_factor_values(
        securities=['000001.XSHG'],
        factors=['size', 'beta', 'momentum'],
        end_date='2024-01-12',
        count=1
    )
    print(f"✅ get_factor_values 可用")
    print(f"   返回类型: {type(factors)}")
    if hasattr(factors, 'head'):
        print(f"   数据形状: {factors.shape}")
        print(f"   列名: {list(factors.columns)}")
except Exception as e:
    print(f"❌ get_factor_values 失败: {e}")

# 测试2: get_all_factors (获取所有因子名称)
print("\n2. 测试 get_all_factors (获取所有因子名称)...")
try:
    all_factors = jq.get_all_factors()
    print(f"✅ get_all_factors 可用")
    print(f"   因子总数: {len(all_factors) if all_factors else 0}")
    
    # 查找情绪相关因子
    if all_factors:
        emotion_keywords = ['PSY', 'ARBR', 'AR', 'BR', 'VR', 'WVAD', 'emotion', 'sentiment', '心理', '人气']
        emotion_factors = []
        for factor in all_factors:
            factor_str = str(factor).upper()
            if any(kw.upper() in factor_str for kw in emotion_keywords):
                emotion_factors.append(factor)
        
        print(f"   情绪相关因子: {len(emotion_factors)} 个")
        if emotion_factors:
            print(f"   前10个: {emotion_factors[:10]}")
        else:
            print("   ⚠️ 未找到情绪相关因子")
except Exception as e:
    print(f"❌ get_all_factors 失败: {e}")

# 测试3: get_factor_kanban_values (因子看板)
print("\n3. 测试 get_factor_kanban_values (因子看板)...")
try:
    kanban = jq.get_factor_kanban_values(
        universe='hs300',
        bt_cycle='month_3',
        model='long_only',
        category=['emotion'],
        skip_paused=False,
        commision_slippage=0
    )
    print(f"✅ get_factor_kanban_values 可用")
    print(f"   返回类型: {type(kanban)}")
    if hasattr(kanban, 'head'):
        print(f"   数据形状: {kanban.shape}")
        if not kanban.empty:
            print(f"   列名: {list(kanban.columns)}")
            print(f"   情绪因子代码示例:")
            emotion_codes = kanban[kanban['category'] == 'emotion']['code'].unique()[:10]
            for code in emotion_codes:
                print(f"     - {code}")
except Exception as e:
    print(f"❌ get_factor_kanban_values 失败: {e}")

# 测试4: 尝试用get_factor_values获取情绪因子
print("\n4. 测试用 get_factor_values 获取情绪因子...")
emotion_factor_codes = ['PSY', 'PSY_12', 'ARBR', 'AR', 'BR', 'VR', 'VR_26', 'WVAD']
for code in emotion_factor_codes:
    try:
        values = jq.get_factor_values(
            securities=['000001.XSHG'],
            factors=[code],
            end_date='2024-01-12',
            count=1
        )
        if values is not None and not values.empty:
            print(f"   ✅ {code}: 可用")
            break
    except:
        continue
else:
    print("   ❌ 未找到可用的情绪因子代码")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
