#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
轩辕剑灵开发助手MCP服务器
========================

提升prompt engineering效率的开发助手

功能模块:
    1. 提示词规范化和管理 - xuanyuan.prompt.*
    2. 错误处理和调试辅助 - xuanyuan.error.*, xuanyuan.debug.*
    3. Linux命令助手 - xuanyuan.command.*
    4. 记忆辅助功能 - xuanyuan.memory.*

运行方式:
    python mcp_servers/xuanyuan_server.py

设计原则:
    - 所有功能通过MCP工具暴露
    - Cursor Chat直接调用，无需扩展
    - 数据存储在data/xuanyuan/目录
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

logger = logging.getLogger('XuanyuanServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
    logger.info("轩辕剑灵MCP服务器已加载")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用: {e}")
    sys.exit(1)

# 创建服务器
server = Server("xuanyuan")

# 数据目录
DATA_DIR = TRQUANT_ROOT / "data" / "xuanyuan"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 子目录
PROMPTS_DIR = DATA_DIR / "prompts"
PROMPTS_DIR.mkdir(exist_ok=True)
ERRORS_DIR = DATA_DIR / "errors"
ERRORS_DIR.mkdir(exist_ok=True)
COMMANDS_DIR = DATA_DIR / "commands"
COMMANDS_DIR.mkdir(exist_ok=True)
MEMORY_DIR = DATA_DIR / "memory"
MEMORY_DIR.mkdir(exist_ok=True)

# ==================== 数据管理工具函数 ====================

def _load_json_file(file_path: Path, default: Any = None) -> Any:
    """加载JSON文件"""
    if file_path.exists():
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"加载JSON失败 {file_path}: {e}")
    return default if default is not None else {}

def _save_json_file(file_path: Path, data: Any) -> None:
    """保存JSON文件"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )

def _generate_id(prefix: str = "id") -> str:
    """生成唯一ID"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    import hashlib
    hash_part = hashlib.md5(f"{timestamp}{prefix}".encode()).hexdigest()[:6]
    return f"{prefix}_{timestamp}_{hash_part}"

# ==================== 工具定义 ====================

TOOLS = [
    # 提示词管理工具
    Tool(
        name="xuanyuan.prompt.templates.list",
        description="列出所有提示词模板",
        inputSchema={
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "分类筛选（可选）: system/code_generation/error_handling/etc"
                }
            }
        }
    ),
    Tool(
        name="xuanyuan.prompt.templates.get",
        description="获取提示词模板详情",
        inputSchema={
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "description": "模板ID"}
            },
            "required": ["template_id"]
        }
    ),
    Tool(
        name="xuanyuan.prompt.templates.create",
        description="创建新的提示词模板",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "模板名称"},
                "content": {"type": "string", "description": "模板内容"},
                "category": {"type": "string", "description": "分类"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表"},
                "description": {"type": "string", "description": "模板描述"}
            },
            "required": ["name", "content"]
        }
    ),
    Tool(
        name="xuanyuan.prompt.templates.update",
        description="更新提示词模板",
        inputSchema={
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "description": "模板ID"},
                "name": {"type": "string", "description": "模板名称（可选）"},
                "content": {"type": "string", "description": "模板内容（可选）"},
                "category": {"type": "string", "description": "分类（可选）"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表（可选）"}
            },
            "required": ["template_id"]
        }
    ),
    Tool(
        name="xuanyuan.prompt.templates.evaluate",
        description="评估提示词效果",
        inputSchema={
            "type": "object",
            "properties": {
                "template_id": {"type": "string", "description": "模板ID"},
                "result_quality": {"type": "number", "description": "结果质量评分(1-5)"},
                "feedback": {"type": "string", "description": "反馈意见"}
            },
            "required": ["template_id", "result_quality"]
        }
    ),
    Tool(
        name="xuanyuan.prompt.best_practices.search",
        description="搜索提示词最佳实践",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "limit": {"type": "integer", "description": "返回结果数量限制", "default": 10}
            },
            "required": ["query"]
        }
    ),
        Tool(
            name="xuanyuan.prompt.optimize",
            description="根据开发任务需求智能生成或优化prompt，遵循Cursor方法论，生成包含目标、约束、范围、验收标准的结构化prompt",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "开发任务描述，描述要实现什么功能或解决什么问题"
                    },
                    "context": {
                        "type": "string",
                        "description": "上下文信息（可选）：相关文件、模块、技术栈等"
                    },
                    "prompt_type": {
                        "type": "string",
                        "description": "Prompt类型：feature_development|refactoring|bug_fix|code_review|testing|documentation",
                        "default": "feature_development"
                    },
                    "include_template": {
                        "type": "boolean",
                        "description": "是否参考已有模板",
                        "default": True
                    }
                },
                "required": ["task_description"]
            }
        ),
        Tool(
            name="xuanyuan.prompt.extract_from_logs",
            description="从开发记录中提取典型的prompt",
        inputSchema={
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "数据源: prompts|cursor_rules|devlog|all",
                    "default": "all"
                },
                "limit": {
                    "type": "integer",
                    "description": "最大提取数量",
                    "default": 20
                },
                "min_length": {
                    "type": "integer",
                    "description": "最小prompt长度（字符）",
                    "default": 30
                },
                "pattern": {
                    "type": "string",
                    "description": "提取模式（可选）"
                }
            }
        }
    ),
    Tool(
        name="xuanyuan.prompt.optimize",
        description="根据开发任务需求智能生成或优化prompt，遵循Cursor方法论，生成包含目标、约束、范围、验收标准的结构化prompt",
        inputSchema={
            "type": "object",
            "properties": {
                "task_description": {
                    "type": "string",
                    "description": "开发任务描述，描述要实现什么功能或解决什么问题"
                },
                "context": {
                    "type": "string",
                    "description": "上下文信息（可选）：相关文件、模块、技术栈等"
                },
                "prompt_type": {
                    "type": "string",
                    "description": "Prompt类型：feature_development|refactoring|bug_fix|code_review|testing|documentation|strategy_development",
                    "default": "feature_development"
                },
                "original_prompt": {
                    "type": "string",
                    "description": "原始prompt（可选）：用于优化已有prompt"
                },
                "include_template": {
                    "type": "boolean",
                    "description": "是否参考已有模板",
                    "default": True
                }
            },
            "required": ["task_description"]
        }
    ),
    Tool(
        name="xuanyuan.prompt.feedback",
        description="提交prompt使用反馈，用于优化工具本身",
        inputSchema={
            "type": "object",
            "properties": {
                "prompt_id": {
                    "type": "string",
                    "description": "prompt ID（可选）"
                },
                "original_prompt": {
                    "type": "string",
                    "description": "原始prompt"
                },
                "optimized_prompt": {
                    "type": "string",
                    "description": "优化后的prompt"
                },
                "rating": {
                    "type": "integer",
                    "description": "评分1-5，5为最佳",
                    "minimum": 1,
                    "maximum": 5
                },
                "feedback": {
                    "type": "string",
                    "description": "文字反馈"
                },
                "execution_result": {
                    "type": "string",
                    "description": "Cursor执行结果（可选）"
                }
            },
            "required": ["rating"]
        }
    ),
    # 错误处理工具
    Tool(
        name="xuanyuan.error.analyze",
        description="分析错误",
        inputSchema={
            "type": "object",
            "properties": {
                "error_message": {"type": "string", "description": "错误信息"},
                "error_type": {"type": "string", "description": "错误类型（可选）"},
                "code_context": {"type": "string", "description": "代码上下文（可选）"}
            },
            "required": ["error_message"]
        }
    ),
    Tool(
        name="xuanyuan.error.suggest_fix",
        description="建议修复方案",
        inputSchema={
            "type": "object",
            "properties": {
                "error_id": {"type": "string", "description": "错误ID（来自analyze）"},
                "code_context": {"type": "string", "description": "代码上下文"}
            },
            "required": ["error_id"]
        }
    ),
    Tool(
        name="xuanyuan.error.history",
        description="查看错误历史",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "返回数量限制", "default": 20},
                "error_type": {"type": "string", "description": "错误类型筛选（可选）"}
            }
        }
    ),
    Tool(
        name="xuanyuan.debug.steps",
        description="生成调试步骤",
        inputSchema={
            "type": "object",
            "properties": {
                "error_message": {"type": "string", "description": "错误信息"},
                "code_context": {"type": "string", "description": "代码上下文"}
            },
            "required": ["error_message"]
        }
    ),
    # 命令助手工具
    Tool(
        name="xuanyuan.command.suggest",
        description="命令建议",
        inputSchema={
            "type": "object",
            "properties": {
                "intent": {"type": "string", "description": "用户意图描述"},
                "context": {"type": "string", "description": "当前上下文（可选）"}
            },
            "required": ["intent"]
        }
    ),
    Tool(
        name="xuanyuan.command.explain",
        description="解释命令",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "要解释的命令"}
            },
            "required": ["command"]
        }
    ),
    Tool(
        name="xuanyuan.command.history",
        description="命令历史",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "description": "返回数量限制", "default": 20},
                "pattern": {"type": "string", "description": "搜索模式（可选）"}
            }
        }
    ),
    Tool(
        name="xuanyuan.command.check_safety",
        description="检查命令安全性",
        inputSchema={
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "要检查的命令"}
            },
            "required": ["command"]
        }
    ),
    # 记忆功能工具
    Tool(
        name="xuanyuan.memory.save_context",
        description="保存上下文",
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "上下文键"},
                "value": {"type": "string", "description": "上下文值"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "标签列表（可选）"}
            },
            "required": ["key", "value"]
        }
    ),
    Tool(
        name="xuanyuan.memory.recall",
        description="回忆历史",
        inputSchema={
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "上下文键"}
            },
            "required": ["key"]
        }
    ),
    Tool(
        name="xuanyuan.memory.search",
        description="搜索记忆",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "limit": {"type": "integer", "description": "返回数量限制", "default": 10}
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="xuanyuan.memory.summarize",
        description="会话摘要",
        inputSchema={
            "type": "object",
            "properties": {
                "session_id": {"type": "string", "description": "会话ID（可选）"},
                "max_length": {"type": "integer", "description": "摘要最大长度", "default": 500}
            }
        }
    ),
]

