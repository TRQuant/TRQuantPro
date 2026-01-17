#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
陈小群策略知识库 - 网络爬取增强工具

使用MCP工具进行网络爬取，获取更多陈小群相关信息
"""

import sys
from pathlib import Path
import json
from datetime import datetime
from typing import Dict, List, Optional

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入知识库工具
from scripts.import_chen_xiaoqun_knowledge import add_to_strategy_kb

# 需要爬取的URL列表
CRAWL_URLS = [
    {
        "url": "https://www.guminchaguan.com/youziwudao/2388.html",
        "title": "陈小群游资之道 - 股民茶馆",
        "tags": ["web_crawl", "trading_method", "growth_story"]
    },
    {
        "url": "https://finance.sina.com.cn/jjxw/2025-12-26/doc-inheautr2809070.shtml",
        "title": "陈小群投资策略 - 新浪财经",
        "tags": ["web_crawl", "investment_strategy", "news"]
    },
    {
        "url": "https://news.hexun.com/2025-11-02/222108378.html",
        "title": "陈小群投资风格演变 - 和讯网",
        "tags": ["web_crawl", "trading_style", "evolution"]
    }
]

# 关键词搜索列表
SEARCH_KEYWORDS = [
    "陈小群 情绪周期 龙头战法",
    "陈小群 首板卡位术 选股技巧",
    "陈小群 仓位管理 止损止盈",
    "陈小群 游资席位 大连黄河路",
    "陈小群 情绪合力 市场共振"
]


def crawl_with_mcp_tool(url: str, title: str, tags: List[str]) -> Optional[str]:
    """
    使用MCP工具爬取网页内容
    
    注意：这个函数需要在MCP环境中调用，这里只是示例
    实际使用时需要通过MCP服务器调用crawler_fetch或crawler_selenium_fetch
    """
    print(f"\n准备爬取: {title}")
    print(f"URL: {url}")
    print(f"标签: {', '.join(tags)}")
    
    # 这里只是示例，实际需要调用MCP工具
    # 在Cursor Chat中，可以使用：
    # "请使用crawler_fetch工具爬取 https://example.com"
    # 或
    # "请使用crawler_selenium_fetch工具爬取 https://example.com"
    
    print("💡 提示: 请在Cursor Chat中使用MCP工具进行爬取")
    print("   例如: 请使用crawler_fetch工具爬取此URL")
    
    return None


def add_crawled_content(title: str, content: str, source_url: str, tags: List[str]):
    """添加爬取的内容到知识库"""
    try:
        kb_id = add_to_strategy_kb(
            title=title,
            content=content,
            source_file=f"web_crawl:{source_url}",
            tags=tags,
            category="strategy"
        )
        print(f"✅ 已添加: {kb_id} - {title}")
        return kb_id
    except Exception as e:
        print(f"❌ 添加失败: {title}, 错误: {e}")
        return None


def create_crawl_instructions():
    """创建爬取指令文档"""
    instructions = {
        "crawl_urls": CRAWL_URLS,
        "search_keywords": SEARCH_KEYWORDS,
        "mcp_tools": {
            "crawler_fetch": {
                "description": "基础网页爬取工具",
                "usage": "在Cursor Chat中: 请使用crawler_fetch工具爬取 {url}",
                "example": "请使用crawler_fetch工具爬取 https://www.guminchaguan.com/youziwudao/2388.html"
            },
            "crawler_selenium_fetch": {
                "description": "Selenium爬取工具（支持JavaScript）",
                "usage": "在Cursor Chat中: 请使用crawler_selenium_fetch工具爬取 {url}",
                "example": "请使用crawler_selenium_fetch工具爬取 https://finance.sina.com.cn/jjxw/2025-12-26/doc-inheautr2809070.shtml"
            },
            "web_search": {
                "description": "网络搜索工具",
                "usage": "在Cursor Chat中: 请使用web_search搜索 {keyword}",
                "example": "请使用web_search搜索 陈小群 情绪周期 龙头战法"
            }
        },
        "instructions": [
            "1. 使用crawler_fetch或crawler_selenium_fetch爬取URL列表中的网页",
            "2. 提取网页中的关键信息（策略、案例、方法等）",
            "3. 使用add_crawled_content函数添加到知识库",
            "4. 使用web_search搜索关键词列表中的内容",
            "5. 整理搜索结果，提取有价值的信息添加到知识库"
        ]
    }
    
    instructions_file = TRQUANT_ROOT / ".trquant" / "dev" / "knowledge" / "strategy_knowledge" / "crawl_instructions.json"
    with open(instructions_file, 'w', encoding='utf-8') as f:
        json.dump(instructions, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 爬取指令已保存到: {instructions_file}")
    return instructions_file


def main():
    """主函数"""
    print("=" * 80)
    print("陈小群策略知识库 - 网络爬取增强工具")
    print("=" * 80)
    
    print("\n📋 待爬取的URL列表:")
    for i, item in enumerate(CRAWL_URLS, 1):
        print(f"  {i}. {item['title']}")
        print(f"     URL: {item['url']}")
        print(f"     标签: {', '.join(item['tags'])}")
    
    print("\n🔍 关键词搜索列表:")
    for i, keyword in enumerate(SEARCH_KEYWORDS, 1):
        print(f"  {i}. {keyword}")
    
    # 创建爬取指令文档
    create_crawl_instructions()
    
    print("\n" + "=" * 80)
    print("使用说明")
    print("=" * 80)
    print("\n在Cursor Chat中使用以下命令进行爬取:")
    print("\n1. 爬取网页:")
    print("   请使用crawler_fetch工具爬取 https://www.guminchaguan.com/youziwudao/2388.html")
    print("   或")
    print("   请使用crawler_selenium_fetch工具爬取 https://finance.sina.com.cn/jjxw/2025-12-26/doc-inheautr2809070.shtml")
    
    print("\n2. 搜索关键词:")
    print("   请使用web_search搜索 陈小群 情绪周期 龙头战法")
    
    print("\n3. 添加内容到知识库:")
    print("   爬取完成后，提取关键信息，使用add_crawled_content函数添加到知识库")
    
    print("\n💡 提示:")
    print("   - 优先使用crawler_fetch（速度快）")
    print("   - 如果页面需要JavaScript渲染，使用crawler_selenium_fetch")
    print("   - 搜索结果需要人工筛选和整理后再添加到知识库")


if __name__ == "__main__":
    main()
