#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
M3.2 MCP工具接口
===============

提供Stage状态机和ScoreCard评分卡的MCP工具
"""

from typing import Dict, Any, List
from .stage_machine import get_stage_machine, Stage, STAGE_DESCRIPTIONS
from .scorecard import get_scorecard_engine


# ==================== Stage 工具 ====================

def stage_compute(security_id: str, event_type: str, event_id: str = "") -> Dict[str, Any]:
    """处理事件，更新状态"""
    machine = get_stage_machine()
    result = machine.process_event(security_id, event_type, event_id)
    return {"success": True, **result}


def stage_get(security_id: str) -> Dict[str, Any]:
    """获取股票阶段"""
    machine = get_stage_machine()
    record = machine.get_stage(security_id)
    if not record:
        return {"success": False, "error": "记录不存在"}
    return {"success": True, "record": record.to_dict()}


def stage_override(security_id: str, new_stage: str, reason: str = "") -> Dict[str, Any]:
    """人工覆盖状态"""
    if new_stage not in [s.value for s in Stage]:
        return {"success": False, "error": f"无效阶段: {new_stage}"}
    
    machine = get_stage_machine()
    success = machine.override_stage(security_id, new_stage, reason)
    return {"success": success, "security_id": security_id, "new_stage": new_stage}


def stage_falsify(security_id: str, reason: str) -> Dict[str, Any]:
    """证伪股票"""
    machine = get_stage_machine()
    success = machine.falsify(security_id, reason)
    return {"success": success, "security_id": security_id, "falsified": True}


def stage_history(security_id: str) -> Dict[str, Any]:
    """获取状态历史"""
    machine = get_stage_machine()
    history = machine.get_history(security_id)
    return {"success": True, "security_id": security_id, "history": history}


def stage_list(stage: str, min_confidence: float = 0.0, limit: int = 100) -> Dict[str, Any]:
    """按阶段列出股票"""
    machine = get_stage_machine()
    records = machine.list_by_stage(stage, min_confidence, limit)
    return {
        "success": True,
        "stage": stage,
        "count": len(records),
        "records": [r.to_dict() for r in records]
    }


def stage_stats() -> Dict[str, Any]:
    """阶段统计"""
    machine = get_stage_machine()
    return {"success": True, **machine.stats()}


def stage_definitions() -> Dict[str, Any]:
    """获取阶段定义"""
    return {
        "success": True,
        "stages": [
            {"stage": s.value, "description": STAGE_DESCRIPTIONS[s]}
            for s in Stage
        ]
    }


# ==================== ScoreCard 工具 ====================

def scorecard_compute(
    security_id: str,
    financial_data: Dict = None
) -> Dict[str, Any]:
    """计算评分卡"""
    engine = get_scorecard_engine()
    machine = get_stage_machine()
    
    # 获取阶段记录
    stage_record = machine.get_stage(security_id)
    stage_dict = stage_record.to_dict() if stage_record else None
    
    # 获取事件
    try:
        from .event_extractor import get_event_extractor
        extractor = get_event_extractor()
        events = extractor.search(security_id=security_id, limit=50)
        events_dict = [e.to_dict() for e in events]
    except:
        events_dict = []
    
    # 计算评分卡
    card = engine.compute(
        security_id=security_id,
        stage_record=stage_dict,
        events=events_dict,
        financial_data=financial_data
    )
    
    return {
        "success": True,
        "card": card.to_dict(),
        "explanation": engine.explain(card)
    }


def scorecard_get(security_id: str) -> Dict[str, Any]:
    """获取最新评分卡"""
    engine = get_scorecard_engine()
    card = engine.get_latest(security_id)
    if not card:
        return {"success": False, "error": "评分卡不存在"}
    return {
        "success": True,
        "card": card.to_dict(),
        "explanation": engine.explain(card)
    }


def scorecard_explain(security_id: str) -> Dict[str, Any]:
    """生成评分解释"""
    engine = get_scorecard_engine()
    card = engine.get_latest(security_id)
    if not card:
        return {"success": False, "error": "评分卡不存在"}
    return {
        "success": True,
        "explanation": engine.explain(card)
    }


def scorecard_history(security_id: str, limit: int = 10) -> Dict[str, Any]:
    """获取评分历史"""
    engine = get_scorecard_engine()
    cards = engine.get_history(security_id, limit)
    return {
        "success": True,
        "security_id": security_id,
        "count": len(cards),
        "history": [c.to_dict() for c in cards]
    }


def scorecard_list_by_grade(grade: str, limit: int = 100) -> Dict[str, Any]:
    """按等级列出评分卡"""
    engine = get_scorecard_engine()
    cards = engine.list_by_grade(grade, limit)
    return {
        "success": True,
        "grade": grade,
        "count": len(cards),
        "cards": [c.to_dict() for c in cards]
    }


def scorecard_dimensions() -> Dict[str, Any]:
    """获取维度定义"""
    engine = get_scorecard_engine()
    return {
        "success": True,
        "dimensions": [
            {
                "key": key,
                "name": config["name"],
                "weight": config["weight"],
                "description": config["description"]
            }
            for key, config in engine.DIMENSIONS.items()
        ]
    }


# ==================== MCP工具定义 ====================

M32_TOOLS = [
    # Stage工具
    {"name": "stage.compute", "description": "处理事件更新状态", "handler": stage_compute},
    {"name": "stage.get", "description": "获取股票阶段", "handler": stage_get},
    {"name": "stage.override", "description": "人工覆盖状态", "handler": stage_override},
    {"name": "stage.falsify", "description": "证伪股票", "handler": stage_falsify},
    {"name": "stage.history", "description": "获取状态历史", "handler": stage_history},
    {"name": "stage.list", "description": "按阶段列出股票", "handler": stage_list},
    {"name": "stage.stats", "description": "阶段统计", "handler": stage_stats},
    {"name": "stage.definitions", "description": "获取阶段定义", "handler": stage_definitions},
    
    # ScoreCard工具
    {"name": "scorecard.compute", "description": "计算评分卡", "handler": scorecard_compute},
    {"name": "scorecard.get", "description": "获取最新评分卡", "handler": scorecard_get},
    {"name": "scorecard.explain", "description": "生成评分解释", "handler": scorecard_explain},
    {"name": "scorecard.history", "description": "获取评分历史", "handler": scorecard_history},
    {"name": "scorecard.list_by_grade", "description": "按等级列出", "handler": scorecard_list_by_grade},
    {"name": "scorecard.dimensions", "description": "获取维度定义", "handler": scorecard_dimensions},
]


def get_m32_tool_names() -> List[str]:
    """获取所有M3.2工具名称"""
    return [t["name"] for t in M32_TOOLS]


def call_m32_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """调用M3.2工具"""
    for tool in M32_TOOLS:
        if tool["name"] == tool_name:
            return tool["handler"](**kwargs)
    return {"success": False, "error": f"未知工具: {tool_name}"}
