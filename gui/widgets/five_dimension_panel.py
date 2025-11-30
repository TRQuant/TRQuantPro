# -*- coding: utf-8 -*-
"""
五维评分面板

基于《市场主线识别模块五维评分系统设计方案.pdf》设计

包含6个子Tab：
1. 📊 综合评分 - 汇总五维评分，雷达图对比
2. 💰 资金维度 - 主力资金流强度
3. 🔥 热度维度 - 市场关注度和情绪强度
4. 📈 动量维度 - 价格趋势和强度
5. 📜 政策维度 - 政策支持力度
6. 👑 龙头维度 - 龙头股表现
"""

import logging
import json
import webbrowser
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QProgressBar, QComboBox,
    QMessageBox, QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt6.QtGui import QDesktopServices

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


class FiveDimensionWorker(QThread):
    """五维评分计算线程"""
    
    finished = pyqtSignal(list)  # 评分结果
    progress = pyqtSignal(str)   # 进度信息
    error = pyqtSignal(str)      # 错误信息
    
    def __init__(self, period: str = "medium"):
        super().__init__()
        self.period = period
    
    def run(self):
        try:
            from markets.ashare.mainline.real_data_fetcher import RealDataFetcher
            from markets.ashare.mainline.five_dimension_engine import FiveDimensionEngine
            
            fetcher = RealDataFetcher()
            engine = FiveDimensionEngine()
            
            # 获取数据
            self.progress.emit("📡 正在获取行业板块数据...")
            sector_result = fetcher.fetch_sector_flow()
            sector_data = sector_result.data if sector_result.success else []
            
            self.progress.emit("📡 正在获取概念板块数据...")
            concept_result = fetcher.fetch_concept_board()
            concept_data = concept_result.data if concept_result.success else []
            
            self.progress.emit("📡 正在获取涨停池数据...")
            sentiment_result = fetcher.fetch_market_sentiment()
            limit_up_data = sentiment_result.data if sentiment_result.success else {}
            
            self.progress.emit("📡 正在获取龙虎榜数据...")
            lhb_result = fetcher.fetch_dragon_tiger()
            lhb_data = lhb_result.data if lhb_result.success else []
            
            self.progress.emit("📡 正在获取北向资金数据...")
            north_result = fetcher.fetch_northbound_flow()
            north_data = north_result.data if north_result.success else {}
            
            # 计算五维评分
            self.progress.emit("🔄 正在计算五维评分...")
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


