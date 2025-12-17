# -*- coding: utf-8 -*-
"""任务优化MCP服务器（标准化版本）"""
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
logger = logging.getLogger('TaskOptimizerServer')

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

server = Server("task-optimizer-server")

TOOLS = [
    Tool(name="task.analyze", description="分析任务复杂度", inputSchema={"type": "object", "properties": {"task": {"type": "string"}}, "required": ["task"]}),
    Tool(name="task.recommend_mode", description="推荐执行模式", inputSchema={"type": "object", "properties": {"complexity": {"type": "string"}}, "required": ["complexity"]}),
    Tool(name="task.cache_context", description="缓存上下文", inputSchema={"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "object"}}, "required": ["key", "value"]}),
]

_context_cache = {}

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "task.analyze":
            task = arguments["task"]
            # 简单的复杂度分析
            complexity = "high" if len(task) > 100 or "策略" in task or "优化" in task else "low"
            result = {"success": True, "task": task[:50], "complexity": complexity, "estimated_tokens": len(task) * 2}
        elif name == "task.recommend_mode":
            complexity = arguments["complexity"]
            mode = "max" if complexity == "high" else "auto"
            result = {"success": True, "complexity": complexity, "recommended_mode": mode, "reason": "复杂任务需要Max模式" if mode == "max" else "简单任务可用Auto模式"}
        elif name == "task.cache_context":
            _context_cache[arguments["key"]] = arguments["value"]
            result = {"success": True, "key": arguments["key"], "cached": True}
        else:
            result = {"error": f"未知工具: {name}"}
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

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
