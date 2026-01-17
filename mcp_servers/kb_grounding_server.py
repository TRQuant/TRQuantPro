# -*- coding: utf-8 -*-
"""
KB Grounding MCP Server - 强制基于知识库的生成工具
实现 Tool-first 强制检索 + Citation-locked 证据绑定生成
"""
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('KBGroundingServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    logger.error(f"官方MCP SDK不可用: {e}")
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

# 导入知识库工具
try:
    from mcp_servers.unified_dev_server import (
        knowledge_search,
        knowledge_get,
        experience_search,
        practice_search,
        error_pattern_search,
        evidence_search,
        research_search,
        docs_search
    )
    KB_TOOLS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"知识库工具导入失败: {e}")
    KB_TOOLS_AVAILABLE = False

server = Server("kb-grounding-server")

# ============================================================================
# 工具定义
# ============================================================================

TOOLS = [
    Tool(
        name="kb.answer_with_evidence",
        description="基于知识库生成回答（强制检索+证据绑定）。必须先调用此工具获取证据，再生成回答。",
        inputSchema={
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "要回答的问题"
                },
                "mode": {
                    "type": "string",
                    "enum": ["research", "code", "ops", "general"],
                    "default": "general",
                    "description": "回答模式: research(研究/分析), code(代码生成), ops(运维/配置), general(通用)"
                },
                "min_evidence_count": {
                    "type": "integer",
                    "default": 3,
                    "description": "最少需要的证据数量"
                },
                "max_context_blocks": {
                    "type": "integer",
                    "default": 10,
                    "description": "最多返回的上下文块数量"
                }
            },
            "required": ["question"]
        }
    ),
    Tool(
        name="kb.code_with_evidence",
        description="基于知识库生成代码（强制检索+接口约束）。必须先调用此工具获取接口规范、项目约束、反例库，再生成代码。",
        inputSchema={
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "代码生成任务描述"
                },
                "file_path": {
                    "type": "string",
                    "description": "目标文件路径（可选，用于获取相关代码规范）"
                },
                "module": {
                    "type": "string",
                    "description": "模块名称（可选，用于获取模块规范）"
                },
                "min_evidence_count": {
                    "type": "integer",
                    "default": 5,
                    "description": "最少需要的证据数量（代码生成需要更多证据）"
                }
            },
            "required": ["task"]
        }
    ),
    Tool(
        name="kb.verify_citations",
        description="验证生成内容的引用覆盖率。检查每个关键断言是否有对应的证据支持。",
        inputSchema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "要验证的内容（回答或代码）"
                },
                "evidence_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "引用的证据ID列表"
                },
                "min_coverage": {
                    "type": "number",
                    "default": 0.7,
                    "description": "最低覆盖率阈值（0-1）"
                }
            },
            "required": ["content", "evidence_ids"]
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """调用工具"""
    try:
        if name == "kb.answer_with_evidence":
            result = await handle_answer_with_evidence(arguments)
        elif name == "kb.code_with_evidence":
            result = await handle_code_with_evidence(arguments)
        elif name == "kb.verify_citations":
            result = await handle_verify_citations(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False, indent=2)
        )]
    except Exception as e:
        logger.error(f"工具执行失败: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, ensure_ascii=False)
        )]


# ============================================================================
# 核心处理函数
# ============================================================================

