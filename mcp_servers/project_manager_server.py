#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 项目规划管理服务器
============================

基于实际开发经验构建的项目管理MCP服务器

功能模块:
    1. 任务管理 - task.*
    2. 进度跟踪 - progress.*
    3. 开发日志 - devlog.*
    4. 经验总结 - experience.*
    5. 问题追踪 - issue.*
    6. 里程碑管理 - milestone.*
    7. 风险评估 - risk.*

运行方式:
    python mcp_servers/project_manager_server.py

设计原则:
    - 基于实际开发经验
    - 支持多项目管理
    - 自动进度统计
    - 经验复用
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
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
logger = logging.getLogger('ProjectManagerServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
    logger.info("项目管理MCP服务器已加载")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用: {e}")
    sys.exit(1)

# 创建服务器
server = Server("trquant-project-manager")

# 数据目录
DATA_DIR = TRQUANT_ROOT / ".trquant" / "project_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==================== 枚举定义 ====================

class TaskStatus(str, Enum):
    PENDING = "pending"          # 待处理
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    BLOCKED = "blocked"          # 被阻塞
    CANCELLED = "cancelled"      # 已取消
    REVIEW = "review"            # 待审查

class TaskPriority(str, Enum):
    CRITICAL = "critical"  # 紧急
    HIGH = "high"          # 高
    MEDIUM = "medium"      # 中
    LOW = "low"            # 低

class IssueType(str, Enum):
    BUG = "bug"                  # Bug
    FEATURE = "feature"          # 新功能
    IMPROVEMENT = "improvement"  # 改进
    QUESTION = "question"        # 问题
    DOCUMENTATION = "documentation"  # 文档

class RiskLevel(str, Enum):
    CRITICAL = "critical"  # 严重
    HIGH = "high"          # 高
    MEDIUM = "medium"      # 中
    LOW = "low"            # 低

# ==================== 数据管理 ====================

def _get_project_file(project: str, data_type: str) -> Path:
    """获取项目数据文件路径"""
    project_dir = DATA_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir / f"{data_type}.json"

def _load_data(project: str, data_type: str) -> Dict[str, Any]:
    """加载数据"""
    file_path = _get_project_file(project, data_type)
    if file_path.exists():
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"加载数据失败: {e}")
    return {"items": [], "updated": datetime.now().isoformat()}

def _save_data(project: str, data_type: str, data: Dict[str, Any]) -> None:
    """保存数据"""
    file_path = _get_project_file(project, data_type)
    data["updated"] = datetime.now().isoformat()
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

