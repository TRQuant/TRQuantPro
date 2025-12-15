# -*- coding: utf-8 -*-
"""密钥管理MCP服务器（标准化版本）"""
import logging, json, os
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("secrets-server")

TOOLS = [
    Tool(name="secrets.list", description="列出可用密钥名称", inputSchema={"type": "object", "properties": {}}),
    Tool(name="secrets.get", description="获取密钥值（仅返回是否存在）", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="secrets.set", description="设置密钥", inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "value": {"type": "string"}}, "required": ["name", "value"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "secrets.list":
            keys = [k for k in os.environ.keys() if any(x in k.upper() for x in ["KEY", "TOKEN", "SECRET", "PASSWORD", "JQDATA"])]
            result = {"success": True, "count": len(keys), "keys": keys[:10]}
        elif name == "secrets.get":
            key_name = arguments["name"]
            exists = key_name in os.environ
            result = {"success": True, "name": key_name, "exists": exists, "value": "***" if exists else None}
        elif name == "secrets.set":
            os.environ[arguments["name"]] = arguments["value"]
            result = {"success": True, "name": arguments["name"], "message": "密钥已设置"}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="secrets-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
