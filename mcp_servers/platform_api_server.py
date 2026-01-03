# -*- coding: utf-8 -*-
"""平台API MCP服务器（标准化版本）"""
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
logger = logging.getLogger('PlatformApiServer')

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

server = Server("platform-api-server")

PLATFORM_APIS = {
    "ptrade": {
        "set_slippage": "set_slippage(0.001)",
        "set_commission": "set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))",
        "get_price": "get_history(count, unit='1d', field='close', security_list=stocks)",
        "order": "order_target_value(stock, value)"
    },
    "joinquant": {
        "set_slippage": "set_slippage(FixedSlippage(0.001))",
        "set_commission": "set_order_cost(OrderCost(open_commission=0.0003, close_commission=0.0003, close_tax=0.001, min_commission=5))",
        "get_price": "get_price(securities, start_date, end_date, frequency, fields, panel=False)",
        "order": "order_target_value(stock, value)"
    },
    "qmt": {
        "set_slippage": "ContextInfo.set_slippage(0.001)",
        "set_commission": "ContextInfo.set_commission(0.0003)",
        "get_price": "ContextInfo.get_market_data(['close'], stock_list, start_time, end_time)",
        "order": "order_target_value(stock, value)"
    }
}

TOOLS = [
    Tool(name="api.list_platforms", description="列出支持的平台", inputSchema={"type": "object", "properties": {}}),
    Tool(name="api.get", description="获取平台API", inputSchema={"type": "object", "properties": {"platform": {"type": "string"}, "function": {"type": "string"}}, "required": ["platform"]}),
    Tool(name="api.convert", description="转换API调用", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "from_platform": {"type": "string"}, "to_platform": {"type": "string"}}, "required": ["code", "from_platform", "to_platform"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "api.list_platforms":
            result = {"success": True, "platforms": list(PLATFORM_APIS.keys())}
        elif name == "api.get":
            platform = arguments["platform"]
            if platform not in PLATFORM_APIS:
                result = {"success": False, "error": f"平台不存在: {platform}"}
            else:
                func = arguments.get("function")
                if func:
                    result = {"success": True, "platform": platform, "function": func, "code": PLATFORM_APIS[platform].get(func, "未知函数")}
                else:
                    result = {"success": True, "platform": platform, "apis": PLATFORM_APIS[platform]}
        elif name == "api.convert":
            from_p = arguments["from_platform"]
            to_p = arguments["to_platform"]
            code = arguments["code"]
            # 简单的转换逻辑
            if from_p == "joinquant" and to_p == "ptrade":
                converted = code.replace("from jqdata import *", "# PTrade原生").replace("get_price(", "get_history(")
            else:
                converted = code
            result = {"success": True, "from": from_p, "to": to_p, "converted": converted[:500]}
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
