# -*- coding: utf-8 -*-
"""
动量维度Tab

权重：20%
刻画主线题材的价格趋势和强度
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from gui.styles.theme import Colors
from .base_dimension_tab import BaseDimensionTab


class MomentumDimensionTab(BaseDimensionTab):
    """动量维度Tab"""
    
    DIMENSION_KEY = "momentum"
    DIMENSION_NAME = "动量维度"
    DIMENSION_ICON = "📈"
    DIMENSION_COLOR = "#10B981"
    DIMENSION_WEIGHT = 0.20
    DIMENSION_DESC = "刻画主线题材的价格趋势和强度，主要基于价格和交易量等技术面因子。核心指标包括价格动量、相对强度、成交量动量等。可引入技术信号如突破重要均线、阶段新高等。"
    
    FACTORS = [
        {"name": "价格动量", "weight": 0.40, "desc": "近期涨跌幅，衡量短期强势程度"},
        {"name": "相对强度", "weight": 0.30, "desc": "相对大盘的超额收益"},
        {"name": "成交活跃度", "weight": 0.30, "desc": "成交额排名，反映资金活跃度"},
    ]
    
    def _create_tools_section(self) -> QFrame:
        """创建动量维度专属工具区"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {self.DIMENSION_COLOR}40;
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        
        title = QLabel("🔧 动量分析工具")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        tools = [
            ("📊 动量曲线", "查看板块动量趋势曲线"),
            ("📈 突破筛选", "筛选突破重要均线的板块"),
            ("🎯 相对强度对比", "与大盘相对强度对比"),
        ]
        
        for btn_text, tooltip in tools:
            btn = QPushButton(btn_text)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_PRIMARY};
                    color: {Colors.TEXT_PRIMARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {self.DIMENSION_COLOR}20;
                    border-color: {self.DIMENSION_COLOR};
                }}
            """)
            tools_layout.addWidget(btn)
        
        tools_layout.addStretch()
        layout.addLayout(tools_layout)
        
        return frame
    
    def _get_raw_data_text(self, result) -> str:
        return f"涨幅: {result.change_pct:+.2f}%"




