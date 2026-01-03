"""
文件名: code_10_9_使用示例.py
保存路径: code_library/010_Chapter10_Development_Guide/10.9/code_10_9_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# ❌ 错误方式：直接读取文件
with open("docs/strategy_guide.md", "r") as f:
    content = f.read()

# ✅ 正确方式：使用MCP工具
result = docs_server.query(query="策略开发流程")
content = result["content"]