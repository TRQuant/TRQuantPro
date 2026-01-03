# -*- coding: utf-8 -*-
"""
Selenium和Lavague爬虫工具使用示例

安装依赖:
    pip install selenium lavague
    # Chrome需要下载chromedriver: https://chromedriver.chromium.org/
"""

import asyncio
from pathlib import Path

# 添加项目路径
import sys
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ==================== 示例1: Selenium基础使用 ====================

def example_selenium_basic():
    """示例1: 使用Selenium抓取动态网页"""
    print("\n=== 示例1: Selenium基础使用 ===")
    
    from mcp_servers.crawlers.selenium_crawler import SeleniumCrawler
    
    # 创建爬虫实例（无头模式）
    with SeleniumCrawler(headless=True) as crawler:
        # 抓取动态页面
        result = crawler.fetch_dynamic_page(
            url="https://www.example.com",
            wait_time=3,
            wait_selector="body"  # 等待body元素加载
        )
        
        if result["success"]:
            print(f"✅ 成功抓取: {result['title']}")
            print(f"   页面长度: {result['text_length']} 字符")
        else:
            print(f"❌ 失败: {result['error']}")


# ==================== 示例2: Selenium交互操作 ====================

def example_selenium_interaction():
    """示例2: Selenium点击、填写表单等交互操作"""
    print("\n=== 示例2: Selenium交互操作 ===")
    
    from mcp_servers.crawlers.selenium_crawler import SeleniumCrawler
    
    with SeleniumCrawler(headless=False) as crawler:  # 显示浏览器窗口
        # 访问登录页面
        crawler.fetch_dynamic_page("https://example.com/login")
        
        # 填写用户名
        result = crawler.fill_input("#username", "test_user", by="css")
        print(f"填写用户名: {result['success']}")
        
        # 填写密码
        result = crawler.fill_input("#password", "test_pass", by="css")
        print(f"填写密码: {result['success']}")
        
        # 点击登录按钮
        result = crawler.click_element("#login-button", by="css")
        print(f"点击登录: {result['success']}")
        
        # 等待页面跳转
        import time
        time.sleep(2)
        
        # 提取登录后的内容
        result = crawler.extract_elements(".welcome-message", attribute="text")
        if result["success"]:
            print(f"提取到 {result['count']} 个元素")


# ==================== 示例3: Selenium提取数据 ====================

def example_selenium_extract():
    """示例3: 使用Selenium提取页面数据"""
    print("\n=== 示例3: Selenium提取数据 ===")
    
    from mcp_servers.crawlers.selenium_crawler import SeleniumCrawler
    
    with SeleniumCrawler(headless=True) as crawler:
        # 访问股票列表页面（示例）
        crawler.fetch_dynamic_page(
            "https://quote.eastmoney.com/center/gridlist.html#hs_a_board",
            wait_selector=".listview"
        )
        
        # 提取股票名称和价格
        stocks = crawler.extract_elements(".stock-name", attribute="text")
        prices = crawler.extract_elements(".stock-price", attribute="text")
        
        print(f"提取到 {stocks['count']} 只股票")
        for i, stock in enumerate(stocks["elements"][:5]):  # 只显示前5个
            price = prices["elements"][i]["value"] if i < len(prices["elements"]) else "N/A"
            print(f"  {stock['value']}: {price}")


# ==================== 示例4: Lavague AI自动化 ====================

def example_lavague_basic():
    """示例4: 使用Lavague执行自然语言指令"""
    print("\n=== 示例4: Lavague AI自动化 ===")
    
    try:
        from mcp_servers.crawlers.lavague_crawler import LavagueCrawler
        
        with LavagueCrawler(headless=True) as crawler:
            # 导航到页面
            crawler.navigate("https://www.example.com")
            
            # 使用自然语言执行操作
            result = crawler.execute_instruction(
                "点击登录按钮，填写用户名test和密码123456，然后点击提交",
                max_actions=10
            )
            
            if result["success"]:
                print(f"✅ 指令执行成功")
                print(f"   执行了 {result.get('actions_executed', 0)} 个动作")
                print(f"   当前页面: {result['title']}")
            else:
                print(f"❌ 执行失败: {result['error']}")
                
    except ImportError:
        print("⚠️ Lavague未安装，跳过此示例")
        print("   安装命令: pip install lavague")


