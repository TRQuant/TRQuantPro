#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主线因子组合测试GUI

独立的测试窗口，用于测试和可视化主线预测因子组合功能
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QTextEdit, QProgressBar, QFrame, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 使用项目中的颜色主题
try:
    from gui.styles.theme import Colors
    COLORS = Colors
except ImportError:
    # 备用颜色定义
    class Colors:
        BG_PRIMARY = "#0d0d14"
        BG_SECONDARY = "#12121f"
        BG_TERTIARY = "#181825"
        TEXT_PRIMARY = "#ffffff"
        TEXT_SECONDARY = "#cdd6f4"
        TEXT_MUTED = "#9ca3af"
        SUCCESS = "#a6e3a1"
        WARNING = "#f9e2af"
        ERROR = "#f38ba8"
        PRIMARY = "#667eea"
        BORDER_PRIMARY = "#2a2a4a"
    COLORS = Colors


class FactorCalculationWorker(QThread):
    """因子计算工作线程"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(int, str)
    
    def __init__(self, industry_code: str, date: str, period: str):
        super().__init__()
        self.industry_code = industry_code
        self.date = date
        self.period = period
    
    def run(self):
        """执行因子计算"""
        try:
            from core.mainline.mainline_workflow_integration import MainlineWorkflowStep
            
            self.progress.emit(10, "初始化工作流步骤...")
            
            # 初始化工作流步骤
            workflow_step = MainlineWorkflowStep()
            
            self.progress.emit(30, "计算因子组合得分...")
            
            # 计算因子组合得分
            factor_combo = workflow_step.factor_combo
            score_result = factor_combo.calculate_mainline_score(
                industry_code=self.industry_code,
                date=self.date,
                period=self.period
            )
            
            self.progress.emit(80, "完成计算...")
            
            # 返回结果
            self.finished.emit(score_result)
            
        except Exception as e:
            logger.error(f"因子计算失败: {e}", exc_info=True)
            self.error.emit(str(e))


class MainlineFactorTestWindow(QMainWindow):
    """主线因子组合测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        """设置UI"""
        self.setWindowTitle("主线因子组合测试工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # ========== 顶部控制面板 ==========
        control_group = QGroupBox("测试参数配置")
        control_layout = QHBoxLayout(control_group)
        
        # 行业代码输入
        control_layout.addWidget(QLabel("行业代码:"))
        self.industry_combo = QComboBox()
        self.industry_combo.setEditable(True)
        self.industry_combo.addItems([
            "801010",  # 申万一级行业示例
            "801020",
            "801030",
            "801040",
            "801050"
        ])
        self.industry_combo.setCurrentText("801010")
        self.industry_combo.setMinimumWidth(150)
        control_layout.addWidget(self.industry_combo)
        
        # 日期选择
        control_layout.addWidget(QLabel("日期:"))
        self.date_combo = QComboBox()
        self.date_combo.setEditable(True)
        today = datetime.now().strftime('%Y-%m-%d')
        self.date_combo.addItems([today])
        self.date_combo.setCurrentText(today)
        self.date_combo.setMinimumWidth(150)
        control_layout.addWidget(self.date_combo)
        
        # 期限选择
        control_layout.addWidget(QLabel("期限:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["short", "medium", "long"])
        self.period_combo.setCurrentText("medium")
        control_layout.addWidget(self.period_combo)
        
        control_layout.addStretch()
        
        # 计算按钮
        self.calculate_btn = QPushButton("🚀 计算因子组合得分")
        self.calculate_btn.clicked.connect(self._on_calculate)
        self.calculate_btn.setMinimumWidth(180)
        self.calculate_btn.setMinimumHeight(35)
        control_layout.addWidget(self.calculate_btn)
        
        layout.addWidget(control_group)
        
        # ========== 进度条 ==========
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # ========== 结果展示区域 ==========
        result_group = QGroupBox("因子组合得分结果")
        result_layout = QVBoxLayout(result_group)
        
        # 总分显示
        score_frame = QFrame()
        score_layout = QHBoxLayout(score_frame)
        score_label = QLabel("综合得分:")
        score_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.total_score_label = QLabel("--")
        self.total_score_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.total_score_label.setStyleSheet(f"color: {COLORS.SUCCESS};")
        score_layout.addWidget(score_label)
        score_layout.addWidget(self.total_score_label)
        score_layout.addStretch()
        result_layout.addWidget(score_frame)
        
        # 各因子得分表格
        self.factor_table = QTableWidget()
        self.factor_table.setColumnCount(3)
        self.factor_table.setHorizontalHeaderLabels(["因子类别", "得分", "权重"])
        self.factor_table.horizontalHeader().setStretchLastSection(True)
        self.factor_table.setMinimumHeight(200)
        result_layout.addWidget(self.factor_table)
        
        layout.addWidget(result_group)
        
        # ========== 详细数据展示 ==========
        detail_group = QGroupBox("详细数据")
        detail_layout = QVBoxLayout(detail_group)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMinimumHeight(200)
        detail_layout.addWidget(self.detail_text)
        
        layout.addWidget(detail_group)
        
        # ========== 状态栏 ==========
        self.statusBar().showMessage("就绪")
    
    def _apply_style(self):
        """应用样式"""
        style = f"""
        QMainWindow {{
            background-color: {COLORS.BG_PRIMARY};
            color: {COLORS.TEXT_PRIMARY};
        }}
        QGroupBox {{
            font-size: 14px;
            font-weight: bold;
            border: 2px solid {COLORS.BORDER_PRIMARY};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            color: {COLORS.TEXT_PRIMARY};
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QLabel {{
            color: {COLORS.TEXT_PRIMARY};
        }}
        QPushButton {{
            background-color: {COLORS.PRIMARY};
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {COLORS.PRIMARY_DARK if hasattr(COLORS, 'PRIMARY_DARK') else '#5568d6'};
        }}
        QPushButton:disabled {{
            background-color: {COLORS.BG_TERTIARY};
            color: {COLORS.TEXT_MUTED};
        }}
        QTableWidget {{
            background-color: {COLORS.BG_SECONDARY};
            border: 1px solid {COLORS.BORDER_PRIMARY};
            gridline-color: {COLORS.BORDER_PRIMARY};
            color: {COLORS.TEXT_PRIMARY};
        }}
        QTableWidget::item {{
            padding: 5px;
        }}
        QHeaderView::section {{
            background-color: {COLORS.BG_TERTIARY};
            color: {COLORS.TEXT_PRIMARY};
            padding: 5px;
            border: none;
            font-weight: bold;
        }}
        QTextEdit {{
            background-color: {COLORS.BG_SECONDARY};
            border: 1px solid {COLORS.BORDER_PRIMARY};
            color: {COLORS.TEXT_PRIMARY};
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 11px;
        }}
        QComboBox {{
            background-color: {COLORS.BG_SECONDARY};
            border: 1px solid {COLORS.BORDER_PRIMARY};
            color: {COLORS.TEXT_PRIMARY};
            padding: 5px;
            border-radius: 3px;
        }}
        QProgressBar {{
            border: 1px solid {COLORS.BORDER_PRIMARY};
            border-radius: 3px;
            text-align: center;
            background-color: {COLORS.BG_SECONDARY};
        }}
        QProgressBar::chunk {{
            background-color: {COLORS.SUCCESS};
        }}
        """
        self.setStyleSheet(style)
    
    def _on_calculate(self):
        """计算按钮点击事件"""
        # 获取参数
        industry_code = self.industry_combo.currentText().strip()
        date = self.date_combo.currentText().strip()
        period = self.period_combo.currentText()
        
        if not industry_code:
            QMessageBox.warning(self, "警告", "请输入行业代码")
            return
        
        # 禁用按钮
        self.calculate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("正在计算...")
        
        # 创建工作线程
        self.worker = FactorCalculationWorker(industry_code, date, period)
        self.worker.finished.connect(self._on_calculation_finished)
        self.worker.error.connect(self._on_calculation_error)
        self.worker.progress.connect(self._on_progress)
        self.worker.start()
    
    def _on_progress(self, value: int, message: str):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.statusBar().showMessage(message)
    
    def _on_calculation_finished(self, result: dict):
        """计算完成"""
        self.progress_bar.setValue(100)
        self.progress_bar.setVisible(False)
        self.calculate_btn.setEnabled(True)
        self.statusBar().showMessage("计算完成")
        
        # 显示总分
        total_score = result.get('total_score', 0)
        self.total_score_label.setText(f"{total_score:.2f}")
        
        # 显示各因子得分
        self._display_factor_scores(result)
        
        # 显示详细数据
        self._display_details(result)
        
        # 成功提示
        QMessageBox.information(self, "成功", f"计算完成！综合得分: {total_score:.2f}")
    
    def _display_factor_scores(self, result: dict):
        """显示因子得分表格"""
        factor_names = {
            'macro_score': '宏观因子',
            'capital_flow_score': '资金流因子',
            'industry_prosperity_score': '行业景气因子',
            'technical_momentum_score': '技术动量因子',
            'market_sentiment_score': '市场情绪因子'
        }
        
        weights = result.get('weights_used', {})
        
        rows = []
        for key, name in factor_names.items():
            score = result.get(key, 0)
            weight = weights.get(key.replace('_score', ''), 0)
            rows.append((name, score, weight))
        
        self.factor_table.setRowCount(len(rows))
        
        for i, (name, score, weight) in enumerate(rows):
            # 因子名称
            name_item = QTableWidgetItem(name)
            self.factor_table.setItem(i, 0, name_item)
            
            # 得分
            score_item = QTableWidgetItem(f"{score:.2f}")
            if score >= 70:
                score_item.setForeground(QColor(COLORS.SUCCESS))
            elif score < 50:
                score_item.setForeground(QColor(COLORS.ERROR))
            else:
                score_item.setForeground(QColor(COLORS.WARNING))
            self.factor_table.setItem(i, 1, score_item)
            
            # 权重
            weight_item = QTableWidgetItem(f"{weight*100:.1f}%")
            self.factor_table.setItem(i, 2, weight_item)
    
    def _display_details(self, result: dict):
        """显示详细数据"""
        import json
        
        # 格式化显示
        details = {
            '综合得分': result.get('total_score', 0),
            '期限': result.get('period', ''),
            '行业代码': result.get('industry_code', ''),
            '日期': result.get('date', ''),
            '股票数量': result.get('n_stocks', 0),
            '因子详细数据': result.get('factor_details', {})
        }
        
        detail_text = json.dumps(details, indent=2, ensure_ascii=False)
        self.detail_text.setText(detail_text)
    
    def _on_calculation_error(self, error_msg: str):
        """计算错误"""
        self.progress_bar.setVisible(False)
        self.calculate_btn.setEnabled(True)
        self.statusBar().showMessage("计算失败")
        
        QMessageBox.critical(self, "错误", f"计算失败:\n{error_msg}")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("主线因子组合测试工具")
    app.setOrganizationName("TRQuant")
    
    # 创建窗口
    window = MainlineFactorTestWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

