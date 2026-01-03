# -*- coding: utf-8 -*-
"""
图表生成MCP服务器
================

提供统一的图表生成工具，支持Plotly交互式图表。

工具列表:
- chart.equity_curve - 净值曲线图
- chart.candlestick - K线图
- chart.bar - 柱状图
- chart.pie - 饼图
- chart.heatmap - 热力图
- chart.radar - 雷达图
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 确定项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("MCP SDK不可用")

# 导入Plotly
try:
    import plotly.graph_objects as go
    from gui.widgets.plotly_chart_widget import PlotlyChartFactory
    PLOTLY_AVAILABLE = True
except ImportError as e:
    PLOTLY_AVAILABLE = False
    logger.warning(f"Plotly不可用: {e}")

def generate_equity_curve(dates, equity_values, benchmark_values=None, title="净值曲线", save_path=None):
    """生成净值曲线图"""
    if not PLOTLY_AVAILABLE:
        return {"error": "Plotly不可用"}
    try:
        fig = PlotlyChartFactory.create_line_chart(
            x_data=dates, y_data=equity_values, title=title,
            x_label="日期", y_label="净值", series_name="策略净值"
        )
        if benchmark_values:
            fig.add_trace(go.Scatter(x=dates, y=benchmark_values, mode='lines', name='基准净值', line=dict(color="#EF4444")))
        import plotly.offline as pyo
        html_str = pyo.plot(fig, output_type='div', include_plotlyjs='cdn')
        if save_path:
            fig.write_html(save_path)
        return {"success": True, "html": html_str, "title": title, "type": "equity_curve"}
    except Exception as e:
        return {"error": str(e)}

if MCP_AVAILABLE:
    server = Server("chart-server")
    TOOLS = [
        Tool(name="chart.equity_curve", description="生成净值曲线图", 
             inputSchema={"type": "object", "properties": {
                 "dates": {"type": "array", "items": {"type": "string"}},
                 "equity_values": {"type": "array", "items": {"type": "number"}},
                 "benchmark_values": {"type": "array", "items": {"type": "number"}},
                 "title": {"type": "string", "default": "净值曲线"},
                 "save_path": {"type": "string"}
             }, "required": ["dates", "equity_values"]})
    ]
    @server.list_tools()
    async def list_tools():
        return TOOLS
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict) -> List[TextContent]:
        if name == "chart.equity_curve":
            result = generate_equity_curve(**arguments)
            return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
        return [TextContent(type="text", text=json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False))]
    if __name__ == "__main__":
        import asyncio
        asyncio.run(mcp.server.stdio.stdio_server(server))
