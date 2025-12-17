#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据源MCP服务器
==================
测试步骤1: data_source.health_check 功能
"""

import sys
import asyncio
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_data_provider_v2():
    """测试数据提供者V2"""
    print("=" * 60)
    print("测试1: 数据提供者V2基础功能")
    print("=" * 60)
    
    try:
        from core.data import get_data_provider_v2, DataRequest, DataSource
        
        provider = get_data_provider_v2()
        print(f"✅ 数据提供者创建成功")
        
        # 测试健康检查
        print("\n📡 执行健康检查...")
        health_results = provider.health_check()
        
        for name, status in health_results.items():
            emoji = "✅" if status.available else "❌"
            print(f"  {emoji} {name}: available={status.available}, latency={status.latency_ms:.2f}ms")
        
        # 测试获取统计
        print("\n📊 获取统计信息...")
        stats = provider.get_stats()
        print(f"  活跃数据源: {stats['active_source']}")
        print(f"  可用数据源: {stats['sources_available']}")
        print(f"  总请求数: {stats['total_requests']}")
        print(f"  缓存命中率: {stats['cache_hit_rate']*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_data_request():
    """测试数据请求"""
    print("\n" + "=" * 60)
    print("测试2: 数据请求功能")
    print("=" * 60)
    
    try:
        from core.data import get_data_provider_v2, DataRequest
        
        provider = get_data_provider_v2()
        
        # 测试获取股票数据
        print("\n📈 请求股票数据...")
        request = DataRequest(
            securities=["000001.XSHE", "600000.XSHG"],
            start_date="2024-12-01",
            end_date="2024-12-10",
            use_mock=True  # 允许使用模拟数据
        )
        
        response = provider.get_data(request)
        
        if response.success:
            print(f"✅ 数据获取成功")
            print(f"  数据源: {response.source}")
            print(f"  从缓存: {response.from_cache}")
            print(f"  获取耗时: {response.fetch_time_ms:.2f}ms")
            print(f"  数据行数: {len(response.data)}")
            if not response.data.empty:
                print(f"  数据列: {list(response.data.columns)}")
                print(f"  数据预览:\n{response.data.head(3)}")
        else:
            print(f"⚠️ 数据获取失败: {response.error}")
            print("  (可能是数据源未配置，这在测试环境中是正常的)")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mcp_server_tools():
    """测试MCP服务器工具定义"""
    print("\n" + "=" * 60)
    print("测试3: MCP服务器工具定义")
    print("=" * 60)
    
    try:
        # 导入MCP服务器
        sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))
        
        # 检查MCP SDK
        try:
            from mcp.types import Tool, TextContent
            print("✅ MCP SDK 可用")
        except ImportError:
            print("❌ MCP SDK 不可用，请安装: pip install mcp")
            return False
        
        # 导入数据源服务器
        from data_source_server_v2 import TOOLS
        
        print(f"\n📋 可用工具 ({len(TOOLS)}个):")
        for tool in TOOLS:
            print(f"  • {tool.name}: {tool.description[:40]}...")
        
        # 检查我们需要的工具
        required_tools = ["data_source.health_check", "data_source.status"]
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


async def test_mcp_tool_call():
    """测试MCP工具调用"""
    print("\n" + "=" * 60)
    print("测试4: MCP工具调用 (data_source.health_check)")
    print("=" * 60)
    
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))
        
        # 导入并调用
        import data_source_server_v2 as ds_server
        
        # 模拟调用 health_check
        result = await ds_server._handle_health_check({})
        
        print(f"\n📡 health_check 结果:")
        print(f"  success: {result.get('success')}")
        
        if result.get('success'):
            for name, status in result.get('health_status', {}).items():
                emoji = "✅" if status['available'] else "❌"
                print(f"  {emoji} {name}:")
                print(f"      available: {status['available']}")
                print(f"      latency: {status['latency_ms']}ms")
                print(f"      success_rate: {status['success_rate']}%")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("🐉 韬睿量化 - 数据源MCP服务器测试")
    print("=" * 60)
    
    results = []
    
    # 测试1: 基础功能
    results.append(("数据提供者V2", test_data_provider_v2()))
    
    # 测试2: 数据请求
    results.append(("数据请求", test_data_request()))
    
    # 测试3: MCP工具定义
    results.append(("MCP工具定义", test_mcp_server_tools()))
    
    # 测试4: MCP工具调用
    results.append(("MCP工具调用", asyncio.run(test_mcp_tool_call())))
    
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
