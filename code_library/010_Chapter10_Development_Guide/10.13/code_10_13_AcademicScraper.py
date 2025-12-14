"""
文件名: code_10_13_AcademicScraper.py
保存路径: code_library/010_Chapter10_Development_Guide/10.13/code_10_13_AcademicScraper.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.13_Web_Crawler_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: AcademicScraper

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from extension.python.tools.data_collector import AcademicScraper
from pathlib import Path

scraper = AcademicScraper(output_dir=Path("data/papers"))

# 从arXiv下载论文
files = scraper.collect(
    database="arxiv",
    query="quantitative+trading",
    max_results=50
)