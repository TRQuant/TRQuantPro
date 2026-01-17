#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库搜索功能 - 完整测试

测试各种搜索场景，验证知识库调用功能

Author: TRQuant Team
Date: 2026-01-01
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from mcp_servers.unified_dev_server import knowledge_search, knowledge_get
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False
    sys.exit(1)


def test_search(query: str, description: str, limit: int = 10):
    """测试搜索功能"""
    print(f"\n{'='*70}")
    print(f"🔍 测试: {description}")
    print(f"查询: {query}")
    print(f"{'='*70}")
    
    try:
        result = knowledge_search(query=query, limit=limit)
        
        if result.get('success'):
            items = result.get('results', [])
            total = result.get('total', 0)
            
            print(f"✅ 搜索成功")
            print(f"   找到: {len(items)} 个结果（共 {total} 个）")
            
            if items:
                print(f"\n前 {min(5, len(items))} 个结果:")
                for i, item in enumerate(items[:5], 1):
                    title = item.get('title', 'N/A')
                    source = item.get('source') or item.get('url') or 'N/A'
                    tags = item.get('tags', [])
                    content_preview = item.get('content', '')[:100] if item.get('content') else ''
                    
                    print(f"\n  {i}. {title[:60]}")
                    if source and source != 'N/A':
                        print(f"     URL: {str(source)[:80]}")
                    print(f"     标签: {', '.join(tags[:5])}")
                    if content_preview:
                        print(f"     内容预览: {content_preview}...")
            else:
                print("   ⚠️ 未找到结果")
        else:
            print(f"❌ 搜索失败: {result.get('error', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_get(knowledge_id: str, description: str):
    """测试获取详情功能"""
    print(f"\n{'='*70}")
    print(f"📄 测试: {description}")
    print(f"ID: {knowledge_id}")
    print(f"{'='*70}")
    
    try:
        result = knowledge_get(knowledge_id=knowledge_id)
        
        if result.get('success'):
            item = result.get('item', {})
            print(f"✅ 获取成功")
            print(f"   标题: {item.get('title', 'N/A')}")
            source = item.get('source') or item.get('url') or ''
            if source:
                print(f"   URL: {str(source)[:80]}")
            tags = item.get('tags', [])
            if tags:
                print(f"   标签: {', '.join(tags[:10])}")
            content = item.get('content', '')
            if content:
                print(f"   内容长度: {len(content)} 字符")
                print(f"   内容预览: {content[:200]}...")
        else:
            print(f"❌ 获取失败: {result.get('error', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """主函数"""
    print("=" * 70)
    print("知识库搜索功能 - 完整测试")
    print("=" * 70)
    
    if not KB_AVAILABLE:
        print("❌ 知识库工具不可用")
        return
    
    # 测试用例列表
    test_cases = [
        # 基础搜索
        ("JQData", "基础搜索 - JQData"),
        ("聚宽", "中文搜索 - 聚宽"),
        ("API", "英文关键词 - API"),
        
        # 因子相关
        ("Alpha", "Alpha因子搜索"),
        ("Alpha101", "Alpha101因子搜索"),
        ("Alpha191", "Alpha191因子搜索"),
        ("因子", "因子关键词搜索"),
        ("CNE5", "CNE5风格因子搜索"),
        ("CNE6", "CNE6风格因子搜索"),
        ("风险模型", "风险模型搜索"),
        
        # 数据相关
        ("股票", "股票数据搜索"),
        ("指数", "指数数据搜索"),
        ("宏观", "宏观数据搜索"),
        ("行业", "行业数据搜索"),
        ("财务", "财务数据搜索"),
        ("历史", "历史数据搜索"),
        ("分钟", "分钟数据搜索"),
        ("tick", "Tick数据搜索"),
        
        # 功能相关
        ("交易", "交易函数搜索"),
        ("下单", "下单函数搜索"),
        ("回测", "回测相关搜索"),
        ("策略", "策略相关搜索"),
        ("筛选", "筛选函数搜索"),
        
        # 具体API函数
        ("get_price", "get_price函数搜索"),
        ("get_fundamentals", "get_fundamentals函数搜索"),
        ("get_all_factors", "get_all_factors函数搜索"),
        
        # 组合搜索（注意：知识库搜索是简单的字符串匹配，不支持AND逻辑）
        # 组合关键词需要分别在内容中查找，这里改为单个关键词
        ("因子构建", "因子构建关键词搜索"),
        ("JQData API", "组合关键词 - JQData API"),
    ]
    
    # 执行测试
    search_results = []
    for query, description in test_cases:
        result = test_search(query, description, limit=5)
        if result:
            search_results.append((query, result))
    
    # 总结
    print("\n" + "=" * 70)
    print("测试总结")
    print("=" * 70)
    
    successful_searches = sum(1 for _, r in search_results if r and r.get('success') and r.get('total', 0) > 0)
    total_tests = len(test_cases)
    
    print(f"总测试数: {total_tests}")
    print(f"成功找到结果: {successful_searches}")
    print(f"成功率: {successful_searches/total_tests*100:.1f}%")
    
    # 找到结果最多的查询
    if search_results:
        results_with_items = [(q, r) for q, r in search_results if r and r.get('total', 0) > 0]
        if results_with_items:
            results_with_items.sort(key=lambda x: x[1].get('total', 0), reverse=True)
            print(f"\n找到结果最多的查询:")
            for query, result in results_with_items[:5]:
                print(f"  - {query}: {result.get('total', 0)} 个结果")
    
    # 测试获取详情（如果有结果）
    if search_results:
        # 找到第一个有结果的搜索
        for query, result in search_results:
            if result and result.get('results'):
                first_item = result['results'][0]
                knowledge_id = first_item.get('id') or first_item.get('knowledge_id')
                if knowledge_id:
                    print(f"\n{'='*70}")
                    print("测试获取详情功能")
                    print(f"{'='*70}")
                    test_get(knowledge_id, f"获取第一个搜索结果详情 ({query})")
                    break
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)


if __name__ == "__main__":
    main()

