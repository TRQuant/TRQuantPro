"""
可视化工具
==========
提供因子分析、组合绩效、优化历史等可视化功能
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    logger.warning("Matplotlib未安装")
    MATPLOTLIB_AVAILABLE = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    logger.warning("Plotly未安装")
    PLOTLY_AVAILABLE = False


def plot_factor_analysis(
    ic_data: pd.Series,
    factor_name: str = "Factor",
    figsize: tuple = (12, 6)
) -> Optional[Any]:
    """绘制因子IC分析图"""
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=ic_data.index, y=ic_data.values,
            mode='lines', name='IC', line=dict(color='blue')
        ))
        ic_mean = ic_data.mean()
        fig.add_hline(y=ic_mean, line_dash="dash", line_color="red",
                     annotation_text=f"Mean IC: {ic_mean:.4f}")
        fig.add_hline(y=0, line_dash="dot", line_color="gray")
        fig.update_layout(
            title=f"{factor_name} - Information Coefficient (IC)",
            xaxis_title="Date", yaxis_title="IC", hovermode='x unified'
        )
        return fig
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(ic_data.index, ic_data.values, label='IC', color='blue')
        ax.axhline(y=ic_data.mean(), color='red', linestyle='--', 
                  label=f'Mean IC: {ic_data.mean():.4f}')
        ax.axhline(y=0, color='gray', linestyle=':', alpha=0.5)
        ax.set_title(f"{factor_name} - Information Coefficient (IC)")
        ax.set_xlabel("Date"); ax.set_ylabel("IC")
        ax.legend(); ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    return None


def plot_portfolio_performance(
    portfolio_returns: pd.Series,
    benchmark_returns: Optional[pd.Series] = None,
    title: str = "Portfolio Performance",
    figsize: tuple = (14, 8)
) -> Optional[Any]:
    """绘制组合绩效图（累计收益+回撤）"""
    if PLOTLY_AVAILABLE:
        fig = make_subplots(rows=2, cols=1,
            subplot_titles=('Cumulative Returns', 'Drawdown'),
            vertical_spacing=0.1, row_heights=[0.7, 0.3])
        
        portfolio_cum = (1 + portfolio_returns).cumprod()
        fig.add_trace(go.Scatter(
            x=portfolio_cum.index, y=portfolio_cum.values,
            mode='lines', name='Portfolio', line=dict(color='blue', width=2)
        ), row=1, col=1)
        
        if benchmark_returns is not None:
            benchmark_cum = (1 + benchmark_returns).cumprod()
            fig.add_trace(go.Scatter(
                x=benchmark_cum.index, y=benchmark_cum.values,
                mode='lines', name='Benchmark', 
                line=dict(color='orange', width=2, dash='dash')
            ), row=1, col=1)
        
        running_max = portfolio_cum.expanding().max()
        drawdown = (portfolio_cum - running_max) / running_max
        fig.add_trace(go.Scatter(
            x=drawdown.index, y=drawdown.values,
            mode='lines', name='Drawdown', fill='tozeroy',
            line=dict(color='red'), fillcolor='rgba(255,0,0,0.3)'
        ), row=2, col=1)
        
        fig.update_layout(title=title, height=800, hovermode='x unified')
        return fig
    elif MATPLOTLIB_AVAILABLE:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, height_ratios=[3, 1])
        portfolio_cum = (1 + portfolio_returns).cumprod()
        ax1.plot(portfolio_cum.index, portfolio_cum.values, label='Portfolio', linewidth=2)
        if benchmark_returns is not None:
            benchmark_cum = (1 + benchmark_returns).cumprod()
            ax1.plot(benchmark_cum.index, benchmark_cum.values, 
                    label='Benchmark', linewidth=2, linestyle='--')
        ax1.set_title(title); ax1.set_ylabel("Cumulative Return")
        ax1.legend(); ax1.grid(True, alpha=0.3)
        
        running_max = portfolio_cum.expanding().max()
        drawdown = (portfolio_cum - running_max) / running_max
        ax2.fill_between(drawdown.index, drawdown.values, 0, color='red', alpha=0.3)
        ax2.plot(drawdown.index, drawdown.values, color='red', linewidth=1)
        ax2.set_xlabel("Date"); ax2.set_ylabel("Drawdown")
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    return None


def plot_optimization_history(
    study_history: Dict,
    metric_name: str = "Objective Value",
    figsize: tuple = (12, 6)
) -> Optional[Any]:
    """绘制优化历史图"""
    trials = study_history.get("trials", [])
    if not trials:
        logger.warning("没有优化历史数据")
        return None
    
    trial_numbers = [t["number"] for t in trials if t.get("value") is not None]
    values = [t["value"] for t in trials if t.get("value") is not None]
    best_value = study_history.get("best_trial", {}).get("value")
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trial_numbers, y=values,
            mode='markers', name='Trials',
            marker=dict(color='lightblue', size=8)
        ))
        if best_value is not None and values:
            best_values = []
            current_best = values[0]
            for v in values:
                current_best = max(current_best, v)
                best_values.append(current_best)
            fig.add_trace(go.Scatter(
                x=trial_numbers, y=best_values,
                mode='lines', name='Best Value',
                line=dict(color='red', width=2)
            ))
        fig.update_layout(
            title="Optimization History",
            xaxis_title="Trial Number", yaxis_title=metric_name
        )
        return fig
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=figsize)
        ax.scatter(trial_numbers, values, alpha=0.6, label='Trials', color='lightblue')
        if best_value is not None and values:
            best_values = []
            current_best = values[0]
            for v in values:
                current_best = max(current_best, v)
                best_values.append(current_best)
            ax.plot(trial_numbers, best_values, color='red', linewidth=2, label='Best Value')
        ax.set_title("Optimization History")
        ax.set_xlabel("Trial Number"); ax.set_ylabel(metric_name)
        ax.legend(); ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    return None


def plot_factor_quantile_returns(
    quantile_returns: pd.DataFrame,
    factor_name: str = "Factor",
    figsize: tuple = (12, 6)
) -> Optional[Any]:
    """绘制因子分位数收益图"""
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        for col in quantile_returns.columns:
            fig.add_trace(go.Bar(
                x=quantile_returns.index,
                y=quantile_returns[col],
                name=f"Quantile {col}"
            ))
        fig.update_layout(
            title=f"{factor_name} - Returns by Quantile",
            xaxis_title="Quantile", yaxis_title="Mean Return", barmode='group'
        )
        return fig
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=figsize)
        quantile_returns.plot(kind='bar', ax=ax)
        ax.set_title(f"{factor_name} - Returns by Quantile")
        ax.set_xlabel("Quantile"); ax.set_ylabel("Mean Return")
        ax.legend(title="Period"); ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    return None

def plot_market_trend(
    price_data: pd.DataFrame,
    ma_periods: list = [5, 20, 60],
    volume_data: Optional[pd.Series] = None,
    title: str = "Market Trend Analysis",
    figsize: tuple = (14, 10)
) -> Optional[Any]:
    """绘制市场趋势图（价格+均线+成交量）"""
    if price_data is None or price_data.empty or 'close' not in price_data.columns:
        logger.error("价格数据无效")
        return None
    
    if PLOTLY_AVAILABLE:
        rows = 2 if volume_data is not None else 1
        row_heights = [0.7, 0.3] if volume_data is not None else [1.0]
        subplot_titles = ['Price & Moving Averages'] + (['Volume'] if volume_data is not None else [])
        
        fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                           row_heights=row_heights, subplot_titles=subplot_titles)
        
        fig.add_trace(go.Scatter(x=price_data.index, y=price_data['close'], mode='lines',
                                name='Close Price', line=dict(color='black', width=2)), row=1, col=1)
        
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        for i, period in enumerate(ma_periods):
            if len(price_data) >= period:
                ma = price_data['close'].rolling(period).mean()
                fig.add_trace(go.Scatter(x=price_data.index, y=ma, mode='lines', name=f'MA{period}',
                                        line=dict(color=colors[i % len(colors)], width=1.5, dash='dash')), row=1, col=1)
        
        if volume_data is not None:
            fig.add_trace(go.Bar(x=volume_data.index, y=volume_data.values, name='Volume',
                                marker_color='lightblue', opacity=0.6), row=2, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
        
        fig.update_xaxes(title_text="Date", row=rows, col=1)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_layout(title=title, height=800 if volume_data is not None else 600,
                         hovermode='x unified', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        fig, axes = plt.subplots(2 if volume_data is not None else 1, 1, figsize=figsize,
                                 height_ratios=[3, 1] if volume_data is not None else [1], sharex=True)
        ax1 = axes[0] if volume_data is not None else axes
        
        ax1.plot(price_data.index, price_data['close'], label='Close Price', color='black', linewidth=2)
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        for i, period in enumerate(ma_periods):
            if len(price_data) >= period:
                ma = price_data['close'].rolling(period).mean()
                ax1.plot(price_data.index, ma, label=f'MA{period}',
                        color=colors[i % len(colors)], linewidth=1.5, linestyle='--')
        
        ax1.set_ylabel('Price')
        ax1.set_title(title)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        if volume_data is not None:
            axes[1].bar(volume_data.index, volume_data.values, color='lightblue', alpha=0.6, label='Volume')
            axes[1].set_ylabel('Volume')
            axes[1].set_xlabel('Date')
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        else:
            ax1.set_xlabel('Date')
        
        plt.tight_layout()
        return fig
    
    return None


def plot_market_comparison(
    index_data: Dict[str, pd.Series],
    normalize: bool = True,
    title: str = "Market Index Comparison",
    figsize: tuple = (14, 6)
) -> Optional[Any]:
    """绘制多个市场指数对比图"""
    if not index_data:
        logger.error("指数数据为空")
        return None
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        for name, series in index_data.items():
            values = (series / series.iloc[0]) * 100 if normalize and len(series) > 0 else series
            fig.add_trace(go.Scatter(x=series.index, y=values, mode='lines', name=name, line=dict(width=2)))
        fig.update_layout(title=title, xaxis_title="Date",
                         yaxis_title="Normalized Price (Base=100)" if normalize else "Price",
                         hovermode='x unified', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01), height=600)
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=figsize)
        for name, series in index_data.items():
            values = (series / series.iloc[0]) * 100 if normalize and len(series) > 0 else series
            ax.plot(series.index, values, label=name, linewidth=2)
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.set_ylabel("Normalized Price (Base=100)" if normalize else "Price")
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    return None


def plot_returns_distribution(
    returns: pd.Series,
    title: str = "Returns Distribution",
    figsize: tuple = (12, 6)
) -> Optional[Any]:
    """绘制收益率分布图"""
    if returns is None or returns.empty:
        logger.error("收益率数据无效")
        return None
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=returns.values, nbinsx=50, name='Returns',
                                  marker_color='lightblue', opacity=0.7))
        fig.add_vline(x=returns.mean(), line_dash="dot", line_color="green",
                     annotation_text=f"Mean: {returns.mean():.4f}")
        fig.update_layout(title=title, xaxis_title="Returns", yaxis_title="Frequency",
                         hovermode='x unified', height=600)
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=figsize)
        ax.hist(returns.values, bins=50, color='lightblue', alpha=0.7, edgecolor='black')
        ax.axvline(returns.mean(), color='green', linestyle=':', linewidth=2,
                  label=f'Mean: {returns.mean():.4f}')
        ax.set_title(title)
        ax.set_xlabel("Returns")
        ax.set_ylabel("Frequency")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    return None
