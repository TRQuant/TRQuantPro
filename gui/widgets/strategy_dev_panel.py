# -*- coding: utf-8 -*-
"""
策略开发面板 - 统一的策略开发工作台
=====================================

整合功能：
- 实战策略库（A股有效策略）
- 策略生成器（因子组合 + 平台选择）
- 策略编辑器（Git集成 + Cursor打开）
- AI助手（预留接口 + Cursor集成）
- 回测验证（PTrade结果导入）
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QComboBox, QTextEdit, QLineEdit,
    QSpinBox, QDoubleSpinBox, QTabWidget, QGridLayout,
    QGroupBox, QCheckBox, QMessageBox, QFileDialog,
    QSplitter, QListWidget, QListWidgetItem, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QTreeWidget,
    QTreeWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal, QUrl, QProcess
from PyQt6.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat, QDesktopServices
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys
import os
import re
import logging

from gui.styles.theme import Colors, ButtonStyles

logger = logging.getLogger(__name__)


# ============================================================
# 实战策略数据库
# ============================================================
PRACTICAL_STRATEGIES = [
    {
        "id": "reversal_5d",
        "name": "短期反转策略",
        "category": "反转",
        "difficulty": "入门",
        "expected_return": "年化15-25%",
        "max_drawdown": "20-30%",
        "sharpe": "0.8-1.2",
        "turnover": "高（周度调仓）",
        "capacity": "中等（50亿以内）",
        "effectiveness": "★★★★★",
        "description": "A股最强因子！利用散户情绪过度反应，买入近期下跌的股票。",
        "logic": "散户主导的A股市场存在明显的过度反应，短期下跌的股票往往会反弹。",
        "factors": ["5日收益率（负向）"],
        "params": {
            "stock_pool": "中证500/中证1000",
            "hold_num": 30,
            "rebalance": "每周",
        },
        "backtest_period": "2015-2024",
        "reference_link": "因子库 → 反转因子",
        "code_template": "reversal_5d_template",
    },
    {
        "id": "quality_value",
        "name": "质量价值组合",
        "category": "多因子",
        "difficulty": "中级",
        "expected_return": "年化12-18%",
        "max_drawdown": "15-25%",
        "sharpe": "0.7-1.0",
        "turnover": "低（月度调仓）",
        "capacity": "大（100亿+）",
        "effectiveness": "★★★★☆",
        "description": "巴菲特风格：买入高质量且便宜的股票，长期持有。",
        "logic": "高ROE代表公司质量，低PE代表估值便宜，两者结合是价值投资的核心。",
        "factors": ["ROE", "EP（市盈率倒数）"],
        "params": {
            "stock_pool": "沪深300",
            "hold_num": 30,
            "rebalance": "每月",
        },
        "backtest_period": "2010-2024",
        "reference_link": "因子库 → 质量因子、价值因子",
        "code_template": "quality_value_template",
    },
    {
        "id": "momentum_quality",
        "name": "动量质量策略",
        "category": "多因子",
        "difficulty": "中级",
        "expected_return": "年化15-25%",
        "max_drawdown": "25-35%",
        "sharpe": "0.6-0.9",
        "turnover": "中等（月度调仓）",
        "capacity": "中等（50亿以内）",
        "effectiveness": "★★★★☆",
        "description": "追涨高质量股票，结合趋势和基本面。",
        "logic": "动量效应在中期有效，叠加质量筛选可以避免追涨垃圾股。",
        "factors": ["12-1月动量", "ROE", "毛利率"],
        "params": {
            "stock_pool": "中证500",
            "hold_num": 30,
            "rebalance": "每月",
        },
        "backtest_period": "2010-2024",
        "reference_link": "因子库 → 动量因子、质量因子",
        "code_template": "momentum_quality_template",
    },
    {
        "id": "low_volatility",
        "name": "低波动策略",
        "category": "风险",
        "difficulty": "入门",
        "expected_return": "年化10-15%",
        "max_drawdown": "10-18%",
        "sharpe": "0.8-1.2",
        "turnover": "低（季度调仓）",
        "capacity": "大（100亿+）",
        "effectiveness": "★★★★☆",
        "description": "防御型策略：买入低波动股票，熊市表现好。",
        "logic": "低波动异象：低风险股票长期收益不低于高风险股票，且回撤更小。",
        "factors": ["60日波动率（负向）"],
        "params": {
            "stock_pool": "沪深300",
            "hold_num": 50,
            "rebalance": "每季度",
        },
        "backtest_period": "2010-2024",
        "reference_link": "因子库 → 波动因子",
        "code_template": "low_volatility_template",
    },
    {
        "id": "dividend_yield",
        "name": "高股息策略",
        "category": "价值",
        "difficulty": "入门",
        "expected_return": "年化8-12%",
        "max_drawdown": "15-20%",
        "sharpe": "0.6-0.9",
        "turnover": "低（年度调仓）",
        "capacity": "大（100亿+）",
        "effectiveness": "★★★☆☆",
        "description": "稳健型策略：买入高股息股票，获取稳定现金流。",
        "logic": "高股息通常意味着公司盈利稳定、估值合理，适合长期投资。",
        "factors": ["股息率"],
        "params": {
            "stock_pool": "沪深300",
            "hold_num": 30,
            "rebalance": "每年",
        },
        "backtest_period": "2010-2024",
        "reference_link": "因子库 → 价值因子",
        "code_template": "dividend_yield_template",
    },
    {
        "id": "small_value",
        "name": "小市值价值策略",
        "category": "多因子",
        "difficulty": "中级",
        "expected_return": "年化18-30%",
        "max_drawdown": "30-45%",
        "sharpe": "0.5-0.8",
        "turnover": "中等（月度调仓）",
        "capacity": "小（10亿以内）",
        "effectiveness": "★★★☆☆",
        "description": "高风险高收益：小市值+低估值，牛市弹性大。",
        "logic": "小市值效应在A股长期有效，但注册制后有所减弱，需配合价值筛选。",
        "factors": ["市值（负向）", "EP"],
        "params": {
            "stock_pool": "全A股（排除ST）",
            "hold_num": 50,
            "rebalance": "每月",
        },
        "backtest_period": "2015-2024",
        "reference_link": "因子库 → 规模因子、价值因子",
        "code_template": "small_value_template",
    },
    {
        "id": "northbound_flow",
        "name": "北向资金跟踪",
        "category": "资金流",
        "difficulty": "中级",
        "expected_return": "年化10-18%",
        "max_drawdown": "20-30%",
        "sharpe": "0.5-0.8",
        "turnover": "中等（周度调仓）",
        "capacity": "大（100亿+）",
        "effectiveness": "★★★☆☆",
        "description": "跟踪聪明钱：买入北向资金持续流入的股票。",
        "logic": "北向资金代表外资偏好，通常具有更长的投资视野和更专业的研究能力。",
        "factors": ["北向资金净流入", "北向持股比例变化"],
        "params": {
            "stock_pool": "沪深港通标的",
            "hold_num": 30,
            "rebalance": "每周",
        },
        "backtest_period": "2017-2024",
        "reference_link": "因子库 → 情绪因子",
        "code_template": "northbound_flow_template",
    },
    {
        "id": "earnings_surprise",
        "name": "业绩超预期策略",
        "category": "事件",
        "difficulty": "高级",
        "expected_return": "年化15-25%",
        "max_drawdown": "20-30%",
        "sharpe": "0.6-1.0",
        "turnover": "中等（季度调仓）",
        "capacity": "中等（50亿以内）",
        "effectiveness": "★★★☆☆",
        "description": "事件驱动：买入业绩超预期的股票。",
        "logic": "业绩超预期后股价通常会持续上涨，存在漂移效应。",
        "factors": ["业绩预告/快报超预期幅度", "分析师预期修正"],
        "params": {
            "stock_pool": "全A股",
            "hold_num": 30,
            "rebalance": "财报季后",
        },
        "backtest_period": "2015-2024",
        "reference_link": "因子库 → 情绪因子",
        "code_template": "earnings_surprise_template",
    },
    {
        "id": "multi_factor_neutral",
        "name": "市场中性策略",
        "category": "对冲",
        "difficulty": "高级",
        "expected_return": "年化8-15%",
        "max_drawdown": "5-10%",
        "sharpe": "1.5-2.5",
        "turnover": "高（周度调仓）",
        "capacity": "中等（30亿以内）",
        "effectiveness": "★★★★☆",
        "description": "对冲策略：多因子选股+股指期货对冲，获取纯Alpha。",
        "logic": "通过股指期货对冲市场风险，只保留因子带来的超额收益。",
        "factors": ["反转", "质量", "动量（组合）"],
        "params": {
            "stock_pool": "沪深300成分股",
            "hold_num": 50,
            "rebalance": "每周",
            "hedge": "IF股指期货",
        },
        "backtest_period": "2015-2024",
        "reference_link": "因子库 → 多因子组合",
        "code_template": "multi_factor_neutral_template",
    },
    {
        "id": "index_enhance",
        "name": "指数增强策略",
        "category": "增强",
        "difficulty": "高级",
        "expected_return": "年化超额5-10%",
        "max_drawdown": "跟踪误差3-5%",
        "sharpe": "信息比率1.5+",
        "turnover": "中等（月度调仓）",
        "capacity": "大（100亿+）",
        "effectiveness": "★★★★☆",
        "description": "在跟踪指数的基础上获取超额收益。",
        "logic": "控制行业和风格偏离，通过多因子选股获取稳定的超额收益。",
        "factors": ["反转", "质量", "价值（行业中性）"],
        "params": {
            "stock_pool": "沪深300成分股",
            "hold_num": 100,
            "rebalance": "每月",
            "benchmark": "沪深300指数",
        },
        "backtest_period": "2015-2024",
        "reference_link": "因子库 → 多因子组合",
        "code_template": "index_enhance_template",
    },
]


# ============================================================
# 策略代码模板（增强注释版）
# ============================================================
STRATEGY_TEMPLATES = {
    "reversal_5d_template": '''# -*- coding: utf-8 -*-
"""
================================================================================
短期反转策略 - PTrade版本
================================================================================
【策略名称】短期反转策略 (5-Day Reversal Strategy)
【策略类型】单因子策略
【核心因子】5日收益率（负向）
【理论基础】
    A股市场散户占比高，存在明显的过度反应现象。当股票短期下跌后，
    往往会出现均值回归，即"跌多了会反弹"。这是A股最有效的因子之一。
    
