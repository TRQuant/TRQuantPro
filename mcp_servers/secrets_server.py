#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Secrets Server
======================

使用官方Python MCP SDK实现的密钥管理服务器
管理密钥、临时令牌和权限验证

运行方式:
    python mcp_servers/secrets_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
    - 安全最佳实践（不返回原始密钥）
"""

import sys
import json
import logging
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timedelta
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
logger = logging.getLogger('SecretsServer')

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
server = Server("trquant-secrets-server")

# 密钥存储目录（应该使用环境变量或密钥管理服务）
SECRETS_DIR = TRQUANT_ROOT / ".taorui" / "secrets"
SECRETS_DIR.mkdir(parents=True, exist_ok=True)

# 审计日志目录
AUDIT_LOG_DIR = TRQUANT_ROOT / ".taorui" / "artifacts" / "audit"
AUDIT_LOG_DIR.mkdir(parents=True, exist_ok=True)


def hash_secret(secret: str) -> str:
    """对密钥进行哈希（用于验证，不存储原始值）"""
    return hashlib.sha256(secret.encode()).hexdigest()


def generate_token(secret_name: str, expires_in: int = 3600) -> Dict[str, Any]:
    """生成临时令牌（不返回原始密钥）"""
    token = secrets.token_urlsafe(32)
    token_hash = hash_secret(token)
    
    token_data = {
        "secret_name": secret_name,
        "token_hash": token_hash,
        "created": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
        "expires_in": expires_in
    }
    
    # 保存令牌（仅存储哈希）
    token_file = SECRETS_DIR / f"token_{token_hash[:16]}.json"
    token_file.write_text(
        json.dumps(token_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    # 记录审计日志
    audit_log("token_generated", secret_name, {"expires_in": expires_in})
    
    return {
        "token": token,  # 仅返回一次
        "expires_in": expires_in,
        "expires_at": token_data["expires"],
        "warning": "此令牌仅显示一次，请妥善保存"
    }


def validate_token(token: str) -> Dict[str, Any]:
    """验证令牌"""
    token_hash = hash_secret(token)
    
    # 查找令牌文件
    token_file = SECRETS_DIR / f"token_{token_hash[:16]}.json"
    
    if not token_file.exists():
        audit_log("token_validation_failed", "unknown", {"reason": "token_not_found"})
        return {
            "valid": False,
            "error": "令牌不存在或已过期"
        }
    
    try:
        token_data = json.loads(token_file.read_text(encoding='utf-8'))
        
        # 检查是否过期
        expires = datetime.fromisoformat(token_data["expires"])
        if datetime.now() > expires:
            audit_log("token_validation_failed", token_data.get("secret_name", "unknown"), {"reason": "expired"})
            return {
                "valid": False,
                "error": "令牌已过期"
            }
        
        # 验证哈希
        if token_data["token_hash"] != token_hash:
            audit_log("token_validation_failed", token_data.get("secret_name", "unknown"), {"reason": "hash_mismatch"})
            return {
                "valid": False,
                "error": "令牌无效"
            }
        
        audit_log("token_validated", token_data.get("secret_name", "unknown"), {})
        return {
            "valid": True,
            "secret_name": token_data["secret_name"],
            "expires_at": token_data["expires"]
        }
    except Exception as e:
        logger.error(f"验证令牌失败: {e}")
        return {
            "valid": False,
            "error": f"验证失败: {str(e)}"
        }


def list_secrets() -> List[Dict[str, Any]]:
    """列出所有密钥（不返回实际值）"""
    secrets_list = []
    
    for secret_file in SECRETS_DIR.glob("secret_*.json"):
        try:
            secret_data = json.loads(secret_file.read_text(encoding='utf-8'))
            secrets_list.append({
                "name": secret_data.get("name", secret_file.stem),
                "type": secret_data.get("type", "unknown"),
                "created": secret_data.get("created", ""),
                "updated": secret_data.get("updated", ""),
                "has_value": "value_hash" in secret_data  # 仅表示是否有值，不返回实际值
            })
        except Exception as e:
            logger.warning(f"无法读取密钥文件 {secret_file}: {e}")
    
    return secrets_list


def audit_log(action: str, secret_name: str, details: Dict[str, Any]) -> None:
    """记录审计日志"""
    log_entry = {
        "action": action,
        "secret_name": secret_name,
        "timestamp": datetime.now().isoformat(),
        "details": details
    }
    
    log_file = AUDIT_LOG_DIR / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
    
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


def rotate_secret(secret_name: str) -> Dict[str, Any]:
    """轮换密钥"""
    secret_file = SECRETS_DIR / f"secret_{secret_name}.json"
    
    if not secret_file.exists():
        raise ValueError(f"未找到密钥: {secret_name}")
    
    # 读取旧密钥信息
    old_secret_data = json.loads(secret_file.read_text(encoding='utf-8'))
    
    # 创建新密钥记录
    new_secret_data = {
        "name": secret_name,
        "type": old_secret_data.get("type", "unknown"),
        "created": old_secret_data.get("created", ""),
        "updated": datetime.now().isoformat(),
        "rotated_from": old_secret_data.get("name", secret_name),
        "rotation_count": old_secret_data.get("rotation_count", 0) + 1
    }
    
    # 保存新密钥（实际应用中应该生成新密钥值）
    secret_file.write_text(
        json.dumps(new_secret_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    
    audit_log("secret_rotated", secret_name, {"rotation_count": new_secret_data["rotation_count"]})
    
    return {
        "secret_name": secret_name,
        "rotated": True,
        "rotation_count": new_secret_data["rotation_count"],
        "timestamp": datetime.now().isoformat()
    }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="secrets.get_token",
            description="获取临时令牌（不返回原始密钥）",
            inputSchema={
                "type": "object",
                "properties": {
                    "secret_name": {
                        "type": "string",
                        "description": "密钥名称"
                    },
                    "expires_in": {
                        "type": "integer",
                        "description": "过期时间（秒），默认3600",
                        "default": 3600
                    }
                },
                "required": ["secret_name"]
            }
        ),
        Tool(
            name="secrets.validate",
            description="验证令牌或权限",
            inputSchema={
                "type": "object",
                "properties": {
                    "token": {
                        "type": "string",
                        "description": "要验证的令牌"
                    }
                },
                "required": ["token"]
            }
        ),
        Tool(
            name="secrets.list",
            description="列出所有密钥（不返回实际值）",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="secrets.rotate",
            description="轮换密钥",
            inputSchema={
                "type": "object",
                "properties": {
                    "secret_name": {
                        "type": "string",
                        "description": "密钥名称"
                    }
                },
                "required": ["secret_name"]
            }
        ),
        Tool(
            name="secrets.audit",
            description="查看审计日志",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "日期（YYYY-MM-DD），默认今天"
                    },
                    "secret_name": {
                        "type": "string",
                        "description": "按密钥名称筛选（可选）"
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
        if name == "secrets.get_token":
            secret_name = arguments.get("secret_name")
            expires_in = arguments.get("expires_in", 3600)
            
            if not secret_name:
                raise ValueError("secret_name参数是必需的")
            
            token_info = generate_token(secret_name, expires_in)
            result = token_info
            
        elif name == "secrets.validate":
            token = arguments.get("token")
            if not token:
                raise ValueError("token参数是必需的")
            
            validation = validate_token(token)
            result = validation
            
        elif name == "secrets.list":
            secrets_list = list_secrets()
            result = {
                "secrets": secrets_list,
                "total": len(secrets_list),
                "note": "不返回实际密钥值，仅显示元数据",
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "secrets.rotate":
            secret_name = arguments.get("secret_name")
            if not secret_name:
                raise ValueError("secret_name参数是必需的")
            
            rotation = rotate_secret(secret_name)
            result = rotation
            
        elif name == "secrets.audit":
            date = arguments.get("date", datetime.now().strftime("%Y%m%d"))
            secret_name = arguments.get("secret_name")
            
            log_file = AUDIT_LOG_DIR / f"audit_{date}.jsonl"
            
            if not log_file.exists():
                result = {
                    "date": date,
                    "logs": [],
                    "message": "该日期无审计日志"
                }
            else:
                logs = []
                with open(log_file, "r", encoding='utf-8') as f:
                    for line in f:
                        try:
                            log_entry = json.loads(line.strip())
                            if secret_name and log_entry.get("secret_name") != secret_name:
                                continue
                            logs.append(log_entry)
                        except:
                            pass
                
                result = {
                    "date": date,
                    "logs": logs,
                    "total": len(logs),
                    "timestamp": datetime.now().isoformat()
                }
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-secrets",
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
            server_name="trquant-secrets",
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
            server_name="trquant-secrets",
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
            server_name="trquant-secrets",
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


