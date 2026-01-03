#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单快速测试数据源检查
只测试核心功能，快速验证
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / 'mcp_servers'))

def test_import():
    """测试1: 导入是否正确"""
    print("测试1: 检查导入...")
    try:
        from core.data.unified_data_provider_v2 import get_data_provider_v2
        print("  ✅ get_data_provider_v2 导入成功")
        
        from workflow_9steps_server import execute_step_data_source
        print("  ✅ execute_step_data_source 导入成功")
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        return False

def test_direct_call():
    """测试2: 直接调用"""
    print("\n测试2: 直接调用数据提供者...")
    try:
        from core.data.unified_data_provider_v2 import get_data_provider_v2
        provider = get_data_provider_v2()
        health_status = provider.health_check()
        
        count = len(health_status)
        print(f"  ✅ 成功！找到 {count} 个数据源")
        for name in health_status.keys():
            print(f"     - {name}")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 数据源检查快速验证")
    print("=" * 50)
    
    r1 = test_import()
    r2 = test_direct_call()
    
    print("\n" + "=" * 50)
    if r1 and r2:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 50)




















































































