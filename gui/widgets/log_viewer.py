# -*- coding: utf-8 -*-
"""
日志查看器
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QComboBox, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class LogViewer(QWidget):
    """日志查看器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_log_file()
        
        # 定时刷新
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_log_file)
        self.refresh_timer.start(5000)  # 5秒刷新一次
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 标题和控制
        header = QHBoxLayout()
        
        title = QLabel("📋 系统日志")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #89b4fa;")
        header.addWidget(title)
        
        header.addStretch()
        
        # 筛选
        header.addWidget(QLabel("级别:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(["全部", "DEBUG", "INFO", "WARNING", "ERROR"])
        self.level_combo.currentTextChanged.connect(self.filter_logs)
        header.addWidget(self.level_combo)
        
        # 搜索
        header.addWidget(QLabel("搜索:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键词...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self.filter_logs)
        header.addWidget(self.search_input)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self.load_log_file)
        header.addWidget(refresh_btn)
        
        # 清空按钮
        clear_btn = QPushButton("🗑️ 清空显示")
        clear_btn.clicked.connect(self.clear_display)
        header.addWidget(clear_btn)
        
        layout.addLayout(header)
        
        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #11111b;
                border: 1px solid #313244;
                border-radius: 8px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                padding: 12px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # 状态栏
        status_layout = QHBoxLayout()
        
        self.line_count_label = QLabel("共 0 行")
        self.line_count_label.setStyleSheet("color: #a6adc8;")
        status_layout.addWidget(self.line_count_label)
        
        status_layout.addStretch()
        
        self.last_update_label = QLabel("最后更新: --")
        self.last_update_label.setStyleSheet("color: #a6adc8;")
        status_layout.addWidget(self.last_update_label)
        
        layout.addLayout(status_layout)
        
        self.all_logs = []
    
    def load_log_file(self):
        """加载日志文件"""
        try:
            log_file = Path(__file__).parent.parent.parent / "logs" / "jqquant.log"
            if log_file.exists():
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    self.all_logs = f.readlines()[-1000:]  # 最近1000行
                
                self.filter_logs()
                self.last_update_label.setText(f"最后更新: {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            logger.error(f"加载日志失败: {e}")
    
    def filter_logs(self):
        """筛选日志"""
        level = self.level_combo.currentText()
        keyword = self.search_input.text().lower()
        
        filtered = []
        for line in self.all_logs:
            # 级别筛选
            if level != "全部":
                if f" - {level} - " not in line:
                    continue
            
            # 关键词筛选
            if keyword and keyword not in line.lower():
                continue
            
            filtered.append(line)
        
        self.display_logs(filtered)
    
    def display_logs(self, logs: list):
        """显示日志"""
        self.log_text.clear()
        
        for line in logs:
            # 根据日志级别设置颜色
            if " - ERROR - " in line:
                color = "#f38ba8"
            elif " - WARNING - " in line:
                color = "#f9e2af"
            elif " - INFO - " in line:
                color = "#89b4fa"
            elif " - DEBUG - " in line:
                color = "#9ca3af"
            else:
                color = "#cdd6f4"
            
            self.log_text.append(f'<span style="color: {color};">{line.strip()}</span>')
        
        self.line_count_label.setText(f"共 {len(logs)} 行")
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_display(self):
        """清空显示"""
        self.log_text.clear()
        self.line_count_label.setText("共 0 行")
    
    def append_log(self, message: str, level: str = "INFO"):
        """追加日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - GUI - {level} - {message}"
        self.all_logs.append(log_line + "\n")
        self.filter_logs()

