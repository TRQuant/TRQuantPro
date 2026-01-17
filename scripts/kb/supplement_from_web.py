#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从网站爬取并补充知识库
======================

从相关网站爬取量化交易、策略、因子等相关知识，并添加到知识库
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from mcp_servers.unified_dev_server import knowledge_add
from core.mcp.client import MCPClient


def fetch_with_mcp_tools(url: str) -> str:
    """
    使用MCP工具爬取网页内容
    
    Args:
        url: 目标URL
        
    Returns:
        网页内容
    """
    client = MCPClient()
    
    # 尝试多种爬虫工具
    tools = [
        'crawler.fetch',
        'crawler.selenium.fetch',
        'crawler.lavague.execute'
    ]
    
    for tool_name in tools:
        try:
            print(f"  尝试使用 {tool_name}...")
            result = client.call(
                tool_name=tool_name,
                arguments={'url': url},
                timeout=60.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    return data
                elif isinstance(data, dict):
                    return data.get('content', '') or data.get('text', '') or str(data)
        except Exception as e:
            print(f"  {tool_name} 失败: {e}")
            continue
    
    return ""


def parse_quant_content(content: str, source_url: str) -> List[Dict[str, Any]]:
    """
    解析量化相关内容，提取知识条目
    
    Args:
        content: 网页内容
        source_url: 来源URL
        
    Returns:
        知识条目列表
    """
    knowledge_items = []
    
    # 移除HTML标签（简单处理）
    text = re.sub(r'<[^>]+>', '', content)
    text = re.sub(r'\s+', ' ', text)
    
    # 提取标题和内容块
    # 查找常见的量化知识结构
    
    # 1. 策略相关（策略名称、策略逻辑、回测结果等）
    strategy_patterns = [
        r'策略[名称名]?[：:]\s*([^\n]+)',
        r'策略逻辑[：:]\s*([^\n]+)',
        r'回测[结果表现]?[：:]\s*([^\n]+)',
    ]
    
    # 2. 因子相关（因子名称、因子定义、因子有效性等）
    factor_patterns = [
        r'因子[名称名]?[：:]\s*([^\n]+)',
        r'因子定义[：:]\s*([^\n]+)',
        r'IC[：:]\s*([^\n]+)',
        r'IR[：:]\s*([^\n]+)',
    ]
    
    # 3. 市场状态相关（市场状态、情绪周期、转换信号等）
    regime_patterns = [
        r'市场状态[：:]\s*([^\n]+)',
        r'情绪周期[：:]\s*([^\n]+)',
        r'转换信号[：:]\s*([^\n]+)',
    ]
    
    # 简单提取：如果内容包含关键词，就创建一个知识条目
    keywords_mapping = {
        'strategy_pattern': ['策略', '回测', '胜率', '收益率', '策略逻辑'],
        'factor_behavior': ['因子', 'IC', 'IR', '有效性', '行为映射'],
        'market_regime': ['市场状态', '情绪周期', '退潮', '主升', '过热'],
        'failure_case': ['失败', '失效', '错误', '教训', '避免']
    }
    
    # 判断内容类型
    kb_type = None
    for kb_t, keywords in keywords_mapping.items():
        if any(kw in text for kw in keywords):
            kb_type = kb_t
            break
    
    if not kb_type:
        kb_type = 'reference'  # 默认类型
    
    # 提取标题（尝试从内容中提取）
    title_match = re.search(r'#+\s*([^\n]+)', content) or re.search(r'<h[1-3][^>]*>([^<]+)</h[1-3]>', content)
    title = title_match.group(1).strip() if title_match else f"来自 {urlparse(source_url).netloc}"
    
    # 限制内容长度
    content_text = text[:2000] if len(text) > 2000 else text
    
    if len(content_text) > 100:  # 最小长度要求
        knowledge_items.append({
            'title': title[:100],
            'content': content_text,
            'type': kb_type,
            'tags': ['网络爬取', '量化交易'],
            'source': source_url
        })
    
    return knowledge_items


def crawl_and_add_knowledge(urls: List[str]) -> int:
    """
    爬取多个URL并添加到知识库
    
    Args:
        urls: URL列表
        
    Returns:
        成功添加的知识条目数
    """
    print("=" * 70)
    print("🌐 从网站爬取并补充知识库")
    print("=" * 70)
    print()
    
    success_count = 0
    total_items = 0
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 爬取: {url}")
        try:
            # 爬取内容
            content = fetch_with_mcp_tools(url)
            
            if not content:
                print(f"   ⚠️ 无法获取内容")
                continue
            
            print(f"   ✅ 获取内容: {len(content)} 字符")
            
            # 解析内容
            knowledge_items = parse_quant_content(content, url)
            
            if not knowledge_items:
                print(f"   ⚠️ 未提取到知识条目")
                continue
            
            print(f"   📝 提取到 {len(knowledge_items)} 条知识")
            total_items += len(knowledge_items)
            
            # 添加到知识库
            for item in knowledge_items:
                try:
                    result = knowledge_add(
                        title=item['title'],
                        content=item['content'],
                        type=item['type'],
                        tags=item['tags'],
                        source=item['source']
                    )
                    
                    if result.get('success') or result.get('knowledge_id'):
                        success_count += 1
                        print(f"      ✅ {item['title'][:50]}")
                    else:
                        print(f"      ❌ 添加失败: {result.get('error', 'Unknown')}")
                except Exception as e:
                    print(f"      ❌ 异常: {e}")
        
        except Exception as e:
            print(f"   ❌ 爬取失败: {e}")
        
        print()
    
    print("=" * 70)
    print(f"📊 爬取完成: {success_count}/{total_items} 条成功添加")
    print("=" * 70)
    
    return success_count


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 从网站爬取并补充知识库")
    print("=" * 70)
    print()
    
    # 定义要爬取的URL列表
    # 注意：这里使用一些公开的量化交易相关网站
    urls = [
        # 聚宽社区策略分享
        "https://www.joinquant.com/view/community/detail/12345",  # 示例URL，需要替换为实际URL
        
        # 量化交易相关博客
        # "https://example.com/quant-strategy",  # 示例URL
        
        # 因子研究相关
        # "https://example.com/factor-research",  # 示例URL
    ]
    
    # 如果URL列表为空，提示用户
    if not urls or all('example.com' in url for url in urls):
        print("⚠️  请先配置要爬取的URL列表")
        print()
        print("📋 建议的URL来源:")
        print("  1. 聚宽社区策略分享页面")
        print("  2. 量化交易相关博客")
        print("  3. 因子研究文章")
        print("  4. 市场分析报告")
        print()
        print("💡 使用方法:")
        print("  修改脚本中的 urls 列表，添加实际URL")
        return
    
    success_count = crawl_and_add_knowledge(urls)
    
    print()
    print("=" * 70)
    if success_count > 0:
        print(f"✅ 知识补充成功！")
        print(f"   成功添加 {success_count} 条知识")
    else:
        print("❌ 知识补充失败或无新知识")
    print("=" * 70)


if __name__ == '__main__':
    main()
