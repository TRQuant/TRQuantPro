#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Data Source Server
==========================

使用官方Python MCP SDK实现的数据源管理服务器
统一数据接口，管理多个数据源

运行方式:
    python mcp_servers/data_source_server.py

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

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('DataSourceServer')

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
server = Server("trquant-data-source-server")

# 数据源配置目录
DATA_SOURCE_CONFIG_DIR = TRQUANT_ROOT / "config" / "data_sources"
DATA_SOURCE_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def list_data_sources() -> List[Dict[str, Any]]:
    """列出所有数据源"""
    data_sources = []
    
    # 常见数据源
    common_sources = [
        {
            "name": "jqdata",
            "type": "quant",
            "description": "聚宽数据",
            "status": "available",
            "features": ["stock_data", "factor_data", "financial_data"]
        },
        {
            "name": "akshare",
            "type": "quant",
            "description": "AKShare数据源",
            "status": "available",
            "features": ["stock_data", "financial_data", "macro_data"]
        },
        {
            "name": "tushare",
            "type": "quant",
            "description": "TuShare数据源",
            "status": "available",
            "features": ["stock_data", "financial_data"]
        },
        {
            "name": "mongodb",
            "type": "database",
            "description": "MongoDB数据库",
            "status": "available",
            "features": ["storage", "query"]
        }
    ]
    
    # 检查配置文件
    for config_file in DATA_SOURCE_CONFIG_DIR.glob("*.json"):
        try:
            config = json.loads(config_file.read_text(encoding='utf-8'))
            data_sources.append({
                "name": config.get("name", config_file.stem),
                "type": config.get("type", "unknown"),
                "description": config.get("description", ""),
                "status": config.get("status", "unknown"),
                "config_file": str(config_file.relative_to(TRQUANT_ROOT)),
                "features": config.get("features", [])
            })
        except Exception as e:
            logger.warning(f"无法读取数据源配置 {config_file}: {e}")
    
    # 合并常见数据源
    existing_names = {ds["name"] for ds in data_sources}
    for source in common_sources:
        if source["name"] not in existing_names:
            data_sources.append(source)
    
    return data_sources


def validate_data_query(query: Dict[str, Any]) -> Dict[str, Any]:
    """验证数据查询请求"""
    required_fields = ["data_source", "data_type"]
    
    for field in required_fields:
        if field not in query:
            return {
                "valid": False,
                "error": f"缺少必需字段: {field}"
            }
    
    data_source = query.get("data_source")
    data_type = query.get("data_type")
    
    # 验证数据源
    sources = list_data_sources()
    source_names = [s["name"] for s in sources]
    if data_source not in source_names:
        return {
            "valid": False,
            "error": f"未知数据源: {data_source}",
            "available_sources": source_names
        }
    
    # 验证数据类型
    valid_types = ["stock_data", "factor_data", "financial_data", "macro_data"]
    if data_type not in valid_types:
        return {
            "valid": False,
            "error": f"未知数据类型: {data_type}",
            "available_types": valid_types
        }
    
    return {
        "valid": True,
        "message": "查询请求有效"
    }


def get_data_source_info(data_source: str) -> Optional[Dict[str, Any]]:
    """获取数据源信息"""
    sources = list_data_sources()
    for source in sources:
        if source["name"] == data_source:
            return source
    return None


