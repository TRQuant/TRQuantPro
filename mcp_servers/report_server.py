# -*- coding: utf-8 -*-
"""
报告MCP服务器（增强版）
=======================
T1.9.1 报告生成系统 MCP 接口

工具：
- report.generate: 生成回测报告
- report.compare: 生成策略对比报告
- report.diagnosis: 生成策略诊断报告
- report.list: 列出已生成的报告
- report.get: 获取报告详情
- report.delete: 删除报告
"""

import logging
import json
from typing import Dict, List, Any
import sys
from pathlib import Path

# 添加项目路径
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 导入官方MCP SDK
try:
    from mcp.server.models import InitializationOptions
    MCP_SDK_AVAILABLE = True
except ImportError as e:
    import sys
    print(f'官方MCP SDK不可用，请安装: pip install mcp. 错误: {e}', file=sys.stderr)
    sys.exit(1)

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("report-server")


TOOLS = [
    Tool(
        name="report.generate",
        description="生成回测报告（支持 HTML/PDF/Markdown/JSON 格式）",
        inputSchema={
            "type": "object",
            "properties": {
                "metrics": {
                    "type": "object",
                    "description": "回测指标，包含 total_return, sharpe_ratio, max_drawdown 等"
                },
                "strategy_name": {"type": "string", "description": "策略名称"},
                "format": {
                    "type": "string", 
                    "enum": ["html", "pdf", "md", "json"],
                    "default": "html",
                    "description": "报告格式"
                },
                "title": {"type": "string", "description": "报告标题"},
                "include_charts": {"type": "boolean", "default": True},
                "theme": {"type": "string", "enum": ["dark", "light"], "default": "dark"}
            },
            "required": ["metrics"]
        }
    ),
    Tool(
        name="report.compare",
        description="生成策略对比报告",
        inputSchema={
            "type": "object",
            "properties": {
                "strategies": {
                    "type": "array",
                    "description": "策略结果列表，每个包含 name, total_return, sharpe_ratio 等"
                },
                "title": {"type": "string", "default": "策略对比报告"},
                "format": {"type": "string", "enum": ["html", "md"], "default": "html"}
            },
            "required": ["strategies"]
        }
    ),
    Tool(
        name="report.diagnosis",
        description="生成策略诊断报告（分析优劣势并给出建议）",
        inputSchema={
            "type": "object",
            "properties": {
                "metrics": {
                    "type": "object",
                    "description": "回测指标"
                },
                "strategy_name": {"type": "string", "description": "策略名称"}
            },
            "required": ["metrics"]
        }
    ),
    Tool(
        name="report.list",
        description="列出已生成的报告",
        inputSchema={
            "type": "object",
            "properties": {
                "report_type": {
                    "type": "string",
                    "enum": ["backtest", "comparison", "diagnosis", "factor", "risk"],
                    "description": "报告类型筛选"
                },
                "limit": {"type": "integer", "default": 20}
            }
        }
    ),
    Tool(
        name="report.get",
        description="获取报告详情",
        inputSchema={
            "type": "object",
            "properties": {
                "report_id": {"type": "string", "description": "报告ID"}
            },
            "required": ["report_id"]
        }
    ),
    Tool(
        name="report.delete",
        description="删除报告",
        inputSchema={
            "type": "object",
            "properties": {
                "report_id": {"type": "string", "description": "报告ID"}
            },
            "required": ["report_id"]
        }
    ),
    Tool(
        name="report.summary",
        description="快速生成策略摘要（Markdown 格式）",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string", "description": "策略类型 momentum/mean_reversion"},
                "start_date": {"type": "string"},
                "end_date": {"type": "string"}
            },
            "required": ["strategy", "start_date", "end_date"]
        }
    )
]


