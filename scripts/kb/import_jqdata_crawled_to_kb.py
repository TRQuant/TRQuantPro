#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将已爬取的JQData文档导入到知识库
==================================

从docs/jqdata_crawled/目录读取已爬取的文档，导入到知识库
"""

import sys
import json
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add


def load_jqdata_kb_items():
    """加载JQData知识库格式文件"""
    kb_file = TRQUANT_ROOT / "docs" / "jqdata_crawled" / "kb_all_items.json"
    
    if not kb_file.exists():
        print(f"❌ 知识库格式文件不存在: {kb_file}")
        return []
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        print(f"✅ 加载了 {len(items)} 条知识库条目")
        return items
    except Exception as e:
        print(f"❌ 加载失败: {e}")
        return []


def check_existing_knowledge():
    """检查知识库中已存在的JQData知识"""
    kb_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
    
    if not kb_file.exists():
        return set()
    
    try:
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb = json.load(f)
        
        items = kb.get('items', [])
        existing_titles = {i.get('title', '') for i in items if '聚宽' in i.get('title', '') or 'JQData' in i.get('title', '')}
        return existing_titles
    except Exception as e:
        print(f"⚠️ 检查现有知识失败: {e}")
        return set()


def import_jqdata_to_kb(limit=None, skip_existing=True):
    """导入JQData文档到知识库"""
    print("=" * 70)
    print("📚 导入JQData文档到知识库")
    print("=" * 70)
    print()
    
    # 加载知识库条目
    items = load_jqdata_kb_items()
    if not items:
        print("❌ 没有可导入的文档")
        return False
    
    # 检查已存在的知识
    existing_titles = set()
    if skip_existing:
        print("🔍 检查已存在的知识...")
        existing_titles = check_existing_knowledge()
        print(f"   已存在 {len(existing_titles)} 条知识")
        print()
    
    # 过滤已存在的条目
    items_to_import = []
    for item in items:
        title = item.get('title', '')
        if skip_existing and title in existing_titles:
            continue
        items_to_import.append(item)
    
    if limit:
        items_to_import = items_to_import[:limit]
    
    print(f"📝 准备导入 {len(items_to_import)} 条知识...")
    print()
    
    success_count = 0
    failed_count = 0
    
    for i, item in enumerate(items_to_import, 1):
        title = item.get('title', f'JQData文档_{i}')
        print(f"[{i}/{len(items_to_import)}] 导入: {title[:60]}...")
        
        try:
            result = knowledge_add(
                title=title,
                content=item.get('content', ''),
                type=item.get('type', 'reference'),
                tags=item.get('tags', ['聚宽', 'JQData', 'API文档']),
                source=item.get('source', '聚宽官方文档')
            )
            
            if result.get('success') or result.get('knowledge_id'):
                print(f"    ✅ 导入成功")
                success_count += 1
            else:
                print(f"    ❌ 导入失败: {result.get('error', 'Unknown')}")
                failed_count += 1
        except Exception as e:
            print(f"    ❌ 异常: {e}")
            failed_count += 1
        
        # 每10条显示一次进度
        if i % 10 == 0:
            print(f"    📊 进度: {success_count}成功, {failed_count}失败")
        print()
    
    print("=" * 70)
    print(f"📊 导入完成: {success_count}成功, {failed_count}失败")
    print("=" * 70)
    
    return success_count > 0


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='导入JQData文档到知识库')
    parser.add_argument('--limit', type=int, help='限制导入数量')
    parser.add_argument('--no-skip', action='store_true', help='不跳过已存在的知识')
    
    args = parser.parse_args()
    
    success = import_jqdata_to_kb(
        limit=args.limit,
        skip_existing=not args.no_skip
    )
    
    if success:
        print()
        print("✅ 导入成功！")
    else:
        print()
        print("❌ 导入失败")


if __name__ == '__main__':
    main()
