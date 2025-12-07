"""报告模块

生成回测和实盘分析报告
"""

from .report_generator import ReportGenerator, generate_backtest_report
from .ai_analyzer import AIAnalyzer, analyze_backtest

__all__ = [
    "ReportGenerator",
    "generate_backtest_report",
    "AIAnalyzer",
    "analyze_backtest",
]



