#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Market Regime MCP Tools
========================

市场环境判断MCP工具集

工具列表：
1. market.regime.detect - 检测当前市场环境
2. market.regime.indicators - 获取市场指标
3. market.regime.strategy - 获取策略推荐
4. market.regime.history - 获取历史环境记录
5. market.regime.predict - 预测市场趋势
"""

import logging
import sys
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_detector():
    """获取检测器实例"""
    from core.market_regime import get_market_regime_detector
    return get_market_regime_detector()


# ============ Tool Definitions ============

MARKET_REGIME_TOOLS = [
    {
        "name": "market.regime.detect",
        "description": """检测当前市场环境

返回市场所处阶段（牛市/熊市/震荡市/复苏期/派发期）及置信度。

Args:
    date: 日期，格式YYYY-MM-DD，默认最新

Returns:
    - regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    - confidence: 置信度 (0-1)
    - score: 综合得分 (-100 to 100)
    - strategy_advice: 策略建议
    - risk_warning: 风险提示
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期，格式YYYY-MM-DD"
                }
            }
        }
    },
    {
        "name": "market.regime.indicators",
        "description": """获取市场环境指标

返回完整的市场环境指标数据，包括：
- 宏观指标：PMI、M2增速、利率
- 市场指标：均线系统、成交量、涨跌比
- 情绪指标：换手率、新高新低、融资余额
- 技术指标：RSI、MACD、波动率

Args:
    date: 日期

Returns:
    完整的市场指标数据
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    },
    {
        "name": "market.regime.strategy",
        "description": """获取当前市场环境的策略推荐

根据市场环境返回：
- 建议仓位
- 推荐策略类型
- 风险偏好
- 关注方向

Args:
    regime: 可选，指定市场环境，默认使用检测结果

Returns:
    策略推荐详情
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                }
            }
        }
    },
    {
        "name": "market.regime.history",
        "description": """获取历史市场环境记录

Args:
    days: 天数，默认30

Returns:
    历史环境记录列表
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "default": 30,
                    "description": "历史天数"
                }
            }
        }
    },
    {
        "name": "market.regime.predict",
        "description": """预测市场趋势

基于当前指标和历史模式预测短期市场走势

Args:
    date: 日期

Returns:
    - trend_prediction: 趋势预测
    - probability: 预测概率
    - key_factors: 关键因素
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    }
]


# ============ Tool Handlers ============