【预期表现】
    - 年化收益: 15-25%
    - 最大回撤: 20-30%
    - 夏普比率: 0.8-1.2
    - 换手率: 高（周度调仓）
    
【风险提示】
    - 在趋势性下跌市场中可能持续亏损
    - 小市值股票流动性风险
    - 需要较高的交易频率
    
【参考文献】
    - Jegadeesh, N. (1990). Evidence of Predictable Behavior of Security Returns
    - A股反转因子研究报告 - 各大券商金工研报
================================================================================
"""

# =============================================================================
# 策略初始化函数
# =============================================================================
def initialize(context):
    """
    策略初始化 - 在策略开始运行时调用一次
    
    参数:
        context: 策略上下文对象，包含账户信息、持仓信息等
    
    功能:
        1. 设置策略参数（股票池、持仓数量、调仓频率）
        2. 初始化全局变量
        3. 打印策略配置信息
    """
    # -------------------------------------------------------------------------
    # 策略核心参数配置
    # -------------------------------------------------------------------------
    g.stock_pool = '000905.XSHG'  # 股票池：中证500指数成分股
                                   # 可选: '000300.XSHG'(沪深300), 
                                   #       '000852.XSHG'(中证1000)
    
    g.hold_num = 30               # 持仓股票数量
                                   # 建议范围: 20-50只，数量越多分散风险越好
    
    g.rebalance_day = 0           # 调仓日：每周的第几个交易日
                                   # 0=周一, 1=周二, ..., 4=周五
    
    # -------------------------------------------------------------------------
    # 打印策略配置信息
    # -------------------------------------------------------------------------
    log.info("=" * 60)
    log.info("【短期反转策略】初始化完成")
    log.info(f"  股票池: {g.stock_pool}")
    log.info(f"  持仓数量: {g.hold_num} 只")
    log.info(f"  调仓日: 每周第 {g.rebalance_day + 1} 个交易日")
    log.info("=" * 60)


# =============================================================================
# 盘前准备函数
# =============================================================================
def before_trading_start(context, data):
    """
    盘前准备 - 每个交易日开盘前调用
    
    参数:
        context: 策略上下文
        data: 数据对象
    
    功能:
        1. 获取最新的股票池成分股
        2. 设置可交易股票范围
    """
    # 获取指数成分股
    g.stocks = get_index_stocks(g.stock_pool)
    
    # 设置股票池（用于行情订阅）
    set_universe(g.stocks)
    
    log.info(f"[盘前] 股票池更新完成，共 {len(g.stocks)} 只股票")


# =============================================================================
# 盘中交易函数
# =============================================================================
def handle_data(context, data):
    """
    盘中交易 - 每个交易时间点调用
    
    参数:
        context: 策略上下文，包含当前时间、账户信息等
        data: 行情数据对象
    
    核心逻辑:
        1. 判断是否为调仓日
        2. 计算5日收益率因子
        3. 选择跌幅最大的股票
        4. 执行调仓
    """
    # -------------------------------------------------------------------------
    # Step 1: 判断是否为调仓日
    # -------------------------------------------------------------------------
    if context.current_dt.weekday() != g.rebalance_day:
        return  # 非调仓日，直接返回
    
    log.info(f"[调仓日] {context.current_dt.strftime('%Y-%m-%d')}")
    
    # -------------------------------------------------------------------------
    # Step 2: 计算5日收益率因子
    # -------------------------------------------------------------------------
    # 获取过去6天的收盘价（计算5日收益率需要6个数据点）
    prices = history(6, '1d', 'close', g.stocks, df=True)
    
    # 计算5日收益率: (今日收盘价 / 5日前收盘价) - 1
    returns_5d = (prices.iloc[-1] / prices.iloc[0] - 1).dropna()
    
    log.info(f"[因子计算] 5日收益率计算完成，有效股票: {len(returns_5d)} 只")
    
    # -------------------------------------------------------------------------
    # Step 3: 选股 - 选择跌幅最大的股票（反转因子）
    # -------------------------------------------------------------------------
    # nsmallest: 选择收益率最小（跌幅最大）的股票
    target_stocks = returns_5d.nsmallest(g.hold_num).index.tolist()
    
    log.info(f"[选股结果] 目标持仓: {len(target_stocks)} 只")
    
    # -------------------------------------------------------------------------
    # Step 4: 执行调仓
    # -------------------------------------------------------------------------
    rebalance(context, target_stocks)


# =============================================================================
# 调仓执行函数
# =============================================================================
def rebalance(context, target_stocks):
    """
    执行调仓操作
    
    参数:
        context: 策略上下文
        target_stocks: 目标持仓股票列表
    
    逻辑:
        1. 卖出不在目标列表中的股票
        2. 等权重买入目标股票
    """
    # -------------------------------------------------------------------------
    # Step 1: 卖出操作
    # -------------------------------------------------------------------------
    sell_count = 0
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)  # 目标持仓为0，即全部卖出
            sell_count += 1
    
    if sell_count > 0:
        log.info(f"[卖出] 卖出 {sell_count} 只股票")
    
    # -------------------------------------------------------------------------
    # Step 2: 买入操作 - 等权重配置
    # -------------------------------------------------------------------------
    if len(target_stocks) > 0:
        # 计算每只股票的目标权重
        weight = 1.0 / len(target_stocks)
        
        buy_count = 0
        for stock in target_stocks:
            order_target_percent(stock, weight)  # 按百分比买入
            buy_count += 1
        
        log.info(f"[买入] 买入 {buy_count} 只股票，每只权重: {weight:.2%}")
    
    log.info("[调仓完成]")
''',

    "quality_value_template": '''# -*- coding: utf-8 -*-
"""
质量价值组合策略 - PTrade版本
============================
策略逻辑：买入高ROE且低PE的股票
"""

def initialize(context):
    """初始化"""
    g.stock_pool = '000300.XSHG'  # 沪深300
    g.hold_num = 30
    g.roe_weight = 0.5
    g.ep_weight = 0.5
    
    log.info("质量价值组合策略初始化完成")

def before_trading_start(context, data):
    """盘前准备"""
    g.stocks = get_index_stocks(g.stock_pool)
    set_universe(g.stocks)

def handle_data(context, data):
    """每月第一个交易日调仓"""
    if context.current_dt.day > 5:
        return
    
    # 获取基本面数据
    df = get_fundamentals(
        query(valuation.code, valuation.pe_ratio, indicator.roe)
        .filter(valuation.code.in_(g.stocks))
        .filter(valuation.pe_ratio > 0)
        .filter(indicator.roe > 0)
    )
    
    if df.empty:
        return
    
    # 计算因子得分
    df['ep'] = 1 / df['pe_ratio']
    df['roe_rank'] = df['roe'].rank(ascending=False)
    df['ep_rank'] = df['ep'].rank(ascending=False)
    df['score'] = g.roe_weight * df['roe_rank'] + g.ep_weight * df['ep_rank']
    
    # 选股
    target_stocks = df.nsmallest(g.hold_num, 'score')['code'].tolist()
    
    # 调仓
    rebalance(context, target_stocks)

def rebalance(context, target_stocks):
    """调仓函数"""
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)
    
    if len(target_stocks) > 0:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)
''',
}


# ============================================================
# Python语法高亮
# ============================================================
class PythonHighlighter(QSyntaxHighlighter):
    """Python语法高亮"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # 关键字
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#cba6f7"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while',
            'with', 'yield', 'self'
        ]
        for word in keywords:
            pattern = rf'\b{word}\b'
            self.highlighting_rules.append((re.compile(pattern), keyword_format))
        
        # 字符串
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a6e3a1"))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        
        # 数字
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#fab387"))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\.?[0-9]*\b'), number_format))
        
        # 注释 - 使用更亮的灰色以提高可读性
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#9ca3af"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'#[^\n]*'), comment_format))
    
    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)


