#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EventExtractor - 事件抽取引擎
============================

M3.1核心组件：从RawDoc中抽取十倍股相关事件

功能：
1. 规则引擎抽取
2. LLM辅助分类
3. 人工纠错入口
"""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(Enum):
    """
    十倍股事件类型
    
    基于altdata数据源.txt的事件标签字典V1
    """
    # 验证类事件
    SAMPLE_DELIVERY = "sample_delivery"         # 送样
    VALIDATION_PASS = "validation_pass"         # 验证通过
    CERTIFICATION = "certification"             # 认证获取
    
    # 订单类事件
    SMALL_BATCH = "small_batch"                 # 小批量订单
    MASS_PRODUCTION = "mass_production"         # 量产订单
    REPEAT_ORDER = "repeat_order"               # 重复订单
    
    # 客户类事件
    SUPPLIER_ENTRY = "supplier_entry"           # 进入供应商体系
    NEW_CUSTOMER = "new_customer"               # 新客户
    KEY_CUSTOMER = "key_customer"               # 大客户进展
    
    # 扩产类事件
    EXPANSION = "expansion"                     # 扩产
    NEW_LINE = "new_line"                       # 新产线
    ENVIRONMENTAL = "environmental"             # 环评公示
    PROJECT_APPROVAL = "project_approval"       # 项目审批
    
    # 组织类事件
    EXECUTIVE_CHANGE = "executive_change"       # 高管变更
    EQUITY_INCENTIVE = "equity_incentive"       # 股权激励
    HIRING_SURGE = "hiring_surge"               # 招聘激增
    
    # 财务类事件
    REVENUE_INFLECTION = "revenue_inflection"   # 营收拐点
    MARGIN_IMPROVEMENT = "margin_improvement"   # 毛利改善
    
    # 其他
    OTHER = "other"


# Stage影响映射
STAGE_IMPACT = {
    EventType.SAMPLE_DELIVERY: ("S1", "S2"),
    EventType.VALIDATION_PASS: ("S2", "S3"),
    EventType.CERTIFICATION: ("S1", "S2"),
    EventType.SMALL_BATCH: ("S2", "S3"),
    EventType.MASS_PRODUCTION: ("S3", "S4"),
    EventType.SUPPLIER_ENTRY: ("S2", "S3"),
    EventType.EXPANSION: ("S3", "S4"),
    EventType.NEW_LINE: ("S3", "S4"),
    EventType.ENVIRONMENTAL: ("S2", "S3"),
}


@dataclass
class Event:
    """
    事件对象
    
    从RawDoc中抽取的结构化事件
    """
    event_id: str
    event_type: str             # EventType
    security_id: str            # 股票代码
    event_date: str             # 事件日期
    
    # 关联
    source_doc_id: str          # 来源文档ID
    
    # 抽取信息
    confidence: float = 0.0     # 置信度 (0-1)
    extracted_by: str = "rule"  # rule/llm/manual
    
    # 事件详情
    title: str = ""             # 事件标题
    summary: str = ""           # 事件摘要
    details: Dict = field(default_factory=dict)  # 详细信息
    
    # Stage影响
    stage_from: str = ""        # 起始Stage
    stage_to: str = ""          # 目标Stage
    
    # 人工标注
    verified: bool = False      # 是否人工验证
    corrected: bool = False     # 是否被纠错
    
    # 时间戳
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(**data)


class EventExtractor:
    """
    事件抽取引擎
    
    支持规则抽取和LLM辅助
    """
    
    # 规则引擎：关键词模式
    EXTRACTION_RULES = {
        EventType.SAMPLE_DELIVERY: {
            "keywords": ["送样", "样品", "试样", "样机", "送测"],
            "patterns": [
                r"(已|完成|开始).*送样",
                r"送样.*客户",
                r"样品.*验证"
            ],
            "confidence": 0.7
        },
        EventType.VALIDATION_PASS: {
            "keywords": ["验证通过", "认证通过", "验证完成", "测试通过"],
            "patterns": [
                r"(验证|认证|测试).*通过",
                r"通过.*验证",
                r"(完成|取得).*认证"
            ],
            "confidence": 0.8
        },
        EventType.CERTIFICATION: {
            "keywords": ["认证", "资质", "ISO", "IATF", "体系认证"],
            "patterns": [
                r"取得.*认证",
                r"获得.*资质",
                r"通过.*体系.*认证"
            ],
            "confidence": 0.75
        },
        EventType.SMALL_BATCH: {
            "keywords": ["小批量", "试产", "小规模", "首批"],
            "patterns": [
                r"小批量.*生产",
                r"(开始|启动).*试产",
                r"首批.*订单"
            ],
            "confidence": 0.7
        },
        EventType.MASS_PRODUCTION: {
            "keywords": ["量产", "批量生产", "大规模生产", "规模化"],
            "patterns": [
                r"(实现|达到).*量产",
                r"批量.*供货",
                r"规模化.*生产"
            ],
            "confidence": 0.8
        },
        EventType.SUPPLIER_ENTRY: {
            "keywords": ["供应商", "供应体系", "合格供应商", "供应链"],
            "patterns": [
                r"进入.*供应(商|体系|链)",
                r"成为.*供应商",
                r"纳入.*供应(商|体系)"
            ],
            "confidence": 0.8
        },
        EventType.EXPANSION: {
            "keywords": ["扩产", "产能扩张", "扩建", "增产"],
            "patterns": [
                r"(计划|拟|将).*扩产",
                r"产能.*扩张",
                r"扩建.*项目"
            ],
            "confidence": 0.75
        },
        EventType.NEW_LINE: {
            "keywords": ["新产线", "新建产线", "投产", "建设产线"],
            "patterns": [
                r"新(建|增).*产线",
                r"产线.*投产",
                r"建设.*生产线"
            ],
            "confidence": 0.75
        },
        EventType.ENVIRONMENTAL: {
            "keywords": ["环评", "环境影响", "环保审批"],
            "patterns": [
                r"环评.*公示",
                r"环境影响.*评价",
                r"通过.*环评"
            ],
            "confidence": 0.8
        },
        EventType.EXECUTIVE_CHANGE: {
            "keywords": ["总经理", "董事长", "高管", "任命", "离职"],
            "patterns": [
                r"(任命|聘任).*总经理",
                r"(董事长|总经理).*变更",
                r"高管.*调整"
            ],
            "confidence": 0.9
        },
        EventType.EQUITY_INCENTIVE: {
            "keywords": ["股权激励", "期权", "限制性股票", "员工持股"],
            "patterns": [
                r"股权激励.*计划",
                r"授予.*期权",
                r"员工持股.*计划"
            ],
            "confidence": 0.85
        }
    }
    
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
            self._collection = self._mongo_db.events
            
            # 创建索引
            self._collection.create_index([("security_id", 1), ("event_type", 1), ("event_date", DESCENDING)])
            self._collection.create_index([("source_doc_id", 1)])
            self._collection.create_index([("event_type", 1), ("event_date", DESCENDING)])
            
            logger.info("EventExtractor: MongoDB连接成功")
        except Exception as e:
            logger.warning(f"EventExtractor: MongoDB连接失败: {e}")
    
    def extract_from_doc(self, doc) -> List[Event]:
        """
        从文档中抽取事件
        
        Args:
            doc: RawDoc对象或字典
        
        Returns:
            抽取的事件列表
        """
        if hasattr(doc, 'to_dict'):
            doc = doc.to_dict()
        
        events = []
        content = f"{doc.get('title', '')} {doc.get('content', '')}"
        security_id = doc.get('security_id', '')
        doc_id = doc.get('doc_id', '')
        publish_time = doc.get('publish_time', datetime.now().isoformat())
        
        # 规则抽取
        for event_type, rules in self.EXTRACTION_RULES.items():
            confidence, matches = self._match_rules(content, rules)
            
            if confidence > 0:
                import uuid
                event = Event(
                    event_id=f"evt_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
                    event_type=event_type.value,
                    security_id=security_id,
                    event_date=publish_time[:10] if publish_time else "",
                    source_doc_id=doc_id,
                    confidence=confidence,
                    extracted_by="rule",
                    title=doc.get('title', ''),
                    summary=self._generate_summary(content, matches),
                    details={"matches": matches}
                )
                
                # 设置Stage影响
                if event_type in STAGE_IMPACT:
                    event.stage_from, event.stage_to = STAGE_IMPACT[event_type]
                
                events.append(event)
        
        return events
    
    def _match_rules(self, content: str, rules: Dict) -> Tuple[float, List[str]]:
        """匹配规则，返回置信度和匹配项"""
        matches = []
        base_confidence = rules.get("confidence", 0.5)
        
        # 关键词匹配
        for keyword in rules.get("keywords", []):
            if keyword in content:
                matches.append(f"keyword:{keyword}")
        
        # 正则模式匹配
        for pattern in rules.get("patterns", []):
            if re.search(pattern, content):
                matches.append(f"pattern:{pattern[:20]}...")
        
        if not matches:
            return 0, []
        
        # 置信度计算：匹配越多越高
        confidence = min(base_confidence + 0.1 * (len(matches) - 1), 0.95)
        return confidence, matches
    
    def _generate_summary(self, content: str, matches: List[str]) -> str:
        """生成事件摘要"""
        # 简单实现：取前100字符
        return content[:100] + "..." if len(content) > 100 else content
    
    def save_event(self, event: Event) -> Dict[str, Any]:
        """保存事件到数据库"""
        if self._collection is None:
            return {"success": False, "error": "MongoDB未连接"}
        
        try:
            self._collection.insert_one(event.to_dict())
            logger.info(f"[Event] 保存: {event.event_id} ({event.event_type})")
            return {"success": True, "event_id": event.event_id}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def batch_save(self, events: List[Event]) -> Dict[str, Any]:
        """批量保存事件"""
        results = {"success": 0, "failed": 0}
        for event in events:
            result = self.save_event(event)
            if result.get("success"):
                results["success"] += 1
            else:
                results["failed"] += 1
        return results
    
    def search(
        self,
        security_id: str = None,
        event_type: str = None,
        start_date: str = None,
        end_date: str = None,
        verified: bool = None,
        limit: int = 100
    ) -> List[Event]:
        """搜索事件"""
        if self._collection is None:
            return []
        
        query = {}
        if security_id:
            query["security_id"] = security_id
        if event_type:
            query["event_type"] = event_type
        if verified is not None:
            query["verified"] = verified
        if start_date:
            query["event_date"] = {"$gte": start_date}
        if end_date:
            if "event_date" in query:
                query["event_date"]["$lte"] = end_date
            else:
                query["event_date"] = {"$lte": end_date}
        
        results = []
        for data in self._collection.find(query).sort("event_date", -1).limit(limit):
            data.pop("_id", None)
            results.append(Event.from_dict(data))
        
        return results
    
    def verify_event(self, event_id: str, verified: bool = True, correction: Dict = None) -> bool:
        """人工验证事件"""
        if self._collection is None:
            return False
        
        update = {"$set": {"verified": verified}}
        if correction:
            update["$set"]["corrected"] = True
            update["$set"].update(correction)
        
        result = self._collection.update_one({"event_id": event_id}, update)
        return result.modified_count > 0
    
    def stats(self) -> Dict[str, Any]:
        """统计信息"""
        if self._collection is None:
            return {"error": "MongoDB未连接"}
        
        total = self._collection.count_documents({})
        verified = self._collection.count_documents({"verified": True})
        
        # 按类型统计
        by_type = {}
        for event_type in EventType:
            count = self._collection.count_documents({"event_type": event_type.value})
            if count > 0:
                by_type[event_type.value] = count
        
        return {
            "total": total,
            "verified": verified,
            "unverified": total - verified,
            "by_type": by_type
        }
    
    def get_event_types(self) -> List[Dict[str, str]]:
        """获取所有事件类型"""
        return [
            {
                "type": et.value,
                "name": et.name,
                "stage_impact": STAGE_IMPACT.get(et, (None, None))
            }
            for et in EventType
        ]


# 全局实例
_extractor: Optional[EventExtractor] = None

def get_event_extractor() -> EventExtractor:
    """获取事件抽取器"""
    global _extractor
    if _extractor is None:
        _extractor = EventExtractor()
    return _extractor
