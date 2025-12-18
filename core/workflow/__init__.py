"""工作流管理模块"""
from .state_manager import WorkflowStateManager, WorkflowState, WorkflowStatus, StepStatus, get_state_manager

# 别名支持（兼容性）
StateManager = WorkflowStateManager

# 增强型编排器（已合并到 workflow_orchestrator.py）
from core.workflow_orchestrator import EnhancedWorkflowOrchestrator, create_workflow

# 可选导入（如果类存在）
try:
    from core.workflow_orchestrator import WorkflowConfig, WorkflowStep, WorkflowStepStatus
except ImportError:
    # 这些类可能不存在，不影响主要功能
    WorkflowConfig = None
    WorkflowStep = None
    WorkflowStepStatus = None
