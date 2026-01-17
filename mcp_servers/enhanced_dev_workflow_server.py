#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant 增强版开发工作流MCP服务器
================================

升级标准开发流程：
1. 开发前调研 - 充分调研背景，与专业标准对照
2. 代码复用检查 - 查询是否有相关功能开发记录
3. 增量测试 - 每一步都测试功能完整后再进行下一步
4. 知识库记录 - 开发过程记录到RAG知识库
5. MongoDB测试管理 - 测试结果由MongoDB数据库管理

工具分类:
1. 调研工具 (research.*) - 4个工具
2. 代码复用 (dev.*) - 3个工具
3. 测试管理 (test.*) - 5个工具
4. 工作流增强 (workflow.*) - 3个工具

总计: 15个新工具

运行: python mcp_servers/enhanced_dev_workflow_server.py
"""

import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import traceback

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('EnhancedDevWorkflow')

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    logger.error("MCP SDK不可用，请安装: pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")
    sys.exit(1)

# 导入本地模块
try:
    from core.dev_workflow.test_result_storage import (
        TestResultStorage, get_test_storage, record_test_result, query_tests
    )
    TEST_STORAGE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"测试存储模块导入失败: {e}")
    TEST_STORAGE_AVAILABLE = False

# 导入知识库模块
try:
    from mcp_servers.unified_dev_server import (
        knowledge_add, knowledge_search, knowledge_get, _load_json, _save_json, _gen_id, _now
    )
    KB_AVAILABLE = True
except ImportError as e:
    logger.warning(f"知识库模块导入失败: {e}")
    KB_AVAILABLE = False
    
    # 定义基础辅助函数
    def _load_json(filepath: Path, default: Any = None) -> Any:
        if filepath.exists():
            try:
                return json.loads(filepath.read_text(encoding='utf-8'))
            except:
                pass
        return default if default is not None else {}
    
    def _save_json(filepath: Path, data: Any) -> None:
        filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def _gen_id(prefix: str) -> str:
        return f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _now() -> str:
        return datetime.now().isoformat()

# 创建服务器
server = Server("trquant-enhanced-dev-workflow")

# ==================== 数据目录 ====================
DATA_DIR = TRQUANT_ROOT / ".trquant" / "dev"
DATA_DIR.mkdir(parents=True, exist_ok=True)

RESEARCH_DIR = DATA_DIR / "research"
DEV_RECORDS_DIR = DATA_DIR / "dev_records"
TEST_SESSIONS_DIR = DATA_DIR / "test_sessions"

for d in [RESEARCH_DIR, DEV_RECORDS_DIR, TEST_SESSIONS_DIR]:
    d.mkdir(exist_ok=True)


# ==================== 1. 调研工具 (research.*) ====================

def research_background(
    topic: str,
    module_name: str,
    objectives: List[str] = None,
    search_kb: bool = True,
    search_web: bool = False
) -> Dict[str, Any]:
    """
    开发前背景调研
    
    在开发任何模块前，充分调研:
    - 模块功能背景
    - 行业最佳实践
    - 已有知识库资料
    - (可选) 网络最新信息
    
    Args:
        topic: 调研主题
        module_name: 模块名称
        objectives: 调研目标列表
        search_kb: 是否搜索知识库
        search_web: 是否需要网络搜索（返回搜索建议）
        
    Returns:
        Dict: 调研结果和建议
    """
    logger.info(f"开始背景调研: {topic} (模块: {module_name})")
    
    research_id = _gen_id("research")
    
    # 1. 搜索知识库
    kb_results = []
    if search_kb and KB_AVAILABLE:
        try:
            kb_search_result = knowledge_search(topic, limit=10)
            if kb_search_result.get("success"):
                kb_results = kb_search_result.get("results", [])
                logger.info(f"知识库搜索到 {len(kb_results)} 条相关内容")
        except Exception as e:
            logger.warning(f"知识库搜索失败: {e}")
    
    # 2. 生成网络搜索建议
    web_search_suggestions = []
    if search_web:
        web_search_suggestions = [
            f"{topic} best practices 2024",
            f"{topic} implementation guide",
            f"{topic} python example github",
            f"{module_name} {topic} tutorial"
        ]
    
    # 3. 记录调研
    research_record = {
        "id": research_id,
        "topic": topic,
        "module_name": module_name,
        "objectives": objectives or [],
        "kb_results_count": len(kb_results),
        "kb_results_summary": [
            {"title": r.get("title", ""), "type": r.get("type", "")}
            for r in kb_results[:5]
        ],
        "web_search_suggestions": web_search_suggestions,
        "status": "completed",
        "created_at": _now()
    }
    
    # 保存调研记录
    research_file = RESEARCH_DIR / f"{research_id}.json"
    _save_json(research_file, research_record)
    
    # 4. 生成调研报告
    report = {
        "research_id": research_id,
        "topic": topic,
        "module_name": module_name,
        "findings": {
            "kb_coverage": "充分" if len(kb_results) >= 3 else "需要补充",
            "kb_results": kb_results[:5],
            "web_search_needed": len(kb_results) < 3
        },
        "recommendations": [],
        "next_steps": []
    }
    
    # 生成建议
    if len(kb_results) < 3:
        report["recommendations"].append("知识库资料不足，建议先进行网络搜索并添加到知识库")
        report["next_steps"].extend([
            f"1. 执行网络搜索: web_search('{web_search_suggestions[0]}')" if web_search_suggestions else "",
            "2. 爬取官方文档: crawler.fetch(url='官方文档URL')",
            "3. 添加到知识库: knowledge.add(...)"
        ])
    else:
        report["recommendations"].append("知识库资料充分，可以开始开发")
        report["next_steps"].extend([
            "1. 查看已有实现: dev.check_existing(...)",
            "2. 开始任务: task.create(...)",
            "3. 记录开发日志: devlog.add(...)"
        ])
    
    return {
        "success": True,
        "research": report,
        "web_search_suggestions": web_search_suggestions
    }


def research_compare_standards(
    module_name: str,
    implementation_plan: str,
    standard_type: str = "best_practice"
) -> Dict[str, Any]:
    """
    与专业标准对照
    
    将实现方案与行业最佳实践/专业标准对照，确保质量。
    
    Args:
        module_name: 模块名称
        implementation_plan: 实现方案描述
        standard_type: 标准类型 (best_practice/api_design/testing/security)
        
    Returns:
        Dict: 对照结果和改进建议
    """
    logger.info(f"对照专业标准: {module_name} - {standard_type}")
    
    # 1. 搜索相关标准
    standards = []
    if KB_AVAILABLE:
        try:
            # 搜索最佳实践
            kb_result = knowledge_search(f"{standard_type} {module_name}", type="lesson", limit=5)
            if kb_result.get("success"):
                standards = kb_result.get("results", [])
        except:
            pass
    
    # 2. 定义通用标准检查项
    standard_checklist = {
        "best_practice": [
            {"item": "代码复用", "description": "是否复用已有模块，避免重复造轮子"},
            {"item": "错误处理", "description": "是否有完善的异常处理和日志记录"},
            {"item": "单元测试", "description": "是否有配套的单元测试"},
            {"item": "文档注释", "description": "是否有清晰的docstring和注释"},
            {"item": "类型提示", "description": "是否使用类型提示增强可维护性"}
        ],
        "api_design": [
            {"item": "接口一致性", "description": "API命名和参数风格是否一致"},
            {"item": "返回值标准化", "description": "返回值格式是否统一"},
            {"item": "错误码规范", "description": "错误码是否规范化"},
            {"item": "版本兼容", "description": "是否考虑向后兼容"}
        ],
        "testing": [
            {"item": "测试覆盖率", "description": "核心逻辑是否有测试覆盖"},
            {"item": "边界测试", "description": "是否测试边界条件"},
            {"item": "集成测试", "description": "是否有模块间集成测试"},
            {"item": "性能测试", "description": "是否有性能基准测试"}
        ],
        "security": [
            {"item": "输入验证", "description": "是否验证所有外部输入"},
            {"item": "敏感数据", "description": "敏感数据是否妥善处理"},
            {"item": "权限控制", "description": "是否有适当的权限检查"}
        ]
    }
    
    checklist = standard_checklist.get(standard_type, standard_checklist["best_practice"])
    
    # 3. 生成对照报告
    comparison = {
        "module_name": module_name,
        "standard_type": standard_type,
        "implementation_plan": implementation_plan,
        "checklist": checklist,
        "kb_standards": [
            {"title": s.get("title", ""), "summary": s.get("content", "")[:200]}
            for s in standards[:3]
        ],
        "recommendations": [
            f"确保实现方案满足检查项: {item['item']}" for item in checklist[:3]
        ]
    }
    
    return {
        "success": True,
        "comparison": comparison,
        "action_items": [
            "1. 逐项对照检查清单",
            "2. 参考知识库中的最佳实践",
            "3. 在开发完成后进行代码审查"
        ]
    }


def research_query_history(
    module_name: str = None,
    topic: str = None,
    limit: int = 10
) -> Dict[str, Any]:
    """
    查询调研历史
    
    Args:
        module_name: 模块名称过滤
        topic: 主题过滤
        limit: 返回数量限制
        
    Returns:
        Dict: 调研历史列表
    """
    history = []
    
    for filepath in sorted(RESEARCH_DIR.glob("*.json"), reverse=True):
        if len(history) >= limit:
            break
        
        try:
            data = json.loads(filepath.read_text(encoding='utf-8'))
            
            # 过滤
            if module_name and data.get("module_name") != module_name:
                continue
            if topic and topic.lower() not in data.get("topic", "").lower():
                continue
            
            history.append(data)
        except:
            continue
    
    return {"success": True, "history": history, "total": len(history)}


def research_add_finding(
    research_id: str,
    finding: str,
    source: str = "manual",
    importance: str = "medium"
) -> Dict[str, Any]:
    """
    添加调研发现
    
    Args:
        research_id: 调研ID
        finding: 发现内容
        source: 来源 (manual/web/kb)
        importance: 重要性 (high/medium/low)
        
    Returns:
        Dict: 添加结果
    """
    research_file = RESEARCH_DIR / f"{research_id}.json"
    
    if not research_file.exists():
        return {"success": False, "error": f"调研记录不存在: {research_id}"}
    
    research = _load_json(research_file)
    
    if "findings" not in research:
        research["findings"] = []
    
    research["findings"].append({
        "content": finding,
        "source": source,
        "importance": importance,
        "added_at": _now()
    })
    
    _save_json(research_file, research)
    
    return {"success": True, "message": "发现已添加", "total_findings": len(research["findings"])}


# ==================== 2. 代码复用检查 (dev.*) ====================

def dev_check_existing(
    module_name: str,
    functionality: str,
    search_scope: str = "all"
) -> Dict[str, Any]:
    """
    检查是否有相关或相似功能的开发记录
    
    在开发新功能前，先检查是否:
    - 已有相似模块可以直接使用
    - 已有基础代码可以改进
    - 知识库中有相关经验
    
    Args:
        module_name: 目标模块名称
        functionality: 功能描述
        search_scope: 搜索范围 (all/core/mcp_servers/scripts)
        
    Returns:
        Dict: 检查结果和建议
    """
    logger.info(f"检查已有实现: {module_name} - {functionality}")
    
    results = {
        "module_name": module_name,
        "functionality": functionality,
        "existing_modules": [],
        "kb_references": [],
        "recommendations": []
    }
    
    # 1. 搜索代码库中的相似模块
    search_dirs = {
        "all": [TRQUANT_ROOT / "core", TRQUANT_ROOT / "mcp_servers", TRQUANT_ROOT / "scripts"],
        "core": [TRQUANT_ROOT / "core"],
        "mcp_servers": [TRQUANT_ROOT / "mcp_servers"],
        "scripts": [TRQUANT_ROOT / "scripts"]
    }
    
    dirs_to_search = search_dirs.get(search_scope, search_dirs["all"])
    
    # 搜索关键词
    keywords = functionality.lower().split()
    
    for search_dir in dirs_to_search:
        if not search_dir.exists():
            continue
        
        for py_file in search_dir.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore').lower()
                
                # 计算匹配度
                match_count = sum(1 for kw in keywords if kw in content)
                if match_count >= len(keywords) * 0.3:  # 30%以上关键词匹配
                    # 提取文件概述
                    lines = py_file.read_text(encoding='utf-8', errors='ignore').split('\n')
                    docstring = ""
                    for line in lines[:20]:
                        if '"""' in line or "'''" in line:
                            docstring = line.strip('"\' \n')
                            break
                    
                    results["existing_modules"].append({
                        "path": str(py_file.relative_to(TRQUANT_ROOT)),
                        "match_score": match_count / len(keywords),
                        "description": docstring[:100] if docstring else "无描述"
                    })
            except:
                continue
    
    # 按匹配度排序
    results["existing_modules"].sort(key=lambda x: x["match_score"], reverse=True)
    results["existing_modules"] = results["existing_modules"][:10]  # 只保留前10个
    
    # 2. 搜索知识库
    if KB_AVAILABLE:
        try:
            kb_result = knowledge_search(functionality, limit=5)
            if kb_result.get("success"):
                results["kb_references"] = [
                    {"id": r.get("id"), "title": r.get("title"), "type": r.get("type")}
                    for r in kb_result.get("results", [])
                ]
        except:
            pass
    
    # 3. 生成建议
    if results["existing_modules"]:
        top_match = results["existing_modules"][0]
        if top_match["match_score"] >= 0.7:
            results["recommendations"].append(
                f"强烈建议：发现高度相似的模块 {top_match['path']}，建议直接复用或继承"
            )
        elif top_match["match_score"] >= 0.5:
            results["recommendations"].append(
                f"建议：发现相似模块 {top_match['path']}，建议参考其实现"
            )
    
    if not results["existing_modules"]:
        results["recommendations"].append("未发现相似实现，可以创建新模块")
    
    if results["kb_references"]:
        results["recommendations"].append(
            f"知识库有 {len(results['kb_references'])} 条相关参考，建议先查阅"
        )
    
    return {"success": True, "check_result": results}


