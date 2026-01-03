"""
Tier2 AltData MCP工具

招投标+招聘数据分析工具

Author: TRQuant Team
Date: 2025-12-18
"""

from typing import Dict, Any, List
from mcp.types import Tool
from datetime import datetime

from .altdata_tier2 import (
    get_bid_store, get_job_store, get_signal_generator,
    BidRecord, JobRecord, BidType, JobType
)


ALTDATA_TOOLS = [
    Tool(
        name="altdata.bid.add",
        description="添加招投标记录",
        inputSchema={
            "type": "object",
            "properties": {
                "company": {"type": "string", "description": "公司名称"},
                "symbol": {"type": "string", "description": "股票代码"},
                "title": {"type": "string", "description": "招标标题"},
                "amount": {"type": "number", "description": "金额(万元)"},
                "bid_type": {"type": "string", "enum": ["government", "enterprise", "construction", "service", "equipment"]}
            },
            "required": ["company", "title"]
        }
    ),
    Tool(
        name="altdata.bid.query",
        description="查询招投标记录",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码"},
                "days": {"type": "integer", "default": 90}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="altdata.bid.trend",
        description="分析招投标趋势",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "days": {"type": "integer", "default": 180}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="altdata.job.add",
        description="添加招聘记录",
        inputSchema={
            "type": "object",
            "properties": {
                "company": {"type": "string"},
                "symbol": {"type": "string"},
                "title": {"type": "string", "description": "职位名称"},
                "job_type": {"type": "string", "enum": ["tech", "sales", "production", "management", "support"]},
                "salary_min": {"type": "number"},
                "salary_max": {"type": "number"},
                "location": {"type": "string"}
            },
            "required": ["company", "title"]
        }
    ),
    Tool(
        name="altdata.job.query",
        description="查询招聘记录",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "days": {"type": "integer", "default": 90}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="altdata.job.trend",
        description="分析招聘趋势",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "days": {"type": "integer", "default": 180}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="altdata.signals",
        description="生成Tier2综合信号",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="altdata.batch",
        description="批量分析多只股票",
        inputSchema={
            "type": "object",
            "properties": {
                "symbols": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["symbols"]
        }
    ),
    Tool(
        name="altdata.stats",
        description="获取AltData统计信息",
        inputSchema={"type": "object", "properties": {}}
    )
]


def _handle_bid_add(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_bid_store()
    
    bid_type_map = {
        "government": BidType.GOVERNMENT,
        "enterprise": BidType.ENTERPRISE,
        "construction": BidType.CONSTRUCTION,
        "service": BidType.SERVICE,
        "equipment": BidType.EQUIPMENT
    }
    
    record = BidRecord(
        bid_id=f"bid_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        company=args.get("company", ""),
        symbol=args.get("symbol"),
        title=args.get("title", ""),
        bid_type=bid_type_map.get(args.get("bid_type", "government"), BidType.GOVERNMENT),
        amount=args.get("amount", 0),
        region=args.get("region", ""),
        industry=args.get("industry", "")
    )
    
    store.add_record(record)
    return {"status": "success", "bid_id": record.bid_id}


def _handle_bid_query(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_bid_store()
    symbol = args.get("symbol", "")
    days = args.get("days", 90)
    
    records = store.get_by_symbol(symbol, days)
    return {
        "status": "success",
        "symbol": symbol,
        "count": len(records),
        "records": [r.to_dict() for r in records[:50]]
    }


def _handle_bid_trend(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_bid_store()
    symbol = args.get("symbol", "")
    days = args.get("days", 180)
    
    trend = store.analyze_trend(symbol, days)
    return {"status": "success", **trend}


def _handle_job_add(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_job_store()
    
    job_type_map = {
        "tech": JobType.TECH,
        "sales": JobType.SALES,
        "production": JobType.PRODUCTION,
        "management": JobType.MANAGEMENT,
        "support": JobType.SUPPORT
    }
    
    record = JobRecord(
        job_id=f"job_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        company=args.get("company", ""),
        symbol=args.get("symbol"),
        title=args.get("title", ""),
        job_type=job_type_map.get(args.get("job_type", "tech"), JobType.TECH),
        salary_min=args.get("salary_min", 0),
        salary_max=args.get("salary_max", 0),
        location=args.get("location", "")
    )
    
    store.add_record(record)
    return {"status": "success", "job_id": record.job_id}


def _handle_job_query(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_job_store()
    symbol = args.get("symbol", "")
    days = args.get("days", 90)
    
    records = store.get_by_symbol(symbol, days)
    return {
        "status": "success",
        "symbol": symbol,
        "count": len(records),
        "records": [r.to_dict() for r in records[:50]]
    }


def _handle_job_trend(args: Dict[str, Any]) -> Dict[str, Any]:
    store = get_job_store()
    symbol = args.get("symbol", "")
    days = args.get("days", 180)
    
    trend = store.analyze_trend(symbol, days)
    return {"status": "success", **trend}


def _handle_signals(args: Dict[str, Any]) -> Dict[str, Any]:
    generator = get_signal_generator()
    symbol = args.get("symbol", "")
    
    signals = generator.generate_signals(symbol)
    return {
        "status": "success",
        "symbol": symbol,
        "signal_count": len(signals),
        "signals": [s.to_dict() for s in signals]
    }


def _handle_batch(args: Dict[str, Any]) -> Dict[str, Any]:
    generator = get_signal_generator()
    symbols = args.get("symbols", [])
    
    results = generator.batch_analyze(symbols)
    summary = {
        symbol: {
            "signal_count": len(signals),
            "has_expansion": any(s.signal_type == "business_expansion" for s in signals)
        }
        for symbol, signals in results.items()
    }
    
    return {
        "status": "success",
        "analyzed": len(symbols),
        "summary": summary
    }


def _handle_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    bid_store = get_bid_store()
    job_store = get_job_store()
    
    return {
        "status": "success",
        "bid_stats": bid_store.get_stats(),
        "job_stats": job_store.get_stats()
    }


ALTDATA_HANDLERS = {
    "altdata.bid.add": _handle_bid_add,
    "altdata.bid.query": _handle_bid_query,
    "altdata.bid.trend": _handle_bid_trend,
    "altdata.job.add": _handle_job_add,
    "altdata.job.query": _handle_job_query,
    "altdata.job.trend": _handle_job_trend,
    "altdata.signals": _handle_signals,
    "altdata.batch": _handle_batch,
    "altdata.stats": _handle_stats
}
