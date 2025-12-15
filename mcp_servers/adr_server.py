# -*- coding: utf-8 -*-
"""架构决策记录MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from datetime import datetime
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("adr-server")
_adr_store = []

TOOLS = [
    Tool(name="adr.create", description="创建架构决策记录", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "context": {"type": "string"}, "decision": {"type": "string"}, "consequences": {"type": "string"}}, "required": ["title", "decision"]}),
    Tool(name="adr.list", description="列出所有ADR", inputSchema={"type": "object", "properties": {}}),
    Tool(name="adr.get", description="获取ADR详情", inputSchema={"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "adr.create":
            adr = {"id": len(_adr_store)+1, "title": arguments["title"], "context": arguments.get("context", ""), "decision": arguments["decision"], "consequences": arguments.get("consequences", ""), "date": datetime.now().isoformat(), "status": "accepted"}
            _adr_store.append(adr)
            result = {"success": True, "adr_id": adr["id"]}
        elif name == "adr.list":
            result = {"success": True, "count": len(_adr_store), "adrs": [{"id": a["id"], "title": a["title"], "status": a["status"]} for a in _adr_store]}
        elif name == "adr.get":
            adr_id = arguments["id"]
            adr = next((a for a in _adr_store if a["id"] == adr_id), None)
            if adr:
                result = {"success": True, **adr}
            else:
                result = {"success": False, "error": f"ADR不存在: {adr_id}"}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="adr-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
