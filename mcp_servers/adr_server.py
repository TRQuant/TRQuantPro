#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant ADR Server
==================

使用官方Python MCP SDK实现的架构决策记录（ADR）服务器
管理架构决策文档

运行方式:
    python mcp_servers/adr_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
    - ADR格式规范
"""

import sys
import json
import logging
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('ADRServer')

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
server = Server("trquant-adr-server")

# ADR目录
ADR_DIR = TRQUANT_ROOT / "docs" / "adr"
ADR_DIR.mkdir(parents=True, exist_ok=True)

# ADR文件名模式
ADR_PATTERN = re.compile(r'^(\d{4})-(.+)\.md$')


def parse_adr_file(adr_file: Path) -> Dict[str, Any]:
    """解析ADR文件"""
    content = adr_file.read_text(encoding='utf-8')
    
    # 提取元数据
    metadata = {
        "number": None,
        "title": None,
        "status": None,
        "date": None,
        "deciders": [],
        "context": "",
        "decision": "",
        "consequences": []
    }
    
    lines = content.split('\n')
    in_context = False
    in_decision = False
    in_consequences = False
    
    for line in lines:
        line = line.strip()
        
        if line.startswith('# '):
            metadata["title"] = line[2:].strip()
        elif line.startswith('## Status'):
            in_context = False
            in_decision = False
            in_consequences = False
        elif line.startswith('## Context'):
            in_context = True
            in_decision = False
            in_consequences = False
        elif line.startswith('## Decision'):
            in_context = False
            in_decision = True
            in_consequences = False
        elif line.startswith('## Consequences'):
            in_context = False
            in_decision = False
            in_consequences = True
        elif line.startswith('- Status:'):
            metadata["status"] = line.split(':', 1)[1].strip()
        elif line.startswith('- Date:'):
            date_str = line.split(':', 1)[1].strip()
            try:
                metadata["date"] = datetime.fromisoformat(date_str).isoformat()
            except:
                metadata["date"] = date_str
        elif line.startswith('- Deciders:'):
            deciders_str = line.split(':', 1)[1].strip()
            metadata["deciders"] = [d.strip() for d in deciders_str.split(',')]
        elif in_context and line:
            metadata["context"] += line + "\n"
        elif in_decision and line:
            metadata["decision"] += line + "\n"
        elif in_consequences and line:
            metadata["consequences"].append(line)
    
    # 从文件名提取编号
    match = ADR_PATTERN.match(adr_file.name)
    if match:
        metadata["number"] = int(match.group(1))
    
    metadata["context"] = metadata["context"].strip()
    metadata["decision"] = metadata["decision"].strip()
    
    return metadata


def list_adrs() -> List[Dict[str, Any]]:
    """列出所有ADR文件"""
    adrs = []
    
    for adr_file in sorted(ADR_DIR.glob("*.md")):
        try:
            metadata = parse_adr_file(adr_file)
            metadata["file"] = adr_file.name
            metadata["path"] = str(adr_file.relative_to(TRQUANT_ROOT))
            metadata["size"] = adr_file.stat().st_size
            metadata["last_modified"] = datetime.fromtimestamp(adr_file.stat().st_mtime).isoformat()
            adrs.append(metadata)
        except Exception as e:
            logger.warning(f"无法解析ADR文件 {adr_file}: {e}")
    
    return sorted(adrs, key=lambda x: x.get("number", 0))


def read_adr(adr_number: Optional[int] = None, adr_title: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """读取ADR"""
    if adr_number:
        # 按编号查找
        pattern = f"{adr_number:04d}-*.md"
        matches = list(ADR_DIR.glob(pattern))
        if matches:
            adr_file = matches[0]
            metadata = parse_adr_file(adr_file)
            metadata["file"] = adr_file.name
            metadata["path"] = str(adr_file.relative_to(TRQUANT_ROOT))
            metadata["content"] = adr_file.read_text(encoding='utf-8')
            return metadata
    
    if adr_title:
        # 按标题查找
        for adr_file in ADR_DIR.glob("*.md"):
            metadata = parse_adr_file(adr_file)
            if adr_title.lower() in metadata.get("title", "").lower():
                metadata["file"] = adr_file.name
                metadata["path"] = str(adr_file.relative_to(TRQUANT_ROOT))
                metadata["content"] = adr_file.read_text(encoding='utf-8')
                return metadata
    
    return None


def create_adr(title: str, status: str = "Proposed", deciders: Optional[List[str]] = None) -> Dict[str, Any]:
    """创建新ADR"""
    # 找到下一个编号
    existing_numbers = []
    for adr_file in ADR_DIR.glob("*.md"):
        match = ADR_PATTERN.match(adr_file.name)
        if match:
            existing_numbers.append(int(match.group(1)))
    
    next_number = max(existing_numbers, default=0) + 1
    
    # 生成文件名
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '-').lower()
    filename = f"{next_number:04d}-{safe_title}.md"
    adr_file = ADR_DIR / filename
    
    # 创建ADR内容模板
    template = f"""# {next_number:04d}. {title}

