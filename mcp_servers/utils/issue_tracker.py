"""
问题记录和Debug工具
==================
用于记录已解决的问题、解决方案和代码模式，
避免重复研究已解决的问题。
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# 存储路径
ISSUES_DIR = Path(__file__).parent.parent.parent / "data" / "issues"
ISSUES_DIR.mkdir(parents=True, exist_ok=True)

ISSUES_FILE = ISSUES_DIR / "known_issues.json"
SOLUTIONS_FILE = ISSUES_DIR / "solutions.json"
PATTERNS_FILE = ISSUES_DIR / "code_patterns.json"


def _load_json(filepath: Path) -> Dict:
    """加载JSON文件"""
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"items": [], "version": "1.0"}


def _save_json(filepath: Path, data: Dict):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _generate_id(content: str) -> str:
    """生成唯一ID"""
    return hashlib.md5(content.encode()).hexdigest()[:12]


# ============================================================
# 问题记录
# ============================================================

def record_issue(
    title: str,
    description: str,
    error_message: str,
    category: str = "general",
    tags: List[str] = None
) -> Dict:
    """记录一个问题"""
    data = _load_json(ISSUES_FILE)
    
    issue_id = _generate_id(f"{title}_{error_message}")
    
    # 检查是否已存在
    for item in data["items"]:
        if item["id"] == issue_id:
            return {"success": True, "message": "问题已存在", "issue_id": issue_id, "existing": True}
    
    issue = {
        "id": issue_id,
        "title": title,
        "description": description,
        "error_message": error_message,
        "category": category,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "status": "open",
        "solution_id": None
    }
    
    data["items"].append(issue)
    _save_json(ISSUES_FILE, data)
    
    return {"success": True, "message": "问题已记录", "issue_id": issue_id}


def search_issue(query: str) -> Dict:
    """搜索已知问题"""
    data = _load_json(ISSUES_FILE)
    results = []
    
    query_lower = query.lower()
    for item in data["items"]:
        if (query_lower in item["title"].lower() or
            query_lower in item["description"].lower() or
            query_lower in item["error_message"].lower() or
            any(query_lower in tag.lower() for tag in item.get("tags", []))):
            results.append(item)
    
    return {"success": True, "count": len(results), "issues": results}


def list_issues(status: str = None, category: str = None) -> Dict:
    """列出问题"""
    data = _load_json(ISSUES_FILE)
    items = data["items"]
    
    if status:
        items = [i for i in items if i["status"] == status]
    if category:
        items = [i for i in items if i["category"] == category]
    
    return {"success": True, "count": len(items), "issues": items}


# ============================================================
# 解决方案记录
# ============================================================

def record_solution(
    issue_id: str,
    title: str,
    description: str,
    code_snippet: str = None,
    steps: List[str] = None,
    files_modified: List[str] = None
) -> Dict:
    """记录解决方案"""
    # 加载数据
    solutions = _load_json(SOLUTIONS_FILE)
    issues = _load_json(ISSUES_FILE)
    
    solution_id = _generate_id(f"{issue_id}_{title}")
    
    solution = {
        "id": solution_id,
        "issue_id": issue_id,
        "title": title,
        "description": description,
        "code_snippet": code_snippet,
        "steps": steps or [],
        "files_modified": files_modified or [],
        "created_at": datetime.now().isoformat(),
        "verified": False
    }
    
    solutions["items"].append(solution)
    _save_json(SOLUTIONS_FILE, solutions)
    
    # 更新问题状态
    for item in issues["items"]:
        if item["id"] == issue_id:
            item["status"] = "resolved"
            item["solution_id"] = solution_id
            break
    _save_json(ISSUES_FILE, issues)
    
    return {"success": True, "message": "解决方案已记录", "solution_id": solution_id}


def get_solution(issue_id: str = None, solution_id: str = None) -> Dict:
    """获取解决方案"""
    data = _load_json(SOLUTIONS_FILE)
    
    for item in data["items"]:
        if (issue_id and item["issue_id"] == issue_id) or \
           (solution_id and item["id"] == solution_id):
            return {"success": True, "solution": item}
    
    return {"success": False, "error": "解决方案未找到"}


def search_solution(query: str) -> Dict:
    """搜索解决方案"""
    data = _load_json(SOLUTIONS_FILE)
    results = []
    
    query_lower = query.lower()
    for item in data["items"]:
        if (query_lower in item["title"].lower() or
            query_lower in item["description"].lower() or
            (item.get("code_snippet") and query_lower in item["code_snippet"].lower())):
            results.append(item)
    
    return {"success": True, "count": len(results), "solutions": results}


# ============================================================
# 代码模式记录
# ============================================================

def record_pattern(
    name: str,
    description: str,
    problem_pattern: str,
    solution_pattern: str,
    example_code: str = None,
    category: str = "general"
) -> Dict:
    """记录代码模式（问题模式 -> 解决方案模式）"""
    data = _load_json(PATTERNS_FILE)
    
    pattern_id = _generate_id(f"{name}_{problem_pattern[:50]}")
    
    pattern = {
        "id": pattern_id,
        "name": name,
        "description": description,
        "problem_pattern": problem_pattern,
        "solution_pattern": solution_pattern,
        "example_code": example_code,
        "category": category,
        "created_at": datetime.now().isoformat(),
        "usage_count": 0
    }
    
    data["items"].append(pattern)
    _save_json(PATTERNS_FILE, data)
    
    return {"success": True, "message": "代码模式已记录", "pattern_id": pattern_id}


def match_pattern(error_message: str) -> Dict:
    """根据错误信息匹配已知模式"""
    data = _load_json(PATTERNS_FILE)
    matches = []
    
    error_lower = error_message.lower()
    for item in data["items"]:
        if item["problem_pattern"].lower() in error_lower:
            matches.append({
                "pattern": item,
                "confidence": "high" if item["problem_pattern"].lower() == error_lower else "medium"
            })
    
    return {"success": True, "count": len(matches), "matches": matches}


# ============================================================
# 快速查找（用于自动debug）
# ============================================================

def quick_debug(error_message: str) -> Dict:
    """
    快速debug：根据错误信息自动查找解决方案
    返回：已知问题、解决方案、相关代码模式
    """
    results = {
        "success": True,
        "error_message": error_message,
        "known_issues": [],
        "solutions": [],
        "patterns": []
    }
    
    # 搜索已知问题
    issue_result = search_issue(error_message)
    if issue_result["count"] > 0:
        results["known_issues"] = issue_result["issues"]
        
        # 获取相关解决方案
        for issue in issue_result["issues"]:
            if issue.get("solution_id"):
                sol = get_solution(solution_id=issue["solution_id"])
                if sol.get("success"):
                    results["solutions"].append(sol["solution"])
    
    # 匹配代码模式
    pattern_result = match_pattern(error_message)
    if pattern_result["count"] > 0:
        results["patterns"] = [m["pattern"] for m in pattern_result["matches"]]
    
    # 判断是否找到解决方案
    results["found_solution"] = len(results["solutions"]) > 0 or len(results["patterns"]) > 0
    
    return results


# ============================================================
# 初始化：记录当前问题
# ============================================================

def init_known_issues():
    """初始化已知问题（首次运行时调用）"""
    # 记录 JQData auth success 问题
    record_issue(
        title="JQData认证输出污染JSON响应",
        description="JQData SDK在认证时会打印'auth success'到stdout，导致JSON解析失败",
        error_message="SyntaxError: Unexpected token 'a', \"auth succe\"... is not valid JSON",
        category="json_parsing",
        tags=["jqdata", "stdout", "json", "auth"]
    )
    
    # 记录解决方案
    issue_result = search_issue("auth success")
    if issue_result["count"] > 0:
        issue_id = issue_result["issues"][0]["id"]
        record_solution(
            issue_id=issue_id,
            title="前端JSON提取 + 后端输出抑制",
            description="""
