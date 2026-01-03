# -*- coding: utf-8 -*-
"""
TRQuant 内置插件
===============

包含常用的数据源、策略、可视化等插件
"""

from .jqdata_plugin import JQDataPlugin
from .mock_data_plugin import MockDataPlugin
from .momentum_strategy_plugin import MomentumStrategyPlugin
from .html_report_plugin import HtmlReportPlugin

__all__ = [
    "JQDataPlugin",
    "MockDataPlugin",
    "MomentumStrategyPlugin",
    "HtmlReportPlugin",
]

