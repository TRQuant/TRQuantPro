# -*- coding: utf-8 -*-
"""
工作流状态管理器
==============
实现工作流状态的持久化和断点续传
"""

import logging
from typing import Dict, Optional, Any, List
from datetime import datetime
from pathlib import Path
import json
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class WorkflowState:
    workflow_id: str
    name: str
    status: str = "pending"
    current_step: int = 0
    total_steps: int = 0
    steps: List[Dict] = None
    context: Dict = None
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.steps is None:
            self.steps = []
        if self.context is None:
            self.context = {}


class WorkflowStateManager:
    """工作流状态管理器"""
    
    WORKFLOW_9STEPS = [
        {"id": "data_source", "name": "信息获取", "mcp_tool": "data_source.check"},
        {"id": "market_trend", "name": "市场趋势", "mcp_tool": "market.status"},
        {"id": "mainline", "name": "投资主线", "mcp_tool": "market.mainlines"},
        {"id": "candidate_pool", "name": "候选池构建", "mcp_tool": "data_source.candidate_pool"},
        {"id": "factor", "name": "因子构建", "mcp_tool": "factor.recommend"},
        {"id": "strategy", "name": "策略生成", "mcp_tool": "strategy_template.generate"},
        {"id": "backtest", "name": "回测验证", "mcp_tool": "backtest.bullettrade"},
        {"id": "optimization", "name": "策略优化", "mcp_tool": "optimizer.optuna"},
        {"id": "report", "name": "报告生成", "mcp_tool": "report.generate"},
    ]
    
    # 保持向后兼容
    WORKFLOW_8STEPS = WORKFLOW_9STEPS[:8]
    
    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir or Path(__file__).parent.parent.parent / "data" / "workflow_states"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._mongo_db = None
        self._init_mongo()
    
    def _init_mongo(self):
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            self._mongo_db = client.get_database("trquant")
        except: pass
    
    def create_workflow(self, name: str = "9步骤工作流") -> WorkflowState:
        import uuid
        workflow = WorkflowState(
            workflow_id=str(uuid.uuid4())[:8],
            name=name,
            total_steps=9,
            steps=[{"id": s["id"], "name": s["name"], "status": "pending", "mcp_tool": s.get("mcp_tool")} for s in self.WORKFLOW_9STEPS],
            created_at=datetime.now().isoformat()
        )
        self._save(workflow)
        return workflow
    
    def start_step(self, workflow_id: str, step_index: int) -> bool:
        w = self._load(workflow_id)
        if not w or step_index >= len(w.steps):
            return False
        w.status = "running"
        w.current_step = step_index
        w.steps[step_index]["status"] = "running"
        w.steps[step_index]["started_at"] = datetime.now().isoformat()
        w.updated_at = datetime.now().isoformat()
        self._save(w)
        return True
    
    def complete_step(self, workflow_id: str, step_index: int, result: Dict = None) -> bool:
        w = self._load(workflow_id)
        if not w:
            return False
        w.steps[step_index]["status"] = "completed"
        w.steps[step_index]["result"] = result
        w.updated_at = datetime.now().isoformat()
        if all(s["status"] == "completed" for s in w.steps):
            w.status = "completed"
        self._save(w)
        return True
    
    def set_context(self, workflow_id: str, key: str, value: Any):
        w = self._load(workflow_id)
        if w:
            w.context[key] = value
            self._save(w)
    
    def get_context(self, workflow_id: str, key: str, default: Any = None) -> Any:
        w = self._load(workflow_id)
        return w.context.get(key, default) if w else default
    
    def resume_workflow(self, workflow_id: str) -> int:
        w = self._load(workflow_id)
        if not w:
            return -1
        for i, step in enumerate(w.steps):
            if step["status"] in ["pending", "failed"]:
                return i
        return -1
    
    # 公共API（简化版）
    def save_state(self, state: WorkflowState):
        """保存工作流状态"""
        if state.created_at is None:
            state.created_at = datetime.now().isoformat()
        state.updated_at = datetime.now().isoformat()
        self._save(state)
    
    def load_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """加载工作流状态"""
        return self._load(workflow_id)
    
    def list_workflows(self) -> List[WorkflowState]:
        """列出所有工作流"""
        workflows = []
        for f in self.storage_dir.glob("*.json"):
            try:
                w = self._load(f.stem)
                if w:
                    workflows.append(w)
            except: pass
        return workflows
    
    def _save(self, w: WorkflowState):
        data = asdict(w)
        with open(self.storage_dir / f"{w.workflow_id}.json", 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if self._mongo_db is not None:
            try:
                self._mongo_db.workflow_states.update_one({"workflow_id": w.workflow_id}, {"$set": data}, upsert=True)
            except: pass
    
    def _load(self, workflow_id: str) -> Optional[WorkflowState]:
        f = self.storage_dir / f"{workflow_id}.json"
        if f.exists():
            with open(f) as fp:
                return WorkflowState(**json.load(fp))
        return None


_mgr = None

def get_state_manager() -> WorkflowStateManager:
    global _mgr
    if _mgr is None:
        _mgr = WorkflowStateManager()
    return _mgr
