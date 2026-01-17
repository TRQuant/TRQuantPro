"""
文件名: code_4_1_kb.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_kb.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: kb

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询主线评分相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "主线评分 多维度评分 因子评分方法",
        "collection": "manual_kb",
        "top_k": 5
    }
)