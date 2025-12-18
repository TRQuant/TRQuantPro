# -*- coding: utf-8 -*-
"""文档MCP服务器（标准化版本）"""
import sys
import logging
import json
from pathlib import Path
from typing import Dict, List, Any

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
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError as e:
    logger.error(f"官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}")
    sys.exit(1)

server = Server("docs-server")

TOOLS = [
    Tool(name="docs.list", description="列出所有文档", inputSchema={"type": "object", "properties": {"category": {"type": "string"}}}),
    Tool(name="docs.get", description="获取文档内容", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="docs.search", description="搜索文档", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        docs_dir = Path(__file__).parent.parent / "docs"
        if name == "docs.list":
            docs = list(docs_dir.glob("*.md")) if docs_dir.exists() else []
            result = {"success": True, "count": len(docs), "docs": [d.name for d in docs[:20]]}
        elif name == "docs.get":
            doc_path = docs_dir / arguments["name"]
            if doc_path.exists():
                content = doc_path.read_text(encoding="utf-8")[:2000]
                result = {"success": True, "name": arguments["name"], "content": content}
            else:
                result = {"success": False, "error": "文档不存在"}
        elif name == "docs.search":
            query = arguments["query"].lower()
            matches = []
            if docs_dir.exists():
                for doc in docs_dir.glob("*.md"):
                    if query in doc.name.lower() or query in doc.read_text(encoding="utf-8").lower()[:1000]:
                        matches.append(doc.name)
            result = {"success": True, "query": query, "matches": matches[:10]}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
