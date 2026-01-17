# -*- coding: utf-8 -*-
"""
OpenManus智能Agent（Core模块版本）
=================================
韬睿量化系统的智能Agent，整合浏览器工具和数据收集功能

提供统一的任务执行接口，支持：
- 自然语言任务解析
- 浏览器自动化
- 财经数据收集
- MCP工具调用

使用方式:
    from core.automation import OpenManusAgent
    
    async with OpenManusAgent() as agent:
        result = await agent.execute("获取最新财经新闻")
        result = await agent.execute("分析市场情绪")
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import re

# 配置日志
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 导入同模块的浏览器Agent
from .browser_agent import BrowserAgent, BrowserResult


class TaskType(Enum):
    """任务类型"""
    BROWSE = "browse"
    FETCH_NEWS = "fetch_news"
    FETCH_ANNOUNCEMENT = "fetch_announcement"
    ANALYZE_MARKET = "analyze_market"
    GET_STOCK_INFO = "get_stock_info"
    SEARCH = "search"
    MCP_CALL = "mcp_call"
    UNKNOWN = "unknown"


@dataclass
class AgentTask:
    """Agent任务"""
    id: str
    type: TaskType
    description: str
    params: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AgentResult:
    """Agent执行结果"""
    success: bool
    task_id: str
    task_type: str
    data: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    steps: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "task_id": self.task_id,
            "task_type": self.task_type,
            "data": self.data,
            "error": self.error,
            "execution_time": self.execution_time,
            "steps": self.steps
        }


class OpenManusAgent:
    """
    OpenManus智能Agent
    
    提供任务解析、执行和工具调用的统一接口
    
    Attributes:
        headless: 浏览器是否使用无头模式
    """
    
    # 任务关键词映射
    TASK_KEYWORDS = {
        TaskType.BROWSE: ["访问", "打开", "浏览", "查看网页", "navigate", "browse"],
        TaskType.FETCH_NEWS: ["新闻", "资讯", "快讯", "消息", "news"],
        TaskType.FETCH_ANNOUNCEMENT: ["公告", "announcement", "披露", "报告"],
        TaskType.ANALYZE_MARKET: ["分析", "市场", "趋势", "情绪", "行情", "analyze"],
        TaskType.GET_STOCK_INFO: ["股票", "股价", "行情", "stock", "price"],
        TaskType.SEARCH: ["搜索", "查找", "search", "find"],
        TaskType.MCP_CALL: ["mcp", "工具", "调用"]
    }
    
    def __init__(self, headless: bool = True):
        """
        初始化Agent
        
        Args:
            headless: 浏览器是否使用无头模式
        """
        self.headless = headless
        self._browser: Optional[BrowserAgent] = None
        self._mcp_client = None
        self._task_counter = 0
        
        # 注册工具
        self._tools: Dict[str, Callable] = {}
        self._register_tools()
    
    def _register_tools(self):
        """注册可用工具"""
        self._tools = {
            "browser.navigate": self._tool_navigate,
            "browser.screenshot": self._tool_screenshot,
            "browser.get_content": self._tool_get_content,
            "stock.get_price": self._tool_get_stock_price,
            "market.analyze": self._tool_analyze_market,
            "mcp.call": self._tool_mcp_call
        }
        logger.info(f"已注册 {len(self._tools)} 个工具")
    
    async def _ensure_browser(self) -> BrowserAgent:
        """确保浏览器Agent已初始化"""
        if self._browser is None:
            self._browser = BrowserAgent(headless=self.headless)
        return self._browser
    
    async def _ensure_mcp_client(self):
        """确保MCP客户端已初始化"""
        if self._mcp_client is None:
            try:
                from core.mcp.client import MCPClient
                self._mcp_client = MCPClient(
                    project_root=PROJECT_ROOT, 
                    python_path=sys.executable
                )
                logger.info("✅ MCP客户端已初始化")
            except ImportError:
                logger.warning("MCP客户端不可用")
        return self._mcp_client
    
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        self._task_counter += 1
        return f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._task_counter:04d}"
    
    def _parse_task(self, description: str) -> AgentTask:
        """
        解析任务描述
        
        Args:
            description: 任务描述文本
        
        Returns:
            AgentTask: 解析后的任务
        """
        task_id = self._generate_task_id()
        task_type = TaskType.UNKNOWN
        params = {}
        
        desc_lower = description.lower()
        
        # 识别任务类型
        for t_type, keywords in self.TASK_KEYWORDS.items():
            if any(kw in desc_lower for kw in keywords):
                task_type = t_type
                break
        
        # 提取参数
        # URL
        url_match = re.search(r'https?://[^\s]+', description)
        if url_match:
            params["url"] = url_match.group()
        
        # 股票代码
        stock_match = re.search(r'(\d{6})', description)
        if stock_match:
            params["stock_code"] = stock_match.group(1)
        
        # 数量
        limit_match = re.search(r'(\d+)\s*(条|个|篇)', description)
        if limit_match:
            params["limit"] = int(limit_match.group(1))
        
        return AgentTask(
            id=task_id,
            type=task_type,
            description=description,
            params=params
        )
    
    async def execute(self, task_description: str) -> AgentResult:
        """
        执行任务
        
        Args:
            task_description: 任务描述
        
        Returns:
            AgentResult: 执行结果
        """
        start_time = datetime.now()
        steps = []
        
        try:
            # 解析任务
            steps.append("解析任务")
            task = self._parse_task(task_description)
            logger.info(f"任务解析: {task.type.value}, 参数: {task.params}")
            
            # 执行任务
            steps.append(f"执行{task.type.value}任务")
            result_data = await self._execute_task(task)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return AgentResult(
                success=True,
                task_id=task.id,
                task_type=task.type.value,
                data=result_data,
                execution_time=execution_time,
                steps=steps
            )
            
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResult(
                success=False,
                task_id=self._generate_task_id(),
                task_type="error",
                error=str(e),
                execution_time=execution_time,
                steps=steps
            )
    
    async def _execute_task(self, task: AgentTask) -> Any:
        """执行具体任务"""
        if task.type == TaskType.BROWSE:
            url = task.params.get("url", "https://www.eastmoney.com")
            return await self._tool_navigate(url)
        
        elif task.type == TaskType.GET_STOCK_INFO:
            code = task.params.get("stock_code", "000001")
            return await self._tool_get_stock_price(code)
        
        elif task.type == TaskType.ANALYZE_MARKET:
            return await self._tool_analyze_market()
        
        elif task.type == TaskType.MCP_CALL:
            tool_name = task.params.get("tool_name", "market.status")
            args = task.params.get("arguments", {})
            return await self._tool_mcp_call(tool_name, args)
        
        else:
            # 默认分析市场
            return await self._tool_analyze_market()
    
    # ==================== 工具实现 ====================
    
    async def _tool_navigate(self, url: str) -> Dict:
        """导航工具"""
        browser = await self._ensure_browser()
        result = await browser.navigate(url)
        return result.to_dict()
    
    async def _tool_screenshot(self, path: str = None) -> Dict:
        """截图工具"""
        browser = await self._ensure_browser()
        result = await browser.screenshot(path)
        return result.to_dict()
    
    async def _tool_get_content(self) -> Dict:
        """获取内容工具"""
        browser = await self._ensure_browser()
        result = await browser.get_content()
        return result.to_dict()
    
    async def _tool_get_stock_price(self, code: str) -> Dict:
        """获取股价工具"""
        browser = await self._ensure_browser()
        result = await browser.get_stock_price(code)
        return result.to_dict()
    
    async def _tool_analyze_market(self) -> Dict:
        """分析市场工具"""
        result = {
            "source": "mcp",
            "market_status": None,
            "sentiment": None
        }
        
        # 尝试调用MCP获取市场状态
        mcp = await self._ensure_mcp_client()
        if mcp:
            try:
                mcp_result = mcp.call("market.status", {"index": "000300.XSHG"})
                if mcp_result.success:
                    result["market_status"] = mcp_result.data
            except Exception as e:
                logger.warning(f"MCP调用失败: {e}")
        
        return result
    
    async def _tool_mcp_call(self, tool_name: str, arguments: Dict = None) -> Dict:
        """MCP调用工具"""
        mcp = await self._ensure_mcp_client()
        if mcp is None:
            return {"success": False, "error": "MCP客户端不可用"}
        
        try:
            result = mcp.call(tool_name, arguments or {})
            return {"success": result.success, "data": result.data, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_tools(self) -> List[Dict]:
        """列出可用工具"""
        return [{"name": name} for name in self._tools.keys()]
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        直接调用工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
        
        Returns:
            工具执行结果
        """
        if tool_name not in self._tools:
            raise ValueError(f"未知工具: {tool_name}")
        
        return await self._tools[tool_name](**kwargs)
    
    async def cleanup(self):
        """清理资源"""
        if self._browser:
            await self._browser.cleanup()
            self._browser = None
        logger.info("✅ Agent资源已清理")
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
