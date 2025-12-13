#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Test Server
===================

使用官方Python MCP SDK实现的测试运行服务器
集成pytest

运行方式:
    python mcp_servers/test_server.py

遵循:
    - MCP协议规范
    - 官方Python SDK
    - 官方最佳实践
"""

import sys
import os
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
logger = logging.getLogger('TestServer')

# 导入官方MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
    logger.info("使用官方MCP SDK")
except ImportError:
    logger.error("官方MCP SDK不可用，请安装: pip install mcp")
    sys.exit(1)

# 创建服务器
server = Server("trquant-test-server")


def run_pytest(test_path: Optional[str] = None, args: Optional[List[str]] = None) -> Dict[str, Any]:
    """运行pytest测试"""
    # 设置环境变量，将venv/bin添加到PATH前面
    venv_bin = TRQUANT_ROOT / "extension" / "venv" / "bin"
    env = dict(os.environ)
    if venv_bin.exists():
        # 将venv/bin添加到PATH前面，确保优先使用venv中的pytest
        current_path = env.get("PATH", "")
        env["PATH"] = f"{str(venv_bin)}:{current_path}"
    
    cmd = ["pytest"]  # 现在可以直接使用pytest，因为PATH已设置
    
    if test_path:
        cmd.append(test_path)
    
    if args:
        cmd.extend(args)
    
    # 添加JSON报告
    cmd.extend(["--json-report", "--json-report-file=/tmp/pytest_report.json"])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(TRQUANT_ROOT),
            env=env,  # 使用修改后的环境变量
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        # 读取JSON报告
        report = {}
        report_file = Path("/tmp/pytest_report.json")
        if report_file.exists():
            try:
                report = json.loads(report_file.read_text())
            except:
                pass
        
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "report": report,
            "summary": {
                "passed": report.get("summary", {}).get("passed", 0),
                "failed": report.get("summary", {}).get("failed", 0),
                "total": report.get("summary", {}).get("total", 0)
            }
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "测试超时（超过5分钟）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_test_coverage(test_path: Optional[str] = None) -> Dict[str, Any]:
    """获取测试覆盖率"""
    cmd = ["pytest", "--cov=.", "--cov-report=json", "--cov-report=term"]
    
    if test_path:
        cmd.append(test_path)
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(TRQUANT_ROOT),
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 读取覆盖率报告
        coverage_file = Path(".coverage.json")
        if not coverage_file.exists():
            coverage_file = Path("coverage.json")
        
        coverage_data = {}
        if coverage_file.exists():
            try:
                coverage_data = json.loads(coverage_file.read_text())
            except:
                pass
        
        return {
            "success": result.returncode == 0,
            "coverage": coverage_data,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="test.run",
            description="运行pytest测试",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_path": {
                        "type": "string",
                        "description": "测试路径（文件或目录），可选"
                    },
                    "args": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "额外的pytest参数"
                    }
                }
            }
        ),
        Tool(
            name="test.report",
            description="生成测试报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_path": {
                        "type": "string",
                        "description": "测试路径，可选"
                    }
                }
            }
        ),
        Tool(
            name="test.coverage",
            description="获取代码覆盖率",
            inputSchema={
                "type": "object",
                "properties": {
                    "test_path": {
                        "type": "string",
                        "description": "测试路径，可选"
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
        if name == "test.run":
            result = run_pytest(
                arguments.get("test_path"),
                arguments.get("args")
            )
        elif name == "test.report":
            # 运行测试并生成报告
            test_result = run_pytest(arguments.get("test_path"))
            result = {
                "test_result": test_result,
                "report": test_result.get("report", {}),
                "summary": test_result.get("summary", {})
            }
        elif name == "test.coverage":
            result = get_test_coverage(arguments.get("test_path"))
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-test",
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
            server_name="trquant-test",
            tool_name=name,
            version="1.0.0",
            error_hint="请检查输入参数是否符合工具Schema要求",
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
            server_name="trquant-test",
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



