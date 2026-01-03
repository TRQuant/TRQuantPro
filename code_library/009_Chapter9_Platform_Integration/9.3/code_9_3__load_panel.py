"""
文件名: code_9_3__load_panel.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.3/code_9_3__load_panel.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.3_Desktop_System_Architecture_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: _load_panel

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/main_window.py (延迟加载部分)
class MainWindow(QMainWindow):
    """主窗口 - 延迟加载优化"""
    
    def _load_panel(self, index: int):
            """
    _load_panel函数
    
    **设计原理**：
    - **核心功能**：实现_load_panel的核心逻辑
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
        if self._panels_loaded[index]:
            return
        
        panel_map = {
            1: ("gui.widgets.data_source_panel", "DataSourcePanel"),
            2: ("gui.widgets.market_analysis_panel", "MarketAnalysisPanel"),
            3: ("gui.widgets.mainline_panel", "MainlinePanel"),
            4: ("gui.widgets.candidate_pool_panel", "CandidatePoolPanel"),
            5: ("gui.widgets.factor_library_panel", "FactorLibraryPanel"),
            6: ("gui.widgets.strategy_panel", "StrategyPanel"),
            7: ("gui.widgets.backtest_panel", "BacktestPanel"),
            8: ("gui.widgets.trading_panel", "TradingPanel"),
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
                self._panel_classes[index] = panel_class
                
                logger.info(f"面板 {index} 加载完成")
                
            except Exception as e:
                logger.error(f"加载面板 {index} 失败: {e}")
                # 显示错误提示
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.warning(
                    self,
                    "加载失败",
                    f"加载面板失败: {e}\n\n请检查模块是否正确安装。"
                )