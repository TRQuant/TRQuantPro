# -*- coding: utf-8 -*-
"""
投研分析面板 - 专业量化因子库与分析工具
包含完整的因子分类、计算方法、市场分析和选股工具
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QComboBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QGraphicsDropShadowEffect, QTextEdit, QSplitter, QGroupBox,
    QSpinBox, QDoubleSpinBox, QCheckBox, QLineEdit, QDialog,
    QDialogButtonBox, QFormLayout, QListWidget, QListWidgetItem,
    QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QColor, QFont
from datetime import datetime, timedelta
from pathlib import Path
import logging
import json

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles

logger = logging.getLogger(__name__)


# ============================================================
# 因子定义数据库
# ============================================================

FACTOR_DATABASE = {
    "value": {
        "name": "价值因子",
        "icon": "💰",
        "description": "衡量股票估值水平的因子，低估值股票通常具有更高的预期收益",
        "factors": [
            {
                "id": "pe_ttm",
                "name": "市盈率(TTM)",
                "formula": "股价 / 近12个月每股收益",
                "interpretation": "PE越低，估值越便宜。一般PE<20为低估值",
                "data_source": "财务数据",
                "direction": "negative",  # 越小越好
            },
            {
                "id": "pb",
                "name": "市净率",
                "formula": "股价 / 每股净资产",
                "interpretation": "PB越低，安全边际越高。PB<1为破净股",
                "data_source": "财务数据",
                "direction": "negative",
            },
            {
                "id": "ps_ttm",
                "name": "市销率(TTM)",
                "formula": "市值 / 近12个月营业收入",
                "interpretation": "适用于亏损但有收入的公司",
                "data_source": "财务数据",
                "direction": "negative",
            },
            {
                "id": "pcf",
                "name": "市现率",
                "formula": "市值 / 经营现金流",
                "interpretation": "现金流更真实反映盈利质量",
                "data_source": "财务数据",
                "direction": "negative",
            },
            {
                "id": "ev_ebitda",
                "name": "EV/EBITDA",
                "formula": "企业价值 / 息税折旧摊销前利润",
                "interpretation": "排除资本结构影响的估值指标",
                "data_source": "财务数据",
                "direction": "negative",
            },
            {
                "id": "dividend_yield",
                "name": "股息率",
                "formula": "每股股息 / 股价",
                "interpretation": "高股息率提供安全边际和现金回报",
                "data_source": "财务数据",
                "direction": "positive",  # 越大越好
            },
        ]
    },
    "growth": {
        "name": "成长因子",
        "icon": "📈",
        "description": "衡量公司业绩增长能力的因子，高成长股票通常享有估值溢价",
        "factors": [
            {
                "id": "revenue_growth_yoy",
                "name": "营收同比增长率",
                "formula": "(本期营收 - 去年同期营收) / 去年同期营收",
                "interpretation": "反映公司规模扩张速度，>20%为高增长",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "net_profit_growth_yoy",
                "name": "净利润同比增长率",
                "formula": "(本期净利润 - 去年同期净利润) / 去年同期净利润",
                "interpretation": "核心盈利增长指标，>30%为高增长",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "roe_growth",
                "name": "ROE增长率",
                "formula": "(本期ROE - 去年同期ROE) / 去年同期ROE",
                "interpretation": "盈利能力提升的信号",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "eps_growth_3y",
                "name": "EPS三年复合增长率",
                "formula": "(当前EPS/三年前EPS)^(1/3) - 1",
                "interpretation": "长期盈利增长能力",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "operating_profit_growth",
                "name": "营业利润增长率",
                "formula": "(本期营业利润 - 去年同期) / 去年同期",
                "interpretation": "主营业务盈利增长",
                "data_source": "财务数据",
                "direction": "positive",
            },
        ]
    },
    "quality": {
        "name": "质量因子",
        "icon": "⭐",
        "description": "衡量公司财务健康度和盈利质量的因子",
        "factors": [
            {
                "id": "roe",
                "name": "净资产收益率(ROE)",
                "formula": "净利润 / 平均股东权益",
                "interpretation": "衡量股东资本回报，>15%为优秀",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "roa",
                "name": "总资产收益率(ROA)",
                "formula": "净利润 / 平均总资产",
                "interpretation": "衡量资产利用效率，>5%为良好",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "gross_margin",
                "name": "毛利率",
                "formula": "(营业收入 - 营业成本) / 营业收入",
                "interpretation": "产品竞争力指标，>30%具有定价权",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "net_margin",
                "name": "净利率",
                "formula": "净利润 / 营业收入",
                "interpretation": "综合盈利能力，>10%为良好",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "asset_turnover",
                "name": "资产周转率",
                "formula": "营业收入 / 平均总资产",
                "interpretation": "资产运营效率",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "current_ratio",
                "name": "流动比率",
                "formula": "流动资产 / 流动负债",
                "interpretation": "短期偿债能力，1.5-2.0为健康",
                "data_source": "财务数据",
                "direction": "positive",
            },
            {
                "id": "debt_to_equity",
                "name": "资产负债率",
                "formula": "总负债 / 总资产",
                "interpretation": "财务杠杆，<60%较安全",
                "data_source": "财务数据",
                "direction": "negative",
            },
            {
                "id": "cash_flow_quality",
                "name": "现金流质量",
                "formula": "经营现金流 / 净利润",
                "interpretation": "盈利含金量，>1为优质",
                "data_source": "财务数据",
                "direction": "positive",
            },
        ]
    },
    "momentum": {
        "name": "动量因子",
        "icon": "🚀",
        "description": "基于价格趋势的因子，捕捉市场动能效应",
        "factors": [
            {
                "id": "momentum_20d",
                "name": "20日动量",
                "formula": "(当前价格 - 20日前价格) / 20日前价格",
                "interpretation": "短期价格趋势",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "momentum_60d",
                "name": "60日动量",
                "formula": "(当前价格 - 60日前价格) / 60日前价格",
                "interpretation": "中期价格趋势，剔除近期波动",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "momentum_120d",
                "name": "120日动量",
                "formula": "(当前价格 - 120日前价格) / 120日前价格",
                "interpretation": "半年趋势强度",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "relative_strength",
                "name": "相对强度(RS)",
                "formula": "个股涨幅 / 指数涨幅",
                "interpretation": "相对市场的超额表现",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "price_to_ma20",
                "name": "价格/MA20",
                "formula": "当前价格 / 20日均线",
                "interpretation": ">1表示短期强势",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "ma_cross",
                "name": "均线多头排列",
                "formula": "MA5 > MA10 > MA20 > MA60",
                "interpretation": "趋势确认信号",
                "data_source": "行情数据",
                "direction": "positive",
            },
        ]
    },
    "volatility": {
        "name": "波动因子",
        "icon": "📉",
        "description": "衡量价格波动风险的因子，低波动股票通常风险调整后收益更高",
        "factors": [
            {
                "id": "volatility_20d",
                "name": "20日波动率",
                "formula": "20日收益率标准差 × √252",
                "interpretation": "短期波动风险",
                "data_source": "行情数据",
                "direction": "negative",
            },
            {
                "id": "volatility_60d",
                "name": "60日波动率",
                "formula": "60日收益率标准差 × √252",
                "interpretation": "中期波动风险",
                "data_source": "行情数据",
                "direction": "negative",
            },
            {
                "id": "beta",
                "name": "Beta系数",
                "formula": "Cov(个股收益, 市场收益) / Var(市场收益)",
                "interpretation": "系统性风险敞口，<1为防御型",
                "data_source": "行情数据",
                "direction": "negative",
            },
            {
                "id": "max_drawdown",
                "name": "最大回撤",
                "formula": "(峰值 - 谷值) / 峰值",
                "interpretation": "历史最大亏损幅度",
                "data_source": "行情数据",
                "direction": "negative",
            },
            {
                "id": "downside_volatility",
                "name": "下行波动率",
                "formula": "负收益日的标准差",
                "interpretation": "下跌风险",
                "data_source": "行情数据",
                "direction": "negative",
            },
        ]
    },
    "liquidity": {
        "name": "流动性因子",
        "icon": "💧",
        "description": "衡量股票交易活跃度的因子",
        "factors": [
            {
                "id": "turnover_rate",
                "name": "换手率",
                "formula": "成交量 / 流通股本",
                "interpretation": "交易活跃度，过高可能是见顶信号",
                "data_source": "行情数据",
                "direction": "neutral",
            },
            {
                "id": "avg_volume_20d",
                "name": "20日平均成交额",
                "formula": "近20日成交额均值",
                "interpretation": "流动性水平",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "volume_ratio",
                "name": "量比",
                "formula": "当日成交量 / 5日平均成交量",
                "interpretation": ">1表示放量",
                "data_source": "行情数据",
                "direction": "neutral",
            },
            {
                "id": "amihud_illiquidity",
                "name": "Amihud非流动性",
                "formula": "|收益率| / 成交额",
                "interpretation": "价格冲击成本",
                "data_source": "行情数据",
                "direction": "negative",
            },
        ]
    },
    "sentiment": {
        "name": "情绪因子",
        "icon": "💭",
        "description": "衡量市场情绪和资金流向的因子",
        "factors": [
            {
                "id": "north_flow",
                "name": "北向资金流入",
                "formula": "北向资金净买入额",
                "interpretation": "外资动向，正向流入为利好",
                "data_source": "资金数据",
                "direction": "positive",
            },
            {
                "id": "main_flow",
                "name": "主力资金流入",
                "formula": "大单净买入额",
                "interpretation": "主力动向",
                "data_source": "资金数据",
                "direction": "positive",
            },
            {
                "id": "margin_balance",
                "name": "融资余额变化",
                "formula": "融资余额环比变化",
                "interpretation": "杠杆资金情绪",
                "data_source": "融资融券数据",
                "direction": "positive",
            },
            {
                "id": "analyst_rating",
                "name": "分析师评级",
                "formula": "买入评级占比",
                "interpretation": "机构观点",
                "data_source": "研报数据",
                "direction": "positive",
            },
        ]
    },
    "technical": {
        "name": "技术因子",
        "icon": "📊",
        "description": "基于技术分析的因子",
        "factors": [
            {
                "id": "rsi_14",
                "name": "RSI(14)",
                "formula": "100 - 100/(1+RS)",
                "interpretation": ">70超买, <30超卖",
                "data_source": "行情数据",
                "direction": "neutral",
            },
            {
                "id": "macd_signal",
                "name": "MACD信号",
                "formula": "DIF - DEA",
                "interpretation": "金叉买入，死叉卖出",
                "data_source": "行情数据",
                "direction": "positive",
            },
            {
                "id": "kdj_j",
                "name": "KDJ-J值",
                "formula": "3K - 2D",
                "interpretation": ">100超买, <0超卖",
                "data_source": "行情数据",
                "direction": "neutral",
            },
            {
                "id": "bollinger_position",
                "name": "布林带位置",
                "formula": "(价格 - 下轨) / (上轨 - 下轨)",
                "interpretation": "0-1之间，>0.8超买",
                "data_source": "行情数据",
                "direction": "neutral",
            },
        ]
    },
}


# ============================================================
# UI组件
# ============================================================

class MetricCard(QFrame):
    """指标卡片"""
    
    def __init__(self, title: str, value: str = "--", 
                 change: str = "", trend: str = "flat", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
            font-weight: 500;
        """)
        layout.addWidget(self.title_label)
        
        value_layout = QHBoxLayout()
        value_layout.setSpacing(8)
        
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        value_layout.addWidget(self.value_label)
        
        self.change_label = QLabel(change)
        self.update_trend(trend)
        value_layout.addWidget(self.change_label)
        value_layout.addStretch()
        
        layout.addLayout(value_layout)
    
    def update_value(self, value: str, change: str = "", trend: str = "flat"):
        self.value_label.setText(value)
        self.change_label.setText(change)
        self.update_trend(trend)
    
    def update_trend(self, trend: str):
        colors = {
            "up": Colors.UP,
            "down": Colors.DOWN,
            "flat": Colors.TEXT_MUTED,
        }
        color = colors.get(trend, Colors.TEXT_MUTED)
        self.change_label.setStyleSheet(f"""
            font-size: 13px;
            font-weight: 600;
            color: {color};
        """)


