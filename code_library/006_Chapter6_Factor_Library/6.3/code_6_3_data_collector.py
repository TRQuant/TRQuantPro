"""
文件名: code_6_3_data_collector.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3_data_collector.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: data_collector

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 爬取因子优化相关网页
content = mcp_client.call_tool(
    "data_collector.crawl_web",
    {
        "url": "https://example.com/factor-optimization",
        "extract_text": True
    }
)