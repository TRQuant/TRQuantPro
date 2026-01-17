#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽知识库全面爬取脚本（使用Selenium和Lavague）

使用新的爬虫工具：
- Selenium: 处理JavaScript渲染页面
- Lavague: 处理复杂交互页面（可选）
- 基础爬虫: 处理静态页面

Author: TRQuant Team
Date: 2025-12-24
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入MCP爬虫工具
try:
    from mcp_servers.unified_dev_server import (
        crawler_fetch,
        crawler_selenium_fetch,
        crawler_selenium_extract,
        crawler_lavague_execute,
    )
    CRAWLER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ MCP爬虫工具不可用: {e}")
    CRAWLER_AVAILABLE = False

# 聚宽基础URL
BASE_URL = "https://www.joinquant.com"
API_BASE = "https://www.joinquant.com/help/api"

# 要爬取的页面列表（分类）
PAGES_TO_CRAWL = {
    "api_docs": [
        # API主页面（需要JS渲染）
        "/help/api/help?name=api",
        "/help/api/help?name=JQData",
        "/help/api/index",
        
        # API分类
        "/help/api/help#api:开始写策略",
        "/help/api/help#api:数据获取",
        "/help/api/help#api:交易执行",
        "/help/api/help#api:策略设置",
        "/help/api/help#api:回测框架",
        "/help/api/help#api:因子分析",
        
        # 重要API函数文档
        "/help/api/doc?name=JQDatadoc&id=10764",  # get_price
        "/help/api/doc?name=JQDatadoc&id=9883",   # get_fundamentals
        "/help/api/doc?name=JQDatadoc&id=10261",  # 数据范围
        "/help/api/doc?name=JQDatadoc&id=10285",  # 报告期接口
        "/help/api/doc?name=JQDatadoc&id=9884",   # valuation
        "/help/api/doc?name=JQDatadoc&id=9842",   # 沪深A股
    ],
    "tutorials": [
        "/help/api/guide",  # 新手指引
        "/help/api/help?name=Strategy",  # 策略编写
        "/help/api/help?name=Factor",    # 因子分析
        "/help/api/help?name=Backtest",  # 回测框架
    ],
    "examples": [
        "/example",  # 策略示例
        "/strategy", # 策略库
    ],
    "data": [
        "/help/api/plateData",  # 行业概念数据
    ],
}

# 网络调研的教程资源
EXTERNAL_TUTORIALS = [
    "https://www.joinquant.com/help/api/guide",
    "https://www.joinquant.com/help/api/help?name=Strategy",
    # 可以添加更多外部教程链接
]

def fetch_with_best_tool(url: str, wait_selector: Optional[str] = None) -> Dict[str, Any]:
    """
    使用最佳工具抓取页面
    优先顺序：基础爬虫 -> Selenium -> Lavague
    """
    if not CRAWLER_AVAILABLE:
        return {"success": False, "error": "爬虫工具不可用"}
    
    print(f"  🔍 抓取: {url}")
    
    # 1. 先尝试基础爬虫（最快）
    try:
        result = crawler_fetch(url, extract_text=True, extract_links=True)
        if result.get("success") and result.get("text") and len(result.get("text", "")) > 500:
            print(f"    ✅ 基础爬虫成功 (文本: {len(result.get('text', ''))} 字符)")
            return result
    except Exception as e:
        print(f"    ⚠️ 基础爬虫失败: {e}")
    
    # 2. 使用Selenium（处理JS渲染）
    try:
        result = crawler_selenium_fetch(
            url=url,
            wait_time=10,
            wait_selector=wait_selector or "body",
            headless=True
        )
        if result.get("success"):
            # 提取文本（从HTML中提取）
            html = result.get("html", "")
            if html:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                # 移除script和style标签
                for script in soup(["script", "style"]):
                    script.decompose()
                result["text"] = soup.get_text(separator=" ", strip=True)
            
            print(f"    ✅ Selenium成功 (HTML: {len(result.get('html', ''))} 字符)")
            return result
    except Exception as e:
        print(f"    ⚠️ Selenium失败: {e}")
    
    # 3. 如果都失败，返回错误
    return {"success": False, "error": "所有爬虫工具都失败"}

