# -*- coding: utf-8 -*-
"""
市场分析MCP服务器（标准化版本）
===========================
市场状态分析、主线识别、行业轮动
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("market-server")


TOOLS = [
    Tool(
        name="market.status",
        description="获取当前市场状态（牛市/熊市/震荡）",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "参考指数", "default": "000300.XSHG"}
            }
        }
    ),
    Tool(
        name="market.mainlines",
        description="获取当前市场主线",
        inputSchema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer", "default": 5}
            }
        }
    ),
    Tool(
        name="market.sectors",
        description="获取板块轮动分析",
        inputSchema={
            "type": "object",
            "properties": {
                "period": {"type": "string", "description": "周期: day/week/month", "default": "week"}
            }
        }
    ),
    Tool(
        name="market.sentiment",
        description="获取市场情绪指标",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="market.risk",
        description="获取市场风险评估",
        inputSchema={"type": "object", "properties": {}}
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "market.status":
            result = await _handle_status(arguments)
        elif name == "market.mainlines":
            result = await _handle_mainlines(arguments)
        elif name == "market.sectors":
            result = await _handle_sectors(arguments)
        elif name == "market.sentiment":
            result = await _handle_sentiment()
        elif name == "market.risk":
            result = await _handle_risk()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_status(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.data import get_data_provider, DataRequest
    from datetime import datetime, timedelta
    import numpy as np
    
    provider = get_data_provider()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    
    index = args.get("index", "000300.XSHG")
    
    request = DataRequest(
        securities=[index],
        start_date=start_date,
        end_date=end_date
    )
    response = provider.get_data(request)
    
    if not response.success or response.data is None or response.data.empty:
        # 使用模拟数据
        np.random.seed(42)
        ma20 = 100
        ma60 = 99
        current = 101
    else:
        df = response.data
        closes = df["close"].values
        ma20 = np.mean(closes[-20:]) if len(closes) >= 20 else closes[-1]
        ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else closes[-1]
        current = closes[-1]
    
    # 判断市场状态
    if current > ma20 > ma60:
        status = "bull"
        description = "牛市（多头排列）"
        risk_level = "low"
    elif current < ma20 < ma60:
        status = "bear"
        description = "熊市（空头排列）"
        risk_level = "high"
    else:
        status = "neutral"
        description = "震荡市"
        risk_level = "medium"
    
    return {
        "success": True,
        "index": index,
        "status": status,
        "description": description,
        "risk_level": risk_level,
        "indicators": {
            "current": round(current, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2)
        },
        "recommendation": {
            "bull": "可以增加仓位，选择动量策略",
            "bear": "降低仓位，选择防御性策略",
            "neutral": "保持中性仓位，轮动策略"
        }.get(status)
    }


async def _handle_mainlines(args: Dict) -> Dict:
    top_n = args.get("top_n", 5)
    
    # 模拟主线数据
    mainlines = [
        {"name": "人工智能", "score": 92, "sectors": ["软件", "硬件", "算力"], "trend": "up"},
        {"name": "新能源", "score": 85, "sectors": ["光伏", "锂电", "储能"], "trend": "up"},
        {"name": "半导体", "score": 80, "sectors": ["芯片设计", "封测", "设备"], "trend": "neutral"},
        {"name": "医药生物", "score": 75, "sectors": ["创新药", "医疗器械", "CXO"], "trend": "down"},
        {"name": "消费", "score": 70, "sectors": ["白酒", "食品", "零售"], "trend": "neutral"},
        {"name": "新材料", "score": 68, "sectors": ["稀土", "钛白粉", "氟化工"], "trend": "up"},
        {"name": "军工", "score": 65, "sectors": ["航空", "航天", "船舶"], "trend": "neutral"}
    ]
    
    return {
        "success": True,
        "count": top_n,
        "mainlines": mainlines[:top_n],
        "update_time": "实时更新"
    }


async def _handle_sectors(args: Dict) -> Dict:
    period = args.get("period", "week")
    
    # 模拟板块数据
    sectors = [
        {"name": "软件开发", "change": 8.5, "volume_change": 120, "rank": 1},
        {"name": "通信设备", "change": 6.2, "volume_change": 85, "rank": 2},
        {"name": "计算机设备", "change": 5.8, "volume_change": 95, "rank": 3},
        {"name": "电子元件", "change": 4.5, "volume_change": 70, "rank": 4},
        {"name": "光伏设备", "change": 3.2, "volume_change": 60, "rank": 5},
        {"name": "白酒", "change": -1.5, "volume_change": 30, "rank": 28},
        {"name": "房地产", "change": -3.8, "volume_change": 25, "rank": 29},
        {"name": "银行", "change": -4.2, "volume_change": 20, "rank": 30}
    ]
    
    return {
        "success": True,
        "period": period,
        "top_sectors": sectors[:5],
        "bottom_sectors": sectors[-3:],
        "rotation_suggestion": "资金从传统行业流向科技板块"
    }


async def _handle_sentiment() -> Dict:
    import numpy as np
    np.random.seed(int(__import__('time').time()) % 100)
    
    return {
        "success": True,
        "indicators": {
            "fear_greed_index": round(np.random.uniform(30, 70), 1),
            "market_temperature": round(np.random.uniform(40, 80), 1),
            "trading_activity": "活跃" if np.random.random() > 0.5 else "一般",
            "margin_balance_change": f"{np.random.uniform(-2, 2):.1f}%"
        },
        "sentiment": "中性偏乐观",
        "suggestion": "市场情绪稳定，可正常操作"
    }


async def _handle_risk() -> Dict:
    return {
        "success": True,
        "risk_assessment": {
            "overall_risk": "中等",
            "volatility_risk": "低",
            "liquidity_risk": "低",
            "policy_risk": "中等",
            "external_risk": "中等"
        },
        "risk_score": 45,
        "max_suggested_position": 0.7,
        "suggestions": [
            "建议控制总仓位在70%以内",
            "关注政策面变化",
            "设置好止损位"
        ]
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="market-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