# ============================================================
# 策略开发面板主类
# ============================================================
class StrategyDevPanel(QWidget):
    """统一策略开发面板"""
    
    # 信号
    strategy_ready = pyqtSignal(str, dict)  # 策略文件路径, 参数
    run_backtest = pyqtSignal(str, dict)    # 策略名称, 参数
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_strategy = None
        self.current_code = ""
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建Tab控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
            QTabBar::tab {{
                background: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_SECONDARY};
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 13px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {Colors.PRIMARY};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        
        # 添加选项卡 - AI策略助手作为首页，介绍开发流程
        self.tab_widget.addTab(self._create_ai_guide_tab(), "🤖 AI策略助手")
        self.tab_widget.addTab(self._create_strategies_tab(), "📚 实战策略库")
        self.tab_widget.addTab(self._create_generator_tab(), "🔧 策略生成器")
        self.tab_widget.addTab(self._create_editor_tab(), "📝 策略编辑器")
        # 回测验证功能已移至"回测验证"模块，此处提供快捷跳转
        
        layout.addWidget(self.tab_widget)
    
    # ============================================================
    # Tab 1: 实战策略库
    # ============================================================
    def _create_strategies_tab(self) -> QWidget:
        """创建实战策略库选项卡"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 左侧：策略列表
        left_panel = QFrame()
        left_panel.setFixedWidth(320)
        left_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border-right: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(12)
        
        # 标题
        title = QLabel("📚 A股实战策略")
        title.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        left_layout.addWidget(title)
        
        subtitle = QLabel(f"共 {len(PRACTICAL_STRATEGIES)} 个经过验证的策略")
        subtitle.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED};")
        left_layout.addWidget(subtitle)
        
        # 分类筛选
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(8)
        
        self.strategy_filter = QComboBox()
        self.strategy_filter.addItems(["全部", "反转", "多因子", "价值", "风险", "资金流", "事件", "对冲", "增强"])
        self.strategy_filter.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 6px 12px;
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        self.strategy_filter.currentTextChanged.connect(self._filter_strategies)
        filter_layout.addWidget(self.strategy_filter)
        
        left_layout.addLayout(filter_layout)
        
        # 策略列表
        self.strategy_list = QListWidget()
        self.strategy_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY}30;
            }}
            QListWidget::item:hover {{
                background-color: {Colors.BG_HOVER};
            }}
        """)
        self.strategy_list.itemClicked.connect(self._on_strategy_selected)
        self._load_strategy_list()
        left_layout.addWidget(self.strategy_list)
        
        layout.addWidget(left_panel)
        
        # 右侧：策略详情
        right_panel = QScrollArea()
        right_panel.setWidgetResizable(True)
        right_panel.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
        """)
        
        self.strategy_detail = QWidget()
        self.strategy_detail_layout = QVBoxLayout(self.strategy_detail)
        self.strategy_detail_layout.setContentsMargins(24, 24, 24, 24)
        self.strategy_detail_layout.setSpacing(16)
        
        # 默认提示
        welcome = QLabel("👈 选择左侧策略查看详情")
        welcome.setStyleSheet(f"font-size: 16px; color: {Colors.TEXT_MUTED};")
        welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.strategy_detail_layout.addWidget(welcome)
        self.strategy_detail_layout.addStretch()
        
        right_panel.setWidget(self.strategy_detail)
        layout.addWidget(right_panel)
        
        return widget
    
    def _load_strategy_list(self, filter_category: str = "全部"):
        """加载策略列表"""
        self.strategy_list.clear()
        
        for strategy in PRACTICAL_STRATEGIES:
            if filter_category != "全部" and strategy["category"] != filter_category:
                continue
            
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, strategy)
            
            # 创建自定义显示
            display_text = f"{strategy['name']}\n"
            display_text += f"📊 {strategy['category']} | {strategy['effectiveness']}"
            item.setText(display_text)
            
            self.strategy_list.addItem(item)
    
    def _filter_strategies(self, category: str):
        """筛选策略"""
        self._load_strategy_list(category)
    
    def _on_strategy_selected(self, item: QListWidgetItem):
        """策略选中事件"""
        strategy = item.data(Qt.ItemDataRole.UserRole)
        self.current_strategy = strategy
        self._display_strategy_detail(strategy)
    
    def _display_strategy_detail(self, strategy: dict):
        """显示策略详情"""
        # 清空现有内容
        while self.strategy_detail_layout.count():
            child = self.strategy_detail_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # 标题
        title = QLabel(f"📈 {strategy['name']}")
        title.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        self.strategy_detail_layout.addWidget(title)
        
        # 标签行
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(8)
        
        tags = [
            (strategy['category'], Colors.PRIMARY),
            (strategy['difficulty'], "#10B981"),
            (strategy['effectiveness'], "#F59E0B"),
        ]
        
        for tag_text, color in tags:
            tag = QLabel(tag_text)
            tag.setStyleSheet(f"""
                font-size: 12px;
                font-weight: 600;
                color: white;
                background-color: {color};
                padding: 4px 12px;
                border-radius: 12px;
            """)
            tags_layout.addWidget(tag)
        
        tags_layout.addStretch()
        self.strategy_detail_layout.addLayout(tags_layout)
        
        # 描述
        desc = QLabel(strategy['description'])
        desc.setStyleSheet(f"font-size: 14px; color: {Colors.TEXT_SECONDARY}; line-height: 1.6;")
        desc.setWordWrap(True)
        self.strategy_detail_layout.addWidget(desc)
        
        # 策略逻辑
        logic_frame = self._create_info_card("💡 策略逻辑", strategy['logic'])
        self.strategy_detail_layout.addWidget(logic_frame)
        
        # 核心因子
        factors_text = "、".join(strategy['factors'])
        factors_frame = self._create_info_card("📊 核心因子", factors_text)
        self.strategy_detail_layout.addWidget(factors_frame)
        
        # 预期表现
        perf_frame = QFrame()
        perf_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        perf_layout = QGridLayout(perf_frame)
        perf_layout.setContentsMargins(16, 16, 16, 16)
        perf_layout.setSpacing(12)
        
        perf_items = [
            ("📈 预期收益", strategy['expected_return']),
            ("📉 最大回撤", strategy['max_drawdown']),
            ("⚖️ 夏普比率", strategy['sharpe']),
            ("🔄 换手率", strategy['turnover']),
            ("💰 策略容量", strategy['capacity']),
            ("📅 回测周期", strategy['backtest_period']),
        ]
        
        for i, (label, value) in enumerate(perf_items):
            row, col = i // 2, i % 2
            
            label_widget = QLabel(label)
            label_widget.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED};")
            perf_layout.addWidget(label_widget, row * 2, col)
            
            value_widget = QLabel(value)
            value_widget.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            perf_layout.addWidget(value_widget, row * 2 + 1, col)
        
        self.strategy_detail_layout.addWidget(perf_frame)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        copy_btn = QPushButton("📋 复制代码")
        copy_btn.setStyleSheet(ButtonStyles.PRIMARY)
        copy_btn.clicked.connect(lambda: self._copy_strategy_code(strategy))
        btn_layout.addWidget(copy_btn)
        
        edit_btn = QPushButton("📝 编辑策略")
        edit_btn.setStyleSheet(ButtonStyles.SECONDARY)
        edit_btn.clicked.connect(lambda: self._edit_strategy(strategy))
        btn_layout.addWidget(edit_btn)
        
        cursor_btn = QPushButton("🚀 在Cursor中打开")
        cursor_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        cursor_btn.clicked.connect(lambda: self._open_in_cursor(strategy))
        btn_layout.addWidget(cursor_btn)
        
        btn_layout.addStretch()
        self.strategy_detail_layout.addLayout(btn_layout)
        
        # 参考链接
        ref_label = QLabel(f"📖 参考: {strategy['reference_link']}")
        ref_label.setStyleSheet(f"font-size: 12px; color: {Colors.PRIMARY}; margin-top: 8px;")
        self.strategy_detail_layout.addWidget(ref_label)
        
        self.strategy_detail_layout.addStretch()
    
    def _create_info_card(self, title: str, content: str) -> QFrame:
        """创建信息卡片"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.PRIMARY};")
        layout.addWidget(title_label)
        
        content_label = QLabel(content)
        content_label.setStyleSheet(f"font-size: 13px; color: {Colors.TEXT_SECONDARY};")
        content_label.setWordWrap(True)
        layout.addWidget(content_label)
        
        return frame
    
    def _copy_strategy_code(self, strategy: dict):
        """复制策略代码"""
        template_key = strategy.get('code_template', '')
        code = STRATEGY_TEMPLATES.get(template_key, "# 策略代码模板待完善")
        
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        
        QMessageBox.information(self, "复制成功", f"策略 '{strategy['name']}' 的代码已复制到剪贴板")
    
    def _edit_strategy(self, strategy: dict):
        """编辑策略"""
        template_key = strategy.get('code_template', '')
        code = STRATEGY_TEMPLATES.get(template_key, "# 策略代码模板待完善")
        
        # 切换到编辑器Tab
        self.tab_widget.setCurrentIndex(2)
        self.code_editor.setPlainText(code)
        self.current_code = code
    
    def _open_in_cursor(self, strategy: dict):
        """在Cursor中打开策略"""
        template_key = strategy.get('code_template', '')
        code = STRATEGY_TEMPLATES.get(template_key, "# 策略代码模板待完善")
        
        # 保存到临时文件
        strategies_dir = Path.home() / ".local/share/trquant/strategies/ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{strategy['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        filepath = strategies_dir / filename
        filepath.write_text(code, encoding='utf-8')
        
        # 尝试在Cursor中打开
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", "-a", "Cursor", str(filepath)])
            elif sys.platform == "win32":
                subprocess.run(["cursor", str(filepath)], shell=True)
            else:
                subprocess.run(["cursor", str(filepath)])
            
            QMessageBox.information(self, "已打开", f"策略文件已在Cursor中打开：\n{filepath}")
        except Exception as e:
            # 如果Cursor未安装，尝试用默认编辑器打开
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(filepath)))
            QMessageBox.information(self, "已保存", f"策略文件已保存：\n{filepath}\n\n请手动在Cursor中打开")
    
    # ============================================================
    # Tab 2: 策略生成器
    # ============================================================
    def _create_generator_tab(self) -> QWidget:
        """创建策略生成器选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("🔧 策略生成器")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        desc = QLabel("通过配置因子组合，自动生成PTrade/QMT策略代码")
        desc.setStyleSheet(f"font-size: 13px; color: {Colors.TEXT_MUTED};")
        layout.addWidget(desc)
        
        # 配置区域
        config_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：因子配置
        factor_frame = QFrame()
        factor_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        factor_layout = QVBoxLayout(factor_frame)
        factor_layout.setContentsMargins(16, 16, 16, 16)
        factor_layout.setSpacing(12)
        
        factor_title = QLabel("📊 因子选择")
        factor_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        factor_layout.addWidget(factor_title)
        
        # 因子列表
        self.factor_checkboxes = {}
        factors = [
            ("reversal_5d", "5日反转", "★★★★★"),
            ("roe", "ROE质量", "★★★★☆"),
            ("ep", "EP价值", "★★★☆☆"),
            ("momentum_12_1", "12-1月动量", "★★★☆☆"),
            ("volatility", "低波动", "★★★★☆"),
            ("dividend", "股息率", "★★★☆☆"),
            ("northbound", "北向资金", "★★★☆☆"),
        ]
        
        for factor_id, name, effectiveness in factors:
            cb = QCheckBox(f"{name} {effectiveness}")
            cb.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 13px;")
            factor_layout.addWidget(cb)
            self.factor_checkboxes[factor_id] = cb
        
        factor_layout.addStretch()
        config_splitter.addWidget(factor_frame)
        
        # 右侧：参数配置
        param_frame = QFrame()
        param_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        param_layout = QFormLayout(param_frame)
        param_layout.setContentsMargins(16, 16, 16, 16)
        param_layout.setSpacing(12)
        
        param_title = QLabel("⚙️ 策略参数")
        param_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        param_layout.addRow(param_title)
        
        # 策略名称
        self.gen_strategy_name = QLineEdit()
        self.gen_strategy_name.setPlaceholderText("my_strategy")
        self.gen_strategy_name.setStyleSheet(self._get_input_style())
        param_layout.addRow("策略名称:", self.gen_strategy_name)
        
        # 平台选择
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["PTrade", "QMT（开发中）", "QuantConnect（开发中）"])
        self.platform_combo.setStyleSheet(self._get_combo_style())
        param_layout.addRow("目标平台:", self.platform_combo)
        
        # 股票池
        self.stock_pool_combo = QComboBox()
        self.stock_pool_combo.addItems(["沪深300", "中证500", "中证1000", "全A股"])
        self.stock_pool_combo.setStyleSheet(self._get_combo_style())
        param_layout.addRow("股票池:", self.stock_pool_combo)
        
        # 持仓数量
        self.hold_num_spin = QSpinBox()
        self.hold_num_spin.setRange(10, 100)
        self.hold_num_spin.setValue(30)
        self.hold_num_spin.setStyleSheet(self._get_spin_style())
        param_layout.addRow("持仓数量:", self.hold_num_spin)
        
        # 调仓周期
        self.rebalance_combo = QComboBox()
        self.rebalance_combo.addItems(["每日", "每周", "每月", "每季度"])
        self.rebalance_combo.setCurrentIndex(2)
        self.rebalance_combo.setStyleSheet(self._get_combo_style())
        param_layout.addRow("调仓周期:", self.rebalance_combo)
        
        config_splitter.addWidget(param_frame)
        layout.addWidget(config_splitter)
        
        # 生成按钮
        btn_layout = QHBoxLayout()
        
        gen_btn = QPushButton("⚡ 生成策略代码")
        gen_btn.setStyleSheet(ButtonStyles.PRIMARY)
        gen_btn.setFixedHeight(44)
        gen_btn.clicked.connect(self._generate_strategy)
        btn_layout.addWidget(gen_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 代码预览区域
        preview_header = QHBoxLayout()
        preview_label = QLabel("📝 代码预览")
        preview_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        preview_header.addWidget(preview_label)
        
        preview_header.addStretch()
        
        # 复制和发送按钮
        copy_code_btn = QPushButton("📋 复制代码")
        copy_code_btn.setStyleSheet(self._get_toolbar_btn_style())
        copy_code_btn.clicked.connect(self._copy_generated_code)
        preview_header.addWidget(copy_code_btn)
        
        edit_code_btn = QPushButton("📝 编辑代码")
        edit_code_btn.setStyleSheet(self._get_toolbar_btn_style())
        edit_code_btn.clicked.connect(self._edit_generated_code)
        preview_header.addWidget(edit_code_btn)
        
        send_backtest_btn = QPushButton("📈 发送到回测")
        send_backtest_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY}CC;
            }}
        """)
        send_backtest_btn.clicked.connect(self._send_generated_to_backtest)
        preview_header.addWidget(send_backtest_btn)
        
        layout.addLayout(preview_header)
        
        self.gen_code_preview = QTextEdit()
        self.gen_code_preview.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1e1e1e;
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', 'Fira Code', monospace;
                font-size: 13px;
                line-height: 1.5;
            }}
        """)
        self.gen_code_preview.setPlaceholderText("配置因子后点击'生成策略代码'...")
        
        # 添加语法高亮
        self.gen_highlighter = PythonHighlighter(self.gen_code_preview.document())
        
        layout.addWidget(self.gen_code_preview)
        
        return widget
    
    def _copy_generated_code(self):
        """复制生成的代码"""
        code = self.gen_code_preview.toPlainText()
        if code.strip():
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(code)
            QMessageBox.information(self, "复制成功", "策略代码已复制到剪贴板")
        else:
            QMessageBox.warning(self, "提示", "请先生成策略代码")
    
    def _edit_generated_code(self):
        """将生成的代码发送到编辑器Tab"""
        code = self.gen_code_preview.toPlainText()
        if code.strip():
            self.code_editor.setPlainText(code)
            self.tab_widget.setCurrentIndex(3)  # 切换到策略编辑器Tab（索引3）
        else:
            QMessageBox.warning(self, "提示", "请先生成策略代码")
    
    def _send_generated_to_backtest(self):
        """将生成的代码发送到回测"""
        code = self.gen_code_preview.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "提示", "请先生成策略代码")
            return
        
        # 保存策略文件
        strategies_dir = Path.home() / ".local/share/trquant/strategies/ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"generated_strategy_{timestamp}.py"
        filepath = strategies_dir / filename
        filepath.write_text(code, encoding='utf-8')
        
        # 发送信号
        self.run_backtest.emit(str(filepath), {
            "code": code,
            "filepath": str(filepath),
            "filename": filename,
        })
        
        QMessageBox.information(self, "已发送", 
            f"策略已保存并发送到回测验证模块：\n{filepath}")
    
    def _generate_strategy(self):
        """生成策略代码"""
        # 获取选中的因子
        selected_factors = [fid for fid, cb in self.factor_checkboxes.items() if cb.isChecked()]
        
        if not selected_factors:
            QMessageBox.warning(self, "提示", "请至少选择一个因子")
            return
        
        # 获取参数
        strategy_name = self.gen_strategy_name.text() or "my_strategy"
        platform = self.platform_combo.currentText()
        stock_pool = self.stock_pool_combo.currentText()
        hold_num = self.hold_num_spin.value()
        rebalance = self.rebalance_combo.currentText()
        
        # 生成代码（简化版）
        code = self._generate_ptrade_code(strategy_name, selected_factors, stock_pool, hold_num, rebalance)
        
        self.gen_code_preview.setPlainText(code)
        self.current_code = code
    
    def _generate_ptrade_code(self, name, factors, stock_pool, hold_num, rebalance):
        """生成PTrade策略代码（增强注释版）"""
        pool_map = {
            "沪深300": "000300.XSHG",
            "中证500": "000905.XSHG",
            "中证1000": "000852.XSHG",
            "全A股": "全A",
        }
        
        rebalance_map = {
            "每日": "daily",
            "每周": "weekly",
            "每月": "monthly",
            "每季度": "quarterly",
        }
        
        # 因子名称映射
        factor_names = {
            "reversal_5d": "5日反转",
            "roe": "ROE质量",
            "ep": "EP价值",
            "momentum_12_1": "12-1月动量",
            "volatility": "低波动",
            "dividend": "股息率",
            "northbound": "北向资金",
        }
        
        factors_str = ", ".join([f"'{f}'" for f in factors])
        factors_desc = ", ".join([factor_names.get(f, f) for f in factors])
        
        code = f'''# -*- coding: utf-8 -*-
"""
================================================================================
{name} - PTrade多因子策略
================================================================================
【生成信息】
    生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    生成工具: 韬睿量化 - 策略生成器
    