def _generate_id(prefix: str) -> str:
    """生成唯一ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    hash_part = hashlib.md5(f"{timestamp}{id(prefix)}".encode()).hexdigest()[:6]
    return f"{prefix}_{timestamp}_{hash_part}"

# ==================== 任务管理 ====================

def task_create(
    title: str,
    project: str = "trquant",
    description: str = "",
    priority: str = TaskPriority.MEDIUM.value,
    estimated_hours: float = 0,
    tags: List[str] = None,
    parent_id: str = None,
    depends_on: List[str] = None
) -> Dict[str, Any]:
    """创建任务"""
    data = _load_data(project, "tasks")
    
    task = {
        "id": _generate_id("task"),
        "title": title,
        "description": description,
        "status": TaskStatus.PENDING.value,
        "priority": priority,
        "estimated_hours": estimated_hours,
        "actual_hours": 0,
        "tags": tags or [],
        "parent_id": parent_id,
        "depends_on": depends_on or [],
        "subtasks": [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "started": None,
        "completed": None,
        "notes": []
    }
    
    if parent_id:
        # 添加为子任务
        for item in data["items"]:
            if item["id"] == parent_id:
                item.setdefault("subtasks", []).append(task["id"])
                break
    
    data["items"].append(task)
    _save_data(project, "tasks", data)
    
    return {"success": True, "task": task, "message": f"任务已创建: {task['id']}"}

def task_update(
    task_id: str,
    project: str = "trquant",
    **updates
) -> Dict[str, Any]:
    """更新任务"""
    data = _load_data(project, "tasks")
    
    for task in data["items"]:
        if task["id"] == task_id:
            # 状态变更处理
            new_status = updates.get("status")
            if new_status:
                if new_status == TaskStatus.IN_PROGRESS.value and not task.get("started"):
                    task["started"] = datetime.now().isoformat()
                elif new_status == TaskStatus.COMPLETED.value and not task.get("completed"):
                    task["completed"] = datetime.now().isoformat()
            
            # 更新字段
            for key, value in updates.items():
                if key in task and value is not None:
                    task[key] = value
            
            task["updated"] = datetime.now().isoformat()
            _save_data(project, "tasks", data)
            return {"success": True, "task": task, "message": "任务已更新"}
    
    return {"success": False, "error": f"未找到任务: {task_id}"}

def task_list(
    project: str = "trquant",
    status: str = None,
    priority: str = None,
    tag: str = None
) -> Dict[str, Any]:
    """列出任务"""
    data = _load_data(project, "tasks")
    tasks = data["items"]
    
    # 过滤
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    if priority:
        tasks = [t for t in tasks if t.get("priority") == priority]
    if tag:
        tasks = [t for t in tasks if tag in t.get("tags", [])]
    
    # 统计
    stats = {
        "total": len(data["items"]),
        "pending": len([t for t in data["items"] if t.get("status") == TaskStatus.PENDING.value]),
        "in_progress": len([t for t in data["items"] if t.get("status") == TaskStatus.IN_PROGRESS.value]),
        "completed": len([t for t in data["items"] if t.get("status") == TaskStatus.COMPLETED.value]),
        "blocked": len([t for t in data["items"] if t.get("status") == TaskStatus.BLOCKED.value])
    }
    
    return {
        "success": True,
        "tasks": tasks,
        "filtered_count": len(tasks),
        "stats": stats
    }

def task_add_note(task_id: str, note: str, project: str = "trquant") -> Dict[str, Any]:
    """为任务添加备注"""
    data = _load_data(project, "tasks")
    
    for task in data["items"]:
        if task["id"] == task_id:
            task.setdefault("notes", []).append({
                "content": note,
                "timestamp": datetime.now().isoformat()
            })
            task["updated"] = datetime.now().isoformat()
            _save_data(project, "tasks", data)
            return {"success": True, "message": "备注已添加"}
    
    return {"success": False, "error": f"未找到任务: {task_id}"}

# ==================== 进度跟踪 ====================

def progress_summary(project: str = "trquant") -> Dict[str, Any]:
    """获取项目进度摘要"""
    tasks_data = _load_data(project, "tasks")
    milestones_data = _load_data(project, "milestones")
    
    tasks = tasks_data["items"]
    milestones = milestones_data["items"]
    
    # 任务统计
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get("status") == TaskStatus.COMPLETED.value])
    in_progress_tasks = len([t for t in tasks if t.get("status") == TaskStatus.IN_PROGRESS.value])
    
    # 工时统计
    total_estimated = sum(t.get("estimated_hours", 0) for t in tasks)
    total_actual = sum(t.get("actual_hours", 0) for t in tasks)
    
    # 里程碑统计
    total_milestones = len(milestones)
    completed_milestones = len([m for m in milestones if m.get("status") == "completed"])
    
    # 计算完成率
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "success": True,
        "project": project,
        "summary": {
            "tasks": {
                "total": total_tasks,
                "completed": completed_tasks,
                "in_progress": in_progress_tasks,
                "pending": total_tasks - completed_tasks - in_progress_tasks,
                "completion_rate": round(completion_rate, 1)
            },
            "hours": {
                "estimated": total_estimated,
                "actual": total_actual,
                "efficiency": round(total_estimated / total_actual * 100, 1) if total_actual > 0 else 0
            },
            "milestones": {
                "total": total_milestones,
                "completed": completed_milestones,
                "remaining": total_milestones - completed_milestones
            }
        },
        "updated": datetime.now().isoformat()
    }

def progress_daily_report(project: str = "trquant", date: str = None) -> Dict[str, Any]:
    """生成每日进度报告"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    tasks_data = _load_data(project, "tasks")
    devlog_data = _load_data(project, "devlog")
    
    # 当日完成的任务
    completed_today = [
        t for t in tasks_data["items"]
        if t.get("completed", "").startswith(date)
    ]
    
    # 当日的开发日志
    today_logs = [
        log for log in devlog_data["items"]
        if log.get("date", "").startswith(date)
    ]
    
    # 进行中的任务
    in_progress = [
        t for t in tasks_data["items"]
        if t.get("status") == TaskStatus.IN_PROGRESS.value
    ]
    
    return {
        "success": True,
        "date": date,
        "report": {
            "completed_tasks": [{"id": t["id"], "title": t["title"]} for t in completed_today],
            "in_progress_tasks": [{"id": t["id"], "title": t["title"]} for t in in_progress],
            "dev_logs": today_logs,
            "total_completed": len(completed_today),
            "total_in_progress": len(in_progress)
        }
    }

