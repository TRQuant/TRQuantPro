# -*- coding: utf-8 -*-
"""
因子库面板
==========

提供因子的可视化管理界面，包括：
- 因子分类浏览
- 因子详情展示
- 因子计算
- 多因子组合
- PTrade策略代码生成
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox, QFormLayout,
    QListWidget, QListWidgetItem, QSplitter, QMessageBox,
    QProgressBar, QCheckBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QColor
import logging
from pathlib import Path
from datetime import datetime
import sys

logger = logging.getLogger(__name__)


class FactorCalculationThread(QThread):
    """因子计算线程"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, factor_manager, factor_names, stocks, date):
        super().__init__()
        self.factor_manager = factor_manager
        self.factor_names = factor_names
        self.stocks = stocks
        self.date = date
    
    def run(self):
        try:
            results = {}
            total = len(self.factor_names)
            
            for i, name in enumerate(self.factor_names):
                self.progress.emit(
                    int((i + 1) / total * 100),
                    f"计算因子: {name}"
                )
                result = self.factor_manager.calculate_factor(name, self.stocks, self.date)
                if result:
                    results[name] = result
            
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))


class FactorPanel(QWidget):
    """因子库面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.factor_manager = None
        self.jq_client = None
        self.current_results = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("📊 量化因子库")
        title.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #4fc3f7; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                background: #2d2d2d;
            }
            QTabBar::tab {
                background: #3d3d3d;
                color: #cccccc;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #4fc3f7;
                color: #1e1e1e;
            }
            QTabBar::tab:hover:!selected {
                background: #4d4d4d;
            }
        """)
        
        # 添加选项卡
        self.tab_widget.addTab(self._create_tutorial_tab(), "📖 使用教程")
        self.tab_widget.addTab(self._create_factor_list_tab(), "因子列表")
        self.tab_widget.addTab(self._create_factor_calc_tab(), "因子计算")
        self.tab_widget.addTab(self._create_strategy_gen_tab(), "策略生成")
        
        layout.addWidget(self.tab_widget)
    
    def _create_tutorial_tab(self) -> QWidget:
        """创建使用教程选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #2d2d2d;
            }
        """)
        
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        
        # 教程内容
        tutorial_html = """
<div style="color: #cccccc; font-family: 'Microsoft YaHei', sans-serif;">

<h2 style="color: #4fc3f7;">📊 韬睿量化因子库使用教程</h2>

<p style="color: #888; font-size: 14px;">
本因子库提供22个量化因子，支持因子计算、多因子组合和PTrade策略代码自动生成。
</p>

<hr style="border-color: #3d3d3d;">

<h3 style="color: #81c784;">🎯 快速开始</h3>

<h4>步骤1: 在终端中运行真实数据测试</h4>
<pre style="background: #1e1e1e; padding: 15px; border-radius: 8px; color: #d4d4d4; font-family: Consolas, monospace;">
cd /home/taotao/.local/share/trquant
source venv/bin/activate
python test_factors_real.py
</pre>

<h4>步骤2: 查看测试结果</h4>
<p>测试脚本会：</p>
<ul style="color: #aaa;">
    <li>连接JQData获取沪深300成分股</li>
    <li>计算EP、ROE、Reversal三个因子</li>
    <li>组合因子并选出Top 10股票</li>
    <li>生成PTrade策略代码并保存</li>
</ul>

<hr style="border-color: #3d3d3d;">

<h3 style="color: #81c784;">📈 因子说明</h3>

<table style="width: 100%; border-collapse: collapse; color: #ccc;">
<tr style="background: #3d3d3d;">
    <th style="padding: 10px; text-align: left;">类别</th>
    <th style="padding: 10px; text-align: left;">因子</th>
    <th style="padding: 10px; text-align: left;">说明</th>
    <th style="padding: 10px; text-align: left;">A股有效性</th>
</tr>
<tr style="border-bottom: 1px solid #3d3d3d;">
    <td style="padding: 8px;">价值</td>
    <td style="padding: 8px;">EP, BP, SP, 股息率</td>
    <td style="padding: 8px;">估值因子，低估值策略</td>
    <td style="padding: 8px; color: #81c784;">★★★☆☆</td>
</tr>
<tr style="border-bottom: 1px solid #3d3d3d;">
    <td style="padding: 8px;">成长</td>
    <td style="padding: 8px;">营收增速, 利润增速, ROE变化</td>
    <td style="padding: 8px;">成长性因子</td>
    <td style="padding: 8px; color: #81c784;">★★★☆☆</td>
</tr>
<tr style="border-bottom: 1px solid #3d3d3d;">
    <td style="padding: 8px;">质量</td>
    <td style="padding: 8px;">ROE, 毛利率, 周转率, 杠杆</td>
    <td style="padding: 8px;">盈利质量因子</td>
    <td style="padding: 8px; color: #81c784;">★★★★☆</td>
</tr>
<tr style="border-bottom: 1px solid #3d3d3d;">
    <td style="padding: 8px;">动量</td>
    <td style="padding: 8px;">价格动量, <b style="color: #4fc3f7;">反转</b>, 相对强弱</td>
    <td style="padding: 8px;">趋势/反转因子</td>
    <td style="padding: 8px; color: #4fc3f7;">★★★★★</td>
</tr>
<tr>
    <td style="padding: 8px;">资金流</td>
    <td style="padding: 8px;"><b style="color: #4fc3f7;">北向资金</b>, 主力资金, 融资</td>
    <td style="padding: 8px;">A股特色因子</td>
    <td style="padding: 8px; color: #4fc3f7;">★★★★★</td>
</tr>
</table>

<p style="color: #888; font-size: 12px; margin-top: 10px;">
💡 <b>提示:</b> 短期反转和北向资金是A股最有效的两个因子
</p>

<hr style="border-color: #3d3d3d;">

<h3 style="color: #81c784;">🚀 PTrade策略部署</h3>

<h4>1. 生成策略代码</h4>
<p>在"策略生成"选项卡中设置参数，点击生成按钮</p>

<h4>2. 上传到PTrade</h4>
<p>将生成的策略文件上传到PTrade平台：</p>
<pre style="background: #1e1e1e; padding: 15px; border-radius: 8px; color: #d4d4d4;">
策略文件位置: /home/taotao/.local/share/trquant/strategies/ptrade/
</pre>

<h4>3. 回测验证</h4>
<p>在PTrade中运行回测，验证策略效果</p>

<hr style="border-color: #3d3d3d;">

<h3 style="color: #81c784;">📝 推荐策略配置</h3>

<pre style="background: #1e1e1e; padding: 15px; border-radius: 8px; color: #d4d4d4;">
<span style="color: #6a9955;"># 经典三因子 + 北向资金增强</span>
因子组合:
  - EP (价值): 权重 0.2
  - ROE (质量): 权重 0.2  
  - Reversal (反转): 权重 0.3
  - NorthboundFlow (北向): 权重 0.3

股票池: 沪深300
持仓数量: 30只
调仓频率: 月度
</pre>

<hr style="border-color: #3d3d3d;">

<h3 style="color: #81c784;">⚠️ 注意事项</h3>

<ul style="color: #aaa;">
    <li><b>JQData权限:</b> 您的账号数据范围为 2024-08-19 至 2025-08-26</li>
    <li><b>因子计算:</b> 首次计算可能较慢，结果会被缓存</li>
    <li><b>回测验证:</b> 建议先在PTrade回测，再进行实盘</li>
    <li><b>风险控制:</b> 实盘时建议设置止损和仓位限制</li>
</ul>

</div>
"""
        
        tutorial_text = QTextEdit()
        tutorial_text.setReadOnly(True)
        tutorial_text.setHtml(tutorial_html)
        tutorial_text.setStyleSheet("""
            QTextEdit {
                background: #2d2d2d;
                border: none;
                padding: 10px;
            }
        """)
        content_layout.addWidget(tutorial_text)
        
        # 快捷按钮
        btn_layout = QHBoxLayout()
        
        run_test_btn = QPushButton("🔬 运行真实数据测试")
        run_test_btn.setStyleSheet("""
            QPushButton {
                background: #4caf50;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #66bb6a;
            }
        """)
        run_test_btn.clicked.connect(self._run_real_test)
        btn_layout.addWidget(run_test_btn)
        
        open_strategy_btn = QPushButton("📂 打开策略目录")
        open_strategy_btn.setStyleSheet("""
            QPushButton {
                background: #2196f3;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #42a5f5;
            }
        """)
        open_strategy_btn.clicked.connect(self._open_strategy_folder)
        btn_layout.addWidget(open_strategy_btn)
        
        btn_layout.addStretch()
        content_layout.addLayout(btn_layout)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        return widget
    
    def _run_real_test(self):
        """运行真实数据测试"""
        import subprocess
        from pathlib import Path
        
        project_root = Path(__file__).parent.parent.parent
        test_script = project_root / "test_factors_real.py"
        venv_python = project_root / "venv" / "bin" / "python"
        
        if not test_script.exists():
            QMessageBox.warning(self, "错误", "测试脚本不存在")
            return
        
        try:
            # 在终端中运行测试
            cmd = f'cd {project_root} && source venv/bin/activate && python test_factors_real.py'
            
            # 使用gnome-terminal或xterm打开
            subprocess.Popen([
                'gnome-terminal', '--', 'bash', '-c', 
                f'{cmd}; echo ""; echo "按Enter键关闭..."; read'
            ])
            
            QMessageBox.information(
                self, 
                "测试启动", 
                "真实数据测试已在新终端中启动。\n\n"
                "测试内容:\n"
                "1. 连接JQData\n"
                "2. 获取沪深300成分股\n"
                "3. 计算EP、ROE、Reversal因子\n"
                "4. 组合因子选股\n"
                "5. 生成PTrade策略代码"
            )
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动测试失败: {e}")
    
    def _open_strategy_folder(self):
        """打开策略文件夹"""
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        from pathlib import Path
        
        strategy_path = Path(__file__).parent.parent.parent / "strategies" / "ptrade"
        
        if strategy_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(strategy_path)))
        else:
            QMessageBox.warning(self, "错误", "策略目录不存在")
    
    def _create_factor_list_tab(self) -> QWidget:
        """创建因子列表选项卡"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # 左侧：因子分类
        left_panel = QGroupBox("因子分类")
        left_panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        
        self.category_list = QListWidget()
        self.category_list.setStyleSheet("""
            QListWidget {
                background: #2d2d2d;
                border: none;
                color: #cccccc;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background: #4fc3f7;
                color: #1e1e1e;
            }
            QListWidget::item:hover:!selected {
                background: #3d3d3d;
            }
        """)
        
        categories = [
            ("📈 价值因子", "value"),
            ("🚀 成长因子", "growth"),
            ("⭐ 质量因子", "quality"),
            ("📊 动量因子", "momentum"),
            ("💰 资金流因子", "flow"),
        ]
        
        for name, key in categories:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.category_list.addItem(item)
        
        self.category_list.currentItemChanged.connect(self._on_category_changed)
        left_layout.addWidget(self.category_list)
        
        # 右侧：因子详情
        right_panel = QGroupBox("因子详情")
        right_panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        
        # 因子表格
        self.factor_table = QTableWidget()
        self.factor_table.setColumnCount(4)
        self.factor_table.setHorizontalHeaderLabels(["因子名称", "类别", "描述", "方向"])
        self.factor_table.setStyleSheet("""
            QTableWidget {
                background: #2d2d2d;
                border: none;
                color: #cccccc;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background: #4fc3f7;
                color: #1e1e1e;
            }
            QHeaderView::section {
                background: #3d3d3d;
                color: #4fc3f7;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.factor_table.horizontalHeader().setStretchLastSection(True)
        self.factor_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.factor_table.currentCellChanged.connect(self._on_factor_selected)
        right_layout.addWidget(self.factor_table)
        
        # 因子说明
        self.factor_detail = QTextEdit()
        self.factor_detail.setReadOnly(True)
        self.factor_detail.setMaximumHeight(150)
        self.factor_detail.setStyleSheet("""
            QTextEdit {
                background: #252526;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #cccccc;
                padding: 10px;
            }
        """)
        right_layout.addWidget(self.factor_detail)
        
        # 添加到布局
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 600])
        
        layout.addWidget(splitter)
        
        # 初始化因子管理器
        self._init_factor_manager()
        
        # 默认选中第一个分类
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
        
        return widget
    
    def _create_factor_calc_tab(self) -> QWidget:
        """创建因子计算选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 参数设置
        params_group = QGroupBox("计算参数")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        params_layout = QFormLayout(params_group)
        
        # 股票池选择
        self.stock_pool_combo = QComboBox()
        self.stock_pool_combo.addItems([
            "沪深300 (000300.XSHG)",
            "中证500 (000905.XSHG)",
            "中证1000 (000852.XSHG)",
            "上证50 (000016.XSHG)",
            "创业板指 (399006.XSHE)"
        ])
        self.stock_pool_combo.setStyleSheet("""
            QComboBox {
                background: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #cccccc;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background: #3d3d3d;
                color: #cccccc;
                selection-background-color: #4fc3f7;
            }
        """)
        params_layout.addRow("股票池:", self.stock_pool_combo)
        
        # 日期选择
        from PyQt6.QtWidgets import QDateEdit
        from PyQt6.QtCore import QDate
        self.calc_date = QDateEdit()
        self.calc_date.setDate(QDate.currentDate().addDays(-1))
        self.calc_date.setCalendarPopup(True)
        self.calc_date.setStyleSheet("""
            QDateEdit {
                background: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #cccccc;
            }
        """)
        params_layout.addRow("计算日期:", self.calc_date)
        
        layout.addWidget(params_group)
        
        # 因子选择
        factors_group = QGroupBox("选择因子")
        factors_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        factors_layout = QVBoxLayout(factors_group)
        
        # 因子复选框
        self.factor_checkboxes = {}
        checkbox_layout = QHBoxLayout()
        
        categories = {
            "价值": ["EP", "BP", "ROE"],
            "成长": ["RevenueGrowth", "ProfitGrowth"],
            "动量": ["Reversal", "PriceMomentum"],
            "资金": ["NorthboundFlow", "MainForceFlow"]
        }
        
        for cat_name, factors in categories.items():
            cat_widget = QWidget()
            cat_layout = QVBoxLayout(cat_widget)
            cat_label = QLabel(cat_name)
            cat_label.setStyleSheet("color: #4fc3f7; font-weight: bold;")
            cat_layout.addWidget(cat_label)
            
            for factor in factors:
                cb = QCheckBox(factor)
                cb.setStyleSheet("color: #cccccc;")
                self.factor_checkboxes[factor] = cb
                cat_layout.addWidget(cb)
            
            cat_layout.addStretch()
            checkbox_layout.addWidget(cat_widget)
        
        factors_layout.addLayout(checkbox_layout)
        
        # 全选/取消
        btn_layout = QHBoxLayout()
        select_all_btn = QPushButton("全选")
        select_all_btn.clicked.connect(lambda: self._toggle_all_factors(True))
        deselect_all_btn = QPushButton("取消全选")
        deselect_all_btn.clicked.connect(lambda: self._toggle_all_factors(False))
        
        for btn in [select_all_btn, deselect_all_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background: #3d3d3d;
                    border: 1px solid #4d4d4d;
                    border-radius: 4px;
                    padding: 5px 15px;
                    color: #cccccc;
                }
                QPushButton:hover {
                    background: #4d4d4d;
                }
            """)
        
        btn_layout.addWidget(select_all_btn)
        btn_layout.addWidget(deselect_all_btn)
        btn_layout.addStretch()
        factors_layout.addLayout(btn_layout)
        
        layout.addWidget(factors_group)
        
        # 计算按钮和进度
        calc_layout = QHBoxLayout()
        
        self.calc_btn = QPushButton("🔄 开始计算")
        self.calc_btn.setStyleSheet("""
            QPushButton {
                background: #4fc3f7;
                border: none;
                border-radius: 4px;
                padding: 10px 30px;
                color: #1e1e1e;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #81d4fa;
            }
            QPushButton:disabled {
                background: #3d3d3d;
                color: #666666;
            }
        """)
        self.calc_btn.clicked.connect(self._start_calculation)
        calc_layout.addWidget(self.calc_btn)
        
        self.calc_progress = QProgressBar()
        self.calc_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background: #2d2d2d;
                color: #cccccc;
            }
            QProgressBar::chunk {
                background: #4fc3f7;
            }
        """)
        self.calc_progress.setVisible(False)
        calc_layout.addWidget(self.calc_progress)
        
        layout.addLayout(calc_layout)
        
        # 结果展示
        results_group = QGroupBox("计算结果")
        results_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        results_layout = QVBoxLayout(results_group)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["因子", "有效值", "Top 5股票"])
        self.results_table.setStyleSheet("""
            QTableWidget {
                background: #2d2d2d;
                border: none;
                color: #cccccc;
                gridline-color: #3d3d3d;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background: #3d3d3d;
                color: #4fc3f7;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        self.results_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.results_table)
        
        layout.addWidget(results_group)
        
        return widget
    
    def _create_strategy_gen_tab(self) -> QWidget:
        """创建策略生成选项卡"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 策略参数
        params_group = QGroupBox("策略参数")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        params_layout = QFormLayout(params_group)
        
        # 股票池
        self.strategy_pool_combo = QComboBox()
        self.strategy_pool_combo.addItems([
            "沪深300 (000300.XSHG)",
            "中证500 (000905.XSHG)",
            "中证1000 (000852.XSHG)"
        ])
        self.strategy_pool_combo.setStyleSheet("""
            QComboBox {
                background: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #cccccc;
            }
        """)
        params_layout.addRow("股票池:", self.strategy_pool_combo)
        
        # 持仓数量
        self.hold_num_spin = QSpinBox()
        self.hold_num_spin.setRange(10, 100)
        self.hold_num_spin.setValue(30)
        self.hold_num_spin.setStyleSheet("""
            QSpinBox {
                background: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #cccccc;
            }
        """)
        params_layout.addRow("持仓数量:", self.hold_num_spin)
        
        # 调仓频率
        self.rebalance_combo = QComboBox()
        self.rebalance_combo.addItems(["月度调仓", "周度调仓", "日度调仓"])
        self.rebalance_combo.setStyleSheet("""
            QComboBox {
                background: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 10px;
                color: #cccccc;
            }
        """)
        params_layout.addRow("调仓频率:", self.rebalance_combo)
        
        layout.addWidget(params_group)
        
        # 因子权重设置
        weights_group = QGroupBox("因子权重")
        weights_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        weights_layout = QFormLayout(weights_group)
        
        self.weight_spins = {}
        default_factors = [
            ("EP", 0.2),
            ("ROE", 0.2),
            ("Reversal", 0.3),
            ("NorthboundFlow", 0.3)
        ]
        
        for factor, default_weight in default_factors:
            spin = QDoubleSpinBox()
            spin.setRange(0, 1)
            spin.setSingleStep(0.1)
            spin.setValue(default_weight)
            spin.setStyleSheet("""
                QDoubleSpinBox {
                    background: #3d3d3d;
                    border: 1px solid #4d4d4d;
                    border-radius: 4px;
                    padding: 5px 10px;
                    color: #cccccc;
                }
            """)
            self.weight_spins[factor] = spin
            weights_layout.addRow(f"{factor}:", spin)
        
        layout.addWidget(weights_group)
        
        # 生成按钮
        gen_btn = QPushButton("🚀 生成PTrade策略")
        gen_btn.setStyleSheet("""
            QPushButton {
                background: #4caf50;
                border: none;
                border-radius: 4px;
                padding: 10px 30px;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #66bb6a;
            }
        """)
        gen_btn.clicked.connect(self._generate_strategy)
        layout.addWidget(gen_btn)
        
        # 代码预览
        code_group = QGroupBox("策略代码预览")
        code_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4fc3f7;
            }
        """)
        code_layout = QVBoxLayout(code_group)
        
        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setStyleSheet("""
            QTextEdit {
                background: #1e1e1e;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        code_layout.addWidget(self.code_preview)
        
        # 保存按钮
        save_btn = QPushButton("💾 保存策略文件")
        save_btn.setStyleSheet("""
            QPushButton {
                background: #ff9800;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ffa726;
            }
        """)
        save_btn.clicked.connect(self._save_strategy)
        code_layout.addWidget(save_btn)
        
        layout.addWidget(code_group)
        
        return widget
    
    def _init_factor_manager(self):
        """初始化因子管理器"""
        try:
            # 添加项目路径
            project_root = Path(__file__).parent.parent.parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            
            from core.factors import FactorManager
            self.factor_manager = FactorManager()
            logger.info("因子管理器初始化成功")
        except Exception as e:
            logger.error(f"因子管理器初始化失败: {e}")
            self.factor_manager = None
    
    def _on_category_changed(self, current, previous):
        """分类切换事件"""
        if current is None:
            return
        
        category = current.data(Qt.ItemDataRole.UserRole)
        self._load_factors_by_category(category)
    
    def _load_factors_by_category(self, category: str):
        """加载指定分类的因子"""
        if self.factor_manager is None:
            return
        
        factors = self.factor_manager.list_factors(category)
        
        self.factor_table.setRowCount(len(factors))
        
        for i, factor_name in enumerate(factors):
            info = self.factor_manager.get_factor_info(factor_name)
            if info:
                self.factor_table.setItem(i, 0, QTableWidgetItem(info['name']))
                self.factor_table.setItem(i, 1, QTableWidgetItem(info['category']))
                self.factor_table.setItem(i, 2, QTableWidgetItem(info['description']))
                direction = "正向 ↑" if info['direction'] == 1 else "负向 ↓"
                self.factor_table.setItem(i, 3, QTableWidgetItem(direction))
        
        self.factor_table.resizeColumnsToContents()
    
    def _on_factor_selected(self, row, col, prev_row, prev_col):
        """因子选择事件"""
        if row < 0 or self.factor_manager is None:
            return
        
        factor_name = self.factor_table.item(row, 0).text()
        factor = self.factor_manager.get_factor(factor_name)
        
        if factor:
            detail = f"""
<h3 style="color: #4fc3f7;">{factor.name}</h3>
<p><b>类别:</b> {factor.category}</p>
<p><b>描述:</b> {factor.description}</p>
<p><b>方向:</b> {"正向（越大越好）" if factor.direction == 1 else "负向（越小越好）"}</p>
<hr>
<p style="color: #888;">此因子可用于多因子组合策略，支持自动生成PTrade代码。</p>
"""
            self.factor_detail.setHtml(detail)
    
    def _toggle_all_factors(self, checked: bool):
        """全选/取消全选因子"""
        for cb in self.factor_checkboxes.values():
            cb.setChecked(checked)
    
    def _start_calculation(self):
        """开始计算因子"""
        if self.factor_manager is None:
            QMessageBox.warning(self, "错误", "因子管理器未初始化")
            return
        
        # 获取选中的因子
        selected_factors = [
            name for name, cb in self.factor_checkboxes.items()
            if cb.isChecked()
        ]
        
        if not selected_factors:
            QMessageBox.warning(self, "提示", "请至少选择一个因子")
            return
        
        # 显示提示（实际计算需要JQData）
        QMessageBox.information(
            self,
            "提示",
            f"已选择 {len(selected_factors)} 个因子进行计算。\n\n"
            "注意：实际计算需要配置JQData账号。\n"
            "当前为演示模式。"
        )
        
        # 模拟结果
        self.results_table.setRowCount(len(selected_factors))
        for i, factor in enumerate(selected_factors):
            self.results_table.setItem(i, 0, QTableWidgetItem(factor))
            self.results_table.setItem(i, 1, QTableWidgetItem("300/300"))
            self.results_table.setItem(i, 2, QTableWidgetItem("模拟数据"))
    
    def _generate_strategy(self):
        """生成策略代码"""
        if self.factor_manager is None:
            QMessageBox.warning(self, "错误", "因子管理器未初始化")
            return
        
        # 获取参数
        pool_text = self.strategy_pool_combo.currentText()
        stock_pool = pool_text.split("(")[1].rstrip(")")
        hold_num = self.hold_num_spin.value()
        
        rebalance_map = {
            "月度调仓": "monthly",
            "周度调仓": "weekly",
            "日度调仓": "daily"
        }
        rebalance = rebalance_map[self.rebalance_combo.currentText()]
        
        # 获取因子权重
        weights = {}
        factor_names = []
        for factor, spin in self.weight_spins.items():
            weight = spin.value()
            if weight > 0:
                weights[factor] = weight
                factor_names.append(factor)
        
        if not factor_names:
            QMessageBox.warning(self, "提示", "请至少设置一个因子的权重")
            return
        
        # 生成代码
        try:
            code = self.factor_manager.generate_ptrade_strategy(
                factor_names=factor_names,
                weights=weights,
                stock_pool=stock_pool,
                hold_num=hold_num,
                rebalance_freq=rebalance
            )
            
            self.code_preview.setPlainText(code)
            self._generated_code = code
            
            logger.info(f"策略代码生成成功: {len(factor_names)}个因子")
            
        except Exception as e:
            logger.error(f"策略生成失败: {e}")
            QMessageBox.critical(self, "错误", f"策略生成失败: {e}")
    
    def _save_strategy(self):
        """保存策略文件"""
        if not hasattr(self, '_generated_code') or not self._generated_code:
            QMessageBox.warning(self, "提示", "请先生成策略代码")
            return
        
        try:
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"multi_factor_strategy_{timestamp}.py"
            
            # 保存
            filepath = self.factor_manager.save_strategy(
                self._generated_code,
                filename
            )
            
            QMessageBox.information(
                self,
                "成功",
                f"策略已保存到:\n{filepath}"
            )
            
        except Exception as e:
            logger.error(f"保存策略失败: {e}")
            QMessageBox.critical(self, "错误", f"保存失败: {e}")
    
    def set_jq_client(self, jq_client):
        """设置JQData客户端"""
        self.jq_client = jq_client
        if self.factor_manager:
            self.factor_manager.set_jq_client(jq_client)

