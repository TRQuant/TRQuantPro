# -*- coding: utf-8 -*-
"""
AI策略助手面板
多因子量化策略生成工具 - 支持PTrade/QMT/QuantConnect
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QComboBox, QTextEdit, QLineEdit,
    QSpinBox, QDoubleSpinBox, QTabWidget, QGridLayout,
    QGroupBox, QCheckBox, QMessageBox, QFileDialog,
    QSplitter, QListWidget, QListWidgetItem, QDialog,
    QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QClipboard
from pathlib import Path
from datetime import datetime
import json
import subprocess
import sys

from gui.styles.theme import Colors, Typography, ButtonStyles, CardStyles


class PromptTemplate:
    """Prompt模板数据结构"""
    
    def __init__(self, name: str, platform: str, description: str, 
                 template: str, variables: dict = None):
        self.name = name
        self.platform = platform
        self.description = description
        self.template = template
        self.variables = variables or {}
        self.created_at = datetime.now().isoformat()


class FactorConfigDialog(QDialog):
    """因子配置对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("因子配置")
        self.setMinimumSize(500, 400)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
            }}
            QLineEdit, QDoubleSpinBox {{
                background-color: {Colors.BG_TERTIARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
            }}
        """)
        
        self.factors = {}
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        
        # 因子列表
        factors_group = QGroupBox("因子定义")
        factors_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
            }}
        """)
        factors_layout = QGridLayout(factors_group)
        
        factor_definitions = [
            ("value", "价值因子", "过去一年平均ROE或1/PE"),
            ("growth", "成长因子", "最近四季度净利润同比增长率"),
            ("momentum", "动量因子", "过去60日收益率（剔除近5日）"),
            ("volatility", "波动因子", "过去60日收益率标准差"),
            ("quality", "质量因子", "ROA、毛利率、资产周转率"),
            ("liquidity", "流动性因子", "日均成交额、换手率"),
        ]
        
        self.factor_inputs = {}
        for i, (key, name, default) in enumerate(factor_definitions):
            label = QLabel(f"{name}:")
            input_field = QLineEdit(default)
            weight_spin = QDoubleSpinBox()
            weight_spin.setRange(0, 1)
            weight_spin.setSingleStep(0.05)
            weight_spin.setValue(0.2 if key != "volatility" else -0.15)
            weight_spin.setPrefix("权重: ")
            
            factors_layout.addWidget(label, i, 0)
            factors_layout.addWidget(input_field, i, 1)
            factors_layout.addWidget(weight_spin, i, 2)
            
            self.factor_inputs[key] = {
                "definition": input_field,
                "weight": weight_spin
            }
        
        layout.addWidget(factors_group)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_factors(self) -> dict:
        """获取因子配置"""
        result = {}
        for key, inputs in self.factor_inputs.items():
            result[key] = {
                "definition": inputs["definition"].text(),
                "weight": inputs["weight"].value()
            }
        return result


class AIAssistantPanel(QWidget):
    """AI策略助手面板"""
    
    strategy_generated = pyqtSignal(str, str)  # (strategy_code, platform)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_root = Path(__file__).parent.parent.parent
        self.prompts_dir = self.project_root / "prompts"
        self.strategies_dir = self.project_root / "strategies"
        
        self.init_ui()
        self.load_templates()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 使用滚动区域
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
        
        # === 标题区域 ===
        header = self._create_header()
        content_layout.addWidget(header)
        
        # === 使用说明 ===
        guide = self._create_guide_section()
        content_layout.addWidget(guide)
        
        # === 主要内容区域（左右分栏） ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {Colors.BORDER_PRIMARY};
                width: 2px;
            }}
        """)
        
        # 左侧：配置面板
        left_panel = self._create_config_panel()
        splitter.addWidget(left_panel)
        
        # 右侧：Prompt预览和输出
        right_panel = self._create_output_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([500, 700])
        content_layout.addWidget(splitter, 1)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _create_header(self) -> QFrame:
        """创建标题区域"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {Colors.SUCCESS}22, stop:1 {Colors.PRIMARY}11);
                border: 1px solid {Colors.SUCCESS}44;
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)
        
        title = QLabel("🤖 AI策略助手")
        title.setStyleSheet(f"""
            font-size: 24px;
            font-weight: 700;
            color: {Colors.TEXT_PRIMARY};
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("多因子量化策略生成工具 · 支持PTrade/QMT/QuantConnect · 自动保存到文件管理系统")
        subtitle.setStyleSheet(f"""
            font-size: 14px;
            color: {Colors.TEXT_TERTIARY};
        """)
        layout.addWidget(subtitle)
        
        return frame
    
    def _create_guide_section(self) -> QFrame:
        """创建使用说明区域"""
        frame = QFrame()
        frame.setStyleSheet(CardStyles.DEFAULT)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 标题
        title_layout = QHBoxLayout()
        title = QLabel("📖 使用说明")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {Colors.TEXT_PRIMARY};
        """)
        title_layout.addWidget(title)
        
        # 折叠按钮
        self.guide_toggle = QPushButton("收起 ▲")
        self.guide_toggle.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {Colors.PRIMARY};
                font-size: 12px;
            }}
        """)
        self.guide_toggle.clicked.connect(self._toggle_guide)
        title_layout.addWidget(self.guide_toggle)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # 说明内容
        self.guide_content = QLabel("""
