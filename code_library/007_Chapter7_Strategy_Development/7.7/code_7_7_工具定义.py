"""
文件名: code_7_7_工具定义.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.7/code_7_7_工具定义.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.7_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 工具定义

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

MCPTool(
    name="kb.query",
    description="查询知识库，支持Manual KB和Engineering KB",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "查询文本"
            },
            "collection": {
                "type": "string",
                "enum": ["manual", "engineering", "both"],
                "description": "查询的知识库类型",
                "default": "both"
            },
            "top_k": {
                "type": "integer",
                "description": "返回前K个结果",
                "default": 5
            }
        },
        "required": ["query"]
    }
)