#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Evidence Server
=======================

使用官方Python MCP SDK实现的证据链服务器
记录和管理开发证据（测试、性能、迁移脚本等）

运行方式:
    python mcp_servers/evidence_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
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
logger = logging.getLogger('EvidenceServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    # 添加utils路径以导入envelope
    TRQUANT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(TRQUANT_ROOT))
    from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
    
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError:
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 创建服务器
server = Server("trquant-evidence-server")

# 证据目录
EVIDENCE_DIR = TRQUANT_ROOT / ".taorui" / "artifacts" / "evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

# 证据类型枚举
class EvidenceType(str, Enum):
    TEST = "test"
    PERFORMANCE = "performance"
    MIGRATION = "migration"
    ROLLBACK = "rollback"
    VALIDATION = "validation"
    DOCUMENTATION = "documentation"


def record_evidence(
    title: str,
    evidence_type: str,
    content: str,
    related_change: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """记录证据"""
    evidence_id = f"evidence_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    evidence = {
        "id": evidence_id,
        "title": title,
        "type": evidence_type,
        "content": content,
        "related_change": related_change,
        "tags": tags or [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat()
    }
    
    # 保存证据文件
    evidence_file = EVIDENCE_DIR / f"{evidence_id}.json"
    evidence_file.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    return evidence


def query_evidence(
    evidence_type: Optional[str] = None,
    related_change: Optional[str] = None,
    tags: Optional[List[str]] = None,
    query: Optional[str] = None
) -> List[Dict[str, Any]]:
    """查询证据"""
    evidences = []
    
    for evidence_file in EVIDENCE_DIR.glob("*.json"):
        try:
            evidence = json.loads(evidence_file.read_text(encoding='utf-8'))
            
            # 过滤
            if evidence_type and evidence.get("type") != evidence_type:
                continue
            
            if related_change and evidence.get("related_change") != related_change:
                continue
            
            if tags:
                evidence_tags = evidence.get("tags", [])
                if not any(tag in evidence_tags for tag in tags):
                    continue
            
            if query:
                query_lower = query.lower()
                title = evidence.get("title", "").lower()
                content = evidence.get("content", "").lower()
                if query_lower not in title and query_lower not in content:
                    continue
            
            evidences.append(evidence)
        except Exception as e:
            logger.warning(f"无法读取证据文件 {evidence_file}: {e}")
    
    return sorted(evidences, key=lambda x: x.get("created", ""), reverse=True)


def link_evidence(evidence_id: str, related_evidence_ids: List[str]) -> Dict[str, Any]:
    """链接证据"""
    evidence_file = EVIDENCE_DIR / f"{evidence_id}.json"
    
    if not evidence_file.exists():
        raise ValueError(f"未找到证据: {evidence_id}")
    
    evidence = json.loads(evidence_file.read_text(encoding='utf-8'))
    evidence.setdefault("links", []).extend(related_evidence_ids)
    evidence["links"] = list(set(evidence["links"]))  # 去重
    evidence["updated"] = datetime.now().isoformat()
    
    evidence_file.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    return evidence


def get_evidence_chain(evidence_id: str) -> Dict[str, Any]:
    """获取证据链"""
    evidence_file = EVIDENCE_DIR / f"{evidence_id}.json"
    
    if not evidence_file.exists():
        raise ValueError(f"未找到证据: {evidence_id}")
    
    evidence = json.loads(evidence_file.read_text(encoding='utf-8'))
    chain = [evidence]
    
    # 递归获取链接的证据
    visited = {evidence_id}
    links = evidence.get("links", [])
    
    while links:
        next_id = links.pop(0)
        if next_id in visited:
            continue
        
        visited.add(next_id)
        linked_file = EVIDENCE_DIR / f"{next_id}.json"
        
        if linked_file.exists():
            try:
                linked_evidence = json.loads(linked_file.read_text(encoding='utf-8'))
                chain.append(linked_evidence)
                links.extend(linked_evidence.get("links", []))
            except:
                pass
    
    return {
        "root": evidence_id,
        "chain": chain,
        "total": len(chain)
    }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="evidence.record",
            description="记录证据（测试、性能、迁移脚本等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "证据标题"
                    },
                    "type": {
                        "type": "string",
                        "enum": ["test", "performance", "migration", "rollback", "validation", "documentation"],
                        "description": "证据类型"
                    },
                    "content": {
                        "type": "string",
                        "description": "证据内容（测试结果、性能数据、脚本等）"
                    },
                    "related_change": {
                        "type": "string",
                        "description": "相关变更ID或描述（可选）"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "标签列表（可选）"
                    }
                },
                "required": ["title", "type", "content"]
            }
        ),
        Tool(
            name="evidence.query",
            description="查询证据",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["test", "performance", "migration", "rollback", "validation", "documentation"],
                        "description": "按类型筛选（可选）"
                    },
                    "related_change": {
                        "type": "string",
                        "description": "按相关变更筛选（可选）"
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "按标签筛选（可选）"
                    },
                    "query": {
                        "type": "string",
                        "description": "搜索关键词（可选）"
                    }
                }
            }
        ),
        Tool(
            name="evidence.link",
            description="链接证据",
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence_id": {
                        "type": "string",
                        "description": "证据ID"
                    },
                    "related_evidence_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "相关证据ID列表"
                    }
                },
                "required": ["evidence_id", "related_evidence_ids"]
            }
        ),
        Tool(
            name="evidence.chain",
            description="获取证据链",
            inputSchema={
                "type": "object",
                "properties": {
                    "evidence_id": {
                        "type": "string",
                        "description": "证据ID"
                    }
                },
                "required": ["evidence_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "evidence.record":
            title = arguments.get("title")
            evidence_type = arguments.get("type")
            content = arguments.get("content")
            related_change = arguments.get("related_change")
            tags = arguments.get("tags", [])
            
            if not title or not evidence_type or not content:
                raise ValueError("title, type, content参数是必需的")
            
            evidence = record_evidence(title, evidence_type, content, related_change, tags)
            
            result = {
                "evidence": evidence,
                "message": "证据已记录",
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "evidence.query":
            evidence_type = arguments.get("type")
            related_change = arguments.get("related_change")
            tags = arguments.get("tags")
            query = arguments.get("query")
            
            evidences = query_evidence(evidence_type, related_change, tags, query)
            
            result = {
                "evidences": evidences,
                "total": len(evidences),
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "evidence.link":
            evidence_id = arguments.get("evidence_id")
            related_evidence_ids = arguments.get("related_evidence_ids", [])
            
            if not evidence_id or not related_evidence_ids:
                raise ValueError("evidence_id和related_evidence_ids参数是必需的")
            
            evidence = link_evidence(evidence_id, related_evidence_ids)
            
            result = {
                "evidence": evidence,
                "message": "证据已链接",
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "evidence.chain":
            evidence_id = arguments.get("evidence_id")
            if not evidence_id:
                raise ValueError("evidence_id参数是必需的")
            
            chain = get_evidence_chain(evidence_id)
            result = chain
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-evidence",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        
        return [TextContent(
            type="text",
            text=json.dumps(envelope, ensure_ascii=False, indent=2)
        )]
    except ValueError as e:
        # 参数验证错误
        logger.error(f"工具执行失败: {name}, 错误: {e}")
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-evidence",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数是否符合工具Schema要求",
            trace_id=trace_id
        )
        return [TextContent(
            type="text",
            text=json.dumps(envelope, ensure_ascii=False, indent=2)
        )]
    except FileNotFoundError as e:
        # 文件不存在错误
        logger.error(f"工具执行失败: {name}, 错误: {e}")
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=str(e),
            server_name="trquant-evidence",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查文件是否存在",
            trace_id=trace_id
        )
        return [TextContent(
            type="text",
            text=json.dumps(envelope, ensure_ascii=False, indent=2)
        )]
    except Exception as e:
        # 其他内部错误
        logger.error(f"工具执行失败: {name}, 错误: {e}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-evidence",
            tool_name=name,
            version="1.0.0",
            error_details={"exception_type": type(e).__name__},
            trace_id=trace_id
        )
        return [TextContent(
            type="text",
            text=json.dumps(envelope, ensure_ascii=False, indent=2)
        )]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    # 使用官方SDK的标准方式
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())


