# -*- coding: utf-8 -*-
"""
配置MCP服务器（标准化版本）
===========================
管理系统配置、策略参数、数据源配置
"""

import logging
import json
from typing import Dict, List, Any
from pathlib import Path
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("config-server")


# 默认配置
DEFAULT_CONFIG = {
    "backtest": {
        "initial_capital": 1000000,
        "commission_rate": 0.0003,
        "slippage": 0.001,
        "benchmark": "000300.XSHG"
    },
    "strategy": {
        "max_stocks": 10,
        "single_position": 0.1,
        "stop_loss": 0.08,
        "take_profit": 0.20,
        "rebalance_days": 5
    },
    "data": {
        "default_source": "akshare",
        "cache_enabled": True,
        "cache_ttl": 3600
    },
    "system": {
        "log_level": "INFO",
        "parallel_workers": 4
    }
}


TOOLS = [
    Tool(
        name="config.get",
        description="获取配置项",
        inputSchema={
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "配置分区"},
                "key": {"type": "string", "description": "配置键（可选）"}
            }
        }
    ),
    Tool(
        name="config.set",
        description="设置配置项",
        inputSchema={
            "type": "object",
            "properties": {
                "section": {"type": "string"},
                "key": {"type": "string"},
                "value": {"description": "配置值"}
            },
            "required": ["section", "key", "value"]
        }
    ),
    Tool(
        name="config.list",
        description="列出所有配置",
        inputSchema={"type": "object", "properties": {}}
    ),
    Tool(
        name="config.reset",
        description="重置为默认配置",
        inputSchema={
            "type": "object",
            "properties": {
                "section": {"type": "string", "description": "要重置的分区（可选，不填则全部重置）"}
            }
        }
    ),
    Tool(
        name="config.validate",
        description="验证配置有效性",
        inputSchema={"type": "object", "properties": {}}
    )
]


# 当前配置
_current_config = DEFAULT_CONFIG.copy()


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "config.get":
            result = await _handle_get(arguments)
        elif name == "config.set":
            result = await _handle_set(arguments)
        elif name == "config.list":
            result = await _handle_list()
        elif name == "config.reset":
            result = await _handle_reset(arguments)
        elif name == "config.validate":
            result = await _handle_validate()
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_get(args: Dict) -> Dict:
    section = args.get("section")
    key = args.get("key")
    
    if not section:
        return {"success": True, "config": _current_config}
    
    if section not in _current_config:
        return {"success": False, "error": f"分区不存在: {section}"}
    
    if key:
        if key not in _current_config[section]:
            return {"success": False, "error": f"配置项不存在: {section}.{key}"}
        return {
            "success": True,
            "section": section,
            "key": key,
            "value": _current_config[section][key]
        }
    
    return {
        "success": True,
        "section": section,
        "config": _current_config[section]
    }


async def _handle_set(args: Dict) -> Dict:
    global _current_config
    
    section = args["section"]
    key = args["key"]
    value = args["value"]
    
    if section not in _current_config:
        _current_config[section] = {}
    
    old_value = _current_config[section].get(key)
    _current_config[section][key] = value
    
    return {
        "success": True,
        "section": section,
        "key": key,
        "old_value": old_value,
        "new_value": value
    }


async def _handle_list() -> Dict:
    sections = list(_current_config.keys())
    total_keys = sum(len(v) for v in _current_config.values())
    
    return {
        "success": True,
        "sections": sections,
        "total_keys": total_keys,
        "config": _current_config
    }


async def _handle_reset(args: Dict) -> Dict:
    global _current_config
    
    section = args.get("section")
    
    if section:
        if section in DEFAULT_CONFIG:
            _current_config[section] = DEFAULT_CONFIG[section].copy()
            return {"success": True, "message": f"已重置分区: {section}"}
        else:
            return {"success": False, "error": f"分区不存在: {section}"}
    
    _current_config = {k: v.copy() for k, v in DEFAULT_CONFIG.items()}
    return {"success": True, "message": "已重置所有配置"}


async def _handle_validate() -> Dict:
    issues = []
    
    # 验证回测配置
    bt = _current_config.get("backtest", {})
    if bt.get("initial_capital", 0) < 10000:
        issues.append("初始资金过低（建议>=10000）")
    if bt.get("commission_rate", 0) > 0.01:
        issues.append("佣金率过高（建议<=1%）")
    
    # 验证策略配置
    st = _current_config.get("strategy", {})
    if st.get("max_stocks", 0) < 3:
        issues.append("持股数过少（建议>=3）")
    if st.get("single_position", 0) > 0.3:
        issues.append("单票仓位过高（建议<=30%）")
    if st.get("stop_loss", 0) > 0.15:
        issues.append("止损线过宽（建议<=15%）")
    
    return {
        "success": len(issues) == 0,
        "valid": len(issues) == 0,
        "issues": issues,
        "message": "配置验证通过" if not issues else f"发现{len(issues)}个问题"
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="config-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
