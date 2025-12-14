"""
文件名: code_2_1_10.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_10.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:28
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 爬取数据源文档网站
data_collector.crawl_web(
    url="https://www.joinquant.com/help/api/help",
    max_depth=2,
    output_dir="data/collected/jqdata_docs"
)

# 2. 下载数据源使用手册
data_collector.download_pdf(
    url="https://example.com/jqdata_manual.pdf",
    output_dir="data/collected/manuals"
)

# 3. 收集学术论文
data_collector.collect_academic(
    database="arxiv",
    query="financial data source quality assessment",
    max_results=10,
    output_dir="data/collected/papers"
)