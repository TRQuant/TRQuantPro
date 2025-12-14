"""
文件名: code_4_4_完整工作流示例.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.4/code_4_4_完整工作流示例.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: 完整工作流示例

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 1. 获取市场状态（使用trquant_market_status）
market_status = client.call_tool(
    "trquant_market_status",
    {"universe": "CN_EQ"}
)

# 2. 根据市场状态选择投资周期
if market_status["regime"] == "risk_on":
    time_horizon = "short"  # 风险偏好上升，选择短期主线
elif market_status["regime"] == "risk_off":
    time_horizon = "long"  # 风险偏好下降，选择长期主线
else:
    time_horizon = "medium"  # 震荡市场，选择中期主线

# 3. 获取投资主线
mainlines = client.call_tool(
    "trquant_mainlines",
    {
        "time_horizon": time_horizon,
        "top_n": 10
    }
)

# 4. 查询相关知识库
knowledge = client.call_tool(
    "kb.query",
    {
        "query": f"投资主线识别 {time_horizon} 策略",
        "collection": "both",
        "top_k": 5
    }
)

# 5. 收集外部资料（如需要）
if len(mainlines) < 5:
    external_data = client.call_tool(
        "data_collector.crawl_web",
        {
            "url": "https://example.com/mainline-analysis",
            "extract_text": True
        }
    )

# 6. 综合分析并生成投资建议
investment_advice = generate_advice(
    market_status=market_status,
    mainlines=mainlines,
    knowledge=knowledge
)