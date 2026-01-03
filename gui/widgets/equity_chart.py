# -*- coding: utf-8 -*-
"""
净值曲线图表组件
================

优先使用Plotly绘制交互式回测净值曲线，降级到Matplotlib
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt
import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Plotly净值曲线图（优先）
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from gui.widgets.plotly_chart_widget import PlotlyChartWidget
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly未安装，将使用Matplotlib")

# Matplotlib作为备用
try:
    import matplotlib
    matplotlib.use('QtAgg')
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("Matplotlib未安装，图表功能不可用")


def _find_chinese_font():
    """查找系统中可用的中文字体"""
    chinese_fonts = [
        'Noto Sans CJK JP', 'Noto Sans CJK SC', 'Noto Sans CJK TC',
        'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
        'Source Han Sans CN', 'Source Han Sans SC',
        'SimHei', 'SimSun', 'Microsoft YaHei',
        'PingFang SC', 'Heiti SC', 'STHeiti'
    ]
    
    available_fonts = set([f.name for f in fm.fontManager.ttflist])
    
    for font in chinese_fonts:
        if font in available_fonts:
            return font
    
    return None




class EquityChartWidget(PlotlyChartWidget if PLOTLY_AVAILABLE else QWidget):
    """
    净值曲线图表组件
    
    优先使用Plotly（交互式），降级到Matplotlib（静态）
    """
    """净值曲线图表组件"""
    
    def __init__(self, parent=None):
        if PLOTLY_AVAILABLE:
            super().__init__(parent, title="策略净值曲线")
            self.equity_data: Optional[pd.DataFrame] = None
            self.benchmark_data: Optional[pd.DataFrame] = None
        else:
            super().__init__(parent)
            self.figure = None
            self.canvas = None
            self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        if not MATPLOTLIB_AVAILABLE:
            error_label = QLabel("⚠️ Matplotlib未安装，无法显示图表")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: #ff9800; font-size: 14px;")
            layout.addWidget(error_label)
            return
        
        # 创建图表
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.figure.patch.set_facecolor('#1a1a1a')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.zoom_in_btn = QPushButton("🔍 放大")
        self.zoom_in_btn.clicked.connect(self._zoom_in)
        toolbar.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("🔍 缩小")
        self.zoom_out_btn.clicked.connect(self._zoom_out)
        toolbar.addWidget(self.zoom_out_btn)
        
        self.reset_btn = QPushButton("↩️ 重置")
        self.reset_btn.clicked.connect(self._reset_view)
        toolbar.addWidget(self.reset_btn)
        
        toolbar.addStretch()
        
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar)
        layout.addWidget(toolbar_widget)
    
    def plot_equity_curve(self, 
                          equity_data: pd.DataFrame, 
                          benchmark_data: pd.DataFrame = None,
                          title: str = "策略净值曲线"):
        """
        绘制净值曲线（优先使用Plotly）
        
        Args:
            equity_data: 净值数据 (date为index, equity列为净值)
            benchmark_data: 基准数据 (可选)
            title: 图表标题
        """
        # 优先使用Plotly
        if PLOTLY_AVAILABLE:
            self._plot_equity_curve_plotly(equity_data, benchmark_data, title)
        else:
            # 降级到Matplotlib
            self._plot_equity_curve_matplotlib(equity_data, benchmark_data, title)
    
    def _plot_equity_curve_plotly(self, 
                                   equity_data: pd.DataFrame, 
                                   benchmark_data: Optional[pd.DataFrame] = None,
                                   title: str = "策略净值曲线"):
        """使用Plotly绘制净值曲线"""
        self.title = title
        self.equity_data = equity_data
        self.benchmark_data = benchmark_data
        
        try:
            # 创建子图（净值曲线 + 回撤曲线）
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=("净值曲线", "回撤曲线"),
                row_heights=[0.7, 0.3]
            )
            
            # 归一化净值
            if 'equity' in equity_data.columns:
                equity = equity_data['equity']
                normalized = equity / equity.iloc[0]
            elif 'normalized' in equity_data.columns:
                normalized = equity_data['normalized']
            else:
                normalized = equity_data.iloc[:, 0] / equity_data.iloc[:, 0].iloc[0]
            
            dates = equity_data.index.tolist()
            if isinstance(dates[0], pd.Timestamp):
                dates = [d.strftime('%Y-%m-%d') for d in dates]
            
            # 绘制策略净值
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=normalized.values,
                    mode='lines+markers',
                    name='策略净值',
                    line=dict(color='#00ff88', width=2),
                    marker=dict(size=4),
                    hovertemplate='日期: %{x}<br>净值: %{y:.4f}<extra></extra>'
                ),
                row=1, col=1
            )
            
            # 绘制基准
            if benchmark_data is not None and not benchmark_data.empty:
                if 'close' in benchmark_data.columns:
                    bench_normalized = benchmark_data['close'] / benchmark_data['close'].iloc[0]
                elif 'normalized' in benchmark_data.columns:
                    bench_normalized = benchmark_data['normalized']
                else:
                    bench_normalized = benchmark_data.iloc[:, 0] / benchmark_data.iloc[:, 0].iloc[0]
                
                bench_dates = benchmark_data.index.tolist()
                if isinstance(bench_dates[0], pd.Timestamp):
                    bench_dates = [d.strftime('%Y-%m-%d') for d in bench_dates]
                
                fig.add_trace(
                    go.Scatter(
                        x=bench_dates,
                        y=bench_normalized.values,
                        mode='lines+markers',
                        name='基准净值',
                        line=dict(color='#ff4444', width=2),
                        marker=dict(size=4),
                        hovertemplate='日期: %{x}<br>净值: %{y:.4f}<extra></extra>'
                    ),
                    row=1, col=1
                )
            
            # 计算回撤
            cumulative_max = normalized.cummax()
            drawdown = (normalized - cumulative_max) / cumulative_max * 100
            
            # 绘制回撤曲线
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=drawdown.values,
                    mode='lines',
                    fill='tozeroy',
                    name='回撤',
                    line=dict(color='#ff4444', width=1),
                    fillcolor='rgba(255, 68, 68, 0.3)',
                    hovertemplate='日期: %{x}<br>回撤: %{y:.2f}%<extra></extra>'
                ),
                row=2, col=1
            )
            
            # 更新布局
            fig.update_xaxes(title_text="日期", row=2, col=1)
            fig.update_yaxes(title_text="净值", row=1, col=1)
            fig.update_yaxes(title_text="回撤 (%)", row=2, col=1)
            
            fig.update_layout(
                title=title,
                hovermode='x unified',
                height=600,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # 显示图表
            self.plot(fig)
            
        except Exception as e:
            logger.error(f"绘制Plotly净值曲线失败: {e}")
            import traceback
            traceback.print_exc()
            # 降级到Matplotlib
            if MATPLOTLIB_AVAILABLE:
                self._plot_equity_curve_matplotlib(equity_data, benchmark_data, title)
    
    def _plot_equity_curve_matplotlib(self, equity_data: pd.DataFrame, benchmark_data: Optional[pd.DataFrame] = None, title: str = "策略净值曲线"):
        """使用Matplotlib绘制净值曲线（备用）"""
        if not MATPLOTLIB_AVAILABLE or self.figure is None:
            return
        
        self.figure.clear()
        
        # 设置中文字体
        chinese_font = _find_chinese_font()
        if chinese_font:
            plt.rcParams['font.sans-serif'] = [chinese_font]
            plt.rcParams['axes.unicode_minus'] = False
        
        # 创建子图
        ax1 = self.figure.add_subplot(211)  # 净值曲线
        ax2 = self.figure.add_subplot(212)  # 回撤曲线
        
        # 设置背景色
        ax1.set_facecolor('#1e1e1e')
        ax2.set_facecolor('#1e1e1e')
        
        # 归一化净值
        if 'equity' in equity_data.columns:
            equity = equity_data['equity']
            normalized = equity / equity.iloc[0]
        elif 'normalized' in equity_data.columns:
            normalized = equity_data['normalized']
        else:
            normalized = equity_data.iloc[:, 0] / equity_data.iloc[:, 0].iloc[0]
        
        # 绘制策略净值
        ax1.plot(equity_data.index, normalized, 
                 color='#00ff88', linewidth=1.5, label='策略净值')
        
        # 绘制基准
        if benchmark_data is not None and not benchmark_data.empty:
            if 'close' in benchmark_data.columns:
                bench_normalized = benchmark_data['close'] / benchmark_data['close'].iloc[0]
            else:
                bench_normalized = benchmark_data.iloc[:, 0] / benchmark_data.iloc[:, 0].iloc[0]
            ax1.plot(benchmark_data.index, bench_normalized,
                     color='#ff4444', linewidth=1.5, label='基准净值')
        
        ax1.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax1.set_ylabel('净值', color='white')
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.2, color='#444')
        ax1.tick_params(colors='white')
        
        # 计算回撤
        cumulative_max = normalized.cummax()
        drawdown = (normalized - cumulative_max) / cumulative_max * 100
        
        # 绘制回撤曲线
        ax2.fill_between(equity_data.index, 0, drawdown, 
                         color='#ff4444', alpha=0.3)
        ax2.plot(equity_data.index, drawdown, 
                 color='#ff4444', linewidth=1)
        
        ax2.set_ylabel('回撤 (%)', color='white')
        ax2.set_xlabel('日期', color='white')
        ax2.grid(True, alpha=0.2, color='#444')
        ax2.tick_params(colors='white')
        
        for spine in ax1.spines.values():
            spine.set_color('#444')
        for spine in ax2.spines.values():
            spine.set_color('#444')
        
        self.figure.tight_layout()
        self.canvas.draw()
    def plot_comparison(self, 
                        curves: Dict[str, pd.Series], 
                        title: str = "策略对比"):
        """
        绘制多条曲线对比
        
        Args:
            curves: {名称: 净值序列} 的字典
            title: 图表标题
        """
        if not MATPLOTLIB_AVAILABLE or self.figure is None:
            return
        
        self.figure.clear()
        
        chinese_font = _find_chinese_font()
        if chinese_font:
            plt.rcParams['font.sans-serif'] = [chinese_font]
            plt.rcParams['axes.unicode_minus'] = False
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e1e1e')
        
        colors = ['#00ff88', '#ff8800', '#00aaff', '#ff44aa', '#ffff00']
        
        for i, (name, data) in enumerate(curves.items()):
            color = colors[i % len(colors)]
            normalized = data / data.iloc[0]
            ax.plot(data.index, normalized, 
                   color=color, linewidth=1.5, label=name)
        
        ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax.set_ylabel('净值', color='white')
        ax.set_xlabel('日期', color='white')
        ax.tick_params(colors='white')
        ax.legend(loc='upper left', facecolor='#2a2a2a', edgecolor='#444', labelcolor='white')
        ax.grid(True, alpha=0.2, color='#444')
        
        for spine in ax.spines.values():
            spine.set_color('#444')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_monthly_returns(self, monthly_data: pd.DataFrame, title: str = "月度收益"):
        """
        绘制月度收益柱状图
        
        Args:
            monthly_data: 月度收益数据
            title: 图表标题
        """
        if not MATPLOTLIB_AVAILABLE or self.figure is None:
            return
        
        self.figure.clear()
        
        chinese_font = _find_chinese_font()
        if chinese_font:
            plt.rcParams['font.sans-serif'] = [chinese_font]
            plt.rcParams['axes.unicode_minus'] = False
        
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#1e1e1e')
        
        returns = monthly_data * 100 if monthly_data.max() < 1 else monthly_data
        
        colors = ['#00ff88' if r >= 0 else '#ff4444' for r in returns]
        
        ax.bar(range(len(returns)), returns, color=colors, alpha=0.8)
        
        ax.set_title(title, color='white', fontsize=14, fontweight='bold')
        ax.set_ylabel('收益率 (%)', color='white')
        ax.set_xlabel('月份', color='white')
        ax.tick_params(colors='white')
        ax.axhline(y=0, color='white', linewidth=0.5)
        ax.grid(True, alpha=0.2, color='#444', axis='y')
        
        for spine in ax.spines.values():
            spine.set_color('#444')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def _zoom_in(self):
        """放大"""
        if self.figure:
            for ax in self.figure.axes:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                ax.set_xlim(xlim[0] * 1.1, xlim[1] * 0.9)
                ax.set_ylim(ylim[0] * 1.1, ylim[1] * 0.9)
            self.canvas.draw()
    
    def _zoom_out(self):
        """缩小"""
        if self.figure:
            for ax in self.figure.axes:
                xlim = ax.get_xlim()
                ylim = ax.get_ylim()
                ax.set_xlim(xlim[0] * 0.9, xlim[1] * 1.1)
                ax.set_ylim(ylim[0] * 0.9, ylim[1] * 1.1)
            self.canvas.draw()
    
    def _reset_view(self):
        """重置视图"""
        if self.figure:
            for ax in self.figure.axes:
                ax.autoscale()
            self.canvas.draw()
    
    def export_to_image(self, filename: str):
        """导出为图片"""
        if self.figure:
            self.figure.savefig(filename, dpi=150, facecolor='#1a1a1a', 
                               bbox_inches='tight')
            logger.info(f"图表已导出: {filename}")

