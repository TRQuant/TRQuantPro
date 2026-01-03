# -*- coding: utf-8 -*-
"""
回测进度面板
============

显示回测任务的实时进度、日志和状态
通过MCPClient调用回测服务

功能:
- 实时进度显示
- 任务状态监控
- 日志实时输出
- 多任务管理
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QProgressBar, QTextEdit, QTableWidget, QTableWidgetItem,
    QSplitter, QHeaderView, QGroupBox, QComboBox, QLineEdit,
    QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt6.QtGui import QColor, QTextCursor
from datetime import datetime
from typing import Dict, Optional, Callable
import logging
import json

logger = logging.getLogger(__name__)


class BacktestWorker(QThread):
    """回测执行线程"""
    progress = pyqtSignal(int, str)  # progress%, message
    log = pyqtSignal(str, str)  # level, message
    finished = pyqtSignal(dict)  # result
    error = pyqtSignal(str)  # error message
    
    def __init__(self, tool_name: str, arguments: dict, parent=None):
        super().__init__(parent)
        self.tool_name = tool_name
        self.arguments = arguments
        self._cancelled = False
    
    def cancel(self):
        self._cancelled = True
    
    def run(self):
        try:
            from core.mcp import get_mcp_client
            
            client = get_mcp_client()
            
            def on_progress(p, msg):
                if not self._cancelled:
                    self.progress.emit(p, msg)
                    self.log.emit("INFO", f"[{p}%] {msg}")
            
            self.log.emit("INFO", f"开始执行: {self.tool_name}")
            self.log.emit("INFO", f"参数: {json.dumps(self.arguments, ensure_ascii=False)}")
            
            result = client.call(self.tool_name, self.arguments, on_progress=on_progress)
            
            if self._cancelled:
                self.log.emit("WARNING", "任务已取消")
                return
            
            if result.success:
                self.log.emit("INFO", f"执行成功, 耗时: {result.duration:.2f}秒")
                self.finished.emit(result.data)
            else:
                self.log.emit("ERROR", f"执行失败: {result.error}")
                self.error.emit(result.error)
                
        except Exception as e:
            self.log.emit("ERROR", f"异常: {str(e)}")
            self.error.emit(str(e))


class BacktestProgressPanel(QWidget):
    """回测进度面板"""
    
    backtest_started = pyqtSignal(str)  # task_id
    backtest_finished = pyqtSignal(str, dict)  # task_id, result
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._tasks: Dict[str, dict] = {}
        self._current_worker: Optional[BacktestWorker] = None
        
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # === 顶部控制区 ===
        control_layout = QHBoxLayout()
        
        # 回测引擎选择
        control_layout.addWidget(QLabel("回测引擎:"))
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["BulletTrade", "QMT", "快速回测"])
        control_layout.addWidget(self.engine_combo)
        
        control_layout.addStretch()
        
        # 操作按钮
        self.start_btn = QPushButton("▶ 开始回测")
        self.start_btn.clicked.connect(self._on_start_clicked)
        control_layout.addWidget(self.start_btn)
        
        self.cancel_btn = QPushButton("⏹ 取消")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._on_cancel_clicked)
        control_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(control_layout)
        
        # === 主内容区 ===
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # --- 进度区 ---
        progress_group = QGroupBox("回测进度")
        progress_layout = QVBoxLayout(progress_group)
        
        # 状态行
        status_layout = QHBoxLayout()
        self.status_label = QLabel("状态: 等待中")
        self.status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.status_label)
        
        self.time_label = QLabel("耗时: --")
        status_layout.addWidget(self.time_label)
        status_layout.addStretch()
        progress_layout.addLayout(status_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #404050;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:1 #00ff88);
                border-radius: 4px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        # 进度消息
        self.progress_msg = QLabel("")
        self.progress_msg.setStyleSheet("color: #888;")
        progress_layout.addWidget(self.progress_msg)
        
        splitter.addWidget(progress_group)
        
        # --- 日志区 ---
        log_group = QGroupBox("执行日志")
        log_layout = QVBoxLayout(log_group)
        
        # 日志筛选
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("级别:"))
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["ALL", "INFO", "WARNING", "ERROR"])
        self.log_level_combo.currentTextChanged.connect(self._filter_logs)
        filter_layout.addWidget(self.log_level_combo)
        
        self.log_search = QLineEdit()
        self.log_search.setPlaceholderText("搜索日志...")
        self.log_search.textChanged.connect(self._filter_logs)
        filter_layout.addWidget(self.log_search)
        
        self.clear_log_btn = QPushButton("清除")
        self.clear_log_btn.clicked.connect(self._clear_logs)
        filter_layout.addWidget(self.clear_log_btn)
        
        log_layout.addLayout(filter_layout)
        
        # 日志文本
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: #1e1e2e;
                color: #e0e0e0;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #404050;
                border-radius: 5px;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        splitter.addWidget(log_group)
        
        # --- 任务列表区 ---
        task_group = QGroupBox("任务列表")
        task_layout = QVBoxLayout(task_group)
        
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(6)
        self.task_table.setHorizontalHeaderLabels([
            "任务ID", "引擎", "策略", "状态", "进度", "开始时间"
        ])
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.task_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        task_layout.addWidget(self.task_table)
        
        splitter.addWidget(task_group)
        
        # 设置分割比例
        splitter.setSizes([100, 200, 150])
        
        layout.addWidget(splitter)
        
        # --- 结果预览区 ---
        result_group = QGroupBox("结果预览")
        result_layout = QHBoxLayout(result_group)
        
        self.result_labels = {}
        metrics = [
            ("total_return", "总收益"),
            ("annual_return", "年化收益"),
            ("sharpe_ratio", "夏普比率"),
            ("max_drawdown", "最大回撤"),
            ("win_rate", "胜率")
        ]
        
        for key, label in metrics:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background: #2d2d3d;
                    border-radius: 8px;
                    padding: 5px;
                }
            """)
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(10, 5, 10, 5)
            
            value_label = QLabel("--")
            value_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00d9ff;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(value_label)
            
            name_label = QLabel(label)
            name_label.setStyleSheet("color: #888; font-size: 11px;")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(name_label)
            
            result_layout.addWidget(frame)
            self.result_labels[key] = value_label
        
        layout.addWidget(result_group)
        
        # 计时器
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_time)
        self._start_time = None
        
        # 日志缓存
        self._log_entries = []
    
    def start_backtest(self, 
                       strategy_path: str = None,
                       strategy_code: str = None,
                       start_date: str = "2024-01-01",
                       end_date: str = "2024-06-30",
                       initial_capital: float = 1000000):
        """启动回测"""
        
        engine = self.engine_combo.currentText()
        
        if engine == "BulletTrade":
            tool_name = "backtest.bullettrade"
        elif engine == "QMT":
            tool_name = "backtest.qmt"
        else:
            tool_name = "backtest.quick"
        
        arguments = {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital
        }
        
        if strategy_path:
            arguments["strategy_path"] = strategy_path
        if strategy_code:
            arguments["strategy_code"] = strategy_code
        
        # 创建任务
        task_id = f"task_{datetime.now().strftime('%H%M%S')}"
        self._tasks[task_id] = {
            "engine": engine,
            "strategy": strategy_path or "inline",
            "status": "running",
            "progress": 0,
            "started_at": datetime.now()
        }
        self._add_task_to_table(task_id)
        
        # 创建工作线程
        self._current_worker = BacktestWorker(tool_name, arguments)
        self._current_worker.progress.connect(self._on_progress)
        self._current_worker.log.connect(self._on_log)
        self._current_worker.finished.connect(lambda r: self._on_finished(task_id, r))
        self._current_worker.error.connect(lambda e: self._on_error(task_id, e))
        
        # 更新UI状态
        self.start_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("状态: 运行中")
        self.status_label.setStyleSheet("font-weight: bold; color: #00d9ff;")
        
        # 启动计时
        self._start_time = datetime.now()
        self._timer.start(1000)
        
        # 启动工作线程
        self._current_worker.start()
        
        self.backtest_started.emit(task_id)
        self._log("INFO", f"回测任务已启动: {task_id}")
    
    def _on_start_clicked(self):
        """开始按钮点击"""
        # 这里简化处理，实际应该弹出配置对话框
        self.start_backtest(
            strategy_path="strategies/bullettrade/TRQuant_momentum_v3_bt.py",
            start_date="2024-01-01",
            end_date="2024-06-30"
        )
    
    def _on_cancel_clicked(self):
        """取消按钮点击"""
        if self._current_worker:
            self._current_worker.cancel()
            self._log("WARNING", "正在取消任务...")
    
    def _on_progress(self, progress: int, message: str):
        """进度更新"""
        self.progress_bar.setValue(progress)
        self.progress_msg.setText(message)
    
    def _on_log(self, level: str, message: str):
        """日志更新"""
        self._log(level, message)
    
    def _on_finished(self, task_id: str, result: dict):
        """回测完成"""
        self._timer.stop()
        
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.status_label.setText("状态: 已完成")
        self.status_label.setStyleSheet("font-weight: bold; color: #00ff88;")
        
        # 更新任务状态
        if task_id in self._tasks:
            self._tasks[task_id]["status"] = "completed"
            self._tasks[task_id]["progress"] = 100
        self._update_task_table()
        
        # 更新结果显示
        self._update_results(result)
        
        self._log("INFO", "=" * 50)
        self._log("INFO", "回测完成!")
        if result.get("total_return"):
            self._log("INFO", f"总收益: {result['total_return']*100:.2f}%")
        if result.get("sharpe_ratio"):
            self._log("INFO", f"夏普比率: {result['sharpe_ratio']:.2f}")
        
        self.backtest_finished.emit(task_id, result)
    
    def _on_error(self, task_id: str, error: str):
        """回测错误"""
        self._timer.stop()
        
        self.start_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.status_label.setText("状态: 失败")
        self.status_label.setStyleSheet("font-weight: bold; color: #ff4444;")
        
        if task_id in self._tasks:
            self._tasks[task_id]["status"] = "failed"
        self._update_task_table()
        
        self._log("ERROR", f"回测失败: {error}")
        
        QMessageBox.critical(self, "回测失败", f"错误: {error}")
    
    def _update_time(self):
        """更新耗时显示"""
        if self._start_time:
            elapsed = (datetime.now() - self._start_time).total_seconds()
            self.time_label.setText(f"耗时: {elapsed:.1f}秒")
    
    def _update_results(self, result: dict):
        """更新结果显示"""
        for key, label in self.result_labels.items():
            value = result.get(key)
            if value is not None:
                if key in ["total_return", "annual_return", "max_drawdown", "win_rate"]:
                    label.setText(f"{value*100:.2f}%")
                    if key in ["total_return", "annual_return", "win_rate"]:
                        color = "#00ff88" if value > 0 else "#ff4444"
                    else:
                        color = "#ff4444"
                    label.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")
                else:
                    label.setText(f"{value:.2f}")
    
    def _log(self, level: str, message: str):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = {"timestamp": timestamp, "level": level, "message": message}
        self._log_entries.append(entry)
        
        # 颜色映射
        colors = {
            "INFO": "#e0e0e0",
            "WARNING": "#ffaa00",
            "ERROR": "#ff4444",
            "DEBUG": "#888888"
        }
        color = colors.get(level, "#e0e0e0")
        
        html = f'<span style="color:#666">[{timestamp}]</span> '
        html += f'<span style="color:{color}">[{level}]</span> '
        html += f'<span style="color:{color}">{message}</span><br>'
        
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
        self.log_text.insertHtml(html)
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)
    
    def _filter_logs(self):
        """筛选日志"""
        level_filter = self.log_level_combo.currentText()
        search_text = self.log_search.text().lower()
        
        self.log_text.clear()
        
        for entry in self._log_entries:
            if level_filter != "ALL" and entry["level"] != level_filter:
                continue
            if search_text and search_text not in entry["message"].lower():
                continue
            
            self._log(entry["level"], entry["message"])
    
    def _clear_logs(self):
        """清除日志"""
        self._log_entries.clear()
        self.log_text.clear()
    
    def _add_task_to_table(self, task_id: str):
        """添加任务到表格"""
        task = self._tasks.get(task_id)
        if not task:
            return
        
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        
        self.task_table.setItem(row, 0, QTableWidgetItem(task_id))
        self.task_table.setItem(row, 1, QTableWidgetItem(task["engine"]))
        self.task_table.setItem(row, 2, QTableWidgetItem(task["strategy"]))
        self.task_table.setItem(row, 3, QTableWidgetItem(task["status"]))
        self.task_table.setItem(row, 4, QTableWidgetItem(f"{task['progress']}%"))
        self.task_table.setItem(row, 5, QTableWidgetItem(
            task["started_at"].strftime("%H:%M:%S")
        ))
    
    def _update_task_table(self):
        """更新任务表格"""
        for row in range(self.task_table.rowCount()):
            task_id = self.task_table.item(row, 0).text()
            task = self._tasks.get(task_id)
            if task:
                self.task_table.item(row, 3).setText(task["status"])
                self.task_table.item(row, 4).setText(f"{task['progress']}%")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = BacktestProgressPanel()
    panel.setWindowTitle("回测进度")
    panel.resize(800, 600)
    panel.show()
    sys.exit(app.exec())
