#!/usr/bin/env python3
"""
批量修复MCP服务器，使其使用process_mcp_tool_call
"""
import sys
from pathlib import Path
import re
import ast
import json

TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

def fix_factor_server():
    """修复factor_server.py"""
    server_file = TRQUANT_ROOT / "mcp_servers" / "factor_server.py"
    content = server_file.read_text(encoding='utf-8')
    
    # 检查是否已经有适配函数
    if '_adapt_mcp_result_to_text_content' not in content:
        # 添加适配函数
        adapter_func = '''
def _adapt_mcp_result_to_text_content(result: Dict[str, Any]) -> List[TextContent]:
    """将process_mcp_tool_call的结果转换为List[TextContent]"""
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
        if re.search(pattern, content):
            content = re.sub(pattern, adapter_func + r'\1', content)
    
    # 修复call_tool方法 - 将每个工具的处理逻辑包装在handler中
    # 这是一个复杂的替换，需要找到每个if/elif块并重构
    
    print(f"✅ factor_server.py: 需要手动重构call_tool方法")
    return False

def analyze_server_structure(server_file: Path):
    """分析服务器结构"""
    content = server_file.read_text(encoding='utf-8')
    
    info = {
        "file": server_file.name,
        "has_import": 'from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call' in content,
        "uses_process": 'process_mcp_tool_call(' in content,
        "has_adapter": '_adapt_mcp_result_to_text_content' in content,
        "is_standard_format": '@server.call_tool()' in content,
        "is_class_format": bool(re.search(r'class\s+\w+.*Server', content)),
        "tool_count": len(set(re.findall(r'name\s*==\s*"([^"]+)"', content)))
    }
    
    return info

if __name__ == "__main__":
    servers = [
        "kb_server.py",
        "factor_server.py",
        "data_quality_server.py",
        "engineering_server.py",
        "report_server.py",
        "schema_server.py",
        "strategy_kb_server.py",
        "strategy_template_server.py",
        "trading_server.py",
        "workflow_server.py"
    ]
    
    print("=" * 70)
    print("MCP服务器结构分析")
    print("=" * 70)
    
    for server_name in servers:
        server_file = TRQUANT_ROOT / "mcp_servers" / server_name
        if not server_file.exists():
            continue
        
        info = analyze_server_structure(server_file)
        print(f"\n{info['file']}:")
        print(f"  格式: {'标准' if info['is_standard_format'] else '类' if info['is_class_format'] else '未知'}")
        print(f"  工具数: {info['tool_count']}")
        print(f"  已导入: {info['has_import']}")
        print(f"  已使用: {info['uses_process']}")
        print(f"  有适配函数: {info['has_adapter']}")
    
    print("\n" + "=" * 70)
    print("由于每个服务器结构不同，建议:")
    print("1. 使用lint.fix_mcp_integration工具逐个修复")
    print("2. 或手动重构每个服务器的call_tool方法")
    print("=" * 70)
