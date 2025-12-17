# -*- coding: utf-8 -*-
"""MCP服务器（标准化版本）"""
import sys
import logging
import json
from pathlib import Path
from typing import Dict, List, Any

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('SchemaServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}")
    sys.exit(1)

server = Server("schema-server")

# 数据模型定义
SCHEMAS = {
    "stock": {
        "fields": ["code", "name", "price", "volume", "market_cap"],
        "types": {"code": "string", "name": "string", "price": "float", "volume": "int", "market_cap": "float"}
    },
    "backtest_result": {
        "fields": ["total_return", "annual_return", "sharpe_ratio", "max_drawdown", "win_rate"],
        "types": {"total_return": "float", "annual_return": "float", "sharpe_ratio": "float", "max_drawdown": "float", "win_rate": "float"}
    },
    "strategy": {
        "fields": ["name", "type", "params", "code"],
        "types": {"name": "string", "type": "string", "params": "object", "code": "string"}
    },
    "factor": {
        "fields": ["name", "category", "value", "rank"],
        "types": {"name": "string", "category": "string", "value": "float", "rank": "int"}
    }
}

TOOLS = [
    Tool(name="schema.list", description="列出所有数据模型", inputSchema={"type": "object", "properties": {}}),
    Tool(name="schema.get", description="获取数据模型定义", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="schema.validate", description="验证数据是否符合模型", inputSchema={"type": "object", "properties": {"schema_name": {"type": "string"}, "data": {"type": "object"}}, "required": ["schema_name", "data"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "schema.list":
            result = {"success": True, "schemas": list(SCHEMAS.keys())}
        elif name == "schema.get":
            schema_name = arguments["name"]
            if schema_name in SCHEMAS:
                result = {"success": True, "name": schema_name, **SCHEMAS[schema_name]}
            else:
                result = {"success": False, "error": f"模型不存在: {schema_name}"}
        elif name == "schema.validate":
            schema_name = arguments["schema_name"]
            data = arguments["data"]
            if schema_name not in SCHEMAS:
                result = {"success": False, "error": f"模型不存在: {schema_name}"}
            else:
                schema = SCHEMAS[schema_name]
                missing = [f for f in schema["fields"] if f not in data]
                result = {"success": True, "valid": len(missing) == 0, "missing_fields": missing}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