# ==================== 示例5: Lavague数据提取 ====================

def example_lavague_extract():
    """示例5: 使用Lavague提取结构化数据"""
    print("\n=== 示例5: Lavague数据提取 ===")
    
    try:
        from mcp_servers.crawlers.lavague_crawler import LavagueCrawler
        
        with LavagueCrawler(headless=True) as crawler:
            # 导航到数据页面
            crawler.navigate("https://example.com/products")
            
            # 使用自然语言描述要提取的数据
            result = crawler.extract_data(
                "提取所有产品的名称、价格和评分，格式为JSON"
            )
            
            if result["success"]:
                print(f"✅ 数据提取成功")
                print(f"   提取结果: {result['data'][:200]}...")  # 只显示前200字符
            else:
                print(f"❌ 提取失败: {result['error']}")
                
    except ImportError:
        print("⚠️ Lavague未安装，跳过此示例")


# ==================== 示例6: 通过MCP工具调用 ====================

async def example_mcp_tools():
    """示例6: 通过MCP工具调用（在Cursor IDE中使用）"""
    print("\n=== 示例6: MCP工具调用示例 ===")
    print("在Cursor IDE中，可以直接调用以下MCP工具：")
    print()
    print("1. Selenium抓取动态页面:")
    print('   await call_mcp("crawler.selenium.fetch", {')
    print('       "url": "https://example.com",')
    print('       "wait_time": 3,')
    print('       "wait_selector": ".content"')
    print('   })')
    print()
    print("2. Selenium点击元素:")
    print('   await call_mcp("crawler.selenium.click", {')
    print('       "selector": "#login-button",')
    print('       "by": "css"')
    print('   })')
    print()
    print("3. Lavague执行指令:")
    print('   await call_mcp("crawler.lavague.execute", {')
    print('       "url": "https://example.com",')
    print('       "instruction": "点击登录按钮并填写表单"')
    print('   })')
    print()
    print("4. Lavague提取数据:")
    print('   await call_mcp("crawler.lavague.extract", {')
    print('       "url": "https://example.com/products",')
    print('       "description": "提取所有产品名称和价格"')
    print('   })')


# ==================== 示例7: 实际应用场景 ====================

def example_real_world_scenario():
    """示例7: 实际应用场景 - 爬取股票公告"""
    print("\n=== 示例7: 实际应用场景 ===")
    print("场景: 爬取东方财富网的股票公告（需要JavaScript渲染）")
    print()
    
    from mcp_servers.crawlers.selenium_crawler import SeleniumCrawler
    
    with SeleniumCrawler(headless=True) as crawler:
        # 访问东方财富公告页面
        url = "http://data.eastmoney.com/notices/stock/000001.html"
        result = crawler.fetch_dynamic_page(
            url,
            wait_time=5,
            wait_selector=".notice-list"  # 等待公告列表加载
        )
        
        if result["success"]:
            # 提取公告标题
            titles = crawler.extract_elements(
                ".notice-title",
                attribute="text"
            )
            
            # 提取公告日期
            dates = crawler.extract_elements(
                ".notice-date",
                attribute="text"
            )
            
            print(f"✅ 成功提取 {titles['count']} 条公告")
            for i, title in enumerate(titles["elements"][:5]):
                date = dates["elements"][i]["value"] if i < len(dates["elements"]) else ""
                print(f"  {date}: {title['value']}")


# ==================== 主函数 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("Selenium和Lavague爬虫工具使用示例")
    print("=" * 60)
    
    # 运行示例
    try:
        example_selenium_basic()
    except Exception as e:
        print(f"示例1失败: {e}")
    
    try:
        example_selenium_extract()
    except Exception as e:
        print(f"示例3失败: {e}")
    
    try:
        example_lavague_basic()
    except Exception as e:
        print(f"示例4失败: {e}")
    
    try:
        example_lavague_extract()
    except Exception as e:
        print(f"示例5失败: {e}")
    
    asyncio.run(example_mcp_tools())
    
    try:
        example_real_world_scenario()
    except Exception as e:
        print(f"示例7失败: {e}")
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)












































