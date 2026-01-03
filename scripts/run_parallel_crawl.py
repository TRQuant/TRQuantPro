#!/usr/bin/env python3
"""并行爬取聚宽API文档 - 自动模式"""
import asyncio
import time
import json
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
CONCURRENT = 3
MAX_PAGES = 300  # 足够覆盖所有页面
START_URL = "https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9842"
OUTPUT_DIR = Path("docs/jqdata_crawled")
KB_FILE = Path(".trquant/dev/knowledge/knowledge_base.json")

async def fetch_page(browser, url, semaphore, results, visited):
    """并行爬取单个页面"""
    async with semaphore:
        page = await browser.new_page()
        start = time.time()
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
            
            title = await page.title()
            content = await page.content()
            
            # 提取文本内容
            text_content = await page.evaluate('''
                () => {
                    const main = document.querySelector('.doc-main, .content, main, article') || document.body;
                    return main.innerText;
                }
            ''')
            
            # 提取链接
            links = await page.evaluate('''
                () => {
                    const links = [];
                    document.querySelectorAll('a[href*="JQDatadoc"]').forEach(a => {
                        const href = a.href.split('#')[0];
                        const text = a.textContent.trim();
                        if (href && text && !links.some(l => l.url === href)) {
                            links.push({url: href, text: text.substring(0, 50)});
                        }
                    });
                    return links;
                }
            ''')
            
            elapsed = time.time() - start
            doc_id = url.split('id=')[-1] if 'id=' in url else 'N/A'
            print(f"  ✅ [{elapsed:.1f}s] {doc_id}: {title[:35]}... ({len(content)//1024}KB)")
            
            results['success'] += 1
            results['pages'].append({
                'url': url,
                'title': title,
                'content': text_content[:50000],  # 限制内容长度
                'size': len(content),
                'links': len(links),
                'time': elapsed
            })
            
            return [l['url'] for l in links if l['url'] not in visited]
            
        except Exception as e:
            elapsed = time.time() - start
            print(f"  ❌ [{elapsed:.1f}s] {url}: {str(e)[:50]}")
            results['failed'] += 1
            return []
        finally:
            await page.close()

def save_to_knowledge_base(pages):
    """保存到知识库"""
    if not KB_FILE.exists():
        kb = {"items": []}
    else:
        kb = json.loads(KB_FILE.read_text(encoding='utf-8'))
    
    existing_urls = {item.get('source_url') for item in kb.get('items', [])}
    added = 0
    
    for page in pages:
        if page['url'] in existing_urls:
            continue
        
        item = {
            "id": f"crawl_{hash(page['url']) % 1000000}",
            "title": page['title'].replace(' - JoinQuant', ''),
            "content": page['content'][:10000],
            "type": "reference",
            "tags": ["JQData", "API文档", "聚宽"],
            "source_url": page['url'],
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        kb['items'].append(item)
        added += 1
    
    KB_FILE.write_text(json.dumps(kb, indent=2, ensure_ascii=False), encoding='utf-8')
    return added

async def main():
    print("=" * 70)
    print(f"🚀 聚宽API文档并行爬取 (并发: {CONCURRENT})")
    print("=" * 70)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 加载已访问URL
    visited_file = OUTPUT_DIR / "visited_urls_parallel.json"
    if visited_file.exists():
        visited = set(json.loads(visited_file.read_text()))
        print(f"📋 加载已访问URL: {len(visited)}")
    else:
        visited = set()
    
    results = {'success': 0, 'failed': 0, 'pages': []}
    queue = [START_URL] if START_URL not in visited else []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        semaphore = asyncio.Semaphore(CONCURRENT)
        
        start_time = time.time()
        batch_num = 0
        
        while queue and len(visited) < MAX_PAGES:
            batch = []
            while queue and len(batch) < CONCURRENT and len(visited) + len(batch) < MAX_PAGES:
                url = queue.pop(0)
                if url not in visited:
                    batch.append(url)
                    visited.add(url)
            
            if not batch:
                break
            
            batch_num += 1
            print(f"\n📥 批次 {batch_num}: 爬取 {len(batch)} 页 (总进度: {len(visited)})...")
            
            tasks = [fetch_page(browser, url, semaphore, results, visited) for url in batch]
            all_links = await asyncio.gather(*tasks)
            
            for links in all_links:
                for link in links:
                    if link not in visited and link not in queue:
                        queue.append(link)
            
            # 保存进度
            if batch_num % 5 == 0:
                visited_file.write_text(json.dumps(list(visited), indent=2, ensure_ascii=False))
                print(f"   💾 进度已保存")
            
            await asyncio.sleep(1)
        
        await browser.close()
        total_time = time.time() - start_time
    
    # 保存最终进度
    visited_file.write_text(json.dumps(list(visited), indent=2, ensure_ascii=False))
    
    # 保存到知识库
    added = save_to_knowledge_base(results['pages'])
    
    print()
    print("=" * 70)
    print("📊 爬取完成")
    print("=" * 70)
    print(f"成功: {results['success']}")
    print(f"失败: {results['failed']}")
    print(f"存入知识库: {added}")
    print(f"总耗时: {total_time/60:.1f} 分钟")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
