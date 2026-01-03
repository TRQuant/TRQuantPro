# -*- coding: utf-8 -*-
"""
候选池展示面板

基于JQData构建的候选池可视化展示模块
支持两种数据模式：
- 历史模式（免费版）：使用历史数据进行策略验证
- 实时模式（付费版）：使用实时数据进行实盘选股
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView,
    QScrollArea, QComboBox, QLineEdit, QCheckBox, QGroupBox,
    QMessageBox, QProgressBar, QSplitter, QTextEdit, QCompleter
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QStringListModel
from PyQt6.QtGui import QFont, QColor
from datetime import datetime
import logging

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)


class ScanAllMarketsWorker(QThread):
    """
    一键扫描全部市场工作线程（基于主线）
    
    数据流：
    1. 从MongoDB读取已映射的主线（综合评分时已完成AKShare→JQData映射）
    2. 直接使用JQData获取成分股（快速）
    3. 对成分股进行动量/成长筛选
    """
    
    finished = pyqtSignal(dict)  # 扫描完成信号，传递扫描结果
    progress = pyqtSignal(str)   # 进度更新信号
    error = pyqtSignal(str)       # 错误信号
    
    def __init__(self, period: str = 'medium', min_score: float = 60.0):
        super().__init__()
        self.period = period  # 'short', 'medium', 'long'
        self.min_score = min_score
    
    def run(self):
        """在后台线程中基于主线扫描"""
        try:
            from jqdata.client import JQDataClient
            from core.mainline_scanner import MainlineBasedScanner
            from config.config_manager import get_config_manager
            
            # 初始化JQData客户端
            self.progress.emit("🔐 正在认证JQData...")
            config_manager = get_config_manager()
            config = config_manager.get_jqdata_config()
            
            if not config.get('username') or not config.get('password'):
                self.error.emit("未找到JQData配置，请先配置 config/jqdata_config.json")
                return
            
            jq_client = JQDataClient()
            if not jq_client.authenticate(config['username'], config['password']):
                self.error.emit("JQData认证失败，请检查账号密码")
                return
            
            # 显示JQData数据权限
            perm = jq_client.get_permission()
            mode = "实时模式" if perm.is_realtime else "历史模式"
            self.progress.emit(f"📊 JQData: {mode} ({perm.start_date} 至 {perm.end_date})")
            
            # 创建基于主线的扫描器
            self.progress.emit("📂 从MongoDB读取已映射的主线...")
            scanner = MainlineBasedScanner(jq_client=jq_client)
            
            # 从主线扫描（直接使用JQData，无需重新映射）
            self.progress.emit("📊 使用JQData获取成分股...")
            
            result = scanner.scan_from_mainlines(
                period=self.period,
                min_score=self.min_score,
                max_mainlines=10,
                max_stocks_per_mainline=20
            )
            
            self.progress.emit("✅ 扫描完成（数据源: JQData）")
            self.finished.emit(result)
            
        except Exception as e:
            import traceback
            logger.error(f"基于主线扫描失败: {e}")
            traceback.print_exc()
            self.error.emit(f"扫描失败: {str(e)}")


class CandidatePoolWorker(QThread):
    """候选池构建工作线程"""
    
    finished = pyqtSignal(object)  # 构建完成信号，传递CandidatePool对象
    progress = pyqtSignal(str)      # 进度更新信号
    error = pyqtSignal(str)         # 错误信号
    data_mode_info = pyqtSignal(dict)  # 数据模式信息信号
    
    def __init__(self, mainline_name: str, mainline_type: str, use_cache: bool = True):
        super().__init__()
        self.mainline_name = mainline_name
        self.mainline_type = mainline_type
        self.use_cache = use_cache
    
    def run(self):
        """在后台线程中构建候选池"""
        try:
            from jqdata.client import JQDataClient
            from core.candidate_pool_builder import CandidatePoolBuilder
            from config.config_manager import get_config_manager
            
            # 初始化JQData客户端
            self.progress.emit("🔐 正在认证JQData...")
            config_manager = get_config_manager()
            config = config_manager.get_jqdata_config()
            
            if not config.get('username') or not config.get('password'):
                self.error.emit("未找到JQData配置，请先配置 config/jqdata_config.json")
                return
            
            jq_client = JQDataClient()
            if not jq_client.authenticate(config['username'], config['password']):
                self.error.emit("JQData认证失败，请检查账号密码")
                return
            
            # 发送数据模式信息
            perm = jq_client.get_permission()
            mode_info = {
                'is_realtime': perm.is_realtime,
                'start_date': perm.start_date,
                'end_date': perm.end_date,
                'detected': perm.detected
            }
            self.data_mode_info.emit(mode_info)
            
            mode_str = "实时模式" if perm.is_realtime else "历史模式"
            self.progress.emit(f"📊 数据模式: {mode_str} ({perm.start_date} 至 {perm.end_date})")
            
            # 创建候选池构建器
            self.progress.emit("🔧 正在初始化构建器...")
            builder = CandidatePoolBuilder(jq_client=jq_client)
            
            # 构建候选池
            self.progress.emit(f"📊 正在构建候选池: {self.mainline_name}...")
            pool = builder.build_from_mainline(
                mainline_name=self.mainline_name,
                mainline_type=self.mainline_type,
                date=None,  # 自动使用权限范围内的最新日期
                use_cache=self.use_cache
            )
            
            self.progress.emit("✅ 候选池构建完成")
            self.finished.emit(pool)
            
        except Exception as e:
            import traceback
            logger.error(f"构建候选池失败: {e}")
            traceback.print_exc()
            self.error.emit(f"构建失败: {str(e)}")


class CandidatePoolPanel(QWidget):
    """候选池展示面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_pool = None
        self.worker = None
        self.scan_worker = None
        self.data_mode_info = None
        self.concept_list = []  # 概念列表缓存
        self.scan_results = {}  # 扫描结果 {period: [stocks]}
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(16)
        
        # 1. 控制面板
        content_layout.addWidget(self._create_control_section())
        
        # 2. 统计信息
        content_layout.addWidget(self._create_stats_section())
        
        # 3. 候选股票表格
        content_layout.addWidget(self._create_table_section())
        
        # 4. 详细信息
        content_layout.addWidget(self._create_detail_section())
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _create_control_section(self) -> QFrame:
        """创建控制面板"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 标题行（包含数据模式指示）
        title_layout = QHBoxLayout()
        
        title = QLabel("🎯 候选池构建")
        title.setFont(QFont("Microsoft YaHei", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        title_layout.addWidget(title)
        
        title_layout.addStretch()
        
        # 数据模式指示器
        self.mode_indicator = QLabel("⏳ 等待连接...")
        self.mode_indicator.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_MUTED};
                font-size: 11px;
                padding: 4px 10px;
                background-color: {Colors.BG_TERTIARY};
                border-radius: 4px;
            }}
        """)
        title_layout.addWidget(self.mode_indicator)
        
        layout.addLayout(title_layout)
        
        # 提示信息（历史模式下显示）
        self.mode_hint = QLabel("")
        self.mode_hint.setStyleSheet(f"""
            QLabel {{
                color: {Colors.WARNING};
                font-size: 11px;
                padding: 6px 10px;
                background-color: {Colors.WARNING}22;
                border-radius: 4px;
            }}
        """)
        self.mode_hint.setVisible(False)
        self.mode_hint.setWordWrap(True)
        layout.addWidget(self.mode_hint)
        
        # 输入区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        # 主线名称
        input_layout.addWidget(QLabel("主线名称:"))
        self.mainline_input = QLineEdit()
        self.mainline_input.setPlaceholderText("例如: 新能源汽车")
        self.mainline_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
        """)
        input_layout.addWidget(self.mainline_input)
        
        # 主线类型
        input_layout.addWidget(QLabel("类型:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["concept", "industry"])
        self.type_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
        """)
        input_layout.addWidget(self.type_combo)
        
        # 使用缓存
        self.cache_checkbox = QCheckBox("使用缓存")
        self.cache_checkbox.setChecked(True)
        input_layout.addWidget(self.cache_checkbox)
        
        # 构建按钮
        self.build_btn = QPushButton("构建候选池")
        self.build_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.ACCENT};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_MUTED};
            }}
        """)
        self.build_btn.clicked.connect(self._build_pool)
        input_layout.addWidget(self.build_btn)
        
        input_layout.addStretch()
        layout.addLayout(input_layout)
        
        # 一键扫描全部区域
        scan_layout = QHBoxLayout()
        scan_layout.setSpacing(12)
        
        scan_layout.addWidget(QLabel("期限:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["短期(1-3月)", "中期(3-6月)", "长期(6-12月)", "全部"])
        self.period_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
        """)
        scan_layout.addWidget(self.period_combo)
        
        scan_layout.addWidget(QLabel("最小得分:"))
        self.min_score_input = QLineEdit()
        self.min_score_input.setPlaceholderText("60")
        self.min_score_input.setText("60")
        self.min_score_input.setFixedWidth(60)
        self.min_score_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
        """)
        scan_layout.addWidget(self.min_score_input)
        
        # 一键扫描全部按钮
        self.scan_all_btn = QPushButton("🚀 一键扫描全部（基于主线→JQData）")
        self.scan_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.ACCENT};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 12px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_MUTED};
            }}
        """)
        self.scan_all_btn.clicked.connect(self._scan_all_markets)
        scan_layout.addWidget(self.scan_all_btn)
        
        scan_layout.addStretch()
        layout.addLayout(scan_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                background-color: {Colors.BG_PRIMARY};
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {Colors.PRIMARY};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px;")
        layout.addWidget(self.status_label)
        
        return frame
    
    def _create_stats_section(self) -> QFrame:
        """创建统计信息面板"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(20)
        
        # 统计项
        self.stats_labels = {}
        stats_items = [
            ("total", "总成分股", "0"),
            ("filtered", "筛选后", "0"),
            ("avg_tech", "平均技术得分", "0.0"),
            ("avg_fund", "平均基本面得分", "0.0"),
            ("avg_composite", "平均综合得分", "0.0"),
            ("data_date", "数据日期", "-"),
        ]
        
        for key, label, default in stats_items:
            stat_frame = QFrame()
            stat_layout = QVBoxLayout(stat_frame)
            stat_layout.setSpacing(4)
            
            stat_label = QLabel(label)
            stat_label.setStyleSheet(f"color: {Colors.TEXT_MUTED}; font-size: 11px;")
            stat_layout.addWidget(stat_label)
            
            stat_value = QLabel(default)
            stat_value.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
            stat_value.setStyleSheet(f"color: {Colors.PRIMARY};")
            stat_layout.addWidget(stat_value)
            
            self.stats_labels[key] = stat_value
            layout.addWidget(stat_frame)
        
        layout.addStretch()
        return frame
    
    def _create_table_section(self) -> QFrame:
        """创建表格区域"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 标题和筛选
        header_layout = QHBoxLayout()
        
        title = QLabel("📋 候选股票列表")
        title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # 排序选择
        header_layout.addWidget(QLabel("排序:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "综合得分 ↓",
            "综合得分 ↑",
            "技术得分 ↓",
            "基本面得分 ↓",
            "涨跌幅 ↓"
        ])
        self.sort_combo.currentIndexChanged.connect(self._update_table)
        header_layout.addWidget(self.sort_combo)
        
        # 最小得分筛选
        header_layout.addWidget(QLabel("最小得分:"))
        self.min_score_input = QLineEdit()
        self.min_score_input.setPlaceholderText("0")
        self.min_score_input.setFixedWidth(60)
        self.min_score_input.textChanged.connect(self._update_table)
        header_layout.addWidget(self.min_score_input)
        
        layout.addLayout(header_layout)
        
        # 期限选择标签
        period_label = QLabel("显示期限:")
        period_label.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-size: 11px;")
        header_layout.addWidget(period_label)
        
        self.period_filter_combo = QComboBox()
        self.period_filter_combo.addItems(["全部", "短期", "中期", "长期"])
        self.period_filter_combo.currentIndexChanged.connect(self._update_table)
        header_layout.addWidget(self.period_filter_combo)
        
        layout.addLayout(header_layout)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "排名", "代码", "名称", "期限", "涨跌幅(1M)", "涨跌幅(3M)", "涨跌幅(6M)",
            "动量得分", "成长得分", "综合得分", "ROE", "标签"
        ])
        
        # 设置表格样式
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                gridline-color: {Colors.BORDER_PRIMARY};
            }}
            QTableWidget::item {{
                padding: 6px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.PRIMARY}33;
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {Colors.BORDER_PRIMARY};
                font-weight: 600;
            }}
        """)
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.setColumnWidth(0, 50)   # 排名
        self.table.setColumnWidth(1, 100)   # 代码
        self.table.setColumnWidth(2, 120)   # 名称
        self.table.setColumnWidth(3, 60)    # 期限
        self.table.setColumnWidth(4, 80)    # 涨跌幅(1M)
        self.table.setColumnWidth(5, 80)    # 涨跌幅(3M)
        self.table.setColumnWidth(6, 80)    # 涨跌幅(6M)
        self.table.setColumnWidth(7, 80)    # 动量得分
        self.table.setColumnWidth(8, 80)    # 成长得分
        self.table.setColumnWidth(9, 80)    # 综合得分
        self.table.setColumnWidth(10, 80)   # ROE
        self.table.setColumnWidth(11, 150)  # 标签
        
        # 设置选择模式
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        
        layout.addWidget(self.table)
        
        return frame
    
    def _create_detail_section(self) -> QFrame:
        """创建详细信息面板"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        title = QLabel("📊 股票详情")
        title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        
        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setMaximumHeight(200)
        self.detail_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 10px;
                font-size: 11px;
                font-family: 'Microsoft YaHei', monospace;
            }}
        """)
        layout.addWidget(self.detail_text)
        
        return frame
    
    def _build_pool(self):
        """构建候选池"""
        mainline_name = self.mainline_input.text().strip()
        if not mainline_name:
            QMessageBox.warning(self, "提示", "请输入主线名称")
            return
        
        mainline_type = self.type_combo.currentText()
        use_cache = self.cache_checkbox.isChecked()
        
        # 禁用按钮
        self.build_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.status_label.setText("正在构建候选池...")
        
        # 创建工作线程
        if self.worker:
            self.worker.terminate()
            self.worker.wait()
        
        self.worker = CandidatePoolWorker(mainline_name, mainline_type, use_cache)
        self.worker.finished.connect(self._on_pool_built)
        self.worker.progress.connect(self._on_progress)
        self.worker.error.connect(self._on_error)
        self.worker.data_mode_info.connect(self._on_data_mode_info)
        self.worker.start()
    
    def _on_progress(self, message: str):
        """进度更新"""
        self.status_label.setText(message)
    
    def _on_pool_built(self, pool):
        """候选池构建完成"""
        self.current_pool = pool
        
        # 更新统计信息
        self._update_stats(pool)
        
        # 更新表格
        self._update_table()
        
        # 恢复按钮
        self.build_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # 显示数据模式和日期信息
        mode_str = "实时" if pool.data_mode == 'realtime' else "历史"
        date_str = pool.data_date if pool.data_date else "未知"
        self.status_label.setText(
            f"✅ 构建完成: {pool.filtered_count} 只候选股票 "
            f"| 数据模式: {mode_str} | 数据日期: {date_str}"
        )
    
    def _on_error(self, error_msg: str):
        """构建失败"""
        QMessageBox.critical(self, "错误", error_msg)
        self.build_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"❌ {error_msg}")
    
    def _on_data_mode_info(self, mode_info: dict):
        """更新数据模式信息"""
        self.data_mode_info = mode_info
        
        if mode_info.get('is_realtime'):
            # 实时模式
            self.mode_indicator.setText("🟢 实时模式")
            self.mode_indicator.setStyleSheet(f"""
                QLabel {{
                    color: {Colors.SUCCESS};
                    font-size: 11px;
                    padding: 4px 10px;
                    background-color: {Colors.SUCCESS}22;
                    border-radius: 4px;
                }}
            """)
            self.mode_hint.setVisible(False)
        else:
            # 历史模式
            start = mode_info.get('start_date', '未知')
            end = mode_info.get('end_date', '未知')
            self.mode_indicator.setText(f"📅 历史模式 ({end})")
            self.mode_indicator.setStyleSheet(f"""
                QLabel {{
                    color: {Colors.WARNING};
                    font-size: 11px;
                    padding: 4px 10px;
                    background-color: {Colors.WARNING}22;
                    border-radius: 4px;
                }}
            """)
            self.mode_hint.setText(
                f"⚠️ 免费版账号仅能访问 {start} 至 {end} 的历史数据。"
                f"筛选结果基于该时间段的数据，可用于策略验证。"
                f"开通付费账号后可获取实时数据。"
            )
            self.mode_hint.setVisible(True)
    
    def _update_stats(self, pool):
        """更新统计信息"""
        if not pool:
            return
        
        self.stats_labels["total"].setText(str(pool.total_count))
        self.stats_labels["filtered"].setText(str(pool.filtered_count))
        self.stats_labels["data_date"].setText(pool.data_date if pool.data_date else "-")
        
        if pool.stocks:
            avg_tech = sum(s.technical_score for s in pool.stocks) / len(pool.stocks)
            avg_fund = sum(s.fundamental_score for s in pool.stocks) / len(pool.stocks)
            avg_composite = sum(s.composite_score for s in pool.stocks) / len(pool.stocks)
            
            self.stats_labels["avg_tech"].setText(f"{avg_tech:.1f}")
            self.stats_labels["avg_fund"].setText(f"{avg_fund:.1f}")
            self.stats_labels["avg_composite"].setText(f"{avg_composite:.1f}")
        else:
            self.stats_labels["avg_tech"].setText("0.0")
            self.stats_labels["avg_fund"].setText("0.0")
            self.stats_labels["avg_composite"].setText("0.0")
    
    def _update_table(self):
        """更新表格"""
        # 优先显示扫描结果
        if self.scan_results:
            self._update_table_from_scan_results()
            return
        
        # 否则显示候选池结果
        if not self.current_pool or not self.current_pool.stocks:
            self.table.setRowCount(0)
            return
        
        # 获取筛选和排序参数
        stocks = self.current_pool.stocks.copy()
        
        # 最小得分筛选
        try:
            min_score = float(self.min_score_input.text() or "0")
            stocks = [s for s in stocks if s.composite_score >= min_score]
        except:
            pass
        
        # 排序
        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:  # 综合得分 ↓
            stocks.sort(key=lambda x: x.composite_score, reverse=True)
        elif sort_index == 1:  # 综合得分 ↑
            stocks.sort(key=lambda x: x.composite_score, reverse=False)
        elif sort_index == 2:  # 技术得分 ↓
            stocks.sort(key=lambda x: x.technical_score, reverse=True)
        elif sort_index == 3:  # 基本面得分 ↓
            stocks.sort(key=lambda x: x.fundamental_score, reverse=True)
        elif sort_index == 4:  # 涨跌幅 ↓
            stocks.sort(key=lambda x: x.change_pct, reverse=True)
        
        # 填充表格
        self.table.setRowCount(len(stocks))
        
        for row, stock in enumerate(stocks):
            # 排名
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # 代码
            self.table.setItem(row, 1, QTableWidgetItem(stock.code))
            
            # 名称
            self.table.setItem(row, 2, QTableWidgetItem(stock.name))
            
            # 涨跌幅
            change_item = QTableWidgetItem(f"{stock.change_pct:.2f}%")
            if stock.change_pct > 0:
                change_item.setForeground(QColor(Colors.ERROR))  # 红色表示上涨
            elif stock.change_pct < 0:
                change_item.setForeground(QColor(Colors.SUCCESS))  # 绿色表示下跌
            self.table.setItem(row, 3, change_item)
            
            # 技术得分
            self.table.setItem(row, 4, QTableWidgetItem(f"{stock.technical_score:.1f}"))
            
            # 基本面得分
            self.table.setItem(row, 5, QTableWidgetItem(f"{stock.fundamental_score:.1f}"))
            
            # 综合得分
            score_item = QTableWidgetItem(f"{stock.composite_score:.1f}")
            score_item.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
            if stock.composite_score >= 70:
                score_item.setForeground(QColor(Colors.PRIMARY))
            self.table.setItem(row, 6, score_item)
            
            # 标签
            tags = ", ".join(stock.tags) if stock.tags else "-"
            self.table.setItem(row, 7, QTableWidgetItem(tags))
            
            # 连续上涨
            self.table.setItem(row, 8, QTableWidgetItem(f"{stock.consecutive_up_days}天"))
            
            # ROE
            roe_text = f"{stock.roe:.2f}%" if stock.roe else "-"
            self.table.setItem(row, 9, QTableWidgetItem(roe_text))
        
        # 调整列宽
        self.table.resizeColumnsToContents()
    
    def _update_table_from_scan_results(self):
        """从扫描结果更新表格"""
        # 获取期限筛选
        period_filter = self.period_filter_combo.currentText()
        
        # 收集所有股票
        all_stocks = []
        if period_filter == "全部":
            for period, stocks in self.scan_results.items():
                all_stocks.extend(stocks)
        elif period_filter == "短期":
            all_stocks = self.scan_results.get('short', [])
        elif period_filter == "中期":
            all_stocks = self.scan_results.get('medium', [])
        elif period_filter == "长期":
            all_stocks = self.scan_results.get('long', [])
        
        # 最小得分筛选
        try:
            min_score = float(self.min_score_input.text() or "0")
            all_stocks = [s for s in all_stocks if s.composite_score >= min_score]
        except:
            pass
        
        # 排序
        sort_index = self.sort_combo.currentIndex()
        if sort_index == 0:  # 综合得分 ↓
            all_stocks.sort(key=lambda x: x.composite_score, reverse=True)
        elif sort_index == 1:  # 综合得分 ↑
            all_stocks.sort(key=lambda x: x.composite_score, reverse=False)
        elif sort_index == 2:  # 动量得分 ↓
            all_stocks.sort(key=lambda x: x.momentum_score, reverse=True)
        elif sort_index == 3:  # 成长得分 ↓
            all_stocks.sort(key=lambda x: x.growth_score, reverse=True)
        
        # 填充表格
        self.table.setRowCount(len(all_stocks))
        
        for row, stock in enumerate(all_stocks):
            # 排名
            self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # 代码
            code = stock.code.replace('.XSHE', '').replace('.XSHG', '')
            self.table.setItem(row, 1, QTableWidgetItem(code))
            
            # 名称
            self.table.setItem(row, 2, QTableWidgetItem(stock.name))
            
            # 期限
            period_map = {'short': '短期', 'medium': '中期', 'long': '长期'}
            period_text = period_map.get(stock.period, stock.period)
            self.table.setItem(row, 3, QTableWidgetItem(period_text))
            
            # 涨跌幅(1M)
            change_1m_item = QTableWidgetItem(f"{stock.price_change_1m:.2f}%")
            if stock.price_change_1m > 0:
                change_1m_item.setForeground(QColor(Colors.ERROR))
            self.table.setItem(row, 4, change_1m_item)
            
            # 涨跌幅(3M)
            change_3m_item = QTableWidgetItem(f"{stock.price_change_3m:.2f}%")
            if stock.price_change_3m > 0:
                change_3m_item.setForeground(QColor(Colors.ERROR))
            self.table.setItem(row, 5, change_3m_item)
            
            # 涨跌幅(6M)
            change_6m_item = QTableWidgetItem(f"{stock.price_change_6m:.2f}%")
            if stock.price_change_6m > 0:
                change_6m_item.setForeground(QColor(Colors.ERROR))
            self.table.setItem(row, 6, change_6m_item)
            
            # 动量得分
            self.table.setItem(row, 7, QTableWidgetItem(f"{stock.momentum_score:.1f}"))
            
            # 成长得分
            self.table.setItem(row, 8, QTableWidgetItem(f"{stock.growth_score:.1f}"))
            
            # 综合得分
            score_item = QTableWidgetItem(f"{stock.composite_score:.1f}")
            score_item.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
            if stock.composite_score >= 70:
                score_item.setForeground(QColor(Colors.PRIMARY))
            self.table.setItem(row, 9, score_item)
            
            # ROE
            roe_text = f"{stock.roe:.2f}%" if stock.roe else "-"
            self.table.setItem(row, 10, QTableWidgetItem(roe_text))
            
            # 标签
            tags = ", ".join(stock.tags) if stock.tags else "-"
            self.table.setItem(row, 11, QTableWidgetItem(tags))
        
        # 调整列宽
        self.table.resizeColumnsToContents()
    
    def _on_selection_changed(self):
        """选择变化时更新详情"""
        selected_items = self.table.selectedItems()
        if not selected_items:
            self.detail_text.clear()
            return
        
        row = selected_items[0].row()
        if not self.current_pool or row >= len(self.current_pool.stocks):
            return
        
        stock = self.current_pool.stocks[row]
        
        # 生成详情文本
        detail = f"""
