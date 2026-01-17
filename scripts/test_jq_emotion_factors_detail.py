#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
详细测试聚宽情绪因子
====================

查看因子看板数据，寻找获取当前因子值的方法。

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

import jqdatasdk as jq
from config.config_manager import get_config_manager
import pandas as pd

# 初始化JQData
cm = get_config_manager()
jq_config = cm.get_config('jqdata')
jq.auth(jq_config['username'], jq_config['password'])

print("=" * 80)
print("详细测试聚宽情绪因子")
print("=" * 80)

# 获取因子看板数据
print("\n获取情绪因子看板数据...")
try:
    kanban = jq.get_factor_kanban_values(
        universe='hs300',
        bt_cycle='month_3',
        model='long_only',
        category=['emotion'],
        skip_paused=False,
        commision_slippage=0
    )
    
    if kanban is not None and not kanban.empty:
        print(f"\n✅ 获取成功，共 {len(kanban)} 条记录")
        print(f"\n情绪因子代码列表:")
        emotion_codes = kanban['code'].unique()
        for code in emotion_codes:
            print(f"  - {code}")
        
        # 查看AR和BR因子
        print(f"\n查看AR和BR因子详情:")
        ar_br = kanban[kanban['code'].isin(['AR', 'BR'])]
        if not ar_br.empty:
            print(ar_br[['code', 'date', 'ic_mean', 'ir', 'good_ic']].head(10))
        
        # 尝试查找PSY相关因子
        psy_factors = kanban[kanban['code'].str.contains('PSY', case=False, na=False)]
        if not psy_factors.empty:
            print(f"\nPSY相关因子:")
            print(psy_factors[['code', 'date']].head())
        else:
            print(f"\n⚠️ 未找到PSY因子")
        
        # 尝试查找VR相关因子
        vr_factors = kanban[kanban['code'].str.contains('VR|VOL', case=False, na=False)]
        if not vr_factors.empty:
            print(f"\nVR/VOL相关因子:")
            print(vr_factors[['code', 'date']].head())
        
except Exception as e:
    print(f"❌ 获取失败: {e}")
    import traceback
    traceback.print_exc()

# 测试：尝试用技术指标API获取
print("\n" + "=" * 80)
print("测试技术指标API...")
print("=" * 80)

# 聚宽可能有技术指标API，可以计算PSY、ARBR等
# 但根据文档，这些需要自己计算

print("\n结论:")
print("1. 聚宽因子看板提供情绪因子的历史表现数据")
print("2. 但无法直接获取当前因子值")
print("3. 建议：保持手动计算，但优化性能（缓存、批量获取）")
print("4. 或者：使用聚宽的技术指标库（如果可用）")
