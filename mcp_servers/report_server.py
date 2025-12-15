# -*- coding: utf-8 -*-
"""
报告MCP服务器（标准化版本）
===========================
生成回测报告、策略分析报告
"""

import logging
import json
from typing import Dict, List, Any
from mcp.server.models import InitializationOptions
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

logger = logging.getLogger(__name__)
server = Server("report-server")


TOOLS = [
    Tool(
        name="report.generate",
        description="生成回测报告",
        inputSchema={
            "type": "object",
            "properties": {
                "metrics": {
                    "type": "object",
                    "description": "回测指标，包含total_return, sharpe_ratio等"
                },
                "title": {"type": "string", "description": "报告标题"},
                "daily_returns": {
                    "type": "array",
                    "description": "每日收益率序列（可选）"
                }
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
                    "description": "策略回测结果列表"
                },
                "title": {"type": "string"}
            },
            "required": ["strategies"]
        }
    ),
    Tool(
        name="report.list",
        description="列出已生成的报告",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {"type": "integer", "default": 10}
            }
        }
    ),
    Tool(
        name="report.summary",
        description="生成策略摘要",
        inputSchema={
            "type": "object",
            "properties": {
                "strategy": {"type": "string"},
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
        elif name == "report.list":
            result = await _handle_list(arguments)
        elif name == "report.summary":
            result = await _handle_summary(arguments)
        else:
            result = {"error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, ensure_ascii=False))]


async def _handle_generate(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from core.visualization import generate_html_report
    
    metrics = args["metrics"]
    title = args.get("title", "回测报告")
    daily_returns = args.get("daily_returns")
    
    filepath = generate_html_report(metrics, daily_returns, title)
    
    return {
        "success": True,
        "filepath": filepath,
        "title": title,
        "metrics": {
            k: f"{v*100:.2f}%" if isinstance(v, float) and abs(v) < 10 else v
            for k, v in metrics.items()
        }
    }


async def _handle_compare(args: Dict) -> Dict:
    import sys
    sys.path.insert(0, str(__file__).rsplit("/mcp_servers", 1)[0])
    
    from pathlib import Path
    from datetime import datetime
    
    strategies = args["strategies"]
    title = args.get("title", "策略对比报告")
    
    # 生成对比报告HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial; background: #1a1a2e; color: #eee; padding: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #333; padding: 10px; text-align: center; }}
        th {{ background: #16213e; }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4444; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <table>
        <tr>
            <th>策略</th>
            <th>总收益</th>
            <th>夏普比率</th>
            <th>最大回撤</th>
            <th>胜率</th>
        </tr>
"""
    
    for s in strategies:
        ret_class = "positive" if s.get("return", 0) > 0 else "negative"
        html += f"""
        <tr>
            <td>{s.get('name', 'N/A')}</td>
            <td class="{ret_class}">{s.get('return', 'N/A')}</td>
            <td>{s.get('sharpe', 'N/A')}</td>
            <td class="negative">{s.get('drawdown', 'N/A')}</td>
            <td>{s.get('win_rate', 'N/A')}</td>
        </tr>
"""
    
    html += """
    </table>
</body>
</html>
"""
    
    # 保存
    report_dir = Path(__file__).parent.parent / "reports"
    report_dir.mkdir(exist_ok=True)
    filepath = report_dir / f"compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath.write_text(html, encoding="utf-8")
    
    return {
        "success": True,
        "filepath": str(filepath),
        "strategies_count": len(strategies)
    }


async def _handle_list(args: Dict) -> Dict:
    from pathlib import Path
    
    report_dir = Path(__file__).parent.parent / "reports"
    limit = args.get("limit", 10)
    
    if not report_dir.exists():
        return {"success": True, "reports": [], "count": 0}
    
    reports = sorted(report_dir.glob("*.html"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    return {
        "success": True,
        "count": len(reports),
        "reports": [
            {"name": r.name, "path": str(r)}
            for r in reports[:limit]
        ]
    }


async def _handle_summary(args: Dict) -> Dict:
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
    
    summary = f"""
## {args['strategy']} 策略摘要

**回测期间**: {args['start_date']} ~ {args['end_date']}

### 绩效指标
- 总收益率: {result.total_return*100:.2f}%
- 年化收益: {result.annual_return*100:.2f}%
- 夏普比率: {result.sharpe_ratio:.2f}
- 最大回撤: {result.max_drawdown*100:.2f}%
- 胜率: {result.win_rate*100:.1f}%
- 交易次数: {result.total_trades}

### 评价
"""
    
    if result.sharpe_ratio > 1.5:
        summary += "- 风险调整收益优秀\n"
    elif result.sharpe_ratio > 0.5:
        summary += "- 风险调整收益一般\n"
    else:
        summary += "- 需要进一步优化\n"
    
    return {
        "success": True,
        "strategy": args["strategy"],
        "summary": summary,
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
            InitializationOptions(
                server_name="report-server",
                server_version="2.0.0"
            )
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