def extract_api_links(html: str, base_url: str) -> List[str]:
    """从HTML中提取API文档链接"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    
    # 查找所有链接
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        
        # 过滤聚宽API相关链接
        if 'joinquant.com' in full_url and (
            '/help/api' in full_url or 
            '/example' in full_url or
            '/strategy' in full_url
        ):
            links.add(full_url)
    
    return list(links)

def crawl_category(category: str, urls: List[str]) -> Dict[str, Any]:
    """爬取一个分类的所有页面"""
    print(f"\n{'='*70}")
    print(f"📚 爬取分类: {category}")
    print(f"{'='*70}")
    
    all_pages = {}
    all_links = set()
    
    for i, page_path in enumerate(urls, 1):
        url = urljoin(BASE_URL, page_path)
        print(f"\n[{i}/{len(urls)}] {url}")
        
        # 抓取页面
        result = fetch_with_best_tool(url)
        
        if result.get("success"):
            # 提取链接
            html = result.get("html", result.get("text", ""))
            links = extract_api_links(html, BASE_URL)
            all_links.update(links)
            
            # 保存页面数据
            all_pages[url] = {
                "url": url,
                "title": result.get("title", ""),
                "text": result.get("text", ""),
                "html": result.get("html", ""),
                "links": links,
                "crawled_at": datetime.now().isoformat(),
                "category": category,
            }
            
            print(f"    ✅ 成功 (文本: {len(result.get('text', ''))}, 链接: {len(links)})")
        else:
            print(f"    ❌ 失败: {result.get('error', 'Unknown error')}")
        
        time.sleep(2)  # 避免请求过快
    
    return {
        "pages": all_pages,
        "links": list(all_links),
        "category": category,
    }

def save_to_knowledge_base(pages: Dict[str, Any], output_dir: Path):
    """将爬取的内容整理并保存为知识库格式"""
    print(f"\n{'='*70}")
    print("💾 整理知识库条目...")
    print(f"{'='*70}")
    
    knowledge_entries = []
    
    # 按分类整理
    categories = {}
    for url, data in pages.items():
        category = data.get("category", "other")
        if category not in categories:
            categories[category] = []
        categories[category].append(data)
    
    # 为每个分类创建知识库条目
    for category, items in categories.items():
        if not items:
            continue
        
        # 合并同类内容
        combined_content = []
        for item in items:
            content_section = f"## {item.get('title', item['url'])}\n\n"
            content_section += f"**URL**: {item['url']}\n\n"
            content_section += f"**内容**:\n{item.get('text', '')[:3000]}\n\n"
            combined_content.append(content_section)
        
        entry = {
            "title": f"聚宽{category}完整文档",
            "content": "\n---\n\n".join(combined_content),
            "type": "reference",
            "tags": ["joinquant", category, "api", "reference"],
            "urls": [item['url'] for item in items],
            "created_at": datetime.now().isoformat(),
        }
        knowledge_entries.append(entry)
        print(f"  ✅ {category}: {len(items)} 个页面")
    
    # 保存知识库JSON
    kb_file = output_dir / "knowledge_base.json"
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_entries, f, ensure_ascii=False, indent=2)
    
    print(f"\n  ✅ 知识库条目: {len(knowledge_entries)} 个")
    print(f"  ✅ 保存到: {kb_file}")
    
    return knowledge_entries

def main():
    """主函数"""
    print("=" * 70)
    print("🐉 聚宽知识库全面爬取（使用Selenium/Lavague）")
    print("=" * 70)
    print()
    
    if not CRAWLER_AVAILABLE:
        print("❌ 爬虫工具不可用，请检查MCP服务器配置")
        return
    
    # 创建输出目录
    output_dir = PROJECT_ROOT / "docs" / "joinquant_kb_comprehensive"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 爬取所有分类
    all_pages = {}
    all_links = set()
    
    for category, urls in PAGES_TO_CRAWL.items():
        result = crawl_category(category, urls)
        all_pages.update(result["pages"])
        all_links.update(result["links"])
    
    # 保存原始数据
    print(f"\n{'='*70}")
    print("💾 保存原始数据...")
    print(f"{'='*70}")
    
    raw_data_file = output_dir / "raw_data.json"
    with open(raw_data_file, 'w', encoding='utf-8') as f:
        json.dump({
            "pages": all_pages,
            "links": list(all_links),
            "crawled_at": datetime.now().isoformat(),
            "total_pages": len(all_pages),
            "total_links": len(all_links),
        }, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 原始数据: {raw_data_file}")
    
    # 整理知识库
    kb_entries = save_to_knowledge_base(all_pages, output_dir)
    
    # 生成报告
    print(f"\n{'='*70}")
    print("📊 生成报告...")
    print(f"{'='*70}")
    
    report_file = output_dir / "CRAWL_REPORT.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 聚宽知识库全面爬取报告\n\n")
        f.write(f"> **爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"> **总页面数**: {len(all_pages)}\n")
        f.write(f"> **总链接数**: {len(all_links)}\n")
        f.write(f"> **知识库条目**: {len(kb_entries)}\n\n")
        
        f.write("## 分类统计\n\n")
        categories = {}
        for url, data in all_pages.items():
            cat = data.get("category", "other")
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            f.write(f"- **{cat}**: {count} 个页面\n")
        
        f.write("\n## 知识库条目\n\n")
        for i, entry in enumerate(kb_entries, 1):
            f.write(f"{i}. **{entry['title']}**\n")
            f.write(f"   - 标签: {', '.join(entry['tags'])}\n")
            f.write(f"   - URL数: {len(entry.get('urls', []))}\n\n")
    
    print(f"  ✅ 报告: {report_file}")
    
    # 总结
    print(f"\n{'='*70}")
    print("✅ 爬取完成!")
    print(f"{'='*70}")
    print(f"""
总页面数: {len(all_pages)}
总链接数: {len(all_links)}
知识库条目: {len(kb_entries)}

输出目录: {output_dir}
  - raw_data.json: 原始爬取数据
  - knowledge_base.json: 知识库格式数据
  - CRAWL_REPORT.md: 爬取报告

下一步: 使用轩辕剑灵knowledge.add工具存入知识库
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

