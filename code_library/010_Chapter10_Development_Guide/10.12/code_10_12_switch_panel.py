"""
文件名: code_10_12_switch_panel.py
保存路径: code_library/010_Chapter10_Development_Guide/10.12/code_10_12_switch_panel.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.12_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: switch_panel

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 主窗口使用延迟加载，只加载当前显示的面板
def switch_panel(self, index: int):
        """
    switch_panel函数
    
    **设计原理**：
    - **核心功能**：实现switch_panel的核心逻辑
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
    if not self._panels_loaded[index]:
        self.load_panel(index)
    self.content_stack.setCurrentIndex(index)

def load_panel(self, index: int):
    """加载面板（延迟加载）"""
    if self._panels_loaded[index]:
        return
    
    panel_class = self._panel_classes.get(index)
    if panel_class:
        panel = panel_class(self)
        self.content_stack.insertWidget(index, panel)
        self._panels_loaded[index] = True