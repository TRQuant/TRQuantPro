"""
文件名: code_9_4_from.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.4/code_9_4_from.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.4_GUI_Workflow_System_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: from

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/widgets/integrated_workflow_panel.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class StepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"      # 待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 执行失败
    SKIPPED = "skipped"      # 已跳过

@dataclass
class WorkflowStep:
    """工作流步骤定义"""
    id: str                  # 步骤ID
    name: str                # 步骤名称
    icon: str                # 图标
    color: str               # 颜色
    step_number: int         # 步骤序号
    description: str         # 描述
    dependencies: List[str] = None  # 依赖的步骤ID列表
    orchestrator_method: str = None  # WorkflowOrchestrator方法名

# 8步骤工作流定义
WORKFLOW_STEPS = [
    WorkflowStep(
        id="data_source",
        name="信息获取",
        icon="📡",
        color="#3b82f6",
        step_number=1,
        description="数据源检测、数据更新",
        dependencies=[],
        orchestrator_method="check_data_sources"
    ),
    WorkflowStep(
        id="market_trend",
        name="市场分析",
        icon="📈",
        color="#60a5fa",
        step_number=2,
        description="市场趋势分析、市场状态判断",
        dependencies=["data_source"],
        orchestrator_method="analyze_market_trend"
    ),
    WorkflowStep(
        id="mainline",
        name="投资主线",
        icon="🔥",
        color="#f59e0b",
        step_number=3,
        description="主线识别、主线评分",
        dependencies=["market_trend"],
        orchestrator_method="identify_mainlines"
    ),
    WorkflowStep(
        id="candidate_pool",
        name="候选池构建",
        icon="📦",
        color="#10b981",
        step_number=4,
        description="股票筛选、候选池管理",
        dependencies=["mainline"],
        orchestrator_method="build_candidate_pool"
    ),
    WorkflowStep(
        id="factor",
        name="因子构建",
        icon="📊",
        color="#3b82f6",
        step_number=5,
        description="因子推荐、因子配置",
        dependencies=["market_trend"],
        orchestrator_method="recommend_factors"
    ),
    WorkflowStep(
        id="strategy",
        name="策略生成",
        icon="🛠️",
        color="#60a5fa",
        step_number=6,
        description="策略代码生成、策略优化",
        dependencies=["candidate_pool", "factor"],
        orchestrator_method="generate_strategy"
    ),
    WorkflowStep(
        id="backtest",
        name="回测验证",
        icon="🔄",
        color="#10b981",
        step_number=7,
        description="BulletTrade回测、回测分析",
        dependencies=["strategy"],
        orchestrator_method="run_backtest"
    ),
    WorkflowStep(
        id="trading",
        name="实盘交易",
        icon="🚀",
        color="#3b82f6",
        step_number=8,
        description="策略部署、实盘交易",
        dependencies=["backtest"],
        orchestrator_method="deploy_strategy"
    ),
]

# 步骤映射（步骤ID -> WorkflowStep）
STEP_MAP = {step.id: step for step in WORKFLOW_STEPS}