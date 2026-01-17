#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 爬虫工具测试脚本
====================
测试所有可用的爬虫工具和辅助功能
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

print("=" * 80)
print("TRQuant 爬虫工具测试")
print("=" * 80)
print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 测试结果
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "details": []
}

def test_result(name: str, success: bool, message: str = "", error: str = None):
    """记录测试结果"""
    test_results["total"] += 1
    if success:
        test_results["passed"] += 1
        status = "✅ PASS"
    elif error is None and not success:
        # 没有错误但也不成功，视为跳过（可选依赖）
        test_results["skipped"] += 1
        status = "⏭️  SKIP"
    else:
        test_results["failed"] += 1
        status = "❌ FAIL"
    
    test_results["details"].append({
        "name": name,
        "status": status,
        "message": message,
        "error": error
    })
    print(f"{status} - {name}")
    if message:
        print(f"      {message}")
    if error:
        print(f"      错误: {error}")
    print()

# ==================== 1. 基础爬虫工具测试 ====================
print("【1. 基础爬虫工具测试】")
print("-" * 80)

# 1.1 测试 crawler.fetch
try:
    from mcp_servers.unified_dev_server import crawler_fetch
    result = crawler_fetch("https://www.example.com", extract_text=True, extract_links=False)
    if result.get("success"):
        test_result("crawler.fetch", True, f"成功抓取，内容长度: {len(result.get('content', ''))} 字符")
    else:
        test_result("crawler.fetch", False, error=result.get("error", "未知错误"))
except Exception as e:
    test_result("crawler.fetch", False, error=str(e))

# 1.2 测试 crawler.search_docs
try:
    from mcp_servers.unified_dev_server import crawler_search_docs
    result = crawler_search_docs("Python requests", site=None)
    if result.get("success"):
        test_result("crawler.search_docs", True, f"搜索成功，找到 {len(result.get('results', []))} 个结果")
    else:
        test_result("crawler.search_docs", False, error=result.get("error", "未知错误"))
except Exception as e:
    test_result("crawler.search_docs", False, error=str(e))

# 1.3 测试 crawler.download
try:
    from mcp_servers.unified_dev_server import crawler_download
    # 测试下载一个真实存在的小文件（使用Python官网的favicon）
    result = crawler_download("https://www.python.org/static/favicon.ico", filename="test_favicon.ico")
    if result.get("success"):
        test_result("crawler.download", True, f"下载成功: {result.get('filename')}")
        # 清理测试文件
        test_file = Path(result.get('filename', 'test_favicon.ico'))
        if test_file.exists():
            test_file.unlink()
    else:
        test_result("crawler.download", False, error=result.get("error", "未知错误"))
except Exception as e:
    test_result("crawler.download", False, error=str(e))

# 1.4 测试 crawler.extract_code
try:
    from mcp_servers.unified_dev_server import crawler_extract_code
    # 测试从GitHub提取代码
    result = crawler_extract_code("https://github.com/scrapy/scrapy", language="python")
    if result.get("success"):
        test_result("crawler.extract_code", True, f"提取成功，找到 {len(result.get('code_blocks', []))} 个代码块")
    else:
        test_result("crawler.extract_code", False, error=result.get("error", "未知错误"))
except Exception as e:
    test_result("crawler.extract_code", False, error=str(e))

# 1.5 测试 crawler.api_docs
try:
    from mcp_servers.unified_dev_server import crawler_api_docs
    result = crawler_api_docs("requests.get", framework="python")
    if result.get("success"):
        test_result("crawler.api_docs", True, f"获取API文档成功")
    else:
        test_result("crawler.api_docs", False, error=result.get("error", "未知错误"))
except Exception as e:
    test_result("crawler.api_docs", False, error=str(e))

# ==================== 2. Selenium爬虫工具测试 ====================
print("\n【2. Selenium爬虫工具测试】")
print("-" * 80)

# 2.1 测试 Selenium 是否安装
try:
    from selenium import webdriver
    selenium_available = True
    test_result("Selenium安装检查", True, "Selenium已安装")
