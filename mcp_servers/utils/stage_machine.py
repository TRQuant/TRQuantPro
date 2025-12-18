#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
StageMachine - 十倍股状态机
==========================

M3.2核心组件：管理股票在十倍股成长路径中的阶段状态

状态定义：
S0: 观察期 - 有产业链位置，无明显兑现信号
S1: 验证期 - 送样/认证中，尚未确认客户
S2: 导入期 - 已进入客户体系，小批量/验证
S3: 放量期 - 批量订单，扩产明确
S4: 加速期 - 业绩拐点，估值修复
S5: 成熟期 - 主流共识，十倍股特征消失
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class Stage(Enum):
    """十倍股成长阶段"""
    S0 = "S0"  # 观察期
    S1 = "S1"  # 验证期
    S2 = "S2"  # 导入期
    S3 = "S3"  # 放量期
    S4 = "S4"  # 加速期
    S5 = "S5"  # 成熟期


STAGE_DESCRIPTIONS = {
    Stage.S0: "观察期 - 有产业链位置，无明显兑现信号",
    Stage.S1: "验证期 - 送样/认证中，尚未确认客户",
    Stage.S2: "导入期 - 已进入客户体系，小批量/验证",
    Stage.S3: "放量期 - 批量订单，扩产明确",
    Stage.S4: "加速期 - 业绩拐点，估值修复",
    Stage.S5: "成熟期 - 主流共识，十倍股特征消失"
}


# 状态转换规则：(当前状态, 事件类型) -> (目标状态, 置信度增量)
TRANSITION_RULES = {
    # S0 → S1
    ("S0", "sample_delivery"): ("S1", 0.3),
    ("S0", "certification"): ("S1", 0.2),
    
    # S1 → S2
    ("S1", "sample_delivery"): ("S1", 0.1),  # 多次送样增加置信度
    ("S1", "validation_pass"): ("S2", 0.4),
    ("S1", "certification"): ("S1", 0.15),
    ("S1", "supplier_entry"): ("S2", 0.35),
    
    # S2 → S3
    ("S2", "small_batch"): ("S2", 0.2),
    ("S2", "repeat_order"): ("S3", 0.3),
    ("S2", "expansion"): ("S3", 0.25),
    ("S2", "environmental"): ("S2", 0.15),
    ("S2", "mass_production"): ("S3", 0.4),
    
    # S3 → S4
    ("S3", "mass_production"): ("S3", 0.15),
    ("S3", "expansion"): ("S3", 0.2),
    ("S3", "new_line"): ("S3", 0.2),
    ("S3", "revenue_inflection"): ("S4", 0.35),
    ("S3", "margin_improvement"): ("S4", 0.3),
    
    # S4 → S5
    ("S4", "revenue_inflection"): ("S4", 0.1),
    ("S4", "margin_improvement"): ("S4", 0.1),
}


# 证伪条件
FALSIFICATION_TRIGGERS = [
    "客户验证失败",
    "订单取消",
    "项目终止",
    "核心人员离职",
    "重大诉讼",
    "财务造假"
]


@dataclass
class StageRecord:
    """
    阶段记录
    
    记录股票在某一时刻的阶段状态
    """
    record_id: str
    security_id: str
    
    # 当前状态
    current_stage: str  # Stage
    confidence: float   # 置信度 (0-1)
    
    # 历史
    previous_stage: str = ""
    stage_history: List[Dict] = field(default_factory=list)
    
    # 证据
    supporting_events: List[str] = field(default_factory=list)  # event_ids
    evidence_count: int = 0
    
    # 证伪
    falsified: bool = False
    falsification_reason: str = ""
    
    # 时间
    first_seen: str = ""
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    stage_entered_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StageRecord":
        return cls(**data)


