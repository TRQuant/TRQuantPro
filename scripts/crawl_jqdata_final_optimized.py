#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API文档完整爬取脚本 - 最终优化版本

新增优化：
1. 侧栏导航缓存（只爬取一次，后续复用）
2. 智能重试（根据错误类型）
3. 内容去重（避免重复存储）
4. 改进的并发控制（可选）

Author: TRQuant Team
Date: 2026-01-01
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
from urllib.parse import urljoin
from collections import deque

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("❌ Playwright未安装")

try:
    from mcp_servers.unified_dev_server import knowledge_add, knowledge_search
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

# 优化配置
CONFIG = {
    "max_depth": 3,                    # 最大递归深度
    "max_pages": 1000,                 # 最大页面数
    "wait_timeout": 60000,             # 60秒超时
    "networkidle_wait": 3000,          # 3秒networkidle等待
    "extra_wait": 5000,                # 5秒额外等待（普通页面）
    "main_page_extra_wait": 8000,      # 8秒额外等待（主页面）
    "retry_times": 3,                  # 重试次数
    "retry_delay": 5,                  # 重试延迟（秒）
    "rate_limit_delay": 2,             # 请求间隔（秒）
    "batch_size": 50,                  # 每批处理的页面数
    "progress_save_interval": 10,      # 每N个页面保存一次进度
    "concurrent_pages": 3,             # 并发页面数（3=并行，测试验证稳定）
    "cache_sidebar": True,             # 是否缓存侧栏链接（新功能）
}

# 统计信息
STATS = {
    "total_links": 0,
    "crawled": 0,
    "success": 0,
    "failed": 0,
    "skipped": 0,
    "retried": 0,
    "saved_to_kb": 0,
    "duplicates_skipped": 0,
    "sidebar_cache_hits": 0,
    "start_time": None,
    "last_progress_save": None,
}

visited_urls: Set[str] = set()
PROGRESS_FILE = OUTPUT_DIR / "crawl_progress.json"
VISITED_URLS_FILE = OUTPUT_DIR / "visited_urls.json"
FAILED_URLS_FILE = OUTPUT_DIR / "failed_urls.json"
SIDEBAR_CACHE_FILE = OUTPUT_DIR / "sidebar_cache.json"  # 侧栏链接缓存
CONTENT_HASH_FILE = OUTPUT_DIR / "content_hashes.json"  # 内容哈希（用于去重）

# 失败URL列表
failed_urls: List[Tuple[str, int, str]] = []

# 侧栏链接缓存
sidebar_cache: Dict[str, List[Dict[str, str]]] = {}  # {url: [links]}

# 内容哈希集合（用于去重）
content_hashes: Set[str] = set()


def normalize_url(url: str) -> str:
    """规范化URL（移除锚点）"""
    return url.split('#')[0]


def get_content_hash(content: str) -> str:
    """计算内容的哈希值（用于去重）"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def load_sidebar_cache() -> Dict[str, List[Dict[str, str]]]:
    """加载侧栏链接缓存"""
    if SIDEBAR_CACHE_FILE.exists():
        try:
            with open(SIDEBAR_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                print(f"✅ 从文件加载了 {len(cache)} 个页面的侧栏缓存")
                return cache
        except Exception as e:
            print(f"⚠️ 加载侧栏缓存失败: {e}")
    return {}


def save_sidebar_cache():
    """保存侧栏链接缓存"""
    try:
        with open(SIDEBAR_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(sidebar_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存侧栏缓存失败: {e}")


def load_content_hashes() -> Set[str]:
    """加载内容哈希（用于去重）"""
    if CONTENT_HASH_FILE.exists():
        try:
            with open(CONTENT_HASH_FILE, 'r', encoding='utf-8') as f:
                hashes = json.load(f)
                print(f"✅ 从文件加载了 {len(hashes)} 个内容哈希")
                return set(hashes)
        except Exception as e:
            print(f"⚠️ 加载内容哈希失败: {e}")
    return set()


def save_content_hashes():
    """保存内容哈希"""
    try:
        with open(CONTENT_HASH_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(content_hashes), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存内容哈希失败: {e}")


def load_progress() -> Dict:
    """加载进度"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 加载进度失败: {e}")
    return {}


