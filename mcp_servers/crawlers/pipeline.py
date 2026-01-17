# -*- coding: utf-8 -*-
"""
端到端数据管道

完整流程: 爬虫 → RawDoc → Event → Stage → Tenbagger评估
"""

import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """管道执行结果"""
    crawled: int = 0
    stored: int = 0
    events: int = 0
    stage_updates: int = 0
    tenbagger_evaluated: int = 0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "crawled": self.crawled,
            "stored": self.stored,
            "events": self.events,
            "stage_updates": self.stage_updates,
            "tenbagger_evaluated": self.tenbagger_evaluated,
            "errors": self.errors,
            "success": self.stored > 0 or self.events > 0,
            "timestamp": datetime.now().isoformat()
        }


class DataPipeline:
    """端到端数据管道"""
    
    def __init__(self):
        self.rawdoc_store = None
        self.stage_machine = None
        self.tenbagger_evaluator = None
        self.event_collection = None
        self._init_components()
    
    def _init_components(self):
        """初始化所有组件"""
        # RawDoc
        try:
            from utils.rawdoc import RawDocStore
            self.rawdoc_store = RawDocStore()
        except Exception as e:
            logger.warning(f"RawDocStore: {e}")
        
        # Stage
        try:
            from utils.stage_machine import StageMachine
            self.stage_machine = StageMachine()
        except Exception as e:
            logger.warning(f"StageMachine: {e}")
        
        # Tenbagger
        try:
            from utils.tenbagger_evaluator import TenbaggerEvaluator
            self.tenbagger_evaluator = TenbaggerEvaluator()
        except Exception as e:
            logger.warning(f"TenbaggerEvaluator: {e}")
        
        # MongoDB
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            db = client.get_database("trquant")
            self.event_collection = db.events
        except Exception as e:
            logger.warning(f"MongoDB: {e}")
    
    def run_full_pipeline(self, source: str = "cninfo", page_size: int = 10) -> PipelineResult:
        """执行完整管道"""
        result = PipelineResult()
        
        # Step 1: 爬取并存储
        logger.info("Step 1: 爬取数据...")
        try:
            from crawlers.crawler_integration import crawl_and_store
            crawl_result = crawl_and_store(source=source, page_size=page_size)
            result.crawled = crawl_result.get('crawled_count', 0)
            result.stored = crawl_result.get('stored_count', 0)
            logger.info(f"  爬取: {result.crawled}, 存储: {result.stored}")
        except Exception as e:
            result.errors.append(f"爬取失败: {e}")
            logger.error(f"Step 1 失败: {e}")
        
        # Step 2: 处理Event
        logger.info("Step 2: 提取Event...")
        try:
            from crawlers.event_processor import process_new_docs
            event_result = process_new_docs(limit=100)
            result.events = event_result.get('extracted_events', 0)
            logger.info(f"  提取事件: {result.events}")
        except Exception as e:
            result.errors.append(f"Event处理失败: {e}")
            logger.error(f"Step 2 失败: {e}")
        
        # Step 3: 更新Stage
        logger.info("Step 3: 更新Stage...")
        result.stage_updates = self._update_stages()
        logger.info(f"  Stage更新: {result.stage_updates}")
        
        # Step 4: Tenbagger评估
        logger.info("Step 4: Tenbagger评估...")
        result.tenbagger_evaluated = self._run_tenbagger_evaluation()
        logger.info(f"  评估股票: {result.tenbagger_evaluated}")
        
        return result
    
    def _update_stages(self) -> int:
        """更新Stage状态"""
        if self.stage_machine is None or self.event_collection is None:
            return 0
        
        count = 0
        try:
            # 获取最近的事件
            recent_events = list(self.event_collection.find().sort('_id', -1).limit(50))
            
            for evt in recent_events:
                try:
                    # 使用正确的接口: process_event(security_id, event_type, event_id)
                    self.stage_machine.process_event(
                        security_id=evt.get('security_id', ''),
                        event_type=evt.get('event_type', 'unknown'),
                        event_id=str(evt.get('_id', ''))
                    )
                    count += 1
                except Exception as e:
                    logger.debug(f"Stage更新跳过: {e}")
        except Exception as e:
            logger.error(f"Stage更新失败: {e}")
        
        return count
    
    def _run_tenbagger_evaluation(self) -> int:
        """运行Tenbagger评估"""
        if self.tenbagger_evaluator is None:
            return 0
        
        count = 0
        try:
            # 获取有事件的股票列表
            if self.event_collection is not None:
                securities = self.event_collection.distinct('security_id')
                
                for sec_id in securities[:20]:  # 限制评估数量
                    try:
                        # 构建评估数据
                        data = self._build_evaluation_data(sec_id)
                        
                        # 执行评估
                        report = self.tenbagger_evaluator.evaluate(
                            security_id=sec_id,
                            name=sec_id,
                            data=data
                        )
                        if report:
                            count += 1
                    except Exception as e:
                        logger.debug(f"评估跳过 {sec_id}: {e}")
        except Exception as e:
            logger.error(f"Tenbagger评估失败: {e}")
        
        return count
    
    def _build_evaluation_data(self, security_id: str) -> Dict[str, Any]:
        """构建评估数据"""
        data = {
            "security_id": security_id,
            "events": [],
            "stage": "S0",
            "financial": {},
            "market": {}
        }
        
        # 获取事件
        if self.event_collection is not None:
            events = list(self.event_collection.find({"security_id": security_id}).limit(10))
            data["events"] = [{"type": e.get("event_type"), "name": e.get("event_name")} for e in events]
        
        # 获取Stage
        if self.stage_machine is not None:
            record = self.stage_machine.get_stage(security_id)
            if record:
                data["stage"] = record.current_stage
        
        return data
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """获取管道状态"""
        status = {
            "components": {
                "rawdoc": self.rawdoc_store is not None,
                "stage_machine": self.stage_machine is not None,
                "tenbagger": self.tenbagger_evaluator is not None,
                "mongodb": self.event_collection is not None
            },
            "counts": {}
        }
        
        # 统计数据
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017)
            db = client.get_database("trquant")
            
            status["counts"] = {
                "raw_docs": db.raw_docs.count_documents({}),
                "events": db.events.count_documents({}),
                "stages": db.stages.count_documents({}) if "stages" in db.list_collection_names() else 0,
            }
        except:
            pass
        
        return status


# 单例
_pipeline = None

def get_pipeline() -> DataPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = DataPipeline()
    return _pipeline

def run_pipeline(source: str = "cninfo", page_size: int = 10) -> Dict[str, Any]:
    """运行完整管道"""
    return get_pipeline().run_full_pipeline(source=source, page_size=page_size).to_dict()

def pipeline_status() -> Dict[str, Any]:
    """获取管道状态"""
    return get_pipeline().get_pipeline_status()