<b>🎯 目标</b>：开发完整的多因子量化系统，根据特定市场和券商平台生成策略代码

<b>📋 工作流程</b>：
1️⃣ <b>选择平台</b> - 选择目标券商平台（PTrade/QMT/QuantConnect）
2️⃣ <b>配置因子</b> - 定义多因子模型参数（价值、成长、动量、波动等）
3️⃣ <b>设置参数</b> - 配置标的池、调仓周期、持仓数量、风控规则
4️⃣ <b>生成Prompt</b> - 系统自动生成完整的策略生成Prompt
5️⃣ <b>复制到Cursor</b> - 将Prompt复制到Cursor中，AI生成策略代码
6️⃣ <b>保存策略</b> - 将生成的代码保存到文件管理系统

<b>💡 提示</b>：
• 生成的Prompt已针对各平台API进行优化
• 策略代码会自动保存到 <code>strategies/{platform}/</code> 目录
• 可在Dashboard中查看和管理所有策略文件
        """)
        self.guide_content.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_SECONDARY};
            line-height: 1.8;
        """)
        self.guide_content.setWordWrap(True)
        self.guide_content.setTextFormat(Qt.TextFormat.RichText)
        layout.addWidget(self.guide_content)
        
        return frame
    
    def _toggle_guide(self):
        """切换说明显示"""
        if self.guide_content.isVisible():
            self.guide_content.hide()
            self.guide_toggle.setText("展开 ▼")
        else:
            self.guide_content.show()
            self.guide_toggle.setText("收起 ▲")
    
    def _create_config_panel(self) -> QFrame:
        """创建配置面板"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # === 平台选择 ===
        platform_group = QGroupBox("🎯 目标平台")
        platform_group.setStyleSheet(self._group_style())
        platform_layout = QVBoxLayout(platform_group)
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems([
            "PTrade (国金证券)",
            "QMT (国金证券)",
            "QuantConnect + IBKR (美股)",
            "本地回测 (JQQuant)"
        ])
        self.platform_combo.setStyleSheet(self._combo_style())
        self.platform_combo.currentTextChanged.connect(self._on_platform_changed)
        platform_layout.addWidget(self.platform_combo)
        
        layout.addWidget(platform_group)
        
        # === 标的池配置 ===
        universe_group = QGroupBox("📊 标的池配置")
        universe_group.setStyleSheet(self._group_style())
        universe_layout = QFormLayout(universe_group)
        
        self.universe_input = QComboBox()
        self.universe_input.setEditable(True)
        self.universe_input.addItems([
            "中证800成分股",
            "沪深300成分股",
            "中证500成分股",
            "创业板指成分股",
            "科创50成分股",
            "全市场（剔除ST）"
        ])
        self.universe_input.setStyleSheet(self._combo_style())
        universe_layout.addRow("标的池:", self.universe_input)
        
        self.exclude_st = QCheckBox("剔除ST/*ST股票")
        self.exclude_st.setChecked(True)
        self.exclude_st.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        universe_layout.addRow("", self.exclude_st)
        
        self.min_volume = QSpinBox()
        self.min_volume.setRange(0, 100000)
        self.min_volume.setValue(3000)
        self.min_volume.setSuffix(" 万")
        self.min_volume.setStyleSheet(self._spin_style())
        universe_layout.addRow("最低日均成交额:", self.min_volume)
        
        layout.addWidget(universe_group)
        
        # === 调仓配置 ===
        rebalance_group = QGroupBox("🔄 调仓配置")
        rebalance_group.setStyleSheet(self._group_style())
        rebalance_layout = QFormLayout(rebalance_group)
        
        self.rebalance_days = QSpinBox()
        self.rebalance_days.setRange(1, 252)
        self.rebalance_days.setValue(20)
        self.rebalance_days.setSuffix(" 交易日")
        self.rebalance_days.setStyleSheet(self._spin_style())
        rebalance_layout.addRow("调仓周期:", self.rebalance_days)
        
        self.max_holdings = QSpinBox()
        self.max_holdings.setRange(1, 100)
        self.max_holdings.setValue(30)
        self.max_holdings.setSuffix(" 只")
        self.max_holdings.setStyleSheet(self._spin_style())
        rebalance_layout.addRow("持仓数量:", self.max_holdings)
        
        self.target_position = QDoubleSpinBox()
        self.target_position.setRange(0, 100)
        self.target_position.setValue(80)
        self.target_position.setSuffix(" %")
        self.target_position.setStyleSheet(self._spin_style())
        rebalance_layout.addRow("目标仓位:", self.target_position)
        
        layout.addWidget(rebalance_group)
        
        # === 因子配置 ===
        factor_group = QGroupBox("🔬 因子配置")
        factor_group.setStyleSheet(self._group_style())
        factor_layout = QVBoxLayout(factor_group)
        
        # 因子权重快速设置
        weights_layout = QGridLayout()
        
        self.factor_weights = {}
        factors = [
            ("value", "价值", 0.25),
            ("growth", "成长", 0.25),
            ("momentum", "动量", 0.30),
            ("volatility", "波动", -0.20),
        ]
        
        for i, (key, name, default) in enumerate(factors):
            label = QLabel(f"{name}:")
            label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
            
            spin = QDoubleSpinBox()
            spin.setRange(-1, 1)
            spin.setSingleStep(0.05)
            spin.setValue(default)
            spin.setStyleSheet(self._spin_style())
            
            weights_layout.addWidget(label, i // 2, (i % 2) * 2)
            weights_layout.addWidget(spin, i // 2, (i % 2) * 2 + 1)
            
            self.factor_weights[key] = spin
        
        factor_layout.addLayout(weights_layout)
        
        # 高级因子配置按钮
        advanced_btn = QPushButton("⚙️ 高级因子配置")
        advanced_btn.setStyleSheet(ButtonStyles.SECONDARY)
        advanced_btn.clicked.connect(self._open_factor_config)
        factor_layout.addWidget(advanced_btn)
        
        layout.addWidget(factor_group)
        
        # === 风控配置 ===
        risk_group = QGroupBox("🛡️ 风控配置")
        risk_group.setStyleSheet(self._group_style())
        risk_layout = QFormLayout(risk_group)
        
        self.max_single_weight = QDoubleSpinBox()
        self.max_single_weight.setRange(1, 100)
        self.max_single_weight.setValue(8)
        self.max_single_weight.setSuffix(" %")
        self.max_single_weight.setStyleSheet(self._spin_style())
        risk_layout.addRow("单只最大权重:", self.max_single_weight)
        
        self.commission_rate = QDoubleSpinBox()
        self.commission_rate.setRange(0, 10)
        self.commission_rate.setDecimals(4)
        self.commission_rate.setValue(0.00025)
        self.commission_rate.setStyleSheet(self._spin_style())
        risk_layout.addRow("交易费率:", self.commission_rate)
        
        layout.addWidget(risk_group)
        
        # === 操作按钮 ===
        btn_layout = QHBoxLayout()
        
        generate_btn = QPushButton("🚀 生成Prompt")
        generate_btn.setStyleSheet(ButtonStyles.PRIMARY)
        generate_btn.setFixedHeight(44)
        generate_btn.clicked.connect(self._generate_prompt)
        btn_layout.addWidget(generate_btn)
        
        save_template_btn = QPushButton("💾 保存模板")
        save_template_btn.setStyleSheet(ButtonStyles.SECONDARY)
        save_template_btn.setFixedHeight(44)
        save_template_btn.clicked.connect(self._save_template)
        btn_layout.addWidget(save_template_btn)
        
        layout.addLayout(btn_layout)
        layout.addStretch()
        
        return frame
    
    def _create_output_panel(self) -> QFrame:
        """创建输出面板"""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_TERTIARY};
                border-radius: 12px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标签页
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                background-color: {Colors.BG_DARK};
            }}
            QTabBar::tab {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_MUTED};
                padding: 10px 20px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.BG_DARK};
                color: {Colors.PRIMARY};
                font-weight: 600;
            }}
        """)
        
        # === Prompt预览标签页 ===
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)
        prompt_layout.setContentsMargins(0, 12, 0, 0)
        
        self.prompt_preview = QTextEdit()
        self.prompt_preview.setReadOnly(True)
        self.prompt_preview.setPlaceholderText("点击「生成Prompt」后，这里将显示生成的Prompt内容...")
        self.prompt_preview.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_DARK};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: 8px;
                font-family: {Typography.FONT_MONO};
                font-size: 13px;
                padding: 16px;
            }}
        """)
        prompt_layout.addWidget(self.prompt_preview)
        
        # Prompt操作按钮
        prompt_btn_layout = QHBoxLayout()
        
        copy_prompt_btn = QPushButton("📋 复制Prompt")
        copy_prompt_btn.setStyleSheet(ButtonStyles.SECONDARY)
        copy_prompt_btn.clicked.connect(self._copy_prompt)
        prompt_btn_layout.addWidget(copy_prompt_btn)
        
        open_cursor_btn = QPushButton("🖥️ 在Cursor中打开")
        open_cursor_btn.setStyleSheet(ButtonStyles.PRIMARY)
        open_cursor_btn.clicked.connect(self._open_in_cursor)
        prompt_btn_layout.addWidget(open_cursor_btn)
        
        prompt_btn_layout.addStretch()
        prompt_layout.addLayout(prompt_btn_layout)
        
        tabs.addTab(prompt_tab, "📝 Prompt预览")
        
        # === 策略代码标签页 ===
        code_tab = QWidget()
        code_layout = QVBoxLayout(code_tab)
        code_layout.setContentsMargins(0, 12, 0, 0)
        
        code_hint = QLabel("💡 将AI生成的策略代码粘贴到下方，然后点击「保存策略」")
        code_hint.setStyleSheet(f"""
            font-size: 13px;
            color: {Colors.TEXT_MUTED};
            padding: 8px;
            background-color: {Colors.WARNING}22;
            border-radius: 6px;
        """)
        code_layout.addWidget(code_hint)
        
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("在Cursor中生成策略代码后，粘贴到这里...")
        self.code_editor.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_DARK};
                color: {Colors.TEXT_SECONDARY};
                border: none;
                border-radius: 8px;
                font-family: {Typography.FONT_MONO};
                font-size: 13px;
                padding: 16px;
            }}
        """)
        code_layout.addWidget(self.code_editor)
        
        # 策略操作按钮
        code_btn_layout = QHBoxLayout()
        
        # 策略名称输入
        name_label = QLabel("策略名称:")
        name_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        code_btn_layout.addWidget(name_label)
        
        self.strategy_name_input = QLineEdit()
        self.strategy_name_input.setPlaceholderText("my_multifactor_strategy")
        self.strategy_name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px;
                color: {Colors.TEXT_PRIMARY};
                min-width: 200px;
            }}
        """)
        code_btn_layout.addWidget(self.strategy_name_input)
        
        code_btn_layout.addStretch()
        
        save_code_btn = QPushButton("💾 保存策略到文件系统")
        save_code_btn.setStyleSheet(ButtonStyles.PRIMARY)
        save_code_btn.clicked.connect(self._save_strategy)
        code_btn_layout.addWidget(save_code_btn)
        
        code_layout.addLayout(code_btn_layout)
        
        tabs.addTab(code_tab, "💻 策略代码")
        
        # === 已保存模板标签页 ===
        templates_tab = QWidget()
        templates_layout = QVBoxLayout(templates_tab)
        templates_layout.setContentsMargins(0, 12, 0, 0)
        
        self.templates_list = QListWidget()
        self.templates_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {Colors.BG_DARK};
                border: none;
                border-radius: 8px;
                color: {Colors.TEXT_SECONDARY};
            }}
            QListWidget::item {{
                padding: 12px;
                border-bottom: 1px solid {Colors.BORDER_DARK};
            }}
            QListWidget::item:selected {{
                background-color: {Colors.PRIMARY}33;
                color: {Colors.PRIMARY};
            }}
        """)
        self.templates_list.itemDoubleClicked.connect(self._load_template)
        templates_layout.addWidget(self.templates_list)
        
        tabs.addTab(templates_tab, "📁 已保存模板")
        
        layout.addWidget(tabs)
        
        return frame
    
    def _group_style(self) -> str:
        return f"""
            QGroupBox {{
                font-weight: 600;
                font-size: 14px;
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                margin-top: 16px;
                padding-top: 16px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
            }}
        """
    
    def _combo_style(self) -> str:
        return f"""
            QComboBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 8px 12px;
                color: {Colors.TEXT_PRIMARY};
                min-height: 20px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY}44;
            }}
        """
    
    def _spin_style(self) -> str:
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 6px;
                padding: 6px 10px;
                color: {Colors.TEXT_PRIMARY};
                min-height: 20px;
            }}
        """
    
    def load_templates(self):
        """加载已保存的模板"""
        self.templates_list.clear()
        templates_file = self.prompts_dir / "saved_templates.json"
        
        if templates_file.exists():
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
                    for t in templates:
                        item = QListWidgetItem(f"📄 {t['name']} ({t['platform']})")
                        item.setData(Qt.ItemDataRole.UserRole, t)
                        self.templates_list.addItem(item)
            except Exception as e:
                print(f"加载模板失败: {e}")
        
        # 添加内置模板
        builtin_templates = [
            ("多因子Alpha策略 (PTrade)", "PTrade"),
            ("动量反转策略 (QMT)", "QMT"),
            ("价值成长组合 (QuantConnect)", "QuantConnect"),
        ]
        
        for name, platform in builtin_templates:
            item = QListWidgetItem(f"📌 {name}")
            item.setData(Qt.ItemDataRole.UserRole, {
                "name": name,
                "platform": platform,
                "builtin": True
            })
            self.templates_list.addItem(item)
    
    def _on_platform_changed(self, platform: str):
        """平台切换时更新UI"""
        # 可以根据平台调整默认参数
        pass
    
    def _open_factor_config(self):
        """打开高级因子配置"""
        dialog = FactorConfigDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            factors = dialog.get_factors()
            # 更新因子权重
            for key, data in factors.items():
                if key in self.factor_weights:
                    self.factor_weights[key].setValue(data["weight"])
    
    def _generate_prompt(self):
        """生成Prompt"""
        platform_map = {
            "PTrade (国金证券)": "PTrade",
            "QMT (国金证券)": "QMT",
            "QuantConnect + IBKR (美股)": "QuantConnect",
            "本地回测 (JQQuant)": "JQQuant"
        }
        
        platform = platform_map.get(self.platform_combo.currentText(), "PTrade")
        
        # 构建Prompt
        prompt = self._build_prompt(platform)
        
        # 显示在预览区
        self.prompt_preview.setPlainText(prompt)
        
        # 自动设置策略名称
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.strategy_name_input.setText(f"mf_strategy_{platform.lower()}_{timestamp}")
    
    def _build_prompt(self, platform: str) -> str:
        """构建完整的Prompt"""
        
        # 获取配置
        universe = self.universe_input.currentText()
        exclude_st = self.exclude_st.isChecked()
        min_vol = self.min_volume.value()
        rebalance = self.rebalance_days.value()
        holdings = self.max_holdings.value()
        target_pos = self.target_position.value()
        max_single = self.max_single_weight.value()
        commission = self.commission_rate.value()
        
        # 因子权重
        weights = {k: v.value() for k, v in self.factor_weights.items()}
        
        # 根据平台生成不同的Prompt
        if platform == "PTrade":
            prompt = self._build_ptrade_prompt(
                universe, exclude_st, min_vol, rebalance, holdings,
                target_pos, max_single, commission, weights
            )
        elif platform == "QMT":
            prompt = self._build_qmt_prompt(
                universe, exclude_st, min_vol, rebalance, holdings,
                target_pos, max_single, commission, weights
            )
        elif platform == "QuantConnect":
            prompt = self._build_quantconnect_prompt(
                universe, exclude_st, min_vol, rebalance, holdings,
                target_pos, max_single, commission, weights
            )
        else:
            prompt = self._build_jqquant_prompt(
                universe, exclude_st, min_vol, rebalance, holdings,
                target_pos, max_single, commission, weights
            )
        
        return prompt
    
    def _build_ptrade_prompt(self, universe, exclude_st, min_vol, rebalance,
                             holdings, target_pos, max_single, commission, weights) -> str:
        """构建PTrade平台Prompt"""
        
        exclude_text = "剔除ST、*ST，以及" if exclude_st else ""
        
        return f"""# 多因子策略生成请求 - PTrade平台

