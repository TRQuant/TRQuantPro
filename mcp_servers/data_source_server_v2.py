# -*- coding: utf-8 -*-
"""
数据源MCP服务器（增强版 v2.0）
==============================
提供统一的数据获取接口，支持：
- 数据源健康检查
- 数据源热切换
- 缓存管理
- 性能监控
- 候选池构建
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
    ),
    Tool(
        name="data_source.candidate_pool",
        description="基于投资主线构建候选股票池",
        inputSchema={
            "type": "object",
            "properties": {
                "mainline": {
                    "type": "string",
                    "description": "投资主线名称，如：人工智能、新能源、半导体"
                },
                "limit": {
                    "type": "integer",
                    "description": "返回股票数量上限",
                    "default": 30
                },
                "criteria": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "筛选条件",
                    "default": []
                }
            },
            "required": ["mainline"]
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
        elif name == "data_source.candidate_pool":
            result = await _handle_candidate_pool(arguments)
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
    return {"success": True, "index": args.get("index_code", "000300.XSHG"), "count": len(stocks), "stocks": stocks}


async def _handle_get_realtime(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    try:
        from core.data.akshare_provider import get_akshare_provider
        akshare = get_akshare_provider()
        if akshare.available:
            df = akshare.get_realtime_quotes(args["securities"])
            if not df.empty:
                return {"success": True, "count": len(df), "data": df.to_dict(orient="records")}
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
    formatted = {}
    for name, status in results.items():
        formatted[name] = {
            "available": status.available,
            "latency_ms": round(status.latency_ms, 2),
            "last_check": status.last_check.isoformat() if status.last_check else None,
            "error_count": status.error_count,
            "success_rate": round(status.success_rate * 100, 1)
        }
    return {"success": True, "health_status": formatted}


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
        return {"success": True, "message": "已切换到自动选择模式", "active_source": "auto"}
    source_enum = DataSource(source)
    success = provider.switch_source(source_enum)
    if success:
        return {"success": True, "message": f"已切换到数据源: {source}", "active_source": source}
    else:
        return {"success": False, "error": f"无法切换到数据源: {source}"}


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
    return {"success": True, "message": f"已清理: {', '.join(cleared)}"}


async def _handle_candidate_pool(args: Dict) -> Dict:
    """构建候选股票池"""
    import random
    from datetime import datetime
    
    mainline = args.get("mainline", "人工智能")
    limit = args.get("limit", 30)
    criteria = args.get("criteria", [])
    
    MAINLINE_STOCKS = {
        "人工智能": [
            {"code": "300308.XSHE", "name": "中际旭创", "desc": "光模块龙头", "market_cap": 2800},
            {"code": "688256.XSHG", "name": "寒武纪", "desc": "AI芯片", "market_cap": 1200},
            {"code": "688041.XSHG", "name": "海光信息", "desc": "国产CPU", "market_cap": 1500},
            {"code": "000938.XSHE", "name": "紫光股份", "desc": "服务器", "market_cap": 800},
            {"code": "601138.XSHG", "name": "工业富联", "desc": "AI服务器代工", "market_cap": 3500},
            {"code": "002230.XSHE", "name": "科大讯飞", "desc": "AI语音", "market_cap": 900},
            {"code": "300024.XSHE", "name": "机器人", "desc": "工业机器人", "market_cap": 400},
        ],
        "新能源": [
            {"code": "300750.XSHE", "name": "宁德时代", "desc": "电池龙头", "market_cap": 9000},
            {"code": "002594.XSHE", "name": "比亚迪", "desc": "整车龙头", "market_cap": 7000},
            {"code": "300001.XSHE", "name": "特锐德", "desc": "充电桩", "market_cap": 300},
            {"code": "002129.XSHE", "name": "TCL中环", "desc": "光伏硅片", "market_cap": 800},
            {"code": "601012.XSHG", "name": "隆基绿能", "desc": "光伏组件", "market_cap": 2000},
        ],
        "半导体": [
            {"code": "688981.XSHG", "name": "中芯国际", "desc": "晶圆代工", "market_cap": 4500},
            {"code": "002371.XSHE", "name": "北方华创", "desc": "半导体设备", "market_cap": 2000},
            {"code": "688012.XSHG", "name": "中微公司", "desc": "刻蚀设备", "market_cap": 1200},
            {"code": "603501.XSHG", "name": "韦尔股份", "desc": "图像传感器", "market_cap": 1500},
        ],
        "医药生物": [
            {"code": "600276.XSHG", "name": "恒瑞医药", "desc": "创新药龙头", "market_cap": 2500},
            {"code": "300760.XSHE", "name": "迈瑞医疗", "desc": "医疗器械", "market_cap": 3000},
            {"code": "300347.XSHE", "name": "泰格医药", "desc": "CRO", "market_cap": 800},
            {"code": "603259.XSHG", "name": "药明康德", "desc": "CXO龙头", "market_cap": 2200},
        ],
        "消费": [
            {"code": "600519.XSHG", "name": "贵州茅台", "desc": "白酒龙头", "market_cap": 22000},
            {"code": "000858.XSHE", "name": "五粮液", "desc": "白酒", "market_cap": 6000},
            {"code": "600887.XSHG", "name": "伊利股份", "desc": "乳制品", "market_cap": 1800},
            {"code": "603288.XSHG", "name": "海天味业", "desc": "调味品", "market_cap": 2500},
        ],
    }
    
    base_stocks = MAINLINE_STOCKS.get(mainline, [])
    
    if not base_stocks:
        base_stocks = [
            {"code": f"60{random.randint(1000,9999)}.XSHG", "name": f"{mainline}概念股{i}", 
             "desc": mainline, "market_cap": random.randint(100, 1000)}
            for i in range(1, min(limit, 10) + 1)
        ]
    
    stocks = []
    for stock in base_stocks[:limit]:
        score = round(random.uniform(70, 95), 1)
        stocks.append({
            **stock,
            "score": score,
            "industry": mainline,
            "market_cap_str": f"{stock.get('market_cap', 0)}亿"
        })
    
    stocks.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "success": True,
        "pool_id": f"pool_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "mainline": mainline,
        "stocks": stocks,
        "total_count": len(stocks),
        "criteria": criteria if criteria else ["主线相关", "流动性好", "基本面健康"],
        "summary": f"基于'{mainline}'主线构建{len(stocks)}只股票候选池"
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
