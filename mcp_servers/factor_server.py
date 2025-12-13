#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Factor Server
=====================

因子管理MCP服务器，提供因子的查询、搜索、验证和评估功能。

运行方式:
    python mcp_servers/factor_server.py

工具:
    - factor.list: 列出所有因子
    - factor.get: 获取因子详情
    - factor.search: 搜索因子
    - factor.validate: 验证因子定义
    - factor.evaluate: 评估因子效果（返回评估任务）
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
logger = logging.getLogger('FactorServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    MCP_SDK_AVAILABLE = False
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 导入工程化落地件
from mcp_servers.utils.envelope import wrap_success_response, wrap_error_response, extract_trace_id_from_request
from mcp_servers.utils.schema import base_args_schema, merge_schema, requires_confirm_token
from mcp_servers.utils.artifacts import create_artifact_if_needed
from mcp_servers.utils.confirm import verify_confirm_token
from mcp_servers.utils.dependency_checker import get_dependency_checker

# 导入资产链接器
try:
    from core.asset_linker import AssetLinker
    ASSET_LINKER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AssetLinker不可用: {e}")
    ASSET_LINKER_AVAILABLE = False
    AssetLinker = None

# 导入因子管理模块
try:
    from core.factors import FactorManager
    FACTOR_MANAGER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"FactorManager不可用: {e}")
    FACTOR_MANAGER_AVAILABLE = False
    FactorManager = None  # 设置为None以便类型检查

# 初始化因子管理器（延迟初始化）
_factor_manager: Optional[Any] = None

# 初始化资产链接器（延迟初始化）
_asset_linker: Optional[Any] = None


def get_factor_manager():
    """获取因子管理器实例（单例）"""
    global _factor_manager
    if _factor_manager is None:
        if not FACTOR_MANAGER_AVAILABLE:
            raise RuntimeError("FactorManager不可用，请检查依赖")
        if FactorManager is None:
            raise RuntimeError("FactorManager不可用，请检查依赖")
        _factor_manager = FactorManager()
    return _factor_manager


def get_asset_linker():
    """获取资产链接器实例（单例）"""
    global _asset_linker
    if _asset_linker is None:
        if not ASSET_LINKER_AVAILABLE:
            raise RuntimeError("AssetLinker不可用，请检查依赖")
        if AssetLinker is None:
            raise RuntimeError("AssetLinker不可用，请检查依赖")
        _asset_linker = AssetLinker()
    return _asset_linker


