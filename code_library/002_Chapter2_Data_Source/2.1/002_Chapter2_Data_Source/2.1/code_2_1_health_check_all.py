"""
文件名: code_2_1_health_check_all.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1_health_check_all.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:30:08
函数/类名: health_check_all

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

def health_check_all(self, interval: int = 300):
        """
    health_check_all函数
    
    **设计原理**：
    - **核心功能**：实现health_check_all的核心逻辑
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
    import threading
    
    def check_loop():
        while True:
            for name, source in self.sources.items():
                health = source.health_check()
                # 记录健康状态到数据库
                self._record_health_status(name, health)
            time.sleep(interval)
    
    thread = threading.Thread(target=check_loop, daemon=True)
    thread.start()