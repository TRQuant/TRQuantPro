#!/usr/bin/env python3
"""
重新抓取聚宽JQData API文档

使用Playwright访问已登录的浏览器会话
"""
import sys
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 输出目录
OUTPUT_DIR = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled_new')
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# JQData文档列表页
DOC_LIST_URL = "https://www.joinquant.com/help/api/doc?name=JQDatadoc"

async def extract_doc_links(page) -> List[Dict[str, str]]:
    """从文档列表页面提取所有文档链接"""
    print("🔍 正在提取文档链接...")
    
    # 等待页面加载
    await page.wait_for_load_state('networkidle')
    await page.wait_for_timeout(3000)
    
    # 获取页面HTML
    html = await page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    links = []
    
    # 查找所有文档链接 (通常在一个侧边栏或列表中)
    # 查找包含 /help/api/doc?name=JQDatadoc&id= 的链接
    all_links = soup.find_all('a', href=True)
    
    for link in all_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        
        # 匹配JQData文档链接
        if '/help/api/doc?name=JQDatadoc&id=' in href:
            # 提取ID
            match = re.search(r'id=(\d+)', href)
            if match:
                doc_id = match.group(1)
                full_url = f"https://www.joinquant.com{href}" if href.startswith('/') else href
                
                links.append({
                    'id': doc_id,
                    'text': text or f"文档{doc_id}",
                    'url': full_url
                })
    
    # 去重
    seen_ids = set()
    unique_links = []
    for link in links:
        if link['id'] not in seen_ids:
            seen_ids.add(link['id'])
            unique_links.append(link)
    
    print(f"✅ 找到 {len(unique_links)} 个文档链接")
    return unique_links

async def crawl_single_doc(page, url: str, doc_id: str, title: str, idx: int, total: int) -> Dict[str, Any]:
    """爬取单个文档"""
    try:
        print(f"\n[{idx:3d}/{total}] 📥 {title[:60]}")
        print(f"      URL: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(2000)
        
        # 获取页面内容
        html = await page.content()
        text = await page.inner_text('body')
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 提取标题
        title_elem = soup.find('title')
        page_title = title_elem.get_text(strip=True) if title_elem else title
        
        # 提取主要内容 (通常在 <main> 或特定的容器中)
        main = soup.find('main') or soup.find('article') or soup.find('body')
        content = main.get_text(separator='\n', strip=True) if main else text
        
        # 清理内容
        content = re.sub(r'\n{3,}', '\n\n', content)  # 多个换行合并
        
        print(f"      ✅ 成功: {len(content):,} 字符")
        
        return {
            'url': url,
            'id': doc_id,
            'title': page_title,
            'content': content,
            'status': 'success',
            'content_length': len(content),
            'crawl_time': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"      ❌ 失败: {str(e)[:100]}")
        return {
            'url': url,
            'id': doc_id,
            'title': title,
            'content': '',
            'status': 'failed',
            'error': str(e),
            'crawl_time': datetime.now().isoformat()
        }

async def save_doc_to_file(doc: Dict[str, Any], idx: int):
    """保存文档到文件"""
    if doc['status'] != 'success':
        return
    
    safe_name = re.sub(r'[^\w\-_\.]', '_', doc['title'] or f"doc_{doc['id']}")[:80]
    file_path = OUTPUT_DIR / f"{idx:03d}_{doc['id']}_{safe_name}.txt"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"URL: {doc['url']}\n")
        f.write(f"ID: {doc['id']}\n")
        f.write(f"标题: {doc['title']}\n")
        f.write(f"爬取时间: {doc['crawl_time']}\n")
        f.write("=" * 70 + "\n\n")
        f.write(doc['content'])

async def main():
    """主函数"""
    print("=" * 70)
    print("🚀 聚宽JQData API文档重新抓取")
    print("=" * 70)
    print()
    
    async with async_playwright() as p:
        # 启动浏览器（非无头模式，以便使用已登录会话）
        # 注意：如果需要在已登录的浏览器中运行，请先手动打开浏览器并登录
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        try:
            # 1. 访问文档列表页
            print(f"📂 访问文档列表页: {DOC_LIST_URL}")
            await page.goto(DOC_LIST_URL, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(3000)
            
            # 2. 提取所有文档链接
            doc_links = await extract_doc_links(page)
            
            if not doc_links:
                print("❌ 未找到文档链接，请检查页面结构或登录状态")
                print("💡 提示：如果页面需要登录，请先在浏览器中登录，然后重新运行脚本")
                return
            
            # 保存链接列表
            links_file = OUTPUT_DIR / 'doc_links.json'
            with open(links_file, 'w', encoding='utf-8') as f:
                json.dump(doc_links, f, ensure_ascii=False, indent=2)
            print(f"📄 链接列表已保存: {links_file}")
            
            # 3. 逐个爬取文档
            print(f"\n📥 开始爬取 {len(doc_links)} 个文档...")
            print("-" * 70)
            
            results = []
            start_time = time.time()
            
            for idx, link in enumerate(doc_links, 1):
                result = await crawl_single_doc(
                    page, 
                    link['url'], 
                    link['id'], 
                    link['text'],
                    idx, 
                    len(doc_links)
                )
                results.append(result)
                
                # 保存到文件
                await save_doc_to_file(result, idx)
                
                # 进度统计
                elapsed = time.time() - start_time
                avg_time = elapsed / idx
                remaining = (len(doc_links) - idx) * avg_time
                progress = idx / len(doc_links) * 100
                
                print(f"     进度: {progress:.1f}% | 已用: {elapsed:.0f}s | 预计剩余: {remaining:.0f}s")
                
                # 避免请求过快
                if idx < len(doc_links):
                    await asyncio.sleep(1)
            
            # 4. 保存结果
            results_file = OUTPUT_DIR / 'crawl_results.json'
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            # 5. 统计
            success = sum(1 for r in results if r['status'] == 'success')
            failed = len(results) - success
            total_chars = sum(r.get('content_length', 0) for r in results)
            
            print("\n" + "=" * 70)
            print("📊 爬取完成")
            print("=" * 70)
            print(f"总文档数: {len(doc_links)}")
            print(f"成功: {success}")
            print(f"失败: {failed}")
            print(f"总内容: {total_chars:,} 字符")
            print(f"结果文件: {results_file}")
            print(f"输出目录: {OUTPUT_DIR}")
            print("=" * 70)
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
