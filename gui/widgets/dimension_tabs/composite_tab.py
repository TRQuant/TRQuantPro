# -*- coding: utf-8 -*-
"""
综合评分Tab（专业投资主线）

汇总五维评分，提供雷达图对比和多周期切换
"""

import logging
import json
import webbrowser
import subprocess
import sys
import io
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QProgressBar, QComboBox, QMessageBox,
    QCheckBox, QSplitter, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QPixmap

# Plotly雷达图（已迁移）
try:
    import plotly.graph_objects as go
    from gui.widgets.plotly_chart_widget import PlotlyChartWidget, PlotlyChartFactory
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("Plotly未安装，雷达图功能不可用")

# 保留Matplotlib作为备用（逐步迁移）
import matplotlib
matplotlib.use('Agg')  # 非GUI后端
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import io

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


# 雷达图颜色配置
RADAR_COLORS = [
    "#3B82F6",   # 蓝色
    "#EF4444",   # 红色
    "#10B981",   # 绿色
    "#F59E0B",   # 橙色
    "#8B5CF6",   # 紫色
    "#EC4899",   # 粉色
    "#14B8A6",   # 青色
    "#F97316",   # 橘色
]


class CompositeWorker(QThread):
    """综合评分计算线程"""
    
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, period: str = "medium", data_source: str = "akshare"):
        super().__init__()
        self.period = period
        self.data_source = data_source
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
            
            fetcher = RealDataFetcher()
            engine = FiveDimensionEngine(data_source=self.data_source)
            
            if self.data_source == "jqdata":
                self.progress.emit("⚠️ 聚宽JQData待开通，当前使用AKShare数据...")
                engine.set_data_source("akshare")
            elif self.data_source == "wind":
                self.progress.emit("⚠️ 万德Wind待开通，当前使用AKShare数据...")
                engine.set_data_source("akshare")
            else:
                self.progress.emit(f"📡 使用{engine.data_source_config.get('name', 'AKShare')}数据源...")
            
            self.progress.emit("📡 获取行业板块数据...")
            sector_result = fetcher.fetch_sector_flow()
            sector_data = sector_result.data if sector_result.success else []
            
            self.progress.emit("📡 获取概念板块数据...")
            concept_result = fetcher.fetch_concept_board()
            concept_data = concept_result.data if concept_result.success else []
            
            self.progress.emit("📡 获取市场情绪数据...")
            sentiment_result = fetcher.fetch_market_sentiment()
            limit_up_data = sentiment_result.data if sentiment_result.success else {}
            
            self.progress.emit("📡 获取龙虎榜数据...")
            lhb_result = fetcher.fetch_dragon_tiger()
            lhb_data = lhb_result.data if lhb_result.success else []
            
            self.progress.emit("📡 获取北向资金数据...")
            north_result = fetcher.fetch_northbound_flow()
            north_data = north_result.data if north_result.success else {}
            
            self.progress.emit("🔄 计算五维综合评分...")
            results = engine.calculate(
                sector_data=sector_data,
                concept_data=concept_data,
                limit_up_data=limit_up_data,
                lhb_data=lhb_data,
                northbound_data=north_data,
                period=self.period,
            )
            
            self.finished.emit(results)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))


