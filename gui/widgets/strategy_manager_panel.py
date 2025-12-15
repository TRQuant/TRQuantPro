# -*- coding: utf-8 -*-
"""
策略管理面板
============

管理策略库、策略版本、策略性能追踪

功能:
- 策略库浏览
- 策略详情查看
- 策略对比
- 策略版本管理
- 性能追踪
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTreeWidget, QTreeWidgetItem, QTabWidget,
    QSplitter, QTextEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QLineEdit, QComboBox,
    QMenu, QMessageBox, QDialog, QFormLayout, QSpinBox,
    QDoubleSpinBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os

logger = logging.getLogger(__name__)


class StrategyConfigDialog(QDialog):
    """策略配置对话框"""
    
    def __init__(self, strategy_info: Dict, parent=None):
        super().__init__(parent)
        self.strategy_info = strategy_info
        self.setWindowTitle(f"策略配置 - {strategy_info.get('name', '')}")
        self.setMinimumSize(500, 400)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # 策略名称
        self.name_edit = QLineEdit(self.strategy_info.get("name", ""))
        form.addRow("策略名称:", self.name_edit)
        
        # 策略类型
        self.type_combo = QComboBox()
        self.type_combo.addItems(["动量", "价值", "趋势", "多因子", "其他"])
        form.addRow("策略类型:", self.type_combo)
        
        # 初始资金
        self.capital_spin = QDoubleSpinBox()
        self.capital_spin.setRange(10000, 100000000)
        self.capital_spin.setValue(self.strategy_info.get("initial_capital", 1000000))
        self.capital_spin.setDecimals(0)
        form.addRow("初始资金:", self.capital_spin)
        
        # 最大持仓数
        self.max_positions = QSpinBox()
        self.max_positions.setRange(1, 100)
        self.max_positions.setValue(self.strategy_info.get("max_positions", 10))
        form.addRow("最大持仓数:", self.max_positions)
        
        # 单票最大仓位
        self.max_weight = QDoubleSpinBox()
        self.max_weight.setRange(0.01, 1.0)
        self.max_weight.setValue(self.strategy_info.get("max_weight", 0.1))
        self.max_weight.setDecimals(2)
        self.max_weight.setSingleStep(0.05)
        form.addRow("单票最大仓位:", self.max_weight)
        
        # 止损线
        self.stop_loss = QDoubleSpinBox()
        self.stop_loss.setRange(0.01, 0.5)
        self.stop_loss.setValue(self.strategy_info.get("stop_loss", 0.08))
        self.stop_loss.setDecimals(2)
        form.addRow("止损线:", self.stop_loss)
        
        # 止盈线
        self.take_profit = QDoubleSpinBox()
        self.take_profit.setRange(0.05, 1.0)
        self.take_profit.setValue(self.strategy_info.get("take_profit", 0.2))
        self.take_profit.setDecimals(2)
        form.addRow("止盈线:", self.take_profit)
        
        layout.addLayout(form)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("保存")
        save_btn.clicked.connect(self.accept)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def get_config(self) -> Dict:
        """获取配置"""
        return {
            "name": self.name_edit.text(),
            "initial_capital": self.capital_spin.value(),
            "max_positions": self.max_positions.value(),
            "max_weight": self.max_weight.value(),
            "stop_loss": self.stop_loss.value(),
            "take_profit": self.take_profit.value()
        }


class StrategyManagerPanel(QWidget):
    """策略管理面板"""
    
    strategy_selected = pyqtSignal(dict)  # 策略信息
    backtest_requested = pyqtSignal(dict)  # 回测请求
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._strategies: Dict[str, Dict] = {}
        self._current_strategy: Optional[Dict] = None
        
        self._init_ui()
        self._load_strategies()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # === 顶部工具栏 ===
        toolbar = QHBoxLayout()
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索策略...")
        self.search_edit.textChanged.connect(self._filter_strategies)
        toolbar.addWidget(self.search_edit)
        
        # 平台筛选
        toolbar.addWidget(QLabel("平台:"))
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["全部", "BulletTrade", "PTrade", "QMT"])
        self.platform_combo.currentTextChanged.connect(self._filter_strategies)
        toolbar.addWidget(self.platform_combo)
        
        toolbar.addStretch()
        
        # 操作按钮
        new_btn = QPushButton("+ 新建策略")
        new_btn.clicked.connect(self._create_strategy)
        toolbar.addWidget(new_btn)
        
        import_btn = QPushButton("📂 导入")
        import_btn.clicked.connect(self._import_strategy)
        toolbar.addWidget(import_btn)
        
        layout.addLayout(toolbar)
        
        # === 主内容区 ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # --- 左侧：策略树 ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.strategy_tree = QTreeWidget()
        self.strategy_tree.setHeaderLabels(["策略名称", "平台", "状态"])
        self.strategy_tree.setColumnWidth(0, 200)
        self.strategy_tree.itemClicked.connect(self._on_strategy_selected)
        self.strategy_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.strategy_tree.customContextMenuRequested.connect(self._show_context_menu)
        left_layout.addWidget(self.strategy_tree)
        
        splitter.addWidget(left_panel)
        
        # --- 右侧：策略详情 ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 策略信息卡片
        info_group = QGroupBox("策略信息")
        info_layout = QVBoxLayout(info_group)
        
        self.strategy_name_label = QLabel("请选择策略")
        self.strategy_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(self.strategy_name_label)
        
        info_grid = QHBoxLayout()
        self.info_labels = {}
        for key, title in [("platform", "平台"), ("type", "类型"), ("version", "版本"), ("updated", "更新时间")]:
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
            self.info_labels[key] = value_label
        
        info_layout.addLayout(info_grid)
        right_layout.addWidget(info_group)
        
        # 详情标签页
        detail_tabs = QTabWidget()
        
        # Tab1: 代码
        code_tab = QWidget()
        code_layout = QVBoxLayout(code_tab)
        
        self.code_edit = QTextEdit()
        self.code_edit.setReadOnly(True)
        self.code_edit.setStyleSheet("""
            QTextEdit {
                background: #1e1e2e;
                color: #e0e0e0;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border: 1px solid #404050;
            }
        """)
        code_layout.addWidget(self.code_edit)
        
        detail_tabs.addTab(code_tab, "📄 代码")
        
        # Tab2: 参数
        params_tab = QWidget()
        params_layout = QVBoxLayout(params_tab)
        
        self.params_table = QTableWidget()
        self.params_table.setColumnCount(4)
        self.params_table.setHorizontalHeaderLabels(["参数", "值", "类型", "说明"])
        self.params_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        params_layout.addWidget(self.params_table)
        
        detail_tabs.addTab(params_tab, "⚙️ 参数")
        
        # Tab3: 性能
        perf_tab = QWidget()
        perf_layout = QVBoxLayout(perf_tab)
        
        self.perf_table = QTableWidget()
        self.perf_table.setColumnCount(6)
        self.perf_table.setHorizontalHeaderLabels([
            "回测日期", "时间范围", "总收益", "夏普", "最大回撤", "状态"
        ])
        self.perf_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        perf_layout.addWidget(self.perf_table)
        
        detail_tabs.addTab(perf_tab, "📊 性能")
        
        # Tab4: 版本
        version_tab = QWidget()
        version_layout = QVBoxLayout(version_tab)
        
        self.version_table = QTableWidget()
        self.version_table.setColumnCount(4)
        self.version_table.setHorizontalHeaderLabels(["版本", "更新时间", "说明", "操作"])
        self.version_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        version_layout.addWidget(self.version_table)
        
        detail_tabs.addTab(version_tab, "📦 版本")
        
        right_layout.addWidget(detail_tabs)
        
        # 操作按钮
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        self.edit_btn = QPushButton("✏️ 编辑")
        self.edit_btn.clicked.connect(self._edit_strategy)
        self.edit_btn.setEnabled(False)
        action_layout.addWidget(self.edit_btn)
        
        self.config_btn = QPushButton("⚙️ 配置")
        self.config_btn.clicked.connect(self._config_strategy)
        self.config_btn.setEnabled(False)
        action_layout.addWidget(self.config_btn)
        
        self.backtest_btn = QPushButton("▶ 回测")
        self.backtest_btn.clicked.connect(self._run_backtest)
        self.backtest_btn.setEnabled(False)
        action_layout.addWidget(self.backtest_btn)
        
        self.export_btn = QPushButton("📤 导出")
        self.export_btn.clicked.connect(self._export_strategy)
        self.export_btn.setEnabled(False)
        action_layout.addWidget(self.export_btn)
        
        right_layout.addLayout(action_layout)
        
        splitter.addWidget(right_panel)
        
        # 设置分割比例
        splitter.setSizes([300, 600])
        
        layout.addWidget(splitter)
    
    def _load_strategies(self):
        """加载策略库"""
        strategies_dir = Path(__file__).parent.parent.parent / "strategies"
        
        # 扫描策略目录
        platforms = {
            "bullettrade": "BulletTrade",
            "ptrade": "PTrade",
            "qmt": "QMT",
            "unified": "Unified"
        }
        
        for folder, platform in platforms.items():
            folder_path = strategies_dir / folder
            if folder_path.exists():
                parent_item = QTreeWidgetItem(self.strategy_tree)
                parent_item.setText(0, f"📁 {platform}")
                parent_item.setExpanded(True)
                
                for file in folder_path.glob("*.py"):
                    if file.name.startswith("__"):
                        continue
                    
                    strategy_id = f"{folder}/{file.stem}"
                    strategy_info = {
                        "id": strategy_id,
                        "name": file.stem,
                        "platform": platform,
                        "path": str(file),
                        "type": "动量" if "momentum" in file.name.lower() else "其他",
                        "version": "1.0.0",
                        "updated": file.stat().st_mtime
                    }
                    self._strategies[strategy_id] = strategy_info
                    
                    item = QTreeWidgetItem(parent_item)
                    item.setText(0, file.stem)
                    item.setText(1, platform)
                    item.setText(2, "✅")
                    item.setData(0, Qt.ItemDataRole.UserRole, strategy_id)
        
        logger.info(f"已加载 {len(self._strategies)} 个策略")
    
    def _filter_strategies(self):
        """筛选策略"""
        search_text = self.search_edit.text().lower()
        platform_filter = self.platform_combo.currentText()
        
        for i in range(self.strategy_tree.topLevelItemCount()):
            parent = self.strategy_tree.topLevelItem(i)
            parent_visible = False
            
            for j in range(parent.childCount()):
                child = parent.child(j)
                strategy_id = child.data(0, Qt.ItemDataRole.UserRole)
                strategy = self._strategies.get(strategy_id, {})
                
                name_match = search_text in strategy.get("name", "").lower()
                platform_match = (platform_filter == "全部" or 
                                  strategy.get("platform") == platform_filter)
                
                visible = name_match and platform_match
                child.setHidden(not visible)
                if visible:
                    parent_visible = True
            
            parent.setHidden(not parent_visible)
    
    def _on_strategy_selected(self, item: QTreeWidgetItem, column: int):
        """策略选中"""
        strategy_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not strategy_id:
            return
        
        strategy = self._strategies.get(strategy_id)
        if not strategy:
            return
        
        self._current_strategy = strategy
        
        # 更新UI
        self.strategy_name_label.setText(strategy["name"])
        self.info_labels["platform"].setText(strategy.get("platform", "--"))
        self.info_labels["type"].setText(strategy.get("type", "--"))
        self.info_labels["version"].setText(strategy.get("version", "--"))
        
        from datetime import datetime
        updated = strategy.get("updated")
        if updated:
            self.info_labels["updated"].setText(
                datetime.fromtimestamp(updated).strftime("%Y-%m-%d")
            )
        
        # 加载代码
        path = strategy.get("path")
        if path and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            self.code_edit.setPlainText(code)
        
        # 启用按钮
        self.edit_btn.setEnabled(True)
        self.config_btn.setEnabled(True)
        self.backtest_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        
        self.strategy_selected.emit(strategy)
    
    def _show_context_menu(self, pos):
        """显示右键菜单"""
        item = self.strategy_tree.itemAt(pos)
        if not item:
            return
        
        strategy_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not strategy_id:
            return
        
        menu = QMenu(self)
        
        edit_action = QAction("✏️ 编辑", self)
        edit_action.triggered.connect(self._edit_strategy)
        menu.addAction(edit_action)
        
        backtest_action = QAction("▶ 回测", self)
        backtest_action.triggered.connect(self._run_backtest)
        menu.addAction(backtest_action)
        
        menu.addSeparator()
        
        delete_action = QAction("🗑️ 删除", self)
        delete_action.triggered.connect(self._delete_strategy)
        menu.addAction(delete_action)
        
        menu.exec(self.strategy_tree.mapToGlobal(pos))
    
    def _create_strategy(self):
        """创建新策略"""
        QMessageBox.information(self, "创建策略", "功能开发中...")
    
    def _import_strategy(self):
        """导入策略"""
        QMessageBox.information(self, "导入策略", "功能开发中...")
    
    def _edit_strategy(self):
        """编辑策略"""
        if self._current_strategy:
            path = self._current_strategy.get("path")
            if path:
                os.system(f"code {path}")  # 用VSCode打开
    
    def _config_strategy(self):
        """配置策略"""
        if self._current_strategy:
            dialog = StrategyConfigDialog(self._current_strategy, self)
            if dialog.exec():
                config = dialog.get_config()
                self._current_strategy.update(config)
                logger.info(f"策略配置已更新: {config}")
    
    def _run_backtest(self):
        """运行回测"""
        if self._current_strategy:
            self.backtest_requested.emit(self._current_strategy)
    
    def _export_strategy(self):
        """导出策略"""
        QMessageBox.information(self, "导出策略", "功能开发中...")
    
    def _delete_strategy(self):
        """删除策略"""
        if self._current_strategy:
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除策略 '{self._current_strategy['name']}' 吗？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                logger.info(f"删除策略: {self._current_strategy['name']}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = StrategyManagerPanel()
    panel.setWindowTitle("策略管理")
    panel.resize(1000, 700)
    panel.show()
    sys.exit(app.exec())
