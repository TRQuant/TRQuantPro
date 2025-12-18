"""
文件名: code_10_11_status_indicator.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_status_indicator.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: 状态指示器

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from gui.main_window import StatusIndicator

indicator = StatusIndicator()
indicator.set_status("online")  # online, offline, warning, error