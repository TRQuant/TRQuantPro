# -*- coding: utf-8 -*-
"""
数据管理面板
============

整合现有的文件管理系统（Web仪表盘），并提供：
- 快速入口：打开Web文件管理系统
- 系统文件概览：智能分类显示所有数据
- A股策略管理：策略库、回测历史、绩效跟踪
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QTextBrowser, QSplitter, QMessageBox, QFileDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer, QProcess
from PyQt6.QtGui import QDesktopServices, QFont, QColor
from pathlib import Path
from datetime import datetime
import json
import shutil
import logging
import subprocess
import sys
import webbrowser

from gui.styles.theme import Colors, ButtonStyles
from gui.widgets.module_banner import ModuleBanner

logger = logging.getLogger(__name__)


class DataManagerPanel(QWidget):
    """数据管理面板 - 整合现有文件管理系统"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._dashboard_process = None
        self._init_ui()
        # 延迟加载数据
        QTimer.singleShot(200, self._load_all_data)
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Banner
        banner = ModuleBanner(
            icon="📁",
            title="数据管理中心",
            subtitle="策略代码、回测报告、研究文档统一管理",
            theme="info"
        )
        layout.addWidget(banner)
        
        # 可滚动内容区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background: {Colors.BG_PRIMARY}; }}")
        
        content = QWidget()
        content.setStyleSheet(f"background: {Colors.BG_PRIMARY};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)
        
        # ==================== 快速入口 ====================
        entry_frame = QFrame()
        entry_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {Colors.PRIMARY}22, stop:1 {Colors.ACCENT}22);
                border: 1px solid {Colors.PRIMARY}44;
                border-radius: 16px;
                padding: 20px;
            }}
        """)
        entry_layout = QVBoxLayout(entry_frame)
        
        entry_title = QLabel("🚀 快速入口 - 文件管理系统")
        entry_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        entry_layout.addWidget(entry_title)
        
        entry_desc = QLabel("打开Web仪表盘，全面管理策略代码、回测报告、研究文档、因子研究、交易日志等")
        entry_desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px; margin-bottom: 12px;")
        entry_layout.addWidget(entry_desc)
        
        btn_layout = QHBoxLayout()
        
        open_dashboard_btn = QPushButton("📂 打开文件管理系统")
        open_dashboard_btn.setStyleSheet(f"""
            QPushButton {{
                background: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 28px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background: #7c8ef2; }}
        """)
        open_dashboard_btn.clicked.connect(self._open_dashboard)
        btn_layout.addWidget(open_dashboard_btn)
        
        refresh_btn = QPushButton("🔄 刷新数据")
        refresh_btn.setStyleSheet(ButtonStyles.SECONDARY)
        refresh_btn.clicked.connect(self._load_all_data)
        btn_layout.addWidget(refresh_btn)
        
        btn_layout.addStretch()
        entry_layout.addLayout(btn_layout)
        
        content_layout.addWidget(entry_frame)
        
        # ==================== 统计卡片 ====================
        stats_layout = QHBoxLayout()
        self.strategy_card = self._create_stat_card("🐍", "策略文件", "0", Colors.PRIMARY)
        self.report_card = self._create_stat_card("📊", "回测报告", "0", Colors.SUCCESS)
        self.doc_card = self._create_stat_card("📄", "研究文档", "0", Colors.INFO)
        self.data_card = self._create_stat_card("🗄️", "数据文件", "0", Colors.WARNING)
        
        stats_layout.addWidget(self.strategy_card)
        stats_layout.addWidget(self.report_card)
        stats_layout.addWidget(self.doc_card)
        stats_layout.addWidget(self.data_card)
        content_layout.addLayout(stats_layout)
        
        # ==================== Tab页 ====================
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
                padding: 12px 20px;
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
        
        # 系统文件概览
        tabs.addTab(self._create_files_overview_tab(), "📂 系统文件概览")
        
        # A股策略管理
        tabs.addTab(self._create_strategy_tab(), "📋 A股策略管理")
        
        # 回测记录
        tabs.addTab(self._create_backtest_tab(), "📊 回测记录")
        
        # 数据库
        tabs.addTab(self._create_database_tab(), "🗄️ 数据库")
        
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
        layout.setSpacing(6)
        
        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 22px;")
        header.addWidget(icon_label)
        
        title = QLabel(label)
        title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet(f"color: {color}; font-size: 26px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card
    
    def _create_files_overview_tab(self) -> QWidget:
        """系统文件概览Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 文件树
        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabels(["名称", "类型", "数量/大小", "最后更新"])
        self.files_tree.setStyleSheet(f"""
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
        self.files_tree.itemDoubleClicked.connect(self._open_file_or_folder)
        layout.addWidget(self.files_tree, 1)
        
        return widget
    
    def _create_strategy_tab(self) -> QWidget:
        """A股策略管理Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        open_folder_btn = QPushButton("📂 打开策略目录")
        open_folder_btn.setStyleSheet(ButtonStyles.SECONDARY)
        open_folder_btn.clicked.connect(self._open_strategies_folder)
        toolbar.addWidget(open_folder_btn)
        
        new_btn = QPushButton("➕ 生成新策略")
        new_btn.setStyleSheet(ButtonStyles.PRIMARY)
        new_btn.clicked.connect(self._generate_new_strategy)
        toolbar.addWidget(new_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 策略列表
        self.strategy_tree = QTreeWidget()
        self.strategy_tree.setHeaderLabels(["策略名称", "类型", "更新时间"])
        self.strategy_tree.setStyleSheet(f"""
            QTreeWidget {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.strategy_tree.itemClicked.connect(self._preview_strategy)
        splitter.addWidget(self.strategy_tree)
        
        # 代码预览
        self.code_preview = QTextBrowser()
        self.code_preview.setStyleSheet(f"""
            QTextBrowser {{
                background: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
                padding: 10px;
            }}
        """)
        splitter.addWidget(self.code_preview)
        splitter.setSizes([300, 500])
        
        layout.addWidget(splitter, 1)
        
        return widget
    
    def _create_backtest_tab(self) -> QWidget:
        """回测记录Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 回测表格
        self.backtest_table = QTableWidget()
        self.backtest_table.setColumnCount(6)
        self.backtest_table.setHorizontalHeaderLabels([
            "策略名称", "回测时间", "收益率", "夏普比率", "最大回撤", "状态"
        ])
        self.backtest_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.backtest_table.setStyleSheet(f"""
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
        layout.addWidget(self.backtest_table, 1)
        
        return widget
    
    def _create_database_tab(self) -> QWidget:
        """数据库Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        export_btn = QPushButton("📤 导出数据")
        export_btn.setStyleSheet(ButtonStyles.PRIMARY)
        export_btn.clicked.connect(self._export_database)
        toolbar.addWidget(export_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 数据库表格
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(4)
        self.db_table.setHorizontalHeaderLabels(["集合名称", "文档数", "大小", "最后更新"])
        self.db_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.db_table.setStyleSheet(f"""
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
        layout.addWidget(self.db_table, 1)
        
        return widget
    
    def _load_all_data(self):
        """加载所有数据"""
        self._load_files_overview()
        self._load_strategies()
        self._load_backtests()
        self._load_database()
    
    def _load_files_overview(self):
        """加载文件概览"""
        self.files_tree.clear()
        
        base_dir = Path(__file__).parent.parent.parent
        
        # 定义目录分类
        categories = [
            ("🐍 策略代码", "strategies", [".py"], "strategy_count"),
            ("📊 回测报告", "reports", [".html", ".json", ".pdf"], "report_count"),
            ("📄 研究文档", "docs", [".md", ".pdf", ".html"], "doc_count"),
            ("🗄️ 数据文件", "data", [".csv", ".json", ".pkl"], "data_count"),
            ("⚙️ 配置文件", "config", [".json", ".yaml", ".ini"], None),
            ("📁 缓存", ".cache", ["*"], None),
        ]
        
        total_counts = {"strategy_count": 0, "report_count": 0, "doc_count": 0, "data_count": 0}
        
        for cat_name, dir_name, extensions, count_key in categories:
            dir_path = base_dir / dir_name
            if not dir_path.exists():
                continue
            
            # 统计文件
            files = []
            total_size = 0
            latest_mtime = None
            
            for ext in extensions:
                if ext == "*":
                    for f in dir_path.rglob("*"):
                        if f.is_file():
                            files.append(f)
                            total_size += f.stat().st_size
                            mtime = f.stat().st_mtime
                            if latest_mtime is None or mtime > latest_mtime:
                                latest_mtime = mtime
                else:
                    for f in dir_path.rglob(f"*{ext}"):
                        if f.is_file():
                            files.append(f)
                            total_size += f.stat().st_size
                            mtime = f.stat().st_mtime
                            if latest_mtime is None or mtime > latest_mtime:
                                latest_mtime = mtime
            
            if count_key:
                total_counts[count_key] = len(files)
            
            # 创建分类节点
            size_str = f"{total_size / 1024 / 1024:.1f} MB" if total_size > 1024*1024 else f"{total_size / 1024:.1f} KB"
            mtime_str = datetime.fromtimestamp(latest_mtime).strftime('%m-%d %H:%M') if latest_mtime else "-"
            
            cat_item = QTreeWidgetItem([cat_name, "文件夹", f"{len(files)} 文件", mtime_str])
            cat_item.setData(0, Qt.ItemDataRole.UserRole, str(dir_path))
            cat_item.setExpanded(True)
            
            # 添加子目录
            subdirs = {}
            for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)[:20]:
                rel_path = f.relative_to(dir_path)
                if len(rel_path.parts) > 1:
                    subdir = rel_path.parts[0]
                    if subdir not in subdirs:
                        subdirs[subdir] = QTreeWidgetItem([f"📁 {subdir}", "子目录", "", ""])
                        subdirs[subdir].setData(0, Qt.ItemDataRole.UserRole, str(dir_path / subdir))
                        cat_item.addChild(subdirs[subdir])
                    parent = subdirs[subdir]
                else:
                    parent = cat_item
                
                fsize = f"{f.stat().st_size / 1024:.1f} KB"
                fmtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')
                file_item = QTreeWidgetItem([f.name, f.suffix.upper(), fsize, fmtime])
                file_item.setData(0, Qt.ItemDataRole.UserRole, str(f))
                parent.addChild(file_item)
            
            self.files_tree.addTopLevelItem(cat_item)
        
        # 更新统计卡片
        self.strategy_card.findChild(QLabel, "value").setText(str(total_counts["strategy_count"]))
        self.report_card.findChild(QLabel, "value").setText(str(total_counts["report_count"]))
        self.doc_card.findChild(QLabel, "value").setText(str(total_counts["doc_count"]))
        self.data_card.findChild(QLabel, "value").setText(str(total_counts["data_count"]))
    
    def _load_strategies(self):
        """加载策略列表"""
        self.strategy_tree.clear()
        
        base_dir = Path(__file__).parent.parent.parent
        strategies_dir = base_dir / "strategies"
        
        if not strategies_dir.exists():
            return
        
        # 按平台分组
        platforms = [
            ("PTrade策略", "ptrade"),
            ("QMT策略", "qmt"),
            ("示例策略", "examples"),
        ]
        
        for platform_name, subdir in platforms:
            platform_dir = strategies_dir / subdir
            if not platform_dir.exists():
                continue
            
            platform_item = QTreeWidgetItem([f"📁 {platform_name}", "", ""])
            platform_item.setExpanded(True)
            
            for f in sorted(platform_dir.glob("*.py"), reverse=True):
                if f.name.startswith("__"):
                    continue
                
                mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%m-%d %H:%M')
                item = QTreeWidgetItem([f.stem, subdir, mtime])
                item.setData(0, Qt.ItemDataRole.UserRole, str(f))
                platform_item.addChild(item)
            
            if platform_item.childCount() > 0:
                self.strategy_tree.addTopLevelItem(platform_item)
    
    def _load_backtests(self):
        """加载回测记录"""
        self.backtest_table.setRowCount(0)
        
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
            db = client['trquant']
            
            backtests = list(db.backtest_results.find().sort("timestamp", -1).limit(30))
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
                self.backtest_table.setItem(i, 5, QTableWidgetItem(bt.get("status", "完成")))
                
        except Exception as e:
            logger.warning(f"加载回测记录失败: {e}")
    
    def _load_database(self):
        """加载数据库信息"""
        self.db_table.setRowCount(0)
        
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=3000)
            db = client['trquant']
            
            collections = db.list_collection_names()
            self.db_table.setRowCount(len(collections))
            
            for i, coll_name in enumerate(sorted(collections)):
                coll = db[coll_name]
                doc_count = coll.count_documents({})
                
                # 获取大小
                try:
                    stats = db.command("collstats", coll_name)
                    size = f"{stats.get('size', 0) / 1024:.1f} KB"
                except:
                    size = "-"
                
                # 获取最后更新
                last_doc = coll.find_one(sort=[("timestamp", -1)])
                if last_doc and "timestamp" in last_doc:
                    ts = last_doc["timestamp"]
                    last_update = ts.strftime('%m-%d %H:%M') if hasattr(ts, 'strftime') else str(ts)[:16]
                else:
                    last_update = "-"
                
                self.db_table.setItem(i, 0, QTableWidgetItem(coll_name))
                self.db_table.setItem(i, 1, QTableWidgetItem(str(doc_count)))
                self.db_table.setItem(i, 2, QTableWidgetItem(size))
                self.db_table.setItem(i, 3, QTableWidgetItem(last_update))
                
        except Exception as e:
            logger.warning(f"加载数据库信息失败: {e}")
    
    def _open_dashboard(self):
        """打开Web文件管理系统"""
        try:
            project_root = Path(__file__).parent.parent.parent
            
            # 启动Dashboard服务
            subprocess.Popen(
                [sys.executable, 'start_dashboard.py'],
                cwd=str(project_root),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # 等待服务启动后打开浏览器
            import time
            time.sleep(2)
            webbrowser.open("http://127.0.0.1:5000")
            
        except Exception as e:
            QMessageBox.warning(self, "启动失败", f"无法启动文件管理系统: {e}")
    
    def _open_file_or_folder(self, item, col):
        """打开文件或文件夹"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path:
            p = Path(path)
            if p.exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(p)))
    
    def _open_strategies_folder(self):
        """打开策略目录"""
        strategies_dir = Path(__file__).parent.parent.parent / "strategies" / "ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(strategies_dir)))
    
    def _generate_new_strategy(self):
        """生成新策略"""
        try:
            from core.workflow_orchestrator import get_workflow_orchestrator
            
            reply = QMessageBox.question(
                self, "生成策略",
                "是否基于当前工作流结果生成新策略？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                orchestrator = get_workflow_orchestrator()
                result = orchestrator.generate_strategy()
                
                if result.success:
                    QMessageBox.information(self, "成功", f"策略已生成:\n{result.details.get('strategy_file', '')}")
                    self._load_strategies()
                else:
                    QMessageBox.warning(self, "失败", result.summary)
        except Exception as e:
            QMessageBox.warning(self, "错误", str(e))
    
    def _preview_strategy(self, item, col):
        """预览策略代码"""
        path = item.data(0, Qt.ItemDataRole.UserRole)
        if path and Path(path).exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_preview.setPlainText(code)
            except Exception as e:
                self.code_preview.setPlainText(f"读取失败: {e}")
    
    def _export_database(self):
        """导出数据库"""
        dest_dir = QFileDialog.getExistingDirectory(self, "选择导出目录")
        if not dest_dir:
            return
        
        try:
            from pymongo import MongoClient
            client = MongoClient('localhost', 27017)
            db = client['trquant']
            
            dest_path = Path(dest_dir) / f"trquant_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {}
            for coll_name in db.list_collection_names():
                docs = list(db[coll_name].find())
                for doc in docs:
                    doc['_id'] = str(doc['_id'])
                    for k, v in doc.items():
                        if hasattr(v, 'isoformat'):
                            doc[k] = v.isoformat()
                export_data[coll_name] = docs
            
            with open(dest_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "成功", f"数据已导出到:\n{dest_path}")
            
        except Exception as e:
            QMessageBox.warning(self, "导出失败", str(e))
