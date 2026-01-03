# -*- coding: utf-8 -*-
"""
策略开发面板 - 专业IDE体验
AI辅助策略开发与版本管理
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QScrollArea, QComboBox, QLineEdit,
    QTextEdit, QSplitter, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QHeaderView, QListWidget, QListWidgetItem, QSpinBox,
    QDoubleSpinBox, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat
from pathlib import Path
import re
import logging

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles

logger = logging.getLogger(__name__)


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
        
        # 内置函数
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#89b4fa"))
        builtins = ['print', 'len', 'range', 'int', 'str', 'float', 'list', 
                   'dict', 'set', 'tuple', 'abs', 'max', 'min', 'sum', 'sorted']
        for word in builtins:
            pattern = rf'\b{word}\b'
            self.highlighting_rules.append((re.compile(pattern), builtin_format))
        
        # 字符串
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a6e3a1"))
        self.highlighting_rules.append((re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))
        
        # 数字
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#fab387"))
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\.?[0-9]*\b'), number_format))
        
        # 注释
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#9ca3af"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((re.compile(r'#[^\n]*'), comment_format))
        
        # 函数定义
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#89dceb"))
        self.highlighting_rules.append((re.compile(r'\bdef\s+(\w+)'), function_format))
        
        # 类定义
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#f9e2af"))
        self.highlighting_rules.append((re.compile(r'\bclass\s+(\w+)'), class_format))
        
        # 装饰器
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor("#f38ba8"))
        self.highlighting_rules.append((re.compile(r'@\w+'), decorator_format))
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)


class CodeEditor(QTextEdit):
    """代码编辑器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置等宽字体
        font = QFont("JetBrains Mono", 12)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        
        # 设置样式
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_DARK};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                padding: 16px;
                line-height: 1.6;
            }}
        """)
        
        # 语法高亮
        self.highlighter = PythonHighlighter(self.document())
        
        # Tab设置
        self.setTabStopDistance(40)
    
    def keyPressEvent(self, event):
        # 自动缩进
        if event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            line = cursor.block().text()
            indent = len(line) - len(line.lstrip())
            
            if line.rstrip().endswith(':'):
                indent += 4
            
            super().keyPressEvent(event)
            self.insertPlainText(' ' * indent)
        else:
            super().keyPressEvent(event)


class StrategyPanel(QWidget):
    """策略开发面板"""
    
    run_backtest = pyqtSignal(str, dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_strategy = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # === 主分割器 ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Colors.BORDER_DARK};
                width: 1px;
            }}
        """)
        
        # === 左侧：策略列表 ===
        left_panel = self.create_strategy_list()
        splitter.addWidget(left_panel)
        
        # === 中间：代码编辑器 ===
        center_panel = self.create_code_editor()
        splitter.addWidget(center_panel)
        
        # === 右侧：参数与工具 ===
        right_panel = self.create_tools_panel()
        splitter.addWidget(right_panel)
        
        # 设置比例
        splitter.setSizes([220, 600, 320])
        
        layout.addWidget(splitter)
    
    def create_strategy_list(self) -> QFrame:
        """创建策略列表"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_DARK};
                border-right: 1px solid {Colors.BORDER_DARK};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        header = QWidget()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            background-color: {Colors.BG_SECONDARY};
            border-bottom: 1px solid {Colors.BORDER_DARK};
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 0, 8, 0)
        
        title = QLabel("策略列表")
        title.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # 新建按钮
        new_btn = QPushButton("+")
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY_LIGHT};
            }}
        """)
        new_btn.setFixedSize(28, 28)
        new_btn.clicked.connect(self.new_strategy)
        header_layout.addWidget(new_btn)
        
        layout.addWidget(header)
        
        # 搜索框
        search = QLineEdit()
        search.setPlaceholderText("🔍 搜索策略...")
        search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: none;
                border-bottom: 1px solid {Colors.BORDER_DARK};
                padding: 12px 16px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        layout.addWidget(search)
        
        # 策略树
        self.strategy_tree = QTreeWidget()
        self.strategy_tree.setHeaderHidden(True)
        self.strategy_tree.setStyleSheet(f"""
            QTreeWidget {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QTreeWidget::item {{
                padding: 8px 16px;
                border-radius: 0;
            }}
            QTreeWidget::item:selected {{
                background-color: {Colors.PRIMARY}33;
                color: {Colors.PRIMARY};
            }}
            QTreeWidget::item:hover {{
                background-color: {Colors.BG_HOVER};
            }}
            QTreeWidget::branch {{
                background-color: transparent;
            }}
        """)
        
        # 加载策略
        self.load_strategies()
        self.strategy_tree.itemClicked.connect(self.on_strategy_selected)
        
        layout.addWidget(self.strategy_tree)
        
        return panel
    
    def create_code_editor(self) -> QFrame:
        """创建代码编辑器"""
        panel = QFrame()
        panel.setStyleSheet(f"background-color: {Colors.BG_SECONDARY};")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 工具栏
        toolbar = QWidget()
        toolbar.setFixedHeight(48)
        toolbar.setStyleSheet(f"""
            background-color: {Colors.BG_TERTIARY};
            border-bottom: 1px solid {Colors.BORDER_DARK};
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(16, 0, 16, 0)
        toolbar_layout.setSpacing(8)
        
        # 文件名
        self.file_label = QLabel("未选择策略")
        self.file_label.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_SECONDARY};
        """)
        toolbar_layout.addWidget(self.file_label)
        toolbar_layout.addStretch()
        
        # 工具按钮
        tools = [
            ("💾", "保存", self.save_strategy),
            ("▶️", "运行回测", self.run_strategy),
            ("🤖", "AI优化", self.ai_optimize),
            ("📋", "复制", self.copy_code),
        ]
        
        for icon, tooltip, callback in tools:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {Colors.TEXT_MUTED};
                    border: none;
                    border-radius: 4px;
                    padding: 6px 10px;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background-color: {Colors.BG_HOVER};
                    color: {Colors.TEXT_SECONDARY};
                }}
            """)
            btn.clicked.connect(callback)
            toolbar_layout.addWidget(btn)
        
        layout.addWidget(toolbar)
        
        # 代码编辑器
        self.code_editor = CodeEditor()
        self.code_editor.setPlaceholderText("# 在此编写策略代码...\n# 选择左侧策略或创建新策略开始")
        layout.addWidget(self.code_editor)
        
        # 底部状态栏
        status_bar = QWidget()
        status_bar.setFixedHeight(28)
        status_bar.setStyleSheet(f"""
            background-color: {Colors.BG_TERTIARY};
            border-top: 1px solid {Colors.BORDER_DARK};
        """)
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(16, 0, 16, 0)
        
        self.cursor_label = QLabel("行 1, 列 1")
        self.cursor_label.setStyleSheet(f"""
            font-size: 11px;
            color: {Colors.TEXT_MUTED};
        """)
        status_layout.addWidget(self.cursor_label)
        status_layout.addStretch()
        
        lang_label = QLabel("Python")
        lang_label.setStyleSheet(f"""
            font-size: 11px;
            color: {Colors.TEXT_MUTED};
        """)
        status_layout.addWidget(lang_label)
        
        layout.addWidget(status_bar)
        
        # 更新光标位置
        self.code_editor.cursorPositionChanged.connect(self.update_cursor_pos)
        
        return panel
    
    def create_tools_panel(self) -> QFrame:
        """创建工具面板"""
        panel = QFrame()
        panel.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_DARK};
                border-left: 1px solid {Colors.BORDER_DARK};
            }}
        """)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标签页
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: transparent;
                border: none;
            }}
            QTabBar::tab {{
                background-color: transparent;
                color: {Colors.TEXT_MUTED};
                padding: 12px 16px;
                border: none;
                border-bottom: 2px solid transparent;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                color: {Colors.PRIMARY};
                border-bottom-color: {Colors.PRIMARY};
            }}
        """)
        
        # 参数标签页
        params_tab = self.create_params_tab()
        tabs.addTab(params_tab, "参数")
        
        # AI助手标签页
        ai_tab = self.create_ai_tab()
        tabs.addTab(ai_tab, "AI助手")
        
        # 版本标签页
        version_tab = self.create_version_tab()
        tabs.addTab(version_tab, "版本")
        
        layout.addWidget(tabs)
        
        return panel
    
    def create_params_tab(self) -> QWidget:
        """创建参数标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # 回测参数
        backtest_group = QGroupBox("回测参数")
        backtest_group.setStyleSheet(f"""
            QGroupBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 16px;
                font-weight: 600;
                color: {Colors.TEXT_PRIMARY};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """)
        backtest_layout = QVBoxLayout(backtest_group)
        backtest_layout.setSpacing(12)
        
        # 初始资金
        capital_layout = QHBoxLayout()
        capital_label = QLabel("初始资金")
        capital_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        capital_layout.addWidget(capital_label)
        self.capital_input = QSpinBox()
        self.capital_input.setRange(10000, 100000000)
        self.capital_input.setValue(1000000)
        self.capital_input.setSingleStep(100000)
        self.capital_input.setSuffix(" 元")
        self.capital_input.setStyleSheet(f"""
            QSpinBox {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        capital_layout.addWidget(self.capital_input)
        backtest_layout.addLayout(capital_layout)
        
        # 手续费
        fee_layout = QHBoxLayout()
        fee_label = QLabel("手续费率")
        fee_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        fee_layout.addWidget(fee_label)
        self.fee_input = QDoubleSpinBox()
        self.fee_input.setRange(0, 0.01)
        self.fee_input.setValue(0.0003)
        self.fee_input.setSingleStep(0.0001)
        self.fee_input.setDecimals(4)
        self.fee_input.setStyleSheet(f"""
            QDoubleSpinBox {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 4px;
                padding: 6px;
                color: {Colors.TEXT_SECONDARY};
            }}
        """)
        fee_layout.addWidget(self.fee_input)
        backtest_layout.addLayout(fee_layout)
        
        layout.addWidget(backtest_group)
        
        # 策略参数（动态生成）
        strategy_group = QGroupBox("策略参数")
        strategy_group.setStyleSheet(backtest_group.styleSheet())
        self.strategy_params_layout = QVBoxLayout(strategy_group)
        
        # 默认提示
        hint = QLabel("选择策略后显示参数")
        hint.setStyleSheet(f"color: {Colors.TEXT_MUTED}; padding: 20px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.strategy_params_layout.addWidget(hint)
        
        layout.addWidget(strategy_group)
        layout.addStretch()
        
        # 运行按钮
        run_btn = QPushButton("▶️ 运行回测")
        run_btn.setStyleSheet(ButtonStyles.PRIMARY)
        run_btn.setFixedHeight(44)
        run_btn.clicked.connect(self.run_strategy)
        layout.addWidget(run_btn)
        
        return tab
    
    def create_ai_tab(self) -> QWidget:
        """创建AI助手标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # 提示
        intro = QLabel("AI助手可帮助您生成、优化和解释策略代码")
        intro.setStyleSheet(f"""
            color: {Colors.TEXT_MUTED};
            font-size: 12px;
        """)
        intro.setWordWrap(True)
        layout.addWidget(intro)
        
        # AI功能按钮
        ai_actions = [
            ("🤖 生成策略", "根据描述生成策略代码", self.ai_generate),
            ("⚡ 优化代码", "分析并优化现有代码", self.ai_optimize),
            ("📖 解释策略", "解释策略逻辑", self.ai_explain),
            ("🔍 因子挖掘", "挖掘有效量化因子", self.ai_factor),
        ]
        
        for text, desc, callback in ai_actions:
            btn_widget = QFrame()
            btn_widget.setStyleSheet(f"""
                QFrame {{
                    background-color: {Colors.BG_SECONDARY};
                    border: 1px solid {Colors.BORDER_PRIMARY};
                    border-radius: 8px;
                }}
                QFrame:hover {{
                    border-color: {Colors.PRIMARY}88;
                }}
            """)
            btn_widget.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_widget.mousePressEvent = lambda e, c=callback: c()
            
            btn_layout = QVBoxLayout(btn_widget)
            btn_layout.setContentsMargins(16, 12, 16, 12)
            btn_layout.setSpacing(4)
            
            title = QLabel(text)
            title.setStyleSheet(f"""
                font-size: 14px;
                font-weight: 600;
                color: {Colors.TEXT_PRIMARY};
            """)
            btn_layout.addWidget(title)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet(f"""
                font-size: 11px;
                color: {Colors.TEXT_MUTED};
            """)
            btn_layout.addWidget(desc_label)
            
            layout.addWidget(btn_widget)
        
        layout.addStretch()
        
        # 在Cursor中打开
        cursor_btn = QPushButton("📝 在Cursor中打开")
        cursor_btn.setStyleSheet(ButtonStyles.SECONDARY)
        cursor_btn.setFixedHeight(40)
        cursor_btn.clicked.connect(self.open_in_cursor)
        layout.addWidget(cursor_btn)
        
        return tab
    
    def create_version_tab(self) -> QWidget:
        """创建版本标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 版本列表
        self.version_list = QListWidget()
        self.version_list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
            }}
            QListWidget::item {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 12px;
                margin: 4px 0;
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY}22;
                border-color: {Colors.PRIMARY}88;
            }}
        """)
        
        # 示例版本
        versions = [
            ("v1.2.0", "当前版本", "2024-11-25"),
            ("v1.1.0", "添加止损逻辑", "2024-11-20"),
            ("v1.0.0", "初始版本", "2024-11-15"),
        ]
        
        for ver, desc, date in versions:
            item = QListWidgetItem(f"{ver}\n{desc}\n{date}")
            self.version_list.addItem(item)
        
        layout.addWidget(self.version_list)
        
        # 版本操作
        btn_layout = QHBoxLayout()
        
        save_ver_btn = QPushButton("保存版本")
        save_ver_btn.setStyleSheet(ButtonStyles.SECONDARY)
        btn_layout.addWidget(save_ver_btn)
        
        compare_btn = QPushButton("对比")
        compare_btn.setStyleSheet(ButtonStyles.SECONDARY)
        btn_layout.addWidget(compare_btn)
        
        layout.addLayout(btn_layout)
        
        return tab
    
    def load_strategies(self):
        """加载策略列表"""
        self.strategy_tree.clear()
        
        # 示例策略
        examples = QTreeWidgetItem(self.strategy_tree, ["📁 示例策略"])
        examples.setExpanded(True)
        
        strategies_dir = Path(__file__).parent.parent.parent / "strategies" / "examples"
        if strategies_dir.exists():
            for file in strategies_dir.glob("*.py"):
                if not file.name.startswith("__"):
                    item = QTreeWidgetItem(examples, [f"📄 {file.stem}"])
                    item.setData(0, Qt.ItemDataRole.UserRole, str(file))
        
        # 自定义策略
        custom = QTreeWidgetItem(self.strategy_tree, ["📁 自定义策略"])
        custom.setExpanded(True)
    
    def on_strategy_selected(self, item: QTreeWidgetItem, column: int):
        """策略选择事件"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path:
            self.load_strategy_file(file_path)
    
    def load_strategy_file(self, file_path: str):
        """加载策略文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            self.code_editor.setPlainText(code)
            self.current_strategy = file_path
            self.file_label.setText(Path(file_path).name)
            
        except Exception as e:
            logger.error(f"加载策略失败: {e}")
    
    def update_cursor_pos(self):
        """更新光标位置"""
        cursor = self.code_editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.cursor_label.setText(f"行 {line}, 列 {col}")
    
    def new_strategy(self):
        """新建策略"""
        template = '''# -*- coding: utf-8 -*-
"""
策略名称: 新策略
策略描述: 请填写策略描述
作者: 
版本: 1.0.0
"""
from strategies.base_strategy import BaseStrategy
import numpy as np


class NewStrategy(BaseStrategy):
    """新策略"""
    
    name = "new_strategy"
    version = "1.0"
    
    def __init__(self, **params):
        super().__init__()
        # 策略参数
        self.lookback = params.get('lookback', 20)
    
    def on_bar(self, date, data, portfolio):
        """
        每日执行的交易逻辑
        
        Args:
            date: 当前日期
            data: 行情数据 DataFrame
            portfolio: 投资组合对象
        
        Returns:
            list: 交易信号列表
        """
        signals = []
        
        # 在此实现交易逻辑
        
        return signals
'''
        self.code_editor.setPlainText(template)
        self.current_strategy = None
        self.file_label.setText("新策略.py *")
    
    def save_strategy(self):
        """保存策略"""
        if self.current_strategy:
            try:
                with open(self.current_strategy, 'w', encoding='utf-8') as f:
                    f.write(self.code_editor.toPlainText())
                QMessageBox.information(self, "成功", "策略已保存")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"保存失败: {e}")
        else:
            QMessageBox.information(self, "提示", "请先选择保存位置")
    
    def run_strategy(self):
        """运行回测"""
        if not self.current_strategy:
            QMessageBox.warning(self, "提示", "请先选择或保存策略")
            return
        
        strategy_name = Path(self.current_strategy).stem
        params = {
            'initial_capital': self.capital_input.value(),
            'commission_rate': self.fee_input.value(),
        }
        
        self.run_backtest.emit(strategy_name, params)
    
    def copy_code(self):
        """复制代码"""
        self.code_editor.selectAll()
        self.code_editor.copy()
        QMessageBox.information(self, "成功", "代码已复制到剪贴板")
    
    def ai_generate(self):
        """AI生成PTrade策略"""
        from core.ptrade_integration import get_ptrade_integration
        integration = get_ptrade_integration()
        
        prompt = integration.create_strategy_prompt(
            description="请在此描述您的策略需求",
            strategy_type="多因子选股策略",
            stock_pool="沪深300成分股",
            factors="动量因子、价值因子(PE/PB)、质量因子(ROE)",
            parameters="回看周期20天，单股持仓上限10%，止损8%"
        )
        self._show_prompt(prompt, "生成PTrade策略")
    
    def ai_optimize(self):
        """AI优化PTrade策略"""
        from core.ptrade_integration import get_ptrade_integration
        integration = get_ptrade_integration()
        
        code = self.code_editor.toPlainText()
        prompt = integration.create_optimization_prompt(
            code=code,
            total_return=0.15,
            max_drawdown=0.10,
            sharpe_ratio=1.5,
            optimization_goals="提高夏普比率到2.0以上，降低最大回撤到5%以内",
            available_factors="动量、价值(PE/PB)、质量(ROE/毛利率)、波动率、资金流"
        )
        self._show_prompt(prompt, "优化PTrade策略")
    
    def ai_explain(self):
        """AI解释策略"""
        code = self.code_editor.toPlainText()
        prompt = f"""请详细解释以下PTrade量化策略代码的逻辑：

## 策略代码
```python
{code}
```

请从以下方面进行解释：
1. 策略的核心思想
2. 选股逻辑和条件
3. 买入卖出信号
4. 风险控制机制
5. 参数含义和影响
6. 潜在的优化空间
"""
        self._show_prompt(prompt, "解释策略")
    
    def ai_factor(self):
        """AI多因子策略生成"""
        from core.ptrade_integration import get_ptrade_integration
        integration = get_ptrade_integration()
        
        prompt = integration.create_factor_strategy_prompt(
            factors=["动量因子(20日收益率)", "价值因子(PE分位数)", "质量因子(ROE)", "波动率因子"],
            weights={"动量因子": 0.3, "价值因子": 0.25, "质量因子": 0.25, "波动率因子": 0.2},
            selection_logic="综合评分前20名",
            rebalance_frequency="每周一开盘调仓",
            max_position=10,
            stop_loss=8,
            max_drawdown=15
        )
        self._show_prompt(prompt, "多因子策略")
    
    def _show_prompt(self, prompt: str, title: str):
        """显示提示词并复制到剪贴板"""
        # 保存到文件
        from core.ptrade_integration import get_ptrade_integration
        integration = get_ptrade_integration()
        file_path = integration.save_prompt_to_file(prompt, f"{title.replace(' ', '_')}.md")
        
        # 复制到剪贴板
        copied = integration.copy_to_clipboard(prompt)
        
        if copied:
            QMessageBox.information(self, title, 
                f"✅ Prompt已复制到剪贴板！\n\n"
                f"📁 同时保存到: {file_path}\n\n"
                f"请在Cursor中按 Ctrl+K 打开AI对话，粘贴使用。")
        else:
            QMessageBox.information(self, title, 
                f"📁 Prompt已保存到: {file_path}\n\n"
                f"请打开文件复制内容到Cursor中使用。")
    
    def open_in_cursor(self):
        """在Cursor中打开"""
        if self.current_strategy:
            import subprocess
            try:
                subprocess.Popen(['cursor', self.current_strategy])
                self.log_action(f"在Cursor中打开: {self.current_strategy}")
            except FileNotFoundError:
                # 尝试使用code命令
                try:
                    subprocess.Popen(['code', self.current_strategy])
                    self.log_action(f"在VS Code中打开: {self.current_strategy}")
                except:
                    QMessageBox.warning(self, "提示", "未找到Cursor或VS Code，请手动打开文件")
        else:
            QMessageBox.warning(self, "提示", "请先选择策略文件")
    
    def log_action(self, message: str):
        """记录操作日志"""
        logger.info(message)
