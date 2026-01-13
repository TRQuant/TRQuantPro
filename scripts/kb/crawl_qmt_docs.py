#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
QMT文档完整爬取脚本
==================

爬取所有QMT相关网页并构建知识库：
1. QMT官方文档
2. xtquant API文档
3. QMT教程和示例
4. QMT相关博客文章

运行: python scripts/kb/crawl_qmt_docs.py
"""

import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
import time

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('QMTDocCrawler')

# 导入知识库爬虫
from scripts.kb.kb_crawler import KnowledgeCrawler

# QMT相关URL列表
QMT_URLS = [
    # QMT官方文档（ptradeapi.com）
    {
        "url": "http://qmt.ptradeapi.com/",
        "title": "QMT Python API 接口文档",
        "category": "official"
    },
    # QMT官方文档（ThinkTrader）
    {
        "url": "https://dict.thinktrader.net/",
        "title": "QMT官方文档（ThinkTrader）",
        "category": "official"
    },
    {
        "url": "https://dict.thinktrader.net/nativeApi/",
        "title": "xtquant API文档",
        "category": "api"
    },
    # QMT教程和博客
    {
        "url": "https://www.cnblogs.com/bigleft/p/18286458",
        "title": "量化交易系统QMT与PTrade的区别",
        "category": "tutorial"
    },
]


def discover_qmt_pages(base_url: str = "http://qmt.ptradeapi.com/") -> List[Dict[str, str]]:
    """
    自动发现QMT文档网站的所有页面
    
    Args:
        base_url: 基础URL
        
    Returns:
        发现的页面列表
    """
    try:
        from playwright.async_api import async_playwright
        import asyncio
        
        async def discover():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True, timeout=30000)
                page = await browser.new_page()
                
                try:
                    await page.goto(base_url, wait_until='networkidle', timeout=60000)
                    await page.wait_for_timeout(3000)
                    
                    # 提取所有链接
                    links = await page.evaluate('''
                        () => {
                            const links = [];
                            const seen = new Set();
                            document.querySelectorAll('a[href]').forEach(a => {
                                const href = a.getAttribute('href');
                                const text = a.innerText.trim();
                                if (href && text && !href.startsWith('javascript:') && !href.startsWith('#')) {
                                    let fullUrl = href;
                                    if (href.startsWith('/')) {
                                        fullUrl = 'http://qmt.ptradeapi.com' + href;
                                    } else if (!href.startsWith('http')) {
                                        fullUrl = 'http://qmt.ptradeapi.com/' + href;
                                    }
                                    
                                    // 只收集qmt.ptradeapi.com的链接
                                    if (fullUrl.startsWith('http://qmt.ptradeapi.com') && !seen.has(fullUrl)) {
                                        seen.add(fullUrl);
                                        links.push({text: text, url: fullUrl});
                                    }
                                }
                            });
                            return links;
                        }
                    ''')
                    
                    await browser.close()
                    return links
                except Exception as e:
                    await browser.close()
                    raise e
        
        return asyncio.run(discover())
        
    except Exception as e:
        logger.error(f"发现页面失败: {e}")
        return []


def crawl_qmt_docs(method: str = "playwright", build_index: bool = True, discover: bool = True) -> Dict[str, Any]:
    """
    爬取所有QMT相关文档
    
    Args:
        method: 爬取方法（playwright/mcp）
        build_index: 是否构建向量索引
        discover: 是否自动发现页面
        
    Returns:
        爬取结果统计
    """
    crawler = KnowledgeCrawler()
    
    # 如果启用自动发现，从QMT文档网站发现所有页面
    urls_to_crawl = QMT_URLS.copy()
    
    if discover:
        print("🔍 自动发现QMT文档页面...")
        discovered_links = discover_qmt_pages("http://qmt.ptradeapi.com/")
        
        if discovered_links:
            print(f"   发现 {len(discovered_links)} 个页面")
            # 添加发现的页面（去重）
            seen_urls = {item["url"] for item in urls_to_crawl}
            for link in discovered_links:
                if link["url"] not in seen_urls:
                    urls_to_crawl.append({
                        "url": link["url"],
                        "title": link["text"],
                        "category": "discovered"
                    })
                    seen_urls.add(link["url"])
            print(f"   新增 {len(urls_to_crawl) - len(QMT_URLS)} 个页面")
        print()
    
    stats = {
        "total_urls": len(urls_to_crawl),
        "success": 0,
        "failed": 0,
        "kb_ids": [],
        "errors": []
    }
    
    print("=" * 70)
    print("🕷️ QMT文档完整爬取")
    print("=" * 70)
    print(f"共 {len(urls_to_crawl)} 个URL")
    print()
    
    for idx, item in enumerate(urls_to_crawl, 1):
        url = item["url"]
        title = item.get("title", url)
        category = item.get("category", "general")
        
        print(f"[{idx}/{len(QMT_URLS)}] {title}")
        print(f"   URL: {url}")
        print(f"   分类: {category}")
        
        try:
            kb_ids = crawler.crawl_and_save(
                url=url,
                platform="QMT",
                method=method
            )
            
            if kb_ids:
                stats["success"] += 1
                stats["kb_ids"].extend(kb_ids)
                print(f"   ✅ 成功添加 {len(kb_ids)} 条知识条目")
            else:
                stats["failed"] += 1
                error_msg = f"未添加任何知识条目: {url}"
                stats["errors"].append(error_msg)
                print(f"   ❌ {error_msg}")
            
            # 延迟，避免请求过快
            if idx < len(QMT_URLS):
                time.sleep(3)
                
        except Exception as e:
            logger.error(f"爬取失败: {url}, 错误: {e}")
            stats["failed"] += 1
            stats["errors"].append(f"{url}: {str(e)}")
    
    # 构建向量索引
    if build_index and stats["kb_ids"]:
        print()
        print("🔨 构建向量索引...")
        result = crawler.builder.build_vector_index(force_rebuild=False)
        if result.get("success"):
            print(f"✅ 向量索引构建成功")
            print(f"   - 条目数: {result.get('items_count', 0)}")
            print(f"   - 模型: {result.get('model', '')}")
            print(f"   - 向量维度: {result.get('embedding_dim', 0)}")
        else:
            print(f"❌ 向量索引构建失败: {result.get('error', 'Unknown error')}")
    
    return stats


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="QMT文档完整爬取")
    parser.add_argument(
        "--method",
        type=str,
        default="playwright",
        choices=["playwright", "mcp"],
        help="爬取方法"
    )
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="不构建向量索引"
    )
    parser.add_argument(
        "--no-discover",
        action="store_true",
        help="不自动发现页面（只爬取预设URL）"
    )
    
    args = parser.parse_args()
    
    # 爬取
    stats = crawl_qmt_docs(
        method=args.method,
        build_index=not args.no_index,
        discover=not args.no_discover
    )
    
    # 输出统计
    print()
    print("=" * 70)
    print("📊 爬取统计")
    print("=" * 70)
    print(f"总URL数: {stats['total_urls']}")
    print(f"成功: {stats['success']}")
    print(f"失败: {stats['failed']}")
    print(f"知识条目: {len(stats['kb_ids'])} 条")
    
    if stats["errors"]:
        print()
        print("❌ 错误列表:")
        for error in stats["errors"]:
            print(f"   - {error}")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
