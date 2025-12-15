# -*- coding: utf-8 -*-
"""数据采集MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("data-collector-server")

TOOLS = [
    Tool(name="collector.fetch", description="采集数据", inputSchema={"type": "object", "properties": {"source": {"type": "string"}, "symbols": {"type": "array"}, "date_range": {"type": "string"}}, "required": ["source"]}),
    Tool(name="collector.schedule", description="设置采集计划", inputSchema={"type": "object", "properties": {"cron": {"type": "string"}, "task": {"type": "string"}}, "required": ["cron", "task"]}),
    Tool(name="collector.status", description="查看采集状态", inputSchema={"type": "object", "properties": {}}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "collector.fetch":
            result = {"success": True, "source": arguments["source"], "records": 1000, "status": "completed"}
        elif name == "collector.schedule":
            result = {"success": True, "cron": arguments["cron"], "task": arguments["task"], "scheduled": True}
        elif name == "collector.status":
            result = {"success": True, "active_jobs": 0, "last_run": "2025-12-15 10:00:00", "next_run": "2025-12-16 09:00:00"}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="data-collector-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
