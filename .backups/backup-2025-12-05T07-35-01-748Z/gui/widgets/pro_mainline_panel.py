"""
专业级主线识别面板

基于《A股主线识别量化流程建议书》设计

特点：
1. 预显示方法论、参数和表格结构
2. 异步数据抓取，不阻塞UI
3. 生成HTML报告，在浏览器中查看
"""

import logging
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QMessageBox, QSplitter,
    QGroupBox, QGridLayout, QSizePolicy, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QUrl
from PyQt6.QtGui import QFont, QColor, QDesktopServices

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


# ============================================================
# 评分维度配置 - 用于UI展示
# ============================================================

SCORING_DIMENSIONS = [
    {
        "name": "资金维度",
        "icon": "💰",
        "weight": 25,
        "color": "#3b82f6",
        "description": "主力资金净流入强度",
        "factors": [
            {"name": "当日净流入排名", "description": "板块净流入金额在所有板块中的排名百分位"},
            {"name": "5日累计净流入", "description": "5日累计净流入在所有板块中的排名百分位"},
            {"name": "流入占比", "description": "净流入/流入资金，反映资金净流入强度"},
        ],
    },
    {
        "name": "动量维度",
        "icon": "📈",
        "weight": 20,
        "color": "#10b981",
        "description": "板块动量效应",
        "factors": [
            {"name": "涨跌幅排名", "description": "板块涨跌幅在所有板块中的排名百分位"},
            {"name": "相对强度", "description": "板块涨幅 - 沪深300涨幅"},
            {"name": "趋势得分", "description": "基于均线排列和突破情况"},
        ],
    },
    {
        "name": "热度维度",
        "icon": "🔥",
        "weight": 20,
        "color": "#f59e0b",
        "description": "市场关注度",
        "factors": [
            {"name": "涨停股占比", "description": "板块涨停股数量/板块总股票数"},
            {"name": "成交量放大", "description": "今日成交量/5日平均成交量"},
            {"name": "关注度得分", "description": "基于搜索热度、新闻数量等"},
        ],
    },
    {
        "name": "政策维度",
        "icon": "📜",
        "weight": 20,
        "color": "#8b5cf6",
        "description": "政策支持力度",
        "factors": [
            {"name": "政策支持", "description": "近期是否有重大政策利好"},
            {"name": "产业趋势", "description": "行业景气度和发展趋势"},
            {"name": "事件催化", "description": "是否有重大事件驱动"},
        ],
    },
    {
        "name": "龙头维度",
        "icon": "👑",
        "weight": 15,
        "color": "#ec4899",
        "description": "龙头股强度",
        "factors": [
            {"name": "龙头强度", "description": "龙头股涨幅和连板情况"},
            {"name": "跟风效应", "description": "板块内跟涨股票比例"},
            {"name": "大市值龙头", "description": "是否有大市值龙头领涨"},
        ],
    },
]

SIGNAL_RULES = [
    {"signal": "买入", "condition": "≥75分", "color": "#10b981", "description": "强主线，可重点配置"},
    {"signal": "持有", "condition": "60-75分", "color": "#3b82f6", "description": "较强主线，适当参与"},
    {"signal": "观察", "condition": "45-60分", "color": "#f59e0b", "description": "一般主线，观察为主"},
    {"signal": "卖出", "condition": "<45分", "color": "#ef4444", "description": "弱主线，暂不参与"},
]


class DataFetchWorker(QThread):
    """异步数据抓取线程"""
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str, int)  # message, percentage
    error = pyqtSignal(str)
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            
            fetcher = RealDataFetcher()
            results = {}
            
            # 抓取行业板块
            self.progress.emit("正在抓取行业板块数据...", 20)
            try:
                sector_result = fetcher.fetch_sector_flow()
                if sector_result and sector_result.success:
                    results["sector_flow"] = sector_result.data
            except Exception as e:
                logger.warning(f"行业板块抓取失败: {e}")
            
            # 抓取概念板块
            self.progress.emit("正在抓取概念板块数据...", 50)
            try:
                concept_result = fetcher.fetch_concept_board()
                if concept_result and concept_result.success:
                    results["concept_flow"] = concept_result.data
            except Exception as e:
                logger.warning(f"概念板块抓取失败: {e}")
            
            # 抓取北向资金
            self.progress.emit("正在抓取北向资金数据...", 70)
            try:
                north_result = fetcher.fetch_northbound_flow()
                if north_result and north_result.success:
                    results["northbound"] = north_result.data
            except Exception as e:
                logger.warning(f"北向资金抓取失败: {e}")
            
            # 抓取涨停池
            self.progress.emit("正在抓取涨停池数据...", 90)
            try:
                limit_result = fetcher.fetch_market_sentiment()
                if limit_result and limit_result.success:
                    results["limit_up"] = limit_result.data
            except Exception as e:
                logger.warning(f"涨停池抓取失败: {e}")
            
            self.progress.emit("数据抓取完成", 100)
            self.finished.emit(results)
            
        except Exception as e:
            logger.exception(f"数据抓取失败: {e}")
            self.error.emit(str(e))


