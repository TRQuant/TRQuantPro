#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大文件去重工具
==============

识别并移除重复的类定义和代码块，保留唯一实现。

使用方法:
    python scripts/deduplication/deduplicate.py <file_path> [--output <output_path>]
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict
import hashlib


class CodeDeduplicator:
    """代码去重器"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        self.lines = []
        self.class_blocks: Dict[str, List[Tuple[int, int, str]]] = defaultdict(list)
        
    def read_file(self):
        """读取文件内容"""
        print(f"📖 读取文件: {self.file_path}")
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        print(f"   总行数: {len(self.lines):,}")
    
    def find_class_blocks(self):
        """查找所有类定义块"""
        print("\n🔍 查找类定义...")
        
        class_pattern = re.compile(r'^class\s+(\w+)')
        current_class = None
        class_start = None
        indent_level = 0
        
        for i, line in enumerate(self.lines):
            # 检查类定义
            match = class_pattern.match(line.strip())
            if match:
                # 保存之前的类
                if current_class and class_start is not None:
                    class_end = i
                    class_code = ''.join(self.lines[class_start:class_end])
                    self.class_blocks[current_class].append((class_start, class_end, class_code))
                
                # 开始新类
                current_class = match.group(1)
                class_start = i
                indent_level = len(line) - len(line.lstrip())
            
            # 检查类是否结束（下一个同级别或更高级别的类定义）
            elif current_class and line.strip():
                line_indent = len(line) - len(line.lstrip())
                if line_indent <= indent_level and class_pattern.match(line.strip()):
                    # 保存当前类
                    class_end = i
                    class_code = ''.join(self.lines[class_start:class_end])
                    self.class_blocks[current_class].append((class_start, class_end, class_code))
                    
                    # 开始新类
                    match = class_pattern.match(line.strip())
                    current_class = match.group(1)
                    class_start = i
                    indent_level = line_indent
        
        # 保存最后一个类
        if current_class and class_start is not None:
            class_end = len(self.lines)
            class_code = ''.join(self.lines[class_start:class_end])
            self.class_blocks[current_class].append((class_start, class_end, class_code))
        
        # 统计重复
        duplicates = {name: blocks for name, blocks in self.class_blocks.items() if len(blocks) > 1}
        
        print(f"   找到 {len(self.class_blocks)} 个不同的类")
        print(f"   ⚠️  发现 {len(duplicates)} 个重复的类:")
        
        total_duplicates = 0
        for name, blocks in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            count = len(blocks)
            total_duplicates += count - 1
            print(f"      - {name}: {count} 次 (行 {blocks[0][0]+1}, {blocks[1][0]+1}, ...)")
        
        print(f"\n   预计可删除 {total_duplicates} 个重复类定义")
        return duplicates
    
    def select_best_implementation(self, blocks: List[Tuple[int, int, str]]) -> int:
        """选择最佳实现（选择最完整的那个）"""
        # 简单策略：选择代码行数最多的
        best_idx = 0
        best_lines = len(blocks[0][2].split('\n'))
        
        for i, (start, end, code) in enumerate(blocks[1:], 1):
            lines = len(code.split('\n'))
            if lines > best_lines:
                best_idx = i
                best_lines = lines
        
        return best_idx
    
    def deduplicate(self, output_path: str = None) -> Path:
        """执行去重"""
        print("\n🔄 开始去重...")
        
        duplicates = self.find_class_blocks()
        
        if not duplicates:
            print("   ✅ 未发现重复代码，无需去重")
            return self.file_path
        
        # 确定要删除的行号
        lines_to_remove = set()
        
        for class_name, blocks in duplicates.items():
            # 选择最佳实现
            best_idx = self.select_best_implementation(blocks)
            print(f"   保留 {class_name} 的最佳实现 (第 {best_idx+1} 个，行 {blocks[best_idx][0]+1})")
            
            # 标记其他块为删除
            for i, (start, end, _) in enumerate(blocks):
                if i != best_idx:
                    # 删除整个类块（包括空行）
                    for line_num in range(start, end):
                        lines_to_remove.add(line_num)
                    
                    # 删除类定义前的空行（如果存在）
                    if start > 0 and not self.lines[start-1].strip():
                        lines_to_remove.add(start - 1)
        
        # 生成新文件
        new_lines = [line for i, line in enumerate(self.lines) if i not in lines_to_remove]
        
        # 清理连续的空行（保留最多2个连续空行）
        cleaned_lines = []
        empty_count = 0
        for line in new_lines:
            if not line.strip():
                empty_count += 1
                if empty_count <= 2:
                    cleaned_lines.append(line)
            else:
                empty_count = 0
                cleaned_lines.append(line)
        
        # 确定输出路径
        if output_path is None:
            output_path = self.file_path.parent / f"{self.file_path.stem}_deduplicated{self.file_path.suffix}"
        else:
            output_path = Path(output_path)
        
        # 写入新文件
        print(f"\n💾 保存去重后的文件: {output_path}")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        
        original_lines = len(self.lines)
        new_lines_count = len(cleaned_lines)
        reduction = original_lines - new_lines_count
        reduction_pct = (reduction / original_lines) * 100
        
        print(f"\n📊 去重结果:")
        print(f"   原始行数: {original_lines:,}")
        print(f"   去重后: {new_lines_count:,}")
        print(f"   减少: {reduction:,} 行 ({reduction_pct:.1f}%)")
        
        return output_path


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python deduplicate.py <file_path> [--output <output_path>]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]
    
    try:
        deduplicator = CodeDeduplicator(file_path)
        deduplicator.read_file()
        output_file = deduplicator.deduplicate(output_path)
        
        print(f"\n✅ 去重完成!")
        print(f"   输出文件: {output_file}")
        print(f"\n⚠️  请手动验证去重后的代码功能是否完整")
        print(f"   建议: 运行测试确保功能正常")
        
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()


