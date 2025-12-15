# -*- coding: utf-8 -*-
"""代码分析MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from pathlib import Path
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("code-server")

TOOLS = [
    Tool(name="code.analyze", description="分析策略代码", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="code.lint", description="检查代码规范", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="code.convert", description="转换代码格式", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "target_platform": {"type": "string"}}, "required": ["code", "target_platform"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        code = arguments.get("code", "")
        if name == "code.analyze":
            lines = code.count('\n') + 1
            has_init = "def initialize" in code
            has_handle = "def handle_data" in code or "def market_open" in code
            result = {"success": True, "lines": lines, "has_initialize": has_init, "has_handler": has_handle, "valid_structure": has_init}
        elif name == "code.lint":
            issues = []
            if "import *" in code: issues.append("避免使用 import *")
            if "print(" in code: issues.append("建议使用 log 替代 print")
            result = {"success": True, "issues": issues, "passed": len(issues) == 0}
        elif name == "code.convert":
            platform = arguments.get("target_platform", "ptrade")
            converted = code.replace("from jqdata import *", "# PTrade不需要jqdata导入")
            result = {"success": True, "platform": platform, "converted": converted[:500]}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="code-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
