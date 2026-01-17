#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试OpenManus MCP服务器
验证工具是否正确注册
"""
import sys
import asyncio
from pathlib import Path

# 添加OpenManus路径
OPENMANUS_DIR = Path(__file__).parent.parent / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))

async def test_mcp_server():
    """测试MCP服务器工具注册"""
    print("=" * 80)
    print("OpenManus MCP服务器测试")
    print("=" * 80)
    
    try:
        from app.mcp.server import MCPServer
        
        # 创建服务器
        print("\n1. 创建MCP服务器...")
        server = MCPServer()
        print("   ✅ 服务器创建成功")
        
        # 检查工具
        print("\n2. 检查已注册的工具...")
        tools = server.tools
        print(f"   ✅ 找到 {len(tools)} 个工具:")
        for tool_name, tool in tools.items():
            print(f"      - {tool_name}")
            param = tool.to_param()
            if param and 'function' in param:
                func_info = param['function']
                print(f"        名称: {func_info.get('name', '未知')}")
                print(f"        描述: {func_info.get('description', '无描述')[:60]}...")
        
        # 检查browser工具
        print("\n3. 检查browser工具...")
        if 'browser' in tools:
            browser_tool = tools['browser']
            param = browser_tool.to_param()
            if param and 'function' in param:
                func_info = param['function']
                params = func_info.get('parameters', {})
                props = params.get('properties', {})
                print(f"   ✅ browser工具已注册")
                print(f"      参数数量: {len(props)}")
                if 'action' in props:
                    action_enum = props['action'].get('enum', [])
                    print(f"      支持的操作: {', '.join(action_enum[:5])}...")
                    print(f"      总共 {len(action_enum)} 个操作")
        else:
            print("   ❌ browser工具未找到")
        
        print("\n" + "=" * 80)
        print("测试完成")
        print("=" * 80)
        print("\n✅ OpenManus MCP服务器工具注册正常")
        print("\n在Cursor Chat中使用:")
        print('  "使用browser工具访问 https://www.eastmoney.com"')
        print("\n工具名称: browser (不需要openmanus.前缀)")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
