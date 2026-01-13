# -*- coding: utf-8 -*-
"""
OpenManus工作流集成
==================
将OpenManus Agent集成到韬睿量化工作流系统

功能:
1. R0数据源检测增强 - 使用Agent验证外部数据源
2. R1市场趋势分析增强 - 集成新闻情绪分析
3. 自动化研究流程中的数据收集步骤

使用方式:
    from core.workflow.openmanus_integration import WorkflowEnhancer
    
    enhancer = WorkflowEnhancer()
    result = await enhancer.enhance_r0_data_source()
    result = await enhancer.enhance_r1_market_trend()
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging

# 配置日志
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 导入Core模块
from core.automation import OpenManusAgent, BrowserAgent, RequestCache, get_global_cache
from core.data_collection import FinancialCollector

# 导入浏览器Agent（用于R4增强）
try:
    from core.automation.browser_agent import BrowserAgent as CoreBrowserAgent
except ImportError:
    CoreBrowserAgent = None


@dataclass
class EnhancementResult:
    """增强结果"""
    success: bool
    step_id: str
    step_name: str
    data: Any = None
    error: Optional[str] = None
    enhancement_source: str = "openmanus"
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "step_id": self.step_id,
            "step_name": self.step_name,
            "data": self.data,
            "error": self.error,
            "enhancement_source": self.enhancement_source,
            "execution_time": self.execution_time
        }


class WorkflowEnhancer:
    """
    工作流增强器
    
    使用OpenManus Agent增强TRQuant工作流的各个步骤
    
    Attributes:
        headless: 浏览器是否使用无头模式
        use_cache: 是否使用缓存
    """
    
    def __init__(self, headless: bool = True, use_cache: bool = True):
        """
        初始化增强器
        
        Args:
            headless: 浏览器是否使用无头模式
            use_cache: 是否使用缓存
        """
        self.headless = headless
        self.use_cache = use_cache
        self._agent: Optional[OpenManusAgent] = None
        self._collector: Optional[FinancialCollector] = None
        self._browser_agent = None
        self._cache = get_global_cache() if use_cache else None
    
    async def _ensure_agent(self) -> OpenManusAgent:
        """确保Agent已初始化"""
        if self._agent is None:
            self._agent = OpenManusAgent(headless=self.headless)
        return self._agent
    
    async def _ensure_collector(self) -> FinancialCollector:
        """确保收集器已初始化"""
        if self._collector is None:
            self._collector = FinancialCollector(headless=self.headless)
        return self._collector
    
    async def enhance_r0_data_source(self) -> EnhancementResult:
        """
        增强R0数据源检测
        
        使用浏览器工具验证外部数据源的可访问性
        
        Returns:
            EnhancementResult: 增强结果
        """
        start_time = datetime.now()
        
        try:
            agent = await self._ensure_agent()
            
            # 检查主要财经网站
            data_sources = [
                {"name": "东方财富", "url": "https://www.eastmoney.com"},
                {"name": "新浪财经", "url": "https://finance.sina.com.cn"},
                {"name": "同花顺", "url": "https://www.10jqka.com.cn"}
            ]
            
            results = []
            for source in data_sources:
                cache_key = f"r0_source_{source['name']}"
                
                # 检查缓存
                if self._cache:
                    cached = self._cache.get(cache_key)
                    if cached:
                        results.append(cached)
                        continue
                
                # 访问网站
                try:
                    nav_result = await agent.call_tool("browser.navigate", url=source["url"])
                    source_result = {
                        "name": source["name"],
                        "url": source["url"],
                        "accessible": nav_result.get("success", False),
                        "error": nav_result.get("error")
                    }
                except Exception as e:
                    source_result = {
                        "name": source["name"],
                        "url": source["url"],
                        "accessible": False,
                        "error": str(e)
                    }
                
                results.append(source_result)
                
                # 存入缓存
                if self._cache and source_result["accessible"]:
                    self._cache.set(cache_key, source_result, ttl=3600)  # 1小时缓存
            
            # 汇总结果
            accessible_count = sum(1 for r in results if r["accessible"])
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return EnhancementResult(
                success=accessible_count > 0,
                step_id="R0",
                step_name="数据源检测",
                data={
                    "sources": results,
                    "accessible_count": accessible_count,
                    "total_count": len(results)
                },
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"R0增强失败: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            return EnhancementResult(
                success=False,
                step_id="R0",
                step_name="数据源检测",
                error=str(e),
                execution_time=execution_time
            )
    
    async def enhance_r1_market_trend(self, index_code: str = "000300.XSHG", as_of_date: str = None) -> EnhancementResult:
        """
        增强R1市场趋势分析
        
        使用MarketTrendAnalyzer（多周期共振+HMM）进行市场趋势分析
        基线实现：TrendAnalyzer + SimpleHMM (已回测验证)
        周期口径：周/月/季 = 5/21/63 交易日
        权重：Trend 0.8 + HMM 0.2
        
        Args:
            index_code: 指数代码（默认沪深300）
            as_of_date: 分析日期（默认今天）
        
        Returns:
            EnhancementResult: 增强结果
        """
        start_time = datetime.now()
        
        try:
            from core.market_trend_analyzer import MarketTrendAnalyzer, MarketTrendAnalyzerConfig
            from datetime import datetime as dt
            
            # 使用MarketTrendAnalyzer进行分析
            config = MarketTrendAnalyzerConfig()
            analyzer = MarketTrendAnalyzer(config)
            
            # 确定分析日期
            if as_of_date is None:
                as_of_date = dt.now().strftime("%Y-%m-%d")
            
            # 执行多周期共振+HMM分析
            signal = analyzer.analyze(index_code, as_of_date)
            
            if signal is None:
                raise Exception(f"MarketTrendAnalyzer返回空结果: {index_code} @ {as_of_date}")
            
            # 使用to_dict()方法获取完整数据
            signal_dict = signal.to_dict()
            
            # 提取关键信息
            trend_data = {
                "index_code": index_code,
                "as_of_date": as_of_date,
                # 综合评分
                "ensemble_score": signal.ensemble_score,
                "ensemble_direction": signal.ensemble_direction.value if signal.ensemble_direction else "震荡盘整",
                "ensemble_confidence": signal.ensemble_confidence,
                # HMM状态（从hmm_signal中提取）
                "hmm_state": signal_dict.get("hmm_state"),
                "hmm_confidence": signal.hmm_signal.confidence if signal.hmm_signal else None,
                # 多周期共振信息
                "period_signals": {},
                # 共振阶段
                "resonance_phase": signal.resonance_phase.value if signal.resonance_phase else None,
                "resonance_phase_name": signal.resonance_phase.name if signal.resonance_phase else None,
                # 市场阶段
                "market_phase": signal_dict.get("market_phase"),
                "market_phase_name": signal_dict.get("market_phase_name"),
                "market_phase_position": signal.market_phase_position,
                # 仓位和策略
                "position_cap": signal.position_cap,
                "strategy_mode": signal.strategy_mode.value if signal.strategy_mode else None,
                # 确认次数
                "confirm_streak": signal.confirm_streak
            }
            
            # 提取各周期信号
            if signal.period_signals:
                for period, period_signal in signal.period_signals.items():
                    if period_signal:
                        trend_data["period_signals"][period] = {
                            "score": period_signal.score,
                            "direction": period_signal.direction.value if period_signal.direction else None,
                            "confidence": period_signal.confidence
                        }
            
            # 提取市场开关信息（多指数共振）
            if signal.market_switch:
                trend_data["market_switch"] = {
                    "position_cap": signal.market_switch.position_cap,
                    "strategy_mode": signal.market_switch.strategy_mode.value if signal.market_switch.strategy_mode else None,
                    "resonance_phase": signal.market_switch.resonance_phase.value if signal.market_switch.resonance_phase else None
                }
            
            # 生成趋势标签
            trend_label = "neutral"
            if signal.ensemble_score > 30:
                trend_label = "bullish"
            elif signal.ensemble_score < -30:
                trend_label = "bearish"
            else:
                trend_label = "neutral"
            
            trend_data["trend_label"] = trend_label
            
            # 添加完整信号字典（用于详细分析）
            trend_data["full_signal"] = signal_dict
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return EnhancementResult(
                success=True,
                step_id="R1",
                step_name="市场趋势分析",
                data=trend_data,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"R1增强失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            execution_time = (datetime.now() - start_time).total_seconds()
            return EnhancementResult(
                success=False,
                step_id="R1",
                step_name="市场趋势分析",
                error=str(e),
                execution_time=execution_time
            )
    
    async def enhance_r2_mainline(self, keywords: List[str] = None) -> EnhancementResult:
        """
        增强R2主线轮动研究
        
        使用网络数据收集来识别当前市场热点主线
        
        Args:
            keywords: 搜索关键词列表
        
        Returns:
            EnhancementResult: 增强结果
        """
        start_time = datetime.now()
        
        try:
            collector = await self._ensure_collector()
            
            # 获取财经新闻
            news_result = await collector.fetch_news("eastmoney", limit=20)
            
            if not news_result.success:
                raise Exception(news_result.error)
            
            # 分析热点关键词
            keyword_counts = {}
            hot_keywords = keywords or ["AI", "新能源", "半导体", "消费", "医药", "金融", "科技", 
                                       "人工智能", "芯片", "光伏", "锂电池", "新能源汽车", "5G", 
                                       "云计算", "大数据", "物联网", "区块链"]
            
            for news in news_result.data:
                title = news.get("title", "")
                content = news.get("content", "")
                text = f"{title} {content}".lower()
                
                for kw in hot_keywords:
                    if kw.lower() in text:
                        keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
            
            # 排序获取热点
            sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
            
            # 计算热度得分
            max_count = max(keyword_counts.values()) if keyword_counts else 1
            hot_topics = [
                {"keyword": kw, "count": count, "score": round(count / max_count * 100, 1)}
                for kw, count in sorted_keywords[:10]
            ]
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return EnhancementResult(
                success=True,
                step_id="R2",
                step_name="主线轮动研究",
                data={
                    "hot_topics": hot_topics[:5],
                    "top10_topics": hot_topics,
                    "news_count": len(news_result.data),
                    "keyword_analysis": keyword_counts,
                    "data_source": "eastmoney"
                },
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"R2增强失败: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            return EnhancementResult(
                success=False,
                step_id="R2",
                step_name="主线轮动研究",
                error=str(e),
                execution_time=execution_time
            )
    
    async def enhance_r4_investment_selection(self, stock_codes: List[str] = None) -> EnhancementResult:
        """
        增强R4投资标的筛选
        
        使用浏览器工具获取股票价格和基本信息
        
        Args:
            stock_codes: 股票代码列表（可选）
        
        Returns:
            EnhancementResult: 增强结果
        """
        start_time = datetime.now()
        
        try:
            # 确保浏览器工具已初始化
            if not hasattr(self, '_browser_agent') or self._browser_agent is None:
                from core.automation import BrowserAgent
                self._browser_agent = BrowserAgent(headless=self.headless)
            
            browser = self._browser_agent
            
            # 如果没有提供股票代码，使用默认的几只股票
            if stock_codes is None:
                stock_codes = ["000001", "600000", "000002", "600036", "000858"]
            
            stock_data = []
            for code in stock_codes[:10]:  # 限制数量
                try:
                    price_result = await browser.get_stock_price(code, source="eastmoney")
                    if price_result.success:
                        stock_data.append({
                            "code": code,
                            **price_result.data
                        })
                except Exception as e:
                    logger.warning(f"获取股票 {code} 价格失败: {e}")
                    continue
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return EnhancementResult(
                success=len(stock_data) > 0,
                step_id="R4",
                step_name="投资标的筛选",
                data={
                    "stocks": stock_data,
                    "count": len(stock_data),
                    "data_source": "eastmoney"
                },
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"R4增强失败: {e}")
            execution_time = (datetime.now() - start_time).total_seconds()
            return EnhancementResult(
                success=False,
                step_id="R4",
                step_name="投资标的筛选",
                error=str(e),
                execution_time=execution_time
            )
    
    async def enhance_all_research_steps(self) -> List[EnhancementResult]:
        """
        增强所有研究阶段步骤
        
        Returns:
            List[EnhancementResult]: 增强结果列表
        """
        results = []
        
        # R0 数据源检测
        r0_result = await self.enhance_r0_data_source()
        results.append(r0_result)
        
        # R1 市场趋势分析（使用MarketTrendAnalyzer - 多周期共振+HMM）
        r1_result = await self.enhance_r1_market_trend()
        results.append(r1_result)
        
        # R2 主线轮动研究
        r2_result = await self.enhance_r2_mainline()
        results.append(r2_result)
        
        # R4 投资标的筛选（可选）
        # r4_result = await self.enhance_r4_investment_selection()
        # results.append(r4_result)
        
        return results
    
    async def cleanup(self):
        """清理资源"""
        if self._agent:
            await self._agent.cleanup()
            self._agent = None
        
        if self._collector:
            await self._collector.cleanup()
            self._collector = None
        
        if self._browser_agent:
            await self._browser_agent.cleanup()
            self._browser_agent = None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()


# ==================== 便捷函数 ====================

async def enhance_workflow_step(step_id: str, **kwargs) -> EnhancementResult:
    """
    增强指定的工作流步骤
    
    Args:
        step_id: 步骤ID (R0, R1, R2, ...)
        **kwargs: 额外参数
    
    Returns:
        EnhancementResult: 增强结果
    """
    async with WorkflowEnhancer() as enhancer:
        if step_id == "R0":
            return await enhancer.enhance_r0_data_source()
        elif step_id == "R1":
            return await enhancer.enhance_r1_market_trend()
        elif step_id == "R2":
            return await enhancer.enhance_r2_mainline(**kwargs)
        else:
            return EnhancementResult(
                success=False,
                step_id=step_id,
                step_name="Unknown",
                error=f"不支持的步骤: {step_id}"
            )
