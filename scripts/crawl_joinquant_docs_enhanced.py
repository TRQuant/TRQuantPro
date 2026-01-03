#!/usr/bin/env python3
"""
聚宽API文档完整爬取脚本（增强版）

使用开源爬虫工具：
- Playwright: 处理JavaScript渲染页面
- Scrapy: 大规模爬取（可选）

Author: TRQuant Team
Date: 2025-12-19
"""

import sys
import os
import time
import json
from datetime import datetime
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 检查并导入Playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright未安装，将使用requests（无法处理JS页面）")
    print("   安装: pip install playwright && playwright install chromium")

# 基础URL
BASE_URL = "https://www.joinquant.com"
API_BASE = "https://www.joinquant.com/help/api"

# 要爬取的页面列表
PAGES_TO_CRAWL = [
    # 主页面
    "/help/api/help?name=api",
    "/help/api/help?name=JQData",
    "/help/api/guide",
    
    # API分类页面
    "/help/api/help#api:开始写策略",
    "/help/api/help#api:数据获取",
    "/help/api/help#api:交易执行",
    "/help/api/help#api:策略设置",
    "/help/api/help#api:回测框架",
    
    # JQData文档
    "/help/api/doc?name=JQDatadoc",
    "/help/api/doc?name=JQDatadoc&id=9883",  # get_fundamentals
    "/help/api/doc?name=JQDatadoc&id=10764",  # get_price
    "/help/api/doc?name=JQDatadoc&id=10261",  # 数据范围
    "/help/api/doc?name=JQDatadoc&id=10285",  # 报告期接口
    "/help/api/doc?name=JQDatadoc&id=9884",   # valuation
]

def fetch_page_requests(url, retry=3):
    """使用requests获取页面（简单页面）"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for i in range(retry):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response.text
        except Exception as e:
            if i == retry - 1:
                print(f"  ❌ 获取失败: {e}")
            else:
                time.sleep(1)
    return None

def fetch_page_playwright(url, wait_time=3000):
    """使用Playwright获取页面（JavaScript渲染）"""
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 访问页面
            page.goto(url, wait_until='networkidle', timeout=60000)
            
            # 等待页面加载
            page.wait_for_timeout(wait_time)
            
            # 获取HTML
            html = page.content()
            
            browser.close()
            return html
    except Exception as e:
        print(f"  ❌ Playwright获取失败: {e}")
        return None

def extract_links(html, base_url):
    """提取页面中的所有链接"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if 'joinquant.com' in full_url and '/help/api' in full_url:
            links.add(full_url)
    
    return list(links)