## Status

- Status: {status}
- Date: {datetime.now().date().isoformat()}
- Deciders: {', '.join(deciders or [])}

## Context

<!-- 描述决策的背景和上下文 -->

## Decision

<!-- 描述所做的决策 -->

## Consequences

<!-- 描述决策的后果和影响 -->

"""
    
    adr_file.write_text(template, encoding='utf-8')
    
    return {
        "number": next_number,
        "title": title,
        "file": filename,
        "path": str(adr_file.relative_to(TRQUANT_ROOT)),
        "status": status,
        "created": datetime.now().isoformat()
    }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="adr.list",
            description="列出所有架构决策记录（ADR）",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "按状态筛选（可选）"
                    }
                }
            }
        ),
        Tool(
            name="adr.read",
            description="读取ADR内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "ADR编号"
                    },
                    "title": {
                        "type": "string",
                        "description": "ADR标题（部分匹配）"
                    }
                }
            }
        ),
        Tool(
            name="adr.create",
            description="创建新ADR",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "ADR标题"
                    },
                    "status": {
                        "type": "string",
                        "description": "状态（默认Proposed）",
                        "default": "Proposed"
                    },
                    "deciders": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "决策者列表"
                    }
                },
                "required": ["title"]
            }
        ),
        Tool(
            name="adr.search",
            description="搜索ADR",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "adr.list":
            adrs = list_adrs()
            status_filter = arguments.get("status")
            
            if status_filter:
                adrs = [adr for adr in adrs if adr.get("status", "").lower() == status_filter.lower()]
            
            result = {
                "adrs": adrs,
                "total": len(adrs),
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "adr.read":
            number = arguments.get("number")
            title = arguments.get("title")
            
            adr = read_adr(number, title)
            if not adr:
                raise ValueError(f"未找到ADR: number={number}, title={title}")
            
            result = adr
            
        elif name == "adr.create":
            title = arguments.get("title")
            status = arguments.get("status", "Proposed")
            deciders = arguments.get("deciders", [])
            
            if not title:
                raise ValueError("title参数是必需的")
            
            result = create_adr(title, status, deciders)
            
        elif name == "adr.search":
            query = arguments.get("query", "").lower()
            
            if not query:
                raise ValueError("query参数是必需的")
            
            adrs = list_adrs()
            matches = []
            
            for adr in adrs:
                # 搜索标题、上下文、决策内容
                content = f"{adr.get('title', '')} {adr.get('context', '')} {adr.get('decision', '')}".lower()
                if query in content:
                    matches.append(adr)
            
            result = {
                "query": query,
                "matches": matches,
                "total": len(matches),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-adr",
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
            server_name="trquant-adr",
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
            server_name="trquant-adr",
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
            server_name="trquant-adr",
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


