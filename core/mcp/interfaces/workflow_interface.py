"""
工作流服务接口定义

提供版本无关的接口定义，支持多版本并存和独立升级。

Author: TRQuant Team
Date: 2025-12-21
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class WorkflowRequest:
    """工作流请求（版本无关）"""
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    args: Optional[Dict[str, Any]] = None
    version: str = "v1"
    
    def __post_init__(self):
        if self.args is None:
            self.args = {}


@dataclass
class WorkflowResponse:
    """工作流响应（版本无关）"""
    success: bool
    workflow_id: Optional[str] = None
    step_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    version: str = "v1"
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "workflow_id": self.workflow_id,
            "step_id": self.step_id,
            "result": self.result,
            "error": self.error,
            "version": self.version
        }


@dataclass
class WorkflowStep:
    """工作流步骤定义"""
    id: str
    name: str
    icon: str
    color: str
    description: str
    status: str = "pending"  # pending/running/completed/failed


class IWorkflowService(ABC):
    """
    工作流服务接口（抽象基类）
    
    所有版本的工作流服务都必须实现此接口。
    """
    
    @abstractmethod
    def get_version(self) -> str:
        """获取服务版本"""
        pass
    
    @abstractmethod
    def get_steps(self) -> List[WorkflowStep]:
        """获取所有步骤定义"""
        pass
    
    @abstractmethod
    def create_workflow(self, name: Optional[str] = None) -> WorkflowResponse:
        """创建新的工作流会话"""
        pass
    
    @abstractmethod
    def get_status(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流状态"""
        pass
    
    @abstractmethod
    def run_step(self, request: WorkflowRequest) -> WorkflowResponse:
        """执行指定步骤"""
        pass
    
    @abstractmethod
    def run_all(self, workflow_id: str) -> WorkflowResponse:
        """一键执行所有步骤"""
        pass
    
    @abstractmethod
    def get_context(self, workflow_id: str) -> WorkflowResponse:
        """获取工作流上下文"""
        pass

