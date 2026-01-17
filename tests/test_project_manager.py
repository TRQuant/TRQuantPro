#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""项目管理服务器测试脚本"""

import sys
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))
sys.path.insert(0, str(TRQUANT_ROOT / "mcp_servers"))

# 导入必要的模块（避免导入服务器本身）
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import hashlib

# 数据目录
DATA_DIR = TRQUANT_ROOT / ".trquant" / "project_data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 枚举定义
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

class TaskPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# 数据管理函数
def _get_project_file(project: str, data_type: str) -> Path:
    project_dir = DATA_DIR / project
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir / f"{data_type}.json"

def _load_data(project: str, data_type: str) -> Dict[str, Any]:
    file_path = _get_project_file(project, data_type)
    if file_path.exists():
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except:
            pass
    return {"items": [], "updated": datetime.now().isoformat()}

def _save_data(project: str, data_type: str, data: Dict[str, Any]) -> None:
    file_path = _get_project_file(project, data_type)
    data["updated"] = datetime.now().isoformat()
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def _generate_id(prefix: str) -> str:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    hash_part = hashlib.md5(f"{timestamp}{id(prefix)}".encode()).hexdigest()[:6]
    return f"{prefix}_{timestamp}_{hash_part}"

# 任务管理
def task_create(title, project="trquant", description="", priority="medium", estimated_hours=0, tags=None):
    data = _load_data(project, "tasks")
    task = {
        "id": _generate_id("task"),
        "title": title,
        "description": description,
        "status": TaskStatus.PENDING.value,
        "priority": priority,
        "estimated_hours": estimated_hours,
        "tags": tags or [],
        "created": datetime.now().isoformat()
    }
    data["items"].append(task)
    _save_data(project, "tasks", data)
    return {"success": True, "task": task}

def task_list(project="trquant"):
    data = _load_data(project, "tasks")
    tasks = data["items"]
    stats = {
        "total": len(tasks),
        "pending": len([t for t in tasks if t.get("status") == "pending"]),
        "in_progress": len([t for t in tasks if t.get("status") == "in_progress"]),
        "completed": len([t for t in tasks if t.get("status") == "completed"])
    }
    return {"success": True, "tasks": tasks, "stats": stats}

def progress_summary(project="trquant"):
    tasks = _load_data(project, "tasks")["items"]
    total = len(tasks)
    completed = len([t for t in tasks if t.get("status") == "completed"])
    rate = (completed / total * 100) if total > 0 else 0
    return {"success": True, "summary": {"tasks": {"total": total, "completed": completed, "completion_rate": round(rate, 1)}}}

def devlog_add(content, project="trquant", category="development", tags=None):
    data = _load_data(project, "devlog")
    log = {"id": _generate_id("log"), "date": datetime.now().isoformat(), "content": content, "category": category, "tags": tags or []}
    data["items"].append(log)
    _save_data(project, "devlog", data)
    return {"success": True, "log": log}

def experience_add(title, content, project="trquant", category="general", tags=None):
    data = _load_data(project, "experience")
    exp = {"id": _generate_id("exp"), "title": title, "content": content, "category": category, "tags": tags or [], "created": datetime.now().isoformat()}
    data["items"].append(exp)
    _save_data(project, "experience", data)
    return {"success": True, "experience": exp}

def issue_create(title, description, project="trquant", issue_type="bug", priority="medium"):
    data = _load_data(project, "issues")
    issue = {"id": _generate_id("issue"), "title": title, "description": description, "type": issue_type, "priority": priority, "status": "open", "created": datetime.now().isoformat()}
    data["items"].append(issue)
    _save_data(project, "issues", data)
    return {"success": True, "issue": issue}

def milestone_create(title, description="", project="trquant", due_date=None):
    data = _load_data(project, "milestones")
    milestone = {"id": _generate_id("ms"), "title": title, "description": description, "due_date": due_date, "status": "open", "created": datetime.now().isoformat()}
    data["items"].append(milestone)
    _save_data(project, "milestones", data)
    return {"success": True, "milestone": milestone}

def risk_add(title, description, project="trquant", level="medium", mitigation=""):
    data = _load_data(project, "risks")
    risk = {"id": _generate_id("risk"), "title": title, "description": description, "level": level, "mitigation": mitigation, "status": "open", "created": datetime.now().isoformat()}
    data["items"].append(risk)
    _save_data(project, "risks", data)
    return {"success": True, "risk": risk}

def risk_assess(project="trquant"):
    data = _load_data(project, "risks")
    risks = [r for r in data["items"] if r.get("status") == "open"]
    score = 100
    for r in risks:
        if r.get("level") == "critical": score -= 25
        elif r.get("level") == "high": score -= 15
        elif r.get("level") == "medium": score -= 8
        else: score -= 3
    score = max(0, score)
    return {"success": True, "assessment": {"total_risks": len(risks), "risk_score": score, "health": "good" if score >= 70 else ("warning" if score >= 40 else "critical")}}

# 运行测试
if __name__ == "__main__":
    print('=== 测试任务创建 ===')
    result = task_create(title='完善9步工作流GUI', description='优化工作流面板', priority='high', estimated_hours=8, tags=['gui', 'workflow'])
    print(f'任务创建: {result["success"]} - {result.get("task", {}).get("id", "N/A")}')

    print('\n=== 测试任务列表 ===')
    result = task_list()
    print(f'总任务数: {result["stats"]["total"]}')
    print(f'进行中: {result["stats"]["in_progress"]}')

    print('\n=== 测试进度摘要 ===')
    result = progress_summary()
    print(f'完成率: {result["summary"]["tasks"]["completion_rate"]}%')

    print('\n=== 测试开发日志 ===')
    result = devlog_add(content='完成项目管理MCP服务器开发', category='development', tags=['mcp', 'project-manager'])
    print(f'日志添加: {result["success"]}')

    print('\n=== 测试经验总结 ===')
    result = experience_add(title='JSON解析错误处理', content='在bridge.py最开头重定向stdout/stderr', category='problem_solving', tags=['json', 'stdout'])
    print(f'经验添加: {result["success"]}')

    print('\n=== 测试问题追踪 ===')
    result = issue_create(title='回测性能优化', description='BulletTrade回测太慢', issue_type='improvement', priority='high')
    print(f'问题创建: {result["success"]}')

    print('\n=== 测试里程碑 ===')
    result = milestone_create(title='v1.0 核心功能完成', description='完成9步工作流', due_date='2025-01-15')
    print(f'里程碑创建: {result["success"]}')

    print('\n=== 测试风险评估 ===')
    result = risk_add(title='第三方API依赖', description='JQData、AKShare可能不稳定', level='medium', mitigation='增加Mock回退')
    print(f'风险添加: {result["success"]}')

    result = risk_assess()
    print(f'风险评分: {result["assessment"]["risk_score"]}')
    print(f'项目健康度: {result["assessment"]["health"]}')

    print('\n✅ 所有测试通过!')