class AnalysisWorker(QThread):
    """异步分析线程"""
    finished = pyqtSignal(list, str)  # mainlines, report_path
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, raw_data: Dict):
        super().__init__()
        self.raw_data = raw_data
    
    def run(self):
        try:
            from markets.ashare.mainline.pro_engine import ProMainlineEngine
            from markets.ashare.mainline.report_generator import MainlineReportGenerator
            
            # 执行分析
            self.progress.emit("正在执行主线识别分析...")
            engine = ProMainlineEngine()
            mainlines = engine.analyze(self.raw_data)
            
            # 生成报告
            self.progress.emit("正在生成HTML报告...")
            generator = MainlineReportGenerator()
            config = engine.get_config_description()
            report_path = generator.generate_html_report(mainlines, self.raw_data, config)
            
            self.finished.emit(mainlines, report_path)
            
        except Exception as e:
            logger.exception(f"分析失败: {e}")
            self.error.emit(str(e))


class DimensionCard(QFrame):
    """评分维度卡片"""
    
    def __init__(self, dimension: Dict, parent=None):
        super().__init__(parent)
        self.dimension = dimension
        self._setup_ui()
    
    def _setup_ui(self):
        color = self.dimension["color"]
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {color}40;
                border-left: 4px solid {color};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(6)
        
        # 标题行
        header = QHBoxLayout()
        
        title = QLabel(f"{self.dimension['icon']} {self.dimension['name']}")
        title.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13px;")
        header.addWidget(title)
        
        header.addStretch()
        
        weight = QLabel(f"{self.dimension['weight']}分")
        weight.setStyleSheet(f"""
            background-color: {color}30;
            color: {color};
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
        """)
        header.addWidget(weight)
        
        layout.addLayout(header)
        
        # 描述
        desc = QLabel(self.dimension["description"])
        desc.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px;")
        layout.addWidget(desc)
        
        # 因子列表
        for factor in self.dimension["factors"]:
            factor_label = QLabel(f"• {factor['name']}")
            factor_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 10px;")
            factor_label.setToolTip(factor["description"])
            layout.addWidget(factor_label)


class SignalRuleCard(QFrame):
    """信号规则卡片"""
    
    def __init__(self, rule: Dict, parent=None):
        super().__init__(parent)
        self.rule = rule
        self._setup_ui()
    
    def _setup_ui(self):
        color = self.rule["color"]
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color}15;
                border: 1px solid {color}30;
                border-radius: 6px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)
        
        # 信号标签
        signal = QLabel(self.rule["signal"])
        signal.setStyleSheet(f"""
            background-color: {color}30;
            color: {color};
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 11px;
        """)
        signal.setFixedWidth(50)
        layout.addWidget(signal)
        
        # 条件
        condition = QLabel(self.rule["condition"])
        condition.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold; font-size: 11px;")
        condition.setFixedWidth(60)
        layout.addWidget(condition)
        
        # 描述
        desc = QLabel(self.rule["description"])
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(desc)
        
        layout.addStretch()