def handle_detect(params: Dict[str, Any]) -> Dict[str, Any]:
    """检测市场环境"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        result = detector.detect_regime(date)
        
        return {
            "success": True,
            "data": result.to_dict()
        }
    except Exception as e:
        logger.error(f"检测市场环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_indicators(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取市场指标"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        indicators = detector.get_market_indicators(date)
        
        return {
            "success": True,
            "data": indicators.to_dict()
        }
    except Exception as e:
        logger.error(f"获取市场指标失败: {e}")
        return {"success": False, "error": str(e)}


def handle_strategy(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略推荐"""
    try:
        detector = _get_detector()
        regime_str = params.get('regime')
        
        if regime_str:
            from core.market_regime import MarketRegime
            regime = MarketRegime(regime_str)
        else:
            regime = None
        
        recommendation = detector.get_strategy_recommendation(regime)
        
        return {
            "success": True,
            "data": recommendation
        }
    except Exception as e:
        logger.error(f"获取策略推荐失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取历史记录"""
    try:
        detector = _get_detector()
        days = params.get('days', 30)
        
        history = detector.get_history_regimes(days)
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        return {"success": False, "error": str(e)}


def handle_predict(params: Dict[str, Any]) -> Dict[str, Any]:
    """预测市场趋势"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        # 获取当前检测结果
        result = detector.detect_regime(date)
        indicators = detector.get_market_indicators(date)
        
        # 生成预测
        prediction = {
            "current_regime": result.regime.value,
            "trend_prediction": result.trend_prediction,
            "confidence": result.confidence,
            "key_factors": {
                "technical_score": result.technical_score,
                "sentiment_score": result.sentiment_score,
                "market_score": result.market_score,
                "macro_score": result.macro_score
            },
            "indicators_summary": {
                "rsi": indicators.rsi,
                "volatility": indicators.volatility,
                "advance_decline": indicators.advance_decline,
                "index_position": indicators.index_position
            },
            "risk_warning": result.risk_warning,
            "strategy_advice": result.strategy_advice
        }
        
        # 短期预测
        if result.score > 30:
            prediction["short_term_outlook"] = "看涨"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        elif result.score < -30:
            prediction["short_term_outlook"] = "看跌"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        else:
            prediction["short_term_outlook"] = "震荡"
            prediction["probability"] = 0.5
        
        return {
            "success": True,
            "data": prediction
        }
    except Exception as e:
        logger.error(f"预测市场趋势失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
MARKET_REGIME_HANDLERS = {
    "market.regime.detect": handle_detect,
    "market.regime.indicators": handle_indicators,
    "market.regime.strategy": handle_strategy,
    "market.regime.history": handle_history,
    "market.regime.predict": handle_predict
}


def get_tool_list():
    """获取工具列表（MCP格式）"""
    from mcp import types
    
    tools = []
    for tool_def in MARKET_REGIME_TOOLS:
        tools.append(types.Tool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=tool_def["inputSchema"]
        ))
    return tools


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = MARKET_REGIME_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}


# -*- coding: utf-8 -*-
"""
Market Regime MCP Tools
========================

市场环境判断MCP工具集

工具列表：
1. market.regime.detect - 检测当前市场环境
2. market.regime.indicators - 获取市场指标
3. market.regime.strategy - 获取策略推荐
4. market.regime.history - 获取历史环境记录
5. market.regime.predict - 预测市场趋势
"""

import logging
import sys
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_detector():
    """获取检测器实例"""
    from core.market_regime import get_market_regime_detector
    return get_market_regime_detector()


# ============ Tool Definitions ============

MARKET_REGIME_TOOLS = [
    {
        "name": "market.regime.detect",
        "description": """检测当前市场环境

返回市场所处阶段（牛市/熊市/震荡市/复苏期/派发期）及置信度。

Args:
    date: 日期，格式YYYY-MM-DD，默认最新

Returns:
    - regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    - confidence: 置信度 (0-1)
    - score: 综合得分 (-100 to 100)
    - strategy_advice: 策略建议
    - risk_warning: 风险提示
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期，格式YYYY-MM-DD"
                }
            }
        }
    },
    {
        "name": "market.regime.indicators",
        "description": """获取市场环境指标

返回完整的市场环境指标数据，包括：
- 宏观指标：PMI、M2增速、利率
- 市场指标：均线系统、成交量、涨跌比
- 情绪指标：换手率、新高新低、融资余额
- 技术指标：RSI、MACD、波动率

Args:
    date: 日期

Returns:
    完整的市场指标数据
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    },
    {
        "name": "market.regime.strategy",
        "description": """获取当前市场环境的策略推荐

根据市场环境返回：
- 建议仓位
- 推荐策略类型
- 风险偏好
- 关注方向

Args:
    regime: 可选，指定市场环境，默认使用检测结果

Returns:
    策略推荐详情
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                }
            }
        }
    },
    {
        "name": "market.regime.history",
        "description": """获取历史市场环境记录

Args:
    days: 天数，默认30

Returns:
    历史环境记录列表
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "default": 30,
                    "description": "历史天数"
                }
            }
        }
    },
    {
        "name": "market.regime.predict",
        "description": """预测市场趋势

基于当前指标和历史模式预测短期市场走势

Args:
    date: 日期

Returns:
    - trend_prediction: 趋势预测
    - probability: 预测概率
    - key_factors: 关键因素
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    }
]


# ============ Tool Handlers ============

