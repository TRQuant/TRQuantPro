"""
文件名: code_10_7_提示定义.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_提示定义.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: 提示定义

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 提示定义示例
prompts = [
    {
        "name": "analyze_market",
        "description": "分析市场状态并给出投资建议",
        "arguments": [
            {
                "name": "universe",
                "description": "市场范围",
                "required": False
            }
        ]
    },
    {
        "name": "generate_strategy",
        "description": "生成量化策略代码",
        "arguments": [
            {
                "name": "factors",
                "description": "使用的因子列表",
                "required": True
            },
            {
                "name": "platform",
                "description": "目标平台（ptrade/qmt）",
                "required": False
            }
        ]
    }
]