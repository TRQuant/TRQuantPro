"""Agent协调器

参考 MetaGPT 的多代理协作机制，实现任务分解、分配和协调
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent角色定义"""
    ARCHITECT = "architect"  # 架构设计师
    CODE_GENERATOR = "code_generator"  # 代码生成器
    QUALITY_CHECKER = "quality_checker"  # 质量检查器
    TEST_GENERATOR = "test_generator"  # 测试生成器
    DOCUMENTER = "documenter"  # 文档生成器


@dataclass
class Task:
    """任务定义
    
    Attributes:
        id: 任务唯一标识
        description: 任务描述
        role: 负责的Agent角色
        dependencies: 依赖的任务ID列表
        status: 任务状态 (pending, running, completed, failed)
        result: 任务执行结果
    """
    id: str
    description: str
    role: AgentRole
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    result: Optional[Any] = None


class AgentOrchestrator:
    """Agent协调器
    
    负责任务分解、分配和协调多个Agent协作
    
    参考: MetaGPT 的 Multi-Agent Framework
    """
    
    def __init__(self):
        """初始化协调器"""
        self.agents: Dict[AgentRole, Any] = {}
        self.tasks: List[Task] = []
        self.results: Dict[str, Any] = {}
        self.execution_log: List[Dict[str, Any]] = []
    
    def register_agent(self, role: AgentRole, agent: Any) -> None:
        """注册Agent
        
        Args:
            role: Agent角色
            agent: Agent实例
        """
        self.agents[role] = agent
        logger.info(f"Registered agent: {role.value}")
    
    def decompose_task(self, requirement: str) -> List[Task]:
        """分解任务
        
        根据需求自动分解为多个子任务，参考MetaGPT的任务分解机制
        
        Args:
            requirement: 需求描述
            
        Returns:
            任务列表
        """
        # 这里应该调用Architect Agent来分解任务
        # 目前先返回示例任务结构
        tasks = [
            Task(
                id="arch_001",
                description="设计BulletTrade模块架构",
                role=AgentRole.ARCHITECT,
                dependencies=[]
            ),
            Task(
                id="code_001",
                description="实现BulletTrade引擎封装",
                role=AgentRole.CODE_GENERATOR,
                dependencies=["arch_001"]
            ),
            Task(
                id="quality_001",
                description="检查代码质量",
                role=AgentRole.QUALITY_CHECKER,
                dependencies=["code_001"]
            )
        ]
        
        return tasks
    
    def execute_task(self, task: Task) -> Any:
        """执行任务
        
        Args:
            task: 要执行的任务
            
        Returns:
            任务执行结果
            
        Raises:
            ValueError: 如果Agent未注册或依赖未完成
        """
        # 检查Agent是否注册
        agent = self.agents.get(task.role)
        if not agent:
            raise ValueError(f"Agent {task.role.value} not registered")
        
        # 检查依赖是否完成
        for dep_id in task.dependencies:
            if dep_id not in self.results:
                raise ValueError(f"Dependency {dep_id} not completed")
        
        # 更新任务状态
        task.status = "running"
        logger.info(f"Executing task: {task.id} ({task.description})")
        
        try:
            # 执行任务
            result = agent.execute(task, self.results)
            
            # 保存结果
            task.result = result
            task.status = "completed"
            self.results[task.id] = result
            
            # 记录执行日志
            self.execution_log.append({
                "task_id": task.id,
                "status": "completed",
                "timestamp": self._get_timestamp()
            })
            
            logger.info(f"Task {task.id} completed successfully")
            return result
            
        except Exception as e:
            task.status = "failed"
            logger.error(f"Task {task.id} failed: {e}", exc_info=True)
            raise
    
    def run(self, requirement: str) -> Dict[str, Any]:
        """运行完整工作流
        
        Args:
            requirement: 需求描述
            
        Returns:
            所有任务的执行结果
        """
        logger.info(f"Starting workflow for requirement: {requirement[:50]}...")
        
        # 1. 任务分解
        tasks = self.decompose_task(requirement)
        self.tasks = tasks
        logger.info(f"Decomposed into {len(tasks)} tasks")
        
        # 2. 按依赖顺序执行
        completed = set()
        max_iterations = len(tasks) * 2  # 防止无限循环
        iteration = 0
        
        while len(completed) < len(tasks) and iteration < max_iterations:
            iteration += 1
            progress_made = False
            
            for task in tasks:
                if task.id in completed:
                    continue
                
                # 检查依赖是否完成
                deps_ready = all(
                    dep_id in completed
                    for dep_id in task.dependencies
                )
                
                if deps_ready:
                    try:
                        self.execute_task(task)
                        completed.add(task.id)
                        progress_made = True
                    except Exception as e:
                        logger.error(f"Task {task.id} failed: {e}")
                        # 可以选择继续或停止
                        raise
            
            if not progress_made:
                # 检测死锁
                remaining = [t.id for t in tasks if t.id not in completed]
                logger.error(f"Deadlock detected. Remaining tasks: {remaining}")
                raise RuntimeError("Workflow deadlock detected")
        
        if len(completed) < len(tasks):
            raise RuntimeError(f"Workflow incomplete. Completed: {len(completed)}/{len(tasks)}")
        
        logger.info("Workflow completed successfully")
        return self.results
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_status(self) -> Dict[str, Any]:
        """获取工作流状态"""
        return {
            "total_tasks": len(self.tasks),
            "completed_tasks": len([t for t in self.tasks if t.status == "completed"]),
            "failed_tasks": len([t for t in self.tasks if t.status == "failed"]),
            "pending_tasks": len([t for t in self.tasks if t.status == "pending"]),
            "execution_log": self.execution_log
        }

