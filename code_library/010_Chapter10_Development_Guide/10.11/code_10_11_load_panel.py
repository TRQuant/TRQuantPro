"""
文件名: code_10_11_load_panel.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_load_panel.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: load_panel

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 主窗口使用延迟加载，只加载当前显示的面板
self._panels_loaded = {i: False for i in range(10)}
self._panel_classes = {}

def load_panel(self, index):
    if not self._panels_loaded[index]:
        panel = self._panel_classes[index]()
        self.content_stack.insertWidget(index, panel)
        self._panels_loaded[index] = True