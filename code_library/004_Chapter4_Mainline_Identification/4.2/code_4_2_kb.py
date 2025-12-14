"""
文件名: code_4_2_kb.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2_kb.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: kb

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询主线筛选相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "主线筛选 评分筛选 行业筛选 时间筛选",
        "collection": "manual_kb",
        "top_k": 5
    }
)