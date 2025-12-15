# -*- coding: utf-8 -*-
"""代码检查MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("lint-server")

TOOLS = [
    Tool(name="lint.check", description="检查代码质量", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "rules": {"type": "array"}}, "required": ["code"]}),
    Tool(name="lint.fix", description="自动修复问题", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="lint.rules", description="列出检查规则", inputSchema={"type": "object", "properties": {}}),
]

LINT_RULES = ["no-import-star", "use-log-not-print", "define-initialize", "proper-indentation"]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "lint.check":
            code = arguments["code"]
            issues = []
            if "import *" in code: issues.append({"rule": "no-import-star", "message": "避免使用 import *"})
            if "print(" in code: issues.append({"rule": "use-log-not-print", "message": "使用 log 替代 print"})
            if "def initialize" not in code: issues.append({"rule": "define-initialize", "message": "缺少 initialize 函数"})
            result = {"success": True, "issues": issues, "passed": len(issues) == 0}
        elif name == "lint.fix":
            code = arguments["code"]
            fixed = code.replace("print(", "log.info(")
            result = {"success": True, "fixed_code": fixed[:500], "changes": 1 if "print(" in code else 0}
        elif name == "lint.rules":
            result = {"success": True, "rules": LINT_RULES}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="lint-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
