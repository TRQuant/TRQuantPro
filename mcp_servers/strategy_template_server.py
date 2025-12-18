# -*- coding: utf-8 -*-
"""
策略模板MCP服务器（标准化版本）
============================
提供策略模板管理、代码生成、导出功能
"""

import logging
import json
from typing import Dict, List, Any
import sys
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入官方MCP SDK
try:
    from mcp.server.models import InitializationOptions
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    import sys
    print(f'官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}', file=sys.stderr)
    sys.exit(1)

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("strategy-template-server")


# ==================== 工具定义 ====================

TOOLS = [
    Tool(
        name="template.list",
        description="列出所有可用的策略模板",
        inputSchema={
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "模板类型: basic/advanced/all",
                    "default": "all"
                }
            }
        }
    ),
    Tool(
        name="template.get",
        description="获取指定模板的详细信息",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "模板名称"}
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="template.generate",
        description="使用模板生成策略代码",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "模板名称"},
                "params": {"type": "object", "description": "策略参数"},
                "platform": {
                    "type": "string",
                    "description": "目标平台: joinquant/ptrade/qmt",
                    "default": "joinquant"
                }
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="template.export",
        description="将策略代码导出为指定平台格式",
        inputSchema={
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "原始策略代码"},
                "platform": {"type": "string", "description": "目标平台"},
                "name": {"type": "string", "description": "策略名称"}
            },
            "required": ["code", "platform"]
        }
    ),
    Tool(
        name="template.params",
        description="获取模板的可配置参数",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "模板名称"}
            },
            "required": ["name"]
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "template.list":
            result = await _handle_list(arguments)
        elif name == "template.get":
            result = await _handle_get(arguments)
        elif name == "template.generate":
            result = await _handle_generate(arguments)
        elif name == "template.export":
            result = await _handle_export(arguments)
        elif name == "template.params":
            result = await _handle_params(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
        
    except Exception as e:
        logger.error(f"工具调用异常: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


# ==================== 工具处理函数 ====================

async def _handle_list(args: Dict) -> Dict:
    """列出模板"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import list_templates, list_advanced_templates, get_all_template_info
    
    template_type = args.get("type", "all")
    
    if template_type == "basic":
        templates = [{"name": t["category"], "description": t["description"]} 
                    for t in list_templates()]
    elif template_type == "advanced":
        from core.templates.advanced_templates import ADVANCED_TEMPLATES
        templates = [{"name": name, "description": t.description} 
                    for name, t in ADVANCED_TEMPLATES.items()]
    else:
        templates = get_all_template_info()
    
    return {
        "success": True,
        "count": len(templates),
        "templates": templates
    }


async def _handle_get(args: Dict) -> Dict:
    """获取模板详情"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import get_any_template
    
    name = args["name"]
    template = get_any_template(name)
    
    if template is None:
        return {"error": f"模板不存在: {name}"}
    
    # 获取参数信息
    params = []
    if hasattr(template, "params"):
        for p in template.params:
            params.append({
                "name": p.name,
                "type": p.type,
                "default": p.default,
                "description": p.description
            })
    
    return {
        "success": True,
        "name": name,
        "description": getattr(template, "description", ""),
        "params": params
    }


async def _handle_generate(args: Dict) -> Dict:
    """生成策略代码"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import get_any_template
    from core.templates.strategy_exporter import export_strategy
    
    name = args["name"]
    params = args.get("params", {})
    platform = args.get("platform", "joinquant")
    
    template = get_any_template(name)
    if template is None:
        return {"error": f"模板不存在: {name}"}
    
    # 生成代码
    code = template.generate_code(params)
    
    # 如果需要导出为其他平台
    if platform != "joinquant":
        code = export_strategy(code, platform, f"{name}策略")
    
    return {
        "success": True,
        "template": name,
        "platform": platform,
        "code": code
    }


async def _handle_export(args: Dict) -> Dict:
    """导出策略代码"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates.strategy_exporter import export_strategy, StrategyExporter
    
    code = args["code"]
    platform = args["platform"]
    name = args.get("name", "exported_strategy")
    
    exported = export_strategy(code, platform, name)
    
    # 保存文件
    exporter = StrategyExporter()
    filepath = exporter.save_strategy(exported, name, platform)
    
    return {
        "success": True,
        "platform": platform,
        "filepath": filepath,
        "code_length": len(exported)
    }


async def _handle_params(args: Dict) -> Dict:
    """获取模板参数"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.templates import get_any_template
    
    name = args["name"]
    template = get_any_template(name)
    
    if template is None:
        return {"error": f"模板不存在: {name}"}
    
    params = []
    if hasattr(template, "params"):
        for p in template.params:
            param_info = {
                "name": p.name,
                "type": p.type,
                "default": p.default,
                "description": p.description
            }
            if hasattr(p, "min_value") and p.min_value is not None:
                param_info["min"] = p.min_value
            if hasattr(p, "max_value") and p.max_value is not None:
                param_info["max"] = p.max_value
            params.append(param_info)
    
    return {
        "success": True,
        "template": name,
        "params": params
    }


# ==================== 主函数 ====================

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