class StageMachine:
    """
    十倍股状态机
    
    管理股票状态的转换和置信度累加
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
            self._collection = self._mongo_db.stages
            
            self._collection.create_index([("security_id", 1)], unique=True)
            self._collection.create_index([("current_stage", 1), ("confidence", DESCENDING)])
            
            logger.info("StageMachine: MongoDB连接成功")
        except Exception as e:
            logger.warning(f"StageMachine: MongoDB连接失败: {e}")
    
    def get_or_create(self, security_id: str) -> StageRecord:
        """获取或创建股票的阶段记录"""
        if self._collection is not None:
            data = self._collection.find_one({"security_id": security_id})
            if data:
                data.pop("_id", None)
                return StageRecord.from_dict(data)
        
        # 创建新记录
        import uuid
        now = datetime.now().isoformat()
        record = StageRecord(
            record_id=f"stg_{uuid.uuid4().hex[:8]}",
            security_id=security_id,
            current_stage="S0",
            confidence=0.0,
            first_seen=now,
            stage_entered_at=now
        )
        self._save(record)
        return record
    
    def process_event(self, security_id: str, event_type: str, event_id: str = "") -> Dict[str, Any]:
        """
        处理事件，更新状态
        
        Returns:
            状态转换结果
        """
        record = self.get_or_create(security_id)
        old_stage = record.current_stage
        old_confidence = record.confidence
        
        # 查找转换规则
        key = (record.current_stage, event_type)
        if key in TRANSITION_RULES:
            target_stage, confidence_delta = TRANSITION_RULES[key]
            
            # 更新置信度
            record.confidence = min(record.confidence + confidence_delta, 1.0)
            
            # 判断是否转换状态（置信度超过阈值）
            stage_threshold = 0.6
            if target_stage != record.current_stage and record.confidence >= stage_threshold:
                # 记录历史
                record.stage_history.append({
                    "from": record.current_stage,
                    "to": target_stage,
                    "confidence": record.confidence,
                    "trigger_event": event_type,
                    "timestamp": datetime.now().isoformat()
                })
                record.previous_stage = record.current_stage
                record.current_stage = target_stage
                record.stage_entered_at = datetime.now().isoformat()
                # 重置置信度（新阶段从0.6开始）
                record.confidence = 0.6
        
        # 记录支持事件
        if event_id and event_id not in record.supporting_events:
            record.supporting_events.append(event_id)
            record.evidence_count = len(record.supporting_events)
        
        record.last_updated = datetime.now().isoformat()
        self._save(record)
        
        return {
            "security_id": security_id,
            "stage_changed": old_stage != record.current_stage,
            "old_stage": old_stage,
            "new_stage": record.current_stage,
            "old_confidence": old_confidence,
            "new_confidence": record.confidence,
            "evidence_count": record.evidence_count
        }
    
    def falsify(self, security_id: str, reason: str) -> bool:
        """证伪股票"""
        record = self.get_or_create(security_id)
        record.falsified = True
        record.falsification_reason = reason
        record.last_updated = datetime.now().isoformat()
        self._save(record)
        logger.warning(f"[Stage] 证伪: {security_id} - {reason}")
        return True
    
    def override_stage(self, security_id: str, new_stage: str, reason: str = "") -> bool:
        """人工覆盖状态"""
        record = self.get_or_create(security_id)
        
        record.stage_history.append({
            "from": record.current_stage,
            "to": new_stage,
            "confidence": record.confidence,
            "trigger_event": "manual_override",
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })
        
        record.previous_stage = record.current_stage
        record.current_stage = new_stage
        record.stage_entered_at = datetime.now().isoformat()
        record.last_updated = datetime.now().isoformat()
        
        self._save(record)
        logger.info(f"[Stage] 人工覆盖: {security_id} -> {new_stage}")
        return True
    
    def get_stage(self, security_id: str) -> Optional[StageRecord]:
        """获取股票阶段"""
        if self._collection is None:
            return None
        
        data = self._collection.find_one({"security_id": security_id})
        if data:
            data.pop("_id", None)
            return StageRecord.from_dict(data)
        return None
    
    def get_history(self, security_id: str) -> List[Dict]:
        """获取状态历史"""
        record = self.get_stage(security_id)
        if record:
            return record.stage_history
        return []
    
    def list_by_stage(self, stage: str, min_confidence: float = 0.0, limit: int = 100) -> List[StageRecord]:
        """按阶段列出股票"""
        if self._collection is None:
            return []
        
        query = {
            "current_stage": stage,
            "confidence": {"$gte": min_confidence},
            "falsified": False
        }
        
        results = []
        for data in self._collection.find(query).sort("confidence", -1).limit(limit):
            data.pop("_id", None)
            results.append(StageRecord.from_dict(data))
        
        return results
    
    def stats(self) -> Dict[str, Any]:
        """统计信息"""
        if self._collection is None:
            return {"error": "MongoDB未连接"}
        
        total = self._collection.count_documents({})
        falsified = self._collection.count_documents({"falsified": True})
        
        by_stage = {}
        for stage in Stage:
            count = self._collection.count_documents({"current_stage": stage.value, "falsified": False})
            if count > 0:
                by_stage[stage.value] = count
        
        return {
            "total": total,
            "active": total - falsified,
            "falsified": falsified,
            "by_stage": by_stage
        }
    
    def _save(self, record: StageRecord):
        """保存记录"""
        if self._collection is not None:
            self._collection.update_one(
                {"security_id": record.security_id},
                {"$set": record.to_dict()},
                upsert=True
            )


# 全局实例
_machine: Optional[StageMachine] = None

def get_stage_machine() -> StageMachine:
    """获取状态机"""
    global _machine
    if _machine is None:
        _machine = StageMachine()
    return _machine
