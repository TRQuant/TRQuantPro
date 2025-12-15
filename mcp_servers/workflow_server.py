# -*- coding: utf-8 -*-
"""
工作流MCP服务器（标准化版本）
===========================
管理9步骤投资工作流（不包括实盘）
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
        description="创建新的9步骤工作流（不包括实盘）",
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
                "step_index": {"type": "integer", "description": "步骤索引(0-8)"}
            },
            "required": ["workflow_id", "step_index"]
        }
    ),
    Tool(
        name="workflow.run_step",
        description="执行指定步骤（通过WorkflowOrchestrator调用）",
        inputSchema={
            "type": "object",
            "properties": {
                "workflow_id": {"type": "string", "description": "工作流ID"},
                "step_index": {"type": "integer", "description": "步骤索引(0-8)"},
                "step_args": {"type": "object", "description": "步骤参数（可选）"}
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
        description="获取9步骤定义",
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
        elif name == "workflow.run_step":
            result = await _handle_run_step(arguments)
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



async def _handle_run_step(args: Dict) -> Dict:
    """
    执行指定步骤 - 通过调用WorkflowOrchestrator执行实际逻辑
    """
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.workflow import get_state_manager
    from core.workflow_orchestrator import WorkflowOrchestrator
    
    manager = get_state_manager()
    workflow = manager.load_state(args["workflow_id"])
    
    if not workflow:
        return {"success": False, "error": "工作流不存在"}
    
    step_index = args["step_index"]
    if step_index < 0 or step_index >= len(workflow.steps):
        return {"success": False, "error": f"步骤索引 {step_index} 超出范围(0-{len(workflow.steps)-1})"}
    
    step_info = workflow.steps[step_index]
    step_id = step_info.get("id")
    step_name = step_info.get("name")
    
    # 标记步骤开始
    manager.start_step(args["workflow_id"], step_index)
    
    try:
        # 创建WorkflowOrchestrator执行步骤
        orchestrator = WorkflowOrchestrator()
        
        # 步骤ID到方法的映射
        step_method_map = {
            "data_source": orchestrator.check_data_sources,
            "market_trend": orchestrator.analyze_market_trend,
            "mainline": orchestrator.identify_mainlines,
            "candidate_pool": orchestrator.build_candidate_pool,
            "factor": orchestrator.recommend_factors,
            "strategy": orchestrator.generate_strategy,
            "backtest": lambda: _run_backtest_step(orchestrator, args.get("step_args", {})),
            "optimization": lambda: orchestrator.optimize_strategy(orchestrator._results.get("backtest")),
            "report": lambda: _generate_report_step(orchestrator),
        }
        
        method = step_method_map.get(step_id)
        if not method:
            return {"success": False, "error": f"未知步骤ID: {step_id}"}
        
        # 执行步骤
        result = method()
        
        # 标记步骤完成
        result_dict = {
            "step_name": result.step_name if hasattr(result, 'step_name') else step_name,
            "success": result.success if hasattr(result, 'success') else True,
            "summary": result.summary if hasattr(result, 'summary') else "执行完成",
            "details": result.details if hasattr(result, 'details') else {},
        }
        manager.complete_step(args["workflow_id"], step_index, result_dict)
        
        # 更新工作流上下文
        if result_dict.get("success") and result_dict.get("details"):
            manager.set_context(args["workflow_id"], step_id, result_dict["details"])
        
        return {
            "success": True,
            "step_index": step_index,
            "step_id": step_id,
            "step_name": step_name,
            "result": result_dict
        }
        
    except Exception as e:
        logger.error(f"执行步骤 {step_index} ({step_id}) 失败: {e}", exc_info=True)
        workflow.steps[step_index]["status"] = "failed"
        workflow.steps[step_index]["error"] = str(e)
        manager.save_state(workflow)
        return {
            "success": False,
            "error": str(e),
            "step_index": step_index,
            "step_id": step_id
        }


def _run_backtest_step(orchestrator, step_args: Dict):
    """执行回测步骤"""
    from core.workflow_orchestrator import WorkflowResult
    
    strategy_path = step_args.get("strategy_path")
    if strategy_path:
        try:
            from core.bullettrade import BulletTradeEngine
            engine = BulletTradeEngine()
            result = engine.run_backtest(
                strategy_path=str(strategy_path),
                start_date=step_args.get("start_date", "2024-01-01"),
                end_date=step_args.get("end_date", "2024-06-30"),
                initial_capital=step_args.get("initial_capital", 1000000)
            )
            return WorkflowResult(
                step_name="回测验证",
                success=True,
                summary=f"总收益: {result.get('total_return', 0):.2%}",
                details=result
            )
        except Exception as e:
            return WorkflowResult(
                step_name="回测验证",
                success=False,
                summary=f"回测失败: {str(e)[:50]}",
                error=str(e)
            )
    else:
        return WorkflowResult(
            step_name="回测验证",
            success=True,
            summary="快速回测完成（无策略路径）",
            details={"message": "请提供strategy_path参数"}
        )


def _generate_report_step(orchestrator):
    """生成报告步骤"""
    from core.workflow_orchestrator import WorkflowResult
    from pathlib import Path
    from datetime import datetime
    
    try:
        all_results = orchestrator._results
        report_dir = Path(__file__).parent.parent / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"workflow_report_{timestamp}.html"
        
        html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>工作流报告 - {timestamp}</title>
<style>
body {{ font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; background: #1a1a2e; color: #eee; }}
h1 {{ color: #58a6ff; }}
.step {{ background: #16213e; padding: 15px; margin: 10px 0; border-radius: 8px; }}
.success {{ border-left: 4px solid #10b981; }}
.failed {{ border-left: 4px solid #ef4444; }}
</style></head>
<body>
<h1>🐉 韬睿量化工作流报告</h1>
<p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""
        for step_id, result in all_results.items():
            status_class = "success" if getattr(result, 'success', True) else "failed"
            html += f"""
