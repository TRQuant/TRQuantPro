"""
文件名: code_4_4_knowledge_base_query.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_knowledge_base_query.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 知识库查询

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询相关知识
knowledge = client.call_tool(
    "kb.query",
    {"query": "投资主线识别 多维度评分", "collection": "both"}
)

# 如果知识库结果不足，收集外部资料
if len(knowledge) < 3:
    external_data = client.call_tool(
        "data_collector.crawl_web",
        {"url": "https://example.com/mainline-analysis"}
    )