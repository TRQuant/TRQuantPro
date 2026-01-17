#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare股票数据知识库构建 - 从Markdown源码构建
==============================================

直接爬取Sphinx文档的Markdown源文件，更高效、更准确
"""

import sys
import asyncio
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.mcp.client import MCPClient
from mcp_servers.unified_dev_server import knowledge_add

# 配置
START_URL = "https://akshare.akfamily.xyz/data/stock/stock.html"
SOURCE_URL = "https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt"
BASE_URL = "https://akshare.akfamily.xyz"
OUTPUT_DIR = TRQUANT_ROOT / "docs" / "akshare_crawled" / "stock_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 统计
STATS = {
    "sections_found": 0,
    "sections_saved": 0,
    "sections_failed": 0,
    "duplicates_skipped": 0
}

# 内容去重
content_hashes = set()

# MCP客户端
MCP_CLIENT_AVAILABLE = False
try:
    client = MCPClient()
    MCP_CLIENT_AVAILABLE = True
except:
    pass


def load_content_hashes():
    """加载已保存的内容哈希"""
    global content_hashes
    hash_file = OUTPUT_DIR / "content_hashes.json"
    if hash_file.exists():
        try:
            content_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass


def save_content_hashes():
    """保存内容哈希"""
    hash_file = OUTPUT_DIR / "content_hashes.json"
    hash_file.write_text(
        json.dumps(list(content_hashes), ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def get_content_hash(content: str) -> str:
    """生成内容哈希"""
    import hashlib
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def save_to_knowledge_base(section: Dict) -> bool:
    """保存内容块到知识库"""
    global STATS, content_hashes
    
    # 生成内容哈希
    content_text = f"{section.get('title', '')}\n{section.get('content', '')}"
    content_hash = get_content_hash(content_text)
    
    # 检查是否重复
    if content_hash in content_hashes:
        STATS['duplicates_skipped'] += 1
        return False
    
    content_hashes.add(content_hash)
    
    # 构建完整内容
    full_content = section.get('content', '')
    
    # 添加代码块
    if section.get('code_blocks'):
        full_content += "\n\n## 代码示例\n\n"
        for i, code in enumerate(section.get('code_blocks', []), 1):
            full_content += f"```python\n{code}\n```\n\n"
    
    # 添加元数据
    full_content += f"\n\n---\n**来源**: {section.get('url', '')}\n"
    if section.get('anchor_id'):
        full_content += f"**锚点**: {section.get('anchor_id')}\n"
    
    # 分类和标签
    title = section.get('title', '')
    kb_type = "reference"  # API文档作为参考
    tags = ["AKShare", "股票数据", "API文档"]
    
    # 根据标题推断类型
    if any(kw in title for kw in ['接口', '函数', 'API', '方法']):
        tags.append("API接口")
    if any(kw in title for kw in ['行情', '价格', '数据']):
        tags.append("行情数据")
    if any(kw in title for kw in ['A股', 'B股', '港股', '美股']):
        tags.append(title.split()[0])  # 添加市场类型标签
    
    # 保存到知识库
    try:
        # 尝试MCP工具
        if MCP_CLIENT_AVAILABLE:
            result = client.call(
                tool_name='knowledge.add',
                arguments={
                    'title': f'AKShare股票数据: {title}',
                    'content': full_content,
                    'type': kb_type,
                    'tags': tags,
                    'source': section.get('url', '')
                },
                timeout=30.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    data = json.loads(data)
                if data.get('success') or data.get('knowledge_id'):
                    STATS['sections_saved'] += 1
                    save_content_hashes()
                    print(f"    ✅ [MCP工具] 成功存入知识库 (ID: {data.get('knowledge_id', 'N/A')})")
                    return True
        
        # 回退到直接函数调用
        result = knowledge_add(
            title=f'AKShare股票数据: {title}',
            content=full_content,
            type=kb_type,
            tags=tags,
            source=section.get('url', '')
        )
        
        if result.get('success') or result.get('knowledge_id'):
            STATS['sections_saved'] += 1
            save_content_hashes()
            print(f"    ✅ [直接函数] 成功存入知识库 (ID: {result.get('knowledge_id', 'N/A')})")
            return True
    except Exception as e:
        print(f"    ❌ 保存失败: {e}")
        STATS['sections_failed'] += 1
        return False
    
    return False


def parse_markdown_source(md_text: str, source_url: str) -> List[Dict]:
    """
    解析Markdown源文件，提取API接口文档
    
    Sphinx文档的Markdown格式通常包含：
    - 标题 (# ## ###)
    - API接口定义 (函数名、参数、返回值)
    - 代码示例
    
    改进版：更准确地解析Sphinx格式的Markdown文档
    """
    sections = []
    lines = md_text.split('\n')
    
    current_section = None
    current_content = []
    current_code_blocks = []
    in_code_block = False
    code_block_language = None
    current_code_block_lines = []
    
    # 统计信息
    total_lines = len(lines)
    processed_lines = 0
    
    for i, line in enumerate(lines):
        processed_lines += 1
        # 检测代码块
        if line.strip().startswith('```'):
            if in_code_block:
                # 结束代码块
                if current_code_block_lines:
                    code_text = '\n'.join(current_code_block_lines).strip()
                    if len(code_text) > 10:  # 最小代码长度
                        current_code_blocks.append(code_text)
                    # 也添加到内容中
                    if current_section:
                        current_content.append(f"\n```{code_block_language}\n{code_text}\n```\n")
                in_code_block = False
                code_block_language = None
                current_code_block_lines = []
            else:
                # 开始代码块
                in_code_block = True
                code_block_language = line.strip()[3:].strip() or 'python'
                current_code_block_lines = []
            continue
        
        if in_code_block:
            current_code_block_lines.append(line)
            continue
        
        # 检测标题（支持多级标题）
        if line.startswith('#'):
            # 保存上一个section（如果有内容）
            if current_section:
                content_text = '\n'.join(current_content).strip()
                # 降低最小长度要求，确保不遗漏小内容块
                if len(content_text) > 20:  # 从50降到20
                    current_section['content'] = content_text
                    current_section['code_blocks'] = current_code_blocks[:10]
                    sections.append(current_section)
                elif content_text:  # 即使很短也保存，可能是重要的API定义
                    current_section['content'] = content_text
                    current_section['code_blocks'] = current_code_blocks[:10]
                    sections.append(current_section)
            
            # 开始新section
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            
            # 跳过空标题
            if not title:
                continue
            
            # 生成锚点ID（Sphinx格式）
            anchor_id = re.sub(r'[^\w\s-]', '', title).strip().lower()
            anchor_id = re.sub(r'[-\s]+', '-', anchor_id)
            
            current_section = {
                'anchor_id': anchor_id,
                'title': title,
                'content': '',
                'code_blocks': [],
                'url': source_url,
                'full_url': f"{START_URL}#{anchor_id}" if anchor_id else START_URL
            }
            current_content = []
            current_code_blocks = []
            continue
        
        # 检测API接口定义（Sphinx格式）
        # 格式: 接口: function_name 或 ``function_name(parameters)``
        if line.strip().startswith('接口:'):
            api_name = line.strip().replace('接口:', '').strip()
            if current_section:
                current_content.append(f"\n**API接口**: `{api_name}`\n")
            continue
        
        # 格式: ``function_name(parameters)``
        api_match = re.match(r'^``([^`]+)\([^)]*\)``', line.strip())
        if api_match:
            api_name = api_match.group(1)
            if current_section:
                current_content.append(f"\n**API接口**: `{api_name}`\n")
            continue
        
        # 检测参数说明（Sphinx格式）
        # 格式: :param name: description
        param_match = re.match(r'^:param\s+(\w+):\s*(.+)$', line.strip())
        if param_match:
            param_name, param_desc = param_match.group(1), param_match.group(2)
            if current_section:
                current_content.append(f"- **{param_name}**: {param_desc}")
            continue
        
        # 检测返回值说明
        return_match = re.match(r'^:return[s]?:\s*(.+)$', line.strip())
        if return_match:
            return_desc = return_match.group(1)
            if current_section:
                current_content.append(f"\n**返回值**: {return_desc}\n")
            continue
        
        # 普通内容
        if current_section:
            # 保留所有行（包括空行），但跳过纯空行如果当前内容为空
            if line.strip() or current_content:
                current_content.append(line)
    
    # 保存最后一个section
    if current_section:
        content_text = '\n'.join(current_content).strip()
        if len(content_text) > 20 or content_text:  # 降低要求，确保不遗漏
            current_section['content'] = content_text
            current_section['code_blocks'] = current_code_blocks[:10]
            sections.append(current_section)
    
    print(f"   📊 解析统计: 总行数 {total_lines}, 处理行数 {processed_lines}, 提取section数 {len(sections)}")
    
    return sections


async def fetch_markdown_source(url: str) -> Dict[str, Any]:
    """使用Playwright抓取Markdown源文件"""
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(url, wait_until='networkidle', timeout=60000)
                await asyncio.sleep(2)
                
                # 获取页面文本内容（Markdown源文件通常是纯文本）
                text = await page.inner_text('body')
                title = await page.title()
                
                await browser.close()
                
                return {
                    'success': True,
                    'text': text,
                    'title': title,
                    'method': 'playwright'
                }
            except Exception as e:
                await browser.close()
                raise e
    except ImportError:
        return {'success': False, 'error': 'Playwright未安装'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


async def main():
    """主函数"""
    global STATS
    
    print("=" * 70)
    print("📚 AKShare 股票数据知识库构建 (Markdown源码)")
    print("=" * 70)
    print(f"源码URL: {SOURCE_URL}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 70)
    print()
    
    load_content_hashes()
    
    # 1. 抓取Markdown源文件
    print(f"📥 步骤1: 抓取Markdown源文件")
    print(f"   URL: {SOURCE_URL}")
    
    fetch_result = await fetch_markdown_source(SOURCE_URL)
    
    if not fetch_result.get('success'):
        print(f"   ❌ 抓取失败: {fetch_result.get('error')}")
        return
    
    print(f"   ✅ 抓取成功")
    print(f"   📊 文本长度: {len(fetch_result.get('text', ''))} 字符")
    
    # 保存原始文件
    source_file = OUTPUT_DIR / "stock.md.txt"
    source_file.write_text(fetch_result.get('text', ''), encoding='utf-8')
    print(f"   💾 源文件已保存: {source_file}")
    
    # 2. 解析Markdown
    print(f"\n📋 步骤2: 解析Markdown内容")
    md_text = fetch_result.get('text', '')
    sections = parse_markdown_source(md_text, SOURCE_URL)
    STATS['sections_found'] = len(sections)
    
    print(f"   ✅ 找到 {len(sections)} 个内容块")
    
    # 显示前10个标题
    if sections:
        print(f"\n   📋 内容块列表（前10个）:")
        for i, section in enumerate(sections[:10], 1):
            print(f"      {i:3d}. {section['title'][:60]}")
    
    # 3. 存入知识库
    print(f"\n💾 步骤3: 存入知识库")
    print(f"   开始存入 {len(sections)} 个内容块...")
    
    for i, section in enumerate(sections, 1):
        print(f"   [{i}/{len(sections)}] 📝 {section['title'][:60]}")
        save_to_knowledge_base(section)
    
    # 4. 统计和验证
    print(f"\n{'='*70}")
    print("📊 最终统计")
    print("=" * 70)
    print(f"找到内容块: {STATS['sections_found']}")
    print(f"成功保存: {STATS['sections_saved']}")
    print(f"保存失败: {STATS['sections_failed']}")
    print(f"跳过重复: {STATS['duplicates_skipped']}")
    print("=" * 70)
    
    # 验证知识库
    if MCP_CLIENT_AVAILABLE:
        print(f"\n🔍 验证知识库")
        try:
            result = client.call(
                tool_name='knowledge.search',
                arguments={
                    'query': 'AKShare 股票数据',
                    'limit': 10
                },
                timeout=30.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    data = json.loads(data)
                items = data.get('items', []) or data.get('results', [])
                print(f"   ✅ 知识库搜索测试成功")
                print(f"   📊 找到 {len(items)} 条相关记录")
                if items:
                    print(f"   📋 示例记录（前5条）:")
                    for i, item in enumerate(items[:5], 1):
                        title = item.get('title', 'N/A')
                        print(f"      {i}. {title[:60]}")
        except Exception as e:
            print(f"   ⚠️ 知识库验证异常: {e}")
    
    print("\n✅ 知识库构建完成！")
    print("=" * 70)


if __name__ == '__main__':
    asyncio.run(main())
