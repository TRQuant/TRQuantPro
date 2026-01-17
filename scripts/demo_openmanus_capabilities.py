#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus功能演示脚本
展示OpenManus的核心能力和实际用途
"""
import sys
import asyncio
from pathlib import Path

# 添加项目根路径和OpenManus路径
PROJECT_ROOT = Path(__file__).parent.parent
OPENMANUS_DIR = PROJECT_ROOT / "third_party" / "OpenManus"

sys.path.insert(0, str(OPENMANUS_DIR))
sys.path.insert(0, str(PROJECT_ROOT))

def print_section(title: str):
    """打印章节标题"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def demo_mcp_tools():
    """演示MCP工具功能"""
    print_section("OpenManus MCP工具功能演示")
    
    print("1. 浏览器自动化工具 (BrowserUseTool)")
    print("   - 功能: 自动化浏览器操作")
    print("   - 能力:")
    print("     • 访问网页")
    print("     • 点击元素")
    print("     • 填写表单")
    print("     • 提取页面内容")
    print("     • 截图")
    print("   - 应用场景:")
    print("     • 抓取财经网站数据（东方财富、同花顺等）")
    print("     • 获取实时行情信息")
    print("     • 抓取新闻和公告")
    print("     • 自动化数据收集")
    print()
    
    print("2. 命令行工具 (Bash)")
    print("   - 功能: 执行系统命令")
    print("   - 能力:")
    print("     • 运行Shell命令")
    print("     • 文件操作")
    print("     • 系统信息查询")
    print("   - 应用场景:")
    print("     • 数据处理和转换")
    print("     • 文件管理")
    print("     • 系统维护")
    print()
    
    print("3. 代码编辑器工具 (StrReplaceEditor)")
    print("   - 功能: 代码编辑和文件操作")
    print("   - 能力:")
    print("     • 读取文件")
    print("     • 修改代码")
    print("     • 字符串替换")
    print("     • 文件写入")
    print("   - 应用场景:")
    print("     • 策略代码生成")
    print("     • 配置文件修改")
    print("     • 代码重构")
    print()
    
    print("4. 终止工具 (Terminate)")
    print("   - 功能: 终止任务执行")
    print("   - 应用场景:")
    print("     • 任务完成时终止")
    print("     • 错误处理")
    print()

def demo_integration_scenarios():
    """演示集成场景"""
    print_section("OpenManus与TRQuant集成场景")
    
    print("场景1: 财经数据收集")
    print("   - 使用BrowserUseTool访问东方财富网站")
    print("   - 抓取实时行情数据")
    print("   - 提取新闻和公告信息")
    print("   - 存储到TRQuant数据库")
    print("   - 示例:")
    print('     "使用openmanus的browser工具访问东方财富，获取000001的实时价格"')
    print()
    
    print("场景2: 策略代码生成")
    print("   - 使用StrReplaceEditor生成策略代码")
    print("   - 基于模板修改策略参数")
    print("   - 保存到strategies目录")
    print("   - 示例:")
    print('     "使用openmanus的editor工具生成一个MA交叉策略"')
    print()
    
    print("场景3: 数据处理")
    print("   - 使用Bash工具执行数据处理脚本")
    print("   - 文件格式转换")
    print("   - 数据清洗和预处理")
    print("   - 示例:")
    print('     "使用openmanus的bash工具处理CSV数据文件"')
    print()
    
    print("场景4: 自动化工作流")
    print("   - 结合多个工具完成任务")
    print("   - 浏览器抓取 → 数据处理 → 代码生成 → 策略部署")
    print("   - 示例:")
    print('     "使用openmanus工具自动化执行：')
    print('      1. 访问财经网站获取数据')
    print('      2. 处理数据并生成报告')
    print('      3. 生成策略代码"')
    print()

