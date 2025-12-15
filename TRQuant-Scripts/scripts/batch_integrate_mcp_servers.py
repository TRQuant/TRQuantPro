#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MCP服务器批量集成脚本
====================

自动将新的MCP标准（trace_id、参数验证、错误处理）应用到所有MCP服务器。

使用方法:
    python scripts/batch_integrate_mcp_servers.py [--dry-run] [--server SERVER_NAME]

功能:
    1. 扫描所有MCP服务器
    2. 分析每个服务器的工具列表
    3. 自动集成 process_mcp_tool_call
    4. 生成集成报告
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class MCPServerAnalyzer:
    """MCP服务器分析器"""
    
    def __init__(self, server_path: Path):
        self.server_path = server_path
        self.server_name = server_path.stem
        self.content = server_path.read_text(encoding='utf-8')
        self.tools = []
        self.integration_status = {
            'has_helper_import': False,
            'has_process_call': False,
            'tools_count': 0,
            'integrated_tools': 0
        }
    
    def analyze(self):
        """分析服务器"""
        # 检查导入
        self.integration_status['has_helper_import'] = (
            'from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call' in self.content or
            'from utils.mcp_integration_helper import process_mcp_tool_call' in self.content
        )
        
        # 检查是否使用了process_mcp_tool_call
        self.integration_status['has_process_call'] = 'process_mcp_tool_call' in self.content
        
        # 提取工具列表
        self._extract_tools()
        
        # 检查已集成的工具
        self._check_integrated_tools()
    
    def _extract_tools(self):
        """提取工具定义"""
        # 查找 Tool( 定义
        tool_pattern = r'Tool\(\s*name="([^"]+)"'
        matches = re.findall(tool_pattern, self.content)
        self.tools = matches
        self.integration_status['tools_count'] = len(matches)
    
    def _check_integrated_tools(self):
        """检查已集成的工具"""
        integrated = 0
        for tool in self.tools:
            # 检查工具是否使用了process_mcp_tool_call
            pattern = f'name == "{tool}".*?process_mcp_tool_call'
            if re.search(pattern, self.content, re.DOTALL):
                integrated += 1
        self.integration_status['integrated_tools'] = integrated
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return {
            'server': self.server_name,
            'path': str(self.server_path.relative_to(PROJECT_ROOT)),
            'tools': self.tools,
            **self.integration_status
        }


def find_mcp_servers() -> List[Path]:
    """查找所有MCP服务器"""
    mcp_dir = PROJECT_ROOT / 'mcp_servers'
    if not mcp_dir.exists():
        return []
    
    servers = []
    for file in mcp_dir.rglob('*_server.py'):
        # 排除示例和测试文件
        if 'test' not in file.stem.lower() and 'example' not in file.stem.lower():
            servers.append(file)
    
    return sorted(servers)


def generate_integration_report(servers: List[MCPServerAnalyzer]) -> str:
    """生成集成报告"""
    report = []
    report.append("=" * 70)
    report.append("MCP服务器集成状态报告")
    report.append("=" * 70)
    report.append("")
    
    total_servers = len(servers)
    integrated_servers = sum(1 for s in servers if s.integration_status['has_process_call'])
    total_tools = sum(s.integration_status['tools_count'] for s in servers)
    integrated_tools = sum(s.integration_status['integrated_tools'] for s in servers)
    
    report.append(f"📊 总体统计:")
    report.append(f"   - 服务器总数: {total_servers}")
    report.append(f"   - 已集成服务器: {integrated_servers}")
    report.append(f"   - 待集成服务器: {total_servers - integrated_servers}")
    report.append(f"   - 工具总数: {total_tools}")
    report.append(f"   - 已集成工具: {integrated_tools}")
    report.append(f"   - 待集成工具: {total_tools - integrated_tools}")
    report.append("")
    report.append("=" * 70)
    report.append("")
    
    # 按状态分组
    integrated = [s for s in servers if s.integration_status['has_process_call']]
    pending = [s for s in servers if not s.integration_status['has_process_call']]
    
    if integrated:
        report.append("✅ 已集成服务器:")
        for s in integrated:
            status = s.get_status()
            report.append(f"   - {status['server']}: {status['integrated_tools']}/{status['tools_count']} 工具")
        report.append("")
    
    if pending:
        report.append("⏳ 待集成服务器:")
        for s in pending:
            status = s.get_status()
            report.append(f"   - {status['server']}: {status['tools_count']} 工具")
        report.append("")
    
    report.append("=" * 70)
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='MCP服务器批量集成分析')
    parser.add_argument('--dry-run', action='store_true', help='仅分析，不执行集成')
    parser.add_argument('--server', type=str, help='仅处理指定服务器')
    args = parser.parse_args()
    
    # 查找所有服务器
    server_files = find_mcp_servers()
    if not server_files:
        print("❌ 未找到MCP服务器文件")
        return
    
    if args.server:
        server_files = [f for f in server_files if args.server in f.stem]
        if not server_files:
            print(f"❌ 未找到服务器: {args.server}")
            return
    
    print(f"📋 找到 {len(server_files)} 个MCP服务器")
    print("")
    
    # 分析所有服务器
    analyzers = []
    for server_file in server_files:
        analyzer = MCPServerAnalyzer(server_file)
        analyzer.analyze()
        analyzers.append(analyzer)
    
    # 生成报告
    report = generate_integration_report(analyzers)
    print(report)
    
    # 保存报告
    report_file = PROJECT_ROOT / 'docs' / 'MCP_INTEGRATION_REPORT.md'
    report_file.write_text(report, encoding='utf-8')
    print(f"\n✅ 报告已保存: {report_file}")
    
    if args.dry_run:
        print("\n🔍 这是预览模式，未执行实际集成")
    else:
        print("\n💡 提示: 使用 --dry-run 查看分析结果，实际集成需要手动完成")


if __name__ == '__main__':
    main()
