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


# ==================== 补充工具 ====================

def _handle_scorecard_batch(**kwargs) -> dict:
    """批量计算多只股票的评分"""
    security_ids = kwargs.get("security_ids", [])
    
    if not security_ids:
        return {"success": False, "error": "需要提供security_ids列表"}
    
    engine = get_scorecard_engine()
    results = []
    
    for sid in security_ids[:50]:  # 限制最多50只
        try:
            card = engine.compute(sid)
            results.append({
                "security_id": sid,
                "total_score": card.total_score,
                "grade": card.grade,
                "current_stage": card.current_stage
            })
        except Exception as e:
            results.append({
                "security_id": sid,
                "error": str(e)
            })
    
    # 按评分排序
    results.sort(key=lambda x: x.get("total_score", 0), reverse=True)
    
    return {
        "success": True,
        "count": len(results),
        "results": results
    }

# 添加到工具列表
M32_TOOLS.append({
    "name": "scorecard.batch",
    "description": "批量计算多只股票的评分，返回排序结果",
    "handler": _handle_scorecard_batch
})


# ==================== 补充工具: scorecard.compare, scorecard.rank, scorecard.stats ====================

def _handle_scorecard_compare(**kwargs) -> dict:
    """比较两只股票的评分"""
    sid1 = kwargs.get("security_id_1")
    sid2 = kwargs.get("security_id_2")
    
    if not sid1 or not sid2:
        return {"success": False, "error": "需要提供两个security_id"}
    
    engine = get_scorecard_engine()
    card1 = engine.compute(sid1)
    card2 = engine.compute(sid2)
    
    comparison = {
        "security_id_1": sid1,
        "security_id_2": sid2,
        "score_1": card1.total_score,
        "score_2": card2.total_score,
        "grade_1": card1.grade,
        "grade_2": card2.grade,
        "winner": sid1 if card1.total_score >= card2.total_score else sid2,
        "score_diff": abs(card1.total_score - card2.total_score),
        "dimension_comparison": []
    }
    
    # 维度对比
    for dim in engine.DIMENSIONS:
        dim_name = dim["name"]
        score1 = card1.dimension_scores.get(dim_name, 0)
        score2 = card2.dimension_scores.get(dim_name, 0)
        comparison["dimension_comparison"].append({
            "dimension": dim_name,
            "score_1": score1,
            "score_2": score2,
            "diff": score1 - score2
        })
    
    return {"success": True, "comparison": comparison}


def _handle_scorecard_rank(**kwargs) -> dict:
    """股票评分排名"""
    security_ids = kwargs.get("security_ids", [])
    top_n = kwargs.get("top_n", 10)
    
    engine = get_scorecard_engine()
    
    # 如果没有指定股票，从数据库获取
    if not security_ids:
        if engine._collection:
            docs = engine._collection.find().sort("total_score", -1).limit(top_n)
            rankings = []
            rank = 1
            for doc in docs:
                rankings.append({
                    "rank": rank,
                    "security_id": doc.get("security_id"),
                    "total_score": doc.get("total_score", 0),
                    "grade": doc.get("grade", "?"),
                    "current_stage": doc.get("current_stage", "?")
                })
                rank += 1
            return {"success": True, "rankings": rankings, "count": len(rankings)}
        else:
            return {"success": False, "error": "无数据可排名"}
    
    # 批量计算并排序
    results = []
    for sid in security_ids:
        try:
            card = engine.compute(sid)
            results.append({
                "security_id": sid,
                "total_score": card.total_score,
                "grade": card.grade,
                "current_stage": card.current_stage
            })
        except Exception:
            pass
    
    results.sort(key=lambda x: x["total_score"], reverse=True)
    
    rankings = []
    for rank, r in enumerate(results[:top_n], 1):
        rankings.append({"rank": rank, **r})
    
    return {"success": True, "rankings": rankings, "count": len(rankings)}


def _handle_scorecard_stats(**kwargs) -> dict:
    """评分卡统计"""
    engine = get_scorecard_engine()
    
    if engine._collection is None:
        return {"success": False, "error": "MongoDB未连接"}
    
    total = engine._collection.count_documents({})
    
    # 按等级统计
    by_grade = {}
    for grade in ["A", "B", "C", "D"]:
        count = engine._collection.count_documents({"grade": grade})
        if count > 0:
            by_grade[grade] = count
    
    # 按阶段统计
    by_stage = {}
    for stage in ["S0", "S1", "S2", "S3", "S4", "S5"]:
        count = engine._collection.count_documents({"current_stage": stage})
        if count > 0:
            by_stage[stage] = count
    
    # 平均分
    pipeline = [{"$group": {"_id": None, "avg_score": {"$avg": "$total_score"}}}]
    avg_result = list(engine._collection.aggregate(pipeline))
    avg_score = avg_result[0]["avg_score"] if avg_result else 0
    
    return {
        "success": True,
        "total": total,
        "by_grade": by_grade,
        "by_stage": by_stage,
        "average_score": round(avg_score, 2)
    }


# 添加到工具列表
M32_TOOLS.append({
    "name": "scorecard.compare",
    "description": "比较两只股票的评分",
    "handler": _handle_scorecard_compare
})

M32_TOOLS.append({
    "name": "scorecard.rank",
    "description": "股票评分排名",
    "handler": _handle_scorecard_rank
})

M32_TOOLS.append({
    "name": "scorecard.stats",
    "description": "评分卡统计",
    "handler": _handle_scorecard_stats
})
