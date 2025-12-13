#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Lint Server
===================

使用官方Python MCP SDK实现的代码格式化和静态检查服务器
集成black和flake8

运行方式:
    python mcp_servers/lint_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
"""

import sys
import json
import logging
import subprocess
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
logger = logging.getLogger('LintServer')

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
server = Server("trquant-lint-server")


def run_black(file_path: Optional[str] = None, check_only: bool = False) -> Dict[str, Any]:
    """运行black格式化"""
    cmd = ["black"]
    
    if check_only:
        cmd.append("--check")
    
    if file_path:
        cmd.append(file_path)
    else:
        cmd.append(".")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(TRQUANT_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "tool": "black",
            "mode": "check" if check_only else "format"
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "black执行超时（超过60秒）",
            "tool": "black"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "black未安装，请运行: pip install black",
            "tool": "black"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"black执行失败: {str(e)}",
            "tool": "black"
        }


def run_flake8(file_path: Optional[str] = None) -> Dict[str, Any]:
    """运行flake8静态检查"""
    cmd = ["flake8"]
    
    # 添加常用配置
    cmd.extend(["--max-line-length=120", "--extend-ignore=E203,W503"])
    
    if file_path:
        cmd.append(file_path)
    else:
        cmd.append(".")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(TRQUANT_ROOT),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        # 解析flake8输出
        issues = []
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        issues.append({
                            "file": parts[0],
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "code": parts[3].split()[0] if parts[3] else "",
                            "message": parts[3].strip() if parts[3] else ""
                        })
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "issues": issues,
            "issue_count": len(issues),
            "tool": "flake8"
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "flake8执行超时（超过120秒）",
            "tool": "flake8"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "flake8未安装，请运行: pip install flake8",
            "tool": "flake8"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"flake8执行失败: {str(e)}",
            "tool": "flake8"
        }


def run_autopep8(file_path: str) -> Dict[str, Any]:
    """使用autopep8自动修复代码"""
    cmd = ["autopep8", "--in-place", "--aggressive", "--aggressive", file_path]
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(TRQUANT_ROOT),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "file": file_path,
            "tool": "autopep8"
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "autopep8执行超时（超过60秒）",
            "tool": "autopep8"
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "autopep8未安装，请运行: pip install autopep8",
            "tool": "autopep8"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"autopep8执行失败: {str(e)}",
            "tool": "autopep8"
        }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="lint.format",
            description="格式化代码（使用black）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要格式化的文件路径（相对项目根目录），留空则格式化整个项目"
                    },
                    "check_only": {
                        "type": "boolean",
                        "description": "仅检查不修改，默认false",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="lint.check",
            description="静态代码检查（使用flake8）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要检查的文件路径（相对项目根目录），留空则检查整个项目"
                    }
                }
            }
        ),
        Tool(
            name="lint.fix",
            description="自动修复代码问题（使用autopep8）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要修复的文件路径（相对项目根目录）"
                    }
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="lint.report",
            description="生成代码质量报告（black + flake8）",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "要检查的文件路径（相对项目根目录），留空则检查整个项目"
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
        if name == "lint.format":
            file_path = arguments.get("file_path")
            check_only = arguments.get("check_only", False)
            result = run_black(file_path, check_only)
            
        elif name == "lint.check":
            file_path = arguments.get("file_path")
            result = run_flake8(file_path)
            
        elif name == "lint.fix":
            file_path = arguments.get("file_path")
            if not file_path:
                raise ValueError("file_path参数是必需的")
            
            # 先检查
            check_result = run_flake8(file_path)
            
            # 尝试修复
            fix_result = run_autopep8(file_path)
            
            # 再次检查
            check_after = run_flake8(file_path)
            
            result = {
                "file": file_path,
                "before": check_result,
                "fix": fix_result,
                "after": check_after,
                "improved": check_result.get("issue_count", 0) > check_after.get("issue_count", 0)
            }
            
        elif name == "lint.report":
            file_path = arguments.get("file_path")
            
            # 运行black检查
            black_result = run_black(file_path, check_only=True)
            
            # 运行flake8检查
            flake8_result = run_flake8(file_path)
            
            result = {
                "file": file_path or "整个项目",
                "timestamp": datetime.now().isoformat(),
                "black": {
                    "needs_formatting": not black_result.get("success", False),
                    "output": black_result.get("stdout", "")
                },
                "flake8": {
                    "issue_count": flake8_result.get("issue_count", 0),
                    "issues": flake8_result.get("issues", []),
                    "output": flake8_result.get("stdout", "")
                },
                "summary": {
                    "needs_formatting": not black_result.get("success", False),
                    "has_issues": flake8_result.get("issue_count", 0) > 0,
                    "total_issues": flake8_result.get("issue_count", 0)
                }
            }
            
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-lint",
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
            server_name="trquant-lint",
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
            server_name="trquant-lint",
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
            server_name="trquant-lint",
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