# ==================== 开发日志 ====================

def devlog_add(
    content: str,
    project: str = "trquant",
    category: str = "development",
    tags: List[str] = None,
    related_tasks: List[str] = None
) -> Dict[str, Any]:
    """添加开发日志"""
    data = _load_data(project, "devlog")
    
    log_entry = {
        "id": _generate_id("log"),
        "date": datetime.now().isoformat(),
        "content": content,
        "category": category,
        "tags": tags or [],
        "related_tasks": related_tasks or []
    }
    
    data["items"].append(log_entry)
    _save_data(project, "devlog", data)
    
    return {"success": True, "log": log_entry, "message": "开发日志已添加"}

def devlog_list(
    project: str = "trquant",
    category: str = None,
    days: int = 7
) -> Dict[str, Any]:
    """列出开发日志"""
    data = _load_data(project, "devlog")
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    logs = [log for log in data["items"] if log.get("date", "") >= cutoff_date]
    
    if category:
        logs = [log for log in logs if log.get("category") == category]
    
    # 按日期分组
    grouped = {}
    for log in logs:
        date = log.get("date", "")[:10]
        grouped.setdefault(date, []).append(log)
    
    return {
        "success": True,
        "logs": logs,
        "grouped_by_date": grouped,
        "total": len(logs)
    }

# ==================== 经验总结 ====================

def experience_add(
    title: str,
    content: str,
    project: str = "trquant",
    category: str = "general",
    tags: List[str] = None,
    related_issues: List[str] = None
) -> Dict[str, Any]:
    """添加经验总结"""
    data = _load_data(project, "experience")
    
    experience = {
        "id": _generate_id("exp"),
        "title": title,
        "content": content,
        "category": category,
        "tags": tags or [],
        "related_issues": related_issues or [],
        "created": datetime.now().isoformat(),
        "useful_count": 0
    }
    
    data["items"].append(experience)
    _save_data(project, "experience", data)
    
    return {"success": True, "experience": experience, "message": "经验已记录"}

def experience_search(
    keyword: str,
    project: str = "trquant",
    category: str = None
) -> Dict[str, Any]:
    """搜索经验"""
    data = _load_data(project, "experience")
    
    results = []
    keyword_lower = keyword.lower()
    
    for exp in data["items"]:
        if (keyword_lower in exp.get("title", "").lower() or 
            keyword_lower in exp.get("content", "").lower() or
            keyword_lower in " ".join(exp.get("tags", [])).lower()):
            if category is None or exp.get("category") == category:
                results.append(exp)
    
    # 按useful_count排序
    results.sort(key=lambda x: x.get("useful_count", 0), reverse=True)
    
    return {
        "success": True,
        "keyword": keyword,
        "results": results,
        "total": len(results)
    }

def experience_mark_useful(exp_id: str, project: str = "trquant") -> Dict[str, Any]:
    """标记经验为有用"""
    data = _load_data(project, "experience")
    
    for exp in data["items"]:
        if exp["id"] == exp_id:
            exp["useful_count"] = exp.get("useful_count", 0) + 1
            _save_data(project, "experience", data)
            return {"success": True, "message": "已标记为有用", "useful_count": exp["useful_count"]}
    
    return {"success": False, "error": f"未找到经验: {exp_id}"}

# ==================== 问题追踪 ====================