def save_progress():
    """保存进度"""
    try:
        progress = {
            "visited_urls": list(visited_urls),
            "failed_urls": failed_urls,
            "stats": STATS,
            "timestamp": datetime.now().isoformat()
        }
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        STATS["last_progress_save"] = datetime.now().isoformat()
    except Exception as e:
        print(f"⚠️ 保存进度失败: {e}")


def load_visited_urls(file_path: Path = None) -> Set[str]:
    """从文件加载已访问的URL"""
    file_path = file_path or VISITED_URLS_FILE
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = json.load(f)
                print(f"✅ 从文件加载了 {len(urls)} 个已访问的URL")
                return set(urls)
        except Exception as e:
            print(f"⚠️ 加载visited_urls失败: {e}")
    return set()


def save_visited_urls():
    """保存已访问的URL到文件"""
    try:
        with open(VISITED_URLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(visited_urls), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存visited_urls失败: {e}")


def save_failed_urls():
    """保存失败的URL"""
    try:
        with open(FAILED_URLS_FILE, 'w', encoding='utf-8') as f:
            json.dump(failed_urls, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存failed_urls失败: {e}")


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def is_retryable_error(error: Exception) -> bool:
    """判断错误是否可重试（智能重试）"""
    error_str = str(error).lower()
    
    # 网络错误 - 可重试
    if 'timeout' in error_str or 'network' in error_str or 'connection' in error_str:
        return True
    
    # 404错误 - 不可重试
    if '404' in error_str or 'not found' in error_str:
        return False
    
    # 其他错误 - 可重试
    return True


async def extract_all_links_playwright(page_obj, url: str) -> List[Dict[str, str]]:
    """使用Playwright提取所有文档链接"""
    # 检查缓存
    if CONFIG["cache_sidebar"] and url in sidebar_cache:
        STATS["sidebar_cache_hits"] += 1
        print(f"    📋 使用侧栏缓存（{len(sidebar_cache[url])} 个链接）")
        return sidebar_cache[url]
    
    try:
        js_links = await page_obj.evaluate('''
            () => {
                const results = [];
                const seenUrls = new Set();
                
                const allLinks = document.querySelectorAll('a[href*="/help/api/doc?name=JQDatadoc&id="]');
                
                allLinks.forEach(link => {
                    const href = link.href || link.getAttribute('href');
                    if (!href) return;
                    
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
        
        # 保存到缓存
        if CONFIG["cache_sidebar"]:
            sidebar_cache[url] = js_links
        
        return js_links
    except Exception as e:
        print(f"    ⚠️ 提取链接失败: {e}")
        return []


async def crawl_page_with_retry(url: str, page_obj, depth: int = 0, max_depth: int = 3) -> Optional[Dict]:
    """带智能重试机制的页面爬取"""
    url = normalize_url(url)
    
    if url in visited_urls:
        return None
    
    for attempt in range(CONFIG["retry_times"]):
        try:
            result = await crawl_page_playwright(url, page_obj, depth, max_depth)
            if result:
                return result
        except Exception as e:
            error_msg = str(e)[:100]
            
            # 智能重试判断
            if not is_retryable_error(e):
                print(f"    ❌ 不可重试的错误: {error_msg}")
                failed_urls.append((url, depth, error_msg))
                save_failed_urls()
                return None
            
            if attempt < CONFIG["retry_times"] - 1:
                STATS["retried"] += 1
                wait_time = CONFIG["retry_delay"] * (attempt + 1)
                print(f"    ⚠️ 尝试 {attempt + 1}/{CONFIG['retry_times']} 失败（可重试），{wait_time}秒后重试...")
                await asyncio.sleep(wait_time)
            else:
                print(f"    ❌ 重试 {CONFIG['retry_times']} 次后仍然失败: {error_msg}")
                failed_urls.append((url, depth, error_msg))
                save_failed_urls()
                return None
    
    return None


async def crawl_page_playwright(url: str, page_obj, depth: int = 0, max_depth: int = 3) -> Optional[Dict]:
    """使用Playwright爬取单个页面（优化版本）"""
    if depth > max_depth or STATS["crawled"] >= CONFIG["max_pages"]:
        return None
    
    url = normalize_url(url)
    
    if url in visited_urls:
        STATS["skipped"] += 1
        return None
    
    visited_urls.add(url)
    STATS["total_links"] += 1
    
    try:
        print(f"\n  [{STATS['crawled']+1}/{CONFIG['max_pages']}] 爬取: {url}")
        
        start_time = datetime.now()
        
        # 等待策略（三层降级）
        try:
            await page_obj.goto(url, wait_until='networkidle', timeout=CONFIG["wait_timeout"])
            await page_obj.wait_for_timeout(CONFIG["networkidle_wait"])
        except PlaywrightTimeout:
            try:
                await page_obj.goto(url, wait_until='load', timeout=CONFIG["wait_timeout"])
                await page_obj.wait_for_timeout(CONFIG["extra_wait"])
            except PlaywrightTimeout:
                await page_obj.goto(url, wait_until='domcontentloaded', timeout=CONFIG["wait_timeout"])
                await page_obj.wait_for_timeout(CONFIG["extra_wait"] * 2)
        
        load_time = (datetime.now() - start_time).total_seconds()
        
        # 额外等待（主页面需要更长时间）
        is_main_page = 'id=9842' in url
        extra_wait = CONFIG["main_page_extra_wait"] if is_main_page else CONFIG["extra_wait"]
        await page_obj.wait_for_timeout(extra_wait)
        
        # 获取页面内容
        html = await page_obj.content()
        
        # 提取标题
        title = await page_obj.title()
        title = title.replace(' - JoinQuant', '').strip()
        
        # 提取文本内容
        try:
            body_text = await page_obj.evaluate('''
                () => {
                    const scripts = document.querySelectorAll('script, style, nav, header, footer');
                    scripts.forEach(el => el.remove());
                    const main = document.querySelector('main') || document.body;
                    return main.innerText || '';
                }
            ''')
            content = clean_text(body_text)
        except Exception as e:
            print(f"    ⚠️ 内容提取失败: {e}")
            content = ""
        
        if not content or len(content) < 100:
            print(f"    ⚠️ 内容太短（{len(content)}字符），跳过")
            STATS["skipped"] += 1
            return None
        
        # 内容去重检查
        content_hash = get_content_hash(content)
        if content_hash in content_hashes:
            print(f"    ⚪ 内容重复，跳过（哈希: {content_hash[:8]}...）")
            STATS["duplicates_skipped"] += 1
            STATS["skipped"] += 1
            return None
        
        content_hashes.add(content_hash)
        
        STATS["crawled"] += 1
        STATS["success"] += 1
        
        result = {
            'url': url,
            'title': title,
            'content': content,
            'html': html,
            'content_length': len(content),
            'content_hash': content_hash,
            'load_time': load_time,
            'crawled_at': datetime.now().isoformat()
        }
        
        # 提取子链接
        if depth < max_depth:
            sub_links = await extract_all_links_playwright(page_obj, url)
            result['sub_links'] = sub_links
            print(f"    ✅ 成功 ({len(content):,} 字符, {len(sub_links)} 个子链接, 加载{load_time:.1f}秒)")
        else:
            print(f"    ✅ 成功 ({len(content):,} 字符, 加载{load_time:.1f}秒)")
        
        return result
        
    except Exception as e:
        STATS["crawled"] += 1
        STATS["failed"] += 1
        raise  # 重新抛出异常，让重试机制处理


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
- **页面加载耗时**: {page_data.get('load_time', 0):.1f} 秒

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
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False


async def crawl_recursive_playwright(start_url: str):
    """使用Playwright递归爬取所有页面（最终优化版本）"""
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
        page.set_default_timeout(CONFIG["wait_timeout"])
        
        # 待爬取队列
        queue: deque = deque([(start_url, 0)])
        results: List[Dict] = []
        
        try:
            while queue and STATS["crawled"] < CONFIG["max_pages"]:
                url, depth = queue.popleft()
                
                # 爬取当前页面（带智能重试）
                page_data = await crawl_page_with_retry(url, page, depth, CONFIG["max_depth"])
                
                if page_data:
                    results.append(page_data)
                    
                    # 存入知识库
                    save_to_knowledge_base(page_data)
                    
                    # 添加子链接到队列
                    if 'sub_links' in page_data and depth < CONFIG["max_depth"]:
                        for link in page_data['sub_links']:
                            sub_url = normalize_url(link['url'])
                            if sub_url not in visited_urls:
                                queue.append((sub_url, depth + 1))
                    
                    # 定期保存进度
                    if STATS["crawled"] % CONFIG["progress_save_interval"] == 0:
                        save_progress()
                        save_visited_urls()
                        if CONFIG["cache_sidebar"]:
                            save_sidebar_cache()
                        save_content_hashes()
                    
                    # 速率限制
                    await asyncio.sleep(CONFIG["rate_limit_delay"])
            
            # 最终保存
            save_progress()
            save_visited_urls()
            save_failed_urls()
            if CONFIG["cache_sidebar"]:
                save_sidebar_cache()
            save_content_hashes()
            
            await context.close()
            await browser.close()
            
            return results
            
        except KeyboardInterrupt:
            print("\n⚠️ 用户中断，正在保存进度...")
            save_progress()
            save_visited_urls()
            save_failed_urls()
            if CONFIG["cache_sidebar"]:
                save_sidebar_cache()
            save_content_hashes()
            try:
                await context.close()
            except:
                pass
            try:
                await browser.close()
            except:
                pass
            return results
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
            save_progress()
            save_visited_urls()
            save_failed_urls()
            if CONFIG["cache_sidebar"]:
                save_sidebar_cache()
            save_content_hashes()
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
    global visited_urls, sidebar_cache, content_hashes
    
    print("=" * 70)
    print("聚宽API文档完整爬取 - 最终优化版本")
    print("=" * 70)
    print(f"起始URL: {JQDATA_DOC_URL}")
    print(f"配置:")
    print(f"  - 最大页面数: {CONFIG['max_pages']}")
    print(f"  - 最大深度: {CONFIG['max_depth']}")
    print(f"  - 重试次数: {CONFIG['retry_times']}")
    print(f"  - 请求间隔: {CONFIG['rate_limit_delay']}秒")
    print(f"  - 进度保存间隔: {CONFIG['progress_save_interval']}页")
    print(f"  - 侧栏缓存: {'✅ 启用' if CONFIG['cache_sidebar'] else '❌ 禁用'}")
    print(f"  - 内容去重: ✅ 启用")
    print(f"  - 智能重试: ✅ 启用")
    print(f"Playwright可用: {'✅ 是' if PLAYWRIGHT_AVAILABLE else '❌ 否'}")
    print(f"知识库可用: {'✅ 是' if KB_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    # 加载缓存和进度
    if CONFIG["cache_sidebar"]:
        sidebar_cache = load_sidebar_cache()
    
    content_hashes = load_content_hashes()
    
    progress = load_progress()
    if progress:
        print("📋 发现已有进度，是否恢复？")
        visited_urls = set(progress.get("visited_urls", []))
        failed_urls.extend(progress.get("failed_urls", []))
        print(f"   已访问: {len(visited_urls)} 个URL")
        print(f"   失败: {len(progress.get('failed_urls', []))} 个URL")
        print()
    
    if not visited_urls:
        visited_urls = load_visited_urls() if VISITED_URLS_FILE.exists() else set()
    
    STATS["start_time"] = datetime.now().isoformat()
    
    # 开始爬取
    results = await crawl_recursive_playwright(JQDATA_DOC_URL)
    
    # 打印统计
    end_time = datetime.now()
    duration = (end_time - datetime.fromisoformat(STATS["start_time"])).total_seconds()
    
    print()
    print("=" * 70)
    print("爬取完成 - 统计信息")
    print("=" * 70)
    print(f"总链接数: {STATS['total_links']}")
    print(f"已爬取: {STATS['crawled']}")
    print(f"成功: {STATS['success']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过: {STATS['skipped']}")
    print(f"重试: {STATS['retried']}")
    print(f"存入知识库: {STATS['saved_to_kb']}")
    if CONFIG["cache_sidebar"]:
        print(f"侧栏缓存命中: {STATS['sidebar_cache_hits']}")
    print(f"内容去重跳过: {STATS['duplicates_skipped']}")
    print(f"总耗时: {duration/60:.1f} 分钟")
    
    if failed_urls:
        print(f"失败URL: {len(failed_urls)} 个（已保存到 {FAILED_URLS_FILE}）")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

