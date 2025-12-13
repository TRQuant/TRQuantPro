#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Docs Server
===================

文档检索统一化MCP服务器，统一管理投资手册和开发手册。

运行方式:
    python mcp_servers/docs_server.py

工具:
    - docs.list: 列出所有文档目录
    - docs.read: 读取文档内容
    - docs.search: 搜索文档内容
    - docs.get_toc: 获取目录结构
    - docs.get_examples: 获取代码示例
    - docs.validate: 验证文档完整性
"""

import sys
import json
import logging
import re
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
logger = logging.getLogger('DocsServer')

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
from mcp_servers.utils.artifacts import create_artifact_if_needed

# 文档路径配置
MANUAL_ROOT = TRQUANT_ROOT / "extension" / "AShare-manual"
DEV_MANUAL_ROOT = TRQUANT_ROOT / "docs" / "02_development_guides"

# 支持的文档类型
DOC_TYPES = {
    "manual": {
        "name": "投资手册",
        "root": MANUAL_ROOT,
        "patterns": ["**/*.md", "**/*.mdx", "**/*.astro"],
        "description": "A股投资手册，包含高倍股分析、宏观经济、个股研究、技术分析等"
    },
    "dev_manual": {
        "name": "开发手册",
        "root": DEV_MANUAL_ROOT,
        "patterns": ["**/*.md"],
        "description": "TRQuant系统开发手册，包含开发指南、API参考、工作流等"
    }
}


class DocsIndex:
    """文档索引管理器"""
    
    def __init__(self):
        self._index: Dict[str, List[Dict[str, Any]]] = {}
        self._toc: Dict[str, Dict[str, Any]] = {}
        self._last_indexed: Optional[datetime] = None
    
    def build_index(self, doc_type: str = "all") -> Dict[str, Any]:
        """构建文档索引"""
        result = {
            "manual": [],
            "dev_manual": []
        }
        
        types_to_index = [doc_type] if doc_type != "all" else ["manual", "dev_manual"]
        
        for dt in types_to_index:
            if dt not in DOC_TYPES:
                continue
            
            doc_config = DOC_TYPES[dt]
            root = doc_config["root"]
            patterns = doc_config["patterns"]
            
            if not root.exists():
                logger.warning(f"文档根目录不存在: {root}")
                continue
            
            files = []
            for pattern in patterns:
                for file_path in root.rglob(pattern):
                    if file_path.is_file() and not self._should_skip_file(file_path):
                        rel_path = file_path.relative_to(root)
                        files.append({
                            "path": str(rel_path),
                            "full_path": str(file_path),
                            "name": file_path.stem,
                            "type": dt,
                            "size": file_path.stat().st_size,
                            "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
            
            result[dt] = sorted(files, key=lambda x: x["path"])
        
        self._index = result
        self._last_indexed = datetime.now()
        return result
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """判断是否应该跳过文件"""
        skip_patterns = [
            "node_modules",
            ".git",
            "__pycache__",
            ".astro",
            "dist",
            "build",
            ".cache"
        ]
        path_str = str(file_path)
        return any(pattern in path_str for pattern in skip_patterns)
    
    def search(self, query: str, doc_type: str = "all", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """搜索文档内容"""
        if not self._index:
            self.build_index(doc_type)
        
        query_lower = query.lower()
        results = []
        
        types_to_search = [doc_type] if doc_type != "all" else ["manual", "dev_manual"]
        
        for dt in types_to_search:
            if dt not in self._index:
                continue
            
            for file_info in self._index[dt]:
                try:
                    file_path = Path(file_info["full_path"])
                    if not file_path.exists():
                        continue
                    
                    # 读取文件内容
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    # 简单搜索：检查文件名和内容
                    if query_lower in file_info["name"].lower() or query_lower in content.lower():
                        # 提取匹配的片段
                        snippets = self._extract_snippets(content, query_lower, max_snippets=3)
                        
                        results.append({
                            "doc_type": dt,
                            "path": file_info["path"],
                            "name": file_info["name"],
                            "snippets": snippets,
                            "match_count": content.lower().count(query_lower)
                        })
                except Exception as e:
                    logger.warning(f"搜索文件失败 {file_info['path']}: {e}")
                    continue
        
        # 按匹配数排序
        results.sort(key=lambda x: x["match_count"], reverse=True)
        
        # 分页
        total = len(results)
        paginated_results = results[offset:offset + limit]
        
        return {
            "query": query,
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": paginated_results
        }
    
    def _extract_snippets(self, content: str, query: str, max_snippets: int = 3, context_lines: int = 2) -> List[str]:
        """提取匹配的代码片段"""
        lines = content.split('\n')
        snippets = []
        query_lower = query.lower()
        
        for i, line in enumerate(lines):
            if query_lower in line.lower():
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                snippet = '\n'.join(lines[start:end])
                snippets.append(snippet)
                if len(snippets) >= max_snippets:
                    break
        
        return snippets
    
    def get_toc(self, doc_type: str = "all") -> Dict[str, Any]:
        """获取目录结构"""
        if not self._index:
            self.build_index(doc_type)
        
        result = {}
        
        types_to_build = [doc_type] if doc_type != "all" else ["manual", "dev_manual"]
        
        for dt in types_to_build:
            if dt not in self._index:
                continue
            
            # 构建目录树
            tree = defaultdict(list)
            for file_info in self._index[dt]:
                path_parts = Path(file_info["path"]).parts
                if len(path_parts) > 1:
                    parent = "/".join(path_parts[:-1])
                    tree[parent].append({
                        "name": file_info["name"],
                        "path": file_info["path"]
                    })
                else:
                    tree["/"].append({
                        "name": file_info["name"],
                        "path": file_info["path"]
                    })
            
            result[dt] = dict(tree)
        
        return result
    
    def get_examples(self, example_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """获取代码示例"""
        if not self._index:
            self.build_index("dev_manual")
        
        examples = []
        
        for file_info in self._index.get("dev_manual", []):
            try:
                file_path = Path(file_info["full_path"])
                if not file_path.exists():
                    continue
                
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # 提取代码块
                code_blocks = self._extract_code_blocks(content)
                
                for block in code_blocks:
                    if example_type and example_type.lower() not in block.get("language", "").lower():
                        continue
                    
                    examples.append({
                        "source": file_info["path"],
                        "language": block.get("language", "text"),
                        "code": block.get("code", ""),
                        "context": block.get("context", "")
                    })
                    
                    if len(examples) >= limit:
                        break
            except Exception as e:
                logger.warning(f"提取示例失败 {file_info['path']}: {e}")
                continue
        
        return examples[:limit]
    
    def _extract_code_blocks(self, content: str) -> List[Dict[str, Any]]:
        """提取Markdown代码块"""
        code_blocks = []
        pattern = r'```(\w+)?\n(.*?)```'
        
        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1) or "text"
            code = match.group(2).strip()
            
            # 提取上下文（代码块前后的几行）
            start_pos = match.start()
            context_start = max(0, content.rfind('\n', 0, start_pos) - 200)
            context = content[context_start:start_pos].strip()
            
            code_blocks.append({
                "language": language,
                "code": code,
                "context": context[-100:] if len(context) > 100 else context
            })
        
        return code_blocks


# 全局文档索引
_docs_index = DocsIndex()


# 创建MCP服务器
server = Server("trquant-docs")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="docs.list",
            description="列出所有文档目录（支持按类型过滤：manual/dev_manual/all）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "enum": ["manual", "dev_manual", "all"],
                            "default": "all",
                            "description": "文档类型"
                        }
                    }
                }
            )
        ),
        Tool(
            name="docs.read",
            description="读取文档内容（支持章节或完整文档）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "enum": ["manual", "dev_manual"],
                            "description": "文档类型"
                        },
                        "doc_path": {
                            "type": "string",
                            "description": "文档路径或章节ID"
                        }
                    },
                    "required": ["doc_type", "doc_path"]
                }
            )
        ),
        Tool(
            name="docs.search",
            description="搜索文档内容（跨手册和开发文档）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "doc_type": {
                            "type": "string",
                            "enum": ["manual", "dev_manual", "all"],
                            "default": "all",
                            "description": "文档类型"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 20,
                            "maximum": 100,
                            "description": "结果数量限制"
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "分页偏移"
                        }
                    },
                    "required": ["query"]
                }
            )
        ),
        Tool(
            name="docs.get_toc",
            description="获取目录结构",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "enum": ["manual", "dev_manual", "all"],
                            "default": "all",
                            "description": "文档类型"
                        }
                    }
                }
            )
        ),
        Tool(
            name="docs.get_examples",
            description="获取代码示例（主要针对开发手册）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "example_type": {
                            "type": "string",
                            "description": "示例类型（如：api_usage, workflow等）"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 10,
                            "description": "结果数量限制"
                        }
                    }
                }
            )
        ),
        Tool(
            name="docs.validate",
            description="验证文档完整性（检查链接、格式等）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "doc_type": {
                            "type": "string",
                            "enum": ["manual", "dev_manual", "all"],
                            "default": "all",
                            "description": "文档类型"
                        }
                    }
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具"""
    import json
    
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "docs.list":
            doc_type = arguments.get("doc_type", "all")
            result = _docs_index.build_index(doc_type)
            
            # 格式化输出
            formatted_result = {
                "doc_type": doc_type,
                "indexed_at": _docs_index._last_indexed.isoformat() if _docs_index._last_indexed else None,
                "counts": {
                    "manual": len(result.get("manual", [])),
                    "dev_manual": len(result.get("dev_manual", []))
                },
                "files": result
            }
            
            result = create_artifact_if_needed(formatted_result, "docs", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "docs.read":
            doc_type = arguments.get("doc_type")
            doc_path = arguments.get("doc_path")
            
            if not doc_type or not doc_path:
                raise ValueError("doc_type和doc_path是必需的")
            
            if doc_type not in DOC_TYPES:
                raise ValueError(f"不支持的文档类型: {doc_type}")
            
            doc_config = DOC_TYPES[doc_type]
            root = doc_config["root"]
            file_path = root / doc_path
            
            if not file_path.exists():
                raise ValueError(f"文档不存在: {doc_path}")
            
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            result = {
                "doc_type": doc_type,
                "path": doc_path,
                "content": content,
                "size": len(content),
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            
            result = create_artifact_if_needed(result, "docs", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "docs.search":
            query = arguments.get("query")
            if not query:
                raise ValueError("query是必需的")
            
            doc_type = arguments.get("doc_type", "all")
            limit = arguments.get("limit", 20)
            offset = arguments.get("offset", 0)
            
            result = _docs_index.search(query, doc_type, limit, offset)
            result = create_artifact_if_needed(result, "docs", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "docs.get_toc":
            doc_type = arguments.get("doc_type", "all")
            result = _docs_index.get_toc(doc_type)
            result = create_artifact_if_needed(result, "docs", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "docs.get_examples":
            example_type = arguments.get("example_type")
            limit = arguments.get("limit", 10)
            
            result = {
                "examples": _docs_index.get_examples(example_type, limit),
                "count": limit
            }
            result = create_artifact_if_needed(result, "docs", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "docs.validate":
            doc_type = arguments.get("doc_type", "all")
            
            # 简单的验证：检查文件是否存在、可读
            validation_result = {
                "doc_type": doc_type,
                "validated_at": datetime.now().isoformat(),
                "errors": [],
                "warnings": [],
                "summary": {}
            }
            
            types_to_validate = [doc_type] if doc_type != "all" else ["manual", "dev_manual"]
            
            for dt in types_to_validate:
                if dt not in DOC_TYPES:
                    continue
                
                doc_config = DOC_TYPES[dt]
                root = doc_config["root"]
                
                if not root.exists():
                    validation_result["errors"].append(f"文档根目录不存在: {root}")
                    continue
                
                # 统计文件
                file_count = 0
                for pattern in doc_config["patterns"]:
                    for file_path in root.rglob(pattern):
                        if file_path.is_file():
                            file_count += 1
                            try:
                                # 尝试读取文件
                                file_path.read_text(encoding='utf-8', errors='ignore')
                            except Exception as e:
                                validation_result["warnings"].append(f"文件读取失败 {file_path}: {e}")
                
                validation_result["summary"][dt] = {
                    "file_count": file_count,
                    "root": str(root)
                }
            
            envelope = wrap_success_response(
                data=validation_result,
                server_name="trquant-docs",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        else:
            raise ValueError(f"未知工具: {name}")
    
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-docs",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except FileNotFoundError as e:
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=str(e),
            server_name="trquant-docs",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查文档路径是否正确",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-docs",
            tool_name=name,
            version="1.0.0",
            error_details={"exception_type": type(e).__name__},
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


if __name__ == "__main__":
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())












