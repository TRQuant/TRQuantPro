"""
文件名: code_2_4_07.py
保存路径: code_library/002_Chapter2_Data_Source/2.4/code_2_4_07.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 20:36:52
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

data_collector.collect_social_media(
    platform="weibo",  # 或 "twitter", "zhihu"
    keywords=["JQData", "量化数据"],
    max_results=50,
    output_dir="data/collected/social"
)