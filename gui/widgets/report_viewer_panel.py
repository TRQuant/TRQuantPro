# -*- coding: utf-8 -*-
"""
报告查看面板
============

查看和管理回测报告

功能:
- HTML报告查看
- 报告对比
- 报告归档
- PDF导出
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QListWidget, QListWidgetItem, QSplitter,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QLineEdit, QComboBox, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIcon
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging
import os
import json

logger = logging.getLogger(__name__)


class ReportCard(QFrame):
    """报告卡片"""
    
    clicked = pyqtSignal(dict)
    
    def __init__(self, report_info: Dict, parent=None):
        super().__init__(parent)
        self.report_info = report_info
        self._init_ui()
    
    def _init_ui(self):
        self.setStyleSheet("""
            QFrame {
                background: #2d2d3d;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame:hover {
                background: #3d3d4d;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        title = QLabel(self.report_info.get("name", "未命名报告"))
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #00d9ff;")
        layout.addWidget(title)
        
        # 信息行
        info_layout = QHBoxLayout()
        
        date_label = QLabel(f"📅 {self.report_info.get('date', '--')}")
        date_label.setStyleSheet("color: #888; font-size: 11px;")
        info_layout.addWidget(date_label)
        
        strategy_label = QLabel(f"📊 {self.report_info.get('strategy', '--')}")
        strategy_label.setStyleSheet("color: #888; font-size: 11px;")
        info_layout.addWidget(strategy_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # 收益指标
        metrics_layout = QHBoxLayout()
        
        total_return = self.report_info.get("total_return", 0)
        return_color = "#00ff88" if total_return >= 0 else "#ff4444"
        return_label = QLabel(f"收益: {total_return*100:.2f}%")
        return_label.setStyleSheet(f"color: {return_color}; font-weight: bold;")
        metrics_layout.addWidget(return_label)
        
        sharpe = self.report_info.get("sharpe_ratio", 0)
        sharpe_label = QLabel(f"夏普: {sharpe:.2f}")
        sharpe_label.setStyleSheet("color: #e0e0e0;")
        metrics_layout.addWidget(sharpe_label)
        
        metrics_layout.addStretch()
        layout.addLayout(metrics_layout)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.report_info)
        super().mousePressEvent(event)


class ReportViewerPanel(QWidget):
    """报告查看面板"""
    
    report_selected = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._reports: List[Dict] = []
        self._current_report: Optional[Dict] = None
        
        self._init_ui()
        self._load_reports()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # === 顶部工具栏 ===
        toolbar = QHBoxLayout()
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索报告...")
        self.search_edit.textChanged.connect(self._filter_reports)
        toolbar.addWidget(self.search_edit)
        
        # 排序
        toolbar.addWidget(QLabel("排序:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["日期 ↓", "日期 ↑", "收益 ↓", "收益 ↑"])
        self.sort_combo.currentTextChanged.connect(self._sort_reports)
        toolbar.addWidget(self.sort_combo)
        
        toolbar.addStretch()
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.clicked.connect(self._load_reports)
        toolbar.addWidget(refresh_btn)
        
        layout.addLayout(toolbar)
        
        # === 主内容区 ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- 左侧：报告列表 ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.report_list = QListWidget()
        self.report_list.setSpacing(5)
        self.report_list.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
            }
            QListWidget::item {
                background: transparent;
                padding: 5px;
            }
        """)
        left_layout.addWidget(self.report_list)
        
        splitter.addWidget(left_panel)
        
        # --- 右侧：报告预览 ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 报告信息
        info_group = QGroupBox("报告信息")
        info_layout = QVBoxLayout(info_group)
        
        self.report_title = QLabel("请选择报告")
        self.report_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(self.report_title)
        
        self.report_info_labels = {}
        info_grid = QHBoxLayout()
        for key, title in [("date", "日期"), ("strategy", "策略"), ("engine", "引擎"), ("duration", "耗时")]:
            frame = QFrame()
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(10, 5, 10, 5)
            
            value_label = QLabel("--")
            value_label.setStyleSheet("font-weight: bold; color: #00d9ff;")
            fl.addWidget(value_label)
            
            name_label = QLabel(title)
            name_label.setStyleSheet("color: #888; font-size: 10px;")
            fl.addWidget(name_label)
            
            info_grid.addWidget(frame)
            self.report_info_labels[key] = value_label
        
        info_layout.addLayout(info_grid)
        right_layout.addWidget(info_group)
        
        # HTML预览（使用QWebEngineView）
        try:
            self.web_view = QWebEngineView()
            self.web_view.setStyleSheet("background: #1e1e2e;")
            right_layout.addWidget(self.web_view)
            self._has_web_view = True
        except Exception as e:
            logger.warning(f"QWebEngineView不可用: {e}")
            self._has_web_view = False
            
            # 退化为纯文本显示
            from PyQt6.QtWidgets import QTextEdit
            self.web_view = QTextEdit()
            self.web_view.setReadOnly(True)
            self.web_view.setStyleSheet("""
                QTextEdit {
                    background: #1e1e2e;
                    color: #e0e0e0;
                    border: 1px solid #404050;
                }
            """)
            right_layout.addWidget(self.web_view)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        open_btn = QPushButton("🌐 在浏览器中打开")
        open_btn.clicked.connect(self._open_in_browser)
        btn_layout.addWidget(open_btn)
        
        export_btn = QPushButton("📄 导出PDF")
        export_btn.clicked.connect(self._export_pdf)
        btn_layout.addWidget(export_btn)
        
        compare_btn = QPushButton("📊 对比分析")
        compare_btn.clicked.connect(self._compare_reports)
        btn_layout.addWidget(compare_btn)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.clicked.connect(self._delete_report)
        btn_layout.addWidget(delete_btn)
        
        right_layout.addLayout(btn_layout)
        
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setSizes([350, 650])
        
        layout.addWidget(splitter)
    
    def _load_reports(self):
        """加载报告列表"""
        self.report_list.clear()
        self._reports.clear()
        
        reports_dir = Path(__file__).parent.parent.parent / "reports"
        
        if not reports_dir.exists():
            reports_dir.mkdir(parents=True, exist_ok=True)
        
        # 扫描HTML报告
        for html_file in reports_dir.glob("**/*.html"):
            report_info = {
                "name": html_file.stem,
                "path": str(html_file),
                "date": datetime.fromtimestamp(html_file.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
                "strategy": self._extract_strategy_name(html_file.stem),
                "engine": "BulletTrade",
                "total_return": 0.0,
                "sharpe_ratio": 0.0
            }
            
            # 尝试读取元数据
            meta_file = html_file.with_suffix(".json")
            if meta_file.exists():
                try:
                    with open(meta_file, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                    report_info.update(meta)
                except:
                    pass
            
            self._reports.append(report_info)
        
        # 按日期排序
        self._reports.sort(key=lambda x: x.get("date", ""), reverse=True)
        
        # 添加到列表
        for report in self._reports:
            card = ReportCard(report)
            card.clicked.connect(self._on_report_selected)
            
            item = QListWidgetItem(self.report_list)
            item.setSizeHint(card.sizeHint())
            self.report_list.addItem(item)
            self.report_list.setItemWidget(item, card)
        
        logger.info(f"已加载 {len(self._reports)} 份报告")
    
    def _extract_strategy_name(self, filename: str) -> str:
        """从文件名提取策略名"""
        parts = filename.split("_")
        if len(parts) >= 2:
            return parts[0]
        return filename
    
    def _filter_reports(self):
        """筛选报告"""
        search_text = self.search_edit.text().lower()
        
        for i in range(self.report_list.count()):
            item = self.report_list.item(i)
            widget = self.report_list.itemWidget(item)
            if widget:
                report = widget.report_info
                visible = (search_text in report.get("name", "").lower() or
                          search_text in report.get("strategy", "").lower())
                item.setHidden(not visible)
    
    def _sort_reports(self):
        """排序报告"""
        sort_key = self.sort_combo.currentText()
        
        if "日期" in sort_key:
            key = "date"
        else:
            key = "total_return"
        
        reverse = "↓" in sort_key
        
        self._reports.sort(key=lambda x: x.get(key, 0), reverse=reverse)
        
        # 重新加载列表
        self._load_reports()
    
    def _on_report_selected(self, report_info: Dict):
        """报告选中"""
        self._current_report = report_info
        
        # 更新信息
        self.report_title.setText(report_info.get("name", ""))
        for key, label in self.report_info_labels.items():
            label.setText(str(report_info.get(key, "--")))
        
        # 加载HTML
        path = report_info.get("path")
        if path and os.path.exists(path):
            if self._has_web_view:
                self.web_view.setUrl(QUrl.fromLocalFile(path))
            else:
                with open(path, "r", encoding="utf-8") as f:
                    html = f.read()
                self.web_view.setHtml(html)
        
        self.report_selected.emit(report_info)
    
    def _open_in_browser(self):
        """在浏览器中打开"""
        if self._current_report:
            path = self._current_report.get("path")
            if path:
                import webbrowser
                webbrowser.open(f"file://{path}")
    
    def _export_pdf(self):
        """导出PDF"""
        if not self._current_report:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出PDF", f"{self._current_report['name']}.pdf", "PDF Files (*.pdf)"
        )
        
        if file_path:
            QMessageBox.information(self, "导出", "PDF导出功能开发中...")
    
    def _compare_reports(self):
        """对比报告"""
        QMessageBox.information(self, "对比分析", "报告对比功能开发中...")
    
    def _delete_report(self):
        """删除报告"""
        if not self._current_report:
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除报告 '{self._current_report['name']}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            path = self._current_report.get("path")
            if path and os.path.exists(path):
                os.remove(path)
                logger.info(f"已删除报告: {path}")
            self._load_reports()


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = ReportViewerPanel()
    panel.setWindowTitle("报告查看")
    panel.resize(1000, 700)
    panel.show()
    sys.exit(app.exec())
