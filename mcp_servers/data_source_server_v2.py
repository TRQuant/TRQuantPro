# -*- coding: utf-8 -*-
"""
数据源MCP服务器（增强版 v2.0）
==============================
提供统一的数据获取接口，支持：
- 数据源健康检查
- 数据源热切换
- 缓存管理
- 性能监控
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("data-source-server-v2")


TOOLS = [
    # 基础数据获取
    Tool(
        name="data_source.get_price",
        description="获取股票历史价格数据",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "start_date": {"type": "string", "description": "开始日期 YYYY-MM-DD"},
                "end_date": {"type": "string", "description": "结束日期 YYYY-MM-DD"},
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
        name="data_source.get_index_stocks",
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
        name="data_source.get_realtime",
        description="获取实时行情",
        inputSchema={
            "type": "object",
            "properties": {
                "securities": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["securities"]
        }
    ),
    # 健康检查
    Tool(
        name="data_source.health_check",
        description="执行数据源健康检查",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "指定数据源: jqdata/akshare/mock，不指定则检查全部",
                    "enum": ["jqdata", "akshare", "mock"]
                }
            }
        }
    ),
    Tool(
        name="data_source.status",
        description="获取数据源状态和统计信息",
        inputSchema={"type": "object", "properties": {}}
    ),
    # 热切换
    Tool(
        name="data_source.switch",
        description="切换数据源",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "目标数据源: jqdata/akshare/mock/auto",
                    "enum": ["jqdata", "akshare", "mock", "auto"]
                }
            },
            "required": ["source"]
        }
    ),
    # 缓存管理
    Tool(
        name="data_source.cache_stats",
        description="获取缓存统计信息",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="data_source.clear_cache",
        description="清理缓存",
        inputSchema={
            "type": "object",
            "properties": {
                "memory": {"type": "boolean", "description": "清理内存缓存", "default": True},
                "disk": {"type": "boolean", "description": "清理磁盘缓存", "default": False}
            }
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "data_source.get_price":
            result = await _handle_get_price(arguments)
        elif name == "data_source.get_index_stocks":
            result = await _handle_get_index_stocks(arguments)
        elif name == "data_source.get_realtime":
            result = await _handle_get_realtime(arguments)
        elif name == "data_source.health_check":
            result = await _handle_health_check(arguments)
        elif name == "data_source.status":
            result = await _handle_status()
        elif name == "data_source.switch":
            result = await _handle_switch(arguments)
        elif name == "data_source.cache_stats":
            result = await _handle_cache_stats()
        elif name == "data_source.clear_cache":
            result = await _handle_clear_cache(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


def _get_provider():
    """获取数据提供者"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    from core.data import get_data_provider_v2, DataRequest, DataSource
    return get_data_provider_v2(), DataRequest, DataSource


async def _handle_get_price(args: Dict) -> Dict:
    provider, DataRequest, _ = _get_provider()
    
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
            "fetch_time_ms": round(response.fetch_time_ms, 2),
            "count": len(response.data),
            "columns": list(response.data.columns),
            "preview": response.data.head(5).to_dict(orient="records")
        }
    else:
        return {"success": False, "error": response.error}


async def _handle_get_index_stocks(args: Dict) -> Dict:
    provider, _, _ = _get_provider()
    
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
        akshare = get_akshare_provider()
        
        if akshare.available:
            df = akshare.get_realtime_quotes(args["securities"])
            if not df.empty:
                return {
                    "success": True,
                    "count": len(df),
                    "data": df.to_dict(orient="records")
                }
    except:
        pass
    
    return {"success": False, "error": "实时数据获取失败"}


async def _handle_health_check(args: Dict) -> Dict:
    provider, _, DataSource = _get_provider()
    
    source = args.get("source")
    if source:
        source_enum = DataSource(source)
        results = provider.health_check(source_enum)
    else:
        results = provider.health_check()
    
    # 转换为可序列化格式
    formatted = {}
    for name, status in results.items():
        formatted[name] = {
            "available": status.available,
            "latency_ms": round(status.latency_ms, 2),
            "last_check": status.last_check.isoformat() if status.last_check else None,
            "error_count": status.error_count,
            "success_rate": round(status.success_rate * 100, 1)
        }
    
    return {
        "success": True,
        "health_status": formatted
    }


async def _handle_status() -> Dict:
    provider, _, _ = _get_provider()
    
    stats = provider.get_stats()
    health = provider.get_health_status()
    
    return {
        "success": True,
        "active_source": stats["active_source"],
        "sources": stats["sources_available"],
        "health": health,
        "stats": {
            "total_requests": stats["total_requests"],
            "cache_hits": stats["cache_hits"],
            "cache_hit_rate": f"{stats['cache_hit_rate']*100:.1f}%",
            "avg_fetch_time_ms": f"{stats['avg_fetch_time_ms']:.2f}ms",
            "errors": stats.get("errors", 0)
        }
    }


async def _handle_switch(args: Dict) -> Dict:
    provider, _, DataSource = _get_provider()
    
    source = args["source"]
    
    if source == "auto":
        provider.reset_source()
        return {
            "success": True,
            "message": "已切换到自动选择模式",
            "active_source": "auto"
        }
    
    source_enum = DataSource(source)
    success = provider.switch_source(source_enum)
    
    if success:
        return {
            "success": True,
            "message": f"已切换到数据源: {source}",
            "active_source": source
        }
    else:
        return {
            "success": False,
            "error": f"无法切换到数据源: {source}，请检查数据源是否可用"
        }


async def _handle_cache_stats() -> Dict:
    provider, _, _ = _get_provider()
    
    stats = provider.get_stats()
    
    return {
        "success": True,
        "total_requests": stats["total_requests"],
        "cache_hits": stats["cache_hits"],
        "jqdata_calls": stats.get("jqdata_calls", 0),
        "akshare_calls": stats.get("akshare_calls", 0),
        "mock_calls": stats.get("mock_calls", 0),
        "cache_hit_rate": f"{stats['cache_hit_rate']*100:.1f}%",
        "avg_fetch_time_ms": f"{stats['avg_fetch_time_ms']:.2f}ms"
    }


async def _handle_clear_cache(args: Dict) -> Dict:
    provider, _, _ = _get_provider()
    
    memory = args.get("memory", True)
    disk = args.get("disk", False)
    
    provider.clear_cache(memory=memory, disk=disk)
    
    cleared = []
    if memory:
        cleared.append("内存缓存")
    if disk:
        cleared.append("磁盘缓存")
    
    return {
        "success": True,
        "message": f"已清理: {', '.join(cleared)}"
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="data-source-server-v2",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
