"""
文件名: code_10_7_call_tool.py
保存路径: code_library/010_Chapter10_Development_Guide/10.7/code_10_7_call_tool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.7_MCP_Server_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: call_tool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

async def call_tool(self, name: str, arguments: dict) -> dict:
        """
    call_tool函数
    
    **设计原理**：
    - **核心功能**：实现call_tool的核心逻辑
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
    logger.info(f"调用工具: {name}")
    
    handlers = {
        "trquant_market_status": self._get_market_status,
        "trquant_mainlines": self._get_mainlines,
        "trquant_recommend_factors": self._recommend_factors,
        "trquant_generate_strategy": self._generate_strategy,
        "trquant_analyze_backtest": self._analyze_backtest
    }
    
    handler = handlers.get(name)
    if not handler:
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"未知工具: {name}"}]
        }
    
    try:
        # 参数验证
        if not self._validate_arguments(name, arguments):
            return {
                "isError": True,
                "content": [{"type": "text", "text": "参数验证失败"}]
            }
        
        result = await handler(arguments)
        return {
            "content": [{
                "type": "text",
                "text": json.dumps(result, ensure_ascii=False, indent=2)
            }]
        }
    except ValueError as e:
        logger.error(f"参数错误: {e}")
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"参数错误: {e}"}]
        }
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        return {
            "isError": True,
            "content": [{"type": "text", "text": f"执行失败: {e}"}]
        }