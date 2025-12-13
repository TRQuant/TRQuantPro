#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRQuant Backtest Server
=======================

使用官方Python MCP SDK实现的回测管理服务器
管理回测任务、结果和报告

运行方式:
    python mcp_servers/backtest_server.py

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
logger = logging.getLogger('BacktestServer')

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
server = Server("trquant-backtest-server")

# 回测结果目录
BACKTEST_RESULTS_DIR = TRQUANT_ROOT / "backtest_results"
BACKTEST_RESULTS_DIR.mkdir(exist_ok=True)


def list_backtest_results() -> List[Dict[str, Any]]:
    """列出所有回测结果"""
    results = []
    
    for result_dir in BACKTEST_RESULTS_DIR.iterdir():
        if not result_dir.is_dir():
            continue
        
        # 查找metrics.json
        metrics_file = result_dir / "metrics.json"
        if metrics_file.exists():
            try:
                metrics = json.loads(metrics_file.read_text(encoding='utf-8'))
                results.append({
                    "name": result_dir.name,
                    "path": str(result_dir.relative_to(TRQUANT_ROOT)),
                    "metrics": metrics,
                    "created": datetime.fromtimestamp(result_dir.stat().st_ctime).isoformat(),
                    "modified": datetime.fromtimestamp(result_dir.stat().st_mtime).isoformat()
                })
            except Exception as e:
                logger.warning(f"无法读取回测结果 {result_dir}: {e}")
    
    return sorted(results, key=lambda x: x.get("modified", ""), reverse=True)


def get_backtest_result(result_name: str) -> Optional[Dict[str, Any]]:
    """获取回测结果详情"""
    result_dir = BACKTEST_RESULTS_DIR / result_name
    
    if not result_dir.exists():
        return None
    
    result = {
        "name": result_name,
        "path": str(result_dir.relative_to(TRQUANT_ROOT)),
        "files": []
    }
    
    # 读取metrics.json
    metrics_file = result_dir / "metrics.json"
    if metrics_file.exists():
        try:
            result["metrics"] = json.loads(metrics_file.read_text(encoding='utf-8'))
        except:
            pass
    
    # 列出所有文件
    for file_path in result_dir.rglob("*"):
        if file_path.is_file():
            result["files"].append({
                "name": file_path.name,
                "path": str(file_path.relative_to(TRQUANT_ROOT)),
                "size": file_path.stat().st_size,
                "type": file_path.suffix
            })
    
    return result


def compare_backtests(result_names: List[str]) -> Dict[str, Any]:
    """对比多个回测结果"""
    if len(result_names) < 2:
        raise ValueError("至少需要2个回测结果进行对比")
    
    results = []
    for name in result_names:
        result = get_backtest_result(name)
        if not result:
            raise ValueError(f"未找到回测结果: {name}")
        results.append(result)
    
    # 提取关键指标进行对比
    comparison = {
        "results": result_names,
        "metrics": {}
    }
    
    for result in results:
        metrics = result.get("metrics", {})
        name = result["name"]
        
        # 提取关键指标
        key_metrics = {
            "total_return": metrics.get("total_return", 0),
            "sharpe_ratio": metrics.get("sharpe_ratio", 0),
            "max_drawdown": metrics.get("max_drawdown", 0),
            "win_rate": metrics.get("win_rate", 0),
            "annual_return": metrics.get("annual_return", 0)
        }
        
        comparison["metrics"][name] = key_metrics
    
    # 计算排名
    comparison["rankings"] = {}
    for metric_name in ["total_return", "sharpe_ratio", "win_rate", "annual_return"]:
        rankings = sorted(
            [(name, comparison["metrics"][name].get(metric_name, 0)) for name in result_names],
            key=lambda x: x[1],
            reverse=True
        )
        comparison["rankings"][metric_name] = rankings
    
    # 最大回撤排名（越小越好）
    drawdown_rankings = sorted(
        [(name, abs(comparison["metrics"][name].get("max_drawdown", 0))) for name in result_names],
        key=lambda x: x[1]
    )
    comparison["rankings"]["max_drawdown"] = drawdown_rankings
    
    return comparison


