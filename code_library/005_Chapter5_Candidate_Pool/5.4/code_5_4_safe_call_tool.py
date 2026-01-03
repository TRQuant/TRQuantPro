"""
文件名: code_5_4_safe_call_tool.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.4/code_5_4_safe_call_tool.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.4_MCP_Tool_Integration_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: safe_call_tool

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def safe_call_tool(tool_name: str, params: dict, max_retries: int = 3):
        """
    safe_call_tool函数
    
    **设计原理**：
    - **核心功能**：实现safe_call_tool的核心逻辑
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
    for attempt in range(max_retries):
        try:
            result = client.call_tool(tool_name, params)
            return result
        except Exception as e:
            logger.warning(f"工具调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                raise
            time.sleep(1)  # 等待1秒后重试