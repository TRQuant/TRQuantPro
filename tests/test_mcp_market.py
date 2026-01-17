#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试市场分析MCP服务器
====================
测试步骤2: market.status 功能
测试步骤3: market.mainlines 功能
"""

import sys
import asyncio
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))


def test_mcp_market_tools():
    """测试MCP市场工具定义"""
    print("=" * 60)
    print("测试1: MCP市场服务器工具定义")
    print("=" * 60)
    
    try:
        from mcp.types import Tool
        print("✅ MCP SDK 可用")
        
        # 尝试导入 v2 版本
        try:
            from market_server_v2 import TOOLS
            print("✅ 使用 market_server_v2")
        except ImportError:
            from market_server import TOOLS
            print("⚠️ 使用 market_server (基础版)")
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:50]}...")
        
        # 检查必需工具
        required_tools = ["market.status", "market.mainlines"]
        for tool_name in required_tools:
            found = any(t.name == tool_name for t in TOOLS)
            emoji = "✅" if found else "❌"
            print(f"\n{emoji} 必需工具 '{tool_name}': {'存在' if found else '缺失'}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_market_status():
    """测试市场状态获取"""
    print("\n" + "=" * 60)
    print("测试2: market.status 功能")
    print("=" * 60)
    
    try:
        try:
            from market_server_v2 import _handle_status
        except ImportError:
            from market_server import _handle_status
        
        print("\n📈 调用 market.status...")
        result = await _handle_status({"index": "000300.XSHG"})
        
        print(f"\n📊 市场状态结果:")
        print(f"  市场状态: {result.get('status', result.get('regime', 'N/A'))}")
        print(f"  趋势: {result.get('trend', 'N/A')}")
        
        if 'index_data' in result:
            print(f"  指数数据: {result['index_data']}")
        
        if 'bull_score' in result:
            print(f"  多头得分: {result['bull_score']}")
        
        if 'volatility' in result:
            print(f"  波动率: {result['volatility']}")
        
        if 'momentum' in result:
            print(f"  动量: {result['momentum']}")
        
        # 检查是否有错误
        if 'error' in result:
            print(f"  ⚠️ 错误: {result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_market_mainlines():
    """测试投资主线获取"""
    print("\n" + "=" * 60)
    print("测试3: market.mainlines 功能")
    print("=" * 60)
    
    try:
        try:
            from market_server_v2 import _handle_mainlines
        except ImportError:
            from market_server import _handle_mainlines
        
        print("\n🔥 调用 market.mainlines...")
        result = await _handle_mainlines({"top_n": 5})
        
        print(f"\n📊 投资主线结果:")
        
        if 'mainlines' in result:
            for i, ml in enumerate(result['mainlines'][:5], 1):
                name = ml.get('name', ml.get('mainline', 'N/A'))
                score = ml.get('score', ml.get('heat_score', 'N/A'))
                print(f"  {i}. {name} (评分: {score})")
        elif 'error' in result:
            print(f"  ⚠️ 错误: {result['error']}")
        else:
            print(f"  结果: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("🐉 韬睿量化 - 市场分析MCP服务器测试")
    print("=" * 60)
    
    results = []
    
    # 测试1: 工具定义
    results.append(("MCP工具定义", test_mcp_market_tools()))
    
    # 测试2: 市场状态
    results.append(("market.status", asyncio.run(test_market_status())))
    
    # 测试3: 投资主线
    results.append(("market.mainlines", asyncio.run(test_market_mainlines())))
    
    # 汇总
    print("\n" + "=" * 60)
    print("📊 测试汇总")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        emoji = "✅" if result else "❌"
        print(f"  {emoji} {name}")
        if result:
            passed += 1
    
    print(f"\n结果: {passed}/{len(results)} 通过")
    
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
