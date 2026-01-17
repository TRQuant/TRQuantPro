#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PTrade API文档完整爬取脚本

功能：
1. 爬取PTrade API文档网站的所有侧栏链接页面
2. 提取页面内容并结构化
3. 存入RAG知识库

Author: TRQuant Team
Date: 2026-01-09
"""

import sys
import asyncio
import json
import re
import time
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse
from collections import deque

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装，请安装: pip install playwright && playwright install")

try:
    from mcp_servers.unified_dev_server import knowledge_add, knowledge_search
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 知识库工具不可用: {e}")
    KB_AVAILABLE = False

# PTrade API文档基础URL
BASE_URL = "https://ptradeapi.com"
START_URL = "https://ptradeapi.com/"

# 输出目录
OUTPUT_DIR = PROJECT_ROOT / "docs" / "ptrade_crawled"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 配置
CONFIG = {
    "wait_timeout": 60000,             # 60秒超时
    "networkidle_wait": 3000,          # 3秒networkidle等待
    "extra_wait": 5000,                # 5秒额外等待
    "retry_times": 3,                  # 重试次数
    "retry_delay": 5,                  # 重试延迟（秒）
    "rate_limit_delay": 2,             # 请求间隔（秒）
    "concurrent_pages": 3,             # 并发页面数
}

# 统计信息
STATS = {
    "total_links": 0,
    "crawled": 0,
    "success": 0,
    "failed": 0,
    "skipped": 0,
    "saved_to_kb": 0,
    "duplicates_skipped": 0,
    "start_time": None,
}

visited_urls: Set[str] = set()
PROGRESS_FILE = OUTPUT_DIR / "crawl_progress.json"
VISITED_URLS_FILE = OUTPUT_DIR / "visited_urls.json"
FAILED_URLS_FILE = OUTPUT_DIR / "failed_urls.json"
CONTENT_HASH_FILE = OUTPUT_DIR / "content_hashes.json"

failed_urls: List[Tuple[str, int, str]] = []
content_hashes: Set[str] = set()


def load_progress():
    """加载爬取进度"""
    global visited_urls, content_hashes
    
    if VISITED_URLS_FILE.exists():
        try:
            visited_urls = set(json.loads(VISITED_URLS_FILE.read_text(encoding='utf-8')))
            print(f"✅ 加载已访问URL: {len(visited_urls)} 个")
        except:
            pass
    
    if CONTENT_HASH_FILE.exists():
        try:
            content_hashes = set(json.loads(CONTENT_HASH_FILE.read_text(encoding='utf-8')))
            print(f"✅ 加载内容哈希: {len(content_hashes)} 个")
        except:
            pass


def save_progress():
    """保存爬取进度"""
    VISITED_URLS_FILE.write_text(json.dumps(list(visited_urls), ensure_ascii=False, indent=2), encoding='utf-8')
    CONTENT_HASH_FILE.write_text(json.dumps(list(content_hashes), ensure_ascii=False, indent=2), encoding='utf-8')
    
    if failed_urls:
        failed_data = [{"url": url, "retries": retries, "error": error} for url, retries, error in failed_urls]
        FAILED_URLS_FILE.write_text(json.dumps(failed_data, ensure_ascii=False, indent=2), encoding='utf-8')


async def extract_sidebar_links(page) -> List[Dict[str, str]]:
    """提取侧栏链接"""
    try:
        # 等待侧栏加载
        try:
            await page.wait_for_selector('nav, .sidebar, .menu, [role="navigation"], aside', timeout=10000)
        except:
            pass  # 如果找不到选择器，继续尝试
        
        # 使用JavaScript提取所有链接
        links_data = await page.evaluate('''
            () => {
                const links = [];
                const seen = new Set();
                
                // 查找所有可能的导航区域
                const navSelectors = [
                    'nav a[href]',
                    '.sidebar a[href]',
                    '.menu a[href]',
                    '[role="navigation"] a[href]',
                    'aside a[href]',
                    '.nav a[href]',
                    'ul a[href]',
                    'li a[href]',
                ];
                
                navSelectors.forEach(selector => {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(elem => {
                        const href = elem.getAttribute('href');
                        const text = elem.textContent.trim();
                        if (href && text && !seen.has(href)) {
                            seen.add(href);
                            links.push({
                                href: href,
                                text: text.substring(0, 200)
                            });
                        }
                    });
                });
                
                return links;
            }
        ''')
        
        # 转换为绝对URL，过滤掉锚点链接（只保留真正的页面链接）
        links = []
        for link_data in links_data:
            href = link_data['href']
            # 跳过纯锚点链接（#开头且没有.html等扩展名）
            if href.startswith('#') and not any(ext in href for ext in ['.html', '.htm', '.php', '.aspx']):
                continue
            
            full_url = urljoin(BASE_URL, href)
            if full_url.startswith(BASE_URL):
                links.append({
                    'url': full_url,
                    'text': link_data['text'],
                    'href': href
                })
        
        # 去重
        seen = set()
        unique_links = []
        for link in links:
            if link['url'] not in seen:
                seen.add(link['url'])
                unique_links.append(link)
        
        return unique_links
    
    except Exception as e:
        print(f"⚠️ 提取侧栏链接失败: {e}")
        return []


async def extract_page_content(page) -> Dict[str, any]:
    """提取页面内容"""
    try:
        # 等待主要内容加载
        await page.wait_for_load_state('networkidle', timeout=CONFIG['networkidle_wait'])
        await asyncio.sleep(CONFIG['extra_wait'] / 1000)
        
        # 获取标题
        title = await page.title() or "PTrade API文档"
        
        # 获取URL
        url = page.url
        
        # 使用JavaScript提取内容
        page_data = await page.evaluate('''
            () => {
                const result = {
                    content: '',
                    code_blocks: [],
                    api_functions: []
                };
                
                // 提取主要内容
                const contentSelectors = [
                    'main',
                    '.content',
                    '.main-content',
                    'article',
                    '#content',
                    '.documentation',
                    '.api-doc',
                ];
                
                for (const selector of contentSelectors) {
                    const elem = document.querySelector(selector);
                    if (elem) {
                        result.content = elem.innerText || elem.textContent || '';
                        if (result.content.length > 100) {
                            break;
                        }
                    }
                }
                
                // 如果没有找到主要内容，使用body
                if (result.content.length < 100) {
                    const body = document.querySelector('body');
                    if (body) {
                        result.content = body.innerText || body.textContent || '';
                    }
                }
                
                // 提取代码块
                const codeElements = document.querySelectorAll('pre code, code');
                codeElements.forEach(elem => {
                    const codeText = elem.innerText || elem.textContent || '';
                    if (codeText && codeText.length > 10) {
                        result.code_blocks.push(codeText);
                    }
                });
                
                // 提取API函数名
                const functionPattern = /(?:def|function)\\s+(\\w+)\\s*\\(|(\\w+)\\s*\\([^)]*\\)/g;
                const matches = result.content.matchAll(functionPattern);
                const functions = new Set();
                for (const match of matches) {
                    if (match[1]) functions.add(match[1]);
                    if (match[2]) functions.add(match[2]);
                }
                result.api_functions = Array.from(functions);
                
                return result;
            }
        ''')
        
        main_content = page_data.get('content', '')
        code_blocks = page_data.get('code_blocks', [])
        api_functions = page_data.get('api_functions', [])
        
        return {
            'title': title,
            'url': url,
            'content': main_content,
            'code_blocks': code_blocks,
            'api_functions': api_functions,
            'content_length': len(main_content),
        }
    
    except Exception as e:
        print(f"⚠️ 提取页面内容失败: {e}")
        try:
            title = await page.title() or "PTrade API文档"
        except:
            title = "PTrade API文档"
        return {
            'title': title,
            'url': page.url,
            'content': '',
            'code_blocks': [],
            'api_functions': [],
            'content_length': 0,
        }


def classify_and_tag(page_data: Dict) -> List[str]:
    """根据内容分类和标签"""
    tags = ['PTrade', 'API文档', '量化交易']
    
    url = page_data.get('url', '')
    title = page_data.get('title', '')
    content = page_data.get('content', '')
    
    # 根据URL路径分类
    if '/api/' in url or 'api' in url.lower():
        tags.append('API接口')
    
    if 'trade' in url.lower() or '交易' in title or '交易' in content:
        tags.append('交易')
    
    if 'data' in url.lower() or '数据' in title or '数据' in content:
        tags.append('数据')
    
    if 'order' in url.lower() or '委托' in title or '委托' in content:
        tags.append('委托下单')
    
    if 'position' in url.lower() or '持仓' in title or '持仓' in content:
        tags.append('持仓查询')
    
    if 'fundamental' in url.lower() or '财务' in title or '财务' in content:
        tags.append('财务数据')
    
    if 'history' in url.lower() or '历史' in title or '历史' in content:
        tags.append('历史数据')
    
    if 'schedule' in url.lower() or '定时' in title or '定时' in content:
        tags.append('定时任务')
    
    if 'run_daily' in content or 'run_interval' in content:
        tags.append('定时函数')
    
    if 'get_price' in content or 'get_history' in content:
        tags.append('行情数据')
    
    if 'order' in content and 'def' in content:
        tags.append('交易函数')
    
    # 根据API函数分类
    api_functions = page_data.get('api_functions', [])
    if api_functions:
        tags.append('函数文档')
    
    return list(dict.fromkeys(tags))  # 去重


def save_to_knowledge_base(page_data: Dict) -> bool:
    """保存到知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        # 计算内容哈希（用于去重）
        content_hash = hashlib.md5(page_data['content'].encode('utf-8')).hexdigest()
        if content_hash in content_hashes:
            STATS['duplicates_skipped'] += 1
            return False
        
        content_hashes.add(content_hash)
        
        # 分类和标签
        tags = classify_and_tag(page_data)
        
        # 构建知识库内容
        kb_content = f"""# {page_data['title']}

**URL**: {page_data['url']}

## 内容

{page_data['content']}

"""
        
        # 添加代码块
        if page_data.get('code_blocks'):
            kb_content += "\n## 代码示例\n\n"
            for i, code in enumerate(page_data['code_blocks'][:5], 1):  # 最多5个代码块
                kb_content += f"### 代码示例 {i}\n\n```python\n{code}\n```\n\n"
        
        # 添加API函数列表
        if page_data.get('api_functions'):
            kb_content += f"\n## API函数\n\n"
            kb_content += ", ".join(page_data['api_functions'][:20])  # 最多20个函数
        
        # 添加到知识库
        result = knowledge_add(
            title=f"PTrade API: {page_data['title']}",
            content=kb_content,
            type='reference',
            tags=tags,
            source=page_data['url']
        )
        
        if result.get('success') or result.get('knowledge_id'):
            STATS['saved_to_kb'] += 1
            return True
        else:
            print(f"  ❌ 知识库存储失败: {result.get('error', 'Unknown error')}")
            return False
    
    except Exception as e:
        print(f"  ❌ 知识库存储异常: {e}")
        return False