## 角色设定
你是一名专门为中国A股市场、基于恒生PTrade平台编写Python策略的量化工程师。

## 任务
请根据以下多因子选股模型，生成一份可在PTrade Python策略环境中直接运行的完整策略代码。

## 1. 标的池与基本设定

- **标的池**：{universe}；{exclude_text}近60日日均成交额低于{min_vol}万的股票
- **回测频率**：日频（使用日线收盘价进行因子计算与调仓）
- **调仓周期**：每{rebalance}个交易日调仓一次
- **持仓数量**：每次持有{holdings}只股票，多头等权

## 2. 因子定义

请实现以下因子，并为每个因子标准化（z-score）：

- **价值因子**（权重{weights['value']:.2f}）：过去一年平均ROE或1/PE
- **成长因子**（权重{weights['growth']:.2f}）：最近四个财报季度净利润同比增长率
- **动量因子**（权重{weights['momentum']:.2f}）：过去60个交易日收益率，剔除最近5日的短期波动
- **波动因子**（权重{weights['volatility']:.2f}）：过去60日收益率标准差（作为风险惩罚项）

## 3. 因子合成与打分

总评分 = {weights['value']:.2f}×价值因子 + {weights['growth']:.2f}×成长因子 + {weights['momentum']:.2f}×动量因子 + ({weights['volatility']:.2f})×波动因子

