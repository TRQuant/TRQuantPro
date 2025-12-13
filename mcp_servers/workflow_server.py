#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Workflow Server
=======================

工作流编排MCP服务器，提供工作流的查询、执行、状态查询和自定义工作流创建功能。

运行方式:
    python mcp_servers/workflow_server.py

工具:
    - workflow.list: 列出所有可用工作流步骤
    - workflow.run: 执行完整工作流或单个步骤
    - workflow.get_status: 获取工作流状态
    - workflow.create: 创建自定义工作流（需要confirm_token）
    - workflow.validate: 验证工作流定义
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import hashlib

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('WorkflowServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 导入工程化落地件
from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
from mcp_servers.utils.schema import base_args_schema, merge_schema, requires_confirm_token
from mcp_servers.utils.artifacts import create_artifact_if_needed
from mcp_servers.utils.confirm import verify_confirm_token
from mcp_servers.utils.error_handler import wrap_exception_response

# 导入工作流编排器
try:
    from core.workflow_orchestrator import get_workflow_orchestrator, WorkflowResult, FullWorkflowResult
    WORKFLOW_ORCHESTRATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"WorkflowOrchestrator不可用: {e}")
    WORKFLOW_ORCHESTRATOR_AVAILABLE = False

# 导入依赖检查器
from mcp_servers.utils.dependency_checker import get_dependency_checker

# 导入Strategy KB集成函数
try:
    from mcp_servers.workflow_server_strategy_integration import _handle_strategy_generate_candidate
    STRATEGY_KB_INTEGRATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Strategy KB集成不可用: {e}")
    STRATEGY_KB_INTEGRATION_AVAILABLE = False

# 启动时检查依赖
_checker = get_dependency_checker()
_deps = _checker.check_dependencies("trquant-workflow")
if not _deps["all_required_available"]:
    missing = ", ".join(_deps["missing_required"])
    logger.warning(f"trquant-workflow缺少必需依赖: {missing}")

# 工作流存储目录
WORKFLOW_STORAGE_DIR = TRQUANT_ROOT / ".taorui" / "workflows"
WORKFLOW_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# 工作流状态存储（内存缓存，用于快速访问）
_workflow_status: Dict[str, Dict[str, Any]] = {}

# 工作流持久化存储
from mcp_servers.utils.workflow_storage import WorkflowStorage
_workflow_storage = WorkflowStorage(WORKFLOW_STORAGE_DIR)


def _wrap_response(envelope: Dict[str, Any]) -> List[TextContent]:
    """将envelope包装为TextContent列表"""
    return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


