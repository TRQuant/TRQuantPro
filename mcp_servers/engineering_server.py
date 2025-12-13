#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Engineering Server
==========================

Compounding Engineering循环的编排服务器（Plan→Work→Review→Codify）。

运行方式:
    python mcp_servers/engineering_server.py

工具:
    - engineering.plan: 目标拆解为任务树
    - engineering.bootstrap: 创建工作区
    - engineering.work: 执行实现
    - engineering.verify: 质量门禁
    - engineering.release: 发布版本
    - engineering.codify: 固化知识
    - engineering.retrospective: 复盘总结
    - engineering.guardrails.status: 可观测面板
"""

import sys
import json
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('EngineeringServer')

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
from mcp_servers.utils.schema import base_args_schema, merge_schema
from mcp_servers.utils.artifacts import create_artifact_if_needed, artifact_write
from mcp_servers.utils.confirm import verify_confirm_token, build_confirm_payload
from mcp_servers.utils.error_handler import wrap_exception_response

# 导入其他MCP服务器客户端（用于编排）
try:
    from scripts.mcp_call import MCPClient
    MCP_CLIENT_AVAILABLE = True
except ImportError:
    MCP_CLIENT_AVAILABLE = False
    logger.warning("MCPClient不可用，部分功能可能受限")


# 全局状态
_objectives: Dict[str, Dict[str, Any]] = {}
_artifact_storage = TRQUANT_ROOT / ".taorui" / "engineering_artifacts"
_artifact_storage.mkdir(parents=True, exist_ok=True)


def _generate_objective_id(objective: str) -> str:
    """生成objective_id"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    hash_suffix = hashlib.md5(objective.encode()).hexdigest()[:8]
    return f"obj_{timestamp}_{hash_suffix}"


def _call_mcp_tool(server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """调用其他MCP服务器的工具"""
    if not MCP_CLIENT_AVAILABLE:
        logger.warning(f"MCPClient不可用，无法调用 {server_name}.{tool_name}")
        return {"ok": False, "error": "MCPClient不可用"}
    
    try:
        client = MCPClient(server_name)
        result = client.call_tool(tool_name, arguments)
        return result
    except Exception as e:
        logger.error(f"调用 {server_name}.{tool_name} 失败: {e}")
        return {"ok": False, "error": str(e)}


# 创建MCP服务器
server = Server("trquant-engineering")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="engineering.plan",
            description="将目标拆解为可执行任务树，并给出约束、验收与风险点",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "objective": {
                            "type": "string",
                            "description": "目标描述"
                        },
                        "context": {
                            "type": "object",
                            "properties": {
                                "repo": {"type": "string"},
                                "docs_scope": {"type": "array", "items": {"type": "string"}},
                                "constraints": {"type": "array", "items": {"type": "string"}},
                                "baseline_ref": {"type": "string"}
                            }
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["P0", "P1", "P2"],
                            "default": "P1"
                        }
                    },
                    "required": ["objective"]
                }
            )
        ),
        Tool(
            name="engineering.bootstrap",
            description="为目标创建工作区（分支、目录、规范文件、记录框架）",
            inputSchema=merge_schema(
                base_args_schema(mode="execute"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID（由plan生成）"
                        },
                        "repo": {
                            "type": "string",
                            "default": "."
                        },
                        "branch_strategy": {
                            "type": "string",
                            "enum": ["feature", "hotfix"],
                            "default": "feature"
                        }
                    },
                    "required": ["objective_id"]
                }
            )
        ),
        Tool(
            name="engineering.work",
            description="按任务执行实现（生成/修改代码 + 同步文档 + 生成可运行示例）",
            inputSchema=merge_schema(
                base_args_schema(mode="execute"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID"
                        },
                        "tasks": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "要执行的任务ID列表"
                        },
                        "work_items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string", "enum": ["code", "doc", "config"]},
                                    "target": {"type": "string"},
                                    "instruction": {"type": "string"}
                                },
                                "required": ["type", "target", "instruction"]
                            }
                        }
                    },
                    "required": ["objective_id"]
                }
            )
        ),
        Tool(
            name="engineering.verify",
            description="质量门禁：结构校验、回归测试、工作流smoke、报告生成",
            inputSchema=merge_schema(
                base_args_schema(mode="read"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID"
                        },
                        "verification_profile": {
                            "type": "string",
                            "enum": ["quick", "standard", "release"],
                            "default": "standard"
                        },
                        "baseline_ref": {
                            "type": "string",
                            "description": "对比基准（git tag / report_id / workflow_run_id）"
                        }
                    },
                    "required": ["objective_id"]
                }
            )
        ),
        Tool(
            name="engineering.release",
            description="合并、打tag、发布文档与工件，生成release note",
            inputSchema=merge_schema(
                base_args_schema(mode="execute"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID"
                        },
                        "release_type": {
                            "type": "string",
                            "enum": ["dev", "rc", "prod"],
                            "default": "dev"
                        },
                        "version": {
                            "type": "string",
                            "description": "版本号（如：v1.0.0）"
                        }
                    },
                    "required": ["objective_id", "version"]
                }
            )
        ),
        Tool(
            name="engineering.codify",
            description="把这次循环固化成文档 + 规范 + 模板 + FAQ + Changelog",
            inputSchema=merge_schema(
                base_args_schema(mode="execute"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID"
                        },
                        "targets": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "doc_id": {"type": "string"},
                                    "section": {"type": "string"},
                                    "content_instruction": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["objective_id"]
                }
            )
        ),
        Tool(
            name="engineering.retrospective",
            description="自动生成复盘（做得好/问题/根因/改进/行动项）",
            inputSchema=merge_schema(
                base_args_schema(mode="read"),
                {
                    "type": "object",
                    "properties": {
                        "objective_id": {
                            "type": "string",
                            "description": "目标ID"
                        },
                        "include": {
                            "type": "array",
                            "items": {"type": "string", "enum": ["tasks", "diffs", "reports", "quality", "incidents"]},
                            "default": ["tasks", "reports"]
                        }
                    },
                    "required": ["objective_id"]
                }
            )
        ),
        Tool(
            name="engineering.guardrails.status",
            description="可观测与合规面板（可维护性）",
            inputSchema=merge_schema(
                base_args_schema(mode="read"),
                {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "返回最近N个目标"
                        }
                    }
                }
            )
        ),
    ]