def issue_create(
    title: str,
    description: str,
    project: str = "trquant",
    issue_type: str = IssueType.BUG.value,
    priority: str = TaskPriority.MEDIUM.value,
    tags: List[str] = None
) -> Dict[str, Any]:
    """创建问题"""
    data = _load_data(project, "issues")
    
    issue = {
        "id": _generate_id("issue"),
        "title": title,
        "description": description,
        "type": issue_type,
        "priority": priority,
        "status": "open",
        "tags": tags or [],
        "created": datetime.now().isoformat(),
        "resolved": None,
        "solution": None,
        "related_tasks": []
    }
    
    data["items"].append(issue)
    _save_data(project, "issues", data)
    
    return {"success": True, "issue": issue, "message": f"问题已创建: {issue['id']}"}

def issue_resolve(
    issue_id: str,
    solution: str,
    project: str = "trquant"
) -> Dict[str, Any]:
    """解决问题"""
    data = _load_data(project, "issues")
    
    for issue in data["items"]:
        if issue["id"] == issue_id:
            issue["status"] = "resolved"
            issue["solution"] = solution
            issue["resolved"] = datetime.now().isoformat()
            _save_data(project, "issues", data)
            
            # 自动添加为经验
            experience_add(
                title=f"问题解决: {issue['title']}",
                content=f"问题描述:\n{issue['description']}\n\n解决方案:\n{solution}",
                project=project,
                category="problem_solving",
                tags=issue.get("tags", []),
                related_issues=[issue_id]
            )
            
            return {"success": True, "issue": issue, "message": "问题已解决，并记录为经验"}
    
    return {"success": False, "error": f"未找到问题: {issue_id}"}

def issue_list(
    project: str = "trquant",
    status: str = None,
    issue_type: str = None
) -> Dict[str, Any]:
    """列出问题"""
    data = _load_data(project, "issues")
    issues = data["items"]
    
    if status:
        issues = [i for i in issues if i.get("status") == status]
    if issue_type:
        issues = [i for i in issues if i.get("type") == issue_type]
    
    # 统计
    stats = {
        "total": len(data["items"]),
        "open": len([i for i in data["items"] if i.get("status") == "open"]),
        "resolved": len([i for i in data["items"] if i.get("status") == "resolved"]),
        "by_type": {}
    }
    for t in IssueType:
        stats["by_type"][t.value] = len([i for i in data["items"] if i.get("type") == t.value])
    
    return {
        "success": True,
        "issues": issues,
        "stats": stats
    }

# ==================== 里程碑管理 ====================

def milestone_create(
    title: str,
    description: str = "",
    project: str = "trquant",
    due_date: str = None,
    tasks: List[str] = None
) -> Dict[str, Any]:
    """创建里程碑"""
    data = _load_data(project, "milestones")
    
    milestone = {
        "id": _generate_id("ms"),
        "title": title,
        "description": description,
        "status": "open",
        "due_date": due_date,
        "tasks": tasks or [],
        "created": datetime.now().isoformat(),
        "completed": None
    }
    
    data["items"].append(milestone)
    _save_data(project, "milestones", data)
    
    return {"success": True, "milestone": milestone, "message": f"里程碑已创建: {milestone['id']}"}

def milestone_progress(milestone_id: str, project: str = "trquant") -> Dict[str, Any]:
    """获取里程碑进度"""
    ms_data = _load_data(project, "milestones")
    tasks_data = _load_data(project, "tasks")
    
    for milestone in ms_data["items"]:
        if milestone["id"] == milestone_id:
            task_ids = milestone.get("tasks", [])
            tasks = [t for t in tasks_data["items"] if t["id"] in task_ids]
            
            total = len(tasks)
            completed = len([t for t in tasks if t.get("status") == TaskStatus.COMPLETED.value])
            
            return {
                "success": True,
                "milestone": milestone,
                "progress": {
                    "total_tasks": total,
                    "completed_tasks": completed,
                    "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
                },
                "tasks": [{"id": t["id"], "title": t["title"], "status": t["status"]} for t in tasks]
            }
    
    return {"success": False, "error": f"未找到里程碑: {milestone_id}"}

# ==================== 风险评估 ====================