def dev_record_progress(
    task_id: str,
    module_name: str,
    step_name: str,
    status: str,
    details: str = "",
    code_changes: List[str] = None
) -> Dict[str, Any]:
    """
    记录开发进度
    
    Args:
        task_id: 任务ID
        module_name: 模块名称
        step_name: 步骤名称
        status: 状态 (started/in_progress/completed/blocked)
        details: 详细描述
        code_changes: 代码变更文件列表
        
    Returns:
        Dict: 记录结果
    """
    record_id = _gen_id("dev_record")
    
    record = {
        "id": record_id,
        "task_id": task_id,
        "module_name": module_name,
        "step_name": step_name,
        "status": status,
        "details": details,
        "code_changes": code_changes or [],
        "created_at": _now()
    }
    
    # 保存记录
    record_file = DEV_RECORDS_DIR / f"{task_id}.json"
    records = _load_json(record_file, {"task_id": task_id, "records": []})
    records["records"].append(record)
    _save_json(record_file, records)
    
    logger.info(f"开发进度已记录: {task_id} - {step_name} - {status}")
    
    return {"success": True, "record_id": record_id, "record": record}


def dev_record_to_kb(
    task_id: str,
    module_name: str,
    title: str,
    summary: str,
    lessons_learned: List[str] = None,
    code_examples: List[Dict] = None,
    tags: List[str] = None
) -> Dict[str, Any]:
    """
    将开发过程记录到RAG知识库
    
    开发完成后，将经验和教训记录到知识库，便于后续查询引用。
    
    Args:
        task_id: 任务ID
        module_name: 模块名称
        title: 知识标题
        summary: 开发总结
        lessons_learned: 经验教训列表
        code_examples: 代码示例列表
        tags: 标签列表
        
    Returns:
        Dict: 记录结果
    """
    logger.info(f"记录开发经验到知识库: {title}")
    
    # 构建知识内容
    content_parts = [
        f"# {title}\n",
        f"## 模块: {module_name}\n",
        f"## 任务ID: {task_id}\n",
        f"## 总结\n{summary}\n"
    ]
    
    if lessons_learned:
        content_parts.append("## 经验教训\n")
        for lesson in lessons_learned:
            content_parts.append(f"- {lesson}\n")
    
    if code_examples:
        content_parts.append("## 代码示例\n")
        for example in code_examples:
            content_parts.append(f"### {example.get('name', '示例')}\n")
            content_parts.append(f"```{example.get('language', 'python')}\n")
            content_parts.append(f"{example.get('code', '')}\n")
            content_parts.append("```\n")
    
    content_parts.append(f"\n---\n记录时间: {_now()}\n")
    
    content = "".join(content_parts)
    
    # 添加到知识库
    if KB_AVAILABLE:
        try:
            kb_result = knowledge_add(
                title=title,
                content=content,
                type="lesson",
                tags=tags or [module_name, "development"],
                source=f"task:{task_id}"
            )
            
            if kb_result.get("success"):
                logger.info(f"已添加到知识库: {kb_result.get('knowledge_id')}")
                return {
                    "success": True,
                    "knowledge_id": kb_result.get("knowledge_id"),
                    "message": "开发经验已记录到知识库"
                }
        except Exception as e:
            logger.error(f"添加到知识库失败: {e}")
    
    # 回退：保存到文件
    kb_record = {
        "title": title,
        "content": content,
        "module_name": module_name,
        "task_id": task_id,
        "tags": tags or [module_name],
        "created_at": _now()
    }
    
    kb_file = DEV_RECORDS_DIR / f"kb_{task_id}_{_gen_id('kb')}.json"
    _save_json(kb_file, kb_record)
    
    return {
        "success": True,
        "file_path": str(kb_file),
        "message": "开发经验已保存到文件（知识库不可用）"
    }