class FactorCategoryCard(QFrame):
    """因子分类卡片"""
    
    clicked = pyqtSignal(str)
    
    def __init__(self, category_id: str, data: dict, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {Colors.PRIMARY}88;
                background-color: {Colors.BG_CARD};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)
        
        # 顶部：图标和数量
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(data["icon"])
        icon_label.setStyleSheet("font-size: 28px;")
        top_layout.addWidget(icon_label)
        
        top_layout.addStretch()
        
        count_label = QLabel(f"{len(data['factors'])}个因子")
        count_label.setStyleSheet(f"""
            font-size: 11px;
            color: {Colors.TEXT_MUTED};
            background-color: {Colors.BG_SECONDARY};
            padding: 4px 8px;
            border-radius: 4px;
        """)
        top_layout.addWidget(count_label)
        
        layout.addLayout(top_layout)
        
        # 名称
        name_label = QLabel(data["name"])
        name_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(name_label)
        
        # 描述
        desc_label = QLabel(data["description"][:50] + "..." if len(data["description"]) > 50 else data["description"])
        desc_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
    
    def mousePressEvent(self, event):
        self.clicked.emit(self.category_id)
        super().mousePressEvent(event)


class FactorDetailPanel(QWidget):
    """因子详情面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_category = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # 标题栏
        header = QHBoxLayout()
        
        self.back_btn = QPushButton("← 返回")
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {Colors.PRIMARY};
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {Colors.ACCENT};
            }}
        """)
        header.addWidget(self.back_btn)
        
        self.title_label = QLabel("因子详情")
        self.title_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        header.addWidget(self.title_label)
        header.addStretch()
        
        layout.addLayout(header)
        
        # 因子列表
        self.factor_list = QListWidget()
        self.factor_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
            QListWidget::item {{
                padding: 16px;
                border-bottom: 1px solid {Colors.BORDER_DARK};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY}22;
            }}
        """)
        self.factor_list.itemClicked.connect(self.on_factor_selected)
        layout.addWidget(self.factor_list)
        
        # 因子详情区域
        self.detail_frame = QFrame()
        self.detail_frame.setStyleSheet(CardStyles.DEFAULT)
        self.detail_frame.setVisible(False)
        
        detail_layout = QVBoxLayout(self.detail_frame)
        detail_layout.setContentsMargins(20, 20, 20, 20)
        detail_layout.setSpacing(12)
        
        self.factor_name_label = QLabel()
        self.factor_name_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        detail_layout.addWidget(self.factor_name_label)
        
        self.factor_formula_label = QLabel()
        self.factor_formula_label.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.PRIMARY};
            background-color: {Colors.PRIMARY}11;
            padding: 12px;
            border-radius: 8px;
            font-family: {Typography.FONT_MONO};
        """)
        self.factor_formula_label.setWordWrap(True)
        detail_layout.addWidget(self.factor_formula_label)
        
        self.factor_interpretation_label = QLabel()
        self.factor_interpretation_label.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_SECONDARY};
            line-height: 1.6;
        """)
        self.factor_interpretation_label.setWordWrap(True)
        detail_layout.addWidget(self.factor_interpretation_label)
        
        # 数据源和方向
        info_layout = QHBoxLayout()
        
        self.data_source_label = QLabel()
        self.data_source_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
            background-color: {Colors.BG_SECONDARY};
            padding: 4px 8px;
            border-radius: 4px;
        """)
        info_layout.addWidget(self.data_source_label)
        
        self.direction_label = QLabel()
        self.direction_label.setStyleSheet(f"""
            font-size: 12px;
            padding: 4px 8px;
            border-radius: 4px;
        """)
        info_layout.addWidget(self.direction_label)
        
        info_layout.addStretch()
        detail_layout.addLayout(info_layout)
        
        layout.addWidget(self.detail_frame)
    
    def show_category(self, category_id: str):
        """显示因子分类"""
        self.current_category = category_id
        data = FACTOR_DATABASE.get(category_id, {})
        
        self.title_label.setText(f"{data.get('icon', '')} {data.get('name', '')}")
        
        self.factor_list.clear()
        for factor in data.get("factors", []):
            item = QListWidgetItem(f"📌 {factor['name']}")
            item.setData(Qt.ItemDataRole.UserRole, factor)
            self.factor_list.addItem(item)
        
        self.detail_frame.setVisible(False)
    
    def on_factor_selected(self, item: QListWidgetItem):
        """选中因子"""
        factor = item.data(Qt.ItemDataRole.UserRole)
        if not factor:
            return
        
        self.factor_name_label.setText(factor["name"])
        self.factor_formula_label.setText(f"计算公式: {factor['formula']}")
        self.factor_interpretation_label.setText(f"解读: {factor['interpretation']}")
        self.data_source_label.setText(f"📊 {factor['data_source']}")
        
        direction = factor.get("direction", "neutral")
        direction_text = {
            "positive": "↑ 越大越好",
            "negative": "↓ 越小越好",
            "neutral": "◆ 中性指标"
        }
        direction_color = {
            "positive": Colors.SUCCESS,
            "negative": Colors.ERROR,
            "neutral": Colors.WARNING
        }
        self.direction_label.setText(direction_text.get(direction, ""))
        self.direction_label.setStyleSheet(f"""
            font-size: 12px;
            color: {direction_color.get(direction, Colors.TEXT_MUTED)};
            background-color: {direction_color.get(direction, Colors.TEXT_MUTED)}22;
            padding: 4px 8px;
            border-radius: 4px;
        """)
        
        self.detail_frame.setVisible(True)


