# -*- coding: utf-8 -*-
"""
实盘交易面板 - 专业交易界面
支持QMT和PTrade券商直连
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QComboBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
    QSpinBox, QDoubleSpinBox, QMessageBox, QTabWidget, QTextEdit,
    QDialog, QFormLayout, QDialogButtonBox, QSplitter
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QColor, QFont
from datetime import datetime
from pathlib import Path
import logging

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles

logger = logging.getLogger(__name__)


class BrokerConnectThread(QThread):
    """券商连接线程"""
    
    finished = pyqtSignal(bool, str)
    
    def __init__(self, broker_type: str, config: dict, parent=None):
        super().__init__(parent)
        self.broker_type = broker_type
        self.config = config
        self.broker = None
    
    def run(self):
        try:
            from core.broker import BrokerFactory, BrokerType
            
            if self.broker_type == "QMT":
                self.broker = BrokerFactory.create(BrokerType.QMT, "QMT_Main")
                if self.broker:
                    success = self.broker.connect(
                        path=self.config.get('path', ''),
                        account_id=self.config.get('account_id', ''),
                        session_id=self.config.get('session_id', 0)
                    )
                    if success:
                        self.finished.emit(True, "QMT连接成功")
                    else:
                        self.finished.emit(False, "QMT连接失败，请检查配置")
                        
            elif self.broker_type == "PTrade":
                self.broker = BrokerFactory.create(BrokerType.PTRADE, "PTrade_Main")
                if self.broker:
                    success = self.broker.connect(
                        host=self.config.get('host', ''),
                        port=self.config.get('port', 8888),
                        account_id=self.config.get('account_id', ''),
                        password=self.config.get('password', '')
                    )
                    if success:
                        self.finished.emit(True, "PTrade连接成功")
                    else:
                        self.finished.emit(False, "PTrade连接失败，请检查配置")
                        
            elif self.broker_type == "Simulation":
                self.broker = BrokerFactory.create(BrokerType.SIMULATION, "Simulation")
                if self.broker:
                    self.broker.connect(
                        initial_cash=self.config.get('initial_cash', 1000000),
                        commission_rate=self.config.get('commission_rate', 0.0003)
                    )
                    self.finished.emit(True, "模拟交易已启动")
            else:
                self.finished.emit(False, f"不支持的券商类型: {self.broker_type}")
                
        except ImportError as e:
            if "xtquant" in str(e):
                self.finished.emit(False, 
                    "xtquant库未安装\n\n"
                    "请从迅投官网下载:\n"
                    "https://dict.thinktrader.net/nativeApi/download_xtquant.html\n\n"
                    "注意: 券商版QMT支持的最高版本为xtquant_241014"
                )
            else:
                self.finished.emit(False, f"导入错误: {e}")
        except Exception as e:
            self.finished.emit(False, f"连接异常: {e}")


class BrokerConfigDialog(QDialog):
    """券商配置对话框"""
    
    def __init__(self, broker_type: str, parent=None):
        super().__init__(parent)
        self.broker_type = broker_type
        self.setWindowTitle(f"配置 {broker_type}")
        self.setMinimumWidth(450)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # 标题
        title = QLabel(f"配置 {self.broker_type}")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(title)
        
        form = QFormLayout()
        form.setSpacing(16)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        
        input_style = f"""
            QLineEdit, QSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                color: {Colors.TEXT_SECONDARY};
            }}
            QLineEdit:focus, QSpinBox:focus {{
                border-color: {Colors.PRIMARY};
            }}
        """
        
        label_style = f"color: {Colors.TEXT_SECONDARY}; font-weight: 500;"
        
        if self.broker_type == "QMT":
            self.path_input = QLineEdit()
            self.path_input.setPlaceholderText("如: C:/国金证券QMT/userdata_mini")
            self.path_input.setStyleSheet(input_style)
            
            path_label = QLabel("miniQMT路径")
            path_label.setStyleSheet(label_style)
            form.addRow(path_label, self.path_input)
            
            self.account_input = QLineEdit()
            self.account_input.setPlaceholderText("资金账号")
            self.account_input.setStyleSheet(input_style)
            
            account_label = QLabel("资金账号")
            account_label.setStyleSheet(label_style)
            form.addRow(account_label, self.account_input)
            
            # SDK提示
            tip = QLabel(f"""
                <p style="color: {Colors.WARNING}; font-size: 12px; line-height: 1.5;">
                <b>SDK获取:</b> https://dict.thinktrader.net/nativeApi/download_xtquant.html<br>
                <b>注意:</b> 券商版QMT支持的最高版本为xtquant_241014
                </p>
            """)
            tip.setTextFormat(Qt.TextFormat.RichText)
            tip.setWordWrap(True)
            layout.addWidget(tip)
            
        elif self.broker_type == "PTrade":
            self.host_input = QLineEdit()
            self.host_input.setPlaceholderText("如: 192.168.1.100")
            self.host_input.setStyleSheet(input_style)
            
            host_label = QLabel("服务器地址")
            host_label.setStyleSheet(label_style)
            form.addRow(host_label, self.host_input)
            
            self.port_input = QSpinBox()
            self.port_input.setRange(1, 65535)
            self.port_input.setValue(8888)
            self.port_input.setStyleSheet(input_style)
            
            port_label = QLabel("端口")
            port_label.setStyleSheet(label_style)
            form.addRow(port_label, self.port_input)
            
            self.account_input = QLineEdit()
            self.account_input.setStyleSheet(input_style)
            
            account_label = QLabel("资金账号")
            account_label.setStyleSheet(label_style)
            form.addRow(account_label, self.account_input)
            
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_input.setStyleSheet(input_style)
            
            pwd_label = QLabel("密码")
            pwd_label.setStyleSheet(label_style)
            form.addRow(pwd_label, self.password_input)
            
            # API文档提示
            tip = QLabel(f"""
                <p style="color: {Colors.WARNING}; font-size: 12px; line-height: 1.5;">
                <b>接口文档:</b> http://180.169.107.9:7766/hub/help/api<br>
                <b>Python版本:</b> 3.11
                </p>
            """)
            tip.setTextFormat(Qt.TextFormat.RichText)
            tip.setWordWrap(True)
            layout.addWidget(tip)
            
        else:  # Simulation
            self.cash_input = QSpinBox()
            self.cash_input.setRange(10000, 100000000)
            self.cash_input.setValue(1000000)
            self.cash_input.setSingleStep(100000)
            self.cash_input.setSuffix(" 元")
            self.cash_input.setStyleSheet(input_style)
            
            cash_label = QLabel("初始资金")
            cash_label.setStyleSheet(label_style)
            form.addRow(cash_label, self.cash_input)
        
        layout.addLayout(form)
        layout.addStretch()
        
        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        cancel_btn = QPushButton("取消")
        cancel_btn.setStyleSheet(ButtonStyles.SECONDARY)
        cancel_btn.setFixedSize(100, 44)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        confirm_btn = QPushButton("连接")
        confirm_btn.setStyleSheet(ButtonStyles.PRIMARY)
        confirm_btn.setFixedSize(100, 44)
        confirm_btn.clicked.connect(self.accept)
        btn_layout.addWidget(confirm_btn)
        
        layout.addLayout(btn_layout)
    
    def get_config(self) -> dict:
        """获取配置"""
        if self.broker_type == "QMT":
            return {
                'path': self.path_input.text(),
                'account_id': self.account_input.text(),
                'session_id': 0,
            }
        elif self.broker_type == "PTrade":
            return {
                'host': self.host_input.text(),
                'port': self.port_input.value(),
                'account_id': self.account_input.text(),
                'password': self.password_input.text(),
            }
        else:
            return {
                'initial_cash': self.cash_input.value(),
                'commission_rate': 0.0003,
            }


class AccountCard(QFrame):
    """账户卡片"""
    
    def __init__(self, name: str, icon: str, parent=None):
        super().__init__(parent)
        self.name = name
        self._status = "offline"
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 12px;
            }}
        """)
        self.setFixedHeight(140)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 顶部
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        top_layout.addWidget(icon_label)
        
        name_label = QLabel(name)
        name_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        top_layout.addWidget(name_label)
        top_layout.addStretch()
        
        self.status_badge = QLabel("● 未连接")
        self.status_badge.setStyleSheet(f"""
            font-size: 12px;
            color: {Colors.TEXT_MUTED};
        """)
        top_layout.addWidget(self.status_badge)
        
        layout.addLayout(top_layout)
        
        # 资金信息
        info_layout = QHBoxLayout()
        
        # 可用资金
        cash_widget = QWidget()
        cash_layout = QVBoxLayout(cash_widget)
        cash_layout.setContentsMargins(0, 0, 0, 0)
        cash_layout.setSpacing(2)
        
        cash_label = QLabel("可用资金")
        cash_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_MUTED};")
        cash_layout.addWidget(cash_label)
        
        self.cash_value = QLabel("--")
        self.cash_value.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        cash_layout.addWidget(self.cash_value)
        
        info_layout.addWidget(cash_widget)
        
        # 今日盈亏
        pnl_widget = QWidget()
        pnl_layout = QVBoxLayout(pnl_widget)
        pnl_layout.setContentsMargins(0, 0, 0, 0)
        pnl_layout.setSpacing(2)
        
        pnl_label = QLabel("今日盈亏")
        pnl_label.setStyleSheet(f"font-size: 11px; color: {Colors.TEXT_MUTED};")
        pnl_layout.addWidget(pnl_label)
        
        self.pnl_value = QLabel("--")
        self.pnl_value.setStyleSheet(f"""
            font-size: 18px;
            font-weight: 700;
            color: {Colors.TEXT_MUTED};
        """)
        pnl_layout.addWidget(self.pnl_value)
        
        info_layout.addWidget(pnl_widget)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
    
    def set_status(self, status: str, cash: float = 0, pnl: float = 0):
        """设置状态"""
        self._status = status
        
        if status == "online":
            self.status_badge.setText("● 已连接")
            self.status_badge.setStyleSheet(f"font-size: 12px; color: {Colors.SUCCESS};")
            self.cash_value.setText(f"¥{cash:,.2f}")
            
            pnl_color = Colors.SUCCESS if pnl >= 0 else Colors.ERROR
            self.pnl_value.setText(f"{'+'if pnl>=0 else ''}¥{pnl:,.2f}")
            self.pnl_value.setStyleSheet(f"""
                font-size: 18px;
                font-weight: 700;
                color: {pnl_color};
            """)
        elif status == "connecting":
            self.status_badge.setText("● 连接中...")
            self.status_badge.setStyleSheet(f"font-size: 12px; color: {Colors.WARNING};")
        else:
            self.status_badge.setText("● 未连接")
            self.status_badge.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_MUTED};")
            self.cash_value.setText("--")
            self.pnl_value.setText("--")