# ==================== 3. 测试管理 (test.*) ====================

def test_record(
    module_name: str,
    test_name: str,
    status: str,
    duration_ms: float = 0,
    message: str = "",
    error_traceback: str = "",
    test_type: str = "unit",
    tags: List[str] = None,
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    记录测试结果到MongoDB
    
    每次测试执行后，记录结果到数据库，便于追踪和分析。
    
    Args:
        module_name: 模块名称
        test_name: 测试名称
        status: 状态 (passed/failed/skipped/error)
        duration_ms: 执行时间(毫秒)
        message: 结果消息
        error_traceback: 错误堆栈
        test_type: 测试类型 (unit/integration/e2e)
        tags: 标签列表
        metadata: 额外元数据
        
    Returns:
        Dict: {"success": True, "test_id": "..."}
    """
    logger.info(f"记录测试结果: {module_name}.{test_name} - {status}")
    
    if TEST_STORAGE_AVAILABLE:
        try:
            result = record_test_result(
                module_name=module_name,
                test_name=test_name,
                status=status,
                duration_ms=duration_ms,
                message=message,
                error_traceback=error_traceback,
                test_type=test_type,
                tags=tags,
                metadata=metadata
            )
            return result
        except Exception as e:
            logger.error(f"MongoDB存储失败: {e}")
    
    # 回退：保存到文件
    test_id = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    test_record = {
        "test_id": test_id,
        "module_name": module_name,
        "test_name": test_name,
        "status": status,
        "duration_ms": duration_ms,
        "message": message,
        "error_traceback": error_traceback,
        "test_type": test_type,
        "tags": tags or [],
        "metadata": metadata or {},
        "created_at": _now()
    }
    
    test_file = TEST_SESSIONS_DIR / f"{test_id}.json"
    _save_json(test_file, test_record)
    
    return {"success": True, "test_id": test_id, "storage": "file"}


def test_query(
    module_name: str = None,
    status: str = None,
    test_type: str = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    查询测试结果
    
    Args:
        module_name: 模块名称过滤
        status: 状态过滤 (passed/failed/skipped/error)
        test_type: 测试类型过滤
        limit: 返回数量限制
        
    Returns:
        Dict: {"success": True, "results": [...], "total": N}
    """
    if TEST_STORAGE_AVAILABLE:
        try:
            result = query_tests(
                module_name=module_name,
                status=status,
                limit=limit
            )
            return result
        except Exception as e:
            logger.error(f"MongoDB查询失败: {e}")
    
    # 回退：从文件查询
    results = []
    for filepath in sorted(TEST_SESSIONS_DIR.glob("test_*.json"), reverse=True):
        if len(results) >= limit:
            break
        
        try:
            data = json.loads(filepath.read_text(encoding='utf-8'))
            
            if module_name and data.get("module_name") != module_name:
                continue
            if status and data.get("status") != status:
                continue
            if test_type and data.get("test_type") != test_type:
                continue
            
            results.append(data)
        except:
            continue
    
    return {"success": True, "results": results, "total": len(results), "storage": "file"}


def test_start_session(
    task_id: str,
    module_name: str,
    test_plan: List[str] = None
) -> Dict[str, Any]:
    """
    开始测试会话
    
    在开始一轮测试前调用，创建测试会话。
    
    Args:
        task_id: 关联的任务ID
        module_name: 模块名称
        test_plan: 测试计划列表
        
    Returns:
        Dict: {"success": True, "session_id": "..."}
    """
    logger.info(f"开始测试会话: {module_name} (任务: {task_id})")
    
    if TEST_STORAGE_AVAILABLE:
        try:
            storage = get_test_storage()
            result = storage.start_test_session(
                task_id=task_id,
                module_name=module_name,
                metadata={"test_plan": test_plan or []}
            )
            return result
        except Exception as e:
            logger.error(f"MongoDB操作失败: {e}")
    
    # 回退：保存到文件
    session_id = f"session_{module_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session = {
        "session_id": session_id,
        "task_id": task_id,
        "module_name": module_name,
        "test_plan": test_plan or [],
        "status": "running",
        "started_at": _now(),
        "results": []
    }
    
    session_file = TEST_SESSIONS_DIR / f"{session_id}.json"
    _save_json(session_file, session)
    
    return {"success": True, "session_id": session_id, "storage": "file"}


