#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Schema Server
======================

使用官方Python MCP SDK实现的Schema校验服务器
支持JSON Schema、OpenAPI、Pydantic模型校验

运行方式:
    python mcp_servers/schema_server.py

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
logger = logging.getLogger('SchemaServer')

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

# 尝试导入JSON Schema库
try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    logger.warning("jsonschema未安装，部分功能将不可用")

# 尝试导入Pydantic
try:
    from pydantic import BaseModel, ValidationError
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    logger.warning("pydantic未安装，部分功能将不可用")

# 创建服务器
server = Server("trquant-schema-server")

# Schema目录
SCHEMA_DIR = TRQUANT_ROOT / "schemas"
SCHEMA_DIR.mkdir(exist_ok=True)


def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """使用JSON Schema验证数据"""
    if not JSONSCHEMA_AVAILABLE:
        return {
            "success": False,
            "error": "jsonschema未安装，请运行: pip install jsonschema"
        }
    
    try:
        jsonschema.validate(instance=data, schema=schema)
        return {
            "success": True,
            "valid": True,
            "errors": []
        }
    except jsonschema.ValidationError as e:
        return {
            "success": True,
            "valid": False,
            "errors": [{
                "path": list(e.path),
                "message": e.message,
                "validator": e.validator
            }]
        }
    except jsonschema.SchemaError as e:
        return {
            "success": False,
            "error": f"Schema错误: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"验证失败: {str(e)}"
        }


def load_schema_file(schema_path: str) -> Optional[Dict[str, Any]]:
    """加载Schema文件"""
    schema_file = Path(schema_path)
    
    if not schema_file.is_absolute():
        # 相对路径，尝试多个位置
        possible_paths = [
            SCHEMA_DIR / schema_path,
            TRQUANT_ROOT / schema_path,
            Path(schema_path)
        ]
        
        for path in possible_paths:
            if path.exists():
                schema_file = path
                break
        else:
            return None
    
    if not schema_file.exists():
        return None
    
    try:
        return json.loads(schema_file.read_text(encoding='utf-8'))
    except Exception as e:
        logger.error(f"加载Schema文件失败: {e}")
        return None


