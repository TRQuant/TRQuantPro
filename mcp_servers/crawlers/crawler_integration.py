# -*- coding: utf-8 -*-
"""
爬虫集成模块 - 将爬虫数据与核心系统集成

数据流：爬虫 → RawDoc(MongoDB) → Event提取 → Stage更新
"""

import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class IntegrationResult:
    """集成结果"""
    success: bool
    crawled_count: int = 0
    stored_count: int = 0
    events_count: int = 0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "crawled_count": self.crawled_count,
            "stored_count": self.stored_count,
            "events_count": self.events_count,
            "errors": self.errors,
            "timestamp": datetime.now().isoformat()
        }


class CrawlerIntegration:
    """爬虫集成服务"""
    
    def __init__(self):
        self.rawdoc_store = None
        self.event_extractor = None
        self._init_components()
    
    def _init_components(self):
        """初始化组件"""
        try:
            from utils.rawdoc import RawDocStore
            self.rawdoc_store = RawDocStore()
            logger.info("RawDocStore初始化成功")
        except Exception as e:
            logger.warning(f"RawDocStore初始化失败: {e}")
        
        try:
            from utils.event_extractor import EventExtractor
            self.event_extractor = EventExtractor()
            logger.info("EventExtractor初始化成功")
        except Exception as e:
            logger.warning(f"EventExtractor初始化失败: {e}")
    
    def process_announcements(self, announcements: List[Dict]) -> IntegrationResult:
        """处理公告数据 - 存储到MongoDB"""
        errors = []
        stored_count = 0
        events_count = 0
        
        for ann in announcements:
            try:
                if self.rawdoc_store is not None:
                    from utils.rawdoc import RawDoc
                    
                    # 生成唯一doc_id
                    doc_id = f"doc_{ann.get('security_id', 'unknown')}_{uuid.uuid4().hex[:8]}"
                    
                    # 创建RawDoc对象（使用正确的参数）
                    doc = RawDoc(
                        doc_id=doc_id,
                        doc_type=ann.get('doc_type', 'announcement'),
                        source=ann.get('metadata', {}).get('source', 'crawler'),
                        security_id=ann.get('security_id', 'unknown'),
                        title=ann.get('title', ''),
                        content=ann.get('content', '') or ann.get('title', ''),
                        url=ann.get('download_url', '') or ann.get('url', ''),
                        publish_time=ann.get('publish_date', '')
                    )
                    
                    # 使用ingest方法存储到MongoDB
                    result = self.rawdoc_store.ingest(doc)
                    if result.get('success') or result.get('doc_id'):
                        stored_count += 1
                        logger.info(f"存储成功: {ann.get('security_id')} - {ann.get('title', '')[:30]}")
                    else:
                        if 'duplicate' not in str(result.get('error', '')).lower():
                            errors.append(f"{ann.get('security_id')}: {result.get('error', '存储失败')}")
                        
            except Exception as e:
                errors.append(f"{ann.get('security_id', 'N/A')}: {str(e)}")
                logger.error(f"处理公告失败: {e}")
        
        return IntegrationResult(
            success=stored_count > 0,
            crawled_count=len(announcements),
            stored_count=stored_count,
            events_count=events_count,
            errors=errors
        )
    
    def run_full_pipeline(self, source: str = "cninfo", **kwargs) -> IntegrationResult:
        """运行完整的数据管道"""
        errors = []
        announcements = []
        
        try:
            if source == "cninfo":
                from crawlers.cninfo_crawler import get_cninfo_crawler
                crawler = get_cninfo_crawler()
                announcements = crawler.fetch_announcements(**kwargs)
            elif source == "eastmoney":
                from crawlers.eastmoney_crawler import get_eastmoney_crawler
                crawler = get_eastmoney_crawler()
                announcements = crawler.get_stock_announcements(**kwargs)
            elif source == "bid":
                from crawlers.bid_crawler import get_bid_crawler
                crawler = get_bid_crawler()
                announcements = crawler.fetch_bids(**kwargs)
            else:
                errors.append(f"未知数据源: {source}")
        except Exception as e:
            errors.append(f"爬取失败: {e}")
            return IntegrationResult(success=False, errors=errors)
        
        logger.info(f"爬取到 {len(announcements)} 条数据")
        result = self.process_announcements(announcements)
        result.errors.extend(errors)
        return result
    
    def get_status(self) -> Dict[str, Any]:
        """获取集成状态"""
        doc_count = 0
        if self.rawdoc_store is not None and self.rawdoc_store._collection is not None:
            try:
                doc_count = self.rawdoc_store._collection.count_documents({})
            except:
                pass
        
        return {
            "rawdoc_available": self.rawdoc_store is not None,
            "event_extractor_available": self.event_extractor is not None,
            "mongodb_doc_count": doc_count,
            "timestamp": datetime.now().isoformat()
        }


_integration = None

def get_crawler_integration() -> CrawlerIntegration:
    global _integration
    if _integration is None:
        _integration = CrawlerIntegration()
    return _integration

def crawl_and_store(source: str = "cninfo", **kwargs) -> Dict[str, Any]:
    """爬取并存储数据到MongoDB"""
    return get_crawler_integration().run_full_pipeline(source=source, **kwargs).to_dict()

def get_integration_status() -> Dict[str, Any]:
    """获取集成状态"""
    return get_crawler_integration().get_status()
