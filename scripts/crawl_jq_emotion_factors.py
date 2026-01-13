#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
爬取聚宽情绪因子API文档并构建知识库
====================================

从 https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10439 爬取情绪因子相关文档

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

PROJECT_ROOT = Path("/home/taotao/.cursor/worktrees/TRQuant/ope")
sys.path.insert(0, str(PROJECT_ROOT))

from core.mcp.client import MCPClient

def crawl_jq_emotion_factors_doc(url: str) -> str:
    """
    爬取聚宽情绪因子API文档
    
    Args:
        url: 文档URL
    
    Returns:
        str: 文档内容（Markdown格式）
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            print(f"❌ 请求失败: HTTP {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取主要内容
        content_parts = []
        
        # 提取标题
        title = soup.find('title')
        if title:
            content_parts.append(f"# {title.get_text().strip()}\n")
        
        # 提取文章内容
        article = soup.find('article')
        if article:
            # 提取所有文本内容
            content = article.get_text(separator='\n', strip=True)
            content_parts.append(content)
        else:
            # 如果没有article标签，尝试提取body内容
            body = soup.find('body')
            if body:
                # 移除script和style标签
                for script in body(["script", "style"]):
                    script.decompose()
                content = body.get_text(separator='\n', strip=True)
                content_parts.append(content)
        
        # 组合内容
        full_content = '\n\n'.join(content_parts)
        
        # 添加元数据
        metadata = f"""
## 文档信息

- **来源URL**: {url}
- **爬取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **文档类型**: JQData API文档 - 情绪类因子

---

"""
        
        return metadata + full_content
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def add_to_knowledge_base(content: str, title: str = None) -> bool:
    """
    将内容添加到知识库
    
    Args:
        content: 文档内容
        title: 标题（可选）
    
    Returns:
        bool: 是否成功
    """
    if not content:
        print("❌ 内容为空，无法添加到知识库")
        return False
    
    if title is None:
        title = "聚宽情绪因子API文档"
    
    try:
        client = MCPClient()
        
        result = client.call(
            tool_name='knowledge.add',
            arguments={
                'title': title,
                'content': content,
                'type': 'reference',
                'tags': ['聚宽', 'JQData', '情绪因子', 'API文档', '量化交易'],
                'source': 'https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10439'
            },
            timeout=30.0
        )
        
        if result.success:
            data = result.data
            if isinstance(data, str):
                data = json.loads(data)
            
            if data.get('success') or data.get('knowledge_id'):
                print(f"✅ 成功添加到知识库 (Trace ID: {result.trace_id})")
                if 'knowledge_id' in data:
                    print(f"   知识ID: {data['knowledge_id']}")
                return True
            else:
                print(f"⚠️ 添加失败: {data.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ MCP调用失败: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ 添加到知识库失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    url = "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=10439"
    
    print("=" * 80)
    print("爬取聚宽情绪因子API文档")
    print("=" * 80)
    print(f"\n目标URL: {url}\n")
    
    # 爬取文档
    print("📥 正在爬取文档...")
    content = crawl_jq_emotion_factors_doc(url)
    
    if not content:
        print("❌ 爬取失败，退出")
        return
    
    print(f"✅ 爬取成功，内容长度: {len(content)} 字符")
    
    # 保存到本地文件（备份）
    output_file = PROJECT_ROOT / "docs" / "jqdata_crawled" / "emotion_factors_doc.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding='utf-8')
    print(f"💾 已保存到本地: {output_file}")
    
    # 添加到知识库
    print("\n📚 正在添加到知识库...")
    success = add_to_knowledge_base(
        content,
        title="聚宽情绪因子API文档 - 情绪类因子使用说明"
    )
    
    if success:
        print("\n✅ 完成！文档已添加到知识库")
    else:
        print("\n⚠️ 添加到知识库失败，但文档已保存到本地")


if __name__ == '__main__':
    main()
