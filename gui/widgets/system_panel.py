# -*- coding: utf-8 -*-
"""
系统设置面板 - 最终产品形态
专业的系统配置与管理界面
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QLineEdit, QGroupBox,
    QComboBox, QSpinBox, QCheckBox, QMessageBox, QTabWidget,
    QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)


class ConnectionTestThread(QThread):
    """连接测试线程"""
    
    finished = pyqtSignal(bool, str)
    
    def __init__(self, source: str, config: dict, parent=None):
        super().__init__(parent)
        self.source = source
        self.config = config
    
    def run(self):
        try:
            if self.source == "jqdata":
                import jqdatasdk as jq
                jq.auth(self.config['username'], self.config['password'])
                count = jq.get_query_count()
                if count:
                    self.finished.emit(True, f"连接成功！剩余查询次数: {count.get('spare', 'N/A')}")
                else:
                    self.finished.emit(False, "连接失败：无法获取账户信息")
            else:
                self.finished.emit(False, "不支持的数据源")
        except Exception as e:
            self.finished.emit(False, f"连接失败: {str(e)}")


class StatusCard(QFrame):
    """状态卡片"""
    
    def __init__(self, title: str, status: str = "未连接", 
                 icon: str = "⚪", parent=None):
        super().__init__(parent)
        
        self.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border: 1px solid #2a2a4a;
                border-radius: 10px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(12)
        
        self.icon_label = QLabel(icon)
        self.icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(self.icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #cdd6f4; font-weight: bold;")
        text_layout.addWidget(self.title_label)
        
        self.status_label = QLabel(status)
        self.status_label.setStyleSheet("color: #667788; font-size: 12px;")
        text_layout.addWidget(self.status_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
    
    def set_status(self, status: str, connected: bool = False):
        """设置状态"""
        self.status_label.setText(status)
        if connected:
            self.icon_label.setText("🟢")
            self.status_label.setStyleSheet("color: #a6e3a1; font-size: 12px;")
        else:
            self.icon_label.setText("🔴")
            self.status_label.setStyleSheet("color: #f38ba8; font-size: 12px;")


class SystemPanel(QWidget):
    """系统设置面板"""
    
    system_started = pyqtSignal()
    system_stopped = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_running = False
        self.test_thread = None
        self.init_ui()
        self.load_config()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(24, 24, 24, 24)
        
        # 标题
        header = QHBoxLayout()
        title = QLabel("⚙️ 系统设置")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        header.addWidget(title)
        header.addStretch()
        content_layout.addLayout(header)
        
        # 系统状态
        status_section = self.create_status_section()
        content_layout.addWidget(status_section)
        
        # 配置标签页
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                background-color: #181825;
            }
            QTabBar::tab {
                background-color: transparent;
                color: #8899aa;
                padding: 12px 24px;
                border: none;
            }
            QTabBar::tab:selected {
                color: #667eea;
                border-bottom: 2px solid #667eea;
            }
        """)
        
        # 数据源配置
        data_tab = self.create_data_tab()
        tabs.addTab(data_tab, "📊 数据源")
        
        # 券商配置
        broker_tab = self.create_broker_tab()
        tabs.addTab(broker_tab, "🏦 券商")
        
        # 通用设置
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, "🔧 通用")
        
        content_layout.addWidget(tabs)
        
        content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def create_status_section(self) -> QFrame:
        """创建状态区域"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #181825;
                border: 1px solid #2a2a4a;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        
        header = QHBoxLayout()
        title = QLabel("🖥️ 系统状态")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        header.addWidget(title)
        header.addStretch()
        
        self.system_status = QLabel("● 未启动")
        self.system_status.setStyleSheet("color: #f38ba8; font-size: 14px;")
        header.addWidget(self.system_status)
        
        layout.addLayout(header)
        
        # 状态卡片
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(12)
        
        self.jqdata_status = StatusCard("聚宽数据", "未连接")
        cards_layout.addWidget(self.jqdata_status)
        
        self.ptrade_status = StatusCard("PTrade", "未连接")
        cards_layout.addWidget(self.ptrade_status)
        
        self.qmt_status = StatusCard("QMT", "未连接")
        cards_layout.addWidget(self.qmt_status)
        
        layout.addLayout(cards_layout)
        
        # 控制按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.start_btn = QPushButton("🚀 启动系统")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 12px 32px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #94d990;
            }
        """)
        self.start_btn.clicked.connect(self.start_system)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ 停止系统")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 32px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e06c75;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_system)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        layout.addLayout(btn_layout)
        
        return frame
    
    def create_data_tab(self) -> QWidget:
        """创建数据源配置"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # 聚宽配置
        jq_group = QGroupBox("聚宽数据 (JQData)")
        jq_group.setStyleSheet("""
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """)
        
        jq_layout = QGridLayout(jq_group)
        jq_layout.setSpacing(12)
        
        label_style = "color: #8899aa; font-size: 12px;"
        input_style = """
            QLineEdit {
                background-color: #12121f;
                border: 1px solid #2a2a4a;
                border-radius: 6px;
                padding: 10px;
                color: #cdd6f4;
            }
            QLineEdit:focus {
                border-color: #667eea;
            }
        """
        
        username_label = QLabel("用户名")
        username_label.setStyleSheet(label_style)
        jq_layout.addWidget(username_label, 0, 0)
        
        self.jq_username = QLineEdit()
        self.jq_username.setPlaceholderText("输入聚宽账号")
        self.jq_username.setStyleSheet(input_style)
        jq_layout.addWidget(self.jq_username, 0, 1)
        
        password_label = QLabel("密码")
        password_label.setStyleSheet(label_style)
        jq_layout.addWidget(password_label, 1, 0)
        
        self.jq_password = QLineEdit()
        self.jq_password.setPlaceholderText("输入聚宽密码")
        self.jq_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.jq_password.setStyleSheet(input_style)
        jq_layout.addWidget(self.jq_password, 1, 1)
        
        jq_btn_layout = QHBoxLayout()
        jq_btn_layout.addStretch()
        
        self.jq_test_btn = QPushButton("测试连接")
        self.jq_test_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6fd6;
            }
        """)
        self.jq_test_btn.clicked.connect(self.test_jqdata)
        jq_btn_layout.addWidget(self.jq_test_btn)
        
        jq_layout.addLayout(jq_btn_layout, 2, 0, 1, 2)
        
        layout.addWidget(jq_group)
        
        # TuShare配置
        ts_group = QGroupBox("TuShare (备选)")
        ts_group.setStyleSheet(jq_group.styleSheet())
        
        ts_layout = QGridLayout(ts_group)
        ts_layout.setSpacing(12)
        
        token_label = QLabel("Token")
        token_label.setStyleSheet(label_style)
        ts_layout.addWidget(token_label, 0, 0)
        
        self.ts_token = QLineEdit()
        self.ts_token.setPlaceholderText("输入TuShare Token")
        self.ts_token.setStyleSheet(input_style)
        ts_layout.addWidget(self.ts_token, 0, 1)
        
        layout.addWidget(ts_group)
        
        # 保存按钮
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        save_btn = QPushButton("💾 保存配置")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 12px 32px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #94d990;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        save_layout.addWidget(save_btn)
        
        layout.addLayout(save_layout)
        layout.addStretch()
        
        return tab
    
    def create_broker_tab(self) -> QWidget:
        """创建券商配置"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        group_style = """
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """
        
        label_style = "color: #8899aa; font-size: 12px;"
        input_style = """
            QLineEdit {
                background-color: #12121f;
                border: 1px solid #2a2a4a;
                border-radius: 6px;
                padding: 10px;
                color: #cdd6f4;
            }
        """
        
        # PTrade配置
        ptrade_group = QGroupBox("国金PTrade")
        ptrade_group.setStyleSheet(group_style)
        
        ptrade_layout = QGridLayout(ptrade_group)
        ptrade_layout.setSpacing(12)
        
        ptrade_ip_label = QLabel("服务器地址")
        ptrade_ip_label.setStyleSheet(label_style)
        ptrade_layout.addWidget(ptrade_ip_label, 0, 0)
        
        self.ptrade_ip = QLineEdit()
        self.ptrade_ip.setPlaceholderText("如: 192.168.1.100")
        self.ptrade_ip.setStyleSheet(input_style)
        ptrade_layout.addWidget(self.ptrade_ip, 0, 1)
        
        ptrade_port_label = QLabel("端口")
        ptrade_port_label.setStyleSheet(label_style)
        ptrade_layout.addWidget(ptrade_port_label, 0, 2)
        
        self.ptrade_port = QLineEdit()
        self.ptrade_port.setPlaceholderText("8888")
        self.ptrade_port.setStyleSheet(input_style)
        ptrade_layout.addWidget(self.ptrade_port, 0, 3)
        
        ptrade_user_label = QLabel("账号")
        ptrade_user_label.setStyleSheet(label_style)
        ptrade_layout.addWidget(ptrade_user_label, 1, 0)
        
        self.ptrade_user = QLineEdit()
        self.ptrade_user.setStyleSheet(input_style)
        ptrade_layout.addWidget(self.ptrade_user, 1, 1)
        
        ptrade_pwd_label = QLabel("密码")
        ptrade_pwd_label.setStyleSheet(label_style)
        ptrade_layout.addWidget(ptrade_pwd_label, 1, 2)
        
        self.ptrade_pwd = QLineEdit()
        self.ptrade_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.ptrade_pwd.setStyleSheet(input_style)
        ptrade_layout.addWidget(self.ptrade_pwd, 1, 3)
        
        layout.addWidget(ptrade_group)
        
        # QMT配置
        qmt_group = QGroupBox("国金QMT")
        qmt_group.setStyleSheet(group_style)
        
        qmt_layout = QGridLayout(qmt_group)
        qmt_layout.setSpacing(12)
        
        qmt_path_label = QLabel("安装路径")
        qmt_path_label.setStyleSheet(label_style)
        qmt_layout.addWidget(qmt_path_label, 0, 0)
        
        self.qmt_path = QLineEdit()
        self.qmt_path.setPlaceholderText("如: C:\\Program Files\\QMT")
        self.qmt_path.setStyleSheet(input_style)
        qmt_layout.addWidget(self.qmt_path, 0, 1, 1, 3)
        
        qmt_account_label = QLabel("资金账号")
        qmt_account_label.setStyleSheet(label_style)
        qmt_layout.addWidget(qmt_account_label, 1, 0)
        
        self.qmt_account = QLineEdit()
        self.qmt_account.setStyleSheet(input_style)
        qmt_layout.addWidget(self.qmt_account, 1, 1)
        
        layout.addWidget(qmt_group)
        
        # 保存按钮
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        
        save_btn = QPushButton("💾 保存配置")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                border: none;
                border-radius: 6px;
                padding: 12px 32px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #94d990;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        save_layout.addWidget(save_btn)
        
        layout.addLayout(save_layout)
        layout.addStretch()
        
        return tab
    
    def create_general_tab(self) -> QWidget:
        """创建通用设置"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
        
        group_style = """
            QGroupBox {
                color: #ffffff;
                font-weight: bold;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }
        """
        
        # 界面设置
        ui_group = QGroupBox("界面设置")
        ui_group.setStyleSheet(group_style)
        
        ui_layout = QVBoxLayout(ui_group)
        ui_layout.setSpacing(12)
        
        self.skip_welcome = QCheckBox("启动时跳过欢迎页面")
        self.skip_welcome.setStyleSheet("color: #cdd6f4;")
        ui_layout.addWidget(self.skip_welcome)
        
        self.auto_start = QCheckBox("启动时自动连接数据源")
        self.auto_start.setStyleSheet("color: #cdd6f4;")
        ui_layout.addWidget(self.auto_start)
        
        layout.addWidget(ui_group)
        
        # 日志设置
        log_group = QGroupBox("日志设置")
        log_group.setStyleSheet(group_style)
        
        log_layout = QHBoxLayout(log_group)
        log_layout.setSpacing(12)
        
        log_level_label = QLabel("日志级别")
        log_level_label.setStyleSheet("color: #8899aa;")
        log_layout.addWidget(log_level_label)
        
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.log_level.setCurrentText("INFO")
        self.log_level.setStyleSheet("""
            QComboBox {
                background-color: #12121f;
                border: 1px solid #2a2a4a;
                border-radius: 6px;
                padding: 8px;
                color: #cdd6f4;
                min-width: 100px;
            }
        """)
        log_layout.addWidget(self.log_level)
        log_layout.addStretch()
        
        layout.addWidget(log_group)
        
        # 关于
        about_group = QGroupBox("关于")
        about_group.setStyleSheet(group_style)
        
        about_layout = QVBoxLayout(about_group)
        
        about_text = QLabel("""
<p style="color: #cdd6f4; line-height: 1.8;">
<b>韬睿量化专业版</b> v2.0<br>
专业的量化投资研究与交易平台<br><br>
<span style="color: #667788;">© 2024 TaoRui Technology</span>
</p>
        """)
        about_text.setTextFormat(Qt.TextFormat.RichText)
        about_layout.addWidget(about_text)
        
        layout.addWidget(about_group)
        
        layout.addStretch()
        
        return tab
    
    def load_config(self):
        """加载配置"""
        try:
            from config.config_manager import get_config_manager
            cm = get_config_manager()
            
            jq_config = cm.get_jqdata_config()
            if jq_config:
                self.jq_username.setText(jq_config.get('username', ''))
                self.jq_password.setText(jq_config.get('password', ''))
                
        except Exception as e:
            logger.warning(f"加载配置失败: {e}")
    
    def save_config(self):
        """保存配置"""
        try:
            from config.config_manager import get_config_manager
            cm = get_config_manager()
            
            cm.save_jqdata_config(
                self.jq_username.text(),
                self.jq_password.text()
            )
            
            QMessageBox.information(self, "成功", "配置已保存")
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            QMessageBox.warning(self, "错误", f"保存失败: {e}")
    
    def test_jqdata(self):
        """测试聚宽连接"""
        username = self.jq_username.text().strip()
        password = self.jq_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "提示", "请输入用户名和密码")
            return
        
        self.jq_test_btn.setEnabled(False)
        self.jq_test_btn.setText("测试中...")
        
        self.test_thread = ConnectionTestThread(
            "jqdata",
            {"username": username, "password": password}
        )
        self.test_thread.finished.connect(self.on_test_finished)
        self.test_thread.start()
    
    def on_test_finished(self, success: bool, message: str):
        """测试完成"""
        self.jq_test_btn.setEnabled(True)
        self.jq_test_btn.setText("测试连接")
        
        if success:
            self.jqdata_status.set_status("已连接", True)
            QMessageBox.information(self, "成功", message)
        else:
            self.jqdata_status.set_status("连接失败", False)
            QMessageBox.warning(self, "失败", message)
    
    def start_system(self):
        """启动系统"""
        username = self.jq_username.text().strip()
        password = self.jq_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "提示", "请先配置聚宽账号")
            return
        
        try:
            import jqdatasdk as jq
            jq.auth(username, password)
            
            count = jq.get_query_count()
            if count:
                self.is_running = True
                self.system_status.setText("● 运行中")
                self.system_status.setStyleSheet("color: #a6e3a1; font-size: 14px;")
                self.jqdata_status.set_status("已连接", True)
                
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
                
                self.system_started.emit()
                QMessageBox.information(self, "成功", "系统启动成功！")
            else:
                QMessageBox.warning(self, "错误", "无法获取账户信息")
                
        except Exception as e:
            logger.error(f"启动系统失败: {e}")
            QMessageBox.warning(self, "错误", f"启动失败: {e}")
    
    def stop_system(self):
        """停止系统"""
        try:
            import jqdatasdk as jq
            jq.logout()
        except:
            pass
        
        self.is_running = False
        self.system_status.setText("● 已停止")
        self.system_status.setStyleSheet("color: #f38ba8; font-size: 14px;")
        self.jqdata_status.set_status("未连接", False)
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self.system_stopped.emit()
        QMessageBox.information(self, "提示", "系统已停止")
