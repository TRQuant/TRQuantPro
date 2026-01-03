"""
System Registry MCP工具

提供模块注册、状态管理、依赖检查的MCP工具
"""

from typing import Dict, Any, List, Optional
from .system_registry import SystemRegistry, ModuleStatus

# 全局注册表实例
_registry: Optional[SystemRegistry] = None


def get_registry() -> SystemRegistry:
    """获取注册表实例"""
    global _registry
    if _registry is None:
        _registry = SystemRegistry()
    return _registry


# MCP工具定义
REGISTRY_TOOLS = [
    {
        "name": "registry.register",
        "description": "注册模块到系统注册表",
        "handler": lambda args: get_registry().register_module(
            module_id=args.get("module_id", ""),
            name=args.get("name", ""),
            version=args.get("version", "1.0"),
            status=args.get("status", ModuleStatus.ACTIVE),
            mcp_server=args.get("mcp_server"),
            tools=args.get("tools", []),
            dependencies=args.get("dependencies", []),
            notes=args.get("notes", "")
        )
    },
    {
        "name": "registry.update",
        "description": "更新模块信息",
        "handler": lambda args: get_registry().update_module(
            args.get("module_id", ""),
            **{k: v for k, v in args.items() if k != "module_id"}
        ) or {"success": False, "error": "模块不存在"}
    },
    {
        "name": "registry.get",
        "description": "获取模块信息",
        "handler": lambda args: get_registry().get_module(args.get("module_id", "")) or {"error": "模块不存在"}
    },
    {
        "name": "registry.list",
        "description": "列出所有模块",
        "handler": lambda args: {"modules": get_registry().list_modules(status=args.get("status"))}
    },
    {
        "name": "registry.check_deps",
        "description": "检查模块依赖",
        "handler": lambda args: get_registry().check_dependencies(args.get("module_id", ""))
    },
    {
        "name": "registry.snapshot",
        "description": "创建系统状态快照",
        "handler": lambda args: get_registry().create_snapshot(args.get("description", ""))
    },
    {
        "name": "registry.changes",
        "description": "记录开发变更",
        "handler": lambda args: get_registry().record_change(
            module_id=args.get("module_id", ""),
            change_type=args.get("change_type", "update"),
            description=args.get("description", ""),
            files=args.get("files", [])
        )
    }
]


def call_registry_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """调用registry工具"""
    for tool in REGISTRY_TOOLS:
        if tool["name"] == name:
            try:
                result = tool["handler"](arguments)
                return result if isinstance(result, dict) else {"result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
    return {"success": False, "error": f"未知工具: {name}"}


def get_registry_tool_names() -> List[str]:
    """获取所有registry工具名称"""
    return [tool["name"] for tool in REGISTRY_TOOLS]