# ==================== 工具处理函数 ====================

async def handle_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        result = {}
        
        if name.startswith("xuanyuan.prompt.templates.") or name == "xuanyuan.prompt.extract_from_logs":
            result = await handle_prompt_templates(name, arguments)
        elif name == "xuanyuan.prompt.optimize":
            result = await handle_optimize_prompt(arguments)
        elif name == "xuanyuan.prompt.feedback":
            result = await handle_prompt_feedback(arguments)
        elif name.startswith("xuanyuan.error.") or name.startswith("xuanyuan.debug."):
            result = await handle_error_debug(name, arguments)
        elif name.startswith("xuanyuan.command."):
            result = await handle_command(name, arguments)
        elif name.startswith("xuanyuan.memory."):
            result = await handle_memory(name, arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.error(f"处理工具 {name} 时出错: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

# ==================== 从开发记录提取Prompt ====================

async def handle_extract_prompts(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """从实际开发记录中提取prompt（遵循Cursor Prompt Engineering最佳实践）"""
    import re
    
    source = arguments.get("source", "all")
    limit = arguments.get("limit", 20)
    min_length = arguments.get("min_length", 30)
    
    extracted_prompts = []
    
    try:
        # 1. 从prompts目录提取Markdown模板
        if source in ["prompts", "all"]:
            prompts_dir_prompts = await _extract_from_prompts_dir(limit, min_length)
            extracted_prompts.extend(prompts_dir_prompts)
        
        # 2. 从.cursor/rules提取Cursor Rules文件
        if source in ["cursor_rules", "all"]:
            rules_prompts = await _extract_from_cursor_rules(limit, min_length)
            extracted_prompts.extend(rules_prompts)
        
        # 3. 从devlog提取开发日志中的prompt
        if source in ["devlog", "all"]:
            devlog_prompts = await _extract_from_devlog(limit, min_length)
            extracted_prompts.extend(devlog_prompts)
        
        # 去重（基于内容相似度）
        unique_prompts = _deduplicate_prompts(extracted_prompts)
        
        # 限制数量
        unique_prompts = unique_prompts[:limit]
        
        # 分类和标签（简单启发式规则）
        for prompt in unique_prompts:
            prompt["category"] = _classify_prompt(prompt.get("content", ""))
            prompt["tags"] = _extract_tags(prompt.get("content", ""))
        
        return {
            "success": True,
            "prompts": unique_prompts,
            "count": len(unique_prompts),
            "source": source
        }
        
    except Exception as e:
        logger.error(f"提取prompt失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _extract_from_prompts_dir(limit: int, min_length: int) -> List[Dict[str, Any]]:
    """从prompts目录提取Markdown模板文件"""
    prompts = []
    
    prompts_dir = TRQUANT_ROOT / "prompts"
    if prompts_dir.exists():
        for md_file in prompts_dir.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                extracted = _extract_prompts_from_markdown(content, md_file.name)
                prompts.extend(extracted)
            except Exception as e:
                logger.warning(f"读取prompt文件失败 {md_file}: {e}")
    
    return prompts


async def _extract_from_cursor_rules(limit: int, min_length: int) -> List[Dict[str, Any]]:
    """从.cursor/rules提取Cursor Rules文件"""
    import re
    prompts = []
    
    # 从.cursor/rules目录提取
    rules_dir = TRQUANT_ROOT / ".cursor" / "rules"
    if rules_dir.exists():
        for mdc_file in rules_dir.rglob("*.mdc"):
            try:
                content = mdc_file.read_text(encoding='utf-8')
                if len(content.strip()) >= min_length:
                    prompts.append({
                        "content": content.strip(),
                        "source": "cursor_rules",
                        "source_info": {"file": mdc_file.name, "type": "rule_file"}
                    })
            except Exception as e:
                logger.warning(f"读取Cursor Rules文件失败 {mdc_file}: {e}")
    
    # 从.cursor/index.mdc提取
    index_file = TRQUANT_ROOT / ".cursor" / "index.mdc"
    if index_file.exists():
        try:
            content = index_file.read_text(encoding='utf-8')
            if len(content.strip()) >= min_length:
                prompts.append({
                    "content": content.strip(),
                    "source": "cursor_rules",
                    "source_info": {"file": "index.mdc", "type": "global_rules"}
                })
        except Exception as e:
            logger.warning(f"读取index.mdc失败: {e}")
    
    return prompts


async def _extract_from_devlog(limit: int, min_length: int) -> List[Dict[str, Any]]:
    """从devlog提取开发日志中的prompt"""
    import re
    prompts = []
    
    # 尝试多个可能的devlog位置
    devlog_paths = [
        TRQUANT_ROOT / ".trquant" / "project_data" / "trquant" / "devlog.json",
        TRQUANT_ROOT / "data" / "devlog.json",
    ]
    
    for devlog_file in devlog_paths:
        if devlog_file.exists():
            try:
                devlog_data = _load_json_file(devlog_file, {})
                logs = devlog_data.get("logs", []) or devlog_data.get("items", [])
                
                # Prompt关键词模式（根据Cursor方法论）
                prompt_keywords = [
                    "目标", "约束", "范围", "验收", "要求", "步骤",
                    "目标：", "约束：", "范围：", "验收标准：",
                    "task", "goal", "constraint", "requirement", "step"
                ]
                
                for log_entry in logs[:50]:  # 只检查最近50条
                    content = log_entry.get("content", "") if isinstance(log_entry, dict) else str(log_entry)
                    if not content or len(content) < min_length:
                        continue
                    
                    # 检查是否包含prompt特征关键词
                    content_lower = content.lower()
                    if any(keyword in content_lower for keyword in prompt_keywords):
                        # 进一步检查是否有结构化特征（包含多个关键词）
                        keyword_count = sum(1 for kw in prompt_keywords if kw in content_lower)
                        if keyword_count >= 2:  # 至少包含2个关键词，更可能是prompt
                            prompts.append({
                                "content": content,
                                "source": "devlog",
                                "source_info": {
                                    "log_id": log_entry.get("id", "unknown"),
                                    "created": log_entry.get("created", log_entry.get("date", ""))
                                }
                            })
            except Exception as e:
                logger.warning(f"读取devlog失败 {devlog_file}: {e}")
            break  # 找到第一个可用的devlog文件就停止
    
    return prompts


# ==================== 智能Prompt优化 ====================

async def handle_optimize_prompt(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """根据开发任务需求智能生成或优化prompt（遵循Cursor方法论）"""
    task_description = arguments.get("task_description", "")
    context = arguments.get("context", "")
    prompt_type = arguments.get("prompt_type", "feature_development")
    include_template = arguments.get("include_template", True)
    original_prompt = arguments.get("original_prompt", "")  # 用于优化已有prompt
    
    if not task_description and not original_prompt:
        return {"success": False, "error": "任务描述或原始prompt不能为空"}
    
    try:
        # 1. 加载相关模板（如果启用）
        template_examples = []
        if include_template:
            templates_file = PROMPTS_DIR / "templates.json"
            templates = _load_json_file(templates_file, {"templates": []})
            template_list = templates.get("templates", [])
            
            # 根据prompt_type筛选相关模板
            relevant_templates = [t for t in template_list if t.get("category") == prompt_type]
            if not relevant_templates:
                relevant_templates = template_list[:3]
            
            template_examples = relevant_templates[:3]
        
        # 2. 根据Cursor方法论生成结构化prompt
        if original_prompt:
            # 优化模式：基于原始prompt进行优化
            optimized_prompt = _optimize_existing_prompt(original_prompt, task_description, prompt_type)
        else:
            # 生成模式：根据任务描述生成新prompt
            optimized_prompt = _generate_structured_prompt(
                task_description=task_description,
                context=context,
                prompt_type=prompt_type,
                template_examples=template_examples
            )
        
        # 3. 分析结构化程度
        structure_analysis = _analyze_prompt_structure(optimized_prompt)
        
        # 4. 提取分类和标签
        category = _classify_prompt(optimized_prompt)
        tags = _extract_tags(optimized_prompt)
        
        # 5. 生成改进建议
        suggestions = _generate_improvement_suggestions(optimized_prompt, structure_analysis)
        
        return {
            "success": True,
            "prompt": optimized_prompt,
            "category": category,
            "tags": tags,
            "prompt_type": prompt_type,
            "structure": structure_analysis,
            "suggestions": suggestions,
            "template_refs": [t.get("name", "") for t in template_examples] if template_examples else []
        }
    except Exception as e:
        logger.error(f"优化prompt失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


def _generate_structured_prompt(
    task_description: str,
    context: str = "",
    prompt_type: str = "feature_development",
    template_examples: List[Dict[str, Any]] = None
) -> str:
    """根据Cursor方法论生成结构化prompt"""
    
    # Prompt类型对应的模板结构
    type_templates = {
        "feature_development": """## 目标
{goal}

## 约束
{constraints}

## 范围
{scope}

## 验收标准
{acceptance}

## 输出要求
{output_format}""",
        "refactoring": """## 重构目标
{goal}

## 约束
- 行为保持一致，不改变公开API
- 最小化diff，只改必要部分
{constraints}

## 范围
{scope}

## 验收标准
{acceptance}""",
        "bug_fix": """## 问题描述
{goal}

## 约束
- 修复问题同时不引入新bug
- 添加回归测试
{constraints}

## 修复范围
{scope}

## 验收标准
{acceptance}""",
        "code_review": """## 审查目标
{goal}

## 审查标准
- Critical: 必须修复的问题
- Major: 建议修复的问题
- Minor: 可选改进
{constraints}

## 审查范围
{scope}

## 输出要求
{acceptance}""",
        "testing": """## 测试目标
{goal}

## 测试约束
{constraints}

## 测试范围
{scope}

## 验收标准
{acceptance}""",
        "documentation": """## 文档目标
{goal}

## 文档要求
{constraints}

## 文档范围
{scope}

## 验收标准
{acceptance}""",
        "strategy_development": """## 策略目标
{goal}

## 约束条件
{constraints}

## 实现范围
{scope}

## 验收标准
{acceptance}

## 回测要求
- 提供回测代码
- 包含关键指标计算
- 考虑交易成本"""
    }
    
    template = type_templates.get(prompt_type, type_templates["feature_development"])
    
    # 提取任务描述中的关键信息
    goal = task_description
    if context:
        goal += f"\n\n**上下文**: {context}"
    
    # 生成约束
    constraints = _generate_constraints(task_description, prompt_type, context)
    
    # 生成范围
    scope = _generate_scope(task_description, context)
    
    # 生成验收标准
    acceptance = _generate_acceptance_criteria(prompt_type)
    
    # 生成输出格式要求
    output_format = _generate_output_format(prompt_type)
    
    # 组装prompt
    prompt = template.format(
        goal=goal,
        constraints=constraints,
        scope=scope,
        acceptance=acceptance,
        output_format=output_format
    )
    
    return prompt


def _optimize_existing_prompt(original_prompt: str, task_description: str, prompt_type: str) -> str:
    """优化已有的prompt，补充缺失的结构化要素"""
    original_lower = original_prompt.lower()
    
    # 分析原始prompt缺少哪些要素
    has_goal = any(k in original_lower for k in ["目标", "goal", "要实现", "实现", "任务"])
    has_constraint = any(k in original_lower for k in ["约束", "constraint", "限制", "要求", "规范"])
    has_scope = any(k in original_lower for k in ["范围", "scope", "文件", "module", "只改"])
    has_acceptance = any(k in original_lower for k in ["验收", "acceptance", "验证", "通过", "完成标准"])
    
    optimized_parts = []
    
    # 如果缺少目标，添加目标
    if not has_goal:
        if task_description:
            optimized_parts.append(f"## 目标\n{task_description}")
        else:
            optimized_parts.append("## 目标\n请明确要实现的功能或解决的问题")
    
    # 添加原始内容
    optimized_parts.append("\n## 原始需求\n" + original_prompt)
    
    # 如果缺少约束，添加默认约束
    if not has_constraint:
        constraints = _generate_constraints(task_description or original_prompt, prompt_type, "")
        optimized_parts.append(f"\n## 约束\n{constraints}")
    
    # 如果缺少范围，添加范围提示
    if not has_scope:
        optimized_parts.append("\n## 范围\n- 请明确涉及的文件和模块\n- 只修改必要部分")
    
    # 如果缺少验收标准，添加默认验收标准
    if not has_acceptance:
        acceptance = _generate_acceptance_criteria(prompt_type)
        optimized_parts.append(f"\n## 验收标准\n{acceptance}")
    
    return "\n".join(optimized_parts)


def _generate_constraints(task_description: str, prompt_type: str, context: str) -> str:
    """生成约束条件"""
    constraints = []
    task_lower = task_description.lower()
    context_lower = context.lower()
    
    # 通用约束
    constraints.append("- 遵循项目现有代码风格和规范")
    constraints.append("- 保持API兼容性（除非明确要求变更）")
    constraints.append("- 添加必要的注释和文档")
    
    # 根据上下文识别技术栈约束
    if "python" in context_lower or "py" in context_lower:
        constraints.append("- 使用Python 3.x语法，遵循PEP8规范")
    if "typescript" in context_lower or "ts" in context_lower:
        constraints.append("- 使用TypeScript，启用严格类型检查")
    if "react" in context_lower:
        constraints.append("- 遵循React最佳实践和Hooks规范")
    if "量化" in task_lower or "策略" in task_lower:
        constraints.append("- 考虑交易成本和滑点")
        constraints.append("- 避免未来函数（look-ahead bias）")
    
    # 根据prompt类型添加特定约束
    if prompt_type == "refactoring":
        constraints.append("- 行为保持一致，不改变公开API")
        constraints.append("- 最小化diff，只改必要部分")
    elif prompt_type == "bug_fix":
        constraints.append("- 修复问题的同时不引入新的bug")
        constraints.append("- 添加回归测试")
    elif prompt_type == "feature_development":
        constraints.append("- 不引入新的外部依赖（除非必要）")
        constraints.append("- 考虑性能影响")
    
    return "\n".join(constraints)


def _generate_scope(task_description: str, context: str) -> str:
    """生成范围说明"""
    import re
    scope_items = []
    
    # 从任务描述中提取文件/模块信息
    files = re.findall(r'[\w/]+\.\w+', task_description + " " + context)
    if files:
        scope_items.append(f"- 涉及文件：{', '.join(set(files[:5]))}")
    
    # 通用范围说明
    if not scope_items:
        scope_items.append("- 需要修改的文件和模块（请具体指定）")
    
    scope_items.append("- 只修改必要部分，保持其他代码不变")
    scope_items.append("- 不要修改不相关的文件")
    
    return "\n".join(scope_items)


def _generate_acceptance_criteria(prompt_type: str) -> str:
    """生成验收标准"""
    criteria_map = {
        "feature_development": [
            "- 功能按需求实现",
            "- 通过单元测试",
            "- 代码通过lint检查",
            "- 更新相关文档"
        ],
        "refactoring": [
            "- 功能行为保持一致",
            "- 代码可读性提升",
            "- 通过现有测试",
            "- 性能不降低"
        ],
        "bug_fix": [
            "- 问题已修复",
            "- 通过回归测试",
            "- 添加相关测试用例",
            "- 说明修复方案和潜在影响"
        ],
        "code_review": [
            "- 输出结构化的审查意见",
            "- 标注Critical/Major/Minor级别",
            "- 提供具体改进建议",
            "- 检查安全性、性能、可维护性"
        ],
        "testing": [
            "- 测试用例覆盖主要功能",
            "- 测试通过",
            "- 包含边界情况和异常情况"
        ],
        "documentation": [
            "- 文档完整准确",
            "- 包含使用示例",
            "- 格式规范统一"
        ],
        "strategy_development": [
            "- 策略逻辑清晰",
            "- 回测结果符合预期",
            "- 风险控制完善",
            "- 代码可复用"
        ]
    }
    
    criteria = criteria_map.get(prompt_type, criteria_map["feature_development"])
    return "\n".join(criteria)


def _generate_output_format(prompt_type: str) -> str:
    """生成输出格式要求"""
    format_map = {
        "feature_development": "- 以diff格式输出代码变更\n- 说明每个改动的目的",
        "refactoring": "- 最小diff\n- 说明重构点",
        "bug_fix": "- 修复diff\n- 回归测试代码",
        "code_review": "- 结构化审查意见\n- 按严重程度分类",
        "testing": "- 测试代码\n- 测试用例说明",
        "documentation": "- Markdown格式\n- 包含示例代码",
        "strategy_development": "- 完整策略代码\n- 回测结果分析"
    }
    return format_map.get(prompt_type, "- 清晰的代码和说明")


def _analyze_prompt_structure(prompt: str) -> Dict[str, bool]:
    """分析prompt的结构化程度"""
    prompt_lower = prompt.lower()
    
    return {
        "has_goal": any(k in prompt_lower for k in ["目标", "goal", "要实现", "实现", "任务"]),
        "has_constraint": any(k in prompt_lower for k in ["约束", "constraint", "限制", "要求", "规范"]),
        "has_scope": any(k in prompt_lower for k in ["范围", "scope", "文件", "module", "只改", "涉及"]),
        "has_acceptance": any(k in prompt_lower for k in ["验收", "acceptance", "验证", "通过", "完成标准"]),
        "has_output_format": any(k in prompt_lower for k in ["输出", "output", "格式", "format", "diff"])
    }


def _generate_improvement_suggestions(prompt: str, structure: Dict[str, bool]) -> List[str]:
    """根据结构分析生成改进建议"""
    suggestions = []
    
    if not structure.get("has_goal"):
        suggestions.append("💡 建议添加明确的目标描述")
    if not structure.get("has_constraint"):
        suggestions.append("💡 建议添加约束条件（技术栈、规范等）")
    if not structure.get("has_scope"):
        suggestions.append("💡 建议明确修改范围（涉及的文件和模块）")
    if not structure.get("has_acceptance"):
        suggestions.append("💡 建议添加验收标准")
    if not structure.get("has_output_format"):
        suggestions.append("💡 建议指定输出格式（diff、代码块等）")
    
    if not suggestions:
        suggestions.append("✅ Prompt结构完整，符合Cursor方法论")
    
    return suggestions


# ==================== 反馈机制 ====================

async def handle_prompt_feedback(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """处理prompt使用反馈，用于优化工具本身"""
    prompt_id = arguments.get("prompt_id", "")
    original_prompt = arguments.get("original_prompt", "")
    optimized_prompt = arguments.get("optimized_prompt", "")
    rating = arguments.get("rating", 3)  # 1-5评分
    feedback_text = arguments.get("feedback", "")
    execution_result = arguments.get("execution_result", "")  # Cursor执行结果
    
    try:
        # 加载反馈记录
        feedback_file = PROMPTS_DIR / "feedback_history.json"
        feedback_data = _load_json_file(feedback_file, {"feedbacks": [], "stats": {}})
        
        # 创建反馈记录
        feedback_record = {
            "id": _generate_id("fb"),
            "prompt_id": prompt_id,
            "original_prompt": original_prompt[:500] if original_prompt else "",
            "optimized_prompt": optimized_prompt[:500] if optimized_prompt else "",
            "rating": rating,
            "feedback": feedback_text,
            "execution_result": execution_result[:500] if execution_result else "",
            "timestamp": datetime.now().isoformat()
        }
        
        feedback_data["feedbacks"].append(feedback_record)
        
        # 更新统计
        stats = feedback_data.get("stats", {"total": 0, "avg_rating": 0})
        total = stats.get("total", 0) + 1
        avg = (stats.get("avg_rating", 0) * stats.get("total", 0) + rating) / total
        feedback_data["stats"] = {"total": total, "avg_rating": round(avg, 2)}
        
        # 保存
        _save_json_file(feedback_file, feedback_data)
        
        # 如果评分低，记录改进点
        improvement_suggestions = []
        if rating <= 2:
            improvement_suggestions.append("需要改进prompt生成逻辑")
            if "约束" not in optimized_prompt:
                improvement_suggestions.append("添加更多约束条件")
            if "验收" not in optimized_prompt:
                improvement_suggestions.append("强化验收标准")
        
        return {
            "success": True,
            "feedback_id": feedback_record["id"],
            "stats": feedback_data["stats"],
            "improvement_suggestions": improvement_suggestions
        }
    except Exception as e:
        logger.error(f"保存反馈失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


def _extract_prompts_from_markdown(content: str, filename: str) -> List[Dict[str, Any]]:
    """从Markdown内容中提取prompt模板"""
    import re
    prompts = []
    
    # 方法1: 提取代码块中的prompt（```标记的内容）
    code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
    for block in code_blocks:
        block = block.strip()
        if len(block) >= 30:  # 最小长度
            prompts.append({
                "content": block,
                "source": "prompts_markdown",
                "source_info": {"file": filename, "type": "code_block"}
            })
    
    # 方法2: 提取标题下的段落内容（可能是prompt描述）
    # 查找"##"或"###"标题后的内容
    sections = re.split(r'^#{2,3}\s+(.+)$', content, flags=re.MULTILINE)
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            title = sections[i].strip()
            body = sections[i + 1].strip()
            
            # 跳过代码块（已经在方法1中提取）
            body_clean = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
            body_clean = body_clean.strip()
            
            # 如果内容足够长且包含描述性文字，可能是prompt
            if len(body_clean) >= 50 and not body_clean.startswith('#'):
                # 提取第一段作为主要内容
                first_paragraph = body_clean.split('\n\n')[0].strip()
                if len(first_paragraph) >= 30:
                    prompts.append({
                        "content": first_paragraph,
                        "source": "prompts_markdown",
                        "source_info": {"file": filename, "section": title, "type": "section"}
                    })
    
    # 方法3: 提取列表项中的内容（如果包含问号或描述性语言）
    list_items = re.findall(r'^[-*+]\s+(.+)$', content, flags=re.MULTILINE)
    for item in list_items:
        item = item.strip()
        if len(item) >= 30 and ('?' in item or len(item) > 50):
            prompts.append({
                "content": item,
                "source": "prompts_markdown",
                "source_info": {"file": filename, "type": "list_item"}
            })
    
    return prompts


def _deduplicate_prompts(prompts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """去重prompt列表（基于内容相似度）"""
    import re
    
    if not prompts:
        return []
    
    unique_prompts = []
    seen_contents = set()
    
    for prompt in prompts:
        content = prompt.get("content", "").strip().lower()
        
        # 简单去重：完全相同的去掉
        if content in seen_contents:
            continue
        
        # 简单相似度检查：如果内容几乎相同（去除空格后），也认为是重复
        content_normalized = re.sub(r"\s+", " ", content)
        if any(
            re.sub(r"\s+", " ", p.get("content", "").strip().lower()) == content_normalized
            for p in unique_prompts
        ):
            continue
        
        seen_contents.add(content)
        unique_prompts.append(prompt)
    
    return unique_prompts


def _classify_prompt(content: str) -> str:
    """基于Cursor方法论的结构化prompt分类"""
    content_lower = content.lower()
    
    # 识别结构化要素（根据Cursor方法论）
    has_goal = any(keyword in content_lower for keyword in ["目标", "goal", "要实现", "实现", "任务", "task", "需求", "requirement"])
    has_constraint = any(keyword in content_lower for keyword in ["约束", "constraint", "限制", "要求", "规范", "不允许", "不引入"])
    has_scope = any(keyword in content_lower for keyword in ["范围", "scope", "文件", "file", "模块", "module", "只改", "不改"])
    has_acceptance = any(keyword in content_lower for keyword in ["验收", "acceptance", "测试", "test", "验证", "verify", "通过", "完成"])
    
    # Bug修复（包含错误、修复、问题等关键词）
    if any(keyword in content_lower for keyword in ["错误", "error", "异常", "exception", "bug", "修复", "fix", "问题", "issue"]):
        if has_acceptance:
            return "bug_fix"  # 包含验收标准的bug修复
        return "error_handling"
    
    # 重构（包含重构、优化、改进等关键词，且可能有约束）
    if any(keyword in content_lower for keyword in ["重构", "refactor", "优化", "optimize", "改进", "improve", "重写", "rewrite"]):
        if has_constraint and has_scope:
            return "refactoring"  # 结构化重构
        return "refactoring"
    
    # 新功能开发（包含目标、实现等，且通常有约束和范围）
    if has_goal and (has_constraint or has_scope):
        if any(keyword in content_lower for keyword in ["功能", "feature", "新功能", "实现", "开发"]):
            return "feature_development"
        return "code_generation"
    
    # 代码Review（包含审查、检查等关键词）
    if any(keyword in content_lower for keyword in ["审查", "review", "检查", "check", "代码审查", "code review"]):
        return "code_review"
    
    # 测试相关
    if any(keyword in content_lower for keyword in ["测试", "test", "测试用例", "test case", "单元测试", "unit test"]):
        return "testing"
    
    # 文档相关
    if any(keyword in content_lower for keyword in ["文档", "document", "doc", "说明", "注释", "comment", "readme"]):
        return "documentation"
    
    # 策略开发（保留原有分类）
    if any(keyword in content_lower for keyword in ["策略", "strategy", "因子", "factor"]):
        return "strategy_development"
    
    # 系统级规则（包含规则、规范等）
    if any(keyword in content_lower for keyword in ["规则", "rule", "规范", "standard", "约定", "convention"]):
        return "system"
    
    return "general"


def _extract_tags(content: str) -> List[str]:
    """基于Cursor方法论提取prompt标签（识别结构化要素和prompt类型）"""
    content_lower = content.lower()
    tags = []
    
    # 结构化要素标签（根据Cursor方法论）
    if any(keyword in content_lower for keyword in ["目标", "goal", "要实现", "实现", "任务"]):
        tags.append("has_goal")
    if any(keyword in content_lower for keyword in ["约束", "constraint", "限制", "要求", "规范", "不允许"]):
        tags.append("has_constraint")
    if any(keyword in content_lower for keyword in ["范围", "scope", "文件", "module", "只改", "不改"]):
        tags.append("has_scope")
    if any(keyword in content_lower for keyword in ["验收", "acceptance", "验证", "通过", "完成标准"]):
        tags.append("has_acceptance")
    if any(keyword in content_lower for keyword in ["步骤", "step", "计划", "plan", "方案"]):
        tags.append("has_plan")
    
    # Prompt类型标签
    if any(keyword in content_lower for keyword in ["新功能", "feature", "新特性", "开发功能"]):
        tags.append("feature_development")
    if any(keyword in content_lower for keyword in ["重构", "refactor", "优化代码结构"]):
        tags.append("refactoring")
    if any(keyword in content_lower for keyword in ["修复", "fix", "bug", "错误修复"]):
        tags.append("bug_fix")
    if any(keyword in content_lower for keyword in ["审查", "review", "代码审查"]):
        tags.append("code_review")
    
    # 技术栈标签
    if any(keyword in content_lower for keyword in ["python", "py", "python3"]):
        tags.append("python")
    if any(keyword in content_lower for keyword in ["javascript", "js", "typescript", "ts"]):
        tags.append("javascript")
    if any(keyword in content_lower for keyword in ["react", "vue", "angular", "前端"]):
        tags.append("frontend")
    if any(keyword in content_lower for keyword in ["api", "后端", "backend", "服务"]):
        tags.append("backend")
    
    # 功能领域标签（保留量化相关）
    if any(keyword in content_lower for keyword in ["量化", "quantitative", "quant"]):
        tags.append("quantitative")
    if any(keyword in content_lower for keyword in ["交易", "trading"]):
        tags.append("trading")
    if any(keyword in content_lower for keyword in ["研究", "research"]):
        tags.append("research")
    if any(keyword in content_lower for keyword in ["数据库", "database", "db", "mongodb", "mysql"]):
        tags.append("database")
    if any(keyword in content_lower for keyword in ["测试", "test", "单元测试", "unit test"]):
        tags.append("testing")
    if any(keyword in content_lower for keyword in ["安全", "security", "认证", "authentication"]):
        tags.append("security")
    if any(keyword in content_lower for keyword in ["策略", "strategy", "因子", "factor"]):
        tags.append("strategy")
    
    # 输出格式标签
    if any(keyword in content_lower for keyword in ["diff", "差异", "变更"]):
        tags.append("diff_output")
    if any(keyword in content_lower for keyword in ["文件清单", "file list", "文件列表"]):
        tags.append("file_list")
    if any(keyword in content_lower for keyword in ["步骤", "step by step", "步骤说明"]):
        tags.append("step_by_step")
    
    return tags if tags else ["general"]

# ==================== 提示词模板处理 ====================

async def handle_prompt_templates(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """处理提示词模板相关工具"""
    # 占位符实现，将在Phase 2中完善
    templates_file = PROMPTS_DIR / "templates.json"
    templates = _load_json_file(templates_file, {"templates": []})
    
    if name == "xuanyuan.prompt.templates.list":
        category = arguments.get("category")
        template_list = templates.get("templates", [])
        if category:
            template_list = [t for t in template_list if t.get("category") == category]
        return {"success": True, "templates": template_list, "count": len(template_list)}
    
    elif name == "xuanyuan.prompt.templates.get":
        template_id = arguments.get("template_id")
        template_list = templates.get("templates", [])
        template = next((t for t in template_list if t.get("id") == template_id), None)
        if template:
            return {"success": True, "template": template}
        return {"success": False, "error": f"模板 {template_id} 不存在"}
    
    elif name == "xuanyuan.prompt.templates.create":
        template_id = _generate_id("tmpl")
        new_template = {
            "id": template_id,
            "name": arguments.get("name"),
            "content": arguments.get("content"),
            "category": arguments.get("category", "general"),
            "tags": arguments.get("tags", []),
            "description": arguments.get("description", ""),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "usage_count": 0,
            "avg_rating": 0.0
        }
        templates.setdefault("templates", []).append(new_template)
        _save_json_file(templates_file, templates)
        return {"success": True, "template_id": template_id, "template": new_template}
    
    elif name == "xuanyuan.prompt.templates.update":
        template_id = arguments.get("template_id")
        template_list = templates.get("templates", [])
        template = next((t for t in template_list if t.get("id") == template_id), None)
        if not template:
            return {"success": False, "error": f"模板 {template_id} 不存在"}
        
        if "name" in arguments:
            template["name"] = arguments["name"]
        if "content" in arguments:
            template["content"] = arguments["content"]
        if "category" in arguments:
            template["category"] = arguments["category"]
        if "tags" in arguments:
            template["tags"] = arguments["tags"]
        template["updated_at"] = datetime.now().isoformat()
        
        _save_json_file(templates_file, templates)
        return {"success": True, "template": template}
    
    elif name == "xuanyuan.prompt.templates.evaluate":
        template_id = arguments.get("template_id")
        result_quality = arguments.get("result_quality")
        feedback = arguments.get("feedback", "")
        
        # 更新模板评分（简化实现）
        template_list = templates.get("templates", [])
        template = next((t for t in template_list if t.get("id") == template_id), None)
        if template:
            usage_count = template.get("usage_count", 0)
            avg_rating = template.get("avg_rating", 0.0)
            new_avg = (avg_rating * usage_count + result_quality) / (usage_count + 1)
            template["usage_count"] = usage_count + 1
            template["avg_rating"] = new_avg
            if feedback:
                template.setdefault("feedback", []).append({
                    "rating": result_quality,
                    "feedback": feedback,
                    "timestamp": datetime.now().isoformat()
                })
            _save_json_file(templates_file, templates)
            return {"success": True, "template_id": template_id, "new_avg_rating": new_avg}
        return {"success": False, "error": f"模板 {template_id} 不存在"}
    
    elif name == "xuanyuan.prompt.best_practices.search":
        query = arguments.get("query", "").lower()
        limit = arguments.get("limit", 10)
        template_list = templates.get("templates", [])
        
        # 简单搜索：按名称、内容、标签匹配
        matches = []
        for t in template_list:
            score = 0
            if query in t.get("name", "").lower():
                score += 3
            if query in t.get("content", "").lower():
                score += 2
            if query in " ".join(t.get("tags", [])).lower():
                score += 1
            if score > 0:
                matches.append((score, t))
        
        matches.sort(key=lambda x: x[0], reverse=True)
        results = [t for _, t in matches[:limit]]
        return {"success": True, "results": results, "count": len(results)}
    
    elif name == "xuanyuan.prompt.extract_from_logs":
        return await handle_extract_prompts(arguments)
    
    return {"error": f"未知工具: {name}"}

# ==================== 错误处理（占位符） ====================

async def handle_error_debug(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """处理错误和调试相关工具"""
    # 占位符实现，将在Phase 3中完善
    errors_file = ERRORS_DIR / "errors.json"
    errors_data = _load_json_file(errors_file, {"errors": []})
    
    if name == "xuanyuan.error.analyze":
        error_message = arguments.get("error_message", "")
        error_type = arguments.get("error_type")
        code_context = arguments.get("code_context", "")
        
        # 简单错误分类
        error_category = "unknown"
        if "SyntaxError" in error_message or "语法" in error_message:
            error_category = "syntax"
        elif "NameError" in error_message or "Name" in error_message:
            error_category = "name"
        elif "TypeError" in error_message or "类型" in error_message:
            error_category = "type"
        elif "AttributeError" in error_message:
            error_category = "attribute"
        elif "ImportError" in error_message or "导入" in error_message:
            error_category = "import"
        elif "RuntimeError" in error_message or "运行时" in error_message:
            error_category = "runtime"
        
        error_id = _generate_id("err")
        error_record = {
            "id": error_id,
            "error_message": error_message,
            "error_type": error_type or error_category,
            "error_category": error_category,
            "code_context": code_context,
            "created_at": datetime.now().isoformat()
        }
        errors_data.setdefault("errors", []).append(error_record)
        _save_json_file(errors_file, errors_data)
        
        return {
            "success": True,
            "error_id": error_id,
            "error_category": error_category,
            "analysis": f"错误类型: {error_category}"
        }
    
    elif name == "xuanyuan.error.suggest_fix":
        error_id = arguments.get("error_id")
        errors_list = errors_data.get("errors", [])
        error_record = next((e for e in errors_list if e.get("id") == error_id), None)
        
        if not error_record:
            return {"success": False, "error": f"错误 {error_id} 不存在"}
        
        # 简单修复建议（将在Phase 3中增强）
        category = error_record.get("error_category", "unknown")
        suggestions = {
            "syntax": "检查语法错误，确保括号、引号匹配",
            "name": "检查变量或函数名是否正确，确认是否已定义",
            "type": "检查数据类型是否匹配",
            "attribute": "检查对象是否有该属性或方法",
            "import": "检查导入语句是否正确，模块是否已安装",
            "runtime": "检查运行时逻辑错误"
        }
        
        return {
            "success": True,
            "error_id": error_id,
            "suggestion": suggestions.get(category, "请检查代码逻辑")
        }
    
    elif name == "xuanyuan.error.history":
        limit = arguments.get("limit", 20)
        error_type = arguments.get("error_type")
        errors_list = errors_data.get("errors", [])
        
        if error_type:
            errors_list = [e for e in errors_list if e.get("error_category") == error_type]
        
        errors_list = sorted(errors_list, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]
        return {"success": True, "errors": errors_list, "count": len(errors_list)}
    
    elif name == "xuanyuan.debug.steps":
        error_message = arguments.get("error_message", "")
        code_context = arguments.get("code_context", "")
        
        # 简单调试步骤（将在Phase 3中增强）
        steps = [
            "1. 仔细阅读错误信息，定位出错位置",
            "2. 检查错误信息中提到的变量、函数或模块",
            "3. 查看代码上下文，确认逻辑是否正确",
            "4. 尝试使用print或日志输出中间值",
            "5. 如果可能，使用调试器单步执行"
        ]
        
        return {
            "success": True,
            "error_message": error_message,
            "debug_steps": steps
        }
    
    return {"error": f"未知工具: {name}"}

# ==================== 命令助手（占位符） ====================

async def handle_command(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """处理命令相关工具"""
    # 占位符实现，将在Phase 4中完善
    commands_file = COMMANDS_DIR / "commands.json"
    commands_data = _load_json_file(commands_file, {"history": [], "common_commands": {}})
    
    # 常用命令库
    common_commands = {
        "file_operations": {
            "ls": "列出目录内容: ls -lah",
            "find": "查找文件: find . -name '*.py'",
            "grep": "搜索文本: grep -r 'pattern' .",
            "cat": "查看文件: cat file.txt",
            "head": "查看文件前几行: head -n 20 file.txt",
            "tail": "查看文件后几行: tail -n 20 file.txt",
        },
        "git": {
            "status": "查看状态: git status",
            "add": "添加文件: git add .",
            "commit": "提交: git commit -m 'message'",
            "push": "推送: git push",
            "pull": "拉取: git pull",
            "log": "查看日志: git log --oneline",
        },
        "process": {
            "ps": "查看进程: ps aux | grep python",
            "kill": "结束进程: kill -9 PID",
            "top": "查看资源使用: top",
            "htop": "交互式查看: htop",
        },
        "network": {
            "ping": "测试连接: ping hostname",
            "curl": "HTTP请求: curl -X GET url",
            "wget": "下载文件: wget url",
        }
    }
    
    if name == "xuanyuan.command.suggest":
        intent = arguments.get("intent", "").lower()
        suggestions = []
        
        # 简单意图匹配
        if "文件" in intent or "file" in intent or "查看" in intent:
            suggestions.extend([
                {"command": "ls -lah", "category": "file_operations", "description": "列出当前目录内容"},
                {"command": "find . -name '*.py'", "category": "file_operations", "description": "查找Python文件"},
            ])
        elif "git" in intent or "提交" in intent:
            suggestions.extend([
                {"command": "git status", "category": "git", "description": "查看Git状态"},
                {"command": "git add .", "category": "git", "description": "添加所有文件"},
            ])
        else:
            # 默认建议
            suggestions.extend([
                {"command": "ls -lah", "category": "file_operations", "description": "列出目录内容"},
                {"command": "pwd", "category": "system", "description": "查看当前目录"},
            ])
        
        return {"success": True, "suggestions": suggestions, "intent": intent}
    
    elif name == "xuanyuan.command.explain":
        command = arguments.get("command", "")
        
        # 简单命令解释（将在Phase 4中增强）
        parts = command.split()
        cmd = parts[0] if parts else ""
        
        explanations = {
            "ls": "列出目录内容。常用选项: -l(详细信息), -a(包含隐藏文件), -h(人类可读大小)",
            "cd": "切换目录",
            "pwd": "显示当前工作目录",
            "grep": "搜索文本模式",
            "find": "查找文件",
            "git": "Git版本控制命令",
        }
        
        explanation = explanations.get(cmd, f"命令 {cmd} 的基本用法")
        return {"success": True, "command": command, "explanation": explanation}
    
    elif name == "xuanyuan.command.history":
        limit = arguments.get("limit", 20)
        pattern = arguments.get("pattern", "")
        history = commands_data.get("history", [])
        
        if pattern:
            history = [h for h in history if pattern.lower() in h.get("command", "").lower()]
        
        history = sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        return {"success": True, "history": history, "count": len(history)}
    
    elif name == "xuanyuan.command.check_safety":
        command = arguments.get("command", "")
        
        # 危险命令列表
        dangerous_patterns = [
            "rm -rf /",
            "rm -rf ~",
            "format",
            "fdisk",
            "mkfs",
            "dd if=",
            "> /dev/sd",
        ]
        
        is_dangerous = any(pattern in command for pattern in dangerous_patterns)
        risk_level = "high" if is_dangerous else "low"
        
        return {
            "success": True,
            "command": command,
            "is_dangerous": is_dangerous,
            "risk_level": risk_level,
            "warning": "警告：此命令可能造成数据丢失！" if is_dangerous else "命令相对安全"
        }
    
    return {"error": f"未知工具: {name}"}

# ==================== 记忆功能（占位符） ====================

async def handle_memory(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """处理记忆相关工具"""
    # 占位符实现，将在Phase 5中完善
    memory_file = MEMORY_DIR / "memory.json"
    memory_data = _load_json_file(memory_file, {"contexts": {}, "sessions": []})
    
    if name == "xuanyuan.memory.save_context":
        key = arguments.get("key")
        value = arguments.get("value")
        tags = arguments.get("tags", [])
        
        memory_data.setdefault("contexts", {})[key] = {
            "value": value,
            "tags": tags,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        _save_json_file(memory_file, memory_data)
        
        return {"success": True, "key": key, "saved": True}
    
    elif name == "xuanyuan.memory.recall":
        key = arguments.get("key")
        contexts = memory_data.get("contexts", {})
        context = contexts.get(key)
        
        if context:
            return {"success": True, "key": key, "value": context.get("value")}
        return {"success": False, "error": f"上下文 {key} 不存在"}
    
    elif name == "xuanyuan.memory.search":
        query = arguments.get("query", "").lower()
        limit = arguments.get("limit", 10)
        contexts = memory_data.get("contexts", {})
        
        matches = []
        for key, context in contexts.items():
            value = str(context.get("value", "")).lower()
            tags = " ".join(context.get("tags", [])).lower()
            if query in key.lower() or query in value or query in tags:
                matches.append({"key": key, "value": context.get("value"), "tags": context.get("tags", [])})
        
        matches = matches[:limit]
        return {"success": True, "results": matches, "count": len(matches)}
    
    elif name == "xuanyuan.memory.summarize":
        max_length = arguments.get("max_length", 500)
        sessions = memory_data.get("sessions", [])
        
        # 简单摘要（将在Phase 5中增强）
        if sessions:
            recent_session = sessions[-1] if sessions else {}
            summary = recent_session.get("summary", "暂无会话摘要")
            if len(summary) > max_length:
                summary = summary[:max_length] + "..."
            return {"success": True, "summary": summary}
        return {"success": True, "summary": "暂无会话记录"}
    
    return {"error": f"未知工具: {name}"}

# ==================== MCP服务器接口 ====================

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    return await handle_tool(name, arguments)

# ==================== 主函数 ====================

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())





