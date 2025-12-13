#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Spec Server (v2.0)
===========================

使用官方Python MCP SDK重构的Spec服务器
参考官方Git服务器实现

运行方式:
    python mcp_servers/spec_server_v2.py

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
from typing import Any, Dict, List, Optional

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('SpecServer')

# 导入官方MCP SDK（参考官方Git服务器实现）
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    # 添加utils路径以导入envelope
    TRQUANT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(TRQUANT_ROOT))
    from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
    
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK (Server)")
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# Spec目录
SPEC_DIR = TRQUANT_ROOT / "spec"
SPEC_FILES = {
    "product": "product.md",
    "domain": "domain.md",
    "api": "api.md",
    "ux": "ux.md",
    "arch": "arch.md",
    "acceptance": "acceptance.md"
}


def validate_spec_type(spec_type: str) -> bool:
    """验证spec类型"""
    return spec_type in SPEC_FILES


def read_spec_file(spec_type: str) -> str:
    """读取spec文件"""
    if not validate_spec_type(spec_type):
        raise ValueError(f"未知spec类型: {spec_type}")
    
    spec_file = SPEC_DIR / SPEC_FILES[spec_type]
    if not spec_file.exists():
        raise FileNotFoundError(f"Spec文件不存在: {spec_file}")
    
    return spec_file.read_text(encoding='utf-8')


def search_spec_content(query: str, spec_type: Optional[str] = None) -> List[Dict]:
    """搜索spec内容"""
    query_lower = query.lower()
    results = []
    
    files_to_search = [SPEC_FILES[spec_type]] if spec_type and spec_type != "all" else SPEC_FILES.values()
    
    for spec_file_name in files_to_search:
        spec_file = SPEC_DIR / spec_file_name
        if not spec_file.exists():
            continue
        
        content = spec_file.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if query_lower in line.lower():
                results.append({
                    "file": spec_file_name,
                    "line": i,
                    "content": line.strip(),
                    "context": "\n".join(lines[max(0, i-2):i+3])
                })
    
    return results


def list_specs() -> List[Dict]:
    """列出所有spec文件"""
    specs = []
    
    for spec_type, filename in SPEC_FILES.items():
        spec_file = SPEC_DIR / filename
        if spec_file.exists():
            stats = spec_file.stat()
            specs.append({
                "type": spec_type,
                "file": filename,
                "size": stats.st_size,
                "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
            })
    
    return specs


# 创建MCP服务器（参考官方Git服务器实现）
server = Server("trquant-spec-server")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="spec.read",
            description="读取spec文件（带版本号）",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_type": {
                        "type": "string",
                        "enum": ["product", "domain", "api", "ux", "arch", "acceptance"],
                        "description": "Spec文件类型"
                    }
                },
                "required": ["spec_type"]
            }
        ),
        Tool(
            name="spec.search",
            description="检索spec内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "spec_type": {
                        "type": "string",
                        "enum": ["product", "domain", "api", "ux", "arch", "acceptance", "all"],
                        "description": "Spec文件类型，'all'表示搜索所有文件"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="spec.list",
            description="列出所有spec文件",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="spec.validate",
            description="校验spec完整性",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_type": {
                        "type": "string",
                        "enum": ["product", "domain", "api", "ux", "arch", "acceptance", "all"],
                        "description": "Spec文件类型，'all'表示校验所有文件"
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "spec.read":
            if "spec_type" not in arguments:
                raise ValueError("缺少必需参数: spec_type")
            
            result = {
                "spec_type": arguments["spec_type"],
                "version": "latest",
                "file_path": str(SPEC_DIR / SPEC_FILES[arguments["spec_type"]]),
                "content": read_spec_file(arguments["spec_type"]),
                "last_modified": datetime.fromtimestamp(
                    (SPEC_DIR / SPEC_FILES[arguments["spec_type"]]).stat().st_mtime
                ).isoformat()
            }
        elif name == "spec.search":
            if "query" not in arguments:
                raise ValueError("缺少必需参数: query")
            
            result = {
                "query": arguments["query"],
                "spec_type": arguments.get("spec_type", "all"),
                "results": search_spec_content(arguments["query"], arguments.get("spec_type")),
                "total_matches": len(search_spec_content(arguments["query"], arguments.get("spec_type")))
            }
        elif name == "spec.list":
            specs = list_specs()
            result = {
                "specs": specs,
                "total": len(specs)
            }
        elif name == "spec.validate":
            spec_type = arguments.get("spec_type", "all")
            files_to_check = [SPEC_FILES[spec_type]] if spec_type != "all" else SPEC_FILES.values()
            results = []
            
            for spec_file_name in files_to_check:
                spec_file = SPEC_DIR / spec_file_name
                if not spec_file.exists():
                    results.append({
                        "file": spec_file_name,
                        "status": "missing",
                        "errors": ["文件不存在"]
                    })
                    continue
                
                content = spec_file.read_text(encoding='utf-8')
                errors = []
                
                if len(content) < 100:
                    errors.append("内容过短，可能不完整")
                
                if "#" not in content:
                    errors.append("缺少Markdown标题")
                
                results.append({
                    "file": spec_file_name,
                    "status": "valid" if not errors else "invalid",
                    "errors": errors,
                    "size": len(content)
                })
            
            result = {
                "spec_type": spec_type,
                "results": results,
                "all_valid": all(r["status"] == "valid" for r in results)
            }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-spec",
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
            server_name="trquant-spec",
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
            server_name="trquant-spec",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查spec文件是否存在",
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
            server_name="trquant-spec",
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