每次调仓时：
1. 在标的池内计算上述因子并打分
2. 按评分从高到低排序，选取前{holdings}只股票
3. 组合等权分配

## 4. 交易与风控规则

- 单个标的最大持仓权重：不超过组合市值的{max_single}%
- 总仓位控制：目标总仓位{target_pos}%，剩余{100-target_pos}%现金
- 交易费用：买卖手续费{commission*10000:.1f}%%
- 换手约束：尽量保留前次高分股票，避免过度换手

## 5. PTrade接口要求

使用PTrade标准接口：
- `initialize(context)` - 初始化
- `before_trading_start(context)` - 盘前处理
- `handle_data(context, data)` - 盘中处理
- `order_target_percent(security, pct)` - 调仓到目标比例
- `get_price()`, `get_fundamentals()`, `get_index_stocks()`

## 6. 输出要求

- 生成完整的Python策略代码文件
- 在代码顶部集中定义所有参数
- 添加详细的中文注释
- 保证代码结构清晰，便于后续修改

请直接输出完整的Python代码，不要添加任何解释性文字。
"""
    
    def _build_qmt_prompt(self, universe, exclude_st, min_vol, rebalance,
                          holdings, target_pos, max_single, commission, weights) -> str:
        """构建QMT平台Prompt"""
        
        exclude_text = "剔除ST、*ST，以及" if exclude_st else ""
        
        return f"""# 多因子策略生成请求 - QMT平台 (xtquant)

