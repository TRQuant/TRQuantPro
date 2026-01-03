"""
Issue Tracker MCP工具

提供问题记录、搜索、解决方案管理的MCP工具
"""

from typing import Dict, Any, List, Optional
from .issue_tracker import (
    record_issue,
    search_issue,
    list_issues,
    record_solution,
    get_solution,
    record_pattern,
    search_pattern,
    quick_debug
)

# MCP工具定义
ISSUE_TOOLS = [
    {
        "name": "issue.record",
        "description": "记录一个问题",
        "handler": lambda args: record_issue(
            title=args.get("title", ""),
            description=args.get("description", ""),
            error_message=args.get("error_message", ""),
            category=args.get("category", "general"),
            tags=args.get("tags", [])
        )
    },
    {
        "name": "issue.search",
        "description": "搜索已知问题",
        "handler": lambda args: search_issue(args.get("query", ""))
    },
    {
        "name": "issue.list",
        "description": "列出问题",
        "handler": lambda args: list_issues(
            status=args.get("status"),
            category=args.get("category")
        )
    },
    {
        "name": "issue.solution",
        "description": "记录问题的解决方案",
        "handler": lambda args: record_solution(
            issue_id=args.get("issue_id", ""),
            solution=args.get("solution", ""),
            code_snippet=args.get("code_snippet", ""),
            tags=args.get("tags", [])
        )
    },
    {
        "name": "issue.get_solution",
        "description": "获取问题的解决方案",
        "handler": lambda args: get_solution(args.get("issue_id", ""))
    },
    {
        "name": "issue.pattern",
        "description": "记录代码模式",
        "handler": lambda args: record_pattern(
            pattern_name=args.get("pattern_name", ""),
            description=args.get("description", ""),
            code_snippet=args.get("code_snippet", ""),
            use_cases=args.get("use_cases", []),
            tags=args.get("tags", [])
        )
    },
    {
        "name": "issue.search_pattern",
        "description": "搜索代码模式",
        "handler": lambda args: search_pattern(args.get("query", ""))
    },
    {
        "name": "issue.quick_debug",
        "description": "快速调试：搜索问题并返回解决方案",
        "handler": lambda args: quick_debug(
            error_message=args.get("error_message", ""),
            context=args.get("context", "")
        )
    }
]


def call_issue_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """调用issue工具"""
    for tool in ISSUE_TOOLS:
        if tool["name"] == name:
            try:
                return tool["handler"](arguments)
            except Exception as e:
                return {"success": False, "error": str(e)}
    return {"success": False, "error": f"未知工具: {name}"}


def get_issue_tool_names() -> List[str]:
    """获取所有issue工具名称"""
    return [tool["name"] for tool in ISSUE_TOOLS]
