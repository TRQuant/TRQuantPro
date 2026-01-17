#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LaVague 快速演示 - 实际可运行的简化版本
========================================

这是一个实际可运行的简化演示，展示LaVague的核心功能。
由于完整演示需要访问真实网站，这里提供一个更实用的版本。

运行方式:
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python examples/lavague_quick_demo.py
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler


def demo_basic_usage():
    """演示1: LaVague基础使用"""
    print("=" * 80)
    print("演示1: LaVague基础使用")
    print("=" * 80)
    print()
    
    try:
        # 创建爬虫实例
        crawler = get_lavague_crawler(headless=True)
        
        if not crawler.engine:
            print("❌ LaVague未正确安装")
            print("   请运行: ./venv/bin/python -m pip install lavague")
            return
        
        # 导航到网页
        print("【步骤1】导航到网页")
        print("-" * 80)
        nav_result = crawler.navigate("https://www.example.com")
        
        if nav_result.get("success"):
            print(f"✅ 导航成功: {nav_result.get('title')}")
            print(f"   当前URL: {nav_result.get('current_url')}")
        else:
            print(f"❌ 导航失败: {nav_result.get('error')}")
        
        print()
        
        # 执行简单指令
        print("【步骤2】执行自然语言指令")
        print("-" * 80)
        instruction = "提取页面标题和主要内容"
        result = crawler.execute_instruction(instruction, max_actions=5)
        
        if result.get("success"):
            print(f"✅ 指令执行成功")
            print(f"   结果: {result.get('result', 'N/A')[:200]}...")
        else:
            print(f"❌ 指令执行失败: {result.get('error')}")
        
        print()
        
        # 提取数据
        print("【步骤3】智能数据提取")
        print("-" * 80)
        description = "提取页面中的所有链接和标题"
        extract_result = crawler.extract_data(description)
        
        if extract_result.get("success"):
            print(f"✅ 数据提取成功")
            print(f"   数据长度: {extract_result.get('page_source_length', 0)} 字符")
        else:
            print(f"❌ 数据提取失败: {extract_result.get('error')}")
        
        # 关闭
        crawler.close()
        
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()


def demo_stock_data_collection():
    """演示2: 股票数据收集（实际示例）"""
    print("\n" + "=" * 80)
    print("演示2: 股票数据收集")
    print("=" * 80)
    print()
    
    stock_code = "000001"  # 平安银行
    
    try:
        crawler = get_lavague_crawler(headless=True)
        
        if not crawler.engine:
            print("❌ LaVague未正确安装")
            return
        
        # 导航到东方财富股票页面
        print(f"【步骤1】访问{stock_code}的股票页面")
        print("-" * 80)
        url = f"https://quote.eastmoney.com/sz{stock_code}.html"
        nav_result = crawler.navigate(url)
        
        if nav_result.get("success"):
            print(f"✅ 页面加载成功: {nav_result.get('title')}")
        else:
            print(f"❌ 页面加载失败: {nav_result.get('error')}")
            return
        
        print()
        
        # 提取股票数据
        print("【步骤2】提取股票实时数据")
        print("-" * 80)
        description = """
        从当前页面提取以下信息：
        - 股票名称和代码
        - 当前价格
        - 涨跌幅
        - 成交量
        """
        
        result = crawler.extract_data(description)
        
        if result.get("success"):
            print("✅ 数据提取成功")
            print(f"   提取的数据: {result.get('data', 'N/A')[:300]}...")
        else:
            print(f"❌ 数据提取失败: {result.get('error')}")
        
        print()
        
        # 执行复杂指令
        print("【步骤3】执行复杂数据收集指令")
        print("-" * 80)
        instruction = f"""
        在当前页面执行以下操作：
        1. 找到并点击"资金流向"标签
        2. 等待数据加载
        3. 提取主力资金流向数据
        4. 返回数据摘要
        """
        
        exec_result = crawler.execute_instruction(instruction, max_actions=10)
        
        if exec_result.get("success"):
            print("✅ 指令执行成功")
            print(f"   执行结果: {exec_result.get('result', 'N/A')[:200]}...")
        else:
            print(f"❌ 指令执行失败: {exec_result.get('error')}")
        
        crawler.close()
        
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()


def demo_workflow_automation():
    """演示3: 工作流自动化"""
    print("\n" + "=" * 80)
    print("演示3: 工作流自动化")
    print("=" * 80)
    print()
    
    try:
        crawler = get_lavague_crawler(headless=True)
        
        if not crawler.engine:
            print("❌ LaVague未正确安装")
            return
        
        # 多步骤工作流
        print("【工作流】执行多步骤数据收集任务")
        print("-" * 80)
        
        workflow = [
            {
                "step": 1,
                "description": "访问数据源网站",
                "instruction": "访问巨潮资讯网首页"
            },
            {
                "step": 2,
                "description": "搜索股票",
                "instruction": "在搜索框中输入000001并搜索"
            },
            {
                "step": 3,
                "description": "提取数据",
                "instruction": "提取搜索结果中的股票基本信息"
            }
        ]
        
        for task in workflow:
            print(f"\n步骤{task['step']}: {task['description']}")
            print(f"  指令: {task['instruction']}")
            
            result = crawler.execute_instruction(task['instruction'], max_actions=5)
            
            if result.get("success"):
                print(f"  ✅ 成功")
            else:
                print(f"  ❌ 失败: {result.get('error')}")
                break
        
        crawler.close()
        
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("LaVague 在 TRQuant 系统中的快速演示")
    print("=" * 80)
    print()
    print("本演示展示LaVague的核心功能：")
    print("1. 基础使用（导航、执行指令、提取数据）")
    print("2. 股票数据收集（实际示例）")
    print("3. 工作流自动化（多步骤任务）")
    print()
    print("注意：")
    print("- 需要正确安装LaVague: pip install lavague")
    print("- 需要配置OPENAI_API_KEY环境变量")
    print("- 某些网站可能有反爬虫机制")
    print()
    
    # 运行演示
    demo_basic_usage()
    demo_stock_data_collection()
    demo_workflow_automation()
    
    print("\n" + "=" * 80)
    print("演示完成！")
    print("=" * 80)
    print()
    print("更多信息请参考:")
    print("- docs/LAVAGUE_IN_TRQUANT_COMPLETE_GUIDE.md")
    print("- examples/lavague_complete_demo.py (完整演示)")


if __name__ == "__main__":
    main()
