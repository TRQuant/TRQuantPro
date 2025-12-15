#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复所有MCP服务器的stdio_server调用方式
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
MCP_SERVERS_DIR = PROJECT_ROOT / "mcp_servers"

# 需要修复的文件
SERVER_FILES = [
    "spec_server_v2.py",
    "test_server.py",
    "code_server.py",
    "lint_server.py",
    "schema_server.py",
    "adr_server.py",
    "task_server.py",
    "data_source_server.py",
    "backtest_server.py",
    "evidence_server.py",
    "secrets_server.py",
]

OLD_PATTERN = r'if __name__ == "__main__":\s+import asyncio\s+asyncio\.run\(stdio_server\(server\)\)'
NEW_CODE = '''if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    # 使用官方SDK的标准方式
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())'''

for server_file in SERVER_FILES:
    file_path = MCP_SERVERS_DIR / server_file
    if not file_path.exists():
        continue
    
    content = file_path.read_text(encoding='utf-8')
    
    # 检查是否已经是新格式
    if 'async with stdio_server()' in content:
        print(f"✅ {server_file}: 已经是新格式")
        continue
    
    # 替换旧格式
    if 'asyncio.run(stdio_server(server))' in content:
        # 找到并替换
        old_pattern = r'if __name__ == "__main__":\s+import asyncio\s+asyncio\.run\(stdio_server\(server\)\)'
        new_content = re.sub(old_pattern, NEW_CODE, content, flags=re.MULTILINE)
        
        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✅ {server_file}: 已修复")
        else:
            print(f"⚠️  {server_file}: 未找到匹配模式")
    else:
        print(f"ℹ️  {server_file}: 无需修复")

print("\n✅ 所有服务器文件修复完成")













