# -*- coding: utf-8 -*-
"""
韬睿量化专业版 - 启动画面
机构级专业设计
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QApplication, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QPen, QBrush

import sys
from pathlib import Path


class AnimatedProgressBar(QProgressBar):
    """动画进度条"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setFixedHeight(3)
        self.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a2e;
                border: none;
                border-radius: 1px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #667eea);
                border-radius: 1px;
            }
        """)


class SplashScreen(QWidget):
    """专业启动画面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(720, 520)
        
        self.init_ui()
        self.center_on_screen()
        
        # 加载动画
        self.current_step = 0
        self.loading_steps = [
            "正在初始化系统组件...",
            "正在加载数据中台...",
            "正在连接券商接口...",
            "正在初始化策略引擎...",
            "正在加载因子库...",
            "正在初始化风控系统...",
            "正在准备用户界面...",
            "正在完成最终配置...",
        ]
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 主容器
        container = QWidget()
        container.setObjectName("splashContainer")
        container.setStyleSheet("""
            #splashContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d0d14, stop:0.5 #12121f, stop:1 #0d0d14);
                border: 1px solid #2a2a4a;
                border-radius: 20px;
            }
        """)
        
        # 添加阴影
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 10)
        container.setGraphicsEffect(shadow)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(48, 48, 48, 40)
        container_layout.setSpacing(0)
        
        # === 顶部装饰 ===
        top_decor = QWidget()
        top_decor.setFixedHeight(4)
        top_decor.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 transparent, stop:0.2 #667eea, stop:0.8 #764ba2, stop:1 transparent);
            border-radius: 2px;
        """)
        container_layout.addWidget(top_decor)
        container_layout.addSpacing(40)
        
        # === Logo区域 ===
        logo_layout = QHBoxLayout()
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo图标
        logo_icon = QLabel()
        logo_icon.setFixedSize(72, 72)
        logo_icon.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 16px;
            font-size: 32px;
            font-weight: bold;
            color: white;
        """)
        logo_icon.setText("TR")
        logo_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_icon.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        
        logo_layout.addWidget(logo_icon)
        container_layout.addLayout(logo_layout)
        container_layout.addSpacing(24)
        
        # === 标题 ===
        title = QLabel("韬睿量化")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 4px;
        """)
        container_layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("TAORUI QUANT PROFESSIONAL")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 12px;
            font-weight: 500;
            color: #667eea;
            letter-spacing: 6px;
            margin-top: 8px;
        """)
        container_layout.addWidget(subtitle)
        container_layout.addSpacing(32)
        
        # === 核心优势 ===
        features_layout = QHBoxLayout()
        features_layout.setSpacing(24)
        
        features = [
            ("🏠", "本地部署", "数据安全"),
            ("🔗", "券商直连", "QMT/PTrade"),
            ("📊", "专业回测", "机构标准"),
            ("🤖", "AI助手", "智能策略"),
        ]
        
        for icon, title_text, desc in features:
            feature_widget = self._create_feature_item(icon, title_text, desc)
            features_layout.addWidget(feature_widget)
        
        container_layout.addLayout(features_layout)
        container_layout.addSpacing(32)
        
        # === 平台介绍 ===
        intro = QLabel(
            "韬睿量化是面向专业投资者的机构级量化研究与交易平台。\n"
            "支持本地化部署、券商API直连、专业因子分析、AI辅助策略开发。"
        )
        intro.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro.setWordWrap(True)
        intro.setStyleSheet("""
            font-size: 13px;
            color: #a6adc8;
            line-height: 1.6;
        """)
        container_layout.addWidget(intro)
        container_layout.addStretch()
        
        # === 进度区域 ===
        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.setSpacing(12)
        
        # 状态文字
        self.status_label = QLabel("准备启动...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #a6adc8;
        """)
        progress_layout.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        container_layout.addWidget(progress_container)
        container_layout.addSpacing(24)
        
        # === 底部版权 ===
        footer = QLabel("© 2024-2025 Taorui Technology · v2.0.0 Professional")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
            font-size: 11px;
            color: #45475a;
        """)
        container_layout.addWidget(footer)
        
        layout.addWidget(container)
    
    def _create_feature_item(self, icon: str, title: str, desc: str) -> QWidget:
        """创建特性项"""
        widget = QWidget()
        widget.setFixedWidth(130)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)
        
        # 标题
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 13px;
            font-weight: 600;
            color: #cdd6f4;
        """)
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel(desc)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("""
            font-size: 11px;
            color: #a6adc8;
        """)
        layout.addWidget(desc_label)
        
        return widget
    
    def center_on_screen(self):
        """居中显示在主屏幕"""
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            x = (screen_geometry.width() - self.width()) // 2 + screen_geometry.x()
            y = (screen_geometry.height() - self.height()) // 2 + screen_geometry.y()
            self.move(x, y)
    
    def start_loading(self):
        """开始加载动画"""
        self.timer.start(500)
    
    def update_progress(self):
        """更新进度"""
        if self.current_step < len(self.loading_steps):
            progress = int((self.current_step + 1) / len(self.loading_steps) * 100)
            self.progress_bar.setValue(progress)
            self.status_label.setText(self.loading_steps[self.current_step])
            self.current_step += 1
        else:
            self.timer.stop()
            self.status_label.setText("启动完成")
            self.progress_bar.setValue(100)
            # 延迟关闭
            QTimer.singleShot(800, self.close)
    
    def set_status(self, text: str, progress: int = None):
        """设置状态"""
        self.status_label.setText(text)
        if progress is not None:
            self.progress_bar.setValue(progress)
    
    def paintEvent(self, event):
        """绘制背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 绘制背景光晕
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(102, 126, 234, 20))
        gradient.setColorAt(0.5, QColor(118, 75, 162, 10))
        gradient.setColorAt(1, QColor(102, 126, 234, 20))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