class ProMainlinePanel(QWidget):
    """专业级主线识别面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fetch_worker = None
        self.analysis_worker = None
        self.raw_data = {}
        self.mainlines = []
        self.report_path = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ========== 顶部工具栏 ==========
        toolbar = QFrame()
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(20, 12, 20, 12)
        
        # 标题
        title = QLabel("🎯 专业级主线识别")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        toolbar_layout.addWidget(title)
        
        subtitle = QLabel("基于《A股主线识别量化流程建议书》")
        subtitle.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px; margin-left: 10px;")
        toolbar_layout.addWidget(subtitle)
        
        toolbar_layout.addStretch()
        
        # 抓取按钮
        self.fetch_btn = QPushButton("🔄 抓取数据")
        self.fetch_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY}dd; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.fetch_btn.clicked.connect(self._start_fetch)
        toolbar_layout.addWidget(self.fetch_btn)
        
        # 分析按钮
        self.analyze_btn = QPushButton("📊 执行分析")
        self.analyze_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SUCCESS};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: #27ae60; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.analyze_btn.setEnabled(False)
        self.analyze_btn.clicked.connect(self._start_analysis)
        toolbar_layout.addWidget(self.analyze_btn)
        
        # 查看报告按钮
        self.report_btn = QPushButton("📄 查看报告")
        self.report_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #8b5cf6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }}
            QPushButton:hover {{ background-color: #7c3aed; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.report_btn.setEnabled(False)
        self.report_btn.clicked.connect(self._open_report)
        toolbar_layout.addWidget(self.report_btn)
        
        layout.addWidget(toolbar)
        
        # ========== 进度条 ==========
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        self.progress_frame.setVisible(False)
        progress_layout = QHBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(20, 8, 20, 8)
        
        self.progress_label = QLabel("准备中...")
        self.progress_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 12px;")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: {Colors.BG_TERTIARY};
                border-radius: 4px;
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
                border-radius: 4px;
            }}
        """)
        self.progress_bar.setFixedWidth(200)
        progress_layout.addWidget(self.progress_bar)
        
        progress_layout.addStretch()
        
        layout.addWidget(self.progress_frame)
        
        # ========== 主内容区域 ==========
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Colors.BG_PRIMARY};
            }}
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # ========== 方法论说明 ==========
        method_section = QFrame()
        method_section.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.PRIMARY}40;
                border-radius: 12px;
            }}
        """)
        method_layout = QVBoxLayout(method_section)
        method_layout.setContentsMargins(20, 16, 20, 16)
        method_layout.setSpacing(16)
        
        method_title = QLabel("📐 评分方法论")
        method_title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        method_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        method_layout.addWidget(method_title)
        
        method_desc = QLabel(
            "基于《A股主线识别量化流程建议书》，采用五维评分模型识别市场主线。"
            "主线是指在特定时期内，市场资金持续流入、热度持续上升的投资方向。"
        )
        method_desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        method_desc.setWordWrap(True)
        method_layout.addWidget(method_desc)
        
        # 评分维度卡片
        dim_grid = QGridLayout()
        dim_grid.setSpacing(12)
        
        for i, dim in enumerate(SCORING_DIMENSIONS):
            card = DimensionCard(dim)
            dim_grid.addWidget(card, i // 3, i % 3)
        
        method_layout.addLayout(dim_grid)
        
        # 信号规则
        signal_title = QLabel("📊 交易信号规则")
        signal_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold; font-size: 13px; margin-top: 8px;")
        method_layout.addWidget(signal_title)
        
        signal_grid = QGridLayout()
        signal_grid.setSpacing(8)
        
        for i, rule in enumerate(SIGNAL_RULES):
            card = SignalRuleCard(rule)
            signal_grid.addWidget(card, i // 2, i % 2)
        
        method_layout.addLayout(signal_grid)
        
        content_layout.addWidget(method_section)
        
        # ========== 数据抓取区域 ==========
        data_section = QFrame()
        data_section.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        data_layout = QVBoxLayout(data_section)
        data_layout.setContentsMargins(20, 16, 20, 16)
        data_layout.setSpacing(12)
        
        data_title = QLabel("📋 数据抓取")
        data_title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        data_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        data_layout.addWidget(data_title)
        
        # 数据源表格
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(["数据源", "来源", "状态", "数据量", "抓取时间"])
        self.data_table.setRowCount(4)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                padding: 8px;
                font-weight: bold;
            }}
        """)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.data_table.setMaximumHeight(180)
        
        # 初始化数据源行
        data_sources = [
            ("行业板块资金流向", "同花顺 via AKShare"),
            ("概念板块资金流向", "同花顺 via AKShare"),
            ("北向资金流向", "东方财富 via AKShare"),
            ("涨停池数据", "东方财富 via AKShare"),
        ]
        
        for i, (name, source) in enumerate(data_sources):
            self.data_table.setItem(i, 0, QTableWidgetItem(name))
            self.data_table.setItem(i, 1, QTableWidgetItem(source))
            
            status_item = QTableWidgetItem("⏳ 等待抓取")
            status_item.setForeground(QColor(Colors.TEXT_MUTED))
            self.data_table.setItem(i, 2, status_item)
            
            self.data_table.setItem(i, 3, QTableWidgetItem("--"))
            self.data_table.setItem(i, 4, QTableWidgetItem("--"))
        
        data_layout.addWidget(self.data_table)
        
        content_layout.addWidget(data_section)
        
        # ========== 分析结果区域 ==========
        result_section = QFrame()
        result_section.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.SUCCESS}40;
                border-radius: 12px;
            }}
        """)
        result_layout = QVBoxLayout(result_section)
        result_layout.setContentsMargins(20, 16, 20, 16)
        result_layout.setSpacing(12)
        
        result_title = QLabel("🎯 主线识别结果")
        result_title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        result_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        result_layout.addWidget(result_title)
        
        # 结果表格
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(10)
        self.result_table.setHorizontalHeaderLabels([
            "排名", "主线名称", "类型", "总分", "资金", "动量", "热度", "政策", "龙头", "信号"
        ])
        self.result_table.setRowCount(10)
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 6px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                padding: 6px;
                font-weight: bold;
                font-size: 11px;
            }}
        """)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.result_table.setMinimumHeight(350)
        
        # 初始化占位
        for i in range(10):
            for j in range(10):
                item = QTableWidgetItem("--")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setForeground(QColor(Colors.TEXT_MUTED))
                self.result_table.setItem(i, j, item)
        
        result_layout.addWidget(self.result_table)
        
        content_layout.addWidget(result_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _start_fetch(self):
        """开始抓取数据"""
        if self.fetch_worker and self.fetch_worker.isRunning():
            return
        
        self.fetch_btn.setEnabled(False)
        self.analyze_btn.setEnabled(False)
        self.report_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 重置数据表格状态
        for i in range(4):
            status_item = QTableWidgetItem("🔄 抓取中...")
            status_item.setForeground(QColor(Colors.PRIMARY))
            self.data_table.setItem(i, 2, status_item)
            self.data_table.setItem(i, 3, QTableWidgetItem("--"))
            self.data_table.setItem(i, 4, QTableWidgetItem("--"))
        
        self.fetch_worker = DataFetchWorker()
        self.fetch_worker.progress.connect(self._on_fetch_progress)
        self.fetch_worker.finished.connect(self._on_fetch_finished)
        self.fetch_worker.error.connect(self._on_fetch_error)
        self.fetch_worker.start()
    
    def _on_fetch_progress(self, message: str, percentage: int):
        """抓取进度更新"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(percentage)
    
    def _on_fetch_finished(self, data: Dict):
        """抓取完成"""
        self.raw_data = data
        self.fetch_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        
        now = datetime.now().strftime("%H:%M:%S")
        
        # 更新数据表格
        data_keys = ["sector_flow", "concept_flow", "northbound", "limit_up"]
        for i, key in enumerate(data_keys):
            if key in data and data[key]:
                status_item = QTableWidgetItem("✅ 成功")
                status_item.setForeground(QColor(Colors.SUCCESS))
                self.data_table.setItem(i, 2, status_item)
                
                count = len(data[key]) if isinstance(data[key], list) else 1
                self.data_table.setItem(i, 3, QTableWidgetItem(str(count)))
                self.data_table.setItem(i, 4, QTableWidgetItem(now))
            else:
                status_item = QTableWidgetItem("❌ 失败")
                status_item.setForeground(QColor(Colors.ERROR))
                self.data_table.setItem(i, 2, status_item)
    
    def _on_fetch_error(self, error: str):
        """抓取错误"""
        self.fetch_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        QMessageBox.warning(self, "抓取失败", f"数据抓取失败: {error}")
    
    def _start_analysis(self):
        """开始分析"""
        if not self.raw_data:
            QMessageBox.warning(self, "提示", "请先抓取数据")
            return
        
        if self.analysis_worker and self.analysis_worker.isRunning():
            return
        
        self.analyze_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 无限进度
        
        self.analysis_worker = AnalysisWorker(self.raw_data)
        self.analysis_worker.progress.connect(self._on_analysis_progress)
        self.analysis_worker.finished.connect(self._on_analysis_finished)
        self.analysis_worker.error.connect(self._on_analysis_error)
        self.analysis_worker.start()
    
    def _on_analysis_progress(self, message: str):
        """分析进度更新"""
        self.progress_label.setText(message)
    
    def _on_analysis_finished(self, mainlines: list, report_path: str):
        """分析完成"""
        self.mainlines = mainlines
        self.report_path = report_path
        self.analyze_btn.setEnabled(True)
        self.report_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        self.progress_bar.setRange(0, 100)
        
        # 更新结果表格
        self._update_result_table(mainlines)
        
        # 自动打开报告
        self._open_report()
        
        # 简短提示
        self.progress_label.setText(
            f"✅ 分析完成！识别到 {len(mainlines)} 条主线，"
            f"强主线 {sum(1 for m in mainlines if m.score.total >= 75)} 条"
        )
        self.progress_frame.setVisible(True)
    
    def _on_analysis_error(self, error: str):
        """分析错误"""
        self.analyze_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        self.progress_bar.setRange(0, 100)
        QMessageBox.warning(self, "分析失败", f"主线分析失败: {error}")
    
    def _update_result_table(self, mainlines: list):
        """更新结果表格"""
        self.result_table.setRowCount(min(len(mainlines), 20))
        
        for i, ml in enumerate(mainlines[:20]):
            # 排名
            rank_item = QTableWidgetItem(str(i + 1))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            rank_item.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
            self.result_table.setItem(i, 0, rank_item)
            
            # 名称
            name_item = QTableWidgetItem(ml.name)
            name_item.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
            self.result_table.setItem(i, 1, name_item)
            
            # 类型
            type_item = QTableWidgetItem(ml.type)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_table.setItem(i, 2, type_item)
            
            # 总分
            score = ml.score
            total_item = QTableWidgetItem(f"{score.total:.1f}")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            total_item.setFont(QFont("Microsoft YaHei", 11, QFont.Weight.Bold))
            if score.total >= 75:
                total_item.setForeground(QColor(Colors.SUCCESS))
            elif score.total >= 60:
                total_item.setForeground(QColor(Colors.PRIMARY))
            elif score.total >= 45:
                total_item.setForeground(QColor("#f59e0b"))
            else:
                total_item.setForeground(QColor(Colors.ERROR))
            self.result_table.setItem(i, 3, total_item)
            
            # 各维度得分
            scores = [score.funds_score, score.momentum_score, score.heat_score, 
                     score.policy_score, score.leader_score]
            for j, s in enumerate(scores):
                item = QTableWidgetItem(f"{s:.1f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.result_table.setItem(i, 4 + j, item)
            
            # 信号
            signal_item = QTableWidgetItem(ml.signal.value)
            signal_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            signal_item.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
            signal_colors = {
                "买入": Colors.SUCCESS,
                "持有": Colors.PRIMARY,
                "观察": "#f59e0b",
                "卖出": Colors.ERROR,
            }
            signal_item.setForeground(QColor(signal_colors.get(ml.signal.value, Colors.TEXT_MUTED)))
            self.result_table.setItem(i, 9, signal_item)
    
    def _open_report(self):
        """打开报告 - 在文件管理器中显示并自动打开"""
        if not self.report_path or not Path(self.report_path).exists():
            QMessageBox.warning(self, "提示", "报告文件不存在，请先执行分析")
            return
        
        import subprocess
        import platform
        
        report_path = Path(self.report_path)
        report_dir = report_path.parent
        
        system = platform.system()
        
        try:
            if system == "Linux":
                # Linux: 使用 xdg-open 打开报告，使用 nautilus/dolphin 显示文件夹
                # 先在浏览器中打开报告
                subprocess.Popen(["xdg-open", str(report_path)])
                
                # 然后在文件管理器中选中文件
                # 尝试不同的文件管理器
                file_managers = [
                    ["nautilus", "--select", str(report_path)],  # GNOME
                    ["dolphin", "--select", str(report_path)],   # KDE
                    ["nemo", str(report_dir)],                   # Cinnamon
                    ["thunar", str(report_dir)],                 # XFCE
                    ["pcmanfm", str(report_dir)],                # LXDE
                ]
                
                for fm_cmd in file_managers:
                    try:
                        subprocess.Popen(fm_cmd, stderr=subprocess.DEVNULL)
                        break
                    except FileNotFoundError:
                        continue
                        
            elif system == "Darwin":
                # macOS: 使用 open 命令
                subprocess.Popen(["open", str(report_path)])
                subprocess.Popen(["open", "-R", str(report_path)])  # 在Finder中显示
                
            elif system == "Windows":
                # Windows: 使用 explorer
                subprocess.Popen(["start", "", str(report_path)], shell=True)
                subprocess.Popen(["explorer", "/select,", str(report_path)])
            
            else:
                # 其他系统：使用 Qt 的方式
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(report_path)))
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(report_dir)))
                
            logger.info(f"已打开报告: {report_path}")
            
        except Exception as e:
            logger.error(f"打开报告失败: {e}")
            # 回退方案：使用webbrowser
            try:
                webbrowser.open(f"file://{report_path}")
                QMessageBox.information(
                    self, "报告已打开", 
                    f"报告已在浏览器中打开。\n\n文件位置:\n{report_path}"
                )
            except Exception as e2:
                QMessageBox.warning(self, "打开失败", f"无法打开报告: {e2}\n\n文件位置:\n{report_path}")


# 导出
__all__ = ["ProMainlinePanel"]

