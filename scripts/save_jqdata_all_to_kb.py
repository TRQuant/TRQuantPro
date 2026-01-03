#!/usr/bin/env python3
"""
将所有JQData API文档存入轩辕剑灵知识库

Author: TRQuant Team
Date: 2025-12-28
"""

import sys
import json
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入MCP工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False

def save_all_jqdata_docs():
    """将所有JQData文档存入知识库"""
    if not KB_AVAILABLE:
        print("❌ 知识库工具不可用，无法存入文档")
        return
    
    kb_file = PROJECT_ROOT / 'docs/jqdata_crawled/kb_all_items.json'
    
    if not kb_file.exists():
        print(f"❌ 知识库格式文件不存在: {kb_file}")
        print("💡 提示: 请先运行 scripts/save_jqdata_to_kb.py 生成知识库格式文件")
        return
    
    # 读取知识库JSON
    print(f"📖 读取知识库格式文件: {kb_file}")
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb_entries = json.load(f)
    
    print(f"📚 找到 {len(kb_entries)} 个文档条目")
    print("=" * 70)
    print()
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for i, entry in enumerate(kb_entries, 1):
        title = entry.get('title', '无标题')
        print(f"[{i:3d}/{len(kb_entries)}] {title[:60]}")
        
        try:
            # 添加标签
            tags = entry.get('tags', [])
            if not tags:
                tags = ['JQData', 'API文档', '官方文档']
            
            result = knowledge_add(
                title=title,
                content=entry.get('content', ''),
                type='reference',  # API文档类型
                tags=tags
            )
            
            if result.get('success'):
                kb_id = result.get('knowledge_id', '')
                print(f"      ✅ 成功存入 ({kb_id})")
                success_count += 1
            else:
                error = result.get('error', 'Unknown error')
                print(f"      ❌ 失败: {error}")
                fail_count += 1
                
        except Exception as e:
            print(f"      ❌ 异常: {str(e)[:100]}")
            fail_count += 1
        
        # 避免请求过快
        if i < len(kb_entries):
            time.sleep(0.5)
    
    print()
    print("=" * 70)
    print("📊 存入结果统计")
    print("=" * 70)
    print(f"总文档数: {len(kb_entries)}")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {fail_count}")
    print(f"⏭️  跳过: {skip_count}")
    print("=" * 70)
    
    if success_count > 0:
        print(f"\n✅ 成功将 {success_count} 个JQData API文档存入知识库！")
    
    return {
        'total': len(kb_entries),
        'success': success_count,
        'failed': fail_count,
        'skipped': skip_count
    }

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 JQData API文档批量存入知识库")
    print("=" * 70)
    print()
    
    save_all_jqdata_docs()