## 角色设定
你是一名专门为中国A股市场、基于迅投QMT平台（使用xtquant库）编写Python策略的量化工程师。

## 任务
请根据以下多因子选股模型，生成一份可在QMT miniQMT环境中运行的完整策略代码。

## 1. 标的池与基本设定

- **标的池**：{universe}；{exclude_text}近60日日均成交额低于{min_vol}万的股票
- **调仓周期**：每{rebalance}个交易日调仓一次
- **持仓数量**：每次持有{holdings}只股票

## 2. 因子定义（z-score标准化）

- **价值因子**（权重{weights['value']:.2f}）：ROE或1/PE
- **成长因子**（权重{weights['growth']:.2f}）：净利润同比增长率
- **动量因子**（权重{weights['momentum']:.2f}）：过去60日收益率
- **波动因子**（权重{weights['volatility']:.2f}）：收益率标准差

## 3. 风控规则

- 单只最大权重：{max_single}%
- 目标仓位：{target_pos}%
- 交易费率：{commission*10000:.1f}%%

## 4. QMT/xtquant接口

使用xtquant库标准接口：
```python
from xtquant import xtdata
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount

# 数据获取
xtdata.get_market_data()
xtdata.get_stock_list_in_sector()

# 交易
trader.order_stock()
trader.order_target_percent()
```

