#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 知识库管理工具
====================

提供完整的知识库管理功能：
1. 添加知识条目
2. 搜索知识
3. 构建/重建向量索引
4. 统计信息
5. 清理重复条目

运行: python scripts/kb/kb_manager.py <command> [options]
"""

import sys
import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('KBManager')

# 导入知识库构建器
from scripts.kb.kb_builder import KnowledgeBaseBuilder

# 导入搜索功能
try:
    from mcp_servers.knowledge_search_api import search as hybrid_search
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False
    logger.warning("搜索功能不可用")


class KnowledgeManager:
    """知识库管理器"""
    
    def __init__(self):
        self.builder = KnowledgeBaseBuilder()
    
    def add(
        self,
        title: str,
        content: str,
        type: str = "reference",
        tags: List[str] = None,
        source: str = "",
        platform: str = ""
    ) -> str:
        """添加知识条目"""
        return self.builder.add_knowledge(
            title=title,
            content=content,
            type=type,
            tags=tags or [],
            source=source,
            platform=platform
        )
    
    def search(self, query: str, limit: int = 10, type_filter: str = None) -> List[Dict]:
        """搜索知识"""
        if not SEARCH_AVAILABLE:
            logger.error("搜索功能不可用")
            return []
        
        try:
            result = hybrid_search(query, limit=limit, type_filter=type_filter)
            return result.get("results", [])
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    def stats(self) -> Dict:
        """获取统计信息"""
        kb = self.builder.load_kb()
        items = kb.get("items", [])
        
        # 按类型统计
        type_stats = {}
        platform_stats = {}
        tag_stats = {}
        
        for item in items:
            # 类型统计
            item_type = item.get("type", "unknown")
            type_stats[item_type] = type_stats.get(item_type, 0) + 1
            
            # 平台统计
            platform = item.get("platform", "")
            if platform:
                platform_stats[platform] = platform_stats.get(platform, 0) + 1
            
            # 标签统计
            tags = item.get("tags", [])
            for tag in tags:
                tag_stats[tag] = tag_stats.get(tag, 0) + 1
        
        return {
            "total": len(items),
            "by_type": type_stats,
            "by_platform": platform_stats,
            "top_tags": dict(sorted(tag_stats.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    
    def build_index(self, force: bool = False) -> Dict:
        """构建向量索引"""
        return self.builder.build_vector_index(force_rebuild=force)
    
    def clean_duplicates(self) -> int:
        """清理重复条目"""
        kb = self.builder.load_kb()
        items = kb.get("items", [])
        
        seen_hashes = {}
        duplicates = []
        
        for idx, item in enumerate(items):
            content_hash = hash(f"{item.get('title', '')}{item.get('content', '')}")
            if content_hash in seen_hashes:
                duplicates.append(idx)
            else:
                seen_hashes[content_hash] = idx
        
        if duplicates:
            # 移除重复项（保留第一个）
            for idx in sorted(duplicates, reverse=True):
                items.pop(idx)
            
            kb["items"] = items
            self.builder.save_kb(kb)
            logger.info(f"✅ 已清理 {len(duplicates)} 个重复条目")
        
        return len(duplicates)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="TRQuant 知识库管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # add命令
    parser_add = subparsers.add_parser("add", help="添加知识条目")
    parser_add.add_argument("--title", type=str, required=True, help="标题")
    parser_add.add_argument("--content", type=str, required=True, help="内容")
    parser_add.add_argument("--type", type=str, default="reference", help="类型")
    parser_add.add_argument("--tags", type=str, nargs="+", default=[], help="标签")
    parser_add.add_argument("--source", type=str, default="", help="来源")
    parser_add.add_argument("--platform", type=str, default="", help="平台")
    
    # search命令
    parser_search = subparsers.add_parser("search", help="搜索知识")
    parser_search.add_argument("--query", type=str, required=True, help="查询文本")
    parser_search.add_argument("--limit", type=int, default=10, help="返回数量")
    parser_search.add_argument("--type", type=str, default=None, help="类型过滤")
    
    # stats命令
    subparsers.add_parser("stats", help="显示统计信息")
    
    # build-index命令
    parser_build = subparsers.add_parser("build-index", help="构建向量索引")
    parser_build.add_argument("--force", action="store_true", help="强制重建")
    
    # clean命令
    subparsers.add_parser("clean", help="清理重复条目")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("=" * 70)
    print("TRQuant 知识库管理工具")
    print("=" * 70)
    print()
    
    manager = KnowledgeManager()
    
    if args.command == "add":
        kb_id = manager.add(
            title=args.title,
            content=args.content,
            type=args.type,
            tags=args.tags,
            source=args.source,
            platform=args.platform
        )
        print(f"✅ 已添加知识条目: {kb_id}")
    
    elif args.command == "search":
        results = manager.search(query=args.query, limit=args.limit, type_filter=args.type)
        print(f"🔍 搜索结果: {len(results)} 条")
        print()
        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result.get('title', 'Untitled')}")
            print(f"   类型: {result.get('type', 'unknown')}")
            print(f"   平台: {result.get('platform', 'N/A')}")
            print(f"   评分: {result.get('_score', 0):.2f}")
            print()
    
    elif args.command == "stats":
        stats = manager.stats()
        print(f"📊 知识库统计:")
        print(f"   总数: {stats['total']} 条")
        print()
        print(f"   按类型:")
        for type_name, count in stats['by_type'].items():
            print(f"     - {type_name}: {count}")
        print()
        print(f"   按平台:")
        for platform, count in stats['by_platform'].items():
            print(f"     - {platform}: {count}")
        print()
        print(f"   热门标签:")
        for tag, count in stats['top_tags'].items():
            print(f"     - {tag}: {count}")
    
    elif args.command == "build-index":
        print("🔨 构建向量索引...")
        result = manager.build_index(force=args.force)
        if result.get("success"):
            print(f"✅ 向量索引构建成功")
            print(f"   - 条目数: {result.get('items_count', 0)}")
            print(f"   - 模型: {result.get('model', '')}")
            print(f"   - 向量维度: {result.get('embedding_dim', 0)}")
        else:
            print(f"❌ 向量索引构建失败: {result.get('error', 'Unknown error')}")
    
    elif args.command == "clean":
        print("🧹 清理重复条目...")
        count = manager.clean_duplicates()
        if count > 0:
            print(f"✅ 已清理 {count} 个重复条目")
        else:
            print("✅ 没有发现重复条目")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