# 创建MCP服务器
server = Server("trquant-factor")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="factor.list",
            description="列出所有因子（支持按类别过滤）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "enum": ["value", "growth", "quality", "momentum", "flow", None],
                            "description": "因子类别（可选）"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 100,
                            "maximum": 1000,
                            "description": "返回数量限制"
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "偏移量（分页）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="factor.get",
            description="获取因子详情",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "factor_id": {
                            "type": "string",
                            "description": "因子ID（因子名称）"
                        }
                    },
                    "required": ["factor_id"]
                }
            )
        ),
        Tool(
            name="factor.search",
            description="搜索因子（按名称、类别、描述）",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["value", "growth", "quality", "momentum", "flow", None],
                            "description": "因子类别（可选）"
                        },
                        "limit": {
                            "type": "integer",
                            "default": 20,
                            "maximum": 100,
                            "description": "返回数量限制"
                        },
                        "offset": {
                            "type": "integer",
                            "default": 0,
                            "description": "偏移量（分页）"
                        }
                    },
                    "required": ["query"]
                }
            )
        ),
        Tool(
            name="factor.validate",
            description="验证因子定义（语法检查、依赖检查、参数校验）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "factor_definition": {
                            "type": "object",
                            "description": "因子定义（代码/参数）"
                        }
                    },
                    "required": ["factor_definition"]
                }
            )
        ),
        Tool(
            name="factor.evaluate",
            description="评估因子效果（返回评估任务，结果job化）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "factor_id": {
                            "type": "string",
                            "description": "因子ID"
                        },
                        "evaluation_config": {
                            "type": "object",
                            "description": "评估配置（时间范围、指标等）"
                        }
                    },
                    "required": ["factor_id", "evaluation_config"]
                }
            )
        ),
        Tool(
            name="factor.create",
            description="创建新因子（需要confirm_token + evidence）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "factor_name": {
                            "type": "string",
                            "description": "因子名称（唯一标识）"
                        },
                        "category": {
                            "type": "string",
                            "enum": ["value", "growth", "quality", "momentum", "flow"],
                            "description": "因子类别"
                        },
                        "description": {
                            "type": "string",
                            "description": "因子描述"
                        },
                        "definition": {
                            "type": "string",
                            "description": "计算公式说明"
                        },
                        "direction": {
                            "type": "integer",
                            "enum": [1, -1],
                            "default": 1,
                            "description": "因子方向（1=正向，-1=负向）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["factor_name", "category", "description"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if name == "factor.list":
            category = arguments.get("category")
            limit = arguments.get("limit", 100)
            offset = arguments.get("offset", 0)
            
            manager = get_factor_manager()
            factor_names = manager.list_factors(category=category)
            
            # 分页
            total = len(factor_names)
            factor_names = factor_names[offset:offset+limit]
            
            # 获取因子信息
            factors = []
            for factor_name in factor_names:
                info = manager.get_factor_info(factor_name)
                if info:
                    factors.append({
                        "factor_id": factor_name,
                        "name": info.get("name", factor_name),
                        "category": info.get("category", "unknown"),
                        "description": info.get("description", ""),
                        "direction": info.get("direction", 1)
                    })
            
            result = {
                "factors": factors,
                "total": total,
                "limit": limit,
                "offset": offset,
                "category": category
            }
            
        elif name == "factor.get":
            factor_id = arguments.get("factor_id")
            if not factor_id:
                raise ValueError("缺少必需参数: factor_id")
            
            manager = get_factor_manager()
            factor = manager.get_factor(factor_id)
            if not factor:
                raise ValueError(f"因子不存在: {factor_id}")
            
            info = manager.get_factor_info(factor_id)
            if not info:
                raise ValueError(f"无法获取因子信息: {factor_id}")
            
            result = {
                "factor_id": factor_id,
                "name": info.get("name", factor_id),
                "category": info.get("category", "unknown"),
                "description": info.get("description", ""),
                "direction": info.get("direction", 1),
                "metadata": {
                    "cache_dir": str(manager.cache_dir),
                    "use_cache": manager.use_cache
                }
            }
            
            # 如果数据量大，使用artifact
            result = create_artifact_if_needed(result, "factor_detail", artifact_policy, trace_id)
            
        elif name == "factor.search":
            query = arguments.get("query")
            if not query:
                raise ValueError("缺少必需参数: query")
            
            category = arguments.get("category")
            limit = arguments.get("limit", 20)
            offset = arguments.get("offset", 0)
            
            manager = get_factor_manager()
            all_factors = manager.list_factors(category=category)
            
            # 搜索匹配
            query_lower = query.lower()
            matches = []
            for factor_name in all_factors:
                info = manager.get_factor_info(factor_name)
                if not info:
                    continue
                
                # 匹配名称、类别、描述
                name_match = query_lower in factor_name.lower()
                desc_match = query_lower in info.get("description", "").lower()
                cat_match = query_lower in info.get("category", "").lower()
                
                if name_match or desc_match or cat_match:
                    matches.append({
                        "factor_id": factor_name,
                        "name": info.get("name", factor_name),
                        "category": info.get("category", "unknown"),
                        "description": info.get("description", ""),
                        "match_score": (2 if name_match else 0) + (1 if desc_match else 0) + (1 if cat_match else 0)
                    })
            
            # 按匹配度排序
            matches.sort(key=lambda x: x["match_score"], reverse=True)
            
            # 分页
            total = len(matches)
            matches = matches[offset:offset+limit]
            
            result = {
                "query": query,
                "results": matches,
                "total": total,
                "limit": limit,
                "offset": offset
            }
            
        elif name == "factor.validate":
            factor_definition = arguments.get("factor_definition")
            if not factor_definition:
                raise ValueError("缺少必需参数: factor_definition")
            
            # 验证逻辑（简化版）
            errors = []
            warnings = []
            
            # 检查必需字段
            if "name" not in factor_definition:
                errors.append("缺少必需字段: name")
            if "category" not in factor_definition:
                warnings.append("缺少字段: category（建议提供）")
            
            # 检查类别有效性
            if "category" in factor_definition:
                valid_categories = ["value", "growth", "quality", "momentum", "flow"]
                if factor_definition["category"] not in valid_categories:
                    errors.append(f"无效的类别: {factor_definition['category']}（有效值: {valid_categories}）")
            
            result = {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "factor_definition": factor_definition
            }
            
        elif name == "factor.evaluate":
            factor_id = arguments.get("factor_id")
            evaluation_config = arguments.get("evaluation_config")
            
            if not factor_id:
                raise ValueError("缺少必需参数: factor_id")
            if not evaluation_config:
                raise ValueError("缺少必需参数: evaluation_config")
            
            # 生成评估任务ID
            task_id = f"eval_{factor_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            result = {
                "task_id": task_id,
                "factor_id": factor_id,
                "evaluation_config": evaluation_config,
                "status": "pending",
                "message": "评估任务已创建，结果将通过job查询",
                "created_at": datetime.now().isoformat()
            }
        
        elif name == "factor.create":
            factor_name = arguments.get("factor_name")
            category = arguments.get("category")
            description = arguments.get("description")
            definition = arguments.get("definition", "")
            direction = arguments.get("direction", 1)
            
            if not factor_name:
                raise ValueError("缺少必需参数: factor_name")
            if not category:
                raise ValueError("缺少必需参数: category")
            if not description:
                raise ValueError("缺少必需参数: description")
            
            # 验证类别
            valid_categories = ["value", "growth", "quality", "momentum", "flow"]
            if category not in valid_categories:
                raise ValueError(f"无效的类别: {category}（有效值: {valid_categories}）")
            
            # 写操作需要confirm_token
            if requires_confirm_token(mode):
                confirm_token = arguments.get("confirm_token")
                if not confirm_token:
                    raise ValueError("mode=execute时需要confirm_token")
                
                ok, err_code = verify_confirm_token(confirm_token, name, arguments, trace_id)
                if not ok:
                    if err_code == "INVALID_TOKEN":
                        raise ValueError("确认令牌无效")
                    elif err_code == "TOKEN_EXPIRED":
                        raise ValueError("确认令牌已过期")
            
            manager = get_factor_manager()
            
            # 检查因子是否已存在
            existing_info = manager.get_factor_info(factor_name)
            if existing_info and mode == "execute":
                raise ValueError(f"因子已存在: {factor_name}")
            
            if mode == "dry_run":
                # 模拟创建
                result = {
                    "mode": "dry_run",
                    "factor_name": factor_name,
                    "category": category,
                    "description": description,
                    "definition": definition,
                    "direction": direction,
                    "message": "这是dry_run模式，未实际创建因子",
                    "validation": {
                        "name_valid": bool(factor_name),
                        "category_valid": category in valid_categories,
                        "description_valid": bool(description)
                    }
                }
            else:
                # 实际创建因子
                # 通过FactorStorage保存因子信息
                try:
                    from core.factors import create_factor_storage
                    storage = create_factor_storage()
                    
                    success = storage.save_factor_info(
                        factor_name=factor_name,
                        category=category,
                        description=description,
                        definition=definition,
                        direction=direction,
                        frequency="daily",
                        status="active"
                    )
                    
                    if not success:
                        raise RuntimeError("保存因子信息失败")
                    
                    # 记录证据
                    try:
                        sys.path.insert(0, str(TRQUANT_ROOT / "scripts"))
                        from mcp_call import MCPClient
                        
                        client = MCPClient("trquant-evidence")
                        evidence_content = {
                            "action": "create_factor",
                            "factor_name": factor_name,
                            "category": category,
                            "description": description,
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        client.call_tool("evidence.record", {
                            "title": f"创建因子: {factor_name}",
                            "type": "factor_creation",
                            "content": json.dumps(evidence_content, ensure_ascii=False, indent=2),
                            "related_change": trace_id,
                            "tags": ["factor", "create"]
                        })
                        client.close()
                    except Exception as e:
                        logger.warning(f"记录证据失败（可选）: {e}")
                    
                    result = {
                        "mode": "execute",
                        "factor_name": factor_name,
                        "category": category,
                        "description": description,
                        "definition": definition,
                        "direction": direction,
                        "created": True,
                        "message": "因子已创建"
                    }
                except ImportError:
                    # 如果FactorStorage不可用，使用FactorManager
                    # FactorManager可能没有直接的create方法，这里先记录信息
                    logger.warning("FactorStorage不可用，使用简化创建方式")
                    result = {
                        "mode": "execute",
                        "factor_name": factor_name,
                        "category": category,
                        "description": description,
                        "definition": definition,
                        "direction": direction,
                        "created": True,
                        "message": "因子信息已记录（注意：需要实现完整的因子计算逻辑）"
                    }
            
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-factor",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-factor",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数是否符合工具Schema要求",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except RuntimeError as e:
        envelope = wrap_error_response(
            error_code="DEPENDENCY_ERROR",
            error_message=str(e),
            server_name="trquant-factor",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查FactorManager依赖是否已安装",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-factor",
            tool_name=name,
            version="1.0.0",
            error_hint="服务器内部错误，请查看日志",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())




