"""
文件名: code_2_4_00.py
保存路径: code_library/002_Chapter2_Data_Source/2.4/code_2_4_00.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 20:37:33
函数/类名: None

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 在Cursor中，AI会自动调用MCP工具
# 用户请求：
"请爬取JQData的API文档，保存到data/collected/jqdata_docs目录"

# AI执行：
data_collector.crawl_web(
    url="https://www.joinquant.com/help/api/help",
    max_depth=2,  # 爬取2层深度
    output_dir="data/collected/jqdata_docs",
    include_patterns=["*.html", "*.md"],  # 只保存HTML和Markdown文件
    exclude_patterns=["*.js", "*.css"]  # 排除JS和CSS文件
)