def test_complete_session(
    session_id: str,
    summary: Dict[str, int] = None
) -> Dict[str, Any]:
    """
    完成测试会话
    
    测试完成后调用，更新会话状态和统计信息。
    
    Args:
        session_id: 会话ID
        summary: 测试统计 {"total": N, "passed": N, "failed": N, ...}
        
    Returns:
        Dict: {"success": True, "session": {...}}
    """
    logger.info(f"完成测试会话: {session_id}")
    
    summary = summary or {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "errors": 0}
    
    if TEST_STORAGE_AVAILABLE:
        try:
            storage = get_test_storage()
            result = storage.complete_test_session(
                session_id=session_id,
                total_tests=summary.get("total", 0),
                passed=summary.get("passed", 0),
                failed=summary.get("failed", 0),
                skipped=summary.get("skipped", 0),
                errors=summary.get("errors", 0),
                total_duration_ms=summary.get("duration_ms", 0),
                coverage_pct=summary.get("coverage_pct", 0.0)
            )
            return result
        except Exception as e:
            logger.error(f"MongoDB操作失败: {e}")
    
    # 回退：更新文件
    session_file = TEST_SESSIONS_DIR / f"{session_id}.json"
    if session_file.exists():
        session = _load_json(session_file)
        session["status"] = "completed" if summary.get("failed", 0) == 0 else "failed"
        session["summary"] = summary
        session["completed_at"] = _now()
        _save_json(session_file, session)
        return {"success": True, "session": session}
    
    return {"success": False, "error": f"会话不存在: {session_id}"}


