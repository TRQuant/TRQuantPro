#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare股票数据知识库构建脚本

专门爬取AKShare股票数据相关页面：
1. 使用Playwright处理侧栏，提取"AKShare 股票数据"下的所有链接
2. 结合多种爬虫工具（Playwright优先，然后回退）
3. 构建完整的RAG知识库

Author: TRQuant Team
Date: 2026-01-12
"""

import sys
import json
import re
import hashlib
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple, Any
from urllib.parse import urljoin, urlparse

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# MCP工具导入
try:
    from core.mcp.client import MCPClient
    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    print("⚠️ MCPClient不可用")

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

# Playwright导入
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright未安装")

# ==================== 配置 ====================

BASE_URL = "https://akshare.akfamily.xyz"
START_URL = "https://akshare.akfamily.xyz/data/stock/stock.html#"

OUTPUT_DIR = PROJECT_ROOT / "docs" / "akshare_crawled" / "stock_data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 统计信息
STATS = {
    "pages_crawled": 0,
    "sections_found": 0,
    "sections_saved": 0,
    "sections_failed": 0,
    "duplicates_skipped": 0,
    "links_found": 0,
    "start_time": None,
    "end_time": None,
}

# 内容哈希（去重）
content_hashes: Set[str] = set()

# 已访问的URL（避免重复爬取）
visited_urls: Set[str] = set()

# ==================== 工具函数 ====================

def load_state():
    """加载状态"""
    global content_hashes, visited_urls
    
    hash_file = OUTPUT_DIR / "content_hashes.json"
    if hash_file.exists():
        try:
            content_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass
    
    visited_file = OUTPUT_DIR / "visited_urls.json"
    if visited_file.exists():
        try:
            visited_urls = set(json.loads(visited_file.read_text(encoding='utf-8')))
            print(f"✅ 加载已访问URL: {len(visited_urls)} 个")
        except:
            pass


def save_state():
    """保存状态"""
    hash_file = OUTPUT_DIR / "content_hashes.json"
    hash_file.write_text(
        json.dumps(list(content_hashes), ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    visited_file = OUTPUT_DIR / "visited_urls.json"
    visited_file.write_text(
        json.dumps(list(visited_urls), ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


async def extract_sidebar_links_playwright(page) -> List[Dict[str, str]]:
    """
    使用Playwright提取侧栏"AKShare 股票数据"下的所有链接
    改进版：更准确地提取Sphinx文档的侧栏链接
    """
    try:
        # 等待页面加载
        await page.wait_for_load_state('networkidle', timeout=30000)
        await asyncio.sleep(3)  # 额外等待确保侧栏渲染
        
        print("  🔍 开始提取侧栏链接...")
        
        # 使用JavaScript提取侧栏链接（改进版 - 更准确地提取Sphinx文档链接）
        links_data = await page.evaluate('''
            () => {
                const links = [];
                const seen = new Set();
                
                // 方法1: 查找当前页面所在目录下的所有链接（最准确）
                // Sphinx文档中，当前页面侧栏会显示同级和子级页面
                const currentPagePath = window.location.pathname;
                const currentDir = currentPagePath.substring(0, currentPagePath.lastIndexOf('/') + 1);
                
                // 查找所有链接，特别是侧栏中的链接
                const allLinks = document.querySelectorAll('a[href]');
                console.log(`总链接数: ${allLinks.length}, 当前目录: ${currentDir}`);
                
                allLinks.forEach(elem => {
                    const href = elem.getAttribute('href');
                    const text = elem.textContent.trim();
                    
                    if (!href || !text || seen.has(href)) return;
                    
                    // 跳过一些明显不相关的链接
                    if (href.includes('_sources') || href.includes('_static') || 
                        href.includes('_images') || href === '#' || 
                        text === '查看页面源码' || text === 'View page source') {
                        return;
                    }
                    
                    // 检查是否在侧栏区域
                    const isInSidebar = elem.closest('nav, .sidebar, .sphinxsidebar, aside, [role="navigation"], .local-toc');
                    
                    // 检查是否与股票数据相关（更精确的条件）
                    // 只提取在"AKShare 股票数据"区域内的链接
                    const parent = elem.closest('li, div, section, nav, aside');
                    const parentText = parent ? parent.textContent.trim() : '';
                    const allParentText = parent ? parent.textContent.trim() : '';
                    
                    // 检查是否在股票数据相关区域（通过父元素文本判断）
                    const isInStockSection = (
                        allParentText.includes('股票数据') ||
                        allParentText.includes('AKShare 股票数据') ||
                        // 向上查找父元素
                        (() => {
                            let current = elem;
                            for (let i = 0; i < 5 && current; i++) {
                                const text = current.textContent || '';
                                if (text.includes('股票数据') || text.includes('AKShare 股票数据')) {
                                    return true;
                                }
                                current = current.parentElement;
                            }
                            return false;
                        })()
                    );
                    
                    // 检查是否与股票数据相关
                    const isStockRelated = (
                        // 文本包含股票相关关键词
                        (text.includes('股票') && !text.includes('期货') && !text.includes('债券') && !text.includes('期权')) ||
                        text.includes('A股') ||
                        text.includes('B股') ||
                        text.includes('港股') ||
                        text.includes('美股') ||
                        text.includes('科创板') ||
                        text.includes('创业板') ||
                        text.includes('行情') ||
                        text.includes('个股') ||
                        text.includes('实时行情') ||
                        text.includes('历史行情') ||
                        text.includes('分笔数据') ||
                        text.includes('个股信息') ||
                        // URL包含stock（且不是其他数据类型）
                        (href.includes('stock') && !href.includes('futures') && !href.includes('bond') && !href.includes('option')) ||
                        href.includes('/data/stock/') ||
                        // 在股票数据页面内
                        currentPagePath.includes('stock')
                    ) && (
                        // 排除其他数据类型
                        !text.includes('期货') &&
                        !text.includes('债券') &&
                        !text.includes('期权') &&
                        !text.includes('外汇') &&
                        !text.includes('基金') &&
                        !text.includes('指数') &&
                        !text.includes('宏观') &&
                        !href.includes('futures') &&
                        !href.includes('bond') &&
                        !href.includes('option') &&
                        !href.includes('fx') &&
                        !href.includes('fund') &&
                        !href.includes('index') &&
                        !href.includes('macro')
                    );
                    
                    // 如果在股票数据区域，或者链接本身是股票相关的
                    const shouldInclude = isInStockSection || (isStockRelated && !isInStockSection);
                    
                    // 如果在侧栏中，或者链接文本/URL与股票相关
                    if (shouldInclude) {
                        // 获取父元素上下文
                        const parent = elem.closest('li, div, section, nav, aside');
                        const parentText = parent ? parent.textContent.trim().substring(0, 200) : '';
                        
                        seen.add(href);
                        links.push({
                            href: href,
                            text: text.substring(0, 200),
                            parentText: parentText,
                            isInSidebar: !!isInSidebar
                        });
                    }
                });
                
                // 方法2: 专门查找Sphinx的toctree结构
                const toctreeElements = document.querySelectorAll('.toctree-wrapper, .toctree, ul.toctree-l1, ul.toctree-l2, ul.toctree-l3');
                toctreeElements.forEach(container => {
                    const containerLinks = container.querySelectorAll('a[href]');
                    containerLinks.forEach(elem => {
                        const href = elem.getAttribute('href');
                        const text = elem.textContent.trim();
                        
                        if (href && text && !seen.has(href)) {
                            // 跳过明显不相关的
                            if (href.includes('_sources') || href.includes('_static') || href === '#') {
                                return;
                            }
                            
                            const parent = elem.closest('li');
                            const parentText = parent ? parent.textContent.trim().substring(0, 200) : '';
                            
                            // 如果父文本包含股票相关，或者链接文本包含，或者URL包含
                            if (parentText.includes('股票') || parentText.includes('stock') ||
                                text.includes('股票') || text.includes('stock') ||
                                href.includes('stock') || href.includes('/data/stock/')) {
                                seen.add(href);
                                links.push({
                                    href: href,
                                    text: text.substring(0, 200),
                                    parentText: parentText,
                                    isInSidebar: true
                                });
                            }
                        }
                    });
                });
                
                // 方法3: 查找页面内容区域中的API接口链接（这些也是重要的）
                const contentArea = document.querySelector('.document, .body, main, article, [role="main"]');
                if (contentArea) {
                    const contentLinks = contentArea.querySelectorAll('a[href]');
                    contentLinks.forEach(elem => {
                        const href = elem.getAttribute('href');
                        const text = elem.textContent.trim();
                        
                        if (href && text && !seen.has(href) && 
                            (href.includes('stock') || href.includes('/data/stock/') ||
                             text.includes('接口') || text.includes('API') || text.includes('函数'))) {
                            seen.add(href);
                            links.push({
                                href: href,
                                text: text.substring(0, 200),
                                parentText: '',
                                isInSidebar: false
                            });
                        }
                    });
                }
                
                console.log(`提取到 ${links.length} 个相关链接`);
                return links;
            }
        ''')
        
        # 转换为绝对URL并过滤
        links = []
        for link_data in links_data:
            href = link_data['href']
            
            # 跳过纯锚点链接（除非是.html文件）
            if href.startswith('#') and not any(ext in href for ext in ['.html', '.htm']):
                continue
            
            # 跳过明显不相关的链接
            if any(skip in href for skip in ['_sources', '_static', '_images', 'javascript:', 'mailto:']):
                continue
            
            # 转换为绝对URL（处理相对路径）
            if href.startswith('http'):
                absolute_url = href
            elif href.startswith('/'):
                absolute_url = BASE_URL + href
            else:
                # 相对路径，需要基于当前页面URL
                absolute_url = urljoin(START_URL, href)
            
            # 只保留同域名的链接
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc == urlparse(BASE_URL).netloc:
                # 移除URL中的锚点部分（#后面的）
                clean_url = absolute_url.split('#')[0]
                
                links.append({
                    'url': clean_url,
                    'text': link_data['text'],
                    'href': href,
                    'parentText': link_data.get('parentText', ''),
                    'isInSidebar': link_data.get('isInSidebar', False)
                })
        
        # 去重（基于URL）
        seen_urls = set()
        unique_links = []
        for link in links:
            url_key = link['url'].split('#')[0]  # 移除锚点
            if url_key not in seen_urls:
                seen_urls.add(url_key)
                unique_links.append(link)
        
        print(f"  📊 提取结果: 原始 {len(links_data)} 个 -> 过滤后 {len(unique_links)} 个")
        
        return unique_links
    
    except Exception as e:
        print(f"  ❌ 提取侧栏链接失败: {e}")
        import traceback
        traceback.print_exc()
        return []


async def fetch_page_with_playwright(page, url: str) -> Dict[str, Any]:
    """使用Playwright抓取页面"""
    try:
        await page.goto(url, wait_until='networkidle', timeout=60000)
        await asyncio.sleep(2)  # 额外等待
        
        html = await page.content()
        title = await page.title()
        text = await page.inner_text('body')
        
        return {
            'success': True,
            'html': html,
            'text': text,
            'title': title,
            'method': 'playwright'
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def fetch_page_with_fallback(url: str) -> Dict[str, Any]:
    """
    使用回退工具抓取页面（当Playwright失败时）
    优先顺序：MCP基础爬虫 -> MCP Selenium -> 直接函数
    """
    # 1. MCP基础爬虫
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
                
                if data.get('success') and data.get('text'):
                    return {
                        'success': True,
                        'html': data.get('html', ''),
                        'text': data.get('text', ''),
                        'title': data.get('title', ''),
                        'method': 'mcp_fetch'
                    }
        except Exception as e:
            pass
    
    # 2. MCP Selenium
    if MCP_CLIENT_AVAILABLE:
        try:
            client = MCPClient()
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
                    import json as json_module
                    data = json_module.loads(data)
                
                if data.get('success') and data.get('html'):
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(data['html'], 'html.parser')
                    for script in soup(["script", "style"]):
                        script.decompose()
                    text = soup.get_text(separator=' ', strip=True)
                    
                    return {
                        'success': True,
                        'html': data['html'],
                        'text': text,
                        'title': data.get('title', ''),
                        'method': 'mcp_selenium'
                    }
        except Exception as e:
            pass
    
    # 3. 直接函数调用
    if DIRECT_FUNCTIONS_AVAILABLE:
        try:
            result = direct_crawler_fetch(url, extract_text=True, extract_links=False)
            if result.get('success') and result.get('text'):
                return {
                    'success': True,
                    'html': result.get('html', ''),
                    'text': result.get('text', ''),
                    'title': result.get('title', ''),
                    'method': 'direct_fetch'
                }
        except Exception as e:
            pass
    
    return {'success': False, 'error': '所有工具都失败'}


def extract_sections_from_html(html: str, url: str) -> List[Dict]:
    """
    从HTML中提取内容块（针对Sphinx文档）
    改进版：更准确地提取API接口文档内容
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        sections = []
        seen_ids = set()
        
        # 移除导航、侧栏、页脚等
        for nav in soup.find_all(['nav', 'aside', 'header', 'footer', 'script', 'style']):
            nav.decompose()
        
        # 方法1: 查找所有有ID的元素（API接口通常有ID）
        for elem in soup.find_all(attrs={'id': True}):
            elem_id = elem.get('id')
            if not elem_id or elem_id in seen_ids:
                continue
            
            # 跳过一些系统ID
            if elem_id in ['search-documentation', 'search-results', 'searchbox', 'navigation']:
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
                # 查找最近的标题
                heading = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if heading:
                    title = heading.get_text(strip=True)
                else:
                    # 向上查找父元素中的标题
                    parent = elem.parent
                    depth = 0
                    while parent and depth < 5:
                        parent_heading = parent.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                        if parent_heading:
                            title = parent_heading.get_text(strip=True)
                            break
                        parent = parent.parent
                        depth += 1
            
            # 提取代码块
            code_blocks = []
            for code_elem in elem.find_all(['pre', 'code']):
                code_text = code_elem.get_text(strip=True)
                if len(code_text) > 10:
                    code_blocks.append(code_text[:5000])
            
            if len(content) > 50:  # 降低最小长度要求
                sections.append({
                    'anchor_id': elem_id,
                    'title': title,
                    'content': content,
                    'code_blocks': code_blocks[:10],
                    'url': url,
                    'full_url': f"{url}#{elem_id}" if elem_id else url
                })
        
        # 方法2: 按标题分割主要内容区域（Sphinx文档通常有清晰的标题结构）
        if not sections or len(sections) < 3:
            main_content = soup.find(['div', 'section'], class_=re.compile(r'body|content|main|document'))
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                # 移除导航等
                for nav in main_content.find_all(['nav', 'aside', 'header', 'footer', 'script', 'style']):
                    nav.decompose()
                
                # 按标题分割
                current_section = None
                for elem in main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'pre', 'table', 'dl']):
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
                        elif elem.name == 'table':
                            # 提取表格内容
                            table_text = elem.get_text(separator=' | ', strip=True)
                            if table_text:
                                current_section['content'] += '\n\n表格:\n' + table_text
                        elif elem.name == 'dl':
                            # 提取定义列表（API参数说明常用）
                            dl_text = elem.get_text(separator='\n', strip=True)
                            if dl_text:
                                current_section['content'] += '\n\n' + dl_text
                        else:
                            text = elem.get_text(strip=True)
                            if text and len(text) > 10:
                                current_section['content'] += '\n' + text
                
                # 保存最后一个section
                if current_section and len(current_section.get('content', '')) > 100:
                    sections.append(current_section)
        
        # 方法3: 如果还是没有找到，将整个页面作为一个条目
        if not sections:
            # 提取主要内容
            main_content = soup.find(['div', 'section'], class_=re.compile(r'body|content|main|document'))
            if not main_content:
                main_content = soup.find('body')
            
            if main_content:
                for nav in main_content.find_all(['nav', 'aside', 'header', 'footer', 'script', 'style']):
                    nav.decompose()
                
                title_elem = soup.find(['h1', 'title'])
                title = title_elem.get_text(strip=True) if title_elem else "AKShare股票数据文档"
                
                content = main_content.get_text(separator='\n', strip=True)
                
                if len(content) > 200:
                    code_blocks = []
                    for code_elem in main_content.find_all(['pre', 'code']):
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
    """分类和标签"""
    title = section_data.get('title', '').lower()
    content = section_data.get('content', '').lower()
    
    # 确定类型
    if any(kw in title or kw in content for kw in ['安装', '配置', 'setup', 'install']):
        kb_type = 'reference'
    elif any(kw in title or kw in content for kw in ['教程', '入门', 'tutorial', 'guide']):
        kb_type = 'lesson'
    elif any(kw in title or kw in content for kw in ['示例', '案例', 'example', 'demo']):
        kb_type = 'practice'
    else:
        kb_type = 'reference'
    
    # 确定标签
    tags = ['AKShare', '股票数据', '数据获取', '量化交易']
    
    if 'api' in content or '接口' in content:
        tags.append('API接口')
    if 'python' in content or '代码' in content:
        tags.append('Python')
    if '实时' in content or 'realtime' in content:
        tags.append('实时数据')
    if '历史' in content or 'history' in content:
        tags.append('历史数据')
    
    return kb_type, list(dict.fromkeys(tags))


