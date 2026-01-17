# -*- coding: utf-8 -*-
"""净值曲线图表组件（Plotly版本）"""
from PyQt6.QtWidgets import QWidget
import logging
from typing import Dict, Optional
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from gui.widgets.plotly_chart_widget import PlotlyChartWidget

logger = logging.getLogger(__name__)

class EquityChartWidget(PlotlyChartWidget):
    """净值曲线图表组件（基于Plotly）"""
    def __init__(self, parent=None):
        super().__init__(parent, title="策略净值曲线")
        self.equity_data = None
        self.benchmark_data = None
    
    def plot_equity_curve(self, equity_data: pd.DataFrame, benchmark_data=None, title="策略净值曲线"):
        """绘制净值曲线"""
        self.title = title
        self.equity_data = equity_data
        self.benchmark_data = benchmark_data
        try:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                              subplot_titles=("净值曲线", "回撤曲线"), row_heights=[0.7, 0.3])
            if 'equity' in equity_data.columns:
                normalized = equity_data['equity'] / equity_data['equity'].iloc[0]
            else:
                normalized = equity_data.iloc[:, 0] / equity_data.iloc[:, 0].iloc[0]
            dates = [d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else str(d) for d in equity_data.index]
            fig.add_trace(go.Scatter(x=dates, y=normalized.values, mode='lines+markers',
                                    name='策略净值', line=dict(color='#00ff88', width=2)), row=1, col=1)
            if benchmark_data is not None and not benchmark_data.empty:
                bench_normalized = benchmark_data.iloc[:, 0] / benchmark_data.iloc[:, 0].iloc[0]
                bench_dates = [d.strftime('%Y-%m-%d') if isinstance(d, pd.Timestamp) else str(d) for d in benchmark_data.index]
                fig.add_trace(go.Scatter(x=bench_dates, y=bench_normalized.values, mode='lines+markers',
                                        name='基准净值', line=dict(color='#ff4444', width=2)), row=1, col=1)
            cumulative_max = normalized.cummax()
            drawdown = (normalized - cumulative_max) / cumulative_max * 100
            fig.add_trace(go.Scatter(x=dates, y=drawdown.values, mode='lines', fill='tozeroy',
                                    name='回撤', line=dict(color='#ff4444', width=1),
                                    fillcolor='rgba(255, 68, 68, 0.3)'), row=2, col=1)
            fig.update_xaxes(title_text="日期", row=2, col=1)
            fig.update_yaxes(title_text="净值", row=1, col=1)
            fig.update_yaxes(title_text="回撤 (%)", row=2, col=1)
            fig.update_layout(title=title, hovermode='x unified', height=600, showlegend=True)
            self.plot(fig)
        except Exception as e:
            logger.error(f"绘制净值曲线失败: {e}")