def handle_detect(params: Dict[str, Any]) -> Dict[str, Any]:
    """检测市场环境"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        result = detector.detect_regime(date)
        
        return {
            "success": True,
            "data": result.to_dict()
        }
    except Exception as e:
        logger.error(f"检测市场环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_indicators(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取市场指标"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        indicators = detector.get_market_indicators(date)
        
        return {
            "success": True,
            "data": indicators.to_dict()
        }
    except Exception as e:
        logger.error(f"获取市场指标失败: {e}")
        return {"success": False, "error": str(e)}


def handle_strategy(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略推荐"""
    try:
        detector = _get_detector()
        regime_str = params.get('regime')
        
        if regime_str:
            from core.market_regime import MarketRegime
            regime = MarketRegime(regime_str)
        else:
            regime = None
        
        recommendation = detector.get_strategy_recommendation(regime)
        
        return {
            "success": True,
            "data": recommendation
        }
    except Exception as e:
        logger.error(f"获取策略推荐失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取历史记录"""
    try:
        detector = _get_detector()
        days = params.get('days', 30)
        
        history = detector.get_history_regimes(days)
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        return {"success": False, "error": str(e)}


def handle_predict(params: Dict[str, Any]) -> Dict[str, Any]:
    """预测市场趋势"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        # 获取当前检测结果
        result = detector.detect_regime(date)
        indicators = detector.get_market_indicators(date)
        
        # 生成预测
        prediction = {
            "current_regime": result.regime.value,
            "trend_prediction": result.trend_prediction,
            "confidence": result.confidence,
            "key_factors": {
                "technical_score": result.technical_score,
                "sentiment_score": result.sentiment_score,
                "market_score": result.market_score,
                "macro_score": result.macro_score
            },
            "indicators_summary": {
                "rsi": indicators.rsi,
                "volatility": indicators.volatility,
                "advance_decline": indicators.advance_decline,
                "index_position": indicators.index_position
            },
            "risk_warning": result.risk_warning,
            "strategy_advice": result.strategy_advice
        }
        
        # 短期预测
        if result.score > 30:
            prediction["short_term_outlook"] = "看涨"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        elif result.score < -30:
            prediction["short_term_outlook"] = "看跌"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        else:
            prediction["short_term_outlook"] = "震荡"
            prediction["probability"] = 0.5
        
        return {
            "success": True,
            "data": prediction
        }
    except Exception as e:
        logger.error(f"预测市场趋势失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
MARKET_REGIME_HANDLERS = {
    "market.regime.detect": handle_detect,
    "market.regime.indicators": handle_indicators,
    "market.regime.strategy": handle_strategy,
    "market.regime.history": handle_history,
    "market.regime.predict": handle_predict
}


def get_tool_list():
    """获取工具列表（MCP格式）"""
    from mcp import types
    
    tools = []
    for tool_def in MARKET_REGIME_TOOLS:
        tools.append(types.Tool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=tool_def["inputSchema"]
        ))
    return tools


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = MARKET_REGIME_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}





















# -*- coding: utf-8 -*-
"""
Market Regime MCP Tools
========================

市场环境判断MCP工具集

工具列表：
1. market.regime.detect - 检测当前市场环境
2. market.regime.indicators - 获取市场指标
3. market.regime.strategy - 获取策略推荐
4. market.regime.history - 获取历史环境记录
5. market.regime.predict - 预测市场趋势
"""

import logging
import sys
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_detector():
    """获取检测器实例"""
    from core.market_regime import get_market_regime_detector
    return get_market_regime_detector()


# ============ Tool Definitions ============

MARKET_REGIME_TOOLS = [
    {
        "name": "market.regime.detect",
        "description": """检测当前市场环境

返回市场所处阶段（牛市/熊市/震荡市/复苏期/派发期）及置信度。

Args:
    date: 日期，格式YYYY-MM-DD，默认最新

Returns:
    - regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    - confidence: 置信度 (0-1)
    - score: 综合得分 (-100 to 100)
    - strategy_advice: 策略建议
    - risk_warning: 风险提示
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期，格式YYYY-MM-DD"
                }
            }
        }
    },
    {
        "name": "market.regime.indicators",
        "description": """获取市场环境指标

返回完整的市场环境指标数据，包括：
- 宏观指标：PMI、M2增速、利率
- 市场指标：均线系统、成交量、涨跌比
- 情绪指标：换手率、新高新低、融资余额
- 技术指标：RSI、MACD、波动率

Args:
    date: 日期

Returns:
    完整的市场指标数据
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    },
    {
        "name": "market.regime.strategy",
        "description": """获取当前市场环境的策略推荐

根据市场环境返回：
- 建议仓位
- 推荐策略类型
- 风险偏好
- 关注方向

Args:
    regime: 可选，指定市场环境，默认使用检测结果

Returns:
    策略推荐详情
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                }
            }
        }
    },
    {
        "name": "market.regime.history",
        "description": """获取历史市场环境记录

Args:
    days: 天数，默认30

Returns:
    历史环境记录列表
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "default": 30,
                    "description": "历史天数"
                }
            }
        }
    },
    {
        "name": "market.regime.predict",
        "description": """预测市场趋势

基于当前指标和历史模式预测短期市场走势

Args:
    date: 日期

Returns:
    - trend_prediction: 趋势预测
    - probability: 预测概率
    - key_factors: 关键因素
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    }
]


