#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API文档完整爬取脚本 - 使用现有爬虫工具组合

使用Selenium + Playwright组合，充分利用现有工具：
- crawler_selenium_fetch: 处理JavaScript渲染
- Playwright: 更强大的浏览器自动化
- knowledge_add: 存储到知识库

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
from urllib.parse import urljoin

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装")

try:
    from mcp_servers.unified_dev_server import crawler_selenium_fetch, knowledge_add
    CRAWLER_AVAILABLE = True
    KB_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 爬虫工具或知识库工具不可用: {e}")
    CRAWLER_AVAILABLE = False
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

# 已访问的URL集合
visited_urls: Set[str] = set()
VISITED_URLS_FILE: Optional[Path] = None


def normalize_url(url: str) -> str:
    """规范化URL（移除锚点）"""
    return url.split('#')[0]


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


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


async def extract_all_links_playwright(page_obj) -> List[Dict[str, str]]:
    """使用Playwright提取所有文档链接（最准确的方法）"""
    try:
        # 使用JavaScript提取所有链接
        js_links = await page_obj.evaluate('''
            () => {
                const results = [];
                const seenUrls = new Set();
                
                // 查找所有文档链接
                const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
                
                allLinks.forEach(link => {
                    const href = link.href || link.getAttribute('href');
                    if (!href) return;
                    
                    // 去除锚点
                    const cleanHref = href.split('#')[0];
                    
                    if (cleanHref.includes('name=') && cleanHref.includes('id=') && !seenUrls.has(cleanHref)) {
                        const text = link.textContent.trim() || '';
                        seenUrls.add(cleanHref);
                        results.push({
                            url: cleanHref,
                            text: text.substring(0, 150)
                        });
                    }
                });
                
                return results;
            }
        ''')
        
        return js_links
    except Exception as e:
        print(f"    ⚠️ Playwright提取链接失败: {e}")
        return []


async def crawl_page_playwright(url: str, page_obj, depth: int = 0, max_depth: int = 3) -> Optional[Dict]:
    """使用Playwright爬取单个页面"""
    if depth > max_depth:
        return None
    
    url = normalize_url(url)
    
    if url in visited_urls:
        return None
    
    visited_urls.add(url)
    STATS["total_links"] += 1
    
    try:
        print(f"  [{STATS['crawled']+1}] 爬取: {url}")
        
        # 使用networkidle等待策略，确保JavaScript完全加载
        await page_obj.goto(url, wait_until='networkidle', timeout=120000)
        await page_obj.wait_for_timeout(5000)  # 额外等待5秒，确保侧栏菜单渲染
        
        # 获取页面内容
        html = await page_obj.content()
        
        # 提取标题和内容
        title = await page_obj.title()
        title = title.replace(' - JoinQuant', '').strip()
        
        # 提取文本内容
        try:
            body_text = await page_obj.evaluate('''
                () => {
                    // 移除script和style
                    const scripts = document.querySelectorAll('script, style, nav, header, footer');
                    scripts.forEach(el => el.remove());
                    
                    // 获取主要内容
                    const main = document.querySelector('main') || document.body;
                    return main.innerText || '';
                }
            ''')
            content = clean_text(body_text)
        except:
            content = ""
        
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
        
        # 提取子链接
        if depth < max_depth:
            sub_links = await extract_all_links_playwright(page_obj)
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


