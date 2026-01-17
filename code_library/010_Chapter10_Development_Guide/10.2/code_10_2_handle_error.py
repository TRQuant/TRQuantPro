"""
文件名: code_10_2_handle_error.py
保存路径: code_library/010_Chapter10_Development_Guide/10.2/code_10_2_handle_error.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.2_Development_Principles_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: handle_error

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# core/utils/error_handler.py
class TRQuantError(Exception):
    """TRQuant基础异常"""
    pass

class DataSourceError(TRQuantError):
    """数据源错误"""
    pass

class StrategyError(TRQuantError):
    """策略错误"""
    pass

def handle_error(func):
        """
    handle_error函数
    
    **设计原理**：
    - **核心功能**：实现handle_error的核心逻辑
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
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TRQuantError as e:
            logger.error(f"TRQuant错误: {e}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {e}", exc_info=True)
            raise TRQuantError(f"未知错误: {e}") from e
    return wrapper