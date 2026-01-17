#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP服务器集成常见错误修复工具
============================

自动检测和修复MCP服务器集成过程中的常见错误：
1. 缩进错误（try-except结构）
2. 转义字符问题
3. 多余的括号/符号
4. 导入语句缩进
5. 适配函数缺失

使用方法:
    python mcp_servers/utils/mcp_integration_fixer.py <server_file>
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Dict, Any

class MCPIntegrationFixer:
    """MCP集成错误修复器"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = file_path.read_text(encoding='utf-8')
        self.lines = self.content.splitlines(keepends=True)
        self.fixes_applied = []
    
    def fix_all(self) -> Dict[str, Any]:
        """应用所有修复"""
        original_content = self.content
        
        # 1. 修复转义字符问题
        self.fix_escape_chars()
        
        # 2. 修复try-except缩进
        self.fix_try_except_indentation()
        
        # 3. 修复多余的括号/符号
        self.fix_extra_brackets()
        
        # 4. 修复导入语句缩进
        self.fix_import_indentation()
        
        # 5. 验证并修复适配函数
        self.verify_adapter_function()
        
        if self.content != original_content:
            self.file_path.write_text(self.content, encoding='utf-8')
            return {
                "fixed": True,
                "fixes": self.fixes_applied,
                "file": str(self.file_path)
            }
        else:
            return {
                "fixed": False,
                "fixes": [],
                "file": str(self.file_path)
            }
    
    def fix_escape_chars(self):
        """修复转义字符问题"""
        # 修复 \\" 应该是 "
        pattern = r'raise NotImplementedError\\(\"([^\"]+)\\"\\)'
        replacement = r'raise NotImplementedError("\1")'
        
        if re.search(pattern, self.content):
            self.content = re.sub(pattern, replacement, self.content)
            self.fixes_applied.append("修复转义字符问题")
    
    def fix_try_except_indentation(self):
        """修复try-except结构的缩进问题"""
        lines = self.content.splitlines(keepends=True)
        new_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 检测try-except结构问题
            if 'try:' in line and i + 1 < len(lines):
                # 检查下一行是否有正确的缩进
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                current_indent = len(line) - len(line.lstrip())
                
                # 如果try在某个块内，下一行应该有更多缩进
                if current_indent > 0 and next_line and not next_line.strip().startswith('#') and not next_line.strip().startswith('except'):
                    next_indent = len(next_line) - len(next_line.lstrip())
                    if next_indent <= current_indent and next_line.strip():
                        # 修复缩进
                        expected_indent = current_indent + 4
                        fixed_line = ' ' * expected_indent + next_line.lstrip()
                        new_lines.append(line)
                        new_lines.append(fixed_line)
                        i += 2
                        self.fixes_applied.append(f"修复第{i+1}行的try块缩进")
                        continue
            
            new_lines.append(line)
            i += 1
        
        self.content = ''.join(new_lines)
    
    def fix_extra_brackets(self):
        """修复多余的括号/符号"""
        lines = self.content.splitlines(keepends=True)
        new_lines = []
        
        for i, line in enumerate(lines):
            # 检测多余的 ] 在except之前
            if line.strip() == ']' and i > 0:
                prev_line = lines[i - 1] if i > 0 else ""
                next_line = lines[i + 1] if i + 1 < len(lines) else ""
                
                # 如果前一行是raise ValueError，后一行是except，这个]是多余的
                if 'raise ValueError' in prev_line and 'except' in next_line:
                    self.fixes_applied.append(f"删除第{i+1}行多余的]")
                    continue
            
            new_lines.append(line)
        
        self.content = ''.join(new_lines)
    
    def fix_import_indentation(self):
        """修复导入语句的缩进"""
        # 检测在try块外的导入语句，应该在try块内
        pattern = r'(try:\s*\n\s*from mcp\.server.*?\n)(from mcp_servers\.utils\.mcp_integration_helper)'
        
        if re.search(pattern, self.content, re.DOTALL):
            # 修复：在try块内的导入应该有缩进
            def fix_import(match):
                try_block = match.group(1)
                import_stmt = match.group(2)
                # 计算try块的缩进
                try_indent = len(try_block.split('\n')[-2]) - len(try_block.split('\n')[-2].lstrip())
                return try_block + ' ' * (try_indent + 4) + import_stmt
            
            self.content = re.sub(pattern, fix_import, self.content, flags=re.DOTALL)
            self.fixes_applied.append("修复导入语句缩进")
    
    def verify_adapter_function(self):
        """验证并添加适配函数（如果需要）"""
        # 检查是否使用了process_mcp_tool_call但缺少适配函数
        if 'process_mcp_tool_call' in self.content and '_adapt_mcp_result_to_text_content' not in self.content:
            # 检查是否返回List[TextContent]
            if 'List[TextContent]' in self.content or '-> List[TextContent]' in self.content:
                # 需要添加适配函数
                adapter_func = '''
def _adapt_mcp_result_to_text_content(result: Dict[str, Any]) -> List[TextContent]:
    """将process_mcp_tool_call的结果转换为List[TextContent]格式"""
    if isinstance(result, dict) and "content" in result:
        text_content = []
        for item in result.get("content", []):
            if item.get("type") == "text":
                text_content.append(TextContent(type="text", text=item.get("text", "")))
        return text_content if text_content else [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
    else:
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

'''
                # 在@server.call_tool()之前插入
                pattern = r'(@server\.call_tool\(\)\s*\n\s*async def call_tool)'
                if re.search(pattern, self.content):
                    self.content = re.sub(pattern, adapter_func + r'\1', self.content)
                    self.fixes_applied.append("添加适配函数 _adapt_mcp_result_to_text_content")


def fix_mcp_server(file_path: str) -> Dict[str, Any]:
    """修复MCP服务器文件"""
    path = Path(file_path)
    if not path.exists():
        return {"error": f"文件不存在: {file_path}"}
    
    fixer = MCPIntegrationFixer(path)
    result = fixer.fix_all()
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python mcp_integration_fixer.py <server_file>")
        sys.exit(1)
    
    result = fix_mcp_server(sys.argv[1])
    if result.get("fixed"):
        print(f"✅ 已修复: {result['file']}")
        print(f"   修复项: {', '.join(result['fixes'])}")
    else:
        print(f"ℹ️  无需修复: {result['file']}")