@server.list_tools()
async def list_tools():
    return TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if name == "report.generate":
            result = await _handle_generate(arguments)
        elif name == "report.compare":
            result = await _handle_compare(arguments)
        elif name == "report.diagnosis":
            result = await _handle_diagnosis(arguments)
        elif name == "report.list":
            result = await _handle_list(arguments)
        elif name == "report.get":
            result = await _handle_get(arguments)
        elif name == "report.delete":
            result = await _handle_delete(arguments)
        elif name == "report.summary":
            result = await _handle_summary(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        logger.exception(f"工具调用失败: {name}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_generate(args: Dict) -> Dict:
    """生成报告"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import generate_report, ReportConfig
    
    metrics = args["metrics"]
    strategy_name = args.get("strategy_name", "策略")
    format_type = args.get("format", "html")
    title = args.get("title", f"{strategy_name} - 回测报告")
    
    # 构建结果对象
    result = {"metrics": metrics}
    
    output = generate_report(
        result=result,
        report_type="backtest",
        format=format_type,
        strategy_name=strategy_name,
        title=title,
        theme=args.get("theme", "dark"),
        include_charts=args.get("include_charts", True)
    )
    
    return output


async def _handle_compare(args: Dict) -> Dict:
    """生成对比报告"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import get_report_manager, ReportConfig, ReportType, ReportFormat
    
    manager = get_report_manager()
    
    strategies = args["strategies"]
    title = args.get("title", "策略对比报告")
    format_type = args.get("format", "html")
    
    # 转换策略数据
    results = {}
    for s in strategies:
        name = s.get("name", "未命名")
        results[name] = {"metrics": s}
    
    config = ReportConfig(
        report_type=ReportType.COMPARISON,
        format=ReportFormat(format_type),
        title=title
    )
    
    file_path, metadata = manager.generate_comparison_report(results, config)
    
    return {
        "success": True,
        "report_id": metadata.report_id,
        "file_path": file_path,
        "strategies_count": len(strategies)
    }


async def _handle_diagnosis(args: Dict) -> Dict:
    """生成诊断报告"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import get_report_manager, ReportConfig, ReportType
    
    manager = get_report_manager()
    
    metrics = args["metrics"]
    strategy_name = args.get("strategy_name", "策略")
    
    result = {"metrics": metrics}
    
    file_path, metadata = manager.generate_diagnosis_report(
        result, strategy_name
    )
    
    return {
        "success": True,
        "report_id": metadata.report_id,
        "file_path": file_path,
        "diagnosis_score": metadata.summary.get("diagnosis_score", 0)
    }


async def _handle_list(args: Dict) -> Dict:
    """列出报告"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import list_reports
    
    report_type = args.get("report_type")
    limit = args.get("limit", 20)
    
    return list_reports(report_type, limit)


async def _handle_get(args: Dict) -> Dict:
    """获取报告详情"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import get_report
    
    report_id = args["report_id"]
    
    result = get_report(report_id)
    
    # 不返回完整内容，太大
    if "content" in result:
        result["content_length"] = len(result["content"]) if result["content"] else 0
        del result["content"]
    
    return result


async def _handle_delete(args: Dict) -> Dict:
    """删除报告"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.reporting import get_report_manager
    
    manager = get_report_manager()
    report_id = args["report_id"]
    
    success = manager.delete_report(report_id)
    
    return {
        "success": success,
        "report_id": report_id,
        "message": "报告已删除" if success else "报告不存在"
    }


async def _handle_summary(args: Dict) -> Dict:
    """快速生成策略摘要"""
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.backtest import quick_backtest
    from core.data import get_data_provider
    
    provider = get_data_provider()
    stocks = provider.get_index_stocks(count=20)
    
    result = quick_backtest(
        securities=stocks,
        start_date=args["start_date"],
        end_date=args["end_date"],
        strategy=args["strategy"],
        use_mock=True
    )
    
    # 评级
    if result.sharpe_ratio > 1.5:
        rating = "⭐⭐⭐⭐⭐ 优秀"
    elif result.sharpe_ratio > 1.0:
        rating = "⭐⭐⭐⭐ 良好"
    elif result.sharpe_ratio > 0.5:
        rating = "⭐⭐⭐ 一般"
    elif result.sharpe_ratio > 0:
        rating = "⭐⭐ 较弱"
    else:
        rating = "⭐ 需改进"
    
    summary = f"""## {args['strategy']} 策略摘要

**回测期间**: {args['start_date']} ~ {args['end_date']}

### 绩效指标
| 指标 | 数值 |
|------|------|
| 总收益率 | {result.total_return*100:.2f}% |
| 年化收益 | {result.annual_return*100:.2f}% |
| 夏普比率 | {result.sharpe_ratio:.2f} |
| 最大回撤 | {result.max_drawdown*100:.2f}% |
| 胜率 | {result.win_rate*100:.1f}% |
| 交易次数 | {result.total_trades} |

### 综合评价
**评级**: {rating}

"""
    
    if result.sharpe_ratio > 1.0 and abs(result.max_drawdown) < 0.15:
        summary += "✅ 策略风险收益比良好，可以考虑进一步优化后实盘\n"
    elif result.total_return > 0:
        summary += "⚠️ 策略盈利但需关注风险控制\n"
    else:
        summary += "❌ 策略需要优化，建议调整参数或选股逻辑\n"
    
    return {
        "success": True,
        "strategy": args["strategy"],
        "summary": summary,
        "rating": rating,
        "metrics": {
            "total_return": result.total_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown": result.max_drawdown
        }
    }


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
