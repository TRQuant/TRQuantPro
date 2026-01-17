#!/usr/bin/env python3
"""按顺序爬取JQData所有API文档并存入知识库"""
import sys, os, json, asyncio, time
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

async def crawl_doc(url, idx, total):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            print(f"[{idx:3d}/{total}] {url}")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(2000)
            html = await page.content()
            text = await page.inner_text('body')
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "无标题"
            main = soup.find('main') or soup.find('body')
            content = main.get_text() if main else text
            await browser.close()
            return {'url': url, 'title': title_text, 'content': content, 'status': 'success'}
        except Exception as e:
            await browser.close()
            return {'url': url, 'title': '失败', 'content': '', 'status': 'failed', 'error': str(e)}

async def main():
    with open('/tmp/jqdata_doc_links.json', 'r', encoding='utf-8') as f:
        links = json.load(f)
    print(f"找到 {len(links)} 个文档，开始爬取...\n")
    results = []
    output_dir = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled')
    output_dir.mkdir(exist_ok=True)
    for i, link in enumerate(links, 1):
        result = await crawl_doc(link['url'], i, len(links))
        results.append(result)
        if result['status'] == 'success':
            safe_name = re.sub(r'[^\w\-_\.]', '_', link.get('text', f'doc_{i}'))
            with open(output_dir / f"{i:03d}_{safe_name}.txt", 'w', encoding='utf-8') as f:
                f.write(f"URL: {result['url']}\n标题: {result['title']}\n{'='*70}\n\n{result['content']}")
            print(f"  ✅ {result['title'][:50]}")
        else:
            print(f"  ❌ {result.get('error', '')}")
        if i < len(links):
            time.sleep(1)
    with open(output_dir / 'all_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    success = sum(1 for r in results if r['status'] == 'success')
    print(f"\n✅ 完成: {success}/{len(links)} 成功")
    return results

if __name__ == "__main__":
    asyncio.run(main())
