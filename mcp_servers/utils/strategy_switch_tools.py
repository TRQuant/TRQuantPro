#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Strategy Switch MCP Tools - 策略切换MCP工具
==========================================

工具列表：
1. strategy.switch.update - 更新市场环境触发策略切换
2. strategy.switch.advice - 获取当前策略建议
3. strategy.switch.signals - 获取股票信号
4. strategy.switch.history - 获取切换历史
"""

import logging
import sys
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_manager():
    """获取策略管理器"""
    from core.strategy.adaptive_strategy_manager import get_adaptive_strategy_manager
    return get_adaptive_strategy_manager()


# ============ Tool Definitions ============

STRATEGY_SWITCH_TOOLS = [
    {
        "name": "strategy.switch.update",
        "description": """更新市场环境并触发策略切换

Args:
    regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    confidence: 置信度 (0-1)

Returns:
    切换结果，包括新激活的策略组合
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                },
                "confidence": {
                    "type": "number",
                    "default": 0.5,
                    "description": "置信度"
                }
            },
            "required": ["regime"]
        }
    },
    {
        "name": "strategy.switch.advice",
        "description": """获取当前策略建议

Args:
    current_holdings: 当前持仓比例

Returns:
    仓位建议和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_holdings": {
                    "type": "number",
                    "default": 0.0,
                    "description": "当前持仓比例"
                }
            }
        }
    },
    {
        "name": "strategy.switch.signals",
        "description": """获取股票信号

根据当前激活的策略组合生成股票交易信号

Args:
    stocks: 股票代码列表
    date: 日期

Returns:
    各股票的综合信号和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "date": {
                    "type": "string",
                    "description": "日期"
                }
            },
            "required": ["stocks"]
        }
    },
    {
        "name": "strategy.switch.history",
        "description": """获取策略切换历史

Returns:
    历史切换记录
""",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


# ============ Tool Handlers ============

def handle_update(params: Dict[str, Any]) -> Dict[str, Any]:
    """更新市场环境"""
    try:
        manager = _get_manager()
        regime = params.get('regime')
        confidence = params.get('confidence', 0.5)
        
        result = manager.update_regime(regime, confidence)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"更新环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_advice(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略建议"""
    try:
        manager = _get_manager()
        current_holdings = params.get('current_holdings', 0.0)
        
        advice = manager.get_position_advice(current_holdings)
        
        return {
            "success": True,
            "data": {
                "target_position": advice.target_position,
                "current_regime": advice.current_regime,
                "strategy_weights": advice.strategy_weights,
                "risk_level": advice.risk_level,
                "action": advice.action,
                "reason": advice.reason
            }
        }
    except Exception as e:
        logger.error(f"获取建议失败: {e}")
        return {"success": False, "error": str(e)}


def handle_signals(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取股票信号"""
    try:
        manager = _get_manager()
        stocks = params.get('stocks', [])
        date = params.get('date')
        
        signals = manager.get_stock_signals(stocks, date)
        
        return {
            "success": True,
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"获取信号失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取切换历史"""
    try:
        manager = _get_manager()
        history = manager.get_regime_history()
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
STRATEGY_SWITCH_HANDLERS = {
    "strategy.switch.update": handle_update,
    "strategy.switch.advice": handle_advice,
    "strategy.switch.signals": handle_signals,
    "strategy.switch.history": handle_history
}


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = STRATEGY_SWITCH_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}


# -*- coding: utf-8 -*-
"""
Strategy Switch MCP Tools - 策略切换MCP工具
==========================================

工具列表：
1. strategy.switch.update - 更新市场环境触发策略切换
2. strategy.switch.advice - 获取当前策略建议
3. strategy.switch.signals - 获取股票信号
4. strategy.switch.history - 获取切换历史
"""

import logging
import sys
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_manager():
    """获取策略管理器"""
    from core.strategy.adaptive_strategy_manager import get_adaptive_strategy_manager
    return get_adaptive_strategy_manager()


# ============ Tool Definitions ============

STRATEGY_SWITCH_TOOLS = [
    {
        "name": "strategy.switch.update",
        "description": """更新市场环境并触发策略切换

Args:
    regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    confidence: 置信度 (0-1)

Returns:
    切换结果，包括新激活的策略组合
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                },
                "confidence": {
                    "type": "number",
                    "default": 0.5,
                    "description": "置信度"
                }
            },
            "required": ["regime"]
        }
    },
    {
        "name": "strategy.switch.advice",
        "description": """获取当前策略建议

Args:
    current_holdings: 当前持仓比例

Returns:
    仓位建议和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_holdings": {
                    "type": "number",
                    "default": 0.0,
                    "description": "当前持仓比例"
                }
            }
        }
    },
    {
        "name": "strategy.switch.signals",
        "description": """获取股票信号

根据当前激活的策略组合生成股票交易信号

Args:
    stocks: 股票代码列表
    date: 日期

Returns:
    各股票的综合信号和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "date": {
                    "type": "string",
                    "description": "日期"
                }
            },
            "required": ["stocks"]
        }
    },
    {
        "name": "strategy.switch.history",
        "description": """获取策略切换历史

Returns:
    历史切换记录
""",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


# ============ Tool Handlers ============

def handle_update(params: Dict[str, Any]) -> Dict[str, Any]:
    """更新市场环境"""
    try:
        manager = _get_manager()
        regime = params.get('regime')
        confidence = params.get('confidence', 0.5)
        
        result = manager.update_regime(regime, confidence)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"更新环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_advice(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略建议"""
    try:
        manager = _get_manager()
        current_holdings = params.get('current_holdings', 0.0)
        
        advice = manager.get_position_advice(current_holdings)
        
        return {
            "success": True,
            "data": {
                "target_position": advice.target_position,
                "current_regime": advice.current_regime,
                "strategy_weights": advice.strategy_weights,
                "risk_level": advice.risk_level,
                "action": advice.action,
                "reason": advice.reason
            }
        }
    except Exception as e:
        logger.error(f"获取建议失败: {e}")
        return {"success": False, "error": str(e)}


def handle_signals(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取股票信号"""
    try:
        manager = _get_manager()
        stocks = params.get('stocks', [])
        date = params.get('date')
        
        signals = manager.get_stock_signals(stocks, date)
        
        return {
            "success": True,
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"获取信号失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取切换历史"""
    try:
        manager = _get_manager()
        history = manager.get_regime_history()
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
STRATEGY_SWITCH_HANDLERS = {
    "strategy.switch.update": handle_update,
    "strategy.switch.advice": handle_advice,
    "strategy.switch.signals": handle_signals,
    "strategy.switch.history": handle_history
}


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = STRATEGY_SWITCH_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}





















# -*- coding: utf-8 -*-
"""
Strategy Switch MCP Tools - 策略切换MCP工具
==========================================

工具列表：
1. strategy.switch.update - 更新市场环境触发策略切换
2. strategy.switch.advice - 获取当前策略建议
3. strategy.switch.signals - 获取股票信号
4. strategy.switch.history - 获取切换历史
"""

import logging
import sys
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_manager():
    """获取策略管理器"""
    from core.strategy.adaptive_strategy_manager import get_adaptive_strategy_manager
    return get_adaptive_strategy_manager()


# ============ Tool Definitions ============

STRATEGY_SWITCH_TOOLS = [
    {
        "name": "strategy.switch.update",
        "description": """更新市场环境并触发策略切换

Args:
    regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    confidence: 置信度 (0-1)

Returns:
    切换结果，包括新激活的策略组合
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                },
                "confidence": {
                    "type": "number",
                    "default": 0.5,
                    "description": "置信度"
                }
            },
            "required": ["regime"]
        }
    },
    {
        "name": "strategy.switch.advice",
        "description": """获取当前策略建议

Args:
    current_holdings: 当前持仓比例

Returns:
    仓位建议和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_holdings": {
                    "type": "number",
                    "default": 0.0,
                    "description": "当前持仓比例"
                }
            }
        }
    },
    {
        "name": "strategy.switch.signals",
        "description": """获取股票信号

根据当前激活的策略组合生成股票交易信号

Args:
    stocks: 股票代码列表
    date: 日期

Returns:
    各股票的综合信号和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "date": {
                    "type": "string",
                    "description": "日期"
                }
            },
            "required": ["stocks"]
        }
    },
    {
        "name": "strategy.switch.history",
        "description": """获取策略切换历史

Returns:
    历史切换记录
""",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


# ============ Tool Handlers ============

def handle_update(params: Dict[str, Any]) -> Dict[str, Any]:
    """更新市场环境"""
    try:
        manager = _get_manager()
        regime = params.get('regime')
        confidence = params.get('confidence', 0.5)
        
        result = manager.update_regime(regime, confidence)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"更新环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_advice(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略建议"""
    try:
        manager = _get_manager()
        current_holdings = params.get('current_holdings', 0.0)
        
        advice = manager.get_position_advice(current_holdings)
        
        return {
            "success": True,
            "data": {
                "target_position": advice.target_position,
                "current_regime": advice.current_regime,
                "strategy_weights": advice.strategy_weights,
                "risk_level": advice.risk_level,
                "action": advice.action,
                "reason": advice.reason
            }
        }
    except Exception as e:
        logger.error(f"获取建议失败: {e}")
        return {"success": False, "error": str(e)}


def handle_signals(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取股票信号"""
    try:
        manager = _get_manager()
        stocks = params.get('stocks', [])
        date = params.get('date')
        
        signals = manager.get_stock_signals(stocks, date)
        
        return {
            "success": True,
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"获取信号失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取切换历史"""
    try:
        manager = _get_manager()
        history = manager.get_regime_history()
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
STRATEGY_SWITCH_HANDLERS = {
    "strategy.switch.update": handle_update,
    "strategy.switch.advice": handle_advice,
    "strategy.switch.signals": handle_signals,
    "strategy.switch.history": handle_history
}


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = STRATEGY_SWITCH_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}


# -*- coding: utf-8 -*-
"""
Strategy Switch MCP Tools - 策略切换MCP工具
==========================================

工具列表：
1. strategy.switch.update - 更新市场环境触发策略切换
2. strategy.switch.advice - 获取当前策略建议
3. strategy.switch.signals - 获取股票信号
4. strategy.switch.history - 获取切换历史
"""

import logging
import sys
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")


def _get_manager():
    """获取策略管理器"""
    from core.strategy.adaptive_strategy_manager import get_adaptive_strategy_manager
    return get_adaptive_strategy_manager()


# ============ Tool Definitions ============

STRATEGY_SWITCH_TOOLS = [
    {
        "name": "strategy.switch.update",
        "description": """更新市场环境并触发策略切换

Args:
    regime: 市场环境 (BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION)
    confidence: 置信度 (0-1)

Returns:
    切换结果，包括新激活的策略组合
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "regime": {
                    "type": "string",
                    "enum": ["BULL", "BEAR", "VOLATILE", "RECOVERY", "DISTRIBUTION"],
                    "description": "市场环境"
                },
                "confidence": {
                    "type": "number",
                    "default": 0.5,
                    "description": "置信度"
                }
            },
            "required": ["regime"]
        }
    },
    {
        "name": "strategy.switch.advice",
        "description": """获取当前策略建议

Args:
    current_holdings: 当前持仓比例

Returns:
    仓位建议和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "current_holdings": {
                    "type": "number",
                    "default": 0.0,
                    "description": "当前持仓比例"
                }
            }
        }
    },
    {
        "name": "strategy.switch.signals",
        "description": """获取股票信号

根据当前激活的策略组合生成股票交易信号

Args:
    stocks: 股票代码列表
    date: 日期

Returns:
    各股票的综合信号和操作建议
""",
        "inputSchema": {
            "type": "object",
            "properties": {
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "股票代码列表"
                },
                "date": {
                    "type": "string",
                    "description": "日期"
                }
            },
            "required": ["stocks"]
        }
    },
    {
        "name": "strategy.switch.history",
        "description": """获取策略切换历史

Returns:
    历史切换记录
""",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


# ============ Tool Handlers ============

def handle_update(params: Dict[str, Any]) -> Dict[str, Any]:
    """更新市场环境"""
    try:
        manager = _get_manager()
        regime = params.get('regime')
        confidence = params.get('confidence', 0.5)
        
        result = manager.update_regime(regime, confidence)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        logger.error(f"更新环境失败: {e}")
        return {"success": False, "error": str(e)}


def handle_advice(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取策略建议"""
    try:
        manager = _get_manager()
        current_holdings = params.get('current_holdings', 0.0)
        
        advice = manager.get_position_advice(current_holdings)
        
        return {
            "success": True,
            "data": {
                "target_position": advice.target_position,
                "current_regime": advice.current_regime,
                "strategy_weights": advice.strategy_weights,
                "risk_level": advice.risk_level,
                "action": advice.action,
                "reason": advice.reason
            }
        }
    except Exception as e:
        logger.error(f"获取建议失败: {e}")
        return {"success": False, "error": str(e)}


def handle_signals(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取股票信号"""
    try:
        manager = _get_manager()
        stocks = params.get('stocks', [])
        date = params.get('date')
        
        signals = manager.get_stock_signals(stocks, date)
        
        return {
            "success": True,
            "data": signals,
            "count": len(signals)
        }
    except Exception as e:
        logger.error(f"获取信号失败: {e}")
        return {"success": False, "error": str(e)}


def handle_history(params: Dict[str, Any]) -> Dict[str, Any]:
    """获取切换历史"""
    try:
        manager = _get_manager()
        history = manager.get_regime_history()
        
        return {
            "success": True,
            "data": history,
            "count": len(history)
        }
    except Exception as e:
        logger.error(f"获取历史失败: {e}")
        return {"success": False, "error": str(e)}


# Handler映射
STRATEGY_SWITCH_HANDLERS = {
    "strategy.switch.update": handle_update,
    "strategy.switch.advice": handle_advice,
    "strategy.switch.signals": handle_signals,
    "strategy.switch.history": handle_history
}


def handle_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """统一工具处理入口"""
    handler = STRATEGY_SWITCH_HANDLERS.get(name)
    if handler:
        return handler(arguments)
    return {"success": False, "error": f"Unknown tool: {name}"}









































