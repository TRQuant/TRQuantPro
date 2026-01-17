#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
轩辕剑灵开发助手 - 独立GUI应用
============================

独立的开发助手GUI，提供提示词管理、错误处理、命令助手、记忆功能

运行方式:
    python gui/xuanyuan_main_window.py
    或
    python -m gui.xuanyuan_main_window
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import logging

# 添加项目根目录到路径（当直接运行此文件时）
if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # 设置TRQUANT_ROOT环境变量（MCPClient需要）
    if 'TRQUANT_ROOT' not in os.environ:
        os.environ['TRQUANT_ROOT'] = str(project_root)

# 导入面板
from gui.widgets.xuanyuan_assistant_panel import XuanyuanAssistantPanel

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XuanyuanMainWindow(QMainWindow):
    """轩辕剑灵主窗口"""
    
    def __init__(self):
        super().__init__()
        self.workers = []  # 跟踪所有工作线程
        # 启用中文输入法支持（全局设置）
        self.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🐉 轩辕剑灵开发助手")
        self.setMinimumSize(1000, 700)
        
        # 启用窗口拖动（设置正确的窗口标志）
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint | 
                          Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinimizeButtonHint |
                          Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
    
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
        self.setStyleSheet("""
            QMainWindow {
                background: #1a1a2e;
            }
            QWidget {
                color: #e0e0e0;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #404050;
                border-radius: 5px;
                background: #1e1e2e;
            }
            QTabBar::tab {
                background: #2d2d3d;
                color: #888;
                padding: 10px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #1e1e2e;
                color: #00d9ff;
                border-bottom: 2px solid #00d9ff;
            }
            QTabBar::tab:hover {
                background: #3d3d4d;
            }
        """)
        
        # 创建主面板
        self.assistant_panel = XuanyuanAssistantPanel()
        self.setCentralWidget(self.assistant_panel)
    
    def closeEvent(self, event):
        """关闭事件"""
        logger.info("轩辕剑灵GUI关闭")
        
        # 停止所有工作线程
        if hasattr(self, 'assistant_panel') and hasattr(self.assistant_panel, 'workers'):
            for worker in list(self.assistant_panel.workers):  # 使用列表副本避免修改时迭代
                if worker.isRunning():
                    worker.quit()
                    worker.wait(1000)  # 等待最多1秒
        
        event.accept()


def main():
    """主函数"""
    # 设置中文输入法环境变量（在创建QApplication之前）
    import os
    if 'QT_IM_MODULE' not in os.environ:
        # 检测可用的输入法
        if os.path.exists('/usr/bin/fcitx') or os.path.exists('/usr/local/bin/fcitx'):
            os.environ['QT_IM_MODULE'] = 'fcitx'
        elif os.path.exists('/usr/bin/ibus-daemon') or os.path.exists('/usr/local/bin/ibus-daemon'):
            os.environ['QT_IM_MODULE'] = 'ibus'
    
    if 'XMODIFIERS' not in os.environ:
        os.environ['XMODIFIERS'] = '@im=fcitx'
    
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("轩辕剑灵")
    app.setApplicationVersion("1.0.0")
    
    # 创建主窗口
    window = XuanyuanMainWindow()
    # 窗口居中（在show()之后调用，因为需要窗口几何信息）
    window.show()
    window.center_window()
    
    logger.info("轩辕剑灵GUI启动成功")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

