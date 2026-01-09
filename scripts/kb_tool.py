#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRQuant 知识库工具
==================

便捷的命令行工具，用于管理知识库。

用法:
    python scripts/kb_tool.py search "关键词"
    python scripts/kb_tool.py search "关键词" --category bulletrade_debug
    python scripts/kb_tool.py add "标题" "内容" --category bulletrade_debug
    python scripts/kb_tool.py list
    python scripts/kb_tool.py list --category bulletrade_debug
    python scripts/kb_tool.py best-practices
    python scripts/kb_tool.py best-practices --category backtest
"""

import sys
import argparse
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "mcp_servers"))

from unified_dev_server import kb_search, kb_add, kb_best_practices, _load_json, DATA_DIR


def cmd_search(args):
    """搜索知识库"""
    result = kb_search(args.query, category=args.category)
    
    print(f"\n搜索: '{args.query}'")
    if args.category:
        print(f"分类: {args.category}")
    print(f"找到 {result['total']} 条结果\n")
    
    if result['results']:
        for i, r in enumerate(result['results'], 1):
            print(f"{'=' * 60}")
            print(f"[{i}] {r.get('title', r.get('key', 'N/A'))}")
            print(f"来源: {r.get('source', 'N/A')} | 分类: {r.get('category', 'N/A')}")
            print("-" * 60)
            content = r.get('content', r.get('description', 'N/A'))
            # 截断长内容
            if len(content) > 500:
                content = content[:500] + "..."
            print(content)
            print()
    else:
        print("未找到相关知识")


def cmd_add(args):
    """添加知识条目"""
    result = kb_add(args.title, args.content, category=args.category)
    
    if result['success']:
        print(f"\n✅ 知识条目添加成功")
        print(f"ID: {result['item']['id']}")
        print(f"标题: {result['item']['title']}")
        print(f"分类: {result['item']['category']}")
    else:
        print(f"\n❌ 添加失败: {result.get('error', '未知错误')}")


def cmd_list(args):
    """列出知识库内容"""
    kb_file = DATA_DIR / "kb" / "custom_kb.json"
    
    if not kb_file.exists():
        print("\n知识库为空")
        return
    
    kb = _load_json(kb_file, {"items": []})
    items = kb.get("items", [])
    
    if args.category:
        items = [i for i in items if i.get("category") == args.category]
    
    print(f"\n知识库共有 {len(items)} 条记录")
    if args.category:
        print(f"(按分类 '{args.category}' 过滤)")
    
    # 按分类分组
    categories = {}
    for item in items:
        cat = item.get("category", "general")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    print()
    for cat, cat_items in sorted(categories.items()):
        print(f"📁 {cat} ({len(cat_items)}条)")
        for item in cat_items:
            print(f"   - {item.get('title', 'N/A')} [{item.get('id', 'N/A')}]")
        print()


def cmd_best_practices(args):
    """获取最佳实践"""
    result = kb_best_practices(category=args.category)
    
    print(f"\n最佳实践 ({result['total']}条)")
    if args.category:
        print(f"分类: {args.category}")
    
    print()
    for p in result['practices']:
        print(f"📌 [{p['category']}] {p['title']}")
        print(f"   {p['content']}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="TRQuant 知识库工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  搜索知识库:
    python scripts/kb_tool.py search "BulletTrade"
    python scripts/kb_tool.py search "get_fundamentals" --category bulletrade_debug
    
  添加知识:
    python scripts/kb_tool.py add "问题标题" "问题描述和解决方案..." --category bulletrade_debug
    
  列出知识:
    python scripts/kb_tool.py list
    python scripts/kb_tool.py list --category bulletrade_debug
    
  最佳实践:
    python scripts/kb_tool.py best-practices
    python scripts/kb_tool.py best-practices --category backtest
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # search 命令
    search_parser = subparsers.add_parser("search", help="搜索知识库")
    search_parser.add_argument("query", help="搜索关键词")
    search_parser.add_argument("--category", "-c", help="按分类过滤")
    
    # add 命令
    add_parser = subparsers.add_parser("add", help="添加知识条目")
    add_parser.add_argument("title", help="标题")
    add_parser.add_argument("content", help="内容")
    add_parser.add_argument("--category", "-c", default="general", help="分类 (默认: general)")
    
    # list 命令
    list_parser = subparsers.add_parser("list", help="列出知识库内容")
    list_parser.add_argument("--category", "-c", help="按分类过滤")
    
    # best-practices 命令
    bp_parser = subparsers.add_parser("best-practices", help="获取最佳实践")
    bp_parser.add_argument("--category", "-c", help="按分类过滤")
    
    args = parser.parse_args()
    
    if args.command == "search":
        cmd_search(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "best-practices":
        cmd_best_practices(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
