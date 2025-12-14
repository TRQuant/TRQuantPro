"""
文件名: code_10_11_Step.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_Step.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: Step

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/main_window.py
from gui.widgets.new_panel import NewPanel

# 在create_sidebar中添加导航按钮
button = SidebarButton("🆕", "新功能", self)
button.clicked.connect(lambda: self.switch_panel(12))

# 在延迟加载中注册
self._panel_classes[12] = NewPanel