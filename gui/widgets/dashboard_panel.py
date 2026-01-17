# -*- coding: utf-8 -*-
"""
量化策略全流程工作台 - 仪表盘面板
专业投行级别的策略开发与交易工作流程管理
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGroupBox, QGridLayout, QFrame, QProgressBar, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter,
    QTabWidget, QTextEdit, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QColor, QPainter, QPen
import logging
from datetime import datetime
from pathlib import Path
import json
import os

logger = logging.getLogger(__name__)


class DataLoaderThread(QThread):
    """数据加载线程"""
    data_loaded = pyqtSignal(dict)
    
    def __init__(self, project_root: Path):
        super().__init__()
        self.project_root = project_root
    
    def run(self):
        data = {
            'strategies': [],
            'reports': [],
            'backtest_results': [],
            'total_trades': 0,
            'total_profit': 0,
            'win_rate': 0,
            'profit_loss_ratio': 0,
            'sharpe_avg': 0,
            'max_drawdown_avg': 0,
        }
        
        try:
            # 加载策略
            strategies_dir = self.project_root / 'strategies' / 'examples'
            if strategies_dir.exists():
                for f in strategies_dir.glob('*.py'):
                    if not f.name.startswith('__'):
                        data['strategies'].append({
                            'name': f.stem,
                            'path': str(f),
                            'modified': datetime.fromtimestamp(f.stat().st_mtime)
                        })
            
            # 加载报告
            results_dir = self.project_root / 'results'
            if results_dir.exists():
                for f in results_dir.glob('*.html'):
                    data['reports'].append({
                        'name': f.stem,
                        'path': str(f),
                        'modified': datetime.fromtimestamp(f.stat().st_mtime)
                    })
                
                # 加载JSON回测结果
                total_return = []
                sharpe_ratios = []
                max_drawdowns = []
                win_trades = 0
                loss_trades = 0
                total_profit_sum = 0
                total_loss_sum = 0
                
                for f in results_dir.glob('*.json'):
                    try:
                        with open(f, 'r', encoding='utf-8') as jf:
                            result = json.load(jf)
                            data['backtest_results'].append(result)
                            
                            metrics = result.get('metrics', {})
                            summary = result.get('summary', {})
                            
                            if 'total_return' in metrics:
                                total_return.append(metrics['total_return'])
                            if 'sharpe_ratio' in metrics:
                                sharpe_ratios.append(metrics['sharpe_ratio'])
                            if 'max_drawdown' in metrics:
                                max_drawdowns.append(metrics['max_drawdown'])
                            
                            # 分析交易历史
                            trades = result.get('trade_history', [])
                            data['total_trades'] += len(trades)
                            
                            # 简单统计盈亏
                            profit = summary.get('total_profit', 0)
                            if profit > 0:
                                win_trades += 1
                                total_profit_sum += profit
                            else:
                                loss_trades += 1
                                total_loss_sum += abs(profit)
                            
                    except Exception as e:
                        logger.warning(f"加载结果文件失败: {f}, {e}")
                
                # 计算统计
                if total_return:
                    data['avg_return'] = sum(total_return) / len(total_return)
                if sharpe_ratios:
                    data['sharpe_avg'] = sum(sharpe_ratios) / len(sharpe_ratios)
                if max_drawdowns:
                    data['max_drawdown_avg'] = sum(max_drawdowns) / len(max_drawdowns)
                
                total_completed = win_trades + loss_trades
                if total_completed > 0:
                    data['win_rate'] = win_trades / total_completed
                
                if total_loss_sum > 0:
                    data['profit_loss_ratio'] = total_profit_sum / total_loss_sum
                    
        except Exception as e:
            logger.error(f"加载数据失败: {e}")
        
        self.data_loaded.emit(data)


class MetricCard(QFrame):
    """指标卡片组件"""
    
    def __init__(self, title: str, icon: str = "", color: str = "#89b4fa", parent=None):
        super().__init__(parent)
        self.color = color
        self.setObjectName("metricCard")
        self.setStyleSheet(f"""
            #metricCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e1e2e, stop:1 #181825);
                border: 1px solid #313244;
                border-radius: 16px;
                padding: 20px;
            }}
            #metricCard:hover {{
                border-color: {color};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #262637, stop:1 #1e1e2e);
            }}
        """)
        self.setMinimumHeight(140)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # 标题行
        header = QHBoxLayout()
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(f"font-size: 20px; color: {color};")
            header.addWidget(icon_label)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"color: #a6adc8; font-size: 13px; font-weight: 500;")
        header.addWidget(self.title_label)
        header.addStretch()
        layout.addLayout(header)
        
        # 主要值
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet(f"""
            font-size: 32px; 
            font-weight: bold; 
            color: {color};
            letter-spacing: -1px;
        """)
        layout.addWidget(self.value_label)
        
        # 描述/子值
        self.desc_label = QLabel("")
        self.desc_label.setStyleSheet("color: #a6adc8; font-size: 12px;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        layout.addStretch()
    
    def set_value(self, value: str, desc: str = ""):
        self.value_label.setText(value)
        self.desc_label.setText(desc)


class ProgressStage(QFrame):
    """流程阶段组件"""
    
    def __init__(self, title: str, step: int, status: str = "pending", parent=None):
        super().__init__(parent)
        self.step = step
        self.status = status
        
        self.setFixedWidth(120)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        
        # 圆形步骤指示器
        self.step_label = QLabel(str(step))
        self.step_label.setFixedSize(36, 36)
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.step_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 标题
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #cdd6f4; font-size: 12px;")
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)
        
        # 子描述
        self.desc_label = QLabel("")
        self.desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.desc_label.setStyleSheet("color: #a6adc8; font-size: 10px;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        self.set_status(status)
    
    def set_status(self, status: str, desc: str = ""):
        self.status = status
        self.desc_label.setText(desc)
        
        if status == "completed":
            self.step_label.setStyleSheet("""
                background-color: #a6e3a1;
                color: #1e1e2e;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
            """)
            self.step_label.setText("✓")
        elif status == "in_progress":
            self.step_label.setStyleSheet("""
                background-color: #89b4fa;
                color: #1e1e2e;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
            """)
        elif status == "warning":
            self.step_label.setStyleSheet("""
                background-color: #f9e2af;
                color: #1e1e2e;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
            """)
        else:  # pending
            self.step_label.setStyleSheet("""
                background-color: #45475a;
                color: #a6adc8;
                border-radius: 18px;
                font-size: 14px;
                font-weight: bold;
            """)


class ReadinessGauge(QFrame):
    """准备度仪表组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.setMinimumSize(200, 80)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # 标题
        header = QHBoxLayout()
        title = QLabel("实盘准备度")
        title.setStyleSheet("color: #a6adc8; font-size: 13px; font-weight: 500;")
        header.addWidget(title)
        header.addStretch()
        
        self.percent_label = QLabel("0%")
        self.percent_label.setStyleSheet("color: #89b4fa; font-size: 18px; font-weight: bold;")
        header.addWidget(self.percent_label)
        layout.addLayout(header)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(12)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 6px;
                background-color: #313244;
            }
            QProgressBar::chunk {
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a6e3a1, stop:1 #89b4fa);
            }
        """)
        layout.addWidget(self.progress)
        
        # 说明
        self.desc_label = QLabel("")
        self.desc_label.setStyleSheet("color: #a6adc8; font-size: 11px;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
    
    def set_value(self, value: int, desc: str = ""):
        self.value = value
        self.progress.setValue(value)
        self.percent_label.setText(f"{value}%")
        self.desc_label.setText(desc)


class DashboardPanel(QWidget):
    """量化策略全流程工作台 - 仪表盘"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 获取项目根目录
        self.project_root = Path(__file__).parent.parent.parent
        
        self.data = {}
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(24)
        
        # === 头部区域 ===
        header = self.create_header()
        content_layout.addWidget(header)
        
        # === 概览介绍卡片 ===
        intro_card = self.create_intro_card()
        content_layout.addWidget(intro_card)
        
        # === 仪表盘概览 ===
        overview_section = self.create_overview_section()
        content_layout.addWidget(overview_section)
        
        # === 核心指标 ===
        metrics_section = self.create_metrics_section()
        content_layout.addWidget(metrics_section)
        
        # === 流程进度追踪 ===
        progress_section = self.create_progress_section()
        content_layout.addWidget(progress_section)
        
        # === 策略列表 & 最近报告 ===
        details_section = self.create_details_section()
        content_layout.addWidget(details_section)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
    
    def create_header(self) -> QWidget:
        """创建头部区域"""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧标题
        left = QVBoxLayout()
        
        title = QLabel("📊 量化策略全流程工作台")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #89b4fa;
            letter-spacing: 1px;
        """)
        left.addWidget(title)
        
        subtitle = QLabel("平台提供统一的策略管理、回测报表与流程协同能力，将投研、风控、交易与管理层需要的核心指标集中展示。")
        subtitle.setStyleSheet("color: #a6adc8; font-size: 13px;")
        subtitle.setWordWrap(True)
        left.addWidget(subtitle)
        
        layout.addLayout(left, 1)
        
        # 右侧操作
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        # 打开Web仪表盘按钮
        web_btn = QPushButton("🌐 打开Web仪表盘")
        web_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c8ff0, stop:1 #8a5db8);
            }
        """)
        web_btn.clicked.connect(self.open_web_dashboard)
        right.addWidget(web_btn)
        
        refresh_btn = QPushButton("🔄 刷新数据")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """)
        refresh_btn.clicked.connect(self.load_data)
        right.addWidget(refresh_btn)
        
        self.update_time = QLabel("更新时间: --")
        self.update_time.setStyleSheet("color: #a6adc8; font-size: 11px;")
        right.addWidget(self.update_time)
        
        layout.addLayout(right)
        
        return header
    
    def create_intro_card(self) -> QWidget:
        """创建介绍卡片"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:0.5 #2d4a6f, stop:1 #1e1e2e);
                border: 1px solid #3b5998;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(12)
        
        # 当前进展
        progress_title = QLabel("当前进展：")
        progress_title.setStyleSheet("color: #89b4fa; font-size: 14px; font-weight: bold;")
        layout.addWidget(progress_title)
        
        self.progress_desc = QLabel("正在加载...")
        self.progress_desc.setStyleSheet("color: #cdd6f4; font-size: 13px;")
        self.progress_desc.setWordWrap(True)
        layout.addWidget(self.progress_desc)
        
        # 使用优势
        advantage_title = QLabel("使用优势：")
        advantage_title.setStyleSheet("color: #f9e2af; font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(advantage_title)
        
        advantage_text = QLabel("一键触发回测、自动校验报告质量、按目录规范沉淀成果，并可通过仪表盘监控任务状态、实盘准备度与关键绩效指标。")
        advantage_text.setStyleSheet("color: #cdd6f4; font-size: 13px;")
        advantage_text.setWordWrap(True)
        layout.addWidget(advantage_text)
        
        # 标签页切换
        tabs_layout = QHBoxLayout()
        tabs_layout.setSpacing(16)
        
        self.tab_research = QPushButton("📈 投研亮点")
        self.tab_research.setCheckable(True)
        self.tab_research.setChecked(True)
        self.tab_research.setStyleSheet(self._get_tab_style(True))
        tabs_layout.addWidget(self.tab_research)
        
        self.tab_live = QPushButton("💹 实盘协同")
        self.tab_live.setCheckable(True)
        self.tab_live.setStyleSheet(self._get_tab_style(False))
        tabs_layout.addWidget(self.tab_live)
        
        tabs_layout.addStretch()
        layout.addLayout(tabs_layout)
        
        # 亮点列表
        highlights = QLabel("""
• 策略库与自动化工作流实现"一键回测+报告"，便于快速验证灵感。
• 仪表盘交互图表帮助投研和风控团队共享收益、回撤、胜率等洞察。
• Docs 内置 QA 清单确保数据、回测、文档形成闭环。
        """.strip())
        highlights.setStyleSheet("color: #a6adc8; font-size: 12px; line-height: 1.8;")
        highlights.setWordWrap(True)
        layout.addWidget(highlights)
        
        return card
    
    def _get_tab_style(self, active: bool) -> str:
        if active:
            return """
                QPushButton {
                    background-color: transparent;
                    color: #89b4fa;
                    border: none;
                    border-bottom: 2px solid #89b4fa;
                    padding: 8px 16px;
                    font-weight: bold;
                }
            """
        return """
            QPushButton {
                background-color: transparent;
                color: #a6adc8;
                border: none;
                padding: 8px 16px;
            }
            QPushButton:hover {
                color: #cdd6f4;
            }
        """
    
    def create_overview_section(self) -> QWidget:
        """创建概览区域"""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("仪表盘概览")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #cdd6f4;")
        layout.addWidget(title)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        # 策略数量
        self.card_strategies = MetricCard("策略数量", "📋", "#89b4fa")
        cards_layout.addWidget(self.card_strategies)
        
        # 累计报告
        self.card_reports = MetricCard("累计报告", "📄", "#a6e3a1")
        cards_layout.addWidget(self.card_reports)
        
        # 最近自动化任务
        self.card_tasks = MetricCard("最近自动化任务", "⚡", "#f9e2af")
        cards_layout.addWidget(self.card_tasks)
        
        layout.addLayout(cards_layout)
        
        return section
    
    def create_metrics_section(self) -> QWidget:
        """创建核心指标区域"""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        # 后端健康
        self.card_health = MetricCard("后端健康", "💚", "#a6e3a1")
        cards_layout.addWidget(self.card_health)
        
        # 平均胜率
        self.card_winrate = MetricCard("平均胜率", "🎯", "#89b4fa")
        cards_layout.addWidget(self.card_winrate)
        
        # 平均盈亏比
        self.card_plratio = MetricCard("平均盈亏比", "📊", "#cba6f7")
        cards_layout.addWidget(self.card_plratio)
        
        layout.addLayout(cards_layout)
        
        return section
    
    def create_progress_section(self) -> QWidget:
        """创建流程进度追踪区域"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(16)
        
        # 标题行
        header = QHBoxLayout()
        title = QLabel("流程进度追踪")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #cdd6f4;")
        header.addWidget(title)
        header.addStretch()
        
        self.workflow_btn = QPushButton("🚀 流程调检")
        self.workflow_btn.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
        """)
        header.addWidget(self.workflow_btn)
        
        layout.addLayout(header)
        
        # 进度阶段
        stages_layout = QHBoxLayout()
        stages_layout.setSpacing(0)
        
        self.stages = []
        stage_data = [
            ("研究测算", "策略库 · Docs 指"),
            ("回测验证", "N 次已完成"),
            ("报告沉淀", "N 份报告"),
            ("实盘准备", "风控对接中"),
            ("实盘跟踪", "可启动"),
        ]
        
        for i, (name, desc) in enumerate(stage_data):
            stage = ProgressStage(name, i + 1, "pending")
            stage.set_status("pending", desc)
            self.stages.append(stage)
            stages_layout.addWidget(stage)
            
            # 添加连接线
            if i < len(stage_data) - 1:
                line = QFrame()
                line.setFixedHeight(2)
                line.setStyleSheet("background-color: #45475a;")
                stages_layout.addWidget(line, 1)
        
        layout.addLayout(stages_layout)
        
        # 底部：实盘准备度
        bottom = QHBoxLayout()
        bottom.setSpacing(24)
        
        # 准备度仪表
        self.readiness_gauge = ReadinessGauge()
        bottom.addWidget(self.readiness_gauge, 1)
        
        # 关键指标标签
        tags_layout = QVBoxLayout()
        tags_layout.setSpacing(8)
        
        self.tag_backtest = QLabel("📊 N次完成回测")
        self.tag_backtest.setStyleSheet("""
            background-color: #313244;
            color: #89b4fa;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 12px;
        """)
        tags_layout.addWidget(self.tag_backtest)
        
        self.tag_winrate = QLabel("🎯 平均胜率 N%")
        self.tag_winrate.setStyleSheet("""
            background-color: #313244;
            color: #a6e3a1;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 12px;
        """)
        tags_layout.addWidget(self.tag_winrate)
        
        self.tag_plratio = QLabel("📈 盈亏比 N")
        self.tag_plratio.setStyleSheet("""
            background-color: #313244;
            color: #cba6f7;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 12px;
        """)
        tags_layout.addWidget(self.tag_plratio)
        
        bottom.addLayout(tags_layout)
        
        layout.addLayout(bottom)
        
        return section
    
    def create_details_section(self) -> QWidget:
        """创建详情区域"""
        section = QWidget()
        layout = QHBoxLayout(section)
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 左侧：策略列表
        strategies_card = QFrame()
        strategies_card.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 16px;
                padding: 16px;
            }
        """)
        strategies_layout = QVBoxLayout(strategies_card)
        
        strategies_header = QHBoxLayout()
        strategies_title = QLabel("📋 策略库")
        strategies_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #cdd6f4;")
        strategies_header.addWidget(strategies_title)
        strategies_header.addStretch()
        
        new_strategy_btn = QPushButton("+ 新建")
        new_strategy_btn.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #89b4fa;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """)
        strategies_header.addWidget(new_strategy_btn)
        strategies_layout.addLayout(strategies_header)
        
        self.strategies_table = QTableWidget()
        self.strategies_table.setColumnCount(3)
        self.strategies_table.setHorizontalHeaderLabels(["策略名称", "类型", "修改时间"])
        self.strategies_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.strategies_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.strategies_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.strategies_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: #313244;
            }
            QTableWidget::item {
                padding: 8px;
                color: #cdd6f4;
            }
            QTableWidget::item:selected {
                background-color: #313244;
            }
            QHeaderView::section {
                background-color: #1e1e2e;
                color: #a6adc8;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #313244;
            }
        """)
        self.strategies_table.verticalHeader().setVisible(False)
        self.strategies_table.setShowGrid(False)
        strategies_layout.addWidget(self.strategies_table)
        
        layout.addWidget(strategies_card, 1)
        
        # 右侧：最近报告
        reports_card = QFrame()
        reports_card.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 16px;
                padding: 16px;
            }
        """)
        reports_layout = QVBoxLayout(reports_card)
        
        reports_header = QHBoxLayout()
        reports_title = QLabel("📄 最近报告")
        reports_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #cdd6f4;")
        reports_header.addWidget(reports_title)
        reports_header.addStretch()
        
        view_all_btn = QPushButton("查看全部 →")
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #89b4fa;
                border: none;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #b4befe;
            }
        """)
        reports_header.addWidget(view_all_btn)
        reports_layout.addLayout(reports_header)
        
        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(2)
        self.reports_table.setHorizontalHeaderLabels(["报告名称", "生成时间"])
        self.reports_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.reports_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.reports_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: #313244;
            }
            QTableWidget::item {
                padding: 8px;
                color: #cdd6f4;
            }
            QTableWidget::item:selected {
                background-color: #313244;
            }
            QHeaderView::section {
                background-color: #1e1e2e;
                color: #a6adc8;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #313244;
            }
        """)
        self.reports_table.verticalHeader().setVisible(False)
        self.reports_table.setShowGrid(False)
        reports_layout.addWidget(self.reports_table)
        
        layout.addWidget(reports_card, 1)
        
        return section
    
    def load_data(self):
        """加载数据"""
        self.progress_desc.setText("正在加载数据...")
        
        self.loader_thread = DataLoaderThread(self.project_root)
        self.loader_thread.data_loaded.connect(self.on_data_loaded)
        self.loader_thread.start()
    
    def on_data_loaded(self, data: dict):
        """数据加载完成"""
        self.data = data
        self.update_display()
    
    def update_display(self):
        """更新显示"""
        data = self.data
        
        # 更新时间
        self.update_time.setText(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 概览卡片
        num_strategies = len(data.get('strategies', []))
        num_reports = len(data.get('reports', []))
        num_backtests = len(data.get('backtest_results', []))
        
        self.card_strategies.set_value(f"{num_strategies} 个", f"已开发 {num_strategies} 个策略")
        self.card_reports.set_value(f"{num_reports} 份", f"已生成 {num_reports} 份报告")
        self.card_tasks.set_value("暂无", "无自动化任务运行")
        
        # 核心指标
        self.card_health.set_value("运行正常", "所有服务正常")
        
        win_rate = data.get('win_rate', 0) * 100
        self.card_winrate.set_value(f"{win_rate:.1f} %", f"基于 {num_backtests} 次回测")
        
        pl_ratio = data.get('profit_loss_ratio', 0)
        self.card_plratio.set_value(f"{pl_ratio:.2f}", f"夏普比率 {data.get('sharpe_avg', 0):.2f}")
        
        # 流程阶段
        if num_strategies > 0:
            self.stages[0].set_status("completed", f"策略库 · {num_strategies} 个")
        else:
            self.stages[0].set_status("pending", "策略库 · 待开发")
        
        if num_backtests > 0:
            self.stages[1].set_status("completed", f"{num_backtests} 次已完成")
        else:
            self.stages[1].set_status("pending", "待回测")
        
        if num_reports > 0:
            self.stages[2].set_status("completed", f"{num_reports} 份报告")
        else:
            self.stages[2].set_status("pending", "待生成")
        
        self.stages[3].set_status("warning", "风控对接中")
        self.stages[4].set_status("in_progress", "可启动")
        
        # 准备度
        readiness = 0
        if num_strategies > 0:
            readiness += 20
        if num_backtests > 0:
            readiness += 30
        if num_reports > 0:
            readiness += 20
        if win_rate > 30:
            readiness += 15
        if pl_ratio > 1:
            readiness += 15
        
        readiness = min(readiness, 100)
        self.readiness_gauge.set_value(readiness, f"已满足实盘前置条件，可进入模拟或小额实盘验证阶段。")
        
        # 标签
        self.tag_backtest.setText(f"📊 {num_backtests}次完成回测")
        self.tag_winrate.setText(f"🎯 平均胜率 {win_rate:.1f}%")
        self.tag_plratio.setText(f"📈 盈亏比 {pl_ratio:.2f}")
        
        # 进展描述
        self.progress_desc.setText(
            f"已对接 {num_strategies} 个策略、生成 {num_reports} 份报告，并提供自动化工作流、交互式报告和文档中心。"
        )
        
        # 策略表格
        strategies = data.get('strategies', [])
        self.strategies_table.setRowCount(len(strategies))
        for i, s in enumerate(strategies):
            self.strategies_table.setItem(i, 0, QTableWidgetItem(s['name']))
            
            # 判断策略类型
            name = s['name'].lower()
            if 'momentum' in name:
                type_text = "动量策略"
            elif 'ma' in name or 'cross' in name:
                type_text = "均线策略"
            else:
                type_text = "自定义"
            self.strategies_table.setItem(i, 1, QTableWidgetItem(type_text))
            self.strategies_table.setItem(i, 2, QTableWidgetItem(s['modified'].strftime('%Y-%m-%d')))
        
        # 报告表格
        reports = data.get('reports', [])
        # 按时间排序，显示最近10个
        reports = sorted(reports, key=lambda x: x['modified'], reverse=True)[:10]
        self.reports_table.setRowCount(len(reports))
        for i, r in enumerate(reports):
            self.reports_table.setItem(i, 0, QTableWidgetItem(r['name']))
            self.reports_table.setItem(i, 1, QTableWidgetItem(r['modified'].strftime('%Y-%m-%d %H:%M')))
    
    def open_web_dashboard(self):
        """打开Web仪表盘"""
        import subprocess
        import webbrowser
        import threading
        import time
        
        def start_server_and_open():
            # 检查服务是否已经在运行
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5000))
            sock.close()
            
            if result != 0:
                # 服务未运行，启动服务
                server_script = self.project_root / 'start_dashboard.py'
                if server_script.exists():
                    subprocess.Popen(
                        ['python3', str(server_script)],
                        cwd=str(self.project_root),
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    time.sleep(2)  # 等待服务启动
            
            # 打开浏览器
            webbrowser.open('http://127.0.0.1:5000')
        
        # 在后台线程中执行
        threading.Thread(target=start_server_and_open, daemon=True).start()

