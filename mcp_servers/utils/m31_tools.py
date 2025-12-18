#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
M3.1 MCP工具接口
===============

提供RawDoc和Event的MCP工具
"""

from typing import Dict, Any, List
from .rawdoc import get_rawdoc_store, create_doc, RawDoc, DocType, DocSource
from .event_extractor import get_event_extractor, Event, EventType


# ==================== RawDoc 工具 ====================

def doc_ingest(
    security_id: str,
    title: str,
    content: str,
    doc_type: str = "announcement",
    source: str = "manual",
    publish_time: str = None,
    url: str = "",
    tags: List[str] = None
) -> Dict[str, Any]:
    """入库原始文档"""
    store = get_rawdoc_store()
    doc = create_doc(
        security_id=security_id,
        title=title,
        content=content,
        doc_type=doc_type,
        source=source,
        publish_time=publish_time,
        url=url,
        tags=tags
    )
    result = store.ingest(doc)
    return result


def doc_search(
    security_id: str = None,
    doc_type: str = None,
    source: str = None,
    start_date: str = None,
    end_date: str = None,
    keyword: str = None,
    processed: bool = None,
    limit: int = 100
) -> Dict[str, Any]:
    """搜索文档"""
    store = get_rawdoc_store()
    docs = store.search(
        security_id=security_id,
        doc_type=doc_type,
        source=source,
        start_date=start_date,
        end_date=end_date,
        keyword=keyword,
        processed=processed,
        limit=limit
    )
    return {
        "success": True,
        "count": len(docs),
        "docs": [d.to_dict() for d in docs]
    }


def doc_get(doc_id: str) -> Dict[str, Any]:
    """获取文档"""
    store = get_rawdoc_store()
    doc = store.get(doc_id)
    if not doc:
        return {"success": False, "error": "文档不存在"}
    return {"success": True, "doc": doc.to_dict()}


def doc_stats() -> Dict[str, Any]:
    """文档统计"""
    store = get_rawdoc_store()
    return {"success": True, **store.stats()}


def doc_dedup(content_hash: str = None) -> Dict[str, Any]:
    """检查去重"""
    store = get_rawdoc_store()
    if not store._collection:
        return {"success": False, "error": "MongoDB未连接"}
    
    if content_hash:
        existing = store._collection.find_one({"content_hash": content_hash})
        return {
            "success": True,
            "duplicate": existing is not None,
            "existing_doc_id": existing.get("doc_id") if existing else None
        }
    
    # 返回重复统计
    pipeline = [
        {"$group": {"_id": "$content_hash", "count": {"$sum": 1}}},
        {"$match": {"count": {"$gt": 1}}}
    ]
    duplicates = list(store._collection.aggregate(pipeline))
    return {
        "success": True,
        "duplicate_hashes": len(duplicates)
    }


# ==================== Event 工具 ====================

def event_extract(doc_id: str = None, auto_save: bool = True) -> Dict[str, Any]:
    """从文档抽取事件"""
    store = get_rawdoc_store()
    extractor = get_event_extractor()
    
    if doc_id:
        # 单个文档
        doc = store.get(doc_id)
        if not doc:
            return {"success": False, "error": "文档不存在"}
        
        events = extractor.extract_from_doc(doc)
        
        if auto_save and events:
            extractor.batch_save(events)
            store.mark_processed(doc_id, len(events))
        
        return {
            "success": True,
            "doc_id": doc_id,
            "event_count": len(events),
            "events": [e.to_dict() for e in events]
        }
    else:
        # 批量处理未处理文档
        unprocessed = store.get_unprocessed(limit=50)
        total_events = 0
        results = []
        
        for doc in unprocessed:
            events = extractor.extract_from_doc(doc)
            if auto_save and events:
                extractor.batch_save(events)
                store.mark_processed(doc.doc_id, len(events))
            
            total_events += len(events)
            results.append({
                "doc_id": doc.doc_id,
                "event_count": len(events)
            })
        
        return {
            "success": True,
            "processed_docs": len(unprocessed),
            "total_events": total_events,
            "results": results
        }


def event_list(
    security_id: str = None,
    event_type: str = None,
    start_date: str = None,
    end_date: str = None,
    verified: bool = None,
    limit: int = 100
) -> Dict[str, Any]:
    """列出事件"""
    extractor = get_event_extractor()
    events = extractor.search(
        security_id=security_id,
        event_type=event_type,
        start_date=start_date,
        end_date=end_date,
        verified=verified,
        limit=limit
    )
    return {
        "success": True,
        "count": len(events),
        "events": [e.to_dict() for e in events]
    }


def event_validate(event_id: str, verified: bool = True, correction: Dict = None) -> Dict[str, Any]:
    """验证/纠错事件"""
    extractor = get_event_extractor()
    success = extractor.verify_event(event_id, verified, correction)
    return {"success": success, "event_id": event_id}


def event_feedback(event_id: str, correct_type: str = None, notes: str = "") -> Dict[str, Any]:
    """人工反馈纠错"""
    correction = {}
    if correct_type:
        correction["event_type"] = correct_type
    if notes:
        correction["feedback_notes"] = notes
    
    return event_validate(event_id, verified=True, correction=correction if correction else None)


def event_stats() -> Dict[str, Any]:
    """事件统计"""
    extractor = get_event_extractor()
    return {"success": True, **extractor.stats()}


def event_types() -> Dict[str, Any]:
    """获取事件类型列表"""
    extractor = get_event_extractor()
    return {
        "success": True,
        "types": extractor.get_event_types()
    }


# ==================== MCP工具定义 ====================

M31_TOOLS = [
    # RawDoc工具
    {"name": "doc.ingest", "description": "入库原始文档", "handler": doc_ingest},
    {"name": "doc.search", "description": "搜索文档", "handler": doc_search},
    {"name": "doc.get", "description": "获取文档", "handler": doc_get},
    {"name": "doc.stats", "description": "文档统计", "handler": doc_stats},
    {"name": "doc.dedup", "description": "检查去重", "handler": doc_dedup},
    
    # Event工具
    {"name": "event.extract", "description": "从文档抽取事件", "handler": event_extract},
    {"name": "event.list", "description": "列出事件", "handler": event_list},
    {"name": "event.validate", "description": "验证事件", "handler": event_validate},
    {"name": "event.feedback", "description": "人工反馈纠错", "handler": event_feedback},
    {"name": "event.stats", "description": "事件统计", "handler": event_stats},
    {"name": "event.types", "description": "获取事件类型", "handler": event_types},
]


def get_m31_tool_names() -> List[str]:
    """获取所有M3.1工具名称"""
    return [t["name"] for t in M31_TOOLS]


def call_m31_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """调用M3.1工具"""
    for tool in M31_TOOLS:
        if tool["name"] == tool_name:
            return tool["handler"](**kwargs)
    return {"success": False, "error": f"未知工具: {tool_name}"}
