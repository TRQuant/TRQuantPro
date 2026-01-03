"""
Tenbagger评估 MCP工具

Author: TRQuant Team
Date: 2025-12-18
"""

from typing import Dict, Any, List
from mcp.types import Tool

from .tenbagger_evaluator import get_evaluator, EvalLevel


TENBAGGER_TOOLS = [
    Tool(
        name="tenbagger.evaluate",
        description="综合评估股票的十倍股潜力",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "股票代码"},
                "name": {"type": "string", "description": "股票名称"},
                "stage": {"type": "string", "description": "当前阶段(S0-S5)"},
                "scorecard": {"type": "object", "description": "7维评分卡数据"},
                "financials": {"type": "object", "description": "财务数据"},
                "industry": {"type": "object", "description": "行业数据"},
                "altdata": {"type": "object", "description": "另类数据"},
                "technicals": {"type": "object", "description": "技术指标"}
            },
            "required": ["symbol", "name"]
        }
    ),
    Tool(
        name="tenbagger.report",
        description="获取股票的评估报告",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.rank",
        description="获取所有已评估股票排名",
        inputSchema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer", "default": 20}
            }
        }
    ),
    Tool(
        name="tenbagger.history",
        description="获取股票评估历史",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"}
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.batch",
        description="批量评估多只股票",
        inputSchema={
            "type": "object",
            "properties": {
                "stocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string"},
                            "name": {"type": "string"},
                            "data": {"type": "object"}
                        }
                    }
                }
            },
            "required": ["stocks"]
        }
    ),
    Tool(
        name="tenbagger.filter",
        description="按等级筛选股票",
        inputSchema={
            "type": "object",
            "properties": {
                "min_level": {
                    "type": "string",
                    "enum": ["S+", "S", "A", "B", "C", "D"],
                    "default": "A"
                }
            }
        }
    ),
    Tool(
        name="tenbagger.stats",
        description="获取评估统计信息",
        inputSchema={"type": "object", "properties": {}}
    )
]


async def _handle_evaluate(args: Dict[str, Any]) -> Dict[str, Any]:
    """评估股票的十倍股潜力"""
    evaluator = get_evaluator()
    
    symbol = args.get("symbol", "")
    name = args.get("name", symbol)
    
    data = {
        "stage": args.get("stage", "S0"),
        "scorecard": args.get("scorecard", {}),
        "financials": args.get("financials", {}),
        "industry": args.get("industry", {}),
        "altdata": args.get("altdata", {}),
        "technicals": args.get("technicals", {})
    }
    
    report = evaluator.evaluate(symbol, name, data)
    return {
        "status": "success",
        "report": report.to_dict()
    }


async def _handle_report(args: Dict[str, Any]) -> Dict[str, Any]:
    """获取评估报告"""
    evaluator = get_evaluator()
    symbol = args.get("symbol", "")
    
    report = evaluator.get_report(symbol)
    if not report:
        return {"status": "error", "message": f"未找到{symbol}的评估报告"}
    
    return {
        "status": "success",
        "report": report.to_dict()
    }


async def _handle_rank(args: Dict[str, Any]) -> Dict[str, Any]:
    """获取排名"""
    evaluator = get_evaluator()
    top_n = args.get("top_n", 20)
    
    rankings = evaluator.rank_all()[:top_n]
    return {
        "status": "success",
        "count": len(rankings),
        "rankings": [
            {"symbol": symbol, "score": score, "level": level.value}
            for symbol, score, level in rankings
        ]
    }


async def _handle_history(args: Dict[str, Any]) -> Dict[str, Any]:
    """获取历史"""
    evaluator = get_evaluator()
    symbol = args.get("symbol", "")
    
    history = evaluator.get_history(symbol)
    return {
        "status": "success",
        "symbol": symbol,
        "count": len(history),
        "history": [r.to_dict() for r in history[-10:]]
    }


async def _handle_batch(args: Dict[str, Any]) -> Dict[str, Any]:
    """批量评估"""
    evaluator = get_evaluator()
    stocks = args.get("stocks", [])
    
    results = []
    for stock in stocks:
        symbol = stock.get("symbol", "")
        name = stock.get("name", symbol)
        data = stock.get("data", {})
        
        report = evaluator.evaluate(symbol, name, data)
        results.append({
            "symbol": symbol,
            "level": report.eval_level.value,
            "score": report.total_score
        })
    
    return {
        "status": "success",
        "evaluated": len(results),
        "results": results
    }


async def _handle_filter(args: Dict[str, Any]) -> Dict[str, Any]:
    """按等级筛选"""
    evaluator = get_evaluator()
    min_level = args.get("min_level", "A")
    
    level_order = {"S+": 0, "S": 1, "A": 2, "B": 3, "C": 4, "D": 5}
    min_order = level_order.get(min_level, 2)
    
    rankings = evaluator.rank_all()
    filtered = [
        {"symbol": symbol, "score": score, "level": level.value}
        for symbol, score, level in rankings
        if level_order.get(level.value, 5) <= min_order
    ]
    
    return {
        "status": "success",
        "min_level": min_level,
        "count": len(filtered),
        "stocks": filtered
    }


async def _handle_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    """获取统计信息"""
    evaluator = get_evaluator()
    stats = evaluator.get_stats()
    return {"status": "success", **stats}


TENBAGGER_HANDLERS = {
    "tenbagger.evaluate": _handle_evaluate,
    "tenbagger.report": _handle_report,
    "tenbagger.rank": _handle_rank,
    "tenbagger.history": _handle_history,
    "tenbagger.batch": _handle_batch,
    "tenbagger.filter": _handle_filter,
    "tenbagger.stats": _handle_stats
}
