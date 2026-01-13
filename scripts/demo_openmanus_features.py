#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus功能演示脚本
==================
演示OpenManus的各个功能模块

功能列表:
1. BrowserUseTool - 浏览器自动化
2. Bash - Shell命令执行
3. PythonExecute - Python代码执行
4. StrReplaceEditor - 代码编辑器
5. WebSearch - 网络搜索
6. MCP Server - MCP服务器工具
7. AskHuman - 询问用户（演示模式）
8. Terminate - 终止工具（演示模式）

作者: TRQuant Team
日期: 2026-01-11
"""

import sys
import asyncio
from pathlib import Path
from typing import Dict, Any

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"
sys.path.insert(0, str(OPENMANUS_DIR))
sys.path.insert(0, str(PROJECT_ROOT))


async def demo_browser_tool():
    """演示浏览器工具功能"""
    print("\n" + "=" * 70)
    print("1. BrowserUseTool - 浏览器自动化工具")
    print("=" * 70)
    
    try:
        from app.tool.browser_use_tool import BrowserUseTool
        
        tool = BrowserUseTool()
        
        print("\n📋 支持的操作:")
        print("  - go_to_url: 访问网页")
        print("  - click_element: 点击元素")
        print("  - input_text: 输入文本")
        print("  - extract_content: 提取内容（需要LLM API）")
        print("  - screenshot: 截图")
        print("  - scroll_down/scroll_up: 滚动")
        print("  - wait: 等待")
        print("  - go_back: 返回")
        print("  - refresh: 刷新")
        print("  - switch_tab/open_tab/close_tab: 标签管理")
        
        print("\n✅ BrowserUseTool已加载")
        print("   注意: 浏览器工具需要LLM API才能使用extract_content功能")
        print("   在TRQuant中，我们封装为BrowserAgent，提供统一的API")
        
        # 清理
        if hasattr(tool, 'cleanup'):
            await tool.cleanup()
            
    except Exception as e:
        print(f"❌ 浏览器工具加载失败: {e}")


async def demo_bash_tool():
    """演示Bash工具功能"""
    print("\n" + "=" * 70)
    print("2. Bash - Shell命令执行工具")
    print("=" * 70)
    
    try:
        from app.tool.bash import Bash
        
        tool = Bash()
        
        print("\n📋 功能:")
        print("  - 执行Shell命令")
        print("  - 捕获命令输出")
        print("  - 错误处理")
        
        print("\n🔧 演示: 执行简单命令")
        
        # 执行一个简单的命令（只演示，不实际执行）
        print("  命令: echo 'Hello OpenManus'")
        print("  功能: 执行Shell命令并返回输出")
        
        print("\n✅ Bash工具已加载")
        print("   注意: 在TRQuant中，可以直接使用Python的subprocess模块")
        
    except Exception as e:
        print(f"❌ Bash工具加载失败: {e}")


async def demo_python_execute_tool():
    """演示Python执行工具功能"""
    print("\n" + "=" * 70)
    print("3. PythonExecute - Python代码执行工具")
    print("=" * 70)
    
    try:
        from app.tool.python_execute import PythonExecute
        
        tool = PythonExecute()
        
        print("\n📋 功能:")
        print("  - 执行Python代码")
        print("  - 支持交互式执行")
        print("  - 结果捕获")
        print("  - 错误处理")
        
        print("\n🔧 演示: 执行Python代码")
        print("  代码: print('Hello from OpenManus')")
        print("  功能: 在隔离环境中执行Python代码")
        
        print("\n✅ PythonExecute工具已加载")
        print("   注意: 在TRQuant中，可以直接使用Python解释器")
        
    except Exception as e:
        print(f"❌ PythonExecute工具加载失败: {e}")


async def demo_editor_tool():
    """演示代码编辑器工具功能"""
    print("\n" + "=" * 70)
    print("4. StrReplaceEditor - 代码编辑器工具")
    print("=" * 70)
    
    try:
        from app.tool.str_replace_editor import StrReplaceEditor
        
        tool = StrReplaceEditor()
        
        print("\n📋 功能:")
        print("  - 文件编辑")
        print("  - 字符串替换")
        print("  - 代码修改")
        print("  - 多行替换")
        
        print("\n🔧 演示: 编辑文件")
        print("  操作: str_replace")
        print("  功能: 在文件中替换指定字符串")
        
        print("\n✅ StrReplaceEditor工具已加载")
        print("   注意: 在TRQuant中，可以直接使用文件操作")
        
    except Exception as e:
        print(f"❌ 编辑器工具加载失败: {e}")


async def demo_web_search_tool():
    """演示网络搜索工具功能"""
    print("\n" + "=" * 70)
    print("5. WebSearch - 网络搜索工具")
    print("=" * 70)
    
    try:
        from app.tool.web_search import WebSearch
        
        tool = WebSearch()
        
        print("\n📋 功能:")
        print("  - Google搜索")
        print("  - Bing搜索")
        print("  - 百度搜索")
        print("  - DuckDuckGo搜索")
        print("  - 搜索结果提取")
        
        print("\n🔧 演示: 网络搜索")
        print("  查询: 'OpenManus AI Agent'")
        print("  功能: 搜索网络并返回结果")
        
        print("\n✅ WebSearch工具已加载")
        print("   注意: 在TRQuant中，可以使用FinancialCollector进行财经数据搜索")
        
    except Exception as e:
        print(f"❌ WebSearch工具加载失败: {e}")


async def demo_mcp_server():
    """演示MCP服务器功能"""
    print("\n" + "=" * 70)
    print("6. MCP Server - MCP服务器工具")
    print("=" * 70)
    
    try:
        from app.mcp.server import MCPServer
        
        server = MCPServer()
        
        print("\n📋 注册的工具:")
        for tool_name, tool in server.tools.items():
            print(f"  - {tool_name}: {tool.name}")
        
        print("\n🔧 功能:")
        print("  - bash: Shell命令执行")
        print("  - browser: 浏览器自动化")
        print("  - editor: 代码编辑器")
        print("  - terminate: 终止工具")
        
        print("\n✅ MCP服务器已加载")
        print("   注意: MCP服务器已配置到Cursor的~/.cursor/mcp.json")
        print("   可以通过Cursor Chat直接调用这些工具")
        
    except Exception as e:
        print(f"❌ MCP服务器加载失败: {e}")


async def demo_ask_human_tool():
    """演示询问用户工具功能"""
    print("\n" + "=" * 70)
    print("7. AskHuman - 询问用户工具（演示模式）")
    print("=" * 70)
    
    try:
        from app.tool.ask_human import AskHuman
        
        tool = AskHuman()
        
        print("\n📋 功能:")
        print("  - 询问用户输入")
        print("  - 获取用户反馈")
        print("  - 交互式对话")
        
        print("\n🔧 演示: 询问用户")
        print("  问题: '请确认操作？'")
        print("  功能: 暂停执行，等待用户输入")
        
        print("\n✅ AskHuman工具已加载")
        print("   注意: 在自动化脚本中，可以使用默认值或跳过此步骤")
        
    except Exception as e:
        print(f"❌ AskHuman工具加载失败: {e}")


async def demo_terminate_tool():
    """演示终止工具功能"""
    print("\n" + "=" * 70)
    print("8. Terminate - 终止工具（演示模式）")
    print("=" * 70)
    
    try:
        from app.tool.terminate import Terminate
        
        tool = Terminate()
        
        print("\n📋 功能:")
        print("  - 终止Agent执行")
        print("  - 任务完成标记")
        print("  - 清理资源")
        
        print("\n🔧 演示: 终止执行")
        print("  功能: 标记任务完成，停止Agent循环")
        
        print("\n✅ Terminate工具已加载")
        print("   注意: 在Agent循环中，调用此工具会结束执行")
        
    except Exception as e:
        print(f"❌ Terminate工具加载失败: {e}")


async def demo_manus_agent():
    """演示Manus Agent功能"""
    print("\n" + "=" * 70)
    print("9. Manus Agent - 通用AI Agent（演示模式）")
    print("=" * 70)
    
    try:
        from app.agent.manus import Manus
        
        print("\n📋 功能:")
        print("  - 多工具支持（PythonExecute, BrowserUseTool等）")
        print("  - MCP工具集成")
        print("  - 浏览器上下文管理")
        print("  - 任务分解和执行")
        print("  - 思考循环（需要LLM API）")
        
        print("\n🔧 核心工具:")
        print("  - PythonExecute: Python代码执行")
        print("  - BrowserUseTool: 浏览器自动化")
        print("  - StrReplaceEditor: 代码编辑器")
        print("  - AskHuman: 询问用户")
        print("  - Terminate: 终止执行")
        
        print("\n✅ Manus Agent已加载")
        print("   注意: 完整功能需要LLM API")
        print("   在TRQuant中，我们封装为OpenManusAgent，简化了实现")
        
    except Exception as e:
        print(f"❌ Manus Agent加载失败: {e}")


async def demo_mcp_agent():
    """演示MCP Agent功能"""
    print("\n" + "=" * 70)
    print("10. MCP Agent - MCP服务器Agent（演示模式）")
    print("=" * 70)
    
    try:
        from app.agent.mcp import MCPAgent
        
        print("\n📋 功能:")
        print("  - 连接MCP服务器")
        print("  - 使用MCP工具")
        print("  - stdio/SSE传输支持")
        print("  - 工具自动发现")
        
        print("\n🔧 使用方式:")
        print("  - 连接MCP服务器（stdio或SSE）")
        print("  - 自动发现可用工具")
        print("  - 通过Agent接口调用工具")
        
        print("\n✅ MCP Agent已加载")
        print("   注意: 在TRQuant中，我们使用core.mcp.client.MCPClient")
        
    except Exception as e:
        print(f"❌ MCP Agent加载失败: {e}")


async def demo_trquant_integration():
    """演示TRQuant集成功能"""
    print("\n" + "=" * 70)
    print("11. TRQuant集成 - 在TRQuant中使用OpenManus功能")
    print("=" * 70)
    
    try:
        print("\n📋 TRQuant集成模块:")
        print("  - core.automation.BrowserAgent: 浏览器自动化")
        print("  - core.automation.OpenManusAgent: OpenManus Agent封装")
        print("  - core.data_collection.FinancialCollector: 财经数据收集")
        print("  - core.workflow.WorkflowEnhancer: 工作流增强")
        
        print("\n🔧 使用示例:")
        print("""