def manage_cache(action: str, key: Optional[str] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """管理数据缓存"""
    cache_dir = TRQUANT_ROOT / ".taorui" / "cache" / "data"
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    if action == "list":
        # 列出所有缓存
        cache_files = list(cache_dir.glob("*.json"))
        caches = []
        for cache_file in cache_files:
            try:
                cache_data = json.loads(cache_file.read_text(encoding='utf-8'))
                caches.append({
                    "key": cache_file.stem,
                    "size": cache_file.stat().st_size,
                    "created": cache_data.get("created", ""),
                    "expires": cache_data.get("expires", "")
                })
            except:
                pass
        return {"caches": caches, "total": len(caches)}
    
    elif action == "get" and key:
        # 获取缓存
        cache_file = cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                return json.loads(cache_file.read_text(encoding='utf-8'))
            except:
                return {"error": "无法读取缓存文件"}
        return {"error": "缓存不存在"}
    
    elif action == "set" and key and data:
        # 设置缓存
        cache_file = cache_dir / f"{key}.json"
        cache_data = {
            "key": key,
            "data": data,
            "created": datetime.now().isoformat(),
            "expires": data.get("expires", "")
        }
        cache_file.write_text(
            json.dumps(cache_data, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        return {"message": "缓存已设置", "key": key}
    
    elif action == "clear" and key:
        # 清除缓存
        cache_file = cache_dir / f"{key}.json"
        if cache_file.exists():
            cache_file.unlink()
            return {"message": "缓存已清除", "key": key}
        return {"error": "缓存不存在"}
    
    return {"error": "无效的操作"}


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="data.list_sources",
            description="列出所有可用的数据源",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="data.query",
            description="查询数据（验证请求，不实际执行）",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_source": {
                        "type": "string",
                        "description": "数据源名称（如jqdata、akshare、tushare）"
                    },
                    "data_type": {
                        "type": "string",
                        "enum": ["stock_data", "factor_data", "financial_data", "macro_data"],
                        "description": "数据类型"
                    },
                    "params": {
                        "type": "object",
                        "description": "查询参数（根据数据源和数据类型而定）"
                    }
                },
                "required": ["data_source", "data_type"]
            }
        ),
        Tool(
            name="data.validate",
            description="验证数据查询请求",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "object",
                        "description": "数据查询请求"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="data.cache",
            description="管理数据缓存",
            inputSchema={
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "get", "set", "clear"],
                        "description": "操作类型"
                    },
                    "key": {
                        "type": "string",
                        "description": "缓存键（get/set/clear时需要）"
                    },
                    "data": {
                        "type": "object",
                        "description": "缓存数据（set时需要）"
                    }
                },
                "required": ["action"]
            }
        ),
        Tool(
            name="data.source_info",
            description="获取数据源详细信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_source": {
                        "type": "string",
                        "description": "数据源名称"
                    }
                },
                "required": ["data_source"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "data.list_sources":
            sources = list_data_sources()
            result = {
                "sources": sources,
                "total": len(sources),
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "data.query":
            data_source = arguments.get("data_source")
            data_type = arguments.get("data_type")
            params = arguments.get("params", {})
            
            # 验证查询
            validation = validate_data_query({
                "data_source": data_source,
                "data_type": data_type
            })
            
            if not validation.get("valid"):
                result = {
                    "error": validation.get("error"),
                    "available_sources": validation.get("available_sources"),
                    "available_types": validation.get("available_types")
                }
            else:
                # 返回查询计划（不实际执行）
                result = {
                    "data_source": data_source,
                    "data_type": data_type,
                    "params": params,
                    "query_plan": {
                        "status": "validated",
                        "note": "实际数据查询需要通过数据源接口执行",
                        "recommended_interface": f"使用{data_source}数据源接口查询{data_type}"
                    },
                    "timestamp": datetime.now().isoformat()
                }
            
        elif name == "data.validate":
            query = arguments.get("query")
            if not query:
                raise ValueError("query参数是必需的")
            
            result = validate_data_query(query)
            
        elif name == "data.cache":
            action = arguments.get("action")
            key = arguments.get("key")
            data = arguments.get("data")
            
            if not action:
                raise ValueError("action参数是必需的")
            
            result = manage_cache(action, key, data)
            result["timestamp"] = datetime.now().isoformat()
            
        elif name == "data.source_info":
            data_source = arguments.get("data_source")
            if not data_source:
                raise ValueError("data_source参数是必需的")
            
            source_info = get_data_source_info(data_source)
            if not source_info:
                result = {
                    "error": f"未找到数据源: {data_source}",
                    "available_sources": [s["name"] for s in list_data_sources()]
                }
            else:
                result = {
                    "source": source_info,
                    "timestamp": datetime.now().isoformat()
                }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-data-source",
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
            server_name="trquant-data-source",
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
            server_name="trquant-data-source",
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
            server_name="trquant-data-source",
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


