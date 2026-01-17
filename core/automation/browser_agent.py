# -*- coding: utf-8 -*-
"""
浏览器自动化Agent
================
提供浏览器自动化功能，支持网页访问、数据提取等操作

基于Playwright实现，可选集成OpenManus的BrowserUseTool

使用方式:
    from core.automation import BrowserAgent
    
    async with BrowserAgent() as agent:
        result = await agent.navigate("https://www.eastmoney.com")
        content = await agent.get_content()
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging
import re

# 配置日志
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class BrowserResult:
    """浏览器操作结果"""
    success: bool
    data: Any = None
    error: Optional[str] = None
    url: Optional[str] = None
    title: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "url": self.url,
            "title": self.title
        }


class BrowserAgent:
    """
    浏览器自动化Agent
    
    提供统一的浏览器操作API，支持：
    - 网页导航
    - 元素点击和输入
    - 内容提取
    - 截图
    
    Attributes:
        headless: 是否使用无头模式
    """
    
    # 财经网站配置
    FINANCE_SITES = {
        "eastmoney": {
            "name": "东方财富",
            "url": "https://www.eastmoney.com",
            "stock_url": "https://quote.eastmoney.com/{market}{code}.html",
            "selectors": {
                "stock_price": ".price",
                "stock_change": ".change"
            }
        },
        "sina": {
            "name": "新浪财经",
            "url": "https://finance.sina.com.cn",
            "stock_url": "https://finance.sina.com.cn/realstock/company/{market}{code}/nc.shtml"
        },
        "tonghuashun": {
            "name": "同花顺",
            "url": "https://www.10jqka.com.cn"
        }
    }
    
    def __init__(self, headless: bool = True, timeout: int = 30000):
        """
        初始化浏览器Agent
        
        Args:
            headless: 是否使用无头模式（默认True）
            timeout: 默认超时时间（毫秒）
        """
        self.headless = headless
        self.timeout = timeout
        self._browser = None
        self._page = None
        self._playwright = None
    
    async def _ensure_browser(self):
        """确保浏览器已初始化"""
        if self._browser is not None:
            return
        
        try:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless
            )
            self._page = await self._browser.new_page()
            self._page.set_default_timeout(self.timeout)
            logger.info("✅ 浏览器初始化成功")
        except ImportError:
            raise RuntimeError(
                "Playwright未安装，请运行: pip install playwright && playwright install"
            )
    
    async def navigate(self, url: str, wait_for: str = "load") -> BrowserResult:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
            wait_for: 等待状态 ("load", "domcontentloaded", "networkidle")
        
        Returns:
            BrowserResult: 操作结果
        """
        await self._ensure_browser()
        
        try:
            await self._page.goto(url, wait_until=wait_for)
            title = await self._page.title()
            return BrowserResult(
                success=True,
                data={"title": title},
                url=url,
                title=title
            )
        except Exception as e:
            logger.error(f"导航失败: {url}, 错误: {e}")
            return BrowserResult(success=False, error=str(e), url=url)
    
    async def click(self, selector: str) -> BrowserResult:
        """
        点击元素
        
        Args:
            selector: CSS选择器
        
        Returns:
            BrowserResult: 操作结果
        """
        await self._ensure_browser()
        
        try:
            await self._page.click(selector)
            return BrowserResult(success=True, data={"clicked": selector})
        except Exception as e:
            logger.error(f"点击失败: {selector}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def type_text(self, selector: str, text: str, submit: bool = False) -> BrowserResult:
        """
        输入文本
        
        Args:
            selector: CSS选择器
            text: 要输入的文本
            submit: 是否提交（按回车）
        
        Returns:
            BrowserResult: 操作结果
        """
        await self._ensure_browser()
        
        try:
            await self._page.fill(selector, text)
            if submit:
                await self._page.press(selector, "Enter")
            return BrowserResult(success=True, data={"typed": text})
        except Exception as e:
            logger.error(f"输入失败: {selector}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def get_text(self, selector: str) -> BrowserResult:
        """
        获取元素文本
        
        Args:
            selector: CSS选择器
        
        Returns:
            BrowserResult: 包含文本的操作结果
        """
        await self._ensure_browser()
        
        try:
            element = await self._page.query_selector(selector)
            if element:
                text = await element.text_content()
                return BrowserResult(success=True, data={"text": text.strip() if text else ""})
            return BrowserResult(success=False, error=f"元素未找到: {selector}")
        except Exception as e:
            logger.error(f"获取文本失败: {selector}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def get_content(self) -> BrowserResult:
        """
        获取当前页面的文本内容
        
        Returns:
            BrowserResult: 包含页面内容的操作结果
        """
        await self._ensure_browser()
        
        try:
            content = await self._page.content()
            
            # 简单提取文本
            from html.parser import HTMLParser
            
            class TextExtractor(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.text = []
                    self._skip_tags = {'script', 'style', 'noscript'}
                    self._skip = False
                
                def handle_starttag(self, tag, attrs):
                    if tag.lower() in self._skip_tags:
                        self._skip = True
                
                def handle_endtag(self, tag):
                    if tag.lower() in self._skip_tags:
                        self._skip = False
                
                def handle_data(self, data):
                    if not self._skip:
                        self.text.append(data.strip())
            
            extractor = TextExtractor()
            extractor.feed(content)
            text = ' '.join(filter(None, extractor.text))
            
            return BrowserResult(success=True, data={"content": text[:10000]})
        except Exception as e:
            logger.error(f"获取页面内容失败: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def screenshot(self, path: str = None, full_page: bool = False) -> BrowserResult:
        """
        截取页面截图
        
        Args:
            path: 保存路径（可选）
            full_page: 是否截取完整页面
        
        Returns:
            BrowserResult: 包含截图路径的操作结果
        """
        await self._ensure_browser()
        
        try:
            if path is None:
                from datetime import datetime
                path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            await self._page.screenshot(path=path, full_page=full_page)
            return BrowserResult(success=True, data={"path": path})
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def get_stock_price(self, code: str, source: str = "eastmoney") -> BrowserResult:
        """
        获取股票价格
        
        Args:
            code: 股票代码
            source: 数据源
        
        Returns:
            BrowserResult: 包含价格信息的操作结果
        """
        await self._ensure_browser()
        
        market = "sh" if code.startswith("6") else "sz"
        site = self.FINANCE_SITES.get(source, self.FINANCE_SITES["eastmoney"])
        url = site.get("stock_url", "").format(market=market, code=code)
        
        if not url:
            return BrowserResult(success=False, error=f"不支持的数据源: {source}")
        
        try:
            nav_result = await self.navigate(url)
            if not nav_result.success:
                return nav_result
            
            await asyncio.sleep(1)
            
            # 尝试提取价格
            price_data = {"code": code, "market": market, "source": source}
            
            selectors = site.get("selectors", {})
            if "stock_price" in selectors:
                price_result = await self.get_text(selectors["stock_price"])
                if price_result.success:
                    price_data["price"] = price_result.data.get("text")
            
            if "stock_change" in selectors:
                change_result = await self.get_text(selectors["stock_change"])
                if change_result.success:
                    price_data["change"] = change_result.data.get("text")
            
            return BrowserResult(success=True, data=price_data, url=url)
        except Exception as e:
            logger.error(f"获取股票价格失败: {code}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def cleanup(self):
        """清理资源"""
        try:
            if self._page:
                await self._page.close()
                self._page = None
            
            if self._browser:
                await self._browser.close()
                self._browser = None
            
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None
            
            logger.info("✅ 浏览器资源已清理")
        except Exception as e:
            logger.warning(f"清理资源时出错: {e}")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self._ensure_browser()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.cleanup()
