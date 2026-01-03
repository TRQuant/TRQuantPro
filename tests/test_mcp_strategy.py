#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试策略生成MCP服务器
====================
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


async def test_strategy_server():
    """测试策略服务器"""
    print("=" * 60)
    print("🐉 韬睿量化 - 策略生成MCP服务器测试")
    print("=" * 60)
    
    try:
        from strategy_template_server import TOOLS, _handle_generate, _handle_list
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:45]}...")
        
        # 测试列出模板
        print("\n📋 测试列出模板...")
        list_result = await _handle_list({})
        if list_result.get("success") or "templates" in list_result:
            templates = list_result.get("templates", [])
            print(f"  ✅ 可用模板数: {len(templates)}")
            for t in templates[:5]:
                name = t.get("name", t) if isinstance(t, dict) else t
                print(f"     • {name}")
        
        # 测试策略生成（使用正确的参数）
        print("\n💻 测试策略生成...")
        
        result = await _handle_generate({
            "name": "multi_factor",  # 模板名称
            "params": {
                "factors": ["momentum", "value"],
                "rebalance_days": 5
            },
            "platform": "joinquant"
        })
        
        if result.get("success"):
            print(f"  ✅ 策略生成成功")
            print(f"  模板: {result.get('template', 'N/A')}")
            print(f"  平台: {result.get('platform', 'N/A')}")
            code = result.get("code", "")
            if code:
                print(f"  代码行数: {len(code.splitlines())}")
                print(f"  代码预览:\n{'='*40}")
                for line in code.splitlines()[:10]:
                    print(f"  {line}")
                print(f"  ...")
        else:
            print(f"  ⚠️ 生成结果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    success = asyncio.run(test_strategy_server())
    
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    print(f"  {'✅' if success else '❌'} 策略生成测试: {'通过' if success else '失败'}")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
