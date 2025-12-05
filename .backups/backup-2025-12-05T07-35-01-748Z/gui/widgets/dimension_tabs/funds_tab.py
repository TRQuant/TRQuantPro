# -*- coding: utf-8 -*-
"""
资金维度Tab

权重：30%
评估主线题材的资金流强度
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from gui.styles.theme import Colors
from .base_dimension_tab import BaseDimensionTab


class FundsDimensionTab(BaseDimensionTab):
    """资金维度Tab"""
    
    DIMENSION_KEY = "funds"
    DIMENSION_NAME = "资金维度"
    DIMENSION_ICON = "💰"
    DIMENSION_COLOR = "#3B82F6"
    DIMENSION_WEIGHT = 0.30
    DIMENSION_DESC = "衡量主线题材的资金流强度。因子包括：主力资金净流入额及连续流入天数、大单成交占比、融资融券余额变化等。使用时间衰减逻辑，近期资金数据加权更高。\n\n📊 数据来源: 同花顺（通过AKShare），实时更新。数据为估算值，建议结合其他维度综合判断。下一阶段将接入聚宽JQData，提供交易所官方Level2数据。"
    
    FACTORS = [
        {"name": "主力净流入排名", "weight": 0.40, "desc": "当日净流入在所有板块中的排名百分位"},
        {"name": "资金流向强度", "weight": 0.25, "desc": "资金连续流入情况，净流入为正则加分"},
        {"name": "流入强度比", "weight": 0.20, "desc": "净流入/总流入，反映资金净流入强度"},
        {"name": "北向资金加成", "weight": 0.15, "desc": "北向资金当日是否净流入"},
    ]
    
    def _create_tools_section(self) -> QFrame:
        """创建资金维度专属工具区"""
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
        
        # 数据来源说明
        source_info = QFrame()
        source_info.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {self.DIMENSION_COLOR}30;
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        source_layout = QVBoxLayout(source_info)
        source_layout.setContentsMargins(8, 6, 8, 6)
        source_layout.setSpacing(4)
        
        source_title = QLabel("📊 数据来源说明")
        source_title.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        source_layout.addWidget(source_title)
        
        source_desc = QLabel(
            "当前: 同花顺（AKShare） - 实时估算值，数据精度⭐⭐⭐⭐\n"
            "下一阶段: 聚宽JQData - 交易所官方Level2数据，数据精度⭐⭐⭐⭐⭐"
        )
        source_desc.setStyleSheet(f"font-size: 10px; color: {Colors.TEXT_MUTED}; line-height: 1.4;")
        source_desc.setWordWrap(True)
        source_layout.addWidget(source_desc)
        
        layout.addWidget(source_info)
        
        title = QLabel("🔧 资金分析工具")
        title.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(8)
        
        # 工具按钮
        tools = [
            ("📊 资金流向图", "查看板块资金流向可视化"),
            ("📈 连续流入筛选", "筛选连续多日资金流入的板块"),
            ("💹 北向资金追踪", "追踪北向资金重点流入板块"),
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
        """获取原始数据文本"""
        return f"净流入: {result.net_inflow:+.2f}亿"