except ImportError:
    selenium_available = False
    test_result("Selenium安装检查", False, error="Selenium未安装，请运行: pip install selenium")

# 2.2 测试 crawler.selenium.fetch
if selenium_available:
    try:
        from mcp_servers.unified_dev_server import crawler_selenium_fetch
        result = crawler_selenium_fetch("https://www.example.com", wait_time=3, headless=True)
        if result.get("success"):
            test_result("crawler.selenium.fetch", True, f"成功抓取动态页面，标题: {result.get('title', 'N/A')}")
        else:
            test_result("crawler.selenium.fetch", False, error=result.get("error", "未知错误"))
    except Exception as e:
        test_result("crawler.selenium.fetch", False, error=str(e))
else:
    test_result("crawler.selenium.fetch", False, error="Selenium未安装")

# 2.3 测试 SeleniumCrawler 类
try:
    from mcp_servers.crawlers.selenium_crawler import SeleniumCrawler
    test_result("SeleniumCrawler类", True, "类可导入")
except Exception as e:
    test_result("SeleniumCrawler类", False, error=str(e))

# ==================== 3. Lavague AI爬虫工具测试 ====================
print("\n【3. Lavague AI爬虫工具测试】")
print("-" * 80)

# 3.1 测试 Lavague 是否安装
try:
    import lavague
    from lavague import ActionEngine
    lavague_available = True
    test_result("Lavague安装检查", True, "Lavague已安装")
except (ImportError, ModuleNotFoundError) as e:
    lavague_available = False
    # Lavague是可选依赖，标记为跳过而不是失败
    test_result("Lavague安装检查", False, message="Lavague未安装（可选依赖）", error=None)

# 3.2 测试 LavagueCrawler 类
try:
    from mcp_servers.crawlers.lavague_crawler import LavagueCrawler
    test_result("LavagueCrawler类", True, "类可导入")
except Exception as e:
    test_result("LavagueCrawler类", False, error=str(e))

# 3.3 测试 crawler.lavague.execute（如果已安装）
if lavague_available:
    try:
        from mcp_servers.unified_dev_server import crawler_lavague_execute
        test_result("crawler.lavague.execute", True, "工具可用（未实际执行，需要API密钥）")
    except Exception as e:
        test_result("crawler.lavague.execute", False, error=str(e))
else:
    # Lavague是可选依赖，标记为跳过而不是失败
    test_result("crawler.lavague.execute", False, message="Lavague未安装（可选依赖）", error=None)

# ==================== 4. 专用爬虫测试 ====================
print("\n【4. 专用爬虫测试】")
print("-" * 80)

# 4.1 测试 BaseCrawler
try:
    from mcp_servers.crawlers.base_crawler import BaseCrawler, CrawlResult, CrawlTask
    test_result("BaseCrawler基类", True, "基类可导入")
except Exception as e:
    test_result("BaseCrawler基类", False, error=str(e))

# 4.2 测试 CninfoCrawler
try:
    from mcp_servers.crawlers.cninfo_crawler import CninfoCrawler, get_cninfo_crawler
    crawler = get_cninfo_crawler()
    test_result("CninfoCrawler", True, "巨潮资讯网爬虫可初始化")
except Exception as e:
    test_result("CninfoCrawler", False, error=str(e))

# 4.3 测试 EastmoneyCrawler
try:
    from mcp_servers.crawlers.eastmoney_crawler import EastmoneyCrawler, get_eastmoney_crawler
    crawler = get_eastmoney_crawler()
    test_result("EastmoneyCrawler", True, "东方财富网爬虫可初始化")
except Exception as e:
    test_result("EastmoneyCrawler", False, error=str(e))

# 4.4 测试 BidCrawler
try:
    from mcp_servers.crawlers.bid_crawler import BidCrawler, get_bid_crawler
    crawler = get_bid_crawler()
    test_result("BidCrawler", True, "招标中标数据爬虫可初始化")
except Exception as e:
    test_result("BidCrawler", False, error=str(e))

