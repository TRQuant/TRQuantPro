# -*- coding: utf-8 -*-
"""
Playwright智能爬虫 - 参考LaVague实现方式
=======================================

本模块参考LaVague的PlaywrightDriver实现，提供智能浏览器自动化功能。

参考实现：
- LaVague PlaywrightDriver: /tmp/lavague-source/lavague-integrations/drivers/lavague-drivers-playwright/
- LaVague BaseDriver: /tmp/lavague-source/lavague-core/lavague/core/base_driver.py

核心特性（参考LaVague）：
1. wait_for_idle - 等待页面稳定（networkidle + DOM稳定）
2. 智能元素定位 - 支持xpath、css等多种方式
3. 交互操作 - click、fill、scroll等
4. 内容提取 - HTML、文本、截图等
"""

import logging
from typing import Dict, Any, Optional, List
import time
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

# 参考LaVague的JavaScript代码
JS_WAIT_DOM_IDLE = """
return new Promise(resolve => {
    const timeout = arguments[0] || 10000;
    const stabilityThreshold = arguments[1] || 100;

    let mutationObserver;
    let timeoutId = null;

    const waitForIdle = () => {
        if (timeoutId) clearTimeout(timeoutId);
        timeoutId = setTimeout(() => resolve(true), stabilityThreshold);
    };
    mutationObserver = new MutationObserver(waitForIdle);
    mutationObserver.observe(document.body, {
        childList: true,
        attributes: true,
        subtree: true,
    });
    waitForIdle();

    setTimeout(() => {
        resolve(false);
        mutationObserver.disconnect();
        mutationObserver = null;
        if (timeoutId) {
            clearTimeout(timeoutId);
            timeoutId = null;
        }
    }, timeout);
});
"""


