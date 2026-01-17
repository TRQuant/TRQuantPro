# -*- coding: utf-8 -*-
"""
轩辕剑灵开发助手面板（可选GUI）

通过MCPClient调用轩辕剑灵MCP服务器工具

使用方式:
    可选添加到主窗口，通过MCP客户端调用MCP工具
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox, QSplitter, QDialog, QFormLayout, QDialogButtonBox,
    QComboBox, QPlainTextEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QMenu
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QClipboard, QFont
from pathlib import Path
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class XuanyuanWorker(QThread):
    """MCP工具调用工作线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, tool_name: str, arguments: dict, parent=None):
        super().__init__(parent)
        self.tool_name = tool_name
        self.arguments = arguments
    
    def run(self):
        try:
            from core.mcp import get_mcp_client
            client = get_mcp_client()
            result = client.call(self.tool_name, self.arguments)
            if result.success:
                self.finished.emit(result.data)
            else:
                self.error.emit(result.error or "未知错误")
        except Exception as e:
            self.error.emit(str(e))


class TemplateDialog(QDialog):
    """模板创建/编辑对话框"""
    
    def __init__(self, parent=None, template_data=None):
        super().__init__(parent)
        self.template_data = template_data
        self.setWindowTitle("创建模板" if template_data is None else "编辑模板")
        self.setMinimumSize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        form = QFormLayout()
        form.setSpacing(12)
        
        # 名称
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("输入模板名称")
        self.name_edit.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.name_edit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.name_edit.setFont(font)
        if self.template_data:
            self.name_edit.setText(self.template_data.get("name", ""))
        form.addRow("名称:", self.name_edit)
        
        # 分类
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "system", "code_generation", "error_handling", 
            "code_review", "refactoring", "documentation", "general"
        ])
        if self.template_data:
            category = self.template_data.get("category", "general")
            index = self.category_combo.findText(category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        form.addRow("分类:", self.category_combo)
        
        # 内容
        self.content_edit = QPlainTextEdit()
        self.content_edit.setPlaceholderText("输入模板内容...")
        self.content_edit.setMinimumHeight(200)
        # 启用中文输入法支持
        self.content_edit.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.content_edit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.content_edit.setFont(font)
        if self.template_data:
            self.content_edit.setPlainText(self.template_data.get("content", ""))
        form.addRow("内容:", self.content_edit)
        
        # 标签
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("多个标签用逗号分隔，如: python, refactoring, best-practice")
        self.tags_edit.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.tags_edit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.tags_edit.setFont(font)
        if self.template_data:
            tags = self.template_data.get("tags", [])
            self.tags_edit.setText(", ".join(tags))
        form.addRow("标签:", self.tags_edit)
        
        # 描述
        self.description_edit = QPlainTextEdit()
        self.description_edit.setPlaceholderText("输入模板描述（可选）")
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.description_edit.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.description_edit.setFont(font)
        if self.template_data:
            self.description_edit.setPlainText(self.template_data.get("description", ""))
        form.addRow("描述:", self.description_edit)
        
        layout.addLayout(form)
        
        # 按钮
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def validate_and_accept(self):
        """验证并接受"""
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "验证失败", "请输入模板名称")
            return
        if not self.content_edit.toPlainText().strip():
            QMessageBox.warning(self, "验证失败", "请输入模板内容")
            return
        self.accept()
    
    def get_template_data(self):
        """获取模板数据"""
        tags_str = self.tags_edit.text().strip()
        tags = [t.strip() for t in tags_str.split(",") if t.strip()] if tags_str else []
        
        return {
            "name": self.name_edit.text().strip(),
            "content": self.content_edit.toPlainText().strip(),
            "category": self.category_combo.currentText(),
            "tags": tags,
            "description": self.description_edit.toPlainText().strip()
        }


