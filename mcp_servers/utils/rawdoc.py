#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RawDoc - 原始文档存储
====================

M3.1核心组件：存储和管理原始文档（公告/年报/互动易/新闻）

功能：
1. 文档入库与去重
2. 文档查询与检索
3. 文档处理状态追踪
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class DocType(Enum):
    """文档类型"""
    ANNOUNCEMENT = "announcement"       # 公告
    ANNUAL_REPORT = "annual_report"     # 年报
    INTERIM_REPORT = "interim_report"   # 中报/季报
    INTERACTIVE_QA = "interactive_qa"   # 互动易问答
    NEWS = "news"                       # 新闻
    RESEARCH_REPORT = "research_report" # 研报摘要


class DocSource(Enum):
    """文档来源"""
    SSE = "sse"                 # 上交所
    SZSE = "szse"               # 深交所
    CNINFO = "cninfo"           # 巨潮资讯网
    SSE_INTERACT = "sse_interact"   # 上证e互动
    SZSE_INTERACT = "szse_interact" # 深证互动易
    EASTMONEY = "eastmoney"     # 东方财富
    CAILIAN = "cailian"         # 财联社
    MANUAL = "manual"           # 手动导入


@dataclass
class RawDoc:
    """
    原始文档
    
    存储来自各数据源的原始文档
    """
    doc_id: str
    doc_type: str           # DocType
    source: str             # DocSource
    security_id: str        # 股票代码 如 000001.SZ
    
    # 内容
    title: str
    content: str
    summary: str = ""       # 摘要
    url: str = ""           # 原文链接
    
    # 时间
    publish_time: str = ""  # 发布时间
    fetch_time: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # 元数据
    credibility: float = 1.0    # 可信度权重 (0-1)
    content_hash: str = ""      # 内容哈希（用于去重）
    word_count: int = 0
    
    # 处理状态
    processed: bool = False     # 是否已抽取事件
    event_count: int = 0        # 抽取的事件数
    
    # 标签
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = self._compute_hash()
        if not self.word_count:
            self.word_count = len(self.content)
    
    def _compute_hash(self) -> str:
        """计算内容哈希"""
        content = f"{self.security_id}:{self.title}:{self.content[:500]}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RawDoc":
        return cls(**data)


