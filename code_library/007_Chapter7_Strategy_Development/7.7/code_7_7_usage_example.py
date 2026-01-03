"""
文件名: code_7_7_使用示例.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.7/code_7_7_使用示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.7_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: 使用示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询策略开发相关的知识
results = mcp_client.call_tool(
    "kb.query",
    {
        "query": "策略生成 策略模板 Strategy KB",
        "collection": "both",
        "top_k": 5
    }
)

# 处理结果
for result in results['data']['results']:
    print(f"文档: {result['title']}")
    print(f"文件路径: {result['file_path']}")
    print(f"相关性: {result['score']:.2f}")
    print(f"内容片段: {result['snippet']}")
    print(f"章节: {result.get('section', '')}")
    print("---")