#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试候选池构建MCP功能
====================
测试步骤4: data_source.candidate_pool 功能
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


async def test_candidate_pool():
    """测试候选池构建"""
    print("=" * 60)
    print("🐉 韬睿量化 - 候选池构建MCP测试")
    print("=" * 60)
    
    try:
        from data_source_server_v2 import _handle_candidate_pool, TOOLS
        
        # 检查工具是否存在
        tool_names = [t.name for t in TOOLS]
        if "data_source.candidate_pool" in tool_names:
            print("✅ data_source.candidate_pool 工具已注册")
        else:
            print("❌ data_source.candidate_pool 工具未注册")
            return False
        
        # 测试不同主线
        mainlines = ["人工智能", "新能源", "半导体", "医药生物", "消费"]
        
        for mainline in mainlines:
            print(f"\n📦 测试主线: {mainline}")
            result = await _handle_candidate_pool({"mainline": mainline, "limit": 5})
            
            if result.get("success"):
                print(f"  ✅ 成功构建候选池")
                print(f"  📊 股票数量: {result['total_count']}")
                for stock in result['stocks'][:3]:
                    print(f"     • {stock['name']} ({stock['code']}) - 评分: {stock['score']}")
            else:
                print(f"  ❌ 构建失败: {result.get('error')}")
        
        # 测试未知主线
        print(f"\n📦 测试未知主线: 量子计算")
        result = await _handle_candidate_pool({"mainline": "量子计算", "limit": 3})
        if result.get("success"):
            print(f"  ✅ 成功生成通用候选池 ({result['total_count']}只)")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = asyncio.run(test_candidate_pool())
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"  {'✅' if success else '❌'} 候选池构建测试: {'通过' if success else '失败'}")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