class FiveDimensionPanel(QWidget):
    """五维评分面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.results = []
        self.worker = None
        self.report_path = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建子Tab
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
            QTabBar::tab {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_MUTED};
                border: none;
                padding: 8px 14px;
                font-size: 11px;
                font-weight: 600;
                min-width: 70px;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.PRIMARY};
                border-bottom: 2px solid {Colors.PRIMARY};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        
        # 添加6个子Tab
        self.tab_widget.addTab(self._create_overview_tab(), "📊 综合评分")
        self.tab_widget.addTab(self._create_dimension_tab("funds"), "💰 资金")
        self.tab_widget.addTab(self._create_dimension_tab("heat"), "🔥 热度")
        self.tab_widget.addTab(self._create_dimension_tab("momentum"), "📈 动量")
        self.tab_widget.addTab(self._create_dimension_tab("policy"), "📜 政策")
        self.tab_widget.addTab(self._create_dimension_tab("leader"), "👑 龙头")
        
        layout.addWidget(self.tab_widget)
    
    def _create_overview_tab(self) -> QWidget:
        """创建综合评分Tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 顶部控制栏
        control_frame = QFrame()
        control_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        control_layout = QHBoxLayout(control_frame)
        control_layout.setContentsMargins(12, 8, 12, 8)
        
        # 周期选择
        period_label = QLabel("评分周期:")
        period_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 12px;")
        control_layout.addWidget(period_label)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["短期(3-5日)", "中期(15-30日)", "长期(60-180日)"])
        self.period_combo.setCurrentIndex(1)  # 默认中期
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
        control_layout.addWidget(self.period_combo)
        
        control_layout.addStretch()
        
        # 计算按钮
        self.calc_btn = QPushButton("🔄 计算五维评分")
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
        control_layout.addWidget(self.calc_btn)
        
        # 导出报告按钮
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
        control_layout.addWidget(self.export_btn)
        
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
        self.progress_bar.setRange(0, 0)  # 无限进度
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_TERTIARY};
                border: none;
                border-radius: 4px;
                height: 6px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
                border-radius: 4px;
            }}
        """)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.progress_frame)
        
        # 方法论说明
        methodology_frame = self._create_methodology_section()
        layout.addWidget(methodology_frame)
        
        # 结果区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background-color: transparent; }}")
        
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.setContentsMargins(0, 0, 0, 0)
        self.result_layout.setSpacing(12)
        
        # 初始占位
        placeholder = QLabel("点击「计算五维评分」开始分析...")
        placeholder.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 12px; padding: 20px;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(placeholder)
        
        scroll.setWidget(self.result_widget)
        layout.addWidget(scroll)
        
        return widget
    
    def _create_methodology_section(self) -> QFrame:
        """创建方法论说明区域"""
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
        
        # 标题
        title = QLabel("📐 五维评分系统方法论")
        title.setStyleSheet(f"font-size: 13px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        # 维度说明
        dimensions_layout = QHBoxLayout()
        dimensions_layout.setSpacing(8)
        
        dimensions = [
            ("💰", "资金", "30%", "#3B82F6", "主力资金净流入强度"),
            ("🔥", "热度", "20%", "#EF4444", "市场关注度和情绪"),
            ("📈", "动量", "20%", "#10B981", "价格趋势和强度"),
            ("📜", "政策", "15%", "#8B5CF6", "政策支持力度"),
            ("👑", "龙头", "15%", "#F59E0B", "龙头股表现"),
        ]
        
        for icon, name, weight, color, desc in dimensions:
            dim_frame = QFrame()
            dim_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {color}40;
                    border-radius: 6px;
                }}
            """)
            dim_layout = QVBoxLayout(dim_frame)
            dim_layout.setContentsMargins(8, 6, 8, 6)
            dim_layout.setSpacing(2)
            
            header = QHBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 14px;")
            header.addWidget(icon_label)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            header.addWidget(name_label)
            
            weight_label = QLabel(weight)
            weight_label.setStyleSheet(f"font-size: 10px; color: {color}; font-weight: 600;")
            header.addWidget(weight_label)
            header.addStretch()
            dim_layout.addLayout(header)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"font-size: 9px; color: {Colors.TEXT_MUTED};")
            dim_layout.addWidget(desc_label)
            
            dimensions_layout.addWidget(dim_frame)
        
        layout.addLayout(dimensions_layout)
        
        # 评分等级说明
        levels_layout = QHBoxLayout()
        levels = [
            ("极强≥80", "#EF4444", "买入"),
            ("强65-80", "#F97316", "持有"),
            ("中等50-65", "#EAB308", "观察"),
            ("弱35-50", "#22C55E", "减仓"),
            ("极弱<35", "#6B7280", "卖出"),
        ]
        
        for level, color, signal in levels:
            level_label = QLabel(f"{level} → {signal}")
            level_label.setStyleSheet(f"""
                font-size: 9px;
                color: {color};
                background-color: {color}15;
                padding: 2px 6px;
                border-radius: 4px;
            """)
            levels_layout.addWidget(level_label)
        
        levels_layout.addStretch()
        layout.addLayout(levels_layout)
        
        return frame
    
    def _create_dimension_tab(self, dimension: str) -> QWidget:
        """创建单维度Tab"""
        from markets.ashare.mainline.five_dimension_engine import DIMENSION_WEIGHTS
        
        config = DIMENSION_WEIGHTS.get(dimension, {})
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 维度说明
        intro_frame = QFrame()
        intro_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {config.get('color', Colors.PRIMARY)}20,
                    stop:1 {Colors.BG_TERTIARY});
                border-left: 4px solid {config.get('color', Colors.PRIMARY)};
                border-radius: 8px;
            }}
        """)
        intro_layout = QVBoxLayout(intro_frame)
        intro_layout.setContentsMargins(16, 12, 16, 12)
        
        title = QLabel(f"{config.get('icon', '')} {config.get('name', dimension)} 维度 ({config.get('weight', 0)*100:.0f}%)")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        intro_layout.addWidget(title)
        
        desc = QLabel(config.get('description', ''))
        desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
        intro_layout.addWidget(desc)
        
        layout.addWidget(intro_frame)
        
        # 因子说明
        factors_frame = QFrame()
        factors_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        factors_layout = QVBoxLayout(factors_frame)
        factors_layout.setContentsMargins(12, 10, 12, 10)
        
        factors_title = QLabel("📊 评分因子")
        factors_title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        factors_layout.addWidget(factors_title)
        
        for factor in config.get('factors', []):
            factor_layout = QHBoxLayout()
            
            name_label = QLabel(f"• {factor['name']}")
            name_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_PRIMARY};")
            factor_layout.addWidget(name_label)
            
            weight_label = QLabel(f"({factor['weight']*100:.0f}%)")
            weight_label.setStyleSheet(f"font-size: 10px; color: {config.get('color', Colors.PRIMARY)};")
            factor_layout.addWidget(weight_label)
            
            factor_layout.addStretch()
            
            desc_label = QLabel(factor['desc'])
            desc_label.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED};")
            factor_layout.addWidget(desc_label)
            
            factors_layout.addLayout(factor_layout)
        
        layout.addWidget(factors_frame)
        
        # 排名表格
        table_title = QLabel(f"🏆 {config.get('name', dimension)}维度排名")
        table_title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(table_title)
        
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["排名", "主线名称", "类型", "维度得分", "因子详情", "综合得分"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 6px;
                color: {Colors.TEXT_PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_MUTED};
                padding: 8px;
                border: none;
                font-weight: 600;
            }}
        """)
        
        # 保存表格引用
        setattr(self, f"{dimension}_table", table)
        
        layout.addWidget(table)
        
        return widget
    
    def _start_calculation(self):
        """开始计算"""
        if self.worker and self.worker.isRunning():
            return
        
        # 获取周期
        period_map = {0: "short", 1: "medium", 2: "long"}
        period = period_map.get(self.period_combo.currentIndex(), "medium")
        
        # 显示进度
        self.calc_btn.setEnabled(False)
        self.progress_frame.setVisible(True)
        self.progress_label.setText("准备中...")
        
        # 启动工作线程
        self.worker = FiveDimensionWorker(period)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()
    
    def _on_progress(self, message: str):
        """进度更新"""
        self.progress_label.setText(message)
    
    def _on_finished(self, results: list):
        """计算完成"""
        self.results = results
        self.calc_btn.setEnabled(True)
        self.export_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        
        # 更新结果显示
        self._update_results()
        
        # 更新各维度Tab
        self._update_dimension_tables()
        
        QMessageBox.information(
            self, "完成",
            f"五维评分计算完成！\n\n"
            f"• 共分析 {len(results)} 条主线\n"
            f"• 极强主线(≥80分): {sum(1 for r in results if r.total_score >= 80)} 条\n"
            f"• 强主线(≥65分): {sum(1 for r in results if 65 <= r.total_score < 80)} 条"
        )
    
    def _on_error(self, error: str):
        """计算错误"""
        self.calc_btn.setEnabled(True)
        self.progress_frame.setVisible(False)
        QMessageBox.warning(self, "错误", f"计算失败: {error}")
    
    def _update_results(self):
        """更新结果显示"""
        # 清空现有内容
        while self.result_layout.count():
            item = self.result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.results:
            placeholder = QLabel("暂无数据")
            placeholder.setStyleSheet(f"color: {Colors.TEXT_MUTED}; padding: 20px;")
            self.result_layout.addWidget(placeholder)
            return
        
        # 统计信息
        stats_frame = self._create_stats_section()
        self.result_layout.addWidget(stats_frame)
        
        # 排名表格
        table_frame = self._create_ranking_table()
        self.result_layout.addWidget(table_frame)
        
        self.result_layout.addStretch()
    
    def _create_stats_section(self) -> QFrame:
        """创建统计区域"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(20)
        
        # 统计卡片
        stats = [
            ("分析数量", str(len(self.results)), "#3B82F6"),
            ("极强主线", str(sum(1 for r in self.results if r.total_score >= 80)), "#EF4444"),
            ("强主线", str(sum(1 for r in self.results if 65 <= r.total_score < 80)), "#F97316"),
            ("最高分", f"{max(r.total_score for r in self.results):.1f}" if self.results else "--", "#10B981"),
        ]
        
        for name, value, color in stats:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {color}40;
                    border-radius: 6px;
                    min-width: 80px;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(12, 8, 12, 8)
            card_layout.setSpacing(2)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED};")
            card_layout.addWidget(name_label)
            
            value_label = QLabel(value)
            value_label.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {color};")
            card_layout.addWidget(value_label)
            
            layout.addWidget(card)
        
        layout.addStretch()
        
        return frame
    
    def _create_ranking_table(self) -> QFrame:
        """创建排名表格"""
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
        
        title = QLabel("🏆 综合排名")
        title.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setRowCount(min(20, len(self.results)))
        table.setColumnCount(10)
        table.setHorizontalHeaderLabels([
            "排名", "主线名称", "类型", "综合得分", "等级", "信号",
            "资金", "热度", "动量", "政策"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet(f"""
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
        
        for i, result in enumerate(self.results[:20]):
            # 排名
            rank_item = QTableWidgetItem(str(result.rank))
            rank_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 0, rank_item)
            
            # 名称
            table.setItem(i, 1, QTableWidgetItem(result.name))
            
            # 类型
            type_item = QTableWidgetItem(result.type)
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 2, type_item)
            
            # 综合得分
            score_item = QTableWidgetItem(f"{result.total_score:.1f}")
            score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 3, score_item)
            
            # 等级
            level_item = QTableWidgetItem(result.level)
            level_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 4, level_item)
            
            # 信号
            signal_item = QTableWidgetItem(result.signal)
            signal_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            table.setItem(i, 5, signal_item)
            
            # 各维度得分
            table.setItem(i, 6, QTableWidgetItem(f"{result.funds_score.score:.0f}"))
            table.setItem(i, 7, QTableWidgetItem(f"{result.heat_score.score:.0f}"))
            table.setItem(i, 8, QTableWidgetItem(f"{result.momentum_score.score:.0f}"))
            table.setItem(i, 9, QTableWidgetItem(f"{result.policy_score.score:.0f}"))
        
        layout.addWidget(table)
        
        return frame
    
    def _update_dimension_tables(self):
        """更新各维度Tab的表格"""
        dimensions = ["funds", "heat", "momentum", "policy", "leader"]
        dim_names = {
            "funds": "资金",
            "heat": "热度",
            "momentum": "动量",
            "policy": "政策",
            "leader": "龙头",
        }
        
        for dim in dimensions:
            table = getattr(self, f"{dim}_table", None)
            if not table:
                continue
            
            # 按该维度排序
            sorted_results = sorted(
                self.results,
                key=lambda x: getattr(x, f"{dim}_score").score,
                reverse=True
            )
            
            table.setRowCount(min(20, len(sorted_results)))
            
            for i, result in enumerate(sorted_results[:20]):
                dim_score = getattr(result, f"{dim}_score")
                
                # 排名
                table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                
                # 名称
                table.setItem(i, 1, QTableWidgetItem(result.name))
                
                # 类型
                table.setItem(i, 2, QTableWidgetItem(result.type))
                
                # 维度得分
                score_item = QTableWidgetItem(f"{dim_score.score:.1f}")
                table.setItem(i, 3, score_item)
                
                # 因子详情
                factors_text = ", ".join([f"{f['name']}:{f['score']:.0f}" for f in dim_score.factors[:2]])
                table.setItem(i, 4, QTableWidgetItem(factors_text))
                
                # 综合得分
                table.setItem(i, 5, QTableWidgetItem(f"{result.total_score:.1f}"))
    
    def _export_report(self):
        """导出报告"""
        if not self.results:
            QMessageBox.warning(self, "提示", "请先计算五维评分")
            return
        
        try:
            # 生成HTML报告
            report_path = self._generate_html_report()
            self.report_path = report_path
            
            # 打开报告
            webbrowser.open(f"file://{report_path}")
            
            # 打开文件管理器
            if sys.platform == "linux":
                subprocess.run(["xdg-open", str(Path(report_path).parent)], check=False)
            elif sys.platform == "darwin":
                subprocess.run(["open", "-R", report_path], check=False)
            elif sys.platform == "win32":
                subprocess.Popen(f'explorer /select,"{report_path}"')
            
            QMessageBox.information(
                self, "导出成功",
                f"报告已导出到:\n{report_path}\n\n已自动在浏览器和文件管理器中打开。"
            )
            
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"报告导出失败: {e}")
    
    def _generate_html_report(self) -> str:
        """生成HTML报告"""
        output_dir = Path.home() / ".local/share/trquant/reports/mainline/five_dimension"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"five_dimension_report_{timestamp}.html"
        
        # 生成HTML内容
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>五维评分报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }}
        h2 {{ color: #8b949e; margin-top: 30px; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px 20px; flex: 1; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #58a6ff; }}
        .stat-label {{ font-size: 12px; color: #8b949e; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; background: #161b22; border-radius: 8px; overflow: hidden; }}
        th {{ background: #21262d; color: #8b949e; padding: 12px; text-align: left; font-weight: 600; }}
        td {{ padding: 10px 12px; border-top: 1px solid #30363d; }}
        tr:hover {{ background: #1f2428; }}
        .score-high {{ color: #3fb950; }}
        .score-mid {{ color: #d29922; }}
        .score-low {{ color: #f85149; }}
        .dimension {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-right: 4px; }}
        .dim-funds {{ background: #3B82F620; color: #3B82F6; }}
        .dim-heat {{ background: #EF444420; color: #EF4444; }}
        .dim-momentum {{ background: #10B98120; color: #10B981; }}
        .dim-policy {{ background: #8B5CF620; color: #8B5CF6; }}
        .dim-leader {{ background: #F59E0B20; color: #F59E0B; }}
    </style>
</head>
<body>
<div class="container">
    <h1>📊 五维评分报告</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{len(self.results)}</div>
            <div class="stat-label">分析主线数量</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{sum(1 for r in self.results if r.total_score >= 80)}</div>
            <div class="stat-label">极强主线(≥80分)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{sum(1 for r in self.results if 65 <= r.total_score < 80)}</div>
            <div class="stat-label">强主线(65-80分)</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{max(r.total_score for r in self.results):.1f}</div>
            <div class="stat-label">最高分</div>
        </div>
    </div>
    
    <h2>🏆 综合排名 Top 20</h2>
    <table>
        <tr>
            <th>排名</th>
            <th>主线名称</th>
            <th>类型</th>
            <th>综合得分</th>
            <th>等级</th>
            <th>信号</th>
            <th>五维得分</th>
        </tr>
"""
        
        for result in self.results[:20]:
            score_class = "score-high" if result.total_score >= 65 else ("score-mid" if result.total_score >= 50 else "score-low")
            html += f"""
        <tr>
            <td>{result.rank}</td>
            <td><strong>{result.name}</strong></td>
            <td>{result.type}</td>
            <td class="{score_class}">{result.total_score:.1f}</td>
            <td>{result.level}</td>
            <td>{result.signal}</td>
            <td>
                <span class="dimension dim-funds">资金:{result.funds_score.score:.0f}</span>
                <span class="dimension dim-heat">热度:{result.heat_score.score:.0f}</span>
                <span class="dimension dim-momentum">动量:{result.momentum_score.score:.0f}</span>
                <span class="dimension dim-policy">政策:{result.policy_score.score:.0f}</span>
                <span class="dimension dim-leader">龙头:{result.leader_score.score:.0f}</span>
            </td>
        </tr>
"""
        
        html += """
    </table>
    
    <h2>📐 评分方法论</h2>
    <table>
        <tr>
            <th>维度</th>
            <th>权重</th>
            <th>说明</th>
            <th>评分因子</th>
        </tr>
        <tr>
            <td>💰 资金维度</td>
            <td>30%</td>
            <td>衡量主线题材的资金流强度</td>
            <td>主力净流入排名(40%)、资金流向强度(25%)、流入强度比(20%)、北向资金(15%)</td>
        </tr>
        <tr>
            <td>🔥 热度维度</td>
            <td>20%</td>
            <td>衡量市场关注度和情绪强度</td>
            <td>涨跌幅强度(25%)、资金流入强度(25%)、涨停板热度(20%)、龙虎榜活跃度(15%)、龙头股强度(15%)</td>
        </tr>
        <tr>
            <td>📈 动量维度</td>
            <td>20%</td>
            <td>刻画主线题材的价格趋势和强度</td>
            <td>价格动量(40%)、相对强度(30%)、成交活跃度(30%)</td>
        </tr>
        <tr>
            <td>📜 政策维度</td>
            <td>15%</td>
            <td>评估主线获得的政策支撑力度</td>
            <td>政策关联度(50%)、事件催化(30%)、产业趋势(20%)</td>
        </tr>
        <tr>
            <td>👑 龙头维度</td>
            <td>15%</td>
            <td>反映题材内领涨股的表现及示范效应</td>
            <td>龙头涨幅(50%)、强势股数量(30%)、连板高度(20%)</td>
        </tr>
    </table>
    
    <p style="color: #8b949e; font-size: 12px; margin-top: 30px;">
        本报告基于《市场主线识别模块五维评分系统设计方案》生成<br>
        数据来源: 同花顺(行业/概念资金流向)、东方财富(涨停池/龙虎榜)
    </p>
</div>
</body>
</html>
"""
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        return str(filepath)




