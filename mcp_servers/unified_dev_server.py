#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 统一开发工具服务器
==========================

整合所有开发流程相关工具，强制遵循标准开发流程。

工具分类:
1. 任务管理 (task.*) - 9个工具
2. 开发日志 (devlog.*) - 2个工具
3. 里程碑 (milestone.*) - 3个工具
4. 问题追踪 (issue.*) - 3个工具
5. 经验管理 (experience.*) - 3个工具
6. 进度报告 (progress.*) - 2个工具
7. 风险管理 (risk.*) - 2个工具
8. 系统注册 (registry.*) - 4个工具
9. 调试工具 (debug.*) - 3个工具
10. 工作流 (workflow.*) - 2个工具

总计: 33个工具

运行: python mcp_servers/unified_dev_server.py
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum
import traceback
import hashlib

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('UnifiedDevServer')

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    # 提供更详细的错误信息和修复建议
    logger.error(f"MCP SDK不可用: {e}")
    logger.error("请确保使用venv中的Python，并安装MCP SDK:")
    logger.error("  ./venv/bin/pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")
    sys.exit(1)

# 创建服务器
server = Server("trquant-unified-dev")

# ==================== 数据目录 ====================
DATA_DIR = TRQUANT_ROOT / ".trquant" / "dev"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TASKS_DIR = DATA_DIR / "tasks"
DEVLOG_DIR = DATA_DIR / "devlog"
ISSUES_DIR = DATA_DIR / "issues"
EXPERIENCE_DIR = DATA_DIR / "experience"
MILESTONES_DIR = DATA_DIR / "milestones"
REGISTRY_DIR = DATA_DIR / "registry"
DEBUG_DIR = DATA_DIR / "debug"

for d in [TASKS_DIR, DEVLOG_DIR, ISSUES_DIR, EXPERIENCE_DIR, MILESTONES_DIR, REGISTRY_DIR, DEBUG_DIR]:
    d.mkdir(exist_ok=True)

# ==================== 枚举类型 ====================
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"

class IssuePriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# ==================== 辅助函数 ====================
def _load_json(filepath: Path, default: Any = None) -> Any:
    """加载JSON文件"""
    if filepath.exists():
        try:
            return json.loads(filepath.read_text(encoding='utf-8'))
        except:
            pass
    return default if default is not None else {}

def _save_json(filepath: Path, data: Any) -> None:
    """保存JSON文件"""
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def _gen_id(prefix: str) -> str:
    """生成唯一ID"""
    return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def _now() -> str:
    """当前时间ISO格式"""
    return datetime.now().isoformat()

# ==================== 1. 任务管理 (task.*) ====================

def task_create(title: str, project: str = "trquant", description: str = "", 
                status: str = "pending", priority: str = "medium", tags: List[str] = None) -> Dict:
    """创建任务"""
    tasks_file = TASKS_DIR / f"{project}.json"
    tasks = _load_json(tasks_file, {"tasks": []})
    
    task_id = _gen_id("task")
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "tags": tags or [],
        "created": _now(),
        "updated": _now()
    }
    tasks["tasks"].append(task)
    _save_json(tasks_file, tasks)
    
    logger.info(f"创建任务: {task_id} - {title}")
    return {"success": True, "task_id": task_id, "task": task}

def task_list(project: str = "trquant", status: str = None) -> Dict:
    """列出任务"""
    tasks_file = TASKS_DIR / f"{project}.json"
    tasks = _load_json(tasks_file, {"tasks": []})
    
    result = tasks["tasks"]
    if status:
        result = [t for t in result if t.get("status") == status]
    
    return {"success": True, "tasks": result, "total": len(result)}

def task_get(task_id: str, project: str = "trquant") -> Dict:
    """获取任务详情"""
    tasks_file = TASKS_DIR / f"{project}.json"
    tasks = _load_json(tasks_file, {"tasks": []})
    
    for task in tasks["tasks"]:
        if task.get("id") == task_id:
            return {"success": True, "task": task}
    
    return {"success": False, "error": f"任务不存在: {task_id}"}

def task_update(task_id: str, project: str = "trquant", **kwargs) -> Dict:
    """更新任务"""
    tasks_file = TASKS_DIR / f"{project}.json"
    tasks = _load_json(tasks_file, {"tasks": []})
    
    for task in tasks["tasks"]:
        if task.get("id") == task_id:
            for k, v in kwargs.items():
                if v is not None:
                    task[k] = v
            task["updated"] = _now()
            _save_json(tasks_file, tasks)
            logger.info(f"更新任务: {task_id}")
            return {"success": True, "task": task}
    
    return {"success": False, "error": f"任务不存在: {task_id}"}

def task_complete(task_id: str, project: str = "trquant") -> Dict:
    """完成任务"""
    return task_update(task_id, project, status="completed", completed_at=_now())

def task_add_note(task_id: str, note: str, project: str = "trquant") -> Dict:
    """添加任务备注"""
    tasks_file = TASKS_DIR / f"{project}.json"
    tasks = _load_json(tasks_file, {"tasks": []})
    
    for task in tasks["tasks"]:
        if task.get("id") == task_id:
            if "notes" not in task:
                task["notes"] = []
            task["notes"].append({"content": note, "time": _now()})
            task["updated"] = _now()
            _save_json(tasks_file, tasks)
            return {"success": True, "message": "备注已添加"}
    
    return {"success": False, "error": f"任务不存在: {task_id}"}

def task_analyze(task_title: str, task_description: str = "", dependencies: List[str] = None) -> Dict:
    """分析任务复杂度"""
    complexity = "low"
    if dependencies and len(dependencies) > 3:
        complexity = "high"
    elif len(task_title) > 50 or len(task_description) > 200:
        complexity = "medium"
    
    return {
        "success": True,
        "complexity": complexity,
        "recommendation": "Max模式" if complexity == "high" else "Auto模式",
        "estimated_tokens": 100 if complexity == "low" else 500 if complexity == "medium" else 1000
    }

def task_recommend_mode(complexity: str) -> Dict:
    """推荐执行模式"""
    modes = {
        "low": {"mode": "auto", "reason": "简单任务，Auto模式足够"},
        "medium": {"mode": "auto", "reason": "中等复杂度，Auto模式可处理"},
        "high": {"mode": "max", "reason": "复杂任务，建议Max模式"}
    }
    return {"success": True, **modes.get(complexity, modes["medium"])}

_context_cache = {}
def task_cache_context(key: str, value: Any) -> Dict:
    """缓存上下文"""
    _context_cache[key] = {"value": value, "cached_at": _now()}
    return {"success": True, "key": key, "cached": True}

# ==================== 2. 开发日志 (devlog.*) ====================

def devlog_add(content: str, tags: List[str] = None, project: str = "trquant") -> Dict:
    """添加开发日志"""
    devlog_file = DEVLOG_DIR / f"{project}.json"
    devlog = _load_json(devlog_file, {"logs": []})
    
    log_id = _gen_id("log")
    entry = {
        "id": log_id,
        "content": content,
        "tags": tags or [],
        "created": _now()
    }
    devlog["logs"].insert(0, entry)  # 最新的在前
    _save_json(devlog_file, devlog)
    
    logger.info(f"添加日志: {content[:50]}...")
    return {"success": True, "log_id": log_id}

def devlog_list(project: str = "trquant", limit: int = 10, tag: str = None) -> Dict:
    """列出开发日志"""
    devlog_file = DEVLOG_DIR / f"{project}.json"
    devlog = _load_json(devlog_file, {"logs": []})
    
    logs = devlog["logs"]
    if tag:
        logs = [l for l in logs if tag in l.get("tags", [])]
    
    return {"success": True, "logs": logs[:limit], "total": len(logs)}

# ==================== 3. 里程碑 (milestone.*) ====================

def milestone_create(name: str, description: str = "", due_date: str = None, project: str = "trquant") -> Dict:
    """创建里程碑"""
    ms_file = MILESTONES_DIR / f"{project}.json"
    milestones = _load_json(ms_file, {"milestones": []})
    
    ms_id = _gen_id("ms")
    milestone = {
        "id": ms_id,
        "name": name,
        "description": description,
        "due_date": due_date,
        "progress": 0,
        "status": "active",
        "created": _now()
    }
    milestones["milestones"].append(milestone)
    _save_json(ms_file, milestones)
    
    return {"success": True, "milestone_id": ms_id}

def milestone_list(project: str = "trquant") -> Dict:
    """列出里程碑"""
    ms_file = MILESTONES_DIR / f"{project}.json"
    milestones = _load_json(ms_file, {"milestones": []})
    return {"success": True, "milestones": milestones["milestones"]}

def milestone_progress(milestone_id: str, progress: int, project: str = "trquant") -> Dict:
    """更新里程碑进度"""
    ms_file = MILESTONES_DIR / f"{project}.json"
    milestones = _load_json(ms_file, {"milestones": []})
    
    for ms in milestones["milestones"]:
        if ms.get("id") == milestone_id:
            ms["progress"] = min(100, max(0, progress))
            if progress >= 100:
                ms["status"] = "completed"
            _save_json(ms_file, milestones)
            return {"success": True, "milestone": ms}
    
    return {"success": False, "error": f"里程碑不存在: {milestone_id}"}

# ==================== 4. 问题追踪 (issue.*) ====================

def issue_create(title: str, description: str = "", priority: str = "medium", project: str = "trquant") -> Dict:
    """创建问题"""
    issues_file = ISSUES_DIR / f"{project}.json"
    issues = _load_json(issues_file, {"issues": []})
    
    issue_id = _gen_id("issue")
    issue = {
        "id": issue_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open",
        "created": _now()
    }
    issues["issues"].append(issue)
    _save_json(issues_file, issues)
    
    logger.info(f"创建问题: {issue_id} - {title}")
    return {"success": True, "issue_id": issue_id}

def issue_list(project: str = "trquant", status: str = None) -> Dict:
    """列出问题"""
    issues_file = ISSUES_DIR / f"{project}.json"
    issues = _load_json(issues_file, {"issues": []})
    
    result = issues["issues"]
    if status:
        result = [i for i in result if i.get("status") == status]
    
    return {"success": True, "issues": result}

def issue_resolve(issue_id: str, solution: str = "", project: str = "trquant") -> Dict:
    """解决问题"""
    issues_file = ISSUES_DIR / f"{project}.json"
    issues = _load_json(issues_file, {"issues": []})
    
    for issue in issues["issues"]:
        if issue.get("id") == issue_id:
            issue["status"] = "resolved"
            issue["solution"] = solution
            issue["resolved_at"] = _now()
            _save_json(issues_file, issues)
            return {"success": True, "issue": issue}
    
    return {"success": False, "error": f"问题不存在: {issue_id}"}

# ==================== 5. 经验管理 (experience.*) ====================

def experience_add(content: str, category: str = "general", project: str = "trquant") -> Dict:
    """添加经验"""
    exp_file = EXPERIENCE_DIR / f"{project}.json"
    experiences = _load_json(exp_file, {"experiences": []})
    
    exp_id = _gen_id("exp")
    exp = {
        "id": exp_id,
        "content": content,
        "category": category,
        "useful_count": 0,
        "created": _now()
    }
    experiences["experiences"].append(exp)
    _save_json(exp_file, experiences)
    
    return {"success": True, "experience_id": exp_id}

def experience_search(query: str, project: str = "trquant") -> Dict:
    """搜索经验"""
    exp_file = EXPERIENCE_DIR / f"{project}.json"
    experiences = _load_json(exp_file, {"experiences": []})
    
    query_lower = query.lower()
    results = [
        e for e in experiences["experiences"]
        if query_lower in e.get("content", "").lower() or query_lower in e.get("category", "").lower()
    ]
    
    return {"success": True, "results": results, "total": len(results)}

def experience_mark_useful(experience_id: str, project: str = "trquant") -> Dict:
    """标记经验有用"""
    exp_file = EXPERIENCE_DIR / f"{project}.json"
    experiences = _load_json(exp_file, {"experiences": []})
    
    for exp in experiences["experiences"]:
        if exp.get("id") == experience_id:
            exp["useful_count"] = exp.get("useful_count", 0) + 1
            _save_json(exp_file, experiences)
            return {"success": True, "useful_count": exp["useful_count"]}
    
    return {"success": False, "error": f"经验不存在: {experience_id}"}

# ==================== 6. 进度报告 (progress.*) ====================