def classify_and_tag(page_data: Dict) -> List[str]:
    """分类并生成标签"""
    tags = ['JQData', '聚宽数据', '官方文档']
    
    title = page_data.get('title', '')
    content = page_data.get('content', '')[:3000]
    url = page_data.get('url', '')
    
    title_lower = title.lower()
    content_lower = content.lower()
    
    # 根据URL路径确定分类
    if 'doc?name=JQDatadoc' in url:
        tags.append('JQDatadoc文档')
        if 'id=' in url:
            tags.append('API函数文档')
    
    # === 因子相关 ===
    if 'alpha' in title_lower or 'alpha' in content_lower[:500]:
        tags.append('因子构建')
        tags.append('Alpha因子')
        if '101' in title_lower or 'alpha101' in content_lower:
            tags.append('Alpha101')
        if '191' in title_lower or 'alpha191' in content_lower:
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
    
    # === 市场数据 ===
    if '宏观' in title or 'macro' in content_lower[:500]:
        tags.append('市场趋势')
        tags.append('宏观经济数据')
    
    if '指数' in title or 'index' in content_lower[:500]:
        tags.append('市场趋势')
        tags.append('指数数据')
    
    # === 行业数据 ===
    if '行业' in title or 'industry' in content_lower[:500]:
        tags.append('主线识别')
        tags.append('行业数据')
    
    # === 股票筛选 ===
    if '股票' in title or 'stock' in content_lower[:500]:
        tags.append('候选池')
        tags.append('股票数据')
    
    # === 交易函数 ===
    if '交易' in content[:500] or '下单' in content[:500]:
        tags.append('策略生成')
        tags.append('交易函数')
    
    # === 回测数据 ===
    if '历史' in content[:500] or '分钟' in title or 'tick' in title_lower:
        tags.append('回测数据')
    
    # 去重
    return list(dict.fromkeys(tags))


def save_to_knowledge_base(page_data: Dict) -> bool:
    """将页面数据存入知识库"""
    if not KB_AVAILABLE:
        return False
    
    try:
        title = page_data['title']
        url = page_data['url']
        
        # 生成标签
        tags = classify_and_tag(page_data)
        
        # 构建结构化内容
        content = f"""# {title}

## 基本信息
- **URL**: {url}
- **爬取时间**: {page_data['crawled_at']}
- **内容长度**: {page_data['content_length']} 字符

## 内容

{page_data['content']}
"""
        
        result = knowledge_add(
            title=title,
            content=content,
            type='api_reference',
            tags=tags,
            source=url
        )
        
        if result.get('success') or result.get('id') or result.get('knowledge_id'):
            STATS["saved_to_kb"] += 1
            return True
        else:
            print(f"    ⚠️ 存入知识库失败")
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False


async def crawl_recursive_playwright(start_url: str, max_depth: int = 3):
    """使用Playwright递归爬取所有页面"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = await context.new_page()
        page.set_default_timeout(120000)
        
        # 待爬取队列
        queue: List[tuple[str, int]] = [(start_url, 0)]
        results: List[Dict] = []
        
        try:
            while queue and STATS["crawled"] < 500:  # 限制最多500个页面
                url, depth = queue.pop(0)
                
                # 爬取当前页面
                page_data = await crawl_page_playwright(url, page, depth, max_depth)
                
                if page_data:
                    results.append(page_data)
                    
                    # 存入知识库
                    save_to_knowledge_base(page_data)
                    
                    # 添加子链接到队列
                    if 'sub_links' in page_data and depth < max_depth:
                        for link in page_data['sub_links']:
                            sub_url = normalize_url(link['url'])
                            if sub_url not in visited_urls:
                                queue.append((sub_url, depth + 1))
                    
                    # 延迟避免请求过快
                    await asyncio.sleep(2)
            
            await context.close()
            await browser.close()
            
            # 保存visited_urls
            if VISITED_URLS_FILE:
                save_visited_urls(VISITED_URLS_FILE)
            
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
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
    print("聚宽API文档完整爬取 - 使用Selenium+Playwright组合")
    print("=" * 70)
    print(f"起始URL: {JQDATA_DOC_URL}")
    print(f"输出目录: {OUTPUT_DIR}")
    print(f"Playwright可用: {'✅ 是' if PLAYWRIGHT_AVAILABLE else '❌ 否'}")
    print(f"知识库可用: {'✅ 是' if KB_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    # 初始化visited_urls持久化
    VISITED_URLS_FILE = OUTPUT_DIR / "visited_urls.json"
    visited_urls = load_visited_urls(VISITED_URLS_FILE)
    if visited_urls:
        print(f"📋 已加载 {len(visited_urls)} 个已访问的URL，将跳过这些页面")
        print()
    
    # 开始爬取
    start_time = datetime.now()
    results = await crawl_recursive_playwright(JQDATA_DOC_URL, max_depth=3)
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
        'results_count': len(results)
    }
    
    summary_file = OUTPUT_DIR / f"crawl_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 打印统计
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

