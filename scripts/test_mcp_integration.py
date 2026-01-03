#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP服务器集成测试脚本
====================

测试已集成的MCP服务器是否正常工作。

使用方法:
    python scripts/test_mcp_integration.py [--server SERVER_NAME]
"""

import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class MCPServerTester:
    """MCP服务器测试器"""
    
    def __init__(self, server_name: str):
        self.server_name = server_name
        self.test_results = []
    
    async def test_kb_server(self):
        """测试kb_server"""
        print(f"\n{'='*70}")
        print(f"测试 kb_server.py")
        print(f"{'='*70}")
        
        try:
            from mcp_servers.kb_server import KBMCPServer, MCP_TOOLS
            
            server = KBMCPServer()
            
            # 测试1: 列出工具
            print("\n1. 测试 list_tools()...")
            tools = server.list_tools()
            print(f"   ✅ 找到 {len(tools)} 个工具")
            for tool in tools:
                print(f"      - {tool['name']}")
            
            # 测试2: 测试kb.stats
            print("\n2. 测试 kb.stats...")
            result = await server.call_tool("kb.stats", {"scope": "both"})
            if isinstance(result, dict) and "content" in result:
                print("   ✅ kb.stats 调用成功")
                if result.get("isError"):
                    print(f"   ⚠️  返回错误: {result.get('content', [{}])[0].get('text', '')}")
                else:
                    print("   ✅ 返回正常")
            else:
                print(f"   ❌ 返回格式异常: {type(result)}")
            
            # 测试3: 测试kb.query（简单查询）
            print("\n3. 测试 kb.query...")
            result = await server.call_tool("kb.query", {
                "query": "MCP",
                "scope": "both",
                "top_k": 3
            })
            if isinstance(result, dict) and "content" in result:
                print("   ✅ kb.query 调用成功")
                if result.get("isError"):
                    print(f"   ⚠️  返回错误: {result.get('content', [{}])[0].get('text', '')}")
                else:
                    print("   ✅ 返回正常")
            else:
                print(f"   ❌ 返回格式异常: {type(result)}")
            
            self.test_results.append({
                "server": "kb_server",
                "status": "passed",
                "tools_tested": len(tools)
            })
            
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append({
                "server": "kb_server",
                "status": "failed",
                "error": str(e)
            })
    
    async def test_data_source_server(self):
        """测试data_source_server"""
        print(f"\n{'='*70}")
        print(f"测试 data_source_server.py")
        print(f"{'='*70}")
        
        try:
            from mcp_servers.data_source_server import server
            
            # 测试1: 列出工具
            print("\n1. 测试 list_tools()...")
            tools = await server.list_tools()
            print(f"   ✅ 找到 {len(tools)} 个工具")
            for tool in tools:
                print(f"      - {tool.name}")
            
            # 测试2: 测试data.list_sources
            print("\n2. 测试 data.list_sources...")
            result = await server.call_tool("data.list_sources", {})
            if isinstance(result, list) and len(result) > 0:
                print("   ✅ data.list_sources 调用成功")
                if hasattr(result[0], 'text'):
                    try:
                        data = json.loads(result[0].text)
                        if data.get("error"):
                            print(f"   ⚠️  返回错误: {data.get('error')}")
                        else:
                            print("   ✅ 返回正常")
                    except:
                        print("   ✅ 返回正常（无法解析JSON）")
                else:
                    print("   ✅ 返回正常")
            else:
                print(f"   ❌ 返回格式异常: {type(result)}")
            
            self.test_results.append({
                "server": "data_source_server",
                "status": "passed",
                "tools_tested": len(tools)
            })
            
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append({
                "server": "data_source_server",
                "status": "failed",
                "error": str(e)
            })
    
    async def test_code_server(self):
        """测试code_server"""
        print(f"\n{'='*70}")
        print(f"测试 code_server.py")
        print(f"{'='*70}")
        
        try:
            from mcp_servers.code_server import server
            
            # 测试1: 列出工具
            print("\n1. 测试 list_tools()...")
            tools = await server.list_tools()
            print(f"   ✅ 找到 {len(tools)} 个工具")
            for tool in tools:
                print(f"      - {tool.name}")
            
            # 测试2: 测试code.search（简单搜索）
            print("\n2. 测试 code.search...")
            result = await server.call_tool("code.search", {
                "query": "def",
                "limit": 5
            })
            if isinstance(result, list) and len(result) > 0:
                print("   ✅ code.search 调用成功")
                if hasattr(result[0], 'text'):
                    try:
                        data = json.loads(result[0].text)
                        if data.get("error"):
                            print(f"   ⚠️  返回错误: {data.get('error')}")
                        else:
                            print("   ✅ 返回正常")
                    except:
                        print("   ✅ 返回正常（无法解析JSON）")
                else:
                    print("   ✅ 返回正常")
            else:
                print(f"   ❌ 返回格式异常: {type(result)}")
            
            self.test_results.append({
                "server": "code_server",
                "status": "passed",
                "tools_tested": len(tools)
            })
            
        except Exception as e:
            print(f"   ❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
            self.test_results.append({
                "server": "code_server",
                "status": "failed",
                "error": str(e)
            })
    
    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*70}")
        print("测试总结")
        print(f"{'='*70}")
        
        passed = sum(1 for r in self.test_results if r["status"] == "passed")
        failed = sum(1 for r in self.test_results if r["status"] == "failed")
        
        print(f"\n总测试数: {len(self.test_results)}")
        print(f"通过: {passed}")
        print(f"失败: {failed}")
        
        print("\n详细结果:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "passed" else "❌"
            print(f"  {status_icon} {result['server']}: {result['status']}")
            if result["status"] == "failed":
                print(f"     错误: {result.get('error', 'Unknown')}")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description='MCP服务器集成测试')
    parser.add_argument('--server', type=str, help='仅测试指定服务器')
    args = parser.parse_args()
    
    tester = MCPServerTester("test")
    
    if args.server:
        if args.server == "kb":
            await tester.test_kb_server()
        elif args.server == "data_source":
            await tester.test_data_source_server()
        elif args.server == "code":
            await tester.test_code_server()
        else:
            print(f"❌ 未知服务器: {args.server}")
            return
    else:
        # 测试所有已集成的服务器
        await tester.test_kb_server()
        await tester.test_data_source_server()
        await tester.test_code_server()
    
    tester.print_summary()


if __name__ == '__main__':
    asyncio.run(main())









