#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试剩余MCP服务器（步骤7-9）
===========================
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


async def test_backtest_server():
    """步骤7: 回测服务器"""
    print("\n" + "=" * 60)
    print("步骤7: 回测验证 (backtest_server)")
    print("=" * 60)
    
    try:
        from backtest_server import TOOLS
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS[:6]:
            print(f"  • {tool.name}: {tool.description[:40]}...")
        if len(TOOLS) > 6:
            print(f"  ... 还有 {len(TOOLS)-6} 个工具")
        
        # 检查必需工具
        tool_names = [t.name for t in TOOLS]
        required = ["backtest.quick", "backtest.bullettrade"]
        for req in required:
            found = req in tool_names
            emoji = "✅" if found else "⚠️"
            print(f"\n{emoji} 工具 '{req}': {'存在' if found else '不存在'}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def test_optimizer_server():
    """步骤8: 优化服务器"""
    print("\n" + "=" * 60)
    print("步骤8: 策略优化 (optimizer_server)")
    print("=" * 60)
    
    try:
        from optimizer_server import TOOLS
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:40]}...")
        
        # 检查必需工具
        tool_names = [t.name for t in TOOLS]
        required = ["optimizer.grid_search", "optimizer.optuna"]
        for req in required:
            found = req in tool_names
            emoji = "✅" if found else "⚠️"
            print(f"\n{emoji} 工具 '{req}': {'存在' if found else '不存在'}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def test_report_server():
    """步骤9: 报告服务器"""
    print("\n" + "=" * 60)
    print("步骤9: 报告生成 (report_server)")
    print("=" * 60)
    
    try:
        from report_server import TOOLS
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:40]}...")
        
        # 检查必需工具
        tool_names = [t.name for t in TOOLS]
        required = ["report.generate", "report.list"]
        for req in required:
            found = req in tool_names
            emoji = "✅" if found else "⚠️"
            print(f"\n{emoji} 工具 '{req}': {'存在' if found else '不存在'}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


async def main():
    print("=" * 60)
    print("🐉 韬睿量化 - MCP服务器测试（步骤7-9）")
    print("=" * 60)
    
    results = []
    
    results.append(("步骤7: 回测验证", await test_backtest_server()))
    results.append(("步骤8: 策略优化", await test_optimizer_server()))
    results.append(("步骤9: 报告生成", await test_report_server()))
    
    print("\n" + "=" * 60)
    print("📊 测试汇总")
    print("=" * 60)
    
    for name, result in results:
        emoji = "✅" if result else "❌"
        print(f"  {emoji} {name}")
    
    passed = sum(1 for _, r in results if r)
    print(f"\n结果: {passed}/{len(results)} 通过")
    
    return passed == len(results)


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
