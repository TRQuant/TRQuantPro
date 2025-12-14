"""
文件名: code_6_2_kb.py
保存路径: code_library/006_Chapter6_Factor_Library/6.2/code_6_2_kb.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.2_Factor_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: kb

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询因子管理相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "因子管理 因子注册 因子版本管理 因子存储",
        "collection": "manual_kb",
        "top_k": 5
    }
)