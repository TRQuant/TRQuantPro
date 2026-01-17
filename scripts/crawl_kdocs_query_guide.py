#!/usr/bin/env python3
"""
使用Playwright爬取kdocs文档 - JQData Query使用方式
"""
import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def crawl_kdocs_page(url: str):
    """使用Playwright爬取kdocs页面"""
    print(f"正在爬取: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = await context.new_page()
        
        try:
            print("📡 正在加载页面...")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(5000)  # 等待内容加载
            
            title = await page.title()
            print(f"📄 页面标题: {title}")
            
            html_content = await page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text(separator='\n', strip=True)
            
            # 查找图片
            images = []
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://www.kdocs.cn' + src
                    images.append({'src': src, 'alt': img.get('alt', '')})
            
            # 截图
            screenshot_path = '/tmp/kdocs_query_guide_screenshot.png'
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 已保存截图: {screenshot_path}")
            
            await browser.close()
            return {
                'title': title,
                'html': html_content,
                'text': text_content,
                'images': images,
                'screenshot': screenshot_path
            }
        except Exception as e:
            print(f"❌ 爬取失败: {e}")
            import traceback
            traceback.print_exc()
            await browser.close()
            return None

def format_content_for_document(data: dict) -> str:
    """格式化内容为Markdown"""
    if not data:
        return "# 爬取失败\n\n无法获取页面内容。"
    
    md = f"""# JQData Query 使用方式指南

> **来源**: https://www.kdocs.cn/l/cgLJ9Kpu2M79  
> **页面标题**: {data.get('title', '未知')}

---

## 📋 文档内容

{data.get('text', '无内容')[:10000]}

---

## 🖼️ 图片资源

"""
    for i, img in enumerate(data.get('images', []), 1):
        md += f"![图片{i}]({img['src']})\n\n"
    
    if data.get('screenshot'):
        md += f"## 📸 页面截图\n\n![截图]({data['screenshot']})\n\n"
    
    return md

async def main():
    url = "https://www.kdocs.cn/l/cgLJ9Kpu2M79"
    print("=" * 70)
    print("JQData Query 使用方式文档爬取")
    print("=" * 70)
    
    data = await crawl_kdocs_page(url)
    
    if data:
        md_content = format_content_for_document(data)
        output_path = "/home/taotao/dev/QuantTest/TRQuant/docs/JQDATA_QUERY_USAGE_GUIDE.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n✅ 文档已保存: {output_path}")
        print(f"📸 截图: {data.get('screenshot')}")
        print(f"🖼️ 图片: {len(data.get('images', []))}个")
    else:
        print("❌ 爬取失败")

if __name__ == "__main__":
    asyncio.run(main())
