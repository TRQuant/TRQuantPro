#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant OpenManus集成功能演示
===========================
演示TRQuant中封装的OpenManus功能

功能列表:
1. BrowserAgent - 浏览器自动化（封装BrowserUseTool）
2. OpenManusAgent - OpenManus Agent封装（简化版）
3. FinancialCollector - 财经数据收集（使用BrowserAgent）
4. WorkflowEnhancer - 工作流增强（R0/R1/R2增强）

作者: TRQuant Team
日期: 2026-01-11
"""

import sys
import asyncio
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


async def demo_browser_agent():
    """演示BrowserAgent功能"""
    print("\n" + "=" * 70)
    print("1. BrowserAgent - 浏览器自动化（TRQuant封装）")
    print("=" * 70)
    
    try:
        from core.automation import BrowserAgent
        
        print("\n📋 功能:")
        print("  - navigate: 访问网页")
        print("  - get_content: 获取页面内容")
        print("  - get_text: 获取元素文本")
        print("  - screenshot: 截图")
        print("  - get_stock_price: 获取股票价格（东方财富）")
        
        print("\n🔧 使用示例:")
        print("""
from core.automation import BrowserAgent

async with BrowserAgent(headless=True) as agent:
    # 访问网页
    result = await agent.navigate("https://www.eastmoney.com")
    if result.success:
        print("页面加载成功")
    
    # 获取页面内容
    content_result = await agent.get_content()
    if content_result.success:
        print(f"页面内容: {content_result.data['content'][:100]}")
        """)
        
        print("\n✅ BrowserAgent已可用")
        print("   位置: core/automation/browser_agent.py")
        
    except Exception as e:
        print(f"❌ BrowserAgent加载失败: {e}")


async def demo_openmanus_agent():
    """演示OpenManusAgent功能"""
    print("\n" + "=" * 70)
    print("2. OpenManusAgent - OpenManus Agent封装（TRQuant简化版）")
    print("=" * 70)
    
    try:
        from core.automation import OpenManusAgent
        
        print("\n📋 功能:")
        print("  - 任务解析和执行")
        print("  - 工具调用（browser, collector等）")
        print("  - 简化的Agent实现（不使用LLM推理）")
        print("  - 直接工具调用")
        
        print("\n🔧 使用示例:")
        print("""
from core.automation import OpenManusAgent

async with OpenManusAgent(headless=True) as agent:
    # 调用工具
    result = await agent.call_tool("browser.navigate", url="https://www.eastmoney.com")
    if result.get("success"):
        print("工具调用成功")
        """)
        
        print("\n✅ OpenManusAgent已可用")
        print("   位置: core/automation/openmanus_agent.py")
        print("   注意: 这是简化版，不使用LLM推理，直接调用工具")
        
    except Exception as e:
        print(f"❌ OpenManusAgent加载失败: {e}")


async def demo_financial_collector():
    """演示FinancialCollector功能"""
    print("\n" + "=" * 70)
    print("3. FinancialCollector - 财经数据收集（使用BrowserAgent）")
    print("=" * 70)
    
    try:
        from core.data_collection import FinancialCollector
        
        print("\n📋 功能:")
        print("  - fetch_news: 获取财经新闻（东方财富）")
        print("  - fetch_announcements: 获取公告（东方财富）")
        print("  - fetch_market_news: 获取市场新闻（关键词搜索）")
        print("  - MongoDB存储支持")
        
        print("\n🔧 使用示例:")
        print("""
from core.data_collection import FinancialCollector

