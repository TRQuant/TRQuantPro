"""
文件名: code_4_4_市场分析.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_市场分析.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 市场分析

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 获取市场状态
market_status = client.call_tool("trquant_market_status", {"universe": "CN_EQ"})

# 根据市场状态选择投资周期
if market_status["regime"] == "risk_on":
    time_horizon = "short"  # 短期主线
elif market_status["regime"] == "risk_off":
    time_horizon = "long"  # 长期主线
else:
    time_horizon = "medium"  # 中期主线

# 获取投资主线
mainlines = client.call_tool(
    "trquant_mainlines",
    {"time_horizon": time_horizon, "top_n": 10}
)