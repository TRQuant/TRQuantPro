#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标准知识库构建流程 - AKShare文档

参考标准开发流程定义的标准知识库构建步骤：
1. 使用MCP工具下载/智能爬取（参考所有爬虫工具的使用）
2. 构建完整的RAG知识库
3. 测试并完善
4. 构建知识库使用的工具和流程本身也要随着项目进化

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import json
import re
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from urllib.parse import urljoin, urlparse

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# MCP工具导入（优先使用MCPClient，失败则回退到直接函数调用）
try:
    from core.mcp.client import MCPClient
    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    print("⚠️ MCPClient不可用，将使用直接函数调用")

try:
    from mcp_servers.unified_dev_server import (
        knowledge_add as direct_knowledge_add,
        crawler_fetch as direct_crawler_fetch,
        crawler_selenium_fetch as direct_crawler_selenium_fetch,
    )
    DIRECT_FUNCTIONS_AVAILABLE = True
except ImportError:
    DIRECT_FUNCTIONS_AVAILABLE = False
    print("⚠️ 直接函数调用不可用")

# ==================== 配置 ====================

BASE_URL = "https://akshare.akfamily.xyz"
START_URL = "https://akshare.akfamily.xyz/"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "akshare_crawled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 统计信息
STATS = {
    "pages_crawled": 0,
    "sections_found": 0,
    "sections_saved": 0,
    "sections_failed": 0,
    "duplicates_skipped": 0,
    "start_time": None,
    "end_time": None,
}

# 内容哈希（去重）
content_hashes: Set[str] = set()

# 已访问的URL（避免重复爬取）
visited_urls: Set[str] = set()

# ==================== 工具函数 ====================

def load_state():
    """加载状态（内容哈希、已访问URL等）"""
    global content_hashes, visited_urls
    
    # 加载内容哈希
    hash_file = OUTPUT_DIR / "content_hashes.json"
    if hash_file.exists():
        try:
            content_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass
    
    # 加载已访问URL
    visited_file = OUTPUT_DIR / "visited_urls.json"
    if visited_file.exists():
        try:
            visited_urls = set(json.loads(visited_file.read_text(encoding='utf-8')))
            print(f"✅ 加载已访问URL: {len(visited_urls)} 个")
        except:
            pass


