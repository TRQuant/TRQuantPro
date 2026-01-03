#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场环境判断MCP工具
==================

提供市场环境判断的MCP Server工具接口

工具列表：
1. detect_market_regime - 综合检测市场环境
2. analyze_macro - 宏观经济分析
3. analyze_capital - 资金流向分析
4. analyze_technical - 技术分析
5. analyze_sentiment - 市场情绪分析
6. get_regime_history - 获取环境判断历史
"""

import sys
import os
import json
from typing import Dict, Any, Optional

PROJECT_ROOT = "/home/taotao/dev/QuantTest/TRQuant"
sys.path.insert(0, PROJECT_ROOT)

from core.market_regime.comprehensive_regime_detector import (
    ComprehensiveRegimeDetector,
    get_detector,
    detect_market_regime,
    MarketRegime,
)


def tool_detect_market_regime(date: str = None) -> Dict[str, Any]:
    """
    MCP工具：综合检测市场环境
    
    参数：
        date: 分析日期，格式 YYYY-MM-DD，默认今天
    
    返回：
        {
            "regime": "BULL/BEAR/VOLATILE/RECOVERY/DISTRIBUTION",
            "confidence": 0-100,
            "composite_score": -100到100,
            "dimensions": {
                "macro": {...},
                "capital": {...},
                "technical": {...},
                "sentiment": {...}
            },
            "recommended_strategy": "策略名称",
            "recommended_position": 0-1,
            "risk_level": "low/medium/high"
        }
    """
    try:
        result = detect_market_regime(date)
        return {
            "success": True,
            "data": result,
            "message": f"市场环境: {result['regime']}, 置信度: {result['confidence']:.1f}%"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"分析失败: {e}"
        }


def tool_analyze_macro(date: str = None) -> Dict[str, Any]:
    """
    MCP工具：宏观经济分析
    
    分析指标：PMI、CPI、M2增速、社融
    """
    try:
        detector = get_detector()
        result = detector.analyze_macro(date)
        return {
            "success": True,
            "data": {
                "name": result.name,
                "score": result.score,
                "signal": result.signal.name,
                "indicators": result.indicators,
                "description": result.description,
                "data_source": result.data_source,
            },
            "message": f"宏观得分: {result.score:.1f}, 信号: {result.signal.name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_analyze_capital(date: str = None) -> Dict[str, Any]:
    """
    MCP工具：资金流向分析
    
    分析指标：北向资金、融资融券、主力资金
    """
    try:
        detector = get_detector()
        result = detector.analyze_capital(date)
        return {
            "success": True,
            "data": {
                "name": result.name,
                "score": result.score,
                "signal": result.signal.name,
                "indicators": result.indicators,
                "description": result.description,
                "data_source": result.data_source,
            },
            "message": f"资金得分: {result.score:.1f}, 信号: {result.signal.name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_analyze_technical(date: str = None) -> Dict[str, Any]:
    """
    MCP工具：技术分析
    
    分析指标：指数趋势、波动率、成交量、均线系统
    """
    try:
        detector = get_detector()
        result = detector.analyze_technical(date)
        return {
            "success": True,
            "data": {
                "name": result.name,
                "score": result.score,
                "signal": result.signal.name,
                "indicators": result.indicators,
                "description": result.description,
                "data_source": result.data_source,
            },
            "message": f"技术得分: {result.score:.1f}, 信号: {result.signal.name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_analyze_sentiment(date: str = None) -> Dict[str, Any]:
    """
    MCP工具：市场情绪分析
    
    分析指标：涨跌比、涨停跌停、连板数、换手率
    """
    try:
        detector = get_detector()
        result = detector.analyze_sentiment(date)
        return {
            "success": True,
            "data": {
                "name": result.name,
                "score": result.score,
                "signal": result.signal.name,
                "indicators": result.indicators,
                "description": result.description,
                "data_source": result.data_source,
            },
            "message": f"情绪得分: {result.score:.1f}, 信号: {result.signal.name}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_get_regime_history(limit: int = 10) -> Dict[str, Any]:
    """
    MCP工具：获取环境判断历史
    """
    try:
        detector = get_detector()
        history = detector._history[-limit:] if detector._history else []
        
        return {
            "success": True,
            "data": [
                {
                    "date": r.analysis_date,
                    "regime": r.regime.value,
                    "confidence": r.confidence,
                    "score": r.composite_score,
                }
                for r in history
            ],
            "count": len(history),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_get_strategy_recommendation() -> Dict[str, Any]:
    """
    MCP工具：获取策略建议
    
    基于当前市场环境给出策略建议
    """
    try:
        result = detect_market_regime()
        
        strategy_details = {
            "BULL": {
                "strategy": "趋势跟踪策略",
                "description": "市场处于上升趋势，适合追涨强势股",
                "focus": ["动量因子", "趋势突破", "成长股"],
                "avoid": ["做空", "过度对冲"],
            },
            "BEAR": {
                "strategy": "防守型策略",
                "description": "市场下行风险大，以防守为主",
                "focus": ["低波动", "高股息", "现金管理"],
                "avoid": ["高杠杆", "追涨"],
            },
            "VOLATILE": {
                "strategy": "网格交易策略",
                "description": "市场震荡，适合高抛低吸",
                "focus": ["均值回归", "波段操作", "期权策略"],
                "avoid": ["趋势跟踪", "重仓单边"],
            },
            "RECOVERY": {
                "strategy": "价值投资策略",
                "description": "市场底部企稳，适合布局优质资产",
                "focus": ["低估值", "基本面改善", "左侧布局"],
                "avoid": ["追涨杀跌", "短线投机"],
            },
            "DISTRIBUTION": {
                "strategy": "减仓观望策略",
                "description": "市场顶部特征明显，控制风险为主",
                "focus": ["止盈", "仓位管理", "风险对冲"],
                "avoid": ["追高", "加仓"],
            },
        }
        
        regime = result['regime']
        details = strategy_details.get(regime, strategy_details['VOLATILE'])
        
        return {
            "success": True,
            "regime": regime,
            "confidence": result['confidence'],
            "position": result['recommended_position'],
            "strategy": details,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# 工具注册表
TOOLS = {
    "detect_market_regime": tool_detect_market_regime,
    "analyze_macro": tool_analyze_macro,
    "analyze_capital": tool_analyze_capital,
    "analyze_technical": tool_analyze_technical,
    "analyze_sentiment": tool_analyze_sentiment,
    "get_regime_history": tool_get_regime_history,
    "get_strategy_recommendation": tool_get_strategy_recommendation,
}


if __name__ == "__main__":
    # 测试
    print("测试市场环境检测工具...")
    result = tool_detect_market_regime()
    print(json.dumps(result, indent=2, ensure_ascii=False))
