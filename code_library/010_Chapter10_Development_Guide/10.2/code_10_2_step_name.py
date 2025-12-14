"""
文件名: code_10_2_step_name.py
保存路径: code_library/010_Chapter10_Development_Guide/10.2/code_10_2_step_name.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.2_Development_Principles_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: step_name

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# core/workflow/workflow_interface.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class WorkflowResult:
    """工作流结果"""
    step_name: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None

class WorkflowStep(ABC):
    """工作流步骤接口"""
    
    @property
    @abstractmethod
    def step_name(self) -> str:
            """
    step_name函数
    
    **设计原理**：
    - **核心功能**：实现step_name的核心逻辑
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
        pass
    
    @property
    @abstractmethod
    def step_number(self) -> int:
        """步骤序号"""
        pass
    
    @abstractmethod
    def execute(
        self,
        context: Dict[str, Any]
    ) -> WorkflowResult:
        """执行步骤"""
        pass
    
    @abstractmethod
    def get_dependencies(self) -> List[str]:
        """获取依赖的步骤名称"""
        pass

# 具体步骤实现
class DataSourceStep(WorkflowStep):
    """数据源步骤"""
    
    @property
    def step_name(self) -> str:
        return "data_source"
    
    @property
    def step_number(self) -> int:
        return 1
    
    def get_dependencies(self) -> List[str]:
        return []
    
    def execute(self, context: Dict[str, Any]) -> WorkflowResult:
        """执行数据源检测"""
        from core.data_source.data_source_manager import DataSourceManager
        
        manager = DataSourceManager()
        sources = manager.get_available_sources()
        
        return WorkflowResult(
            step_name=self.step_name,
            success=len(sources) > 0,
            data={'sources': sources}
        )