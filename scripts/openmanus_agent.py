#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus Agent
===============
韬睿量化系统的智能Agent，整合浏览器工具和数据收集功能

功能:
1. Agent主类 - 任务解析和执行
2. 工具注册 - 浏览器、数据收集
3. MCP客户端集成 - 调用TRQuant工具
4. 任务执行引擎

使用方式:
    agent = OpenManusAgent()
    result = await agent.execute("获取最新财经新闻并分析市场情绪")

作者: TRQuant Team
日期: 2026-01-11
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
import json
import re

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 项目路径配置
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

# 导入工具
from openmanus_browser_tool import OpenManusBrowserTool, BrowserResult
from openmanus_data_collector import DataCollector, CollectorResult


class TaskType(Enum):
    """任务类型"""
    BROWSE = "browse"           # 浏览网页
    FETCH_NEWS = "fetch_news"   # 抓取新闻
    FETCH_ANNOUNCEMENT = "fetch_announcement"  # 抓取公告
    ANALYZE_MARKET = "analyze_market"  # 分析市场
    GET_STOCK_INFO = "get_stock_info"  # 获取股票信息
    SEARCH = "search"           # 搜索
    UNKNOWN = "unknown"         # 未知


@dataclass
class AgentTask:
    """Agent任务"""
    id: str
    type: TaskType
    description: str
    params: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "description": self.description,
            "params": self.params,
            "created_at": self.created_at
        }


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
    OpenManus Agent
    
    智能Agent，整合浏览器工具、数据收集和MCP客户端
    """
    
    def __init__(self, headless: bool = True):
        """
        初始化Agent
        
        Args:
            headless: 浏览器是否使用无头模式
        """
        self.headless = headless
        self._browser = None
        self._collector = None
        self._mcp_client = None
        self._task_counter = 0
        
        # 关键词映射（用于任务类型识别）
        self._task_keywords = {
            TaskType.BROWSE: ["访问", "打开", "浏览", "查看网页", "navigate", "browse", "visit"],
            TaskType.FETCH_NEWS: ["新闻", "资讯", "快讯", "消息", "news", "财经新闻"],
            TaskType.FETCH_ANNOUNCEMENT: ["公告", "announcement", "披露", "报告"],
            TaskType.ANALYZE_MARKET: ["分析", "市场", "趋势", "情绪", "行情", "analyze", "market"],
            TaskType.GET_STOCK_INFO: ["股票", "股价", "行情", "stock", "price", "quote"],
            TaskType.SEARCH: ["搜索", "查找", "search", "find"]
        }
        
        # 注册工具
        self._tools: Dict[str, Callable] = {}
        self._register_tools()
    
    def _register_tools(self):
        """注册可用工具"""
        self._tools = {
            "browser.navigate": self._tool_browser_navigate,
            "browser.screenshot": self._tool_browser_screenshot,
            "browser.get_content": self._tool_browser_get_content,
            "collector.fetch_news": self._tool_fetch_news,
            "collector.fetch_announcements": self._tool_fetch_announcements,
            "collector.fetch_market_news": self._tool_fetch_market_news,
            "stock.get_price": self._tool_get_stock_price,
            "stock.search": self._tool_search_stock,
            "mcp.call": self._tool_mcp_call
        }
        logger.info(f"已注册 {len(self._tools)} 个工具")
    
    async def _ensure_browser(self) -> OpenManusBrowserTool:
        """确保浏览器工具已初始化"""
        if self._browser is None:
            self._browser = OpenManusBrowserTool(headless=self.headless)
        return self._browser
    
    async def _ensure_collector(self) -> DataCollector:
        """确保数据收集器已初始化"""
        if self._collector is None:
            self._collector = DataCollector(headless=self.headless)
        return self._collector
    
    async def _ensure_mcp_client(self):
        """确保MCP客户端已初始化"""
        if self._mcp_client is None:
            try:
                from core.mcp.client import MCPClient
                self._mcp_client = MCPClient(project_root=PROJECT_ROOT, python_path=sys.executable)
                logger.info("✅ MCP客户端已初始化")
            except ImportError:
                logger.warning("MCP客户端不可用")
        return self._mcp_client
    
    def _generate_task_id(self) -> str:
        """生成任务ID"""
        self._task_counter += 1
        return f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{self._task_counter:04d}"
    
    def _parse_task(self, task_description: str) -> AgentTask:
        """
        解析任务描述
        
        Args:
            task_description: 任务描述文本
        
        Returns:
            AgentTask: 解析后的任务对象
        """
        task_id = self._generate_task_id()
        task_type = TaskType.UNKNOWN
        params = {}
        
        # 小写化处理
        desc_lower = task_description.lower()
        
        # 识别任务类型
        for t_type, keywords in self._task_keywords.items():
            if any(kw in desc_lower for kw in keywords):
                task_type = t_type
                break
        
        # 提取参数
        # URL提取
        url_match = re.search(r'https?://[^\s]+', task_description)
        if url_match:
            params["url"] = url_match.group()
        
        # 股票代码提取
        stock_match = re.search(r'(\d{6})', task_description)
        if stock_match:
            params["stock_code"] = stock_match.group(1)
        
        # 数量提取
        limit_match = re.search(r'(\d+)\s*(条|个|篇)', task_description)
        if limit_match:
            params["limit"] = int(limit_match.group(1))
        
        return AgentTask(
            id=task_id,
            type=task_type,
            description=task_description,
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
            # 1. 解析任务
            steps.append("解析任务")
            task = self._parse_task(task_description)
            logger.info(f"任务解析: {task.type.value}, 参数: {task.params}")
            
            # 2. 执行任务
            steps.append(f"执行{task.type.value}任务")
            result_data = await self._execute_task(task)
            
            # 3. 计算执行时间
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
            return await self._tool_browser_navigate(task.params.get("url", "https://www.eastmoney.com"))
        
        elif task.type == TaskType.FETCH_NEWS:
            return await self._tool_fetch_news(
                source=task.params.get("source", "eastmoney"),
                limit=task.params.get("limit", 10)
            )
        
        elif task.type == TaskType.FETCH_ANNOUNCEMENT:
            stock_code = task.params.get("stock_code", "000001")
            return await self._tool_fetch_announcements(
                stock_code=stock_code,
                limit=task.params.get("limit", 10)
            )
        
        elif task.type == TaskType.ANALYZE_MARKET:
            return await self._analyze_market(task.params)
        
        elif task.type == TaskType.GET_STOCK_INFO:
            stock_code = task.params.get("stock_code", "000001")
            return await self._tool_get_stock_price(stock_code)
        
        elif task.type == TaskType.SEARCH:
            query = task.params.get("query", task.description)
            return await self._tool_search_stock(query)
        
        else:
            # 默认尝试获取市场新闻
            return await self._tool_fetch_market_news(limit=10)
    
    # ==================== 工具实现 ====================
    
    async def _tool_browser_navigate(self, url: str) -> Dict:
        """浏览器导航工具"""
        browser = await self._ensure_browser()
        result = await browser.navigate(url)
        return result.to_dict()
    
    async def _tool_browser_screenshot(self, path: str = None) -> Dict:
        """浏览器截图工具"""
        browser = await self._ensure_browser()
        result = await browser.screenshot(path)
        return result.to_dict()
    
    async def _tool_browser_get_content(self) -> Dict:
        """获取页面内容工具"""
        browser = await self._ensure_browser()
        result = await browser.get_page_content()
        return result.to_dict()
    
    async def _tool_fetch_news(self, source: str = "eastmoney", limit: int = 10) -> Dict:
        """抓取新闻工具"""
        collector = await self._ensure_collector()
        result = await collector.fetch_news(source, limit)
        return result.to_dict()
    
    async def _tool_fetch_announcements(self, stock_code: str, limit: int = 10) -> Dict:
        """抓取公告工具"""
        collector = await self._ensure_collector()
        result = await collector.fetch_announcements(stock_code, limit=limit)
        return result.to_dict()
    
    async def _tool_fetch_market_news(self, limit: int = 20) -> Dict:
        """抓取市场综合新闻工具"""
        collector = await self._ensure_collector()
        result = await collector.fetch_market_news(limit)
        return result.to_dict()
    
    async def _tool_get_stock_price(self, stock_code: str) -> Dict:
        """获取股票价格工具"""
        browser = await self._ensure_browser()
        result = await browser.extract_stock_price(stock_code)
        return result.to_dict()
    
    async def _tool_search_stock(self, query: str) -> Dict:
        """搜索股票工具"""
        browser = await self._ensure_browser()
        result = await browser.search_stock(query)
        return result.to_dict()
    
    async def _tool_mcp_call(self, tool_name: str, arguments: Dict) -> Dict:
        """调用MCP工具"""
        mcp = await self._ensure_mcp_client()
        if mcp is None:
            return {"success": False, "error": "MCP客户端不可用"}
        
        try:
            result = await mcp.call(tool_name, arguments)
            return {"success": result.success, "data": result.data, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _analyze_market(self, params: Dict) -> Dict:
        """分析市场"""
        # 1. 获取市场新闻
        collector = await self._ensure_collector()
        news_result = await collector.fetch_market_news(limit=20)
        
        # 2. 简单的情绪分析
        sentiment = self._simple_sentiment_analysis(news_result.data if news_result.success else [])
        
        # 3. 尝试调用MCP获取市场状态
        market_status = None
        mcp = await self._ensure_mcp_client()
        if mcp:
            try:
                from core.mcp.client import MCPClient
                result = await mcp.call("market.status", {"index": "000300.XSHG"})
                if result.success:
                    market_status = result.data
            except:
                pass
        
        return {
            "news_count": len(news_result.data) if news_result.success else 0,
            "sentiment": sentiment,
            "market_status": market_status,
            "news_sample": news_result.data[:5] if news_result.success else []
        }
    
    def _simple_sentiment_analysis(self, news_list: List[Dict]) -> Dict:
        """
        简单的情绪分析
        
        基于关键词进行情绪判断
        """
        positive_keywords = ["涨", "上涨", "突破", "利好", "上升", "增长", "牛市", "反弹", "创新高"]
        negative_keywords = ["跌", "下跌", "暴跌", "利空", "下降", "下滑", "熊市", "回调", "创新低"]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for news in news_list:
            title = news.get("title", "")
            
            has_positive = any(kw in title for kw in positive_keywords)
            has_negative = any(kw in title for kw in negative_keywords)
            
            if has_positive and not has_negative:
                positive_count += 1
            elif has_negative and not has_positive:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = len(news_list) or 1
        
        # 计算情绪得分 (-1 到 1)
        score = (positive_count - negative_count) / total
        
        # 确定情绪标签
        if score > 0.2:
            label = "乐观"
        elif score < -0.2:
            label = "悲观"
        else:
            label = "中性"
        
        return {
            "label": label,
            "score": round(score, 3),
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "total": total
        }
    
    def list_tools(self) -> List[Dict]:
        """列出可用工具"""
        return [
            {"name": name, "description": f"Tool: {name}"} 
            for name in self._tools.keys()
        ]
    
    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """
        调用指定工具
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
        
        Returns:
            工具执行结果
        """
        if tool_name not in self._tools:
            raise ValueError(f"未知工具: {tool_name}")
        
        tool_func = self._tools[tool_name]
        return await tool_func(**kwargs)
    
    async def cleanup(self):
        """清理资源"""
        if self._browser:
            await self._browser.cleanup()
            self._browser = None
        
        if self._collector:
            await self._collector.cleanup()
            self._collector = None
        
        logger.info("✅ Agent资源已清理")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.cleanup()


# ==================== 测试函数 ====================

async def test_agent():
    """测试Agent"""
    print("=" * 80)
    print("OpenManus Agent 测试")
    print("=" * 80)
    
    async with OpenManusAgent(headless=True) as agent:
        # 测试1: 列出可用工具
        print("\n测试1: 列出可用工具")
        tools = agent.list_tools()
        for tool in tools:
            print(f"  - {tool['name']}")
        
        # 测试2: 执行任务 - 获取新闻
        print("\n测试2: 执行任务 - 获取财经新闻")
        result = await agent.execute("获取最新5条财经新闻")
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        print(f"  任务类型: {result.task_type}")
        print(f"  执行时间: {result.execution_time:.2f}秒")
        if result.success and result.data:
            data = result.data
            print(f"  新闻数量: {data.get('count', 0)}")
        
        # 测试3: 执行任务 - 分析市场
        print("\n测试3: 执行任务 - 分析市场情绪")
        result = await agent.execute("分析当前市场情绪")
        print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
        if result.success and result.data:
            sentiment = result.data.get("sentiment", {})
            print(f"  市场情绪: {sentiment.get('label', 'N/A')}")
            print(f"  情绪得分: {sentiment.get('score', 'N/A')}")
        
        # 测试4: 直接调用工具
        print("\n测试4: 直接调用工具 - 获取股票公告")
        try:
            result = await agent.call_tool("collector.fetch_announcements", stock_code="000001", limit=3)
            print(f"  状态: {'✅ 成功' if result.get('success') else '❌ 失败'}")
            print(f"  公告数量: {result.get('count', 0)}")
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n" + "=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_agent())
