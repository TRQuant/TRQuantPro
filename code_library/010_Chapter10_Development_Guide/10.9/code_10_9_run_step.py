"""
文件名: code_10_9_run_step.py
保存路径: code_library/010_Chapter10_Development_Guide/10.9/code_10_9_run_step.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.9_MCP_Cursor_Workflow_CN.md
提取时间: 2025-12-13 21:16:53
函数/类名: run_step

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def run_step(self, step_func, step_name: str) -> WorkflowResult:
        """
    run_step函数
    
    **设计原理**：
    - **核心功能**：实现run_step的核心逻辑
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
    try:
        result = step_func()
        return WorkflowResult(
            step_name=step_name,
            success=True,
            summary=f"{step_name}完成",
            details=result
        )
    except Exception as e:
        logger.error(f"{step_name}失败: {e}", exc_info=True)
        return WorkflowResult(
            step_name=step_name,
            success=False,
            summary=f"{step_name}失败",
            error=str(e)
        )