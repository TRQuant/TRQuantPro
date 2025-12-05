# -*- coding: utf-8 -*-
"""
集成热度评分面板

================================================================================
                        与主线识别的衔接关系
================================================================================

主线识别(5维度)                    热度评分(5因子)
├── 资金维度 (25%)  ←───────────── 资金流入强度 (25%)
├── 动量维度 (20%)  ←───────────── 涨跌幅强度 (25%)
├── 热度维度 (20%)  ←─ 本模块输出 ← 涨停数+龙虎榜 (35%)
├── 政策维度 (20%)  (需LLM分析)
└── 龙头维度 (15%)  ←───────────── 龙头股强度 (15%)

热度评分 → 主线识别"热度维度" → 综合评分 → 个股筛选

================================================================================
                           数据流向个股筛选
================================================================================

热度评分结果 → 保存到 reports/heatmap/ → 个股筛选模块读取 → 
    → 筛选高热度主线内的个股
    → 按"所属主线热度 × 15%"加权
    → 输出个股推荐列表

================================================================================
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QGroupBox, QComboBox, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QFont, QColor, QDesktopServices
from datetime import datetime
from typing import Dict, List, Optional
import logging
import webbrowser
import subprocess
import sys
import json
from pathlib import Path

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


# ============================================================
# 5因子模型配置 - 完整展示
# ============================================================

HEAT_FACTORS_CONFIG = [
    {
        "id": "change",
        "name": "涨跌幅强度",
        "icon": "📈",
        "weight": 25,
        "color": "#10b981",
        "data_source": "同花顺 stock_fund_flow_industry",
        "api_field": "行业-涨跌幅",
        "calculation": "涨跌幅排名百分位 × 100",
        "interpretation": "涨幅越高，市场资金关注度越高",
        "to_mainline": "→ 主线识别[动量维度]",
    },
    {
        "id": "flow",
        "name": "资金流入强度",
        "icon": "💰",
        "weight": 25,
        "color": "#3b82f6",
        "data_source": "同花顺 stock_fund_flow_industry",
        "api_field": "净额（亿元）",
        "calculation": "净流入排名百分位 × 100",
        "interpretation": "资金净流入越多，机构认可度越高",
        "to_mainline": "→ 主线识别[资金维度]",
    },
    {
        "id": "limit_up",
        "name": "涨停板数量",
        "icon": "🔥",
        "weight": 20,
        "color": "#ef4444",
        "data_source": "东方财富 stock_zt_pool_em",
        "api_field": "涨停股数量/连板数",
        "calculation": "板块涨停数 / 全市场涨停数 × 100",
        "interpretation": "涨停股越多，板块炒作热度越高",
        "to_mainline": "→ 主线识别[热度维度]",
    },
    {
        "id": "lhb",
        "name": "龙虎榜活跃度",
        "icon": "🐉",
        "weight": 15,
        "color": "#f97316",
        "data_source": "东方财富 stock_lhb_detail_em",
        "api_field": "龙虎榜上榜次数",
        "calculation": "板块龙虎榜数 / 全市场龙虎榜数 × 100",
        "interpretation": "龙虎榜越多，游资参与度越高",
        "to_mainline": "→ 主线识别[热度维度]",
    },
    {
        "id": "leader",
        "name": "龙头股强度",
        "icon": "👑",
        "weight": 15,
        "color": "#8b5cf6",
        "data_source": "同花顺 stock_fund_flow_industry",
        "api_field": "领涨股-涨跌幅",
        "calculation": "龙头涨幅排名百分位 × 100",
        "interpretation": "龙头越强，板块带动效应越强",
        "to_mainline": "→ 主线识别[龙头维度]",
    },
]


# ============================================================
# 数据获取工作线程
# ============================================================

class IntegratedHeatmapWorker(QThread):
    """集成热度数据获取工作线程"""
    
    finished = pyqtSignal(list, dict)  # 评分结果, 原始数据
    progress = pyqtSignal(str, int)    # 进度信息, 百分比
    error = pyqtSignal(str)            # 错误信息
    
    def __init__(self, period: str = "short"):
        super().__init__()
        self.period = period
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            from markets.ashare.mainline.integrated_heatmap import IntegratedHeatmapEngine
            
            fetcher = RealDataFetcher()
            raw_data = {}
            
            # 1. 获取行业板块数据
            self.progress.emit("📡 获取行业板块数据 [同花顺 stock_fund_flow_industry]", 10)
            sector_result = fetcher.fetch_sector_flow()
            if sector_result.success:
                raw_data["sector"] = {
                    "source": sector_result.source,
                    "api": "ak.stock_fund_flow_industry(symbol='即时')",
                    "count": len(sector_result.data) if isinstance(sector_result.data, list) else 0,
                    "data": sector_result.data,
                    "sample": sector_result.data[:3] if isinstance(sector_result.data, list) else [],
                }
            else:
                raw_data["sector"] = {"source": "获取失败", "api": "", "count": 0, "data": [], "sample": []}
            
            # 2. 获取概念板块数据
            self.progress.emit("📡 获取概念板块数据 [同花顺 stock_fund_flow_concept]", 35)
            concept_result = fetcher.fetch_concept_board()
            if concept_result.success:
                raw_data["concept"] = {
                    "source": concept_result.source,
                    "api": "ak.stock_fund_flow_concept(symbol='即时')",
                    "count": len(concept_result.data) if isinstance(concept_result.data, list) else 0,
                    "data": concept_result.data,
                    "sample": concept_result.data[:3] if isinstance(concept_result.data, list) else [],
                }
            else:
                raw_data["concept"] = {"source": "获取失败", "api": "", "count": 0, "data": [], "sample": []}
            
            # 3. 获取涨停池数据
            self.progress.emit("📡 获取涨停池数据 [东方财富 stock_zt_pool_em]", 60)
            limit_up_result = fetcher.fetch_market_sentiment()
            if limit_up_result.success and isinstance(limit_up_result.data, dict):
                raw_data["limit_up"] = {
                    "source": limit_up_result.source,
                    "api": "ak.stock_zt_pool_em(date='YYYYMMDD')",
                    "count": limit_up_result.data.get("up_limit_count", 0),
                    "data": limit_up_result.data,
                    "continuous": limit_up_result.data.get("continuous_limit", {}),
                }
            else:
                raw_data["limit_up"] = {"source": "获取失败", "api": "", "count": 0, "data": {}, "continuous": {}}
            
            # 4. 获取龙虎榜数据
            self.progress.emit("📡 获取龙虎榜数据 [东方财富 stock_lhb_detail_em]", 80)
            lhb_result = fetcher.fetch_dragon_tiger()
            if lhb_result.success and isinstance(lhb_result.data, list):
                raw_data["lhb"] = {
                    "source": lhb_result.source,
                    "api": "ak.stock_lhb_detail_em(start_date, end_date)",
                    "count": len(lhb_result.data),
                    "data": lhb_result.data,
                    "sample": lhb_result.data[:3] if lhb_result.data else [],
                }
            else:
                raw_data["lhb"] = {"source": "获取失败", "api": "", "count": 0, "data": [], "sample": []}
            
            # 5. 计算热度评分
            self.progress.emit("🔢 计算热度评分...", 95)
            
            engine = IntegratedHeatmapEngine()
            scores = engine.calculate_heatmap_scores(
                sector_data=raw_data["sector"]["data"] if isinstance(raw_data["sector"]["data"], list) else [],
                concept_data=raw_data["concept"]["data"] if isinstance(raw_data["concept"]["data"], list) else [],
                limit_up_data=raw_data["limit_up"]["data"] if isinstance(raw_data["limit_up"]["data"], dict) else {},
                lhb_data=raw_data["lhb"]["data"] if isinstance(raw_data["lhb"]["data"], list) else [],
                period=self.period,
            )
            
            self.finished.emit(scores, raw_data)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.error.emit(str(e))


# ============================================================
# 主面板
# ============================================================

class HeatmapPanel(QWidget):
    """集成热度评分面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scores = []
        self.raw_data = {}
        self.worker = None
        self.report_path = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        
        # 1. 衔接关系说明
        content_layout.addWidget(self._create_integration_section())
        
        # 2. 5因子模型完整展示
        content_layout.addWidget(self._create_factors_section())
        
        # 3. 数据源状态（显示具体API和数据）
        content_layout.addWidget(self._create_data_source_section())
        
        # 4. 控制面板
        content_layout.addWidget(self._create_controls_section())
        
        # 5. 热度排名表
        content_layout.addWidget(self._create_ranking_section())
        
        # 6. 个股筛选预留说明
        content_layout.addWidget(self._create_stock_selection_section())
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _create_integration_section(self) -> QWidget:
        """创建衔接关系说明"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {Colors.PRIMARY}20, stop:1 {Colors.BG_TERTIARY});
                border: 1px solid {Colors.PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # 标题
        title = QLabel("🔗 与主线识别的衔接关系")
        title.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {Colors.PRIMARY};")
        layout.addWidget(title)
        
        # 衔接图
        integration_html = f"""
        <table style='width:100%; color: {Colors.TEXT_PRIMARY}; font-size: 12px;'>
        <tr>
            <td style='width:45%; padding:8px; background-color: {Colors.BG_TERTIARY}; border-radius:4px;'>
                <b>🎯 主线识别 (5维度)</b><br/>
                <span style='color:{Colors.TEXT_SECONDARY};'>
                ├─ 资金维度 25% ← <span style='color:#3b82f6;'>资金流入</span><br/>
                ├─ 动量维度 20% ← <span style='color:#10b981;'>涨跌幅</span><br/>
                ├─ <span style='color:#f59e0b;'>热度维度 20%</span> ← <b>本模块输出</b><br/>
                ├─ 政策维度 20%<br/>
                └─ 龙头维度 15% ← <span style='color:#8b5cf6;'>龙头强度</span>
                </span>
            </td>
            <td style='width:10%; text-align:center; color:{Colors.PRIMARY};'>
                ⟹
            </td>
            <td style='width:45%; padding:8px; background-color: {Colors.BG_TERTIARY}; border-radius:4px;'>
                <b>📊 热度评分 (5因子)</b><br/>
                <span style='color:{Colors.TEXT_SECONDARY};'>
                ├─ <span style='color:#10b981;'>涨跌幅强度 25%</span><br/>
                ├─ <span style='color:#3b82f6;'>资金流入强度 25%</span><br/>
                ├─ <span style='color:#ef4444;'>涨停板数量 20%</span><br/>
                ├─ <span style='color:#f97316;'>龙虎榜活跃度 15%</span><br/>
                └─ <span style='color:#8b5cf6;'>龙头股强度 15%</span>
                </span>
            </td>
        </tr>
        </table>
        """
        
        integration_label = QLabel(integration_html)
        integration_label.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(integration_label)
        
        # 数据流说明
        flow_label = QLabel(
            "📌 数据流：热度评分结果 → 主线识别[热度维度] → 综合评分 → 个股筛选"
        )
        flow_label.setStyleSheet(f"""
            color: {Colors.TEXT_SECONDARY};
            font-size: 11px;
            padding: 6px;
            background-color: {Colors.BG_TERTIARY};
            border-radius: 4px;
        """)
        layout.addWidget(flow_label)
        
        return frame
    
    def _create_factors_section(self) -> QWidget:
        """创建5因子模型完整展示"""
        frame = QGroupBox("📊 5因子热度评分模型（完整配置）")
        frame.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        # 因子卡片网格
        grid = QGridLayout()
        grid.setSpacing(8)
        
        for i, factor in enumerate(HEAT_FACTORS_CONFIG):
            card = self._create_factor_card(factor)
            grid.addWidget(card, i // 3, i % 3)
        
        layout.addLayout(grid)
        
        # 计算公式
        formula = QLabel(
            "📐 热度得分 = 涨跌幅×25% + 资金×25% + 涨停×20% + 龙虎榜×15% + 龙头×15%"
        )
        formula.setStyleSheet(f"""
            color: {Colors.PRIMARY};
            font-size: 12px;
            font-weight: bold;
            padding: 8px;
            background-color: {Colors.PRIMARY}15;
            border-radius: 4px;
            margin-top: 8px;
        """)
        layout.addWidget(formula)
        
        return frame
    
    def _create_factor_card(self, factor: dict) -> QFrame:
        """创建单个因子卡片"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {factor['color']}40;
                border-left: 3px solid {factor['color']};
                border-radius: 6px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        
        # 标题行
        header = QHBoxLayout()
        name = QLabel(f"{factor['icon']} {factor['name']}")
        name.setStyleSheet(f"font-weight: bold; color: {factor['color']}; font-size: 12px;")
        header.addWidget(name)
        
        weight = QLabel(f"{factor['weight']}%")
        weight.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px;")
        header.addWidget(weight)
        header.addStretch()
        layout.addLayout(header)
        
        # 数据源
        source = QLabel(f"📡 {factor['data_source']}")
        source.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 10px;")
        layout.addWidget(source)
        
        # 字段
        field = QLabel(f"📝 字段: {factor['api_field']}")
        field.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 10px;")
        layout.addWidget(field)
        
        # 衔接
        link = QLabel(factor['to_mainline'])
        link.setStyleSheet(f"color: {Colors.PRIMARY}; font-size: 10px;")
        layout.addWidget(link)
        
        return card
    
    def _create_data_source_section(self) -> QWidget:
        """创建数据源状态区域（显示具体数据）"""
        frame = QGroupBox("📡 数据源状态（点击计算后显示具体数据）")
        frame.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        # 数据源表格
        self.data_source_table = QTableWidget()
        self.data_source_table.setColumnCount(5)
        self.data_source_table.setHorizontalHeaderLabels([
            "数据类型", "API接口", "来源", "数据量", "示例数据"
        ])
        self.data_source_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.data_source_table.setRowCount(4)
        self.data_source_table.setMaximumHeight(180)
        self.data_source_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: none;
                gridline-color: {Colors.BORDER_PRIMARY};
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                padding: 6px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }}
        """)
        
        # 初始化表格
        self._init_data_source_table()
        
        layout.addWidget(self.data_source_table)
        
        return frame
    
    def _init_data_source_table(self):
        """初始化数据源表格"""
        sources = [
            ("🏭 行业板块", "ak.stock_fund_flow_industry", "同花顺", "--", "等待获取..."),
            ("💡 概念板块", "ak.stock_fund_flow_concept", "同花顺", "--", "等待获取..."),
            ("📈 涨停池", "ak.stock_zt_pool_em", "东方财富", "--", "等待获取..."),
            ("🐉 龙虎榜", "ak.stock_lhb_detail_em", "东方财富", "--", "等待获取..."),
        ]
        
        for i, (name, api, source, count, sample) in enumerate(sources):
            self.data_source_table.setItem(i, 0, QTableWidgetItem(name))
            self.data_source_table.setItem(i, 1, QTableWidgetItem(api))
            self.data_source_table.setItem(i, 2, QTableWidgetItem(source))
            self.data_source_table.setItem(i, 3, QTableWidgetItem(count))
            self.data_source_table.setItem(i, 4, QTableWidgetItem(sample))
    
    def _update_data_source_table(self, raw_data: dict):
        """更新数据源表格"""
        # 行业板块
        sector = raw_data.get("sector", {})
        self.data_source_table.setItem(0, 2, QTableWidgetItem(sector.get("source", "未知")))
        self.data_source_table.setItem(0, 3, QTableWidgetItem(f"{sector.get('count', 0)}条"))
        sample = sector.get("sample", [])
        if sample:
            sample_text = ", ".join([s.get("sector_name", "")[:6] for s in sample[:3]])
            self.data_source_table.setItem(0, 4, QTableWidgetItem(sample_text))
        
        # 概念板块
        concept = raw_data.get("concept", {})
        self.data_source_table.setItem(1, 2, QTableWidgetItem(concept.get("source", "未知")))
        self.data_source_table.setItem(1, 3, QTableWidgetItem(f"{concept.get('count', 0)}条"))
        sample = concept.get("sample", [])
        if sample:
            sample_text = ", ".join([s.get("board_name", "")[:6] for s in sample[:3]])
            self.data_source_table.setItem(1, 4, QTableWidgetItem(sample_text))
        
        # 涨停池
        limit_up = raw_data.get("limit_up", {})
        self.data_source_table.setItem(2, 2, QTableWidgetItem(limit_up.get("source", "未知")))
        self.data_source_table.setItem(2, 3, QTableWidgetItem(f"{limit_up.get('count', 0)}只"))
        continuous = limit_up.get("continuous", {})
        if continuous:
            cont_text = ", ".join([f"{k}板:{v}只" for k, v in list(continuous.items())[:3]])
            self.data_source_table.setItem(2, 4, QTableWidgetItem(cont_text))
        
        # 龙虎榜
        lhb = raw_data.get("lhb", {})
        self.data_source_table.setItem(3, 2, QTableWidgetItem(lhb.get("source", "未知")))
        self.data_source_table.setItem(3, 3, QTableWidgetItem(f"{lhb.get('count', 0)}条"))
        sample = lhb.get("sample", [])
        if sample:
            sample_text = ", ".join([s.get("名称", s.get("股票名称", ""))[:4] for s in sample[:3]])
            self.data_source_table.setItem(3, 4, QTableWidgetItem(sample_text))
    
    def _create_controls_section(self) -> QWidget:
        """创建控制面板"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # 按钮行
        btn_layout = QHBoxLayout()
        
        # 周期选择
        period_label = QLabel("评分周期:")
        period_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        btn_layout.addWidget(period_label)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["短期(3-5日)", "中期(15-30日)", "长期(60-180日)"])
        self.period_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 120px;
            }}
        """)
        btn_layout.addWidget(self.period_combo)
        
        btn_layout.addStretch()
        
        # 计算按钮
        self.calc_btn = QPushButton("📊 计算热度评分")
        self.calc_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_LIGHT};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_MUTED};
            }}
        """)
        self.calc_btn.clicked.connect(self._start_calculation)
        btn_layout.addWidget(self.calc_btn)
        
        # 导出报告按钮
        self.export_btn = QPushButton("📄 导出报告并打开")
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_SECONDARY};
            }}
            QPushButton:disabled {{
                color: {Colors.TEXT_MUTED};
            }}
        """)
        self.export_btn.clicked.connect(self._export_and_open_report)
        btn_layout.addWidget(self.export_btn)
        
        layout.addLayout(btn_layout)
        
        # 进度条
        self.progress_frame = QFrame()
        self.progress_frame.setVisible(False)
        progress_layout = QHBoxLayout(self.progress_frame)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        
        self.progress_label = QLabel("准备中...")
        self.progress_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_TERTIARY};
                border: none;
                border-radius: 4px;
                height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
                border-radius: 4px;
            }}
        """)
        self.progress_bar.setTextVisible(False)
        progress_layout.addWidget(self.progress_bar, 1)
        
        layout.addWidget(self.progress_frame)
        
        return frame
    
    def _create_ranking_section(self) -> QWidget:
        """创建热度排名区域"""
        frame = QGroupBox("🏆 热度排名（按总分排序）")
        frame.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: bold;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 8px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        
        # 排名表格
        self.ranking_table = QTableWidget()
        self.ranking_table.setColumnCount(10)
        self.ranking_table.setHorizontalHeaderLabels([
            "排名", "主线", "类型", "总分",
            "涨幅", "资金", "涨停", "龙虎", "龙头", "等级"
        ])
        self.ranking_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ranking_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.ranking_table.setMinimumHeight(300)
        self.ranking_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                border: none;
                gridline-color: {Colors.BORDER_PRIMARY};
                font-size: 11px;
            }}
            QTableWidget::item {{
                padding: 6px;
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.PRIMARY}30;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 11px;
            }}
        """)
        layout.addWidget(self.ranking_table)
        
        return frame
    
    def _create_stock_selection_section(self) -> QWidget:
        """创建个股筛选预留说明"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        
        title = QLabel("🎯 个股筛选接口（后续模块使用）")
        title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        desc_html = f"""
        <p style='color: {Colors.TEXT_SECONDARY}; font-size: 11px;'>
        热度评分结果将被个股筛选模块使用：<br/>
        1. 筛选高热度(≥60分)主线内的个股<br/>
        2. 个股评分 = 所属主线热度 × 15% + 个股因子 × 85%<br/>
        3. 结果保存到 <code>~/.local/share/trquant/reports/heatmap/</code>
        </p>
        """
        desc = QLabel(desc_html)
        desc.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(desc)
        
        return frame
    
    # ============================================================
    # 功能方法
    # ============================================================
    
    def _start_calculation(self):
        """开始计算"""
        period_map = {0: "short", 1: "medium", 2: "long"}
        period = period_map.get(self.period_combo.currentIndex(), "short")
        
        self.calc_btn.setEnabled(False)
        self.export_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = IntegratedHeatmapWorker(period)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()
    
    def _on_progress(self, message: str, percent: int):
        """更新进度"""
        self.progress_label.setText(message)
        self.progress_bar.setValue(percent)
    
    def _on_finished(self, scores: list, raw_data: dict):
        """计算完成"""
        self.scores = scores
        self.raw_data = raw_data
        
        # 更新数据源表格
        self._update_data_source_table(raw_data)
        
        # 更新排名表格
        self._update_ranking_table()
        
        # 保存结果供个股筛选使用
        self._save_for_stock_selection()
        
        # 完成
        self.calc_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        
        QMessageBox.information(
            self, "计算完成",
            f"热度评分计算完成！\n\n"
            f"• 行业板块: {raw_data['sector']['count']} 条\n"
            f"• 概念板块: {raw_data['concept']['count']} 条\n"
            f"• 涨停池: {raw_data['limit_up']['count']} 只\n"
            f"• 龙虎榜: {raw_data['lhb']['count']} 条\n\n"
            f"共计算出 {len(scores)} 条主线的热度评分\n\n"
            f"点击「导出报告并打开」查看详细报告"
        )
    
    def _on_error(self, error: str):
        """处理错误"""
        self.calc_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        QMessageBox.critical(self, "计算失败", f"热度评分计算失败：\n{error}")
    
    def _update_ranking_table(self):
        """更新排名表格"""
        self.ranking_table.setRowCount(len(self.scores))
        
        for i, score in enumerate(self.scores):
            # 排名
            rank_item = QTableWidgetItem(str(score.rank))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if score.rank <= 3:
                rank_item.setForeground(QColor("#f59e0b"))
                rank_item.setFont(QFont("", -1, QFont.Weight.Bold))
            self.ranking_table.setItem(i, 0, rank_item)
            
            # 名称
            self.ranking_table.setItem(i, 1, QTableWidgetItem(score.name))
            
            # 类型
            type_text = "行业" if score.type == "industry" else "概念"
            type_item = QTableWidgetItem(type_text)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ranking_table.setItem(i, 2, type_item)
            
            # 总分
            score_item = QTableWidgetItem(f"{score.total_score:.1f}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            score_item.setForeground(QColor(score.level_color))
            score_item.setFont(QFont("", -1, QFont.Weight.Bold))
            self.ranking_table.setItem(i, 3, score_item)
            
            # 5个因子得分
            for j, (attr, col) in enumerate([
                ("change_score", 4), ("flow_score", 5), ("limit_up_score", 6),
                ("lhb_score", 7), ("leader_score", 8)
            ]):
                val = getattr(score, attr, 0)
                item = QTableWidgetItem(f"{val:.0f}")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.ranking_table.setItem(i, col, item)
            
            # 等级
            level_item = QTableWidgetItem(score.level)
            level_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            level_item.setForeground(QColor(score.level_color))
            self.ranking_table.setItem(i, 9, level_item)
    
    def _save_for_stock_selection(self):
        """保存结果供个股筛选使用"""
        try:
            output_dir = Path.home() / ".local/share/trquant/reports/heatmap"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 保存为JSON供其他模块读取
            data = {
                "timestamp": datetime.now().isoformat(),
                "scores": [s.to_dict() for s in self.scores],
                "high_heat_mainlines": [s.name for s in self.scores if s.total_score >= 60],
            }
            
            json_path = output_dir / "latest_heatmap_scores.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"热度评分结果已保存到: {json_path}")
        except Exception as e:
            logger.error(f"保存热度评分结果失败: {e}")
    
    def _export_and_open_report(self):
        """导出报告并自动打开"""
        if not self.scores:
            QMessageBox.warning(self, "提示", "请先计算热度评分")
            return
        
        try:
            from markets.ashare.mainline.heatmap_report_generator import HeatmapReportGenerator
            
            generator = HeatmapReportGenerator()
            self.report_path = generator.generate_html_report(self.scores, self.raw_data)
            
            # 在浏览器中打开
            webbrowser.open(f"file://{self.report_path}")
            
            # 在文件管理器中打开目录
            report_dir = Path(self.report_path).parent
            if sys.platform == "linux":
                subprocess.run(["xdg-open", str(report_dir)], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["open", "-R", self.report_path], check=False)
            elif sys.platform == "win32":
                subprocess.Popen(f'explorer /select,"{self.report_path}"')
            
            QMessageBox.information(
                self, "导出成功",
                f"热度评分报告已生成并打开！\n\n"
                f"报告路径:\n{self.report_path}\n\n"
                f"• 报告已在浏览器中打开\n"
                f"• 文件管理器已打开报告目录"
            )
        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出报告失败：\n{e}")
