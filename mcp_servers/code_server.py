#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Code Server
===================

使用官方Python MCP SDK实现的代码搜索服务器
支持代码搜索、引用查找、定义查找

运行方式:
    python mcp_servers/code_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
"""

import sys
import json
import logging
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('CodeServer')

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
server = Server("trquant-code-server")

# 代码文件扩展名
CODE_EXTENSIONS = {'.py', '.ts', '.tsx', '.js', '.jsx', '.json', '.md'}

# 排除目录
EXCLUDE_DIRS = {
    '__pycache__', '.git', 'node_modules', 'venv', '.venv',
    'dist', 'build', '.pytest_cache', '.mypy_cache'
}


def is_code_file(file_path: Path) -> bool:
    """判断是否为代码文件"""
    return file_path.suffix in CODE_EXTENSIONS


def should_exclude(path: Path) -> bool:
    """判断是否应该排除"""
    parts = path.parts
    return any(part in EXCLUDE_DIRS for part in parts)


def search_code(query: str, file_pattern: Optional[str] = None, 
                search_type: str = "all", limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """
    搜索代码
    
    Args:
        query: 搜索关键词
        file_pattern: 文件模式（如 "*.py"）
        search_type: 搜索类型（"all", "function", "class", "variable"）
        limit: 最大返回结果数（默认100，防止输出过大）
        offset: 偏移量（用于分页）
    
    Returns:
        搜索结果列表（最多limit个）
    """
    results = []
    query_lower = query.lower()
    max_results = limit + offset  # 提前退出条件
    
    # 构建搜索路径
    search_paths = [TRQUANT_ROOT]
    
    # 根据文件模式过滤
    if file_pattern:
        # 简单的glob模式支持
        if file_pattern.startswith("*."):
            ext = file_pattern[1:]
            CODE_EXTENSIONS.add(ext)
    
    # 遍历文件
    for search_path in search_paths:
        for file_path in search_path.rglob("*"):
            if len(results) >= max_results:
                break  # 提前退出，避免不必要的遍历
            
            if not file_path.is_file():
                continue
            
            if should_exclude(file_path):
                continue
            
            if not is_code_file(file_path):
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    if len(results) >= max_results:
                        break
                    
                    if query_lower in line.lower():
                        # 根据搜索类型过滤
                        if search_type == "function" and not re.search(r'\bdef\s+\w*' + re.escape(query), line):
                            continue
                        if search_type == "class" and not re.search(r'\bclass\s+\w*' + re.escape(query), line):
                            continue
                        
                        results.append({
                            "file": str(file_path.relative_to(TRQUANT_ROOT)),
                            "line": i,
                            "content": line.strip(),
                            "context": "\n".join(lines[max(0, i-2):i+3])
                        })
            except Exception as e:
                logger.debug(f"读取文件失败: {file_path}, {e}")
                continue
        
        if len(results) >= max_results:
            break
    
    # 应用分页
    return results[offset:offset+limit]


def find_references(symbol: str, file_path: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """查找符号引用
    
    Args:
        symbol: 符号名称
        file_path: 文件路径（可选，用于限制搜索范围）
        limit: 最大返回结果数（默认100）
        offset: 偏移量（用于分页）
    
    Returns:
        引用结果列表（最多limit个）
    """
    results = []
    max_results = limit + offset
    
    # 构建搜索路径
    search_paths = [TRQUANT_ROOT / file_path] if file_path else [TRQUANT_ROOT]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        for file_path_obj in search_path.rglob("*"):
            if len(results) >= max_results:
                break
            
            if not file_path_obj.is_file():
                continue
            
            if should_exclude(file_path_obj):
                continue
            
            if not is_code_file(file_path_obj):
                continue
            
            try:
                content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # 简单的引用查找（可以改进）
                pattern = re.compile(r'\b' + re.escape(symbol) + r'\b')
                
                for i, line in enumerate(lines, 1):
                    if len(results) >= max_results:
                        break
                    
                    if pattern.search(line):
                        results.append({
                            "file": str(file_path_obj.relative_to(TRQUANT_ROOT)),
                            "line": i,
                            "content": line.strip(),
                            "context": "\n".join(lines[max(0, i-2):i+3])
                        })
            except Exception as e:
                logger.debug(f"读取文件失败: {file_path_obj}, {e}")
                continue
        
        if len(results) >= max_results:
            break
    
    # 应用分页
    return results[offset:offset+limit]


def find_definition(symbol: str, file_path: Optional[str] = None, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    """查找符号定义
    
    Args:
        symbol: 符号名称
        file_path: 文件路径（可选，用于限制搜索范围）
        limit: 最大返回结果数（默认100）
        offset: 偏移量（用于分页）
    
    Returns:
        定义结果列表（最多limit个）
    """
    results = []
    max_results = limit + offset
    
    # 构建搜索路径
    search_paths = [TRQUANT_ROOT / file_path] if file_path else [TRQUANT_ROOT]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
        
        for file_path_obj in search_path.rglob("*"):
            if len(results) >= max_results:
                break
            
            if not file_path_obj.is_file():
                continue
            
            if should_exclude(file_path_obj):
                continue
            
            if not is_code_file(file_path_obj):
                continue
            
            try:
                content = file_path_obj.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')
                
                # 查找定义（def, class, = 等）
                def_patterns = [
                    re.compile(r'\bdef\s+' + re.escape(symbol) + r'\s*\('),
                    re.compile(r'\bclass\s+' + re.escape(symbol) + r'\s*[(:]'),
                    re.compile(r'\b' + re.escape(symbol) + r'\s*='),
                ]
                
                for i, line in enumerate(lines, 1):
                    if len(results) >= max_results:
                        break
                    
                    for pattern in def_patterns:
                        if pattern.search(line):
                            results.append({
                                "file": str(file_path_obj.relative_to(TRQUANT_ROOT)),
                                "line": i,
                                "content": line.strip(),
                                "context": "\n".join(lines[max(0, i-2):i+3]),
                                "type": "definition"
                            })
                            break
            except Exception as e:
                logger.debug(f"读取文件失败: {file_path_obj}, {e}")
                continue
        
        if len(results) >= max_results:
            break
    
    # 应用分页
    return results[offset:offset+limit]


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="code.search",
            description="搜索代码（类/函数/变量）",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "file_pattern": {
                        "type": "string",
                        "description": "文件模式（如 '*.py'），可选"
                    },
                    "search_type": {
                        "type": "string",
                        "enum": ["all", "function", "class", "variable"],
                        "description": "搜索类型",
                        "default": "all"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最大返回结果数（默认100，防止输出过大）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 500
                    },
                    "offset": {
                        "type": "integer",
                        "description": "偏移量（用于分页）",
                        "default": 0,
                        "minimum": 0
                    },
                    "trace_id": {
                        "type": "string",
                        "description": "追踪ID（可选，用于E2E链路追踪）"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="code.references",
            description="查找符号引用",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "符号名称"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "文件路径（可选，用于限制搜索范围）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最大返回结果数（默认100）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 500
                    },
                    "offset": {
                        "type": "integer",
                        "description": "偏移量（用于分页）",
                        "default": 0,
                        "minimum": 0
                    },
                    "trace_id": {
                        "type": "string",
                        "description": "追踪ID（可选，用于E2E链路追踪）"
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="code.definition",
            description="查找符号定义",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "符号名称"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "文件路径（可选，用于限制搜索范围）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最大返回结果数（默认100）",
                        "default": 100,
                        "minimum": 1,
                        "maximum": 500
                    },
                    "offset": {
                        "type": "integer",
                        "description": "偏移量（用于分页）",
                        "default": 0,
                        "minimum": 0
                    },
                    "trace_id": {
                        "type": "string",
                        "description": "追踪ID（可选，用于E2E链路追踪）"
                    }
                },
                "required": ["symbol"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "code.search":
            # 获取分页参数
            limit = min(arguments.get("limit", 100), 500)  # 最大500
            offset = max(arguments.get("offset", 0), 0)
            
            # 只调用一次，避免重复执行
            results = search_code(
                arguments["query"],
                arguments.get("file_pattern"),
                arguments.get("search_type", "all"),
                limit=limit,
                offset=offset
            )
            
            result = {
                "query": arguments["query"],
                "file_pattern": arguments.get("file_pattern"),
                "search_type": arguments.get("search_type", "all"),
                "results": results,
                "limit": limit,
                "offset": offset,
                "returned_count": len(results),
                "has_more": len(results) == limit  # 如果返回数量等于limit，可能还有更多
            }
        elif name == "code.references":
            limit = min(arguments.get("limit", 100), 500)
            offset = max(arguments.get("offset", 0), 0)
            
            results = find_references(
                arguments["symbol"],
                arguments.get("file_path"),
                limit=limit,
                offset=offset
            )
            
            result = {
                "symbol": arguments["symbol"],
                "file_path": arguments.get("file_path"),
                "results": results,
                "limit": limit,
                "offset": offset,
                "returned_count": len(results),
                "has_more": len(results) == limit
            }
        elif name == "code.definition":
            limit = min(arguments.get("limit", 100), 500)
            offset = max(arguments.get("offset", 0), 0)
            
            results = find_definition(
                arguments["symbol"],
                arguments.get("file_path"),
                limit=limit,
                offset=offset
            )
            
            result = {
                "symbol": arguments["symbol"],
                "file_path": arguments.get("file_path"),
                "results": results,
                "limit": limit,
                "offset": offset,
                "returned_count": len(results),
                "has_more": len(results) == limit
            }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-code",
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
            server_name="trquant-code",
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
            server_name="trquant-code",
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
            server_name="trquant-code",
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



