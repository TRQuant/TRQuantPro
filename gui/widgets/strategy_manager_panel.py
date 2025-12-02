# -*- coding: utf-8 -*-
"""
A股策略管理模块
===============

统一管理所有策略相关数据：
- 策略代码（Python/PTrade）
- 策略配置和参数
- 回测历史记录
- 策略绩效跟踪
- 实盘运行状态
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QTextBrowser, QSplitter, QMessageBox, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QDialog, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QFormLayout, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices, QFont, QColor
from pathlib import Path
from datetime import datetime
import json
import shutil
import logging

from gui.styles.theme import Colors, ButtonStyles
from gui.widgets.module_banner import ModuleBanner

logger = logging.getLogger(__name__)


class StrategyManagerPanel(QWidget):
    """A股策略管理面板"""
    
    run_backtest = pyqtSignal(str, dict)  # 运行回测信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._strategies = []
        self._init_ui()
        QTimer.singleShot(100, self._load_all_data)
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner
        banner = ModuleBanner(
            title="📋 A股策略管理中心",
            subtitle="统一管理策略代码、回测历史、绩效跟踪",
            gradient_colors=("#8B5CF6", "#6366F1")
        )
        layout.addWidget(banner)
        
        # 内容区域 - 可滚动
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {Colors.BG_PRIMARY}; }}")
        
        content = QWidget()
        content.setStyleSheet(f"background: {Colors.BG_PRIMARY};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(16)
        
        # 统计卡片
        stats_layout = QHBoxLayout()
        self.strategy_count_card = self._create_stat_card("🐍", "策略总数", "0", Colors.PRIMARY)
        self.backtest_count_card = self._create_stat_card("🔄", "回测次数", "0", Colors.INFO)
        self.best_return_card = self._create_stat_card("📈", "最佳收益", "0%", Colors.SUCCESS)
        self.live_count_card = self._create_stat_card("🚀", "实盘运行", "0", Colors.WARNING)
        
        stats_layout.addWidget(self.strategy_count_card)
        stats_layout.addWidget(self.backtest_count_card)
        stats_layout.addWidget(self.best_return_card)
        stats_layout.addWidget(self.live_count_card)
        content_layout.addLayout(stats_layout)
        
        # 主Tab页
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                background: {Colors.BG_SECONDARY};
            }}
            QTabBar::tab {{
                background: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                padding: 12px 24px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
                font-size: 13px;
            }}
            QTabBar::tab:selected {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                font-weight: bold;
            }}
        """)
        
        # 策略库Tab
        tabs.addTab(self._create_strategy_library_tab(), "📚 策略库")
        
        # 回测历史Tab
        tabs.addTab(self._create_backtest_history_tab(), "📊 回测历史")
        
        # 绩效跟踪Tab
        tabs.addTab(self._create_performance_tab(), "📈 绩效跟踪")
        
        # 文档管理Tab
        tabs.addTab(self._create_docs_tab(), "📄 策略文档")
        
        content_layout.addWidget(tabs, 1)
        
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)
    
    def _create_stat_card(self, icon: str, label: str, value: str, color: str) -> QFrame:
        """创建统计卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-left: 4px solid {color};
                border-radius: 12px;
                padding: 16px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(8)
        
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header.addWidget(icon_label)
        
        title = QLabel(label)
        title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card
    
    def _create_strategy_library_tab(self) -> QWidget:
        """策略库Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setStyleSheet(ButtonStyles.SECONDARY)
        refresh_btn.clicked.connect(self._refresh_strategies)
        toolbar.addWidget(refresh_btn)
        
        new_btn = QPushButton("➕ 新建策略")
        new_btn.setStyleSheet(ButtonStyles.PRIMARY)
        new_btn.clicked.connect(self._create_new_strategy)
        toolbar.addWidget(new_btn)
        
        import_btn = QPushButton("📥 导入策略")
        import_btn.setStyleSheet(ButtonStyles.SECONDARY)
        import_btn.clicked.connect(self._import_strategy)
        toolbar.addWidget(import_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 策略列表
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.strategy_tree = QTreeWidget()
        self.strategy_tree.setHeaderLabels(["策略名称", "类型", "状态", "更新时间"])
        self.strategy_tree.setStyleSheet(f"""
            QTreeWidget {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QTreeWidget::item {{ padding: 6px; }}
            QTreeWidget::item:hover {{ background: {Colors.BG_HOVER}; }}
            QTreeWidget::item:selected {{ background: {Colors.PRIMARY}; }}
            QHeaderView::section {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                padding: 10px;
                border: none;
            }}
        """)
        self.strategy_tree.itemClicked.connect(self._on_strategy_selected)
        left_layout.addWidget(self.strategy_tree)
        
        splitter.addWidget(left_frame)
        
        # 右侧详情
        right_frame = QFrame()
        right_frame.setStyleSheet(f"""
            QFrame {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(16, 16, 16, 16)
        
        # 策略信息
        self.strategy_info = QLabel("选择左侧策略查看详情")
        self.strategy_info.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 14px;")
        self.strategy_info.setWordWrap(True)
        right_layout.addWidget(self.strategy_info)
        
        # 代码预览
        self.code_preview = QTextBrowser()
        self.code_preview.setStyleSheet(f"""
            QTextBrowser {{
                background: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                color: {Colors.TEXT_PRIMARY};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }}
        """)
        right_layout.addWidget(self.code_preview, 1)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        edit_btn = QPushButton("✏️ 编辑")
        edit_btn.setStyleSheet(ButtonStyles.SECONDARY)
        edit_btn.clicked.connect(self._edit_strategy)
        btn_layout.addWidget(edit_btn)
        
        backtest_btn = QPushButton("🔄 回测")
        backtest_btn.setStyleSheet(ButtonStyles.PRIMARY)
        backtest_btn.clicked.connect(self._run_backtest)
        btn_layout.addWidget(backtest_btn)
        
        export_btn = QPushButton("📤 导出")
        export_btn.setStyleSheet(ButtonStyles.SECONDARY)
        export_btn.clicked.connect(self._export_strategy)
        btn_layout.addWidget(export_btn)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.setStyleSheet(ButtonStyles.DANGER)
        delete_btn.clicked.connect(self._delete_strategy)
        btn_layout.addWidget(delete_btn)
        
        right_layout.addLayout(btn_layout)
        
        splitter.addWidget(right_frame)
        splitter.setSizes([350, 550])
        
        layout.addWidget(splitter, 1)
        
        return widget
    
    def _create_backtest_history_tab(self) -> QWidget:
        """回测历史Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setStyleSheet(ButtonStyles.SECONDARY)
        refresh_btn.clicked.connect(self._refresh_backtests)
        toolbar.addWidget(refresh_btn)
        
        clear_btn = QPushButton("🗑️ 清理旧记录")
        clear_btn.setStyleSheet(ButtonStyles.DANGER)
        clear_btn.clicked.connect(self._clear_old_backtests)
        toolbar.addWidget(clear_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 回测历史表格
        self.backtest_table = QTableWidget()
        self.backtest_table.setColumnCount(7)
        self.backtest_table.setHorizontalHeaderLabels([
            "策略名称", "回测时间", "收益率", "夏普比率", "最大回撤", "胜率", "状态"
        ])
        self.backtest_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.backtest_table.setStyleSheet(f"""
            QTableWidget {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{ padding: 8px; }}
            QHeaderView::section {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                padding: 10px;
                border: none;
                font-weight: bold;
            }}
        """)
        self.backtest_table.itemDoubleClicked.connect(self._view_backtest_detail)
        layout.addWidget(self.backtest_table, 1)
        
        return widget
    
    def _create_performance_tab(self) -> QWidget:
        """绩效跟踪Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 说明
        info = QLabel("""
<h3 style="color:#8B5CF6;">📈 策略绩效跟踪</h3>
<p style="color:#9CA3AF;">跟踪策略的历史绩效表现，包括：</p>
<ul style="color:#D1D5DB;">
    <li>各策略的累计收益曲线</li>
    <li>关键绩效指标对比（夏普、最大回撤、胜率等）</li>
    <li>策略排名和评分</li>
</ul>
<p style="color:#6B7280; margin-top:20px;">
    <i>提示：运行回测后，绩效数据会自动更新到此处。</i>
</p>
        """)
        info.setStyleSheet(f"background: {Colors.BG_TERTIARY}; border-radius: 12px; padding: 20px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # 绩效表格
        self.performance_table = QTableWidget()
        self.performance_table.setColumnCount(6)
        self.performance_table.setHorizontalHeaderLabels([
            "策略名称", "回测次数", "平均收益", "最佳收益", "平均夏普", "评分"
        ])
        self.performance_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.performance_table.setStyleSheet(f"""
            QTableWidget {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                padding: 10px;
                border: none;
            }}
        """)
        layout.addWidget(self.performance_table, 1)
        
        return widget
    
    def _create_docs_tab(self) -> QWidget:
        """策略文档Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 刷新")
        refresh_btn.setStyleSheet(ButtonStyles.SECONDARY)
        refresh_btn.clicked.connect(self._refresh_docs)
        toolbar.addWidget(refresh_btn)
        
        open_folder_btn = QPushButton("📂 打开文档目录")
        open_folder_btn.setStyleSheet(ButtonStyles.SECONDARY)
        open_folder_btn.clicked.connect(self._open_docs_folder)
        toolbar.addWidget(open_folder_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 文档列表
        self.docs_tree = QTreeWidget()
        self.docs_tree.setHeaderLabels(["文档名称", "类型", "大小", "更新时间"])
        self.docs_tree.setStyleSheet(f"""
            QTreeWidget {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.docs_tree.itemDoubleClicked.connect(self._open_doc)
        layout.addWidget(self.docs_tree, 1)
        
        return widget
    
    def _load_all_data(self):
        """加载所有数据"""
        self._refresh_strategies()
        self._refresh_backtests()
        self._refresh_performance()
        self._refresh_docs()
    
    def _refresh_strategies(self):
        """刷新策略列表"""
        self.strategy_tree.clear()
        self._strategies = []
        
        base_dir = Path(__file__).parent.parent.parent
        strategies_dir = base_dir / "strategies" / "ptrade"
        
        if not strategies_dir.exists():
            strategies_dir.mkdir(parents=True, exist_ok=True)
            return
        
        # 按类型分组
        groups = {
            "生成策略": [],
            "多因子策略": [],
            "动量策略": [],
            "其他": []
        }
        
        for f in sorted(strategies_dir.glob("*.py"), reverse=True):
            if f.name.endswith("_meta.json"):
                continue
            
            name = f.stem
            mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')
            
            # 读取元数据
            meta_file = f.with_suffix('.py').with_name(f.stem + "_meta.json")
            meta = {}
            if meta_file.exists():
                try:
                    with open(meta_file, 'r', encoding='utf-8') as mf:
                        meta = json.load(mf)
                except:
                    pass
            
            strategy_type = meta.get("type", "other")
            status = meta.get("status", "未测试")
            
            strategy_data = {
                "name": name,
                "path": str(f),
                "meta_path": str(meta_file),
                "type": strategy_type,
                "status": status,
                "mtime": mtime,
                "meta": meta
            }
            self._strategies.append(strategy_data)
            
            # 分类
            if "generated" in name or "strategy_2" in name:
                groups["生成策略"].append(strategy_data)
            elif "multi_factor" in name:
                groups["多因子策略"].append(strategy_data)
            elif "momentum" in name:
                groups["动量策略"].append(strategy_data)
            else:
                groups["其他"].append(strategy_data)
        
        # 添加到树
        for group_name, strategies in groups.items():
            if strategies:
                group_item = QTreeWidgetItem([f"📁 {group_name}", "", "", ""])
                group_item.setExpanded(True)
                
                for s in strategies:
                    item = QTreeWidgetItem([
                        s["name"],
                        s["type"],
                        s["status"],
                        s["mtime"]
                    ])
                    item.setData(0, Qt.ItemDataRole.UserRole, s)
                    
                    # 状态颜色
                    if s["status"] == "已验证":
                        item.setForeground(2, QColor(Colors.SUCCESS))
                    elif s["status"] == "测试中":
                        item.setForeground(2, QColor(Colors.WARNING))
                    
                    group_item.addChild(item)
                
                self.strategy_tree.addTopLevelItem(group_item)
        
        # 更新统计
        self.strategy_count_card.findChild(QLabel, "value").setText(str(len(self._strategies)))
    
    def _refresh_backtests(self):
        """刷新回测历史"""
        self.backtest_table.setRowCount(0)
        
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
            db = client['trquant']
            
            backtests = list(db.backtest_results.find().sort("timestamp", -1).limit(50))
            self.backtest_table.setRowCount(len(backtests))
            
            for i, bt in enumerate(backtests):
                self.backtest_table.setItem(i, 0, QTableWidgetItem(bt.get("strategy_name", "-")))
                
                timestamp = bt.get("timestamp", "")
                if hasattr(timestamp, 'strftime'):
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M')
                self.backtest_table.setItem(i, 1, QTableWidgetItem(str(timestamp)[:16]))
                
                returns = bt.get("total_return", 0)
                item = QTableWidgetItem(f"{returns:.2f}%")
                item.setForeground(QColor(Colors.SUCCESS if returns > 0 else Colors.DANGER))
                self.backtest_table.setItem(i, 2, item)
                
                self.backtest_table.setItem(i, 3, QTableWidgetItem(f"{bt.get('sharpe_ratio', 0):.2f}"))
                self.backtest_table.setItem(i, 4, QTableWidgetItem(f"{bt.get('max_drawdown', 0):.2f}%"))
                self.backtest_table.setItem(i, 5, QTableWidgetItem(f"{bt.get('win_rate', 0):.1f}%"))
                self.backtest_table.setItem(i, 6, QTableWidgetItem(bt.get("status", "完成")))
            
            # 更新统计
            self.backtest_count_card.findChild(QLabel, "value").setText(str(len(backtests)))
            
            if backtests:
                best_return = max(bt.get("total_return", 0) for bt in backtests)
                self.best_return_card.findChild(QLabel, "value").setText(f"{best_return:.1f}%")
            
        except Exception as e:
            logger.warning(f"刷新回测历史失败: {e}")
    
    def _refresh_performance(self):
        """刷新绩效数据"""
        self.performance_table.setRowCount(0)
        
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
            db = client['trquant']
            
            # 聚合每个策略的绩效
            pipeline = [
                {"$group": {
                    "_id": "$strategy_name",
                    "count": {"$sum": 1},
                    "avg_return": {"$avg": "$total_return"},
                    "max_return": {"$max": "$total_return"},
                    "avg_sharpe": {"$avg": "$sharpe_ratio"}
                }},
                {"$sort": {"max_return": -1}}
            ]
            
            results = list(db.backtest_results.aggregate(pipeline))
            self.performance_table.setRowCount(len(results))
            
            for i, r in enumerate(results):
                self.performance_table.setItem(i, 0, QTableWidgetItem(r.get("_id", "-")))
                self.performance_table.setItem(i, 1, QTableWidgetItem(str(r.get("count", 0))))
                self.performance_table.setItem(i, 2, QTableWidgetItem(f"{r.get('avg_return', 0):.2f}%"))
                self.performance_table.setItem(i, 3, QTableWidgetItem(f"{r.get('max_return', 0):.2f}%"))
                self.performance_table.setItem(i, 4, QTableWidgetItem(f"{r.get('avg_sharpe', 0):.2f}"))
                
                # 评分
                score = min(100, max(0, 50 + r.get('avg_return', 0) * 2 + r.get('avg_sharpe', 0) * 10))
                self.performance_table.setItem(i, 5, QTableWidgetItem(f"{score:.0f}"))
                
        except Exception as e:
            logger.warning(f"刷新绩效数据失败: {e}")
    
    def _refresh_docs(self):
        """刷新文档列表"""
        self.docs_tree.clear()
        
        base_dir = Path(__file__).parent.parent.parent
        
        # 文档目录
        doc_dirs = [
            ("📊 报告", base_dir / "reports"),
            ("📄 文档", base_dir / "docs"),
            ("📝 策略说明", base_dir / "strategies" / "docs"),
        ]
        
        for dir_name, dir_path in doc_dirs:
            if not dir_path.exists():
                continue
            
            group_item = QTreeWidgetItem([dir_name, "", "", ""])
            group_item.setExpanded(True)
            
            for f in sorted(dir_path.rglob("*"), reverse=True):
                if f.is_file() and f.suffix in ['.html', '.md', '.pdf', '.json']:
                    rel_path = f.relative_to(dir_path)
                    size = f"{f.stat().st_size / 1024:.1f} KB"
                    mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')
                    
                    item = QTreeWidgetItem([str(rel_path), f.suffix.upper(), size, mtime])
                    item.setData(0, Qt.ItemDataRole.UserRole, str(f))
                    group_item.addChild(item)
            
            if group_item.childCount() > 0:
                self.docs_tree.addTopLevelItem(group_item)
    
    def _on_strategy_selected(self, item, col):
        """选择策略"""
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        # 显示策略信息
        info_html = f"""
<h3 style="color:{Colors.PRIMARY};">{data['name']}</h3>
<p><b>类型:</b> {data.get('type', '未知')}</p>
<p><b>状态:</b> <span style="color:{Colors.SUCCESS if data.get('status') == '已验证' else Colors.WARNING};">{data.get('status', '未测试')}</span></p>
<p><b>更新时间:</b> {data.get('mtime', '-')}</p>
        """
        
        if data.get('meta'):
            meta = data['meta']
            if meta.get('description'):
                info_html += f"<p><b>描述:</b> {meta['description']}</p>"
            if meta.get('factors'):
                info_html += f"<p><b>因子:</b> {', '.join(meta['factors'])}</p>"
        
        self.strategy_info.setText(info_html)
        
        # 显示代码
        try:
            with open(data['path'], 'r', encoding='utf-8') as f:
                code = f.read()
            self.code_preview.setPlainText(code)
        except Exception as e:
            self.code_preview.setPlainText(f"读取失败: {e}")
    
    def _create_new_strategy(self):
        """创建新策略"""
        from core.workflow_orchestrator import get_workflow_orchestrator
        
        reply = QMessageBox.question(
            self, "创建新策略",
            "是否基于当前工作流结果创建新策略？\n\n"
            "这将使用最新的市场趋势、投资主线和因子推荐来生成策略代码。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            orchestrator = get_workflow_orchestrator()
            result = orchestrator.generate_strategy()
            
            if result.success:
                QMessageBox.information(
                    self, "成功",
                    f"策略已生成:\n{result.details.get('strategy_file', '')}"
                )
                self._refresh_strategies()
            else:
                QMessageBox.warning(self, "失败", result.summary)
    
    def _import_strategy(self):
        """导入策略"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择策略文件", "", "Python文件 (*.py)"
        )
        
        if file_path:
            dest_dir = Path(__file__).parent.parent.parent / "strategies" / "ptrade"
            dest_file = dest_dir / Path(file_path).name
            
            shutil.copy(file_path, dest_file)
            QMessageBox.information(self, "成功", f"策略已导入:\n{dest_file}")
            self._refresh_strategies()
    
    def _edit_strategy(self):
        """编辑策略"""
        selected = self.strategy_tree.currentItem()
        if not selected:
            return
        
        data = selected.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        QDesktopServices.openUrl(QUrl.fromLocalFile(data['path']))
    
    def _run_backtest(self):
        """运行回测"""
        selected = self.strategy_tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "提示", "请先选择要回测的策略")
            return
        
        data = selected.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        self.run_backtest.emit(data['path'], {})
        QMessageBox.information(self, "提示", "请切换到回测验证页面查看结果")
    
    def _export_strategy(self):
        """导出策略"""
        selected = self.strategy_tree.currentItem()
        if not selected:
            return
        
        data = selected.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        dest, _ = QFileDialog.getSaveFileName(
            self, "导出策略", data['name'] + ".py", "Python文件 (*.py)"
        )
        
        if dest:
            shutil.copy(data['path'], dest)
            QMessageBox.information(self, "成功", f"策略已导出到:\n{dest}")
    
    def _delete_strategy(self):
        """删除策略"""
        selected = self.strategy_tree.currentItem()
        if not selected:
            return
        
        data = selected.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除策略 '{data['name']}' 吗？\n此操作不可恢复！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            Path(data['path']).unlink()
            meta_path = Path(data['meta_path'])
            if meta_path.exists():
                meta_path.unlink()
            
            QMessageBox.information(self, "成功", "策略已删除")
            self._refresh_strategies()
    
    def _view_backtest_detail(self, item):
        """查看回测详情"""
        row = item.row()
        strategy_name = self.backtest_table.item(row, 0).text()
        QMessageBox.information(self, "回测详情", f"策略: {strategy_name}\n\n详细结果请查看回测验证页面")
    
    def _clear_old_backtests(self):
        """清理旧回测记录"""
        reply = QMessageBox.question(
            self, "确认", "确定要删除30天前的回测记录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from pymongo import MongoClient
                from datetime import timedelta
                
                client = MongoClient('localhost', 27017)
                db = client['trquant']
                
                threshold = datetime.now() - timedelta(days=30)
                result = db.backtest_results.delete_many({"timestamp": {"$lt": threshold}})
                
                QMessageBox.information(self, "完成", f"已删除 {result.deleted_count} 条旧记录")
                self._refresh_backtests()
            except Exception as e:
                QMessageBox.warning(self, "失败", str(e))
    
    def _open_docs_folder(self):
        """打开文档目录"""
        docs_dir = Path(__file__).parent.parent.parent / "docs"
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(docs_dir)))
    
    def _open_doc(self, item, col):
        """打开文档"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and Path(path).exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    def update_backtest_result(self, strategy_name: str, result: dict):
        """更新回测结果（被回测模块调用）"""
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017)
            db = client['trquant']
            
            db.backtest_results.insert_one({
                "strategy_name": strategy_name,
                "timestamp": datetime.now(),
                "total_return": result.get("total_return", 0),
                "sharpe_ratio": result.get("sharpe_ratio", 0),
                "max_drawdown": result.get("max_drawdown", 0),
                "win_rate": result.get("win_rate", 0),
                "status": "完成",
                "params": result.get("params", {})
            })
            
            self._refresh_backtests()
            self._refresh_performance()
            
        except Exception as e:
            logger.error(f"保存回测结果失败: {e}")