# ============ Tool Handlers ============

def handle_detect(params: Dict[str, Any]) -> Dict[str, Any]:
    """检测市场环境"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        result = detector.detect_regime(date)
        
        return {
            "success": True,
            "data": result.to_dict()
        }
    except Exception as e:
        logger.error(f"检测市场环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_indicators(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取市场指标"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        indicators = detector.get_market_indicators(date)
        
        return {
            "success": True,
            "data": indicators.to_dict()
        }
    except Exception as e:
        logger.error(f"获取市场指标失败: {e}")
        return {"success": False, "error": str(e)}


def handle_strategy(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略推荐"""
    try:
        detector = _get_detector()
        regime_str = params.get('regime')
        
        if regime_str:
            from core.market_regime import MarketRegime
            regime = MarketRegime(regime_str)
        else:
            regime = None
        
        recommendation = detector.get_strategy_recommendation(regime)
        
        return {
            "success": True,
            "data": recommendation
        }
    except Exception as e:
        logger.error(f"获取策略推荐失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取历史记录"""
    try:
        detector = _get_detector()
        days = params.get('days', 30)
        
        history = detector.get_history_regimes(days)
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        return {"success": False, "error": str(e)}


def handle_predict(params: Dict[str, Any]) -> Dict[str, Any]:
    """预测市场趋势"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        # 获取当前检测结果
        result = detector.detect_regime(date)
        indicators = detector.get_market_indicators(date)
        
        # 生成预测
        prediction = {
            "current_regime": result.regime.value,
            "trend_prediction": result.trend_prediction,
            "confidence": result.confidence,
            "key_factors": {
                "technical_score": result.technical_score,
                "sentiment_score": result.sentiment_score,
                "market_score": result.market_score,
                "macro_score": result.macro_score
            },
            "indicators_summary": {
                "rsi": indicators.rsi,
                "volatility": indicators.volatility,
                "advance_decline": indicators.advance_decline,
                "index_position": indicators.index_position
            },
            "risk_warning": result.risk_warning,
            "strategy_advice": result.strategy_advice
        }
        
        # 短期预测
        if result.score > 30:
            prediction["short_term_outlook"] = "看涨"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        elif result.score < -30:
            prediction["short_term_outlook"] = "看跌"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        else:
            prediction["short_term_outlook"] = "震荡"
            prediction["probability"] = 0.5
        
        return {
            "success": True,
            "data": prediction
        }
    except Exception as e:
        logger.error(f"预测市场趋势失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
MARKET_REGIME_HANDLERS = {
    "market.regime.detect": handle_detect,
    "market.regime.indicators": handle_indicators,
    "market.regime.strategy": handle_strategy,
    "market.regime.history": handle_history,
    "market.regime.predict": handle_predict
}


def get_tool_list():
    """获取工具列表（MCP格式）"""
    from mcp import types
    
    tools = []
    for tool_def in MARKET_REGIME_TOOLS:
        tools.append(types.Tool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=tool_def["inputSchema"]
        ))
    return tools


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = MARKET_REGIME_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}


# -*- coding: utf-8 -*-
"""
Market Regime MCP Tools
========================

市场环境判断MCP工具集

工具列表：
1. market.regime.detect - 检测当前市场环境
2. market.regime.indicators - 获取市场指标
3. market.regime.strategy - 获取策略推荐
4. market.regime.history - 获取历史环境记录
5. market.regime.predict - 预测市场趋势
"""

import logging
import sys
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

# 添加项目路径
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_detector():
    """获取检测器实例"""
    from core.market_regime import get_market_regime_detector
    return get_market_regime_detector()


# ============ Tool Definitions ============

MARKET_REGIME_TOOLS = [
    {
        "name": "market.regime.detect",
        "description": """检测当前市场环境

返回市场所处阶段（牛市/熊市/震荡市/复苏期/派发期）及置信度。

Args:
    date: 日期，格式YYYY-MM-DD，默认最新

Returns:
    - regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    - confidence: 置信度 (0-1)
    - score: 综合得分 (-100 to 100)
    - strategy_advice: 策略建议
    - risk_warning: 风险提示
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期，格式YYYY-MM-DD"
                }
            }
        }
    },
    {
        "name": "market.regime.indicators",
        "description": """获取市场环境指标

返回完整的市场环境指标数据，包括：
- 宏观指标：PMI、M2增速、利率
- 市场指标：均线系统、成交量、涨跌比
- 情绪指标：换手率、新高新低、融资余额
- 技术指标：RSI、MACD、波动率

Args:
    date: 日期

Returns:
    完整的市场指标数据
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    },
    {
        "name": "market.regime.strategy",
        "description": """获取当前市场环境的策略推荐

根据市场环境返回：
- 建议仓位
- 推荐策略类型
- 风险偏好
- 关注方向

Args:
    regime: 可选，指定市场环境，默认使用检测结果

Returns:
    策略推荐详情
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                }
            }
        }
    },
    {
        "name": "market.regime.history",
        "description": """获取历史市场环境记录

Args:
    days: 天数，默认30

Returns:
    历史环境记录列表
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {
                    "type": "integer",
                    "default": 30,
                    "description": "历史天数"
                }
            }
        }
    },
    {
        "name": "market.regime.predict",
        "description": """预测市场趋势

基于当前指标和历史模式预测短期市场走势

Args:
    date: 日期

Returns:
    - trend_prediction: 趋势预测
    - probability: 预测概率
    - key_factors: 关键因素
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "分析日期"
                }
            }
        }
    }
]