def demo_usage_examples():
    """演示使用示例"""
    print_section("使用示例")
    
    print("1. 在Cursor Chat中使用OpenManus MCP服务器")
    print("   - 配置MCP服务器（见配置文件）")
    print("   - 在Cursor Chat中输入自然语言指令")
    print("   - Cursor通过MCP协议调用OpenManus工具")
    print("   - 示例对话:")
    print('     用户: "使用openmanus的browser工具访问 https://www.eastmoney.com"')
    print('     Cursor: [通过MCP调用OpenManus的browser工具]')
    print('     OpenManus: [执行浏览器操作，返回结果]')
    print()
    
    print("2. 通过Python代码使用OpenManus工具")
    print("   - 直接导入OpenManus工具")
    print("   - 在TRQuant脚本中使用")
    print("   - 示例代码:")
    print("     ```python")
    print("     from app.tool.browser_use_tool import BrowserUseTool")
    print("     ")
    print("     browser = BrowserUseTool()")
    print("     result = await browser.execute(")
    print("         instruction='访问东方财富网站',")
    print("         url='https://www.eastmoney.com'")
    print("     )")
    print("     ```")
    print()
    
    print("3. 在Notebook中使用")
    print("   - 在Jupyter Notebook中导入工具")
    print("   - 交互式使用OpenManus功能")
    print("   - 与TRQuant的数据分析流程集成")
    print()

def demo_capabilities_summary():
    """演示能力总结"""
    print_section("OpenManus核心能力总结")
    
    capabilities = [
        {
            "功能": "浏览器自动化",
            "工具": "BrowserUseTool",
            "能力": [
                "访问网页",
                "智能元素识别",
                "表单填写",
                "内容提取",
                "截图和录制"
            ],
            "在TRQuant中的应用": [
                "财经网站数据抓取",
                "实时行情获取",
                "新闻和公告收集",
                "自动化数据更新"
            ]
        },
        {
            "功能": "命令行执行",
            "工具": "Bash",
            "能力": [
                "Shell命令执行",
                "文件操作",
                "系统调用",
                "脚本运行"
            ],
            "在TRQuant中的应用": [
                "数据处理脚本",
                "文件格式转换",
                "系统维护",
                "批量操作"
            ]
        },
        {
            "功能": "代码编辑",
            "工具": "StrReplaceEditor",
            "能力": [
                "文件读取",
                "代码修改",
                "字符串替换",
                "文件写入"
            ],
            "在TRQuant中的应用": [
                "策略代码生成",
                "配置文件修改",
                "代码重构",
                "模板填充"
            ]
        },
        {
            "功能": "MCP服务器",
            "工具": "MCPServer",
            "能力": [
                "工具注册",
                "MCP协议支持",
                "工具调用",
                "结果返回"
            ],
            "在TRQuant中的应用": [
                "通过Cursor Chat调用",
                "与其他MCP服务器集成",
                "工具统一管理",
                "工作流自动化"
            ]
        }
    ]
    
    for i, cap in enumerate(capabilities, 1):
        print(f"{i}. {cap['功能']} ({cap['工具']})")
        print(f"   - 核心能力: {', '.join(cap['能力'][:3])}...")
        print(f"   - TRQuant应用: {', '.join(cap['在TRQuant中的应用'][:2])}...")
        print()

def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("  OpenManus 功能演示")
    print("=" * 80)
    print("\nOpenManus是一个开源AI Agent框架，提供强大的工具能力")
    print("可以与TRQuant系统集成，增强数据收集和自动化能力")
    
    demo_mcp_tools()
    demo_integration_scenarios()
    demo_usage_examples()
    demo_capabilities_summary()
    
    print_section("下一步建议")
    
    print("1. 配置OpenManus MCP服务器到Cursor")
    print("   - 编辑 .cursor/mcp.json")
    print("   - 添加openmanus服务器配置")
    print()
    
    print("2. 测试MCP工具调用")
    print("   - 在Cursor Chat中测试browser工具")
    print("   - 验证工具是否正常工作")
    print()
    
    print("3. 集成到TRQuant工作流")
    print("   - 在R0（数据源检测）中使用browser工具")
    print("   - 在数据收集步骤中使用OpenManus工具")
    print()
    
    print("4. 开发实际应用")
    print("   - 财经网站数据抓取")
    print("   - 策略代码自动生成")
    print("   - 自动化数据处理")
    print()
    
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
