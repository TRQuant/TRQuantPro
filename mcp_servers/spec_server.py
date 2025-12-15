# -*- coding: utf-8 -*-
"""规范MCP服务器（标准化版本）"""
import logging, json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("spec-server")

SPECS = {
    "naming": {"rule": "使用snake_case命名", "examples": ["get_price", "calculate_momentum"]},
    "structure": {"rule": "策略必须包含initialize和handler函数", "examples": ["def initialize(context):", "def handle_data(context, data):"]},
    "risk": {"rule": "必须设置止损", "examples": ["stop_loss = 0.08"]},
}

TOOLS = [
    Tool(name="spec.list", description="列出所有规范", inputSchema={"type": "object", "properties": {}}),
    Tool(name="spec.get", description="获取规范详情", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="spec.check", description="检查是否符合规范", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "specs": {"type": "array"}}, "required": ["code"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "spec.list":
            result = {"success": True, "specs": list(SPECS.keys())}
        elif name == "spec.get":
            spec_name = arguments["name"]
            if spec_name in SPECS:
                result = {"success": True, "name": spec_name, **SPECS[spec_name]}
            else:
                result = {"success": False, "error": f"规范不存在: {spec_name}"}
        elif name == "spec.check":
            code = arguments["code"]
            violations = []
            if "def initialize" not in code: violations.append("structure: 缺少initialize函数")
            if "stop_loss" not in code.lower(): violations.append("risk: 未设置止损")
            result = {"success": True, "compliant": len(violations) == 0, "violations": violations}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(server_name="spec-server", server_version="2.0.0"))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