def generate_backtest_report(result_name: str) -> Dict[str, Any]:
    """生成回测报告"""
    result = get_backtest_result(result_name)
    if not result:
        raise ValueError(f"未找到回测结果: {result_name}")
    
    metrics = result.get("metrics", {})
    
    report = {
        "result_name": result_name,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_return": metrics.get("total_return", 0),
            "annual_return": metrics.get("annual_return", 0),
            "sharpe_ratio": metrics.get("sharpe_ratio", 0),
            "max_drawdown": metrics.get("max_drawdown", 0),
            "win_rate": metrics.get("win_rate", 0),
            "total_trades": metrics.get("total_trades", 0)
        },
        "performance": {
            "returns": metrics.get("returns", {}),
            "drawdowns": metrics.get("drawdowns", {}),
            "risk_metrics": metrics.get("risk_metrics", {})
        },
        "files": result.get("files", []),
        "recommendations": []
    }
    
    # 生成建议
    if metrics.get("sharpe_ratio", 0) < 1:
        report["recommendations"].append("夏普比率较低，建议优化策略或调整参数")
    
    if abs(metrics.get("max_drawdown", 0)) > 0.2:
        report["recommendations"].append("最大回撤较大，建议加强风险控制")
    
    if metrics.get("win_rate", 0) < 0.5:
        report["recommendations"].append("胜率较低，建议优化选股逻辑")
    
    return report


@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="backtest.list",
            description="列出所有回测结果",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="backtest.get",
            description="获取回测结果详情",
            inputSchema={
                "type": "object",
                "properties": {
                    "result_name": {
                        "type": "string",
                        "description": "回测结果名称"
                    }
                },
                "required": ["result_name"]
            }
        ),
        Tool(
            name="backtest.compare",
            description="对比多个回测结果",
            inputSchema={
                "type": "object",
                "properties": {
                    "result_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "回测结果名称列表（至少2个）"
                    }
                },
                "required": ["result_names"]
            }
        ),
        Tool(
            name="backtest.report",
            description="生成回测报告",
            inputSchema={
                "type": "object",
                "properties": {
                    "result_name": {
                        "type": "string",
                        "description": "回测结果名称"
                    }
                },
                "required": ["result_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> List[TextContent]:
    """调用工具（返回统一envelope格式）"""
    # 提取trace_id（如果存在）
    trace_id = arguments.get("trace_id")
    
    try:
        if name == "backtest.list":
            results = list_backtest_results()
            result = {
                "results": results,
                "total": len(results),
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "backtest.get":
            result_name = arguments.get("result_name")
            if not result_name:
                raise ValueError("result_name参数是必需的")
            
            backtest_result = get_backtest_result(result_name)
            if not backtest_result:
                raise ValueError(f"未找到回测结果: {result_name}")
            
            result = backtest_result
            
        elif name == "backtest.compare":
            result_names = arguments.get("result_names", [])
            if not result_names:
                raise ValueError("result_names参数是必需的")
            
            comparison = compare_backtests(result_names)
            result = {
                "comparison": comparison,
                "timestamp": datetime.now().isoformat()
            }
            
        elif name == "backtest.report":
            result_name = arguments.get("result_name")
            if not result_name:
                raise ValueError("result_name参数是必需的")
            
            report = generate_backtest_report(result_name)
            result = report
        else:
            raise ValueError(f"未知工具: {name}")
        
        # 包装为统一envelope格式
        envelope = wrap_success_response(
            data=result,
            server_name="trquant-backtest",
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
            server_name="trquant-backtest",
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
            server_name="trquant-backtest",
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
            server_name="trquant-backtest",
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