class RawDocStore:
    """
    原始文档存储
    
    管理RawDoc的存储、查询和去重
    """
    
    def __init__(self):
        self._mongo_db = None
        self._collection = None
        self._init_mongo()
    
    def _init_mongo(self):
        """初始化MongoDB连接"""
        try:
            from pymongo import MongoClient, DESCENDING
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            self._mongo_db = client.get_database("trquant")
            self._collection = self._mongo_db.raw_docs
            
            # 创建索引
            self._collection.create_index([("security_id", 1), ("publish_time", DESCENDING)])
            self._collection.create_index([("doc_type", 1), ("publish_time", DESCENDING)])
            self._collection.create_index([("content_hash", 1)], unique=True, sparse=True)
            self._collection.create_index([("processed", 1)])
            
            logger.info("RawDocStore: MongoDB连接成功")
        except Exception as e:
            logger.warning(f"RawDocStore: MongoDB连接失败: {e}")
    
    def ingest(self, doc: RawDoc) -> Dict[str, Any]:
        """
        入库文档
        
        自动去重，返回入库结果
        """
        if self._collection is None:
            return {"success": False, "error": "MongoDB未连接"}
        
        try:
            # 检查是否已存在
            existing = self._collection.find_one({"content_hash": doc.content_hash})
            if existing:
                return {
                    "success": False,
                    "error": "文档已存在",
                    "existing_doc_id": existing.get("doc_id"),
                    "duplicate": True
                }
            
            # 入库
            self._collection.insert_one(doc.to_dict())
            logger.info(f"[RawDoc] 入库: {doc.doc_id} ({doc.security_id})")
            
            return {
                "success": True,
                "doc_id": doc.doc_id,
                "content_hash": doc.content_hash
            }
        except Exception as e:
            logger.error(f"[RawDoc] 入库失败: {e}")
            return {"success": False, "error": str(e)}
    
    def batch_ingest(self, docs: List[RawDoc]) -> Dict[str, Any]:
        """批量入库"""
        results = {"success": 0, "duplicate": 0, "failed": 0, "details": []}
        
        for doc in docs:
            result = self.ingest(doc)
            if result.get("success"):
                results["success"] += 1
            elif result.get("duplicate"):
                results["duplicate"] += 1
            else:
                results["failed"] += 1
            results["details"].append(result)
        
        return results
    
    def get(self, doc_id: str) -> Optional[RawDoc]:
        """获取文档"""
        if self._collection is None:
            return None
        
        data = self._collection.find_one({"doc_id": doc_id})
        if data:
            data.pop("_id", None)
            return RawDoc.from_dict(data)
        return None
    
    def search(
        self,
        security_id: str = None,
        doc_type: str = None,
        source: str = None,
        start_date: str = None,
        end_date: str = None,
        keyword: str = None,
        processed: bool = None,
        limit: int = 100
    ) -> List[RawDoc]:
        """搜索文档"""
        if self._collection is None:
            return []
        
        query = {}
        if security_id:
            query["security_id"] = security_id
        if doc_type:
            query["doc_type"] = doc_type
        if source:
            query["source"] = source
        if processed is not None:
            query["processed"] = processed
        if start_date:
            query["publish_time"] = {"$gte": start_date}
        if end_date:
            if "publish_time" in query:
                query["publish_time"]["$lte"] = end_date
            else:
                query["publish_time"] = {"$lte": end_date}
        if keyword:
            query["$or"] = [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"content": {"$regex": keyword, "$options": "i"}}
            ]
        
        results = []
        for data in self._collection.find(query).sort("publish_time", -1).limit(limit):
            data.pop("_id", None)
            results.append(RawDoc.from_dict(data))
        
        return results
    
    def mark_processed(self, doc_id: str, event_count: int = 0) -> bool:
        """标记文档已处理"""
        if self._collection is None:
            return False
        
        result = self._collection.update_one(
            {"doc_id": doc_id},
            {"$set": {"processed": True, "event_count": event_count}}
        )
        return result.modified_count > 0
    
    def get_unprocessed(self, limit: int = 100) -> List[RawDoc]:
        """获取未处理的文档"""
        return self.search(processed=False, limit=limit)
    
    def stats(self) -> Dict[str, Any]:
        """统计信息"""
        if self._collection is None:
            return {"error": "MongoDB未连接"}
        
        total = self._collection.count_documents({})
        processed = self._collection.count_documents({"processed": True})
        
        # 按类型统计
        by_type = {}
        for doc_type in DocType:
            count = self._collection.count_documents({"doc_type": doc_type.value})
            if count > 0:
                by_type[doc_type.value] = count
        
        # 按来源统计
        by_source = {}
        for source in DocSource:
            count = self._collection.count_documents({"source": source.value})
            if count > 0:
                by_source[source.value] = count
        
        return {
            "total": total,
            "processed": processed,
            "unprocessed": total - processed,
            "by_type": by_type,
            "by_source": by_source
        }
    
    def delete(self, doc_id: str) -> bool:
        """删除文档"""
        if self._collection is None:
            return False
        
        result = self._collection.delete_one({"doc_id": doc_id})
        return result.deleted_count > 0


# 全局存储实例
_store: Optional[RawDocStore] = None

def get_rawdoc_store() -> RawDocStore:
    """获取RawDoc存储实例"""
    global _store
    if _store is None:
        _store = RawDocStore()
    return _store


# 便捷函数
def create_doc(
    security_id: str,
    title: str,
    content: str,
    doc_type: str = "announcement",
    source: str = "manual",
    publish_time: str = None,
    url: str = "",
    tags: List[str] = None
) -> RawDoc:
    """创建文档的便捷函数"""
    import uuid
    
    doc_id = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    return RawDoc(
        doc_id=doc_id,
        doc_type=doc_type,
        source=source,
        security_id=security_id,
        title=title,
        content=content,
        publish_time=publish_time or datetime.now().isoformat(),
        url=url,
        tags=tags or []
    )
