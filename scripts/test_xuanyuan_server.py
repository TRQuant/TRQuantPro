#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试轩辕剑灵MCP服务器

用于验证服务器是否正常工作
"""

import sys
import json
import asyncio
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

async def test_server():
    """测试服务器功能"""
    print("=" * 60)
    print("测试轩辕剑灵MCP服务器")
    print("=" * 60)
    print()
    
    # 测试1: 导入服务器
    print("测试1: 导入服务器模块...")
    try:
        from mcp_servers.xuanyuan_server import TOOLS, handle_tool
        print(f"✅ 导入成功，工具数量: {len(TOOLS)}")
    except Exception as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 测试2: 列出所有工具
    print("\n测试2: 列出所有工具...")
    for i, tool in enumerate(TOOLS, 1):
        print(f"  {i:2d}. {tool.name}: {tool.description[:50]}...")
    
    # 测试3: 测试提示词模板列表
    print("\n测试3: 测试 xuanyuan.prompt.templates.list...")
    try:
        result = await handle_tool("xuanyuan.prompt.templates.list", {})
        result_text = result[0].text if result else ""
        result_data = json.loads(result_text) if result_text else {}
        if result_data.get("success"):
            print(f"✅ 测试通过，模板数量: {result_data.get('count', 0)}")
        else:
            print(f"⚠️  返回: {result_data}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试4: 测试错误分析
    print("\n测试4: 测试 xuanyuan.error.analyze...")
    try:
        result = await handle_tool("xuanyuan.error.analyze", {
            "error_message": "NameError: name 'x' is not defined"
        })
        result_text = result[0].text if result else ""
        result_data = json.loads(result_text) if result_text else {}
        if result_data.get("success"):
            print(f"✅ 测试通过，错误ID: {result_data.get('error_id')}")
            print(f"   错误分类: {result_data.get('error_category')}")
        else:
            print(f"⚠️  返回: {result_data}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试5: 测试命令解释
    print("\n测试5: 测试 xuanyuan.command.explain...")
    try:
        result = await handle_tool("xuanyuan.command.explain", {
            "command": "ls -lah"
        })
        result_text = result[0].text if result else ""
        result_data = json.loads(result_text) if result_text else {}
        if result_data.get("success"):
            print(f"✅ 测试通过")
            print(f"   解释: {result_data.get('explanation', '')[:80]}...")
        else:
            print(f"⚠️  返回: {result_data}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试6: 测试记忆保存
    print("\n测试6: 测试 xuanyuan.memory.save_context...")
    try:
        result = await handle_tool("xuanyuan.memory.save_context", {
            "key": "test_key",
            "value": "测试值",
            "tags": ["test"]
        })
        result_text = result[0].text if result else ""
        result_data = json.loads(result_text) if result_text else {}
        if result_data.get("success"):
            print(f"✅ 测试通过，键: {result_data.get('key')}")
        else:
            print(f"⚠️  返回: {result_data}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
    return True

if __name__ == "__main__":
    asyncio.run(test_server())