def save_to_knowledge_base(section_data: Dict) -> bool:
    """保存到知识库"""
    try:
        # 计算内容哈希
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
        
        # 添加到知识库
        success = False
        
        if MCP_CLIENT_AVAILABLE:
            try:
                client = MCPClient()
                result = client.call(
                    tool_name='knowledge.add',
                    arguments={
                        'title': f"AKShare股票数据: {section_data['title']}",
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
                pass
        
        if not success and DIRECT_FUNCTIONS_AVAILABLE:
            try:
                result = direct_knowledge_add(
                    title=f"AKShare股票数据: {section_data['title']}",
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
                pass
        
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


async def crawl_page(page, url: str) -> Dict[str, Any]:
    """
    爬取单个页面（使用Playwright）
    返回详细的爬取报告
    """
    if url in visited_urls:
        return {'skipped': True, 'reason': 'already_visited'}
    
    visited_urls.add(url)
    STATS['pages_crawled'] += 1
    
    report = {
        'url': url,
        'page_number': STATS['pages_crawled'],
        'success': False,
        'sections_found': 0,
        'sections_saved': 0,
        'sections_failed': 0,
        'method': None,
        'error': None
    }
    
    print(f"\n{'='*70}")
    print(f"[{STATS['pages_crawled']}] 📄 爬取页面")
    print(f"{'='*70}")
    print(f"URL: {url}")
    
    # 使用Playwright抓取
    print(f"  🔍 使用Playwright抓取...")
    fetch_result = await fetch_page_with_playwright(page, url)
    report['method'] = 'playwright'
    
    # 如果Playwright失败，使用回退工具
    if not fetch_result.get('success'):
        print(f"  ⚠️ Playwright失败: {fetch_result.get('error')}")
        print(f"  🔄 尝试回退工具...")
        fetch_result = fetch_page_with_fallback(url)
        report['method'] = fetch_result.get('method', 'fallback')
    
    if not fetch_result.get('success'):
        error_msg = fetch_result.get('error', 'Unknown error')
        print(f"  ❌ 抓取失败: {error_msg}")
        report['error'] = error_msg
        return report
    
    print(f"  ✅ 抓取成功 (方法: {report['method']})")
    print(f"  📊 HTML长度: {len(fetch_result.get('html', ''))} 字符")
    print(f"  📊 文本长度: {len(fetch_result.get('text', ''))} 字符")
    print(f"  📝 页面标题: {fetch_result.get('title', 'N/A')}")
    
    # 提取内容块
    print(f"  🔍 解析HTML内容...")
    sections = extract_sections_from_html(fetch_result['html'], url)
    report['sections_found'] = len(sections)
    STATS['sections_found'] += len(sections)
    
    print(f"  ✅ 找到 {len(sections)} 个内容块")
    
    # 保存每个内容块到知识库
    if sections:
        print(f"  💾 开始存入知识库...")
        for i, section in enumerate(sections, 1):
            print(f"    [{i}/{len(sections)}] 📝 {section['title'][:60]}")
            if save_to_knowledge_base(section):
                report['sections_saved'] += 1
            else:
                report['sections_failed'] += 1
        
        print(f"  ✅ 知识库存储完成: 成功 {report['sections_saved']} 个, 失败 {report['sections_failed']} 个")
    else:
        print(f"  ⚠️ 未找到内容块，可能页面结构特殊")
    
    report['success'] = True
    
    # 延迟避免请求过快
    await asyncio.sleep(1)
    
    return report


async def main():
    """主函数"""
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装，请运行: pip install playwright && playwright install chromium")
        return
    
    print('=' * 70)
    print('📚 AKShare 股票数据知识库构建')
    print('=' * 70)
    print(f'开始时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'起始URL: {START_URL}')
    print()
    
    # 加载状态
    load_state()
    
    STATS['start_time'] = datetime.now()
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
            )
            page = await context.new_page()
            page.set_default_timeout(60000)
            
            # 1. 访问起始页面，提取侧栏链接
            print(f"\n{'='*70}")
            print(f"📋 步骤1: 提取侧栏链接")
            print(f"{'='*70}")
            print(f"访问起始URL: {START_URL}")
            
            await page.goto(START_URL, wait_until='networkidle', timeout=60000)
            await asyncio.sleep(3)  # 等待侧栏渲染
            
            print(f"✅ 页面加载完成")
            
            sidebar_links = await extract_sidebar_links_playwright(page)
            STATS['links_found'] = len(sidebar_links)
            
            print(f"\n✅ 找到 {len(sidebar_links)} 个股票数据相关链接")
            
            # 保存链接列表
            links_file = OUTPUT_DIR / "sidebar_links.json"
            links_file.write_text(
                json.dumps(sidebar_links, ensure_ascii=False, indent=2),
                encoding='utf-8'
            )
            print(f"💾 链接列表已保存: {links_file}")
            
            # 显示所有链接
            if sidebar_links:
                print(f"\n📋 链接列表:")
                for i, link in enumerate(sidebar_links, 1):
                    print(f"   {i:3d}. {link['text'][:60]:60s} -> {link['url']}")
            else:
                print(f"⚠️ 未找到链接，将尝试爬取当前页面")
            
            # 2. 爬取起始页面本身
            print(f"\n{'='*70}")
            print(f"📋 步骤2: 爬取起始页面")
            print(f"{'='*70}")
            start_page_url = START_URL.split('#')[0]
            start_report = await crawl_page(page, start_page_url)
            
            # 3. 过滤出只与股票数据相关的链接
            stock_related_links = []
            for link in sidebar_links:
                url = link['url']
                text = link['text']
                # 只保留股票数据相关的链接
                if ('stock' in url.lower() and '/data/stock/' in url) or \
                   (any(kw in text for kw in ['A股', 'B股', '港股', '美股', '科创板', '创业板', '个股', '行情', '股票']) and 
                    not any(kw in text for kw in ['期货', '债券', '期权', '外汇', '基金', '指数', '宏观'])):
                    stock_related_links.append(link)
            
            print(f"\n📊 链接过滤结果:")
            print(f"   原始链接: {len(sidebar_links)} 个")
            print(f"   股票相关: {len(stock_related_links)} 个")
            
            # 4. 爬取所有股票数据相关链接
            if stock_related_links:
                print(f"\n{'='*70}")
                print(f"📋 步骤3: 爬取股票数据相关链接 ({len(stock_related_links)} 个)")
                print(f"{'='*70}")
                
                crawl_reports = []
                for i, link in enumerate(stock_related_links, 1):
                    print(f"\n{'─'*70}")
                    print(f"处理链接 [{i}/{len(stock_related_links)}]")
                    print(f"标题: {link['text']}")
                    print(f"URL: {link['url']}")
                    
                    report = await crawl_page(page, link['url'])
                    crawl_reports.append(report)
                    
                    # 每5个页面保存一次状态并报告进度
                    if i % 5 == 0:
                        save_state()
                        print(f"\n{'='*70}")
                        print(f"📊 进度报告 (已处理 {i}/{len(stock_related_links)} 个链接)")
                        print(f"{'='*70}")
                        print(f"总页面数: {STATS['pages_crawled']}")
                        print(f"找到内容块: {STATS['sections_found']}")
                        print(f"成功保存: {STATS['sections_saved']}")
                        print(f"保存失败: {STATS['sections_failed']}")
                        print(f"跳过重复: {STATS['duplicates_skipped']}")
                        print(f"{'='*70}")
                
                # 保存爬取报告
                reports_file = OUTPUT_DIR / "crawl_reports.json"
                reports_file.write_text(
                    json.dumps(crawl_reports, ensure_ascii=False, indent=2, default=str),
                    encoding='utf-8'
                )
                print(f"\n💾 爬取报告已保存: {reports_file}")
            else:
                print(f"\n⚠️ 未找到侧栏链接，仅爬取了起始页面")
            
            await context.close()
            await browser.close()
    
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
        print('📊 最终统计信息')
        print('=' * 70)
        print(f'找到链接数: {STATS["links_found"]}')
        print(f'爬取页面数: {STATS["pages_crawled"]}')
        print(f'找到内容块: {STATS["sections_found"]}')
        print(f'成功保存: {STATS["sections_saved"]}')
        print(f'保存失败: {STATS["sections_failed"]}')
        print(f'跳过重复: {STATS["duplicates_skipped"]}')
        print(f'总耗时: {duration:.1f} 秒 ({duration/60:.1f} 分钟)')
        print('=' * 70)
        
        # 验证知识库
        print(f"\n{'='*70}")
        print('🔍 验证知识库')
        print('=' * 70)
        
        if MCP_CLIENT_AVAILABLE:
            try:
                client = MCPClient()
                # 搜索AKShare股票数据相关内容
                search_result = client.call(
                    tool_name='knowledge.search',
                    arguments={
                        'query': 'AKShare 股票数据',
                        'limit': 5
                    },
                    timeout=30.0
                )
                
                if search_result.success:
                    data = search_result.data
                    if isinstance(data, str):
                        import json as json_module
                        data = json_module.loads(data)
                    
                    items = data.get('items', [])
                    print(f"✅ 知识库搜索测试成功")
                    print(f"   找到 {len(items)} 条相关记录")
                    if items:
                        print(f"   示例记录:")
                        for i, item in enumerate(items[:3], 1):
                            title = item.get('title', 'N/A')
                            print(f"     {i}. {title[:60]}")
                else:
                    print(f"⚠️ 知识库搜索测试失败: {search_result.error}")
            except Exception as e:
                print(f"⚠️ 知识库验证异常: {e}")
        
        print('=' * 70)
        print('✅ 知识库构建完成！')
        print('=' * 70)


if __name__ == '__main__':
    asyncio.run(main())
