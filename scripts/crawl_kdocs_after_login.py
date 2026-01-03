#!/usr/bin/env python3
"""交互式爬取kdocs文档 - 等待用户登录后爬取"""
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://www.kdocs.cn/l/cgLJ9Kpu2M79')
        input('请在浏览器中完成登录，然后按Enter继续...')
        await page.wait_for_timeout(3000)
        html = await page.content()
        text = await page.inner_text('body')
        with open('/tmp/kdocs_content.html', 'w', encoding='utf-8') as f:
            f.write(html)
        with open('/tmp/kdocs_content.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        await browser.close()
        print('✅ 内容已保存')

if __name__ == "__main__":
    asyncio.run(main())