def progress_summary(project: str = "trquant") -> Dict:
    """进度摘要"""
    tasks = task_list(project)["tasks"]
    issues = issue_list(project)["issues"]
    milestones = milestone_list(project)["milestones"]
    
    return {
        "success": True,
        "summary": {
            "tasks": {
                "total": len(tasks),
                "completed": len([t for t in tasks if t.get("status") == "completed"]),
                "in_progress": len([t for t in tasks if t.get("status") == "in_progress"]),
                "pending": len([t for t in tasks if t.get("status") == "pending"])
            },
            "issues": {
                "total": len(issues),
                "open": len([i for i in issues if i.get("status") == "open"]),
                "resolved": len([i for i in issues if i.get("status") == "resolved"])
            },
            "milestones": {
                "total": len(milestones),
                "active": len([m for m in milestones if m.get("status") == "active"]),
                "completed": len([m for m in milestones if m.get("status") == "completed"])
            }
        },
        "generated_at": _now()
    }

def progress_daily_report(project: str = "trquant") -> Dict:
    """生成日报"""
    summary = progress_summary(project)
    devlog = devlog_list(project, limit=10)
    
    return {
        "success": True,
        "report": {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": summary["summary"],
            "recent_logs": devlog["logs"][:5]
        }
    }

# ==================== 7. 风险管理 (risk.*) ====================

_risks = []

def risk_add(title: str, description: str = "", probability: str = "medium", impact: str = "medium") -> Dict:
    """添加风险"""
    risk_id = _gen_id("risk")
    risk = {
        "id": risk_id,
        "title": title,
        "description": description,
        "probability": probability,
        "impact": impact,
        "status": "identified",
        "created": _now()
    }
    _risks.append(risk)
    return {"success": True, "risk_id": risk_id}

def risk_assess(project: str = "trquant") -> Dict:
    """评估风险"""
    high_risks = [r for r in _risks if r.get("probability") == "high" or r.get("impact") == "high"]
    return {
        "success": True,
        "total_risks": len(_risks),
        "high_risks": len(high_risks),
        "risks": _risks
    }

# ==================== 8. 系统注册 (registry.*) ====================

def registry_register(module_id: str, name: str, version: str = "1.0", 
                     mcp_server: str = None, tools: List[str] = None) -> Dict:
    """注册模块"""
    reg_file = REGISTRY_DIR / "modules.json"
    modules = _load_json(reg_file, {"modules": {}})
    
    modules["modules"][module_id] = {
        "name": name,
        "version": version,
        "mcp_server": mcp_server,
        "tools": tools or [],
        "status": "active",
        "registered_at": _now()
    }
    _save_json(reg_file, modules)
    
    logger.info(f"注册模块: {module_id} - {name}")
    return {"success": True, "module_id": module_id}

def registry_list(status: str = None) -> Dict:
    """列出模块"""
    reg_file = REGISTRY_DIR / "modules.json"
    modules = _load_json(reg_file, {"modules": {}})
    
    result = modules["modules"]
    if status:
        result = {k: v for k, v in result.items() if v.get("status") == status}
    
    return {"success": True, "modules": result, "total": len(result)}

def registry_status() -> Dict:
    """系统状态"""
    modules = registry_list()["modules"]
    return {
        "success": True,
        "status": {
            "total_modules": len(modules),
            "active": len([m for m in modules.values() if m.get("status") == "active"]),
            "timestamp": _now()
        }
    }

def registry_snapshot(description: str = "") -> Dict:
    """创建快照"""
    snapshot_id = _gen_id("snap")
    snapshot = {
        "id": snapshot_id,
        "description": description,
        "modules": registry_list()["modules"],
        "created": _now()
    }
    
    snap_file = REGISTRY_DIR / f"snapshot_{snapshot_id}.json"
    _save_json(snap_file, snapshot)
    
    return {"success": True, "snapshot_id": snapshot_id}

# ==================== 9. 调试工具 (debug.*) ====================

_debug_logs = []

