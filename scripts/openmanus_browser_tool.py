#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus浏览器工具封装
======================
封装Playwright浏览器操作，支持财经网站数据抓取

功能:
1. 网页导航和交互
2. 智能元素识别
3. 财经网站适配（东方财富、同花顺）
4. 股票价格提取

使用方式:
    tool = OpenManusBrowserTool()
    result = await tool.navigate("https://www.eastmoney.com")
    price = await tool.extract_stock_price("000001")

作者: TRQuant Team
日期: 2026-01-11
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import logging
import re

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 项目路径配置
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"

# 检查OpenManus是否可用
OPENMANUS_AVAILABLE = OPENMANUS_DIR.exists() and (OPENMANUS_DIR / ".venv").exists()

if OPENMANUS_AVAILABLE:
    sys.path.insert(0, str(OPENMANUS_DIR))


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


class OpenManusBrowserTool:
    """
    OpenManus浏览器工具
    
    封装Playwright和OpenManus的浏览器功能，提供统一的API接口
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化浏览器工具
        
        Args:
            headless: 是否使用无头模式（默认True）
        """
        self.headless = headless
        self._browser = None
        self._page = None
        self._openmanus_browser = None
        
        # 财经网站配置
        self.finance_sites = {
            "eastmoney": {
                "name": "东方财富",
                "url": "https://www.eastmoney.com",
                "search_url": "https://so.eastmoney.com/web/s?keyword={query}",
                "stock_url": "https://quote.eastmoney.com/{market}{code}.html",
                "selectors": {
                    "search_input": "input[name='keyword']",
                    "stock_price": ".price",
                    "stock_change": ".change",
                    "stock_name": ".name"
                }
            },
            "sina": {
                "name": "新浪财经",
                "url": "https://finance.sina.com.cn",
                "search_url": "https://search.sina.com.cn/?q={query}&c=stock",
                "stock_url": "https://finance.sina.com.cn/realstock/company/{market}{code}/nc.shtml",
                "selectors": {
                    "stock_price": "#price",
                    "stock_change": "#change"
                }
            },
            "tonghuashun": {
                "name": "同花顺",
                "url": "https://www.10jqka.com.cn",
                "search_url": "http://www.iwencai.com/unifiedwap/result?w={query}",
                "selectors": {
                    "stock_price": ".price",
                    "stock_change": ".change"
                }
            }
        }
    
    async def _ensure_browser(self):
        """确保浏览器已初始化"""
        if self._browser is not None:
            return
        
        # 优先使用OpenManus的浏览器工具
        if OPENMANUS_AVAILABLE:
            try:
                from app.tool.browser_use_tool import BrowserUseTool
                self._openmanus_browser = BrowserUseTool()
                logger.info("✅ 使用OpenManus BrowserUseTool")
                return
            except Exception as e:
                logger.warning(f"OpenManus BrowserUseTool初始化失败: {e}")
        
        # 回退到直接使用Playwright
        try:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=self.headless)
            self._page = await self._browser.new_page()
            logger.info("✅ 使用Playwright直接模式")
        except ImportError:
            raise RuntimeError("Playwright未安装，请运行: pip install playwright && playwright install")
    
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
            if self._openmanus_browser:
                # 使用OpenManus
                result = await self._openmanus_browser.execute(
                    action="go_to_url",
                    url=url
                )
                return BrowserResult(
                    success=True,
                    data={"output": result.output if hasattr(result, 'output') else str(result)},
                    url=url
                )
            else:
                # 使用Playwright
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
            selector: CSS选择器或元素索引
        
        Returns:
            BrowserResult: 操作结果
        """
        await self._ensure_browser()
        
        try:
            if self._openmanus_browser:
                # OpenManus使用索引
                if isinstance(selector, int):
                    result = await self._openmanus_browser.execute(
                        action="click_element",
                        index=selector
                    )
                else:
                    # 尝试转换选择器到索引（需要先获取页面状态）
                    result = await self._openmanus_browser.execute(
                        action="click_element",
                        index=0  # 默认点击第一个匹配元素
                    )
                return BrowserResult(
                    success=True,
                    data={"output": result.output if hasattr(result, 'output') else str(result)}
                )
            else:
                await self._page.click(selector)
                return BrowserResult(success=True, data={"clicked": selector})
        except Exception as e:
            logger.error(f"点击失败: {selector}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def type_text(self, selector: str, text: str, submit: bool = False) -> BrowserResult:
        """
        输入文本
        
        Args:
            selector: CSS选择器或元素索引
            text: 要输入的文本
            submit: 是否提交（按回车）
        
        Returns:
            BrowserResult: 操作结果
        """
        await self._ensure_browser()
        
        try:
            if self._openmanus_browser:
                result = await self._openmanus_browser.execute(
                    action="input_text",
                    index=0 if isinstance(selector, str) else selector,
                    text=text,
                    submit=submit
                )
                return BrowserResult(
                    success=True,
                    data={"output": result.output if hasattr(result, 'output') else str(result)}
                )
            else:
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
            if self._openmanus_browser:
                # OpenManus需要使用extract_content
                result = await self._openmanus_browser.execute(
                    action="extract_content",
                    goal=f"获取元素 {selector} 的文本内容"
                )
                text = result.output if hasattr(result, 'output') else str(result)
                return BrowserResult(success=True, data={"text": text})
            else:
                element = await self._page.query_selector(selector)
                if element:
                    text = await element.text_content()
                    return BrowserResult(success=True, data={"text": text.strip() if text else ""})
                return BrowserResult(success=False, error=f"元素未找到: {selector}")
        except Exception as e:
            logger.error(f"获取文本失败: {selector}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def screenshot(self, path: str = None) -> BrowserResult:
        """
        截取页面截图
        
        Args:
            path: 保存路径（可选）
        
        Returns:
            BrowserResult: 包含截图路径的操作结果
        """
        await self._ensure_browser()
        
        try:
            if path is None:
                from datetime import datetime
                path = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            if self._openmanus_browser:
                # OpenManus的截图功能
                result = await self._openmanus_browser.execute(
                    action="screenshot",
                    filename=path
                )
                return BrowserResult(success=True, data={"path": path})
            else:
                await self._page.screenshot(path=path)
                return BrowserResult(success=True, data={"path": path})
        except Exception as e:
            logger.error(f"截图失败: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def extract_stock_price(self, stock_code: str, source: str = "eastmoney") -> BrowserResult:
        """
        提取股票价格
        
        Args:
            stock_code: 股票代码（如 000001, 600000）
            source: 数据源 ("eastmoney", "sina", "tonghuashun")
        
        Returns:
            BrowserResult: 包含价格信息的操作结果
        """
        await self._ensure_browser()
        
        # 确定市场
        market = "sh" if stock_code.startswith("6") else "sz"
        
        site_config = self.finance_sites.get(source, self.finance_sites["eastmoney"])
        
        try:
            # 构建URL
            if source == "eastmoney":
                url = site_config["stock_url"].format(market=market, code=stock_code)
            else:
                url = site_config["stock_url"].format(market=market, code=stock_code)
            
            # 导航到股票页面
            nav_result = await self.navigate(url)
            if not nav_result.success:
                return nav_result
            
            # 等待页面加载
            await asyncio.sleep(2)
            
            # 提取价格
            if self._openmanus_browser:
                result = await self._openmanus_browser.execute(
                    action="extract_content",
                    goal=f"获取股票 {stock_code} 的当前价格、涨跌幅和成交量"
                )
                
                # 解析结果
                output = result.output if hasattr(result, 'output') else str(result)
                return BrowserResult(
                    success=True,
                    data={
                        "code": stock_code,
                        "market": market,
                        "source": source,
                        "raw_data": output
                    },
                    url=url
                )
            else:
                # 使用Playwright直接提取
                price_data = {}
                
                # 尝试提取价格
                try:
                    price_el = await self._page.query_selector(site_config["selectors"]["stock_price"])
                    if price_el:
                        price_data["price"] = await price_el.text_content()
                except:
                    pass
                
                # 尝试提取涨跌幅
                try:
                    change_el = await self._page.query_selector(site_config["selectors"]["stock_change"])
                    if change_el:
                        price_data["change"] = await change_el.text_content()
                except:
                    pass
                
                return BrowserResult(
                    success=True,
                    data={
                        "code": stock_code,
                        "market": market,
                        "source": source,
                        **price_data
                    },
                    url=url
                )
        except Exception as e:
            logger.error(f"提取股票价格失败: {stock_code}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def search_stock(self, query: str, source: str = "eastmoney") -> BrowserResult:
        """
        搜索股票
        
        Args:
            query: 搜索关键词（股票代码或名称）
            source: 数据源
        
        Returns:
            BrowserResult: 包含搜索结果的操作结果
        """
        await self._ensure_browser()
        
        site_config = self.finance_sites.get(source, self.finance_sites["eastmoney"])
        search_url = site_config["search_url"].format(query=query)
        
        try:
            nav_result = await self.navigate(search_url)
            if not nav_result.success:
                return nav_result
            
            await asyncio.sleep(2)
            
            if self._openmanus_browser:
                result = await self._openmanus_browser.execute(
                    action="extract_content",
                    goal=f"提取搜索结果中的股票列表，包括股票代码、名称和当前价格"
                )
                
                output = result.output if hasattr(result, 'output') else str(result)
                return BrowserResult(
                    success=True,
                    data={
                        "query": query,
                        "source": source,
                        "results": output
                    },
                    url=search_url
                )
            else:
                # Playwright模式：简单返回页面标题
                title = await self._page.title()
                return BrowserResult(
                    success=True,
                    data={
                        "query": query,
                        "source": source,
                        "page_title": title
                    },
                    url=search_url
                )
        except Exception as e:
            logger.error(f"搜索股票失败: {query}, 错误: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def get_page_content(self) -> BrowserResult:
        """
        获取当前页面的文本内容
        
        Returns:
            BrowserResult: 包含页面内容的操作结果
        """
        await self._ensure_browser()
        
        try:
            if self._openmanus_browser:
                result = await self._openmanus_browser.execute(
                    action="extract_content",
                    goal="提取页面的主要文本内容"
                )
                output = result.output if hasattr(result, 'output') else str(result)
                return BrowserResult(success=True, data={"content": output})
            else:
                content = await self._page.content()
                # 简单提取文本
                from html.parser import HTMLParser
                
                class TextExtractor(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.text = []
                    
                    def handle_data(self, data):
                        self.text.append(data.strip())
                
                extractor = TextExtractor()
                extractor.feed(content)
                text = ' '.join(filter(None, extractor.text))
                
                return BrowserResult(success=True, data={"content": text[:5000]})  # 限制长度
        except Exception as e:
            logger.error(f"获取页面内容失败: {e}")
            return BrowserResult(success=False, error=str(e))
    
    async def cleanup(self):
        """清理资源"""
        try:
            if self._openmanus_browser:
                await self._openmanus_browser.cleanup()
                self._openmanus_browser = None
            
            if self._page:
                await self._page.close()
                self._page = None
            
            if self._browser:
                await self._browser.close()
                self._browser = None
            
            if hasattr(self, '_playwright') and self._playwright:
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


# ==================== 测试函数 ====================

async def test_browser_tool():
    """测试浏览器工具"""
    print("=" * 80)
    print("OpenManus浏览器工具测试")
    print("=" * 80)
    
    async with OpenManusBrowserTool(headless=True) as tool:
        # 测试1: 导航到东方财富
        print("\n测试1: 导航到东方财富网站")
        result = await tool.navigate("https://www.eastmoney.com")
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.success:
            print(f"  URL: {result.url}")
        else:
            print(f"  错误: {result.error}")
        
        # 测试2: 获取页面内容
        print("\n测试2: 获取页面内容")
        result = await tool.get_page_content()
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.success:
            content = result.data.get("content", "")[:200]
            print(f"  内容预览: {content}...")
        
        # 测试3: 提取股票价格（需要LLM API才能智能提取）
        print("\n测试3: 提取股票价格 (000001)")
        result = await tool.extract_stock_price("000001")
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.success:
            print(f"  数据: {result.data}")
        else:
            print(f"  错误: {result.error}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_browser_tool())