async def crawl_page(browser, url: str, retries: int = 0) -> bool:
    """爬取单个页面"""
    if url in visited_urls:
        STATS['skipped'] += 1
        return True
    
    if not url.startswith(BASE_URL):
        return False
    
    try:
        page = await browser.new_page()
        
        try:
            # 访问页面
            await page.goto(url, wait_until='networkidle', timeout=CONFIG['wait_timeout'])
            
            # 提取内容
            page_data = await extract_page_content(page)
            
            if page_data['content_length'] < 50:
                print(f"  ⚠️ 内容太短，跳过: {url}")
                await page.close()
                return False
            
            # 保存到知识库
            if save_to_knowledge_base(page_data):
                print(f"  ✅ 已存入知识库: {page_data['title'][:50]}")
            
            # 保存页面数据（备份）
            url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
            page_file = OUTPUT_DIR / f"page_{url_hash}.json"
            page_file.write_text(json.dumps(page_data, ensure_ascii=False, indent=2), encoding='utf-8')
            
            visited_urls.add(url)
            STATS['crawled'] += 1
            STATS['success'] += 1
            
            await page.close()
            return True
        
        except PlaywrightTimeout:
            print(f"  ⚠️ 页面加载超时: {url}")
            await page.close()
            if retries < CONFIG['retry_times']:
                await asyncio.sleep(CONFIG['retry_delay'])
                return await crawl_page(browser, url, retries + 1)
            else:
                failed_urls.append((url, retries, "Timeout"))
                STATS['failed'] += 1
                return False
        
        except Exception as e:
            print(f"  ❌ 爬取失败: {url} - {e}")
            await page.close()
            if retries < CONFIG['retry_times']:
                await asyncio.sleep(CONFIG['retry_delay'])
                return await crawl_page(browser, url, retries + 1)
            else:
                failed_urls.append((url, retries, str(e)))
                STATS['failed'] += 1
                return False
    
    except Exception as e:
        print(f"  ❌ 创建页面失败: {url} - {e}")
        STATS['failed'] += 1
        return False