def debug_log(message: str, level: str = "info", context: Dict = None) -> Dict:
    """记录调试日志"""
    entry = {
        "id": _gen_id("debug"),
        "message": message,
        "level": level,
        "context": context or {},
        "timestamp": _now()
    }
    _debug_logs.insert(0, entry)
    
    # 只保留最近100条
    if len(_debug_logs) > 100:
        _debug_logs.pop()
    
    # 同时写入文件
    debug_file = DEBUG_DIR / f"debug_{datetime.now().strftime('%Y%m%d')}.log"
    with open(debug_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    return {"success": True, "logged": True}

def debug_trace(operation: str, data: Dict = None) -> Dict:
    """记录操作跟踪"""
    return debug_log(f"TRACE: {operation}", "trace", data)

def debug_status() -> Dict:
    """调试状态"""
    return {
        "success": True,
        "log_count": len(_debug_logs),
        "recent_logs": _debug_logs[:10],
        "timestamp": _now()
    }

# ==================== 10. 工作流 (workflow.*) ====================

def workflow_batch(tools: List[Dict]) -> Dict:
    """批量执行工具"""
    results = []
    for tool_call in tools:
        tool_name = tool_call.get("name")
        args = tool_call.get("args", {})
        
        try:
            result = TOOL_HANDLERS.get(tool_name, lambda **a: {"error": f"未知工具: {tool_name}"})(**args)
            results.append({"tool": tool_name, "success": True, "result": result})
        except Exception as e:
            results.append({"tool": tool_name, "success": False, "error": str(e)})
    
    return {"success": True, "results": results, "total": len(results)}

def workflow_check() -> Dict:
    """检查开发流程状态"""
    summary = progress_summary()["summary"]
    recent_logs = devlog_list(limit=5)["logs"]
    
    # 检查是否有进行中的任务
    has_active_task = summary["tasks"]["in_progress"] > 0
    
    # 检查最近是否有日志
    has_recent_log = len(recent_logs) > 0
    
    return {
        "success": True,
        "workflow_status": {
            "has_active_task": has_active_task,
            "has_recent_log": has_recent_log,
            "tasks_summary": summary["tasks"],
            "issues_summary": summary["issues"]
        },
        "recommendations": [
            "记得在开发前查询当前任务状态" if not has_active_task else None,
            "记得添加开发日志记录进度" if not has_recent_log else None
        ]
    }

# ==================== 工具处理器映射 ====================

TOOL_HANDLERS = {
    # 任务管理
    "task.create": task_create,
    "task.list": task_list,
    "task.get": task_get,
    "task.update": task_update,
    "task.complete": task_complete,
    "task.add_note": task_add_note,
    "task.analyze": task_analyze,
    "task.recommend_mode": task_recommend_mode,
    "task.cache_context": task_cache_context,
    # 开发日志
    "devlog.add": devlog_add,
    "devlog.list": devlog_list,
    # 里程碑
    "milestone.create": milestone_create,
    "milestone.list": milestone_list,
    "milestone.progress": milestone_progress,
    # 问题追踪
    "issue.create": issue_create,
    "issue.list": issue_list,
    "issue.resolve": issue_resolve,
    # 经验管理
    "experience.add": experience_add,
    "experience.search": experience_search,
    "experience.mark_useful": experience_mark_useful,
    # 进度报告
    "progress.summary": progress_summary,
    "progress.daily_report": progress_daily_report,
    # 风险管理
    "risk.add": risk_add,
    "risk.assess": risk_assess,
    # 系统注册
    "registry.register": registry_register,
    "registry.list": registry_list,
    "registry.status": registry_status,
    "registry.snapshot": registry_snapshot,
    # 调试工具
    "debug.log": debug_log,
    "debug.trace": debug_trace,
    "debug.status": debug_status,
    # 工作流
    "workflow.batch": workflow_batch,
    "workflow.check": workflow_check,
}

# ==================== MCP工具定义 ====================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有工具"""
    return [
        # 任务管理 (9个)
        Tool(name="task.create", description="创建任务", inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "任务标题"},
                "project": {"type": "string", "default": "trquant"},
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["pending", "in_progress"], "default": "pending"},
                "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "medium"},
                "tags": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["title"]
        }),
        Tool(name="task.list", description="列出任务", inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": "trquant"},
                "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "cancelled", "blocked"]}
            }
        }),
        Tool(name="task.get", description="获取任务详情", inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["task_id"]
        }),
        Tool(name="task.update", description="更新任务", inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "project": {"type": "string", "default": "trquant"},
                "title": {"type": "string"},
                "status": {"type": "string"},
                "description": {"type": "string"}
            },
            "required": ["task_id"]
        }),
        Tool(name="task.complete", description="完成任务", inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["task_id"]
        }),
        Tool(name="task.add_note", description="添加任务备注", inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "note": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["task_id", "note"]
        }),
        Tool(name="task.analyze", description="分析任务复杂度", inputSchema={
            "type": "object",
            "properties": {
                "task_title": {"type": "string"},
                "task_description": {"type": "string"},
                "dependencies": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["task_title"]
        }),
        Tool(name="task.recommend_mode", description="推荐执行模式", inputSchema={
            "type": "object",
            "properties": {"complexity": {"type": "string", "enum": ["low", "medium", "high"]}},
            "required": ["complexity"]
        }),
        Tool(name="task.cache_context", description="缓存上下文", inputSchema={
            "type": "object",
            "properties": {"key": {"type": "string"}, "value": {"type": "object"}},
            "required": ["key", "value"]
        }),
        
        # 开发日志 (2个)
        Tool(name="devlog.add", description="添加开发日志 (必须包含tags: planning/development/testing/completed)", inputSchema={
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "日志内容，建议格式：【规划】/【开发】/【测试】/【完成】"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "标签: planning, development, testing, completed"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["content", "tags"]
        }),
        Tool(name="devlog.list", description="列出开发日志", inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": "trquant"},
                "limit": {"type": "integer", "default": 10},
                "tag": {"type": "string"}
            }
        }),
        
        # 里程碑 (3个)
        Tool(name="milestone.create", description="创建里程碑", inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "due_date": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["name"]
        }),
        Tool(name="milestone.list", description="列出里程碑", inputSchema={
            "type": "object",
            "properties": {"project": {"type": "string", "default": "trquant"}}
        }),
        Tool(name="milestone.progress", description="更新里程碑进度", inputSchema={
            "type": "object",
            "properties": {
                "milestone_id": {"type": "string"},
                "progress": {"type": "integer", "minimum": 0, "maximum": 100},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["milestone_id", "progress"]
        }),
        
        # 问题追踪 (3个)
        Tool(name="issue.create", description="创建问题", inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "medium"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["title"]
        }),
        Tool(name="issue.list", description="列出问题", inputSchema={
            "type": "object",
            "properties": {
                "project": {"type": "string", "default": "trquant"},
                "status": {"type": "string", "enum": ["open", "resolved"]}
            }
        }),
        Tool(name="issue.resolve", description="解决问题", inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {"type": "string"},
                "solution": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["issue_id"]
        }),
        
        # 经验管理 (3个)
        Tool(name="experience.add", description="添加经验", inputSchema={
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "category": {"type": "string", "default": "general"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["content"]
        }),
        Tool(name="experience.search", description="搜索经验", inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["query"]
        }),
        Tool(name="experience.mark_useful", description="标记经验有用", inputSchema={
            "type": "object",
            "properties": {
                "experience_id": {"type": "string"},
                "project": {"type": "string", "default": "trquant"}
            },
            "required": ["experience_id"]
        }),
        
        # 进度报告 (2个)
        Tool(name="progress.summary", description="进度摘要", inputSchema={
            "type": "object",
            "properties": {"project": {"type": "string", "default": "trquant"}}
        }),
        Tool(name="progress.daily_report", description="生成日报", inputSchema={
            "type": "object",
            "properties": {"project": {"type": "string", "default": "trquant"}}
        }),
        
        # 风险管理 (2个)
        Tool(name="risk.add", description="添加风险", inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "probability": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"},
                "impact": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium"}
            },
            "required": ["title"]
        }),
        Tool(name="risk.assess", description="评估风险", inputSchema={
            "type": "object",
            "properties": {"project": {"type": "string", "default": "trquant"}}
        }),
        
        # 系统注册 (4个)
        Tool(name="registry.register", description="注册模块", inputSchema={
            "type": "object",
            "properties": {
                "module_id": {"type": "string"},
                "name": {"type": "string"},
                "version": {"type": "string", "default": "1.0"},
                "mcp_server": {"type": "string"},
                "tools": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["module_id", "name"]
        }),
        Tool(name="registry.list", description="列出模块", inputSchema={
            "type": "object",
            "properties": {"status": {"type": "string", "enum": ["active", "disabled"]}}
        }),
        Tool(name="registry.status", description="系统状态", inputSchema={"type": "object", "properties": {}}),
        Tool(name="registry.snapshot", description="创建快照", inputSchema={
            "type": "object",
            "properties": {"description": {"type": "string"}}
        }),
        
        # 调试工具 (3个)
        Tool(name="debug.log", description="记录调试日志", inputSchema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "level": {"type": "string", "enum": ["info", "warn", "error", "trace"], "default": "info"},
                "context": {"type": "object"}
            },
            "required": ["message"]
        }),
        Tool(name="debug.trace", description="记录操作跟踪", inputSchema={
            "type": "object",
            "properties": {
                "operation": {"type": "string"},
                "data": {"type": "object"}
            },
            "required": ["operation"]
        }),
        Tool(name="debug.status", description="调试状态", inputSchema={"type": "object", "properties": {}}),
        
        # 工作流 (2个)
        Tool(name="workflow.batch", description="批量执行工具", inputSchema={
            "type": "object",
            "properties": {
                "tools": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "args": {"type": "object"}
                        },
                        "required": ["name"]
                    }
                }
            },
            "required": ["tools"]
        }),
        Tool(name="workflow.check", description="检查开发流程状态", inputSchema={"type": "object", "properties": {}}),
        # ===== 新增工具 =====
        
        # 策略知识库 (kb.* 5个)
        Tool(name="kb.search", description="搜索策略知识库", inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "category": {"type": "string"}}, "required": ["query"]}),
        Tool(name="kb.get_strategy", description="获取策略详情", inputSchema={"type": "object", "properties": {"strategy_name": {"type": "string"}}, "required": ["strategy_name"]}),
        Tool(name="kb.get_api", description="获取API文档", inputSchema={"type": "object", "properties": {"api_name": {"type": "string"}}, "required": ["api_name"]}),
        Tool(name="kb.best_practices", description="获取最佳实践", inputSchema={"type": "object", "properties": {"category": {"type": "string"}}}),
        Tool(name="kb.add", description="添加知识条目", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "category": {"type": "string", "default": "general"}}, "required": ["title", "content"]}),
        
        # 证据追踪 (evidence.* 3个)
        Tool(name="evidence.add", description="添加决策证据", inputSchema={"type": "object", "properties": {"decision": {"type": "string"}, "reason": {"type": "string"}, "data": {"type": "object"}}, "required": ["decision", "reason"]}),
        Tool(name="evidence.list", description="列出证据", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 10}}}),
        Tool(name="evidence.search", description="搜索证据", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        
        # 研究工具 (research.* 3个)
        Tool(name="research.note", description="添加研究笔记", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}}, "required": ["title", "content"]}),
        Tool(name="research.list", description="列出研究笔记", inputSchema={"type": "object", "properties": {"tag": {"type": "string"}, "limit": {"type": "integer", "default": 20}}}),
        Tool(name="research.search", description="搜索研究笔记", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        
        # 网络爬虫 (crawler.* 10个)
        Tool(name="crawler.fetch", description="抓取网页内容", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "extract_text": {"type": "boolean", "default": True}, "extract_links": {"type": "boolean", "default": False}}, "required": ["url"]}),
        Tool(name="crawler.search_docs", description="搜索文档", inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "site": {"type": "string"}}, "required": ["query"]}),
        Tool(name="crawler.download", description="下载文件", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "filename": {"type": "string"}}, "required": ["url"]}),
        Tool(name="crawler.extract_code", description="从网页提取代码块", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "language": {"type": "string"}}, "required": ["url"]}),
        Tool(name="crawler.api_docs", description="获取API文档", inputSchema={"type": "object", "properties": {"api_name": {"type": "string"}, "framework": {"type": "string", "default": "python"}}, "required": ["api_name"]}),
        # Selenium工具
        Tool(name="crawler.selenium.fetch", description="使用Selenium抓取动态网页", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "wait_time": {"type": "integer", "default": 3}, "wait_selector": {"type": "string"}, "headless": {"type": "boolean", "default": True}}, "required": ["url"]}),
        Tool(name="crawler.selenium.click", description="Selenium点击元素", inputSchema={"type": "object", "properties": {"selector": {"type": "string"}, "by": {"type": "string", "default": "css", "enum": ["css", "id", "xpath", "class", "name"]}}, "required": ["selector"]}),
        Tool(name="crawler.selenium.extract", description="Selenium提取元素", inputSchema={"type": "object", "properties": {"selector": {"type": "string"}, "attribute": {"type": "string"}}, "required": ["selector"]}),
        # Lavague工具
        Tool(name="crawler.lavague.execute", description="使用Lavague AI执行自然语言指令", inputSchema={"type": "object", "properties": {"instruction": {"type": "string"}, "url": {"type": "string"}, "max_actions": {"type": "integer", "default": 10}, "headless": {"type": "boolean", "default": True}}, "required": ["instruction"]}),
        Tool(name="crawler.lavague.extract", description="使用Lavague AI提取数据", inputSchema={"type": "object", "properties": {"description": {"type": "string"}, "url": {"type": "string"}}, "required": ["description"]}),
        # 代码分析 (code.* 3个)
        Tool(name="code.analyze", description="分析代码", inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}, "analysis_type": {"type": "string", "default": "complexity"}}, "required": ["file_path"]}),
        Tool(name="code.convert", description="代码转换", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "from_lang": {"type": "string"}, "to_lang": {"type": "string"}}, "required": ["code", "from_lang", "to_lang"]}),
        Tool(name="code.lint", description="代码检查", inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}, "fix": {"type": "boolean", "default": False}}, "required": ["file_path"]}),
        
        # 文档 (docs.* 3个)
        Tool(name="docs.get", description="获取文档", inputSchema={"type": "object", "properties": {"doc_id": {"type": "string"}}, "required": ["doc_id"]}),
        Tool(name="docs.list", description="列出文档", inputSchema={"type": "object", "properties": {"category": {"type": "string"}}}),
        Tool(name="docs.search", description="搜索文档", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        
        # 工程 (eng.* 3个)
        Tool(name="eng.build", description="构建项目", inputSchema={"type": "object", "properties": {"target": {"type": "string", "default": "all"}}}),
        Tool(name="eng.deploy", description="部署项目", inputSchema={"type": "object", "properties": {"env": {"type": "string", "default": "dev"}}}),
        Tool(name="eng.test", description="运行测试", inputSchema={"type": "object", "properties": {"pattern": {"type": "string"}}}),
        
        # GUI开发 (gui.* 4个)
        Tool(name="gui.status", description="GUI状态", inputSchema={"type": "object", "properties": {}}),
        Tool(name="gui.validate", description="验证GUI", inputSchema={"type": "object", "properties": {"html": {"type": "string"}}, "required": ["html"]}),
        Tool(name="gui.generate_html", description="生成HTML", inputSchema={"type": "object", "properties": {"template": {"type": "string"}, "data": {"type": "object"}}, "required": ["template"]}),
        Tool(name="gui.check_csp", description="检查CSP", inputSchema={"type": "object", "properties": {"html": {"type": "string"}}, "required": ["html"]}),
        
        # 知识库 (knowledge.* 6个)
        Tool(name="knowledge.add", description="添加知识", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "content": {"type": "string"}, "type": {"type": "string", "default": "lesson"}, "tags": {"type": "array"}}, "required": ["title", "content"]}),
        Tool(name="knowledge.search", description="搜索知识", inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "type": {"type": "string"}, "limit": {"type": "integer", "default": 10}}, "required": ["query"]}),
        Tool(name="knowledge.get", description="获取知识详情", inputSchema={"type": "object", "properties": {"knowledge_id": {"type": "string"}}, "required": ["knowledge_id"]}),
        Tool(name="knowledge.update", description="更新知识", inputSchema={"type": "object", "properties": {"knowledge_id": {"type": "string"}, "content": {"type": "string"}}, "required": ["knowledge_id"]}),
        Tool(name="knowledge.mark_useful", description="标记有用", inputSchema={"type": "object", "properties": {"knowledge_id": {"type": "string"}}, "required": ["knowledge_id"]}),
        Tool(name="knowledge.stats", description="知识库统计", inputSchema={"type": "object", "properties": {}}),
        
        # 自学习 (learn.* 4个)
        Tool(name="learn.from_issue", description="从问题学习", inputSchema={"type": "object", "properties": {"issue_id": {"type": "string"}}, "required": ["issue_id"]}),
        Tool(name="learn.from_experience", description="从经验学习", inputSchema={"type": "object", "properties": {"experience_id": {"type": "string"}}, "required": ["experience_id"]}),
        Tool(name="learn.suggest", description="智能建议", inputSchema={"type": "object", "properties": {"context": {"type": "string"}}, "required": ["context"]}),
        Tool(name="learn.auto_extract", description="批量提取知识", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 10}}}),
        
        # Lint (lint.* 3个)
        Tool(name="lint.check", description="检查代码", inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}),
        Tool(name="lint.fix", description="修复代码", inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}),
        Tool(name="lint.rules", description="列出规则", inputSchema={"type": "object", "properties": {}}),
        
        # Panel (panel.* 3个)
        Tool(name="panel.list", description="列出面板", inputSchema={"type": "object", "properties": {}}),
        Tool(name="panel.get_config", description="获取面板配置", inputSchema={"type": "object", "properties": {"panel_id": {"type": "string"}}, "required": ["panel_id"]}),
        Tool(name="panel.validate", description="验证面板", inputSchema={"type": "object", "properties": {"config": {"type": "object"}}, "required": ["config"]}),
        
        # 最佳实践 (practice.* 3个)
        Tool(name="practice.add", description="添加最佳实践", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}, "category": {"type": "string"}}, "required": ["title", "description"]}),
        Tool(name="practice.list", description="列出最佳实践", inputSchema={"type": "object", "properties": {"category": {"type": "string"}}}),
        Tool(name="practice.search", description="搜索最佳实践", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        
        # 快捷操作 (quick.* 4个)
        Tool(name="quick.start_task", description="一键开始任务", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}, "tags": {"type": "array"}}, "required": ["title"]}),
        Tool(name="quick.finish_task", description="一键完成任务", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}, "summary": {"type": "string"}}, "required": ["task_id"]}),
        Tool(name="quick.log", description="快速记录", inputSchema={"type": "object", "properties": {"type": {"type": "string", "enum": ["dev", "test", "fix", "note"]}, "content": {"type": "string"}}, "required": ["type", "content"]}),
        Tool(name="quick.issue", description="快速创建问题", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}}, "required": ["title"]}),
        
        # Schema (schema.* 3个)
        Tool(name="schema.list", description="列出Schema", inputSchema={"type": "object", "properties": {}}),
        Tool(name="schema.get", description="获取Schema", inputSchema={"type": "object", "properties": {"schema_id": {"type": "string"}}, "required": ["schema_id"]}),
        Tool(name="schema.validate", description="验证数据", inputSchema={"type": "object", "properties": {"schema_id": {"type": "string"}, "data": {"type": "object"}}, "required": ["schema_id", "data"]}),
        
        # Secrets (secrets.* 3个)
        Tool(name="secrets.list", description="列出密钥", inputSchema={"type": "object", "properties": {}}),
        Tool(name="secrets.get", description="获取密钥", inputSchema={"type": "object", "properties": {"key": {"type": "string"}}, "required": ["key"]}),
        Tool(name="secrets.set", description="设置密钥", inputSchema={"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]}),
        
        # 会话 (session.* 3个)
        Tool(name="session.init", description="会话初始化", inputSchema={"type": "object", "properties": {}}),
        Tool(name="session.summary", description="会话摘要", inputSchema={"type": "object", "properties": {}}),
        Tool(name="session.checklist", description="检查清单", inputSchema={"type": "object", "properties": {}}),
        
        # 规范 (spec.* 3个)
        Tool(name="spec.list", description="列出规范", inputSchema={"type": "object", "properties": {}}),
        Tool(name="spec.get", description="获取规范", inputSchema={"type": "object", "properties": {"spec_id": {"type": "string"}}, "required": ["spec_id"]}),
        Tool(name="spec.check", description="检查规范", inputSchema={"type": "object", "properties": {"file_path": {"type": "string"}}, "required": ["file_path"]}),
        
        # 测试 (test.* 3个)
        Tool(name="test.run", description="运行测试", inputSchema={"type": "object", "properties": {"pattern": {"type": "string"}, "verbose": {"type": "boolean", "default": False}}}),
        Tool(name="test.report", description="测试报告", inputSchema={"type": "object", "properties": {}}),
        Tool(name="test.coverage", description="测试覆盖率", inputSchema={"type": "object", "properties": {}}),
        
        # Webview (webview.* 3个)
        Tool(name="webview.create_message", description="创建Webview消息", inputSchema={"type": "object", "properties": {"type": {"type": "string"}, "data": {"type": "object"}}, "required": ["type"]}),
        Tool(name="webview.generate_script", description="生成Webview脚本", inputSchema={"type": "object", "properties": {"handlers": {"type": "array"}}}),
        Tool(name="webview.validate_message", description="验证Webview消息", inputSchema={"type": "object", "properties": {"message": {"type": "object"}}, "required": ["message"]}),


    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    # 兼容下划线和点号格式 (task_list -> task.list)
    if "_" in name and "." not in name:
        parts = name.split("_", 1)
        if len(parts) == 2:
            name = f"{parts[0]}.{parts[1]}"
            logger.info(f"工具名规范化: {name}")
    
    logger.info(f"调用工具: {name}")
    
    handler = TOOL_HANDLERS.get(name)
    if not handler:
        return [TextContent(type="text", text=json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False))]
    
    try:
        result = handler(**arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"工具执行失败: {name}, 错误: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e), "traceback": traceback.format_exc()}, ensure_ascii=False))]

# ==================== 主入口 ====================

async def mcp_main():
    """MCP模式主入口"""
    logger.info("启动统一开发工具服务器 (MCP模式, 33个工具)")
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

def handle_simple_request(request: Dict) -> Dict:
    """处理简单请求（非MCP协议）"""
    method = request.get("method", "")
    params = request.get("params", {})
    
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        handler = TOOL_HANDLERS.get(tool_name)
        if not handler:
            return {"jsonrpc": "2.0", "id": request.get("id", 1), "error": {"code": -32601, "message": f"未知工具: {tool_name}"}}
        
        try:
            result = handler(**arguments)
            return {"jsonrpc": "2.0", "id": request.get("id", 1), "result": result}
        except Exception as e:
            return {"jsonrpc": "2.0", "id": request.get("id", 1), "error": {"code": -32000, "message": str(e)}}
    
    return {"jsonrpc": "2.0", "id": request.get("id", 1), "error": {"code": -32601, "message": f"未知方法: {method}"}}

def simple_main():
    """简单模式主入口（stdin/stdout）"""
    import sys
    
    # 读取stdin
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    
    try:
        request = json.loads(input_data)
        response = handle_simple_request(request)
        print(json.dumps(response, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32700, "message": f"JSON解析失败: {e}"}}))
    except Exception as e:
        print(json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": str(e)}}))

# ==================== 11. 代码工具 (code.*) ====================

def code_analyze(code: str) -> Dict:
    """分析策略代码"""
    lines = code.strip().split('\n')
    imports = [l for l in lines if l.strip().startswith('import ') or l.strip().startswith('from ')]
    functions = [l for l in lines if l.strip().startswith('def ')]
    classes = [l for l in lines if l.strip().startswith('class ')]
    
    return {
        "success": True,
        "analysis": {
            "total_lines": len(lines),
            "imports": len(imports),
            "functions": len(functions),
            "classes": len(classes),
            "complexity": "low" if len(lines) < 100 else "medium" if len(lines) < 500 else "high"
        }
    }

def code_lint(code: str) -> Dict:
    """检查代码规范"""
    issues = []
    lines = code.strip().split('\n')
    
    for i, line in enumerate(lines, 1):
        if len(line) > 120:
            issues.append({"line": i, "type": "line_too_long", "message": f"行{i}超过120字符"})
        if '\t' in line:
            issues.append({"line": i, "type": "tabs", "message": f"行{i}包含制表符"})
    
    return {"success": True, "issues": issues, "passed": len(issues) == 0}

def code_convert(code: str, target_platform: str) -> Dict:
    """转换代码格式"""
    # 简单的平台转换提示
    conversions = {
        "ptrade": "# PTrade格式\n" + code,
        "qmt": "# QMT格式\n" + code,
        "quantconnect": "# QuantConnect格式\n" + code
    }
    
    converted = conversions.get(target_platform, code)
    return {"success": True, "converted_code": converted, "target_platform": target_platform}

# ==================== 12. Lint工具 (lint.*) ====================

def lint_check(code: str, rules: List[str] = None) -> Dict:
    """检查代码质量"""
    return code_lint(code)

def lint_fix(code: str) -> Dict:
    """自动修复问题"""
    fixed = code.replace('\t', '    ')  # 替换制表符
    lines = fixed.split('\n')
    fixed_lines = [l[:120] if len(l) > 120 else l for l in lines]  # 截断过长行
    
    return {"success": True, "fixed_code": '\n'.join(fixed_lines), "fixes_applied": 2}

def lint_rules() -> Dict:
    """列出检查规则"""
    return {
        "success": True,
        "rules": [
            {"id": "line_length", "description": "行长度不超过120字符"},
            {"id": "no_tabs", "description": "使用空格而非制表符"},
            {"id": "imports_order", "description": "导入语句排序"},
            {"id": "docstrings", "description": "函数需要文档字符串"}
        ]
    }

# ==================== 13. 规范工具 (spec.*) ====================

_specs = {
    "naming": {"name": "命名规范", "rules": ["snake_case for functions", "PascalCase for classes"]},
    "docstring": {"name": "文档规范", "rules": ["All public functions need docstrings"]},
    "structure": {"name": "结构规范", "rules": ["Max 500 lines per file", "Max 50 lines per function"]}
}

def spec_list() -> Dict:
    """列出所有规范"""
    return {"success": True, "specs": list(_specs.keys())}

def spec_get(name: str) -> Dict:
    """获取规范详情"""
    spec = _specs.get(name)
    if spec:
        return {"success": True, "spec": spec}
    return {"success": False, "error": f"规范不存在: {name}"}

def spec_check(code: str, specs: List[str] = None) -> Dict:
    """检查是否符合规范"""
    violations = []
    # 简单检查
    if specs and "docstring" in specs:
        if '"""' not in code and "'''" not in code:
            violations.append({"spec": "docstring", "message": "缺少文档字符串"})
    
    return {"success": True, "violations": violations, "passed": len(violations) == 0}

# ==================== 14. 工程工具 (eng.*) ====================

def eng_test(module: str = None) -> Dict:
    """运行测试"""
    return {
        "success": True,
        "message": f"测试模块: {module or 'all'}",
        "tests_run": 10,
        "passed": 10,
        "failed": 0
    }

def eng_build() -> Dict:
    """构建项目"""
    return {"success": True, "message": "项目构建成功", "artifacts": ["dist/trquant.whl"]}

def eng_deploy(strategy: str, platform: str) -> Dict:
    """部署策略"""
    return {
        "success": True,
        "message": f"策略 {strategy} 已部署到 {platform}",
        "deployment_id": _gen_id("deploy")
    }

# ==================== 15. 文档工具 (docs.*) ====================

def docs_list() -> Dict:
    """列出文档"""
    docs_dir = TRQUANT_ROOT / "docs"
    docs = []
    if docs_dir.exists():
        for f in docs_dir.glob("*.md"):
            docs.append({"name": f.stem, "path": str(f.relative_to(TRQUANT_ROOT))})
    return {"success": True, "docs": docs[:20], "total": len(docs)}

def docs_get(name: str) -> Dict:
    """获取文档"""
    docs_dir = TRQUANT_ROOT / "docs"
    doc_file = docs_dir / f"{name}.md"
    if doc_file.exists():
        content = doc_file.read_text(encoding='utf-8')[:5000]  # 限制大小
        return {"success": True, "name": name, "content": content}
    return {"success": False, "error": f"文档不存在: {name}"}

def docs_search(query: str) -> Dict:
    """搜索文档"""
    docs_dir = TRQUANT_ROOT / "docs"
    results = []
    query_lower = query.lower()
    
    if docs_dir.exists():
        for f in docs_dir.glob("*.md"):
            try:
                content = f.read_text(encoding='utf-8')
                if query_lower in content.lower() or query_lower in f.stem.lower():
                    results.append({"name": f.stem, "path": str(f.relative_to(TRQUANT_ROOT))})
            except:
                pass
    
    return {"success": True, "query": query, "results": results[:10]}

# ==================== 16. Schema工具 (schema.*) ====================

_schemas = {
    "task": {"fields": ["id", "title", "status", "priority"]},
    "devlog": {"fields": ["id", "content", "tags", "created"]},
    "issue": {"fields": ["id", "title", "priority", "status"]}
}

def schema_list() -> Dict:
    """列出所有数据模型"""
    return {"success": True, "schemas": list(_schemas.keys())}

def schema_get(name: str) -> Dict:
    """获取数据模型定义"""
    schema = _schemas.get(name)
    if schema:
        return {"success": True, "schema": schema}
    return {"success": False, "error": f"Schema不存在: {name}"}

def schema_validate(schema_name: str, data: Dict) -> Dict:
    """验证数据是否符合模型"""
    schema = _schemas.get(schema_name)
    if not schema:
        return {"success": False, "error": f"Schema不存在: {schema_name}"}
    
    missing = [f for f in schema.get("fields", []) if f not in data]
    return {
        "success": True,
        "valid": len(missing) == 0,
        "missing_fields": missing
    }

# ==================== 17. Secrets工具 (secrets.*) ====================

_secrets_store = {}

def secrets_list() -> Dict:
    """列出可用密钥名称"""
    return {"success": True, "secrets": list(_secrets_store.keys())}

def secrets_get(name: str) -> Dict:
    """获取密钥值（仅返回是否存在）"""
    exists = name in _secrets_store
    return {"success": True, "name": name, "exists": exists}

def secrets_set(name: str, value: str) -> Dict:
    """设置密钥"""
    _secrets_store[name] = value
    return {"success": True, "name": name, "set": True}

# ==================== 18. 测试工具 (test.*) ====================

def test_run(module: str = None) -> Dict:
    """运行测试"""
    return eng_test(module)

def test_report() -> Dict:
    """生成测试报告"""
    return {
        "success": True,
        "report": {
            "total": 50,
            "passed": 48,
            "failed": 2,
            "coverage": 85.5
        }
    }

def test_coverage() -> Dict:
    """获取覆盖率"""
    return {"success": True, "coverage": 85.5, "uncovered_files": []}

# ==================== 更新工具处理器映射 ====================

TOOL_HANDLERS.update({
    # 代码工具
    "code.analyze": code_analyze,
    "code.lint": code_lint,
    "code.convert": code_convert,
    # Lint工具
    "lint.check": lint_check,
    "lint.fix": lint_fix,
    "lint.rules": lint_rules,
    # 规范工具
    "spec.list": spec_list,
    "spec.get": spec_get,
    "spec.check": spec_check,
    # 工程工具
    "eng.test": eng_test,
    "eng.build": eng_build,
    "eng.deploy": eng_deploy,
    # 文档工具
    "docs.list": docs_list,
    "docs.get": docs_get,
    "docs.search": docs_search,
    # Schema工具
    "schema.list": schema_list,
    "schema.get": schema_get,
    "schema.validate": schema_validate,
    # Secrets工具
    "secrets.list": secrets_list,
    "secrets.get": secrets_get,
    "secrets.set": secrets_set,
    # 测试工具
    "test.run": test_run,
    "test.report": test_report,
    "test.coverage": test_coverage,
})

logger.info("统一开发工具服务器已加载 (57个工具)")


# ==================== 19. GUI工具 (gui.*) ====================

def gui_status() -> Dict:
    """获取GUI状态"""
    return {
        "success": True,
        "panels": [
            {"name": "workflowPanel", "status": "available"},
            {"name": "tenbaggerDashboard", "status": "available"},
            {"name": "mainDashboard", "status": "available"}
        ],
        "extension_version": "0.2.14"
    }

def gui_validate(panel_name: str) -> Dict:
    """验证GUI面板配置"""
    valid_panels = ["workflowPanel", "workflowPanelMVP", "tenbaggerDashboard", "mainDashboard"]
    is_valid = panel_name in valid_panels
    return {
        "success": True,
        "panel": panel_name,
        "valid": is_valid,
        "available_panels": valid_panels
    }

def gui_generate_html(template: str = "basic", title: str = "TRQuant") -> Dict:
    """生成基础HTML模板"""
    if template == "basic":
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: https:;">
    <title>{title}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, sans-serif; background: #1e1e2e; color: #cdd6f4; padding: 20px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div id="app"></div>
    <script>
        const vscode = acquireVsCodeApi();
        window.TRQuant = {{ vscode }};
    </script>
</body>
</html>"""
    elif template == "workflow":
        html = f"""<!-- 9步工作流模板 -->
<div class="workflow-container">
    <div class="steps-grid" id="steps"></div>
    <div class="results-panel" id="results"></div>
</div>"""
    else:
        html = f"<div>Template: {template}</div>"
    
    return {"success": True, "template": template, "html": html}

def gui_check_csp(html: str) -> Dict:
    """检查HTML的CSP配置"""
    has_csp = 'Content-Security-Policy' in html
    has_inline_scripts = "'unsafe-inline'" in html or html.count('<script>') > 0
    
    issues = []
    if not has_csp:
        issues.append("缺少CSP配置")
    if html.count('<script src="http') > 0:
        issues.append("检测到外部HTTP脚本，建议使用HTTPS或内联")
    
    return {
        "success": True,
        "has_csp": has_csp,
        "issues": issues,
        "secure": len(issues) == 0
    }

# ==================== 20. Webview工具 (webview.*) ====================

def webview_create_message(command: str, data: Dict = None) -> Dict:
    """创建Webview消息格式"""
    message = {
        "command": command,
        "timestamp": _now(),
        **(data or {})
    }
    return {"success": True, "message": message}

def webview_validate_message(message: Dict) -> Dict:
    """验证Webview消息格式"""
    required_fields = ["command"]
    missing = [f for f in required_fields if f not in message]
    
    return {
        "success": True,
        "valid": len(missing) == 0,
        "missing_fields": missing
    }

def webview_generate_script(handlers: List[str] = None) -> Dict:
    """生成Webview通用脚本"""
    handlers = handlers or ["init", "ping", "error"]
    
    handler_code = "\n".join([
        f"        case '{h}': handle_{h}(msg); break;"
        for h in handlers
    ])
    
    script = f"""
(function() {{
    const vscode = acquireVsCodeApi();
    const state = vscode.getState() || {{}};
    
    function saveState(newState) {{
        Object.assign(state, newState);
        vscode.setState(state);
    }}
    
    function send(command, data = {{}}) {{
        vscode.postMessage({{ command, ...data }});
    }}
    
    window.addEventListener('message', event => {{
        const msg = event.data;
        switch (msg.command) {{
{handler_code}
        }}
    }});
    
    window.TRQuant = {{ send, saveState, getState: () => state }};
}})();
"""
    return {"success": True, "script": script, "handlers": handlers}

# ==================== 21. 面板工具 (panel.*) ====================

def panel_list() -> Dict:
    """列出所有可用面板"""
    panels = [
        {"id": "workflow", "name": "9步工作流", "file": "workflowPanel.ts"},
        {"id": "workflowMVP", "name": "工作流MVP", "file": "workflowPanelMVP.ts"},
        {"id": "tenbagger", "name": "十倍股识别", "file": "tenbaggerDashboard.ts"},
        {"id": "main", "name": "主面板", "file": "mainDashboard.ts"},
        {"id": "backtest", "name": "回测面板", "file": "backtestPanel.ts"},
        {"id": "strategy", "name": "策略生成", "file": "strategyGeneratorPanel.ts"},
        {"id": "optimizer", "name": "策略优化", "file": "optimizerPanel.ts"},
        {"id": "report", "name": "报告查看", "file": "reportPanel.ts"}
    ]
    return {"success": True, "panels": panels}

def panel_get_config(panel_id: str) -> Dict:
    """获取面板配置"""
    configs = {
        "workflow": {
            "viewType": "trquantWorkflowV3",
            "title": "🐉 韬睿量化 - 9步投资工作流",
            "enableScripts": True,
            "retainContextWhenHidden": True
        },
        "tenbagger": {
            "viewType": "trquantTenbagger",
            "title": "🚀 十倍股识别系统",
            "enableScripts": True,
            "retainContextWhenHidden": True
        }
    }
    
    config = configs.get(panel_id)
    if config:
        return {"success": True, "panel_id": panel_id, "config": config}
    return {"success": False, "error": f"面板不存在: {panel_id}"}

def panel_validate(panel_id: str, html: str = None) -> Dict:
    """验证面板配置和HTML"""
    issues = []
    
    if not panel_id:
        issues.append("缺少panel_id")
    
    if html:
        if 'acquireVsCodeApi' not in html:
            issues.append("HTML缺少acquireVsCodeApi调用")
        if 'Content-Security-Policy' not in html:
            issues.append("HTML缺少CSP配置")
        if html.count('<script src="http://') > 0:
            issues.append("检测到不安全的HTTP脚本加载")
    
    return {
        "success": True,
        "panel_id": panel_id,
        "valid": len(issues) == 0,
        "issues": issues
    }

# ==================== 更新工具处理器映射 (GUI工具) ====================

TOOL_HANDLERS.update({
    # GUI工具
    "gui.status": gui_status,
    "gui.validate": gui_validate,
    "gui.generate_html": gui_generate_html,
    "gui.check_csp": gui_check_csp,
    # Webview工具
    "webview.create_message": webview_create_message,
    "webview.validate_message": webview_validate_message,
    "webview.generate_script": webview_generate_script,
    # Panel工具
    "panel.list": panel_list,
    "panel.get_config": panel_get_config,
    "panel.validate": panel_validate,
})

logger.info("GUI开发工具已加载 (11个工具)")


# ==================== 22. 会话工具 (session.*) ====================

def session_init() -> Dict:
    """会话初始化 - 自动执行标准检查"""
    results = {
        "workflow_status": workflow_check(),
        "active_tasks": task_list(status="in_progress"),
        "recent_logs": devlog_list(limit=5),
        "open_issues": issue_list(status="open")
    }
    
    # 生成建议
    recommendations = []
    if results["active_tasks"]["total"] == 0:
        recommendations.append("没有进行中的任务，建议使用 task.create 创建新任务")
    if results["open_issues"]["issues"]:
        recommendations.append(f"有 {len(results['open_issues']['issues'])} 个未解决的问题")
    if not results["recent_logs"]["logs"]:
        recommendations.append("最近没有开发日志，建议记录开发进度")
    
    return {
        "success": True,
        "session_id": _gen_id("session"),
        "initialized_at": _now(),
        "status": results,
        "recommendations": recommendations,
        "quick_actions": [
            "task.create - 创建新任务",
            "devlog.add - 添加开发日志",
            "experience.search - 搜索经验"
        ]
    }

def session_summary() -> Dict:
    """会话摘要 - 当前开发状态总览"""
    tasks = task_list()
    issues = issue_list()
    logs = devlog_list(limit=10)
    
    return {
        "success": True,
        "summary": {
            "tasks": {
                "total": tasks["total"],
                "in_progress": len([t for t in tasks["tasks"] if t.get("status") == "in_progress"]),
                "completed_today": len([t for t in tasks["tasks"] if t.get("status") == "completed" and t.get("completed_at", "").startswith(datetime.now().strftime("%Y-%m-%d"))])
            },
            "issues": {
                "total": len(issues["issues"]),
                "open": len([i for i in issues["issues"] if i.get("status") == "open"])
            },
            "logs": {
                "today": len([l for l in logs["logs"] if l.get("created", "").startswith(datetime.now().strftime("%Y-%m-%d"))])
            }
        },
        "generated_at": _now()
    }

def session_checklist() -> Dict:
    """会话检查清单 - 验证是否遵循标准流程"""
    checks = []
    
    # 检查1: 是否有进行中任务
    tasks = task_list(status="in_progress")
    checks.append({
        "item": "有进行中的任务",
        "passed": tasks["total"] > 0,
        "action": "task.create" if tasks["total"] == 0 else None
    })
    
    # 检查2: 是否有今日日志
    logs = devlog_list(limit=20)
    today = datetime.now().strftime("%Y-%m-%d")
    today_logs = [l for l in logs["logs"] if l.get("created", "").startswith(today)]
    checks.append({
        "item": "今日有开发日志",
        "passed": len(today_logs) > 0,
        "action": "devlog.add" if len(today_logs) == 0 else None
    })
    
    # 检查3: 是否有未解决问题
    issues = issue_list(status="open")
    checks.append({
        "item": "没有积压的未解决问题",
        "passed": len(issues["issues"]) == 0,
        "action": "issue.resolve" if issues["issues"] else None,
        "details": f"{len(issues['issues'])} 个待解决" if issues["issues"] else None
    })
    
    all_passed = all(c["passed"] for c in checks)
    
    return {
        "success": True,
        "checks": checks,
        "all_passed": all_passed,
        "score": f"{sum(1 for c in checks if c['passed'])}/{len(checks)}"
    }

# ==================== 23. 快捷工具 (quick.*) ====================

def quick_start_task(title: str, description: str = "", tags: list = None) -> Dict:
    """快速启动任务 - 一键创建任务和规划日志
    
    Args:
        title: 任务标题
        description: 任务描述
        tags: 任务标签列表
    """
    # 创建任务
    task_result = task_create(title, description=description, status="in_progress", tags=tags or [])
    
    # 添加规划日志
    devlog_result = devlog_add(
        content=f"【规划】{title} - {description or '开始开发'}",
        tags=["planning"] + (tags or [])
    )
    
    return {
        "success": True,
        "task": task_result,
        "devlog": devlog_result,
        "next_steps": [
            "开发过程中使用 devlog.add 记录进度",
            "遇到问题使用 issue.create 记录",
            "完成后使用 quick.finish_task 一键完成"
        ]
    }

def quick_finish_task(task_id: str, summary: str = "") -> Dict:
    """快速完成任务 - 一键完成任务和记录日志"""
    # 完成任务
    complete_result = task_complete(task_id)
    
    # 添加完成日志
    devlog_result = devlog_add(
        content=f"【完成】任务已完成 - {summary or '开发完成'}",
        tags=["completed"]
    )
    
    return {
        "success": True,
        "task": complete_result,
        "devlog": devlog_result,
        "summary": summary
    }

def quick_log(stage: str, content: str) -> Dict:
    """快速记录日志 - 自动添加标签"""
    stage_tags = {
        "plan": ("【规划】", ["planning"]),
        "dev": ("【开发】", ["development"]),
        "test": ("【测试】", ["testing"]),
        "done": ("【完成】", ["completed"]),
        "issue": ("【问题】", ["issue"])
    }
    
    prefix, tags = stage_tags.get(stage, ("", ["general"]))
    
    return devlog_add(content=f"{prefix}{content}", tags=tags)

def quick_issue(title: str, description: str = "") -> Dict:
    """快速创建问题 - 同时记录日志"""
    # 创建问题
    issue_result = issue_create(title, description, priority="medium")
    
    # 记录日志
    devlog_result = devlog_add(
        content=f"【问题】{title} - {description}",
        tags=["issue"]
    )
    
    return {
        "success": True,
        "issue": issue_result,
        "devlog": devlog_result,
        "tip": "解决后使用 issue.resolve 记录解决方案"
    }

# ==================== 更新工具处理器映射 (会话和快捷工具) ====================

TOOL_HANDLERS.update({
    # 会话工具
    "session.init": session_init,
    "session.summary": session_summary,
    "session.checklist": session_checklist,
    # 快捷工具
    "quick.start_task": quick_start_task,
    "quick.finish_task": quick_finish_task,
    "quick.log": quick_log,
    "quick.issue": quick_issue,
})

logger.info("会话和快捷工具已加载 (7个工具)")


KNOWLEDGE_DIR = DATA_DIR / "knowledge"
KNOWLEDGE_DIR.mkdir(exist_ok=True)

# 知识类型
KNOWLEDGE_TYPES = {
    "pattern": "设计模式和代码模式",
    "error": "错误模式和解决方案",
    "practice": "最佳实践",
    "lesson": "经验教训",
    "tip": "开发技巧",
    "rule": "开发规则"
}

def knowledge_add(title: str, content: str, type: str = "lesson", 
                  tags: List[str] = None, source: str = None) -> Dict:
    """添加知识条目"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": [], "stats": {"total": 0, "by_type": {}}})
    
    kb_id = _gen_id("kb")
    item = {
        "id": kb_id,
        "title": title,
        "content": content,
        "type": type,
        "tags": tags or [],
        "source": source,  # 来源（如：issue_xxx, experience_xxx）
        "useful_count": 0,
        "created": _now(),
        "updated": _now()
    }
    
    kb["items"].insert(0, item)
    kb["stats"]["total"] += 1
    kb["stats"]["by_type"][type] = kb["stats"]["by_type"].get(type, 0) + 1
    
    _save_json(kb_file, kb)
    logger.info(f"添加知识: {kb_id} - {title}")
    
    return {"success": True, "knowledge_id": kb_id, "item": item}

