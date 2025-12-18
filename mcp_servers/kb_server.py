# -*- coding: utf-8 -*-
"""
知识库MCP服务器（标准化版本）
===========================
管理策略知识库、API文档、最佳实践
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
server = Server("kb-server")


# 知识库内容
KNOWLEDGE_BASE = {
    "strategies": {
        "momentum": {
            "title": "动量策略",
            "description": "追涨杀跌，买入近期表现强势的股票",
            "best_params": {"period": 20, "top_n": 10},
            "suitable_market": ["牛市", "震荡市"],
            "risks": ["回撤大", "换手率高"]
        },
        "value": {
            "title": "价值策略",
            "description": "低估值投资，买入PE/PB较低的股票",
            "best_params": {"pe_max": 15, "pb_max": 2},
            "suitable_market": ["熊市", "震荡市"],
            "risks": ["价值陷阱", "长期持有"]
        },
        "trend": {
            "title": "趋势跟踪",
            "description": "顺势而为，追随市场趋势",
            "best_params": {"fast_ma": 5, "slow_ma": 20},
            "suitable_market": ["趋势市"],
            "risks": ["震荡市表现差"]
        }
    },
    "api": {
        "ptrade": {
            "set_slippage": "set_slippage(0.001)",
            "set_commission": "set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013))",
            "get_price": "get_history(count, unit='1d', field='close', security_list=stocks)"
        },
        "joinquant": {
            "set_slippage": "set_slippage(FixedSlippage(0.001))",
            "set_commission": "set_order_cost(OrderCost(...))",
            "get_price": "get_price(securities, start_date, end_date, ...)"
        }
    },
    "best_practices": [
        "单票仓位不超过20%",
        "设置止损线（通常8-10%）",
        "分散投资（10-20只股票）",
        "定期再平衡（周/月）",
        "回测时间足够长（至少1年）",
        "样本外测试验证"
    ]
}


TOOLS = [
    Tool(
        name="kb.search",
        description="搜索知识库",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "category": {
                    "type": "string",
                    "description": "类别: strategies/api/best_practices"
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="kb.get_strategy",
        description="获取策略知识",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "策略名称"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="kb.get_api",
        description="获取平台API文档",
        inputSchema={
            "type": "object",
            "properties": {
                "platform": {"type": "string", "description": "平台: ptrade/joinquant"},
                "function": {"type": "string", "description": "函数名称（可选）"}
            },
            "required": ["platform"]
        }
    ),
    Tool(
        name="kb.best_practices",
        description="获取最佳实践建议",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="kb.add",
        description="添加知识条目",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "key": {"type": "string"},
                "content": {"type": "object"}
            },
            "required": ["category", "key", "content"]
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "kb.search":
            result = await _handle_search(arguments)
        elif name == "kb.get_strategy":
            result = await _handle_get_strategy(arguments)
        elif name == "kb.get_api":
            result = await _handle_get_api(arguments)
        elif name == "kb.best_practices":
            result = await _handle_best_practices()
        elif name == "kb.add":
            result = await _handle_add(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_search(args: Dict) -> Dict:
    query = args["query"].lower()
    category = args.get("category")
    
    results = []
    
    # 搜索策略
    if not category or category == "strategies":
        for key, info in KNOWLEDGE_BASE["strategies"].items():
            if query in key or query in info["title"] or query in info["description"]:
                results.append({
                    "category": "strategies",
                    "key": key,
                    "title": info["title"],
                    "snippet": info["description"][:100]
                })
    
    # 搜索API
    if not category or category == "api":
        for platform, apis in KNOWLEDGE_BASE["api"].items():
            for func, code in apis.items():
                if query in func or query in code.lower():
                    results.append({
                        "category": "api",
                        "platform": platform,
                        "function": func,
                        "code": code
                    })
    
    # 搜索最佳实践
    if not category or category == "best_practices":
        for practice in KNOWLEDGE_BASE["best_practices"]:
            if query in practice:
                results.append({
                    "category": "best_practices",
                    "content": practice
                })
    
    return {
        "success": True,
        "query": args["query"],
        "count": len(results),
        "results": results
    }


async def _handle_get_strategy(args: Dict) -> Dict:
    name = args["name"]
    
    if name not in KNOWLEDGE_BASE["strategies"]:
        return {"success": False, "error": f"策略不存在: {name}"}
    
    return {
        "success": True,
        "strategy": name,
        **KNOWLEDGE_BASE["strategies"][name]
    }


async def _handle_get_api(args: Dict) -> Dict:
    platform = args["platform"]
    func = args.get("function")
    
    if platform not in KNOWLEDGE_BASE["api"]:
        return {"success": False, "error": f"平台不存在: {platform}"}
    
    apis = KNOWLEDGE_BASE["api"][platform]
    
    if func:
        if func not in apis:
            return {"success": False, "error": f"函数不存在: {func}"}
        return {
            "success": True,
            "platform": platform,
            "function": func,
            "code": apis[func]
        }
    
    return {
        "success": True,
        "platform": platform,
        "apis": apis
    }


async def _handle_best_practices() -> Dict:
    return {
        "success": True,
        "count": len(KNOWLEDGE_BASE["best_practices"]),
        "practices": KNOWLEDGE_BASE["best_practices"]
    }


async def _handle_add(args: Dict) -> Dict:
    category = args["category"]
    key = args["key"]
    content = args["content"]
    
    if category not in KNOWLEDGE_BASE:
        KNOWLEDGE_BASE[category] = {}
    
    KNOWLEDGE_BASE[category][key] = content
    
    return {
        "success": True,
        "message": f"已添加到 {category}/{key}"
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