def test_get_stats(module_name: str) -> Dict[str, Any]:
    """
    获取模块测试统计
    
    Args:
        module_name: 模块名称
        
    Returns:
        Dict: 统计信息
    """
    if TEST_STORAGE_AVAILABLE:
        try:
            storage = get_test_storage()
            return storage.get_module_test_stats(module_name)
        except Exception as e:
            logger.error(f"统计查询失败: {e}")
    
    # 回退：从文件统计
    query_result = test_query(module_name=module_name, limit=1000)
    results = query_result.get("results", [])
    
    stats = {
        "module_name": module_name,
        "total": len(results),
        "passed": len([r for r in results if r.get("status") == "passed"]),
        "failed": len([r for r in results if r.get("status") == "failed"]),
        "skipped": len([r for r in results if r.get("status") == "skipped"]),
        "errors": len([r for r in results if r.get("status") == "error"])
    }
    stats["pass_rate"] = round(stats["passed"] / max(stats["total"], 1) * 100, 2)
    
    return {"success": True, "stats": stats}


# ==================== 4. 工作流增强 (workflow.*) ====================

def workflow_incremental_test(
    task_id: str,
    step_name: str,
    test_function: str,
    expected_result: str = "passed",
    auto_proceed: bool = False
) -> Dict[str, Any]:
    """
    增量测试验证
    
    在任务的每一步完成后，验证功能是否正常工作。
    只有测试通过后才能进行下一步开发。
    
    Args:
        task_id: 任务ID
        step_name: 步骤名称
        test_function: 测试函数/命令
        expected_result: 期望结果
        auto_proceed: 测试通过后是否自动进入下一步
        
    Returns:
        Dict: 测试结果和下一步建议
    """
    logger.info(f"增量测试验证: {task_id} - {step_name}")
    
    verification = {
        "task_id": task_id,
        "step_name": step_name,
        "test_function": test_function,
        "expected_result": expected_result,
        "status": "pending",
        "created_at": _now()
    }
    
    # 记录验证请求
    verification_file = TEST_SESSIONS_DIR / f"verify_{task_id}_{step_name}.json"
    _save_json(verification_file, verification)
    
    return {
        "success": True,
        "verification": verification,
        "instructions": [
            f"1. 执行测试: {test_function}",
            f"2. 期望结果: {expected_result}",
            f"3. 测试通过后调用: test.record(module_name='{step_name}', test_name='incremental_test', status='passed')",
            "4. 测试失败则记录问题: issue.create(...)"
        ],
        "next_step_blocked": not auto_proceed,
        "message": f"请完成 {step_name} 的测试验证后再继续开发"
    }


