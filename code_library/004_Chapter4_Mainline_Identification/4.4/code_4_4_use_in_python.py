"""
文件名: code_4_4_use_in_python.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_use_in_python.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 在Python代码中使用

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from mcp import MCPClient

# 初始化MCP客户端
client = MCPClient(server_url="http://localhost:8000")

# 获取短期投资主线
short_mainlines = client.call_tool(
    "trquant_mainlines",
    {
        "time_horizon": "short",
        "top_n": 10
    }
)

# 获取中期投资主线
medium_mainlines = client.call_tool(
    "trquant_mainlines",
    {
        "time_horizon": "medium",
        "top_n": 20
    }
)

# 获取长期投资主线
long_mainlines = client.call_tool(
    "trquant_mainlines",
    {
        "time_horizon": "long",
        "top_n": 15
    }
)

# 处理结果
for mainline in short_mainlines:
    if mainline['score'] >= 80:
        print(f"高评分主线: {mainline['name']}")
        print(f"评分: {mainline['score']}")
        print(f"相关行业: {mainline['industries']}")
        print(f"投资逻辑: {mainline['logic']}")
        print(f"生命周期: {mainline['stage']}")
        print(f"主线类型: {mainline['type']}")
        print(f"推荐等级: {mainline['recommendation']}")
        print(f"建议仓位: {mainline['position_suggestion']}")
        print("-" * 60)