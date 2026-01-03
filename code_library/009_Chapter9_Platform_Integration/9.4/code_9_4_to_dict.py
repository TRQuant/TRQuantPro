"""
文件名: code_9_4_to_dict.py
保存路径: code_library/009_Chapter9_Platform_Integration/9.4/code_9_4_to_dict.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/009_Chapter9_Platform_Integration/9.4_GUI_Workflow_System_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: to_dict

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

# gui/widgets/workflow_state_manager.py
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum

class StepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class StepState:
    """步骤状态"""
    step_id: str
    status: StepStatus
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    progress: int = 0  # 0-100
    
    def to_dict(self) -> Dict:
            """
    to_dict函数
    
    **设计原理**：
    - **核心功能**：实现to_dict的核心逻辑
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
        return {
            'step_id': self.step_id,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'result': self.result,
            'error': self.error,
            'progress': self.progress
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'StepState':
        """从字典创建"""
        return cls(
            step_id=data['step_id'],
            status=StepStatus(data['status']),
            start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else None,
            end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
            result=data.get('result'),
            error=data.get('error'),
            progress=data.get('progress', 0)
        )

class WorkflowStateManager:
    """工作流状态管理器"""
    
    def __init__(self, db_connection=None):
        """
        初始化状态管理器
        
        Args:
            db_connection: 数据库连接（用于持久化）
        """
        self.db = db_connection
        self.states: Dict[str, StepState] = {}
        self.workflow_id: Optional[str] = None
    
    def init_workflow(self, workflow_id: str):
        """初始化工作流"""
        self.workflow_id = workflow_id
        # 从数据库加载状态
        self._load_states()
    
    def get_step_state(self, step_id: str) -> Optional[StepState]:
        """获取步骤状态"""
        return self.states.get(step_id)
    
    def set_step_status(
        self,
        step_id: str,
        status: StepStatus,
        result: Optional[Dict] = None,
        error: Optional[str] = None,
        progress: int = 0
    ):
        """
        设置步骤状态
        
        Args:
            step_id: 步骤ID
            status: 状态
            result: 结果（可选）
            error: 错误信息（可选）
            progress: 进度（0-100）
        """
        if step_id not in self.states:
            self.states[step_id] = StepState(
                step_id=step_id,
                status=status
            )
        
        state = self.states[step_id]
        state.status = status
        state.progress = progress
        
        if status == StepStatus.RUNNING and not state.start_time:
            state.start_time = datetime.now()
        
        if status in [StepStatus.COMPLETED, StepStatus.FAILED]:
            state.end_time = datetime.now()
            state.progress = 100
        
        if result:
            state.result = result
        
        if error:
            state.error = error
        
        # 持久化状态
        self._save_state(state)
    
    def get_completed_steps(self) -> List[str]:
        """获取已完成的步骤ID列表"""
        return [
            step_id for step_id, state in self.states.items()
            if state.status == StepStatus.COMPLETED
        ]
    
    def get_failed_steps(self) -> List[str]:
        """获取失败的步骤ID列表"""
        return [
            step_id for step_id, state in self.states.items()
            if state.status == StepStatus.FAILED
        ]
    
    def reset_workflow(self):
        """重置工作流状态"""
        self.states.clear()
        self.workflow_id = None
        if self.db:
            # 清除数据库中的状态
            self.db.execute(
                "DELETE FROM workflow_states WHERE workflow_id = %s",
                (self.workflow_id,)
            )
    
    def _save_state(self, state: StepState):
        """保存状态到数据库"""
        if self.db and self.workflow_id:
            self.db.execute(
                """
                INSERT INTO workflow_states 
                (workflow_id, step_id, status, start_time, end_time, result, error, progress)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (workflow_id, step_id) 
                DO UPDATE SET 
                    status = EXCLUDED.status,
                    start_time = EXCLUDED.start_time,
                    end_time = EXCLUDED.end_time,
                    result = EXCLUDED.result,
                    error = EXCLUDED.error,
                    progress = EXCLUDED.progress
                """,
                (
                    self.workflow_id,
                    state.step_id,
                    state.status.value,
                    state.start_time,
                    state.end_time,
                    json.dumps(state.result) if state.result else None,
                    state.error,
                    state.progress
                )
            )
    
    def _load_states(self):
        """从数据库加载状态"""
        if self.db and self.workflow_id:
            rows = self.db.fetch_all(
                "SELECT * FROM workflow_states WHERE workflow_id = %s",
                (self.workflow_id,)
            )
            
            for row in rows:
                state = StepState(
                    step_id=row['step_id'],
                    status=StepStatus(row['status']),
                    start_time=row['start_time'],
                    end_time=row['end_time'],
                    result=json.loads(row['result']) if row['result'] else None,
                    error=row['error'],
                    progress=row['progress']
                )
                self.states[state.step_id] = state