## 5. 输出要求

- 生成完整的Python策略代码
- 包含数据订阅、因子计算、信号生成、下单执行
- 添加详细中文注释

请直接输出完整的Python代码。
"""
    
    def _build_quantconnect_prompt(self, universe, exclude_st, min_vol, rebalance,
                                   holdings, target_pos, max_single, commission, weights) -> str:
        """构建QuantConnect平台Prompt"""
        
        return f"""# Multi-Factor Strategy Generation - QuantConnect Platform

## Role
You are a quantitative engineer specializing in developing Python strategies for the QuantConnect platform with Interactive Brokers.

## Task
Generate a complete multi-factor equity strategy that can run on QuantConnect's LEAN engine.

## 1. Universe Selection

- **Universe**: US Large Cap stocks (similar to S&P 500)
- **Filters**: Minimum daily volume > ${min_vol * 10000}, exclude penny stocks
- **Rebalance**: Every {rebalance} trading days
- **Holdings**: Top {holdings} stocks

## 2. Factor Definitions (z-score normalized)

- **Value Factor** (weight {weights['value']:.2f}): P/E ratio inverse, P/B ratio inverse
- **Growth Factor** (weight {weights['growth']:.2f}): Revenue growth, EPS growth
- **Momentum Factor** (weight {weights['momentum']:.2f}): 60-day returns excluding last 5 days
- **Volatility Factor** (weight {weights['volatility']:.2f}): 60-day return standard deviation (penalty)

