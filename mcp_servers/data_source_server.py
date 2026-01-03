# -*- coding: utf-8 -*-
"""
数据源MCP服务器（标准化版本）
===========================
提供统一的数据获取接口
"""

import logging
import json
from typing import Dict, List, Any
import sys
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入官方MCP SDK
try:
    from mcp.server.models import InitializationOptions
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    import sys
    print(f'官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}', file=sys.stderr)
    sys.exit(1)

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("data-source-server")


TOOLS = [
    Tool(
        name="data.get_price",
        description="获取股票历史价格数据",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "start_date": {"type": "string", "description": "开始日期"},
                "end_date": {"type": "string", "description": "结束日期"},
                "frequency": {
                    "type": "string",
                    "description": "数据频率: daily/weekly/monthly",
                    "default": "daily"
                }
            },
            "required": ["securities", "start_date", "end_date"]
        }
    ),
    Tool(
        name="data.get_index_stocks",
        description="获取指数成分股",
        inputSchema={
            "type": "object",
            "properties": {
                "index_code": {
                    "type": "string",
                    "description": "指数代码",
                    "default": "000300.XSHG"
                },
                "count": {"type": "integer", "description": "返回数量", "default": 50}
            }
        }
    ),
    Tool(
        name="data.get_realtime",
        description="获取实时行情",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["securities"]
        }
    ),
    Tool(
        name="data.status",
        description="检查数据源状态",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="data.cache_stats",
        description="获取缓存统计信息",
        inputSchema={"type": "object", "properties": {}}
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "data.get_price":
            result = await _handle_get_price(arguments)
        elif name == "data.get_index_stocks":
            result = await _handle_get_index_stocks(arguments)
        elif name == "data.get_realtime":
            result = await _handle_get_realtime(arguments)
        elif name == "data.status":
            result = await _handle_status()
        elif name == "data.cache_stats":
            result = await _handle_cache_stats()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_get_price(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider, DataRequest
    
    provider = get_data_provider()
    request = DataRequest(
        securities=args["securities"],
        start_date=args["start_date"],
        end_date=args["end_date"],
        frequency=args.get("frequency", "daily")
    )
    
    response = provider.get_data(request)
    
    if response.success:
        return {
            "success": True,
            "source": response.source,
            "from_cache": response.from_cache,
            "count": len(response.data),
            "columns": list(response.data.columns),
            "preview": response.data.head(5).to_dict(orient="records")
        }
    else:
        return {"success": False, "error": response.error}


async def _handle_get_index_stocks(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stocks = provider.get_index_stocks(
        args.get("index_code", "000300.XSHG"),
        args.get("count", 50)
    )
    
    return {
        "success": True,
        "index": args.get("index_code", "000300.XSHG"),
        "count": len(stocks),
        "stocks": stocks
    }


async def _handle_get_realtime(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    try:
        from core.data.akshare_provider import get_akshare_provider
        provider = get_akshare_provider()
        
        if provider.available:
            df = provider.get_realtime_quotes(args["securities"])
            if not df.empty:
                return {
                    "success": True,
                    "count": len(df),
                    "data": df.to_dict(orient="records")
                }
    except:
        pass
    
    return {"success": False, "error": "实时数据获取失败"}


async def _handle_status() -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stats = provider.get_stats()
    
    return {
        "success": True,
        "sources": stats["sources_available"],
        "stats": {
            "total_requests": stats["total_requests"],
            "cache_hits": stats["cache_hits"],
            "cache_hit_rate": f"{stats['cache_hit_rate']*100:.1f}%"
        }
    }


async def _handle_cache_stats() -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stats = provider.get_stats()
    
    return {
        "success": True,
        "total_requests": stats["total_requests"],
        "cache_hits": stats["cache_hits"],
        "jqdata_calls": stats.get("jqdata_calls", 0),
        "akshare_calls": stats.get("akshare_calls", 0),
        "mock_calls": stats.get("mock_calls", 0),
        "cache_hit_rate": f"{stats['cache_hit_rate']*100:.1f}%"
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