【策略配置】
    因子组合: {factors_desc}
    股票池: {stock_pool}
    持仓数量: {hold_num} 只
    调仓频率: {rebalance}
    
【策略说明】
    本策略基于多因子模型，通过组合多个Alpha因子进行选股。
    策略会在每个调仓日计算所有股票的因子得分，选择得分最优的股票持有。
    
【风险提示】
    - 历史回测表现不代表未来收益
    - 请根据市场环境调整参数
    - 建议先在模拟盘验证后再实盘交易
================================================================================
"""

# =============================================================================
# 策略初始化
# =============================================================================
def initialize(context):
    """
    策略初始化函数 - 设置策略参数
    
    参数说明:
        context: PTrade策略上下文对象
    """
    # -------------------------------------------------------------------------
    # 核心参数配置
    # -------------------------------------------------------------------------
    g.stock_pool = '{pool_map.get(stock_pool, "000300.XSHG")}'  # 股票池指数代码
    g.hold_num = {hold_num}                                      # 目标持仓数量
    g.factors = [{factors_str}]                                  # 使用的因子列表
    g.rebalance = '{rebalance_map.get(rebalance, "monthly")}'   # 调仓频率
    
    # -------------------------------------------------------------------------
    # 打印策略配置
    # -------------------------------------------------------------------------
    log.info("=" * 60)
    log.info("【{name}】策略初始化完成")
    log.info(f"  股票池: {{g.stock_pool}}")
    log.info(f"  持仓数量: {{g.hold_num}} 只")
    log.info(f"  因子组合: {{g.factors}}")
    log.info(f"  调仓频率: {{g.rebalance}}")
    log.info("=" * 60)


# =============================================================================
# 盘前准备
# =============================================================================
def before_trading_start(context, data):
    """
    盘前准备函数 - 每个交易日开盘前执行
    
    功能:
        1. 获取最新的股票池成分股
        2. 设置可交易股票范围
    """
    # 获取股票池
    if g.stock_pool == '全A':
        # 全A股：获取所有上市股票
        g.stocks = list(get_all_securities(['stock']).index)
    else:
        # 指数成分股
        g.stocks = get_index_stocks(g.stock_pool)
    
    # 设置股票池（用于行情订阅）
    set_universe(g.stocks)
    
    log.info(f"[盘前] 股票池更新: {{len(g.stocks)}} 只")


# =============================================================================
# 盘中交易
# =============================================================================
def handle_data(context, data):
    """
    盘中交易函数 - 每个交易时间点执行
    
    核心逻辑:
        1. 判断是否为调仓日
        2. 计算多因子得分
        3. 选择得分最优的股票
        4. 执行调仓
    """
    # Step 1: 判断是否调仓日
    if not is_rebalance_day(context):
        return
    
    log.info(f"[调仓日] {{context.current_dt.strftime('%Y-%m-%d')}}")
    
    # Step 2: 计算因子得分
    scores = calculate_factor_scores(g.stocks, g.factors)
    
    if scores.empty:
        log.warning("[警告] 因子计算结果为空，跳过本次调仓")
        return
    
    # Step 3: 选股 - 选择得分最小（排名最靠前）的股票
    target_stocks = scores.nsmallest(g.hold_num, 'score')['code'].tolist()
    
    log.info(f"[选股] 目标持仓: {{len(target_stocks)}} 只")
    
    # Step 4: 执行调仓
    rebalance(context, target_stocks)


# =============================================================================
# 辅助函数：判断调仓日
# =============================================================================
def is_rebalance_day(context):
    """
    判断当前是否为调仓日
    
    返回:
        bool: True表示今天需要调仓
    """
    if g.rebalance == 'daily':
        return True
    elif g.rebalance == 'weekly':
        # 每周一调仓
        return context.current_dt.weekday() == 0
    elif g.rebalance == 'monthly':
        # 每月前5个交易日调仓
        return context.current_dt.day <= 5
    elif g.rebalance == 'quarterly':
        # 每季度初调仓（1月、4月、7月、10月）
        return context.current_dt.month in [1, 4, 7, 10] and context.current_dt.day <= 5
    return False


# =============================================================================
# 辅助函数：计算因子得分
# =============================================================================
def calculate_factor_scores(stocks, factors):
    """
    计算多因子综合得分
    
    参数:
        stocks: 股票列表
        factors: 因子列表
        
    返回:
        DataFrame: 包含股票代码和综合得分
    """
    import pandas as pd
    
    # 获取基本面数据
    df = get_fundamentals(
        query(valuation.code, valuation.pe_ratio, indicator.roe)
        .filter(valuation.code.in_(stocks))
    )
    
    if df.empty:
        return pd.DataFrame()
    
    # 计算综合得分（简化版）
    df['score'] = 0
    
    if 'ep' in factors:
        df['ep'] = 1 / df['pe_ratio'].replace(0, float('inf'))
        df['score'] += df['ep'].rank(ascending=False)
    
    if 'roe' in factors:
        df['score'] += df['roe'].rank(ascending=False)
    
    return df

def rebalance(context, target_stocks):
    """调仓函数"""
    # 卖出不在目标列表的股票
    for stock in context.portfolio.positions:
        if stock not in target_stocks:
            order_target(stock, 0)
    
    # 等权买入目标股票
    if len(target_stocks) > 0:
        weight = 1.0 / len(target_stocks)
        for stock in target_stocks:
            order_target_percent(stock, weight)
'''
        return code
    
    # ============================================================
    # Tab 3: 策略编辑器
    # ============================================================
    def _create_editor_tab(self) -> QWidget:
        """创建策略编辑器选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = QFrame()
        toolbar.setFixedHeight(56)
        toolbar.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border-bottom: 1px solid {Colors.BORDER_PRIMARY};
            }}
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 8, 16, 8)
        toolbar_layout.setSpacing(12)
        
        # 文件操作
        new_btn = QPushButton("📄 新建")
        new_btn.setStyleSheet(self._get_toolbar_btn_style())
        new_btn.clicked.connect(self._new_file)
        toolbar_layout.addWidget(new_btn)
        
        open_btn = QPushButton("📂 打开")
        open_btn.setStyleSheet(self._get_toolbar_btn_style())
        open_btn.clicked.connect(self._open_file)
        toolbar_layout.addWidget(open_btn)
        
        save_btn = QPushButton("💾 保存")
        save_btn.setStyleSheet(self._get_toolbar_btn_style())
        save_btn.clicked.connect(self._save_file)
        toolbar_layout.addWidget(save_btn)
        
        toolbar_layout.addWidget(self._create_separator())
        
        # Git操作
        git_status_btn = QPushButton("📊 Git状态")
        git_status_btn.setStyleSheet(self._get_toolbar_btn_style())
        git_status_btn.clicked.connect(self._git_status)
        toolbar_layout.addWidget(git_status_btn)
        
        git_commit_btn = QPushButton("✅ Git提交")
        git_commit_btn.setStyleSheet(self._get_toolbar_btn_style())
        git_commit_btn.clicked.connect(self._git_commit)
        toolbar_layout.addWidget(git_commit_btn)
        
        toolbar_layout.addWidget(self._create_separator())
        
        # Cursor集成
        cursor_btn = QPushButton("🚀 在Cursor中打开")
        cursor_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        cursor_btn.clicked.connect(self._open_current_in_cursor)
        toolbar_layout.addWidget(cursor_btn)
        
        toolbar_layout.addWidget(self._create_separator())
        
        # 发送到回测按钮
        backtest_btn = QPushButton("📈 发送到回测")
        backtest_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY}CC;
            }}
        """)
        backtest_btn.clicked.connect(self._send_to_backtest)
        toolbar_layout.addWidget(backtest_btn)
        
        toolbar_layout.addStretch()
        
        # 当前文件
        self.current_file_label = QLabel("未打开文件")
        self.current_file_label.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED};")
        toolbar_layout.addWidget(self.current_file_label)
        
        layout.addWidget(toolbar)
        
        # 代码编辑器
        self.code_editor = QTextEdit()
        self.code_editor.setStyleSheet(f"""
            QTextEdit {{
                background-color: #1e1e1e;
                border: none;
                padding: 16px;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', 'Fira Code', monospace;
                font-size: 14px;
                line-height: 1.5;
            }}
        """)
        self.code_editor.setPlaceholderText("# 在此编写策略代码...\n# 或从实战策略库复制模板")
        
        # 添加语法高亮
        self.highlighter = PythonHighlighter(self.code_editor.document())
        
        layout.addWidget(self.code_editor)
        
        return widget
    
    def _create_separator(self) -> QFrame:
        """创建分隔线"""
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background-color: {Colors.BORDER_PRIMARY};")
        return sep
    
    def _get_toolbar_btn_style(self) -> str:
        """工具栏按钮样式"""
        return f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.PRIMARY}80;
            }}
        """
    
    def _new_file(self):
        """新建文件"""
        self.code_editor.clear()
        self.current_file_label.setText("新建文件")
        self.current_file_path = None
    
    def _open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开策略文件", 
            str(Path.home() / ".local/share/trquant/strategies"),
            "Python Files (*.py)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.code_editor.setPlainText(f.read())
                self.current_file_path = file_path
                self.current_file_label.setText(Path(file_path).name)
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法打开文件：{e}")
    
    def _save_file(self):
        """保存文件"""
        if not hasattr(self, 'current_file_path') or not self.current_file_path:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存策略文件",
                str(Path.home() / ".local/share/trquant/strategies/ptrade/my_strategy.py"),
                "Python Files (*.py)"
            )
            if not file_path:
                return
            self.current_file_path = file_path
        
        try:
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.toPlainText())
            self.current_file_label.setText(Path(self.current_file_path).name)
            QMessageBox.information(self, "保存成功", f"文件已保存：{self.current_file_path}")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存失败：{e}")
    
    def _git_status(self):
        """查看Git状态"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=str(Path.home() / ".local/share/trquant"),
                capture_output=True,
                text=True
            )
            QMessageBox.information(self, "Git状态", result.stdout or result.stderr)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"Git命令执行失败：{e}")
    
    def _git_commit(self):
        """Git提交"""
        from PyQt6.QtWidgets import QInputDialog
        
        message, ok = QInputDialog.getText(self, "Git提交", "提交信息：")
        if ok and message:
            try:
                # 先添加文件
                subprocess.run(
                    ["git", "add", "."],
                    cwd=str(Path.home() / ".local/share/trquant"),
                    capture_output=True
                )
                # 提交
                result = subprocess.run(
                    ["git", "commit", "-m", message],
                    cwd=str(Path.home() / ".local/share/trquant"),
                    capture_output=True,
                    text=True
                )
                QMessageBox.information(self, "Git提交", result.stdout or result.stderr or "提交成功")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"Git提交失败：{e}")
    
    def _open_current_in_cursor(self):
        """在Cursor中打开当前文件"""
        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "提示", "请先编写或加载策略代码")
            return
        
        # 保存到临时文件
        strategies_dir = Path.home() / ".local/share/trquant/strategies/ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"temp_strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        filepath = strategies_dir / filename
        filepath.write_text(code, encoding='utf-8')
        
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", "-a", "Cursor", str(filepath)])
            elif sys.platform == "win32":
                subprocess.run(["cursor", str(filepath)], shell=True)
            else:
                subprocess.run(["cursor", str(filepath)])
            
            self.current_file_path = str(filepath)
            self.current_file_label.setText(filename)
        except Exception as e:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(filepath)))
            QMessageBox.information(self, "已保存", f"文件已保存：{filepath}")
    
    def _send_to_backtest(self):
        """发送当前策略到回测验证模块"""
        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "提示", "请先编写或加载策略代码")
            return
        
        # 保存策略文件
        strategies_dir = Path.home() / ".local/share/trquant/strategies/ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"strategy_{timestamp}.py"
        filepath = strategies_dir / filename
        filepath.write_text(code, encoding='utf-8')
        
        # 发送信号，通知主窗口切换到回测页面并加载策略
        self.run_backtest.emit(str(filepath), {
            "code": code,
            "filepath": str(filepath),
            "filename": filename,
        })
        
        QMessageBox.information(self, "已发送", 
            f"策略已保存并发送到回测验证模块：\n{filepath}\n\n"
            "正在跳转到回测验证页面...")
    
    # ============================================================
    # Tab 4: AI助手
    # ============================================================
    def _create_ai_guide_tab(self) -> QWidget:
        """创建AI策略助手Tab - 开发流程指南 + AI交互"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {Colors.BG_SECONDARY};
            }}
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(32, 24, 32, 24)
        content_layout.setSpacing(24)
        
        # =========================================================
        # Hero区域 - 标题和简介
        # =========================================================
        hero = QFrame()
        hero.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {Colors.PRIMARY}22, stop:0.5 #10B98122, stop:1 {Colors.BG_TERTIARY});
                border: 1px solid {Colors.PRIMARY}44;
                border-radius: 16px;
            }}
        """)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(28, 24, 28, 24)
        hero_layout.setSpacing(12)
        
        hero_title = QLabel("🤖 AI策略助手 ✨ 热重载测试中")
        hero_title.setStyleSheet(f"font-size: 28px; font-weight: 700; color: {Colors.PRIMARY};")
        hero_layout.addWidget(hero_title)
        
        hero_subtitle = QLabel("使用AI辅助开发量化交易策略，从想法到实盘的完整工作流 | 修改代码后点击侧栏'热重载'按钮即可生效")
        hero_subtitle.setStyleSheet(f"font-size: 15px; color: {Colors.TEXT_SECONDARY};")
        hero_layout.addWidget(hero_subtitle)
        
        content_layout.addWidget(hero)
        
        # =========================================================
        # 开发流程图
        # =========================================================
        flow_title = QLabel("📋 策略开发流程")
        flow_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(flow_title)
        
        flow_frame = QFrame()
        flow_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        flow_layout = QHBoxLayout(flow_frame)
        flow_layout.setContentsMargins(20, 20, 20, 20)
        flow_layout.setSpacing(8)
        
        flow_steps = [
            ("1️⃣", "需求分析", "明确策略目标\n风险偏好\n资金规模", Colors.INFO),
            ("2️⃣", "因子研究", "选择因子\n因子测试\n因子组合", Colors.SUCCESS),
            ("3️⃣", "策略编写", "AI生成代码\n代码优化\n逻辑检查", Colors.WARNING),
            ("4️⃣", "回测验证", "历史回测\n参数优化\n风险分析", Colors.PRIMARY),
            ("5️⃣", "模拟交易", "纸面交易\n实时监控\n问题修复", Colors.ACCENT),
            ("6️⃣", "实盘部署", "资金配置\n风控设置\n持续优化", Colors.ERROR),
        ]
        
        for i, (num, title, desc, color) in enumerate(flow_steps):
            step_card = QFrame()
            step_card.setFixedWidth(140)
            step_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 2px solid {color}40;
                    border-radius: 10px;
                }}
            """)
            step_layout = QVBoxLayout(step_card)
            step_layout.setContentsMargins(12, 12, 12, 12)
            step_layout.setSpacing(6)
            
            num_label = QLabel(num)
            num_label.setStyleSheet(f"font-size: 20px;")
            num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_layout.addWidget(num_label)
            
            title_label = QLabel(title)
            title_label.setStyleSheet(f"font-size: 13px; font-weight: 600; color: {color};")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_MUTED};")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            step_layout.addWidget(desc_label)
            
            flow_layout.addWidget(step_card)
            
            # 添加箭头（除了最后一个）
            if i < len(flow_steps) - 1:
                arrow = QLabel("→")
                arrow.setStyleSheet(f"font-size: 18px; color: {Colors.TEXT_MUTED};")
                flow_layout.addWidget(arrow)
        
        content_layout.addWidget(flow_frame)
        
        # =========================================================
        # 注意事项
        # =========================================================
        tips_title = QLabel("⚠️ 开发注意事项")
        tips_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(tips_title)
        
        tips_grid = QGridLayout()
        tips_grid.setSpacing(16)
        
        tips_data = [
            ("🎯", "明确目标", "先确定策略类型（趋势/反转/套利）、预期收益、可承受回撤，再开始编码。", Colors.PRIMARY),
            ("📊", "数据质量", "确保使用复权价格、处理停牌股票、注意财务数据发布时间（避免未来函数）。", Colors.SUCCESS),
            ("⚡", "执行成本", "考虑滑点、手续费、冲击成本。高换手策略需要更高的毛收益才能盈利。", Colors.WARNING),
            ("🛡️", "风险控制", "设置止损、仓位上限、行业分散。单只股票仓位建议不超过5%。", Colors.ERROR),
            ("🔄", "过拟合", "避免参数过度优化。使用样本外测试、滚动回测验证策略稳健性。", Colors.ACCENT),
            ("📈", "容量限制", "小市值策略容量有限。评估策略在不同资金规模下的表现。", Colors.INFO),
        ]
        
        for i, (icon, title, desc, color) in enumerate(tips_data):
            tip_card = QFrame()
            tip_card.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border-left: 4px solid {color};
                    border-radius: 8px;
                }}
            """)
            tip_layout = QVBoxLayout(tip_card)
            tip_layout.setContentsMargins(16, 12, 16, 12)
            tip_layout.setSpacing(4)
            
            tip_header = QLabel(f"{icon} {title}")
            tip_header.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            tip_layout.addWidget(tip_header)
            
            tip_desc = QLabel(desc)
            tip_desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
            tip_desc.setWordWrap(True)
            tip_layout.addWidget(tip_desc)
            
            tips_grid.addWidget(tip_card, i // 2, i % 2)
        
        content_layout.addLayout(tips_grid)
        
        # =========================================================
        # PTrade API 要点
        # =========================================================
        api_title = QLabel("📖 PTrade API 要点")
        api_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(api_title)
        
        api_frame = QFrame()
        api_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        api_layout = QVBoxLayout(api_frame)
        api_layout.setContentsMargins(20, 16, 20, 16)
        api_layout.setSpacing(12)
        
        api_items = [
            ("initialize(context)", "策略初始化，设置参数。只在策略启动时执行一次。"),
            ("before_trading_start(context, data)", "盘前准备，获取股票池。每个交易日开盘前执行。"),
            ("handle_data(context, data)", "盘中交易逻辑。根据设置的频率执行（分钟/日）。"),
            ("get_index_stocks(index)", "获取指数成分股。如 '000300.XSHG' 获取沪深300成分股。"),
            ("get_fundamentals(query)", "获取财务数据。注意：只能获取已发布的数据。"),
            ("order_target_percent(stock, pct)", "按目标百分比下单。pct=0.1 表示买入10%仓位。"),
            ("context.portfolio.positions", "当前持仓字典。key为股票代码，value为持仓信息。"),
        ]
        
        for func, desc in api_items:
            item_layout = QHBoxLayout()
            
            func_label = QLabel(func)
            func_label.setStyleSheet(f"""
                font-size: 12px; 
                font-family: 'Consolas', 'Monaco', monospace;
                color: {Colors.PRIMARY};
                background-color: {Colors.BG_SECONDARY};
                padding: 4px 8px;
                border-radius: 4px;
            """)
            func_label.setFixedWidth(280)
            item_layout.addWidget(func_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
            item_layout.addWidget(desc_label)
            
            api_layout.addLayout(item_layout)
        
        content_layout.addWidget(api_frame)
        
        # =========================================================
        # AI 交互区域
        # =========================================================
        ai_title = QLabel("💬 AI 策略生成")
        ai_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(ai_title)
        
        # Cursor推荐卡片
        cursor_card = QFrame()
        cursor_card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #10B98120, stop:1 #3B82F620);
                border: 1px solid #10B98140;
                border-radius: 12px;
            }}
        """)
        cursor_layout = QHBoxLayout(cursor_card)
        cursor_layout.setContentsMargins(20, 16, 20, 16)
        
        cursor_info = QVBoxLayout()
        cursor_title = QLabel("🚀 推荐：在Cursor中开发策略")
        cursor_title.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        cursor_info.addWidget(cursor_title)
        
        cursor_desc = QLabel(
            "Cursor内置Claude AI，可以：理解项目上下文 • 直接编辑调试代码 • 访问因子库模板 • 自动补全和错误修复"
        )
        cursor_desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
        cursor_info.addWidget(cursor_desc)
        
        cursor_layout.addLayout(cursor_info)
        cursor_layout.addStretch()
        
        open_cursor_btn = QPushButton("🚀 打开Cursor")
        open_cursor_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        open_cursor_btn.clicked.connect(self._open_project_in_cursor)
        cursor_layout.addWidget(open_cursor_btn)
        
        content_layout.addWidget(cursor_card)
        
        # 策略描述输入
        input_label = QLabel("📝 策略需求描述")
        input_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(input_label)
        
        self.ai_input = QTextEdit()
        self.ai_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 14px;
            }}
        """)
        self.ai_input.setPlaceholderText(
            "描述您想要的策略，例如：\n\n"
            "• 我想要一个基于短期反转的策略，每周调仓，持有30只股票，股票池为中证500\n"
            "• 请帮我创建一个ROE+EP的多因子策略，月度调仓，沪深300股票池，考虑行业中性\n"
            "• 我需要一个低波动+高股息的防御型策略，季度调仓，适合震荡市\n\n"
            "提示：描述越详细，生成的策略越符合预期。"
        )
        self.ai_input.setFixedHeight(120)
        content_layout.addWidget(self.ai_input)
        
        # 快速模板
        template_label = QLabel("📋 快速模板")
        template_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(template_label)
        
        templates_layout = QHBoxLayout()
        templates_layout.setSpacing(12)
        
        templates = [
            ("反转策略", "请帮我创建一个A股短期反转策略，使用5日收益率作为反转因子，每周调仓，中证500股票池，持有30只股票"),
            ("多因子策略", "请创建一个ROE+EP的多因子策略，月度调仓，沪深300股票池，持有30只股票，等权配置"),
            ("低波动策略", "请创建一个低波动防御策略，使用60日波动率因子，季度调仓，沪深300股票池"),
            ("指数增强", "请创建一个沪深300指数增强策略，使用反转+质量因子，月度调仓，控制行业偏离"),
        ]
        
        for name, prompt in templates:
            btn = QPushButton(name)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_PRIMARY};
                    color: {Colors.TEXT_PRIMARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-size: 13px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.BG_HOVER};
                    border-color: {Colors.PRIMARY};
                }}
            """)
            btn.clicked.connect(lambda checked, p=prompt: self.ai_input.setPlainText(p))
            templates_layout.addWidget(btn)
        
        templates_layout.addStretch()
        content_layout.addLayout(templates_layout)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        send_cursor_btn = QPushButton("🚀 发送到Cursor处理")
        send_cursor_btn.setStyleSheet(ButtonStyles.PRIMARY)
        send_cursor_btn.setFixedHeight(44)
        send_cursor_btn.clicked.connect(self._send_to_cursor)
        btn_layout.addWidget(send_cursor_btn)
        
        go_strategies_btn = QPushButton("📚 查看实战策略库")
        go_strategies_btn.setStyleSheet(ButtonStyles.SECONDARY)
        go_strategies_btn.setFixedHeight(44)
        go_strategies_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(1))
        btn_layout.addWidget(go_strategies_btn)
        
        go_generator_btn = QPushButton("🔧 使用策略生成器")
        go_generator_btn.setStyleSheet(ButtonStyles.SECONDARY)
        go_generator_btn.setFixedHeight(44)
        go_generator_btn.clicked.connect(lambda: self.tab_widget.setCurrentIndex(2))
        btn_layout.addWidget(go_generator_btn)
        
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)
        
        # =========================================================
        # 快速入口卡片
        # =========================================================
        quick_title = QLabel("🎯 快速入口")
        quick_title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        content_layout.addWidget(quick_title)
        
        quick_grid = QGridLayout()
        quick_grid.setSpacing(16)
        
        quick_items = [
            ("📚", "实战策略库", "10个经过验证的A股策略，可直接使用", 1, Colors.SUCCESS),
            ("🔧", "策略生成器", "选择因子组合，自动生成策略代码", 2, Colors.WARNING),
            ("📝", "策略编辑器", "编辑代码，Git管理，Cursor集成", 3, Colors.PRIMARY),
            ("📈", "回测验证", "发送策略到回测模块进行验证", -1, Colors.ACCENT),
        ]
        
        for i, (icon, title, desc, tab_idx, color) in enumerate(quick_items):
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 10px;
                }}
                QFrame:hover {{
                    border-color: {color};
                    background-color: {Colors.BG_HOVER};
                }}
            """)
            card.setCursor(Qt.CursorShape.PointingHandCursor)
            
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(16, 14, 16, 14)
            card_layout.setSpacing(8)
            
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(f"font-size: 28px;")
            card_layout.addWidget(icon_label)
            
            title_label = QLabel(title)
            title_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
            card_layout.addWidget(title_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED};")
            desc_label.setWordWrap(True)
            card_layout.addWidget(desc_label)
            
            # 添加点击事件
            if tab_idx >= 0:
                card.mousePressEvent = lambda e, idx=tab_idx: self.tab_widget.setCurrentIndex(idx)
            else:
                # 回测验证 - 发送信号切换到回测页面
                card.mousePressEvent = lambda e: self.run_backtest.emit("", {})
            
            quick_grid.addWidget(card, i // 2, i % 2)
        
        content_layout.addLayout(quick_grid)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return widget
    
    def _open_project_in_cursor(self):
        """在Cursor中打开项目"""
        project_path = Path.home() / ".local/share/trquant"
        
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", "-a", "Cursor", str(project_path)])
            elif sys.platform == "win32":
                subprocess.run(["cursor", str(project_path)], shell=True)
            else:
                subprocess.run(["cursor", str(project_path)])
        except Exception as e:
            QMessageBox.warning(self, "提示", f"无法打开Cursor，请确保已安装：{e}")
    
    def _send_to_cursor(self):
        """发送到Cursor处理"""
        prompt = self.ai_input.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "提示", "请先输入策略描述")
            return
        
        # 创建包含prompt的文件
        strategies_dir = Path.home() / ".local/share/trquant/strategies/ptrade"
        strategies_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"ai_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        filepath = strategies_dir / filename
        
        content = f'''# -*- coding: utf-8 -*-
"""
AI策略生成请求
==============
请求时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

