# -*- coding: utf-8 -*-
"""
工作流MCP服务器（标准化版本）
===========================
管理8步骤投资工作流
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("workflow-server")


TOOLS = [
    Tool(
        name="workflow.create",
        description="创建新的8步骤工作流",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "工作流名称"}
            }
        }
    ),
    Tool(
        name="workflow.list",
        description="列出所有工作流",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="workflow.status",
        description="获取工作流状态",
        inputSchema={
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string", "description": "工作流ID"}
            },
            "required": ["workflow_id"]
        }
    ),
    Tool(
        name="workflow.start_step",
        description="开始执行指定步骤",
        inputSchema={
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string"},
                "step_index": {"type": "integer", "description": "步骤索引(0-7)"}
            },
            "required": ["workflow_id", "step_index"]
        }
    ),
    Tool(
        name="workflow.complete_step",
        description="完成当前步骤",
        inputSchema={
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string"},
                "step_index": {"type": "integer"},
                "result": {"type": "object", "description": "步骤结果"}
            },
            "required": ["workflow_id", "step_index"]
        }
    ),
    Tool(
        name="workflow.resume",
        description="恢复中断的工作流",
        inputSchema={
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string"}
            },
            "required": ["workflow_id"]
        }
    ),
    Tool(
        name="workflow.steps",
        description="获取8步骤定义",
        inputSchema={"type": "object", "properties": {}}
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "workflow.create":
            result = await _handle_create(arguments)
        elif name == "workflow.list":
            result = await _handle_list()
        elif name == "workflow.status":
            result = await _handle_status(arguments)
        elif name == "workflow.start_step":
            result = await _handle_start_step(arguments)
        elif name == "workflow.complete_step":
            result = await _handle_complete_step(arguments)
        elif name == "workflow.resume":
            result = await _handle_resume(arguments)
        elif name == "workflow.steps":
            result = await _handle_steps()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_create(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    workflow = manager.create_workflow(args.get("name", "8步骤工作流"))
    
    return {
        "success": True,
        "workflow_id": workflow.workflow_id,
        "name": workflow.name,
        "total_steps": workflow.total_steps,
        "steps": [s["name"] for s in workflow.steps]
    }


async def _handle_list() -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    workflows = manager.list_workflows()
    
    return {
        "success": True,
        "count": len(workflows),
        "workflows": [
            {
                "id": w.workflow_id,
                "name": w.name,
                "status": w.status,
                "current_step": w.current_step,
                "total_steps": w.total_steps
            }
            for w in workflows
        ]
    }


async def _handle_status(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    workflow = manager.load_state(args["workflow_id"])
    
    if not workflow:
        return {"success": False, "error": "工作流不存在"}
    
    return {
        "success": True,
        "workflow_id": workflow.workflow_id,
        "name": workflow.name,
        "status": workflow.status,
        "current_step": workflow.current_step,
        "total_steps": workflow.total_steps,
        "steps": workflow.steps,
        "created_at": workflow.created_at,
        "updated_at": workflow.updated_at
    }


async def _handle_start_step(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    success = manager.start_step(args["workflow_id"], args["step_index"])
    
    if success:
        workflow = manager.load_state(args["workflow_id"])
        step_name = workflow.steps[args["step_index"]]["name"]
        return {
            "success": True,
            "message": f"开始执行步骤 {args['step_index']}: {step_name}"
        }
    else:
        return {"success": False, "error": "开始步骤失败"}


async def _handle_complete_step(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    success = manager.complete_step(
        args["workflow_id"],
        args["step_index"],
        args.get("result")
    )
    
    if success:
        return {"success": True, "message": f"步骤 {args['step_index']} 已完成"}
    else:
        return {"success": False, "error": "完成步骤失败"}


async def _handle_resume(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    
    manager = get_state_manager()
    next_step = manager.resume_workflow(args["workflow_id"])
    
    if next_step >= 0:
        workflow = manager.load_state(args["workflow_id"])
        step_name = workflow.steps[next_step]["name"]
        return {
            "success": True,
            "next_step": next_step,
            "step_name": step_name,
            "message": f"可以从步骤 {next_step}: {step_name} 继续"
        }
    else:
        return {"success": False, "error": "无法恢复工作流"}


async def _handle_steps() -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import WorkflowStateManager
    
    steps = WorkflowStateManager.WORKFLOW_8STEPS
    
    return {
        "success": True,
        "count": len(steps),
        "steps": [
            {"index": i, **s}
            for i, s in enumerate(steps)
        ]
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="workflow-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
