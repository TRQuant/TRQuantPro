# -*- coding: utf-8 -*-
"""证据追踪MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from datetime import datetime
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("evidence-server")
_evidence_store = []

TOOLS = [
    Tool(name="evidence.add", description="添加决策证据", inputSchema={"type": "object", "properties": {"decision": {"type": "string"}, "reason": {"type": "string"}, "data": {"type": "object"}}, "required": ["decision", "reason"]}),
    Tool(name="evidence.list", description="列出证据", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 10}}}),
    Tool(name="evidence.search", description="搜索证据", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "evidence.add":
            evidence = {"id": len(_evidence_store)+1, "decision": arguments["decision"], "reason": arguments["reason"], "data": arguments.get("data", {}), "timestamp": datetime.now().isoformat()}
            _evidence_store.append(evidence)
            result = {"success": True, "evidence_id": evidence["id"]}
        elif name == "evidence.list":
            limit = arguments.get("limit", 10)
            result = {"success": True, "count": len(_evidence_store), "evidence": _evidence_store[-limit:]}
        elif name == "evidence.search":
            query = arguments["query"].lower()
            matches = [e for e in _evidence_store if query in e["decision"].lower() or query in e["reason"].lower()]
            result = {"success": True, "query": query, "matches": matches}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="evidence-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
