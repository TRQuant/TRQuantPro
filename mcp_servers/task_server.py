#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Task Server
===================

使用官方Python MCP SDK实现的任务管理服务器
管理开发任务树和任务状态

运行方式:
    python mcp_servers/task_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
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
logger = logging.getLogger('TaskServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    # 添加utils路径以导入envelope
    TRQUANT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(TRQUANT_ROOT))
    from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
    from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
    
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError:
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 创建服务器
server = Server("trquant-task-server")

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


def load_tasks(project: str = "default") -> Dict[str, Any]:
    """加载任务树"""
    tasks_file = TASKS_DIR / f"{project}.json"
    
    if tasks_file.exists():
        try:
            return json.loads(tasks_file.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"加载任务文件失败: {e}")
    
    # 返回默认结构
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
    
    # 生成任务ID
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
        # 添加到父任务
        parent = find_task(tasks, parent_id)
        if parent:
            parent.setdefault("subtasks", []).append(new_task)
        else:
            raise ValueError(f"未找到父任务: {parent_id}")
    else:
        # 添加到根级别
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


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
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
        )
    ]



def _adapt_mcp_result_to_text_content(result: Dict[str, Any]) -> List[TextContent]:
    """将process_mcp_tool_call的结果转换为List[TextContent]格式"""
    if isinstance(result, dict) and "content" in result:
        text_content = []
        for item in result.get("content", []):
            if item.get("type") == "text":
                text_content.append(TextContent(type="text", text=item.get("text", "")))
        return text_content if text_content else [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
    else:
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    
    def handle_task_create(args):
        task_type = args.get("task_type")
        task_config = args.get("task_config", {})
        
        if not task_type:
            raise ValueError("task_type参数是必需的")
        
        task = create_task(task_type, task_config)
        return task
    
    def handle_task_list(args):
        status = args.get("status")
        task_type = args.get("task_type")
        
        tasks = list_tasks(status, task_type)
        return {
            "tasks": tasks,
            "total": len(tasks),
            "timestamp": datetime.now().isoformat()
        }
    
    def handle_task_get(args):
        task_id = args.get("task_id")
        if not task_id:
            raise ValueError("task_id参数是必需的")
        
        task = get_task(task_id)
        if not task:
            raise ValueError(f"未找到任务: {task_id}")
        
        return {
            "task": task,
            "timestamp": datetime.now().isoformat()
        }
    
    def handle_task_update(args):
        task_id = args.get("task_id")
        updates = args.get("updates", {})
        
        if not task_id:
            raise ValueError("task_id参数是必需的")
        
        task = update_task(task_id, updates)
        return {
            "task": task,
            "message": "任务已更新",
            "timestamp": datetime.now().isoformat()
        }
    
    def handle_task_cancel(args):
        task_id = args.get("task_id")
        if not task_id:
            raise ValueError("task_id参数是必需的")
        
        task = cancel_task(task_id)
        return {
            "task": task,
            "message": "任务已取消",
            "timestamp": datetime.now().isoformat()
        }
    
    tool_handlers = {
        "task.create": handle_task_create,
        "task.list": handle_task_list,
        "task.get": handle_task_get,
        "task.update": handle_task_update,
        "task.cancel": handle_task_cancel,
    }
    
    handler = tool_handlers.get(name)
    if handler:
        result = process_mcp_tool_call(
            tool_name=name,
            arguments=arguments,
            tools_list=server.list_tools(),
            tool_handler_func=handler,
            server_name="trquant-task",
            version="1.0.0"
        )
        return _adapt_mcp_result_to_text_content(result)
    else:
        from mcp_servers.utils.error_handler import MCPError, ErrorCodes
        raise MCPError(
            code=ErrorCodes.TOOL_NOT_FOUND,
            message=f"未知工具: {name}",
            hint="请检查工具名称是否正确"
        )


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())