## 3. Risk Management

- Max single position: {max_single}%
- Target exposure: {target_pos}%
- Commission: ${commission * 100:.4f} per share

## 4. QuantConnect Framework

Use QuantConnect's standard structure:
```python
class MultiFactorAlgorithm(QCAlgorithm):
    def Initialize(self):
        # Setup
    def OnData(self, data):
        # Signal generation
    def Rebalance(self):
        # Portfolio rebalancing
```

## 5. Output Requirements

- Complete Python algorithm file
- Use QuantConnect's data and trading APIs
- Include detailed comments
- Follow QuantConnect best practices

Output the complete Python code only.
"""
    
    def _build_jqquant_prompt(self, universe, exclude_st, min_vol, rebalance,
                              holdings, target_pos, max_single, commission, weights) -> str:
        """构建JQQuant本地回测Prompt"""
        
        exclude_text = "剔除ST、*ST，以及" if exclude_st else ""
        
        return f"""# 多因子策略生成请求 - JQQuant本地回测

## 任务
请根据以下多因子选股模型，生成一份可在JQQuant本地回测系统中运行的策略代码。

## 1. 标的池配置

- **标的池**：{universe}；{exclude_text}近60日日均成交额低于{min_vol}万的股票
- **调仓周期**：每{rebalance}个交易日
- **持仓数量**：{holdings}只股票

## 2. 因子定义

- 价值因子（权重{weights['value']:.2f}）
- 成长因子（权重{weights['growth']:.2f}）
- 动量因子（权重{weights['momentum']:.2f}）
- 波动因子（权重{weights['volatility']:.2f}）

## 3. 风控配置

- 单只最大权重：{max_single}%
- 目标仓位：{target_pos}%
- 交易费率：{commission*10000:.1f}%%

## 4. JQQuant框架

继承BaseStrategy基类：
```python
from strategies.base_strategy import BaseStrategy

class MultiFactorStrategy(BaseStrategy):
    def __init__(self, params):
        super().__init__(params)
    
    def generate_signals(self, date, data):
        # 返回信号字典
        return signals
```

## 5. 输出要求

- 生成完整的策略类代码
- 兼容JQQuant回测引擎
- 添加中文注释