# 使用BrowserAgent
from core.automation import BrowserAgent

async with BrowserAgent() as agent:
    result = await agent.navigate("https://www.eastmoney.com")
    content = await agent.get_content()

# 使用WorkflowEnhancer
from core.workflow import WorkflowEnhancer

async with WorkflowEnhancer() as enhancer:
    r1 = await enhancer.enhance_r1_market_trend(index_code="000300.XSHG")
    r2 = await enhancer.enhance_r2_mainline()
        """)
        
        print("\n✅ TRQuant集成已完成")
        print("   位置: core/automation/, core/data_collection/, core/workflow/")
        
    except Exception as e:
        print(f"❌ TRQuant集成演示失败: {e}")


async def main():
    """主函数"""
    print("=" * 70)
    print("OpenManus功能演示")
    print("=" * 70)
    print("\n本演示将展示OpenManus的各个功能模块")
    print("注意: 部分功能需要LLM API，这里仅演示模块加载和功能说明")
    
    # 演示各个功能
    await demo_browser_tool()
    await demo_bash_tool()
    await demo_python_execute_tool()
    await demo_editor_tool()
    await demo_web_search_tool()
    await demo_mcp_server()
    await demo_ask_human_tool()
    await demo_terminate_tool()
    await demo_manus_agent()
    await demo_mcp_agent()
    await demo_trquant_integration()
    
    print("\n" + "=" * 70)
    print("演示完成")
    print("=" * 70)
    print("\n📚 相关文档:")
    print("  - OpenManus知识库: 使用knowledge_search('OpenManus')搜索")
    print("  - 集成文档: docs/research/OPENMANUS_INTEGRATION_COMPLETE.md")
    print("  - 知识库总结: docs/research/OPENMANUS_KB_SUMMARY.md")
    print("\n💡 提示:")
    print("  - 浏览器工具需要LLM API才能使用extract_content功能")
    print("  - 在TRQuant中，我们封装了这些功能，提供统一的API")
    print("  - MCP服务器已配置到Cursor，可以通过Cursor Chat调用")


if __name__ == "__main__":
    asyncio.run(main())