async def handle_answer_with_evidence(args: Dict) -> Dict:
    """
    基于知识库生成回答的上下文包
    
    返回结构:
    {
        "context_blocks": [
            {
                "id": "kb_xxx",
                "title": "标题",
                "snippet": "相关片段",
                "source": "来源",
                "confidence": 0.95,
                "type": "knowledge|experience|practice|error_pattern"
            }
        ],
        "constraints": ["必须遵守的约束"],
        "unknowns": ["缺失的信息"],
        "recommended_actions": ["下一步建议"],
        "citation_format": "[KB:doc_id#chunk_id]",
        "evidence_sufficient": true
    }
    """
    question = args["question"]
    mode = args.get("mode", "general")
    min_evidence = args.get("min_evidence_count", 3)
    max_blocks = args.get("max_context_blocks", 10)
    
    logger.info(f"处理问题: {question}, 模式: {mode}")
    
    if not KB_TOOLS_AVAILABLE:
        return {
            "error": "知识库工具不可用",
            "context_blocks": [],
            "evidence_sufficient": False
        }
    
    # 1. 多源检索（混合搜索）
    context_blocks = []
    
    # 1.1 知识库搜索
    try:
        kb_results = knowledge_search(query=question, limit=max_blocks)
        if kb_results.get("success"):
            for item in kb_results.get("results", [])[:max_blocks]:
                context_blocks.append({
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "snippet": item.get("content", "")[:500],  # 截取前500字符
                    "source": item.get("source", "knowledge_base"),
                    "confidence": item.get("_score", 0.5) / 20.0,  # 归一化到0-1
                    "type": "knowledge",
                    "tags": item.get("tags", [])
                })
    except Exception as e:
        logger.warning(f"知识库搜索失败: {e}")
    
    # 1.2 经验搜索
    try:
        exp_results = experience_search(query=question, project="trquant")
        if exp_results.get("success"):
            for item in exp_results.get("results", [])[:max_blocks//2]:
                context_blocks.append({
                    "id": f"exp_{item.get('id', '')}",
                    "title": f"经验: {item.get('title', '')}",
                    "snippet": item.get("content", "")[:500],
                    "source": "experience_base",
                    "confidence": 0.8,
                    "type": "experience"
                })
    except Exception as e:
        logger.warning(f"经验搜索失败: {e}")
    
    # 1.3 最佳实践搜索
    try:
        practice_results = practice_search(query=question)
        if practice_results.get("success"):
            for item in practice_results.get("results", [])[:max_blocks//2]:
                context_blocks.append({
                    "id": f"practice_{item.get('id', '')}",
                    "title": f"最佳实践: {item.get('title', '')}",
                    "snippet": item.get("description", "")[:500],
                    "source": "best_practices",
                    "confidence": 0.85,
                    "type": "practice"
                })
    except Exception as e:
        logger.warning(f"最佳实践搜索失败: {e}")
    
    # 1.4 错误模式搜索（如果是代码相关）
    if mode == "code":
        try:
            error_results = error_pattern_search(error_msg=question)
            if error_results.get("success"):
                for item in error_results.get("results", [])[:3]:
                    context_blocks.append({
                        "id": f"error_{item.get('id', '')}",
                        "title": f"错误模式: {item.get('error_pattern', '')}",
                        "snippet": item.get("solution", "")[:500],
                        "source": "error_patterns",
                        "confidence": 0.9,
                        "type": "error_pattern"
                    })
        except Exception as e:
            logger.warning(f"错误模式搜索失败: {e}")
    
    # 2. 按置信度排序并去重
    context_blocks = sorted(context_blocks, key=lambda x: x["confidence"], reverse=True)
    # 简单去重（基于title）
    seen_titles = set()
    unique_blocks = []
    for block in context_blocks:
        if block["title"] not in seen_titles:
            seen_titles.add(block["title"])
            unique_blocks.append(block)
    context_blocks = unique_blocks[:max_blocks]
    
    # 3. 提取约束和未知信息
    constraints = []
    unknowns = []
    
    # 根据模式添加特定约束
    if mode == "code":
        constraints.append("必须使用项目标准路径: /home/taotao/dev/QuantTest/TRQuant")
        constraints.append("必须遵循JQData API调用规范（见知识库）")
        constraints.append("代码必须包含错误处理")
    elif mode == "research":
        constraints.append("所有数据来源必须可追溯")
        constraints.append("所有指标定义必须引用知识库")
    
    # 检查证据是否充足
    evidence_sufficient = len(context_blocks) >= min_evidence
    
    if not evidence_sufficient:
        unknowns.append(f"需要至少{min_evidence}条证据，当前只有{len(context_blocks)}条")
        unknowns.append("建议：补充相关文档到知识库")
    
    # 4. 推荐行动
    recommended_actions = []
    if not evidence_sufficient:
        recommended_actions.append("调用 knowledge.add 补充缺失信息")
        recommended_actions.append("调用 crawler.search_docs 搜索外部文档")
    
    if mode == "code":
        recommended_actions.append("调用 repo.search_symbol 查找相关函数签名")
        recommended_actions.append("调用 spec.get_contract 获取接口规范")
    
    return {
        "context_blocks": context_blocks,
        "constraints": constraints,
        "unknowns": unknowns,
        "recommended_actions": recommended_actions,
        "citation_format": "[KB:{doc_id}#{chunk_id}]",
        "evidence_sufficient": evidence_sufficient,
        "evidence_count": len(context_blocks),
        "min_required": min_evidence,
        "mode": mode
    }


async def handle_code_with_evidence(args: Dict) -> Dict:
    """
    基于知识库生成代码的上下文包
    
    返回结构:
    {
        "context_blocks": [...],
        "interface_contracts": [
            {
                "function": "function_name",
                "signature": "...",
                "params": {...},
                "returns": "...",
                "source": "kb_xxx"
            }
        ],
        "project_constraints": [...],
        "anti_patterns": [
            {
                "pattern": "错误模式",
                "solution": "正确做法",
                "source": "error_pattern_xxx"
            }
        ],
        "code_templates": [...],
        "evidence_sufficient": true
    }
    """
    task = args["task"]
    file_path = args.get("file_path")
    module = args.get("module")
    min_evidence = args.get("min_evidence_count", 5)
    
    logger.info(f"处理代码任务: {task}, 文件: {file_path}, 模块: {module}")
    
    # 1. 检索代码相关证据
    code_query = f"{task} {module or ''} {file_path or ''}"
    answer_result = await handle_answer_with_evidence({
        "question": code_query,
        "mode": "code",
        "min_evidence_count": min_evidence,
        "max_context_blocks": 15
    })
    
    context_blocks = answer_result.get("context_blocks", [])
    
    # 2. 提取接口契约（从知识库中查找API文档）
    interface_contracts = []
    for block in context_blocks:
        if "api" in block.get("type", "").lower() or "api" in block.get("title", "").lower():
            # 尝试解析API文档
            interface_contracts.append({
                "function": block.get("title", ""),
                "signature": block.get("snippet", "")[:200],
                "source": block.get("id", "")
            })
    
    # 3. 项目约束
    project_constraints = [
        "所有文件路径必须使用绝对路径: /home/taotao/dev/QuantTest/TRQuant/...",
        "禁止使用worktree路径",
        "JQData finance表必须使用正确的查询方法（见知识库）",
        "代码必须包含错误处理和日志记录"
    ]
    
    # 4. 反例库（错误模式）
    anti_patterns = []
    try:
        error_results = error_pattern_search(error_msg=task)
        if error_results.get("success"):
            for item in error_results.get("results", [])[:5]:
                anti_patterns.append({
                    "pattern": item.get("error_pattern", ""),
                    "solution": item.get("solution", ""),
                    "source": item.get("id", "")
                })
    except Exception as e:
        logger.warning(f"错误模式搜索失败: {e}")
    
    # 5. 代码模板（从最佳实践中提取）
    code_templates = []
    for block in context_blocks:
        if block.get("type") == "practice":
            code_templates.append({
                "title": block.get("title", ""),
                "snippet": block.get("snippet", ""),
                "source": block.get("id", "")
            })
    
    evidence_sufficient = len(context_blocks) >= min_evidence
    
    return {
        "context_blocks": context_blocks,
        "interface_contracts": interface_contracts,
        "project_constraints": project_constraints,
        "anti_patterns": anti_patterns,
        "code_templates": code_templates,
        "evidence_sufficient": evidence_sufficient,
        "evidence_count": len(context_blocks),
        "min_required": min_evidence,
        "citation_format": "[KB:{doc_id}#{chunk_id}]"
    }


async def handle_verify_citations(args: Dict) -> Dict:
    """
    验证生成内容的引用覆盖率
    
    返回结构:
    {
        "coverage": 0.85,
        "verified_sentences": [
            {
                "sentence": "关键断言",
                "has_evidence": true,
                "evidence_ids": ["kb_xxx"],
                "confidence": 0.9
            }
        ],
        "unverified_sentences": [...],
        "pass": true,
        "recommendations": [...]
    }
    """
    content = args["content"]
    evidence_ids = args.get("evidence_ids", [])
    min_coverage = args.get("min_coverage", 0.7)
    
    # 简单实现：检查内容中是否包含引用标记
    # 实际应该用NLP提取关键断言，然后匹配证据
    
    # 提取引用标记 [KB:xxx]
    import re
    citation_pattern = r'\[KB:([^\]]+)\]'
    citations = re.findall(citation_pattern, content)
    
    # 计算覆盖率（简化版：基于引用数量）
    sentences = content.split('。')  # 简单分句
    verified_count = len(citations)
    total_sentences = len([s for s in sentences if len(s.strip()) > 10])  # 过滤太短的句子
    
    coverage = verified_count / max(total_sentences, 1)
    
    # 检查未验证的句子
    unverified_sentences = []
    for sentence in sentences:
        if len(sentence.strip()) > 20:  # 只检查有意义的句子
            # 检查是否包含技术术语（可能需要证据）
            tech_keywords = ["JQData", "API", "函数", "接口", "规范", "必须", "应该"]
            if any(kw in sentence for kw in tech_keywords):
                # 检查是否有引用
                if not any(cid in sentence for cid in evidence_ids):
                    unverified_sentences.append({
                        "sentence": sentence.strip(),
                        "reason": "包含技术术语但无引用"
                    })
    
    pass_verification = coverage >= min_coverage
    
    recommendations = []
    if not pass_verification:
        recommendations.append(f"覆盖率{coverage:.1%}低于阈值{min_coverage:.1%}，需要补充引用")
        recommendations.append(f"发现{len(unverified_sentences)}个未验证的关键断言")
    
    return {
        "coverage": coverage,
        "verified_citations": citations,
        "unverified_sentences": unverified_sentences,
        "pass": pass_verification,
        "min_coverage": min_coverage,
        "recommendations": recommendations
    }


# ============================================================================
# 主函数
# ============================================================================

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

