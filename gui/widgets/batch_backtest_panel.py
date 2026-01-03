# -*- coding: utf-8 -*-
"""
批量回测面板
============
支持参数网格搜索、批量回测、结果对比

功能:
- 参数网格配置
- 并行回测执行
- 结果排名展示
- 最优参数发现
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QSpinBox, QDoubleSpinBox,
    QComboBox, QDateEdit, QGroupBox, QSplitter, QTextEdit,
    QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from gui.styles.theme import Colors, ButtonStyles

logger = logging.getLogger(__name__)


class ParameterRangeWidget(QFrame):
    """参数范围配置控件"""
    
    def __init__(self, param_name: str, param_config: Dict, parent=None):
        super().__init__(parent)
        self.param_name = param_name
        self.param_config = param_config
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)
        
        # 参数名称
        name_label = QLabel(param_name)
        name_label.setStyleSheet(f"font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        name_label.setFixedWidth(100)
        layout.addWidget(name_label)
        
        # 启用复选框
        self.enabled_check = QCheckBox("启用")
        self.enabled_check.setChecked(True)
        self.enabled_check.stateChanged.connect(self._on_enabled_changed)
        layout.addWidget(self.enabled_check)
        
        # 起始值
        layout.addWidget(QLabel("起始:"))
        self.start_spin = self._create_spin(param_config)
        self.start_spin.setValue(param_config.get("range", [1, 100])[0])
        layout.addWidget(self.start_spin)
        
        # 结束值
        layout.addWidget(QLabel("结束:"))
        self.end_spin = self._create_spin(param_config)
        self.end_spin.setValue(param_config.get("range", [1, 100])[1])
        layout.addWidget(self.end_spin)
        
        # 步长
        layout.addWidget(QLabel("步长:"))
        self.step_spin = self._create_spin(param_config)
        default_step = 5 if param_config.get("type") == "int" else 0.5
        self.step_spin.setValue(default_step)
        layout.addWidget(self.step_spin)
        
        # 组合数预览
        self.count_label = QLabel("0 个值")
        self.count_label.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        layout.addWidget(self.count_label)
        
        layout.addStretch()
        
        # 连接信号
        self.start_spin.valueChanged.connect(self._update_count)
        self.end_spin.valueChanged.connect(self._update_count)
        self.step_spin.valueChanged.connect(self._update_count)
        
        self._update_count()
    
    def _create_spin(self, config: Dict):
        """创建数值输入框"""
        if config.get("type") == "float":
            spin = QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setSingleStep(0.1)
            spin.setRange(0, 1000)
        else:
            spin = QSpinBox()
            spin.setRange(1, 1000)
        
        spin.setStyleSheet(f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 4px 8px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        return spin
    
    def _on_enabled_changed(self, state):
        """启用状态变化"""
        enabled = state == Qt.CheckState.Checked.value
        self.start_spin.setEnabled(enabled)
        self.end_spin.setEnabled(enabled)
        self.step_spin.setEnabled(enabled)
    
    def _update_count(self):
        """更新组合数"""
        values = self.get_values()
        self.count_label.setText(f"{len(values)} 个值")
    
    def is_enabled(self) -> bool:
        return self.enabled_check.isChecked()
    
    def get_values(self) -> List:
        """获取参数值列表"""
        if not self.is_enabled():
            return [self.param_config.get("default", 10)]
        
        start = self.start_spin.value()
        end = self.end_spin.value()
        step = self.step_spin.value()
        
        if step <= 0:
            return [start]
        
        values = []
        current = start
        while current <= end:
            values.append(current)
            current += step
        
        return values if values else [start]


class BatchBacktestPanel(QWidget):
    """批量回测面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._integration = None
        self._results = []
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # === 标题 ===
        title_frame = self._create_title()
        layout.addWidget(title_frame)
        
        # === 主分割器 ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：配置面板
        config_panel = self._create_config_panel()
        splitter.addWidget(config_panel)
        
        # 右侧：结果面板
        result_panel = self._create_result_panel()
        splitter.addWidget(result_panel)
        
        splitter.setSizes([400, 700])
        layout.addWidget(splitter)
    
    def _create_title(self) -> QFrame:
        """创建标题"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1E3A5F,
                    stop:1 #2E5A8F
                );
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(32, 24, 32, 24)
        
        title = QLabel("🔬 批量回测 & 参数优化")
        title.setStyleSheet(f"font-size: 22px; font-weight: 800; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        subtitle = QLabel("参数网格搜索 · 并行回测 · 最优参数发现 · 结果对比分析")
        subtitle.setStyleSheet(f"font-size: 13px; color: {Colors.TEXT_MUTED};")
        layout.addWidget(subtitle)
        
        return frame
    
    def _create_config_panel(self) -> QFrame:
        """创建配置面板"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        panel.setFixedWidth(420)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # === 基础配置 ===
        basic_group = QGroupBox("基础配置")
        basic_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """)
        basic_layout = QGridLayout(basic_group)
        basic_layout.setSpacing(12)
        
        # 策略类型
        basic_layout.addWidget(QLabel("策略类型:"), 0, 0)
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(["momentum - 动量策略", "mean_reversion - 均值回归"])
        self.strategy_combo.currentIndexChanged.connect(self._on_strategy_changed)
        basic_layout.addWidget(self.strategy_combo, 0, 1)
        
        # 日期
        basic_layout.addWidget(QLabel("开始日期:"), 1, 0)
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-3))
        self.start_date.setCalendarPopup(True)
        basic_layout.addWidget(self.start_date, 1, 1)
        
        basic_layout.addWidget(QLabel("结束日期:"), 2, 0)
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        basic_layout.addWidget(self.end_date, 2, 1)
        
        # 并行数
        basic_layout.addWidget(QLabel("并行任务数:"), 3, 0)
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 8)
        self.workers_spin.setValue(4)
        basic_layout.addWidget(self.workers_spin, 3, 1)
        
        layout.addWidget(basic_group)
        
        # === 参数配置 ===
        param_group = QGroupBox("参数范围配置")
        param_group.setStyleSheet(basic_group.styleSheet())
        self.param_layout = QVBoxLayout(param_group)
        self.param_layout.setSpacing(8)
        
        self.param_widgets: Dict[str, ParameterRangeWidget] = {}
        self._load_strategy_params("momentum")
        
        layout.addWidget(param_group)
        
        # === 组合统计 ===
        stats_frame = QFrame()
        stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        stats_layout = QHBoxLayout(stats_frame)
        
        self.total_combo_label = QLabel("总组合数: 0")
        self.total_combo_label.setStyleSheet(f"font-weight: 600; color: {Colors.PRIMARY};")
        stats_layout.addWidget(self.total_combo_label)
        
        self.est_time_label = QLabel("预计耗时: --")
        self.est_time_label.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        stats_layout.addWidget(self.est_time_label)
        
        stats_layout.addStretch()
        layout.addWidget(stats_frame)
        
        layout.addStretch()
        
        # === 进度 ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p% - %v/%m")
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 12px;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.hide()
        layout.addWidget(self.progress_label)
        
        # === 按钮 ===
        btn_layout = QHBoxLayout()
        
        self.run_btn = QPushButton("🚀 开始批量回测")
        self.run_btn.setStyleSheet(ButtonStyles.PRIMARY)
        self.run_btn.setFixedHeight(48)
        self.run_btn.clicked.connect(self._run_batch)
        btn_layout.addWidget(self.run_btn)
        
        self.cancel_btn = QPushButton("⏹ 取消")
        self.cancel_btn.setFixedHeight(48)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(btn_layout)
        
        return panel
    
    def _create_result_panel(self) -> QFrame:
        """创建结果面板"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # === 最佳结果 ===
        best_group = QGroupBox("🏆 最佳结果")
        best_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                color: {Colors.SUCCESS};
                border: 2px solid {Colors.SUCCESS}40;
                border-radius: 8px;
                margin-top: 12px;
                padding: 16px;
            }}
        """)
        best_layout = QHBoxLayout(best_group)
        
        self.best_labels = {}
        metrics = [
            ("params", "最优参数"),
            ("sharpe", "夏普比率"),
            ("return", "总收益"),
            ("drawdown", "最大回撤"),
        ]
        
        for key, title in metrics:
            frame = QFrame()
            frame.setStyleSheet(f"background-color: {Colors.BG_PRIMARY}; border-radius: 8px; padding: 8px;")
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(12, 8, 12, 8)
            
            value_label = QLabel("--")
            value_label.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {Colors.SUCCESS};")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(value_label)
            
            name_label = QLabel(title)
            name_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(name_label)
            
            best_layout.addWidget(frame)
            self.best_labels[key] = value_label
        
        layout.addWidget(best_group)
        
        # === 结果表格 ===
        table_label = QLabel("📊 所有结果排名 (按夏普比率)")
        table_label.setStyleSheet(f"font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(table_label)
        
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(7)
        self.result_table.setHorizontalHeaderLabels([
            "排名", "参数", "总收益%", "年化%", "夏普比率", "最大回撤%", "胜率%"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_MUTED};
                padding: 10px;
                border: none;
                font-weight: 600;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
        """)
        layout.addWidget(self.result_table)
        
        # === 统计摘要 ===
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMaximumHeight(150)
        self.summary_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        self.summary_text.setPlaceholderText("运行批量回测后显示统计摘要...")
        layout.addWidget(self.summary_text)
        
        return panel
    
    def _on_strategy_changed(self, index):
        """策略类型变化"""
        strategy_type = self.strategy_combo.currentText().split(" - ")[0]
        self._load_strategy_params(strategy_type)
    
    def _load_strategy_params(self, strategy_type: str):
        """加载策略参数配置"""
        # 清除现有参数
        for widget in self.param_widgets.values():
            widget.deleteLater()
        self.param_widgets.clear()
        
        # 获取参数定义
        from gui.widgets.backtest_integration import get_strategy_params
        params = get_strategy_params(strategy_type)
        
        for name, config in params.items():
            widget = ParameterRangeWidget(name, config)
            widget.start_spin.valueChanged.connect(self._update_total_combo)
            widget.end_spin.valueChanged.connect(self._update_total_combo)
            widget.step_spin.valueChanged.connect(self._update_total_combo)
            widget.enabled_check.stateChanged.connect(self._update_total_combo)
            
            self.param_layout.addWidget(widget)
            self.param_widgets[name] = widget
        
        self._update_total_combo()
    
    def _update_total_combo(self):
        """更新总组合数"""
        total = 1
        for widget in self.param_widgets.values():
            if widget.is_enabled():
                total *= len(widget.get_values())
        
        self.total_combo_label.setText(f"总组合数: {total}")
        
        # 估算时间（假设每个组合0.5秒）
        workers = self.workers_spin.value()
        est_seconds = total * 0.5 / workers
        if est_seconds < 60:
            self.est_time_label.setText(f"预计耗时: {est_seconds:.0f}秒")
        else:
            self.est_time_label.setText(f"预计耗时: {est_seconds/60:.1f}分钟")
    
    def _get_parameter_ranges(self) -> Dict[str, List]:
        """获取参数范围"""
        ranges = {}
        for name, widget in self.param_widgets.items():
            ranges[name] = widget.get_values()
        return ranges
    
    def _run_batch(self):
        """运行批量回测"""
        from gui.widgets.backtest_integration import get_backtest_integration
        
        self._integration = get_backtest_integration()
        
        # 连接信号
        self._integration.batch_progress.connect(self._on_progress)
        self._integration.batch_finished.connect(self._on_finished)
        self._integration.batch_error.connect(self._on_error)
        
        # 获取配置
        strategy_type = self.strategy_combo.currentText().split(" - ")[0]
        parameter_ranges = self._get_parameter_ranges()
        
        # 默认股票池
        securities = ["000001.XSHE", "600000.XSHG", "000002.XSHE", "600036.XSHG", "000858.XSHE"]
        
        # 更新UI
        self.run_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.show()
        self.progress_label.show()
        
        # 启动批量回测
        self._integration.run_batch_backtest(
            securities=securities,
            start_date=self.start_date.date().toString("yyyy-MM-dd"),
            end_date=self.end_date.date().toString("yyyy-MM-dd"),
            strategy_type=strategy_type,
            parameter_ranges=parameter_ranges,
            use_mock=True,
            max_workers=self.workers_spin.value()
        )
    
    def _cancel(self):
        """取消"""
        if self._integration:
            self._integration.cancel()
    
    def _on_progress(self, progress: float, message: str):
        """进度更新"""
        self.progress_bar.setValue(int(progress * 100))
        self.progress_label.setText(message)
    
    def _on_finished(self, data: Dict):
        """批量回测完成"""
        self.run_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.hide()
        self.progress_label.hide()
        
        # 更新最佳结果
        best = data.get("best_result")
        if best:
            params_str = ", ".join(f"{k}={v}" for k, v in best.get("params", {}).items())
            self.best_labels["params"].setText(params_str[:30] + "..." if len(params_str) > 30 else params_str)
            self.best_labels["sharpe"].setText(f"{best.get('sharpe_ratio', 0):.2f}")
            self.best_labels["return"].setText(f"{best.get('total_return', 0):.2f}%")
            self.best_labels["drawdown"].setText(f"{best.get('max_drawdown', 0):.2f}%")
        
        # 更新表格
        results = data.get("results", [])
        results.sort(key=lambda x: x.get("sharpe_ratio", 0), reverse=True)
        
        self.result_table.setRowCount(len(results))
        for i, r in enumerate(results[:50]):  # 只显示前50
            params_str = ", ".join(f"{k}={v}" for k, v in r.get("params", {}).items())
            
            self.result_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.result_table.setItem(i, 1, QTableWidgetItem(params_str))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{r.get('total_return', 0):.2f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(f"{r.get('annual_return', 0):.2f}"))
            self.result_table.setItem(i, 4, QTableWidgetItem(f"{r.get('sharpe_ratio', 0):.2f}"))
            self.result_table.setItem(i, 5, QTableWidgetItem(f"{r.get('max_drawdown', 0):.2f}"))
            self.result_table.setItem(i, 6, QTableWidgetItem(f"{r.get('win_rate', 0):.2f}"))
            
            # 颜色
            if i == 0:  # 最佳
                for col in range(7):
                    item = self.result_table.item(i, col)
                    if item:
                        item.setBackground(QColor(Colors.SUCCESS + "20"))
        
        # 更新摘要
        summary = data.get("summary", {})
        report = data.get("report", {})
        
        summary_text = f"""
批量回测完成！

📊 执行统计:
- 总任务数: {summary.get('total_tasks', 0)}
- 完成数: {summary.get('completed_tasks', 0)}
- 失败数: {summary.get('failed_tasks', 0)}
- 总耗时: {summary.get('total_time_seconds', 0):.2f}秒

📈 结果统计:
- 夏普比率: 均值={report.get('statistics', {}).get('sharpe_ratio', {}).get('mean', 0):.2f}, 最大={report.get('statistics', {}).get('sharpe_ratio', {}).get('max', 0):.2f}
- 总收益: 均值={report.get('statistics', {}).get('total_return', {}).get('mean', 0):.2f}%, 最大={report.get('statistics', {}).get('total_return', {}).get('max', 0):.2f}%
"""
        self.summary_text.setPlainText(summary_text)
        
        QMessageBox.information(self, "完成", f"批量回测完成！共 {len(results)} 个结果")
    
    def _on_error(self, error: str):
        """错误处理"""
        self.run_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.hide()
        self.progress_label.hide()
        
        QMessageBox.warning(self, "错误", f"批量回测失败: {error}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = BatchBacktestPanel()
    panel.setWindowTitle("批量回测")
    panel.resize(1200, 800)
    panel.show()
    sys.exit(app.exec())
