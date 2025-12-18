#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 开发任务管理服务器 (合并版)
===================================

合并了 task_server.py 和 task_optimizer_server.py 的功能
提供完整的任务管理和优化工具

运行方式:
    python mcp_servers/dev_task_server.py

功能:
    - 任务管理: task.list, task.create, task.get, task.update, task.complete
    - 任务优化: task.analyze, task.recommend_mode, task.cache_context
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('DevTaskServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}")
    sys.exit(1)

# 创建服务器
server = Server("trquant-dev-task")

# 任务目录
TASKS_DIR = TRQUANT_ROOT / ".taorui" / "artifacts" / "tasks"
TASKS_DIR.mkdir(parents=True, exist_ok=True)

# 任务状态枚举
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

# 上下文缓存（用于任务优化）
_context_cache = {}


def load_tasks(project: str = "default") -> Dict[str, Any]:
    """加载任务树"""
    tasks_file = TASKS_DIR / f"{project}.json"
    
    if tasks_file.exists():
        try:
            return json.loads(tasks_file.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"加载任务文件失败: {e}")
    
    return {
        "project": project,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "tasks": []
    }


def save_tasks(tasks_data: Dict[str, Any]) -> None:
    """保存任务树"""
    project = tasks_data.get("project", "default")
    tasks_file = TASKS_DIR / f"{project}.json"
    
    tasks_data["updated"] = datetime.now().isoformat()
    tasks_file.write_text(
        json.dumps(tasks_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )


def find_task(tasks: List[Dict[str, Any]], task_id: str) -> Optional[Dict[str, Any]]:
    """查找任务（递归）"""
    for task in tasks:
        if task.get("id") == task_id:
            return task
        if "subtasks" in task:
            found = find_task(task["subtasks"], task_id)
            if found:
                return found
    return None


def create_task(
    title: str,
    description: str = "",
    status: str = TaskStatus.PENDING.value,
    parent_id: Optional[str] = None,
    project: str = "default"
) -> Dict[str, Any]:
    """创建新任务"""
    tasks_data = load_tasks(project)
    tasks = tasks_data.get("tasks", [])
    
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    new_task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": status,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "subtasks": []
    }
    
    if parent_id:
        parent = find_task(tasks, parent_id)
        if parent:
            parent.setdefault("subtasks", []).append(new_task)
        else:
            raise ValueError(f"未找到父任务: {parent_id}")
    else:
        tasks.append(new_task)
    
    tasks_data["tasks"] = tasks
    save_tasks(tasks_data)
    
    return new_task


def update_task(
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    project: str = "default"
) -> Dict[str, Any]:
    """更新任务"""
    tasks_data = load_tasks(project)
    tasks = tasks_data.get("tasks", [])
    
    task = find_task(tasks, task_id)
    if not task:
        raise ValueError(f"未找到任务: {task_id}")
    
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if status is not None:
        if status not in [s.value for s in TaskStatus]:
            raise ValueError(f"无效的状态: {status}")
        task["status"] = status
    
    task["updated"] = datetime.now().isoformat()
    
    tasks_data["tasks"] = tasks
    save_tasks(tasks_data)
    
    return task


def list_tasks(project: str = "default", status: Optional[str] = None) -> List[Dict[str, Any]]:
    """列出任务（扁平化）"""
    tasks_data = load_tasks(project)
    tasks = tasks_data.get("tasks", [])
    
    def flatten_tasks(task_list: List[Dict[str, Any]], level: int = 0) -> List[Dict[str, Any]]:
        result = []
        for task in task_list:
            task_copy = task.copy()
            task_copy["level"] = level
            if "subtasks" in task_copy:
                subtasks = task_copy.pop("subtasks")
                result.append(task_copy)
                result.extend(flatten_tasks(subtasks, level + 1))
            else:
                result.append(task_copy)
        return result
    
    all_tasks = flatten_tasks(tasks)
    
    if status:
        all_tasks = [t for t in all_tasks if t.get("status") == status]
    
    return all_tasks


def get_task(task_id: str, project: str = "default") -> Optional[Dict[str, Any]]:
    """获取任务详情"""
    tasks_data = load_tasks(project)
    tasks = tasks_data.get("tasks", [])
    return find_task(tasks, task_id)


def complete_task(task_id: str, project: str = "default") -> Dict[str, Any]:
    """完成任务"""
    return update_task(task_id, status=TaskStatus.COMPLETED.value, project=project)


def cancel_task(task_id: str, project: str = "default") -> Dict[str, Any]:
    """取消任务"""
    return update_task(task_id, status=TaskStatus.CANCELLED.value, project=project)


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        # 任务管理工具
        Tool(
            name="task.list",
            description="列出所有任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {
                        "type": "string",
                        "description": "项目名称，默认default",
                        "default": "default"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled", "blocked"],
                        "description": "按状态筛选（可选）"
                    }
                }
            }
        ),
        Tool(
            name="task.create",
            description="创建新任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "任务标题"
                    },
                    "description": {
                        "type": "string",
                        "description": "任务描述"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled", "blocked"],
                        "description": "任务状态，默认pending",
                        "default": "pending"
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "父任务ID（可选，用于创建子任务）"
                    },
                    "project": {
                        "type": "string",
                        "description": "项目名称，默认default",
                        "default": "default"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="task.get",
            description="获取任务详情",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "任务ID"
                    },
                    "project": {
                        "type": "string",
                        "description": "项目名称，默认default",
                        "default": "default"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="task.update",
            description="更新任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "任务ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "新标题（可选）"
                    },
                    "description": {
                        "type": "string",
                        "description": "新描述（可选）"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["pending", "in_progress", "completed", "cancelled", "blocked"],
                        "description": "新状态（可选）"
                    },
                    "project": {
                        "type": "string",
                        "description": "项目名称，默认default",
                        "default": "default"
                    }
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="task.complete",
            description="完成任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "任务ID"
                    },
                    "project": {
                        "type": "string",
                        "description": "项目名称，默认default",
                        "default": "default"
                    }
                },
                "required": ["task_id"]
            }
        ),
        # 任务优化工具
        Tool(
            name="task.analyze",
            description="分析任务复杂度，判断是否需要Max mode",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_title": {
                        "type": "string",
                        "description": "任务标题"
                    },
                    "task_description": {
                        "type": "string",
                        "description": "任务描述（可选）"
                    },
                    "estimated_time": {
                        "type": "string",
                        "description": "预估时间（可选）"
                    },
                    "dependencies": {
                        "type": "array",
                        "description": "依赖项（可选）"
                    }
                },
                "required": ["task_title"]
            }
        ),
        Tool(
            name="task.recommend_mode",
            description="推荐执行模式",
            inputSchema={
                "type": "object",
                "properties": {
                    "complexity": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "任务复杂度"
                    }
                },
                "required": ["complexity"]
            }
        ),
        Tool(
            name="task.cache_context",
            description="缓存上下文",
            inputSchema={
                "type": "object",
                "properties": {
                    "key": {
                        "type": "string",
                        "description": "缓存键"
                    },
                    "value": {
                        "type": "object",
                        "description": "缓存值"
                    }
                },
                "required": ["key", "value"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    try:
        # 任务管理工具
        if name == "task.list":
            project = arguments.get("project", "default")
            status = arguments.get("status")
            tasks = list_tasks(project, status)
            result = {
                "tasks": tasks,
                "total": len(tasks),
                "timestamp": datetime.now().isoformat()
            }
        
        elif name == "task.create":
            title = arguments.get("title")
            if not title:
                raise ValueError("title参数是必需的")
            task = create_task(
                title=title,
                description=arguments.get("description", ""),
                status=arguments.get("status", TaskStatus.PENDING.value),
                parent_id=arguments.get("parent_id"),
                project=arguments.get("project", "default")
            )
            result = {
                "task": task,
                "message": "任务已创建",
                "timestamp": datetime.now().isoformat()
            }
        
        elif name == "task.get":
            task_id = arguments.get("task_id")
            if not task_id:
                raise ValueError("task_id参数是必需的")
            task = get_task(task_id, arguments.get("project", "default"))
            if not task:
                raise ValueError(f"未找到任务: {task_id}")
            result = {
                "task": task,
                "timestamp": datetime.now().isoformat()
            }
        
        elif name == "task.update":
            task_id = arguments.get("task_id")
            if not task_id:
                raise ValueError("task_id参数是必需的")
            updates = {k: v for k, v in arguments.items() if k != "task_id" and k != "project" and v is not None}
            task = update_task(
                task_id,
                title=updates.get("title"),
                description=updates.get("description"),
                status=updates.get("status"),
                project=arguments.get("project", "default")
            )
            result = {
                "task": task,
                "message": "任务已更新",
                "timestamp": datetime.now().isoformat()
            }
        
        elif name == "task.complete":
            task_id = arguments.get("task_id")
            if not task_id:
                raise ValueError("task_id参数是必需的")
            task = complete_task(task_id, arguments.get("project", "default"))
            result = {
                "task": task,
                "message": "任务已完成",
                "timestamp": datetime.now().isoformat()
            }
        
        # 任务优化工具
        elif name == "task.analyze":
            task_title = arguments.get("task_title", "")
            task_description = arguments.get("task_description", "")
            task_text = f"{task_title} {task_description}".strip()
            
            # 简单的复杂度分析
            complexity = "high" if (
                len(task_text) > 100 or 
                "策略" in task_text or 
                "优化" in task_text or
                "系统" in task_text or
                "架构" in task_text
            ) else "low"
            
            estimated_tokens = len(task_text) * 2
            result = {
                "success": True,
                "task_title": task_title[:50],
                "complexity": complexity,
                "estimated_tokens": estimated_tokens,
                "recommendation": "建议使用Max模式" if complexity == "high" else "可以使用Auto模式"
            }
        
        elif name == "task.recommend_mode":
            complexity = arguments.get("complexity", "low")
            mode = "max" if complexity == "high" else ("auto" if complexity == "medium" else "auto")
            result = {
                "success": True,
                "complexity": complexity,
                "recommended_mode": mode,
                "reason": "复杂任务需要Max模式" if mode == "max" else "简单任务可用Auto模式"
            }
        
        elif name == "task.cache_context":
            key = arguments.get("key")
            value = arguments.get("value")
            if not key or value is None:
                raise ValueError("key和value参数是必需的")
            _context_cache[key] = value
            result = {
                "success": True,
                "key": key,
                "cached": True,
                "timestamp": datetime.now().isoformat()
            }
        
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())















































