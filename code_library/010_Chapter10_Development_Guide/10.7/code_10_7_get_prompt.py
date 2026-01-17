"""
文件名: code_10_7_get_prompt.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_get_prompt.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: get_prompt

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

async def get_prompt(self, name: str, arguments: dict) -> dict:
        """
    get_prompt函数
    
    **设计原理**：
    - **核心功能**：实现get_prompt的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
    prompt_templates = {
        "analyze_market": """
        请分析当前A股市场状态，包括：
        1. 市场Regime（risk_on/risk_off/neutral）
        2. 指数趋势
        3. 风格轮动
        4. 投资建议
        
        市场范围：{universe}
        """,
        "generate_strategy": """
        请生成量化策略代码，要求：
        1. 使用因子：{factors}
        2. 目标平台：{platform}
        3. 策略风格：{style}
        4. 风险参数：max_position={max_position}, stop_loss={stop_loss}
        """
    }
    
    template = prompt_templates.get(name)
    if not template:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"未知提示: {name}"}]
        }
    
    # 渲染模板
    prompt = template.format(**arguments)
    
    return {
        "content": [{
            "type": "text",
            "text": prompt
        }]
    }