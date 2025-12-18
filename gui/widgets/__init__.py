# -*- coding: utf-8 -*-
"""
韬睿量化GUI组件
"""

from .factor_panel import FactorPanel
from .factor_builder_panel import FactorBuilderPanel
from .user_guide_dialog import UserGuideDialog
from .data_source_panel import DataSourcePanel
from .strategy_dev_panel import StrategyDevPanel
from .mainline_panel import MainlinePanel

__all__ = [
    'FactorPanel',
    'FactorBuilderPanel',
    'UserGuideDialog',
    'DataSourcePanel',
    'StrategyDevPanel',
    'MainlinePanel',
]


# 新增面板
from .backtest_progress_panel import BacktestProgressPanel, BacktestWorker
from .backtest_result_panel import BacktestResultPanel, MetricCard, SimpleChart
from .strategy_manager_panel import StrategyManagerPanel, StrategyConfigDialog
from .report_viewer_panel import ReportViewerPanel, ReportCard
