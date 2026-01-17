"""
文件名: code_10_7_tool.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_tool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 工具

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 工具定义示例
tool = {
    "name": "trquant_market_status",
    "description": "获取A股市场当前状态，包括市场Regime、指数趋势和风格轮动",
    "inputSchema": {
        "type": "object",
        "properties": {
            "universe": {
                "type": "string",
                "description": "市场，默认CN_EQ表示A股",
                "default": "CN_EQ"
            }
        },
        "required": []
    }
}