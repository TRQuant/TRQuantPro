#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""启动投资工作流程前端面板"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDialog
from PyQt6.QtCore import Qt
import logging

from gui.widgets.investment_workflow_panel import InvestmentWorkflowPanel
from gui.styles.theme import Colors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkflowMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 TRQuant 投资工作流程")
        self.setMinimumSize(1400, 900)
        self.setStyleSheet(f"QMainWindow {{ background: {Colors.BG_PRIMARY}; }} QWidget {{ color: {Colors.TEXT_PRIMARY}; font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif; }}")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.workflow_panel = InvestmentWorkflowPanel(self)
        self.workflow_panel.open_notebook.connect(lambda p: logger.info(f"Notebook已打开: {p}"))
        self.workflow_panel.open_data_source_panel.connect(self._on_open_data_source)
        self.workflow_panel.execute_action.connect(lambda a: logger.info(f"执行动作: {a}"))
        layout.addWidget(self.workflow_panel)
    
    def _on_open_data_source(self):
        from gui.widgets.data_status_panel import DataStatusPanel
        dialog = QDialog(self)
        dialog.setWindowTitle("📡 数据源状态")
        dialog.setMinimumSize(800, 600)
        layout = QVBoxLayout(dialog)
        layout.addWidget(DataStatusPanel())
        dialog.exec()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TRQuant Workflow")
    window = WorkflowMainWindow()
    window.show()
    logger.info("投资工作流程面板已启动")
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
