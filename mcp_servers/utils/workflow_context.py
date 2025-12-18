#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
WorkflowContext - 工作流上下文管理
=================================

M1里程碑核心组件：实现步骤间数据自动传递

功能：
1. 步骤输出自动流入下游步骤输入
2. 上下文数据版本追踪
3. 数据依赖图谱
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field, asdict
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class StepOutput:
    """步骤输出数据"""
    step_id: str
    output_key: str
    value: Any
    data_type: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    hash: str = ""
    
    def __post_init__(self):
        if not self.hash:
            self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """计算数据哈希"""
        try:
            content = json.dumps(self.value, sort_keys=True, default=str)
            return hashlib.md5(content.encode()).hexdigest()[:8]
        except:
            return "unknown"


@dataclass
class DataDependency:
    """数据依赖关系"""
    from_step: str
    from_key: str
    to_step: str
    to_key: str
    transform: Optional[str] = None  # 可选的数据转换函数名


class WorkflowContext:
    """
    工作流上下文 - 管理步骤间数据流
    
    核心特性：
    1. 自动数据传递：上游步骤输出自动成为下游步骤输入
    2. 数据版本追踪：每个数据有唯一hash
    3. 依赖图谱：清晰的数据流向
    """
    
    # 9步工作流数据依赖定义
    DEFAULT_DEPENDENCIES = [
        # 市场趋势 → 投资主线
        DataDependency("market_trend", "market_status", "mainline", "market_context"),
        # 投资主线 → 候选池
        DataDependency("mainline", "mainlines", "candidate_pool", "sector_hints"),
        # 候选池 → 因子构建
        DataDependency("candidate_pool", "stocks", "factor", "stock_pool"),
        # 市场趋势 → 因子构建
        DataDependency("market_trend", "regime", "factor", "market_regime"),
        # 因子构建 → 策略生成
        DataDependency("factor", "factors", "strategy", "factor_list"),
        DataDependency("candidate_pool", "stocks", "strategy", "stock_pool"),
        # 策略生成 → 回测
        DataDependency("strategy", "code", "backtest", "strategy_code"),
        DataDependency("candidate_pool", "stocks", "backtest", "stock_pool"),
        # 回测 → 优化
        DataDependency("backtest", "result", "optimization", "baseline_result"),
        DataDependency("strategy", "params", "optimization", "param_config"),
        # 优化 → 报告
        DataDependency("optimization", "best_params", "report", "optimized_params"),
        DataDependency("backtest", "result", "report", "backtest_result"),
    ]
    
    def __init__(self, workflow_id: str, storage_path: Optional[Path] = None):
        self.workflow_id = workflow_id
        self.storage_path = storage_path or Path(__file__).parent.parent.parent / "data" / "workflow_contexts"
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self._outputs: Dict[str, Dict[str, StepOutput]] = {}  # {step_id: {key: StepOutput}}
        self._dependencies: List[DataDependency] = list(self.DEFAULT_DEPENDENCIES)
        self._transforms: Dict[str, Callable] = {}
        self._metadata: Dict[str, Any] = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # 尝试加载已有上下文
        self._load()
    
    def set_output(self, step_id: str, key: str, value: Any, data_type: str = "auto") -> StepOutput:
        """
        设置步骤输出
        
        Args:
            step_id: 步骤ID
            key: 输出键名
            value: 输出值
            data_type: 数据类型（auto自动推断）
        
        Returns:
            StepOutput对象
        """
        if data_type == "auto":
            data_type = type(value).__name__
        
        output = StepOutput(
            step_id=step_id,
            output_key=key,
            value=value,
            data_type=data_type
        )
        
        if step_id not in self._outputs:
            self._outputs[step_id] = {}
        self._outputs[step_id][key] = output
        
        self._metadata["updated_at"] = datetime.now().isoformat()
        self._save()
        
        logger.info(f"[Context] 设置输出: {step_id}.{key} (hash: {output.hash})")
        return output
    
    def get_input(self, step_id: str, key: str, default: Any = None) -> Any:
        """
        获取步骤输入（从上游依赖自动获取）
        
        Args:
            step_id: 步骤ID
            key: 输入键名
            default: 默认值
        
        Returns:
            输入值
        """
        # 查找依赖关系
        for dep in self._dependencies:
            if dep.to_step == step_id and dep.to_key == key:
                from_output = self._outputs.get(dep.from_step, {}).get(dep.from_key)
                if from_output:
                    value = from_output.value
                    # 应用转换
                    if dep.transform and dep.transform in self._transforms:
                        value = self._transforms[dep.transform](value)
                    logger.debug(f"[Context] 获取输入: {step_id}.{key} <- {dep.from_step}.{dep.from_key}")
                    return value
        
        return default
    
    def get_all_inputs(self, step_id: str) -> Dict[str, Any]:
        """获取步骤的所有输入"""
        inputs = {}
        for dep in self._dependencies:
            if dep.to_step == step_id:
                value = self.get_input(step_id, dep.to_key)
                if value is not None:
                    inputs[dep.to_key] = value
        return inputs
    
    def get_output(self, step_id: str, key: str) -> Optional[StepOutput]:
        """直接获取步骤输出"""
        return self._outputs.get(step_id, {}).get(key)
    
    def get_all_outputs(self, step_id: str) -> Dict[str, Any]:
        """获取步骤的所有输出值"""
        return {k: v.value for k, v in self._outputs.get(step_id, {}).items()}
    
    def add_dependency(self, from_step: str, from_key: str, to_step: str, to_key: str, transform: str = None):
        """添加自定义依赖"""
        dep = DataDependency(from_step, from_key, to_step, to_key, transform)
        self._dependencies.append(dep)
    
    def register_transform(self, name: str, func: Callable):
        """注册数据转换函数"""
        self._transforms[name] = func
    
    def get_data_flow(self) -> Dict[str, Any]:
        """获取数据流图谱"""
        flow = {"nodes": [], "edges": []}
        
        # 收集所有步骤节点
        steps = set()
        for dep in self._dependencies:
            steps.add(dep.from_step)
            steps.add(dep.to_step)
        
        for step in steps:
            outputs = list(self._outputs.get(step, {}).keys())
            flow["nodes"].append({
                "id": step,
                "outputs": outputs,
                "has_data": len(outputs) > 0
            })
        
        # 添加边
        for dep in self._dependencies:
            flow["edges"].append({
                "from": f"{dep.from_step}.{dep.from_key}",
                "to": f"{dep.to_step}.{dep.to_key}",
                "transform": dep.transform
            })
        
        return flow
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        return {
            "workflow_id": self.workflow_id,
            "metadata": self._metadata,
            "outputs": {
                step_id: {key: asdict(output) for key, output in outputs.items()}
                for step_id, outputs in self._outputs.items()
            },
            "dependencies": [asdict(d) for d in self._dependencies if d not in self.DEFAULT_DEPENDENCIES]
        }
    
    def _save(self):
        """保存上下文到文件"""
        file_path = self.storage_path / f"{self.workflow_id}_context.json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"保存上下文失败: {e}")
    
    def _load(self):
        """从文件加载上下文"""
        file_path = self.storage_path / f"{self.workflow_id}_context.json"
        if not file_path.exists():
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self._metadata = data.get("metadata", self._metadata)
            
            # 恢复输出
            for step_id, outputs in data.get("outputs", {}).items():
                self._outputs[step_id] = {}
                for key, output_data in outputs.items():
                    self._outputs[step_id][key] = StepOutput(**output_data)
            
            logger.info(f"[Context] 已加载上下文: {self.workflow_id}")
        except Exception as e:
            logger.warning(f"加载上下文失败: {e}")


# 全局上下文管理
_contexts: Dict[str, WorkflowContext] = {}

def get_context(workflow_id: str) -> WorkflowContext:
    """获取或创建工作流上下文"""
    if workflow_id not in _contexts:
        _contexts[workflow_id] = WorkflowContext(workflow_id)
    return _contexts[workflow_id]

def clear_context(workflow_id: str):
    """清除工作流上下文"""
    if workflow_id in _contexts:
        del _contexts[workflow_id]