class CompositeDimensionTab(QWidget):
    """综合评分Tab"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []
        self.worker = None
        self.report_path = None
        self.selected_indices = set()
        self.checkboxes = []
        self._cached_data = None  # 缓存上次结果
        self.table_frame = None  # 初始化表格框架引用
        self.table = None  # 表格控件引用
        self.setup_ui()
        
        # 立即加载缓存（setup_ui已完成）
        self._load_cached_results()
    
    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 整个页面可滚动
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                background-color: {Colors.BG_SECONDARY};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Colors.BORDER_LIGHT};
                border-radius: 5px;
                min-height: 40px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {Colors.PRIMARY};
            }}
        """)
        
        # 滚动内容
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 顶部介绍
        intro_frame = self._create_intro_section()
        layout.addWidget(intro_frame)
        
        # 控制栏
        control_frame = self._create_control_section()
        layout.addWidget(control_frame)
        
        # 进度条
        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        progress_layout = QVBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.progress_label = QLabel("准备中...")
        self.progress_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{ background-color: {Colors.BG_TERTIARY}; border: none; border-radius: 4px; height: 6px; }}
            QProgressBar::chunk {{ background-color: {Colors.PRIMARY}; border-radius: 4px; }}
        """)
        progress_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_frame)
        
        # 五维权重说明
        weights_frame = self._create_weights_section()
        layout.addWidget(weights_frame)
        
        # 雷达图区域（水平分割）
        radar_section = QFrame()
        radar_section.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        radar_layout = QHBoxLayout(radar_section)
        radar_layout.setContentsMargins(12, 10, 12, 10)
        radar_layout.setSpacing(16)
        
        # 左侧：雷达图
        self.radar_frame = self._create_radar_content()
        radar_layout.addWidget(self.radar_frame, 3)
        
        # 右侧：图例和详情
        self.details_frame = self._create_details_content()
        radar_layout.addWidget(self.details_frame, 2)
        
        layout.addWidget(radar_section)
        
        # 排名表格容器
        self.table_container = QFrame()
        self.table_container.setLayout(QVBoxLayout())
        self.table_container.layout().setContentsMargins(0, 0, 0, 0)
        self.table_container.layout().setSpacing(0)
        
        # 初始显示空状态
        self.table_frame = self._create_table_section_empty()
        self.table_container.layout().addWidget(self.table_frame)
        
        layout.addWidget(self.table_container)
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
    
    def _create_intro_section(self) -> QFrame:
        """创建介绍区"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1E3A5F, stop:1 {Colors.BG_TERTIARY});
                border-left: 4px solid {Colors.PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)
        
        title = QLabel("🎯 专业投资主线（综合评分）")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        desc = QLabel("汇总资金、热度、动量、政策、龙头五大维度评分，生成综合主线排名。在表格中选择主线可在雷达图中对比各维度强弱。")
        desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        score_info = QLabel("💡 综合得分 = 资金×30% + 热度×20% + 动量×20% + 政策×15% + 龙头×15%")
        score_info.setStyleSheet(f"""
            font-size: 11px;
            color: {Colors.PRIMARY};
            background-color: {Colors.PRIMARY}15;
            padding: 6px 10px;
            border-radius: 6px;
            margin-top: 4px;
        """)
        layout.addWidget(score_info)
        
        return frame
    
    def _create_control_section(self) -> QFrame:
        """创建控制栏"""
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background-color: {Colors.BG_TERTIARY}; border-radius: 8px; }}")
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        
        source_label = QLabel("数据源:")
        source_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(source_label)
        
        self.source_combo = QComboBox()
        self.source_map = {}
        try:
            from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
            engine = FiveDimensionEngine()
            sources = engine.get_available_data_sources()
            for idx, source in enumerate(sources):
                self.source_combo.addItem(f"{source['name']} - {source['status']}")
                self.source_map[idx] = source['type']
        except:
            self.source_combo.addItems([
                "AKShare（免费） - ✅ 已启用",
                "聚宽JQData（付费） - ⏳ 待开通",
                "万德Wind（机构级） - ⏳ 待开通",
            ])
            self.source_map = {0: "akshare", 1: "jqdata", 2: "wind"}
        self.source_combo.setCurrentIndex(0)
        self.source_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 180px;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.source_combo)
        
        period_label = QLabel("评分周期:")
        period_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(period_label)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["短期(3-5日)", "中期(15-30日)", "长期(60-180日)"])
        self.period_combo.setCurrentIndex(1)
        self.period_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 4px 8px;
                min-width: 120px;
            }}
        """)
        layout.addWidget(self.period_combo)
        
        layout.addStretch()
        
        self.calc_btn = QPushButton("🔄 计算综合评分")
        self.calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY_LIGHT}; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.calc_btn.clicked.connect(self._start_calculation)
        layout.addWidget(self.calc_btn)
        
        self.export_btn = QPushButton("📄 导出报告")
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {Colors.BG_TERTIARY}; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.export_btn.clicked.connect(self._export_report)
        layout.addWidget(self.export_btn)
        
        return frame
    
    def _create_weights_section(self) -> QFrame:
        """创建权重说明区"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        
        title = QLabel("📐 五维评分权重")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        weights_layout = QHBoxLayout()
        weights_layout.setSpacing(8)
        
        dimensions = [
            ("💰", "资金", "30%", "#3B82F6"),
            ("🔥", "热度", "20%", "#EF4444"),
            ("📈", "动量", "20%", "#10B981"),
            ("📜", "政策", "15%", "#8B5CF6"),
            ("👑", "龙头", "15%", "#F59E0B"),
        ]
        
        for icon, name, weight, color in dimensions:
            dim_frame = QFrame()
            dim_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {color}40;
                    border-radius: 6px;
                }}
            """)
            dim_layout = QHBoxLayout(dim_frame)
            dim_layout.setContentsMargins(10, 6, 10, 6)
            dim_layout.setSpacing(6)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 14px;")
            dim_layout.addWidget(icon_label)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            dim_layout.addWidget(name_label)
            
            weight_label = QLabel(weight)
            weight_label.setStyleSheet(f"font-size: 11px; color: {color}; font-weight: 600;")
            dim_layout.addWidget(weight_label)
            
            weights_layout.addWidget(dim_frame)
        
        layout.addLayout(weights_layout)
        return frame
    
    def _create_radar_content(self) -> QFrame:
        """创建雷达图内容区域"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 标题栏
        header_layout = QHBoxLayout()
        title = QLabel("📊 五维雷达图对比")
        title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.clear_btn = QPushButton("清除选择")
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {Colors.TEXT_MUTED};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 10px;
            }}
            QPushButton:hover {{ background-color: {Colors.BG_PRIMARY}; }}
        """)
        self.clear_btn.clicked.connect(self._clear_selection)
        header_layout.addWidget(self.clear_btn)
        
        layout.addLayout(header_layout)
        
        # 雷达图显示区 - 支持Plotly和Matplotlib两种模式
        # Plotly模式（优先）
        try:
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            self.radar_webview = QWebEngineView()
            self.radar_webview.setMinimumSize(600, 600)
            self.radar_webview.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.radar_webview.setHtml("<div style='color: white; text-align: center; padding: 50px;'>请先计算综合评分<br>然后在表格中选择要对比的主线</div>")
            self.use_plotly = True
        except ImportError:
            self.radar_webview = None
            self.use_plotly = False
        
        # Matplotlib模式（备用）
        self.radar_label = QLabel()
        self.radar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.radar_label.setMinimumSize(600, 600)
        self.radar_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.radar_label.setScaledContents(False)
        self.radar_label.setText("请先计算综合评分\n然后在表格中选择要对比的主线")
        self.radar_label.setStyleSheet(f"""
            QLabel {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                color: {Colors.TEXT_MUTED};
                font-size: 12px;
            }}
        """)
        
        # 根据模式选择显示组件
        if self.use_plotly and self.radar_webview:
            layout.addWidget(self.radar_webview)
        else:
            layout.addWidget(self.radar_label)
        layout.addWidget(self.radar_label)
        
        return frame
    
    def _create_details_content(self) -> QFrame:
        """创建详情内容区域"""
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 图例
        legend_title = QLabel("📌 选中主线")
        legend_title.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(legend_title)
        
        self.legend_frame = QFrame()
        self.legend_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
            }}
        """)
        self.legend_layout = QVBoxLayout(self.legend_frame)
        self.legend_layout.setContentsMargins(8, 8, 8, 8)
        self.legend_layout.setSpacing(4)
        
        self.legend_placeholder = QLabel("勾选表格中的主线...")
        self.legend_placeholder.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED}; padding: 10px;")
        self.legend_layout.addWidget(self.legend_placeholder)
        
        layout.addWidget(self.legend_frame)
        
        # 维度数值详情
        detail_title = QLabel("📋 各维度得分")
        detail_title.setStyleSheet(f"font-size: 12px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(detail_title)
        
        self.detail_frame = QFrame()
        self.detail_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
            }}
        """)
        self.detail_layout = QVBoxLayout(self.detail_frame)
        self.detail_layout.setContentsMargins(8, 8, 8, 8)
        self.detail_layout.setSpacing(4)
        
        self.detail_placeholder = QLabel("选择主线后显示详细得分")
        self.detail_placeholder.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED}; padding: 10px;")
        self.detail_layout.addWidget(self.detail_placeholder)
        
        layout.addWidget(self.detail_frame)
        layout.addStretch()
        
        return frame
    
    def _create_table_section_empty(self) -> QFrame:
        """创建空的表格区域"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        
        title = QLabel("🏆 综合排名 Top 20")
        title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        tip = QLabel("💡 勾选主线可在雷达图中对比各维度强弱（最多选8个）")
        tip.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED};")
        layout.addWidget(tip)
        
        placeholder = QLabel("点击「计算综合评分」开始分析...")
        placeholder.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 12px; padding: 40px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder, 1)
        
        return frame
    
    def _start_calculation(self):
        """开始计算"""
        if self.worker and self.worker.isRunning():
            return
        
        idx = self.source_combo.currentIndex()
        data_source = self.source_map.get(idx, "akshare")
        
        period_map = {0: "short", 1: "medium", 2: "long"}
        period = period_map.get(self.period_combo.currentIndex(), "medium")
        
        self.calc_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.selected_indices.clear()
        
        self.worker = CompositeWorker(period, data_source)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()
    
    def _on_progress(self, message: str):
        self.progress_label.setText(message)
    
    def _on_finished(self, results: list):
        self.results = results
        self.calc_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        self._update_table()
        
        # 保存综合评分结果，供候选池模块使用
        self._save_composite_scores(results)
        
        QMessageBox.information(
            self, "完成",
            f"综合评分计算完成！\n\n"
            f"• 共分析 {len(results)} 条主线\n"
            f"• 极强(≥80分): {sum(1 for r in results if r.total_score >= 80)} 条\n"
            f"• 强(≥65分): {sum(1 for r in results if 65 <= r.total_score < 80)} 条\n\n"
            f"💡 结果已保存，候选池模块可自动读取"
        )
    
    def _save_composite_scores(self, results: list):
        """
        保存综合评分结果，并映射到JQData写入MongoDB
        
        流程：
        1. 转换为可序列化格式
        2. 对Top20主线进行JQData映射
        3. 写入MongoDB统一管理
        4. 同时保存到文件作为备份
        """
        try:
            output_dir = Path.home() / ".local/share/trquant/reports/mainline"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 转换为可序列化的格式
            scores_data = []
            for r in results:
                # DimensionScore对象需要提取score属性
                def get_score_value(score_obj):
                    if hasattr(score_obj, 'score'):
                        return score_obj.score
                    elif isinstance(score_obj, (int, float)):
                        return float(score_obj)
                    return 0.0
                
                scores_data.append({
                    "name": r.name,
                    "total_score": float(r.total_score),
                    "funds_score": get_score_value(r.funds_score),
                    "heat_score": get_score_value(r.heat_score),
                    "momentum_score": get_score_value(r.momentum_score),
                    "policy_score": get_score_value(r.policy_score),
                    "leader_score": get_score_value(r.leader_score),
                    "leader_stock": str(r.leader_stock) if r.leader_stock else "",
                    "leader_change": float(r.leader_change) if r.leader_change else 0.0,
                    "signal": str(r.signal) if hasattr(r, 'signal') else "",
                    "mainline_type": str(r.type) if hasattr(r, 'type') else "concept",
                })
            
            # 按分数排序，取Top20
            scores_data.sort(key=lambda x: x['total_score'], reverse=True)
            top20 = scores_data[:20]
            
            # 映射到JQData并写入MongoDB
            self._map_and_save_to_mongodb(top20)
            
            data = {
                "timestamp": datetime.now().isoformat(),
                "period": self.period_combo.currentText(),
                "count": len(results),
                "scores": scores_data,
                "top20": top20,
                "high_score_mainlines": [r.name for r in results if r.total_score >= 65],
            }
            
            # 保存到文件（备份）
            json_path = output_dir / "latest_composite_scores.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 综合评分结果已保存到: {json_path}")
            
        except Exception as e:
            logger.error(f"保存综合评分失败: {e}")
    
    def _map_and_save_to_mongodb(self, top20_mainlines: list):
        """
        将Top20主线映射到JQData并写入MongoDB
        
        Args:
            top20_mainlines: Top20主线列表
        """
        try:
            from jqdata.client import JQDataClient
            from core.mainline_mapper import MainlineMapper
            from config.config_manager import get_config_manager
            from pymongo import MongoClient
            
            # 初始化JQData
            config_manager = get_config_manager()
            config = config_manager.get_jqdata_config()
            
            if not config.get('username') or not config.get('password'):
                logger.warning("⚠️ 未找到JQData配置，跳过映射")
                return
            
            jq_client = JQDataClient()
            if not jq_client.authenticate(config['username'], config['password']):
                logger.warning("⚠️ JQData认证失败，跳过映射")
                return
            
            # 创建映射器
            mapper = MainlineMapper(jq_client=jq_client)
            
            # 映射每个主线
            mapped_mainlines = []
            for mainline in top20_mainlines:
                name = mainline.get('name', '')
                if not name:
                    continue
                
                mapping = mapper.map_mainline(name, prefer_type='auto')
                
                mapped_data = {
                    **mainline,  # 保留原有评分数据
                    "jqdata_mapped": mapping is not None,
                    "jqdata_code": mapping.jqdata_code if mapping else None,
                    "jqdata_name": mapping.jqdata_name if mapping else None,
                    "jqdata_type": mapping.mapping_type if mapping else None,
                    "mapping_confidence": mapping.confidence if mapping else 0.0,
                    "mapping_method": mapping.match_method if mapping else None,
                }
                mapped_mainlines.append(mapped_data)
                
                if mapping:
                    logger.info(f"  ✅ {name} → {mapping.jqdata_name} ({mapping.mapping_type}, {mapping.confidence:.2f})")
                else:
                    logger.warning(f"  ⚠️ {name} → 未找到匹配")
            
            # 写入MongoDB
            try:
                client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
                client.server_info()
                db = client.jqquant
                
                # 保存到mainline_mapped集合
                collection = db.mainline_mapped
                doc = {
                    "timestamp": datetime.now().isoformat(),
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "period": self.period_combo.currentText(),
                    "mainlines": mapped_mainlines,
                    "mapped_count": sum(1 for m in mapped_mainlines if m.get('jqdata_mapped')),
                    "total_count": len(mapped_mainlines),
                }
                
                # 使用日期作为唯一键，更新或插入
                collection.replace_one(
                    {"date": doc["date"], "period": doc["period"]},
                    doc,
                    upsert=True
                )
                
                logger.info(f"✅ 已写入MongoDB: {doc['mapped_count']}/{doc['total_count']} 个主线映射成功")
                
                # 同时保存时间维度快照
                self._save_mainline_time_snapshot(mapped_mainlines, doc["period"])
                
            except Exception as e:
                logger.warning(f"⚠️ MongoDB写入失败: {e}，数据已保存到文件")
                
        except ImportError as e:
            logger.warning(f"⚠️ 模块导入失败: {e}，跳过JQData映射")
        except Exception as e:
            logger.error(f"JQData映射失败: {e}")
    
    def _save_mainline_time_snapshot(self, mainlines: list, period_text: str):
        """保存主线时间维度快照"""
        try:
            from core.time_dimension_manager import create_time_dimension_manager, Period
            
            # 映射周期文本到Period枚举
            period_map = {
                "短期 (1-5天)": Period.SHORT,
                "中期 (1-4周)": Period.MEDIUM, 
                "长期 (1月+)": Period.LONG,
                "short": Period.SHORT,
                "medium": Period.MEDIUM,
                "long": Period.LONG
            }
            period = period_map.get(period_text, Period.MEDIUM)
            
            # 获取市场背景（如果有趋势模块的数据）
            market_context = {}
            try:
                from core.trend_analyzer import create_trend_analyzer
                # 这里可以添加市场趋势信息
            except:
                pass
            
            # 保存快照
            tdm = create_time_dimension_manager()
            success = tdm.save_mainline_snapshot(
                mainlines=mainlines,
                period=period,
                rotation_signal=None,  # 可后续添加轮动信号
                market_context=market_context,
                source="composite_score"
            )
            
            if success:
                logger.info(f"✅ 主线时间维度快照已保存: {len(mainlines)} 条, 周期={period.value}")
                
        except Exception as e:
            logger.warning(f"保存主线时间维度快照失败: {e}")
    
    def _load_cached_results(self):
        """加载缓存的综合评分结果（初始化时自动调用）"""
        try:
            # 先尝试从MongoDB加载
            from pymongo import MongoClient
            
            client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
            client.server_info()  # 测试连接
            db = client.jqquant
            
            # 查找最新的主线映射记录
            latest = db.mainline_mapped.find_one(sort=[("timestamp", -1)])
            
            if latest:
                mainlines = latest.get("mainlines", [])
                period = latest.get("period", "")
                record_date = latest.get("date", "")
                timestamp = latest.get("timestamp", "")
                
                if mainlines:
                    logger.info(f"✅ 从MongoDB加载缓存: {len(mainlines)}个主线, 日期={record_date}, 周期={period}")
                    
                    # 转换为FiveDimensionResult格式用于显示
                    from markets.ashare.mainline.five_dimension_engine import FiveDimensionResult, DimensionScore
                    
                    self.results = []
                    for ml in mainlines:
                        result = FiveDimensionResult(
                            name=ml.get("name", ""),
                            type=ml.get("mainline_type", "concept"),
                            total_score=ml.get("total_score", 0),
                            funds_score=DimensionScore(score=ml.get("funds_score", 0)),
                            heat_score=DimensionScore(score=ml.get("heat_score", 0)),
                            momentum_score=DimensionScore(score=ml.get("momentum_score", 0)),
                            policy_score=DimensionScore(score=ml.get("policy_score", 0)),
                            leader_score=DimensionScore(score=ml.get("leader_score", 0)),
                            leader_stock=ml.get("leader_stock", ""),
                            leader_change=ml.get("leader_change", 0),
                            signal=ml.get("signal", "")
                        )
                        self.results.append(result)
                    
                    logger.info(f"✅ 解析出 {len(self.results)} 条结果")
                    
                    # 更新UI显示 - 替换空表格为有数据的表格
                    if self.results:
                        self._rebuild_table_with_cache()
                        self.status_label.setText(f"📂 已加载缓存 ({record_date} {period})")
                    return
            
        except Exception as e:
            logger.debug(f"MongoDB缓存加载失败: {e}")
        
        # 备选：从本地文件加载
        try:
            cache_file = Path.home() / ".local/share/trquant/reports/mainline/latest_composite_scores.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                scores = data.get("scores", [])
                period = data.get("period", "")
                timestamp = data.get("timestamp", "")
                
                if scores:
                    from markets.ashare.mainline.five_dimension_engine import FiveDimensionResult, DimensionScore
                    
                    self.results = []
                    for s in scores[:50]:  # 限制数量
                        result = FiveDimensionResult(
                            name=s.get("name", ""),
                            type=s.get("mainline_type", "concept"),
                            total_score=s.get("total_score", 0),
                            funds_score=DimensionScore(score=s.get("funds_score", 0)),
                            heat_score=DimensionScore(score=s.get("heat_score", 0)),
                            momentum_score=DimensionScore(score=s.get("momentum_score", 0)),
                            policy_score=DimensionScore(score=s.get("policy_score", 0)),
                            leader_score=DimensionScore(score=s.get("leader_score", 0)),
                            leader_stock=s.get("leader_stock", ""),
                            leader_change=s.get("leader_change", 0),
                            signal=s.get("signal", "")
                        )
                        self.results.append(result)
                    
                    if self.results:
                        self._update_table()
                        self.status_label.setText(f"📂 已加载本地缓存 ({timestamp[:10]} {period})")
                    
                    logger.info(f"✅ 从本地文件加载缓存: {len(self.results)}个主线")
                    
        except Exception as e:
            logger.debug(f"本地缓存加载失败: {e}")
    
    def _on_error(self, error: str):
        self.calc_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        QMessageBox.warning(self, "错误", f"计算失败: {error}")
    
    def _rebuild_table_with_cache(self):
        """重建表格显示缓存数据"""
        if not self.results:
            logger.debug("无数据，跳过表格重建")
            return
        
        try:
            # 清空容器
            layout = self.table_container.layout()
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # 创建新表格
            self.table_frame = self._create_table_section()
            layout.addWidget(self.table_frame)
            
            logger.info(f"✅ 缓存表格已重建: {len(self.results)} 条数据")
            
        except Exception as e:
            logger.error(f"重建表格失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_table(self):
        """更新表格"""
        if not self.results:
            return
        
        self._rebuild_table_with_cache()
    
    def _create_table_section(self) -> QFrame:
        """创建排名表格 - 添加更多指标列"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        
        header_layout = QHBoxLayout()
        title = QLabel("🏆 综合排名 Top 20")
        title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.select_top5_btn = QPushButton("选前5名")
        self.select_top5_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY}20;
                color: {Colors.PRIMARY};
                border: 1px solid {Colors.PRIMARY}40;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 10px;
            }}
            QPushButton:hover {{ background-color: {Colors.PRIMARY}30; }}
        """)
        self.select_top5_btn.clicked.connect(self._select_top5)
        header_layout.addWidget(self.select_top5_btn)
        
        layout.addLayout(header_layout)
        
        tip = QLabel("💡 勾选主线可在雷达图中对比各维度强弱（最多选8个）")
        tip.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED};")
        layout.addWidget(tip)
        
        # 表格 - 添加更多列：涨跌幅、净流入、龙头股、趋势
        self.table = QTableWidget()
        display_count = min(20, len(self.results))
        self.table.setRowCount(display_count)
        self.table.setColumnCount(16)  # 增加列数
        self.table.setHorizontalHeaderLabels([
            "选择", "排名", "主线名称", "类型", "综合得分", "等级", "信号",
            "💰资金", "🔥热度", "📈动量", "📜政策", "👑龙头",
            "涨跌幅", "净流入(亿)", "龙头股", "趋势"
        ])
        
        # 设置表格高度 - 确保20行都能显示
        row_height = 32  # 每行高度
        header_height = 36  # 表头高度
        total_height = header_height + (display_count * row_height) + 20  # 额外边距
        self.table.setMinimumHeight(total_height)
        
        # 设置行高
        for i in range(display_count):
            self.table.setRowHeight(i, row_height)
        
        # 设置列宽 - 主线名称列缩小
        self.table.setColumnWidth(0, 40)   # 选择
        self.table.setColumnWidth(1, 45)   # 排名
        self.table.setColumnWidth(2, 100)  # 主线名称（缩小）
        self.table.setColumnWidth(3, 60)   # 类型
        self.table.setColumnWidth(4, 70)   # 综合得分
        self.table.setColumnWidth(5, 50)   # 等级
        self.table.setColumnWidth(6, 50)   # 信号
        for col in range(7, 12):  # 五维得分
            self.table.setColumnWidth(col, 55)
        self.table.setColumnWidth(12, 70)  # 涨跌幅
        self.table.setColumnWidth(13, 90)  # 净流入
        self.table.setColumnWidth(14, 80)  # 龙头股
        self.table.setColumnWidth(15, 60)  # 趋势
        
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 6px 4px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 10px;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_MUTED};
                padding: 6px;
                border: none;
                font-weight: 600;
                font-size: 10px;
            }}
        """)
        
        self.checkboxes = []
        for i, result in enumerate(self.results[:20]):
            # 选择复选框
            checkbox = QCheckBox()
            checkbox.setStyleSheet(f"""
                QCheckBox::indicator {{
                    width: 16px; height: 16px;
                    border: 2px solid {Colors.BORDER_PRIMARY};
                    border-radius: 3px;
                    background-color: {Colors.BG_PRIMARY};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {Colors.PRIMARY};
                    border-color: {Colors.PRIMARY};
                }}
            """)
            checkbox.stateChanged.connect(lambda state, idx=i: self._on_checkbox_changed(idx, state))
            self.checkboxes.append(checkbox)
            
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.addWidget(checkbox)
            self.table.setCellWidget(i, 0, checkbox_widget)
            
            # 数据列
            self.table.setItem(i, 1, QTableWidgetItem(str(result.rank)))
            self.table.setItem(i, 2, QTableWidgetItem(result.name))
            self.table.setItem(i, 3, QTableWidgetItem(result.type))
            
            score_item = QTableWidgetItem(f"{result.total_score:.1f}")
            if result.total_score >= 80:
                score_item.setForeground(Qt.GlobalColor.red)
            elif result.total_score >= 65:
                score_item.setForeground(Qt.GlobalColor.yellow)
            self.table.setItem(i, 4, score_item)
            
            self.table.setItem(i, 5, QTableWidgetItem(result.level))
            self.table.setItem(i, 6, QTableWidgetItem(result.signal))
            
            # 五维得分
            self.table.setItem(i, 7, QTableWidgetItem(f"{result.funds_score.score:.0f}"))
            self.table.setItem(i, 8, QTableWidgetItem(f"{result.heat_score.score:.0f}"))
            self.table.setItem(i, 9, QTableWidgetItem(f"{result.momentum_score.score:.0f}"))
            self.table.setItem(i, 10, QTableWidgetItem(f"{result.policy_score.score:.0f}"))
            self.table.setItem(i, 11, QTableWidgetItem(f"{result.leader_score.score:.0f}"))
            
            # 新增指标列
            change_pct = result.change_pct if hasattr(result, 'change_pct') else 0.0
            change_item = QTableWidgetItem(f"{change_pct:+.2f}%")
            if change_pct > 0:
                change_item.setForeground(Qt.GlobalColor.red)
            elif change_pct < 0:
                change_item.setForeground(Qt.GlobalColor.green)
            self.table.setItem(i, 12, change_item)
            
            net_inflow = result.net_inflow if hasattr(result, 'net_inflow') else 0.0
            inflow_item = QTableWidgetItem(f"{net_inflow/100000000:.2f}")
            if net_inflow > 0:
                inflow_item.setForeground(Qt.GlobalColor.red)
            self.table.setItem(i, 13, inflow_item)
            
            leader_stock = result.leader_stock if hasattr(result, 'leader_stock') else "-"
            self.table.setItem(i, 14, QTableWidgetItem(leader_stock))
            
            trend = result.trend if hasattr(result, 'trend') else "unknown"
            trend_text = {"rising": "上升", "stable": "平稳", "falling": "下降", "unknown": "未知"}.get(trend, trend)
            self.table.setItem(i, 15, QTableWidgetItem(trend_text))
        
        layout.addWidget(self.table)
        return frame
    
    def _on_checkbox_changed(self, idx: int, state: int):
        """复选框状态变化"""
        if state == 2:
            if len(self.selected_indices) >= 8:
                self.checkboxes[idx].setChecked(False)
                QMessageBox.warning(self, "提示", "最多只能选择8个主线进行对比")
                return
            self.selected_indices.add(idx)
        else:
            self.selected_indices.discard(idx)
        
        self._update_radar_chart()
    
    def _select_top5(self):
        """选择前5名"""
        self.selected_indices.clear()
        for cb in self.checkboxes:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        
        for i in range(min(5, len(self.checkboxes))):
            self.checkboxes[i].blockSignals(True)
            self.checkboxes[i].setChecked(True)
            self.checkboxes[i].blockSignals(False)
            self.selected_indices.add(i)
        
        self._update_radar_chart()
    
    def _clear_selection(self):
        """清除所有选择"""
        self.selected_indices.clear()
        for cb in self.checkboxes:
            cb.blockSignals(True)
            cb.setChecked(False)
            cb.blockSignals(False)
        self._update_radar_chart()
    
    def _update_radar_chart(self):
        """更新雷达图（优先使用Plotly）"""
        if not self.results or not self.selected_indices:
            placeholder_text = "请在表格中选择要对比的主线\n（最多选择8个）"
            if self.use_plotly and self.radar_webview:
                self.radar_webview.setHtml(f"<div style='color: white; text-align: center; padding: 50px;'>{placeholder_text.replace(chr(10), '<br>')}</div>")
            else:
                self.radar_label.setText(placeholder_text)
                self.radar_label.setStyleSheet(f"""
                    QLabel {{
                        background-color: {Colors.BG_PRIMARY};
                        border: 1px solid {Colors.BORDER_PRIMARY};
                        border-radius: 8px;
                        color: {Colors.TEXT_MUTED};
                        font-size: 12px;
                    }}
                """)
            self.radar_pixmap = None
            self._update_legend([])
            self._update_detail([])
            return
        
        # 优先使用Plotly生成雷达图
        if self.use_plotly and PLOTLY_AVAILABLE:
            html_str = self._generate_radar_chart_plotly()
            if html_str:
                self.radar_webview.setHtml(html_str)
                self.radar_pixmap = None  # Plotly模式不使用pixmap
                # 更新图例和详情
                selected_results = [self.results[idx] for idx in sorted(self.selected_indices) if idx < len(self.results)]
                self._update_legend(selected_results)
                self._update_detail(selected_results)
                return
        
        # 降级到Matplotlib
        pixmap = self._generate_radar_chart()
        if pixmap:
            # 自适应窗口大小
            label_size = self.radar_label.size()
            target_size = min(label_size.width(), label_size.height(), 800)
            if target_size < 400:
                target_size = 600  # 最小显示尺寸
            
            scaled = pixmap.scaled(
                target_size, target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.radar_label.setPixmap(scaled)
            self.radar_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 8px;
                }}
            """)
        
        selected_results = [(idx, self.results[idx]) for idx in sorted(self.selected_indices) if idx < len(self.results)]
        self._update_legend(selected_results)
        self._update_detail(selected_results)
    
    def _generate_radar_chart_plotly(self) -> str:
        """使用Plotly生成雷达图HTML（交互式）"""
        if not PLOTLY_AVAILABLE:
            # 降级到Matplotlib
            pixmap = self._generate_radar_chart()
            # 将QPixmap转换为临时HTML（简单实现）
            return None
        
        try:
            categories = ['资金', '热度', '动量', '政策', '龙头']
            values_list = []
            series_names = []
            
            # 收集选中的主线数据
            for idx in sorted(self.selected_indices):
                if idx >= len(self.results):
                    continue
                    
                result = self.results[idx]
                values = [
                    result.funds_score.score if hasattr(result.funds_score, 'score') else result.funds_score,
                    result.heat_score.score if hasattr(result.heat_score, 'score') else result.heat_score,
                    result.momentum_score.score if hasattr(result.momentum_score, 'score') else result.momentum_score,
                    result.policy_score.score if hasattr(result.policy_score, 'score') else result.policy_score,
                    result.leader_score.score if hasattr(result.leader_score, 'score') else result.leader_score,
                ]
                values_list.append(values)
                series_names.append(result.name)
            
            if not values_list:
                return None
            
            # 使用PlotlyChartFactory创建雷达图
            fig = PlotlyChartFactory.create_radar_chart(
                categories=categories,
                values_list=values_list,
                series_names=series_names,
                title="五维评分雷达图"
            )
            
            # 应用颜色
            for i, trace in enumerate(fig.data):
                if i < len(RADAR_COLORS):
                    trace.line.color = RADAR_COLORS[i]
                    # 设置填充颜色（带透明度）
                    import re
                    color_hex = RADAR_COLORS[i].lstrip('#')
                    trace.fillcolor = f'rgba({int(color_hex[0:2], 16)}, {int(color_hex[2:4], 16)}, {int(color_hex[4:6], 16)}, 0.25)'
            
            # 生成HTML
            import plotly.offline as pyo
            html_str = pyo.plot(fig, output_type='div', include_plotlyjs='cdn')
            
            return html_str
            
        except Exception as e:
            logger.error(f"生成Plotly雷达图失败: {e}")
            import traceback
            traceback.print_exc()
            return None


    def _generate_radar_chart(self) -> QPixmap:
        """使用matplotlib生成雷达图（稳定可靠）"""
        try:
            # 维度标签（英文+中文符号，确保兼容性）
            categories = ['Funds\n资金', 'Heat\n热度', 'Momentum\n动量', 'Policy\n政策', 'Leader\n龙头']
            N = len(categories)
            
            # 计算角度
            angles = [n / float(N) * 2 * np.pi for n in range(N)]
            angles += angles[:1]  # 闭合
            
            # 创建图形 - 深色背景
            fig = Figure(figsize=(8, 8), dpi=100, facecolor='#0d0d14')
            ax = fig.add_subplot(111, polar=True, facecolor='#0d0d14')
            
            # 使用Noto Sans CJK字体（支持中日韩文字）
            import matplotlib.font_manager as fm
            
            # 强制使用CJK字体
            cjk_fonts = ['Noto Sans CJK JP', 'Noto Sans CJK SC', 'Noto Sans CJK TC', 
                        'WenQuanYi Micro Hei', 'SimHei', 'Microsoft YaHei']
            
            for font_name in cjk_fonts:
                try:
                    matching = [f for f in fm.fontManager.ttflist if font_name in f.name]
                    if matching:
                        plt.rcParams['font.family'] = 'sans-serif'
                        plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
                        categories = ['资金', '热度', '动量', '政策', '龙头']  # 纯中文
                        logger.info(f"雷达图使用字体: {font_name}")
                        break
                except:
                    continue
            
            plt.rcParams['axes.unicode_minus'] = False
            
            # 绘制每个选中的主线
            for i, idx in enumerate(sorted(self.selected_indices)):
                if idx >= len(self.results):
                    continue
                    
                result = self.results[idx]
                values = [
                    result.funds_score.score if hasattr(result.funds_score, 'score') else result.funds_score,
                    result.heat_score.score if hasattr(result.heat_score, 'score') else result.heat_score,
                    result.momentum_score.score if hasattr(result.momentum_score, 'score') else result.momentum_score,
                    result.policy_score.score if hasattr(result.policy_score, 'score') else result.policy_score,
                    result.leader_score.score if hasattr(result.leader_score, 'score') else result.leader_score,
                ]
                values += values[:1]  # 闭合
                
                color = RADAR_COLORS[i % len(RADAR_COLORS)]
                
                # 绘制线条和填充
                ax.plot(angles, values, 'o-', linewidth=2.5, label=result.name, color=color, markersize=6)
                ax.fill(angles, values, alpha=0.25, color=color)
            
            # 设置角度标签
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories, fontsize=14, color='#ffffff', fontweight='bold')
            
            # 设置径向刻度
            ax.set_ylim(0, 100)
            ax.set_yticks([20, 40, 60, 80, 100])
            ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=10, color='#aaaaaa')
            
            # 设置网格线颜色
            ax.spines['polar'].set_color('#3a3a5a')
            ax.grid(color='#2a2a4a', linestyle='-', linewidth=0.5)
            
            # 添加图例
            if len(self.selected_indices) > 0:
                legend = ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), 
                                   fontsize=10, facecolor='#1a1a2e', edgecolor='#3a3a5a',
                                   labelcolor='#ffffff')
            
            # 调整布局
            fig.tight_layout(pad=2.0)
            
            # 转换为QPixmap
            canvas = FigureCanvasAgg(fig)
            canvas.draw()
            
            # 获取图像数据
            buf = io.BytesIO()
            fig.savefig(buf, format='png', facecolor='#0d0d14', edgecolor='none', 
                       bbox_inches='tight', pad_inches=0.5)
            buf.seek(0)
            
            # 创建QPixmap
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            
            # 关闭图形释放内存
            plt.close(fig)
            
            return pixmap
            
        except Exception as e:
            logger.error(f"生成雷达图失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _update_legend(self, selected_results):
        """更新图例"""
        while self.legend_layout.count():
            item = self.legend_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not selected_results:
            placeholder = QLabel("勾选表格中的主线...")
            placeholder.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED}; padding: 10px;")
            self.legend_layout.addWidget(placeholder)
            return
        
        for i, (idx, result) in enumerate(selected_results):
            color = RADAR_COLORS[i % len(RADAR_COLORS)]
            item = QLabel(f"● {result.name} ({result.total_score:.1f})")
            item.setStyleSheet(f"color: {color}; font-size: 10px; padding: 2px 0;")
            self.legend_layout.addWidget(item)
    
    def _update_detail(self, selected_results):
        """更新详情"""
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not selected_results:
            placeholder = QLabel("选择主线后显示详细得分")
            placeholder.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED}; padding: 10px;")
            self.detail_layout.addWidget(placeholder)
            return
        
        for i, (idx, result) in enumerate(selected_results):
            color = RADAR_COLORS[i % len(RADAR_COLORS)]
            text = (f"【{result.name}】\n"
                   f"💰{result.funds_score.score:.0f} "
                   f"🔥{result.heat_score.score:.0f} "
                   f"📈{result.momentum_score.score:.0f} "
                   f"📜{result.policy_score.score:.0f} "
                   f"👑{result.leader_score.score:.0f}")
            
            item = QLabel(text)
            item.setStyleSheet(f"""
                font-size: 10px;
                color: {Colors.TEXT_SECONDARY};
                background-color: {color}10;
                border-left: 2px solid {color};
                padding: 4px 6px;
                border-radius: 4px;
                margin: 2px 0;
            """)
            self.detail_layout.addWidget(item)
    
    def _export_report(self):
        """导出报告"""
        if not self.results:
            QMessageBox.warning(self, "提示", "请先计算综合评分")
            return
        
        try:
            output_dir = Path.home() / ".local/share/trquant/reports/mainline/composite"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = output_dir / f"composite_report_{timestamp}.html"
            
            html = self._generate_html_report()
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html)
            
            self.report_path = str(filepath)
            
            webbrowser.open(f"file://{filepath}")
            
            if sys.platform == "linux":
                subprocess.run(["xdg-open", str(output_dir)], check=False)
            
            QMessageBox.information(self, "导出成功", f"报告已保存到:\n{filepath}")
            
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"导出失败: {e}")
    
    def _generate_html_report(self) -> str:
        """生成HTML报告"""
        rows = ""
        for r in self.results[:20]:
            net_inflow = r.net_inflow / 100000000 if hasattr(r, 'net_inflow') else 0.0
            rows += f"""
            <tr>
                <td>{r.rank}</td>
                <td><strong>{r.name}</strong></td>
                <td>{r.type}</td>
                <td class="score">{r.total_score:.1f}</td>
                <td>{r.level}</td>
                <td>{r.signal}</td>
                <td>{r.funds_score.score:.0f}</td>
                <td>{r.heat_score.score:.0f}</td>
                <td>{r.momentum_score.score:.0f}</td>
                <td>{r.policy_score.score:.0f}</td>
                <td>{r.leader_score.score:.0f}</td>
                <td>{r.change_pct:+.2f}%</td>
                <td>{net_inflow:.2f}</td>
            </tr>"""
        
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>综合评分报告 - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; background: #161b22; border-radius: 8px; overflow: hidden; }}
        th {{ background: #21262d; color: #8b949e; padding: 12px; text-align: left; font-size: 12px; }}
        td {{ padding: 10px 12px; border-top: 1px solid #30363d; font-size: 13px; }}
        tr:hover {{ background: #1f2428; }}
        .score {{ font-weight: bold; color: #58a6ff; }}
    </style>
</head>
<body>
<div class="container">
    <h1>🎯 综合评分报告</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <tr>
            <th>排名</th><th>主线</th><th>类型</th><th>综合分</th><th>等级</th><th>信号</th>
            <th>💰资金</th><th>🔥热度</th><th>📈动量</th><th>📜政策</th><th>👑龙头</th>
            <th>涨跌幅</th><th>净流入(亿)</th>
        </tr>
        {rows}
    </table>
</div>
</body>
</html>"""