# 创建MCP服务器
server = Server("trquant-workflow")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="workflow.list",
            description="列出所有可用工作流步骤",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ),
        Tool(
            name="workflow.run",
            description="执行完整工作流或单个步骤（支持dry_run模式）",
            inputSchema=merge_schema(
                base_args_schema(mode="read"),
                {
                    "type": "object",
                    "properties": {
                        "step_id": {
                            "type": "string",
                            "description": "步骤ID（可选，不提供则执行完整工作流）。可选值：data_source, market_trend, mainline, candidate_pool, factor, strategy",
                            "enum": ["data_source", "market_trend", "mainline", "candidate_pool", "factor", "strategy"]
                        },
                        "callback_url": {
                            "type": "string",
                            "description": "可选的回调URL，用于接收步骤完成通知"
                        }
                    },
                    "required": []
                }
            )
        ),
        Tool(
            name="workflow.get_status",
            description="获取工作流状态（单个步骤或完整工作流）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "工作流ID（可选，不提供则返回最近的工作流状态）"
                        },
                        "step_id": {
                            "type": "string",
                            "description": "步骤ID（可选，用于获取特定步骤的状态）"
                        }
                    },
                    "required": []
                }
            )
        ),
        Tool(
            name="workflow.create",
            description="创建自定义工作流（需要confirm_token）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "workflow_id": {
                            "type": "string",
                            "description": "工作流ID（必需）"
                        },
                        "name": {
                            "type": "string",
                            "description": "工作流名称（必需）"
                        },
                        "steps": {
                            "type": "array",
                            "description": "工作流步骤列表（必需）",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "step_id": {"type": "string"},
                                    "step_name": {"type": "string"},
                                    "enabled": {"type": "boolean"},
                                    "params": {"type": "object"}
                                },
                                "required": ["step_id", "step_name"]
                            }
                        },
                        "description": {
                            "type": "string",
                            "description": "工作流描述（可选）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["workflow_id", "name", "steps"]
                }
            )
        ),
        Tool(
            name="workflow.validate",
            description="验证工作流定义",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "workflow_definition": {
                            "type": "object",
                            "description": "工作流定义（必需）",
                            "properties": {
                                "workflow_id": {"type": "string"},
                                "name": {"type": "string"},
                                "steps": {
                                    "type": "array",
                                    "items": {"type": "object"}
                                }
                            },
                            "required": ["workflow_id", "name", "steps"]
                        }
                    },
                    "required": ["workflow_definition"]
                }
            )
        ),
        Tool(
            name="workflow.history",
            description="查询工作流历史记录",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "返回数量限制（默认：100）",
                            "default": 100
                        },
                        "offset": {
                            "type": "integer",
                            "description": "偏移量（默认：0）",
                            "default": 0
                        },
                        "status_filter": {
                            "type": "string",
                            "description": "状态过滤（可选）。可选值：completed, failed, running, all",
                            "enum": ["completed", "failed", "running", "all"],
                            "default": "all"
                        }
                    },
                    "required": []
                }
            )
        ),
        Tool(
            name="workflow.strategy.generate_candidate",
            description="生成候选策略（受Strategy KB规则约束）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "mainline": {
                            "type": "string",
                            "description": "投资主线"
                        },
                        "candidate_pool": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "候选股票池"
                        },
                        "factors": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "使用的因子列表"
                        },
                        "research_query": {
                            "type": "string",
                            "description": "研究卡检索查询（可选）"
                        },
                        "rule_set": {
                            "type": "string",
                            "enum": ["all", "strategy_constraints", "data_rules", "risk_model", "cost_model", "universe_rules"],
                            "default": "all",
                            "description": "要应用的规则集"
                        }
                    },
                    "required": ["mainline", "candidate_pool", "factors"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    trace_id = extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "workflow.list":
            return await _handle_workflow_list(trace_id, artifact_policy)
        
        elif name == "workflow.run":
            step_id = arguments.get("step_id")
            callback_url = arguments.get("callback_url")
            return await _handle_workflow_run(step_id, callback_url, mode, trace_id, artifact_policy)
        
        elif name == "workflow.get_status":
            workflow_id = arguments.get("workflow_id")
            step_id = arguments.get("step_id")
            return await _handle_workflow_get_status(workflow_id, step_id, trace_id, artifact_policy)
        
        elif name == "workflow.create":
            workflow_id = arguments.get("workflow_id")
            name = arguments.get("name")
            steps = arguments.get("steps")
            description = arguments.get("description")
            confirm_token = arguments.get("confirm_token")
            return await _handle_workflow_create(
                workflow_id, name, steps, description, mode, confirm_token, trace_id, artifact_policy
            )
        
        elif name == "workflow.validate":
            workflow_definition = arguments.get("workflow_definition")
            return await _handle_workflow_validate(workflow_definition, trace_id, artifact_policy)
        
        elif name == "workflow.history":
            limit = arguments.get("limit", 100)
            offset = arguments.get("offset", 0)
            status_filter = arguments.get("status_filter", "all")
            return await _handle_workflow_history(limit, offset, status_filter, trace_id, artifact_policy)
        
        elif name == "workflow.strategy.generate_candidate":
            # 动态导入以避免循环依赖
            try:
                from mcp_servers.workflow_server_strategy_integration import _handle_strategy_generate_candidate
                mainline = arguments.get("mainline")
                candidate_pool = arguments.get("candidate_pool", [])
                factors = arguments.get("factors", [])
                research_query = arguments.get("research_query", "")
                rule_set = arguments.get("rule_set", "all")
                return await _handle_strategy_generate_candidate(
                    mainline, candidate_pool, factors, research_query, rule_set, trace_id, artifact_policy
                )
            except ImportError as e:
                envelope = wrap_error_response(
                    error_code="DEPENDENCY_ERROR",
                    error_message=f"Strategy KB集成不可用: {e}",
                    server_name="trquant-workflow",
                    tool_name="workflow.strategy.generate_candidate",
                    version="1.0.0",
                    trace_id=trace_id
                )
                return _wrap_response(envelope)
        
        else:
            envelope = wrap_error_response(
                error_code="UNKNOWN_TOOL",
                error_message=f"未知工具: {name}",
                server_name="trquant-workflow",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-workflow",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


async def _handle_workflow_list(trace_id: str, artifact_policy: str) -> List[TextContent]:
    """处理workflow.list"""
    steps = [
        {
            "step_id": "data_source",
            "step_name": "数据源检测",
            "description": "检测JQData、AKShare、MongoDB等数据源状态",
            "estimated_time": "5-10秒"
        },
        {
            "step_id": "market_trend",
            "step_name": "市场趋势分析",
            "description": "分析短期、中期、长期市场趋势",
            "estimated_time": "30-60秒"
        },
        {
            "step_id": "mainline",
            "step_name": "投资主线识别",
            "description": "识别当前市场投资主线",
            "estimated_time": "60-120秒"
        },
        {
            "step_id": "candidate_pool",
            "step_name": "候选池构建",
            "description": "构建股票候选池",
            "estimated_time": "30-60秒"
        },
        {
            "step_id": "factor",
            "step_name": "因子推荐",
            "description": "基于市场状态推荐量化因子",
            "estimated_time": "10-30秒"
        },
        {
            "step_id": "strategy",
            "step_name": "策略生成",
            "description": "生成策略代码",
            "estimated_time": "30-60秒"
        }
    ]
    
    data = {
        "steps": steps,
        "total_steps": len(steps),
        "full_workflow_estimated_time": "3-5分钟"
    }
    
    result = create_artifact_if_needed(data, "workflow_list", artifact_policy, trace_id)
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-workflow",
        tool_name="workflow.list",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


async def _handle_workflow_run(
    step_id: Optional[str],
    callback_url: Optional[str],
    mode: str,
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理workflow.run"""
    if not WORKFLOW_ORCHESTRATOR_AVAILABLE:
        envelope = wrap_error_response(
            error_code="DEPENDENCY_UNAVAILABLE",
            error_message="WorkflowOrchestrator不可用，请检查依赖",
            server_name="trquant-workflow",
            tool_name="workflow.run",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    try:
        orchestrator = get_workflow_orchestrator()
        
        if mode == "dry_run":
            # dry_run模式：返回执行计划
            if step_id:
                data = {
                    "mode": "dry_run",
                    "plan": {
                        "step_id": step_id,
                        "step_name": _get_step_name(step_id),
                        "action": "执行单个步骤",
                        "estimated_time": _get_estimated_time(step_id)
                    }
                }
            else:
                data = {
                    "mode": "dry_run",
                    "plan": {
                        "action": "执行完整工作流",
                        "steps": [
                            {"step_id": "data_source", "step_name": "数据源检测"},
                            {"step_id": "market_trend", "step_name": "市场趋势分析"},
                            {"step_id": "mainline", "step_name": "投资主线识别"},
                            {"step_id": "candidate_pool", "step_name": "候选池构建"},
                            {"step_id": "factor", "step_name": "因子推荐"},
                            {"step_id": "strategy", "step_name": "策略生成"}
                        ],
                        "estimated_time": "3-5分钟"
                    }
                }
            
            result = create_artifact_if_needed(data, "workflow_plan", artifact_policy, trace_id)
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-workflow",
                tool_name="workflow.run",
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
        
        # execute模式：实际执行
        if step_id:
            # 执行单个步骤
            step_map = {
                "data_source": orchestrator.check_data_sources,
                "market_trend": orchestrator.analyze_market_trend,
                "mainline": orchestrator.identify_mainlines,
                "candidate_pool": orchestrator.build_candidate_pool,
                "factor": orchestrator.recommend_factors,
                "strategy": orchestrator.generate_strategy
            }
            
            if step_id not in step_map:
                return wrap_error_response(
                    f"未知步骤ID: {step_id}",
                    trace_id=trace_id,
                    error_code="INVALID_STEP_ID"
                )
            
            result = step_map[step_id]()
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{step_id}"
            
            # 保存状态（内存和持久化）
            status_data = {
                "workflow_id": workflow_id,
                "step_id": step_id,
                "status": "completed" if result.success else "failed",
                "result": {
                    "step_name": result.step_name,
                    "success": result.success,
                    "summary": result.summary,
                    "details": result.details,
                    "timestamp": result.timestamp,
                    "error": result.error
                },
                "timestamp": datetime.now().isoformat()
            }
            _workflow_status[workflow_id] = status_data
            _workflow_storage.save_workflow_status(workflow_id, status_data)
            
            data = {
                "workflow_id": workflow_id,
                "step_id": step_id,
                "status": "completed" if result.success else "failed",
                "result": {
                    "step_name": result.step_name,
                    "success": result.success,
                    "summary": result.summary,
                    "details": result.details,
                    "timestamp": result.timestamp,
                    "error": result.error
                }
            }
        else:
            # 执行完整工作流
            def callback(step_name, result):
                if callback_url:
                    # 这里可以发送HTTP请求到callback_url
                    logger.info(f"步骤完成: {step_name}, 回调URL: {callback_url}")
            
            full_result = orchestrator.run_full_workflow(callback=callback)
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_full"
            
            # 保存状态（内存和持久化）
            status_data = {
                "workflow_id": workflow_id,
                "status": "completed" if full_result.success else "failed",
                "steps": [
                    {
                        "step_name": r.step_name,
                        "success": r.success,
                        "summary": r.summary,
                        "timestamp": r.timestamp,
                        "error": r.error
                    }
                    for r in full_result.steps
                ],
                "strategy_file": full_result.strategy_file,
                "total_time": full_result.total_time,
                "timestamp": datetime.now().isoformat()
            }
            _workflow_status[workflow_id] = status_data
            _workflow_storage.save_workflow_status(workflow_id, status_data)
            
            data = {
                "workflow_id": workflow_id,
                "status": "completed" if full_result.success else "failed",
                "steps": [
                    {
                        "step_name": r.step_name,
                        "success": r.success,
                        "summary": r.summary,
                        "timestamp": r.timestamp,
                        "error": r.error
                    }
                    for r in full_result.steps
                ],
                "strategy_file": full_result.strategy_file,
                "total_time": full_result.total_time
            }
        
        result = create_artifact_if_needed(data, "workflow_result", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-workflow",
            tool_name="workflow.run",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-workflow",
            tool_name="workflow.run",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


async def _handle_workflow_get_status(
    workflow_id: Optional[str],
    step_id: Optional[str],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理workflow.get_status"""
    if not workflow_id:
        # 返回最近的工作流状态
        if not _workflow_status:
            envelope = wrap_error_response(error_code="NO_WORKFLOW_STATUS", error_message="没有可用的工作流状态", server_name="trquant-workflow", tool_name="workflow.get_status", version="1.0.0", trace_id=trace_id)
            return _wrap_response(envelope)
        workflow_id = max(_workflow_status.keys(), key=lambda k: _workflow_status[k]["timestamp"])
    
    if workflow_id not in _workflow_status:
        return wrap_error_response(
            f"工作流ID不存在: {workflow_id}",
            trace_id=trace_id,
            error_code="WORKFLOW_NOT_FOUND"
        )
    
    status = _workflow_status[workflow_id].copy()
    
    if step_id:
        # 返回特定步骤的状态
        if "steps" in status:
            step_status = next(
                (s for s in status["steps"] if s.get("step_name") == step_id or s.get("step_id") == step_id),
                None
            )
            if step_status:
                data = {"workflow_id": workflow_id, "step_id": step_id, "status": step_status}
            else:
                return wrap_error_response(
                    f"步骤ID不存在: {step_id}",
                    trace_id=trace_id,
                    error_code="STEP_NOT_FOUND"
                )
        else:
            envelope = wrap_error_response(error_code="NO_STEPS", error_message="该工作流没有步骤信息", server_name="trquant-workflow", tool_name="workflow.get_status", version="1.0.0", trace_id=trace_id)
            return _wrap_response(envelope)
    else:
        data = status
    
    result = create_artifact_if_needed(data, "workflow_status", artifact_policy, trace_id)
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-workflow",
        tool_name="workflow.get_status",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


async def _handle_workflow_create(
    workflow_id: str,
    name: str,
    steps: List[Dict[str, Any]],
    description: Optional[str],
    mode: str,
    confirm_token: Optional[str],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理workflow.create"""
    # 验证工作流定义
    validation_result = _validate_workflow_definition(workflow_id, name, steps)
    if not validation_result["valid"]:
        return wrap_error_response(
            f"工作流定义验证失败: {validation_result['error']}",
            trace_id=trace_id,
            error_code="VALIDATION_FAILED"
        )
    
    if mode == "dry_run":
        # dry_run模式：返回验证结果
        data = {
            "mode": "dry_run",
            "validation": validation_result,
            "workflow": {
                "workflow_id": workflow_id,
                "name": name,
                "steps": steps,
                "description": description
            }
        }
        
        result = create_artifact_if_needed(data, "workflow_validation", artifact_policy, trace_id)
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-workflow",
            tool_name="workflow.create",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    # execute模式：需要confirm_token
    if not confirm_token:
        envelope = wrap_error_response(error_code="MISSING_CONFIRM_TOKEN", error_message="execute模式需要confirm_token", server_name="trquant-workflow", tool_name="workflow.create", version="1.0.0", trace_id=trace_id)
        return _wrap_response(envelope)
    
    # 验证confirm_token
    ok, err_code = verify_confirm_token(confirm_token, "workflow.create", {
        "workflow_id": workflow_id,
        "name": name,
        "steps": steps
    }, trace_id)
    
    if not ok:
        return wrap_error_response(
            f"confirm_token验证失败: {err_code}",
            trace_id=trace_id,
            error_code=err_code
        )
    
    # 保存工作流定义
    workflow_file = WORKFLOW_STORAGE_DIR / f"{workflow_id}.json"
    workflow_data = {
        "workflow_id": workflow_id,
        "name": name,
        "description": description,
        "steps": steps,
        "created_at": datetime.now().isoformat(),
        "created_by": trace_id
    }
    
    with open(workflow_file, "w", encoding="utf-8") as f:
        json.dump(workflow_data, f, ensure_ascii=False, indent=2)
    
    # 记录evidence
    try:
        from scripts.mcp_call import MCPClient
        evidence_client = MCPClient("trquant-evidence")
        evidence_client.call_tool("evidence.record", {
            "evidence_type": "workflow_creation",
            "evidence_data": {
                "workflow_id": workflow_id,
                "name": name,
                "steps_count": len(steps),
                "trace_id": trace_id
            },
            "trace_id": trace_id
        })
        evidence_client.close()
    except Exception as e:
        logger.warning(f"记录evidence失败: {e}")
    
    data = {
        "workflow_id": workflow_id,
        "name": name,
        "steps": steps,
        "description": description,
        "workflow_file": str(workflow_file),
        "created_at": workflow_data["created_at"]
    }
    
    result = create_artifact_if_needed(data, "workflow_created", artifact_policy, trace_id)
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-workflow",
        tool_name="workflow.create",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


async def _handle_workflow_validate(
    workflow_definition: Dict[str, Any],
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理workflow.validate"""
    workflow_id = workflow_definition.get("workflow_id")
    name = workflow_definition.get("name")
    steps = workflow_definition.get("steps", [])
    
    validation_result = _validate_workflow_definition(workflow_id, name, steps)
    
    data = {
        "valid": validation_result["valid"],
        "errors": validation_result.get("errors", []),
        "warnings": validation_result.get("warnings", []),
        "workflow_id": workflow_id,
        "name": name,
        "steps_count": len(steps) if steps else 0
    }
    
    result = create_artifact_if_needed(data, "workflow_validation", artifact_policy, trace_id)
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-workflow",
        tool_name="workflow.validate",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


async def _handle_workflow_history(
    limit: int,
    offset: int,
    status_filter: str,
    trace_id: str,
    artifact_policy: str
) -> List[TextContent]:
    """处理workflow.history"""
    try:
        workflows = _workflow_storage.list_workflows(
            limit=limit,
            offset=offset,
            status_filter=status_filter
        )
        
        total_count = _workflow_storage.get_workflow_count(status_filter=status_filter)
        
        # 清理内部字段
        for workflow in workflows:
            workflow.pop("_file_path", None)
            workflow.pop("_file_mtime", None)
            workflow.pop("_saved_at", None)
        
        data = {
            "workflows": workflows,
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "status_filter": status_filter
        }
        
        result = create_artifact_if_needed(data, "workflow_history", artifact_policy, trace_id)
        
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-workflow",
            tool_name="workflow.history",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-workflow",
            tool_name="workflow.history",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


def _validate_workflow_definition(
    workflow_id: Optional[str],
    name: Optional[str],
    steps: Optional[List[Dict[str, Any]]]
) -> Dict[str, Any]:
    """验证工作流定义"""
    errors = []
    warnings = []
    
    if not workflow_id:
        errors.append("workflow_id是必需的")
    elif not isinstance(workflow_id, str) or len(workflow_id) == 0:
        errors.append("workflow_id必须是非空字符串")
    
    if not name:
        errors.append("name是必需的")
    elif not isinstance(name, str) or len(name) == 0:
        errors.append("name必须是非空字符串")
    
    if not steps:
        errors.append("steps是必需的")
    elif not isinstance(steps, list) or len(steps) == 0:
        errors.append("steps必须是非空数组")
    else:
        valid_step_ids = ["data_source", "market_trend", "mainline", "candidate_pool", "factor", "strategy"]
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"步骤{i+1}必须是对象")
                continue
            
            step_id = step.get("step_id")
            step_name = step.get("step_name")
            
            if not step_id:
                errors.append(f"步骤{i+1}缺少step_id")
            elif step_id not in valid_step_ids:
                warnings.append(f"步骤{i+1}的step_id '{step_id}' 不在标准步骤列表中")
            
            if not step_name:
                errors.append(f"步骤{i+1}缺少step_name")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def _get_step_name(step_id: str) -> str:
    """获取步骤名称"""
    step_names = {
        "data_source": "数据源检测",
        "market_trend": "市场趋势分析",
        "mainline": "投资主线识别",
        "candidate_pool": "候选池构建",
        "factor": "因子推荐",
        "strategy": "策略生成"
    }
    return step_names.get(step_id, step_id)


def _get_estimated_time(step_id: str) -> str:
    """获取预估时间"""
    estimated_times = {
        "data_source": "5-10秒",
        "market_trend": "30-60秒",
        "mainline": "60-120秒",
        "candidate_pool": "30-60秒",
        "factor": "10-30秒",
        "strategy": "30-60秒"
    }
    return estimated_times.get(step_id, "未知")


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