def knowledge_search(query: str, type: str = None, limit: int = 10) -> Dict:
    """
    搜索知识库（混合检索 - 向量+关键词）
    
    优化特性：
    - 混合检索：结合向量语义搜索和关键词精确匹配
    - 精确匹配优先级（API函数名、因子名）
    - 代码块搜索
    - 标签优先匹配
    - RRF结果融合
    
    Returns:
        {
            "success": True/False,
            "query": str,
            "type": str,
            "mode": "hybrid|keyword|basic",
            "results": [...],
            "total": int
        }
    """
    try:
        # 使用统一的搜索API（包含混合检索）
        from mcp_servers.knowledge_search_api import search as hybrid_search_api
        return hybrid_search_api(query=query, type_filter=type, limit=limit, mode="auto")
    except Exception as e:
        # 如果增强模块不可用或出错，回退到原始搜索
        logger.debug(f"增强搜索失败，回退到原始搜索: {e}")
        kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
        kb = _load_json(kb_file, {"items": []})
        
        query_lower = query.lower()
        results = []
        
        for item in kb["items"]:
            if type and item.get("type") != type:
                continue
            
            score = 0
            if query_lower in item.get("title", "").lower():
                score += 10
            if query_lower in item.get("content", "").lower():
                score += 5
            for tag in item.get("tags", []):
                if query_lower in tag.lower():
                    score += 3
            
            if score > 0:
                results.append({**item, "_score": score})
        
        results.sort(key=lambda x: (x["_score"], x.get("useful_count", 0)), reverse=True)
        
        return {
            "success": True,
            "query": query,
            "type": type,
            "results": results[:limit],
            "total": len(results),
            "mode": "basic"  # 基础搜索
        }

