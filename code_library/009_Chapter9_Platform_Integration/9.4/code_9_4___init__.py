"""
文件名: code_9_4___init__.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.4/code_9_4___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.4_GUI_Workflow_System_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

# gui/widgets/integrated_workflow_panel.py (完整实现)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QProgressBar, QTextBrowser,
    QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from gui.styles.theme import Colors, ButtonStyles
from gui.widgets.workflow_state_manager import WorkflowStateManager, StepStatus
from gui.widgets.workflow_executor import WorkflowExecutor
from gui.widgets.integrated_workflow_panel import WORKFLOW_STEPS, WorkflowDependencyManager

class IntegratedWorkflowPanel(QWidget):
    """集成工作流面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.state_manager = WorkflowStateManager()
        self.dependency_manager = WorkflowDependencyManager(WORKFLOW_STEPS)
        self.executor: Optional[WorkflowExecutor] = None
        self.step_cards: Dict[str, 'StepCard'] = {}
        
        self.init_ui()
        self.init_workflow()
    
    def init_ui(self):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        
        # 标题
        title = QLabel("🔄 8步骤投资工作流")
        title.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 24px;
                font-weight: 700;
                padding: 12px 0;
            }}
        """)
        layout.addWidget(title)
        
        # 工具栏
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # 主内容区（分割器）
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧：步骤列表
        steps_widget = self.create_steps_widget()
        splitter.addWidget(steps_widget)
        
        # 右侧：结果展示
        results_widget = self.create_results_widget()
        splitter.addWidget(results_widget)
        
        # 设置分割比例
        splitter.setSizes([400, 600])
        layout.addWidget(splitter)
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QWidget()
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 执行全部按钮
        run_all_btn = QPushButton("▶️ 执行全部步骤")
        run_all_btn.setStyleSheet(ButtonStyles.PRIMARY)
        run_all_btn.clicked.connect(self.run_full_workflow)
        layout.addWidget(run_all_btn)
        
        # 重置按钮
        reset_btn = QPushButton("🔄 重置")
        reset_btn.setStyleSheet(ButtonStyles.SECONDARY)
        reset_btn.clicked.connect(self.reset_workflow)
        layout.addWidget(reset_btn)
        
        layout.addStretch()
        
        return toolbar
    
    def create_steps_widget(self):
        """创建步骤列表"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # 步骤标题
        steps_title = QLabel("工作流步骤")
        steps_title.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 600;
                padding: 8px 0;
            }}
        """)
        layout.addWidget(steps_title)
        
        # 步骤卡片列表
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                background-color: {Colors.BG_SECONDARY};
            }}
        """)
        
        steps_container = QWidget()
        steps_layout = QVBoxLayout(steps_container)
        steps_layout.setSpacing(12)
        steps_layout.setContentsMargins(12, 12, 12, 12)
        
        # 创建步骤卡片
        for step in WORKFLOW_STEPS:
            card = StepCard(step, self)
            card.clicked.connect(self.on_step_clicked)
            steps_layout.addWidget(card)
            self.step_cards[step.id] = card
        
        steps_layout.addStretch()
        scroll.setWidget(steps_container)
        layout.addWidget(scroll)
        
        return widget
    
    def create_results_widget(self):
        """创建结果展示区"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # 结果标题
        results_title = QLabel("执行结果")
        results_title.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: 18px;
                font-weight: 600;
                padding: 8px 0;
            }}
        """)
        layout.addWidget(results_title)
        
        # 结果文本区
        self.results_text = QTextBrowser()
        self.results_text.setStyleSheet(f"""
            QTextBrowser {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_PRIMARY};
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }}
        """)
        layout.addWidget(self.results_text)
        
        return widget
    
    def init_workflow(self):
        """初始化工作流"""
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.state_manager.init_workflow(workflow_id)
        self.log(f"工作流已初始化: {workflow_id}")
    
    def run_full_workflow(self):
        """执行完整工作流"""
        if self.executor and self.executor.isRunning():
            QMessageBox.warning(self, "警告", "工作流正在执行中，请等待完成")
            return
        
        # 创建执行引擎
        self.executor = WorkflowExecutor(
            self.state_manager,
            self.dependency_manager
        )
        
        # 连接信号
        self.executor.step_started.connect(self.on_step_started)
        self.executor.step_progress.connect(self.on_step_progress)
        self.executor.step_completed.connect(self.on_step_completed)
        self.executor.step_failed.connect(self.on_step_failed)
        self.executor.workflow_completed.connect(self.on_workflow_completed)
        
        # 启动执行
        self.executor.start()
        self.log("开始执行完整工作流...")
    
    def on_step_clicked(self, step_id: str):
        """步骤点击事件"""
        if self.executor and self.executor.isRunning():
            QMessageBox.warning(self, "警告", "工作流正在执行中，无法执行单个步骤")
            return
        
        # 执行单个步骤
        self.executor = WorkflowExecutor(
            self.state_manager,
            self.dependency_manager
        )
        
        self.executor.step_started.connect(self.on_step_started)
        self.executor.step_progress.connect(self.on_step_progress)
        self.executor.step_completed.connect(self.on_step_completed)
        self.executor.step_failed.connect(self.on_step_failed)
        
        # 执行步骤
        self.executor.execute_step(step_id)
    
    def on_step_started(self, step_id: str):
        """步骤开始"""
        if step_id in self.step_cards:
            self.step_cards[step_id].set_running(True)
        self.log(f"步骤 {step_id} 开始执行...")
    
    def on_step_progress(self, step_id: str, progress: int, message: str):
        """步骤进度更新"""
        self.log(f"步骤 {step_id}: {message} ({progress}%)")
    
    def on_step_completed(self, step_id: str, result: dict):
        """步骤完成"""
        if step_id in self.step_cards:
            self.step_cards[step_id].set_running(False)
            self.step_cards[step_id].set_completed(True)
        
        success = result.get('success', False)
        summary = result.get('summary', '')
        self.log(f"步骤 {step_id} 完成: {summary}")
        
        if not success:
            self.log(f"⚠️ 步骤 {step_id} 执行失败")
    
    def on_step_failed(self, step_id: str, error: str):
        """步骤失败"""
        if step_id in self.step_cards:
            self.step_cards[step_id].set_running(False)
            self.step_cards[step_id].set_completed(False)
        
        self.log(f"❌ 步骤 {step_id} 执行失败: {error}")
    
    def on_workflow_completed(self, result: dict):
        """工作流完成"""
        success = result.get('success', False)
        completed_steps = result.get('completed_steps', [])
        failed_steps = result.get('failed_steps', [])
        
        if success:
            self.log(f"✅ 完整工作流执行成功！完成 {len(completed_steps)} 个步骤")
        else:
            self.log(f"⚠️ 完整工作流执行完成，但有 {len(failed_steps)} 个步骤失败")
            self.log(f"失败的步骤: {', '.join(failed_steps)}")
    
    def reset_workflow(self):
        """重置工作流"""
        if self.executor and self.executor.isRunning():
            self.executor.cancel()
            self.executor.wait()
        
        self.state_manager.reset_workflow()
        self.init_workflow()
        
        # 重置所有卡片状态
        for card in self.step_cards.values():
            card.set_running(False)
            card.set_completed(False)
        
        self.results_text.clear()
        self.log("工作流已重置")
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.append(f"[{timestamp}] {message}")