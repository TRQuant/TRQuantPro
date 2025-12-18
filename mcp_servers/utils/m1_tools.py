#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
M1 MCP工具接口
=============

提供WorkflowContext、DataSnapshot、Experiment的MCP工具
"""

from typing import Dict, Any, List
from .workflow_context import get_context, clear_context, WorkflowContext
from .data_snapshot import get_snapshot_manager, DataSnapshot
from .experiment import get_experiment_tracker, ExperimentConfig, ExperimentMetrics


# ==================== WorkflowContext 工具 ====================

def context_set_output(workflow_id: str, step_id: str, key: str, value: Any, data_type: str = "auto") -> Dict[str, Any]:
    """设置步骤输出"""
    ctx = get_context(workflow_id)
    output = ctx.set_output(step_id, key, value, data_type)
    return {
        "success": True,
        "step_id": step_id,
        "key": key,
        "hash": output.hash,
        "data_type": output.data_type
    }


def context_get_input(workflow_id: str, step_id: str, key: str) -> Dict[str, Any]:
    """获取步骤输入（从上游依赖自动获取）"""
    ctx = get_context(workflow_id)
    value = ctx.get_input(step_id, key)
    return {
        "success": value is not None,
        "step_id": step_id,
        "key": key,
        "value": value
    }


def context_get_all_inputs(workflow_id: str, step_id: str) -> Dict[str, Any]:
    """获取步骤的所有输入"""
    ctx = get_context(workflow_id)
    inputs = ctx.get_all_inputs(step_id)
    return {
        "success": True,
        "step_id": step_id,
        "inputs": inputs,
        "count": len(inputs)
    }


def context_get_data_flow(workflow_id: str) -> Dict[str, Any]:
    """获取数据流图谱"""
    ctx = get_context(workflow_id)
    flow = ctx.get_data_flow()
    return {
        "success": True,
        "workflow_id": workflow_id,
        "flow": flow
    }


def context_clear(workflow_id: str) -> Dict[str, Any]:
    """清除工作流上下文"""
    clear_context(workflow_id)
    return {"success": True, "workflow_id": workflow_id}


# ==================== DataSnapshot 工具 ====================

def snapshot_create(
    name: str,
    data: Any,
    data_source: str = "unknown",
    data_type: str = "generic",
    symbols: List[str] = None,
    start_date: str = "",
    end_date: str = "",
    description: str = "",
    tags: List[str] = None
) -> Dict[str, Any]:
    """创建数据快照"""
    manager = get_snapshot_manager()
    snapshot = manager.create_snapshot(
        name=name,
        data=data,
        data_source=data_source,
        data_type=data_type,
        symbols=symbols,
        start_date=start_date,
        end_date=end_date,
        description=description,
        tags=tags
    )
    return {
        "success": True,
        "snapshot_id": snapshot.snapshot_id,
        "data_hash": snapshot.data_hash,
        "row_count": snapshot.row_count,
        "column_count": snapshot.column_count
    }


def snapshot_get(snapshot_id: str) -> Dict[str, Any]:
    """获取快照元数据"""
    manager = get_snapshot_manager()
    snapshot = manager.get_snapshot(snapshot_id)
    if not snapshot:
        return {"success": False, "error": "快照不存在"}
    return {
        "success": True,
        "snapshot": snapshot.to_dict()
    }


def snapshot_list(
    data_type: str = None,
    data_source: str = None,
    tags: List[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """列出快照"""
    manager = get_snapshot_manager()
    snapshots = manager.list_snapshots(data_type, data_source, tags, limit)
    return {
        "success": True,
        "snapshots": snapshots,
        "count": len(snapshots)
    }


def snapshot_compare(snapshot_id_1: str, snapshot_id_2: str) -> Dict[str, Any]:
    """对比两个快照"""
    manager = get_snapshot_manager()
    comparison = manager.compare_snapshots(snapshot_id_1, snapshot_id_2)
    return {
        "success": "error" not in comparison,
        **comparison
    }


def snapshot_delete(snapshot_id: str) -> Dict[str, Any]:
    """删除快照"""
    manager = get_snapshot_manager()
    success = manager.delete_snapshot(snapshot_id)
    return {"success": success, "snapshot_id": snapshot_id}


# ==================== Experiment 工具 ====================

def experiment_create(
    name: str,
    description: str = "",
    strategy_pack: str = "",
    strategy_version: str = "",
    tags: List[str] = None
) -> Dict[str, Any]:
    """创建实验"""
    tracker = get_experiment_tracker()
    config = ExperimentConfig(
        strategy_pack=strategy_pack,
        strategy_version=strategy_version
    )
    experiment = tracker.create_experiment(
        name=name,
        config=config,
        description=description,
        tags=tags
    )
    return {
        "success": True,
        "experiment_id": experiment.experiment_id,
        "name": experiment.name
    }


def experiment_start(experiment_id: str) -> Dict[str, Any]:
    """开始实验"""
    tracker = get_experiment_tracker()
    success = tracker.start_experiment(experiment_id)
    return {"success": success, "experiment_id": experiment_id}


def experiment_complete(
    experiment_id: str,
    total_return: float = 0.0,
    annual_return: float = 0.0,
    sharpe_ratio: float = 0.0,
    max_drawdown: float = 0.0,
    win_rate: float = 0.0,
    notes: str = ""
) -> Dict[str, Any]:
    """完成实验"""
    tracker = get_experiment_tracker()
    metrics = ExperimentMetrics(
        total_return=total_return,
        annual_return=annual_return,
        sharpe_ratio=sharpe_ratio,
        max_drawdown=max_drawdown,
        win_rate=win_rate
    )
    success = tracker.complete_experiment(experiment_id, metrics, notes)
    return {"success": success, "experiment_id": experiment_id}


def experiment_get(experiment_id: str) -> Dict[str, Any]:
    """获取实验详情"""
    tracker = get_experiment_tracker()
    experiment = tracker.get_experiment(experiment_id)
    if not experiment:
        return {"success": False, "error": "实验不存在"}
    return {
        "success": True,
        "experiment": experiment.to_dict()
    }


def experiment_list(
    status: str = None,
    strategy_pack: str = None,
    tags: List[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """列出实验"""
    tracker = get_experiment_tracker()
    experiments = tracker.list_experiments(status, strategy_pack, tags, limit)
    return {
        "success": True,
        "experiments": [e.to_dict() for e in experiments],
        "count": len(experiments)
    }


def experiment_compare(exp_id_1: str, exp_id_2: str) -> Dict[str, Any]:
    """对比两个实验"""
    tracker = get_experiment_tracker()
    comparison = tracker.compare_experiments(exp_id_1, exp_id_2)
    return {
        "success": "error" not in comparison,
        **comparison
    }


def experiment_link_snapshot(experiment_id: str, snapshot_id: str) -> Dict[str, Any]:
    """关联数据快照"""
    tracker = get_experiment_tracker()
    success = tracker.link_snapshot(experiment_id, snapshot_id)
    return {"success": success}


def experiment_link_workflow(experiment_id: str, workflow_id: str) -> Dict[str, Any]:
    """关联工作流"""
    tracker = get_experiment_tracker()
    success = tracker.link_workflow(experiment_id, workflow_id)
    return {"success": success}


def experiment_export(experiment_id: str) -> Dict[str, Any]:
    """导出实验"""
    tracker = get_experiment_tracker()
    path = tracker.export_experiment(experiment_id)
    return {
        "success": bool(path),
        "export_path": path
    }


# ==================== MCP工具定义 ====================

M1_TOOLS = [
    # Context工具
    {"name": "context.set_output", "description": "设置步骤输出", "handler": context_set_output},
    {"name": "context.get_input", "description": "获取步骤输入（自动从上游获取）", "handler": context_get_input},
    {"name": "context.get_all_inputs", "description": "获取步骤所有输入", "handler": context_get_all_inputs},
    {"name": "context.get_data_flow", "description": "获取数据流图谱", "handler": context_get_data_flow},
    {"name": "context.clear", "description": "清除上下文", "handler": context_clear},
    
    # Snapshot工具
    {"name": "snapshot.create", "description": "创建数据快照", "handler": snapshot_create},
    {"name": "snapshot.get", "description": "获取快照", "handler": snapshot_get},
    {"name": "snapshot.list", "description": "列出快照", "handler": snapshot_list},
    {"name": "snapshot.compare", "description": "对比快照", "handler": snapshot_compare},
    {"name": "snapshot.delete", "description": "删除快照", "handler": snapshot_delete},
    
    # Experiment工具
    {"name": "experiment.create", "description": "创建实验", "handler": experiment_create},
    {"name": "experiment.start", "description": "开始实验", "handler": experiment_start},
    {"name": "experiment.complete", "description": "完成实验", "handler": experiment_complete},
    {"name": "experiment.get", "description": "获取实验", "handler": experiment_get},
    {"name": "experiment.list", "description": "列出实验", "handler": experiment_list},
    {"name": "experiment.compare", "description": "对比实验", "handler": experiment_compare},
    {"name": "experiment.link_snapshot", "description": "关联快照", "handler": experiment_link_snapshot},
    {"name": "experiment.link_workflow", "description": "关联工作流", "handler": experiment_link_workflow},
    {"name": "experiment.export", "description": "导出实验", "handler": experiment_export},
]


def get_m1_tool_names() -> List[str]:
    """获取所有M1工具名称"""
    return [t["name"] for t in M1_TOOLS]


def call_m1_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """调用M1工具"""
    for tool in M1_TOOLS:
        if tool["name"] == tool_name:
            return tool["handler"](**kwargs)
    return {"success": False, "error": f"未知工具: {tool_name}"}
