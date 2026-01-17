# -*- coding: utf-8 -*-
"""
LaVague AI浏览器自动化爬虫工具 - V2（基于官方源码重构）
=======================================================

本版本完全参照LaVague官方实现，使用正确的API和Context机制。

参考：
- https://github.com/lavague-ai/LaVague
- 使用官方推荐的WebAgent + Context方式
"""

import logging
from typing import Dict, Any, Optional
import time
import sys
from pathlib import Path

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


class LavagueCrawlerV2:
    """
    基于LaVague的AI驱动浏览器自动化（V2版本）
    
    完全参照官方实现，使用正确的API：
    - 使用WebAgent（官方推荐）
    - 使用Context配置模型
    - 支持自定义模型（Cursor/Ollama/OpenAI）
    """
    
    def __init__(
        self,
        headless: bool = True,
        model_type: str = "ollama",  # "ollama", "cursor", "openai"
        llm_model: str = "llama3.2",
        mm_llm_model: str = "llama3.2-vision",
    ):
        """
        初始化Lavague爬虫
        
        Args:
            headless: 是否无头模式
            model_type: 模型类型
                - "ollama": 本地Ollama模型（推荐，无需API密钥）
                - "cursor": Cursor内置模型（通过Cursor IDE）
                - "openai": OpenAI API（需要OPENAI_API_KEY）
            llm_model: LLM模型名称
            mm_llm_model: 多模态LLM模型名称
        """
        self.headless = headless
        self.model_type = model_type
        self.llm_model = llm_model
        self.mm_llm_model = mm_llm_model
        self.agent = None
        self.driver = None
        self._init_agent()
    
    def _init_agent(self):
        """初始化LaVague Agent（参照官方实现）"""
        try:
            # 导入LaVague核心模块
            from lavague.core import ActionEngine, WorldModel
            from lavague.core.agents import WebAgent
            from lavague.drivers.selenium import SeleniumDriver
            
            # 导入自定义Context
            try:
                from core.crawlers.lavague_cursor_context import CursorContext
                context = CursorContext(model_type=self.model_type)
                logger.info(f"✅ 使用CursorContext (model_type={self.model_type})")
            except ImportError:
                # 如果自定义Context不可用，使用默认Context
                from lavague.core.context import get_default_context
                context = get_default_context()
                logger.warning("⚠️  使用默认Context（需要OPENAI_API_KEY）")
            
            # 创建Selenium driver
            self.driver = SeleniumDriver(headless=self.headless)
            
            # 使用from_context方法创建ActionEngine和WorldModel（官方推荐方式）
            action_engine = ActionEngine.from_context(context, self.driver)
            world_model = WorldModel.from_context(context)
            
            # 创建WebAgent（官方推荐使用WebAgent）
            self.agent = WebAgent(world_model, action_engine)
            
            logger.info(f"✅ LaVague Agent初始化成功 (model_type={self.model_type})")
            
        except ImportError as e:
            logger.warning(f"LaVague未安装或导入失败: {e}")
            logger.info("请运行: ./venv/bin/python -m pip install lavague")
            if self.model_type == "ollama":
                logger.info("还需要: pip install llama-index-llms-ollama llama-index-embeddings-ollama")
            self.agent = None
            self.driver = None
        except Exception as e:
            logger.error(f"LaVague Agent初始化失败: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            self.agent = None
            self.driver = None
    
    def navigate(self, url: str) -> Dict[str, Any]:
        """
        导航到指定URL
        
        Args:
            url: 目标URL
        """
        if not self.agent:
            return {
                "success": False,
                "error": "LaVague Agent未初始化，请先安装: pip install lavague"
            }
        
        try:
            self.agent.get(url)
            time.sleep(2)  # 等待页面加载
            
            if self.driver:
                current_url = self.driver.driver.current_url
                title = self.driver.driver.title
            else:
                current_url = url
                title = ""
            
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
    
    def execute_instruction(self, instruction: str, max_actions: int = 10) -> Dict[str, Any]:
        """
        执行自然语言指令
        
        Args:
            instruction: 自然语言指令
            max_actions: 最大执行动作数
        """
        if not self.agent:
            return {
                "success": False,
                "error": "LaVague Agent未初始化"
            }
        
        try:
            # 使用WebAgent的run方法（官方推荐）
            result = self.agent.run(instruction, n_steps=max_actions)
            
            # 获取页面状态
            if self.driver:
                page_source = self.driver.driver.page_source
                current_url = self.driver.driver.current_url
                title = self.driver.driver.title
            else:
                page_source = ""
                current_url = ""
                title = ""
            
            return {
                "success": True,
                "instruction": instruction,
                "result": str(result) if result else "",
                "current_url": current_url,
                "title": title,
                "page_length": len(page_source),
                "actions_executed": getattr(result, 'actions_count', 0) if hasattr(result, 'actions_count') else 0
            }
            
        except Exception as e:
            logger.error(f"执行LaVague指令失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "instruction": instruction
            }
    
    def extract_data(self, description: str) -> Dict[str, Any]:
        """
        根据描述提取数据
        
        Args:
            description: 数据描述
        """
        if not self.agent:
            return {
                "success": False,
                "error": "LaVague Agent未初始化"
            }
        
        try:
            # 使用WebAgent提取数据
            instruction = f"提取以下数据：{description}，并将结果以JSON格式返回"
            result = self.agent.run(instruction)
            
            # 获取页面源码
            if self.driver:
                page_source = self.driver.driver.page_source
            else:
                page_source = ""
            
            return {
                "success": True,
                "description": description,
                "data": str(result) if result else "",
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
        if not self.driver:
            return {"success": False, "error": "Driver未初始化"}
        
        try:
            if not save_path:
                save_path = f"/tmp/lavague_screenshot_{int(time.time())}.png"
            
            self.driver.driver.save_screenshot(save_path)
            return {
                "success": True,
                "screenshot_path": save_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.driver.quit()
            except:
                pass
            self.driver = None
        self.agent = None
        logger.info("LaVague Agent已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局实例
_lavague_crawler_v2: Optional[LavagueCrawlerV2] = None

def get_lavague_crawler_v2(
    headless: bool = True,
    model_type: str = "ollama"
) -> LavagueCrawlerV2:
    """
    获取LaVague爬虫实例（V2版本）
    
    Args:
        headless: 是否无头模式
        model_type: 模型类型 ("ollama", "cursor", "openai")
    
    Returns:
        LavagueCrawlerV2实例
    """
    global _lavague_crawler_v2
    if _lavague_crawler_v2 is None:
        _lavague_crawler_v2 = LavagueCrawlerV2(headless=headless, model_type=model_type)
    return _lavague_crawler_v2