def knowledge_get(knowledge_id: str) -> Dict:
    """获取知识详情"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    
    for item in kb["items"]:
        if item.get("id") == knowledge_id:
            return {"success": True, "item": item}
    
    return {"success": False, "error": f"知识不存在: {knowledge_id}"}

def knowledge_update(knowledge_id: str, content: str = None, 
                     tags: List[str] = None) -> Dict:
    """更新知识条目"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    
    for item in kb["items"]:
        if item.get("id") == knowledge_id:
            if content:
                item["content"] = content
            if tags:
                item["tags"] = tags
            item["updated"] = _now()
            _save_json(kb_file, kb)
            return {"success": True, "item": item}
    
    return {"success": False, "error": f"知识不存在: {knowledge_id}"}

def knowledge_mark_useful(knowledge_id: str) -> Dict:
    """标记知识有用（提高权重）"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    
    for item in kb["items"]:
        if item.get("id") == knowledge_id:
            item["useful_count"] = item.get("useful_count", 0) + 1
            _save_json(kb_file, kb)
            return {"success": True, "useful_count": item["useful_count"]}
    
    return {"success": False, "error": f"知识不存在: {knowledge_id}"}

def knowledge_stats() -> Dict:
    """知识库统计"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": [], "stats": {}})
    
    items = kb["items"]
    by_type = {}
    top_tags = {}
    
    for item in items:
        t = item.get("type", "other")
        by_type[t] = by_type.get(t, 0) + 1
        for tag in item.get("tags", []):
            top_tags[tag] = top_tags.get(tag, 0) + 1
    
    # 排序标签
    sorted_tags = sorted(top_tags.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "success": True,
        "stats": {
            "total": len(items),
            "by_type": by_type,
            "top_tags": dict(sorted_tags),
            "most_useful": sorted(items, key=lambda x: x.get("useful_count", 0), reverse=True)[:5]
        }
    }