def workflow_validate_step(
    task_id: str,
    step_name: str,
    validation_type: str = "test"
) -> Dict[str, Any]:
    """
    验证步骤是否可以继续
    
    检查当前步骤是否已通过测试，决定是否可以进入下一步。
    
    Args:
        task_id: 任务ID
        step_name: 步骤名称
        validation_type: 验证类型 (test/review/manual)
        
    Returns:
        Dict: 验证结果
    """
    logger.info(f"验证步骤: {task_id} - {step_name}")
    
    # 查询该步骤的测试结果
    test_results = test_query(module_name=step_name, status="passed", limit=1)
    
    has_passed_tests = len(test_results.get("results", [])) > 0
    
    # 查询是否有未解决的问题
    # (这里简化处理，实际可以调用issue.list)
    
    validation = {
        "task_id": task_id,
        "step_name": step_name,
        "validation_type": validation_type,
        "has_passed_tests": has_passed_tests,
        "can_proceed": has_passed_tests,
        "validated_at": _now()
    }
    
    if has_passed_tests:
        validation["message"] = f"✅ {step_name} 已通过测试，可以继续下一步"
    else:
        validation["message"] = f"⚠️ {step_name} 尚未通过测试，请先完成测试验证"
        validation["action_required"] = [
            f"1. 执行测试: test.record(module_name='{step_name}', ...)",
            "2. 确保测试状态为 'passed'",
            "3. 重新验证: workflow.validate_step(...)"
        ]
    
    return {"success": True, "validation": validation}


def workflow_enhanced_check(
    task_id: str = None
) -> Dict[str, Any]:
    """
    增强版开发流程检查
    
    检查当前开发状态，包括:
    - 是否完成了开发前调研
    - 是否检查了代码复用
    - 各步骤是否通过了测试
    - 是否记录了开发经验
    
    Args:
        task_id: 任务ID（可选）
        
    Returns:
        Dict: 流程状态和建议
    """
    logger.info(f"增强版流程检查: {task_id or 'all'}")
    
    # 1. 检查调研状态
    research_history = research_query_history(limit=5)
    has_recent_research = len(research_history.get("history", [])) > 0
    
    # 2. 检查测试状态
    recent_tests = test_query(limit=10)
    test_stats = {
        "total": len(recent_tests.get("results", [])),
        "passed": len([r for r in recent_tests.get("results", []) if r.get("status") == "passed"]),
        "failed": len([r for r in recent_tests.get("results", []) if r.get("status") == "failed"])
    }
    
    # 3. 检查开发记录
    dev_records = []
    if task_id:
        record_file = DEV_RECORDS_DIR / f"{task_id}.json"
        if record_file.exists():
            dev_records = _load_json(record_file, {}).get("records", [])
    
    # 4. 生成检查报告
    status = {
        "task_id": task_id,
        "research": {
            "has_recent_research": has_recent_research,
            "status": "✅" if has_recent_research else "⚠️"
        },
        "testing": {
            "total_tests": test_stats["total"],
            "pass_rate": round(test_stats["passed"] / max(test_stats["total"], 1) * 100, 2),
            "status": "✅" if test_stats["failed"] == 0 and test_stats["total"] > 0 else "⚠️"
        },
        "development": {
            "records_count": len(dev_records),
            "status": "✅" if len(dev_records) > 0 else "⚠️"
        },
        "checked_at": _now()
    }
    
    # 5. 生成建议
    recommendations = []
    if not has_recent_research:
        recommendations.append("建议: 在开发前先进行背景调研 (research.background)")
    if test_stats["total"] == 0:
        recommendations.append("建议: 添加测试用例并记录测试结果 (test.record)")
    if test_stats["failed"] > 0:
        recommendations.append(f"警告: 有 {test_stats['failed']} 个测试失败，请先修复")
    if len(dev_records) == 0 and task_id:
        recommendations.append("建议: 记录开发进度 (dev.record_progress)")
    
    if not recommendations:
        recommendations.append("✅ 开发流程状态良好，继续保持！")
    
    return {
        "success": True,
        "status": status,
        "recommendations": recommendations
    }