async def crawl_sidebar_links(browser) -> List[Dict[str, str]]:
    """爬取侧栏链接"""
    print(f"\n📋 获取侧栏链接...")
    print(f"   访问: {START_URL}")
    
    page = await browser.new_page()
    
    try:
        print("   ⏳ 加载页面...")
        await page.goto(START_URL, wait_until='networkidle', timeout=CONFIG['wait_timeout'])
        print("   ✅ 页面加载完成")
        
        print("   ⏳ 等待页面稳定...")
        await asyncio.sleep(CONFIG['extra_wait'] / 1000)
        
        print("   🔍 提取侧栏链接...")
        # 提取侧栏链接
        all_links = await extract_sidebar_links(page)
        
        # 过滤：只保留真实页面（.html文件），过滤掉纯锚点链接
        real_pages = []
        for link in all_links:
            url = link['url']
            href = link.get('href', '')
            # 保留.html页面，或者不是纯锚点的链接
            if '.html' in url or (not href.startswith('#') and href != '#'):
                real_pages.append(link)
        
        print(f"   📊 总链接数: {len(all_links)}")
        print(f"   ✅ 真实页面: {len(real_pages)}")
        print(f"   ⏭️  锚点链接: {len(all_links) - len(real_pages)} (已过滤)")
        
        if real_pages:
            print("   📋 真实页面列表（前10个）:")
            for i, link in enumerate(real_pages[:10], 1):
                print(f"      {i}. {link.get('text', '')[:50]} - {link['url']}")
        
        # 保存所有链接和真实页面
        sidebar_file = OUTPUT_DIR / "sidebar_links.json"
        sidebar_file.write_text(json.dumps(all_links, ensure_ascii=False, indent=2), encoding='utf-8')
        
        real_pages_file = OUTPUT_DIR / "real_pages.json"
        real_pages_file.write_text(json.dumps(real_pages, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"   💾 侧栏链接已保存: {sidebar_file}")
        print(f"   💾 真实页面已保存: {real_pages_file}")
        
        await page.close()
        return real_pages  # 只返回真实页面
    
    except Exception as e:
        print(f"   ❌ 获取侧栏链接失败: {e}")
        import traceback
        traceback.print_exc()
        try:
            await page.close()
        except:
            pass
        return []


async def crawl_all_pages(links: List[Dict[str, str]]):
    """爬取所有页面"""
    print(f"\n🚀 开始爬取 {len(links)} 个页面...")
    print("=" * 70)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        try:
            # 创建信号量控制并发
            semaphore = asyncio.Semaphore(CONFIG['concurrent_pages'])
            
            async def crawl_with_semaphore(link: Dict[str, str]):
                async with semaphore:
                    url = link['url']
                    text = link.get('text', '')
                    print(f"\n[{STATS['crawled'] + 1}/{len(links)}] {text[:50]} - {url}")
                    
                    success = await crawl_page(browser, url)
                    
                    # 保存进度
                    if STATS['crawled'] % 10 == 0:
                        save_progress()
                    
                    # 限流
                    await asyncio.sleep(CONFIG['rate_limit_delay'])
                    
                    return success
            
            # 并发爬取
            tasks = [crawl_with_semaphore(link) for link in links]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        finally:
            await browser.close()


async def main():
    """主函数"""
    print("=" * 70)
    print("📚 PTrade API文档爬取脚本")
    print("=" * 70)
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装，请先安装: pip install playwright && playwright install")
        return
    
    if not KB_AVAILABLE:
        print("⚠️ 知识库工具不可用，将只保存到本地文件")
    
    # 加载进度
    print("\n📂 加载爬取进度...")
    load_progress()
    
    STATS['start_time'] = datetime.now().isoformat()
    
    print("\n🚀 启动浏览器...")
    try:
        async with async_playwright() as p:
            print("   ✅ Playwright已启动")
            print("   🔧 启动Chromium浏览器...")
            browser = await p.chromium.launch(
                headless=True,
                timeout=30000  # 30秒超时
            )
            print("   ✅ 浏览器已启动")
            
            try:
                # 1. 获取侧栏链接
                print("\n" + "=" * 70)
                links = await crawl_sidebar_links(browser)
                
                if not links:
                    print("❌ 未找到侧栏链接")
                    print("💡 提示: 可能需要手动检查网站结构或使用浏览器工具")
                    return
                
                STATS['total_links'] = len(links)
                print(f"\n✅ 共找到 {len(links)} 个链接，准备爬取...")
                
                # 2. 爬取所有页面
                await crawl_all_pages(links)
            
            finally:
                print("\n🔒 关闭浏览器...")
                await browser.close()
                print("   ✅ 浏览器已关闭")
    
    except Exception as e:
        print(f"\n❌ 主函数异常: {e}")
        import traceback
        traceback.print_exc()
    
    # 保存最终进度
    save_progress()
    
    # 打印统计信息
    print("\n" + "=" * 70)
    print("📊 爬取统计")
    print("=" * 70)
    print(f"总链接数: {STATS['total_links']}")
    print(f"已爬取: {STATS['crawled']}")
    print(f"成功: {STATS['success']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过: {STATS['skipped']}")
    print(f"存入知识库: {STATS['saved_to_kb']}")
    print(f"重复跳过: {STATS['duplicates_skipped']}")
    print("=" * 70)
    
    if failed_urls:
        print(f"\n⚠️ 失败URL ({len(failed_urls)} 个):")
        for url, retries, error in failed_urls[:10]:
            print(f"   - {url} ({retries}次重试): {error}")


if __name__ == "__main__":
    asyncio.run(main())