async with FinancialCollector(headless=True) as collector:
    # 获取财经新闻
    news_result = await collector.fetch_news("eastmoney", limit=10)
    if news_result.success:
        print(f"获取到 {len(news_result.data)} 条新闻")
        for news in news_result.data[:3]:
            print(f"  - {news.get('title', 'N/A')}")
        """)
        
        print("\n✅ FinancialCollector已可用")
        print("   位置: core/data_collection/financial_collector.py")
        
    except Exception as e:
        print(f"❌ FinancialCollector加载失败: {e}")


async def demo_workflow_enhancer():
    """演示WorkflowEnhancer功能"""
    print("\n" + "=" * 70)
    print("4. WorkflowEnhancer - 工作流增强（R0/R1/R2增强）")
    print("=" * 70)
    
    try:
        from core.workflow import WorkflowEnhancer
        
        print("\n📋 功能:")
        print("  - enhance_r0_data_source: R0数据源检测增强")
        print("  - enhance_r1_market_trend: R1市场趋势分析增强（使用MarketTrendAnalyzer）")
        print("  - enhance_r2_mainline: R2主线轮动研究增强")
        print("  - enhance_r4_investment_selection: R4投资标的筛选增强（可选）")
        
        print("\n🔧 使用示例:")
        print("""
from core.workflow import WorkflowEnhancer

async with WorkflowEnhancer(headless=True) as enhancer:
    # R0数据源检测
    r0 = await enhancer.enhance_r0_data_source()
    print(f"数据源可访问: {r0.data['accessible_count']}/{r0.data['total_count']}")
    
    # R1市场趋势分析（使用MarketTrendAnalyzer - 多周期共振+HMM）
    r1 = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
    if r1.success:
        print(f"市场趋势: {r1.data.get('trend_label', 'N/A')}")
        print(f"HMM状态: {r1.data.get('hmm_state', 'N/A')}")
        print(f"共振阶段: {r1.data.get('resonance_phase', 'N/A')}")
    
    # R2主线轮动研究
    r2 = await enhancer.enhance_r2_mainline()
    if r2.success:
        hot_topics = r2.data.get('hot_topics', [])
        print(f"热点主题: {[t['keyword'] for t in hot_topics]}")
        """)
        
        print("\n✅ WorkflowEnhancer已可用")
        print("   位置: core/workflow/openmanus_integration.py")
        print("   注意: R1使用MarketTrendAnalyzer（多周期共振+HMM）")
        
    except Exception as e:
        print(f"❌ WorkflowEnhancer加载失败: {e}")


async def demo_actual_usage():
    """演示实际使用（可选）"""
    print("\n" + "=" * 70)
    print("5. 实际使用演示（可选，需要网络连接）")
    print("=" * 70)
    
    print("\n📋 可选的演示:")
    print("  - BrowserAgent访问网页（需要网络）")
    print("  - FinancialCollector获取新闻（需要网络）")
    print("  - WorkflowEnhancer增强工作流（需要网络和数据源）")
    
    print("\n🔧 运行实际演示:")
    print("""
# 取消注释以下代码运行实际演示

# async with BrowserAgent(headless=True) as agent:
#     result = await agent.navigate("https://www.eastmoney.com")
#     print(f"访问结果: {result.success}")

# async with FinancialCollector(headless=True) as collector:
#     news_result = await collector.fetch_news("eastmoney", limit=5)
#     if news_result.success:
#         print(f"获取到 {len(news_result.data)} 条新闻")
        """)
    
    print("\n⚠️  注意: 实际演示需要网络连接，这里仅展示代码示例")


async def main():
    """主函数"""
    print("=" * 70)
    print("TRQuant OpenManus集成功能演示")
    print("=" * 70)
    print("\n本演示将展示TRQuant中封装的OpenManus功能")
    print("这些功能是OpenManus工具的封装，提供统一的API接口")
    
    # 演示各个功能
    await demo_browser_agent()
    await demo_openmanus_agent()
    await demo_financial_collector()
    await demo_workflow_enhancer()
    await demo_actual_usage()
    
    print("\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n📚 相关文档:")
    print("  - 集成完成报告: docs/research/OPENMANUS_INTEGRATION_COMPLETE.md")
    print("  - 集成增强报告: docs/research/OPENMANUS_INTEGRATION_ENHANCED.md")
    print("  - 知识库总结: docs/research/OPENMANUS_KB_SUMMARY.md")
    print("\n💡 提示:")
    print("  - TRQuant封装了OpenManus功能，提供统一的API")
    print("  - 无需LLM API即可使用浏览器自动化等功能")
    print("  - 工作流增强功能已集成到9步工作流中")


if __name__ == "__main__":
    asyncio.run(main())
