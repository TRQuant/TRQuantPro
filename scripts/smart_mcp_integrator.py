#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能MCP服务器集成脚本
====================

避免常见错误的集成方法：
1. 分析现有代码结构
2. 智能插入代码而不是替换
3. 自动验证语法
4. 处理各种边界情况
"""

import re
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional

class SmartMCPIntegrator:
    """智能MCP服务器集成器"""
    
    def __init__(self, server_file: Path):
        self.server_file = server_file
        with open(server_file, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
            self.content = ''.join(self.lines)
    
    def analyze_structure(self) -> dict:
        """分析代码结构"""
        structure = {
            'has_mcp_sdk': 'from mcp.server import Server' in self.content,
            'has_envelope': 'from mcp_servers.utils.envelope import' in self.content,
            'has_integration_helper': 'process_mcp_tool_call' in self.content and 'tool_handlers' in self.content,
            'has_adapter': '_adapt_mcp_result_to_text_content' in self.content,
            'call_tool_start': None,
            'call_tool_end': None,
            'tools': [],
            'has_nested_try': False,
            'has_async_handlers': False,
        }
        
        # 查找call_tool方法
        for i, line in enumerate(self.lines):
            if '@server.call_tool()' in line:
                structure['call_tool_start'] = i
            if structure['call_tool_start'] and 'async def main' in line:
                structure['call_tool_end'] = i
                break
        
        # 查找工具
        if structure['call_tool_start']:
            start_idx = structure['call_tool_start']
            end_idx = structure['call_tool_end'] or len(self.lines)
            call_tool_section = ''.join(self.lines[start_idx:end_idx])
            tools = re.findall(r'name == "([^"]+)"', call_tool_section)
            structure['tools'] = tools
        
        # 检查是否有嵌套try或async处理函数
        if structure['call_tool_start']:
            start_idx = structure['call_tool_start']
            end_idx = structure['call_tool_end'] or len(self.lines)
            section = ''.join(self.lines[start_idx:end_idx])
            structure['has_nested_try'] = section.count('try:') > 1
            structure['has_async_handlers'] = 'async def _handle_' in section or 'async def handle_' in section
        
        return structure
    
    def verify_syntax(self) -> Tuple[bool, Optional[str]]:
        """验证语法"""
        result = subprocess.run(
            ['python3', '-m', 'py_compile', str(self.server_file)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python smart_mcp_integrator.py <server_file>")
        sys.exit(1)
    
    server_file = Path(sys.argv[1])
    integrator = SmartMCPIntegrator(server_file)
    
    print(f"分析 {server_file.name}...")
    structure = integrator.analyze_structure()
    print(f"结构: {structure}")
    
    ok, error = integrator.verify_syntax()
    if ok:
        print("✅ 语法检查通过")
    else:
        print(f"❌ 语法错误: {error}")
