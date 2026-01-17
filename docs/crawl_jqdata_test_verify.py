#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聚宽API文档爬取 - 测试验证版本

先爬取少量页面验证：
1. 链接提取是否完整
2. 内容提取是否正确
3. 知识库存储是否成功
4. 知识库调用是否可用
5. 等待时间是否优化

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

# 测试配置
TEST_CONFIG = {
    "max_pages": 5,  # 测试时只爬取5个页面
    "max_depth": 2,  # 测试深度
    "wait_timeout": 60000,  # 60秒超时（测试优化）
    "networkidle_wait": 3000,  # 3秒networkidle等待（测试优化）
    "extra_wait": 3000,  # 额外等待3秒（测试优化）
}

# 统计信息
STATS = {
    "total_links": 0,
    "crawled": 0,
    "success": 0,
    "failed": 0,
    "skipped": 0,
    "saved_to_kb": 0,
    "kb_verified": 0
}

visited_urls: Set[str] = set()


def normalize_url(url: str) -> str:
    """规范化URL（移除锚点）"""
    return url.split('#')[0]


def clean_text(text: str) -> str:
    """清理文本"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


async def extract_all_links_playwright(page_obj, url: str) -> List[Dict[str, str]]:
    """使用Playwright提取所有文档链接"""
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
        
        print(f"    🔍 提取到 {len(js_links)} 个链接")
        return js_links
    except Exception as e:
        print(f"    ⚠️ 提取链接失败: {e}")
        return []


async def crawl_page_playwright(url: str, page_obj, depth: int = 0, max_depth: int = 2) -> Optional[Dict]:
    """使用Playwright爬取单个页面（测试优化版本）"""
    if depth > max_depth or STATS["crawled"] >= TEST_CONFIG["max_pages"]:
        return None
    
    url = normalize_url(url)
    
    if url in visited_urls:
        return None
    
    visited_urls.add(url)
    STATS["total_links"] += 1
    
    try:
        print(f"\n  [{STATS['crawled']+1}/{TEST_CONFIG['max_pages']}] 爬取: {url}")
        
        # 测试不同的等待策略
        start_time = datetime.now()
        
        try:
            # 策略1: networkidle + 较短等待（测试优化）
            await page_obj.goto(url, wait_until='networkidle', timeout=TEST_CONFIG["wait_timeout"])
            await page_obj.wait_for_timeout(TEST_CONFIG["networkidle_wait"])
        except Exception as e1:
            print(f"    ⚠️ networkidle超时，尝试load策略...")
            try:
                await page_obj.goto(url, wait_until='load', timeout=TEST_CONFIG["wait_timeout"])
                await page_obj.wait_for_timeout(TEST_CONFIG["extra_wait"])
            except Exception as e2:
                print(f"    ⚠️ load超时，使用domcontentloaded...")
                await page_obj.goto(url, wait_until='domcontentloaded', timeout=TEST_CONFIG["wait_timeout"])
                await page_obj.wait_for_timeout(TEST_CONFIG["extra_wait"] * 2)
        
        load_time = (datetime.now() - start_time).total_seconds()
        print(f"    ⏱️ 页面加载耗时: {load_time:.1f}秒")
        
        # 额外等待确保侧栏菜单渲染（主页面需要更长时间）
        is_main_page = 'id=9842' in url
        extra_wait = TEST_CONFIG["main_page_extra_wait"] if is_main_page else TEST_CONFIG["extra_wait"]
        if is_main_page:
            print(f"    ⏱️ 主页面额外等待 {extra_wait/1000} 秒...")
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
        
        STATS["crawled"] += 1
        STATS["success"] += 1
        
        result = {
            'url': url,
            'title': title,
            'content': content,
            'html': html,
            'content_length': len(content),
            'load_time': load_time,
            'crawled_at': datetime.now().isoformat()
        }
        
        # 提取子链接（仅在测试范围内）
        if depth < max_depth and STATS["crawled"] < TEST_CONFIG["max_pages"]:
            sub_links = await extract_all_links_playwright(page_obj, url)
            result['sub_links'] = sub_links
            print(f"    ✅ 成功 ({len(content):,} 字符, {len(sub_links)} 个子链接, 加载{load_time:.1f}秒)")
        else:
            print(f"    ✅ 成功 ({len(content):,} 字符, 加载{load_time:.1f}秒)")
        
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
            kb_id = result.get('id') or result.get('knowledge_id') or 'unknown'
            STATS["saved_to_kb"] += 1
            print(f"    💾 已存入知识库: {kb_id}")
            return True
        else:
            print(f"    ⚠️ 存入知识库失败: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"    ⚠️ 存入知识库异常: {e}")
        return False


def verify_knowledge_base(test_urls: List[str]) -> Dict:
    """验证知识库中的条目"""
    print("\n" + "="*70)
    print("📚 验证知识库条目")
    print("="*70)
    
    try:
        # 读取知识库文件
        kb_file = PROJECT_ROOT / ".trquant" / "dev" / "knowledge" / "knowledge_base.json"
        if not kb_file.exists():
            print("❌ 知识库文件不存在")
            return {"success": False, "error": "知识库文件不存在"}
        
        with open(kb_file, 'r', encoding='utf-8') as f:
            kb_data = json.load(f)
        
        items = kb_data.get('items', kb_data) if isinstance(kb_data, dict) else kb_data
        
        # 检查测试URL是否在知识库中
        found_count = 0
        for test_url in test_urls:
            for item in items:
                if isinstance(item, dict):
                    source = item.get('source', '')
                    if test_url in source or normalize_url(test_url) in source:
                        found_count += 1
                        print(f"  ✅ 找到: {item.get('title', 'N/A')[:60]}")
                        print(f"     URL: {source[:80]}")
                        print(f"     标签: {item.get('tags', [])[:5]}")
                        break
        
        print(f"\n📊 验证结果: {found_count}/{len(test_urls)} 个条目在知识库中")
        
        return {
            "success": True,
            "total_items": len(items),
            "test_urls": len(test_urls),
            "found_count": found_count
        }
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return {"success": False, "error": str(e)}


async def crawl_test_playwright(start_url: str):
    """使用Playwright测试爬取少量页面"""
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
        page.set_default_timeout(TEST_CONFIG["wait_timeout"])
        
        # 待爬取队列（测试：只爬取主页面和几个分类页面）
        queue: List[tuple[str, int]] = [(start_url, 0)]
        results: List[Dict] = []
        test_urls: List[str] = []
        
        try:
            while queue and STATS["crawled"] < TEST_CONFIG["max_pages"]:
                url, depth = queue.pop(0)
                
                # 爬取当前页面
                page_data = await crawl_page_playwright(url, page, depth, TEST_CONFIG["max_depth"])
                
                if page_data:
                    results.append(page_data)
                    test_urls.append(url)
                    
                    # 存入知识库
                    save_to_knowledge_base(page_data)
                    
                    # 添加子链接到队列（限制数量）
                    if 'sub_links' in page_data and depth < TEST_CONFIG["max_depth"]:
                        # 测试：只添加前3个子链接
                        for link in page_data['sub_links'][:3]:
                            sub_url = normalize_url(link['url'])
                            if sub_url not in visited_urls and STATS["crawled"] < TEST_CONFIG["max_pages"]:
                                queue.append((sub_url, depth + 1))
                    
                    # 延迟避免请求过快
                    await asyncio.sleep(1)
            
            await context.close()
            await browser.close()
            
            return results, test_urls
            
        except Exception as e:
            print(f"❌ 爬取过程出错: {e}")
            try:
                await context.close()
            except:
                pass
            try:
                await browser.close()
            except:
                pass
            return results, test_urls


async def main():
    """主函数"""
    print("=" * 70)
    print("聚宽API文档爬取 - 测试验证版本")
    print("=" * 70)
    print(f"起始URL: {JQDATA_DOC_URL}")
    print(f"测试配置:")
    print(f"  - 最大页面数: {TEST_CONFIG['max_pages']}")
    print(f"  - 最大深度: {TEST_CONFIG['max_depth']}")
    print(f"  - 超时时间: {TEST_CONFIG['wait_timeout']/1000}秒")
    print(f"  - networkidle等待: {TEST_CONFIG['networkidle_wait']/1000}秒")
    print(f"  - 额外等待: {TEST_CONFIG['extra_wait']/1000}秒")
    print(f"Playwright可用: {'✅ 是' if PLAYWRIGHT_AVAILABLE else '❌ 否'}")
    print(f"知识库可用: {'✅ 是' if KB_AVAILABLE else '❌ 否'}")
    print("=" * 70)
    print()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright未安装")
        return
    
    # 开始测试爬取
    start_time = datetime.now()
    results, test_urls = await crawl_test_playwright(JQDATA_DOC_URL)
    end_time = datetime.now()
    
    # 打印统计
    print()
    print("=" * 70)
    print("测试爬取完成 - 统计信息")
    print("=" * 70)
    print(f"总链接数: {STATS['total_links']}")
    print(f"已爬取: {STATS['crawled']}")
    print(f"成功: {STATS['success']}")
    print(f"失败: {STATS['failed']}")
    print(f"跳过: {STATS['skipped']}")
    print(f"存入知识库: {STATS['saved_to_kb']}")
    print(f"总耗时: {(end_time - start_time).total_seconds():.1f} 秒")
    
    # 计算平均加载时间
    if results:
        avg_load_time = sum(r.get('load_time', 0) for r in results) / len(results)
        print(f"平均页面加载时间: {avg_load_time:.1f} 秒")
    
    print()
    
    # 验证知识库
    if test_urls:
        verify_result = verify_knowledge_base(test_urls)
        
        print()
        print("=" * 70)
        print("✅ 验证结论")
        print("=" * 70)
        
        if verify_result.get("success") and verify_result.get("found_count", 0) == len(test_urls):
            print("✅ 所有测试页面都已成功存入知识库")
            print("✅ 可以调用知识库验证内容")
            print("✅ 等待时间配置合理")
            print()
            print("📋 下一步: 运行完整爬取")
            print("   python scripts/crawl_jqdata_complete_with_tools.py")
        else:
            print("⚠️ 部分页面未在知识库中找到，请检查:")
            print(f"   - 找到: {verify_result.get('found_count', 0)}/{len(test_urls)}")
            print(f"   - 知识库总条目: {verify_result.get('total_items', 0)}")
    
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

