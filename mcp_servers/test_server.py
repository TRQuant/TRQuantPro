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
    from mcp_servers.utils.mcp_integration_helper import process_mcp_tool_call
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



def _adapt_mcp_result_to_text_content(result: Dict[str, Any]) -> List[TextContent]:
    """将process_mcp_tool_call的结果转换为List[TextContent]"""
    if isinstance(result, dict) and "content" in result:
        text_content = []
        for item in result.get("content", []):
            if item.get("type") == "text":
                text_content.append(TextContent(type="text", text=item.get("text", "")))
        return text_content if text_content else [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
    else:
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（使用process_mcp_tool_call）"""
    # 获取工具列表
    tools_list = []
    try:
        import inspect
        for obj_name in dir(server):
            obj = getattr(server, obj_name, None)
            if inspect.iscoroutinefunction(obj) and obj_name == 'list_tools':
                tools_result = await obj()
                if tools_result:
                    tools_list = tools_result
                    break
    except:
        pass
    
    def handler(validated_args):
        if name == "test.run":
            return run_pytest(
                validated_args.get("test_path"),
                validated_args.get("args")
            )
        elif name == "test.report":
            test_result = run_pytest(validated_args.get("test_path"))
            return {
                "test_result": test_result,
                "report": test_result.get("report", {}),
                "summary": test_result.get("summary", {})
            }
        elif name == "test.coverage":
            return get_test_coverage(validated_args.get("test_path"))
        else:
            raise ValueError(f"未知工具: {name}")
    
    result = process_mcp_tool_call(
        server_name="trquant-test",
        tool_name=name,
        arguments=arguments,
        mcp_tools_list=tools_list,
        tool_handler=handler,
        server_version="1.0.0"
    )
    return _adapt_mcp_result_to_text_content(result)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