# ============ Tool Handlers ============

def handle_detect(params: Dict[str, Any]) -> Dict[str, Any]:
    """检测市场环境"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        result = detector.detect_regime(date)
        
        return {
            "success": True,
            "data": result.to_dict()
        }
    except Exception as e:
        logger.error(f"检测市场环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_indicators(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取市场指标"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        indicators = detector.get_market_indicators(date)
        
        return {
            "success": True,
            "data": indicators.to_dict()
        }
    except Exception as e:
        logger.error(f"获取市场指标失败: {e}")
        return {"success": False, "error": str(e)}


def handle_strategy(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略推荐"""
    try:
        detector = _get_detector()
        regime_str = params.get('regime')
        
        if regime_str:
            from core.market_regime import MarketRegime
            regime = MarketRegime(regime_str)
        else:
            regime = None
        
        recommendation = detector.get_strategy_recommendation(regime)
        
        return {
            "success": True,
            "data": recommendation
        }
    except Exception as e:
        logger.error(f"获取策略推荐失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取历史记录"""
    try:
        detector = _get_detector()
        days = params.get('days', 30)
        
        history = detector.get_history_regimes(days)
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        return {"success": False, "error": str(e)}


def handle_predict(params: Dict[str, Any]) -> Dict[str, Any]:
    """预测市场趋势"""
    try:
        detector = _get_detector()
        date = params.get('date')
        
        # 获取当前检测结果
        result = detector.detect_regime(date)
        indicators = detector.get_market_indicators(date)
        
        # 生成预测
        prediction = {
            "current_regime": result.regime.value,
            "trend_prediction": result.trend_prediction,
            "confidence": result.confidence,
            "key_factors": {
                "technical_score": result.technical_score,
                "sentiment_score": result.sentiment_score,
                "market_score": result.market_score,
                "macro_score": result.macro_score
            },
            "indicators_summary": {
                "rsi": indicators.rsi,
                "volatility": indicators.volatility,
                "advance_decline": indicators.advance_decline,
                "index_position": indicators.index_position
            },
            "risk_warning": result.risk_warning,
            "strategy_advice": result.strategy_advice
        }
        
        # 短期预测
        if result.score > 30:
            prediction["short_term_outlook"] = "看涨"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        elif result.score < -30:
            prediction["short_term_outlook"] = "看跌"
            prediction["probability"] = min(0.8, 0.5 + result.confidence * 0.3)
        else:
            prediction["short_term_outlook"] = "震荡"
            prediction["probability"] = 0.5
        
        return {
            "success": True,
            "data": prediction
        }
    except Exception as e:
        logger.error(f"预测市场趋势失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
MARKET_REGIME_HANDLERS = {
    "market.regime.detect": handle_detect,
    "market.regime.indicators": handle_indicators,
    "market.regime.strategy": handle_strategy,
    "market.regime.history": handle_history,
    "market.regime.predict": handle_predict
}


def get_tool_list():
    """获取工具列表（MCP格式）"""
    from mcp import types
    
    tools = []
    for tool_def in MARKET_REGIME_TOOLS:
        tools.append(types.Tool(
            name=tool_def["name"],
            description=tool_def["description"],
            inputSchema=tool_def["inputSchema"]
        ))
    return tools


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = MARKET_REGIME_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}









































