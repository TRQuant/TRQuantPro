"""
文件名: code_10_12_3.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12_3.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 3

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from python.tools.data_collector import WebCrawler
from pathlib import Path

# 创建爬虫
crawler = WebCrawler(
    output_dir=Path("data/collected"),
    delay_range=(1, 3),
    respect_robots=True
)

# 爬取网页
files = crawler.collect(
    url="https://example.com/docs",
    max_depth=2,
    allowed_domains=["example.com"]
)

print(f"✅ 共下载 {len(files)} 个文件")