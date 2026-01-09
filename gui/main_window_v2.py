# -*- coding: utf-8 -*-
"""
TRQuant主窗口 V2
================

集成策略管理、回测可视化、报告查看

特性:
- 侧边栏导航
- 多面板切换
- MCP调用集成
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame,
    QMessageBox, QStatusBar, QProgressBar, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from typing import Optional
import logging
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径（当直接运行此文件时）
if __name__ == "__main__":
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# 导入面板
from gui.widgets.strategy_manager_panel import StrategyManagerPanel
from gui.widgets.backtest_progress_panel import BacktestProgressPanel
from gui.widgets.backtest_result_panel import BacktestResultPanel
from gui.widgets.report_viewer_panel import ReportViewerPanel

logger = logging.getLogger(__name__)


class SidebarButton(QPushButton):
    """侧边栏按钮"""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                text-align: left;
                font-size: 13px;
                color: #888;
            }
            QPushButton:hover {
                background: #3d3d4d;
                color: #e0e0e0;
            }
            QPushButton:checked {
                background: linear-gradient(90deg, #00d9ff22, transparent);
                color: #00d9ff;
                border-left: 3px solid #00d9ff;
            }
        """)


class MainWindowV2(QMainWindow):
    """TRQuant主窗口 V2"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("TRQuant 韬睿量化系统 v2.0")
        self.setMinimumSize(1200, 800)
        
        # 设置深色主题
        self.setStyleSheet("""
            QMainWindow {
                background: #1a1a2e;
            }
            QWidget {
                color: #e0e0e0;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QGroupBox {
                border: 1px solid #404050;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTableWidget {
                background: #1e1e2e;
                border: 1px solid #404050;
                border-radius: 5px;
                gridline-color: #404050;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background: #00d9ff33;
            }
            QHeaderView::section {
                background: #2d2d3d;
                padding: 5px;
                border: none;
                border-bottom: 1px solid #404050;
            }
            QScrollBar:vertical {
                background: #2d2d3d;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #404050;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #505060;
            }
            QPushButton {
                background: #2d2d3d;
                border: 1px solid #404050;
                border-radius: 5px;
                padding: 8px 15px;
                color: #e0e0e0;
            }
            QPushButton:hover {
                background: #3d3d4d;
                border-color: #00d9ff;
            }
            QPushButton:pressed {
                background: #00d9ff33;
            }
            QLineEdit, QComboBox {
                background: #2d2d3d;
                border: 1px solid #404050;
                border-radius: 5px;
                padding: 8px;
                color: #e0e0e0;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #00d9ff;
            }
        """)
        
        self._init_ui()
        self._connect_signals()
        
        logger.info("TRQuant 主窗口V2已初始化")
    
    def _init_ui(self):
        """初始化UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === 左侧边栏 ===
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background: #16162a;
                border-right: 1px solid #404050;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(5)
        
        # Logo
        logo = QLabel("🚀 TRQuant")
        logo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #00d9ff;
            padding: 10px;
            margin-bottom: 20px;
        """)
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo)
        
        # 导航按钮
        self.nav_buttons = {}
        
        nav_items = [
            ("dashboard", "📊", "仪表盘"),
            ("strategy", "📋", "策略管理"),
            ("backtest", "▶️", "回测运行"),
            ("results", "📈", "结果分析"),
            ("reports", "📄", "报告中心"),
            ("settings", "⚙️", "系统设置"),
        ]
        
        for key, icon, text in nav_items:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(lambda checked, k=key: self._on_nav_clicked(k))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[key] = btn
        
        sidebar_layout.addStretch()
        
        # 版本信息
        version = QLabel("v2.0.0")
        version.setStyleSheet("color: #666; font-size: 11px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version)
        
        main_layout.addWidget(sidebar)
        
        # === 右侧内容区 ===
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 顶部栏
        topbar = QFrame()
        topbar.setFixedHeight(60)
        topbar.setStyleSheet("""
            QFrame {
                background: #1e1e2e;
                border-bottom: 1px solid #404050;
            }
        """)
        
        topbar_layout = QHBoxLayout(topbar)
        topbar_layout.setContentsMargins(20, 0, 20, 0)
        
        self.page_title = QLabel("仪表盘")
        self.page_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        topbar_layout.addWidget(self.page_title)
        
        topbar_layout.addStretch()
        
        # 状态指示
        self.status_label = QLabel("🟢 系统就绪")
        self.status_label.setStyleSheet("color: #00ff88;")
        topbar_layout.addWidget(self.status_label)
        
        content_layout.addWidget(topbar)
        
        # 页面堆栈
        self.page_stack = QStackedWidget()
        
        # 创建各页面
        self._create_dashboard_page()
        self._create_strategy_page()
        self._create_backtest_page()
        self._create_results_page()
        self._create_reports_page()
        self._create_settings_page()
        
        content_layout.addWidget(self.page_stack)
        
        main_layout.addWidget(content)
        
        # 状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background: #16162a; border-top: 1px solid #404050;")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(150)
        self.progress_bar.setVisible(False)
        self.statusBar.addPermanentWidget(self.progress_bar)
        
        # 默认选中仪表盘
        self.nav_buttons["dashboard"].setChecked(True)
    
    def _create_dashboard_page(self):
        """创建仪表盘页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 概览卡片
        cards_layout = QHBoxLayout()
        
        card_data = [
            ("策略数量", "12", "#00d9ff"),
            ("本月回测", "45", "#00ff88"),
            ("平均收益", "+18.5%", "#00ff88"),
            ("最新报告", "2份", "#ffaa00"),
        ]
        
        for title, value, color in card_data:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: #2d2d3d;
                    border-radius: 10px;
                    padding: 20px;
                }}
            """)
            cl = QVBoxLayout(card)
            
            v = QLabel(value)
            v.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(v)
            
            t = QLabel(title)
            t.setStyleSheet("color: #888; font-size: 12px;")
            t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(t)
            
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        
        # 快捷操作
        quick_group = QFrame()
        quick_group.setStyleSheet("""
            QFrame {
                background: #2d2d3d;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        ql = QVBoxLayout(quick_group)
        
        ql.addWidget(QLabel("⚡ 快捷操作"))
        
        btn_layout = QHBoxLayout()
        
        quick_btns = [
            ("📋 新建策略", self._quick_new_strategy),
            ("▶️ 快速回测", self._quick_backtest),
            ("📊 市场分析", self._quick_market),
            ("📄 生成报告", self._quick_report),
        ]
        
        for text, callback in quick_btns:
            btn = QPushButton(text)
            btn.setMinimumHeight(50)
            btn.clicked.connect(callback)
            btn_layout.addWidget(btn)
        
        ql.addLayout(btn_layout)
        
        layout.addWidget(quick_group)
        layout.addStretch()
        
        self.page_stack.addWidget(page)
    
    def _create_strategy_page(self):
        """创建策略管理页面"""
        self.strategy_panel = StrategyManagerPanel()
        self.page_stack.addWidget(self.strategy_panel)
    
    def _create_backtest_page(self):
        """创建回测页面"""
        self.backtest_panel = BacktestProgressPanel()
        self.page_stack.addWidget(self.backtest_panel)
    
    def _create_results_page(self):
        """创建结果分析页面"""
        self.results_panel = BacktestResultPanel()
        self.page_stack.addWidget(self.results_panel)
    
    def _create_reports_page(self):
        """创建报告中心页面"""
        self.reports_panel = ReportViewerPanel()
        self.page_stack.addWidget(self.reports_panel)
    
    def _create_settings_page(self):
        """创建设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        
        layout.addWidget(QLabel("⚙️ 系统设置 (开发中...)"))
        layout.addStretch()
        
        self.page_stack.addWidget(page)
    
    def _connect_signals(self):
        """连接信号"""
        # 策略面板 -> 回测面板
        self.strategy_panel.backtest_requested.connect(self._on_backtest_requested)
        
        # 回测面板 -> 结果面板
        self.backtest_panel.backtest_finished.connect(self._on_backtest_finished)
    
    def _on_nav_clicked(self, key: str):
        """导航点击"""
        # 更新按钮状态
        for k, btn in self.nav_buttons.items():
            btn.setChecked(k == key)
        
        # 切换页面
        page_map = {
            "dashboard": 0,
            "strategy": 1,
            "backtest": 2,
            "results": 3,
            "reports": 4,
            "settings": 5,
        }
        
        self.page_stack.setCurrentIndex(page_map.get(key, 0))
        
        # 更新标题
        titles = {
            "dashboard": "仪表盘",
            "strategy": "策略管理",
            "backtest": "回测运行",
            "results": "结果分析",
            "reports": "报告中心",
            "settings": "系统设置",
        }
        self.page_title.setText(titles.get(key, ""))
    
    def _on_backtest_requested(self, strategy_info: dict):
        """回测请求"""
        # 切换到回测页面
        self._on_nav_clicked("backtest")
        
        # 启动回测
        self.backtest_panel.start_backtest(
            strategy_path=strategy_info.get("path"),
            start_date="2024-01-01",
            end_date="2024-06-30"
        )
    
    def _on_backtest_finished(self, task_id: str, result: dict):
        """回测完成"""
        # 更新结果面板
        self.results_panel.load_result(result)
        
        # 提示用户
        QMessageBox.information(
            self, "回测完成",
            f"回测任务 {task_id} 已完成！\n"
            f"总收益: {result.get('total_return', 0)*100:.2f}%"
        )
    
    def _quick_new_strategy(self):
        """快速新建策略"""
        self._on_nav_clicked("strategy")
    
    def _quick_backtest(self):
        """快速回测"""
        self._on_nav_clicked("backtest")
    
    def _quick_market(self):
        """快速市场分析"""
        QMessageBox.information(self, "市场分析", "功能开发中...")
    
    def _quick_report(self):
        """快速生成报告"""
        self._on_nav_clicked("reports")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("TRQuant")
    app.setApplicationVersion("2.0.0")
    
    window = MainWindowV2()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
