"""
文件名: code_2_2_16.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_16.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:37:33
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 收集学术论文
data_collector.collect_academic(
    database="arxiv",
    query="data quality assessment financial time series",
    max_results=10,
    output_dir="data/collected/papers/data_quality"
)

# 2. 爬取技术文档
data_collector.crawl_web(
    url="https://pandas.pydata.org/docs/user_guide/missing_data.html",
    max_depth=1,
    output_dir="data/collected/docs/pandas_missing_data"
)