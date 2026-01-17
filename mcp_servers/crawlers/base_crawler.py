# -*- coding: utf-8 -*-
"""TRQuant 爬虫基类"""

import asyncio
import random
import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class CrawlerStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class CrawlResult:
    url: str
    success: bool
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    crawl_time: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        return {
            "url": self.url, "success": self.success,
            "content_length": len(self.content) if self.content else 0,
            "error": self.error
        }

@dataclass
class CrawlTask:
    task_id: str
    url: str
    params: Dict[str, Any] = field(default_factory=dict)

class BaseCrawler(ABC):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, name: str, base_url: str, delay_range: tuple = (1.0, 3.0), timeout: int = 30):
        self.name = name
        self.base_url = base_url
        self.delay_range = delay_range
        self.timeout = timeout
        self.status = CrawlerStatus.IDLE
        self.results: List[CrawlResult] = []
        self.stats = {"total_requests": 0, "success_count": 0, "error_count": 0}
        self._session = None
    
    def get_random_ua(self) -> str:
        return random.choice(self.USER_AGENTS)
    
    def get_headers(self, referer: str = None) -> Dict[str, str]:
        headers = {
            "User-Agent": self.get_random_ua(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        if referer:
            headers["Referer"] = referer
        return headers
    
    async def delay(self):
        await asyncio.sleep(random.uniform(*self.delay_range))
    
    def fetch_sync(self, url: str, params: Dict = None) -> CrawlResult:
        try:
            import requests
        except ImportError:
            return CrawlResult(url=url, success=False, error="requests库未安装")
        
        self.stats["total_requests"] += 1
        try:
            if self._session is None:
                self._session = requests.Session()
            response = self._session.get(url, params=params, headers=self.get_headers(self.base_url), timeout=self.timeout)
            response.raise_for_status()
            self.stats["success_count"] += 1
            return CrawlResult(url=url, success=True, content=response.text)
        except Exception as e:
            self.stats["error_count"] += 1
            return CrawlResult(url=url, success=False, error=str(e))
    
    def post_sync(self, url: str, data: Dict = None, json_data: Dict = None) -> CrawlResult:
        try:
            import requests
        except ImportError:
            return CrawlResult(url=url, success=False, error="requests库未安装")
        
        self.stats["total_requests"] += 1
        try:
            if self._session is None:
                self._session = requests.Session()
            response = self._session.post(url, data=data, json=json_data, headers=self.get_headers(self.base_url), timeout=self.timeout)
            response.raise_for_status()
            self.stats["success_count"] += 1
            return CrawlResult(url=url, success=True, content=response.text)
        except Exception as e:
            self.stats["error_count"] += 1
            return CrawlResult(url=url, success=False, error=str(e))
    
    @abstractmethod
    def parse_content(self, content: str) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def build_url(self, **kwargs) -> str:
        pass
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            "crawler_name": self.name, "status": self.status.value,
            "total_requests": self.stats["total_requests"],
            "success_count": self.stats["success_count"],
            "error_count": self.stats["error_count"],
            "success_rate": self.stats["success_count"] / max(self.stats["total_requests"], 1)
        }

_crawlers: Dict[str, BaseCrawler] = {}

def register_crawler(name: str, crawler: BaseCrawler):
    _crawlers[name] = crawler

def get_crawler(name: str) -> Optional[BaseCrawler]:
    return _crawlers.get(name)

def list_crawlers() -> List[str]:
    return list(_crawlers.keys())
