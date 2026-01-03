#!/usr/bin/env python3
"""分批爬取JQData文档，显示详细进度"""
import sys, json, asyncio, time
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
from datetime import datetime

sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

async def crawl_doc(url, idx, total, link_text):
    """爬取单个文档"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print(f"  [{idx:3d}/{total}] 正在爬取: {link_text[:50]}")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(2000)
            
            html = await page.content()
            text = await page.inner_text('body')
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else link_text
            main = soup.find('main') or soup.find('body')
            content = main.get_text() if main else text
            
            await browser.close()
            
            # 保存文件
            output_dir = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled')
            output_dir.mkdir(exist_ok=True)
            safe_name = re.sub(r'[^\w\-_\.]', '_', link_text or f"doc_{idx}")[:50]
            doc_file = output_dir / f"{idx:03d}_{safe_name}.txt"
            
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n")
                f.write(f"标题: {title_text}\n")
                f.write(f"爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                f.write(content)
            
            print(f"      ✅ 成功: {title_text[:50]} ({len(content):,} 字符)")
            return {
                'url': url,
                'title': title_text,
                'content': content,
                'status': 'success',
                'index': idx,
                'content_length': len(content)
            }
        except Exception as e:
            await browser.close()
            print(f"      ❌ 失败: {str(e)[:50]}")
            return {
                'url': url,
                'title': '失败',
                'content': '',
                'status': 'failed',
                'error': str(e),
                'index': idx
            }

async def batch_crawl(start_idx, batch_size):
    """分批爬取"""
    with open('/tmp/jqdata_doc_links.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    
    total = len(links)
    end_idx = min(start_idx + batch_size, total)
    batch = links[start_idx:end_idx]
    
    print("=" * 70)
    print(f"批次爬取: 第 {start_idx+1} - {end_idx} 个文档 (共 {total} 个)")
    print("=" * 70)
    print()
    
    results = []
    start_time = time.time()
    
    for i, link in enumerate(batch, start_idx+1):
        link_text = link.get('text', f'文档{i}')
        result = await crawl_doc(link['url'], i, total, link_text)
        results.append(result)
        
        # 显示进度
        elapsed = time.time() - start_time
        avg_time = elapsed / (i - start_idx)
        remaining = (end_idx - i) * avg_time
        progress = (i - start_idx) / len(batch) * 100
        
        print(f"      进度: {progress:.1f}% | 已用: {elapsed:.1f}s | 预计剩余: {remaining:.1f}s")
        print()
        
        if i < end_idx:
            time.sleep(1)  # 避免请求过快
    
    # 保存批次结果
    output_dir = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled')
    batch_file = output_dir / f'batch_{start_idx+1}_{end_idx}.json'
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 统计
    success = sum(1 for r in results if r['status'] == 'success')
    failed = len(results) - success
    total_chars = sum(r.get('content_length', 0) for r in results)
    
    print("=" * 70)
    print(f"批次完成: 成功 {success}/{len(batch)}, 失败 {failed}")
    print(f"总内容: {total_chars:,} 字符")
    print(f"结果保存: {batch_file}")
    print("=" * 70)
    print()
    
    return results

if __name__ == "__main__":
    import sys
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # 默认每次5个
    
    print(f"\n开始爬取: 从第 {start+1} 个开始，每次 {size} 个\n")
    asyncio.run(batch_crawl(start, size))
