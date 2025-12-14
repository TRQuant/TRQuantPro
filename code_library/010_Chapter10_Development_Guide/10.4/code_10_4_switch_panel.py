"""
文件名: code_10_4_switch_panel.py
保存路径: code_library/010_Chapter10_Development_Guide/10.4/code_10_4_switch_panel.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.4_Desktop_System_Development_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: switch_panel

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

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
    # 更新按钮状态
    for i, btn in enumerate(self.nav_buttons):
        btn.setChecked(i == index)
    
    # 延迟加载面板
    if not self._panels_loaded[index]:
        self._load_panel(index)
    
    # 切换到对应面板
    self.content_stack.setCurrentIndex(index)

def _load_panel(self, index: int):
    """延迟加载面板"""
    panel_map = {
        1: ("gui.widgets.data_source_panel", "DataSourcePanel"),
        2: ("gui.widgets.market_analysis_panel", "MarketAnalysisPanel"),
        3: ("gui.widgets.mainline_panel", "MainlinePanel"),
        # ... 其他面板
    }
    
    if index in panel_map:
        try:
            module_path, class_name = panel_map[index]
            module = __import__(module_path, fromlist=[class_name])
            panel_class = getattr(module, class_name)
            
            # 创建面板实例
            panel = panel_class()
            
            # 替换占位符
            old_widget = self.content_stack.widget(index)
            self.content_stack.removeWidget(old_widget)
            old_widget.deleteLater()  # 释放内存
            
            self.content_stack.insertWidget(index, panel)
            self._panels_loaded[index] = True
            
        except Exception as e:
            logger.error(f"加载面板 {index} 失败: {e}")