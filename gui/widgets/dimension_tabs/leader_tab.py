# -*- coding: utf-8 -*-
"""
龙头维度Tab

权重：15%
反映题材内领涨股的表现及示范效应
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from gui.styles.theme import Colors
from .base_dimension_tab import BaseDimensionTab


class LeaderDimensionTab(BaseDimensionTab):
    """龙头维度Tab"""
    
    DIMENSION_KEY = "leader"
    DIMENSION_NAME = "龙头维度"
    DIMENSION_ICON = "👑"
    DIMENSION_COLOR = "#F59E0B"
    DIMENSION_WEIGHT = 0.15
    DIMENSION_DESC = "反映题材内领涨股的表现及示范效应。核心考虑龙头股高度（连续涨停天数或累计涨幅）、梯队结构（一进二板、二进三板接力）、市值龙头影响力等。"
    
    FACTORS = [
        {"name": "龙头涨幅", "weight": 0.50, "desc": "龙头股涨幅，反映带动效应"},
        {"name": "强势股数量", "weight": 0.30, "desc": "板块内强势股数量"},
        {"name": "连板高度", "weight": 0.20, "desc": "最高连板数（如有）"},
    ]
    
    def _create_tools_section(self) -> QFrame:
        """创建龙头维度专属工具区"""
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
        
        title = QLabel("🔧 龙头分析工具")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        tools = [
            ("👑 龙头股列表", "查看各板块龙头股"),
            ("📊 连板梯队", "查看连板接力梯队结构"),
            ("📈 龙头对比", "对比多个主线龙头表现"),
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
        return f"龙头: {result.leader_stock} {result.leader_change:+.2f}%"




