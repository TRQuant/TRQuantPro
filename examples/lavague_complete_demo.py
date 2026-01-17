#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LaVague 在 TRQuant 系统中的完整功能演示
==========================================

本示例展示LaVague在量化交易系统中的6大应用场景：
1. 自动化数据收集（公告、研报、财务数据）
2. 自动化表单填写和登录
3. 智能数据提取
4. 自动化测试和验证
5. 自动化工作流
6. 智能信息检索

运行方式:
    cd /home/taotao/.cursor/worktrees/TRQuant/ope
    ./venv/bin/python examples/lavague_complete_demo.py
"""

import sys
from pathlib import Path
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler

# 配置
DEMO_STOCK_CODE = "000001"  # 平安银行
DEMO_STOCK_NAME = "平安银行"


class LaVagueTRQuantDemo:
    """LaVague在TRQuant系统中的完整功能演示"""
    
    def __init__(self, headless: bool = True):
        """初始化演示"""
        self.headless = headless
        self.crawler = None
        self.results = {
            "demo_time": datetime.now().isoformat(),
            "scenarios": {}
        }
        
    def __enter__(self):
        """上下文管理器入口"""
        print("=" * 80)
        print("LaVague 在 TRQuant 系统中的完整功能演示")
        print("=" * 80)
        print()
        print(f"演示股票: {DEMO_STOCK_CODE} ({DEMO_STOCK_NAME})")
        print(f"演示时间: {self.results['demo_time']}")
        print()
        
        # 初始化LaVague爬虫
        try:
            self.crawler = get_lavague_crawler(headless=self.headless)
            if not self.crawler.engine:
                print("⚠️  LaVague未正确安装，部分功能可能无法使用")
                print("   请运行: ./venv/bin/python -m pip install lavague")
                print()
        except Exception as e:
            print(f"⚠️  LaVague初始化失败: {e}")
            print()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.crawler:
            self.crawler.close()
        
        # 保存结果
        results_file = TRQUANT_ROOT / "examples" / "lavague_demo_results.json"
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print()
        print("=" * 80)
        print("演示完成！结果已保存到: examples/lavague_demo_results.json")
        print("=" * 80)
    
    # ==================== 场景1: 自动化数据收集 ====================
    
    def scenario1_automated_data_collection(self):
        """场景1: 自动化数据收集"""
        print("\n" + "=" * 80)
        print("【场景1】自动化数据收集")
        print("=" * 80)
        print()
        
        scenario_results = {
            "announcements": {},
            "research_reports": {},
            "financial_data": {}
        }
        
        # 1.1 自动收集公告
        print("【1.1】自动收集上市公司公告")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                访问巨潮资讯网（http://www.cninfo.com.cn），
                搜索股票代码{DEMO_STOCK_CODE}，
                进入公告页面，提取最近30天的所有公告，
                包括：
                - 公告标题
                - 发布日期
                - 公告类型
                - 公告链接
                将结果整理为JSON格式
                """
                
                print(f"执行指令: 收集{DEMO_STOCK_CODE}的公告...")
                result = self.crawler.execute_instruction(instruction, max_actions=15)
                
                if result.get("success"):
                    scenario_results["announcements"] = {
                        "success": True,
                        "count": "未知（需要解析结果）",
                        "message": "公告收集成功"
                    }
                    print("✅ 公告收集成功")
                else:
                    scenario_results["announcements"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 公告收集失败: {result.get('error')}")
            except Exception as e:
                scenario_results["announcements"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["announcements"] = {"skipped": True}
        
        print()
        
        # 1.2 自动收集研报
        print("【1.2】自动收集研报数据")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                访问东方财富网（https://www.eastmoney.com），
                搜索股票代码{DEMO_STOCK_CODE}，
                进入研报页面，提取最近3个月的所有研报，
                包括：
                - 研报标题
                - 发布机构
                - 发布时间
                - 评级和目标价
                - 核心观点摘要
                将结果整理为结构化数据
                """
                
                print(f"执行指令: 收集{DEMO_STOCK_CODE}的研报...")
                result = self.crawler.execute_instruction(instruction, max_actions=15)
                
                if result.get("success"):
                    scenario_results["research_reports"] = {
                        "success": True,
                        "count": "未知（需要解析结果）",
                        "message": "研报收集成功"
                    }
                    print("✅ 研报收集成功")
                else:
                    scenario_results["research_reports"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 研报收集失败: {result.get('error')}")
            except Exception as e:
                scenario_results["research_reports"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["research_reports"] = {"skipped": True}
        
        print()
        
        # 1.3 自动收集财务数据
        print("【1.3】自动收集财务数据")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                访问同花顺网站（https://www.10jqka.com.cn），
                搜索股票代码{DEMO_STOCK_CODE}，
                进入财务数据页面，提取最近5年的关键财务指标：
                - 营业收入（亿元）
                - 净利润（亿元）
                - 净资产收益率（ROE）
                - 资产负债率
                - 每股收益（EPS）
                将数据整理为时间序列格式
                """
                
                print(f"执行指令: 收集{DEMO_STOCK_CODE}的财务数据...")
                result = self.crawler.execute_instruction(instruction, max_actions=15)
                
                if result.get("success"):
                    scenario_results["financial_data"] = {
                        "success": True,
                        "message": "财务数据收集成功"
                    }
                    print("✅ 财务数据收集成功")
                else:
                    scenario_results["financial_data"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 财务数据收集失败: {result.get('error')}")
            except Exception as e:
                scenario_results["financial_data"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["financial_data"] = {"skipped": True}
        
        self.results["scenarios"]["1_automated_data_collection"] = scenario_results
        print()
    
    # ==================== 场景2: 自动化表单填写和登录 ====================
    
    def scenario2_automated_form_filling(self):
        """场景2: 自动化表单填写和登录"""
        print("\n" + "=" * 80)
        print("【场景2】自动化表单填写和登录")
        print("=" * 80)
        print()
        
        scenario_results = {}
        
        # 2.1 模拟登录流程
        print("【2.1】模拟数据源网站登录流程")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                # 注意：这里使用示例网站，实际使用时替换为真实数据源
                instruction = """
                访问示例网站（https://www.example.com），
                找到登录按钮并点击，
                在登录表单中填写：
                - 用户名：demo_user
                - 密码：demo_password
                点击登录按钮完成登录
                （注意：这是演示，实际使用时需要真实凭证）
                """
                
                print("执行指令: 模拟登录流程...")
                print("⚠️  注意：这是演示，使用示例网站")
                result = self.crawler.execute_instruction(instruction, max_actions=10)
                
                if result.get("success"):
                    scenario_results["login"] = {
                        "success": True,
                        "message": "登录流程演示成功"
                    }
                    print("✅ 登录流程演示成功")
                else:
                    scenario_results["login"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 登录流程失败: {result.get('error')}")
            except Exception as e:
                scenario_results["login"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["login"] = {"skipped": True}
        
        print()
        
        # 2.2 自动化查询
        print("【2.2】自动化数据查询")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                假设已经登录数据源网站，
                进入数据查询页面，
                填写查询条件：
                - 股票代码：{DEMO_STOCK_CODE}
                - 时间范围：2024-01-01 至 2024-12-31
                - 数据类型：日线数据
                点击查询按钮，等待结果加载，
                下载查询结果（CSV格式）
                """
                
                print("执行指令: 自动化数据查询...")
                result = self.crawler.execute_instruction(instruction, max_actions=12)
                
                if result.get("success"):
                    scenario_results["query"] = {
                        "success": True,
                        "message": "数据查询演示成功"
                    }
                    print("✅ 数据查询演示成功")
                else:
                    scenario_results["query"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 数据查询失败: {result.get('error')}")
            except Exception as e:
                scenario_results["query"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["query"] = {"skipped": True}
        
        self.results["scenarios"]["2_automated_form_filling"] = scenario_results
        print()
    
    # ==================== 场景3: 智能数据提取 ====================
    
    def scenario3_intelligent_data_extraction(self):
        """场景3: 智能数据提取"""
        print("\n" + "=" * 80)
        print("【场景3】智能数据提取")
        print("=" * 80)
        print()
        
        scenario_results = {}
        
        # 3.1 从复杂页面提取数据
        print("【3.1】从复杂页面提取股票数据")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                # 先导航到页面
                nav_result = self.crawler.navigate(f"https://quote.eastmoney.com/sz{DEMO_STOCK_CODE}.html")
                
                if nav_result.get("success"):
                    description = f"""
                    从当前页面提取以下信息：
                    - 股票代码和名称
                    - 当前价格和涨跌幅
                    - 今日最高价和最低价
                    - 成交量（手）和成交额（万元）
                    - 技术指标：MA5, MA10, MA20
                    - 资金流向：主力净流入、超大单、大单
                    - 市盈率、市净率
                    将数据整理为JSON格式
                    """
                    
                    print(f"执行指令: 提取{DEMO_STOCK_CODE}的实时数据...")
                    result = self.crawler.extract_data(description)
                    
                    if result.get("success"):
                        scenario_results["stock_data"] = {
                            "success": True,
                            "message": "股票数据提取成功",
                            "data_length": result.get("page_source_length", 0)
                        }
                        print("✅ 股票数据提取成功")
                    else:
                        scenario_results["stock_data"] = {
                            "success": False,
                            "error": result.get("error", "未知错误")
                        }
                        print(f"❌ 股票数据提取失败: {result.get('error')}")
                else:
                    scenario_results["stock_data"] = {
                        "success": False,
                        "error": "页面导航失败"
                    }
                    print(f"❌ 页面导航失败: {nav_result.get('error')}")
            except Exception as e:
                scenario_results["stock_data"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["stock_data"] = {"skipped": True}
        
        print()
        
        # 3.2 提取动态内容
        print("【3.2】提取动态渲染的内容")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = """
                访问一个包含JavaScript动态内容的页面，
                等待页面完全加载（包括AJAX请求），
                提取所有实时更新的数据：
                - 实时价格
                - 实时成交量
                - 实时资金流向
                确保数据是最新的
                """
                
                print("执行指令: 提取动态内容...")
                result = self.crawler.execute_instruction(instruction, max_actions=10)
                
                if result.get("success"):
                    scenario_results["dynamic_content"] = {
                        "success": True,
                        "message": "动态内容提取成功"
                    }
                    print("✅ 动态内容提取成功")
                else:
                    scenario_results["dynamic_content"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 动态内容提取失败: {result.get('error')}")
            except Exception as e:
                scenario_results["dynamic_content"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["dynamic_content"] = {"skipped": True}
        
        self.results["scenarios"]["3_intelligent_data_extraction"] = scenario_results
        print()
    
    # ==================== 场景4: 自动化测试和验证 ====================
    
    def scenario4_automated_testing(self):
        """场景4: 自动化测试和验证"""
        print("\n" + "=" * 80)
        print("【场景4】自动化测试和验证")
        print("=" * 80)
        print()
        
        scenario_results = {}
        
        # 4.1 数据源可用性检测
        print("【4.1】数据源可用性检测")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = """
                访问数据源网站（https://www.cninfo.com.cn），
                执行以下检测：
                1. 检查网站是否可以正常访问
                2. 检查首页是否正常加载
                3. 检查搜索功能是否可用
                4. 检查数据查询接口是否响应
                生成检测报告，包括：
                - 网站状态（正常/异常）
                - 响应时间
                - 功能可用性列表
                """
                
                print("执行指令: 检测数据源可用性...")
                result = self.crawler.execute_instruction(instruction, max_actions=12)
                
                if result.get("success"):
                    scenario_results["availability_check"] = {
                        "success": True,
                        "message": "数据源可用性检测完成"
                    }
                    print("✅ 数据源可用性检测完成")
                else:
                    scenario_results["availability_check"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 检测失败: {result.get('error')}")
            except Exception as e:
                scenario_results["availability_check"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["availability_check"] = {"skipped": True}
        
        print()
        
        # 4.2 数据完整性验证
        print("【4.2】数据完整性验证")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                访问股票数据页面，验证数据完整性：
                1. 检查必要字段是否存在（价格、成交量等）
                2. 检查数据格式是否正确
                3. 检查数据是否在合理范围内
                4. 检查时间戳是否最新
                生成验证报告
                """
                
                print("执行指令: 验证数据完整性...")
                result = self.crawler.execute_instruction(instruction, max_actions=10)
                
                if result.get("success"):
                    scenario_results["data_validation"] = {
                        "success": True,
                        "message": "数据完整性验证完成"
                    }
                    print("✅ 数据完整性验证完成")
                else:
                    scenario_results["data_validation"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 验证失败: {result.get('error')}")
            except Exception as e:
                scenario_results["data_validation"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["data_validation"] = {"skipped": True}
        
        self.results["scenarios"]["4_automated_testing"] = scenario_results
        print()
    
    # ==================== 场景5: 自动化工作流 ====================
    
    def scenario5_automated_workflow(self):
        """场景5: 自动化工作流"""
        print("\n" + "=" * 80)
        print("【场景5】自动化工作流")
        print("=" * 80)
        print()
        
        scenario_results = {}
        
        # 5.1 每日数据更新工作流
        print("【5.1】每日数据更新工作流")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                workflow_steps = [
                    "访问数据源网站",
                    "登录账户（如果需要）",
                    "导航到数据下载页面",
                    "选择最新交易日",
                    "下载数据文件",
                    "验证文件完整性",
                    "生成更新报告"
                ]
                
                print("执行多步骤工作流:")
                for i, step in enumerate(workflow_steps, 1):
                    print(f"  步骤{i}: {step}")
                
                instruction = f"""
                执行以下完整工作流：
                1. 访问数据源网站
                2. 登录账户（如果需要）
                3. 导航到数据下载页面
                4. 选择最新交易日的数据
                5. 下载数据文件
                6. 验证文件是否完整（检查文件大小、格式）
                7. 生成数据更新报告，包括：
                   - 下载时间
                   - 文件大小
                   - 数据记录数
                   - 更新状态
                """
                
                print()
                print("执行指令: 运行完整工作流...")
                result = self.crawler.execute_instruction(instruction, max_actions=20)
                
                if result.get("success"):
                    scenario_results["daily_update"] = {
                        "success": True,
                        "steps": len(workflow_steps),
                        "message": "每日数据更新工作流完成"
                    }
                    print("✅ 每日数据更新工作流完成")
                else:
                    scenario_results["daily_update"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 工作流失败: {result.get('error')}")
            except Exception as e:
                scenario_results["daily_update"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["daily_update"] = {"skipped": True}
        
        print()
        
        # 5.2 多数据源数据同步
        print("【5.2】多数据源数据同步")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                执行多数据源数据同步任务：
                
                数据源1 - 巨潮资讯网：
                - 访问网站
                - 搜索股票{DEMO_STOCK_CODE}
                - 收集最新公告
                
                数据源2 - 东方财富网：
                - 访问网站
                - 搜索股票{DEMO_STOCK_CODE}
                - 收集最新研报
                
                数据源3 - 同花顺：
                - 访问网站
                - 搜索股票{DEMO_STOCK_CODE}
                - 收集财务数据
                
                最后，合并所有数据源的数据，
                生成统一的数据报告，包括：
                - 数据来源
                - 数据时间
                - 数据摘要
                """
                
                print("执行指令: 同步多数据源数据...")
                result = self.crawler.execute_instruction(instruction, max_actions=25)
                
                if result.get("success"):
                    scenario_results["multi_source_sync"] = {
                        "success": True,
                        "sources": 3,
                        "message": "多数据源数据同步完成"
                    }
                    print("✅ 多数据源数据同步完成")
                else:
                    scenario_results["multi_source_sync"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 同步失败: {result.get('error')}")
            except Exception as e:
                scenario_results["multi_source_sync"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["multi_source_sync"] = {"skipped": True}
        
        self.results["scenarios"]["5_automated_workflow"] = scenario_results
        print()
    
    # ==================== 场景6: 智能信息检索 ====================
    
    def scenario6_intelligent_information_retrieval(self):
        """场景6: 智能信息检索"""
        print("\n" + "=" * 80)
        print("【场景6】智能信息检索")
        print("=" * 80)
        print()
        
        scenario_results = {}
        
        # 6.1 投资主线信息收集
        print("【6.1】投资主线信息收集")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = """
                访问财经网站，搜索"人工智能"相关投资主线信息：
                1. 搜索相关新闻和研报
                2. 提取以下信息：
                   - 相关公司列表（股票代码和名称）
                   - 行业动态和政策信息
                   - 市场观点和投资建议
                   - 技术发展趋势
                3. 整理为结构化数据，包括：
                   - 公司列表
                   - 行业分析
                   - 投资建议摘要
                """
                
                print("执行指令: 收集投资主线信息...")
                result = self.crawler.execute_instruction(instruction, max_actions=15)
                
                if result.get("success"):
                    scenario_results["mainline_info"] = {
                        "success": True,
                        "topic": "人工智能",
                        "message": "投资主线信息收集完成"
                    }
                    print("✅ 投资主线信息收集完成")
                else:
                    scenario_results["mainline_info"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 信息收集失败: {result.get('error')}")
            except Exception as e:
                scenario_results["mainline_info"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["mainline_info"] = {"skipped": True}
        
        print()
        
        # 6.2 竞争对手分析
        print("【6.2】竞争对手分析")
        print("-" * 80)
        if self.crawler and self.crawler.engine:
            try:
                instruction = f"""
                访问行业分析网站，分析{DEMO_STOCK_NAME}的竞争对手：
                1. 搜索同行业公司
                2. 收集竞争对手信息：
                   - 竞争对手列表
                   - 市场份额对比
                   - 财务数据对比
                   - 业务模式分析
                3. 生成竞争分析报告，包括：
                   - 主要竞争对手
                   - 竞争优势和劣势
                   - 市场地位对比
                """
                
                print(f"执行指令: 分析{DEMO_STOCK_NAME}的竞争对手...")
                result = self.crawler.execute_instruction(instruction, max_actions=15)
                
                if result.get("success"):
                    scenario_results["competitor_analysis"] = {
                        "success": True,
                        "target": DEMO_STOCK_NAME,
                        "message": "竞争对手分析完成"
                    }
                    print("✅ 竞争对手分析完成")
                else:
                    scenario_results["competitor_analysis"] = {
                        "success": False,
                        "error": result.get("error", "未知错误")
                    }
                    print(f"❌ 分析失败: {result.get('error')}")
            except Exception as e:
                scenario_results["competitor_analysis"] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ 异常: {e}")
        else:
            print("⏭️  跳过（LaVague未初始化）")
            scenario_results["competitor_analysis"] = {"skipped": True}
        
        self.results["scenarios"]["6_intelligent_information_retrieval"] = scenario_results
        print()
    
    # ==================== 运行所有场景 ====================
    
    def run_all_scenarios(self):
        """运行所有演示场景"""
        print("\n开始运行所有演示场景...\n")
        
        # 运行所有场景
        self.scenario1_automated_data_collection()
        time.sleep(2)  # 短暂休息
        
        self.scenario2_automated_form_filling()
        time.sleep(2)
        
        self.scenario3_intelligent_data_extraction()
        time.sleep(2)
        
        self.scenario4_automated_testing()
        time.sleep(2)
        
        self.scenario5_automated_workflow()
        time.sleep(2)
        
        self.scenario6_intelligent_information_retrieval()
        
        # 生成总结
        self._print_summary()
    
    def _print_summary(self):
        """打印演示总结"""
        print("\n" + "=" * 80)
        print("演示总结")
        print("=" * 80)
        print()
        
        total_scenarios = len(self.results["scenarios"])
        successful_scenarios = sum(
            1 for scenario in self.results["scenarios"].values()
            if any(v.get("success") for v in scenario.values() if isinstance(v, dict))
        )
        
        print(f"总场景数: {total_scenarios}")
        print(f"成功场景: {successful_scenarios}")
        print()
        
        print("各场景状态:")
        for scenario_name, scenario_data in self.results["scenarios"].items():
            scenario_display = scenario_name.replace("_", " ").title()
            print(f"  - {scenario_display}: ", end="")
            
            # 检查是否有成功的子任务
            has_success = any(
                v.get("success") for v in scenario_data.values()
                if isinstance(v, dict) and not v.get("skipped")
            )
            
            if has_success:
                print("✅ 部分成功")
            elif any(v.get("skipped") for v in scenario_data.values() if isinstance(v, dict)):
                print("⏭️  已跳过")
            else:
                print("❌ 失败")
        
        print()


def main():
    """主函数"""
    # 创建演示实例
    with LaVagueTRQuantDemo(headless=True) as demo:
        # 运行所有场景
        demo.run_all_scenarios()


if __name__ == "__main__":
    main()
