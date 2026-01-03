"""
文件名: code_7_7_generate.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.7/code_7_7_generate.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.7_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: generate

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 查询开发手册（Manual KB）
manual_results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "策略模板 模板定义 模板管理",
        "collection": "manual",
        "top_k": 3
    }
)

# 2. 查询工程代码（Engineering KB）
engineering_results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "StrategyGenerator class generate method",
        "collection": "engineering",
        "top_k": 3
    }
)

# 3. 组合查询（同时查询两个知识库）
both_results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "策略生成 Python代码生成",
        "collection": "both",
        "top_k": 10
    }
)