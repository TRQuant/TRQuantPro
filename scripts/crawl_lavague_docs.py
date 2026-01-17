#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬取LaVague官方文档，整理功能和应用场景
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import (
    crawler_fetch,
    crawler_selenium_fetch,
    crawler_search_docs
)

def crawl_lavague_docs():
    """爬取LaVague官方文档"""
    
    print("=" * 80)
    print("LaVague 官方文档爬取")
    print("=" * 80)
    print()
    
    results = {
        "crawl_time": datetime.now().isoformat(),
        "sources": [],
        "features": [],
        "use_cases": [],
        "trquant_applications": []
    }
    
    # 1. 爬取官网首页
    print("【1. 爬取官网首页】")
    print("-" * 80)
    try:
        result = crawler_selenium_fetch(
            url="https://www.lavague.ai",
            wait_time=5,
            headless=True
        )
        if result.get("success"):
            results["sources"].append({
                "url": "https://www.lavague.ai",
                "type": "homepage",
                "content_length": len(result.get("text", "")),
                "title": result.get("title", "")
            })
            print(f"✅ 成功爬取官网首页: {result.get('title')}")
            print(f"   内容长度: {len(result.get('text', ''))} 字符")
        else:
            print(f"❌ 失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    print()
    
    # 2. 爬取文档首页
    print("【2. 爬取文档首页】")
    print("-" * 80)
    try:
        result = crawler_selenium_fetch(
            url="https://docs.lavague.ai",
            wait_time=5,
            headless=True
        )
        if result.get("success"):
            results["sources"].append({
                "url": "https://docs.lavague.ai",
                "type": "docs_homepage",
                "content_length": len(result.get("text", "")),
                "title": result.get("title", "")
            })
            print(f"✅ 成功爬取文档首页: {result.get('title')}")
            print(f"   内容长度: {len(result.get('text', ''))} 字符")
        else:
            print(f"❌ 失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 异常: {e}")
    print()
    
    # 3. 爬取快速开始文档
    print("【3. 爬取快速开始文档】")
    print("-" * 80)
    quick_start_urls = [
        "https://docs.lavague.ai/en/latest/docs/get-started/quick-tour/",
        "https://docs.lavague.ai/en/latest/docs/get-started/installation/",
        "https://docs.lavague.ai/en/latest/docs/get-started/troubleshoot/",
    ]
    
    for url in quick_start_urls:
        try:
            result = crawler_selenium_fetch(url=url, wait_time=5, headless=True)
            if result.get("success"):
                results["sources"].append({
                    "url": url,
                    "type": "quick_start",
                    "content_length": len(result.get("text", "")),
                    "title": result.get("title", ""),
                    "text": result.get("text", "")[:5000]  # 保存前5000字符
                })
                print(f"✅ 成功: {url}")
            else:
                print(f"❌ 失败: {url} - {result.get('error')}")
        except Exception as e:
            print(f"❌ 异常: {url} - {e}")
    print()
    
    # 4. 搜索LaVague功能特性
    print("【4. 搜索LaVague功能特性】")
    print("-" * 80)
    search_queries = [
        "lavague features capabilities",
        "lavague use cases examples",
        "lavague ActionEngine WorldModel",
        "lavague web automation"
    ]
    
    for query in search_queries:
        try:
            result = crawler_search_docs(query=query, site="docs.lavague.ai")
            if result.get("success"):
                results["sources"].append({
                    "query": query,
                    "type": "search",
                    "results_count": len(result.get("results", [])),
                    "results": result.get("results", [])[:5]  # 前5个结果
                })
                print(f"✅ 搜索成功: {query} - 找到 {len(result.get('results', []))} 个结果")
            else:
                print(f"❌ 搜索失败: {query}")
        except Exception as e:
            print(f"❌ 异常: {query} - {e}")
    print()
    
    # 5. 保存结果
    output_file = TRQUANT_ROOT / "docs" / "LAVAGUE_DOCS_CRAWL_RESULTS.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("=" * 80)
    print(f"爬取完成，结果已保存到: {output_file}")
    print(f"共爬取 {len(results['sources'])} 个来源")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    crawl_lavague_docs()