def extract_text(html):
    """提取页面文本内容"""
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    for script in soup(["script", "style"]):
        script.decompose()
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def crawl_all_pages():
    """爬取所有页面"""
    print("=" * 70)
    print("聚宽API文档完整爬取（增强版）")
    print("=" * 70)
    print()
    
    if PLAYWRIGHT_AVAILABLE:
        print("✅ 使用Playwright处理JavaScript页面")
    else:
        print("⚠️ 使用requests（无法处理JS页面）")
    print()
    
    all_pages = {}
    all_links = set()
    crawled_urls = set()
    
    # 第一步：爬取初始页面列表
    print("📡 Step 1: 爬取初始页面列表...")
    print("-" * 50)
    
    for page_path in PAGES_TO_CRAWL:
        url = urljoin(BASE_URL, page_path)
        print(f"  爬取: {url}")
        
        # 先尝试requests（快速）
        html = fetch_page_requests(url)
        
        # 如果为空且Playwright可用，使用Playwright
        if (not html or len(extract_text(html)) < 100) and PLAYWRIGHT_AVAILABLE:
            print("    ⚠️ 内容为空，使用Playwright...")
            html = fetch_page_playwright(url)
        
        if html:
            text = extract_text(html)
            links = extract_links(html, BASE_URL)
            
            all_pages[url] = {
                "url": url,
                "text": text,
                "links": links,
                "crawled_at": datetime.now().isoformat(),
                "method": "playwright" if PLAYWRIGHT_AVAILABLE and len(text) > 100 else "requests"
            }
            
            all_links.update(links)
            crawled_urls.add(url)
            print(f"    ✅ 成功 (文本: {len(text)}, 链接: {len(links)})")
        else:
            print(f"    ❌ 失败")
        time.sleep(1)
    
    print(f"\n  初始页面: {len(all_pages)} 个")
    print(f"  发现链接: {len(all_links)} 个")
    print()
    
    # 第二步：爬取发现的链接（限制数量）
    print("📡 Step 2: 爬取发现的链接页面...")
    print("-" * 50)
    
    new_links = list(all_links - crawled_urls)[:20]  # 限制20个
    print(f"  待爬取: {len(new_links)} 个")
    
    for i, url in enumerate(new_links, 1):
        if url in crawled_urls:
            continue
        
        print(f"  [{i}/{len(new_links)}] {url}")
        
        # 优先使用Playwright（处理JS）
        if PLAYWRIGHT_AVAILABLE:
            html = fetch_page_playwright(url)
        else:
            html = fetch_page_requests(url)
        
        if html:
            text = extract_text(html)
            links = extract_links(html, BASE_URL)
            
            all_pages[url] = {
                "url": url,
                "text": text,
                "links": links,
                "crawled_at": datetime.now().isoformat(),
                "method": "playwright" if PLAYWRIGHT_AVAILABLE else "requests"
            }
            
            all_links.update(links)
            crawled_urls.add(url)
            print(f"    ✅ 成功 (文本: {len(text)}, 链接: {len(links)})")
        else:
            print(f"    ❌ 失败")
        
        time.sleep(0.5)
    
    print(f"\n  总计页面: {len(all_pages)} 个")
    print()
    
    # 第三步：保存结果
    print("💾 Step 3: 保存爬取结果...")
    print("-" * 50)
    
    output_dir = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存JSON
    json_file = os.path.join(output_dir, "all_pages_enhanced.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_pages, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON: {json_file}")
    
    # 保存文本摘要
    summary_file = os.path.join(output_dir, "summary_enhanced.md")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# 聚宽API文档爬取摘要（增强版）\n\n")
        f.write(f"> **爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> **总页面数**: {len(all_pages)}\n")
        f.write(f"> **使用工具**: {'Playwright + requests' if PLAYWRIGHT_AVAILABLE else 'requests'}\n\n")
        f.write("## 页面列表\n\n")
        
        for url, data in all_pages.items():
            f.write(f"### {url}\n\n")
            f.write(f"- **文本长度**: {len(data['text'])} 字符\n")
            f.write(f"- **链接数**: {len(data['links'])}\n")
            f.write(f"- **爬取方法**: {data.get('method', 'unknown')}\n")
            f.write(f"- **爬取时间**: {data['crawled_at']}\n\n")
            if len(data['text']) > 0:
                f.write(f"**内容摘要**:\n```\n{data['text'][:500]}...\n```\n\n")
            f.write("---\n\n")
    
    print(f"  ✅ 摘要: {summary_file}")
    
    # 保存每个页面的文本
    texts_dir = os.path.join(output_dir, "texts_enhanced")
    os.makedirs(texts_dir, exist_ok=True)
    
    for url, data in all_pages.items():
        parsed = urlparse(url)
        filename = parsed.path.replace('/', '_').replace('?', '_').replace('=', '_')
        if len(filename) > 100:
            filename = filename[:100]
        filename = filename.strip('_') + '.txt'
        
        text_file = os.path.join(texts_dir, filename)
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Method: {data.get('method', 'unknown')}\n")
            f.write(f"Crawled: {data['crawled_at']}\n")
            f.write("=" * 70 + "\n\n")
            f.write(data['text'])
    
    print(f"  ✅ 文本文件: {texts_dir}/ ({len(all_pages)} 个文件)")
    print()
    
    # 统计
    playwright_count = sum(1 for p in all_pages.values() if p.get('method') == 'playwright')
    requests_count = sum(1 for p in all_pages.values() if p.get('method') == 'requests')
    
    print("=" * 70)
    print("📊 爬取总结")
    print("=" * 70)
    print(f"""
总页面数: {len(all_pages)}
  - Playwright: {playwright_count} 个
  - requests: {requests_count} 个
总链接数: {len(all_links)}
已爬取: {len(crawled_urls)}

输出目录: {output_dir}
  - all_pages_enhanced.json: 所有页面数据
  - summary_enhanced.md: 爬取摘要
  - texts_enhanced/: 各页面文本文件

爬取完成!
""")
    
    return all_pages

if __name__ == "__main__":
    try:
        all_pages = crawl_all_pages()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

