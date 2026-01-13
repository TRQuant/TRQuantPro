#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus数据收集器
==================
财经新闻和公告数据抓取工具

功能:
1. 财经新闻抓取（东方财富、新浪财经）
2. 公告信息抓取（巨潮资讯）
3. 数据标准化和存储
4. 支持MongoDB存储

使用方式:
    collector = DataCollector()
    news = await collector.fetch_news("eastmoney", limit=5)
    announcements = await collector.fetch_announcements("000001")

作者: TRQuant Team
日期: 2026-01-11
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json
import re
import hashlib

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 项目路径配置
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

# 导入浏览器工具
from openmanus_browser_tool import OpenManusBrowserTool, BrowserResult


@dataclass
class NewsItem:
    """新闻数据项"""
    id: str                          # 唯一ID
    title: str                       # 标题
    source: str                      # 来源
    url: str                         # 链接
    publish_time: Optional[str] = None  # 发布时间
    content: Optional[str] = None    # 内容摘要
    category: Optional[str] = None   # 分类
    tags: List[str] = field(default_factory=list)  # 标签
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())  # 抓取时间
    
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
    id: str                          # 唯一ID
    title: str                       # 标题
    stock_code: str                  # 股票代码
    stock_name: Optional[str] = None # 股票名称
    source: str = ""                 # 来源
    url: str = ""                    # 链接
    publish_time: Optional[str] = None  # 发布时间
    content: Optional[str] = None    # 内容摘要
    type: Optional[str] = None       # 公告类型
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


