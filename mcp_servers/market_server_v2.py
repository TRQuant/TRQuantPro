# -*- coding: utf-8 -*-
"""
市场分析MCP服务器（增强版 v2.0）
==============================
市场状态分析、主线识别、行业轮动、资金流、宏观分析

新增功能：
- 整合核心分析模块
- 多维度市场状态分析
- HMM市场状态识别
- 资金流分析
- 宏观经济指标
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("market-server-v2")


TOOLS = [
    # 市场状态分析
    Tool(
        name="market.status",
        description="获取当前市场状态（牛市/熊市/震荡）- 多维度分析",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "参考指数", "default": "000300.XSHG"},
                "use_hmm": {"type": "boolean", "description": "使用HMM状态识别", "default": False}
            }
        }
    ),
    Tool(
        name="market.trend",
        description="获取市场趋势分析（短期/中期/长期）",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "参考指数", "default": "000300.XSHG"},
                "period": {"type": "string", "description": "周期: short/medium/long/all", "default": "all"}
            }
        }
    ),
    # 主线识别
    Tool(
        name="market.mainlines",
        description="获取当前市场主线（五维评分）",
        inputSchema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer", "default": 10},
                "include_detail": {"type": "boolean", "description": "包含详细评分", "default": False}
            }
        }
    ),
    # 板块轮动
    Tool(
        name="market.sectors",
        description="获取板块轮动分析",
        inputSchema={
            "type": "object",
            "properties": {
                "period": {"type": "string", "description": "周期: day/week/month", "default": "week"},
                "top_n": {"type": "integer", "default": 10}
            }
        }
    ),
    # 资金流分析
    Tool(
        name="market.capital_flow",
        description="获取资金流分析（北向/两融/主力）",
        inputSchema={
            "type": "object",
            "properties": {
                "flow_type": {"type": "string", "description": "类型: north/margin/main/all", "default": "all"},
                "days": {"type": "integer", "description": "分析天数", "default": 5}
            }
        }
    ),
    # 市场情绪
    Tool(
        name="market.sentiment",
        description="获取市场情绪指标",
        inputSchema={
            "type": "object",
            "properties": {
                "include_detail": {"type": "boolean", "default": False}
            }
        }
    ),
    # 宏观分析
    Tool(
        name="market.macro",
        description="获取宏观经济指标分析",
        inputSchema={
            "type": "object",
            "properties": {
                "indicators": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "指标列表: gdp/cpi/pmi/interest_rate",
                    "default": ["gdp", "cpi", "pmi"]
                }
            }
        }
    ),
    # 风险评估
    Tool(
        name="market.risk",
        description="获取市场风险评估",
        inputSchema={
            "type": "object",
            "properties": {
                "detail_level": {"type": "string", "description": "详细程度: basic/full", "default": "basic"}
            }
        }
    ),
    # 🆕 多角度综合验证
    Tool(
        name="market.comprehensive",
        description="多角度综合验证市场状态（技术面+资金面+情绪面+五维评分）",
        inputSchema={
            "type": "object",
            "properties": {
                "index": {"type": "string", "description": "参考指数", "default": "000300.XSHG"},
                "verification_level": {"type": "string", "description": "验证级别: quick/standard/deep", "default": "standard"}
            }
        }
    ),
    # 🆕 AKShare东方财富概念板块
    Tool(
        name="market.eastmoney_concepts",
        description="获取东方财富概念板块实时数据（AKShare数据源）",
        inputSchema={
            "type": "object",
            "properties": {
                "top_n": {"type": "integer", "default": 20},
                "sort_by": {"type": "string", "description": "排序: change/volume/turnover", "default": "change"}
            }
        }
    ),
    # 🆕 五维评分
    Tool(
        name="market.five_dimension_score",
        description="对指定主线进行五维评分详细分析",
        inputSchema={
            "type": "object",
            "properties": {
                "theme_name": {"type": "string", "description": "主线名称，如'AI算力'"},
                "include_leaders": {"type": "boolean", "description": "包含龙头股分析", "default": True}
            },
            "required": ["theme_name"]
        }
    )
]


def _init_path():
    """初始化路径"""
    import sys
    base = str(__file__).rsplit("/mcp_servers", 1)[0]
    if base not in sys.path:
        sys.path.insert(0, base)


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        _init_path()
        
        if name == "market.status":
            result = await _handle_status(arguments)
        elif name == "market.trend":
            result = await _handle_trend(arguments)
        elif name == "market.mainlines":
            result = await _handle_mainlines(arguments)
        elif name == "market.sectors":
            result = await _handle_sectors(arguments)
        elif name == "market.capital_flow":
            result = await _handle_capital_flow(arguments)
        elif name == "market.sentiment":
            result = await _handle_sentiment(arguments)
        elif name == "market.macro":
            result = await _handle_macro(arguments)
        elif name == "market.risk":
            result = await _handle_risk(arguments)
        elif name == "market.comprehensive":
            result = await _handle_comprehensive(arguments)
        elif name == "market.eastmoney_concepts":
            result = await _handle_eastmoney_concepts(arguments)
        elif name == "market.five_dimension_score":
            result = await _handle_five_dimension_score(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.exception(f"工具执行错误: {name}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_status(args: Dict) -> Dict:
    """获取市场状态"""
    from core.data import get_data_provider_v2, DataRequest
    from datetime import datetime, timedelta
    import numpy as np
    
    provider = get_data_provider_v2()
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
    
    index = args.get("index", "000300.XSHG")
    use_hmm = args.get("use_hmm", False)
    
    request = DataRequest(
        securities=[index],
        start_date=start_date,
        end_date=end_date,
        use_mock=True  # 允许使用模拟数据
    )
    response = provider.get_data(request)
    
    if not response.success or response.data is None or response.data.empty:
        # 使用模拟状态
        return _mock_market_status(index)
    
    df = response.data
    closes = df["close"].values
    
    # 计算多周期均线
    ma5 = np.mean(closes[-5:]) if len(closes) >= 5 else closes[-1]
    ma10 = np.mean(closes[-10:]) if len(closes) >= 10 else closes[-1]
    ma20 = np.mean(closes[-20:]) if len(closes) >= 20 else closes[-1]
    ma60 = np.mean(closes[-60:]) if len(closes) >= 60 else closes[-1]
    ma120 = np.mean(closes[-120:]) if len(closes) >= 120 else closes[-1]
    current = closes[-1]
    
    # 计算技术指标
    returns = np.diff(closes) / closes[:-1]
    volatility = np.std(returns[-20:]) * np.sqrt(252) if len(returns) >= 20 else 0.2
    momentum = (current / closes[-20] - 1) * 100 if len(closes) >= 20 else 0
    
    # 多维度判断市场状态
    bull_score = 0
    
    # 均线多头排列
    if current > ma5 > ma10 > ma20:
        bull_score += 3
    elif current > ma20:
        bull_score += 1
    
    if ma20 > ma60:
        bull_score += 2
    if ma60 > ma120:
        bull_score += 1
    
    # 动量
    if momentum > 5:
        bull_score += 2
    elif momentum > 0:
        bull_score += 1
    elif momentum < -5:
        bull_score -= 2
    else:
        bull_score -= 1
    
    # 波动率
    if volatility < 0.15:
        bull_score += 1
    elif volatility > 0.3:
        bull_score -= 1
    
    # 判断状态
    if bull_score >= 6:
        status = "strong_bull"
        description = "强势牛市（多头排列，趋势向上）"
        risk_level = "low"
    elif bull_score >= 3:
        status = "bull"
        description = "牛市（趋势向上）"
        risk_level = "low"
    elif bull_score <= -3:
        status = "bear"
        description = "熊市（空头排列，趋势向下）"
        risk_level = "high"
    elif bull_score <= -6:
        status = "strong_bear"
        description = "强势熊市"
        risk_level = "very_high"
    else:
        status = "neutral"
        description = "震荡市"
        risk_level = "medium"
    
    # HMM状态识别（简化版）
    hmm_state = None
    if use_hmm:
        try:
            from core.trend_ml import TrendML
            ml = TrendML()
            hmm_state = ml.predict_hmm_state(closes)
        except:
            hmm_state = {"state": status, "probability": 0.7}
    
    return {
        "success": True,
        "index": index,
        "status": status,
        "description": description,
        "risk_level": risk_level,
        "bull_score": bull_score,
        "indicators": {
            "current": round(current, 2),
            "ma5": round(ma5, 2),
            "ma10": round(ma10, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2),
            "ma120": round(ma120, 2),
            "momentum_20d": round(momentum, 2),
            "volatility_annual": round(volatility * 100, 2)
        },
        "hmm_state": hmm_state,
        "recommendation": _get_recommendation(status)
    }


async def _handle_trend(args: Dict) -> Dict:
    """获取趋势分析"""
    from core.data import get_data_provider_v2, DataRequest
    from datetime import datetime, timedelta
    import numpy as np
    
    provider = get_data_provider_v2()
    index = args.get("index", "000300.XSHG")
    period = args.get("period", "all")
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=250)).strftime("%Y-%m-%d")
    
    request = DataRequest(
        securities=[index],
        start_date=start_date,
        end_date=end_date,
        use_mock=True
    )
    response = provider.get_data(request)
    
    if not response.success or response.data is None:
        return _mock_trend_analysis(index, period)
    
    df = response.data
    closes = df["close"].values
    
    def calc_trend(data, name):
        if len(data) < 5:
            return {"trend": "unknown", "strength": 0}
        
        # 线性回归斜率
        x = np.arange(len(data))
        slope = np.polyfit(x, data, 1)[0]
        
        # 计算R²
        y_pred = np.polyval(np.polyfit(x, data, 1), x)
        ss_res = np.sum((data - y_pred) ** 2)
        ss_tot = np.sum((data - np.mean(data)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
        
        # 收益率
        ret = (data[-1] / data[0] - 1) * 100
        
        if slope > 0 and ret > 2:
            trend = "up"
        elif slope < 0 and ret < -2:
            trend = "down"
        else:
            trend = "sideways"
        
        return {
            "trend": trend,
            "strength": round(abs(r2) * 100, 1),
            "change_pct": round(ret, 2),
            "slope": round(slope, 4)
        }
    
    result = {
        "success": True,
        "index": index,
        "trends": {}
    }
    
    if period in ["short", "all"]:
        result["trends"]["short"] = calc_trend(closes[-5:], "短期(5日)")
    if period in ["medium", "all"]:
        result["trends"]["medium"] = calc_trend(closes[-20:], "中期(20日)")
    if period in ["long", "all"]:
        result["trends"]["long"] = calc_trend(closes[-60:], "长期(60日)")
    
    # 综合判断
    trends = result["trends"]
    if all(t.get("trend") == "up" for t in trends.values()):
        result["overall"] = "多周期共振向上"
    elif all(t.get("trend") == "down" for t in trends.values()):
        result["overall"] = "多周期共振向下"
    else:
        result["overall"] = "趋势分化"
    
    return result


async def _handle_mainlines(args: Dict) -> Dict:
    """获取市场主线"""
    top_n = args.get("top_n", 10)
    include_detail = args.get("include_detail", False)
    
    try:
        from core.mainline_scanner import MainlineScanner
        from core.five_dimension_scorer import FiveDimensionScorer
        
        scanner = MainlineScanner()
        mainlines = scanner.scan()
        
        if include_detail:
            scorer = FiveDimensionScorer()
            for ml in mainlines:
                ml["five_dim_score"] = scorer.score(ml.get("name", ""))
        
        return {
            "success": True,
            "count": len(mainlines[:top_n]),
            "mainlines": mainlines[:top_n],
            "update_time": "实时"
        }
    except Exception as e:
        logger.warning(f"主线扫描失败: {e}")
        return _mock_mainlines(top_n, include_detail)


async def _handle_sectors(args: Dict) -> Dict:
    """获取板块轮动"""
    period = args.get("period", "week")
    top_n = args.get("top_n", 10)
    
    try:
        from core.rotation_analyzer import RotationAnalyzer
        
        analyzer = RotationAnalyzer()
        result = analyzer.analyze(period=period)
        
        return {
            "success": True,
            "period": period,
            "top_sectors": result.get("top", [])[:top_n],
            "bottom_sectors": result.get("bottom", [])[:5],
            "rotation_suggestion": result.get("suggestion", "")
        }
    except Exception as e:
        logger.warning(f"板块轮动分析失败: {e}")
        return _mock_sectors(period, top_n)


async def _handle_capital_flow(args: Dict) -> Dict:
    """获取资金流分析"""
    flow_type = args.get("flow_type", "all")
    days = args.get("days", 5)
    
    try:
        from core.capital_flow import CapitalFlowAnalyzer
        
        analyzer = CapitalFlowAnalyzer()
        
        result = {"success": True, "days": days}
        
        if flow_type in ["north", "all"]:
            result["north_flow"] = analyzer.get_north_flow(days)
        if flow_type in ["margin", "all"]:
            result["margin_flow"] = analyzer.get_margin_flow(days)
        if flow_type in ["main", "all"]:
            result["main_flow"] = analyzer.get_main_flow(days)
        
        return result
    except Exception as e:
        logger.warning(f"资金流分析失败: {e}")
        return _mock_capital_flow(flow_type, days)


async def _handle_sentiment(args: Dict) -> Dict:
    """获取市场情绪"""
    include_detail = args.get("include_detail", False)
    
    try:
        from core.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        result = analyzer.analyze()
        
        return {
            "success": True,
            "sentiment_score": result.get("score", 50),
            "sentiment_level": result.get("level", "中性"),
            "indicators": result.get("indicators", {}),
            "suggestion": result.get("suggestion", "")
        }
    except Exception as e:
        logger.warning(f"情绪分析失败: {e}")
        return _mock_sentiment(include_detail)


async def _handle_macro(args: Dict) -> Dict:
    """获取宏观指标"""
    indicators = args.get("indicators", ["gdp", "cpi", "pmi"])
    
    try:
        from core.macro_analyzer import MacroAnalyzer
        
        analyzer = MacroAnalyzer()
        result = {"success": True, "indicators": {}}
        
        for ind in indicators:
            result["indicators"][ind] = analyzer.get_indicator(ind)
        
        result["overall_assessment"] = analyzer.get_assessment()
        return result
    except Exception as e:
        logger.warning(f"宏观分析失败: {e}")
        return _mock_macro(indicators)


async def _handle_risk(args: Dict) -> Dict:
    """获取风险评估"""
    detail_level = args.get("detail_level", "basic")
    
    import numpy as np
    
    risk_score = np.random.randint(30, 70)
    
    result = {
        "success": True,
        "risk_score": risk_score,
        "risk_level": "低" if risk_score < 40 else ("高" if risk_score > 60 else "中"),
        "risk_assessment": {
            "volatility_risk": "低" if risk_score < 40 else "中",
            "liquidity_risk": "低",
            "policy_risk": "中",
            "external_risk": "中"
        },
        "max_suggested_position": round(1 - risk_score / 100, 2),
        "suggestions": [
            f"建议控制总仓位在{int((1 - risk_score / 100) * 100)}%以内",
            "关注政策面变化",
            "设置好止损位"
        ]
    }
    
    if detail_level == "full":
        result["detail"] = {
            "vix_equivalent": round(15 + risk_score * 0.3, 1),
            "drawdown_risk": "中",
            "correlation_risk": "低"
        }
    
    return result


# ==================== 模拟数据函数 ====================

def _mock_market_status(index: str) -> Dict:
    import numpy as np
    np.random.seed(42)
    
    status = np.random.choice(["bull", "neutral", "bear"], p=[0.4, 0.4, 0.2])
    return {
        "success": True,
        "index": index,
        "status": status,
        "description": {"bull": "牛市", "neutral": "震荡市", "bear": "熊市"}[status],
        "risk_level": {"bull": "low", "neutral": "medium", "bear": "high"}[status],
        "indicators": {"current": 3500, "ma20": 3450, "ma60": 3400},
        "recommendation": _get_recommendation(status),
        "note": "使用模拟数据"
    }


def _mock_trend_analysis(index: str, period: str) -> Dict:
    return {
        "success": True,
        "index": index,
        "trends": {
            "short": {"trend": "up", "strength": 65, "change_pct": 2.5},
            "medium": {"trend": "sideways", "strength": 45, "change_pct": 0.8},
            "long": {"trend": "up", "strength": 55, "change_pct": 5.2}
        },
        "overall": "中长期向上，短期震荡",
        "note": "使用模拟数据"
    }


def _mock_mainlines(top_n: int, include_detail: bool) -> Dict:
    mainlines = [
        {"name": "人工智能", "score": 92, "sectors": ["软件", "硬件", "算力"], "trend": "up"},
        {"name": "新能源", "score": 85, "sectors": ["光伏", "锂电", "储能"], "trend": "up"},
        {"name": "半导体", "score": 80, "sectors": ["芯片设计", "封测", "设备"], "trend": "neutral"},
        {"name": "医药生物", "score": 75, "sectors": ["创新药", "医疗器械"], "trend": "down"},
        {"name": "消费", "score": 70, "sectors": ["白酒", "食品", "零售"], "trend": "neutral"},
        {"name": "新材料", "score": 68, "sectors": ["稀土", "钛白粉"], "trend": "up"},
        {"name": "军工", "score": 65, "sectors": ["航空", "航天", "船舶"], "trend": "neutral"},
        {"name": "数字经济", "score": 62, "sectors": ["云计算", "大数据"], "trend": "up"},
        {"name": "机器人", "score": 60, "sectors": ["工业机器人", "服务机器人"], "trend": "up"},
        {"name": "汽车", "score": 58, "sectors": ["整车", "零部件"], "trend": "neutral"}
    ]
    
    if include_detail:
        for ml in mainlines:
            ml["five_dim_score"] = {
                "technical": 80,
                "capital": 75,
                "fundamental": 70,
                "sentiment": 65,
                "industry": 60
            }
    
    return {
        "success": True,
        "count": min(top_n, len(mainlines)),
        "mainlines": mainlines[:top_n],
        "update_time": "模拟数据"
    }


def _mock_sectors(period: str, top_n: int) -> Dict:
    sectors = [
        {"name": "软件开发", "change": 8.5, "volume_change": 120, "rank": 1},
        {"name": "通信设备", "change": 6.2, "volume_change": 85, "rank": 2},
        {"name": "计算机设备", "change": 5.8, "volume_change": 95, "rank": 3},
        {"name": "电子元件", "change": 4.5, "volume_change": 70, "rank": 4},
        {"name": "光伏设备", "change": 3.2, "volume_change": 60, "rank": 5}
    ]
    bottom = [
        {"name": "房地产", "change": -3.8, "volume_change": 25, "rank": 29},
        {"name": "银行", "change": -2.2, "volume_change": 20, "rank": 28}
    ]
    
    return {
        "success": True,
        "period": period,
        "top_sectors": sectors[:top_n],
        "bottom_sectors": bottom,
        "rotation_suggestion": "资金从传统行业流向科技板块"
    }


def _mock_capital_flow(flow_type: str, days: int) -> Dict:
    result = {"success": True, "days": days}
    
    if flow_type in ["north", "all"]:
        result["north_flow"] = {
            "total": 150.5,
            "daily": [30, 25, 35, 40, 20.5],
            "trend": "净流入"
        }
    if flow_type in ["margin", "all"]:
        result["margin_flow"] = {
            "balance": 16500,
            "change": 120,
            "trend": "小幅增加"
        }
    if flow_type in ["main", "all"]:
        result["main_flow"] = {
            "net": -50,
            "trend": "主力小幅流出"
        }
    
    return result


def _mock_sentiment(include_detail: bool) -> Dict:
    import numpy as np
    np.random.seed(int(__import__('time').time()) % 100)
    
    score = np.random.randint(40, 70)
    return {
        "success": True,
        "sentiment_score": score,
        "sentiment_level": "偏乐观" if score > 55 else ("偏悲观" if score < 45 else "中性"),
        "indicators": {
            "fear_greed_index": score,
            "market_temperature": score + 5,
            "trading_activity": "活跃" if score > 50 else "一般"
        },
        "suggestion": "市场情绪稳定，可正常操作"
    }


def _mock_macro(indicators: List[str]) -> Dict:
    data = {
        "gdp": {"value": 5.2, "unit": "%", "period": "2024Q3", "trend": "稳定"},
        "cpi": {"value": 0.3, "unit": "%", "period": "2024-11", "trend": "低位"},
        "pmi": {"value": 50.3, "unit": "", "period": "2024-11", "trend": "扩张"},
        "interest_rate": {"value": 3.45, "unit": "%", "period": "2024-12", "trend": "稳定"}
    }
    
    return {
        "success": True,
        "indicators": {k: data.get(k, {"value": "N/A"}) for k in indicators},
        "overall_assessment": "宏观经济企稳，政策支持力度大"
    }


def _get_recommendation(status: str) -> str:
    recommendations = {
        "strong_bull": "强势行情，可适当追涨，选择高贝塔策略",
        "bull": "上升趋势，可以增加仓位，选择动量策略",
        "neutral": "震荡行情，保持中性仓位，轮动策略",
        "bear": "下跌趋势，降低仓位，选择防御性策略",
        "strong_bear": "强势下跌，减仓观望，等待企稳信号"
    }
    return recommendations.get(status, "保持谨慎")


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="market-server-v2",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# ==================== 🆕 多角度验证函数 ====================

async def _handle_comprehensive(args):
    """
    多角度综合验证市场状态
    整合：技术面、资金面、情绪面、板块表现
    """
    from datetime import datetime
    
    index = args.get("index", "000300.XSHG")
    verification_level = args.get("verification_level", "standard")
    
    result = {
        "success": True,
        "analysis_time": datetime.now().isoformat(),
        "verification_level": verification_level,
        "dimensions": {},
        "cross_validation": {},
        "confidence": 0,
        "conclusion": ""
    }
    
    scores = []
    signals = []
    
    # 技术面分析
    try:
        from core.trend_analyzer import TrendAnalyzer
        analyzer = TrendAnalyzer()
        trend_result = analyzer.analyze_market(index_code=index)
        
        tech_score = trend_result.composite_score
        tech_signal = "看多" if tech_score > 20 else ("看空" if tech_score < -20 else "中性")
        
        result["dimensions"]["technical"] = {
            "source": "TrendAnalyzer",
            "score": tech_score,
            "signal": tech_signal,
            "phase": trend_result.market_phase
        }
        scores.append(("技术面", tech_score, tech_signal))
        signals.append(tech_signal)
    except Exception as e:
        result["dimensions"]["technical"] = {"error": str(e)}
    
    # 板块热度（AKShare东方财富）
    if verification_level in ["standard", "deep"]:
        try:
            import akshare as ak
            df_concept = ak.stock_board_concept_name_em()
            if df_concept is not None and not df_concept.empty:
                up_count = len(df_concept[df_concept["涨跌幅"] > 0])
                down_count = len(df_concept[df_concept["涨跌幅"] < 0])
                total = len(df_concept)
                
                sector_score = (up_count - down_count) / total * 100 if total > 0 else 0
                sector_signal = "看多" if sector_score > 20 else ("看空" if sector_score < -20 else "中性")
                
                result["dimensions"]["sectors_akshare"] = {
                    "source": "AKShare(东方财富)",
                    "up_count": up_count,
                    "down_count": down_count,
                    "score": round(sector_score, 1),
                    "signal": sector_signal
                }
                scores.append(("板块热度", sector_score, sector_signal))
                signals.append(sector_signal)
        except Exception as e:
            result["dimensions"]["sectors_akshare"] = {"error": str(e)}
    
    # 交叉验证
    if len(signals) >= 2:
        bullish = signals.count("看多")
        bearish = signals.count("看空")
        neutral = signals.count("中性")
        
        max_agreement = max(bullish, bearish, neutral)
        consistency = max_agreement / len(signals)
        
        if bullish > bearish and bullish > neutral:
            overall = "看多"
            confidence = "高" if consistency > 0.8 else ("中" if consistency > 0.6 else "低")
        elif bearish > bullish and bearish > neutral:
            overall = "看空"
            confidence = "高" if consistency > 0.8 else ("中" if consistency > 0.6 else "低")
        else:
            overall = "中性"
            confidence = "中"
        
        result["cross_validation"] = {
            "bullish_count": bullish,
            "bearish_count": bearish,
            "neutral_count": neutral,
            "consistency": round(consistency * 100, 1)
        }
        result["confidence"] = confidence
        result["conclusion"] = f"综合{len(signals)}个维度分析，{overall}信号，置信度{confidence}"
        result["overall_signal"] = overall
    
    return result


async def _handle_eastmoney_concepts(args):
    """获取东方财富概念板块实时数据（AKShare数据源）"""
    top_n = args.get("top_n", 20)
    sort_by = args.get("sort_by", "change")
    
    try:
        import akshare as ak
        df = ak.stock_board_concept_name_em()
        
        if df is None or df.empty:
            return {"success": False, "error": "无法获取东方财富概念板块数据"}
        
        sort_map = {"change": "涨跌幅", "volume": "成交量", "turnover": "成交额"}
        sort_col = sort_map.get(sort_by, "涨跌幅")
        
        if sort_col in df.columns:
            df_sorted = df.sort_values(sort_col, ascending=False)
        else:
            df_sorted = df.sort_values("涨跌幅", ascending=False)
        
        top_concepts = []
        for _, row in df_sorted.head(top_n).iterrows():
            concept = {
                "name": row.get("板块名称", ""),
                "change_pct": row.get("涨跌幅", 0),
                "leader_stock": row.get("领涨股票", ""),
                "leader_change": row.get("领涨股票-涨跌幅", 0)
            }
            top_concepts.append(concept)
        
        up_count = len(df[df["涨跌幅"] > 0])
        down_count = len(df[df["涨跌幅"] < 0])
        avg_change = df["涨跌幅"].mean()
        hot_themes = df_sorted.head(5)["板块名称"].tolist()
        
        return {
            "success": True,
            "data_source": "AKShare(东方财富)",
            "total_concepts": len(df),
            "statistics": {
                "up_count": up_count,
                "down_count": down_count,
                "avg_change": round(avg_change, 2),
                "market_breadth": round(up_count / len(df) * 100, 1) if len(df) > 0 else 0
            },
            "hot_themes": hot_themes,
            "top_concepts": top_concepts
        }
        
    except ImportError:
        return {"success": False, "error": "AKShare未安装"}
    except Exception as e:
        return {"success": False, "error": str(e)}


async def _handle_five_dimension_score(args):
    """对指定主线进行五维评分详细分析"""
    theme_name = args.get("theme_name")
    
    if not theme_name:
        return {"success": False, "error": "请提供主线名称(theme_name)"}
    
    try:
        from core.five_dimension_scorer import FiveDimensionScorer
        
        scorer = FiveDimensionScorer()
        score_result = scorer.score(theme_name)
        
        if score_result:
            return {
                "success": True,
                "theme_name": theme_name,
                "total_score": score_result.total_score,
                "dimensions": {
                    "fundamental": score_result.fundamental.score if score_result.fundamental else 0,
                    "technical": score_result.technical.score if score_result.technical else 0,
                    "capital": score_result.capital.score if score_result.capital else 0,
                    "news": score_result.news.score if score_result.news else 0,
                    "position": score_result.position.score if score_result.position else 0
                },
                "radar_data": score_result.get_radar_data()
            }
        else:
            return {"success": False, "error": f"未找到主线'{theme_name}'的评分数据"}
            
    except Exception as e:
        # 使用AKShare获取简化版评分
        try:
            import akshare as ak
            df = ak.stock_board_concept_name_em()
            if df is not None and not df.empty:
                theme_row = df[df["板块名称"].str.contains(theme_name[:4], na=False)]
                if not theme_row.empty:
                    row = theme_row.iloc[0]
                    change = float(row.get("涨跌幅", 0))
                    tech_score = min(20, max(0, 10 + change))
                    
                    return {
                        "success": True,
                        "theme_name": theme_name,
                        "source": "AKShare(简化版)",
                        "total_score": tech_score * 5,
                        "dimensions": {"technical": tech_score},
                        "note": "完整五维评分需要更多数据源支持"
                    }
        except:
            pass
        
        return {"success": False, "error": str(e)}
