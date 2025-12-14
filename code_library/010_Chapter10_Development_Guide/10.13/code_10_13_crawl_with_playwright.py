"""
文件名: code_10_13_crawl_with_playwright.py
保存路径: code_library/010_Chapter10_Development_Guide/10.13/code_10_13_crawl_with_playwright.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.13_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: crawl_with_playwright

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from playwright.sync_api import sync_playwright
from pathlib import Path

def crawl_with_playwright(url: str, output_dir: Path):
        """
    crawl_with_playwright函数
    
    **设计原理**：
    - **核心功能**：实现crawl_with_playwright的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面
        page.goto(url)
        
        # 等待内容加载
        page.wait_for_selector('body')
        
        # 获取内容
        content = page.content()
        text = page.inner_text('body')
        
        # 保存
        output_file = output_dir / "page.html"
        output_file.write_text(content, encoding='utf-8')
        
        browser.close()