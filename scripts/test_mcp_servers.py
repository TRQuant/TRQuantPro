#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试MCP服务器是否正常运行
"""

import sys
import asyncio
from pathlib import Path

TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

def test_import(server_name: str, module_path: str):
    """测试MCP服务器模块导入"""
    try:
        module = __import__(module_path, fromlist=[''])
        print(f"✅ {server_name}: 导入成功")
        return True
    except Exception as e:
        print(f"❌ {server_name}: 导入失败 - {e}")
        return False

def test_knowledge_base():
    """测试知识库相关模块"""
    print("\n📚 测试知识库模块...")
    
    # 测试知识库向量索引
    try:
        from mcp_servers.knowledge_vector_index import build_vector_index
        print("✅ knowledge_vector_index: 导入成功")
    except Exception as e:
        print(f"❌ knowledge_vector_index: 导入失败 - {e}")
    
    # 测试知识库搜索
    try:
        from mcp_servers.knowledge_search_api import search
        print("✅ knowledge_search_api: 导入成功")
    except Exception as e:
        print(f"❌ knowledge_search_api: 导入失败 - {e}")
    
    # 测试混合搜索
    try:
        from mcp_servers.knowledge_hybrid_search import vector_search
        print("✅ knowledge_hybrid_search: 导入成功")
    except Exception as e:
        print(f"❌ knowledge_hybrid_search: 导入失败 - {e}")

def test_mcp_servers():
    """测试MCP服务器"""
    print("\n🔧 测试MCP服务器...")
    
    servers = [
        ("kb_server", "mcp_servers.kb_server"),
        ("unified_dev_server", "mcp_servers.unified_dev_server"),
        ("knowledge_vector_index", "mcp_servers.knowledge_vector_index"),
    ]
    
    results = []
    for name, module_path in servers:
        results.append(test_import(name, module_path))
    
    return all(results)

def main():
    print("=" * 70)
    print("🧪 MCP服务器测试")
    print("=" * 70)
    
    # 测试MCP服务器
    server_ok = test_mcp_servers()
    
    # 测试知识库模块
    test_knowledge_base()
    
    print("\n" + "=" * 70)
    if server_ok:
        print("✅ 所有MCP服务器测试通过")
    else:
        print("⚠️  部分MCP服务器测试失败，请检查依赖")
    print("=" * 70)

if __name__ == '__main__':
    main()
