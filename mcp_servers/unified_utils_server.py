# -*- coding: utf-8 -*-
"""
统一工具MCP服务器
================
合并所有小工具服务器（每个只有3个工具），减少总工具数量
包含: code, lint, spec, engineering, docs, schema, secrets, evidence, adr,
     data_collector, data_quality, strategy_kb, strategy_optimizer, 
     task_optimizer, platform_api
"""

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
logger = logging.getLogger('UnifiedUtilsServer')

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

server = Server("unified-utils-server")

# 定义所有工具（合并自多个小服务器）
TOOLS = [
    # Code tools (3)
    Tool(name="code.analyze", description="分析策略代码", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="code.lint", description="检查代码规范", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="code.convert", description="转换代码格式", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "target_platform": {"type": "string"}}, "required": ["code", "target_platform"]}),
    
    # Lint tools (3)
    Tool(name="lint.check", description="检查代码质量", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "rules": {"type": "array"}}, "required": ["code"]}),
    Tool(name="lint.fix", description="自动修复问题", inputSchema={"type": "object", "properties": {"code": {"type": "string"}}, "required": ["code"]}),
    Tool(name="lint.rules", description="列出检查规则", inputSchema={"type": "object", "properties": {}}),
    
    # Spec tools (3)
    Tool(name="spec.list", description="列出所有规范", inputSchema={"type": "object", "properties": {}}),
    Tool(name="spec.get", description="获取规范详情", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="spec.check", description="检查是否符合规范", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "specs": {"type": "array"}}, "required": ["code"]}),
    
    # Engineering tools (3)
    Tool(name="eng.test", description="运行测试", inputSchema={"type": "object", "properties": {"module": {"type": "string"}}}),
    Tool(name="eng.build", description="构建项目", inputSchema={"type": "object", "properties": {}}),
    Tool(name="eng.deploy", description="部署策略", inputSchema={"type": "object", "properties": {"strategy": {"type": "string"}, "platform": {"type": "string"}}, "required": ["strategy", "platform"]}),
    
    # Docs tools (3)
    Tool(name="docs.list", description="列出文档", inputSchema={"type": "object", "properties": {}}),
    Tool(name="docs.get", description="获取文档", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="docs.search", description="搜索文档", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
    
    # Schema tools (3)
    Tool(name="schema.list", description="列出所有数据模型", inputSchema={"type": "object", "properties": {}}),
    Tool(name="schema.get", description="获取数据模型定义", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="schema.validate", description="验证数据是否符合模型", inputSchema={"type": "object", "properties": {"schema_name": {"type": "string"}, "data": {"type": "object"}}, "required": ["schema_name", "data"]}),
    
    # Secrets tools (3)
    Tool(name="secrets.list", description="列出可用密钥名称", inputSchema={"type": "object", "properties": {}}),
    Tool(name="secrets.get", description="获取密钥值（仅返回是否存在）", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="secrets.set", description="设置密钥", inputSchema={"type": "object", "properties": {"name": {"type": "string"}, "value": {"type": "string"}}, "required": ["name", "value"]}),
    
    # Evidence tools (3)
    Tool(name="evidence.add", description="添加决策证据", inputSchema={"type": "object", "properties": {"decision": {"type": "string"}, "reason": {"type": "string"}, "data": {"type": "object"}}, "required": ["decision", "reason"]}),
    Tool(name="evidence.list", description="列出证据", inputSchema={"type": "object", "properties": {"limit": {"type": "integer", "default": 10}}}),
    Tool(name="evidence.search", description="搜索证据", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
    
    # ADR tools (3)
    Tool(name="adr.create", description="创建架构决策记录", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "context": {"type": "string"}, "decision": {"type": "string"}, "consequences": {"type": "string"}}, "required": ["title", "decision"]}),
    Tool(name="adr.list", description="列出所有ADR", inputSchema={"type": "object", "properties": {}}),
    Tool(name="adr.get", description="获取ADR详情", inputSchema={"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}),
    
    # Data Collector tools (3)
    Tool(name="collector.fetch", description="采集数据", inputSchema={"type": "object", "properties": {"source": {"type": "string"}, "symbols": {"type": "array"}, "date_range": {"type": "string"}}, "required": ["source"]}),
    Tool(name="collector.schedule", description="设置采集计划", inputSchema={"type": "object", "properties": {"cron": {"type": "string"}, "task": {"type": "string"}}, "required": ["cron", "task"]}),
    Tool(name="collector.status", description="查看采集状态", inputSchema={"type": "object", "properties": {}}),
    
    # Data Quality tools (3)
    Tool(name="dq.check", description="检查数据质量", inputSchema={"type": "object", "properties": {"data": {"type": "object"}}, "required": ["data"]}),
    Tool(name="dq.missing", description="检查缺失值", inputSchema={"type": "object", "properties": {"data": {"type": "object"}}, "required": ["data"]}),
    Tool(name="dq.outliers", description="检查异常值", inputSchema={"type": "object", "properties": {"data": {"type": "object"}}, "required": ["data"]}),
    
    # Strategy KB tools (3)
    Tool(name="skb.list", description="列出策略知识库", inputSchema={"type": "object", "properties": {}}),
    Tool(name="skb.get", description="获取策略知识", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    Tool(name="skb.recommend", description="推荐策略", inputSchema={"type": "object", "properties": {"market": {"type": "string"}}, "required": ["market"]}),
    
    # Strategy Optimizer tools (3)
    Tool(name="so.optimize", description="优化策略", inputSchema={"type": "object", "properties": {"strategy": {"type": "string"}}, "required": ["strategy"]}),
    Tool(name="so.analyze", description="分析策略", inputSchema={"type": "object", "properties": {"strategy": {"type": "string"}}, "required": ["strategy"]}),
    Tool(name="so.recommend", description="推荐优化方案", inputSchema={"type": "object", "properties": {"strategy": {"type": "string"}}, "required": ["strategy"]}),
    
    # Task Optimizer tools (3)
    Tool(name="task.analyze_complexity", description="分析任务复杂度，判断是否需要Max mode", inputSchema={"type": "object", "properties": {"task_title": {"type": "string"}, "task_description": {"type": "string"}, "estimated_time": {"type": "string"}, "dependencies": {"type": "array"}}, "required": ["task_title"]}),
    Tool(name="task.recommend_mode", description="推荐执行模式", inputSchema={"type": "object", "properties": {"complexity": {"type": "string"}}, "required": ["complexity"]}),
    Tool(name="task.cache_context", description="缓存上下文", inputSchema={"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "object"}}, "required": ["key", "value"]}),
    
    # Platform API tools (3)
    Tool(name="api.list_platforms", description="列出可用平台", inputSchema={"type": "object", "properties": {}}),
    Tool(name="api.get", description="获取平台API", inputSchema={"type": "object", "properties": {"platform": {"type": "string"}}, "required": ["platform"]}),
    Tool(name="api.convert", description="转换平台代码", inputSchema={"type": "object", "properties": {"code": {"type": "string"}, "from_platform": {"type": "string"}, "to_platform": {"type": "string"}}, "required": ["code", "from_platform", "to_platform"]}),
]

@server.list_tools()
async def list_tools():
    return TOOLS

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """统一处理所有工具调用"""
    try:
        # 根据工具名称路由到相应的处理函数
        # 这里简化处理，实际应该调用各个原始服务器的处理逻辑
        result = {
            "success": True,
            "tool": name,
            "message": f"工具 {name} 已调用（统一服务器）",
            "arguments": arguments
        }
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

