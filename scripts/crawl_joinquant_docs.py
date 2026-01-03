#!/usr/bin/env python3
"""
聚宽API文档完整爬取脚本

功能:
1. 爬取聚宽API文档所有页面
2. 提取所有链接
3. 批量下载所有相关页面
4. 统一构建知识库

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
    "/help/api/doc?name=JQDatadoc&id=9886",   # 存量性质
]

def fetch_page(url, retry=3):
    """获取页面内容"""
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

def extract_links(html, base_url):
    """提取页面中的所有链接"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    # 提取所有a标签
    for a in soup.find_all('a', href=True):
        href = a['href']
        # 转换为绝对URL
        full_url = urljoin(base_url, href)
        # 只保留joinquant.com的链接
        if 'joinquant.com' in full_url and '/help/api' in full_url:
            links.add(full_url)
    
    return list(links)

def extract_text(html):
    """提取页面文本内容"""
    if not html:
        return ""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 移除script和style标签
    for script in soup(["script", "style"]):
        script.decompose()
    
    # 获取文本
    text = soup.get_text()
    
    # 清理文本
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def crawl_all_pages():
    """爬取所有页面"""
    print("=" * 70)
    print("聚宽API文档完整爬取")
    print("=" * 70)
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
        
        html = fetch_page(url)
        if html:
            text = extract_text(html)
            links = extract_links(html, BASE_URL)
            
            all_pages[url] = {
                "url": url,
                "text": text,
                "links": links,
                "crawled_at": datetime.now().isoformat()
            }
            
            all_links.update(links)
            crawled_urls.add(url)
            print(f"    ✅ 成功 (文本长度: {len(text)}, 链接数: {len(links)})")
        else:
            print(f"    ❌ 失败")
        time.sleep(1)  # 避免请求过快
    
    print(f"\n  初始页面: {len(all_pages)} 个")
    print(f"  发现链接: {len(all_links)} 个")
    print()
    
    # 第二步：爬取所有发现的链接
    print("📡 Step 2: 爬取发现的链接页面...")
    print("-" * 50)
    
    new_links = all_links - crawled_urls
    print(f"  待爬取: {len(new_links)} 个")
    
    for i, url in enumerate(new_links, 1):
        if url in crawled_urls:
            continue
        
        print(f"  [{i}/{len(new_links)}] {url}")
        
        html = fetch_page(url)
        if html:
            text = extract_text(html)
            links = extract_links(html, BASE_URL)
            
            all_pages[url] = {
                "url": url,
                "text": text,
                "links": links,
                "crawled_at": datetime.now().isoformat()
            }
            
            all_links.update(links)
            crawled_urls.add(url)
            print(f"    ✅ 成功 (文本: {len(text)}, 链接: {len(links)})")
        else:
            print(f"    ❌ 失败")
        
        time.sleep(0.5)  # 避免请求过快
        
        # 限制爬取数量（避免过多）
        if i >= 50:
            print(f"  ⚠️ 已爬取50个页面，停止")
            break
    
    print(f"\n  总计页面: {len(all_pages)} 个")
    print()
    
    # 第三步：保存结果
    print("💾 Step 3: 保存爬取结果...")
    print("-" * 50)
    
    output_dir = "/home/taotao/dev/QuantTest/TRQuant/docs/joinquant_crawled"
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存JSON
    json_file = os.path.join(output_dir, "all_pages.json")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(all_pages, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON: {json_file}")
    
    # 保存文本摘要
    summary_file = os.path.join(output_dir, "summary.md")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# 聚宽API文档爬取摘要\n\n")
        f.write(f"> **爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> **总页面数**: {len(all_pages)}\n\n")
        f.write("## 页面列表\n\n")
        
        for url, data in all_pages.items():
            f.write(f"### {url}\n\n")
            f.write(f"- **文本长度**: {len(data['text'])} 字符\n")
            f.write(f"- **链接数**: {len(data['links'])}\n")
            f.write(f"- **爬取时间**: {data['crawled_at']}\n\n")
            f.write(f"**内容摘要**:\n```\n{data['text'][:500]}...\n```\n\n")
            f.write("---\n\n")
    
    print(f"  ✅ 摘要: {summary_file}")
    
    # 保存每个页面的文本
    texts_dir = os.path.join(output_dir, "texts")
    os.makedirs(texts_dir, exist_ok=True)
    
    for url, data in all_pages.items():
        # 生成文件名
        parsed = urlparse(url)
        filename = parsed.path.replace('/', '_').replace('?', '_').replace('=', '_')
        if len(filename) > 100:
            filename = filename[:100]
        filename = filename.strip('_') + '.txt'
        
        text_file = os.path.join(texts_dir, filename)
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(f"Crawled: {data['crawled_at']}\n")
            f.write("=" * 70 + "\n\n")
            f.write(data['text'])
    
    print(f"  ✅ 文本文件: {texts_dir}/ ({len(all_pages)} 个文件)")
    print()
    
    # 第四步：生成知识库条目
    print("📚 Step 4: 生成知识库条目...")
    print("-" * 50)
    
    # 按主题分类
    knowledge_entries = []
    
    # 策略编写相关
    strategy_pages = [url for url in all_pages.keys() if '策略' in all_pages[url]['text'][:1000] or 'strategy' in url.lower()]
    if strategy_pages:
        knowledge_entries.append({
            "title": "聚宽策略编写指南",
            "content": "\n\n".join([f"**{url}**\n{all_pages[url]['text'][:2000]}" for url in strategy_pages[:5]]),
            "type": "guide",
            "tags": ["joinquant", "strategy", "guide"]
        })
    
    # 数据获取相关
    data_pages = [url for url in all_pages.keys() if '数据' in all_pages[url]['text'][:1000] or 'data' in url.lower() or 'get_' in url]
    if data_pages:
        knowledge_entries.append({
            "title": "聚宽数据获取API完整文档",
            "content": "\n\n".join([f"**{url}**\n{all_pages[url]['text'][:2000]}" for url in data_pages[:10]]),
            "type": "api",
            "tags": ["joinquant", "data", "api"]
        })
    
    # 回测相关
    backtest_pages = [url for url in all_pages.keys() if '回测' in all_pages[url]['text'][:1000] or 'backtest' in url.lower()]
    if backtest_pages:
        knowledge_entries.append({
            "title": "聚宽回测框架完整文档",
            "content": "\n\n".join([f"**{url}**\n{all_pages[url]['text'][:2000]}" for url in backtest_pages[:5]]),
            "type": "guide",
            "tags": ["joinquant", "backtest", "framework"]
        })
    
    # 保存知识库条目
    kb_file = os.path.join(output_dir, "knowledge_entries.json")
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_entries, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 知识库条目: {len(knowledge_entries)} 个")
    print(f"  ✅ 保存到: {kb_file}")
    print()
    
    # 总结
    print("=" * 70)
    print("📊 爬取总结")
    print("=" * 70)
    print(f"""
总页面数: {len(all_pages)}
总链接数: {len(all_links)}
已爬取: {len(crawled_urls)}
知识库条目: {len(knowledge_entries)}

输出目录: {output_dir}
  - all_pages.json: 所有页面数据
  - summary.md: 爬取摘要
  - texts/: 各页面文本文件
  - knowledge_entries.json: 知识库条目

爬取完成!
""")
    
    return all_pages, knowledge_entries

if __name__ == "__main__":
    try:
        all_pages, knowledge_entries = crawl_all_pages()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

