#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 知识库爬虫工具
====================

支持多源数据抓取：
1. 网页内容（使用MCP工具或Playwright）
2. PDF文档（需要PDF解析库）
3. Markdown文件

运行: python scripts/kb/kb_crawler.py --url <URL> --platform <平台名>
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger('KBCrawler')

# 导入知识库构建器
from scripts.kb.kb_builder import KnowledgeBaseBuilder


class KnowledgeCrawler:
    """知识爬虫"""
    
    def __init__(self):
        self.builder = KnowledgeBaseBuilder()
    
    def crawl_with_playwright(self, url: str, wait_time: int = 5) -> Dict[str, Any]:
        """使用Playwright爬取网页"""
        try:
            from playwright.async_api import async_playwright
            
            async def fetch():
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True, timeout=30000)
                    page = await browser.new_page()
                    
                    try:
                        await page.goto(url, wait_until='networkidle', timeout=60000)
                        await page.wait_for_timeout(wait_time * 1000)
                        
                        html = await page.content()
                        title = await page.title()
                        text = await page.inner_text('body')
                        
                        await browser.close()
                        
                        return {
                            "success": True,
                            "url": url,
                            "title": title,
                            "html": html,
                            "text": text
                        }
                    except Exception as e:
                        await browser.close()
                        raise e
            
            return asyncio.run(fetch())
            
        except ImportError:
            logger.error("Playwright未安装，请运行: pip install playwright && playwright install chromium")
            return {"success": False, "error": "Playwright未安装"}
        except Exception as e:
            logger.error(f"Playwright爬取失败: {e}")
            return {"success": False, "error": str(e)}
    
    def crawl_with_mcp(self, url: str) -> Dict[str, Any]:
        """使用MCP工具爬取网页"""
        try:
            from core.mcp.client import MCPClient
            
            client = MCPClient()
            
            # 尝试使用Selenium工具
            result = client.call(
                tool_name='crawler.selenium.fetch',
                arguments={
                    'url': url,
                    'wait_time': 10,
                    'headless': True
                },
                timeout=60.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    import json
                    data = json.loads(data)
                
                if data.get('success'):
                    return {
                        "success": True,
                        "url": url,
                        "html": data.get('html', ''),
                        "text": data.get('text', ''),
                        "title": data.get('title', '')
                    }
            
            return {"success": False, "error": "MCP工具爬取失败"}
            
        except Exception as e:
            logger.error(f"MCP工具爬取失败: {e}")
            return {"success": False, "error": str(e)}
    
    def crawl_web(self, url: str, method: str = "playwright") -> Dict[str, Any]:
        """爬取网页"""
        logger.info(f"🕷️ 爬取网页: {url}")
        
        if method == "playwright":
            return self.crawl_with_playwright(url)
        elif method == "mcp":
            return self.crawl_with_mcp(url)
        else:
            return {"success": False, "error": f"未知方法: {method}"}
    
    def crawl_and_save(
        self,
        url: str,
        platform: str = "",
        method: str = "playwright"
    ) -> List[str]:
        """
        爬取并保存到知识库
        
        Args:
            url: 目标URL
            platform: 平台名称（如JoinQuant、BulletTrade、PTrade、QMT）
            method: 爬取方法（playwright/mcp）
            
        Returns:
            添加的知识条目ID列表
        """
        # 爬取
        result = self.crawl_web(url, method=method)
        
        if not result.get("success"):
            logger.error(f"❌ 爬取失败: {result.get('error', 'Unknown error')}")
            return []
        
        # 处理并保存
        html = result.get("html", "")
        kb_ids = self.builder.process_crawled_data(
            url=url,
            raw_content=html,
            source_type="web",
            platform=platform
        )
        
        logger.info(f"✅ 已添加 {len(kb_ids)} 条知识条目")
        return kb_ids


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="TRQuant 知识库爬虫工具")
    parser.add_argument("--url", type=str, required=True, help="目标URL")
    parser.add_argument("--platform", type=str, default="", help="平台名称（JoinQuant/BulletTrade/PTrade/QMT）")
    parser.add_argument("--method", type=str, default="playwright", choices=["playwright", "mcp"], help="爬取方法")
    parser.add_argument("--build-index", action="store_true", help="爬取后构建向量索引")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("TRQuant 知识库爬虫工具")
    print("=" * 70)
    print()
    
    crawler = KnowledgeCrawler()
    
    # 爬取并保存
    kb_ids = crawler.crawl_and_save(
        url=args.url,
        platform=args.platform,
        method=args.method
    )
    
    if kb_ids:
        print(f"✅ 成功添加 {len(kb_ids)} 条知识条目")
        
        # 构建向量索引
        if args.build_index:
            print()
            print("🔨 构建向量索引...")
            result = crawler.builder.build_vector_index(force_rebuild=False)
            if result.get("success"):
                print(f"✅ 向量索引构建成功")
            else:
                print(f"❌ 向量索引构建失败: {result.get('error', 'Unknown error')}")
    else:
        print("❌ 未添加任何知识条目")
    
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
