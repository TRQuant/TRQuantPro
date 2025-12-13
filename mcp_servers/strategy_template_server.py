#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Strategy Template Server
=================================

策略模板管理MCP服务器，提供策略模板的查询、生成和验证功能。

运行方式:
    python mcp_servers/strategy_template_server.py

工具:
    - template.list: 列出所有策略模板
    - template.get: 获取模板详情
    - template.generate: 生成策略代码（输入：模板ID + 参数）
    - template.validate: 验证模板定义
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
logger = logging.getLogger('StrategyTemplateServer')

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

# 导入资产链接器
try:
    from core.asset_linker import AssetLinker
    ASSET_LINKER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AssetLinker不可用: {e}")
    ASSET_LINKER_AVAILABLE = False
    AssetLinker = None

# 导入策略管理模块
try:
    from extension.dashboard.strategy_manager import StrategyManager, STRATEGY_TEMPLATES
    STRATEGY_MANAGER_AVAILABLE = True
except ImportError:
    try:
        from core.strategy_generator import StrategyGenerator
        STRATEGY_MANAGER_AVAILABLE = True
        StrategyManager = None  # 使用StrategyGenerator
    except ImportError as e:
        logger.warning(f"StrategyManager/StrategyGenerator不可用: {e}")
        STRATEGY_MANAGER_AVAILABLE = False
        StrategyManager = None
        STRATEGY_TEMPLATES = {}

# 初始化策略管理器（延迟初始化）
_strategy_manager: Optional[Any] = None
_strategy_generator: Optional[Any] = None


