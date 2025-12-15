# -*- coding: utf-8 -*-
"""
增强型工作流编排器
==================

支持：
- 8+1步骤完整工作流
- 断点续传
- 并行执行
- 工作流模板
"""
import logging
import time
import json
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from enum import Enum
import threading

logger = logging.getLogger(__name__)


class WorkflowStepStatus(Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowStep:
    """工作流步骤"""
    id: str
    name: str
    description: str
    func: Optional[Callable] = None
    status: WorkflowStepStatus = WorkflowStepStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    dependencies: List[str] = field(default_factory=list)
    
    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "duration": self.duration,
            "error": self.error,
        }


@dataclass
class WorkflowConfig:
    """工作流配置"""
    name: str = "TRQuant工作流"
    start_date: str = ""
    end_date: str = ""
    initial_capital: float = 1000000.0
    benchmark: str = "000300.XSHG"
    auto_optimize: bool = True
    save_to_db: bool = True
    generate_report: bool = True
    backtest_engine: str = "bullettrade"  # bullettrade/qmt/fast
    optimization_trials: int = 30
    parallel_steps: bool = False


class EnhancedWorkflowOrchestrator:
    """增强型工作流编排器"""
    
    # 标准8+1步骤定义
    STANDARD_STEPS = [
        {"id": "data_check", "name": "数据源检查", "desc": "检查数据源可用性"},
        {"id": "market_trend", "name": "市场趋势分析", "desc": "分析大盘走势和市场情绪"},
        {"id": "mainline", "name": "投资主线识别", "desc": "识别当前市场热点主线"},
        {"id": "candidate_pool", "name": "候选池构建", "desc": "构建股票候选池"},
        {"id": "factor_recommend", "name": "因子推荐", "desc": "推荐适合当前市场的因子"},
        {"id": "strategy_gen", "name": "策略生成", "desc": "生成策略代码"},
        {"id": "backtest", "name": "回测验证", "desc": "执行策略回测"},
        {"id": "optimize", "name": "策略优化", "desc": "优化策略参数"},
        {"id": "report", "name": "报告生成", "desc": "生成最终报告"},
    ]
    
    def __init__(self, config: Optional[WorkflowConfig] = None):
        self.config = config or WorkflowConfig()
        self.steps: Dict[str, WorkflowStep] = {}
        self.workflow_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._state_file = Path(f"workflow_state_{self.workflow_id}.json")
        self._db = None
        self._init_db()
        self._init_steps()
    
    def _init_db(self):
        """初始化数据库"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=5000)
            self._db = client["trquant"]
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.warning(f"MongoDB连接失败: {e}")
    
    def _init_steps(self):
        """初始化步骤"""
        for step_def in self.STANDARD_STEPS:
            self.steps[step_def["id"]] = WorkflowStep(
                id=step_def["id"],
                name=step_def["name"],
                description=step_def["desc"],
            )
        
        # 设置依赖关系
        self.steps["market_trend"].dependencies = ["data_check"]
        self.steps["mainline"].dependencies = ["market_trend"]
        self.steps["candidate_pool"].dependencies = ["mainline"]
        self.steps["factor_recommend"].dependencies = ["candidate_pool"]
        self.steps["strategy_gen"].dependencies = ["factor_recommend"]
        self.steps["backtest"].dependencies = ["strategy_gen"]
        self.steps["optimize"].dependencies = ["backtest"]
        self.steps["report"].dependencies = ["optimize"]
    
    def register_step_handler(self, step_id: str, handler: Callable):
        """注册步骤处理器"""
        if step_id in self.steps:
            self.steps[step_id].func = handler
    
    def save_state(self):
        """保存工作流状态"""
        state = {
            "workflow_id": self.workflow_id,
            "config": {
                "name": self.config.name,
                "start_date": self.config.start_date,
                "end_date": self.config.end_date,
            },
            "steps": {k: v.to_dict() for k, v in self.steps.items()},
            "timestamp": datetime.now().isoformat(),
        }
        
        self._state_file.write_text(json.dumps(state, ensure_ascii=False, indent=2))
        
        if self._db is not None:
            self._db.workflow_states.replace_one(
                {"workflow_id": self.workflow_id},
                state,
                upsert=True
            )
    
    def load_state(self, state_file: Optional[Path] = None) -> bool:
        """加载工作流状态"""
        file_path = state_file or self._state_file
        if not file_path.exists():
            return False
        
        try:
            state = json.loads(file_path.read_text())
            self.workflow_id = state["workflow_id"]
            
            for step_id, step_state in state["steps"].items():
                if step_id in self.steps:
                    self.steps[step_id].status = WorkflowStepStatus(step_state["status"])
            
            logger.info(f"已恢复工作流状态: {self.workflow_id}")
            return True
        except Exception as e:
            logger.error(f"加载状态失败: {e}")
            return False
    
    def run_step(self, step_id: str) -> bool:
        """执行单个步骤"""
        if step_id not in self.steps:
            logger.error(f"未知步骤: {step_id}")
            return False
        
        step = self.steps[step_id]
        
        # 检查依赖
        for dep_id in step.dependencies:
            dep = self.steps.get(dep_id)
            if dep and dep.status != WorkflowStepStatus.COMPLETED:
                logger.error(f"依赖步骤未完成: {dep_id}")
                return False
        
        # 执行步骤
        step.status = WorkflowStepStatus.RUNNING
        step.start_time = time.time()
        self.save_state()
        
        try:
            if step.func:
                result = step.func()
                step.result = result if isinstance(result, dict) else {"result": result}
            else:
                # 使用默认处理器
                result = self._default_handler(step_id)
                step.result = result
            
            step.status = WorkflowStepStatus.COMPLETED
            step.end_time = time.time()
            logger.info(f"✅ 步骤完成: {step.name} ({step.duration:.2f}s)")
            
        except Exception as e:
            step.status = WorkflowStepStatus.FAILED
            step.error = str(e)
            step.end_time = time.time()
            logger.error(f"❌ 步骤失败: {step.name} - {e}")
            return False
        
        self.save_state()
        return True
    
    def _default_handler(self, step_id: str) -> Dict:
        """默认步骤处理器"""
        from core.workflow_orchestrator import get_workflow_orchestrator
        orchestrator = get_workflow_orchestrator()
        
        handlers = {
            "data_check": orchestrator.check_data_sources,
            "market_trend": orchestrator.analyze_market_trend,
            "mainline": orchestrator.identify_mainlines,
            "candidate_pool": orchestrator.build_candidate_pool,
            "factor_recommend": orchestrator.recommend_factors,
            "strategy_gen": orchestrator.generate_strategy,
            "backtest": orchestrator.backtest_strategy,
            "optimize": orchestrator.optimize_strategy,
            "report": orchestrator.generate_final_report,
        }
        
        if step_id in handlers:
            result = handlers[step_id]()
            return {"success": result.success, "summary": result.summary, "details": result.details}
        
        return {"success": True, "message": f"步骤{step_id}完成"}
    
    def run_all(self, resume: bool = False, callback: Optional[Callable] = None) -> Dict:
        """执行所有步骤"""
        start_time = time.time()
        
        if resume:
            self.load_state()
        
        results = {}
        failed_steps = []
        
        for step_id in [s["id"] for s in self.STANDARD_STEPS]:
            step = self.steps[step_id]
            
            # 跳过已完成的步骤（断点续传）
            if resume and step.status == WorkflowStepStatus.COMPLETED:
                logger.info(f"⏭️ 跳过已完成步骤: {step.name}")
                results[step_id] = {"status": "skipped", "reason": "已完成"}
                continue
            
            # 跳过可选步骤
            if step_id == "optimize" and not self.config.auto_optimize:
                step.status = WorkflowStepStatus.SKIPPED
                continue
            
            if step_id == "report" and not self.config.generate_report:
                step.status = WorkflowStepStatus.SKIPPED
                continue
            
            # 执行步骤
            success = self.run_step(step_id)
            results[step_id] = step.to_dict()
            
            if callback:
                callback(step_id, step)
            
            if not success:
                failed_steps.append(step_id)
                # 继续执行不依赖失败步骤的其他步骤
        
        total_time = time.time() - start_time
        
        return {
            "workflow_id": self.workflow_id,
            "success": len(failed_steps) == 0,
            "total_time": f"{total_time:.2f}s",
            "completed_steps": sum(1 for s in self.steps.values() if s.status == WorkflowStepStatus.COMPLETED),
            "failed_steps": failed_steps,
            "results": results,
        }
    
    def get_status(self) -> Dict:
        """获取工作流状态"""
        return {
            "workflow_id": self.workflow_id,
            "steps": [
                {
                    "id": step.id,
                    "name": step.name,
                    "status": step.status.value,
                    "duration": step.duration,
                }
                for step in self.steps.values()
            ],
            "progress": sum(1 for s in self.steps.values() if s.status == WorkflowStepStatus.COMPLETED) / len(self.steps) * 100,
        }


# 工厂函数
def create_workflow(
    name: str = "默认工作流",
    start_date: str = "",
    end_date: str = "",
    **kwargs
) -> EnhancedWorkflowOrchestrator:
    """创建工作流"""
    config = WorkflowConfig(
        name=name,
        start_date=start_date,
        end_date=end_date,
        **kwargs
    )
    return EnhancedWorkflowOrchestrator(config)
