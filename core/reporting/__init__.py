# -*- coding: utf-8 -*-
"""
报告生成模块
============
T1.9.1 报告生成系统实现

功能：
1. 回测报告生成（HTML/PDF）
2. 策略分析报告
3. 策略对比报告
4. 报告模板管理
5. GUI 友好的 API 接口
"""

from core.reporting.report_manager import (
    ReportManager,
    ReportConfig,
    ReportType,
    ReportFormat,
    get_report_manager,
    generate_report,
    list_reports,
    get_report,
)

__all__ = [
    "ReportManager",
    "ReportConfig",
    "ReportType",
    "ReportFormat",
    "get_report_manager",
    "generate_report",
    "list_reports",
    "get_report",
]