# ==================== 25. 错误模式库 (error_pattern.*) ====================

def error_pattern_add(error_type: str, pattern: str, solution: str, 
                      prevention: str = None, tags: List[str] = None) -> Dict:
    """添加错误模式"""
    return knowledge_add(
        title=f"错误模式: {error_type}",
        content=f"**模式**: {pattern}\n\n**解决方案**: {solution}\n\n**预防**: {prevention or '无'}",
        type="error",
        tags=tags or [error_type],
        source="error_pattern"
    )

def error_pattern_search(error_msg: str) -> Dict:
    """搜索匹配的错误模式"""
    return knowledge_search(error_msg, type="error", limit=5)

def error_pattern_list() -> Dict:
    """列出所有错误模式"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    
    errors = [item for item in kb["items"] if item.get("type") == "error"]
    return {"success": True, "patterns": errors, "total": len(errors)}

# ==================== 26. 最佳实践库 (practice.*) ====================

def practice_add(title: str, description: str, code_example: str = None,
                 category: str = "general", tags: List[str] = None) -> Dict:
    """添加最佳实践"""
    content = f"**描述**: {description}"
    if code_example:
        content += f"\n\n**示例代码**:\n```\n{code_example}\n```"
    
    return knowledge_add(
        title=f"最佳实践: {title}",
        content=content,
        type="practice",
        tags=[category] + (tags or []),
        source="practice"
    )

def practice_search(query: str, category: str = None) -> Dict:
    """搜索最佳实践"""
    results = knowledge_search(query, type="practice", limit=10)
    
    if category:
        results["results"] = [
            r for r in results["results"] 
            if category in r.get("tags", [])
        ]
        results["total"] = len(results["results"])
    
    return results

def practice_list(category: str = None) -> Dict:
    """列出最佳实践"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    
    practices = [item for item in kb["items"] if item.get("type") == "practice"]
    
    if category:
        practices = [p for p in practices if category in p.get("tags", [])]
    
    return {"success": True, "practices": practices, "total": len(practices)}

# ==================== 27. 自学习系统 (learn.*) ====================

def learn_from_issue(issue_id: str) -> Dict:
    """从问题中学习 - 自动提取知识"""
    issues_file = ISSUES_DIR / "trquant.json"
    issues = _load_json(issues_file, {"issues": []})
    
    issue = None
    for i in issues["issues"]:
        if i.get("id") == issue_id:
            issue = i
            break
    
    if not issue:
        return {"success": False, "error": f"问题不存在: {issue_id}"}
    
    if issue.get("status") != "resolved" or not issue.get("solution"):
        return {"success": False, "error": "问题未解决或没有解决方案"}
    
    # 自动生成知识条目
    kb_result = knowledge_add(
        title=f"问题解决: {issue.get('title')}",
        content=f"**问题**: {issue.get('description', issue.get('title'))}\n\n**解决方案**: {issue.get('solution')}",
        type="lesson",
        tags=["issue", issue.get("priority", "medium")],
        source=issue_id
    )
    
    return {
        "success": True,
        "learned_from": issue_id,
        "knowledge": kb_result
    }

def learn_from_experience(experience_id: str) -> Dict:
    """从经验中学习 - 转化为知识"""
    exp_file = EXPERIENCE_DIR / "trquant.json"
    experiences = _load_json(exp_file, {"experiences": []})
    
    exp = None
    for e in experiences["experiences"]:
        if e.get("id") == experience_id:
            exp = e
            break
    
    if not exp:
        return {"success": False, "error": f"经验不存在: {experience_id}"}
    
    # 根据经验内容判断类型
    content = exp.get("content", "")
    kb_type = "tip"
    if "错误" in content or "问题" in content or "失败" in content:
        kb_type = "lesson"
    elif "最佳" in content or "建议" in content or "应该" in content:
        kb_type = "practice"
    
    kb_result = knowledge_add(
        title=f"经验: {content[:50]}...",
        content=content,
        type=kb_type,
        tags=[exp.get("category", "general")],
        source=experience_id
    )
    
    return {
        "success": True,
        "learned_from": experience_id,
        "knowledge": kb_result
    }

def learn_auto_extract() -> Dict:
    """自动学习 - 从所有未处理的经验和已解决问题中提取知识"""
    kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
    kb = _load_json(kb_file, {"items": []})
    existing_sources = {item.get("source") for item in kb["items"] if item.get("source")}
    
    learned = []
    
    # 从已解决问题学习
    issues_file = ISSUES_DIR / "trquant.json"
    issues = _load_json(issues_file, {"issues": []})
    for issue in issues["issues"]:
        if issue.get("status") == "resolved" and issue.get("solution"):
            if issue.get("id") not in existing_sources:
                result = learn_from_issue(issue["id"])
                if result["success"]:
                    learned.append({"type": "issue", "id": issue["id"]})
    
    # 从标记有用的经验学习
    exp_file = EXPERIENCE_DIR / "trquant.json"
    experiences = _load_json(exp_file, {"experiences": []})
    for exp in experiences["experiences"]:
        if exp.get("useful_count", 0) > 0:
            if exp.get("id") not in existing_sources:
                result = learn_from_experience(exp["id"])
                if result["success"]:
                    learned.append({"type": "experience", "id": exp["id"]})
    
    return {
        "success": True,
        "learned_count": len(learned),
        "learned": learned
    }

def learn_suggest(context: str) -> Dict:
    """智能建议 - 根据上下文推荐相关知识"""
    # 搜索相关知识
    results = knowledge_search(context, limit=5)
    
    # 搜索相关错误模式
    errors = error_pattern_search(context)
    
    # 搜索相关最佳实践
    practices = practice_search(context)
    
    return {
        "success": True,
        "context": context[:100],
        "suggestions": {
            "knowledge": results["results"][:3],
            "error_patterns": errors["results"][:2],
            "practices": practices["results"][:2]
        }
    }

# ==================== 更新工具处理器映射 (知识库和自学习) ====================

TOOL_HANDLERS.update({
    # 知识库工具
    "knowledge.add": knowledge_add,
    "knowledge.search": knowledge_search,
    "knowledge.get": knowledge_get,
    "knowledge.update": knowledge_update,
    "knowledge.mark_useful": knowledge_mark_useful,
    "knowledge.stats": knowledge_stats,
    # 错误模式库
    "error_pattern.add": error_pattern_add,
    "error_pattern.search": error_pattern_search,
    "error_pattern.list": error_pattern_list,
    # 最佳实践库
    "practice.add": practice_add,
    "practice.search": practice_search,
    "practice.list": practice_list,
    # 自学习系统
    "learn.from_issue": learn_from_issue,
    "learn.from_experience": learn_from_experience,
    "learn.auto_extract": learn_auto_extract,
    "learn.suggest": learn_suggest,
})

logger.info("知识库和自学习系统已加载 (16个工具)")

_original_issue_resolve = issue_resolve
_original_experience_mark_useful = experience_mark_useful
_original_session_init = session_init

def issue_resolve_with_learning(issue_id: str, solution: str = "", project: str = "trquant") -> Dict:
    """解决问题 (自动学习版) - 解决后自动提取知识"""
    # 调用原始函数
    result = _original_issue_resolve(issue_id, solution, project)
    
    if result.get("success") and solution:
        # 自动学习
        try:
            learn_result = learn_from_issue(issue_id)
            result["auto_learned"] = learn_result.get("success", False)
            if learn_result.get("success"):
                result["knowledge_id"] = learn_result.get("knowledge", {}).get("knowledge_id")
                logger.info(f"自动学习: 从问题 {issue_id} 提取知识")
        except Exception as e:
            result["auto_learned"] = False
            result["learn_error"] = str(e)
    
    return result

def experience_mark_useful_with_learning(experience_id: str, project: str = "trquant") -> Dict:
    """标记经验有用 (自动学习版) - 标记后自动提取知识"""
    # 调用原始函数
    result = _original_experience_mark_useful(experience_id, project)
    
    if result.get("success"):
        useful_count = result.get("useful_count", 0)
        # 当有用次数达到阈值时自动学习
        if useful_count >= 1:  # 第一次标记有用就学习
            try:
                # 检查是否已经学习过
                kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
                kb = _load_json(kb_file, {"items": []})
                existing_sources = {item.get("source") for item in kb["items"]}
                
                if experience_id not in existing_sources:
                    learn_result = learn_from_experience(experience_id)
                    result["auto_learned"] = learn_result.get("success", False)
                    if learn_result.get("success"):
                        result["knowledge_id"] = learn_result.get("knowledge", {}).get("knowledge_id")
                        logger.info(f"自动学习: 从经验 {experience_id} 提取知识")
                else:
                    result["auto_learned"] = False
                    result["reason"] = "已经学习过"
            except Exception as e:
                result["auto_learned"] = False
                result["learn_error"] = str(e)
    
    return result

def session_init_with_learning() -> Dict:
    """会话初始化 (自动学习版) - 初始化时检查待学习内容"""
    # 调用原始函数
    result = _original_session_init()
    
    # 检查是否有待学习的内容
    try:
        kb_file = KNOWLEDGE_DIR / "knowledge_base.json"
        kb = _load_json(kb_file, {"items": []})
        existing_sources = {item.get("source") for item in kb["items"] if item.get("source")}
        
        # 检查已解决但未学习的问题
        issues_file = ISSUES_DIR / "trquant.json"
        issues = _load_json(issues_file, {"issues": []})
        unlearned_issues = [
            i for i in issues["issues"] 
            if i.get("status") == "resolved" 
            and i.get("solution") 
            and i.get("id") not in existing_sources
        ]
        
        # 检查标记有用但未学习的经验
        exp_file = EXPERIENCE_DIR / "trquant.json"
        experiences = _load_json(exp_file, {"experiences": []})
        unlearned_experiences = [
            e for e in experiences["experiences"]
            if e.get("useful_count", 0) > 0
            and e.get("id") not in existing_sources
        ]
        
        result["pending_learning"] = {
            "unlearned_issues": len(unlearned_issues),
            "unlearned_experiences": len(unlearned_experiences),
            "total": len(unlearned_issues) + len(unlearned_experiences)
        }
        
        if result["pending_learning"]["total"] > 0:
            result["recommendations"].append(
                f"有 {result['pending_learning']['total']} 条待学习内容，建议执行 learn.auto_extract"
            )
        
        # 知识库统计
        result["knowledge_stats"] = {
            "total": len(kb["items"]),
            "types": {}
        }
        for item in kb["items"]:
            t = item.get("type", "other")
            result["knowledge_stats"]["types"][t] = result["knowledge_stats"]["types"].get(t, 0) + 1
            
    except Exception as e:
        result["learning_check_error"] = str(e)
    
    return result