def risk_add(
    title: str,
    description: str,
    project: str = "trquant",
    level: str = RiskLevel.MEDIUM.value,
    mitigation: str = "",
    related_tasks: List[str] = None
) -> Dict[str, Any]:
    """添加风险"""
    data = _load_data(project, "risks")
    
    risk = {
        "id": _generate_id("risk"),
        "title": title,
        "description": description,
        "level": level,
        "status": "open",
        "mitigation": mitigation,
        "related_tasks": related_tasks or [],
        "created": datetime.now().isoformat(),
        "resolved": None
    }
    
    data["items"].append(risk)
    _save_data(project, "risks", data)
    
    return {"success": True, "risk": risk, "message": f"风险已记录: {risk['id']}"}

def risk_assess(project: str = "trquant") -> Dict[str, Any]:
    """评估项目风险"""
    data = _load_data(project, "risks")
    risks = [r for r in data["items"] if r.get("status") == "open"]
    
    # 按级别统计
    by_level = {
        RiskLevel.CRITICAL.value: [],
        RiskLevel.HIGH.value: [],
        RiskLevel.MEDIUM.value: [],
        RiskLevel.LOW.value: []
    }
    
    for risk in risks:
        level = risk.get("level", RiskLevel.MEDIUM.value)
        by_level[level].append({"id": risk["id"], "title": risk["title"]})
    
    # 计算风险分数 (0-100)
    score = 100
    score -= len(by_level[RiskLevel.CRITICAL.value]) * 25
    score -= len(by_level[RiskLevel.HIGH.value]) * 15
    score -= len(by_level[RiskLevel.MEDIUM.value]) * 8
    score -= len(by_level[RiskLevel.LOW.value]) * 3
    score = max(0, score)
    
    return {
        "success": True,
        "assessment": {
            "total_risks": len(risks),
            "by_level": by_level,
            "risk_score": score,
            "health": "good" if score >= 70 else ("warning" if score >= 40 else "critical")
        }
    }