解决方案包含两部分：
1. 后端(bridge.py): 在文件开头抑制stdout/stderr输出
2. 前端(workflowPanel.ts): 使用正则表达式提取JSON

关键代码：
- bridge.py: 使用os.dup2重定向文件描述符到/dev/null
- workflowPanel.ts: stdout.match(/\{[\s\S]*\}(?=\s*$)/) 提取最后的JSON对象
            """,
            code_snippet="""
# bridge.py 开头添加:
import os
_devnull_fd = os.open(os.devnull, os.O_WRONLY)
_saved_fd1 = os.dup(1)
_saved_fd2 = os.dup(2)
os.dup2(_devnull_fd, 1)
os.dup2(_devnull_fd, 2)

# workflowPanel.ts JSON提取:
const jsonMatch = stdout.match(/\{[\s\S]*\}(?=\s*$)/);
if (jsonMatch) {
    const result = JSON.parse(jsonMatch[0]);
}
            """,
            steps=[
                "在bridge.py文件开头添加输出抑制代码",
                "在workflowPanel.ts中使用正则提取JSON",
                "重新编译扩展: npm run compile",
                "重新打包: npx vsce package",
                "重新安装: code --install-extension *.vsix --force",
                "重新加载Cursor窗口"
            ],
            files_modified=[
                "extension/python/bridge.py",
                "extension/src/views/workflowPanel.ts"
            ]
        )
    
    # 记录代码模式
    record_pattern(
        name="stdout_pollution_fix",
        description="解决第三方库输出污染JSON响应的问题",
        problem_pattern="Unexpected token",
        solution_pattern="使用正则提取JSON: stdout.match(/\\{[\\s\\S]*\\}(?=\\s*$)/)",
        example_code='const jsonMatch = stdout.match(/\\{[\\s\\S]*\\}(?=\\s*$)/);',
        category="json_parsing"
    )
    
    return {"success": True, "message": "已知问题初始化完成"}


if __name__ == "__main__":
    # 初始化已知问题
    result = init_known_issues()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试快速debug
    debug_result = quick_debug("auth succe")
    print(json.dumps(debug_result, ensure_ascii=False, indent=2))