class XuanyuanAssistantPanel(QWidget):
    """轩辕剑灵开发助手面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workers = []  # 跟踪所有工作线程
        self.current_templates = []  # 当前模板列表
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("🐉 轩辕剑灵开发助手")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 提示词管理标签页
        self.prompt_tab = self.create_prompt_tab()
        self.tabs.addTab(self.prompt_tab, "提示词管理")
        
        # 错误处理标签页
        self.error_tab = self.create_error_tab()
        self.tabs.addTab(self.error_tab, "错误处理")
        
        # 命令助手标签页
        self.command_tab = self.create_command_tab()
        self.tabs.addTab(self.command_tab, "命令助手")
        
        # 记忆管理标签页
        self.memory_tab = self.create_memory_tab()
        self.tabs.addTab(self.memory_tab, "记忆管理")
        
        # Prompt优化标签页（核心功能）
        self.optimize_tab = self.create_optimize_tab()
        self.tabs.addTab(self.optimize_tab, "🚀 智能优化")
        
        # 默认选中优化标签页
        self.tabs.setCurrentIndex(4)
        
        layout.addWidget(self.tabs)
    
    def create_prompt_tab(self) -> QWidget:
        """创建提示词管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.btn_list_templates = QPushButton("📋 刷新列表")
        self.btn_extract_prompts = QPushButton("📥 提取Prompt")
        self.btn_create_template = QPushButton("➕ 创建模板")
        self.btn_edit_template = QPushButton("✏️ 编辑")
        self.btn_delete_template = QPushButton("🗑️ 删除")
        self.btn_copy_template = QPushButton("📋 复制内容")
        
        self.btn_edit_template.setEnabled(False)
        self.btn_delete_template.setEnabled(False)
        self.btn_copy_template.setEnabled(False)
        
        toolbar.addWidget(self.btn_list_templates)
        toolbar.addWidget(self.btn_extract_prompts)
        toolbar.addWidget(self.btn_create_template)
        toolbar.addWidget(self.btn_edit_template)
        toolbar.addWidget(self.btn_delete_template)
        toolbar.addWidget(self.btn_copy_template)
        toolbar.addStretch()
        
        # 分类筛选
        toolbar.addWidget(QLabel("分类:"))
        self.category_filter = QComboBox()
        self.category_filter.addItems(["全部", "system", "code_generation", "error_handling", 
                                       "code_review", "refactoring", "documentation", "general"])
        toolbar.addWidget(self.category_filter)
        
        layout.addLayout(toolbar)
        
        # 主区域：使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：模板列表（使用表格）
        self.template_table = QTableWidget()
        self.template_table.setColumnCount(4)
        self.template_table.setHorizontalHeaderLabels(["名称", "分类", "标签", "创建时间"])
        self.template_table.horizontalHeader().setStretchLastSection(True)
        self.template_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.template_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.template_table.setAlternatingRowColors(True)
        self.template_table.itemSelectionChanged.connect(self.on_template_selection_changed)
        self.template_table.itemDoubleClicked.connect(self.on_template_double_clicked)
        splitter.addWidget(self.template_table)
        
        # 右侧：模板详情
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(10, 10, 10, 10)
        
        detail_label = QLabel("模板详情:")
        detail_label.setStyleSheet("font-weight: bold;")
        detail_layout.addWidget(detail_label)
        
        self.template_detail = QTextEdit()
        self.template_detail.setReadOnly(True)
        self.template_detail.setPlaceholderText("选择一个模板查看详情...")
        detail_layout.addWidget(self.template_detail)
        
        splitter.addWidget(detail_widget)
        splitter.setSizes([300, 400])
        
        layout.addWidget(splitter)
        
        # 连接信号
        self.btn_list_templates.clicked.connect(self.list_templates)
        self.btn_extract_prompts.clicked.connect(self.extract_prompts_from_logs)
        self.btn_create_template.clicked.connect(self.create_template)
        self.btn_edit_template.clicked.connect(self.edit_template)
        self.btn_delete_template.clicked.connect(self.delete_template)
        self.btn_copy_template.clicked.connect(self.copy_template_content)
        self.category_filter.currentTextChanged.connect(self.filter_templates)
        
        return widget
    
    def create_error_tab(self) -> QWidget:
        """创建错误处理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 错误输入
        error_input_layout = QHBoxLayout()
        error_input_layout.addWidget(QLabel("错误信息:"))
        self.error_input = QLineEdit()
        self.error_input.setPlaceholderText("输入错误信息...")
        error_input_layout.addWidget(self.error_input)
        self.btn_analyze_error = QPushButton("分析")
        error_input_layout.addWidget(self.btn_analyze_error)
        layout.addLayout(error_input_layout)
        
        # 结果显示
        self.error_result = QTextEdit()
        self.error_result.setReadOnly(True)
        layout.addWidget(self.error_result)
        
        # 连接信号
        self.btn_analyze_error.clicked.connect(self.analyze_error)
        
        return widget
    
    def create_command_tab(self) -> QWidget:
        """创建命令助手标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 命令输入
        command_input_layout = QHBoxLayout()
        command_input_layout.addWidget(QLabel("命令:"))
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("输入命令...")
        command_input_layout.addWidget(self.command_input)
        self.btn_explain_command = QPushButton("解释")
        command_input_layout.addWidget(self.btn_explain_command)
        layout.addLayout(command_input_layout)
        
        # 结果显示
        self.command_result = QTextEdit()
        self.command_result.setReadOnly(True)
        layout.addWidget(self.command_result)
        
        # 连接信号
        self.btn_explain_command.clicked.connect(self.explain_command)
        
        return widget
    
    def create_memory_tab(self) -> QWidget:
        """创建记忆管理标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 记忆操作
        memory_btn_layout = QHBoxLayout()
        self.btn_save_memory = QPushButton("保存上下文")
        self.btn_search_memory = QPushButton("搜索记忆")
        memory_btn_layout.addWidget(self.btn_save_memory)
        memory_btn_layout.addWidget(self.btn_search_memory)
        memory_btn_layout.addStretch()
        layout.addLayout(memory_btn_layout)
        
        # 结果显示
        self.memory_result = QTextEdit()
        self.memory_result.setReadOnly(True)
        layout.addWidget(self.memory_result)
        
        # 连接信号
        self.btn_save_memory.clicked.connect(self.save_memory)
        self.btn_search_memory.clicked.connect(self.search_memory)
        
        return widget
    
    def on_template_selection_changed(self):
        """模板选择改变"""
        selected = self.template_table.selectionModel().selectedRows()
        has_selection = len(selected) > 0
        
        self.btn_edit_template.setEnabled(has_selection)
        self.btn_delete_template.setEnabled(has_selection)
        self.btn_copy_template.setEnabled(has_selection)
        
        if has_selection:
            row = selected[0].row()
            self.show_template_detail(row)
    
    def on_template_double_clicked(self, item):
        """双击模板项"""
        self.edit_template()
    
    def show_template_detail(self, row):
        """显示模板详情"""
        if row < 0 or row >= len(self.current_templates):
            return
        
        template = self.current_templates[row]
        
        # 格式化显示
        detail_text = f"""名称: {template.get('name', 'N/A')}
