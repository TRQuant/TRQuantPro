#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试知识库构建流程

用于验证知识库构建脚本是否正常工作
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_mcp_tools():
    """测试MCP工具是否可用"""
    print("=" * 70)
    print("测试1: MCP工具可用性")
    print("=" * 70)
    
    try:
        from core.mcp.client import MCPClient
        client = MCPClient()
        print("✅ MCPClient可用")
        return True
    except Exception as e:
        print(f"❌ MCPClient不可用: {e}")
        return False


def test_direct_functions():
    """测试直接函数是否可用"""
    print("\n" + "=" * 70)
    print("测试2: 直接函数可用性")
    print("=" * 70)
    
    try:
        from mcp_servers.unified_dev_server import (
            knowledge_add,
            crawler_fetch,
            crawler_selenium_fetch,
        )
        print("✅ 直接函数可用")
        return True
    except Exception as e:
        print(f"❌ 直接函数不可用: {e}")
        return False


def test_crawler_fetch():
    """测试爬虫工具"""
    print("\n" + "=" * 70)
    print("测试3: 爬虫工具测试")
    print("=" * 70)
    
    test_url = "https://akshare.akfamily.xyz/"
    
    # 测试MCP工具
    try:
        from core.mcp.client import MCPClient
        client = MCPClient()
        result = client.call(
            tool_name='crawler.fetch',
            arguments={
                'url': test_url,
                'extract_text': True,
                'extract_links': False
            },
            timeout=30.0
        )
        
        if result.success:
            print(f"✅ MCP爬虫工具成功")
            data = result.data
            if isinstance(data, str):
                import json
                data = json.loads(data)
            if data.get('text'):
                print(f"   文本长度: {len(data.get('text', ''))} 字符")
            return True
        else:
            print(f"❌ MCP爬虫工具失败: {result.error}")
    except Exception as e:
        print(f"⚠️ MCP爬虫工具异常: {e}")
    
    # 测试直接函数
    try:
        from mcp_servers.unified_dev_server import crawler_fetch
        result = crawler_fetch(test_url, extract_text=True, extract_links=False)
        if result.get('success'):
            print(f"✅ 直接函数爬虫成功")
            if result.get('text'):
                print(f"   文本长度: {len(result.get('text', ''))} 字符")
            return True
        else:
            print(f"❌ 直接函数爬虫失败: {result.get('error')}")
    except Exception as e:
        print(f"⚠️ 直接函数爬虫异常: {e}")
    
    return False


def test_knowledge_add():
    """测试知识库添加功能"""
    print("\n" + "=" * 70)
    print("测试4: 知识库添加功能")
    print("=" * 70)
    
    test_title = "测试知识条目"
    test_content = "这是一个测试知识条目，用于验证知识库添加功能是否正常工作。"
    
    # 测试MCP工具
    try:
        from core.mcp.client import MCPClient
        client = MCPClient()
        result = client.call(
            tool_name='knowledge.add',
            arguments={
                'title': test_title,
                'content': test_content,
                'type': 'reference',
                'tags': ['测试', 'AKShare'],
                'source': 'https://test.example.com'
            },
            timeout=30.0
        )
        
        if result.success:
            data = result.data
            if isinstance(data, str):
                import json
                data = json.loads(data)
            if data.get('success') or data.get('knowledge_id'):
                kb_id = data.get('knowledge_id') or data.get('id', 'unknown')
                print(f"✅ MCP知识库工具成功 (ID: {kb_id})")
                return True
            else:
                print(f"❌ MCP知识库工具返回失败: {data}")
        else:
            print(f"❌ MCP知识库工具失败: {result.error}")
    except Exception as e:
        print(f"⚠️ MCP知识库工具异常: {e}")
    
    # 测试直接函数
    try:
        from mcp_servers.unified_dev_server import knowledge_add
        result = knowledge_add(
            title=test_title,
            content=test_content,
            type='reference',
            tags=['测试', 'AKShare'],
            source='https://test.example.com'
        )
        if result.get('success') or result.get('knowledge_id'):
            kb_id = result.get('knowledge_id') or result.get('id', 'unknown')
            print(f"✅ 直接函数知识库成功 (ID: {kb_id})")
            return True
        else:
            print(f"❌ 直接函数知识库失败: {result.get('error')}")
    except Exception as e:
        print(f"⚠️ 直接函数知识库异常: {e}")
    
    return False


def main():
    """主函数"""
    print("\n" + "=" * 70)
    print("知识库构建流程测试")
    print("=" * 70)
    
    results = {
        'mcp_tools': test_mcp_tools(),
        'direct_functions': test_direct_functions(),
        'crawler': test_crawler_fetch(),
        'knowledge': test_knowledge_add(),
    }
    
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n✅ 所有测试通过！可以开始构建知识库。")
    else:
        print("\n⚠️ 部分测试失败，请检查相关工具和依赖。")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
