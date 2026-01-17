#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查所有知识库状态
==================

检查内容：
1. 知识库条目统计
2. 向量索引状态
3. 混合搜索功能测试
4. 各类型知识库完整性
"""

import sys
import json
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))


def check_knowledge_base() -> Dict[str, Any]:
    """检查知识库文件"""
    print("=" * 70)
    print("📚 知识库总览")
    print("=" * 70)
    
    kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
    
    if not kb_file.exists():
        return {
            "success": False,
            "error": "知识库文件不存在",
            "file": str(kb_file)
        }
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    items = kb.get('items', [])
    
    # 统计信息
    stats = {
        "total": len(items),
        "by_type": Counter(item.get('type', 'unknown') for item in items),
        "by_tag": Counter(tag for item in items for tag in item.get('tags', [])),
        "by_source": Counter(item.get('source', 'unknown')[:50] for item in items if item.get('source')),
    }
    
    print(f"总条目数: {stats['total']}")
    print()
    
    print("📊 按类型统计:")
    for type_name, count in stats['by_type'].most_common():
        print(f"  {type_name}: {count} 条")
    print()
    
    print("🏷️  热门标签（前10）:")
    for tag, count in stats['by_tag'].most_common(10):
        print(f"  {tag}: {count} 条")
    print()
    
    print("📥 来源统计（前10）:")
    for source, count in stats['by_source'].most_common(10):
        print(f"  {source[:50]}: {count} 条")
    print()
    
    return {
        "success": True,
        "stats": stats,
        "file": str(kb_file)
    }


def check_vector_index() -> Dict[str, Any]:
    """检查向量索引状态"""
    print("=" * 70)
    print("🔍 向量索引状态")
    print("=" * 70)
    
    index_dir = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "vector_index"
    index_meta_file = index_dir / "index_meta.json"
    
    if not index_meta_file.exists():
        return {
            "success": False,
            "error": "向量索引未构建",
            "index_dir": str(index_dir)
        }
    
    try:
        meta = json.loads(index_meta_file.read_text(encoding='utf-8'))
        print("✅ 向量索引已构建")
        print(f"  条目数: {meta.get('items_count', 0)}")
        print(f"  模型: {meta.get('model', 'N/A')}")
        print(f"  向量维度: {meta.get('embedding_dim', 0)}")
        print(f"  索引路径: {meta.get('index_path', 'N/A')}")
        print()
        
        # 检查ChromaDB集合
        try:
            import chromadb
            print(f"  ✅ chromadb已导入 (版本: {chromadb.__version__})")
            
            client = chromadb.PersistentClient(path=str(index_dir))
            collection = client.get_collection(name='knowledge_base')
            count = collection.count()
            
            print(f"  ✅ ChromaDB集合条目数: {count}")
            print("✅ ChromaDB集合正常")
            print()
            
            return {
                "success": True,
                "meta": meta,
                "chromadb_count": count,
                "index_dir": str(index_dir)
            }
        except ImportError as e:
            print(f"  ❌ chromadb未安装: {e}")
            return {
                "success": False,
                "error": f"chromadb未安装: {e}",
                "meta": meta
            }
        except Exception as e:
            print(f"  ⚠️  ChromaDB检查失败: {e}")
            return {
                "success": True,
                "warning": f"ChromaDB检查失败: {e}",
                "meta": meta
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"读取索引元数据失败: {e}"
        }


def test_hybrid_search() -> Dict[str, Any]:
    """测试混合搜索功能"""
    print("=" * 70)
    print("🔍 混合搜索功能测试")
    print("=" * 70)
    
    try:
        from mcp_servers.knowledge_search_api import search
        
        test_queries = [
            ("情绪因子", "情绪因子相关"),
            ("资金流向", "资金流向相关"),
            ("AKShare", "AKShare相关"),
            ("聚宽", "聚宽相关"),
            ("PTrade", "PTrade相关"),
        ]
        
        results = []
        
        for query, desc in test_queries:
            print(f"\n📋 测试查询: \"{query}\" ({desc})")
            try:
                result = search(query, limit=3, mode="hybrid")
                
                if result.get('success'):
                    items = result.get('results', [])
                    mode = result.get('mode', 'unknown')
                    print(f"   ✅ 找到 {len(items)} 条记录 (模式: {mode})")
                    
                    if items:
                        for i, item in enumerate(items[:2], 1):
                            title = item.get('title', 'N/A')
                            score = item.get('_score', 0)
                            print(f"      {i}. {title[:60]}")
                            print(f"         分数: {score:.2f}")
                    
                    results.append({
                        "query": query,
                        "desc": desc,
                        "success": True,
                        "count": len(items),
                        "mode": mode
                    })
                else:
                    print(f"   ❌ 搜索失败: {result.get('error', 'Unknown')}")
                    results.append({
                        "query": query,
                        "desc": desc,
                        "success": False,
                        "error": result.get('error', 'Unknown')
                    })
            except Exception as e:
                print(f"   ❌ 异常: {e}")
                results.append({
                    "query": query,
                    "desc": desc,
                    "success": False,
                    "error": str(e)
                })
        
        print()
        
        # 统计
        successful = sum(1 for r in results if r.get('success'))
        total = len(results)
        
        return {
            "success": successful == total,
            "total_tests": total,
            "successful_tests": successful,
            "results": results
        }
        
    except ImportError as e:
        print(f"❌ 搜索API导入失败: {e}")
        return {
            "success": False,
            "error": f"搜索API导入失败: {e}"
        }
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }


def check_kb_categories() -> Dict[str, Any]:
    """检查各类知识库的完整性"""
    print("=" * 70)
    print("📂 知识库分类检查")
    print("=" * 70)
    
    kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
    
    if not kb_file.exists():
        return {"success": False, "error": "知识库文件不存在"}
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    items = kb.get('items', [])
    
    # 按标签分类
    categories = {
        "AKShare": [item for item in items if 'AKShare' in item.get('tags', []) or 'akshare' in str(item.get('source', '')).lower()],
        "聚宽": [item for item in items if '聚宽' in item.get('tags', []) or 'JoinQuant' in item.get('tags', []) or 'JQData' in item.get('tags', [])],
        "PTrade": [item for item in items if 'PTrade' in item.get('tags', []) or 'ptrade' in str(item.get('source', '')).lower()],
        "QMT": [item for item in items if 'QMT' in item.get('tags', []) or 'qmt' in str(item.get('source', '')).lower()],
        "情绪因子": [item for item in items if '情绪因子' in item.get('title', '') or '情绪因子' in item.get('content', '')],
        "资金流向": [item for item in items if '资金流向' in item.get('title', '') or '资金流向' in item.get('content', '')],
    }
    
    print("各类知识库条目数:")
    for category, category_items in categories.items():
        print(f"  {category}: {len(category_items)} 条")
    print()
    
    return {
        "success": True,
        "categories": {k: len(v) for k, v in categories.items()}
    }


def main():
    """主函数"""
    print("=" * 70)
    print("🧪 知识库全面检查")
    print("=" * 70)
    print()
    
    # 1. 检查知识库文件
    kb_result = check_knowledge_base()
    print()
    
    # 2. 检查向量索引
    index_result = check_vector_index()
    print()
    
    # 3. 测试混合搜索
    search_result = test_hybrid_search()
    print()
    
    # 4. 检查知识库分类
    category_result = check_kb_categories()
    print()
    
    # 总结
    print("=" * 70)
    print("📊 检查总结")
    print("=" * 70)
    print(f"知识库文件: {'✅ 正常' if kb_result.get('success') else '❌ 异常'}")
    if kb_result.get('success'):
        print(f"  总条目数: {kb_result['stats']['total']}")
    
    print(f"向量索引: {'✅ 正常' if index_result.get('success') else '❌ 异常'}")
    if index_result.get('success'):
        print(f"  条目数: {index_result['meta'].get('items_count', 0)}")
        if 'chromadb_count' in index_result:
            print(f"  ChromaDB集合: {index_result['chromadb_count']} 条")
    
    print(f"混合搜索: {'✅ 正常' if search_result.get('success') else '❌ 异常'}")
    if search_result.get('success'):
        print(f"  测试通过: {search_result['successful_tests']}/{search_result['total_tests']}")
    
    print(f"知识库分类: {'✅ 正常' if category_result.get('success') else '❌ 异常'}")
    if category_result.get('success'):
        for category, count in category_result['categories'].items():
            print(f"  {category}: {count} 条")
    
    print()
    
    # 最终状态
    all_ok = (
        kb_result.get('success') and
        index_result.get('success') and
        search_result.get('success') and
        category_result.get('success')
    )
    
    if all_ok:
        print("✅ 所有知识库检查通过！")
    else:
        print("⚠️  部分检查未通过，请查看上述详细信息")
    
    print("=" * 70)


if __name__ == '__main__':
    main()
