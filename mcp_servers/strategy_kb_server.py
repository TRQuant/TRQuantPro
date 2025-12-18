# -*- coding: utf-8 -*-
"""策略知识库MCP服务器（标准化版本）"""
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
logger = logging.getLogger('StrategyKbServer')

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

server = Server("strategy-kb-server")

STRATEGY_KB = {
    "momentum": {"description": "动量策略追踪近期表现强势的股票", "params": ["period", "top_n"], "risk": "高", "suitable_market": "牛市"},
    "value": {"description": "价值策略寻找被低估的股票", "params": ["pe_max", "pb_max"], "risk": "低", "suitable_market": "熊市"},
    "trend": {"description": "趋势跟踪策略顺应市场趋势", "params": ["fast_ma", "slow_ma"], "risk": "中", "suitable_market": "趋势市"},
    "rotation": {"description": "行业轮动策略在不同行业间切换", "params": ["rotation_period", "sectors"], "risk": "中", "suitable_market": "震荡市"},
}

TOOLS = [
    Tool(name="skb.list", description="列出策略知识", inputSchema={"type": "object", "properties": {}}),
    Tool(name="skb.get", description="获取策略详情", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="skb.recommend", description="推荐策略", inputSchema={"type": "object", "properties": {"market_state": {"type": "string"}, "risk_level": {"type": "string"}}}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "skb.list":
            result = {"success": True, "strategies": list(STRATEGY_KB.keys())}
        elif name == "skb.get":
            strategy = arguments["name"]
            if strategy in STRATEGY_KB:
                result = {"success": True, "name": strategy, **STRATEGY_KB[strategy]}
            else:
                result = {"success": False, "error": f"策略不存在: {strategy}"}
        elif name == "skb.recommend":
            market = arguments.get("market_state", "neutral")
            risk = arguments.get("risk_level", "medium")
            recommendations = {"bull": ["momentum", "trend"], "bear": ["value"], "neutral": ["rotation", "value"]}
            result = {"success": True, "market": market, "recommendations": recommendations.get(market, ["value"])}
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
