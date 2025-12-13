#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Config Server
=====================

配置管理MCP服务器，提供配置的查询、验证、更新、备份和恢复功能。

运行方式:
    python mcp_servers/config_server.py

工具:
    - config.list: 列出所有配置文件
    - config.get: 获取配置详情
    - config.validate: 验证配置
    - config.update: 更新配置（需要confirm_token + evidence）
    - config.backup: 备份配置
    - config.restore: 恢复配置
"""

import sys
import json
import logging
import shutil
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
logger = logging.getLogger('ConfigServer')

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

# 导入配置验证器
try:
    from core.config_validator import ConfigValidator
    CONFIG_VALIDATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ConfigValidator不可用: {e}")
    CONFIG_VALIDATOR_AVAILABLE = False
    ConfigValidator = None

# 导入配置管理器
try:
    from config.config_manager import ConfigManager, get_config_manager
    CONFIG_MANAGER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ConfigManager不可用: {e}")
    CONFIG_MANAGER_AVAILABLE = False

# 配置目录
CONFIG_DIR = TRQUANT_ROOT / "config"
BACKUP_DIR = TRQUANT_ROOT / ".taorui" / "backups" / "config"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def record_evidence_via_mcp(trace_id: str, action: str, config_name: str, details: Dict[str, Any]) -> bool:
    """通过MCP调用evidence.record（如果可用）"""
    try:
        # 尝试导入MCP客户端
        sys.path.insert(0, str(TRQUANT_ROOT / "scripts"))
        from mcp_call import MCPClient
        
        client = MCPClient("trquant-evidence")
        evidence_content = {
            "action": action,
            "config_name": config_name,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        client.call_tool("evidence.record", {
            "title": f"配置变更: {config_name}",
            "type": "config_change",
            "content": json.dumps(evidence_content, ensure_ascii=False, indent=2),
            "related_change": trace_id,
            "tags": ["config", action]
        })
        client.close()
        return True
    except Exception as e:
        logger.warning(f"记录证据失败（可选）: {e}")
        return False


def validate_config_schema(config_name: str, config_data: Dict[str, Any]) -> List[str]:
    """验证配置Schema（简单验证）"""
    errors = []
    
    # 基本验证：检查必需字段
    if config_name == "jqdata_config.json":
        required_fields = ["username", "password"]
        for field in required_fields:
            if field not in config_data:
                errors.append(f"缺少必需字段: {field}")
    
    # JSON格式验证（已在load_config中完成）
    # 可以扩展更复杂的验证逻辑
    
    return errors


# 创建MCP服务器
server = Server("trquant-config")


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    base_schema_read = base_args_schema(mode="read")
    base_schema_dry_run = base_args_schema(mode="dry_run")
    
    return [
        Tool(
            name="config.list",
            description="列出所有配置文件",
            inputSchema=merge_schema(
                base_schema_read,
                {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "文件名模式（可选，如 '*_config.json'）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="config.get",
            description="获取配置详情",
            inputSchema=merge_schema(
                base_schema_read,
                {
                    "type": "object",
                    "properties": {
                        "config_name": {
                            "type": "string",
                            "description": "配置文件名（如 'jqdata_config.json'）"
                        },
                        "mask_sensitive": {
                            "type": "boolean",
                            "default": True,
                            "description": "是否屏蔽敏感信息（密码等）"
                        }
                    },
                    "required": ["config_name"]
                }
            )
        ),
        Tool(
            name="config.validate",
            description="验证配置（Schema和格式）",
            inputSchema=merge_schema(
                base_schema_dry_run,
                {
                    "type": "object",
                    "properties": {
                        "config_name": {
                            "type": "string",
                            "description": "配置文件名"
                        }
                    },
                    "required": ["config_name"]
                }
            )
        ),
        Tool(
            name="config.update",
            description="更新配置（需要confirm_token + evidence）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "config_name": {
                            "type": "string",
                            "description": "配置文件名"
                        },
                        "config_data": {
                            "type": "object",
                            "description": "配置数据（部分更新）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["config_name", "config_data"]
                }
            )
        ),
        Tool(
            name="config.backup",
            description="备份配置",
            inputSchema=merge_schema(
                base_schema_read,
                {
                    "type": "object",
                    "properties": {
                        "config_name": {
                            "type": "string",
                            "description": "配置文件名（可选，不提供则备份所有）"
                        }
                    }
                }
            )
        ),
        Tool(
            name="config.restore",
            description="恢复配置（需要confirm_token）",
            inputSchema=merge_schema(
                base_args_schema(mode="dry_run"),
                {
                    "type": "object",
                    "properties": {
                        "backup_id": {
                            "type": "string",
                            "description": "备份ID（从config.backup获取）"
                        },
                        "confirm_token": {
                            "type": "string",
                            "description": "确认令牌（mode=execute时需要）"
                        }
                    },
                    "required": ["backup_id"]
                }
            )
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具"""
    import json
    
    trace_id = arguments.get("trace_id") or extract_trace_id_from_request(arguments)
    mode = arguments.get("mode", "read")
    artifact_policy = arguments.get("artifact_policy", "inline")
    
    try:
        if not CONFIG_MANAGER_AVAILABLE:
            raise RuntimeError("ConfigManager不可用，请检查依赖")
        
        config_manager = get_config_manager()
        
        if name == "config.list":
            pattern = arguments.get("pattern", "*.json")
            
            config_files = []
            for config_file in CONFIG_DIR.glob(pattern):
                if config_file.is_file() and not config_file.name.endswith(".example.json"):
                    stat = config_file.stat()
                    config_files.append({
                        "name": config_file.name,
                        "size": stat.st_size,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
            
            result = {
                "configs": sorted(config_files, key=lambda x: x["name"]),
                "total": len(config_files),
                "config_dir": str(CONFIG_DIR)
            }
            
            result = create_artifact_if_needed(result, "config", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "config.get":
            config_name = arguments.get("config_name")
            if not config_name:
                raise ValueError("config_name是必需的")
            
            mask_sensitive = arguments.get("mask_sensitive", True)
            
            config_data = config_manager.load_config(config_name)
            
            # 屏蔽敏感信息
            if mask_sensitive:
                masked_data = config_data.copy()
                sensitive_keys = ["password", "token", "secret", "key", "api_key"]
                for key in sensitive_keys:
                    if key in masked_data:
                        masked_data[key] = "***MASKED***"
                config_data = masked_data
            
            result = {
                "config_name": config_name,
                "config_data": config_data,
                "masked": mask_sensitive
            }
            
            result = create_artifact_if_needed(result, "config", artifact_policy, trace_id)
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "config.validate":
            config_name = arguments.get("config_name")
            if not config_name:
                raise ValueError("config_name是必需的")
            
            config_data = config_manager.load_config(config_name)
            
            # Schema验证
            schema_errors = validate_config_schema(config_name, config_data)
            
            # JSON格式验证（已在load_config中完成）
            json_valid = True
            
            result = {
                "config_name": config_name,
                "valid": len(schema_errors) == 0 and json_valid,
                "schema_errors": schema_errors,
                "json_valid": json_valid
            }
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "config.update":
            config_name = arguments.get("config_name")
            config_data = arguments.get("config_data")
            
            if not config_name or not config_data:
                raise ValueError("config_name和config_data是必需的")
            
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
            
            if mode == "dry_run":
                # 模拟更新
                current_config = config_manager.load_config(config_name)
                updated_config = {**current_config, **config_data}
                
                # 验证
                validation_errors = validate_config_schema(config_name, updated_config)
                
                result = {
                    "config_name": config_name,
                    "mode": "dry_run",
                    "current_config": current_config,
                    "updated_config": updated_config,
                    "validation_errors": validation_errors,
                    "message": "这是dry_run模式，未实际更新配置"
                }
            else:
                # 实际更新
                current_config = config_manager.load_config(config_name)
                updated_config = {**current_config, **config_data}
                
                # 验证
                validation_errors = validate_config_schema(config_name, updated_config)
                if validation_errors:
                    raise ValueError(f"配置验证失败: {validation_errors}")
                
                # 保存配置
                config_manager.save_config(config_name, updated_config)
                
                # 记录证据
                record_evidence_via_mcp(trace_id, "update", config_name, {
                    "old_config": current_config,
                    "new_config": updated_config
                })
                
                result = {
                    "config_name": config_name,
                    "mode": "execute",
                    "updated": True,
                    "message": "配置已更新"
                }
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "config.backup":
            config_name = arguments.get("config_name")
            
            backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if config_name:
                # 备份单个配置
                config_path = CONFIG_DIR / config_name
                if not config_path.exists():
                    raise FileNotFoundError(f"配置文件不存在: {config_name}")
                
                backup_path = BACKUP_DIR / f"{backup_id}_{config_name}"
                shutil.copy2(config_path, backup_path)
                
                result = {
                    "backup_id": backup_id,
                    "config_name": config_name,
                    "backup_path": str(backup_path),
                    "message": "配置已备份"
                }
            else:
                # 备份所有配置
                backup_dir = BACKUP_DIR / backup_id
                backup_dir.mkdir(parents=True, exist_ok=True)
                
                backed_up = []
                for config_file in CONFIG_DIR.glob("*.json"):
                    if config_file.is_file() and not config_file.name.endswith(".example.json"):
                        backup_path = backup_dir / config_file.name
                        shutil.copy2(config_file, backup_path)
                        backed_up.append(config_file.name)
                
                result = {
                    "backup_id": backup_id,
                    "backup_dir": str(backup_dir),
                    "backed_up": backed_up,
                    "message": f"已备份 {len(backed_up)} 个配置文件"
                }
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        elif name == "config.restore":
            backup_id = arguments.get("backup_id")
            if not backup_id:
                raise ValueError("backup_id是必需的")
            
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
            
            # 查找备份文件
            backup_path = None
            for backup_file in BACKUP_DIR.glob(f"{backup_id}_*"):
                if backup_file.is_file():
                    backup_path = backup_file
                    break
            
            if not backup_path:
                # 尝试查找目录
                backup_dir = BACKUP_DIR / backup_id
                if backup_dir.exists() and backup_dir.is_dir():
                    # 恢复目录中的所有文件
                    if mode == "dry_run":
                        restored = list(backup_dir.glob("*.json"))
                        result = {
                            "backup_id": backup_id,
                            "mode": "dry_run",
                            "files_to_restore": [f.name for f in restored],
                            "message": "这是dry_run模式，未实际恢复配置"
                        }
                    else:
                        restored = []
                        for backup_file in backup_dir.glob("*.json"):
                            config_name = backup_file.name
                            config_path = CONFIG_DIR / config_name
                            shutil.copy2(backup_file, config_path)
                            restored.append(config_name)
                        
                        # 记录证据
                        record_evidence_via_mcp(trace_id, "restore", "all", {
                            "backup_id": backup_id,
                            "restored_files": restored
                        })
                        
                        result = {
                            "backup_id": backup_id,
                            "mode": "execute",
                            "restored": restored,
                            "message": f"已恢复 {len(restored)} 个配置文件"
                        }
                else:
                    raise FileNotFoundError(f"备份不存在: {backup_id}")
            else:
                # 恢复单个文件
                config_name = backup_path.name.replace(f"{backup_id}_", "")
                config_path = CONFIG_DIR / config_name
                
                if mode == "dry_run":
                    result = {
                        "backup_id": backup_id,
                        "config_name": config_name,
                        "mode": "dry_run",
                        "message": "这是dry_run模式，未实际恢复配置"
                    }
                else:
                    shutil.copy2(backup_path, config_path)
                    
                    # 记录证据
                    record_evidence_via_mcp(trace_id, "restore", config_name, {
                        "backup_id": backup_id
                    })
                    
                    result = {
                        "backup_id": backup_id,
                        "config_name": config_name,
                        "mode": "execute",
                        "message": "配置已恢复"
                    }
            
            envelope = wrap_success_response(
                data=result,
                server_name="trquant-config",
                tool_name=name,
                version="1.0.0",
                trace_id=trace_id
            )
            return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
        
        else:
            raise ValueError(f"未知工具: {name}")
    
    except ValueError as e:
        envelope = wrap_error_response(
            error_code="VALIDATION_ERROR",
            error_message=str(e),
            server_name="trquant-config",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except FileNotFoundError as e:
        envelope = wrap_error_response(
            error_code="NOT_FOUND",
            error_message=str(e),
            server_name="trquant-config",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查配置文件名或备份ID是否正确",
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        envelope = wrap_error_response(
            error_code="INTERNAL_ERROR",
            error_message=str(e),
            server_name="trquant-config",
            tool_name=name,
            version="1.0.0",
            error_details={"exception_type": type(e).__name__},
            trace_id=trace_id
        )
        return [TextContent(type="text", text=json.dumps(envelope, ensure_ascii=False, indent=2))]


if __name__ == "__main__":
    import asyncio
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())
    
    asyncio.run(main())