class DataCollector:
    """
    数据收集器
    
    支持从多个财经网站抓取新闻和公告
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化数据收集器
        
        Args:
            headless: 浏览器是否使用无头模式
        """
        self.headless = headless
        self._browser_tool = None
        self._mongo_client = None
        
        # 新闻源配置
        self.news_sources = {
            "eastmoney": {
                "name": "东方财富",
                "url": "https://finance.eastmoney.com/a/cywjh.html",
                "news_list_url": "https://finance.eastmoney.com/a/cywjh.html",
                "selectors": {
                    "news_list": ".repeatList li",
                    "title": "a",
                    "time": ".time"
                }
            },
            "sina": {
                "name": "新浪财经",
                "url": "https://finance.sina.com.cn/",
                "news_list_url": "https://finance.sina.com.cn/roll/index.d.html?cid=56588",
                "selectors": {
                    "news_list": ".list_009 li",
                    "title": "a",
                    "time": "span"
                }
            },
            "cls": {
                "name": "财联社",
                "url": "https://www.cls.cn/telegraph",
                "news_list_url": "https://www.cls.cn/telegraph",
                "selectors": {
                    "news_list": ".telegraph-list-item",
                    "title": ".telegraph-content",
                    "time": ".telegraph-time"
                }
            }
        }
        
        # 公告源配置
        self.announcement_sources = {
            "cninfo": {
                "name": "巨潮资讯",
                "url": "http://www.cninfo.com.cn/new/disclosure",
                "search_url": "http://www.cninfo.com.cn/new/fulltextSearch?searchkey={code}",
                "selectors": {
                    "list": ".el-table__row",
                    "title": ".title-link",
                    "time": ".date"
                }
            },
            "eastmoney": {
                "name": "东方财富公告",
                "url": "https://data.eastmoney.com/notices/",
                "search_url": "https://data.eastmoney.com/notices/stock/{code}.html",
                "selectors": {
                    "list": ".dataview tbody tr",
                    "title": "a",
                    "time": "td:nth-child(3)"
                }
            }
        }
    
    async def _ensure_browser(self) -> OpenManusBrowserTool:
        """确保浏览器工具已初始化"""
        if self._browser_tool is None:
            self._browser_tool = OpenManusBrowserTool(headless=self.headless)
        return self._browser_tool
    
    async def fetch_news(self, source: str = "eastmoney", limit: int = 10) -> CollectorResult:
        """
        抓取财经新闻
        
        Args:
            source: 新闻源 ("eastmoney", "sina", "cls")
            limit: 限制数量
        
        Returns:
            CollectorResult: 包含新闻列表的结果
        """
        browser = await self._ensure_browser()
        
        source_config = self.news_sources.get(source)
        if not source_config:
            return CollectorResult(
                success=False, 
                error=f"未知的新闻源: {source}",
                source=source
            )
        
        try:
            # 导航到新闻列表页
            url = source_config["news_list_url"]
            nav_result = await browser.navigate(url, wait_for="domcontentloaded")
            
            if not nav_result.success:
                return CollectorResult(
                    success=False,
                    error=f"导航失败: {nav_result.error}",
                    source=source
                )
            
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 获取页面内容
            content_result = await browser.get_page_content()
            
            if not content_result.success:
                return CollectorResult(
                    success=False,
                    error=f"获取内容失败: {content_result.error}",
                    source=source
                )
            
            # 解析新闻（简化版，使用正则提取）
            content = content_result.data.get("content", "")
            news_items = self._parse_news_from_content(content, source, limit)
            
            return CollectorResult(
                success=True,
                data=[item.to_dict() for item in news_items],
                source=source,
                count=len(news_items)
            )
            
        except Exception as e:
            logger.error(f"抓取新闻失败: {source}, 错误: {e}")
            return CollectorResult(
                success=False,
                error=str(e),
                source=source
            )
    
    def _parse_news_from_content(self, content: str, source: str, limit: int) -> List[NewsItem]:
        """
        从页面内容解析新闻
        
        Args:
            content: 页面文本内容
            source: 新闻源
            limit: 限制数量
        
        Returns:
            List[NewsItem]: 新闻列表
        """
        news_items = []
        
        # 简单的新闻标题提取（基于常见模式）
        # 实际生产环境应使用更复杂的解析逻辑
        
        # 尝试提取看起来像新闻标题的文本
        # 通常是20-80个字符，包含关键词
        
        lines = content.split()
        seen_titles = set()
        
        for line in lines:
            line = line.strip()
            # 过滤太短或太长的行
            if len(line) < 10 or len(line) > 100:
                continue
            
            # 过滤明显不是新闻标题的行
            if any(skip in line for skip in ["登录", "注册", "客服", "广告", "版权", "备案"]):
                continue
            
            # 检查是否包含财经相关关键词
            keywords = ["股", "市", "涨", "跌", "基金", "央行", "经济", "投资", "利率", "A股", 
                       "板块", "行情", "交易", "券商", "银行", "收益", "增长", "下跌"]
            
            if any(kw in line for kw in keywords):
                if line not in seen_titles:
                    seen_titles.add(line)
                    news_items.append(NewsItem(
                        id=NewsItem.generate_id(source, line),
                        title=line,
                        source=source,
                        url=self.news_sources[source]["url"],
                        category="财经",
                        tags=[kw for kw in keywords if kw in line]
                    ))
                    
                    if len(news_items) >= limit:
                        break
        
        return news_items
    
    async def fetch_announcements(self, stock_code: str, source: str = "eastmoney", limit: int = 10) -> CollectorResult:
        """
        抓取股票公告
        
        Args:
            stock_code: 股票代码
            source: 公告源 ("cninfo", "eastmoney")
            limit: 限制数量
        
        Returns:
            CollectorResult: 包含公告列表的结果
        """
        browser = await self._ensure_browser()
        
        source_config = self.announcement_sources.get(source)
        if not source_config:
            return CollectorResult(
                success=False,
                error=f"未知的公告源: {source}",
                source=source
            )
        
        try:
            # 构建搜索URL
            url = source_config["search_url"].format(code=stock_code)
            nav_result = await browser.navigate(url, wait_for="domcontentloaded")
            
            if not nav_result.success:
                return CollectorResult(
                    success=False,
                    error=f"导航失败: {nav_result.error}",
                    source=source
                )
            
            await asyncio.sleep(2)
            
            # 获取页面内容
            content_result = await browser.get_page_content()
            
            if not content_result.success:
                return CollectorResult(
                    success=False,
                    error=f"获取内容失败: {content_result.error}",
                    source=source
                )
            
            # 解析公告
            content = content_result.data.get("content", "")
            announcements = self._parse_announcements_from_content(content, stock_code, source, limit)
            
            return CollectorResult(
                success=True,
                data=[item.to_dict() for item in announcements],
                source=source,
                count=len(announcements)
            )
            
        except Exception as e:
            logger.error(f"抓取公告失败: {stock_code}, 错误: {e}")
            return CollectorResult(
                success=False,
                error=str(e),
                source=source
            )
    
    def _parse_announcements_from_content(self, content: str, stock_code: str, source: str, limit: int) -> List[AnnouncementItem]:
        """
        从页面内容解析公告
        
        Args:
            content: 页面文本内容
            stock_code: 股票代码
            source: 公告源
            limit: 限制数量
        
        Returns:
            List[AnnouncementItem]: 公告列表
        """
        announcements = []
        
        # 公告关键词
        announcement_keywords = ["公告", "报告", "年报", "季报", "半年报", "公司章程", "股东大会", 
                                "董事会", "监事会", "关于", "业绩预告", "风险提示"]
        
        lines = content.split()
        seen_titles = set()
        
        for line in lines:
            line = line.strip()
            if len(line) < 5 or len(line) > 150:
                continue
            
            # 检查是否包含公告关键词
            if any(kw in line for kw in announcement_keywords):
                if line not in seen_titles:
                    seen_titles.add(line)
                    
                    # 确定公告类型
                    ann_type = "其他"
                    if "年报" in line or "年度报告" in line:
                        ann_type = "年度报告"
                    elif "季报" in line or "季度报告" in line:
                        ann_type = "季度报告"
                    elif "半年报" in line:
                        ann_type = "半年度报告"
                    elif "业绩" in line:
                        ann_type = "业绩公告"
                    elif "股东" in line:
                        ann_type = "股东相关"
                    
                    announcements.append(AnnouncementItem(
                        id=NewsItem.generate_id(source, line),
                        title=line,
                        stock_code=stock_code,
                        source=source,
                        url=self.announcement_sources[source]["url"],
                        type=ann_type
                    ))
                    
                    if len(announcements) >= limit:
                        break
        
        return announcements
    
    async def fetch_market_news(self, limit: int = 20) -> CollectorResult:
        """
        抓取市场综合新闻（从多个源）
        
        Args:
            limit: 总限制数量
        
        Returns:
            CollectorResult: 包含综合新闻列表的结果
        """
        all_news = []
        errors = []
        
        # 从每个源抓取
        per_source_limit = max(limit // len(self.news_sources), 5)
        
        for source in self.news_sources:
            try:
                result = await self.fetch_news(source, limit=per_source_limit)
                if result.success:
                    all_news.extend(result.data)
                else:
                    errors.append(f"{source}: {result.error}")
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
        
        # 去重（按标题）
        seen = set()
        unique_news = []
        for news in all_news:
            if news["title"] not in seen:
                seen.add(news["title"])
                unique_news.append(news)
        
        return CollectorResult(
            success=len(unique_news) > 0,
            data=unique_news[:limit],
            error="; ".join(errors) if errors else None,
            source="multiple",
            count=len(unique_news[:limit])
        )
    
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
            
            # 批量插入（使用upsert避免重复）
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
        if self._browser_tool:
            await self._browser_tool.cleanup()
            self._browser_tool = None
        
        if self._mongo_client:
            self._mongo_client.close()
            self._mongo_client = None
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.cleanup()


# ==================== 测试函数 ====================

async def test_data_collector():
    """测试数据收集器"""
    print("=" * 80)
    print("OpenManus数据收集器测试")
    print("=" * 80)
    
    async with DataCollector(headless=True) as collector:
        # 测试1: 抓取东方财富新闻
        print("\n测试1: 抓取东方财富新闻")
        result = await collector.fetch_news("eastmoney", limit=5)
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        print(f"  数量: {result.count}")
        if result.success and result.data:
            for i, news in enumerate(result.data[:3], 1):
                print(f"  {i}. {news['title'][:50]}...")
        elif result.error:
            print(f"  错误: {result.error}")
        
        # 测试2: 抓取股票公告
        print("\n测试2: 抓取股票公告 (000001)")
        result = await collector.fetch_announcements("000001", limit=5)
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        print(f"  数量: {result.count}")
        if result.success and result.data:
            for i, ann in enumerate(result.data[:3], 1):
                print(f"  {i}. [{ann.get('type', 'N/A')}] {ann['title'][:40]}...")
        elif result.error:
            print(f"  错误: {result.error}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_data_collector())
