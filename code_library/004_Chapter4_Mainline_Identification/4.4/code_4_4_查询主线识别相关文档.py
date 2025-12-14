"""
文件名: code_4_4_查询主线识别相关文档.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_查询主线识别相关文档.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 查询主线识别相关文档

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 查询主线识别相关的开发文档
results = client.call_tool(
    "kb.query",
    {
        "query": "投资主线识别 多维度评分 主线筛选算法",
        "collection": "manual_kb",
        "top_k": 5
    }
)

# 处理结果
for result in results:
    print(f"文档: {result['title']}")
    print(f"文件路径: {result['file_path']}")
    print(f"相关性: {result['score']:.2f}")
    print(f"内容片段: {result['snippet']}")
    print("-" * 60)