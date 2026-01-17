"""
数据源 MCP工具

Author: TRQuant Team
Date: 2025-12-18
"""

from typing import Dict, Any, List
from mcp.types import Tool

from .datasource_manager import (
    get_datasource_manager, DataRequest, DataCategory, DataSourceType
)


DATASOURCE_TOOLS = [
    Tool(
        name="datasource.stats",
        description="获取数据源统计信息",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="datasource.fetch_financial",
        description="获取财务数据",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}},
                "source": {"type": "string", "enum": ["jqdata", "akshare", "mock"]}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.fetch_price",
        description="获取行情数据",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}},
                "source": {"type": "string"}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.fetch_events",
        description="获取事件数据",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.fetch_announcements",
        description="获取公告数据",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.fetch_altdata",
        description="获取另类数据(招投标+招聘)",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.fetch_all",
        description="获取Tenbagger系统所需的全部数据",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="datasource.clear_cache",
        description="清空数据缓存",
        inputSchema={"type": "object", "properties": {}}
    )
]


def _handle_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    return {"status": "success", **manager.get_stats()}


def _handle_fetch_financial(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    source = args.get("source")
    
    source_type = None
    if source:
        source_map = {"jqdata": DataSourceType.JQDATA, "akshare": DataSourceType.AKSHARE, "mock": DataSourceType.MOCK}
        source_type = source_map.get(source)
    
    request = DataRequest(category=DataCategory.FINANCIAL, symbols=symbols)
    response = manager.fetch(request, preferred_source=source_type)
    
    return {
        "status": "success" if response.success else "error",
        "source": response.source.value,
        "cached": response.cached,
        "data": response.data,
        "error": response.error
    }


def _handle_fetch_price(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    
    request = DataRequest(category=DataCategory.PRICE, symbols=symbols)
    response = manager.fetch(request)
    
    return {
        "status": "success" if response.success else "error",
        "source": response.source.value,
        "data": response.data
    }


def _handle_fetch_events(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    
    request = DataRequest(category=DataCategory.EVENT, symbols=symbols)
    response = manager.fetch(request)
    
    return {
        "status": "success" if response.success else "error",
        "data": response.data
    }


def _handle_fetch_announcements(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    
    request = DataRequest(category=DataCategory.ANNOUNCEMENT, symbols=symbols)
    response = manager.fetch(request)
    
    return {
        "status": "success" if response.success else "error",
        "data": response.data
    }


def _handle_fetch_altdata(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    
    bidding = manager.fetch(DataRequest(category=DataCategory.BIDDING, symbols=symbols))
    recruitment = manager.fetch(DataRequest(category=DataCategory.RECRUITMENT, symbols=symbols))
    
    return {
        "status": "success",
        "bidding": bidding.data if bidding.success else {},
        "recruitment": recruitment.data if recruitment.success else {}
    }


def _handle_fetch_all(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    symbols = args.get("symbols", [])
    
    data = manager.fetch_for_tenbagger(symbols)
    return {
        "status": "success",
        "symbols": symbols,
        "data": data
    }


def _handle_clear_cache(args: Dict[str, Any]) -> Dict[str, Any]:
    manager = get_datasource_manager()
    manager.clear_cache()
    return {"status": "success", "message": "缓存已清空"}


DATASOURCE_HANDLERS = {
    "datasource.stats": _handle_stats,
    "datasource.fetch_financial": _handle_fetch_financial,
    "datasource.fetch_price": _handle_fetch_price,
    "datasource.fetch_events": _handle_fetch_events,
    "datasource.fetch_announcements": _handle_fetch_announcements,
    "datasource.fetch_altdata": _handle_fetch_altdata,
    "datasource.fetch_all": _handle_fetch_all,
    "datasource.clear_cache": _handle_clear_cache
}
