"""
Strategy Pack MCP工具

提供策略管理的MCP接口

Author: TRQuant Team
Date: 2025-12-18
"""

from typing import Dict, Any, List
from mcp.types import Tool

from .strategy_pack import (
    get_strategy_registry, 
    StrategyConfig, 
    StrategyType,
    StrategyStatus
)


STRATEGY_TOOLS = [
    Tool(
        name="strategy.list",
        description="列出所有注册的策略",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="strategy.info",
        description="获取策略详情",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "策略名称"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="strategy.create",
        description="创建策略实例",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "策略名称"},
                "strategy_type": {
                    "type": "string",
                    "enum": ["factor", "tenbagger", "momentum"],
                    "description": "策略类型"
                },
                "params": {"type": "object", "description": "策略参数"},
                "max_position": {"type": "number", "default": 0.1},
                "stop_loss": {"type": "number", "default": 0.08}
            },
            "required": ["name", "strategy_type"]
        }
    ),
    Tool(
        name="strategy.run",
        description="运行策略生成信号",
        inputSchema={
            "type": "object",
            "properties": {
                "instance_key": {"type": "string", "description": "策略实例key"},
                "data": {"type": "object", "description": "市场数据"}
            },
            "required": ["instance_key"]
        }
    ),
    Tool(
        name="strategy.select",
        description="运行策略选股",
        inputSchema={
            "type": "object",
            "properties": {
                "instance_key": {"type": "string", "description": "策略实例key"},
                "universe": {"type": "array", "items": {"type": "string"}},
                "data": {"type": "object"}
            },
            "required": ["instance_key", "universe"]
        }
    ),
    Tool(
        name="strategy.instances",
        description="列出所有策略实例",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="strategy.stats",
        description="获取策略统计信息",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="strategy.types",
        description="列出支持的策略类型",
        inputSchema={"type": "object", "properties": {}}
    )
]


def _handle_strategy_list(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    strategies = registry.list_strategies()
    return {
        "status": "success",
        "count": len(strategies),
        "strategies": strategies
    }


def _handle_strategy_info(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    name = args.get("name", "")
    
    cls = registry.get_class(name)
    if not cls:
        return {"status": "error", "message": f"策略未找到: {name}"}
    
    meta = registry._metadata.get(name, {})
    return {
        "status": "success",
        "name": name,
        "class": cls.__name__,
        "type": meta.get("type", "unknown"),
        "description": meta.get("description", ""),
        "author": meta.get("author", "")
    }


def _handle_strategy_create(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    
    name = args.get("name", "")
    strategy_type = args.get("strategy_type", "factor")
    params = args.get("params", {})
    max_position = args.get("max_position", 0.1)
    stop_loss = args.get("stop_loss", 0.08)
    
    # 映射策略类型
    type_map = {
        "factor": StrategyType.FACTOR,
        "tenbagger": StrategyType.TENBAGGER,
        "momentum": StrategyType.MOMENTUM,
        "value": StrategyType.VALUE,
        "growth": StrategyType.GROWTH,
        "event": StrategyType.EVENT,
        "hybrid": StrategyType.HYBRID
    }
    
    config = StrategyConfig(
        name=f"{name}_instance",
        strategy_type=type_map.get(strategy_type, StrategyType.FACTOR),
        params=params,
        max_position=max_position,
        stop_loss=stop_loss
    )
    
    instance = registry.create_instance(strategy_type, config)
    if not instance:
        return {"status": "error", "message": f"创建失败，策略类型不存在: {strategy_type}"}
    
    instance.on_init()
    instance_key = f"{strategy_type}_{config.version}"
    
    return {
        "status": "success",
        "instance_key": instance_key,
        "info": instance.get_info()
    }


def _handle_strategy_run(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    
    instance_key = args.get("instance_key", "")
    data = args.get("data", {})
    
    instance = registry.get_instance(instance_key)
    if not instance:
        return {"status": "error", "message": f"策略实例未找到: {instance_key}"}
    
    signals = instance.generate_signals(data)
    return {
        "status": "success",
        "instance_key": instance_key,
        "signals_count": len(signals),
        "signals": signals
    }


def _handle_strategy_select(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    
    instance_key = args.get("instance_key", "")
    universe = args.get("universe", [])
    data = args.get("data", {})
    
    instance = registry.get_instance(instance_key)
    if not instance:
        return {"status": "error", "message": f"策略实例未找到: {instance_key}"}
    
    selected = instance.select_stocks(universe, data)
    return {
        "status": "success",
        "instance_key": instance_key,
        "universe_size": len(universe),
        "selected_count": len(selected),
        "selected": selected
    }


def _handle_strategy_instances(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    instances = registry.list_instances()
    return {
        "status": "success",
        "count": len(instances),
        "instances": instances
    }


def _handle_strategy_stats(args: Dict[str, Any]) -> Dict[str, Any]:
    registry = get_strategy_registry()
    stats = registry.get_stats()
    return {
        "status": "success",
        **stats
    }


def _handle_strategy_types(args: Dict[str, Any]) -> Dict[str, Any]:
    types = [
        {"name": "factor", "description": "多因子选股策略"},
        {"name": "tenbagger", "description": "十倍股识别策略"},
        {"name": "momentum", "description": "动量策略"},
        {"name": "value", "description": "价值投资策略"},
        {"name": "growth", "description": "成长股策略"},
        {"name": "event", "description": "事件驱动策略"},
        {"name": "hybrid", "description": "混合策略"}
    ]
    return {
        "status": "success",
        "count": len(types),
        "types": types
    }


STRATEGY_HANDLERS = {
    "strategy.list": _handle_strategy_list,
    "strategy.info": _handle_strategy_info,
    "strategy.create": _handle_strategy_create,
    "strategy.run": _handle_strategy_run,
    "strategy.select": _handle_strategy_select,
    "strategy.instances": _handle_strategy_instances,
    "strategy.stats": _handle_strategy_stats,
    "strategy.types": _handle_strategy_types
}
