# -*- coding: utf-8 -*-
"""
知识库MCP服务器（标准化版本）
===========================
管理策略知识库、API文档、最佳实践

跨平台兼容：Windows/Linux
"""

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
logger = logging.getLogger('KBServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
    logger.info("MCP SDK加载成功")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用: {e}")
    logger.error("请确保使用venv中的Python，并安装MCP SDK:")
    logger.error("  ./venv/bin/pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")
    sys.exit(1)

# 创建服务器
server = Server("kb-server")

# 知识库内容
KNOWLEDGE_BASE = {
    "strategies": {
        "momentum": {
            "name": "动量策略",
            "description": "追涨杀跌，买入近期表现强势的股票",
            "best_params": {"period": 20, "top_n": 10},
            "suitable_market": "趋势市场",
            "risk": "中等"
        },
        "value": {
            "name": "价值策略", 
            "description": "低估值投资，买入PE/PB较低的股票",
            "best_params": {"pe_max": 15, "pb_max": 2},
            "suitable_market": "震荡市场",
            "risk": "低"
        },
        "growth": {
            "name": "成长策略",
            "description": "投资高增长公司，关注ROE和营收增长",
            "best_params": {"roe_min": 15, "growth_min": 20},
            "suitable_market": "牛市",
            "risk": "高"
        },
        "mean_reversion": {
            "name": "均值回归策略",
            "description": "买入超跌股票，卖出超涨股票",
            "best_params": {"lookback": 20, "threshold": 2},
            "suitable_market": "震荡市场",
            "risk": "中等"
        }
    },
    "apis": {
        "get_price": {
            "module": "jqdata",
            "description": "获取历史价格数据",
            "example": "get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-12-31', frequency='daily')",
            "params": ["security", "start_date", "end_date", "frequency", "fields"]
        },
        "get_fundamentals": {
            "module": "jqdata",
            "description": "获取基本面数据",
            "example": "get_fundamentals(query(valuation).filter(valuation.code=='000001.XSHE'))",
            "params": ["query_object", "date"]
        },
        "get_index_stocks": {
            "module": "jqdata",
            "description": "获取指数成分股",
            "example": "get_index_stocks('000300.XSHG')",
            "params": ["index_symbol", "date"]
        }
    },
    "best_practices": {
        "risk_control": {
            "title": "风险控制最佳实践",
            "rules": [
                "单只股票仓位不超过10%",
                "设置止损线（通常8-10%）",
                "分散投资，持仓不少于10只",
                "避免追涨杀跌"
            ]
        },
        "backtest": {
            "title": "回测最佳实践",
            "rules": [
                "使用足够长的历史数据（至少3年）",
                "考虑交易成本和滑点",
                "避免过拟合",
                "进行样本外测试"
            ]
        }
    }
}

# 定义工具
TOOLS = [
    Tool(
        name="kb.search",
        description="搜索知识库（策略、API、最佳实践）",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "category": {"type": "string", "description": "类别: strategies/apis/best_practices"}
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="kb.get_strategy",
        description="获取策略详情",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy_name": {"type": "string", "description": "策略名称: momentum/value/growth/mean_reversion"}
            },
            "required": ["strategy_name"]
        }
    ),
    Tool(
        name="kb.get_api",
        description="获取API文档",
        inputSchema={
            "type": "object",
            "properties": {
                "api_name": {"type": "string", "description": "API名称: get_price/get_fundamentals/get_index_stocks"}
            },
            "required": ["api_name"]
        }
    ),
    Tool(
        name="kb.best_practices",
        description="获取最佳实践",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "类别: risk_control/backtest"}
            }
        }
    ),
    Tool(
        name="kb.list",
        description="列出知识库所有内容",
        inputSchema={
            "type": "object",
            "properties": {}
        }
    )
]


@server.list_tools()
async def list_tools():
    """列出所有工具"""
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "kb.search":
            result = _handle_search(arguments.get("query", ""), arguments.get("category"))
        elif name == "kb.get_strategy":
            result = _handle_get_strategy(arguments.get("strategy_name", ""))
        elif name == "kb.get_api":
            result = _handle_get_api(arguments.get("api_name", ""))
        elif name == "kb.best_practices":
            result = _handle_best_practices(arguments.get("category"))
        elif name == "kb.list":
            result = _handle_list()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"工具调用失败: {name}, 错误: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


def _handle_search(query: str, category: str = None) -> Dict:
    """搜索知识库"""
    results = []
    query_lower = query.lower()
    
    for cat, items in KNOWLEDGE_BASE.items():
        if category and cat != category:
            continue
        for key, value in items.items():
            if query_lower in key.lower() or query_lower in str(value).lower():
                results.append({
                    "category": cat,
                    "key": key,
                    **value
                })
    
    return {
        "success": True,
        "query": query,
        "category": category,
        "results": results,
        "total": len(results)
    }


def _handle_get_strategy(strategy_name: str) -> Dict:
    """获取策略详情"""
    strategies = KNOWLEDGE_BASE.get("strategies", {})
    if strategy_name in strategies:
        return {
            "success": True,
            "strategy": strategy_name,
            **strategies[strategy_name]
        }
    return {
        "success": False,
        "error": f"策略不存在: {strategy_name}",
        "available": list(strategies.keys())
    }


def _handle_get_api(api_name: str) -> Dict:
    """获取API文档"""
    apis = KNOWLEDGE_BASE.get("apis", {})
    if api_name in apis:
        return {
            "success": True,
            "api": api_name,
            **apis[api_name]
        }
    return {
        "success": False,
        "error": f"API不存在: {api_name}",
        "available": list(apis.keys())
    }


def _handle_best_practices(category: str = None) -> Dict:
    """获取最佳实践"""
    practices = KNOWLEDGE_BASE.get("best_practices", {})
    if category:
        if category in practices:
            return {
                "success": True,
                "category": category,
                **practices[category]
            }
        return {
            "success": False,
            "error": f"类别不存在: {category}",
            "available": list(practices.keys())
        }
    return {
        "success": True,
        "practices": practices
    }


def _handle_list() -> Dict:
    """列出所有知识库内容"""
    return {
        "success": True,
        "strategies": list(KNOWLEDGE_BASE.get("strategies", {}).keys()),
        "apis": list(KNOWLEDGE_BASE.get("apis", {}).keys()),
        "best_practices": list(KNOWLEDGE_BASE.get("best_practices", {}).keys())
    }


async def main():
    """主入口"""
    logger.info("KB Server启动中...")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