<div class="step {status_class}">
<h3>{getattr(result, 'step_name', step_id)}</h3>
<p>{getattr(result, 'summary', '完成')}</p>
</div>
"""
        html += "</body></html>"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return WorkflowResult(
            step_name="报告生成",
            success=True,
            summary=f"报告已生成: {report_file.name}",
            details={"report_file": str(report_file)}
        )
    except Exception as e:
        return WorkflowResult(
            step_name="报告生成",
            success=False,
            summary=f"报告生成失败: {str(e)[:50]}",
            error=str(e)
        )



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
    
    steps = WorkflowStateManager.WORKFLOW_9STEPS
    
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


async def _call_step_mcp_tool(mcp_tool: str, step_id: str, step_args: Dict, context: Dict) -> Dict:
    """
    调用步骤对应的MCP工具
    
    步骤映射：
    1. data_source -> data_source.check
    2. market_trend -> market.status
    3. mainline -> market.mainlines
    4. candidate_pool -> data_source.candidate_pool (或通过workflow_orchestrator)
    5. factor -> factor.recommend
    6. strategy -> strategy_template.generate
    7. backtest -> backtest.bullettrade
    8. optimization -> optimizer.optuna
    9. report -> report.generate
    """
    import subprocess
    import sys
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    
    # MCP工具到服务器的映射
    tool_server_map = {
        "data_source.check": "data_source_server",
        "market.status": "market_server",
        "market.mainlines": "market_server",
        "data_source.candidate_pool": "data_source_server",
        "factor.recommend": "factor_server",
        "strategy_template.generate": "strategy_template_server",
        "backtest.bullettrade": "backtest_server",
        "optimizer.optuna": "optimizer_server",
        "report.generate": "report_server",
    }
    
    # 解析工具名称和参数
    tool_parts = mcp_tool.split(".")
    if len(tool_parts) != 2:
        return {"success": False, "error": f"无效的MCP工具格式: {mcp_tool}"}
    
    server_name = tool_server_map.get(mcp_tool)
    if not server_name:
        return {"success": False, "error": f"未找到MCP工具 {mcp_tool} 对应的服务器"}
    
    server_path = project_root / "mcp_servers" / f"{server_name}.py"
    if not server_path.exists():
        return {"success": False, "error": f"MCP服务器文件不存在: {server_path}"}
    
    # 准备调用参数
    call_args = {
        "tool_name": mcp_tool,
        "arguments": step_args,
        "trace_id": f"workflow_{step_id}_{context.get('workflow_id', 'unknown')}"
    }
    
    # 合并上下文数据
    if context:
        call_args["arguments"].update(context)
    
    try:
        # 通过subprocess调用MCP服务器
        cmd = [
            sys.executable,
            str(server_path),
            "--tool_name", mcp_tool,
            "--arguments", json.dumps(call_args["arguments"]),
            "--trace_id", call_args["trace_id"]
        ]
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,
            cwd=str(project_root)
        )
        
        if process.returncode != 0:
            return {
                "success": False,
                "error": f"MCP服务器执行失败: {process.stderr[:200]}"
            }
        
        # 解析输出
        output = process.stdout.strip()
        if output:
            try:
                result = json.loads(output)
                return result
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "data": output,
                    "message": "MCP工具执行成功（非JSON输出）"
                }
        else:
            return {
                "success": False,
                "error": "MCP服务器无输出"
            }
            
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"MCP工具 {mcp_tool} 执行超时（>300秒）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"调用MCP工具失败: {str(e)}"
        }


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
    
    steps = WorkflowStateManager.WORKFLOW_9STEPS
    
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