def compare_schemas(schema1: Dict[str, Any], schema2: Dict[str, Any]) -> Dict[str, Any]:
    """对比两个Schema的差异"""
    def get_properties(schema: Dict[str, Any]) -> Dict[str, Any]:
        """提取Schema的属性"""
        if "properties" in schema:
            return schema["properties"]
        return {}
    
    def get_required(schema: Dict[str, Any]) -> List[str]:
        """提取必需字段"""
        return schema.get("required", [])
    
    props1 = get_properties(schema1)
    props2 = get_properties(schema2)
    required1 = set(get_required(schema1))
    required2 = set(get_required(schema2))
    
    # 找出差异
    added = set(props2.keys()) - set(props1.keys())
    removed = set(props1.keys()) - set(props2.keys())
    changed = []
    
    for key in set(props1.keys()) & set(props2.keys()):
        if props1[key] != props2[key]:
            changed.append(key)
    
    required_added = required2 - required1
    required_removed = required1 - required2
    
    return {
        "properties": {
            "added": list(added),
            "removed": list(removed),
            "changed": changed
        },
        "required": {
            "added": list(required_added),
            "removed": list(required_removed)
        },
        "breaking_changes": len(removed) > 0 or len(required_added) > 0,
        "summary": {
            "total_added": len(added),
            "total_removed": len(removed),
            "total_changed": len(changed)
        }
    }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="schema.validate",
            description="校验数据是否符合Schema（JSON Schema）",
            inputSchema={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "description": "要验证的数据（JSON对象）"
                    },
                    "schema": {
                        "type": "object",
                        "description": "JSON Schema定义（JSON对象）"
                    },
                    "schema_path": {
                        "type": "string",
                        "description": "Schema文件路径（相对项目根目录或schemas目录）"
                    }
                },
                "required": ["data"]
            }
        ),
        Tool(
            name="schema.check",
            description="检查API变更（对比两个Schema）",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema1_path": {
                        "type": "string",
                        "description": "旧Schema文件路径"
                    },
                    "schema2_path": {
                        "type": "string",
                        "description": "新Schema文件路径"
                    },
                    "schema1": {
                        "type": "object",
                        "description": "旧Schema定义（JSON对象）"
                    },
                    "schema2": {
                        "type": "object",
                        "description": "新Schema定义（JSON对象）"
                    }
                },
                "required": ["schema1_path", "schema2_path"]
            }
        ),
        Tool(
            name="schema.diff",
            description="对比Schema差异（详细对比）",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema1_path": {
                        "type": "string",
                        "description": "Schema1文件路径"
                    },
                    "schema2_path": {
                        "type": "string",
                        "description": "Schema2文件路径"
                    }
                },
                "required": ["schema1_path", "schema2_path"]
            }
        ),
        Tool(
            name="schema.list",
            description="列出所有Schema文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Schema目录路径（相对项目根目录），默认schemas"
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
        if name == "schema.validate":
            data = arguments.get("data")
            schema = arguments.get("schema")
            schema_path = arguments.get("schema_path")
            
            # 如果没有提供schema，尝试从文件加载
            if not schema and schema_path:
                schema = load_schema_file(schema_path)
                if not schema:
                    raise ValueError(f"无法加载Schema文件: {schema_path}")
            
            if not schema:
                raise ValueError("必须提供schema或schema_path参数")
            
            if not data:
                raise ValueError("必须提供data参数")
            
            result = validate_json_schema(data, schema)
            result["timestamp"] = datetime.now().isoformat()
            
        elif name == "schema.check":
            schema1_path = arguments.get("schema1_path")
            schema2_path = arguments.get("schema2_path")
            schema1 = arguments.get("schema1")
            schema2 = arguments.get("schema2")
            
            # 加载Schema
            if not schema1 and schema1_path:
                schema1 = load_schema_file(schema1_path)
            if not schema2 and schema2_path:
                schema2 = load_schema_file(schema2_path)
            
            if not schema1:
                raise ValueError(f"无法加载Schema1: {schema1_path}")
            if not schema2:
                raise ValueError(f"无法加载Schema2: {schema2_path}")
            
            diff = compare_schemas(schema1, schema2)
            result = {
                "schema1_path": schema1_path,
                "schema2_path": schema2_path,
                "diff": diff,
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "schema.diff":
            schema1_path = arguments.get("schema1_path")
            schema2_path = arguments.get("schema2_path")
            
            schema1 = load_schema_file(schema1_path)
            schema2 = load_schema_file(schema2_path)
            
            if not schema1:
                raise ValueError(f"无法加载Schema1: {schema1_path}")
            if not schema2:
                raise ValueError(f"无法加载Schema2: {schema2_path}")
            
            diff = compare_schemas(schema1, schema2)
            
            # 添加详细对比
            result = {
                "schema1_path": schema1_path,
                "schema2_path": schema2_path,
                "diff": diff,
                "schema1": schema1,
                "schema2": schema2,
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "schema.list":
            directory = arguments.get("directory", "schemas")
            schema_dir = TRQUANT_ROOT / directory
            
            if not schema_dir.exists():
                result = {
                    "directory": str(schema_dir),
                    "schemas": [],
                    "message": "目录不存在"
                }
            else:
                schemas = []
                for schema_file in schema_dir.glob("*.json"):
                    try:
                        schema_data = json.loads(schema_file.read_text(encoding='utf-8'))
                        schemas.append({
                            "file": schema_file.name,
                            "path": str(schema_file.relative_to(TRQUANT_ROOT)),
                            "title": schema_data.get("title", ""),
                            "type": schema_data.get("type", ""),
                            "size": schema_file.stat().st_size,
                            "last_modified": datetime.fromtimestamp(schema_file.stat().st_mtime).isoformat()
                        })
                    except Exception as e:
                        logger.warning(f"无法读取Schema文件 {schema_file}: {e}")
                
                result = {
                    "directory": str(schema_dir.relative_to(TRQUANT_ROOT)),
                    "schemas": schemas,
                    "total": len(schemas),
                    "timestamp": datetime.now().isoformat()
                }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-schema",
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
            server_name="trquant-schema",
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
            server_name="trquant-schema",
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
            server_name="trquant-schema",
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


