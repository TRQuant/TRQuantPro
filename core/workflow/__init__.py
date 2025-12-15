"""工作流管理模块"""
from .state_manager import WorkflowStateManager, WorkflowState, WorkflowStatus, StepStatus, get_state_manager

# 别名支持（兼容性）
StateManager = WorkflowStateManager


# 增强型编排器
from .enhanced_orchestrator import (
    EnhancedWorkflowOrchestrator,
    WorkflowConfig,
    WorkflowStep,
    WorkflowStepStatus,
    create_workflow,
)
