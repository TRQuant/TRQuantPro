# -*- coding: utf-8 -*-
"""
投资工作流程前端面板
==================

基于完整投资工作流程图的独立前端界面
每个步骤都有按钮可以打开对应的Notebook或执行相应操作
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QGridLayout, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from pathlib import Path
import logging
import subprocess
import os
import threading

from gui.styles.theme import Colors

logger = logging.getLogger(__name__)

# 工作流程步骤配置

# 系统架构总览（最顶部，独立显示）
SYSTEM_OVERVIEW_STEP = {
    "name": "系统架构与工作流程",
    "icon": "🏗️",
    "color": "#6366F1",
    "notebook": "notebooks/research/00_system_architecture_workflow.ipynb",
    "description": "系统架构总览、研究-实战工作流程详解、数据流转图"
}

DATA_SOURCE_STEP = {
    "name": "信息获取",
    "icon": "📡",
    "color": "#3B82F6",
}

RESEARCH_STEPS = [
    {"name": "市场趋势分析", "icon": "📈", "color": "#10B981", "notebook": "notebooks/research/01_market_trend_comprehensive.ipynb", "description": "多周期趋势分析、市场环境评估"},
    {"name": "主线轮动研究", "icon": "🔥", "color": "#F59E0B", "notebook": "notebooks/templates/02_mainline_identification.ipynb", "description": "投资主线识别、行业板块分析"},
    {"name": "因子组合开发", "icon": "🧮", "color": "#8B5CF6", "notebook": "notebooks/templates/04_factor_research.ipynb", "description": "因子研究、IC/IR分析、因子组合"},
    {"name": "投资标的筛选", "icon": "📦", "color": "#EC4899", "notebook": "notebooks/templates/03_candidate_pool.ipynb", "description": "候选池构建、股票筛选"},
    {"name": "风控模块设计", "icon": "🛡️", "color": "#06B6D4", "notebook": "notebooks/research/04_risk_assessment.ipynb", "description": "风险评估、风控策略设计"},
    {"name": "策略开发与回测", "icon": "💻", "color": "#EF4444", "notebook": "notebooks/templates/05_strategy_generation.ipynb", "description": "策略开发、回测验证、绩效分析", "additional_notebooks": ["notebooks/templates/06_backtest_analysis.ipynb", "notebooks/templates/07_optimization.ipynb"]},
]

LIVE_TRADING_STEPS = [
    {"name": "PTrade回测优化", "icon": "📊", "color": "#3B82F6", "action": "ptrade_backtest"},
    {"name": "QMT回测优化", "icon": "📊", "color": "#10B981", "action": "qmt_backtest"},
    {"name": "小盘试水", "icon": "🌊", "color": "#F59E0B", "action": "small_scale_trial"},
    {"name": "监控优化", "icon": "📈", "color": "#8B5CF6", "action": "monitor_optimize"},
    {"name": "重仓押注", "icon": "💰", "color": "#EF4444", "action": "heavy_position"},
]

KNOWLEDGE_BASE_ITEMS = [
    {"name": "聚宽API文档", "icon": "📚", "color": "#3B82F6", "action": "open_jqdata_docs"},
    {"name": "历史研究结论", "icon": "📝", "color": "#10B981", "action": "open_research_conclusions"},
    {"name": "策略模板库", "icon": "📋", "color": "#F59E0B", "action": "open_strategy_templates"},
    {"name": "错误经验库", "icon": "⚠️", "color": "#EF4444", "action": "open_error_experience"},
]

CONVERSION_ITEMS = [
    {"name": "聚宽→PTrade转换器", "icon": "🔄", "color": "#3B82F6", "action": "convert_jqdata_to_ptrade"},
    {"name": "聚宽→QMT转换器", "icon": "🔄", "color": "#10B981", "action": "convert_jqdata_to_qmt"},
    {"name": "数据源适配器", "icon": "🔌", "color": "#8B5CF6", "action": "data_source_adapter"},
]

class InvestmentWorkflowPanel(QWidget):
    """投资工作流程前端面板"""
    
    open_notebook = pyqtSignal(str)
    open_data_source_panel = pyqtSignal()
    execute_action = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.project_root = Path(__file__).parent.parent.parent
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题和快速操作按钮
        title_layout = QHBoxLayout()
        title_layout.setSpacing(15)
        
        title = QLabel("📊 投资工作流程")
        title.setStyleSheet(f"font-size: 24px; font-weight: 700; color: {Colors.TEXT_PRIMARY}; padding: 10px 0;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        # 添加打开 Jupyter Notebook 按钮
        jupyter_btn = QPushButton("📓 打开 Jupyter Notebook")
        jupyter_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #10B981;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #059669;
            }}
        """)
        jupyter_btn.clicked.connect(self._on_open_jupyter_notebook)
        title_layout.addWidget(jupyter_btn)
        
        layout.addLayout(title_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"QScrollArea {{ border: none; background: transparent; }}")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(30)
        
        # 0. 系统架构总览（最顶部）
        content_layout.addWidget(self._create_system_overview_section())
        
        # 1. 信息获取
        content_layout.addWidget(self._create_data_source_section())
        content_layout.addWidget(self._create_research_phase_section())
        content_layout.addWidget(self._create_live_trading_section())
        content_layout.addWidget(self._create_knowledge_base_section())
        content_layout.addWidget(self._create_conversion_section())
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)
    
    def _create_system_overview_section(self):
        """创建系统架构总览部分（最顶部）"""
        group = QGroupBox("🏗️ 系统架构与工作流程")
        group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 18px;
                font-weight: 700;
                color: {Colors.TEXT_PRIMARY};
                border: 2px solid {SYSTEM_OVERVIEW_STEP['color']};
                border-radius: 12px;
                padding-top: 15px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }}
        """)
        
        layout = QVBoxLayout(group)
        layout.setSpacing(12)
        
        # 说明
        desc = QLabel(SYSTEM_OVERVIEW_STEP['description'])
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        
        # 按钮
        btn = QPushButton(f"{SYSTEM_OVERVIEW_STEP['icon']} 打开系统架构流程图")
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {SYSTEM_OVERVIEW_STEP['color']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: #7C7CF9;
            }}
        """)
        btn.clicked.connect(lambda: self._on_open_notebook(SYSTEM_OVERVIEW_STEP['notebook']))
        layout.addWidget(btn)
        
        return group
    
    def _create_data_source_section(self):
        """创建信息获取（数据源验证）部分"""
        group = QGroupBox("📡 信息获取（数据源验证）")
        group.setStyleSheet(f"""
            QGroupBox {{ font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY}; border: 2px solid {DATA_SOURCE_STEP['color']}; border-radius: 12px; padding-top: 15px; margin-top: 10px; }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 15px; padding: 0 10px; }}
        """)
        layout = QVBoxLayout(group)
        desc = QLabel("检测并验证JQData、AKShare、MongoDB等数据源连接状态")
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        btn = QPushButton(f"{DATA_SOURCE_STEP['icon']} 打开数据源状态面板")
        btn.setStyleSheet(f"QPushButton {{ background: {DATA_SOURCE_STEP['color']}; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: 600; }} QPushButton:hover {{ background: {self._darken_color(DATA_SOURCE_STEP['color'])}; }}")
        btn.clicked.connect(self._on_open_data_source_panel)
        layout.addWidget(btn)
        return group
    
    def _create_research_phase_section(self):
        """创建研究阶段部分"""
        group = QGroupBox("🔬 研究阶段 (Jupyter Notebook)")
        group.setStyleSheet(f"QGroupBox {{ font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY}; border: 2px solid #10B981; border-radius: 12px; padding-top: 15px; margin-top: 10px; }} QGroupBox::title {{ subcontrol-origin: margin; left: 15px; padding: 0 10px; }}")
        layout = QVBoxLayout(group)
        desc = QLabel("在Jupyter Notebook中进行策略研究和开发")
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        grid = QGridLayout()
        grid.setSpacing(15)
        for i, step in enumerate(RESEARCH_STEPS):
            row, col = i // 2, i % 2
            step_widget = self._create_step_button(step['name'], step['icon'], step['color'], step['description'], lambda checked, nb=step['notebook']: self._on_open_notebook(nb), step.get('additional_notebooks', []))
            grid.addWidget(step_widget, row, col)
        layout.addLayout(grid)
        return group
    
    def _create_live_trading_section(self):
        """创建实战阶段部分"""
        group = QGroupBox("💰 实战阶段 (券商端)")
        group.setStyleSheet(f"QGroupBox {{ font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY}; border: 2px solid #F59E0B; border-radius: 12px; padding-top: 15px; margin-top: 10px; }} QGroupBox::title {{ subcontrol-origin: margin; left: 15px; padding: 0 10px; }}")
        layout = QVBoxLayout(group)
        desc = QLabel("在PTrade/QMT平台进行实盘交易和监控")
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        grid = QGridLayout()
        grid.setSpacing(15)
        for i, step in enumerate(LIVE_TRADING_STEPS):
            row, col = i // 3, i % 3
            step_widget = self._create_action_button(step['name'], step['icon'], step['color'], step['action'])
            grid.addWidget(step_widget, row, col)
        layout.addLayout(grid)
        return group
    
    def _create_knowledge_base_section(self):
        """创建知识库（RAG）部分"""
        group = QGroupBox("📚 知识库 (RAG)")
        group.setStyleSheet(f"QGroupBox {{ font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY}; border: 2px solid #8B5CF6; border-radius: 12px; padding-top: 15px; margin-top: 10px; }} QGroupBox::title {{ subcontrol-origin: margin; left: 15px; padding: 0 10px; }}")
        layout = QVBoxLayout(group)
        desc = QLabel("策略知识库、历史研究结论、错误经验库")
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        grid = QGridLayout()
        grid.setSpacing(15)
        for i, item in enumerate(KNOWLEDGE_BASE_ITEMS):
            row, col = i // 2, i % 2
            item_widget = self._create_action_button(item['name'], item['icon'], item['color'], item['action'])
            grid.addWidget(item_widget, row, col)
        layout.addLayout(grid)
        return group
    
    def _create_conversion_section(self):
        """创建转换层部分"""
        group = QGroupBox("🔄 转换层")
        group.setStyleSheet(f"QGroupBox {{ font-size: 16px; font-weight: 600; color: {Colors.TEXT_PRIMARY}; border: 2px solid #06B6D4; border-radius: 12px; padding-top: 15px; margin-top: 10px; }} QGroupBox::title {{ subcontrol-origin: margin; left: 15px; padding: 0 10px; }}")
        layout = QVBoxLayout(group)
        desc = QLabel("策略转换工具、数据源适配器")
        desc.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(desc)
        grid = QGridLayout()
        grid.setSpacing(15)
        for i, item in enumerate(CONVERSION_ITEMS):
            row, col = i // 2, i % 2
            item_widget = self._create_action_button(item['name'], item['icon'], item['color'], item['action'])
            grid.addWidget(item_widget, row, col)
        layout.addLayout(grid)
        return group
    
    def _create_step_button(self, name, icon, color, description, callback, additional_notebooks=None):
        """创建步骤按钮"""
        frame = QFrame()
        frame.setStyleSheet(f"QFrame {{ background: {Colors.BG_CARD}; border: 2px solid {color}; border-radius: 12px; padding: 15px; }} QFrame:hover {{ background: {Colors.BG_HOVER}; border-color: {self._lighten_color(color)}; }}")
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        title = QLabel(f"{icon} {name}")
        title.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {Colors.TEXT_PRIMARY};")
        layout.addWidget(title)
        desc = QLabel(description)
        desc.setStyleSheet(f"font-size: 12px; color: {Colors.TEXT_SECONDARY};")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        btn = QPushButton("📓 打开Notebook")
        btn.setStyleSheet(f"QPushButton {{ background: {color}; color: white; border: none; border-radius: 6px; padding: 8px 15px; font-size: 13px; font-weight: 600; }} QPushButton:hover {{ background: {self._darken_color(color)}; }}")
        btn.clicked.connect(callback)
        layout.addWidget(btn)
        if additional_notebooks:
            for nb in additional_notebooks:
                btn_extra = QPushButton(f"📓 {Path(nb).stem}")
                btn_extra.setStyleSheet(f"QPushButton {{ background: {Colors.BG_TERTIARY}; color: {Colors.TEXT_PRIMARY}; border: 1px solid {color}; border-radius: 6px; padding: 6px 12px; font-size: 12px; }} QPushButton:hover {{ background: {Colors.BG_HOVER}; }}")
                btn_extra.clicked.connect(lambda checked, nb=nb: self._on_open_notebook(nb))
                layout.addWidget(btn_extra)
        return frame
    
    def _create_action_button(self, name, icon, color, action):
        """创建动作按钮"""
        btn = QPushButton(f"{icon} {name}")
        btn.setStyleSheet(f"QPushButton {{ background: {color}; color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: 600; }} QPushButton:hover {{ background: {self._darken_color(color)}; }}")
        btn.clicked.connect(lambda: self._on_execute_action(action))
        return btn
    
    def _on_open_notebook(self, notebook_path):
        """打开Notebook - 优先在Cursor中打开"""
        full_path = self.project_root / notebook_path
        
        if not full_path.exists():
            QMessageBox.warning(
                self,
                "文件不存在",
                f"Notebook文件不存在:\n{full_path}"
            )
            return
        
        opened = False
        error_msg = None
        
        # 方法1: 优先使用Cursor打开（可以在Cursor中直接运行）
        try:
            result = subprocess.run(
                ["which", "cursor"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode == 0:
                subprocess.Popen(
                    ["cursor", str(full_path)],
                    cwd=str(self.project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                logger.info(f"✅ 已在Cursor中打开Notebook: {full_path}")
                opened = True
        except Exception as e:
            error_msg = f"Cursor命令失败: {str(e)}"
            logger.debug(error_msg)
        
        # 方法2: 如果没有cursor，尝试使用code命令（VS Code/Cursor兼容）
        if not opened:
            try:
                result = subprocess.run(
                    ["which", "code"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    subprocess.Popen(
                        ["code", str(full_path)],
                        cwd=str(self.project_root),
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    logger.info(f"✅ 已在VS Code/Cursor中打开Notebook: {full_path}")
                    opened = True
            except Exception as e:
                if error_msg:
                    error_msg += f"\ncode命令失败: {str(e)}"
                else:
                    error_msg = f"code命令失败: {str(e)}"
                logger.debug(error_msg)
        
        # 方法3: 回退到JupyterLab（如果Cursor/VS Code都不可用）
        if not opened:
            try:
                subprocess.Popen(
                    ["jupyter", "lab", str(full_path)],
                    cwd=str(self.project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                logger.info(f"✅ 已在JupyterLab中打开Notebook: {full_path}")
                opened = True
            except Exception as e:
                if error_msg:
                    error_msg += f"\nJupyterLab失败: {str(e)}"
                else:
                    error_msg = f"JupyterLab失败: {str(e)}"
                logger.debug(error_msg)
        
        # 方法4: 最后尝试系统默认程序
        if not opened:
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(str(full_path))
                elif os.name == 'posix':  # macOS/Linux
                    subprocess.Popen(['xdg-open', str(full_path)])
                logger.info(f"✅ 已使用系统默认程序打开Notebook: {full_path}")
                opened = True
            except Exception as e2:
                error_msg = error_msg or ""
                error_msg += f"\n系统默认程序失败: {str(e2)}"
                QMessageBox.warning(
                    self,
                    "打开失败",
                    f"无法打开Notebook:\n{error_msg}\n\n请手动打开: {full_path}"
                )
                logger.error(f"打开Notebook失败: {error_msg}")
        
        self.open_notebook.emit(str(full_path))

    def _on_open_data_source_panel(self):
        """打开数据源状态面板"""
        self.open_data_source_panel.emit()
        logger.info("打开数据源状态面板")
    
    def _on_open_jupyter_notebook(self):
        """打开 Jupyter Notebook（在独立浏览器中）"""
        notebook_dir = self.project_root / "notebooks"
        notebook_dir.mkdir(exist_ok=True)
        
        # 检查是否已经运行
        pid_file = Path("/tmp/jupyter_notebook.pid")
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
                # 检查进程是否还在运行
                try:
                    os.kill(pid, 0)  # 发送信号0检查进程是否存在
                    logger.info(f"Jupyter Notebook 已在运行 (PID: {pid})")
                    # 打开浏览器
                    subprocess.Popen(
                        ["xdg-open", "http://localhost:8888"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    return
                except OSError:
                    # 进程不存在，删除旧的 PID 文件
                    pid_file.unlink()
            except (ValueError, OSError):
                pid_file.unlink()
        
        # 查找 jupyter 命令
        jupyter_cmd = None
        for conda_path in [
            Path.home() / "miniconda3" / "bin" / "jupyter",
            Path.home() / "anaconda3" / "bin" / "jupyter",
            Path("/opt/miniconda3/bin/jupyter"),
            Path("/opt/anaconda3/bin/jupyter"),
        ]:
            if conda_path.exists():
                jupyter_cmd = str(conda_path)
                break
        
        if not jupyter_cmd:
            # 尝试系统路径
            try:
                result = subprocess.run(
                    ["which", "jupyter"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0:
                    jupyter_cmd = result.stdout.strip()
            except Exception:
                pass
        
        if not jupyter_cmd:
            logger.error("未找到 jupyter 命令")
            return
        
        try:
            # 启动 Jupyter Notebook（后台运行）
            log_file = Path("/tmp/jupyter_notebook.log")
            pid_file_path = "/tmp/jupyter_notebook.pid"
            
            # 使用 nohup 在后台启动
            cmd = [
                "nohup", jupyter_cmd, "notebook",
                "--no-browser",
                f"--notebook-dir={notebook_dir}",
                "--ip=127.0.0.1",
                "--port=8888",
                "--NotebookApp.open_browser=True",
                "--NotebookApp.token=",
                "--NotebookApp.password=",
            ]
            
            with open(log_file, "w") as log:
                process = subprocess.Popen(
                    cmd,
                    cwd=str(notebook_dir),
                    stdout=log,
                    stderr=subprocess.STDOUT,
                    start_new_session=True
                )
                
                # 保存 PID
                with open(pid_file_path, "w") as f:
                    f.write(str(process.pid))
            
            logger.info(f"✅ 已启动 Jupyter Notebook 服务器 (PID: {process.pid})")
            
            # 等待几秒后打开浏览器
            def open_browser():
                import time
                time.sleep(3)
                subprocess.Popen(
                    ["xdg-open", "http://localhost:8888"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # 在后台线程中打开浏览器
            threading.Thread(target=open_browser, daemon=True).start()
            
        except Exception as e:
            logger.error(f"启动 Jupyter Notebook 失败: {str(e)}")
    
    def _on_execute_action(self, action):
        """执行动作"""
        self.execute_action.emit(action)
        logger.info(f"执行动作: {action}")
        QMessageBox.information(self, "动作执行", f"已触发动作: {action}\n\n具体功能待实现")
    
    def _darken_color(self, color):
        """加深颜色"""
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r, g, b = max(0, r - 30), max(0, g - 30), max(0, b - 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
    
    def _lighten_color(self, color):
        """变亮颜色"""
        if color.startswith('#'):
            r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