def save_state():
    """保存状态"""
    # 保存内容哈希
    hash_file = OUTPUT_DIR / "content_hashes.json"
    hash_file.write_text(
        json.dumps(list(content_hashes), ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    # 保存已访问URL
    visited_file = OUTPUT_DIR / "visited_urls.json"
    visited_file.write_text(
        json.dumps(list(visited_urls), ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def fetch_with_playwright(url: str, wait_time: int = 5) -> Dict[str, Any]:
    """
    使用Playwright抓取页面（直接调用Python库）
    """
    try:
        from playwright.async_api import async_playwright
        import asyncio
        
        async def fetch():
            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                page = await browser.new_page()
                
                try:
                    await page.goto(url, wait_until='networkidle', timeout=60000)
                    await page.wait_for_timeout(wait_time * 1000)
                    
                    html = await page.content()
                    title = await page.title()
                    text = await page.inner_text('body')
                    
                    await browser.close()
                    
                    return {
                        'success': True,
                        'html': html,
                        'text': text,
                        'title': title,
                        'links': [],
                        'method': 'playwright'
                    }
                except Exception as e:
                    await browser.close()
                    raise e
        
        return asyncio.run(fetch())
    except ImportError:
        return {'success': False, 'error': 'Playwright未安装'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_openmanus(url: str) -> Dict[str, Any]:
    """
    使用OpenManus抓取页面（通过MCP工具或直接调用）
    """
    # 方法1: 尝试通过MCP工具调用
    if MCP_CLIENT_AVAILABLE:
        try:
            client = MCPClient()
            # OpenManus的browser_use工具
            result = client.call(
                tool_name='browser_use',
                arguments={
                    'action': 'go_to_url',
                    'url': url
                },
                timeout=60.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    import json as json_module
                    data = json_module.loads(data)
                
                # 然后提取内容
                extract_result = client.call(
                    tool_name='browser_use',
                    arguments={
                        'action': 'extract_content',
                        'goal': '提取页面所有文本和HTML内容'
                    },
                    timeout=30.0
                )
                
                if extract_result.success:
                    extract_data = extract_result.data
                    if isinstance(extract_data, str):
                        import json as json_module
                        extract_data = json_module.loads(extract_data)
                    
                    return {
                        'success': True,
                        'html': extract_data.get('html', ''),
                        'text': extract_data.get('text', ''),
                        'title': extract_data.get('title', ''),
                        'links': [],
                        'method': 'openmanus_mcp'
                    }
        except Exception as e:
            print(f"    ⚠️ OpenManus MCP调用失败: {e}")
    
    # 方法2: 直接调用OpenManus Python库（如果可用）
    try:
        from scripts.openmanus_browser_tool import OpenManusBrowserTool
        import asyncio
        
        async def fetch():
            tool = OpenManusBrowserTool(headless=True)
            result = await tool.navigate(url)
            if result.success:
                # 提取内容
                content = await tool.extract_content()
                await tool.close()
                
                return {
                    'success': True,
                    'html': content.get('html', ''),
                    'text': content.get('text', ''),
                    'title': content.get('title', ''),
                    'links': [],
                    'method': 'openmanus_direct'
                }
            await tool.close()
            return {'success': False, 'error': 'OpenManus导航失败'}
        
        return asyncio.run(fetch())
    except ImportError:
        return {'success': False, 'error': 'OpenManus未安装或不可用'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_with_best_tool(url: str, wait_selector: Optional[str] = None) -> Dict[str, Any]:
    """
    使用最佳工具抓取页面
    优先顺序：Playwright -> OpenManus -> MCP基础爬虫 -> MCP Selenium -> 直接函数调用
    """
    print(f"  🔍 抓取: {url}")
    
    # 1. 优先使用Playwright（最快、最可靠）
    try:
        result = fetch_with_playwright(url, wait_time=5)
        if result.get('success') and result.get('html') and len(result.get('html', '')) > 500:
            print(f"    ✅ Playwright成功 (HTML: {len(result.get('html', ''))} 字符)")
            return result
    except Exception as e:
        print(f"    ⚠️ Playwright失败: {e}")
    
    # 2. 尝试OpenManus（智能浏览器工具）
    try:
        result = fetch_with_openmanus(url)
        if result.get('success') and result.get('html') and len(result.get('html', '')) > 500:
            print(f"    ✅ OpenManus成功 (HTML: {len(result.get('html', ''))} 字符)")
            return result
    except Exception as e:
        print(f"    ⚠️ OpenManus失败: {e}")
    
    # 3. 使用MCP工具 - 基础爬虫（最快）
    if MCP_CLIENT_AVAILABLE:
        try:
            client = MCPClient()
            result = client.call(
                tool_name='crawler.fetch',
                arguments={
                    'url': url,
                    'extract_text': True,
                    'extract_links': True
                },
                timeout=30.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    import json as json_module
                    data = json_module.loads(data)
                
                if data.get('success') and data.get('text') and len(data.get('text', '')) > 500:
                    print(f"    ✅ MCP基础爬虫成功 (文本: {len(data.get('text', ''))} 字符)")
                    return {
                        'success': True,
                        'html': data.get('html', ''),
                        'text': data.get('text', ''),
                        'links': data.get('links', []),
                        'title': data.get('title', ''),
                        'method': 'mcp_fetch'
                    }
        except Exception as e:
            print(f"    ⚠️ MCP基础爬虫失败: {e}")
    
    # 2. 使用MCP工具 - Selenium（处理JS渲染）
    if MCP_CLIENT_AVAILABLE:
        try:
            client = MCPClient()
            result = client.call(
                tool_name='crawler.selenium.fetch',
                arguments={
                    'url': url,
                    'wait_time': 10,
                    'wait_selector': wait_selector or 'body',
                    'headless': True
                },
                timeout=60.0
            )
            
            if result.success:
                data = result.data
                if isinstance(data, str):
                    import json as json_module
                    data = json_module.loads(data)
                
                if data.get('success') and data.get('html'):
                    # 提取文本
                    html = data.get('html', '')
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(html, 'html.parser')
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text(separator=' ', strip=True)
                    
                    print(f"    ✅ MCP Selenium成功 (HTML: {len(html)} 字符)")
                    return {
                        'success': True,
                        'html': html,
                        'text': text,
                        'links': [],
                        'title': data.get('title', ''),
                        'method': 'mcp_selenium'
                    }
        except Exception as e:
            print(f"    ⚠️ MCP Selenium失败: {e}")
    
    # 3. 回退到直接函数调用 - 基础爬虫
    if DIRECT_FUNCTIONS_AVAILABLE:
        try:
            result = direct_crawler_fetch(url, extract_text=True, extract_links=True)
            if result.get('success') and result.get('text') and len(result.get('text', '')) > 500:
                print(f"    ✅ 直接函数基础爬虫成功 (文本: {len(result.get('text', ''))} 字符)")
                return {
                    'success': True,
                    'html': result.get('html', ''),
                    'text': result.get('text', ''),
                    'links': result.get('links', []),
                    'title': result.get('title', ''),
                    'method': 'direct_fetch'
                }
        except Exception as e:
            print(f"    ⚠️ 直接函数基础爬虫失败: {e}")
    
    # 4. 回退到直接函数调用 - Selenium
    if DIRECT_FUNCTIONS_AVAILABLE:
        try:
            result = direct_crawler_selenium_fetch(
                url=url,
                wait_time=10,
                wait_selector=wait_selector or 'body',
                headless=True
            )
            if result.get('success') and result.get('html'):
                html = result.get('html', '')
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator=' ', strip=True)
                
                print(f"    ✅ 直接函数Selenium成功 (HTML: {len(html)} 字符)")
                return {
                    'success': True,
                    'html': html,
                    'text': text,
                    'links': [],
                    'title': result.get('title', ''),
                    'method': 'direct_selenium'
                }
        except Exception as e:
            print(f"    ⚠️ 直接函数Selenium失败: {e}")
    
    return {'success': False, 'error': '所有爬虫工具都失败'}


def extract_sections_from_html(html: str, url: str) -> List[Dict]:
    """
    从HTML中提取内容块（针对Sphinx文档结构）
    参考PTrade爬虫的成功方法
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        sections = []
        seen_ids = set()
        
        # 方法1: 查找所有有ID的元素（最通用方法）
        for elem in soup.find_all(attrs={'id': True}):
            elem_id = elem.get('id')
            if not elem_id or elem_id in seen_ids:
                continue
            
            seen_ids.add(elem_id)
            
            # 提取内容
            content = elem.get_text(separator='\n', strip=True)
            
            # 如果内容太短，尝试获取后续兄弟元素
            if len(content) < 100:
                sibling = elem.next_sibling
                depth = 0
                while sibling and depth < 10:
                    if hasattr(sibling, 'get_text'):
                        sibling_text = sibling.get_text(separator='\n', strip=True)
                        if len(sibling_text) > 50:
                            content += '\n\n' + sibling_text
                    sibling = getattr(sibling, 'next_sibling', None)
                    depth += 1
            
            # 获取标题
            title = elem_id
            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                title = elem.get_text(strip=True)
            else:
                # 查找最近的标题元素
                heading = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if heading:
                    title = heading.get_text(strip=True)
                else:
                    # 查找父元素中的标题
                    parent = elem.parent
                    if parent:
                        parent_heading = parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        if parent_heading:
                            title = parent_heading.get_text(strip=True)
            
            # 提取代码块
            code_blocks = []
            for code_elem in elem.find_all(['pre', 'code']):
                code_text = code_elem.get_text(strip=True)
                if len(code_text) > 10:
                    code_blocks.append(code_text[:5000])  # 限制长度
            
            if len(content) > 50:  # 降低最小长度要求
                sections.append({
                    'anchor_id': elem_id,
                    'title': title,
                    'content': content,
                    'code_blocks': code_blocks[:10],  # 限制数量
                    'url': url,
                    'full_url': f"{url}#{elem_id}" if elem_id else url
                })
        
        # 方法2: 如果没有找到，尝试提取主要内容区域（针对Sphinx）
        if not sections:
            # 查找Sphinx文档的主要内容区域
            main_content = soup.find(['div', 'section'], class_=re.compile(r'body|content|main|document'))
            if main_content:
                # 移除导航和侧边栏
                for nav in main_content.find_all(['nav', 'aside', 'header', 'footer']):
                    nav.decompose()
                
                # 按标题分割
                current_section = None
                for elem in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'pre', 'ul', 'ol']):
                    if elem.name in ['h1', 'h2', 'h3', 'h4']:
                        # 保存上一个section
                        if current_section and len(current_section.get('content', '')) > 100:
                            sections.append(current_section)
                        
                        # 开始新section
                        anchor_id = elem.get('id', '') or elem.get('name', '')
                        title = elem.get_text(strip=True)
                        current_section = {
                            'anchor_id': anchor_id,
                            'title': title,
                            'content': '',
                            'code_blocks': [],
                            'url': url,
                            'full_url': f"{url}#{anchor_id}" if anchor_id else url
                        }
                    elif current_section:
                        if elem.name == 'pre':
                            code = elem.get_text(strip=True)
                            if len(code) > 20:
                                current_section['code_blocks'].append(code[:5000])
                        else:
                            text = elem.get_text(strip=True)
                            if text:
                                current_section['content'] += '\n' + text
                
                # 保存最后一个section
                if current_section and len(current_section.get('content', '')) > 100:
                    sections.append(current_section)
        
        # 方法3: 如果还是没有找到，将整个页面作为一个条目
        if not sections:
            # 移除导航和侧边栏
            for nav in soup.find_all(['nav', 'aside', 'header', 'footer', 'script', 'style']):
                nav.decompose()
            
            title_elem = soup.find(['h1', 'title'])
            title = title_elem.get_text(strip=True) if title_elem else "AKShare文档"
            
            content = soup.get_text(separator='\n', strip=True)
            
            if len(content) > 200:
                code_blocks = []
                for code_elem in soup.find_all(['pre', 'code']):
                    code_text = code_elem.get_text(strip=True)
                    if len(code_text) > 20:
                        code_blocks.append(code_text[:5000])
                
                sections.append({
                    'anchor_id': '',
                    'title': title,
                    'content': content,
                    'code_blocks': code_blocks[:10],
                    'url': url,
                    'full_url': url
                })
        
        return sections
    
    except Exception as e:
        print(f"  ❌ 解析HTML失败: {e}")
        import traceback
        traceback.print_exc()
        return []


def classify_and_tag(section_data: Dict) -> Tuple[str, List[str]]:
    """
    分类和标签（根据内容智能分类）
    """
    title = section_data.get('title', '').lower()
    content = section_data.get('content', '').lower()
    anchor_id = section_data.get('anchor_id', '').lower()
    
    # 确定类型
    if any(kw in title or kw in content for kw in ['安装', '配置', '环境', 'setup', 'install', 'config']):
        kb_type = 'reference'
    elif any(kw in title or kw in content for kw in ['教程', '入门', '快速', 'tutorial', 'guide', 'quick']):
        kb_type = 'lesson'
    elif any(kw in title or kw in content for kw in ['示例', '案例', 'example', 'demo', 'sample']):
        kb_type = 'practice'
    elif any(kw in title or kw in content for kw in ['api', '接口', '函数', 'function', 'method']):
        kb_type = 'reference'
    else:
        kb_type = 'reference'  # 默认
    
    # 确定标签
    tags = ['AKShare', '数据获取', '量化交易']
    
    # 根据内容添加标签
    if '股票' in content or 'stock' in content:
        tags.append('股票数据')
    if '期货' in content or 'futures' in content:
        tags.append('期货数据')
    if '基金' in content or 'fund' in content:
        tags.append('基金数据')
    if '指数' in content or 'index' in content:
        tags.append('指数数据')
    if '宏观' in content or 'macro' in content:
        tags.append('宏观数据')
    if '债券' in content or 'bond' in content:
        tags.append('债券数据')
    if '期权' in content or 'option' in content:
        tags.append('期权数据')
    if 'api' in content or '接口' in content:
        tags.append('API接口')
    if 'python' in content or '代码' in content:
        tags.append('Python')
    
    return kb_type, list(dict.fromkeys(tags))  # 去重


def save_to_knowledge_base(section_data: Dict) -> bool:
    """
    保存到知识库（优先使用MCP工具，失败则回退）
    """
    try:
        # 计算内容哈希（去重）
        content_hash = hashlib.md5(
            (section_data['content'] + section_data.get('title', '')).encode('utf-8')
        ).hexdigest()
        
        if content_hash in content_hashes:
            STATS['duplicates_skipped'] += 1
            return False
        
        content_hashes.add(content_hash)
        
        # 分类和标签
        kb_type, tags = classify_and_tag(section_data)
        
        # 构建知识库内容
        kb_content = f"""# {section_data['title']}

**锚点ID**: {section_data.get('anchor_id', 'N/A')}
**URL**: {section_data.get('full_url', section_data.get('url', ''))}

## 内容

{section_data['content']}

"""
        
        # 添加代码块
        if section_data.get('code_blocks'):
            kb_content += "\n## 代码示例\n\n"
            for i, code in enumerate(section_data['code_blocks'][:5], 1):
                kb_content += f"### 代码示例 {i}\n\n```python\n{code}\n```\n\n"
        
        # 添加到知识库（优先使用MCP工具）
        success = False
        
        if MCP_CLIENT_AVAILABLE:
            try:
                client = MCPClient()
                result = client.call(
                    tool_name='knowledge.add',
                    arguments={
                        'title': f"AKShare: {section_data['title']}",
                        'content': kb_content,
                        'type': kb_type,
                        'tags': tags,
                        'source': section_data.get('full_url', section_data.get('url', ''))
                    },
                    timeout=30.0
                )
                
                if result.success:
                    data = result.data
                    if isinstance(data, str):
                        import json as json_module
                        data = json_module.loads(data)
                    
                    if data.get('success') or data.get('knowledge_id'):
                        success = True
                        kb_id = data.get('knowledge_id') or data.get('id', 'unknown')
                        print(f"    ✅ [MCP工具] 成功存入知识库 (ID: {kb_id})")
            except Exception as e:
                print(f"    ⚠️ MCP工具调用失败: {e}")
        
        # 回退到直接函数调用
        if not success and DIRECT_FUNCTIONS_AVAILABLE:
            try:
                result = direct_knowledge_add(
                    title=f"AKShare: {section_data['title']}",
                    content=kb_content,
                    type=kb_type,
                    tags=tags,
                    source=section_data.get('full_url', section_data.get('url', ''))
                )
                
                if result.get('success') or result.get('knowledge_id'):
                    success = True
                    kb_id = result.get('knowledge_id') or result.get('id', 'unknown')
                    print(f"    ✅ [直接函数] 成功存入知识库 (ID: {kb_id})")
            except Exception as e:
                print(f"    ❌ 直接函数调用也失败: {e}")
        
        if success:
            STATS['sections_saved'] += 1
            return True
        else:
            STATS['sections_failed'] += 1
            return False
    
    except Exception as e:
        print(f"  ❌ 保存到知识库失败: {e}")
        STATS['sections_failed'] += 1
        return False


def extract_links_from_html(html: str, base_url: str) -> List[str]:
    """从HTML中提取链接"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            # 转换为绝对URL
            absolute_url = urljoin(base_url, href)
            # 只保留同域名的链接
            if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                links.append(absolute_url)
        
        return list(set(links))  # 去重
    except Exception as e:
        print(f"  ⚠️ 提取链接失败: {e}")
        return []


def crawl_page(url: str, max_depth: int = 3, current_depth: int = 0) -> None:
    """
    爬取单个页面（递归爬取链接）
    """
    if current_depth > max_depth:
        return
    
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    STATS['pages_crawled'] += 1
    
    print(f"\n[{STATS['pages_crawled']}] 爬取页面 (深度 {current_depth}): {url}")
    
    # 抓取页面
    fetch_result = fetch_with_best_tool(url)
    if not fetch_result.get('success'):
        print(f"  ❌ 抓取失败: {fetch_result.get('error', 'Unknown error')}")
        return
    
    # 提取内容块
    sections = extract_sections_from_html(fetch_result['html'], url)
    STATS['sections_found'] += len(sections)
    
    print(f"  📝 找到 {len(sections)} 个内容块")
    
    # 保存每个内容块到知识库
    for i, section in enumerate(sections, 1):
        print(f"  [{i}/{len(sections)}] {section['title']}")
        save_to_knowledge_base(section)
    
    # 提取链接（用于递归爬取）
    if current_depth < max_depth:
        links = extract_links_from_html(fetch_result['html'], url)
        print(f"  🔗 找到 {len(links)} 个链接")
        
        # 限制链接数量（避免过多）
        for link in links[:20]:  # 每页最多爬取20个链接
            if link not in visited_urls:
                time.sleep(1)  # 避免请求过快
                crawl_page(link, max_depth, current_depth + 1)


def main():
    """主函数"""
    print('=' * 70)
    print('📚 AKShare 知识库构建')
    print('=' * 70)
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    
    # 加载状态
    load_state()
    
    # 开始爬取
    STATS['start_time'] = datetime.now()
    
    try:
        # 从起始URL开始爬取
        crawl_page(START_URL, max_depth=2)  # 最大深度2层
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 保存状态
        save_state()
        
        # 统计信息
        STATS['end_time'] = datetime.now()
        duration = (STATS['end_time'] - STATS['start_time']).total_seconds()
        
        print('\n' + '=' * 70)
        print('📊 统计信息')
        print('=' * 70)
        print(f'爬取页面数: {STATS["pages_crawled"]}')
        print(f'找到内容块: {STATS["sections_found"]}')
        print(f'成功保存: {STATS["sections_saved"]}')
        print(f'保存失败: {STATS["sections_failed"]}')
        print(f'跳过重复: {STATS["duplicates_skipped"]}')
        print(f'总耗时: {duration:.1f} 秒')
        print('=' * 70)


if __name__ == '__main__':
    main()