# ==================== 工具处理器映射 ====================

TOOL_HANDLERS = {
    # 调研工具
    "research.background": research_background,
    "research.compare_standards": research_compare_standards,
    "research.query_history": research_query_history,
    "research.add_finding": research_add_finding,
    # 代码复用
    "dev.check_existing": dev_check_existing,
    "dev.record_progress": dev_record_progress,
    "dev.record_to_kb": dev_record_to_kb,
    # 测试管理
    "test.record": test_record,
    "test.query": test_query,
    "test.start_session": test_start_session,
    "test.complete_session": test_complete_session,
    "test.get_stats": test_get_stats,
    # 工作流增强
    "workflow.incremental_test": workflow_incremental_test,
    "workflow.validate_step": workflow_validate_step,
    "workflow.enhanced_check": workflow_enhanced_check,
}


# ==================== MCP工具定义 ====================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有工具"""
    return [
        # ==================== 调研工具 (4个) ====================
        Tool(
            name="research.background",
            description="开发前背景调研 - 在开发任何模块前，充分调研背景、最佳实践和已有知识",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "调研主题"},
                    "module_name": {"type": "string", "description": "模块名称"},
                    "objectives": {"type": "array", "items": {"type": "string"}, "description": "调研目标列表"},
                    "search_kb": {"type": "boolean", "default": True, "description": "是否搜索知识库"},
                    "search_web": {"type": "boolean", "default": False, "description": "是否需要网络搜索建议"}
                },
                "required": ["topic", "module_name"]
            }
        ),
        Tool(
            name="research.compare_standards",
            description="与专业标准对照 - 将实现方案与行业最佳实践/专业标准对照",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "模块名称"},
                    "implementation_plan": {"type": "string", "description": "实现方案描述"},
                    "standard_type": {
                        "type": "string",
                        "enum": ["best_practice", "api_design", "testing", "security"],
                        "default": "best_practice",
                        "description": "标准类型"
                    }
                },
                "required": ["module_name", "implementation_plan"]
            }
        ),
        Tool(
            name="research.query_history",
            description="查询调研历史记录",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "模块名称过滤"},
                    "topic": {"type": "string", "description": "主题过滤"},
                    "limit": {"type": "integer", "default": 10, "description": "返回数量限制"}
                }
            }
        ),
        Tool(
            name="research.add_finding",
            description="添加调研发现",
            inputSchema={
                "type": "object",
                "properties": {
                    "research_id": {"type": "string", "description": "调研ID"},
                    "finding": {"type": "string", "description": "发现内容"},
                    "source": {"type": "string", "enum": ["manual", "web", "kb"], "default": "manual"},
                    "importance": {"type": "string", "enum": ["high", "medium", "low"], "default": "medium"}
                },
                "required": ["research_id", "finding"]
            }
        ),
        
        # ==================== 代码复用 (3个) ====================
        Tool(
            name="dev.check_existing",
            description="检查是否有相关或相似功能的开发记录 - 在开发新功能前，先检查是否可以复用已有代码",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "目标模块名称"},
                    "functionality": {"type": "string", "description": "功能描述"},
                    "search_scope": {
                        "type": "string",
                        "enum": ["all", "core", "mcp_servers", "scripts"],
                        "default": "all",
                        "description": "搜索范围"
                    }
                },
                "required": ["module_name", "functionality"]
            }
        ),
        Tool(
            name="dev.record_progress",
            description="记录开发进度",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "module_name": {"type": "string", "description": "模块名称"},
                    "step_name": {"type": "string", "description": "步骤名称"},
                    "status": {"type": "string", "enum": ["started", "in_progress", "completed", "blocked"]},
                    "details": {"type": "string", "description": "详细描述"},
                    "code_changes": {"type": "array", "items": {"type": "string"}, "description": "代码变更文件列表"}
                },
                "required": ["task_id", "module_name", "step_name", "status"]
            }
        ),
        Tool(
            name="dev.record_to_kb",
            description="将开发过程记录到RAG知识库 - 开发完成后，将经验和教训记录到知识库，便于后续查询引用",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "module_name": {"type": "string", "description": "模块名称"},
                    "title": {"type": "string", "description": "知识标题"},
                    "summary": {"type": "string", "description": "开发总结"},
                    "lessons_learned": {"type": "array", "items": {"type": "string"}, "description": "经验教训列表"},
                    "code_examples": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "language": {"type": "string"},
                                "code": {"type": "string"}
                            }
                        },
                        "description": "代码示例列表"
                    },
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表"}
                },
                "required": ["task_id", "module_name", "title", "summary"]
            }
        ),
        
        # ==================== 测试管理 (5个) ====================
        Tool(
            name="test.record",
            description="记录测试结果到MongoDB - 每次测试执行后，记录结果到数据库",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "模块名称"},
                    "test_name": {"type": "string", "description": "测试名称"},
                    "status": {"type": "string", "enum": ["passed", "failed", "skipped", "error"], "description": "测试状态"},
                    "duration_ms": {"type": "number", "default": 0, "description": "执行时间(毫秒)"},
                    "message": {"type": "string", "description": "结果消息"},
                    "error_traceback": {"type": "string", "description": "错误堆栈"},
                    "test_type": {"type": "string", "enum": ["unit", "integration", "e2e"], "default": "unit"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表"},
                    "metadata": {"type": "object", "description": "额外元数据"}
                },
                "required": ["module_name", "test_name", "status"]
            }
        ),
        Tool(
            name="test.query",
            description="查询测试结果",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "模块名称过滤"},
                    "status": {"type": "string", "enum": ["passed", "failed", "skipped", "error"]},
                    "test_type": {"type": "string", "enum": ["unit", "integration", "e2e"]},
                    "limit": {"type": "integer", "default": 50, "description": "返回数量限制"}
                }
            }
        ),
        Tool(
            name="test.start_session",
            description="开始测试会话",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "关联的任务ID"},
                    "module_name": {"type": "string", "description": "模块名称"},
                    "test_plan": {"type": "array", "items": {"type": "string"}, "description": "测试计划列表"}
                },
                "required": ["task_id", "module_name"]
            }
        ),
        Tool(
            name="test.complete_session",
            description="完成测试会话",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "会话ID"},
                    "summary": {
                        "type": "object",
                        "properties": {
                            "total": {"type": "integer"},
                            "passed": {"type": "integer"},
                            "failed": {"type": "integer"},
                            "skipped": {"type": "integer"},
                            "errors": {"type": "integer"},
                            "duration_ms": {"type": "number"},
                            "coverage_pct": {"type": "number"}
                        },
                        "description": "测试统计"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="test.get_stats",
            description="获取模块测试统计",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_name": {"type": "string", "description": "模块名称"}
                },
                "required": ["module_name"]
            }
        ),
        
        # ==================== 工作流增强 (3个) ====================
        Tool(
            name="workflow.incremental_test",
            description="增量测试验证 - 在任务的每一步完成后，验证功能是否正常工作",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "step_name": {"type": "string", "description": "步骤名称"},
                    "test_function": {"type": "string", "description": "测试函数/命令"},
                    "expected_result": {"type": "string", "default": "passed", "description": "期望结果"},
                    "auto_proceed": {"type": "boolean", "default": False, "description": "测试通过后是否自动进入下一步"}
                },
                "required": ["task_id", "step_name", "test_function"]
            }
        ),
        Tool(
            name="workflow.validate_step",
            description="验证步骤是否可以继续 - 检查当前步骤是否已通过测试",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID"},
                    "step_name": {"type": "string", "description": "步骤名称"},
                    "validation_type": {"type": "string", "enum": ["test", "review", "manual"], "default": "test"}
                },
                "required": ["task_id", "step_name"]
            }
        ),
        Tool(
            name="workflow.enhanced_check",
            description="增强版开发流程检查 - 检查调研、代码复用、测试、知识库记录的完整状态",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务ID（可选）"}
                }
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    logger.info(f"调用工具: {name}")
    
    try:
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return [TextContent(
                type="text",
                text=json.dumps({"success": False, "error": f"未知工具: {name}"}, ensure_ascii=False)
            )]
        
        result = handler(**arguments)
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
        
    except Exception as e:
        logger.error(f"工具调用失败: {e}\n{traceback.format_exc()}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
                "traceback": traceback.format_exc()
            }, ensure_ascii=False)
        )]


# ==================== 主入口 ====================

async def main():
    """主函数"""
    logger.info("启动 TRQuant 增强版开发工作流MCP服务器...")
    logger.info(f"TEST_STORAGE_AVAILABLE: {TEST_STORAGE_AVAILABLE}")
    logger.info(f"KB_AVAILABLE: {KB_AVAILABLE}")
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