def get_strategy_manager():
    """获取策略管理器实例（单例）"""
    global _strategy_manager, _strategy_generator
    
    if StrategyManager is not None:
        if _strategy_manager is None:
            _strategy_manager = StrategyManager()
        return _strategy_manager
    else:
        if _strategy_generator is None:
            if not STRATEGY_MANAGER_AVAILABLE:
                raise RuntimeError("StrategyGenerator不可用，请检查依赖")
            _strategy_generator = StrategyGenerator()
        return _strategy_generator


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
server = Server("trquant-strategy-template")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema = base_args_schema(mode="read")
    
    return [
        Tool(
            name="template.list",
            description="列出所有策略模板",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt", "all", None],
                            "description": "平台类型（可选）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="template.get",
            description="获取模板详情",
            inputSchema=merge_schema(
                base_schema,
                {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "模板ID"
                        }
                    },
                    "required": ["template_id"]
                }
            )
        ),
        Tool(
            name="template.generate",
            description="生成策略代码（输入：模板ID + 参数 → 输出：策略代码工件指针 + 摘要）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "模板ID"
                        },
                        "params": {
                            "type": "object",
                            "description": "模板参数（如：name, description, factors等）"
                        }
                    },
                    "required": ["template_id", "params"]
                }
            )
        ),
        Tool(
            name="template.validate",
            description="验证模板定义",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "模板ID"
                        }
                    },
                    "required": ["template_id"]
                }
            )
        ),
        Tool(
            name="template.create",
            description="创建新策略模板（需要confirm_token + evidence）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "模板ID（唯一标识）"
                        },
                        "name": {
                            "type": "string",
                            "description": "模板名称"
                        },
                        "platform": {
                            "type": "string",
                            "enum": ["ptrade", "qmt"],
                            "description": "平台类型"
                        },
                        "template_code": {
                            "type": "string",
                            "description": "模板代码（支持参数占位符）"
                        },
                        "description": {
                            "type": "string",
                            "description": "模板描述"
                        },
                        "params_schema": {
                            "type": "object",
                            "description": "参数Schema定义（可选）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["template_id", "name", "platform", "template_code"]
                }
            )
        ),
        Tool(
            name="template.update",
            description="更新策略模板（需要confirm_token + evidence）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "template_id": {
                            "type": "string",
                            "description": "模板ID"
                        },
                        "name": {
                            "type": "string",
                            "description": "模板名称（可选）"
                        },
                        "template_code": {
                            "type": "string",
                            "description": "模板代码（可选）"
                        },
                        "description": {
                            "type": "string",
                            "description": "模板描述（可选）"
                        },
                        "params_schema": {
                            "type": "object",
                            "description": "参数Schema定义（可选）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["template_id"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "pointer")  # 策略代码默认使用pointer
    
    try:
        if name == "template.list":
            platform = arguments.get("platform", "all")
            
            manager = get_strategy_manager()
            
            if StrategyManager is not None:
                # 使用StrategyManager
                templates = manager.get_templates()
                if platform != "all":
                    templates = [t for t in templates if t.get("platform") == platform]
            else:
                # 使用StrategyGenerator
                templates = manager.get_templates()
                if platform != "all":
                    templates = [t for t in templates if t.get("platform") == platform]
            
            result = {
                "templates": templates,
                "total": len(templates),
                "platform": platform
            }
            
        elif name == "template.get":
            template_id = arguments.get("template_id")
            if not template_id:
                raise ValueError("缺少必需参数: template_id")
            
            manager = get_strategy_manager()
            
            if StrategyManager is not None:
                # 使用StrategyManager
                templates = manager.get_templates()
                template = next((t for t in templates if t.get("key") == template_id), None)
                
                if not template:
                    raise ValueError(f"模板不存在: {template_id}")
                
                # 获取模板代码
                template_code = STRATEGY_TEMPLATES.get(template_id, "")
                
                result = {
                    "template_id": template_id,
                    "name": template.get("name", template_id),
                    "platform": template.get("platform", "unknown"),
                    "code_preview": template_code[:500] if template_code else "",  # 预览前500字符
                    "code_length": len(template_code),
                    "has_code": bool(template_code)
                }
            else:
                # 使用StrategyGenerator
                template = manager.get_template(template_id)
                if not template:
                    raise ValueError(f"模板不存在: {template_id}")
                
                result = {
                    "template_id": template_id,
                    "name": template.name if hasattr(template, "name") else template_id,
                    "description": template.description if hasattr(template, "description") else "",
                    "factors_count": len(template.factors) if hasattr(template, "factors") else 0,
                    "rebalance_freq": template.rebalance.frequency.value if hasattr(template, "rebalance") else "unknown"
                }
            
            # 如果数据量大，使用artifact
            result = create_artifact_if_needed(result, "strategy", artifact_policy, trace_id)
            
        elif name == "template.generate":
            template_id = arguments.get("template_id")
            params = arguments.get("params")
            
            if not template_id:
                raise ValueError("缺少必需参数: template_id")
            if not params:
                raise ValueError("缺少必需参数: params")
            
            # 如果是dry_run模式，只返回生成计划
            if mode == "dry_run":
                result = {
                    "mode": "dry_run",
                    "template_id": template_id,
                    "params": params,
                    "message": "这是dry_run模式，不会实际生成代码",
                    "generation_plan": {
                        "will_generate": True,
                        "estimated_size": "unknown"
                    }
                }
            else:
                manager = get_strategy_manager()
                
                if StrategyManager is not None:
                    # 使用StrategyManager生成
                    template_code = STRATEGY_TEMPLATES.get(template_id)
                    if not template_code:
                        raise ValueError(f"模板不存在: {template_id}")
                    
                    # 格式化模板代码
                    try:
                        strategy_code = template_code.format(**params)
                    except KeyError as e:
                        raise ValueError(f"模板参数缺失: {e}")
                    
                    # 生成策略摘要
                    summary = {
                        "name": params.get("name", "未命名策略"),
                        "description": params.get("description", ""),
                        "template_id": template_id,
                        "platform": template_id.split("_")[0] if "_" in template_id else "unknown",
                        "code_length": len(strategy_code),
                        "lines": len(strategy_code.split("\n"))
                    }
                    
                    # 使用artifact存储策略代码
                    artifact_data = {
                        "strategy_code": strategy_code,
                        "template_id": template_id,
                        "params": params,
                        "generated_at": datetime.now().isoformat()
                    }
                    
                    artifact_pointer = create_artifact_if_needed(
                        artifact_data, "strategy", "pointer", trace_id
                    )
                    
                    result = {
                        "artifact": artifact_pointer,
                        "summary": summary,
                        "preview": strategy_code[:200]  # 预览前200字符
                    }
                else:
                    # 使用StrategyGenerator生成
                    template = manager.get_template(template_id)
                    if not template:
                        raise ValueError(f"模板不存在: {template_id}")
                    
                    # 创建策略配置（需要根据params构建）
                    # 这里简化处理，实际应该根据StrategyConfig结构构建
                    strategy_code = manager.create_strategy(template)
                    
                    result = {
                        "strategy_code": strategy_code,
                        "template_id": template_id,
                        "summary": {
                            "code_length": len(strategy_code),
                            "lines": len(strategy_code.split("\n"))
                        }
                    }
                    
                    # 使用artifact存储
                    result = create_artifact_if_needed(result, "strategy", artifact_policy, trace_id)
            
        elif name == "template.validate":
            template_id = arguments.get("template_id")
            if not template_id:
                raise ValueError("缺少必需参数: template_id")
            
            errors = []
            warnings = []
            
            manager = get_strategy_manager()
            
            if StrategyManager is not None:
                # 使用StrategyManager验证
                template_code = STRATEGY_TEMPLATES.get(template_id)
                if not template_code:
                    errors.append(f"模板不存在: {template_id}")
                else:
                    # 检查模板格式
                    if "{" not in template_code or "}" not in template_code:
                        warnings.append("模板可能不包含参数占位符")
                    
                    # 检查必需参数
                    import re
                    placeholders = re.findall(r'\{(\w+)\}', template_code)
                    if not placeholders:
                        warnings.append("模板未定义任何参数")
            else:
                # 使用StrategyGenerator验证
                template = manager.get_template(template_id)
                if not template:
                    errors.append(f"模板不存在: {template_id}")
            
            result = {
                "template_id": template_id,
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings
            }
        
        elif name == "template.create":
            template_id = arguments.get("template_id")
            name = arguments.get("name")
            platform = arguments.get("platform")
            template_code = arguments.get("template_code")
            description = arguments.get("description", "")
            params_schema = arguments.get("params_schema", {})
            
            if not template_id:
                raise ValueError("缺少必需参数: template_id")
            if not name:
                raise ValueError("缺少必需参数: name")
            if not platform:
                raise ValueError("缺少必需参数: platform")
            if not template_code:
                raise ValueError("缺少必需参数: template_code")
            
            # 验证平台
            if platform not in ["ptrade", "qmt"]:
                raise ValueError(f"无效的平台: {platform}（有效值: ptrade, qmt）")
            
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
            
            manager = get_strategy_manager()
            
            # 检查模板是否已存在
            if StrategyManager is not None:
                templates = manager.get_templates()
                existing = next((t for t in templates if t.get("key") == template_id), None)
                if existing and mode == "execute":
                    raise ValueError(f"模板已存在: {template_id}")
            
            if mode == "dry_run":
                # 模拟创建
                result = {
                    "mode": "dry_run",
                    "template_id": template_id,
                    "name": name,
                    "platform": platform,
                    "code_length": len(template_code),
                    "message": "这是dry_run模式，未实际创建模板",
                    "validation": {
                        "template_id_valid": bool(template_id),
                        "platform_valid": platform in ["ptrade", "qmt"],
                        "code_valid": bool(template_code)
                    }
                }
            else:
                # 实际创建模板
                # 保存模板到文件或数据库（这里简化处理，保存到文件）
                templates_dir = TRQUANT_ROOT / "config" / "strategy_templates"
                templates_dir.mkdir(parents=True, exist_ok=True)
                
                template_file = templates_dir / f"{template_id}.json"
                
                template_data = {
                    "template_id": template_id,
                    "name": name,
                    "platform": platform,
                    "template_code": template_code,
                    "description": description,
                    "params_schema": params_schema,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                # 保存模板文件
                template_file.write_text(
                    json.dumps(template_data, ensure_ascii=False, indent=2),
                    encoding='utf-8'
                )
                
                # 记录证据
                try:
                    sys.path.insert(0, str(TRQUANT_ROOT / "scripts"))
                    from mcp_call import MCPClient
                    
                    client = MCPClient("trquant-evidence")
                    evidence_content = {
                        "action": "create_template",
                        "template_id": template_id,
                        "name": name,
                        "platform": platform,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    client.call_tool("evidence.record", {
                        "title": f"创建策略模板: {template_id}",
                        "type": "template_creation",
                        "content": json.dumps(evidence_content, ensure_ascii=False, indent=2),
                        "related_change": trace_id,
                        "tags": ["template", "create"]
                    })
                    client.close()
                except Exception as e:
                    logger.warning(f"记录证据失败（可选）: {e}")
                
                result = {
                    "mode": "execute",
                    "template_id": template_id,
                    "name": name,
                    "platform": platform,
                    "created": True,
                    "file_path": str(template_file),
                    "message": "模板已创建"
                }
        
        elif name == "template.update":
            template_id = arguments.get("template_id")
            name = arguments.get("name")
            template_code = arguments.get("template_code")
            description = arguments.get("description")
            params_schema = arguments.get("params_schema")
            
            if not template_id:
                raise ValueError("缺少必需参数: template_id")
            
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
            
            # 检查模板是否存在
            templates_dir = TRQUANT_ROOT / "config" / "strategy_templates"
            template_file = templates_dir / f"{template_id}.json"
            
            if not template_file.exists():
                # 检查是否在STRATEGY_TEMPLATES中
                if StrategyManager is not None:
                    templates = get_strategy_manager().get_templates()
                    existing = next((t for t in templates if t.get("key") == template_id), None)
                    if not existing:
                        raise ValueError(f"模板不存在: {template_id}")
                else:
                    raise ValueError(f"模板不存在: {template_id}")
            
            if mode == "dry_run":
                # 模拟更新
                if template_file.exists():
                    current_data = json.loads(template_file.read_text(encoding='utf-8'))
                else:
                    current_data = {}
                
                result = {
                    "mode": "dry_run",
                    "template_id": template_id,
                    "current": {
                        "name": current_data.get("name", "unknown"),
                        "code_length": len(current_data.get("template_code", ""))
                    },
                    "updates": {
                        "name": name if name else "未更改",
                        "code_length": len(template_code) if template_code else "未更改"
                    },
                    "message": "这是dry_run模式，未实际更新模板"
                }
            else:
                # 实际更新模板
                if template_file.exists():
                    current_data = json.loads(template_file.read_text(encoding='utf-8'))
                else:
                    current_data = {
                        "template_id": template_id,
                        "created_at": datetime.now().isoformat()
                    }
                
                # 更新字段
                if name:
                    current_data["name"] = name
                if template_code:
                    current_data["template_code"] = template_code
                if description is not None:
                    current_data["description"] = description
                if params_schema:
                    current_data["params_schema"] = params_schema
                
                current_data["updated_at"] = datetime.now().isoformat()
                
                # 保存更新
                template_file.write_text(
                    json.dumps(current_data, ensure_ascii=False, indent=2),
                    encoding='utf-8'
                )
                
                # 记录证据
                try:
                    sys.path.insert(0, str(TRQUANT_ROOT / "scripts"))
                    from mcp_call import MCPClient
                    
                    client = MCPClient("trquant-evidence")
                    evidence_content = {
                        "action": "update_template",
                        "template_id": template_id,
                        "updated_fields": [k for k in ["name", "template_code", "description", "params_schema"] if arguments.get(k)],
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    client.call_tool("evidence.record", {
                        "title": f"更新策略模板: {template_id}",
                        "type": "template_update",
                        "content": json.dumps(evidence_content, ensure_ascii=False, indent=2),
                        "related_change": trace_id,
                        "tags": ["template", "update"]
                    })
                    client.close()
                except Exception as e:
                    logger.warning(f"记录证据失败（可选）: {e}")
                
                result = {
                    "mode": "execute",
                    "template_id": template_id,
                    "updated": True,
                    "file_path": str(template_file),
                    "message": "模板已更新"
                }
            
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-strategy-template",
            tool_name=name,
            version="1.0.0",
            trace_id=trace_id
        )
        
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-strategy-template",
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
            server_name="trquant-strategy-template",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查StrategyManager/StrategyGenerator依赖是否已安装",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-strategy-template",
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




