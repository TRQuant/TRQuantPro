#!/usr/bin/env python3
"""
测试爬取"开始写策略"页面
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json

def test_crawl_strategy_page():
    """测试爬取开始写策略页面"""
    url = "https://www.joinquant.com/help/api/help#api:开始写策略"
    
    print("=" * 70)
    print("测试爬取: 开始写策略页面")
    print("=" * 70)
    print(f"URL: {url}")
    print()
    
    try:
        with sync_playwright() as p:
            print("🚀 启动浏览器...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print(f"📡 访问页面...")
            page.goto(url, wait_until='networkidle', timeout=60000)
            
            print("⏳ 等待页面加载...")
            page.wait_for_timeout(5000)  # 等待5秒确保JS加载完成
            
            # 检查页面标题
            title = page.title()
            print(f"📄 页面标题: {title}")
            
            # 获取HTML
            html = page.content()
            print(f"📦 HTML长度: {len(html)} 字符")
            
            # 提取文本
            soup = BeautifulSoup(html, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text()
            text_clean = ' '.join(text.split())
            print(f"📝 文本长度: {len(text_clean)} 字符")
            
            # 检查是否包含关键词
            keywords = ['策略', 'strategy', '开始', '写', '编写', '回测', 'initialize', 'handle_data']
            found_keywords = [kw for kw in keywords if kw in text_clean]
            print(f"🔍 找到关键词: {found_keywords}")
            
            # 保存HTML
            output_file = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled/test_strategy_page.html"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"💾 已保存HTML: {output_file}")
            
            # 保存文本
            text_file = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled/test_strategy_page.txt"
            with open(text_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"Title: {title}\n")
                f.write("=" * 70 + "\n\n")
                f.write(text_clean)
            print(f"💾 已保存文本: {text_file}")
            
            # 显示文本前500字符
            print("\n" + "=" * 70)
            print("📄 文本内容预览（前500字符）:")
            print("=" * 70)
            print(text_clean[:500])
            print("...")
            
            browser.close()
            
            print("\n" + "=" * 70)
            if len(text_clean) > 100:
                print("✅ 成功抓取到内容！")
            else:
                print("⚠️ 内容较少，可能页面需要特殊处理")
            print("=" * 70)
            
            return {
                "success": len(text_clean) > 100,
                "url": url,
                "title": title,
                "html_length": len(html),
                "text_length": len(text_clean),
                "keywords_found": found_keywords
            }
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_crawl_strategy_page()
    if result:
        print("\n📊 结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))