# 4.5 测试 JobCrawler
try:
    from mcp_servers.crawlers.job_crawler import JobCrawler, get_job_crawler
    crawler = get_job_crawler()
    test_result("JobCrawler", True, "招聘数据爬虫可初始化")
except Exception as e:
    test_result("JobCrawler", False, error=str(e))

# ==================== 5. 辅助工具测试 ====================
print("\n【5. 辅助工具测试】")
print("-" * 80)

# 5.1 测试 CrawlerIntegration
try:
    from mcp_servers.crawlers.crawler_integration import CrawlerIntegration, get_crawler_integration
    integration = get_crawler_integration()
    test_result("CrawlerIntegration", True, "爬虫集成工具可初始化")
except Exception as e:
    test_result("CrawlerIntegration", False, error=str(e))

# 5.2 测试 EventProcessor
try:
    from mcp_servers.crawlers.event_processor import EventProcessor, get_event_processor
    processor = get_event_processor()
    test_result("EventProcessor", True, "事件处理器可初始化")
except Exception as e:
    test_result("EventProcessor", False, error=str(e))

# 5.3 测试 DataPipeline
try:
    from mcp_servers.crawlers.pipeline import DataPipeline, get_pipeline
    pipeline = get_pipeline()
    test_result("DataPipeline", True, "数据管道可初始化")
except Exception as e:
    test_result("DataPipeline", False, error=str(e))

# 5.4 测试 crawler_tools
try:
    from mcp_servers.crawlers.crawler_tools import CRAWLER_TOOLS
    test_result("crawler_tools", True, f"定义了 {len(CRAWLER_TOOLS)} 个爬虫工具")
except Exception as e:
    test_result("crawler_tools", False, error=str(e))

# ==================== 6. 爬虫注册系统测试 ====================
print("\n【6. 爬虫注册系统测试】")
print("-" * 80)

try:
    from mcp_servers.crawlers.base_crawler import register_crawler, get_crawler, list_crawlers
    crawlers = list_crawlers()
    test_result("爬虫注册系统", True, f"已注册 {len(crawlers)} 个爬虫: {', '.join(crawlers)}")
except Exception as e:
    test_result("爬虫注册系统", False, error=str(e))

# ==================== 7. 依赖检查 ====================
print("\n【7. 依赖检查】")
print("-" * 80)

dependencies = {
    "requests": ("requests", "基础HTTP请求", False),  # 必需
    "beautifulsoup4": ("bs4", "HTML解析", False),  # 必需
    "selenium": ("selenium", "浏览器自动化", False),  # 必需
    "lavague": ("lavague", "AI驱动浏览器自动化（可选）", True),  # 可选
    "playwright": ("playwright", "浏览器自动化（可选）", True),  # 可选
}

for dep, (import_name, desc, optional) in dependencies.items():
    try:
        __import__(import_name)
        test_result(f"依赖: {dep}", True, desc)
    except (ImportError, ModuleNotFoundError):
        if optional:
            # 可选依赖，标记为跳过而不是失败
            test_result(f"依赖: {dep}", False, message=f"{dep}未安装（可选）", error=None)
        else:
            test_result(f"依赖: {dep}", False, error=f"{dep}未安装")

# ==================== 测试总结 ====================
print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"总测试数: {test_results['total']}")
print(f"✅ 通过: {test_results['passed']}")
print(f"❌ 失败: {test_results['failed']}")
print(f"⏭️  跳过: {test_results['skipped']}")
print(f"通过率: {test_results['passed'] / test_results['total'] * 100:.1f}%")
print()

# 保存测试结果
results_file = TRQUANT_ROOT / "docs" / "CRAWLER_TEST_RESULTS.json"
results_file.parent.mkdir(parents=True, exist_ok=True)
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        "test_time": datetime.now().isoformat(),
        "summary": {
            "total": test_results['total'],
            "passed": test_results['passed'],
            "failed": test_results['failed'],
            "skipped": test_results['skipped'],
            "pass_rate": f"{test_results['passed'] / test_results['total'] * 100:.1f}%"
        },
        "details": test_results['details']
    }, f, ensure_ascii=False, indent=2)

print(f"测试结果已保存到: {results_file}")
