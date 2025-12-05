# -*- coding: utf-8 -*-
"""
政策维度Tab

权重：15%
评估主线获得的政策支撑力度
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from gui.styles.theme import Colors
from .base_dimension_tab import BaseDimensionTab


class PolicyDimensionTab(BaseDimensionTab):
    """政策维度Tab"""
    
    DIMENSION_KEY = "policy"
    DIMENSION_NAME = "政策维度"
    DIMENSION_ICON = "📜"
    DIMENSION_COLOR = "#8B5CF6"
    DIMENSION_WEIGHT = 0.15
    DIMENSION_DESC = "评估主线获得的政策支撑力度，包括政府政策、产业扶持和重大事件驱动等因子。根据政策文件级别赋分（国家级政策加权最高，地方扶持其次），并考虑时效衰减。"
    
    FACTORS = [
        {"name": "政策关联度", "weight": 0.50, "desc": "是否为当前政策重点支持方向"},
        {"name": "事件催化", "weight": 0.30, "desc": "近期是否有重大政策事件"},
        {"name": "产业趋势", "weight": 0.20, "desc": "行业是否处于上升周期"},
    ]
    
    def _create_tools_section(self) -> QFrame:
        """创建政策维度专属工具区"""
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
        
        title = QLabel("🔧 政策分析工具")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        tools = [
            ("📋 政策列表", "查看近期相关政策文件"),
            ("🔍 关键词搜索", "搜索特定政策关键词"),
            ("📅 政策时间轴", "查看政策发布时间轴"),
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
        dim_score = result.policy_score
        policy_level = "高" if dim_score.score >= 70 else ("中" if dim_score.score >= 50 else "低")
        return f"政策关联: {policy_level}"