class TradingPanel(QWidget):
    """实盘交易面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_broker = None
        self.connect_thread = None
        self.init_ui()
        
        # 定时刷新
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
    
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
        
        # === 左侧：账户与下单 ===
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # === 右侧：持仓与委托 ===
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 700])
        layout.addWidget(splitter)
    
    def create_header(self) -> QHBoxLayout:
        """创建标题栏"""
        header = QHBoxLayout()
        
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)
        
        title = QLabel("🚀 实盘交易")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        subtitle = QLabel("券商直连 · 风险控制 · 实时监控")
        subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.TEXT_MUTED};
        """)
        title_layout.addWidget(subtitle)
        
        header.addWidget(title_widget)
        header.addStretch()
        
        # 添加账户按钮
        add_btn = QPushButton("+ 添加账户")
        add_btn.setStyleSheet(ButtonStyles.PRIMARY)
        add_btn.setFixedSize(120, 40)
        add_btn.clicked.connect(self.add_account)
        header.addWidget(add_btn)
        
        return header
    
    def create_left_panel(self) -> QFrame:
        """创建左侧面板"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 24, 0)
        layout.setSpacing(20)
        
        # === 账户卡片 ===
        accounts_label = QLabel("交易账户")
        accounts_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(accounts_label)
        
        self.qmt_card = AccountCard("QMT", "📊")
        self.qmt_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.qmt_card.mousePressEvent = lambda e: self.connect_broker("QMT")
        layout.addWidget(self.qmt_card)
        
        self.ptrade_card = AccountCard("PTrade", "📈")
        self.ptrade_card.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ptrade_card.mousePressEvent = lambda e: self.connect_broker("PTrade")
        layout.addWidget(self.ptrade_card)
        
        # === 快捷下单 ===
        order_frame = QFrame()
        order_frame.setStyleSheet(CardStyles.DEFAULT)
        order_layout = QVBoxLayout(order_frame)
        order_layout.setContentsMargins(20, 20, 20, 20)
        order_layout.setSpacing(16)
        
        order_title = QLabel("快捷下单")
        order_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        order_layout.addWidget(order_title)
        
        # 股票代码
        code_layout = QHBoxLayout()
        code_label = QLabel("代码")
        code_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; min-width: 50px;")
        code_layout.addWidget(code_label)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("如 600519")
        self.code_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        code_layout.addWidget(self.code_input)
        order_layout.addLayout(code_layout)
        
        # 买卖方向
        dir_layout = QHBoxLayout()
        dir_label = QLabel("方向")
        dir_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; min-width: 50px;")
        dir_layout.addWidget(dir_label)
        
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["买入", "卖出"])
        self.direction_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        dir_layout.addWidget(self.direction_combo)
        order_layout.addLayout(dir_layout)
        
        # 价格
        price_layout = QHBoxLayout()
        price_label = QLabel("价格")
        price_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; min-width: 50px;")
        price_layout.addWidget(price_label)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 9999.99)
        self.price_input.setValue(10.00)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("¥ ")
        self.price_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        price_layout.addWidget(self.price_input)
        order_layout.addLayout(price_layout)
        
        # 数量
        qty_layout = QHBoxLayout()
        qty_label = QLabel("数量")
        qty_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; min-width: 50px;")
        qty_layout.addWidget(qty_label)
        
        self.qty_input = QSpinBox()
        self.qty_input.setRange(100, 1000000)
        self.qty_input.setValue(100)
        self.qty_input.setSingleStep(100)
        self.qty_input.setSuffix(" 股")
        self.qty_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 10px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        qty_layout.addWidget(self.qty_input)
        order_layout.addLayout(qty_layout)
        
        # 下单按钮
        self.submit_btn = QPushButton("确认下单")
        self.submit_btn.setStyleSheet(ButtonStyles.PRIMARY)
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setEnabled(False)
        self.submit_btn.clicked.connect(self.submit_order)
        order_layout.addWidget(self.submit_btn)
        
        layout.addWidget(order_frame)
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self) -> QFrame:
        """创建右侧面板"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(24, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标签页
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
        
        # 持仓
        positions_tab = self.create_positions_tab()
        tabs.addTab(positions_tab, "📋 持仓")
        
        # 委托
        orders_tab = self.create_orders_tab()
        tabs.addTab(orders_tab, "📝 委托")
        
        # 成交
        trades_tab = self.create_trades_tab()
        tabs.addTab(trades_tab, "✅ 成交")
        
        layout.addWidget(tabs)
        
        return panel
    
    def create_positions_tab(self) -> QWidget:
        """创建持仓标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(7)
        self.positions_table.setHorizontalHeaderLabels([
            "股票代码", "股票名称", "持仓数量", "可用数量", "成本价", "现价", "盈亏"
        ])
        self.positions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.positions_table.verticalHeader().setVisible(False)
        self.positions_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: transparent;
                border: none;
            }}
            QTableWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Colors.BORDER_DARK};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_MUTED};
                padding: 12px;
                border: none;
                font-weight: 600;
            }}
        """)
        layout.addWidget(self.positions_table)
        
        return tab
    
    def create_orders_tab(self) -> QWidget:
        """创建委托标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(7)
        self.orders_table.setHorizontalHeaderLabels([
            "时间", "股票代码", "股票名称", "方向", "价格", "数量", "状态"
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.orders_table.verticalHeader().setVisible(False)
        self.orders_table.setStyleSheet(self.positions_table.styleSheet())
        layout.addWidget(self.orders_table)
        
        return tab
    
    def create_trades_tab(self) -> QWidget:
        """创建成交标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.trades_table = QTableWidget()
        self.trades_table.setColumnCount(7)
        self.trades_table.setHorizontalHeaderLabels([
            "时间", "股票代码", "股票名称", "方向", "成交价", "成交量", "成交额"
        ])
        self.trades_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.trades_table.verticalHeader().setVisible(False)
        self.trades_table.setStyleSheet(self.positions_table.styleSheet())
        layout.addWidget(self.trades_table)
        
        return tab
    
    def add_account(self):
        """添加账户"""
        from PyQt6.QtWidgets import QInputDialog
        
        brokers = ["QMT (迅投miniQMT)", "PTrade (恒生PTrade)", "模拟交易"]
        broker, ok = QInputDialog.getItem(
            self, "选择券商", "请选择要连接的券商:", brokers, 0, False
        )
        
        if ok and broker:
            if "QMT" in broker:
                self.connect_broker("QMT")
            elif "PTrade" in broker:
                self.connect_broker("PTrade")
            else:
                self.connect_broker("Simulation")
    
    def connect_broker(self, broker_type: str):
        """连接券商"""
        dialog = BrokerConfigDialog(broker_type, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            config = dialog.get_config()
            
            # 显示连接中状态
            if broker_type == "QMT":
                self.qmt_card.set_status("connecting")
            elif broker_type == "PTrade":
                self.ptrade_card.set_status("connecting")
            
            # 启动连接线程
            self.connect_thread = BrokerConnectThread(broker_type, config)
            self.connect_thread.finished.connect(
                lambda ok, msg: self.on_broker_connected(broker_type, ok, msg)
            )
            self.connect_thread.start()
    
    def on_broker_connected(self, broker_type: str, success: bool, message: str):
        """券商连接完成回调"""
        if success:
            QMessageBox.information(self, "成功", message)
            
            if broker_type == "QMT":
                self.qmt_card.set_status("online", 0, 0)
                self.current_broker = self.connect_thread.broker
            elif broker_type == "PTrade":
                self.ptrade_card.set_status("online", 0, 0)
                self.current_broker = self.connect_thread.broker
            elif broker_type == "Simulation":
                self.current_broker = self.connect_thread.broker
            
            self.refresh_timer.start(5000)
            self.refresh_data()
            self.submit_btn.setEnabled(True)
        else:
            QMessageBox.warning(self, "连接失败", message)
            
            if broker_type == "QMT":
                self.qmt_card.set_status("offline")
            elif broker_type == "PTrade":
                self.ptrade_card.set_status("offline")
    
    def submit_order(self):
        """提交委托"""
        if not self.current_broker or not self.current_broker.is_connected:
            QMessageBox.warning(self, "提示", "请先连接券商")
            return
        
        code = self.code_input.text().strip()
        if not code:
            QMessageBox.warning(self, "提示", "请输入股票代码")
            return
        
        direction = self.direction_combo.currentText()
        price = self.price_input.value()
        qty = self.qty_input.value()
        
        reply = QMessageBox.question(self, "确认委托", 
            f"确认提交以下委托？\n\n"
            f"股票代码: {code}\n"
            f"交易方向: {direction}\n"
            f"委托价格: ¥{price:.2f}\n"
            f"委托数量: {qty}股",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from core.broker.base import OrderSide, OrderType
                
                side = OrderSide.BUY if direction == "买入" else OrderSide.SELL
                order_id = self.current_broker.place_order(
                    stock_code=code,
                    side=side,
                    quantity=qty,
                    price=price,
                    order_type=OrderType.LIMIT
                )
                
                if order_id:
                    QMessageBox.information(self, "成功", f"委托已提交\n订单号: {order_id}")
                    self.refresh_data()
                else:
                    QMessageBox.warning(self, "失败", "委托提交失败")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"委托异常: {e}")
    
    def refresh_data(self):
        """刷新数据"""
        if not self.current_broker or not self.current_broker.is_connected:
            return
        
        try:
            account = self.current_broker.get_account()
            if account:
                profit = account.profit if hasattr(account, 'profit') else 0
                if self.current_broker.name.startswith("QMT"):
                    self.qmt_card.set_status("online", account.cash, profit)
                elif self.current_broker.name.startswith("PTrade"):
                    self.ptrade_card.set_status("online", account.cash, profit)
            
            positions = self.current_broker.get_positions()
            self.update_positions_table(positions)
            
            orders = self.current_broker.get_orders()
            self.update_orders_table(orders)
            
            trades = self.current_broker.get_trades()
            self.update_trades_table(trades)
        except Exception as e:
            logger.error(f"刷新数据失败: {e}")
    
    def update_positions_table(self, positions):
        """更新持仓表格"""
        self.positions_table.setRowCount(0)
        for pos in positions:
            row = self.positions_table.rowCount()
            self.positions_table.insertRow(row)
            
            self.positions_table.setItem(row, 0, QTableWidgetItem(pos.stock_code))
            self.positions_table.setItem(row, 1, QTableWidgetItem(pos.stock_name))
            self.positions_table.setItem(row, 2, QTableWidgetItem(str(pos.quantity)))
            self.positions_table.setItem(row, 3, QTableWidgetItem(str(pos.available)))
            self.positions_table.setItem(row, 4, QTableWidgetItem(f"¥{pos.cost_price:.2f}"))
            self.positions_table.setItem(row, 5, QTableWidgetItem(f"¥{pos.current_price:.2f}"))
            
            profit_item = QTableWidgetItem(f"{'+'if pos.profit>=0 else ''}¥{pos.profit:.2f}")
            profit_item.setForeground(QColor(Colors.SUCCESS if pos.profit >= 0 else Colors.ERROR))
            self.positions_table.setItem(row, 6, profit_item)
    
    def update_orders_table(self, orders):
        """更新委托表格"""
        self.orders_table.setRowCount(0)
        for order in orders:
            row = self.orders_table.rowCount()
            self.orders_table.insertRow(row)
            
            time_str = order.create_time.strftime("%H:%M:%S") if hasattr(order.create_time, 'strftime') else str(order.create_time)
            self.orders_table.setItem(row, 0, QTableWidgetItem(time_str))
            self.orders_table.setItem(row, 1, QTableWidgetItem(order.stock_code))
            self.orders_table.setItem(row, 2, QTableWidgetItem(""))
            self.orders_table.setItem(row, 3, QTableWidgetItem(order.side.value))
            self.orders_table.setItem(row, 4, QTableWidgetItem(f"¥{order.price:.2f}"))
            self.orders_table.setItem(row, 5, QTableWidgetItem(str(order.quantity)))
            self.orders_table.setItem(row, 6, QTableWidgetItem(order.status.value))
    
    def update_trades_table(self, trades):
        """更新成交表格"""
        self.trades_table.setRowCount(0)
        for trade in trades:
            row = self.trades_table.rowCount()
            self.trades_table.insertRow(row)
            
            self.trades_table.setItem(row, 0, QTableWidgetItem(str(trade.get('time', ''))))
            self.trades_table.setItem(row, 1, QTableWidgetItem(trade.get('stock_code', '')))
            self.trades_table.setItem(row, 2, QTableWidgetItem(""))
            self.trades_table.setItem(row, 3, QTableWidgetItem(trade.get('side', '')))
            self.trades_table.setItem(row, 4, QTableWidgetItem(f"¥{trade.get('price', 0):.2f}"))
            self.trades_table.setItem(row, 5, QTableWidgetItem(str(trade.get('quantity', 0))))
            self.trades_table.setItem(row, 6, QTableWidgetItem(f"¥{trade.get('amount', 0):.2f}"))
