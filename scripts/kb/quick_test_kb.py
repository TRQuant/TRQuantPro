#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库快速测试脚本
==================

快速测试知识库的核心功能
"""

import sys
import json
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_search
from core.mcp.client import MCPClient


def test_kb_basic():
    """基础测试：知识库文件完整性"""
    print("=" * 70)
    print("📊 知识库基础测试")
    print("=" * 70)
    print()
    
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    
    if not kb_file.exists():
        print("❌ 知识库文件不存在")
        return False
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        items = kb.get('items', [])
        print(f"✅ 知识库文件存在")
        print(f"   总条目数: {len(items)}条")
        
        # 检查质量指标
        has_reliability = sum(1 for i in items if '可靠性评级' in i.get('content', ''))
        has_conclusion = sum(1 for i in items if '## 结论' in i.get('content', '') or '### 结论' in i.get('content', ''))
        
        print(f"   可靠性标注: {has_reliability}条 ({has_reliability/len(items)*100:.1f}%)")
        print(f"   结论部分: {has_conclusion}条 ({has_conclusion/len(items)*100:.1f}%)")
        
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        return False


def test_kb_search():
    """测试搜索功能"""
    print()
    print("=" * 70)
    print("🔍 知识库搜索功能测试")
    print("=" * 70)
    print()
    
    test_queries = [
        "资金流向",
        "情绪因子",
        "主升期策略",
        "BulletTrade",
    ]
    
    success_count = 0
    for query in test_queries:
        print(f"📋 搜索: \"{query}\"")
        try:
            result = knowledge_search(query, limit=3)
            
            if result and isinstance(result, dict):
                items = result.get('items', []) or result.get('results', [])
                if items:
                    print(f"   ✅ 找到 {len(items)} 条记录")
                    for i, item in enumerate(items[:2], 1):
                        title = item.get('title', 'Unknown')[:50]
                        print(f"      {i}. {title}")
                    success_count += 1
                else:
                    print(f"   ⚠️  未找到结果")
            else:
                print(f"   ⚠️  返回格式异常")
        except Exception as e:
            print(f"   ❌ 搜索失败: {e}")
        print()
    
    print(f"✅ 搜索测试: {success_count}/{len(test_queries)} 成功")
    return success_count == len(test_queries)


def test_mcp_client():
    """测试MCP客户端"""
    print()
    print("=" * 70)
    print("🔧 MCP客户端测试")
    print("=" * 70)
    print()
    
    try:
        client = MCPClient()
        print("✅ MCP客户端初始化成功")
        
        # 测试搜索
        result = client.call(
            tool_name='knowledge.search',
            arguments={'query': '资金流向', 'limit': 3},
            timeout=30.0
        )
        
        if result.success:
            print("✅ MCP工具调用成功")
            data = result.data
            if isinstance(data, str):
                import json
                data = json.loads(data)
            
            items = data.get('items', []) or data.get('results', [])
            if items:
                print(f"   ✅ 找到 {len(items)} 条记录")
                return True
            else:
                print(f"   ⚠️  未找到结果")
                return False
        else:
            print(f"❌ MCP工具调用失败: {result.error}")
            return False
    except Exception as e:
        print(f"❌ MCP客户端测试失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 知识库快速测试")
    print("=" * 70)
    print()
    
    results = []
    
    # 测试1: 基础测试
    results.append(("基础测试", test_kb_basic()))
    
    # 测试2: 搜索功能
    results.append(("搜索功能", test_kb_search()))
    
    # 测试3: MCP客户端
    results.append(("MCP客户端", test_mcp_client()))
    
    # 总结
    print()
    print("=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print()
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print()
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查")
    print("=" * 70)


if __name__ == '__main__':
    main()
