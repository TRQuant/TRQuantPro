"""
文件名: code_9_3___init__.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.3/code_9_3___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.3_Desktop_System_Architecture_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/widgets/base_panel.py (扩展)
from PyQt6.QtCore import QThread, pyqtSignal
from typing import Dict, Any, Optional

class DataFetchWorker(QThread):
    """数据获取工作线程"""
    data_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, fetch_func, *args, **kwargs):
        super().__init__()
        self.fetch_func = fetch_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
            result = self.fetch_func(*self.args, **self.kwargs)
            self.data_ready.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))

class BasePanel(QWidget):
    """功能面板基类（扩展）"""
    
    def fetch_data_async(
        self,
        fetch_func,
        callback,
        error_callback=None,
        *args,
        **kwargs
    ):
        """
        异步获取数据
        
        Args:
            fetch_func: 数据获取函数
            callback: 成功回调
            error_callback: 错误回调
            *args, **kwargs: 传递给fetch_func的参数
        """
        worker = DataFetchWorker(fetch_func, *args, **kwargs)
        worker.data_ready.connect(callback)
        if error_callback:
            worker.error_occurred.connect(error_callback)
        worker.start()
        return worker