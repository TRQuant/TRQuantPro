#!/usr/bin/env python3
"""
适配器架构端到端测试

测试Python端和TypeScript端的适配器通信是否正常工作
"""

import sys
import json
import asyncio
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp_servers.utils.adapters.tenbagger_adapter import get_tenbagger_adapter
from mcp_servers.utils.adapters.workflow_adapter import get_workflow_adapter


async def test_tenbagger_adapter():
    """测试十倍股适配器"""
    print("=" * 70)
    print("测试十倍股适配器")
    print("=" * 70)
    
    try:
        adapter = get_tenbagger_adapter()
        if adapter is None:
            print("❌ 适配器未初始化")
            return False
        
        print("✅ 适配器初始化成功")
        
        # 测试获取排名
        print("\n📊 测试获取排名...")
        result = await adapter.handle_get_rankings({
            "top_n": 5,
            "min_level": "A"
        })
        
        if result and result.get("success"):
            report = result.get("report", [])
            if isinstance(report, list):
                print(f"✅ 获取排名成功: {len(report)} 条记录")
            else:
                print(f"✅ 获取排名成功")
            return True
        else:
            print(f"❌ 获取排名失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_workflow_adapter():
    """测试工作流适配器"""
    print("\n" + "=" * 70)
    print("测试工作流适配器")
    print("=" * 70)
    
    try:
        adapter = get_workflow_adapter()
        if adapter is None:
            print("❌ 适配器未初始化")
            return False
        
        print("✅ 适配器初始化成功")
        
        # 测试获取步骤
        print("\n📋 测试获取步骤定义...")
        result = await adapter.handle_get_steps({})
        
        if result and result.get("success"):
            steps = result.get("steps", [])
            print(f"✅ 获取步骤成功: {len(steps)} 个步骤")
            return True
        else:
            print(f"❌ 获取步骤失败: {result.get('error', '未知错误')}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("适配器架构端到端测试")
    print("=" * 70)
    
    results = []
    
    # 测试十倍股适配器
    results.append(("十倍股适配器", await test_tenbagger_adapter()))
    
    # 测试工作流适配器
    results.append(("工作流适配器", await test_workflow_adapter()))
    
    # 汇总结果
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