分类: {template.get('category', 'N/A')}
标签: {', '.join(template.get('tags', [])) if template.get('tags') else '无'}
创建时间: {template.get('created_at', 'N/A')}
使用次数: {template.get('usage_count', 0)}
平均评分: {template.get('avg_rating', 0.0):.1f}

描述:
{template.get('description', '无描述')}

内容:
{template.get('content', '')}
"""
        self.template_detail.setPlainText(detail_text)
    
    def get_selected_template(self):
        """获取选中的模板"""
        selected = self.template_table.selectionModel().selectedRows()
        if not selected:
            return None
        row = selected[0].row()
        if row < 0 or row >= len(self.current_templates):
            return None
        return self.current_templates[row]
    
    def list_templates(self):
        """列出提示词模板"""
        category = self.category_filter.currentText()
        arguments = {}
        if category != "全部":
            arguments["category"] = category
        
        worker = XuanyuanWorker("xuanyuan.prompt.templates.list", arguments)
        worker.finished.connect(self.on_templates_listed)
        worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"列出模板失败: {err}"))
        worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        self.workers.append(worker)
        worker.start()
    
    def on_templates_listed(self, data):
        """模板列表加载完成"""
        if not data.get("success"):
            QMessageBox.warning(self, "错误", data.get("error", "未知错误"))
            return
        
        templates = data.get("templates", [])
        self.current_templates = templates
        
        # 更新表格
        self.template_table.setRowCount(len(templates))
        for row, template in enumerate(templates):
            self.template_table.setItem(row, 0, QTableWidgetItem(template.get("name", "")))
            self.template_table.setItem(row, 1, QTableWidgetItem(template.get("category", "")))
            tags_str = ", ".join(template.get("tags", [])) if template.get("tags") else ""
            self.template_table.setItem(row, 2, QTableWidgetItem(tags_str))
            
            # 格式化时间
            created_at = template.get("created_at", "")
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
            self.template_table.setItem(row, 3, QTableWidgetItem(created_at))
        
        self.template_table.resizeColumnsToContents()
        QMessageBox.information(self, "成功", f"已加载 {len(templates)} 个模板")
    
    def create_template(self):
        """创建模板"""
        dialog = TemplateDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            template_data = dialog.get_template_data()
            
            worker = XuanyuanWorker("xuanyuan.prompt.templates.create", template_data)
            worker.finished.connect(self.on_template_created)
            worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"创建模板失败: {err}"))
            worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            self.workers.append(worker)
            worker.start()
    
    def on_template_created(self, data):
        """模板创建完成"""
        if data.get("success"):
            QMessageBox.information(self, "成功", "模板创建成功！")
            self.list_templates()  # 刷新列表
        else:
            QMessageBox.warning(self, "错误", data.get("error", "创建失败"))
    
    def edit_template(self):
        """编辑模板"""
        template = self.get_selected_template()
        if not template:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        dialog = TemplateDialog(self, template_data=template)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            template_data = dialog.get_template_data()
            template_data["template_id"] = template.get("id")
            
            worker = XuanyuanWorker("xuanyuan.prompt.templates.update", template_data)
            worker.finished.connect(self.on_template_updated)
            worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"更新模板失败: {err}"))
            worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            self.workers.append(worker)
            worker.start()
    
    def on_template_updated(self, data):
        """模板更新完成"""
        if data.get("success"):
            QMessageBox.information(self, "成功", "模板更新成功！")
            self.list_templates()  # 刷新列表
        else:
            QMessageBox.warning(self, "错误", data.get("error", "更新失败"))
    
    def delete_template(self):
        """删除模板"""
        template = self.get_selected_template()
        if not template:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        reply = QMessageBox.question(
            self, "确认删除", 
            f"确定要删除模板 '{template.get('name')}' 吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 注意：MCP工具中可能没有delete，需要检查
            # 暂时使用update来标记删除，或者提示用户
            QMessageBox.information(self, "提示", "删除功能需要MCP服务器支持，请检查xuanyuan.prompt.templates.delete工具")
    
    def extract_prompts_from_logs(self):
        """从开发记录提取prompt"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QSpinBox, QListWidget, QMessageBox
        from PyQt6.QtCore import Qt
        
        # 创建提取对话框
        dialog = QDialog(self)
        dialog.setWindowTitle("从开发记录提取Prompt")
        dialog.setMinimumSize(700, 500)
        
        layout = QVBoxLayout(dialog)
        
        # 参数设置
        param_layout = QHBoxLayout()
        param_layout.addWidget(QLabel("数据源:"))
        source_combo = QComboBox()
        source_combo.addItems(["全部", "Prompts目录", "Cursor Rules", "开发日志"])
        param_layout.addWidget(source_combo)
        
        param_layout.addWidget(QLabel("最大数量:"))
        limit_spin = QSpinBox()
        limit_spin.setRange(1, 100)
        limit_spin.setValue(20)
        param_layout.addWidget(limit_spin)
        
        param_layout.addWidget(QLabel("最小长度:"))
        min_length_spin = QSpinBox()
        min_length_spin.setRange(10, 500)
        min_length_spin.setValue(30)
        param_layout.addWidget(min_length_spin)
        layout.addLayout(param_layout)
        
        # 提取按钮
        btn_extract = QPushButton("开始提取")
        layout.addWidget(btn_extract)
        
        # 结果显示
        result_list = QListWidget()
        result_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(QLabel("提取结果（可多选保存为模板）:"))
        layout.addWidget(result_list)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_save_selected = QPushButton("保存选中为模板")
        btn_save_selected.setEnabled(False)
        btn_close = QPushButton("关闭")
        btn_layout.addWidget(btn_save_selected)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_close)
        layout.addLayout(btn_layout)
        
        extracted_prompts = []  # 存储提取的结果
        
        def on_extract():
            """执行提取"""
            source_map = {
                "全部": "all",
                "Prompts目录": "prompts",
                "Cursor Rules": "cursor_rules",
                "开发日志": "devlog"
            }
            
            source = source_map.get(source_combo.currentText(), "all")
            limit = limit_spin.value()
            min_length = min_length_spin.value()
            
            btn_extract.setEnabled(False)
            btn_extract.setText("提取中...")
            result_list.clear()
            
            worker = XuanyuanWorker(
                'xuanyuan.prompt.extract_from_logs',
                {
                    'source': source,
                    'limit': limit,
                    'min_length': min_length
                }
            )
            
            def on_finished(result_data):
                btn_extract.setEnabled(True)
                btn_extract.setText("开始提取")
                
                if isinstance(result_data, dict) and result_data.get('success'):
                    prompts = result_data.get('prompts', [])
                    extracted_prompts.clear()
                    extracted_prompts.extend(prompts)
                    
                    result_list.clear()
                    for i, prompt in enumerate(prompts, 1):
                        content = prompt.get('content', '')[:100]
                        category = prompt.get('category', 'N/A')
                        item_text = f"[{category}] {content}..."
                        result_list.addItem(item_text)
                    
                    if prompts:
                        QMessageBox.information(dialog, "提取完成", f"成功提取 {len(prompts)} 个prompt")
                        btn_save_selected.setEnabled(True)
                    else:
                        QMessageBox.information(dialog, "提取完成", "未提取到符合条件的prompt")
                else:
                    error = result_data.get('error', '未知错误') if isinstance(result_data, dict) else str(result_data)
                    QMessageBox.warning(dialog, "提取失败", f"提取失败: {error}")
            
            worker.finished.connect(on_finished)
            worker.error.connect(lambda err: (
                btn_extract.setEnabled(True),
                btn_extract.setText("开始提取"),
                QMessageBox.warning(dialog, "错误", f"提取失败: {err}")
            ))
            worker.start()
            self.workers.append(worker)
            worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        
        def on_save_selected():
            """保存选中的prompt为模板"""
            selected_items = result_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(dialog, "提示", "请先选择要保存的prompt")
                return
            
            selected_indices = [result_list.row(item) for item in selected_items]
            saved_count = 0
            
            for idx in selected_indices:
                if 0 <= idx < len(extracted_prompts):
                    prompt_data = extracted_prompts[idx]
                    
                    # 使用创建模板的功能
                    worker = XuanyuanWorker(
                        'xuanyuan.prompt.templates.create',
                        {
                            'name': prompt_data.get('content', '')[:50] + "...",
                            'content': prompt_data.get('content', ''),
                            'category': prompt_data.get('category', 'general'),
                            'tags': prompt_data.get('tags', []),
                            'description': f"从{prompt_data.get('source', 'unknown')}提取"
                        }
                    )
                    
                    def on_template_created(result_data, idx=idx):
                        if isinstance(result_data, dict) and result_data.get('success'):
                            nonlocal saved_count
                            saved_count += 1
                            if saved_count == len(selected_indices):
                                QMessageBox.information(dialog, "保存完成", f"成功保存 {saved_count} 个模板")
                                self.list_templates()  # 刷新模板列表
                    
                    worker.finished.connect(on_template_created)
                    worker.start()
                    self.workers.append(worker)
                    worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
                    worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
            
            # 等待所有保存完成（简化处理，实际应该用更复杂的同步机制）
            dialog.accept()
        
        btn_extract.clicked.connect(on_extract)
        btn_save_selected.clicked.connect(on_save_selected)
        btn_close.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def copy_template_content(self):
        """复制模板内容"""
        template = self.get_selected_template()
        if not template:
            QMessageBox.warning(self, "提示", "请先选择一个模板")
            return
        
        content = template.get("content", "")
        if content:
            from PyQt6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, "成功", "模板内容已复制到剪贴板")
        else:
            QMessageBox.warning(self, "提示", "模板内容为空")
    
    def filter_templates(self, category):
        """筛选模板"""
        self.list_templates()
    
    def analyze_error(self):
        """分析错误"""
        error_msg = self.error_input.text()
        if not error_msg:
            QMessageBox.warning(self, "警告", "请输入错误信息")
            return
        
        worker = XuanyuanWorker("xuanyuan.error.analyze", {"error_message": error_msg})
        worker.finished.connect(lambda data: self.error_result.setPlainText(json.dumps(data, ensure_ascii=False, indent=2)))
        worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"分析错误失败: {err}"))
        worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        self.workers.append(worker)
        worker.start()
    
    def explain_command(self):
        """解释命令"""
        command = self.command_input.text()
        if not command:
            QMessageBox.warning(self, "警告", "请输入命令")
            return
        
        worker = XuanyuanWorker("xuanyuan.command.explain", {"command": command})
        worker.finished.connect(lambda data: self.command_result.setPlainText(json.dumps(data, ensure_ascii=False, indent=2)))
        worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"解释命令失败: {err}"))
        worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        self.workers.append(worker)
        worker.start()
    
    def save_memory(self):
        """保存上下文"""
        QMessageBox.information(self, "提示", "保存上下文功能：请在Cursor Chat中使用 xuanyuan.memory.save_context")
    
    def search_memory(self):
        """搜索记忆"""
        QMessageBox.information(self, "提示", "搜索记忆功能：请在Cursor Chat中使用 xuanyuan.memory.search")
    
    # ==================== Prompt智能优化 ====================
    
    def create_optimize_tab(self) -> QWidget:
        """创建Prompt智能优化标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # 标题说明
        header = QLabel("🚀 智能Prompt优化器")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        layout.addWidget(header)
        
        desc = QLabel("根据Cursor方法论，智能生成结构化Prompt（目标、约束、范围、验收标准）")
        desc.setStyleSheet("color: #666; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # 输入区域
        input_group = QVBoxLayout()
        input_group.setSpacing(12)  # 增加间距
        
        # 任务描述
        task_label = QLabel("📝 任务描述（必填）:")
        task_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        input_group.addWidget(task_label)
        self.task_input = QPlainTextEdit()
        self.task_input.setPlaceholderText("描述你要实现的功能或解决的问题...\n例如：实现用户登录功能，使用JWT认证")
        self.task_input.setMinimumHeight(80)
        self.task_input.setMaximumHeight(120)
        self.task_input.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.task_input.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.task_input.setFont(font)
        input_group.addWidget(self.task_input)
        
        # 上下文信息
        context_label = QLabel("📂 上下文信息（可选）:")
        context_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        input_group.addWidget(context_label)
        self.context_input = QPlainTextEdit()
        self.context_input.setPlaceholderText("相关技术栈、文件、模块等...\n例如：Python Flask项目，已有用户模型")
        self.context_input.setMinimumHeight(60)
        self.context_input.setMaximumHeight(80)
        self.context_input.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.context_input.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.context_input.setFont(font)
        input_group.addWidget(self.context_input)
        
        # 原始Prompt（用于优化模式）
        original_label = QLabel("📄 原始Prompt（可选，用于优化已有prompt）:")
        original_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        input_group.addWidget(original_label)
        self.original_prompt_input = QPlainTextEdit()
        self.original_prompt_input.setPlaceholderText("如果要优化已有的prompt，请粘贴在这里...")
        self.original_prompt_input.setMinimumHeight(60)
        self.original_prompt_input.setMaximumHeight(80)
        self.original_prompt_input.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.original_prompt_input.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.original_prompt_input.setFont(font)
        input_group.addWidget(self.original_prompt_input)
        
        # Prompt类型选择
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("📌 Prompt类型:"))
        self.prompt_type_combo = QComboBox()
        self.prompt_type_combo.addItems([
            "feature_development - 新功能开发",
            "bug_fix - Bug修复",
            "refactoring - 代码重构",
            "code_review - 代码审查",
            "testing - 测试编写",
            "documentation - 文档编写",
            "strategy_development - 策略开发"
        ])
        self.prompt_type_combo.setMinimumWidth(250)
        type_row.addWidget(self.prompt_type_combo)
        type_row.addStretch()
        input_group.addLayout(type_row)
        
        layout.addLayout(input_group)
        
        # 操作按钮
        btn_row = QHBoxLayout()
        
        self.btn_optimize = QPushButton("🔮 生成/优化 Prompt")
        self.btn_optimize.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.btn_optimize.clicked.connect(self.optimize_prompt)
        btn_row.addWidget(self.btn_optimize)
        
        self.btn_copy_to_cursor = QPushButton("📋 复制到剪贴板")
        self.btn_copy_to_cursor.setEnabled(False)
        self.btn_copy_to_cursor.clicked.connect(self.copy_optimized_to_clipboard)
        btn_row.addWidget(self.btn_copy_to_cursor)
        
        self.btn_open_cursor = QPushButton("🚀 发送到Cursor")
        self.btn_open_cursor.setEnabled(False)
        self.btn_open_cursor.clicked.connect(self.send_to_cursor)
        btn_row.addWidget(self.btn_open_cursor)
        
        btn_row.addStretch()
        layout.addLayout(btn_row)
        
        # 结果显示区
        result_group = QVBoxLayout()
        result_label = QLabel("📤 优化后的Prompt:")
        result_label.setStyleSheet("font-weight: bold;")
        result_group.addWidget(result_label)
        
        self.optimized_result = QPlainTextEdit()
        # 允许编辑优化后的prompt
        self.optimized_result.setReadOnly(False)
        self.optimized_result.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 5px;
                font-family: 'WenQuanYi Micro Hei', 'Microsoft YaHei', 'SimHei', 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                padding: 10px;
                selection-background-color: #444;
            }
            QPlainTextEdit:focus {
                border-color: #2196F3;
            }
        """)
        self.optimized_result.setMinimumHeight(250)
        self.optimized_result.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.optimized_result.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.optimized_result.setFont(font)
        result_group.addWidget(self.optimized_result)
        
        layout.addLayout(result_group)
        
        # 结构分析和建议
        analysis_row = QHBoxLayout()
        analysis_row.setSpacing(15)  # 增加间距
        
        # 结构分析
        structure_group = QVBoxLayout()
        structure_label = QLabel("📊 结构分析:")
        structure_label.setStyleSheet("font-weight: bold;")
        structure_group.addWidget(structure_label)
        self.structure_display = QLabel("等待生成...")
        self.structure_display.setStyleSheet("color: #666; padding: 8px; background: #f9f9f9; border-radius: 3px; min-height: 40px;")
        self.structure_display.setWordWrap(True)
        structure_group.addWidget(self.structure_display)
        analysis_row.addLayout(structure_group, 1)
        
        # 改进建议
        suggestion_group = QVBoxLayout()
        suggestion_label = QLabel("💡 建议:")
        suggestion_label.setStyleSheet("font-weight: bold;")
        suggestion_group.addWidget(suggestion_label)
        self.suggestion_display = QLabel("等待生成...")
        self.suggestion_display.setStyleSheet("color: #666; padding: 8px; background: #f9f9f9; border-radius: 3px; min-height: 40px;")
        self.suggestion_display.setWordWrap(True)
        suggestion_group.addWidget(self.suggestion_display)
        analysis_row.addLayout(suggestion_group, 1)
        
        layout.addLayout(analysis_row)
        
        # 反馈区
        feedback_group = QHBoxLayout()
        feedback_group.addWidget(QLabel("📝 使用反馈:"))
        
        self.feedback_rating = QComboBox()
        self.feedback_rating.addItems(["5 - 非常好", "4 - 好", "3 - 一般", "2 - 差", "1 - 很差"])
        feedback_group.addWidget(self.feedback_rating)
        
        self.feedback_text = QLineEdit()
        self.feedback_text.setPlaceholderText("输入反馈意见（可选）...")
        # 启用中文输入法支持
        self.feedback_text.setAttribute(Qt.WidgetAttribute.WA_InputMethodEnabled, True)
        self.feedback_text.setInputMethodHints(Qt.InputMethodHint.ImhNone)
        font = QFont("WenQuanYi Micro Hei", 12)
        self.feedback_text.setFont(font)
        feedback_group.addWidget(self.feedback_text, 1)
        
        self.btn_submit_feedback = QPushButton("提交反馈")
        self.btn_submit_feedback.setEnabled(False)
        self.btn_submit_feedback.clicked.connect(self.submit_feedback)
        feedback_group.addWidget(self.btn_submit_feedback)
        
        layout.addLayout(feedback_group)
        
        # 保存当前优化结果用于反馈
        self.current_optimized_prompt = ""
        self.current_original_prompt = ""
        
        return widget
    
    def optimize_prompt(self):
        """执行Prompt优化"""
        task_desc = self.task_input.toPlainText().strip()
        context = self.context_input.toPlainText().strip()
        original = self.original_prompt_input.toPlainText().strip()
        
        if not task_desc and not original:
            QMessageBox.warning(self, "警告", "请输入任务描述或原始Prompt")
            return
        
        # 获取选中的prompt类型
        type_text = self.prompt_type_combo.currentText()
        prompt_type = type_text.split(" - ")[0] if " - " in type_text else "feature_development"
        
        # 显示加载状态
        self.btn_optimize.setEnabled(False)
        self.btn_optimize.setText("⏳ 正在优化...")
        self.optimized_result.setPlainText("正在生成优化后的Prompt，请稍候...")
        
        # 保存原始输入用于反馈
        self.current_original_prompt = task_desc if task_desc else original
        
        # 调用MCP工具
        arguments = {
            "task_description": task_desc,
            "context": context,
            "prompt_type": prompt_type,
            "include_template": True
        }
        if original:
            arguments["original_prompt"] = original
        
        worker = XuanyuanWorker("xuanyuan.prompt.optimize", arguments)
        worker.finished.connect(self.on_optimize_finished)
        worker.error.connect(self.on_optimize_error)
        worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        self.workers.append(worker)
        worker.start()
    
    def on_optimize_finished(self, data: dict):
        """优化完成回调"""
        self.btn_optimize.setEnabled(True)
        self.btn_optimize.setText("🔮 生成/优化 Prompt")
        
        if data.get("success"):
            prompt = data.get("prompt", "")
            self.optimized_result.setPlainText(prompt)
            self.current_optimized_prompt = prompt
            
            # 更新结构分析
            structure = data.get("structure", {})
            structure_text = []
            for key, value in structure.items():
                label = key.replace("has_", "").replace("_", " ").title()
                icon = "✅" if value else "❌"
                structure_text.append(f"{icon} {label}")
            self.structure_display.setText(" | ".join(structure_text))
            
            # 更新建议
            suggestions = data.get("suggestions", [])
            self.suggestion_display.setText("\n".join(suggestions) if suggestions else "无建议")
            
            # 启用操作按钮
            self.btn_copy_to_cursor.setEnabled(True)
            self.btn_open_cursor.setEnabled(True)
            self.btn_submit_feedback.setEnabled(True)
        else:
            self.optimized_result.setPlainText(f"优化失败: {data.get('error', '未知错误')}")
    
    def on_optimize_error(self, error: str):
        """优化错误回调"""
        self.btn_optimize.setEnabled(True)
        self.btn_optimize.setText("🔮 生成/优化 Prompt")
        self.optimized_result.setPlainText(f"错误: {error}")
        QMessageBox.warning(self, "错误", f"Prompt优化失败: {error}")
    
    def copy_optimized_to_clipboard(self):
        """复制优化后的Prompt到剪贴板"""
        from PyQt6.QtWidgets import QApplication
        # 使用当前编辑框的内容（用户可能已修改）
        prompt_text = self.optimized_result.toPlainText().strip()
        if not prompt_text:
            QMessageBox.warning(self, "警告", "优化后的Prompt为空")
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt_text)
        QMessageBox.information(self, "成功", "已复制到剪贴板！\n\n现在可以在Cursor Chat中粘贴使用。")
    
    def send_to_cursor(self):
        """发送到Cursor（复制到剪贴板并尝试通过系统方式发送）"""
        from PyQt6.QtWidgets import QApplication
        import subprocess
        import os
        
        # 获取当前编辑框的内容（用户可能已经修改过）
        prompt_text = self.optimized_result.toPlainText().strip()
        if not prompt_text:
            QMessageBox.warning(self, "警告", "优化后的Prompt为空，请先生成Prompt")
            return
        
        # 复制到剪贴板
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt_text)
        
        # 尝试通过系统快捷键发送到Cursor（如果Cursor支持）
        # 注意：这需要Cursor支持全局快捷键或剪贴板监听
        # 实际实现可能需要使用Cursor的API或扩展
        
        QMessageBox.information(
            self, 
            "提示", 
            "Prompt已复制到剪贴板！\n\n"
            "请在Cursor Chat中:\n"
            "1. 点击Cursor的Chat输入框\n"
            "2. 按 Ctrl+V 粘贴Prompt\n"
            "3. 按 Enter 执行\n\n"
            "提示：如果Cursor支持全局快捷键，可以尝试使用快捷键打开Chat。"
        )
    
    def submit_feedback(self):
        """提交使用反馈"""
        rating_text = self.feedback_rating.currentText()
        rating = int(rating_text[0])  # 取第一个字符作为评分
        feedback = self.feedback_text.text().strip()
        
        arguments = {
            "original_prompt": self.current_original_prompt[:500],
            "optimized_prompt": self.current_optimized_prompt[:500],
            "rating": rating,
            "feedback": feedback
        }
        
        worker = XuanyuanWorker("xuanyuan.prompt.feedback", arguments)
        worker.finished.connect(self.on_feedback_submitted)
        worker.error.connect(lambda err: QMessageBox.warning(self, "错误", f"提交反馈失败: {err}"))
        worker.finished.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        worker.error.connect(lambda: self.workers.remove(worker) if worker in self.workers else None)
        self.workers.append(worker)
        worker.start()
    
    def on_feedback_submitted(self, data: dict):
        """反馈提交完成"""
        if data.get("success"):
            stats = data.get("stats", {})
            QMessageBox.information(
                self, 
                "感谢反馈", 
                f"反馈已提交！\n\n"
                f"统计信息:\n"
                f"  总反馈数: {stats.get('total', 0)}\n"
                f"  平均评分: {stats.get('avg_rating', 0):.1f}/5\n\n"
                f"您的反馈将帮助我们改进Prompt优化工具。"
            )
            self.feedback_text.clear()
        else:
            QMessageBox.warning(self, "错误", f"提交失败: {data.get('error', '未知错误')}")