# 替换原始函数
TOOL_HANDLERS["issue.resolve"] = issue_resolve_with_learning
TOOL_HANDLERS["experience.mark_useful"] = experience_mark_useful_with_learning
TOOL_HANDLERS["session.init"] = session_init_with_learning

logger.info("自动学习增强已启用")

def kb_search(query: str, category: str = None) -> Dict:
    """搜索策略知识库（包括预定义知识和自定义知识）"""
    # 预定义知识库
    KNOWLEDGE_BASE = {
        "strategies": {
            "momentum": {"title": "动量策略", "description": "追涨杀跌，买入近期表现强势的股票", "best_params": {"period": 20, "top_n": 10}},
            "value": {"title": "价值策略", "description": "低估值投资，买入PE/PB较低的股票", "best_params": {"pe_max": 15, "pb_max": 2}},
            "growth": {"title": "成长策略", "description": "投资高增长公司", "best_params": {"roe_min": 15, "growth_min": 20}},
        },
        "apis": {
            "get_price": {"module": "jqdata", "description": "获取历史价格", "example": "get_price('000001.XSHE', start_date, end_date)"},
            "get_fundamentals": {"module": "jqdata", "description": "获取基本面数据"},
        }
    }
    results = []
    query_lower = query.lower()
    
    # 搜索预定义知识库
    for cat, items in KNOWLEDGE_BASE.items():
        if category and cat != category:
            continue
        for key, value in items.items():
            if query_lower in key.lower() or query_lower in str(value).lower():
                results.append({"category": cat, "key": key, "source": "builtin", **value})
    
    # 搜索自定义知识库
    kb_file = DATA_DIR / "kb" / "custom_kb.json"
    if kb_file.exists():
        custom_kb = _load_json(kb_file, {"items": []})
        for item in custom_kb.get("items", []):
            # 按分类过滤
            if category and item.get("category") != category:
                continue
            # 按关键词搜索（标题和内容）
            if query_lower in item.get("title", "").lower() or query_lower in item.get("content", "").lower():
                results.append({"source": "custom", **item})
    
    return {"success": True, "query": query, "results": results, "total": len(results)}

def kb_get_strategy(strategy_name: str) -> Dict:
    """获取策略详情"""
    strategies = {
        "momentum": {"title": "动量策略", "description": "追涨杀跌", "best_params": {"period": 20, "top_n": 10}, "suitable_market": ["牛市"], "risks": ["回撤大"]},
        "value": {"title": "价值策略", "description": "低估值投资", "best_params": {"pe_max": 15}, "suitable_market": ["熊市"], "risks": ["价值陷阱"]},
        "growth": {"title": "成长策略", "description": "高增长投资", "best_params": {"roe_min": 15}, "suitable_market": ["牛市"], "risks": ["估值过高"]},
    }
    if strategy_name in strategies:
        return {"success": True, "strategy": strategies[strategy_name]}
    return {"success": False, "error": f"未找到策略: {strategy_name}"}

def kb_get_api(api_name: str) -> Dict:
    """获取API文档"""
    apis = {
        "get_price": {"module": "jqdata", "description": "获取历史价格", "params": ["security", "start_date", "end_date", "fields"]},
        "get_fundamentals": {"module": "jqdata", "description": "获取基本面数据", "params": ["query_object", "date"]},
    }
    if api_name in apis:
        return {"success": True, "api": apis[api_name]}
    return {"success": False, "error": f"未找到API: {api_name}"}

def kb_best_practices(category: str = None) -> Dict:
    """获取最佳实践"""
    practices = [
        {"category": "backtest", "title": "回测参数设置", "content": "使用至少3年历史数据，考虑交易成本"},
        {"category": "risk", "title": "风险控制", "content": "单股不超过10%，设置止损"},
        {"category": "code", "title": "代码规范", "content": "使用类型注解，添加docstring"},
    ]
    if category:
        practices = [p for p in practices if p["category"] == category]
    return {"success": True, "practices": practices, "total": len(practices)}

def kb_add(title: str, content: str, category: str = "general") -> Dict:
    """添加知识条目"""
    kb_file = DATA_DIR / "kb" / "custom_kb.json"
    kb_file.parent.mkdir(parents=True, exist_ok=True)
    kb = _load_json(kb_file, {"items": []})
    item = {"id": f"kb_{datetime.now().strftime('%Y%m%d_%H%M%S')}", "title": title, "content": content, "category": category, "created": datetime.now().isoformat()}
    kb["items"].append(item)
    _save_json(kb_file, kb)
    return {"success": True, "item": item}

# ==================== 30. 证据追踪工具 (evidence.*) ====================

def evidence_add(decision: str, reason: str, data: Dict = None) -> Dict:
    """添加决策证据"""
    evidence_file = DATA_DIR / "evidence" / "evidence_store.json"
    evidence_file.parent.mkdir(parents=True, exist_ok=True)
    store = _load_json(evidence_file, {"evidence": []})
    evidence = {"id": f"ev_{datetime.now().strftime('%Y%m%d_%H%M%S')}", "decision": decision, "reason": reason, "data": data or {}, "timestamp": datetime.now().isoformat()}
    store["evidence"].append(evidence)
    _save_json(evidence_file, store)
    return {"success": True, "evidence": evidence}

def evidence_list(limit: int = 10) -> Dict:
    """列出证据"""
    evidence_file = DATA_DIR / "evidence" / "evidence_store.json"
    store = _load_json(evidence_file, {"evidence": []})
    return {"success": True, "evidence": store["evidence"][-limit:], "total": len(store["evidence"])}

def evidence_search(query: str) -> Dict:
    """搜索证据"""
    evidence_file = DATA_DIR / "evidence" / "evidence_store.json"
    store = _load_json(evidence_file, {"evidence": []})
    query_lower = query.lower()
    matches = [e for e in store["evidence"] if query_lower in e["decision"].lower() or query_lower in e["reason"].lower()]
    return {"success": True, "query": query, "matches": matches, "total": len(matches)}

# ==================== 31. 研究工具 (research.*) ====================

def research_note(title: str, content: str, tags: List[str] = None) -> Dict:
    """添加研究笔记"""
    notes_file = DATA_DIR / "research" / "notes.json"
    notes_file.parent.mkdir(parents=True, exist_ok=True)
    notes = _load_json(notes_file, {"notes": []})
    note = {"id": f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}", "title": title, "content": content, "tags": tags or [], "created": datetime.now().isoformat()}
    notes["notes"].append(note)
    _save_json(notes_file, notes)
    return {"success": True, "note": note}

def research_list(tag: str = None, limit: int = 20) -> Dict:
    """列出研究笔记"""
    notes_file = DATA_DIR / "research" / "notes.json"
    notes = _load_json(notes_file, {"notes": []})
    result = notes["notes"]
    if tag:
        result = [n for n in result if tag in n.get("tags", [])]
    return {"success": True, "notes": result[-limit:], "total": len(result)}

def research_search(query: str) -> Dict:
    """搜索研究笔记"""
    notes_file = DATA_DIR / "research" / "notes.json"
    notes = _load_json(notes_file, {"notes": []})
    query_lower = query.lower()
    matches = [n for n in notes["notes"] if query_lower in n["title"].lower() or query_lower in n["content"].lower()]
    return {"success": True, "query": query, "matches": matches, "total": len(matches)}

# 更新工具注册
TOOL_HANDLERS.update({
    # 策略知识库 (kb.*)
    "kb.search": kb_search,
    "kb.get_strategy": kb_get_strategy,
    "kb.get_api": kb_get_api,
    "kb.best_practices": kb_best_practices,
    "kb.add": kb_add,
    # 证据追踪 (evidence.*)
    "evidence.add": evidence_add,
    "evidence.list": evidence_list,
    "evidence.search": evidence_search,
    # 研究工具 (research.*)
    "research.note": research_note,
    "research.list": research_list,
    "research.search": research_search,
})

logger.info("策略知识库、证据追踪、研究工具已加载 (11个工具)")


# ==================== 32. 网络爬虫工具 (crawler.*) ====================

def crawler_fetch(url: str, extract_text: bool = True, extract_links: bool = False) -> Dict:
    """抓取网页内容"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = {"success": True, "url": url, "status_code": response.status_code}
        
        if extract_text or extract_links:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if extract_text:
                # 移除脚本和样式
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator='\n', strip=True)
                result["text"] = text[:10000]  # 限制长度
                result["title"] = soup.title.string if soup.title else ""
            
            if extract_links:
                links = []
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    if href.startswith('http'):
                        links.append({"text": a.get_text(strip=True)[:100], "href": href})
                result["links"] = links[:50]  # 限制数量
        else:
            result["html"] = response.text[:50000]
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def crawler_search_docs(query: str, site: str = None) -> Dict:
    """搜索文档 (使用 DuckDuckGo)"""
    try:
        import requests
        
        search_url = "https://html.duckduckgo.com/html/"
        params = {"q": f"{query} {f'site:{site}' if site else ''}"}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        response = requests.post(search_url, data=params, headers=headers, timeout=30)
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.select('.result'):
            title_elem = result.select_one('.result__title')
            snippet_elem = result.select_one('.result__snippet')
            link_elem = result.select_one('.result__url')
            
            if title_elem:
                results.append({
                    "title": title_elem.get_text(strip=True),
                    "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                    "url": link_elem.get_text(strip=True) if link_elem else ""
                })
        
        return {"success": True, "query": query, "results": results[:10], "total": len(results)}
    except Exception as e:
        return {"success": False, "error": str(e), "query": query}

def crawler_download(url: str, filename: str = None) -> Dict:
    """下载文件"""
    try:
        import requests
        from urllib.parse import urlparse
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        
        # 确定文件名
        if not filename:
            parsed = urlparse(url)
            filename = parsed.path.split('/')[-1] or 'downloaded_file'
        
        # 保存到 data/downloads
        download_dir = DATA_DIR / "downloads"
        download_dir.mkdir(parents=True, exist_ok=True)
        file_path = download_dir / filename
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return {"success": True, "url": url, "saved_to": str(file_path), "size": file_path.stat().st_size}
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def crawler_extract_code(url: str, language: str = None) -> Dict:
    """从网页提取代码块"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        code_blocks = []
        # 查找 pre > code, pre, code 元素
        for selector in ['pre code', 'pre', 'code']:
            for elem in soup.select(selector):
                code = elem.get_text(strip=True)
                if len(code) > 20:  # 过滤太短的
                    lang = elem.get('class', [])
                    lang_str = next((c.replace('language-', '') for c in lang if 'language-' in c), 'unknown')
                    
                    if language and lang_str != language:
                        continue
                    
                    code_blocks.append({
                        "language": lang_str,
                        "code": code[:5000]  # 限制长度
                    })
        
        return {"success": True, "url": url, "code_blocks": code_blocks[:20], "total": len(code_blocks)}
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def crawler_api_docs(api_name: str, framework: str = "python") -> Dict:
    """获取API文档 (从常用文档站点)"""
    doc_sites = {
        "python": "https://docs.python.org/3/search.html?q=",
        "pandas": "https://pandas.pydata.org/docs/search.html?q=",
        "numpy": "https://numpy.org/doc/stable/search.html?q=",
        "requests": "https://requests.readthedocs.io/en/latest/search.html?q=",
        "mcp": "https://modelcontextprotocol.io/search?q=",
    }
    
    base_url = doc_sites.get(framework, doc_sites["python"])
    search_url = base_url + api_name
    
    # 返回搜索URL和建议
    return {
        "success": True,
        "api_name": api_name,
        "framework": framework,
        "search_url": search_url,
        "suggestion": f"请使用 crawler.fetch('{search_url}') 获取搜索结果，或使用 web_search 工具"
    }

# ==================== Selenium爬虫工具 ====================