用户需求:
{prompt}

请根据以上需求生成PTrade策略代码。

参考资料:
- 因子库位置: gui/widgets/factor_builder_panel.py
- 策略模板: gui/widgets/strategy_dev_panel.py
- PTrade API文档: docs/ptrade_api.md
"""

# TODO: 在此处生成策略代码

def initialize(context):
    """初始化"""
    pass

def handle_data(context, data):
    """盘中交易"""
    pass
'''
        
        filepath.write_text(content, encoding='utf-8')
        
        # 打开Cursor
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", "-a", "Cursor", str(filepath)])
            elif sys.platform == "win32":
                subprocess.run(["cursor", str(filepath)], shell=True)
            else:
                subprocess.run(["cursor", str(filepath)])
            
            QMessageBox.information(self, "已发送", 
                f"策略请求已保存并在Cursor中打开：\n{filepath}\n\n"
                "请在Cursor中使用AI助手完成策略开发")
        except Exception as e:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(filepath)))
            QMessageBox.information(self, "已保存", f"文件已保存：{filepath}")
    
    # ============================================================
    # Tab 5: 回测验证
    # ============================================================
    def _create_backtest_tab(self) -> QWidget:
        """创建回测验证选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("▶️ 回测验证")
        title.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        desc = QLabel("快速验证策略效果，或导入PTrade回测结果进行分析")
        desc.setStyleSheet(f"font-size: 13px; color: {Colors.TEXT_MUTED};")
        layout.addWidget(desc)
        
        # 回测配置
        config_frame = QFrame()
        config_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        config_layout = QFormLayout(config_frame)
        config_layout.setContentsMargins(16, 16, 16, 16)
        config_layout.setSpacing(12)
        
        # 策略文件
        file_layout = QHBoxLayout()
        self.backtest_file_input = QLineEdit()
        self.backtest_file_input.setPlaceholderText("选择策略文件...")
        self.backtest_file_input.setStyleSheet(self._get_input_style())
        file_layout.addWidget(self.backtest_file_input)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setStyleSheet(self._get_toolbar_btn_style())
        browse_btn.clicked.connect(self._browse_strategy_file)
        file_layout.addWidget(browse_btn)
        
        config_layout.addRow("策略文件:", file_layout)
        
        # 回测周期
        period_layout = QHBoxLayout()
        self.start_date = QLineEdit("2020-01-01")
        self.start_date.setStyleSheet(self._get_input_style())
        period_layout.addWidget(self.start_date)
        
        period_layout.addWidget(QLabel("至"))
        
        self.end_date = QLineEdit("2024-01-01")
        self.end_date.setStyleSheet(self._get_input_style())
        period_layout.addWidget(self.end_date)
        
        config_layout.addRow("回测周期:", period_layout)
        
        # 初始资金
        self.capital_input = QSpinBox()
        self.capital_input.setRange(100000, 100000000)
        self.capital_input.setValue(1000000)
        self.capital_input.setSingleStep(100000)
        self.capital_input.setStyleSheet(self._get_spin_style())
        config_layout.addRow("初始资金:", self.capital_input)
        
        layout.addWidget(config_frame)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        local_btn = QPushButton("🖥️ 本地回测（开发中）")
        local_btn.setStyleSheet(ButtonStyles.SECONDARY)
        local_btn.setEnabled(False)
        btn_layout.addWidget(local_btn)
        
        ptrade_btn = QPushButton("📤 发送到PTrade回测")
        ptrade_btn.setStyleSheet(ButtonStyles.PRIMARY)
        ptrade_btn.clicked.connect(self._send_to_ptrade)
        btn_layout.addWidget(ptrade_btn)
        
        import_btn = QPushButton("📥 导入PTrade结果")
        import_btn.setStyleSheet(ButtonStyles.SECONDARY)
        import_btn.clicked.connect(self._import_ptrade_result)
        btn_layout.addWidget(import_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 回测结果区域
        result_label = QLabel("📊 回测结果")
        result_label.setStyleSheet(f"font-size: 14px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(result_label)
        
        self.backtest_result = QTextEdit()
        self.backtest_result.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
        """)
        self.backtest_result.setPlaceholderText(
            "回测结果将显示在这里...\n\n"
            "支持的指标：\n"
            "• 策略收益率\n"
            "• 基准收益率\n"
            "• 超额收益（Alpha）\n"
            "• 最大回撤\n"
            "• 夏普比率\n"
            "• 胜率"
        )
        self.backtest_result.setReadOnly(True)
        layout.addWidget(self.backtest_result)
        
        return widget
    
    def _browse_strategy_file(self):
        """浏览策略文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择策略文件",
            str(Path.home() / ".local/share/trquant/strategies"),
            "Python Files (*.py)"
        )
        if file_path:
            self.backtest_file_input.setText(file_path)
    
    def _send_to_ptrade(self):
        """发送到PTrade回测"""
        file_path = self.backtest_file_input.text()
        if not file_path:
            QMessageBox.warning(self, "提示", "请先选择策略文件")
            return
        
        QMessageBox.information(self, "提示", 
            f"请在PTrade客户端中：\n\n"
            f"1. 打开策略文件：{file_path}\n"
            f"2. 设置回测参数\n"
            f"3. 运行回测\n"
            f"4. 导出回测结果\n\n"
            f"完成后使用'导入PTrade结果'功能分析结果")
    
    def _import_ptrade_result(self):
        """导入PTrade回测结果"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入PTrade回测结果",
            str(Path.home()),
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                
                # 解析并显示结果
                result_text = self._format_backtest_result(result)
                self.backtest_result.setPlainText(result_text)
                
            except Exception as e:
                QMessageBox.warning(self, "错误", f"无法解析回测结果：{e}")
    
    def _format_backtest_result(self, result: dict) -> str:
        """格式化回测结果"""
        # 预留接口，根据PTrade返回的格式解析
        text = "=" * 50 + "\n"
        text += "PTrade回测结果分析\n"
        text += "=" * 50 + "\n\n"
        
        # 尝试解析常见字段
        if isinstance(result, dict):
            for key, value in result.items():
                text += f"{key}: {value}\n"
        else:
            text += str(result)
        
        return text
    
    # ============================================================
    # 样式辅助方法
    # ============================================================
    def _get_input_style(self) -> str:
        return f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.PRIMARY};
            }}
        """
    
    def _get_combo_style(self) -> str:
        return f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
        """
    
    def _get_spin_style(self) -> str:
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                font-size: 13px;
            }}
        """

