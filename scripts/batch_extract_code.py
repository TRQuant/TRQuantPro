#!/usr/bin/env python3
"""
批量代码提取脚本

功能：
批量处理所有Markdown文件，提取代码并迁移

使用方法：
    python scripts/batch_extract_code.py [--dry-run] [--chapter <chapter>]
"""

import sys
from pathlib import Path
from extract_code_to_files import CodeExtractor

PROJECT_ROOT = Path(__file__).parent.parent
EXTENSION_DIR = PROJECT_ROOT / "extension" / "AShare-manual"
PAGES_DIR = EXTENSION_DIR / "src" / "pages"


def find_markdown_files(chapter: str = None) -> list:
    """
    查找所有Markdown文件
    
    Args:
        chapter: 章节过滤（如 "003" 只处理第3章）
    
    Returns:
        Markdown文件列表
    """
    markdown_files = []
    
    # 查找所有.md文件
    for md_file in PAGES_DIR.rglob("*.md"):
        # 跳过备份文件
        if md_file.name.endswith('.backup'):
            continue
        
        # 章节过滤
        if chapter:
            if chapter not in str(md_file):
                continue
        
        markdown_files.append(md_file)
    
    return sorted(markdown_files)


def batch_process(dry_run: bool = False, chapter: str = None):
    """
    批量处理所有Markdown文件
    
    Args:
        dry_run: 是否只是预览
        chapter: 章节过滤
    """
    markdown_files = find_markdown_files(chapter)
    
    print(f"📚 找到 {len(markdown_files)} 个Markdown文件")
    
    if chapter:
        print(f"📖 过滤章节: {chapter}")
    
    total_extracted = 0
    total_updated = 0
    total_files = 0
    
    for i, md_file in enumerate(markdown_files, 1):
        print(f"\n{'='*60}")
        print(f"[{i}/{len(markdown_files)}] 处理: {md_file.relative_to(PROJECT_ROOT)}")
        print('='*60)
        
        try:
            extractor = CodeExtractor(md_file)
            result = extractor.process(dry_run=dry_run)
            
            total_extracted += result['extracted']
            total_updated += result['updated']
            if result['extracted'] > 0:
                total_files += 1
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"📊 批量处理完成:")
    print(f"   处理文件数: {total_files}/{len(markdown_files)}")
    print(f"   提取代码块: {total_extracted}")
    print(f"   更新Markdown: {total_updated}")
    print('='*60)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='批量提取代码')
    parser.add_argument('--dry-run', action='store_true', help='预览模式')
    parser.add_argument('--chapter', type=str, default=None, help='章节过滤（如 003）')
    
    args = parser.parse_args()
    
    batch_process(dry_run=args.dry_run, chapter=args.chapter)