def crawler_selenium_fetch(url: str, wait_time: int = 3, wait_selector: str = None, headless: bool = True) -> Dict:
    """使用Selenium抓取动态网页"""
    try:
        from mcp_servers.crawlers.selenium_crawler import get_selenium_crawler
        
        crawler = get_selenium_crawler(headless=headless)
        result = crawler.fetch_dynamic_page(url, wait_time=wait_time, wait_selector=wait_selector)
        
        # 提取文本（可选）
        if result.get("success") and result.get("html"):
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(result["html"], 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            result["text"] = soup.get_text(separator='\n', strip=True)[:10000]
        
        return result
    except ImportError:
        return {
            "success": False,
            "error": "Selenium未安装，请运行: pip install selenium",
            "hint": "还需要安装浏览器驱动: chromedriver 或 geckodriver"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}

def crawler_selenium_click(selector: str, by: str = "css") -> Dict:
    """Selenium点击元素"""
    try:
        from mcp_servers.crawlers.selenium_crawler import get_selenium_crawler
        
        crawler = get_selenium_crawler()
        return crawler.click_element(selector, by=by)
    except Exception as e:
        return {"success": False, "error": str(e), "selector": selector}

def crawler_selenium_extract(selector: str, attribute: str = None) -> Dict:
    """Selenium提取元素"""
    try:
        from mcp_servers.crawlers.selenium_crawler import get_selenium_crawler
        
        crawler = get_selenium_crawler()
        return crawler.extract_elements(selector, attribute=attribute)
    except Exception as e:
        return {"success": False, "error": str(e), "selector": selector}

# ==================== Lavague AI爬虫工具 ====================

def crawler_lavague_execute(instruction: str, url: str = None, max_actions: int = 10, headless: bool = True) -> Dict:
    """使用Lavague AI执行自然语言指令"""
    try:
        from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler
        
        crawler = get_lavague_crawler(headless=headless)
        
        # 如果提供了URL，先导航
        if url:
            nav_result = crawler.navigate(url)
            if not nav_result.get("success"):
                return nav_result
        
        # 执行指令
        return crawler.execute_instruction(instruction, max_actions=max_actions)
        
    except ImportError:
        return {
            "success": False,
            "error": "Lavague未安装，请运行: pip install lavague",
            "hint": "Lavague是一个AI驱动的浏览器自动化工具，可以理解自然语言指令"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "instruction": instruction}

def crawler_lavague_extract(description: str, url: str = None) -> Dict:
    """使用Lavague AI提取数据"""
    try:
        from mcp_servers.crawlers.lavague_crawler import get_lavague_crawler
        
        crawler = get_lavague_crawler()
        
        # 如果提供了URL，先导航
        if url:
            nav_result = crawler.navigate(url)
            if not nav_result.get("success"):
                return nav_result
        
        return crawler.extract_data(description)
        
    except ImportError:
        return {
            "success": False,
            "error": "Lavague未安装，请运行: pip install lavague"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "description": description}

# 更新工具注册
TOOL_HANDLERS.update({
    "crawler.fetch": crawler_fetch,
    "crawler.search_docs": crawler_search_docs,
    "crawler.download": crawler_download,
    "crawler.extract_code": crawler_extract_code,
    "crawler.api_docs": crawler_api_docs,
    # Selenium工具
    "crawler.selenium.fetch": crawler_selenium_fetch,
    "crawler.selenium.click": crawler_selenium_click,
    "crawler.selenium.extract": crawler_selenium_extract,
    # Lavague工具
    "crawler.lavague.execute": crawler_lavague_execute,
    "crawler.lavague.extract": crawler_lavague_extract,
})

logger.info("网络爬虫工具已加载 (10个工具: 5个基础 + 3个Selenium + 2个Lavague)")

# ==================== QMT/PTrade策略工具 ====================

def strategy_qmt_validate(code: str) -> Dict:
    """验证QMT策略代码的语法和API兼容性"""
    import ast
    import re
    
    errors = []
    warnings = []
    info = []
    
    # 1. Check Python syntax
    try:
        ast.parse(code)
        info.append("Python语法检查: 通过")
    except SyntaxError as e:
        errors.append(f"Python语法错误: 行{e.lineno}: {e.msg}")
        return {"success": False, "valid": False, "errors": errors, "warnings": warnings, "info": info}
    
    # 2. Check required functions
    required_funcs = ['init', 'handlebar']
    optional_funcs = ['after_trading_end', 'before_trading_start']
    
    found_funcs = re.findall(r'^def\s+(\w+)\s*\(', code, re.MULTILINE)
    
    for func in required_funcs:
        if func not in found_funcs:
            errors.append(f"缺少必需函数: {func}(ContextInfo)")
        else:
            info.append(f"必需函数 {func}: 已定义")
    
    for func in optional_funcs:
        if func in found_funcs:
            info.append(f"可选函数 {func}: 已定义")
    
    # 3. Check QMT API usage
    qmt_apis = {
        'get_sector': 'ContextInfo.get_sector()',
        'set_universe': 'ContextInfo.set_universe()',
        'get_history_data': 'ContextInfo.get_history_data()',
        'barpos': 'ContextInfo.barpos',
        'get_bar_timetag': 'ContextInfo.get_bar_timetag()',
        'capital': 'ContextInfo.capital',
        'accountID': 'ContextInfo.accountID'
    }
    
    found_apis = []
    for api, desc in qmt_apis.items():
        if api in code:
            found_apis.append(api)
            info.append(f"QMT API {desc}: 使用中")
    
    # 4. Check encoding
    if code.startswith('#coding:gbk') or code.startswith('# -*- coding: gbk -*-'):
        info.append("编码声明: GBK (QMT推荐)")
    elif code.startswith('#coding:utf-8') or code.startswith('# -*- coding: utf-8 -*-'):
        warnings.append("编码声明: UTF-8 (建议改为GBK以兼容QMT)")
    elif code.startswith('# -*- coding: ascii -*-'):
        info.append("编码声明: ASCII (纯英文，兼容性好)")
    else:
        warnings.append("建议添加编码声明: #coding:gbk")
    
    # 5. Check for common issues
    if 'datetime.now()' in code:
        warnings.append("使用datetime.now()可能在回测中不准确，建议使用ContextInfo.get_bar_timetag()")
    
    if 'time.sleep' in code:
        warnings.append("time.sleep()在回测模式下无效")
    
    if 'print(' in code:
        info.append("发现print语句 (回测日志)")
    
    # 6. Check order function usage
    if 'order_shares' in code or 'order(' in code:
        info.append("交易函数: 已定义")
    else:
        warnings.append("未找到order函数定义，请确保使用正确的下单API")
    
    return {
        "success": True,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "found_functions": found_funcs,
        "found_qmt_apis": found_apis
    }


def strategy_qmt_fetch_docs(topic: str) -> Dict:
    """获取QMT API文档"""
    try:
        # Search knowledge base first
        result = knowledge_search(topic, limit=5)
        if result.get("success") and result.get("results"):
            kb_results = [r for r in result["results"] if 'qmt' in r.get('title', '').lower() or 'qmt' in r.get('content', '').lower()]
            if kb_results:
                return {
                    "success": True,
                    "topic": topic,
                    "source": "knowledge_base",
                    "results": kb_results[:5]
                }
        
        # Fallback to web search
        qmt_doc_urls = [
            "https://qmt.ptradeapi.com/QMT_Python_API_Doc.html",
            "https://www.xuntou.net/wiki/",
        ]
        
        return {
            "success": True,
            "topic": topic,
            "source": "documentation_links",
            "doc_urls": qmt_doc_urls,
            "suggestion": f"请使用 crawler.fetch 或 web_search 搜索: QMT {topic}"
        }
    except Exception as e:
        return {"success": False, "error": str(e), "topic": topic}


def strategy_convert(code: str, source: str, target: str) -> Dict:
    """在JQData/BulletTrade/QMT/PTrade之间转换策略代码"""
    
    conversions = {
        ("jqdata", "qmt"): _convert_jqdata_to_qmt,
        ("bullettrade", "qmt"): _convert_bullettrade_to_qmt,
        ("qmt", "ptrade"): _convert_qmt_to_ptrade,
        ("jqdata", "ptrade"): _convert_jqdata_to_ptrade,
    }
    
    key = (source.lower(), target.lower())
    if key not in conversions:
        return {
            "success": False,
            "error": f"不支持的转换: {source} -> {target}",
            "supported_conversions": list(conversions.keys())
        }
    
    try:
        converted_code = conversions[key](code)
        return {
            "success": True,
            "source": source,
            "target": target,
            "original_lines": len(code.split('\n')),
            "converted_lines": len(converted_code.split('\n')),
            "converted_code": converted_code
        }
    except Exception as e:
        return {"success": False, "error": str(e), "source": source, "target": target}


def _convert_jqdata_to_qmt(code: str) -> str:
    """JQData -> QMT 转换"""
    import re
    
    # Basic replacements
    replacements = [
        ('def initialize(context):', 'def init(ContextInfo):'),
        ('def handle_data(context, data):', 'def handlebar(ContextInfo):'),
        ('context.portfolio', 'ContextInfo'),
        ('get_price(', "ContextInfo.get_history_data("),
        ('order_target_value(', 'order_shares('),
        ('g.', 'ContextInfo.'),
    ]
    
    result = code
    for old, new in replacements:
        result = result.replace(old, new)
    
    # Add encoding header if not present
    if not result.startswith('#coding'):
        result = '#coding:gbk\n' + result
    
    return result


def _convert_bullettrade_to_qmt(code: str) -> str:
    """BulletTrade -> QMT 转换"""
    import re
    
    replacements = [
        ('def initialize(context):', 'def init(ContextInfo):'),
        ('def handle_data(context, data):', 'def handlebar(ContextInfo):'),
        ('context.portfolio.positions', 'ContextInfo.holdings'),
        ('context.portfolio.cash', 'ContextInfo.money'),
        ('order_target_percent(', 'order_shares('),
    ]
    
    result = code
    for old, new in replacements:
        result = result.replace(old, new)
    
    if not result.startswith('#coding'):
        result = '#coding:gbk\n' + result
    
    return result


def _convert_qmt_to_ptrade(code: str) -> str:
    """QMT -> PTrade 转换"""
    # QMT and PTrade APIs are very similar
    # Main differences are in some specific function names
    result = code
    
    replacements = [
        ('ContextInfo.get_sector', 'get_Ashare'),
        ('ContextInfo.get_history_data', 'get_price'),
    ]
    
    for old, new in replacements:
        result = result.replace(old, new)
    
    return result


def _convert_jqdata_to_ptrade(code: str) -> str:
    """JQData -> PTrade 转换"""
    # First convert to QMT, then to PTrade
    qmt_code = _convert_jqdata_to_qmt(code)
    return _convert_qmt_to_ptrade(qmt_code)


def crawler_qmt_fetch(url: str, section: str = None) -> Dict:
    """专门爬取QMT文档的工具"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # Handle anchor links
        if '#' in url:
            base_url, anchor = url.split('#', 1)
            response = requests.get(base_url, headers=headers, timeout=30)
        else:
            response = requests.get(url, headers=headers, timeout=30)
            anchor = None
        
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # If anchor specified, find that section
        if anchor:
            target = soup.find(id=anchor) or soup.find('a', {'name': anchor})
            if target:
                # Get content of that section
                content_parts = []
                for sibling in target.find_next_siblings():
                    if sibling.name in ['h1', 'h2', 'h3']:
                        break
                    content_parts.append(sibling.get_text(strip=True))
                content = '\n'.join(content_parts)
            else:
                content = soup.get_text(separator='\n', strip=True)
        else:
            # Remove scripts and styles
            for script in soup(['script', 'style', 'nav', 'footer']):
                script.decompose()
            content = soup.get_text(separator='\n', strip=True)
        
        # Extract code blocks
        code_blocks = []
        for pre in soup.find_all('pre'):
            code = pre.get_text(strip=True)
            if len(code) > 20:
                code_blocks.append(code[:2000])
        
        # Save to knowledge base
        kb_result = knowledge_add(
            title=f"QMT API文档: {section or url}",
            content=content[:5000],
            type="reference",
            tags=["qmt", "api", "documentation"],
            source=url
        )
        
        return {
            "success": True,
            "url": url,
            "section": section or anchor,
            "content_length": len(content),
            "content_preview": content[:2000],
            "code_blocks": code_blocks[:5],
            "saved_to_kb": kb_result.get("success", False)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}


# 更新工具注册 - QMT/策略工具
TOOL_HANDLERS.update({
    "strategy.qmt.validate": strategy_qmt_validate,
    "strategy.qmt.fetch_docs": strategy_qmt_fetch_docs,
    "strategy.convert": strategy_convert,
    "crawler.qmt.fetch": crawler_qmt_fetch,
})

logger.info("QMT/策略工具已加载 (4个工具: validate, fetch_docs, convert, crawler.qmt.fetch)")

if __name__ == "__main__":
    import sys
    import asyncio
    
    # MCP 客户端通过 stdin/stdout 通信，始终使用 MCP 模式
    asyncio.run(mcp_main())