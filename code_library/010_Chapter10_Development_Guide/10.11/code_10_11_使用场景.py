"""
文件名: code_10_11_使用场景.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_使用场景.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_Development_Methodology_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 使用场景

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 知识库检索示例
results = kb.query(
    query="如何开发MCP服务器？",
    scope="manual",
    top_k=5
)

# 使用结果
for result in results:
    print(f"文档: {result['metadata']['file_path']}")
    print(f"内容: {result['content'][:200]}...")