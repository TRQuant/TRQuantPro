#!/usr/bin/env python3
import asyncio, json, time
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def crawl_page(url, page_obj):
    try:
        await page_obj.goto(url, wait_until='networkidle', timeout=60000)
        await page_obj.wait_for_timeout(2000)
        html = await page_obj.content()
        text = await page_obj.inner_text('body')
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "无标题"
        main = soup.find('main') or soup.find('body')
        content = main.get_text() if main else text
        return {'url': url, 'title': title_text, 'content': content, 'status': 'success', 'content_length': len(content)}
    except Exception as e:
        return {'url': url, 'title': '失败', 'content': '', 'status': 'failed', 'error': str(e)}

async def main():
    main_url = 'https://www.joinquant.com/help/api/doc?name=JQDatadoc&id=9842'
    print("=" * 70)
    print("抓取JQData API文档页面及其所有链接")
    print("=" * 70)
    print()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"📡 正在抓取主页面...")
        main_result = await crawl_page(main_url, page)
        
        if main_result['status'] != 'success':
            print("❌ 主页面抓取失败")
            await browser.close()
            return
        
        print(f"✅ 主页面: {main_result['title']} ({main_result['content_length']:,} 字符)")
        print()
        
        # 提取链接
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            link_text = link.get_text(strip=True)
            if href.startswith('/'):
                full_url = f"https://www.joinquant.com{href}"
            elif href.startswith('http'):
                full_url = href
            elif 'help/api/doc' in href or 'JQDatadoc' in href:
                full_url = f"https://www.joinquant.com/help/api/doc{href}"
            else:
                continue
            if 'help/api/doc' in full_url or 'JQDatadoc' in full_url:
                if full_url not in [l['url'] for l in links]:
                    links.append({'url': full_url, 'text': link_text, 'href': href})
        
        print(f"📚 找到 {len(links)} 个链接")
        print()
        
        # 抓取链接页面
        all_results = [main_result]
        print(f"开始抓取 {len(links)} 个链接页面...")
        print()
        
        for i, link in enumerate(links, 1):
            print(f"[{i:3d}/{len(links)}] {link['text'][:50]}")
            result = await crawl_page(link['url'], page)
            result['link_text'] = link['text']
            all_results.append(result)
            if result['status'] == 'success':
                print(f"      ✅ {result['title'][:50]} ({result['content_length']:,} 字符)")
            else:
                print(f"      ❌ {result.get('error', '')[:50]}")
            if i < len(links):
                time.sleep(1)
        
        await browser.close()
    
    # 保存结果
    output_dir = Path('/home/taotao/dev/QuantTest/TRQuant/docs/jqdata_crawled')
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'jqdata_9842_all_pages.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # 生成知识库格式
    kb_items = []
    for i, result in enumerate(all_results, 1):
        if result.get('status') != 'success':
            continue
        kb_content = f"""JQData API文档: {result['title']}

来源URL: {result['url']}
链接文本: {result.get('link_text', '')}

主要内容:
{result['content'][:5000]}

"""
        if len(result['content']) > 5000:
            kb_content += "\n(内容已截断，完整内容请查看原始文件)\n"
        kb_items.append({
            'title': f"JQData API: {result['title']}",
            'content': kb_content,
            'url': result['url'],
            'link_text': result.get('link_text', ''),
            'index': i
        })
    
    kb_file = output_dir / 'jqdata_9842_kb_items.json'
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(kb_items, f, ensure_ascii=False, indent=2)
    
    success_count = sum(1 for r in all_results if r.get('status') == 'success')
    print()
    print("=" * 70)
    print(f"✅ 完成: {success_count}/{len(all_results)} 成功")
    print(f"   结果: {output_file}")
    print(f"   知识库格式: {kb_file}")
    print(f"   准备存入: {len(kb_items)} 个条目")
    print("=" * 70)

asyncio.run(main())
