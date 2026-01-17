#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识库搜索统一API
================
封装所有搜索逻辑，对外提供简单接口

架构：
    用户查询
        ↓
    search() 入口函数
        ↓
    ├── 1. 基础关键词搜索
    ├── 2. 增强评分 (knowledge_search_enhanced)
    └── 3. 混合检索 (knowledge_hybrid_search)
        ↓
    返回结果 {"success": True, "mode": "hybrid|keyword|basic", "results": [...]}
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# 项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
KNOWLEDGE_DIR = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge"


def _load_knowledge_base() -> List[Dict]:
    """加载知识库"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    if not kb_file.exists():
        logger.warning(f"知识库文件不存在: {kb_file}")
        return []
    
    try:
        kb = json.loads(kb_file.read_text(encoding='utf-8'))
        return kb.get("items", [])
    except Exception as e:
        logger.error(f"加载知识库失败: {e}")
        return []


def _basic_keyword_search(items: List[Dict], query: str, type_filter: str = None) -> List[Dict]:
    """
    基础关键词搜索
    
    Args:
        items: 知识库条目
        query: 查询字符串
        type_filter: 类型过滤
        
    Returns:
        匹配的条目列表（包含_score）
    """
    query_lower = query.lower()
    results = []
    
    for item in items:
        # 类型过滤
        if type_filter and item.get("type") != type_filter:
            continue
        
        # 计算基础分数
        score = 0
        
        # 标题匹配
        title = item.get("title", "").lower()
        if query_lower in title:
            score += 10
        
        # 内容匹配
        content = item.get("content", "").lower()
        if query_lower in content:
            score += 5
        
        # 标签匹配
        for tag in item.get("tags", []):
            if query_lower in tag.lower():
                score += 3
        
        if score > 0:
            results.append({**item, "_score": score})
    
    return results


def search(
    query: str, 
    type_filter: str = None, 
    limit: int = 10,
    mode: str = "auto"
) -> Dict[str, Any]:
    """
    知识库搜索统一接口
    
    Args:
        query: 查询字符串
        type_filter: 类型过滤（可选）
        limit: 返回结果数量
        mode: 搜索模式
            - "auto": 自动选择最佳模式（默认）
            - "hybrid": 强制混合检索
            - "keyword": 仅关键词检索
            - "basic": 基础搜索
            
    Returns:
        {
            "success": True/False,
            "query": str,
            "type": str,
            "mode": "hybrid|keyword|basic",
            "results": [...],
            "total": int,
            "error": str (仅失败时)
        }
    """
    try:
        # 加载知识库
        items = _load_knowledge_base()
        if not items:
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "basic",
                "results": [],
                "total": 0,
                "message": "知识库为空"
            }
        
        # Step 1: 基础关键词搜索
        keyword_results = _basic_keyword_search(items, query, type_filter)
        
        # 如果强制基础模式，直接返回
        if mode == "basic":
            keyword_results.sort(key=lambda x: x["_score"], reverse=True)
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "basic",
                "results": keyword_results[:limit],
                "total": len(keyword_results)
            }
        
        # Step 2: 增强评分
        try:
            from mcp_servers.knowledge_search_enhanced import enhance_search_results
            enhanced_results = enhance_search_results(
                items=keyword_results,
                query=query,
                exact_match_boost=10.0,
                code_match_boost=8.0,
                tag_match_boost=5.0,
                title_match_boost=3.0,
                content_match_boost=1.0
            )
            enhanced_results.sort(key=lambda x: x["_score"], reverse=True)
        except ImportError as e:
            logger.debug(f"增强搜索模块不可用: {e}")
            enhanced_results = keyword_results
            enhanced_results.sort(key=lambda x: x["_score"], reverse=True)
        
        # 如果强制关键词模式，返回增强结果
        if mode == "keyword":
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "keyword",
                "results": enhanced_results[:limit],
                "total": len(enhanced_results)
            }
        
        # Step 3: 混合检索（auto 或 hybrid 模式）
        try:
            from mcp_servers.knowledge_hybrid_search import hybrid_search
            final_results = hybrid_search(
                query=query,
                keyword_results=enhanced_results,
                vector_limit=20,
                final_limit=limit
            )
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "hybrid",
                "results": final_results,
                "total": len(final_results)
            }
        except ImportError as e:
            logger.debug(f"混合检索模块不可用，回退到关键词检索: {e}")
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "keyword",
                "results": enhanced_results[:limit],
                "total": len(enhanced_results)
            }
        except Exception as e:
            logger.warning(f"混合检索执行失败，回退到关键词检索: {e}")
            return {
                "success": True,
                "query": query,
                "type": type_filter,
                "mode": "keyword",
                "results": enhanced_results[:limit],
                "total": len(enhanced_results)
            }
    
    except Exception as e:
        logger.error(f"搜索失败: {e}", exc_info=True)
        return {
            "success": False,
            "query": query,
            "type": type_filter,
            "mode": "error",
            "results": [],
            "total": 0,
            "error": str(e)
        }


# 测试函数
def _test():
    """测试搜索功能"""
    logging.basicConfig(level=logging.INFO)
    
    test_cases = [
        ("get_price", "API函数精确搜索"),
        ("Alpha101", "因子名搜索"),
        ("如何获取历史行情", "自然语言搜索"),
    ]
    
    print("=" * 60)
    print("🔍 知识库搜索测试")
    print("=" * 60)
    
    for query, desc in test_cases:
        result = search(query, limit=3)
        mode = result.get("mode", "unknown")
        total = result.get("total", 0)
        success = result.get("success", False)
        
        status = "✅" if success and total > 0 else "⚠️"
        print(f"{status} {desc}: 模式={mode}, 结果数={total}")
        
        if result.get("results"):
            for i, item in enumerate(result["results"][:2], 1):
                title = item.get("title", "")[:50]
                print(f"   {i}. {title}")
    
    print("=" * 60)


if __name__ == "__main__":
    _test()

