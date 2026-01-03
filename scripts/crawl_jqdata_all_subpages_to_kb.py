#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽数据页面完整爬取脚本 - 抓取所有子页面并存入知识库

用途：构建支持量化研究9步工作流的知识库
- 步骤1 市场趋势判断: 宏观数据、指数数据
- 步骤2 主线识别: 行业数据、板块数据  
- 步骤3 候选池: 股票数据、财务数据、筛选函数
- 步骤4 因子构建: Alpha因子、聚宽因子库、技术指标、风险模型
- 步骤5 策略生成: 交易函数、下单API
- 步骤6 回测: 历史行情、分钟/Tick数据
- 步骤7 优化: 参数优化、风险控制

使用最先进的爬虫工具：
- Playwright: 处理JavaScript渲染页面（高效异步）
- BeautifulSoup: 解析HTML和提取链接
- visited_urls持久化: 避免重复爬取

Author: TRQuant Team
Date: 2026-01-01
"""

import sys
import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from urllib.parse import urljoin, urlparse, parse_qs

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装，请运行: pip install playwright && playwright install chromium")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print("❌ BeautifulSoup4未安装，请运行: pip install beautifulsoup4")
    sys.exit(1)

try:
    from mcp_servers.unified_dev_server import knowledge_add
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False

# 聚宽基础URL
BASE_URL = "https://www.joinquant.com"
JQDATA_DOC_URL = "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9842"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "docs" / "jqdata_crawled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 统计信息
STATS = {
    "total_links": 0,
    "crawled": 0,
    "success": 0,
    "failed": 0,
    "skipped": 0,
    "saved_to_kb": 0
}

# 已访问的URL集合（避免重复）
visited_urls: Set[str] = set()

# visited_urls持久化文件（将在main函数中初始化）
VISITED_URLS_FILE: Optional[Path] = None


def load_visited_urls(file_path: Path) -> Set[str]:
    """从文件加载已访问的URL"""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = json.load(f)
                print(f"✅ 从文件加载了 {len(urls)} 个已访问的URL")
                return set(urls)
        except Exception as e:
            print(f"⚠️ 加载visited_urls失败: {e}")
    return set()


def save_visited_urls(file_path: Path):
    """保存已访问的URL到文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(list(visited_urls), f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存 {len(visited_urls)} 个已访问的URL到文件")
    except Exception as e:
        print(f"⚠️ 保存visited_urls失败: {e}")


def normalize_url(url: str) -> str:
    """规范化URL（移除锚点）"""
    return url.split('#')[0]


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def extract_title(html: str, url: str) -> str:
    """从HTML中提取标题 - 优先从内容中提取更具描述性的标题"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 方法1: 尝试从h1/h2标签提取
        for tag in ['h1', 'h2']:
            header = soup.find(tag)
            if header:
                title = header.get_text(strip=True)
                if title and len(title) > 3 and len(title) < 100:
                    return title
        
        # 方法2: 从URL的id参数推断
        if 'id=' in url:
            # 尝试从内容开头提取标题（通常在API文档的第一行）
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                # 获取第一段有意义的文本
                for p in main_content.find_all(['p', 'div', 'span'], limit=5):
                    text = p.get_text(strip=True)
                    if text and len(text) > 5 and len(text) < 80:
                        # 排除导航文本
                        if '返回' not in text and '目录' not in text:
                            return text[:60]
        
        # 方法3: 使用HTML title标签
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            title = title.replace(' - JoinQuant', '').strip()
            if title and title != 'JQData使用说明':
                return title
        
        # 方法4: 从URL提取id作为标题后缀
        if 'id=' in url:
            import re
            match = re.search(r'id=(\d+)', url)
            if match:
                return f"JQData文档_{match.group(1)}"
        
        return url
    except:
        return url


def extract_content(html: str) -> str:
    """从HTML中提取主要内容"""
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除script和style标签
        for tag in soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        
        # 优先查找main标签
        main = soup.find('main')
        if main:
            content = main.get_text(separator='\n', strip=True)
        else:
            # 查找body
            body = soup.find('body')
            if body:
                content = body.get_text(separator='\n', strip=True)
            else:
                content = soup.get_text(separator='\n', strip=True)
        
        return clean_text(content)
    except Exception as e:
        print(f"    ⚠️ 提取内容失败: {e}")
        return ""


async def extract_links_advanced(page_obj, base_url: str) -> List[Dict[str, str]]:
    """使用JavaScript从页面中提取所有JQData相关链接（高级方法）"""
    links = []
    try:
        # 使用JavaScript提取链接（更准确，能获取动态加载的链接，包括侧栏菜单）
        js_links = await page_obj.evaluate('''
            () => {
                const results = [];
                const seenUrls = new Set();
                
                // 方法1: 查找所有文档链接（包括侧栏、表格、目录中的所有链接）
                const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
                
                allLinks.forEach(link => {
                    const href = link.href || link.getAttribute('href');
                    if (!href || seenUrls.has(href)) return;
                    
                    // 确保URL格式正确（包含name和id参数）
                    if (href.includes('name=') && href.includes('id=')) {
                        const text = link.textContent.trim() || '';
                        // 移除URL中的锚点（#）
                        const cleanHref = href.split('#')[0];
                        
                        if (!seenUrls.has(cleanHref)) {
                            seenUrls.add(cleanHref);
                            results.push({
                                url: cleanHref,
                                text: text.substring(0, 150),
                                parent: link.parentElement?.tagName || 'unknown',
                                parentText: link.parentElement?.textContent.trim().substring(0, 50) || ''
                            });
                        }
                    }
                });
                
                // 方法2: 也尝试查找可能的侧栏菜单链接（通过特定的选择器）
                // 有些链接可能在ul>li结构中
                const menuLinks = document.querySelectorAll('ul a[href*="/help/api/doc"], nav a[href*="/help/api/doc"], aside a[href*="/help/api/doc"]');
                menuLinks.forEach(link => {
                    const href = link.href || link.getAttribute('href');
                    if (href && href.includes('/help/api/doc?name=JQDatadoc&id=') && href.includes('name=') && href.includes('id=')) {
                        const cleanHref = href.split('#')[0];
                        if (!seenUrls.has(cleanHref)) {
                            const text = link.textContent.trim() || '';
                            seenUrls.add(cleanHref);
                            results.push({
                                url: cleanHref,
                                text: text.substring(0, 150),
                                parent: 'menu',
                                parentText: ''
                            });
                        }
                    }
                });
                
                return results;
            }
        ''')
        
        # 转换为标准格式并去重
        seen_normalized = set()
        for link in js_links:
            normalized_url = normalize_url(link['url'])
            if normalized_url not in seen_normalized:
                seen_normalized.add(normalized_url)
                links.append({
                    'url': normalized_url,
                    'text': link['text']
                })
        
        print(f"    🔍 JavaScript提取到 {len(links)} 个链接（包括侧栏菜单）")
        return links
    except Exception as e:
        print(f"    ⚠️ JavaScript提取链接失败，使用备用方法: {e}")
        return []


def extract_links(html: str, base_url: str) -> List[Dict[str, str]]:
    """从HTML中提取所有JQData相关链接（备用方法）"""
    links = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # 方法1: 查找所有a标签中的链接
        for a in soup.find_all('a', href=True):
            href = a.get('href', '')
            if not href:
                continue
            
            # 转换为绝对URL
            full_url = urljoin(base_url, href)
            normalized_url = normalize_url(full_url)
            
            # 只保留聚宽API文档相关链接（必须包含/help/api/doc路径）
            if 'joinquant.com' in normalized_url and '/help/api/doc' in normalized_url:
                # 确保URL格式正确（包含name和id参数）
                if 'name=' in normalized_url and 'id=' in normalized_url:
                    link_text = a.get_text(strip=True) or href
                    links.append({
                        'url': normalized_url,
                        'text': link_text[:100]  # 限制长度
                    })
        
        # 方法2: 特别查找表格中的链接（侧栏目录通常在表格中）
        for table in soup.find_all(['table', 'tbody']):
            for a in table.find_all('a', href=True):
                href = a.get('href', '')
                if not href:
                    continue
                full_url = urljoin(base_url, href)
                normalized_url = normalize_url(full_url)
                if 'joinquant.com' in normalized_url and '/help/api/doc' in normalized_url:
                    if 'name=' in normalized_url and 'id=' in normalized_url:
                        link_text = a.get_text(strip=True) or href
                        links.append({
                            'url': normalized_url,
                            'text': link_text[:100]
                        })
        
        # 去重
        seen_urls = set()
        unique_links = []
        for link in links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)
        
        return unique_links
    except Exception as e:
        print(f"    ⚠️ 提取链接失败: {e}")
        return []


async def crawl_page(url: str, page_obj, depth: int = 0, max_depth: int = 2) -> Optional[Dict]:
    """爬取单个页面"""
    # 检查深度限制
    if depth > max_depth:
        return None
    
    # 规范化URL（移除锚点）
    url = normalize_url(url)
    
    # 检查是否已访问
    if url in visited_urls:
        return None
    
    visited_urls.add(url)
    STATS["total_links"] += 1
    
    try:
        print(f"  [{STATS['crawled']+1}] 爬取: {url}")
        
        # 访问页面（增加超时时间，使用更宽松的等待策略）
        try:
            await page_obj.goto(url, wait_until='networkidle', timeout=120000)  # 使用networkidle确保JS加载完成
            await page_obj.wait_for_timeout(5000)  # 等待JS执行，增加到5秒（确保侧栏菜单渲染）
        except Exception as goto_error:
            # 如果networkidle超时，尝试使用load事件
            print(f"    ⚠️ networkidle超时，尝试load策略...")
            try:
                await page_obj.goto(url, wait_until='load', timeout=120000)
                await page_obj.wait_for_timeout(8000)  # 等待更长时间
            except Exception as retry_error:
                # 最后一次尝试，使用domcontentloaded
                print(f"    ⚠️ load超时，使用domcontentloaded策略...")
                await page_obj.goto(url, wait_until='domcontentloaded', timeout=120000)
                await page_obj.wait_for_timeout(10000)  # 等待10秒确保内容加载
        
        # 获取HTML和文本
        html = await page_obj.content()
        title = extract_title(html, url)
        content = extract_content(html)
        
        if not content or len(content) < 100:
            print(f"    ⚠️ 内容太短，跳过")
            STATS["skipped"] += 1
            return None
        
        STATS["crawled"] += 1
        STATS["success"] += 1
        
        result = {
            'url': url,
            'title': title,
            'content': content,
            'html': html,
            'content_length': len(content),
            'crawled_at': datetime.now().isoformat()
        }
        
        # 提取子链接（用于递归爬取）- 使用高级方法
        if depth < max_depth:
            # 优先使用JavaScript方法提取链接（更准确）
            sub_links = await extract_links_advanced(page_obj, BASE_URL)
            # 如果JavaScript方法失败或结果为空，使用HTML解析备用方法
            if not sub_links:
                sub_links = extract_links(html, BASE_URL)
            
            result['sub_links'] = sub_links
            print(f"    ✅ 成功 ({len(content):,} 字符, {len(sub_links)} 个子链接)")
        else:
            print(f"    ✅ 成功 ({len(content):,} 字符)")
        
        return result
        
    except Exception as e:
        STATS["crawled"] += 1
        STATS["failed"] += 1
        print(f"    ❌ 失败: {str(e)[:100]}")
        return None


def save_to_knowledge_base(page_data: Dict) -> bool:
    """将页面数据存入知识库（结构化、有条理）"""
    if not KB_AVAILABLE:
        return False
    
    try:
        title = page_data['title']
        url = page_data['url']
        
        # 构建结构化内容（Markdown格式）
        content = f"""# {title}

## 基本信息
- **URL**: {url}
- **爬取时间**: {page_data['crawled_at']}
- **内容长度**: {page_data['content_length']} 字符

## 内容

{page_data['content']}
"""
        
        # 根据URL和标题确定分类标签（有序、有条理）
        tags = ['JQData', '聚宽数据', '官方文档']
        
        # 根据URL路径确定分类
        if 'doc?name=JQDatadoc' in url:
            tags.append('JQDatadoc文档')
            if 'id=' in url:
                tags.append('API函数文档')
        elif 'logon' in url:
            tags.append('登录认证文档')
        elif 'help' in url:
            tags.append('帮助文档')
        
        # 根据标题关键词确定具体分类（覆盖9步工作流）
        title_lower = title.lower()
        content_lower = page_data['content'][:2000].lower() if page_data.get('content') else ''
        
        # === 因子相关（步骤4：因子构建） ===
        if 'alpha' in title_lower or 'alpha' in content_lower[:500]:
            tags.append('因子构建')
            tags.append('Alpha因子')
            if '101' in title_lower or '101' in content_lower[:500]:
                tags.append('Alpha101')
            if '191' in title_lower or '191' in content_lower[:500]:
                tags.append('Alpha191')
        if '因子' in title or 'factor' in title_lower:
            tags.append('因子构建')
            tags.append('因子库')
        if '风险' in title or 'risk' in title_lower or 'cne' in title_lower:
            tags.append('风险模型')
            if 'cne5' in title_lower:
                tags.append('CNE5风格因子')
            if 'cne6' in title_lower:
                tags.append('CNE6风格因子')
        
        # === 市场数据（步骤1：市场趋势判断） ===
        if '宏观' in title or 'macro' in title_lower:
            tags.append('市场趋势')
            tags.append('宏观经济数据')
        if '指数' in title or 'index' in title_lower:
            tags.append('市场趋势')
            tags.append('指数数据')
        if '行情' in title or 'price' in title_lower or 'quote' in title_lower:
            tags.append('行情数据')
            tags.append('回测数据')
        
        # === 行业数据（步骤2：主线识别） ===
        if '行业' in title or 'industry' in title_lower or 'sector' in title_lower:
            tags.append('主线识别')
            tags.append('行业数据')
        if '板块' in title or '概念' in title:
            tags.append('主线识别')
            tags.append('板块数据')
        
        # === 股票筛选（步骤3：候选池） ===
        if '股票' in title or 'stock' in title_lower:
            tags.append('候选池')
            tags.append('股票数据')
        if '筛选' in title or 'filter' in title_lower or 'query' in title_lower:
            tags.append('候选池')
            tags.append('数据筛选')
        if '财务' in title or 'financial' in title_lower or 'valuation' in title_lower:
            tags.append('候选池')
            tags.append('财务数据')
        
        # === 技术指标（步骤4&5：因子&策略） ===
        if '技术' in title or 'technical' in title_lower:
            tags.append('因子构建')
            tags.append('技术指标')
        if 'macd' in title_lower or 'rsi' in title_lower or 'kdj' in title_lower:
            tags.append('因子构建')
            tags.append('技术指标')
        
        # === 交易函数（步骤5：策略生成） ===
        if '交易' in title or 'trade' in title_lower or 'order' in title_lower:
            tags.append('策略生成')
            tags.append('交易函数')
        if '买入' in title or '卖出' in title or 'buy' in title_lower or 'sell' in title_lower:
            tags.append('策略生成')
            tags.append('交易函数')
        
        # === 回测数据（步骤6：回测） ===
        if '历史' in title or 'history' in title_lower or 'historical' in title_lower:
            tags.append('回测数据')
        if '分钟' in title or 'minute' in title_lower or 'tick' in title_lower:
            tags.append('回测数据')
            tags.append('高频数据')
        
        # === 其他市场数据 ===
        if '期货' in title or 'futures' in title_lower:
            tags.append('期货数据')
        if '基金' in title or 'fund' in title_lower:
            tags.append('基金数据')
        if '期权' in title or 'option' in title_lower:
            tags.append('期权数据')
        if '债券' in title or 'bond' in title_lower:
            tags.append('债券数据')
        
        # === 认证和使用 ===
        if '试用' in title or '购买' in title or 'purchase' in title_lower:
            tags.append('购买说明')
        if '认证' in title or 'auth' in title_lower or 'login' in title_lower:
            tags.append('认证登录')
        
        # 确保标签唯一且有序
        tags = list(dict.fromkeys(tags))  # 保持顺序的去重
        
        # 存入知识库
        result = knowledge_add(
            title=title,
            content=content,
            type='reference',
            tags=tags,
            source=url
        )
        
        if result.get('success') or result.get('id') or result.get('knowledge_id'):
            STATS["saved_to_kb"] += 1
            return True
        else:
            error_msg = result.get('error', 'Unknown')
            print(f"    ⚠️ 存入知识库失败: {error_msg}")
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False


def save_to_file(page_data: Dict, index: int):
    """保存到文件（备份）"""
    try:
        safe_title = re.sub(r'[^\w\-_\.]', '_', page_data['title'])[:50]
        filename = f"{index:03d}_{safe_title}.txt"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"URL: {page_data['url']}\n")
            f.write(f"标题: {page_data['title']}\n")
            f.write(f"爬取时间: {page_data['crawled_at']}\n")
            f.write("=" * 70 + "\n\n")
            f.write(page_data['content'])
        
        return filepath
    except Exception as e:
        print(f"    ⚠️ 保存文件失败: {e}")
        return None


async def crawl_recursive(start_url: str, max_depth: int = 2):
    """递归爬取所有子页面"""
    async with async_playwright() as p:
        # 使用更宽松的浏览器选项
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        # 设置更长的超时时间
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        page.set_default_timeout(120000)  # 设置默认超时120秒
        
        # 待爬取队列
        queue: List[tuple[str, int]] = [(start_url, 0)]  # (url, depth)
        results: List[Dict] = []
        
        try:
            while queue and STATS["crawled"] < 500:  # 限制最多爬取500个页面
                url, depth = queue.pop(0)
                
                # 爬取当前页面
                page_data = await crawl_page(url, page, depth, max_depth)
                
                if page_data:
                    results.append(page_data)
                    
                    # 保存到文件
                    save_to_file(page_data, len(results))
                    
                    # 存入知识库
                    save_to_knowledge_base(page_data)
                    
                    # 添加子链接到队列
                    if 'sub_links' in page_data and depth < max_depth:
                        for link in page_data['sub_links']:
                            sub_url = normalize_url(link['url'])
                            if sub_url not in visited_urls:
                                queue.append((sub_url, depth + 1))
                    
                    # 避免请求过快（增加延迟，减少服务器压力）
                    await asyncio.sleep(2)  # 从1秒增加到2秒
            
            await context.close()
            await browser.close()
            
            # 保存visited_urls到文件
            if VISITED_URLS_FILE:
                save_visited_urls(VISITED_URLS_FILE)
            
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
            # 即使出错也保存visited_urls
            if VISITED_URLS_FILE:
                save_visited_urls(VISITED_URLS_FILE)
            try:
                await context.close()
            except:
                pass
            try:
                await browser.close()
            except:
                pass
        
        return results


async def main():
    """主函数"""
    global visited_urls, VISITED_URLS_FILE
    
    print("=" * 70)
    print("聚宽数据页面完整爬取 - 抓取所有子页面并存入知识库")
    print("=" * 70)
    print(f"起始URL: {JQDATA_DOC_URL}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"知识库可用: {'✅ 是' if KB_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    # 初始化visited_urls持久化文件
    VISITED_URLS_FILE = OUTPUT_DIR / "visited_urls.json"
    
    # 加载已访问的URL（如果存在）
    visited_urls = load_visited_urls(VISITED_URLS_FILE)
    if visited_urls:
        print(f"📋 已加载 {len(visited_urls)} 个已访问的URL，将跳过这些页面")
        print()
    
    # 开始爬取
    start_time = datetime.now()
    results = await crawl_recursive(JQDATA_DOC_URL, max_depth=2)
    end_time = datetime.now()
    
    # 最终保存visited_urls
    if VISITED_URLS_FILE:
        save_visited_urls(VISITED_URLS_FILE)
    
    # 保存结果摘要
    summary = {
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'duration_seconds': (end_time - start_time).total_seconds(),
        'stats': STATS,
        'results_count': len(results),
        'results': [
            {
                'url': r['url'],
                'title': r['title'],
                'content_length': r['content_length']
            }
            for r in results
        ]
    }
    
    summary_file = OUTPUT_DIR / f"crawl_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 打印统计信息
    print()
    print("=" * 70)
    print("爬取完成 - 统计信息")
    print("=" * 70)
    print(f"总链接数: {STATS['total_links']}")
    print(f"已爬取: {STATS['crawled']}")
    print(f"成功: {STATS['success']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过: {STATS['skipped']}")
    print(f"存入知识库: {STATS['saved_to_kb']}")
    print(f"耗时: {(end_time - start_time).total_seconds():.1f} 秒")
    print(f"结果摘要: {summary_file}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