股票代码: {stock.code}
股票名称: {stock.name}
所属主线: {stock.sector or self.current_pool.mainline_name}
主线类型: {stock.sector_type or self.current_pool.mainline_type}

【技术指标】
涨跌幅: {stock.change_pct:.2f}%
是否涨停: {'是' if stock.is_limit_up else '否'}
是否放量突破: {'是' if stock.is_volume_breakout else '否'}
是否站上均线: {'是' if stock.is_ma_breakthrough else '否'}
连续上涨天数: {stock.consecutive_up_days}天
技术面得分: {stock.technical_score:.1f}

【财务指标】
ROE: {(f'{stock.roe:.2f}%' if stock.roe else 'N/A')}
净利润同比增长: {(f'{stock.net_profit_growth:.2f}%' if stock.net_profit_growth else 'N/A')}
营收同比增长: {(f'{stock.revenue_growth:.2f}%' if stock.revenue_growth else 'N/A')}
基本面得分: {stock.fundamental_score:.1f}

【综合评分】
综合得分: {stock.composite_score:.1f}
标签: {', '.join(stock.tags) if stock.tags else '无'}

更新时间: {stock.update_time}
        """.strip()
        
        self.detail_text.setText(detail)
    
    def _scan_all_markets(self):
        """一键扫描全部市场"""
        try:
            min_score = float(self.min_score_input.text() or "60")
        except:
            min_score = 60.0
        
        period_text = self.period_combo.currentText()
        if "短期" in period_text:
            period = 'short'
        elif "中期" in period_text:
            period = 'medium'
        elif "长期" in period_text:
            period = 'long'
        else:
            period = 'all'
        
        # 禁用按钮
        self.scan_all_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText("正在扫描全市场...")
        
        # 创建工作线程
        if self.scan_worker:
            self.scan_worker.terminate()
            self.scan_worker.wait()
        
        self.scan_worker = ScanAllMarketsWorker(period=period, min_score=min_score)
        self.scan_worker.finished.connect(self._on_scan_all_finished)
        self.scan_worker.progress.connect(self._on_progress)
        self.scan_worker.error.connect(self._on_error)
        self.scan_worker.start()
    
    def _on_scan_all_finished(self, result: dict):
        """扫描全部完成（基于主线）"""
        # 转换结果格式
        stocks = result.get('stocks', [])
        mainlines = result.get('mainlines', [])
        features = result.get('features', {})
        
        # 按期限分组
        self.scan_results = {
            'short': [s for s in stocks if s.period == 'short'],
            'medium': [s for s in stocks if s.period == 'medium'],
            'long': [s for s in stocks if s.period == 'long']
        }
        
        # 统计信息
        total_stocks = len(stocks)
        short_count = len(self.scan_results['short'])
        medium_count = len(self.scan_results['medium'])
        long_count = len(self.scan_results['long'])
        
        # 更新统计
        self.stats_labels["total"].setText(str(total_stocks))
        self.stats_labels["filtered"].setText(f"短:{short_count} 中:{medium_count} 长:{long_count}")
        
        # 显示主线映射信息
        mainline_info = f"处理了 {len(mainlines)} 个主线"
        if mainlines:
            mainline_info += f": {', '.join([m['akshare_name'] for m in mainlines[:3]])}"
            if len(mainlines) > 3:
                mainline_info += "..."
        
        # 显示推荐特征
        feature_info = ""
        if features:
            feature_info = f" | 推荐: 综合≥{features.get('min_composite_score', 65)}分"
        
        # 更新表格
        self._update_table()
        
        # 恢复按钮
        self.scan_all_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText(
            f"✅ 扫描完成: {total_stocks} 只股票 ({mainline_info}){feature_info}"
        )
        
        # 显示特征条件（可选）
        if features:
            logger.info(f"推荐特征条件: {features}")