class StockScreenerDialog(QDialog):
    """选股器对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("多因子选股器")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
            }}
        """)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 标题
        title = QLabel("🔍 多因子选股器")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(title)
        
        # 因子选择区域
        factors_group = QGroupBox("选择因子条件")
        factors_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: 600;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }}
        """)
        factors_layout = QGridLayout(factors_group)
        
        self.factor_checks = {}
        row = 0
        for cat_id, cat_data in FACTOR_DATABASE.items():
            label = QLabel(f"{cat_data['icon']} {cat_data['name']}")
            label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-weight: 600;")
            factors_layout.addWidget(label, row, 0, 1, 4)
            row += 1
            
            col = 0
            for factor in cat_data["factors"][:4]:  # 只显示前4个
                check = QCheckBox(factor["name"])
                check.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
                factors_layout.addWidget(check, row, col)
                self.factor_checks[factor["id"]] = check
                col += 1
            row += 1
        
        layout.addWidget(factors_group)
        
        # 筛选条件
        filter_group = QGroupBox("筛选条件")
        filter_group.setStyleSheet(factors_group.styleSheet())
        filter_layout = QFormLayout(filter_group)
        
        self.universe_combo = QComboBox()
        self.universe_combo.addItems(["全市场", "沪深300", "中证500", "中证800", "创业板"])
        filter_layout.addRow("标的池:", self.universe_combo)
        
        self.min_market_cap = QSpinBox()
        self.min_market_cap.setRange(0, 10000)
        self.min_market_cap.setValue(50)
        self.min_market_cap.setSuffix(" 亿")
        filter_layout.addRow("最小市值:", self.min_market_cap)
        
        self.exclude_st = QCheckBox("剔除ST/*ST")
        self.exclude_st.setChecked(True)
        filter_layout.addRow("", self.exclude_st)
        
        layout.addWidget(filter_group)
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(ButtonStyles.SECONDARY)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        screen_btn = QPushButton("🔍 开始选股")
        screen_btn.setStyleSheet(ButtonStyles.PRIMARY)
        screen_btn.clicked.connect(self.run_screener)
        btn_layout.addWidget(screen_btn)
        
        layout.addLayout(btn_layout)
    
    def run_screener(self):
        """运行选股"""
        selected_factors = [fid for fid, check in self.factor_checks.items() if check.isChecked()]
        if not selected_factors:
            QMessageBox.warning(self, "提示", "请至少选择一个因子")
            return
        
        QMessageBox.information(
            self, "选股结果",
            f"已选择 {len(selected_factors)} 个因子进行选股\n\n"
            f"标的池: {self.universe_combo.currentText()}\n"
            f"最小市值: {self.min_market_cap.value()}亿\n\n"
            "注: 实际选股功能需要连接数据源后使用"
        )


class ResearchPanel(QWidget):
    """投研分析面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_connected = False
        self.init_ui()
        
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 使用堆叠布局切换视图
        self.stack = QStackedWidget()
        
        # 主视图
        self.main_view = self.create_main_view()
        self.stack.addWidget(self.main_view)
        
        # 因子详情视图
        self.factor_detail_view = FactorDetailPanel()
        self.factor_detail_view.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.stack.addWidget(self.factor_detail_view)
        
        layout.addWidget(self.stack)
    
    def create_main_view(self) -> QWidget:
        """创建主视图"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(24)
        
        # 标题栏
        header = self.create_header()
        layout.addLayout(header)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 16, 0)
        scroll_layout.setSpacing(24)
        
        # 市场概览
        market_section = self.create_market_section()
        scroll_layout.addWidget(market_section)
        
        # 量化因子库
        factor_section = self.create_factor_library_section()
        scroll_layout.addWidget(factor_section)
        
        # 分析工具
        tools_section = self.create_tools_section()
        scroll_layout.addWidget(tools_section)
        
        # 智能推荐
        recommend_section = self.create_recommend_section()
        scroll_layout.addWidget(recommend_section)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        return widget
    
    def create_header(self) -> QHBoxLayout:
        """创建标题栏"""
        header = QHBoxLayout()
        
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)
        
        title = QLabel("🔬 投研分析")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("专业量化因子库 · 多维度分析 · 智能选股")
        subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.TEXT_MUTED};
        """)
        title_layout.addWidget(subtitle)
        
        header.addWidget(title_widget)
        header.addStretch()
        
        # 状态
        self.status_badge = QLabel("● 未连接")
        self.status_badge.setStyleSheet(f"""
            background-color: {Colors.TEXT_MUTED}22;
            color: {Colors.TEXT_MUTED};
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
        """)
        header.addWidget(self.status_badge)
        
        # 选股器按钮
        screener_btn = QPushButton("🔍 选股器")
        screener_btn.setStyleSheet(ButtonStyles.SECONDARY)
        screener_btn.setFixedHeight(40)
        screener_btn.clicked.connect(self.open_screener)
        header.addWidget(screener_btn)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 8px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
            }}
        """)
        refresh_btn.setFixedSize(40, 40)
        refresh_btn.clicked.connect(self.refresh_data)
        header.addWidget(refresh_btn)
        
        return header
    
    def create_market_section(self) -> QFrame:
        """创建市场概览区域"""
        section = QFrame()
        section.setStyleSheet(CardStyles.DEFAULT)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        title = QLabel("📈 市场概览")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(title)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        
        self.market_cards = {}
        
        metrics = [
            ("上证指数", "3,150.23", "+0.85%", "up"),
            ("深证成指", "10,234.56", "+1.12%", "up"),
            ("创业板指", "2,045.67", "-0.32%", "down"),
            ("北向资金", "+52.3亿", "净流入", "up"),
        ]
        
        for name, value, change, trend in metrics:
            card = MetricCard(name, value, change, trend)
            self.market_cards[name] = card
            cards_layout.addWidget(card)
        
        layout.addLayout(cards_layout)
        
        return section
    
    def create_factor_library_section(self) -> QFrame:
        """创建量化因子库区域"""
        section = QFrame()
        section.setStyleSheet(CardStyles.DEFAULT)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # 标题
        title_layout = QHBoxLayout()
        
        title = QLabel("📊 量化因子库")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        count_label = QLabel(f"共 {sum(len(d['factors']) for d in FACTOR_DATABASE.values())} 个因子")
        count_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
            background-color: {Colors.BG_SECONDARY};
            padding: 4px 12px;
            border-radius: 10px;
        """)
        title_layout.addWidget(count_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 因子分类卡片网格
        grid = QGridLayout()
        grid.setSpacing(16)
        
        for i, (cat_id, cat_data) in enumerate(FACTOR_DATABASE.items()):
            card = FactorCategoryCard(cat_id, cat_data)
            card.clicked.connect(self.on_category_clicked)
            grid.addWidget(card, i // 4, i % 4)
        
        layout.addLayout(grid)
        
        return section
    
    def create_tools_section(self) -> QFrame:
        """创建分析工具区域"""
        section = QFrame()
        section.setStyleSheet(CardStyles.DEFAULT)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        title = QLabel("🛠️ 分析工具")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(title)
        
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(16)
        
        tools = [
            ("🔍", "多因子选股", "根据因子条件筛选股票", self.open_screener),
            ("📊", "因子分析", "分析因子有效性和相关性", self.open_factor_analysis),
            ("📈", "行业轮动", "追踪行业资金流向", self.open_industry_rotation),
            ("🎯", "组合优化", "构建最优投资组合", self.open_portfolio_optimizer),
        ]
        
        for icon, name, desc, callback in tools:
            tool_card = QFrame()
            tool_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_SECONDARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 10px;
                }}
                QFrame:hover {{
                    border-color: {Colors.PRIMARY}66;
                }}
            """)
            tool_card.setCursor(Qt.CursorShape.PointingHandCursor)
            
            tool_layout = QVBoxLayout(tool_card)
            tool_layout.setContentsMargins(16, 16, 16, 16)
            tool_layout.setSpacing(8)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 24px;")
            tool_layout.addWidget(icon_label)
            
            name_label = QLabel(name)
            name_label.setStyleSheet(f"""
                font-size: 14px;
                font-weight: 600;
                color: {Colors.TEXT_PRIMARY};
            """)
            tool_layout.addWidget(name_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"""
                font-size: 11px;
                color: {Colors.TEXT_MUTED};
            """)
            tool_layout.addWidget(desc_label)
            
            tool_card.mousePressEvent = lambda e, cb=callback: cb()
            tools_layout.addWidget(tool_card)
        
        layout.addLayout(tools_layout)
        
        return section
    
    def create_recommend_section(self) -> QFrame:
        """创建智能推荐区域"""
        section = QFrame()
        section.setStyleSheet(CardStyles.DEFAULT)
        
        layout = QVBoxLayout(section)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        title_layout = QHBoxLayout()
        
        title = QLabel("🤖 智能推荐")
        title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        badge = QLabel("AI驱动")
        badge.setStyleSheet(f"""
            background-color: {Colors.PRIMARY}33;
            color: {Colors.PRIMARY};
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 600;
        """)
        title_layout.addWidget(badge)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # 推荐表格
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["股票代码", "股票名称", "综合评分", "主要因子", "信号强度", "操作"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                border: none;
                gridline-color: {Colors.BORDER_DARK};
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Colors.BORDER_DARK};
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.PRIMARY}22;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_MUTED};
                padding: 12px;
                border: none;
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
                font-weight: 600;
                font-size: 12px;
            }}
        """)
        
        recommendations = [
            ("600519.SH", "贵州茅台", "92", "质量+价值", "强", Colors.SUCCESS),
            ("000858.SZ", "五粮液", "85", "动量+质量", "较强", Colors.SUCCESS),
            ("601318.SH", "中国平安", "78", "价值+成长", "中等", Colors.WARNING),
            ("000333.SZ", "美的集团", "75", "质量+资金", "中等", Colors.WARNING),
            ("002415.SZ", "海康威视", "72", "成长+动量", "较弱", Colors.TEXT_MUTED),
        ]
        
        table.setRowCount(len(recommendations))
        for row, (code, name, score, factors, signal, color) in enumerate(recommendations):
            table.setItem(row, 0, QTableWidgetItem(code))
            table.setItem(row, 1, QTableWidgetItem(name))
            
            score_item = QTableWidgetItem(score)
            score_item.setForeground(QColor(color))
            table.setItem(row, 2, score_item)
            
            table.setItem(row, 3, QTableWidgetItem(factors))
            
            signal_item = QTableWidgetItem(signal)
            signal_item.setForeground(QColor(color))
            table.setItem(row, 4, signal_item)
            
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(4, 4, 4, 4)
            
            detail_btn = QPushButton("详情")
            detail_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.PRIMARY}22;
                    color: {Colors.PRIMARY};
                    border: none;
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.PRIMARY}44;
                }}
            """)
            btn_layout.addWidget(detail_btn)
            
            table.setCellWidget(row, 5, btn_widget)
        
        table.setFixedHeight(300)
        layout.addWidget(table)
        
        return section
    
    def on_category_clicked(self, category_id: str):
        """因子分类点击"""
        self.factor_detail_view.show_category(category_id)
        self.stack.setCurrentIndex(1)
    
    def open_screener(self):
        """打开选股器"""
        dialog = StockScreenerDialog(self)
        dialog.exec()
    
    def open_factor_analysis(self):
        """打开因子分析"""
        QMessageBox.information(self, "因子分析", "因子分析工具正在开发中...")
    
    def open_industry_rotation(self):
        """打开行业轮动"""
        QMessageBox.information(self, "行业轮动", "行业轮动分析工具正在开发中...")
    
    def open_portfolio_optimizer(self):
        """打开组合优化"""
        QMessageBox.information(self, "组合优化", "组合优化工具正在开发中...")
    
    def check_connection(self):
        """检查数据连接状态"""
        try:
            import jqdatasdk as jq
            count = jq.get_query_count()
            if count:
                self.is_connected = True
                self.status_badge.setText("● 已连接")
                self.status_badge.setStyleSheet(f"""
                    background-color: {Colors.SUCCESS}22;
                    color: {Colors.SUCCESS};
                    border-radius: 12px;
                    padding: 6px 16px;
                    font-size: 12px;
                    font-weight: 600;
                """)
                self.refresh_timer.start(60000)
                self.refresh_data()
                return True
        except:
            pass
        
        self.is_connected = False
        self.status_badge.setText("● 未连接")
        self.status_badge.setStyleSheet(f"""
            background-color: {Colors.TEXT_MUTED}22;
            color: {Colors.TEXT_MUTED};
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
        """)
        return False
    
    def refresh_data(self):
        """刷新数据"""
        if not self.is_connected:
            return
        
        try:
            import jqdatasdk as jq
            
            indices = {
                "上证指数": "000001.XSHG",
                "深证成指": "399001.XSHE",
                "创业板指": "399006.XSHE",
            }
            
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
            
            for name, code in indices.items():
                try:
                    df = jq.get_price(code, start_date=start_date, end_date=end_date, 
                                     frequency='daily', fields=['close'])
                    if df is not None and len(df) >= 2:
                        current = df['close'].iloc[-1]
                        prev = df['close'].iloc[-2]
                        change = (current - prev) / prev * 100
                        trend = "up" if change > 0 else "down" if change < 0 else "flat"
                        
                        if name in self.market_cards:
                            self.market_cards[name].update_value(
                                f"{current:,.2f}",
                                f"{'+' if change > 0 else ''}{change:.2f}%",
                                trend
                            )
                except Exception as e:
                    logger.warning(f"获取{name}数据失败: {e}")
                    
        except Exception as e:
            logger.error(f"刷新数据失败: {e}")
