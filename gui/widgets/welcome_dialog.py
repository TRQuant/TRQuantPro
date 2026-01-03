# -*- coding: utf-8 -*-
"""
欢迎弹窗
启动时显示，带关闭按钮和"下次不再显示"选项
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QFrame, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer
from pathlib import Path

from gui.styles.theme import Colors, ButtonStyles


class WelcomeDialog(QDialog):
    """欢迎弹窗"""
    
    SETTINGS_KEY = "welcome/dont_show_again"
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("欢迎使用韬睿量化")
        self.setFixedSize(700, 600)
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint
        )
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
        
        # === 顶部Logo区域 ===
        header = QFrame()
        header.setFixedHeight(140)
        header.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {Colors.PRIMARY}33, stop:1 {Colors.ACCENT}22);
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.setSpacing(16)
        
        # 加载SVG logo
        logo_label = QLabel()
        logo_path = Path(__file__).parent.parent / "resources" / "logo.svg"
        if logo_path.exists():
            pixmap = QPixmap(48, 48)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer = QSvgRenderer(str(logo_path))
            renderer.render(painter)
            painter.end()
            logo_label.setPixmap(pixmap)
        
        logo_layout.addWidget(logo_label)
        
        # 标题
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)
        
        title = QLabel("韬睿量化专业版")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("Taorui Quant Professional v2.0")
        subtitle.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.PRIMARY};
            letter-spacing: 1px;
        """)
        title_layout.addWidget(subtitle)
        
        logo_layout.addWidget(title_widget)
        header_layout.addLayout(logo_layout)
        
        layout.addWidget(header)
        
        # === 内容区域 ===
        content = QScrollArea()
        content.setWidgetResizable(True)
        content.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(20)
        
        # 欢迎信息
        welcome_text = QLabel("""
<h3 style="color: #cdd6f4; margin-bottom: 12px;">欢迎使用韬睿量化投研平台</h3>
<p style="color: #a6adc8; line-height: 1.8;">
韬睿量化是面向专业投资者的机构级量化研究与交易平台，专注于A股市场，
提供从策略开发、回测验证到实盘交易的完整解决方案。
</p>
        """)
        welcome_text.setTextFormat(Qt.TextFormat.RichText)
        welcome_text.setWordWrap(True)
        content_layout.addWidget(welcome_text)
        
        # 核心功能
        features_title = QLabel("核心功能")
        features_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 8px;
        """)
        content_layout.addWidget(features_title)
        
        features = [
            ("🔬 投研分析", "多因子量化分析，市场洞察，智能选股推荐"),
            ("💻 策略开发", "AI辅助代码生成，支持PTrade/QMT策略格式"),
            ("📊 回测验证", "专业回测引擎，风控检查，绩效分析"),
            ("🚀 实盘交易", "券商API直连，支持国金PTrade和QMT"),
        ]
        
        for icon_title, desc in features:
            feature = self._create_feature_item(icon_title, desc)
            content_layout.addWidget(feature)
        
        # 快速开始
        quickstart_title = QLabel("快速开始")
        quickstart_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 12px;
        """)
        content_layout.addWidget(quickstart_title)
        
        quickstart_text = QLabel(f"""
<ol style="color: #a6adc8; line-height: 2; margin-left: -20px;">
<li>进入<b style="color: {Colors.PRIMARY};">系统设置</b>，配置JQData账号连接数据源</li>
<li>在<b style="color: {Colors.PRIMARY};">策略开发</b>中编写或使用AI生成策略代码</li>
<li>使用<b style="color: {Colors.PRIMARY};">回测验证</b>测试策略表现</li>
<li>配置券商账户，进行<b style="color: {Colors.PRIMARY};">实盘交易</b></li>
</ol>
        """)
        quickstart_text.setTextFormat(Qt.TextFormat.RichText)
        quickstart_text.setWordWrap(True)
        content_layout.addWidget(quickstart_text)
        
        content_layout.addStretch()
        content.setWidget(content_widget)
        layout.addWidget(content)
        
        # === 底部按钮区域 ===
        footer = QFrame()
        footer.setFixedHeight(72)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-top: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(24, 0, 24, 0)
        
        # 不再显示复选框
        self.dont_show_checkbox = QCheckBox("下次不再显示")
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
        footer_layout.addWidget(self.dont_show_checkbox)
        
        footer_layout.addStretch()
        
        # 关闭按钮
        close_btn = QPushButton("开始使用")
        close_btn.setStyleSheet(ButtonStyles.PRIMARY)
        close_btn.setFixedSize(120, 40)
        close_btn.clicked.connect(self.on_close)
        footer_layout.addWidget(close_btn)
        
        layout.addWidget(footer)
    
    def _create_feature_item(self, title: str, desc: str) -> QFrame:
        """创建功能项"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            min-width: 120px;
        """)
        layout.addWidget(title_label)
        
        desc_label = QLabel(desc)
        desc_label.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_TERTIARY};
        """)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        return frame
    
    def on_close(self):
        """关闭按钮点击"""
        if self.dont_show_checkbox.isChecked():
            settings = QSettings("TaoRui", "JQQuant")
            settings.setValue(self.SETTINGS_KEY, True)
        
        self.accept()
    
    @classmethod
    def should_show(cls) -> bool:
        """是否应该显示欢迎弹窗"""
        settings = QSettings("TaoRui", "JQQuant")
        return not settings.value(cls.SETTINGS_KEY, False, type=bool)
    
    @classmethod
    def reset_preference(cls):
        """重置显示偏好"""
        settings = QSettings("TaoRui", "JQQuant")
        settings.remove(cls.SETTINGS_KEY)
