"""
文件名: code_10_11_test_button_click.py
保存路径: code_library/010_Chapter10_Development_Guide/10.11/code_10_11_test_button_click.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.11_GUI_Development_Guide_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: test_button_click

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# 使用PyAutoGUI进行GUI测试
import pyautogui
import time

def test_button_click():
    # 启动应用
    # 等待界面加载
    time.sleep(2)
    
    # 查找并点击按钮
    button = pyautogui.locateOnScreen('button.png')
    if button:
        pyautogui.click(button)
        assert True