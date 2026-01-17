# -*- coding: utf-8 -*-
"""Lavague AI浏览器自动化爬虫工具"""

import logging
from typing import Dict, Any, Optional, List
import time

logger = logging.getLogger(__name__)

class LavagueCrawler:
    """基于Lavague的AI驱动浏览器自动化"""
    
    def __init__(self, headless: bool = True, model: str = "gpt-4o-mini"):
        """
        初始化Lavague爬虫
        
        Args:
            headless: 是否无头模式
            model: 使用的AI模型
        """
        self.headless = headless
        self.model = model
        self.engine = None
        self._init_engine()
    
    def _init_engine(self):
        """初始化Lavague引擎"""
        try:
            from lavague import ActionEngine, WorldModel, get_selenium_driver
            from lavague.core import PythonActionEngine
            
            # 获取Selenium driver
            driver = get_selenium_driver(headless=self.headless)
            
            # 初始化WorldModel和ActionEngine
            world_model = WorldModel(model=self.model)
            self.engine = ActionEngine(world_model, driver)
            
            logger.info(f"Lavague引擎初始化成功 (model: {self.model})")
            
        except ImportError:
            logger.warning("Lavague未安装，请运行: pip install lavague")
            logger.info("Lavague是一个AI驱动的浏览器自动化工具，可以理解自然语言指令")
            self.engine = None
        except Exception as e:
            logger.error(f"Lavague引擎初始化失败: {e}")
            self.engine = None
    
    def navigate(self, url: str) -> Dict[str, Any]:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
        """
        if not self.engine:
            return {
                "success": False,
                "error": "Lavague引擎未初始化，请先安装: pip install lavague"
            }
        
        try:
            self.engine.get(url)
            time.sleep(2)  # 等待页面加载
            
            return {
                "success": True,
                "url": url,
                "current_url": self.engine.driver.current_url,
                "title": self.engine.driver.title
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    def execute_instruction(self, instruction: str, max_actions: int = 10) -> Dict[str, Any]:
        """
        执行自然语言指令
        
        Args:
            instruction: 自然语言指令，如"点击登录按钮"、"填写用户名和密码"
            max_actions: 最大执行动作数
        
        Returns:
            执行结果
        """
        if not self.engine:
            return {
                "success": False,
                "error": "Lavague引擎未初始化"
            }
        
        try:
            # 执行指令
            result = self.engine.run(instruction, max_actions=max_actions)
            
            # 获取页面状态
            page_source = self.engine.driver.page_source
            current_url = self.engine.driver.current_url
            title = self.engine.driver.title
            
            return {
                "success": True,
                "instruction": instruction,
                "result": str(result),
                "current_url": current_url,
                "title": title,
                "page_length": len(page_source),
                "actions_executed": getattr(result, 'actions_count', 0)
            }
            
        except Exception as e:
            logger.error(f"执行Lavague指令失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "instruction": instruction
            }
    
    def extract_data(self, description: str) -> Dict[str, Any]:
        """
        根据描述提取数据
        
        Args:
            description: 数据描述，如"提取所有产品名称和价格"
        
        Returns:
            提取的数据
        """
        if not self.engine:
            return {
                "success": False,
                "error": "Lavague引擎未初始化"
            }
        
        try:
            # 使用Lavague提取数据
            instruction = f"提取以下数据：{description}，并将结果以JSON格式返回"
            result = self.engine.run(instruction)
            
            # 尝试从页面提取结构化数据
            page_source = self.engine.driver.page_source
            
            return {
                "success": True,
                "description": description,
                "data": str(result),
                "page_source_length": len(page_source)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "description": description
            }
    
    def take_screenshot(self, save_path: Optional[str] = None) -> Dict[str, Any]:
        """截取页面截图"""
        if not self.engine:
            return {"success": False, "error": "Lavague引擎未初始化"}
        
        try:
            if not save_path:
                save_path = f"/tmp/lavague_screenshot_{int(time.time())}.png"
            
            self.engine.driver.save_screenshot(save_path)
            return {
                "success": True,
                "screenshot_path": save_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭浏览器"""
        if self.engine and self.engine.driver:
            self.engine.driver.quit()
            self.engine = None
            logger.info("Lavague引擎已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局实例
_lavague_crawler: Optional[LavagueCrawler] = None

def get_lavague_crawler(headless: bool = True, model: str = "gpt-4o-mini") -> LavagueCrawler:
    """获取Lavague爬虫实例"""
    global _lavague_crawler
    if _lavague_crawler is None:
        _lavague_crawler = LavagueCrawler(headless=headless, model=model)
    return _lavague_crawler













































