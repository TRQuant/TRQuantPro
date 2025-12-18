"""
文件名: code_10_7_tool_definition.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_tool_definition.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 工具定义

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# 定义MCP工具
MCP_TOOLS: List[MCPTool] = [
    MCPTool(
        name="trquant_market_status",
        description="获取A股市场当前状态，包括市场Regime（risk_on/risk_off/neutral）、指数趋势和风格轮动",
        input_schema={
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
    ),
    MCPTool(
        name="trquant_mainlines",
        description="获取当前A股市场的投资主线，包括主线名称、评分、相关行业和投资逻辑",
        input_schema={
            "type": "object",
            "properties": {
                "top_n": {
                    "type": "integer",
                    "description": "返回前N条主线，默认10",
                    "default": 10
                },
                "time_horizon": {
                    "type": "string",
                    "enum": ["short", "medium", "long"],
                    "description": "投资周期：short(1-5天)、medium(1-4周)、long(1月+)",
                    "default": "short"
                }
            },
            "required": []
        }
    ),
    MCPTool(
        name="trquant_generate_strategy",
        description="生成PTrade或QMT量化策略代码，支持多因子、动量成长、价值、市场中性四种风格",
        input_schema={
            "type": "object",
            "properties": {
                "platform": {
                    "type": "string",
                    "enum": ["ptrade", "qmt"],
                    "description": "目标平台",
                    "default": "ptrade"
                },
                "style": {
                    "type": "string",
                    "enum": ["multi_factor", "momentum_growth", "value", "market_neutral"],
                    "description": "策略风格",
                    "default": "multi_factor"
                },
                "factors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "使用的因子列表"
                },
                "max_position": {
                    "type": "number",
                    "description": "单票最大仓位(0-1)，默认0.1",
                    "default": 0.1
                }
            },
            "required": ["factors"]
        }
    )
]