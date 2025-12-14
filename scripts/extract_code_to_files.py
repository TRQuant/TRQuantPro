#!/usr/bin/env python3
"""
代码提取和迁移脚本

功能：
1. 从Markdown文件中提取Python代码块
2. 保存为独立的代码文件到code_library目录
3. 更新Markdown文件，将代码块替换为<CodeFromFile>标签
4. 支持设计原理提取和增强

使用方法：
    python scripts/extract_code_to_files.py <markdown_file> [options]
"""

import re
import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional
import argparse
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
CODE_LIBRARY = PROJECT_ROOT / "code_library"
EXTENSION_DIR = PROJECT_ROOT / "extension" / "AShare-manual"


class CodeExtractor:
    """代码提取器"""
    
    def __init__(self, markdown_file: Path, output_dir: Path = None):
        self.markdown_file = Path(markdown_file)
        self.output_dir = output_dir or CODE_LIBRARY
        self.content = self.markdown_file.read_text(encoding='utf-8')
        self.extracted_codes = []
        
    def extract_code_blocks(self) -> List[Dict]:
        """
        提取所有Python代码块
        
        Returns:
            代码块列表，每个包含：content, start_pos, end_pos, metadata
        """
        pattern = r'```python\n(.*?)```'
        matches = list(re.finditer(pattern, self.content, re.DOTALL))
        
        code_blocks = []
        for match in matches:
            code_content = match.group(1).strip()
            start_pos = match.start()
            end_pos = match.end()
            
            # 提取代码块前的上下文，寻找函数名或类名
            context_start = max(0, start_pos - 500)
            context = self.content[context_start:start_pos]
            
            # 尝试提取函数名或类名
            func_match = re.search(r'def\s+(\w+)', code_content)
            class_match = re.search(r'class\s+(\w+)', code_content)
            
            name = None
            if func_match:
                name = func_match.group(1)
            elif class_match:
                name = class_match.group(1)
            
            # 提取章节信息（从文件路径）
            chapter_info = self._extract_chapter_info()
            
            code_blocks.append({
                'content': code_content,
                'start_pos': start_pos,
                'end_pos': end_pos,
                'name': name,
                'context': context,
                'chapter_info': chapter_info
            })
        
        return code_blocks
    
    def _extract_chapter_info(self) -> Dict:
        """从文件路径提取章节信息"""
        path_parts = self.markdown_file.parts
        chapter_info = {}
        
        # 查找章节编号（如 1.4, 1.9, 3.1, 3.2）
        for part in path_parts:
            match = re.search(r'(\d+)\.(\d+)', part)
            if match:
                chapter_info['chapter'] = match.group(1)
                chapter_info['section'] = match.group(2)
                break
        
        # 从文件路径中提取章节目录名（如 001_Chapter1_System_Overview）
        for part in path_parts:
            if part.startswith('001_Chapter1'):
                chapter_info['chapter_dir'] = part
                break
            elif part.startswith('002_Chapter2'):
                chapter_info['chapter_dir'] = part
                break
            elif part.startswith('003_Chapter3'):
                chapter_info['chapter_dir'] = part
                break
            elif part.startswith('00') and '_Chapter' in part:
                chapter_info['chapter_dir'] = part
                break
        
        # 如果没有找到，尝试从路径构建
        if 'chapter_dir' not in chapter_info and chapter_info.get('chapter'):
            chapter = chapter_info['chapter']
            # 从路径中查找章节名称
            for part in path_parts:
                if f'Chapter{chapter}' in part or f'chapter{chapter}' in part:
                    chapter_info['chapter_dir'] = part
                    break
        
        return chapter_info
    
    def generate_code_file_path(self, code_block: Dict, index: int) -> Path:
        """
        生成代码文件路径
        
        Args:
            code_block: 代码块信息
            index: 代码块索引
        
        Returns:
            代码文件路径
        """
        chapter_info = code_block['chapter_info']
        name = code_block['name']
        
        # 构建路径：code_library/00X_ChapterX/3.X/code_3_X_X_name.py
        if chapter_info.get('chapter') and chapter_info.get('section'):
            chapter = chapter_info['chapter']
            section = chapter_info['section']
            
            # 章节目录名（如 003_Chapter3_Market_Analysis）
            chapter_dir_name = f"00{chapter}_Chapter{chapter}_Market_Analysis"
            # 小节目录（如 1.4, 1.9）
            section_dir = f"{chapter}.{section}"
            
            # 生成文件名
            if name:
                # 使用函数名或类名
                file_name = f"code_{chapter}_{section}_{name}.py"
            else:
                # 使用索引
                file_name = f"code_{chapter}_{section}_{index:02d}.py"
            
            # 简化路径：直接放在小节文件夹下
            code_file_path = (
                self.output_dir / 
                chapter_dir_name / 
                section_dir / 
                file_name
            )
        else:
            # 如果无法提取章节信息，使用默认路径
            if name:
                file_name = f"code_{name}.py"
            else:
                file_name = f"code_{index:02d}.py"
            
            code_file_path = self.output_dir / "misc" / file_name
        
        return code_file_path
    
    def enhance_code_with_design_principles(self, code_content: str) -> str:
        """
        增强代码，添加设计原理说明（如果缺失）
        
        Args:
            code_content: 原始代码内容
        
        Returns:
            增强后的代码内容
        """
        # 检查是否已有设计原理
        if '**设计原理**' in code_content or '设计原理' in code_content:
            return code_content
        
        # 提取函数或类的docstring
        func_match = re.search(r'def\s+(\w+).*?("""(.*?)""")', code_content, re.DOTALL)
        class_match = re.search(r'class\s+(\w+).*?("""(.*?)""")', code_content, re.DOTALL)
        
        if func_match:
            func_name = func_match.group(1)
            docstring = func_match.group(2)
            
            # 生成设计原理模板
            design_principles = f'''    """
    {func_name}函数
    
    **设计原理**：
    - **核心功能**：实现{func_name}的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """'''
            
            # 替换docstring
            enhanced_code = code_content.replace(docstring, design_principles)
            return enhanced_code
        
        return code_content
    
    def save_code_file(self, code_block: Dict, code_file_path: Path) -> bool:
        """
        保存代码文件（统一添加文件头注释）
        
        Args:
            code_block: 代码块信息
            code_file_path: 代码文件路径
        
        Returns:
            是否成功保存
        """
        try:
            # 创建目录
            code_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 生成文件头注释（放在最顶部）
            file_header = self._generate_file_header(code_file_path, code_block)
            
            # 增强代码
            enhanced_code = self.enhance_code_with_design_principles(code_block['content'])
            
            # 添加必要的导入（如果缺失）
            imports = []
            if 'import pandas' not in enhanced_code and 'pd.' in enhanced_code:
                imports.append("import pandas as pd")
            if 'import numpy' not in enhanced_code and 'np.' in enhanced_code:
                imports.append("import numpy as np")
            if 'from typing' not in enhanced_code and ('->' in enhanced_code or 'Dict' in enhanced_code or 'List' in enhanced_code):
                imports.append("from typing import Dict, List, Optional")
            
            # 组合最终代码：文件头注释 + 导入 + 代码
            final_code = file_header
            if imports:
                final_code += "\n" + "\n".join(imports) + "\n"
            final_code += "\n" + enhanced_code
            
            # 保存文件
            code_file_path.write_text(final_code, encoding='utf-8')
            print(f"✅ 已保存代码文件: {code_file_path.relative_to(PROJECT_ROOT)}")
            return True
        except Exception as e:
            print(f"❌ 保存代码文件失败: {e}")
            return False
    
    def _generate_file_header(self, code_file_path: Path, code_block: Dict) -> str:
        """
        生成文件头注释（统一格式）
        
        包含信息：
        - 文件名
        - 保存路径（绝对路径和相对路径）
        - 来源Markdown文件
        - 提取时间
        - 函数/类名
        - 使用说明
        
        Args:
            code_file_path: 代码文件路径
            code_block: 代码块信息
        
        Returns:
            文件头注释字符串
        """
        # 计算相对路径（从项目根目录）
        relative_path = code_file_path.relative_to(PROJECT_ROOT)
        relative_path_str = str(relative_path).replace('\\', '/')
        
        # 绝对路径
        absolute_path = str(code_file_path.resolve())
        
        # 来源Markdown文件路径
        source_markdown = str(self.markdown_file.relative_to(PROJECT_ROOT)).replace('\\', '/')
        
        # 提取函数名或类名
        func_or_class_name = code_block.get('name', '未知')
        
        # 提取时间
        extract_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 生成统一格式的文件头注释
        # 只包含必要信息：文件名、保存路径、来源文件、提取时间、函数/类名
        # 不包含CodeFromFile示例（已在Markdown中，避免冗余）
        header = f'''"""
文件名: {code_file_path.name}
保存路径: {relative_path_str}
来源文件: {source_markdown}
提取时间: {extract_time}
函数/类名: {func_or_class_name}

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""
'''
        return header
    
    def replace_with_code_from_file(self, code_block: Dict, code_file_path: Path) -> str:
        """
        将代码块替换为<CodeFromFile>标签
        
        Args:
            code_block: 代码块信息
            code_file_path: 代码文件路径
        
        Returns:
            替换后的内容
        """
        # 计算相对路径（从extension/AShare-manual开始）
        relative_path = code_file_path.relative_to(PROJECT_ROOT)
        relative_path_str = str(relative_path).replace('\\', '/')
        
        # 生成CodeFromFile标签
        code_from_file_tag = f'''<CodeFromFile 
  filePath="{relative_path_str}"
  language="python"
  showDesignPrinciples="true"
/>'''
        
        # 保留原始代码作为注释（可选）
        original_code_comment = f"\n\n<!-- 原始代码（保留作为备份）：\n```python\n{code_block['content']}\n```\n-->"
        
        # 替换代码块
        old_code_block = self.content[code_block['start_pos']:code_block['end_pos']]
        new_content = self.content.replace(
            old_code_block,
            code_from_file_tag + original_code_comment,
            1  # 只替换第一个匹配
        )
        
        return new_content
    
    def process(self, dry_run: bool = False) -> Dict:
        """
        处理Markdown文件，提取代码并更新
        
        Args:
            dry_run: 是否只是预览，不实际修改文件
        
        Returns:
            处理结果统计
        """
        print(f"📄 处理文件: {self.markdown_file.relative_to(PROJECT_ROOT)}")
        
        # 提取代码块
        code_blocks = self.extract_code_blocks()
        print(f"📊 找到 {len(code_blocks)} 个代码块")
        
        if not code_blocks:
            print("⚠️  未找到代码块")
            return {'extracted': 0, 'updated': 0}
        
        extracted_count = 0
        updated_count = 0
        
        for i, code_block in enumerate(code_blocks):
            # 生成代码文件路径
            code_file_path = self.generate_code_file_path(code_block, i)
            
            print(f"\n📝 处理代码块 {i+1}/{len(code_blocks)}")
            if code_block['name']:
                print(f"   函数/类名: {code_block['name']}")
            print(f"   输出路径: {code_file_path.relative_to(PROJECT_ROOT)}")
            
            if not dry_run:
                # 保存代码文件
                if self.save_code_file(code_block, code_file_path):
                    extracted_count += 1
                    
                    # 更新Markdown内容
                    self.content = self.replace_with_code_from_file(code_block, code_file_path)
                    updated_count += 1
            else:
                print("   [预览模式] 将保存到此路径")
                extracted_count += 1
                updated_count += 1
        
        if not dry_run and updated_count > 0:
            # 保存更新后的Markdown文件
            backup_file = self.markdown_file.with_suffix('.md.backup')
            self.markdown_file.rename(backup_file)
            self.markdown_file.write_text(self.content, encoding='utf-8')
            print(f"\n✅ 已更新Markdown文件")
            print(f"   备份文件: {backup_file.relative_to(PROJECT_ROOT)}")
        
        return {
            'extracted': extracted_count,
            'updated': updated_count,
            'total': len(code_blocks)
        }


def main():
    parser = argparse.ArgumentParser(description='从Markdown提取代码并迁移到独立文件')
    parser.add_argument('markdown_file', type=str, help='Markdown文件路径')
    parser.add_argument('--output-dir', type=str, default=None, help='代码输出目录')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际修改文件')
    parser.add_argument('--batch', action='store_true', help='批量处理模式')
    
    args = parser.parse_args()
    
    markdown_file = Path(args.markdown_file)
    if not markdown_file.is_absolute():
        markdown_file = PROJECT_ROOT / markdown_file
    
    if not markdown_file.exists():
        print(f"❌ 文件不存在: {markdown_file}")
        sys.exit(1)
    
    output_dir = None
    if args.output_dir:
        output_dir = Path(args.output_dir)
        if not output_dir.is_absolute():
            output_dir = PROJECT_ROOT / output_dir
    
    extractor = CodeExtractor(markdown_file, output_dir)
    result = extractor.process(dry_run=args.dry_run)
    
    print(f"\n📊 处理完成:")
    print(f"   提取代码块: {result['extracted']}/{result['total']}")
    print(f"   更新Markdown: {result['updated']}/{result['total']}")


if __name__ == '__main__':
    main()

