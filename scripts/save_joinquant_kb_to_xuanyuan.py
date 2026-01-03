#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将聚宽知识库存入轩辕剑灵知识库系统

Author: TRQuant Team
Date: 2025-12-24
"""

import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入MCP工具
try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError:
    print("⚠️ 知识库工具不可用")
    KB_AVAILABLE = False

def save_kb_entries(kb_file: Path):
    """将知识库条目存入轩辕剑灵"""
    if not KB_AVAILABLE:
        print("❌ 知识库工具不可用")
        return
    
    # 读取知识库JSON
    with open(kb_file, 'r', encoding='utf-8') as f:
        kb_entries = json.load(f)
    
    print(f"📚 准备存入 {len(kb_entries)} 个知识库条目...")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for i, entry in enumerate(kb_entries, 1):
        print(f"\n[{i}/{len(kb_entries)}] {entry['title']}")
        
        try:
            result = knowledge_add(
                title=entry['title'],
                content=entry['content'],
                type=entry.get('type', 'reference'),
                tags=entry.get('tags', [])
            )
            
            if result.get('success'):
                print(f"  ✅ 成功存入")
                success_count += 1
            else:
                print(f"  ❌ 失败: {result.get('error', 'Unknown error')}")
                fail_count += 1
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            fail_count += 1
    
    print("\n" + "=" * 70)
    print("📊 存入结果")
    print("=" * 70)
    print(f"成功: {success_count} 个")
    print(f"失败: {fail_count} 个")
    print(f"总计: {len(kb_entries)} 个")

def main():
    """主函数"""
    kb_file = PROJECT_ROOT / "docs" / "joinquant_kb_comprehensive" / "knowledge_base.json"
    
    if not kb_file.exists():
        print(f"❌ 知识库文件不存在: {kb_file}")
        print("   请先运行 crawl_joinquant_kb_comprehensive.py")
        return
    
    save_kb_entries(kb_file)

if __name__ == "__main__":
    main()





































