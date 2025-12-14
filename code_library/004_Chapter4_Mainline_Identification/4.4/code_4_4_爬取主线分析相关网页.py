"""
文件名: code_4_4_爬取主线分析相关网页.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_爬取主线分析相关网页.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 爬取主线分析相关网页

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 爬取主线分析相关网页
result = client.call_tool(
    "data_collector.crawl_web",
    {
        "url": "https://example.com/mainline-analysis",
        "extract_text": True,
        "max_depth": 2,
        "output_dir": "data/collected/mainline_analysis"
    }
)

# 处理结果
print(f"爬取页面数: {result['pages_crawled']}")
print(f"提取文本长度: {result['text_length']}")
print(f"保存路径: {result['output_path']}")
print(f"文件列表: {result['files']}")