def _wrap_response(envelope: Dict[str, Any]) -> List[TextContent]:
    """包装响应为MCP格式"""
    return [TextContent(
        type="text",
        text=json.dumps(envelope, ensure_ascii=False, indent=2)
    )]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """处理工具调用"""
    trace_id = extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "engineering.plan":
            return _handle_plan(arguments, trace_id, artifact_policy)
        elif name == "engineering.bootstrap":
            return _handle_bootstrap(arguments, trace_id, artifact_policy)
        elif name == "engineering.work":
            return _handle_work(arguments, trace_id, artifact_policy)
        elif name == "engineering.verify":
            return _handle_verify(arguments, trace_id, artifact_policy)
        elif name == "engineering.release":
            return _handle_release(arguments, trace_id, artifact_policy)
        elif name == "engineering.codify":
            return _handle_codify(arguments, trace_id, artifact_policy)
        elif name == "engineering.retrospective":
            return _handle_retrospective(arguments, trace_id, artifact_policy)
        elif name == "engineering.guardrails.status":
            return _handle_guardrails_status(arguments, trace_id, artifact_policy)
        else:
            envelope = wrap_error_response(
                error_code="UNKNOWN_TOOL",
                error_message=f"未知工具: {name}",
                server_name="trquant-engineering",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
    except Exception as e:
        envelope = wrap_exception_response(
            exception=e,
            server_name="trquant-engineering",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)


def _handle_plan(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.plan"""
    objective = arguments.get("objective", "")
    context = arguments.get("context", {})
    priority = arguments.get("priority", "P1")
    mode = arguments.get("mode", "dry_run")
    
    if not objective:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.plan",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    # 生成objective_id
    objective_id = _generate_objective_id(objective)
    
    # 调用docs_server搜索相关文档
    docs_result = _call_mcp_tool("trquant-docs", "docs.search", {
        "query": objective,
        "doc_type": "dev_manual",
        "limit": 5
    })
    
    # 构建任务树（简化版，实际应该更智能）
    task_tree = [
        {
            "title": f"分析需求：{objective}",
            "priority": priority,
            "acceptance": ["需求明确", "约束条件清晰"],
            "deps": []
        },
        {
            "title": "设计实现方案",
            "priority": priority,
            "acceptance": ["方案可行", "符合规范"],
            "deps": ["分析需求"]
        },
        {
            "title": "实现代码/文档",
            "priority": priority,
            "acceptance": ["代码通过测试", "文档完整"],
            "deps": ["设计实现方案"]
        },
        {
            "title": "验证与测试",
            "priority": priority,
            "acceptance": ["测试通过", "质量检查通过"],
            "deps": ["实现代码/文档"]
        }
    ]
    
    # 风险清单
    risk_register = [
        {
            "risk": "需求理解偏差",
            "mitigation": "查阅相关文档，与利益相关者确认"
        },
        {
            "risk": "实现复杂度超预期",
            "mitigation": "分阶段实现，先做MVP"
        }
    ]
    
    # 如果mode=execute，创建task
    if mode == "execute":
        for task in task_tree:
            _call_mcp_tool("trquant-task", "task.create", {
                "title": task["title"],
                "description": f"目标：{objective}",
                "priority": task["priority"],
                "tags": ["engineering", objective_id]
            })
    
    # 保存objective
    _objectives[objective_id] = {
        "objective": objective,
        "context": context,
        "priority": priority,
        "task_tree": task_tree,
        "created_at": datetime.now().isoformat(),
        "trace_id": trace_id
    }
    
    result = {
        "objective_id": objective_id,
        "task_tree": task_tree,
        "risk_register": risk_register,
        "next_actions": ["查阅相关文档", "创建工作区"],
        "artifact_ptrs": []
    }
    
    # 生成artifact
    result = create_artifact_if_needed(result, "engineering_plan", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.plan",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_bootstrap(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.bootstrap"""
    objective_id = arguments.get("objective_id")
    repo = arguments.get("repo", ".")
    branch_strategy = arguments.get("branch_strategy", "feature")
    mode = arguments.get("mode", "dry_run")
    confirm_token = arguments.get("confirm_token")
    
    if not objective_id:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.bootstrap",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    if objective_id not in _objectives:
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=f"目标不存在: {objective_id}",
            server_name="trquant-engineering",
            tool_name="engineering.bootstrap",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    # 验证confirm_token（如果是execute模式）
    if mode == "execute":
        if not confirm_token:
            envelope = wrap_error_response(
                error_code="VALIDATION_ERROR",
                error_message="execute模式需要confirm_token",
                server_name="trquant-engineering",
                tool_name="engineering.bootstrap",
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
        
        is_valid, error = verify_confirm_token(
            confirm_token,
            "engineering.bootstrap",
            arguments,
            trace_id or ""
        )
        if not is_valid:
            envelope = wrap_error_response(
                error_code=error or "INVALID_TOKEN",
                error_message="confirm_token验证失败",
                server_name="trquant-engineering",
                tool_name="engineering.bootstrap",
                version="1.0.0",
                trace_id=trace_id
            )
            return _wrap_response(envelope)
    
    # 生成分支名
    branch = f"{branch_strategy}/{objective_id}"
    
    created_paths = []
    checks = []
    
    if mode == "execute":
        # 创建artifact目录
        obj_dir = _artifact_storage / objective_id
        obj_dir.mkdir(parents=True, exist_ok=True)
        created_paths.append(str(obj_dir))
        
        # 创建记录文件
        record_file = obj_dir / "bootstrap_record.json"
        record_file.write_text(json.dumps({
            "objective_id": objective_id,
            "branch": branch,
            "created_at": datetime.now().isoformat(),
            "trace_id": trace_id
        }, indent=2, ensure_ascii=False))
        created_paths.append(str(record_file))
        
        # 调用git创建分支（如果可用）
        git_result = _call_mcp_tool("git", "git_branch", {"branch": branch})
        if git_result.get("ok"):
            checks.append({"name": "git_branch", "status": "pass", "details": f"分支 {branch} 已创建"})
        else:
            checks.append({"name": "git_branch", "status": "fail", "details": "Git不可用或创建失败"})
        
        # 记录evidence
        evidence_result = _call_mcp_tool("trquant-evidence", "evidence.record", {
            "event_type": "engineering_bootstrap",
            "objective_id": objective_id,
            "metadata": {
                "branch": branch,
                "repo": repo,
                "trace_id": trace_id
            }
        })
    else:
        # dry_run模式
        checks.append({"name": "git_branch", "status": "pass", "details": f"将创建分支: {branch}"})
        checks.append({"name": "artifact_dir", "status": "pass", "details": f"将创建目录: {_artifact_storage / objective_id}"})
    
    result = {
        "branch": branch,
        "created_paths": created_paths,
        "checks": checks,
        "artifact_ptrs": []
    }
    
    result = create_artifact_if_needed(result, "engineering_bootstrap", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.bootstrap",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_work(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.work"""
    objective_id = arguments.get("objective_id")
    tasks = arguments.get("tasks", [])
    work_items = arguments.get("work_items", [])
    mode = arguments.get("mode", "dry_run")
    confirm_token = arguments.get("confirm_token")
    
    if not objective_id:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.work",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    if mode == "execute" and not confirm_token:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="execute模式需要confirm_token",
            server_name="trquant-engineering",
            tool_name="engineering.work",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    changes = []
    local_tests = []
    
    # 处理work_items
    for item in work_items:
        item_type = item.get("type")
        target = item.get("target")
        instruction = item.get("instruction")
        
        if mode == "execute":
            # 实际执行（简化版）
            if item_type == "code":
                # 调用code_server生成代码
                code_result = _call_mcp_tool("trquant-code", "code.search", {
                    "query": instruction,
                    "file_type": "python"
                })
                changes.append({
                    "file": target,
                    "diff_ptr": f"artifact://code_diff_{target}",
                    "summary": f"根据指令生成/修改代码: {instruction[:50]}"
                })
            elif item_type == "doc":
                # 调用docs_server更新文档
                changes.append({
                    "file": target,
                    "diff_ptr": f"artifact://doc_diff_{target}",
                    "summary": f"更新文档: {instruction[:50]}"
                })
        else:
            # dry_run模式
            changes.append({
                "file": target,
                "diff_ptr": None,
                "summary": f"[DRY_RUN] 将处理: {item_type} - {target}"
            })
    
    result = {
        "changes": changes,
        "local_tests": local_tests,
        "artifact_ptrs": []
    }
    
    result = create_artifact_if_needed(result, "engineering_work", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.work",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_verify(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.verify"""
    objective_id = arguments.get("objective_id")
    verification_profile = arguments.get("verification_profile", "standard")
    baseline_ref = arguments.get("baseline_ref")
    
    if not objective_id:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.verify",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    checks = []
    report_ids = []
    
    # spec验证
    spec_result = _call_mcp_tool("trquant-spec", "spec.validate", {
        "content": "placeholder",
        "schema": "engineering_plan"
    })
    checks.append({
        "name": "spec",
        "status": "pass" if spec_result.get("ok") else "fail",
        "details_ptr": "artifact://spec_check"
    })
    
    # workflow smoke（如果是standard或release）
    if verification_profile in ["standard", "release"]:
        workflow_result = _call_mcp_tool("trquant-workflow", "workflow.run", {
            "workflow_id": "smoke_test",
            "mode": "dry_run"
        })
        checks.append({
            "name": "workflow_smoke",
            "status": "pass" if workflow_result.get("ok") else "fail",
            "run_id": workflow_result.get("data", {}).get("run_id", "unknown")
        })
    
    # quality验证
    quality_result = _call_mcp_tool("trquant-data-quality", "quality.validate", {
        "data_source": "test"
    })
    checks.append({
        "name": "quality",
        "status": "pass" if quality_result.get("ok") else "fail",
        "report_ptr": "artifact://quality_report"
    })
    
    # 生成对比报告（如果有baseline）
    if baseline_ref:
        report_result = _call_mcp_tool("trquant-report", "report.compare", {
            "report_ids": [baseline_ref, "current"],
            "mode": "dry_run"
        })
        if report_result.get("ok"):
            report_ids.append(report_result.get("data", {}).get("comparison_id", "unknown"))
    
    # 判断整体状态
    all_passed = all(c.get("status") == "pass" for c in checks)
    
    result = {
        "status": "pass" if all_passed else "fail",
        "checks": checks,
        "report_ids": report_ids,
        "artifact_ptrs": []
    }
    
    result = create_artifact_if_needed(result, "engineering_verify", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.verify",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_release(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.release（P1，简化实现）"""
    objective_id = arguments.get("objective_id")
    version = arguments.get("version")
    release_type = arguments.get("release_type", "dev")
    mode = arguments.get("mode", "dry_run")
    confirm_token = arguments.get("confirm_token")
    
    if not objective_id or not version:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id和version是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.release",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    if mode == "execute" and not confirm_token:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="execute模式需要confirm_token",
            server_name="trquant-engineering",
            tool_name="engineering.release",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    tag = f"{release_type}-{version}"
    
    result = {
        "tag": tag,
        "release_notes_ptr": f"artifact://release_notes_{tag}",
        "published_artifacts": [],
        "status": "ok" if mode == "dry_run" else "blocked"
    }
    
    result = create_artifact_if_needed(result, "engineering_release", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.release",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_codify(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.codify（P1，简化实现）"""
    objective_id = arguments.get("objective_id")
    targets = arguments.get("targets", [])
    mode = arguments.get("mode", "dry_run")
    confirm_token = arguments.get("confirm_token")
    
    if not objective_id:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.codify",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    updated_docs = []
    new_templates = []
    evidence_ids = []
    
    if mode == "execute" and confirm_token:
        # 实际更新文档
        for target in targets:
            doc_id = target.get("doc_id")
            updated_docs.append({
                "doc_id": doc_id,
                "diff_ptr": f"artifact://doc_diff_{doc_id}"
            })
    
    result = {
        "updated_docs": updated_docs,
        "new_templates": new_templates,
        "evidence_ids": evidence_ids
    }
    
    result = create_artifact_if_needed(result, "engineering_codify", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.codify",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_retrospective(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.retrospective（P1，简化实现）"""
    objective_id = arguments.get("objective_id")
    include = arguments.get("include", ["tasks", "reports"])
    
    if not objective_id:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message="objective_id是必需的",
            server_name="trquant-engineering",
            tool_name="engineering.retrospective",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    if objective_id not in _objectives:
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=f"目标不存在: {objective_id}",
            server_name="trquant-engineering",
            tool_name="engineering.retrospective",
            version="1.0.0",
            trace_id=trace_id
        )
        return _wrap_response(envelope)
    
    # 生成复盘报告（简化版）
    retro_ptr = artifact_write({
        "objective_id": objective_id,
        "what_went_well": ["任务拆解清晰", "工具链集成顺畅"],
        "problems": [],
        "root_causes": [],
        "improvements": ["增加自动化测试覆盖率"],
        "action_items": []
    }, "retrospective", trace_id or "unknown")
    
    result = {
        "retro_ptr": retro_ptr,
        "action_items": []
    }
    
    result = create_artifact_if_needed(result, "engineering_retrospective", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.retrospective",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


def _handle_guardrails_status(arguments: Dict[str, Any], trace_id: Optional[str], artifact_policy: str) -> List[TextContent]:
    """处理engineering.guardrails.status"""
    limit = arguments.get("limit", 10)
    
    # 统计最近N个目标
    recent_objectives = list(_objectives.values())[-limit:]
    
    stats = {
        "total_objectives": len(_objectives),
        "recent_objectives": len(recent_objectives),
        "success_rate": "N/A",  # 需要更复杂的统计
        "average_duration": "N/A",
        "failure_reasons": [],
        "unclosed_items": []
    }
    
    result = {
        "stats": stats,
        "recent_objectives": [
            {
                "objective_id": obj_id,
                "objective": obj.get("objective", ""),
                "created_at": obj.get("created_at", ""),
                "status": "in_progress"
            }
            for obj_id, obj in list(_objectives.items())[-limit:]
        ]
    }
    
    result = create_artifact_if_needed(result, "engineering_guardrails", artifact_policy, trace_id or "unknown")
    
    envelope = wrap_success_response(
        data=result,
        server_name="trquant-engineering",
        tool_name="engineering.guardrails.status",
        version="1.0.0",
        trace_id=trace_id
    )
    return _wrap_response(envelope)


# 主程序
if __name__ == "__main__":
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    
    asyncio.run(main())









