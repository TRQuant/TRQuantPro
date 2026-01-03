"""
文件名: code_10_12_parse.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12_parse.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: parse

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# spiders/example_spider.py
import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['https://example.com']
    
    def parse(self, response):
        # 提取数据
        title = response.css('title::text').get()
        content = response.css('div.content::text').getall()
        
        yield {
            'url': response.url,
            'title': title,
            'content': ' '.join(content)
        }
        
        # 跟随链接
        for link in response.css('a::attr(href)').getall():
            yield response.follow(link, self.parse)