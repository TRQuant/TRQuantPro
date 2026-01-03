"""
市场状态可视化模块
==================

提供市场状态的多种可视化方式：
1. chart_engine - 专业图表引擎（K线、指标叠加、热力图）
2. dashboard - 综合仪表盘组件
3. report - 报告生成器

使用方法：
    from core.visualization import ChartEngine, Dashboard
    
    engine = ChartEngine()
    fig = engine.plot_market_trend(df, trend_result)
    
    dashboard = Dashboard()
    dashboard.render(state)
"""

from .chart_engine import ChartEngine
from .dashboard import Dashboard, MarketGauge, StatusTimeline

__all__ = [
    "ChartEngine",
    "Dashboard",
    "MarketGauge",
    "StatusTimeline",
]
