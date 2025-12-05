# -*- coding: utf-8 -*-
"""
用户使用指南对话框
启动时默认显示，带"下次不再显示"选项
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame
)
from PyQt6.QtCore import Qt, QSettings

from gui.styles.theme import Colors, ButtonStyles
from gui.widgets.user_guide_panel import UserGuidePanel


class UserGuideDialog(QDialog):
    """用户使用指南对话框"""
    
    SETTINGS_KEY = "user_guide/dont_show_on_startup"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📖 韬睿量化平台使用指南")
        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)
        self.setModal(False)  # 非模态，不阻塞主窗口
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
            }}
        """)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 添加使用指南面板
        guide_panel = UserGuidePanel()
        layout.addWidget(guide_panel, 1)
        
        # 底部按钮栏
        footer = QFrame()
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_DARK};
                border-top: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(24, 16, 24, 16)
        
        # 不再显示复选框
        self.dont_show_checkbox = QCheckBox("启动时不再显示此指南")
        self.dont_show_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {Colors.TEXT_MUTED};
                font-size: 13px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                background-color: {Colors.BG_SECONDARY};
            }}
            QCheckBox::indicator:checked {{
                background-color: {Colors.PRIMARY};
                border-color: {Colors.PRIMARY};
            }}
        """)
        # 读取当前设置
        settings = QSettings("TaoRui", "JQQuant")
        self.dont_show_checkbox.setChecked(
            settings.value(self.SETTINGS_KEY, False, type=bool)
        )
        footer_layout.addWidget(self.dont_show_checkbox)
        
        footer_layout.addStretch()
        
        # 提示文字
        tip_label = QLabel("💡 可随时从工作台点击「查看使用指南」重新打开")
        tip_label.setStyleSheet(f"""
            color: {Colors.TEXT_MUTED};
            font-size: 12px;
        """)
        footer_layout.addWidget(tip_label)
        
        footer_layout.addSpacing(24)
        
        # 关闭按钮
        close_btn = QPushButton("开始使用")
        close_btn.setStyleSheet(ButtonStyles.PRIMARY)
        close_btn.setFixedSize(120, 40)
        close_btn.clicked.connect(self.on_close)
        footer_layout.addWidget(close_btn)
        
        layout.addWidget(footer)
    
    def on_close(self):
        """关闭按钮点击"""
        # 保存用户偏好
        settings = QSettings("TaoRui", "JQQuant")
        settings.setValue(self.SETTINGS_KEY, self.dont_show_checkbox.isChecked())
        self.close()
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 保存用户偏好
        settings = QSettings("TaoRui", "JQQuant")
        settings.setValue(self.SETTINGS_KEY, self.dont_show_checkbox.isChecked())
        event.accept()
    
    @classmethod
    def should_show_on_startup(cls) -> bool:
        """是否应该在启动时显示"""
        settings = QSettings("TaoRui", "JQQuant")
        return not settings.value(cls.SETTINGS_KEY, False, type=bool)
    
    @classmethod
    def reset_preference(cls):
        """重置显示偏好（用于调试）"""
        settings = QSettings("TaoRui", "JQQuant")
        settings.remove(cls.SETTINGS_KEY)