class PlaywrightSmartCrawler:
    """
    Playwright智能爬虫 - 参考LaVague实现方式
    
    核心功能（参考LaVague）：
    - wait_for_idle: 等待页面稳定（networkidle + DOM稳定）
    - 智能元素定位和交互
    - 内容提取
    """
    
    def __init__(
        self,
        headless: bool = True,
        width: int = 1920,
        height: int = 1080,
        waiting_completion_timeout: int = 10,
    ):
        """
        初始化Playwright智能爬虫
        
        Args:
            headless: 是否无头模式
            width: 窗口宽度
            height: 窗口高度
            waiting_completion_timeout: 等待完成超时时间（秒）
        """
        self.headless = headless
        self.width = width
        self.height = height
        self.waiting_completion_timeout = waiting_completion_timeout
        self._playwright = None
        self._browser = None
        self._page = None
        self._init_browser()
    
    def _init_browser(self):
        """初始化浏览器（参考LaVague PlaywrightDriver）"""
        try:
            from playwright.sync_api import sync_playwright
            
            self._playwright = sync_playwright().start()
            
            # 参考LaVague的浏览器配置
            user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
            args = [
                "--disable-web-security",
                "--disable-site-isolation-trials",
                "--disable-notifications",
            ]
            
            self._browser = self._playwright.chromium.launch(
                headless=self.headless,
                args=args,
            )
            context = self._browser.new_context(user_agent=user_agent)
            self._page = context.new_page()
            self._page.set_viewport_size({"width": self.width, "height": self.height})
            
            logger.info("✅ Playwright浏览器初始化成功")
            
        except ImportError:
            logger.error("Playwright未安装，请运行: pip install playwright && playwright install chromium")
            raise
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            raise
    
    def wait_for_idle(self):
        """
        等待页面稳定（参考LaVague实现）
        
        LaVague的实现方式：
        1. 等待networkidle（网络空闲）
        2. 等待DOM稳定（MutationObserver）
        """
        t = time.time()
        try:
            # 等待网络空闲（参考LaVague）
            self._page.wait_for_load_state(
                "networkidle", timeout=self.waiting_completion_timeout * 1000
            )
        except:
            # 超时也继续
            pass
        
        elapsed = time.time() - t
        
        # 等待DOM稳定（参考LaVague的JS_WAIT_DOM_IDLE）
        try:
            self._page.evaluate(
                JS_WAIT_DOM_IDLE,
                max(0, round((self.waiting_completion_timeout - elapsed) * 1000)),
                100  # stabilityThreshold
            )
        except:
            pass
        
        total_elapsed = time.time() - t
        if total_elapsed > 10:
            logger.info(f"等待页面稳定耗时: {total_elapsed:.2f}秒")
    
    def navigate(self, url: str) -> Dict[str, Any]:
        """
        导航到指定URL（参考LaVague）
        
        Args:
            url: 目标URL
        """
        try:
            self._page.goto(url, wait_until="domcontentloaded")
            self.wait_for_idle()  # 参考LaVague的wait_for_idle
            
            current_url = self._page.url
            title = self._page.title()
            
            return {
                "success": True,
                "url": url,
                "current_url": current_url,
                "title": title
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def click(self, selector: str, by: str = "css") -> Dict[str, Any]:
        """
        点击元素（参考LaVague）
        
        Args:
            selector: 选择器
            by: 选择器类型 ("css", "xpath")
        """
        try:
            if by == "xpath":
                locator = self._page.locator(f"xpath={selector}")
            else:
                locator = self._page.locator(selector)
            
            locator.first.click()
            self.wait_for_idle()  # 等待操作完成
            
            return {"success": True, "action": "click", "selector": selector}
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector}
    
    def fill(self, selector: str, value: str, enter: bool = False) -> Dict[str, Any]:
        """
        填写输入框（参考LaVague）
        
        Args:
            selector: 选择器
            value: 要输入的值
            enter: 是否按回车
        """
        try:
            locator = self._page.locator(selector).first
            locator.clear()
            locator.click()
            locator.fill(value)
            
            if enter:
                locator.press("Enter")
            
            self.wait_for_idle()
            
            return {"success": True, "action": "fill", "selector": selector, "value": value}
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector}
    
    def extract_text(self, selector: Optional[str] = None) -> Dict[str, Any]:
        """
        提取文本内容（参考LaVague）
        
        Args:
            selector: 选择器（None则提取整个页面）
        """
        try:
            if selector:
                elements = self._page.locator(selector).all()
                texts = [elem.text_content() for elem in elements]
                return {
                    "success": True,
                    "selector": selector,
                    "count": len(texts),
                    "texts": texts
                }
            else:
                # 提取整个页面文本
                content = self._page.content()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator='\n', strip=True)
                
                return {
                    "success": True,
                    "text": text,
                    "length": len(text)
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_html(self) -> str:
        """获取页面HTML（参考LaVague）"""
        return self._page.content()
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Dict[str, Any]:
        """截取页面截图（参考LaVague）"""
        try:
            if not save_path:
                save_path = f"/tmp/playwright_screenshot_{int(time.time())}.png"
            
            self._page.screenshot(path=save_path)
            return {
                "success": True,
                "screenshot_path": save_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭浏览器"""
        if self._page:
            self._page.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        logger.info("Playwright浏览器已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局实例
_playwright_smart_crawler: Optional[PlaywrightSmartCrawler] = None

def get_playwright_smart_crawler(
    headless: bool = True,
    width: int = 1920,
    height: int = 1080
) -> PlaywrightSmartCrawler:
    """
    获取Playwright智能爬虫实例
    
    Args:
        headless: 是否无头模式
        width: 窗口宽度
        height: 窗口高度
    
    Returns:
        PlaywrightSmartCrawler实例
    """
    global _playwright_smart_crawler
    if _playwright_smart_crawler is None:
        _playwright_smart_crawler = PlaywrightSmartCrawler(
            headless=headless,
            width=width,
            height=height
        )
    return _playwright_smart_crawler
