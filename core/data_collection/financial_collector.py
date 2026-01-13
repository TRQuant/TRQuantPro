# -*- coding: utf-8 -*-
"""
财经数据收集器（Core模块版本）
============================
从财经网站收集新闻、公告等数据

支持:
- 东方财富、新浪财经、财联社新闻
- 巨潮资讯、东方财富公告
- MongoDB存储
- 增量更新

使用方式:
    from core.data_collection import FinancialCollector
    
    async with FinancialCollector() as collector:
        news = await collector.fetch_news("eastmoney", limit=10)
        announcements = await collector.fetch_announcements("000001")
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging
import hashlib

# 配置日志
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 导入浏览器Agent
from core.automation.browser_agent import BrowserAgent


@dataclass
class NewsItem:
    """新闻数据项"""
    id: str
    title: str
    source: str
    url: str
    publish_time: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "url": self.url,
            "publish_time": self.publish_time,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "fetched_at": self.fetched_at
        }
    
    @staticmethod
    def generate_id(url: str, title: str) -> str:
        """生成唯一ID"""
        return hashlib.md5(f"{url}:{title}".encode()).hexdigest()[:16]


@dataclass
class AnnouncementItem:
    """公告数据项"""
    id: str
    title: str
    stock_code: str
    stock_name: Optional[str] = None
    source: str = ""
    url: str = ""
    publish_time: Optional[str] = None
    content: Optional[str] = None
    type: Optional[str] = None
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "source": self.source,
            "url": self.url,
            "publish_time": self.publish_time,
            "content": self.content,
            "type": self.type,
            "fetched_at": self.fetched_at
        }


@dataclass
class CollectorResult:
    """收集器结果"""
    success: bool
    data: List[Dict] = field(default_factory=list)
    error: Optional[str] = None
    source: str = ""
    count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "source": self.source,
            "count": self.count
        }


class FinancialCollector:
    """
    财经数据收集器
    
    从多个财经网站收集新闻和公告
    
    Attributes:
        headless: 浏览器是否使用无头模式
    """
    
    # 新闻源配置
    NEWS_SOURCES = {
        "eastmoney": {
            "name": "东方财富",
            "url": "https://finance.eastmoney.com/a/cywjh.html"
        },
        "sina": {
            "name": "新浪财经",
            "url": "https://finance.sina.com.cn/"
        },
        "cls": {
            "name": "财联社",
            "url": "https://www.cls.cn/telegraph"
        }
    }
    
    # 公告源配置
    ANNOUNCEMENT_SOURCES = {
        "eastmoney": {
            "name": "东方财富公告",
            "url": "https://data.eastmoney.com/notices/stock/{code}.html"
        },
        "cninfo": {
            "name": "巨潮资讯",
            "url": "http://www.cninfo.com.cn/new/disclosure"
        }
    }
    
    # 新闻关键词
    NEWS_KEYWORDS = ["股", "市", "涨", "跌", "基金", "央行", "经济", "投资", 
                    "利率", "A股", "板块", "行情", "交易", "券商", "银行"]
    
    # 公告关键词
    ANNOUNCEMENT_KEYWORDS = ["公告", "报告", "年报", "季报", "半年报", "章程", 
                            "股东大会", "董事会", "监事会", "业绩预告"]
    
    def __init__(self, headless: bool = True):
        """
        初始化收集器
        
        Args:
            headless: 浏览器是否使用无头模式
        """
        self.headless = headless
        self._browser: Optional[BrowserAgent] = None
        self._mongo_client = None
    
    async def _ensure_browser(self) -> BrowserAgent:
        """确保浏览器已初始化"""
        if self._browser is None:
            self._browser = BrowserAgent(headless=self.headless)
        return self._browser
    
    async def fetch_news(self, source: str = "eastmoney", limit: int = 10) -> CollectorResult:
        """
        抓取财经新闻
        
        Args:
            source: 新闻源
            limit: 限制数量
        
        Returns:
            CollectorResult: 包含新闻列表的结果
        """
        source_config = self.NEWS_SOURCES.get(source)
        if not source_config:
            return CollectorResult(
                success=False,
                error=f"未知的新闻源: {source}",
                source=source
            )
        
        browser = await self._ensure_browser()
        
        try:
            url = source_config["url"]
            nav_result = await browser.navigate(url, wait_for="domcontentloaded")
            
            if not nav_result.success:
                return CollectorResult(
                    success=False,
                    error=f"导航失败: {nav_result.error}",
                    source=source
                )
            
            await asyncio.sleep(2)
            
            content_result = await browser.get_content()
            if not content_result.success:
                return CollectorResult(
                    success=False,
                    error=f"获取内容失败: {content_result.error}",
                    source=source
                )
            
            content = content_result.data.get("content", "")
            news_items = self._parse_news(content, source, limit)
            
            return CollectorResult(
                success=True,
                data=[item.to_dict() for item in news_items],
                source=source,
                count=len(news_items)
            )
            
        except Exception as e:
            logger.error(f"抓取新闻失败: {source}, 错误: {e}")
            return CollectorResult(success=False, error=str(e), source=source)
    
    def _parse_news(self, content: str, source: str, limit: int) -> List[NewsItem]:
        """解析新闻内容"""
        news_items = []
        seen_titles = set()
        
        lines = content.split()
        for line in lines:
            line = line.strip()
            if len(line) < 10 or len(line) > 100:
                continue
            
            if any(skip in line for skip in ["登录", "注册", "客服", "广告", "版权"]):
                continue
            
            if any(kw in line for kw in self.NEWS_KEYWORDS):
                if line not in seen_titles:
                    seen_titles.add(line)
                    news_items.append(NewsItem(
                        id=NewsItem.generate_id(source, line),
                        title=line,
                        source=source,
                        url=self.NEWS_SOURCES[source]["url"],
                        category="财经",
                        tags=[kw for kw in self.NEWS_KEYWORDS if kw in line]
                    ))
                    
                    if len(news_items) >= limit:
                        break
        
        return news_items
    
    async def fetch_announcements(self, stock_code: str, source: str = "eastmoney", 
                                  limit: int = 10) -> CollectorResult:
        """
        抓取股票公告
        
        Args:
            stock_code: 股票代码
            source: 公告源
            limit: 限制数量
        
        Returns:
            CollectorResult: 包含公告列表的结果
        """
        source_config = self.ANNOUNCEMENT_SOURCES.get(source)
        if not source_config:
            return CollectorResult(
                success=False,
                error=f"未知的公告源: {source}",
                source=source
            )
        
        browser = await self._ensure_browser()
        
        try:
            url = source_config["url"].format(code=stock_code)
            nav_result = await browser.navigate(url, wait_for="domcontentloaded")
            
            if not nav_result.success:
                return CollectorResult(
                    success=False,
                    error=f"导航失败: {nav_result.error}",
                    source=source
                )
            
            await asyncio.sleep(2)
            
            content_result = await browser.get_content()
            if not content_result.success:
                return CollectorResult(
                    success=False,
                    error=f"获取内容失败: {content_result.error}",
                    source=source
                )
            
            content = content_result.data.get("content", "")
            announcements = self._parse_announcements(content, stock_code, source, limit)
            
            return CollectorResult(
                success=True,
                data=[item.to_dict() for item in announcements],
                source=source,
                count=len(announcements)
            )
            
        except Exception as e:
            logger.error(f"抓取公告失败: {stock_code}, 错误: {e}")
            return CollectorResult(success=False, error=str(e), source=source)
    
    def _parse_announcements(self, content: str, stock_code: str, 
                            source: str, limit: int) -> List[AnnouncementItem]:
        """解析公告内容"""
        announcements = []
        seen_titles = set()
        
        lines = content.split()
        for line in lines:
            line = line.strip()
            if len(line) < 5 or len(line) > 150:
                continue
            
            if any(kw in line for kw in self.ANNOUNCEMENT_KEYWORDS):
                if line not in seen_titles:
                    seen_titles.add(line)
                    
                    ann_type = "其他"
                    if "年报" in line:
                        ann_type = "年度报告"
                    elif "季报" in line:
                        ann_type = "季度报告"
                    elif "半年报" in line:
                        ann_type = "半年度报告"
                    elif "业绩" in line:
                        ann_type = "业绩公告"
                    
                    announcements.append(AnnouncementItem(
                        id=NewsItem.generate_id(source, line),
                        title=line,
                        stock_code=stock_code,
                        source=source,
                        url=self.ANNOUNCEMENT_SOURCES[source]["url"].format(code=stock_code),
                        type=ann_type
                    ))
                    
                    if len(announcements) >= limit:
                        break
        
        return announcements
    
    async def save_to_mongodb(self, collection_name: str, data: List[Dict]) -> bool:
        """
        保存数据到MongoDB
        
        Args:
            collection_name: 集合名称
            data: 数据列表
        
        Returns:
            bool: 是否成功
        """
        try:
            from pymongo import MongoClient
            
            if self._mongo_client is None:
                self._mongo_client = MongoClient("mongodb://localhost:27017/")
            
            db = self._mongo_client["trquant"]
            collection = db[collection_name]
            
            for item in data:
                collection.update_one(
                    {"id": item["id"]},
                    {"$set": item},
                    upsert=True
                )
            
            logger.info(f"保存 {len(data)} 条数据到 {collection_name}")
            return True
            
        except Exception as e:
            logger.error(f"保存到MongoDB失败: {e}")
            return False
    
    async def cleanup(self):
        """清理资源"""
        if self._browser:
            await self._browser.cleanup()
            self._browser = None
        
        if self._mongo_client:
            self._mongo_client.close()
            self._mongo_client = None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
