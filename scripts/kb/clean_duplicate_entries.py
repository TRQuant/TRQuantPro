#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清理知识库中的重复条目
====================

合并相同标题的条目，保留最完整的版本
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))


def merge_items(items: List[Dict]) -> Dict:
    """合并多个条目，保留最完整的版本"""
    if not items:
        return None
    
    if len(items) == 1:
        return items[0]
    
    # 选择最完整的条目（内容最长的）
    best_item = max(items, key=lambda x: len(x.get('content', '')))
    
    # 合并tags
    all_tags = set()
    for item in items:
        tags = item.get('tags', [])
        if isinstance(tags, list):
            all_tags.update(tags)
        elif isinstance(tags, str):
            all_tags.add(tags)
    
    best_item['tags'] = list(all_tags)
    
    # 合并来源信息
    sources = [item.get('source', '') for item in items if item.get('source')]
    if len(sources) > 1:
        best_item['source'] = f"合并自: {', '.join(set(sources))}"
    
    return best_item


def clean_duplicate_entries():
    """清理重复条目"""
    
    print("=" * 70)
    print("🧹 清理知识库重复条目")
    print("=" * 70)
    print()
    
    # 加载知识库
    kb_file = Path('.trquant/dev/knowledge/knowledge_base.json')
    if not kb_file.exists():
        print("❌ 知识库文件不存在")
        return False
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb = json.load(f)
    
    items = kb.get('items', [])
    v2_items = [i for i in items if i.get('type') in ['market_regime', 'factor_behavior', 'strategy_pattern', 'failure_case']]
    
    print(f"📊 找到 {len(v2_items)} 条V2知识")
    print()
    
    # 按标题分组
    title_groups = defaultdict(list)
    for item in v2_items:
        title = item.get('title', '')
        if title:
            title_groups[title].append(item)
    
    # 找出重复标题
    duplicates = {title: items for title, items in title_groups.items() if len(items) > 1}
    
    if not duplicates:
        print("✅ 无重复标题，无需清理")
        return True
    
    print(f"⚠️  发现 {len(duplicates)} 个重复标题")
    print()
    
    # 合并重复条目
    merged_count = 0
    removed_ids = set()
    
    for title, dup_items in duplicates.items():
        print(f"📋 处理重复标题: {title[:60]}")
        print(f"   发现 {len(dup_items)} 个重复条目")
        
        # 合并条目
        merged_item = merge_items(dup_items)
        
        if merged_item:
            # 保留第一个条目的ID，删除其他的
            keep_id = dup_items[0].get('id')
            merged_item['id'] = keep_id
            
            # 更新第一个条目
            for i, item in enumerate(items):
                if item.get('id') == keep_id:
                    items[i] = merged_item
                    break
            
            # 标记其他条目为删除
            for item in dup_items[1:]:
                removed_ids.add(item.get('id'))
                print(f"   - 删除: ID={item.get('id')}")
            
            merged_count += len(dup_items) - 1
            print(f"   ✅ 已合并，保留ID: {keep_id}")
        print()
    
    # 删除重复条目
    kb['items'] = [item for item in items if item.get('id') not in removed_ids]
    
    # 保存知识库
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"📊 清理完成: 删除了 {merged_count} 个重复条目")
    print(f"   - 处理了 {len(duplicates)} 个重复标题")
    print(f"   - 保留了 {len(duplicates)} 个合并后的条目")
    print("=" * 70)
    
    return True


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 清理知识库重复条目")
    print("=" * 70)
    print()
    
    success = clean_duplicate_entries()
    
    print()
    print("=" * 70)
    if success:
        print("✅ 重复条目清理成功！")
        print()
        print("🎯 下一步:")
        print("   1. 运行测试脚本验证清理效果")
        print("   2. 继续补充更多高可靠性知识")
    else:
        print("❌ 重复条目清理失败")
    print("=" * 70)


if __name__ == '__main__':
    main()
