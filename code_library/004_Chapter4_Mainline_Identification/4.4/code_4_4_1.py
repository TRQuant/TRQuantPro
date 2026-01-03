"""
文件名: code_4_4_1.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_1.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 1

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 获取高评分主线
mainlines = client.call_tool(
    "trquant_mainlines",
    {"time_horizon": "medium", "top_n": 10}
)

# 根据主线构建候选池
for mainline in mainlines:
    if mainline['score'] >= 80:
        # 高评分主线，用于候选池构建
        candidate_pool = build_candidate_pool(
            mainline=mainline,
            industries=mainline['industries'],
            key_stocks=mainline.get('key_stocks', [])
        )