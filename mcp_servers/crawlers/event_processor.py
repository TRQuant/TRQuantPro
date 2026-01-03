# -*- coding: utf-8 -*-
"""
Event自动处理模块

从RawDoc自动提取Event并更新Stage状态机
数据流: RawDoc(MongoDB) → EventExtractor → Event(MongoDB) → StageMachine
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ProcessResult:
    """处理结果"""
    processed_docs: int = 0
    extracted_events: int = 0
    stage_updates: int = 0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "processed_docs": self.processed_docs,
            "extracted_events": self.extracted_events,
            "stage_updates": self.stage_updates,
            "errors": self.errors,
            "success": len(self.errors) == 0,
            "timestamp": datetime.now().isoformat()
        }


class EventProcessor:
    """Event自动处理服务"""
    
    def __init__(self):
        self.rawdoc_store = None
        self.event_extractor = None
        self.stage_machine = None
        self.event_collection = None
        self._init_components()
    
    def _init_components(self):
        """初始化组件"""
        # RawDoc存储
        try:
            from utils.rawdoc import RawDocStore
            self.rawdoc_store = RawDocStore()
            logger.info("RawDocStore初始化成功")
        except Exception as e:
            logger.warning(f"RawDocStore初始化失败: {e}")
        
        # Event提取器
        try:
            from utils.event_extractor import EventExtractor
            self.event_extractor = EventExtractor()
            logger.info("EventExtractor初始化成功")
        except Exception as e:
            logger.warning(f"EventExtractor初始化失败: {e}")
        
        # Stage状态机
        try:
            from utils.stage_machine import StageMachine
            self.stage_machine = StageMachine()
            logger.info("StageMachine初始化成功")
        except Exception as e:
            logger.warning(f"StageMachine初始化失败: {e}")
        
        # Event存储集合
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            db = client.get_database("trquant")
            self.event_collection = db.events
            logger.info("Event集合初始化成功")
        except Exception as e:
            logger.warning(f"Event集合初始化失败: {e}")
    
    def process_unprocessed_docs(self, limit: int = 100) -> ProcessResult:
        """处理未处理的RawDoc"""
        result = ProcessResult()
        
        if self.rawdoc_store is None:
            result.errors.append("RawDocStore未初始化")
            return result
        
        # 1. 获取未处理的文档
        try:
            unprocessed = self.rawdoc_store.get_unprocessed(limit=limit)
            logger.info(f"获取到 {len(unprocessed)} 个未处理文档")
        except Exception as e:
            result.errors.append(f"获取未处理文档失败: {e}")
            return result
        
        # 2. 逐个处理
        for doc in unprocessed:
            try:
                events = self._process_single_doc(doc)
                result.processed_docs += 1
                result.extracted_events += len(events)
                
                # 标记文档已处理
                self.rawdoc_store.mark_processed(doc.doc_id, event_count=len(events))
                
            except Exception as e:
                result.errors.append(f"{doc.doc_id}: {str(e)}")
                logger.error(f"处理文档失败: {doc.doc_id} - {e}")
        
        return result
    
    def _process_single_doc(self, doc) -> List[Dict]:
        """处理单个文档"""
        events = []
        
        # 1. 提取Event
        if self.event_extractor is not None:
            try:
                extracted = self.event_extractor.extract_events(doc)
                if extracted:
                    events.extend(extracted)
            except Exception as e:
                logger.warning(f"Event提取失败: {e}")
        
        # 2. 如果没有提取器，使用规则匹配
        if not events:
            events = self._rule_based_extraction(doc)
        
        # 3. 存储Event到MongoDB
        for event in events:
            self._store_event(event, doc)
        
        # 4. 更新Stage状态机
        if self.stage_machine is not None and events:
            for event in events:
                try:
                    self.stage_machine.process_event(
                        security_id=doc.security_id,
                        event_type=event.get('event_type', 'unknown'),
                        event_data=event
                    )
                except Exception as e:
                    logger.warning(f"Stage更新失败: {e}")
        
        return events
    
    def _rule_based_extraction(self, doc) -> List[Dict]:
        """基于规则的事件提取"""
        events = []
        title = doc.title.lower() if doc.title else ""
        content = doc.content.lower() if doc.content else ""
        text = title + " " + content
        
        # 业绩相关
        if any(kw in text for kw in ['业绩预增', '净利润增长', '业绩快报', '盈利']):
            events.append({
                'event_type': 'performance_growth',
                'event_name': '业绩增长',
                'confidence': 0.8,
                'keywords': ['业绩预增', '净利润增长']
            })
        
        # 股权相关
        if any(kw in text for kw in ['增持', '回购', '股权激励']):
            events.append({
                'event_type': 'equity_action',
                'event_name': '股权动作',
                'confidence': 0.7,
                'keywords': ['增持', '回购', '股权激励']
            })
        
        # 融资相关
        if any(kw in text for kw in ['定增', '发行股票', '募集资金', '可转债']):
            events.append({
                'event_type': 'financing',
                'event_name': '融资事件',
                'confidence': 0.75,
                'keywords': ['定增', '发行股票', '募集资金']
            })
        
        # 重大合同
        if any(kw in text for kw in ['中标', '签订合同', '重大订单', '战略合作']):
            events.append({
                'event_type': 'major_contract',
                'event_name': '重大合同',
                'confidence': 0.8,
                'keywords': ['中标', '签订合同', '重大订单']
            })
        
        # 资产重组
        if any(kw in text for kw in ['重组', '并购', '收购', '资产注入']):
            events.append({
                'event_type': 'restructuring',
                'event_name': '资产重组',
                'confidence': 0.7,
                'keywords': ['重组', '并购', '收购']
            })
        
        # 高管变动
        if any(kw in text for kw in ['董事长', '总经理', '高管', '换届', '离任']):
            events.append({
                'event_type': 'management_change',
                'event_name': '高管变动',
                'confidence': 0.6,
                'keywords': ['董事长', '总经理', '高管']
            })
        
        return events
    
    def _store_event(self, event: Dict, doc) -> bool:
        """存储Event到MongoDB"""
        if self.event_collection is None:
            return False
        
        try:
            event_doc = {
                "security_id": doc.security_id,
                "event_type": event.get('event_type', 'unknown'),
                "event_name": event.get('event_name', ''),
                "confidence": event.get('confidence', 0.5),
                "keywords": event.get('keywords', []),
                "source_doc_id": doc.doc_id,
                "source_title": doc.title,
                "created_at": datetime.now().isoformat()
            }
            self.event_collection.insert_one(event_doc)
            return True
        except Exception as e:
            logger.error(f"Event存储失败: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取处理状态"""
        unprocessed_count = 0
        event_count = 0
        
        if self.rawdoc_store is not None:
            try:
                unprocessed = self.rawdoc_store.get_unprocessed(limit=1000)
                unprocessed_count = len(unprocessed)
            except:
                pass
        
        if self.event_collection is not None:
            try:
                event_count = self.event_collection.count_documents({})
            except:
                pass
        
        return {
            "rawdoc_available": self.rawdoc_store is not None,
            "event_extractor_available": self.event_extractor is not None,
            "stage_machine_available": self.stage_machine is not None,
            "unprocessed_docs": unprocessed_count,
            "total_events": event_count,
            "timestamp": datetime.now().isoformat()
        }


# 单例
_processor = None

def get_event_processor() -> EventProcessor:
    """获取Event处理器实例"""
    global _processor
    if _processor is None:
        _processor = EventProcessor()
    return _processor


def process_new_docs(limit: int = 100) -> Dict[str, Any]:
    """处理新文档"""
    return get_event_processor().process_unprocessed_docs(limit=limit).to_dict()


def get_processor_status() -> Dict[str, Any]:
    """获取处理器状态"""
    return get_event_processor().get_status()