请直接输出完整的Python代码。
"""
    
    def _copy_prompt(self):
        """复制Prompt到剪贴板"""
        prompt = self.prompt_preview.toPlainText()
        if prompt:
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt)
            QMessageBox.information(self, "已复制", "Prompt已复制到剪贴板！\n\n请在Cursor中粘贴并让AI生成策略代码。")
    
    def _open_in_cursor(self):
        """在Cursor中打开"""
        prompt = self.prompt_preview.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "提示", "请先生成Prompt")
            return
        
        # 保存Prompt到临时文件
        temp_file = self.prompts_dir / "current_prompt.md"
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        try:
            # 尝试用Cursor打开
            subprocess.Popen(['cursor', str(temp_file)])
            QMessageBox.information(
                self, "已打开",
                "Prompt文件已在Cursor中打开！\n\n"
                "请在Cursor中：\n"
                "1. 选中Prompt内容\n"
                "2. 使用Ctrl+K或Cmd+K调用AI\n"
                "3. 生成策略代码后复制回本工具保存"
            )
        except FileNotFoundError:
            # Cursor不可用，复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(prompt)
            QMessageBox.information(
                self, "已复制",
                "Cursor未安装或不在PATH中。\n\n"
                "Prompt已复制到剪贴板，请手动粘贴到Cursor中。"
            )
    
    def _save_template(self):
        """保存当前配置为模板"""
        name, ok = QMessageBox.getText(
            self, "保存模板", "请输入模板名称:",
            QLineEdit.EchoMode.Normal, "我的多因子策略"
        ) if hasattr(QMessageBox, 'getText') else (None, False)
        
        # 简化处理
        name = f"模板_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        platform_map = {
            "PTrade (国金证券)": "PTrade",
            "QMT (国金证券)": "QMT",
            "QuantConnect + IBKR (美股)": "QuantConnect",
            "本地回测 (JQQuant)": "JQQuant"
        }
        
        template = {
            "name": name,
            "platform": platform_map.get(self.platform_combo.currentText(), "PTrade"),
            "created_at": datetime.now().isoformat(),
            "config": {
                "universe": self.universe_input.currentText(),
                "exclude_st": self.exclude_st.isChecked(),
                "min_volume": self.min_volume.value(),
                "rebalance_days": self.rebalance_days.value(),
                "max_holdings": self.max_holdings.value(),
                "target_position": self.target_position.value(),
                "max_single_weight": self.max_single_weight.value(),
                "commission_rate": self.commission_rate.value(),
                "weights": {k: v.value() for k, v in self.factor_weights.items()}
            }
        }
        
        # 保存到文件
        templates_file = self.prompts_dir / "saved_templates.json"
        templates_file.parent.mkdir(parents=True, exist_ok=True)
        
        templates = []
        if templates_file.exists():
            try:
                with open(templates_file, 'r', encoding='utf-8') as f:
                    templates = json.load(f)
            except:
                pass
        
        templates.append(template)
        
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(templates, f, ensure_ascii=False, indent=2)
        
        # 刷新列表
        self.load_templates()
        QMessageBox.information(self, "已保存", f"模板 '{name}' 已保存！")
    
    def _load_template(self, item: QListWidgetItem):
        """加载模板"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return
        
        if data.get("builtin"):
            QMessageBox.information(self, "内置模板", "这是内置模板，配置已预设。")
            return
        
        config = data.get("config", {})
        
        # 恢复配置
        if "universe" in config:
            self.universe_input.setCurrentText(config["universe"])
        if "exclude_st" in config:
            self.exclude_st.setChecked(config["exclude_st"])
        if "min_volume" in config:
            self.min_volume.setValue(config["min_volume"])
        if "rebalance_days" in config:
            self.rebalance_days.setValue(config["rebalance_days"])
        if "max_holdings" in config:
            self.max_holdings.setValue(config["max_holdings"])
        if "target_position" in config:
            self.target_position.setValue(config["target_position"])
        if "max_single_weight" in config:
            self.max_single_weight.setValue(config["max_single_weight"])
        if "commission_rate" in config:
            self.commission_rate.setValue(config["commission_rate"])
        
        if "weights" in config:
            for k, v in config["weights"].items():
                if k in self.factor_weights:
                    self.factor_weights[k].setValue(v)
        
        QMessageBox.information(self, "已加载", f"模板 '{data['name']}' 已加载！")
    
    def _save_strategy(self):
        """保存策略代码到文件系统"""
        code = self.code_editor.toPlainText().strip()
        if not code:
            QMessageBox.warning(self, "提示", "请先粘贴策略代码")
            return
        
        name = self.strategy_name_input.text().strip()
        if not name:
            name = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 确保文件名合法
        name = "".join(c for c in name if c.isalnum() or c in "_-")
        
        # 根据平台选择保存目录
        platform_map = {
            "PTrade (国金证券)": "ptrade",
            "QMT (国金证券)": "qmt",
            "QuantConnect + IBKR (美股)": "quantconnect",
            "本地回测 (JQQuant)": "examples"
        }
        
        platform_dir = platform_map.get(self.platform_combo.currentText(), "examples")
        save_dir = self.strategies_dir / platform_dir
        save_dir.mkdir(parents=True, exist_ok=True)
        
        save_path = save_dir / f"{name}.py"
        
        # 检查文件是否存在
        if save_path.exists():
            reply = QMessageBox.question(
                self, "文件已存在",
                f"文件 {save_path.name} 已存在，是否覆盖？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
        
        # 保存文件
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # 发送信号
        self.strategy_generated.emit(str(save_path), platform_dir)
        
        QMessageBox.information(
            self, "保存成功",
            f"策略已保存到：\n{save_path}\n\n"
            f"可在Dashboard的「策略代码」页面查看和管理。"
        )

