# -*- coding: utf-8 -*-
"""Selenium浏览器自动化爬虫工具"""

import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import time

logger = logging.getLogger(__name__)

class SeleniumCrawler:
    """基于Selenium的浏览器自动化爬虫"""
    
    def __init__(self, headless: bool = True, browser: str = "chrome"):
        """
        初始化Selenium爬虫
        
        Args:
            headless: 是否无头模式（不显示浏览器窗口）
            browser: 浏览器类型 ("chrome" 或 "firefox")
        """
        self.headless = headless
        self.browser = browser
        self.driver = None
        self._init_driver()
    
    def _init_driver(self):
        """初始化WebDriver"""
        try:
            if self.browser.lower() == "chrome":
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.chrome.service import Service
                
                chrome_options = Options()
                if self.headless:
                    chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36')
                
                self.driver = webdriver.Chrome(options=chrome_options)
                
            elif self.browser.lower() == "firefox":
                from selenium import webdriver
                from selenium.webdriver.firefox.options import Options
                
                firefox_options = Options()
                if self.headless:
                    firefox_options.add_argument('--headless')
                self.driver = webdriver.Firefox(options=firefox_options)
            else:
                raise ValueError(f"不支持的浏览器类型: {self.browser}")
                
            logger.info(f"Selenium {self.browser} driver 初始化成功")
            
        except ImportError:
            logger.error("Selenium未安装，请运行: pip install selenium")
            raise
        except Exception as e:
            logger.error(f"Selenium driver初始化失败: {e}")
            raise
    
    def fetch_dynamic_page(self, url: str, wait_time: int = 3, wait_selector: Optional[str] = None) -> Dict[str, Any]:
        """
        抓取动态加载的网页
        
        Args:
            url: 目标URL
            wait_time: 等待时间（秒）
            wait_selector: 等待元素选择器（CSS选择器）
        
        Returns:
            包含页面内容的字典
        """
        try:
            if not self.driver:
                self._init_driver()
            
            self.driver.get(url)
            
            # 等待页面加载
            if wait_selector:
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                from selenium.webdriver.common.by import By
                
                wait = WebDriverWait(self.driver, wait_time)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_selector)))
            else:
                time.sleep(wait_time)
            
            # 获取页面内容
            page_source = self.driver.page_source
            title = self.driver.title
            current_url = self.driver.current_url
            
            return {
                "success": True,
                "url": url,
                "current_url": current_url,
                "title": title,
                "html": page_source,
                "text_length": len(page_source)
            }
            
        except Exception as e:
            logger.error(f"抓取动态页面失败: {e}")
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }
    
    def click_element(self, selector: str, by: str = "css") -> Dict[str, Any]:
        """
        点击页面元素
        
        Args:
            selector: 元素选择器
            by: 选择器类型 ("css", "id", "xpath", "class", "name")
        
        Returns:
            操作结果
        """
        try:
            if not self.driver:
                return {"success": False, "error": "Driver未初始化"}
            
            from selenium.webdriver.common.by import By
            
            by_map = {
                "css": By.CSS_SELECTOR,
                "id": By.ID,
                "xpath": By.XPATH,
                "class": By.CLASS_NAME,
                "name": By.NAME
            }
            
            element = self.driver.find_element(by_map[by.lower()], selector)
            element.click()
            
            return {"success": True, "action": "click", "selector": selector}
            
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector}
    
    def fill_input(self, selector: str, text: str, by: str = "css") -> Dict[str, Any]:
        """
        填写输入框
        
        Args:
            selector: 元素选择器
            text: 要输入的文本
            by: 选择器类型
        """
        try:
            from selenium.webdriver.common.by import By
            
            by_map = {
                "css": By.CSS_SELECTOR,
                "id": By.ID,
                "xpath": By.XPATH,
                "class": By.CLASS_NAME,
                "name": By.NAME
            }
            
            element = self.driver.find_element(by_map[by.lower()], selector)
            element.clear()
            element.send_keys(text)
            
            return {"success": True, "action": "fill", "selector": selector, "text": text}
            
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector}
    
    def extract_elements(self, selector: str, attribute: Optional[str] = None) -> Dict[str, Any]:
        """
        提取页面元素
        
        Args:
            selector: CSS选择器
            attribute: 要提取的属性（如"text", "href", "src"），None则提取文本
        
        Returns:
            提取的元素列表
        """
        try:
            if not self.driver:
                return {"success": False, "error": "Driver未初始化"}
            
            from selenium.webdriver.common.by import By
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
            
            results = []
            for elem in elements:
                if attribute == "text":
                    value = elem.text
                elif attribute:
                    value = elem.get_attribute(attribute)
                else:
                    value = elem.text
                
                results.append({
                    "tag": elem.tag_name,
                    "value": value,
                    "html": elem.get_attribute('outerHTML')[:500] if attribute != "html" else None
                })
            
            return {
                "success": True,
                "selector": selector,
                "count": len(results),
                "elements": results
            }
            
        except Exception as e:
            return {"success": False, "error": str(e), "selector": selector}
    
    def execute_script(self, script: str) -> Dict[str, Any]:
        """
        执行JavaScript代码
        
        Args:
            script: JavaScript代码
        """
        try:
            result = self.driver.execute_script(script)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Dict[str, Any]:
        """
        截取页面截图
        
        Args:
            save_path: 保存路径
        """
        try:
            if not save_path:
                save_path = f"/tmp/selenium_screenshot_{int(time.time())}.png"
            
            self.driver.save_screenshot(save_path)
            return {
                "success": True,
                "screenshot_path": save_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Selenium driver 已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局实例（可选）
_selenium_crawler: Optional[SeleniumCrawler] = None

def get_selenium_crawler(headless: bool = True, browser: str = "chrome") -> SeleniumCrawler:
    """获取Selenium爬虫实例（单例模式）"""
    global _selenium_crawler
    if _selenium_crawler is None:
        _selenium_crawler = SeleniumCrawler(headless=headless, browser=browser)
    return _selenium_crawler