# ==================== MCP工具定义 ====================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        # 任务管理
        Tool(
            name="task.create",
            description="创建新任务，支持优先级、标签、依赖关系",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "任务标题"},
                    "project": {"type": "string", "default": "trquant", "description": "项目名称"},
                    "description": {"type": "string", "description": "任务描述"},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "medium"},
                    "estimated_hours": {"type": "number", "description": "预估工时"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表"},
                    "parent_id": {"type": "string", "description": "父任务ID"},
                    "depends_on": {"type": "array", "items": {"type": "string"}, "description": "依赖任务ID列表"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="task.update",
            description="更新任务状态和信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "project": {"type": "string", "default": "trquant"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "blocked", "cancelled", "review"]},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                    "actual_hours": {"type": "number", "description": "实际工时"}
                },
                "required": ["task_id"]
            }
        ),
        Tool(
            name="task.list",
            description="列出任务，支持按状态、优先级、标签过滤",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"},
                    "status": {"type": "string", "enum": ["pending", "in_progress", "completed", "blocked", "cancelled", "review"]},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
                    "tag": {"type": "string", "description": "按标签过滤"}
                }
            }
        ),
        Tool(
            name="task.add_note",
            description="为任务添加备注",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "note": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"}
                },
                "required": ["task_id", "note"]
            }
        ),
        
        # 进度跟踪
        Tool(
            name="progress.summary",
            description="获取项目进度摘要，包括任务统计、工时统计、里程碑进度",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"}
                }
            }
        ),
        Tool(
            name="progress.daily_report",
            description="生成每日进度报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"},
                    "date": {"type": "string", "description": "日期，格式YYYY-MM-DD，默认今天"}
                }
            }
        ),
        
        # 开发日志
        Tool(
            name="devlog.add",
            description="添加开发日志，记录开发过程",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "日志内容"},
                    "project": {"type": "string", "default": "trquant"},
                    "category": {"type": "string", "default": "development", "description": "分类：development/debug/design/meeting"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "related_tasks": {"type": "array", "items": {"type": "string"}, "description": "关联任务ID"}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="devlog.list",
            description="列出开发日志",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"},
                    "category": {"type": "string"},
                    "days": {"type": "integer", "default": 7, "description": "查看最近几天"}
                }
            }
        ),
        
        # 经验总结
        Tool(
            name="experience.add",
            description="添加经验总结，便于知识复用",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"},
                    "category": {"type": "string", "default": "general", "description": "分类：general/problem_solving/best_practice/pitfall"},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "related_issues": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["title", "content"]
            }
        ),
        Tool(
            name="experience.search",
            description="搜索经验，按关键词和分类",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"},
                    "category": {"type": "string"}
                },
                "required": ["keyword"]
            }
        ),
        Tool(
            name="experience.mark_useful",
            description="标记经验为有用，提升搜索排名",
            inputSchema={
                "type": "object",
                "properties": {
                    "exp_id": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"}
                },
                "required": ["exp_id"]
            }
        ),
        
        # 问题追踪
        Tool(
            name="issue.create",
            description="创建问题，记录Bug、新功能需求等",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"},
                    "issue_type": {"type": "string", "enum": ["bug", "feature", "improvement", "question", "documentation"], "default": "bug"},
                    "priority": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "medium"},
                    "tags": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["title", "description"]
            }
        ),
        Tool(
            name="issue.resolve",
            description="解决问题，自动记录为经验",
            inputSchema={
                "type": "object",
                "properties": {
                    "issue_id": {"type": "string"},
                    "solution": {"type": "string", "description": "解决方案"},
                    "project": {"type": "string", "default": "trquant"}
                },
                "required": ["issue_id", "solution"]
            }
        ),
        Tool(
            name="issue.list",
            description="列出问题",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"},
                    "status": {"type": "string", "enum": ["open", "resolved"]},
                    "issue_type": {"type": "string", "enum": ["bug", "feature", "improvement", "question", "documentation"]}
                }
            }
        ),
        
        # 里程碑管理
        Tool(
            name="milestone.create",
            description="创建里程碑，关联任务",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"},
                    "due_date": {"type": "string", "description": "截止日期，格式YYYY-MM-DD"},
                    "tasks": {"type": "array", "items": {"type": "string"}, "description": "关联任务ID"}
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="milestone.progress",
            description="获取里程碑进度",
            inputSchema={
                "type": "object",
                "properties": {
                    "milestone_id": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"}
                },
                "required": ["milestone_id"]
            }
        ),
        
        # 风险评估
        Tool(
            name="risk.add",
            description="添加项目风险",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "project": {"type": "string", "default": "trquant"},
                    "level": {"type": "string", "enum": ["critical", "high", "medium", "low"], "default": "medium"},
                    "mitigation": {"type": "string", "description": "缓解措施"},
                    "related_tasks": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["title", "description"]
            }
        ),
        Tool(
            name="risk.assess",
            description="评估项目整体风险状况",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "default": "trquant"}
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    try:
        handlers = {
            # 任务管理
            "task.create": lambda a: task_create(**a),
            "task.update": lambda a: task_update(a.pop("task_id"), **a),
            "task.list": lambda a: task_list(**a),
            "task.add_note": lambda a: task_add_note(a["task_id"], a["note"], a.get("project", "trquant")),
            
            # 进度跟踪
            "progress.summary": lambda a: progress_summary(a.get("project", "trquant")),
            "progress.daily_report": lambda a: progress_daily_report(a.get("project", "trquant"), a.get("date")),
            
            # 开发日志
            "devlog.add": lambda a: devlog_add(**a),
            "devlog.list": lambda a: devlog_list(**a),
            
            # 经验总结
            "experience.add": lambda a: experience_add(**a),
            "experience.search": lambda a: experience_search(a["keyword"], a.get("project", "trquant"), a.get("category")),
            "experience.mark_useful": lambda a: experience_mark_useful(a["exp_id"], a.get("project", "trquant")),
            
            # 问题追踪
            "issue.create": lambda a: issue_create(**a),
            "issue.resolve": lambda a: issue_resolve(a["issue_id"], a["solution"], a.get("project", "trquant")),
            "issue.list": lambda a: issue_list(**a),
            
            # 里程碑
            "milestone.create": lambda a: milestone_create(**a),
            "milestone.progress": lambda a: milestone_progress(a["milestone_id"], a.get("project", "trquant")),
            
            # 风险评估
            "risk.add": lambda a: risk_add(**a),
            "risk.assess": lambda a: risk_assess(a.get("project", "trquant"))
        }
        
        if name in handlers:
            result = handlers[name](arguments.copy())
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False))]
    
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

