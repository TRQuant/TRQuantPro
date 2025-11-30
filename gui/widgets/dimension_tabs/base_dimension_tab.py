# -*- coding: utf-8 -*-
"""
维度Tab基类

提供统一的布局和功能，各维度Tab继承并扩展
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QProgressBar, QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


class DimensionDataWorker(QThread):
    """维度数据获取线程"""
    
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, dimension: str, period: str = "medium", data_source: str = "akshare"):
        super().__init__()
        self.dimension = dimension
        self.period = period
        self.data_source = data_source
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
            
            fetcher = RealDataFetcher()
            engine = FiveDimensionEngine(data_source=self.data_source)
            
            # 检查数据源可用性
            if self.data_source == "jqdata":
                self.progress.emit("⚠️ 聚宽JQData待开通，当前使用AKShare数据...")
                # 暂时回退到AKShare
                engine.set_data_source("akshare")
            elif self.data_source == "wind":
                self.progress.emit("⚠️ 万德Wind待开通，当前使用AKShare数据...")
                # 暂时回退到AKShare
                engine.set_data_source("akshare")
            else:
                self.progress.emit(f"📡 使用{engine.data_source_config.get('name', 'AKShare')}数据源...")
            
            self.progress.emit("📡 正在获取数据...")
            
            # 获取数据
            sector_result = fetcher.fetch_sector_flow()
            sector_data = sector_result.data if sector_result.success else []
            
            concept_result = fetcher.fetch_concept_board()
            concept_data = concept_result.data if concept_result.success else []
            
            sentiment_result = fetcher.fetch_market_sentiment()
            limit_up_data = sentiment_result.data if sentiment_result.success else {}
            
            lhb_result = fetcher.fetch_dragon_tiger()
            lhb_data = lhb_result.data if lhb_result.success else []
            
            north_result = fetcher.fetch_northbound_flow()
            north_data = north_result.data if north_result.success else {}
            
            self.progress.emit("🔄 正在计算评分...")
            
            results = engine.calculate(
                sector_data=sector_data,
                concept_data=concept_data,
                limit_up_data=limit_up_data,
                lhb_data=lhb_data,
                northbound_data=north_data,
                period=self.period,
            )
            
            # 按该维度排序
            dim_attr = f"{self.dimension}_score"
            sorted_results = sorted(
                results,
                key=lambda x: getattr(x, dim_attr).score,
                reverse=True
            )
            
            self.finished.emit(sorted_results)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))


class BaseDimensionTab(QWidget):
    """维度Tab基类"""
    
    # 子类需要覆盖的属性
    DIMENSION_KEY = ""  # funds/heat/momentum/policy/leader
    DIMENSION_NAME = ""
    DIMENSION_ICON = ""
    DIMENSION_COLOR = ""
    DIMENSION_WEIGHT = 0.0
    DIMENSION_DESC = ""
    FACTORS = []  # [{"name": "", "weight": 0.0, "desc": ""}]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []
        self.worker = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 顶部介绍区
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
            QProgressBar::chunk {{ background-color: {self.DIMENSION_COLOR}; border-radius: 4px; }}
        """)
        progress_layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_frame)
        
        # 因子说明
        factors_frame = self._create_factors_section()
        layout.addWidget(factors_frame)
        
        # 工具区（子类可扩展）
        tools_frame = self._create_tools_section()
        if tools_frame:
            layout.addWidget(tools_frame)
        
        # 排名表格
        table_frame = self._create_table_section()
        layout.addWidget(table_frame)
    
    def _create_intro_section(self) -> QFrame:
        """创建介绍区"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.DIMENSION_COLOR}25,
                    stop:1 {Colors.BG_TERTIARY});
                border-left: 4px solid {self.DIMENSION_COLOR};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)
        
        # 标题行
        header = QHBoxLayout()
        
        title = QLabel(f"{self.DIMENSION_ICON} {self.DIMENSION_NAME}")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        header.addWidget(title)
        
        weight_label = QLabel(f"权重 {self.DIMENSION_WEIGHT*100:.0f}%")
        weight_label.setStyleSheet(f"""
            font-size: 12px; font-weight: 600;
            color: {self.DIMENSION_COLOR};
            background-color: {self.DIMENSION_COLOR}20;
            padding: 4px 10px;
            border-radius: 10px;
        """)
        header.addWidget(weight_label)
        
        header.addStretch()
        layout.addLayout(header)
        
        # 描述
        desc = QLabel(self.DIMENSION_DESC)
        desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        return frame
    
    def _create_control_section(self) -> QFrame:
        """创建控制栏"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # 数据源选择
        source_label = QLabel("数据源:")
        source_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(source_label)
        
        self.source_combo = QComboBox()
        # 从引擎获取可用数据源
        self.source_map = {}  # 存储索引到数据源类型的映射
        try:
            from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
            engine = FiveDimensionEngine()
            sources = engine.get_available_data_sources()
            for idx, source in enumerate(sources):
                self.source_combo.addItem(f"{source['name']} - {source['status']}")
                self.source_map[idx] = source['type']
        except:
            # 默认选项
            self.source_combo.addItems([
                "AKShare（免费） - ✅ 已启用",
                "聚宽JQData（付费） - ⏳ 待开通",
                "万德Wind（机构级） - ⏳ 待开通",
            ])
            self.source_map = {0: "akshare", 1: "jqdata", 2: "wind"}
        
        self.source_combo.setCurrentIndex(0)  # 默认AKShare
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
        
        # 周期选择
        period_label = QLabel("分析周期:")
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
                min-width: 100px;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.period_combo)
        
        layout.addStretch()
        
        # 刷新按钮
        self.refresh_btn = QPushButton(f"🔄 刷新{self.DIMENSION_NAME}数据")
        self.refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.DIMENSION_COLOR};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 11px;
                font-weight: 600;
            }}
            QPushButton:hover {{ background-color: {self.DIMENSION_COLOR}DD; }}
            QPushButton:disabled {{ background-color: {Colors.BG_TERTIARY}; color: {Colors.TEXT_MUTED}; }}
        """)
        self.refresh_btn.clicked.connect(self._start_refresh)
        layout.addWidget(self.refresh_btn)
        
        return frame
    
    def _create_factors_section(self) -> QFrame:
        """创建因子说明区"""
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
        
        title = QLabel("📊 评分因子")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # 因子列表
        factors_grid = QHBoxLayout()
        factors_grid.setSpacing(8)
        
        for factor in self.FACTORS:
            factor_frame = QFrame()
            factor_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {self.DIMENSION_COLOR}30;
                    border-radius: 6px;
                }}
            """)
            factor_layout = QVBoxLayout(factor_frame)
            factor_layout.setContentsMargins(10, 8, 10, 8)
            factor_layout.setSpacing(4)
            
            # 因子名称和权重
            header = QHBoxLayout()
            name_label = QLabel(factor["name"])
            name_label.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            header.addWidget(name_label)
            
            weight_label = QLabel(f"{factor['weight']*100:.0f}%")
            weight_label.setStyleSheet(f"font-size: 10px; color: {self.DIMENSION_COLOR}; font-weight: 600;")
            header.addWidget(weight_label)
            header.addStretch()
            factor_layout.addLayout(header)
            
            # 因子描述
            desc_label = QLabel(factor["desc"])
            desc_label.setStyleSheet(f"font-size: 9px; color: {Colors.TEXT_MUTED};")
            desc_label.setWordWrap(True)
            factor_layout.addWidget(desc_label)
            
            factors_grid.addWidget(factor_frame)
        
        layout.addLayout(factors_grid)
        
        return frame
    
    def _create_tools_section(self) -> Optional[QFrame]:
        """创建工具区 - 子类可覆盖扩展"""
        return None
    
    def _create_table_section(self) -> QFrame:
        """创建排名表格区"""
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
        
        title = QLabel(f"🏆 {self.DIMENSION_NAME}维度排名")
        title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "排名", "主线名称", "类型", f"{self.DIMENSION_NAME}得分", 
            "因子详情", "原始数据", "综合得分"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet(f"""
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
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_MUTED};
                padding: 8px;
                border: none;
                font-weight: 600;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.table)
        
        return frame
    
    def _start_refresh(self):
        """开始刷新数据"""
        if self.worker and self.worker.isRunning():
            return
        
        # 获取数据源
        idx = self.source_combo.currentIndex()
        data_source = self.source_map.get(idx, "akshare")
        if not data_source:
            # 从文本解析（备用方案）
            text = self.source_combo.currentText()
            if "AKShare" in text or "akshare" in text.lower():
                data_source = "akshare"
            elif "JQData" in text or "jqdata" in text.lower() or "聚宽" in text:
                data_source = "jqdata"
            elif "Wind" in text or "wind" in text.lower() or "万德" in text:
                data_source = "wind"
            else:
                data_source = "akshare"  # 默认
        
        period_map = {0: "short", 1: "medium", 2: "long"}
        period = period_map.get(self.period_combo.currentIndex(), "medium")
        
        self.refresh_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        
        self.worker = DimensionDataWorker(self.DIMENSION_KEY, period, data_source)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()
    
    def _on_progress(self, message: str):
        self.progress_label.setText(message)
    
    def _on_finished(self, results: list):
        self.results = results
        self.refresh_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        self._update_table()
    
    def _on_error(self, error: str):
        self.refresh_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        QMessageBox.warning(self, "错误", f"数据获取失败: {error}")
    
    def _update_table(self):
        """更新表格"""
        self.table.setRowCount(min(20, len(self.results)))
        
        for i, result in enumerate(self.results[:20]):
            dim_score = getattr(result, f"{self.DIMENSION_KEY}_score")
            
            # 排名
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            
            # 名称
            self.table.setItem(i, 1, QTableWidgetItem(result.name))
            
            # 类型
            self.table.setItem(i, 2, QTableWidgetItem(result.type))
            
            # 维度得分
            score_item = QTableWidgetItem(f"{dim_score.score:.1f}")
            self.table.setItem(i, 3, score_item)
            
            # 因子详情
            factors_text = ", ".join([f"{f['name']}:{f['score']:.0f}" for f in dim_score.factors[:2]])
            self.table.setItem(i, 4, QTableWidgetItem(factors_text))
            
            # 原始数据
            raw_data = self._get_raw_data_text(result)
            self.table.setItem(i, 5, QTableWidgetItem(raw_data))
            
            # 综合得分
            self.table.setItem(i, 6, QTableWidgetItem(f"{result.total_score:.1f}"))
    
    def _get_raw_data_text(self, result) -> str:
        """获取原始数据文本 - 子类可覆盖"""
        return f"{result.change_pct:+.2f}%, {result.net_inflow:+.2f}亿"

