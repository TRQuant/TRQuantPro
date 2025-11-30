# -*- coding: utf-8 -*-
"""
回测验证面板 - 专业数据可视化
回测执行与结果分析
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QComboBox, QDateEdit,
    QSpinBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QTabWidget, QTextEdit, QSplitter,
    QMessageBox, QLineEdit
)
from PyQt6.QtCore import Qt, QDate, QThread, pyqtSignal
from PyQt6.QtGui import QColor
from datetime import datetime, timedelta
from pathlib import Path
import logging

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles

logger = logging.getLogger(__name__)


class BacktestThread(QThread):
    """回测执行线程"""
    
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, strategy_name: str, params: dict, parent=None):
        super().__init__(parent)
        self.strategy_name = strategy_name
        self.params = params
    
    def run(self):
        try:
            self.progress.emit(10, "初始化回测引擎...")
            
            from main import run_backtest
            
            self.progress.emit(30, "加载数据...")
            
            # 获取默认股票池
            securities = self.params.get('securities', [])
            if not securities:
                # 使用默认股票池
                securities = self._get_default_securities()
            
            self.progress.emit(50, "执行回测...")
            
            result = run_backtest(
                strategy_name=self.strategy_name,
                start_date=self.params.get('start_date'),
                end_date=self.params.get('end_date'),
                securities=securities,
                initial_cash=self.params.get('initial_capital', 1000000),
                commission_rate=self.params.get('commission_rate', 0.0003),
                slippage=self.params.get('slippage', 0.001),
                strategy_params=self.params.get('strategy_params', {})
            )
            
            self.progress.emit(90, "生成报告...")
            
            if result is None:
                self.error.emit("回测失败，请检查数据源连接和日期范围")
                return
            
            # 转换结果格式以适配UI
            formatted_result = self._format_result(result)
            
            self.progress.emit(100, "回测完成")
            self.finished.emit(formatted_result)
            
        except Exception as e:
            logger.error(f"回测失败: {e}", exc_info=True)
            self.error.emit(str(e))
    
    def _get_default_securities(self) -> list:
        """获取默认股票池"""
        # 默认使用一些常见股票
        return [
            '600519.XSHG',  # 贵州茅台
            '000858.XSHE',  # 五粮液
            '601318.XSHG',  # 中国平安
            '000333.XSHE',  # 美的集团
            '600036.XSHG',  # 招商银行
        ]
    
    def _format_result(self, result: dict) -> dict:
        """格式化回测结果"""
        metrics = result.get('metrics', {})
        summary = result.get('summary', {})
        
        formatted = {
            'metrics': {
                'total_return': summary.get('total_profit_rate', 0),
                'annual_return': metrics.get('annual_return', 0),
                'sharpe_ratio': metrics.get('sharpe_ratio', 0),
                'max_drawdown': metrics.get('max_drawdown', 0),
                'win_rate': metrics.get('win_rate', 0),
                'total_trades': metrics.get('total_trades', 0),
                'profit_loss_ratio': metrics.get('profit_loss_ratio', 0),
                'volatility': metrics.get('volatility', 0),
                'benchmark_return': metrics.get('benchmark_return', 0),
            },
            'trades': [],
            'equity_curve': result.get('portfolio_history', {}),
            'summary': summary,
        }
        
        # 格式化交易记录
        for trade in result.get('trade_history', []):
            formatted['trades'].append({
                'date': trade.get('date', ''),
                'code': trade.get('code', ''),
                'direction': '买入' if trade.get('action') == 'buy' else '卖出',
                'price': trade.get('price', 0),
                'quantity': trade.get('quantity', 0),
                'amount': trade.get('price', 0) * trade.get('quantity', 0),
                'pnl': trade.get('pnl', 0),
            })
        
        return formatted


class MetricCard(QFrame):
    """指标卡片"""
    
    def __init__(self, title: str, value: str = "--", 
                 subtitle: str = "", color: str = None, parent=None):
        super().__init__(parent)
        
        color = color or Colors.TEXT_PRIMARY
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
            font-weight: 500;
        """)
        layout.addWidget(title_label)
        
        # 数值
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {color};
        """)
        layout.addWidget(self.value_label)
        
        # 副标题
        if subtitle:
            sub_label = QLabel(subtitle)
            sub_label.setStyleSheet(f"""
                font-size: 11px;
                color: {Colors.TEXT_MUTED};
            """)
            layout.addWidget(sub_label)
    
    def set_value(self, value: str, color: str = None):
        """设置数值"""
        self.value_label.setText(value)
        if color:
            self.value_label.setStyleSheet(f"""
                font-size: 28px;
                font-weight: 700;
                color: {color};
            """)


class BacktestPanel(QWidget):
    """回测验证面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backtest_thread = None
        self.current_result = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(24)
        
        # === 标题栏 ===
        header = self.create_header()
        layout.addLayout(header)
        
        # === 主分割器 ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Colors.BORDER_DARK};
                width: 1px;
            }}
        """)
        
        # === 左侧：配置面板 ===
        config_panel = self.create_config_panel()
        splitter.addWidget(config_panel)
        
        # === 右侧：结果面板 ===
        result_panel = self.create_result_panel()
        splitter.addWidget(result_panel)
        
        splitter.setSizes([320, 800])
        layout.addWidget(splitter)
    
    def create_header(self) -> QHBoxLayout:
        """创建标题栏"""
        header = QHBoxLayout()
        
        # 标题
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)
        
        title = QLabel("📊 回测验证")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("策略回测 · 风控检查 · 绩效分析")
        subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.TEXT_MUTED};
        """)
        title_layout.addWidget(subtitle)
        
        header.addWidget(title_widget)
        header.addStretch()
        
        return header
    
    def create_config_panel(self) -> QFrame:
        """创建配置面板"""
        panel = QFrame()
        panel.setStyleSheet(CardStyles.DEFAULT)
        panel.setFixedWidth(320)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # === 策略选择 ===
        strategy_label = QLabel("选择策略")
        strategy_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(strategy_label)
        
        self.strategy_combo = QComboBox()
        self.strategy_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        self.load_strategies()
        layout.addWidget(self.strategy_combo)
        
        # === 股票池选择 ===
        pool_label = QLabel("股票池")
        pool_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 8px;
        """)
        layout.addWidget(pool_label)
        
        self.pool_combo = QComboBox()
        self.pool_combo.addItems([
            "默认股票池 (5只)",
            "沪深300成分股",
            "中证500成分股",
            "自定义股票池",
        ])
        self.pool_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(self.pool_combo)
        
        # 自定义股票输入
        self.custom_stocks_input = QLineEdit()
        self.custom_stocks_input.setPlaceholderText("输入股票代码，用逗号分隔 (如: 600519,000858)")
        self.custom_stocks_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        self.custom_stocks_input.setVisible(False)
        self.pool_combo.currentIndexChanged.connect(self._on_pool_changed)
        layout.addWidget(self.custom_stocks_input)
        
        # === 回测区间 ===
        date_label = QLabel("回测区间")
        date_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 8px;
        """)
        layout.addWidget(date_label)
        
        date_layout = QHBoxLayout()
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-3))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet(f"""
            QDateEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        date_layout.addWidget(self.start_date)
        
        to_label = QLabel("至")
        to_label.setStyleSheet(f"color: {Colors.TEXT_MUTED};")
        to_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        date_layout.addWidget(to_label)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet(self.start_date.styleSheet())
        date_layout.addWidget(self.end_date)
        
        layout.addLayout(date_layout)
        
        # === 资金设置 ===
        capital_label = QLabel("初始资金")
        capital_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 8px;
        """)
        layout.addWidget(capital_label)
        
        self.capital_input = QSpinBox()
        self.capital_input.setRange(10000, 100000000)
        self.capital_input.setValue(1000000)
        self.capital_input.setSingleStep(100000)
        self.capital_input.setSuffix(" 元")
        self.capital_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(self.capital_input)
        
        # === 手续费 ===
        fee_label = QLabel("手续费率")
        fee_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
            margin-top: 8px;
        """)
        layout.addWidget(fee_label)
        
        self.fee_input = QDoubleSpinBox()
        self.fee_input.setRange(0, 0.01)
        self.fee_input.setValue(0.0003)
        self.fee_input.setSingleStep(0.0001)
        self.fee_input.setDecimals(4)
        self.fee_input.setStyleSheet(self.capital_input.styleSheet())
        layout.addWidget(self.fee_input)
        
        layout.addStretch()
        
        # === 进度条 ===
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {Colors.BG_SECONDARY};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.PRIMARY}, stop:1 {Colors.ACCENT});
                border-radius: 2px;
            }}
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
        """)
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.hide()
        layout.addWidget(self.progress_label)
        
        # === 运行按钮 ===
        self.run_btn = QPushButton("▶️ 开始回测")
        self.run_btn.setStyleSheet(ButtonStyles.PRIMARY)
        self.run_btn.setFixedHeight(48)
        self.run_btn.clicked.connect(self.run_backtest)
        layout.addWidget(self.run_btn)
        
        return panel
    
    def create_result_panel(self) -> QFrame:
        """创建结果面板"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 0, 0, 0)
        layout.setSpacing(24)
        
        # === 指标卡片 ===
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(16)
        
        self.metric_cards = {}
        
        metrics = [
            ("total_return", "总收益率", "--", Colors.TEXT_PRIMARY),
            ("annual_return", "年化收益", "--", Colors.TEXT_PRIMARY),
            ("sharpe_ratio", "夏普比率", "--", Colors.TEXT_PRIMARY),
            ("max_drawdown", "最大回撤", "--", Colors.ERROR),
            ("win_rate", "胜率", "--", Colors.SUCCESS),
        ]
        
        for key, title, value, color in metrics:
            card = MetricCard(title, value, color=color)
            self.metric_cards[key] = card
            metrics_layout.addWidget(card)
        
        layout.addLayout(metrics_layout)
        
        # === 标签页 ===
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
                margin-top: -1px;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {Colors.TEXT_MUTED};
                padding: 12px 24px;
                border: none;
                border-bottom: 2px solid transparent;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                color: {Colors.PRIMARY};
                border-bottom-color: {Colors.PRIMARY};
            }}
        """)
        
        # 收益曲线
        curve_tab = self.create_curve_tab()
        tabs.addTab(curve_tab, "📈 收益曲线")
        
        # 交易记录
        trades_tab = self.create_trades_tab()
        tabs.addTab(trades_tab, "📋 交易记录")
        
        # 风控报告
        risk_tab = self.create_risk_tab()
        tabs.addTab(risk_tab, "🛡️ 风控报告")
        
        # 详细报告
        report_tab = self.create_report_tab()
        tabs.addTab(report_tab, "📊 详细报告")
        
        layout.addWidget(tabs)
        
        return panel
    
    def create_curve_tab(self) -> QWidget:
        """创建收益曲线标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 图表占位
        self.chart_placeholder = QLabel("运行回测后显示收益曲线")
        self.chart_placeholder.setStyleSheet(f"""
            background-color: {Colors.BG_SECONDARY};
            color: {Colors.TEXT_MUTED};
            border: 1px dashed {Colors.BORDER_PRIMARY};
            border-radius: 8px;
            font-size: 14px;
        """)
        self.chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.chart_placeholder.setMinimumHeight(400)
        layout.addWidget(self.chart_placeholder)
        
        return tab
    
    def create_trades_tab(self) -> QWidget:
        """创建交易记录标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.trades_table = QTableWidget()
        self.trades_table.setColumnCount(7)
        self.trades_table.setHorizontalHeaderLabels([
            "日期", "股票代码", "方向", "价格", "数量", "金额", "盈亏"
        ])
        self.trades_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trades_table.verticalHeader().setVisible(False)
        self.trades_table.setAlternatingRowColors(True)
        self.trades_table.setStyleSheet(f"""
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
            }}
        """)
        layout.addWidget(self.trades_table)
        
        return tab
    
    def create_risk_tab(self) -> QWidget:
        """创建风控报告标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 风控检查项
        self.risk_checks = QWidget()
        risk_layout = QVBoxLayout(self.risk_checks)
        risk_layout.setSpacing(12)
        
        checks = [
            ("夏普比率 >= 0.5", "pending"),
            ("最大回撤 <= 30%", "pending"),
            ("胜率 >= 40%", "pending"),
            ("盈亏比 >= 1.0", "pending"),
            ("交易次数 >= 10", "pending"),
        ]
        
        for name, status in checks:
            item = self._create_check_item(name, status)
            risk_layout.addWidget(item)
        
        layout.addWidget(self.risk_checks)
        layout.addStretch()
        
        return tab
    
    def _create_check_item(self, name: str, status: str) -> QFrame:
        """创建检查项"""
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(item)
        layout.setContentsMargins(16, 12, 16, 12)
        
        # 状态图标
        icons = {
            "pass": ("✅", Colors.SUCCESS),
            "fail": ("❌", Colors.ERROR),
            "warning": ("⚠️", Colors.WARNING),
            "pending": ("⏳", Colors.TEXT_MUTED),
        }
        icon, color = icons.get(status, ("⏳", Colors.TEXT_MUTED))
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(icon_label)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.TEXT_SECONDARY};
        """)
        layout.addWidget(name_label)
        layout.addStretch()
        
        return item
    
    def create_report_tab(self) -> QWidget:
        """创建详细报告标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        
        view_btn = QPushButton("🌐 在浏览器中查看")
        view_btn.setStyleSheet(ButtonStyles.SECONDARY)
        view_btn.clicked.connect(self.view_report)
        btn_layout.addWidget(view_btn)
        
        export_btn = QPushButton("📥 导出报告")
        export_btn.setStyleSheet(ButtonStyles.SECONDARY)
        export_btn.clicked.connect(self.export_report)
        btn_layout.addWidget(export_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 报告预览
        self.report_preview = QTextEdit()
        self.report_preview.setReadOnly(True)
        self.report_preview.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 16px;
                font-family: {Typography.FONT_MONO};
            }}
        """)
        self.report_preview.setPlaceholderText("运行回测后显示详细报告...")
        layout.addWidget(self.report_preview)
        
        return tab
    
    def load_strategies(self):
        """加载策略列表"""
        self.strategy_combo.clear()
        
        # 添加已注册的策略
        registered_strategies = [
            ("ma_cross", "MA均线交叉策略"),
            ("adaptive_momentum", "自适应动量策略"),
            ("adaptive_momentum_a", "自适应动量策略A"),
            ("adaptive_momentum_a_v2", "自适应动量策略A V2"),
        ]
        
        for strategy_id, strategy_name in registered_strategies:
            self.strategy_combo.addItem(strategy_name, strategy_id)
    
    def _on_pool_changed(self, index: int):
        """股票池选择变化"""
        self.custom_stocks_input.setVisible(index == 3)  # 自定义股票池
    
    def _get_securities(self) -> list:
        """获取选中的股票池"""
        pool_index = self.pool_combo.currentIndex()
        
        if pool_index == 0:  # 默认股票池
            return [
                '600519.XSHG',  # 贵州茅台
                '000858.XSHE',  # 五粮液
                '601318.XSHG',  # 中国平安
                '000333.XSHE',  # 美的集团
                '600036.XSHG',  # 招商银行
            ]
        elif pool_index == 1:  # 沪深300
            # 返回部分沪深300成分股
            return [
                '600519.XSHG', '000858.XSHE', '601318.XSHG', 
                '000333.XSHE', '600036.XSHG', '601166.XSHG',
                '000651.XSHE', '600276.XSHG', '601888.XSHG',
                '000001.XSHE',
            ]
        elif pool_index == 2:  # 中证500
            return [
                '002415.XSHE', '300750.XSHE', '002230.XSHE',
                '300059.XSHE', '002241.XSHE', '300274.XSHE',
                '002714.XSHE', '300433.XSHE', '002049.XSHE',
                '300124.XSHE',
            ]
        elif pool_index == 3:  # 自定义
            custom_text = self.custom_stocks_input.text().strip()
            if not custom_text:
                return []
            
            # 解析自定义股票代码
            codes = [c.strip() for c in custom_text.split(',') if c.strip()]
            securities = []
            for code in codes:
                # 自动补全后缀
                if code.startswith('6'):
                    securities.append(f"{code}.XSHG")
                elif code.startswith('0') or code.startswith('3'):
                    securities.append(f"{code}.XSHE")
                else:
                    securities.append(code)
            return securities
        
        return []
    
    def run_backtest(self):
        """运行回测"""
        # 获取策略ID
        strategy_id = self.strategy_combo.currentData()
        if not strategy_id:
            QMessageBox.warning(self, "提示", "请选择策略")
            return
        
        # 获取股票池
        securities = self._get_securities()
        if not securities:
            QMessageBox.warning(self, "提示", "请选择或输入股票池")
            return
        
        # 显示进度
        self.progress_bar.show()
        self.progress_label.show()
        self.run_btn.setEnabled(False)
        
        params = {
            'start_date': self.start_date.date().toString("yyyy-MM-dd"),
            'end_date': self.end_date.date().toString("yyyy-MM-dd"),
            'initial_capital': self.capital_input.value(),
            'commission_rate': self.fee_input.value(),
            'securities': securities,
            'slippage': 0.001,
            'strategy_params': {},
        }
        
        # 启动回测线程
        self.backtest_thread = BacktestThread(strategy_id, params)
        self.backtest_thread.progress.connect(self.on_progress)
        self.backtest_thread.finished.connect(self.on_backtest_finished)
        self.backtest_thread.error.connect(self.on_backtest_error)
        self.backtest_thread.start()
    
    def on_progress(self, value: int, message: str):
        """进度更新"""
        self.progress_bar.setValue(value)
        self.progress_label.setText(message)
    
    def on_backtest_finished(self, result: dict):
        """回测完成"""
        self.progress_bar.hide()
        self.progress_label.hide()
        self.run_btn.setEnabled(True)
        
        self.current_result = result
        self.update_results(result)
        
        QMessageBox.information(self, "成功", "回测完成！")
    
    def on_backtest_error(self, error: str):
        """回测错误"""
        self.progress_bar.hide()
        self.progress_label.hide()
        self.run_btn.setEnabled(True)
        
        QMessageBox.warning(self, "错误", f"回测失败: {error}")
    
    def update_results(self, result: dict):
        """更新结果显示"""
        metrics = result.get('metrics', {})
        
        # 更新指标卡片
        if 'total_return' in self.metric_cards:
            total_return = metrics.get('total_return', 0) * 100
            color = Colors.SUCCESS if total_return > 0 else Colors.ERROR
            self.metric_cards['total_return'].set_value(f"{total_return:.2f}%", color)
        
        if 'annual_return' in self.metric_cards:
            annual = metrics.get('annual_return', 0) * 100
            color = Colors.SUCCESS if annual > 0 else Colors.ERROR
            self.metric_cards['annual_return'].set_value(f"{annual:.2f}%", color)
        
        if 'sharpe_ratio' in self.metric_cards:
            sharpe = metrics.get('sharpe_ratio', 0)
            color = Colors.SUCCESS if sharpe > 1 else Colors.WARNING if sharpe > 0 else Colors.ERROR
            self.metric_cards['sharpe_ratio'].set_value(f"{sharpe:.2f}", color)
        
        if 'max_drawdown' in self.metric_cards:
            mdd = abs(metrics.get('max_drawdown', 0)) * 100
            color = Colors.SUCCESS if mdd < 10 else Colors.WARNING if mdd < 20 else Colors.ERROR
            self.metric_cards['max_drawdown'].set_value(f"{mdd:.2f}%", color)
        
        if 'win_rate' in self.metric_cards:
            wr = metrics.get('win_rate', 0) * 100
            color = Colors.SUCCESS if wr > 50 else Colors.WARNING if wr > 40 else Colors.ERROR
            self.metric_cards['win_rate'].set_value(f"{wr:.1f}%", color)
        
        # 更新交易记录
        trades = result.get('trades', [])
        self.update_trades_table(trades)
        
        # 更新报告预览
        self.update_report_preview(result)
    
    def update_trades_table(self, trades: list):
        """更新交易记录表格"""
        self.trades_table.setRowCount(0)
        
        for trade in trades[-50:]:  # 只显示最近50条
            row = self.trades_table.rowCount()
            self.trades_table.insertRow(row)
            
            self.trades_table.setItem(row, 0, QTableWidgetItem(str(trade.get('date', ''))))
            self.trades_table.setItem(row, 1, QTableWidgetItem(trade.get('code', '')))
            self.trades_table.setItem(row, 2, QTableWidgetItem(trade.get('direction', '')))
            self.trades_table.setItem(row, 3, QTableWidgetItem(f"¥{trade.get('price', 0):.2f}"))
            self.trades_table.setItem(row, 4, QTableWidgetItem(str(trade.get('quantity', 0))))
            self.trades_table.setItem(row, 5, QTableWidgetItem(f"¥{trade.get('amount', 0):.2f}"))
            
            pnl = trade.get('pnl', 0)
            pnl_item = QTableWidgetItem(f"{'+'if pnl>0 else ''}¥{pnl:.2f}")
            pnl_item.setForeground(QColor(Colors.SUCCESS if pnl > 0 else Colors.ERROR))
            self.trades_table.setItem(row, 6, pnl_item)
    
    def update_report_preview(self, result: dict):
        """更新报告预览"""
        metrics = result.get('metrics', {})
        
        report = f"""
═══════════════════════════════════════════════════
                    回测报告摘要
═══════════════════════════════════════════════════

【基本信息】
策略名称: {self.strategy_combo.currentText()}
回测区间: {self.start_date.date().toString("yyyy-MM-dd")} ~ {self.end_date.date().toString("yyyy-MM-dd")}
初始资金: ¥{self.capital_input.value():,}

【收益指标】
总收益率: {metrics.get('total_return', 0)*100:.2f}%
年化收益: {metrics.get('annual_return', 0)*100:.2f}%
基准收益: {metrics.get('benchmark_return', 0)*100:.2f}%

【风险指标】
最大回撤: {abs(metrics.get('max_drawdown', 0))*100:.2f}%
夏普比率: {metrics.get('sharpe_ratio', 0):.2f}
波动率: {metrics.get('volatility', 0)*100:.2f}%

【交易统计】
总交易次数: {metrics.get('total_trades', 0)}
胜率: {metrics.get('win_rate', 0)*100:.1f}%
盈亏比: {metrics.get('profit_loss_ratio', 0):.2f}

═══════════════════════════════════════════════════
"""
        self.report_preview.setPlainText(report)
    
    def view_report(self):
        """在浏览器中查看报告"""
        if not self.current_result:
            QMessageBox.warning(self, "提示", "请先运行回测")
            return
        
        # 查找最新报告
        results_dir = Path(__file__).parent.parent.parent / "results"
        reports = list(results_dir.glob("*.html"))
        if reports:
            latest = max(reports, key=lambda p: p.stat().st_mtime)
            import webbrowser
            webbrowser.open(f"file://{latest}")
        else:
            QMessageBox.warning(self, "提示", "未找到报告文件")
    
    def export_report(self):
        """导出报告"""
        if not self.current_result:
            QMessageBox.warning(self, "提示", "请先运行回测")
            return
        
        QMessageBox.information(self, "提示", "报告已保存到 results 目录")
