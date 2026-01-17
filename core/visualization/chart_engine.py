"""
图表引擎
========

提供专业的市场分析图表：
1. K线图 + 技术指标叠加
2. 多周期共振热力图
3. 状态转换概率矩阵
4. 回测净值曲线
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 尝试导入可视化库
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # 创建占位符以避免类型注解错误
    go = None
    make_subplots = None
    logger.warning("Plotly not available. Install with: pip install plotly")

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    logger.warning("Matplotlib not available. Install with: pip install matplotlib")


class ChartEngine:
    """
    图表引擎
    
    支持Plotly（交互式）和Matplotlib（静态）两种后端。
    """
    
    def __init__(self, backend: str = "auto"):
        """
        初始化图表引擎
        
        Args:
            backend: 图表后端 ("plotly", "matplotlib", "auto")
        """
        if backend == "auto":
            self.backend = "plotly" if PLOTLY_AVAILABLE else "matplotlib"
        else:
            self.backend = backend
        
        # 主题配置
        self.colors = {
            "up": "#00C853",      # 上涨绿色
            "down": "#F44336",    # 下跌红色
            "neutral": "#9E9E9E", # 中性灰色
            "ma5": "#2196F3",     # MA5蓝色
            "ma10": "#FF9800",    # MA10橙色
            "ma20": "#9C27B0",    # MA20紫色
            "ma60": "#795548",    # MA60棕色
            "volume": "#607D8B",  # 成交量灰色
            "background": "#FAFAFA",
            "grid": "#E0E0E0",
        }
        
        logger.info(f"ChartEngine initialized with backend: {self.backend}")
    
    def plot_candlestick_with_indicators(
        self,
        df: pd.DataFrame,
        ma_periods: List[int] = [5, 20, 60],
        show_volume: bool = True,
        show_macd: bool = True,
        title: str = "K线图",
        height: int = 800,
    ) -> Any:
        """
        绘制K线图 + 技术指标
        
        Args:
            df: OHLCV数据，需包含 open, high, low, close, volume
            ma_periods: 均线周期列表
            show_volume: 是否显示成交量
            show_macd: 是否显示MACD
            title: 图表标题
            height: 图表高度
        
        Returns:
            Plotly Figure 或 Matplotlib Figure
        """
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            return self._plotly_candlestick(df, ma_periods, show_volume, show_macd, title, height)
        elif MATPLOTLIB_AVAILABLE:
            return self._matplotlib_candlestick(df, ma_periods, show_volume, show_macd, title)
        else:
            logger.error("No visualization backend available")
            return None
    
    def _plotly_candlestick(
        self,
        df: pd.DataFrame,
        ma_periods: List[int],
        show_volume: bool,
        show_macd: bool,
        title: str,
        height: int,
    ) -> Any:  # 使用 Any 避免 plotly 未安装时的类型错误
        """Plotly实现的K线图"""
        # 计算子图数量
        rows = 1 + int(show_volume) + int(show_macd)
        row_heights = [0.6] if rows == 1 else ([0.5, 0.2, 0.3] if rows == 3 else [0.7, 0.3])
        
        fig = make_subplots(
            rows=rows,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=row_heights[:rows],
            subplot_titles=[title] + (["成交量"] if show_volume else []) + (["MACD"] if show_macd else [])
        )
        
        # K线图
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="K线",
                increasing_line_color=self.colors["up"],
                decreasing_line_color=self.colors["down"],
            ),
            row=1, col=1
        )
        
        # 均线
        ma_colors = ["#2196F3", "#FF9800", "#9C27B0", "#795548"]
        for i, period in enumerate(ma_periods):
            ma = df["close"].rolling(period).mean()
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=ma,
                    name=f"MA{period}",
                    line=dict(color=ma_colors[i % len(ma_colors)], width=1),
                ),
                row=1, col=1
            )
        
        current_row = 2
        
        # 成交量
        if show_volume and "volume" in df.columns:
            colors = [self.colors["up"] if df["close"].iloc[i] >= df["open"].iloc[i] 
                     else self.colors["down"] for i in range(len(df))]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["volume"],
                    name="成交量",
                    marker_color=colors,
                    opacity=0.7,
                ),
                row=current_row, col=1
            )
            current_row += 1
        
        # MACD
        if show_macd:
            macd, signal, hist = self._calc_macd(df["close"])
            
            # MACD线和信号线
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=macd, name="MACD",
                    line=dict(color="#2196F3", width=1)
                ),
                row=current_row, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=signal, name="Signal",
                    line=dict(color="#FF9800", width=1)
                ),
                row=current_row, col=1
            )
            
            # 柱状图
            colors = [self.colors["up"] if h >= 0 else self.colors["down"] for h in hist]
            fig.add_trace(
                go.Bar(
                    x=df.index, y=hist, name="MACD Hist",
                    marker_color=colors, opacity=0.7
                ),
                row=current_row, col=1
            )
        
        # 布局设置
        fig.update_layout(
            height=height,
            xaxis_rangeslider_visible=False,
            template="plotly_white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        
        return fig
    
    def _matplotlib_candlestick(
        self,
        df: pd.DataFrame,
        ma_periods: List[int],
        show_volume: bool,
        show_macd: bool,
        title: str,
    ) -> plt.Figure:
        """Matplotlib实现的K线图"""
        rows = 1 + int(show_volume) + int(show_macd)
        fig, axes = plt.subplots(rows, 1, figsize=(14, 4 * rows), sharex=True)
        
        if rows == 1:
            axes = [axes]
        
        ax_main = axes[0]
        
        # K线图（简化版：收盘价折线）
        ax_main.plot(df.index, df["close"], color=self.colors["neutral"], linewidth=1, alpha=0.5)
        
        # 填充涨跌区域
        for i in range(1, len(df)):
            if df["close"].iloc[i] >= df["close"].iloc[i-1]:
                ax_main.fill_between(
                    [df.index[i-1], df.index[i]],
                    [df["low"].iloc[i-1], df["low"].iloc[i]],
                    [df["high"].iloc[i-1], df["high"].iloc[i]],
                    color=self.colors["up"], alpha=0.3
                )
            else:
                ax_main.fill_between(
                    [df.index[i-1], df.index[i]],
                    [df["low"].iloc[i-1], df["low"].iloc[i]],
                    [df["high"].iloc[i-1], df["high"].iloc[i]],
                    color=self.colors["down"], alpha=0.3
                )
        
        # 均线
        ma_colors = ["#2196F3", "#FF9800", "#9C27B0", "#795548"]
        for i, period in enumerate(ma_periods):
            ma = df["close"].rolling(period).mean()
            ax_main.plot(df.index, ma, label=f"MA{period}", 
                        color=ma_colors[i % len(ma_colors)], linewidth=1)
        
        ax_main.set_title(title)
        ax_main.legend(loc="upper left")
        ax_main.grid(True, alpha=0.3)
        
        current_row = 1
        
        # 成交量
        if show_volume and "volume" in df.columns:
            ax_vol = axes[current_row]
            colors = [self.colors["up"] if df["close"].iloc[i] >= df["open"].iloc[i] 
                     else self.colors["down"] for i in range(len(df))]
            ax_vol.bar(df.index, df["volume"], color=colors, alpha=0.7)
            ax_vol.set_ylabel("成交量")
            ax_vol.grid(True, alpha=0.3)
            current_row += 1
        
        # MACD
        if show_macd:
            ax_macd = axes[current_row]
            macd, signal, hist = self._calc_macd(df["close"])
            
            ax_macd.plot(df.index, macd, label="MACD", color="#2196F3", linewidth=1)
            ax_macd.plot(df.index, signal, label="Signal", color="#FF9800", linewidth=1)
            
            colors = [self.colors["up"] if h >= 0 else self.colors["down"] for h in hist]
            ax_macd.bar(df.index, hist, color=colors, alpha=0.7)
            ax_macd.axhline(y=0, color="black", linewidth=0.5)
            ax_macd.set_ylabel("MACD")
            ax_macd.legend(loc="upper left")
            ax_macd.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_resonance_heatmap(
        self,
        history: List[Dict],
        title: str = "多周期共振热力图",
    ) -> Any:
        """
        绘制多周期共振热力图
        
        Args:
            history: 历史分析结果列表，每个元素包含 date, short_score, medium_score, long_score
            title: 图表标题
        
        Returns:
            Figure对象
        """
        if not history:
            logger.warning("No history data for resonance heatmap")
            return None
        
        dates = [h["date"] for h in history]
        short_scores = [h.get("short_score", 0) for h in history]
        medium_scores = [h.get("medium_score", 0) for h in history]
        long_scores = [h.get("long_score", 0) for h in history]
        
        data = np.array([short_scores, medium_scores, long_scores])
        
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            fig = go.Figure(data=go.Heatmap(
                z=data,
                x=dates,
                y=["短期", "中期", "长期"],
                colorscale=[
                    [0, "#F44336"],      # -100 红色
                    [0.5, "#FFFFFF"],    # 0 白色
                    [1, "#00C853"],      # +100 绿色
                ],
                zmid=0,
                colorbar=dict(title="得分"),
            ))
            fig.update_layout(
                title=title,
                xaxis_title="日期",
                yaxis_title="周期",
                height=300,
            )
            return fig
        
        elif MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(14, 4))
            im = ax.imshow(data, aspect="auto", cmap="RdYlGn", vmin=-100, vmax=100)
            
            ax.set_yticks([0, 1, 2])
            ax.set_yticklabels(["短期", "中期", "长期"])
            
            # 简化x轴标签
            step = max(1, len(dates) // 10)
            ax.set_xticks(range(0, len(dates), step))
            ax.set_xticklabels([dates[i] for i in range(0, len(dates), step)], rotation=45)
            
            plt.colorbar(im, label="得分")
            ax.set_title(title)
            plt.tight_layout()
            return fig
        
        return None
    
    def plot_backtest_curve(
        self,
        portfolio_values: pd.Series,
        benchmark_values: pd.Series = None,
        drawdown: pd.Series = None,
        title: str = "回测净值曲线",
        height: int = 500,
    ) -> Any:
        """
        绘制回测净值曲线
        
        Args:
            portfolio_values: 策略净值序列
            benchmark_values: 基准净值序列
            drawdown: 回撤序列
            title: 图表标题
            height: 图表高度
        
        Returns:
            Figure对象
        """
        show_dd = drawdown is not None
        
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            rows = 2 if show_dd else 1
            fig = make_subplots(
                rows=rows, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.05,
                row_heights=[0.7, 0.3] if show_dd else [1.0],
            )
            
            # 净值曲线
            fig.add_trace(
                go.Scatter(
                    x=portfolio_values.index,
                    y=portfolio_values,
                    name="策略净值",
                    line=dict(color="#2196F3", width=2),
                ),
                row=1, col=1
            )
            
            if benchmark_values is not None:
                fig.add_trace(
                    go.Scatter(
                        x=benchmark_values.index,
                        y=benchmark_values,
                        name="基准净值",
                        line=dict(color="#9E9E9E", width=1),
                    ),
                    row=1, col=1
                )
            
            # 回撤曲线
            if show_dd:
                fig.add_trace(
                    go.Scatter(
                        x=drawdown.index,
                        y=drawdown * 100,  # 转为百分比
                        name="回撤",
                        fill="tozeroy",
                        line=dict(color="#F44336", width=1),
                    ),
                    row=2, col=1
                )
                fig.update_yaxes(title_text="回撤(%)", row=2, col=1)
            
            fig.update_layout(
                title=title,
                height=height,
                template="plotly_white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
            )
            fig.update_yaxes(title_text="净值", row=1, col=1)
            
            return fig
        
        elif MATPLOTLIB_AVAILABLE:
            rows = 2 if show_dd else 1
            fig, axes = plt.subplots(rows, 1, figsize=(14, 4 * rows), sharex=True)
            
            if rows == 1:
                axes = [axes]
            
            # 净值曲线
            axes[0].plot(portfolio_values.index, portfolio_values, 
                        label="策略净值", color="#2196F3", linewidth=2)
            if benchmark_values is not None:
                axes[0].plot(benchmark_values.index, benchmark_values,
                            label="基准净值", color="#9E9E9E", linewidth=1)
            axes[0].set_ylabel("净值")
            axes[0].legend(loc="upper left")
            axes[0].grid(True, alpha=0.3)
            axes[0].set_title(title)
            
            # 回撤曲线
            if show_dd:
                axes[1].fill_between(drawdown.index, 0, drawdown * 100, 
                                    color="#F44336", alpha=0.5)
                axes[1].set_ylabel("回撤(%)")
                axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            return fig
        
        return None
    
    def plot_phase_distribution(
        self,
        phases: List[str],
        title: str = "市场阶段分布",
    ) -> Any:
        """
        绘制市场阶段分布饼图
        
        Args:
            phases: 市场阶段列表
            title: 图表标题
        
        Returns:
            Figure对象
        """
        from collections import Counter
        phase_counts = Counter(phases)
        
        labels = list(phase_counts.keys())
        values = list(phase_counts.values())
        
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                textinfo="label+percent",
            )])
            fig.update_layout(title=title, height=400)
            return fig
        
        elif MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
            ax.set_title(title)
            return fig
        
        return None
    
    def _calc_macd(
        self,
        close: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算MACD"""
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        return macd, signal_line, histogram
    
    def plot_signal_accuracy(
        self,
        accuracy_data: Dict[str, float],
        title: str = "信号准确率",
    ) -> Any:
        """
        绘制信号准确率柱状图
        
        Args:
            accuracy_data: {信号名称: 准确率} 字典
            title: 图表标题
        
        Returns:
            Figure对象
        """
        labels = list(accuracy_data.keys())
        values = list(accuracy_data.values())
        
        # 根据准确率设置颜色
        colors = [self.colors["up"] if v >= 0.55 else 
                 (self.colors["neutral"] if v >= 0.45 else self.colors["down"])
                 for v in values]
        
        if self.backend == "plotly" and PLOTLY_AVAILABLE:
            fig = go.Figure(data=[go.Bar(
                x=labels,
                y=[v * 100 for v in values],
                marker_color=colors,
                text=[f"{v*100:.1f}%" for v in values],
                textposition="outside",
            )])
            
            # 添加基准线
            fig.add_hline(y=55, line_dash="dash", line_color="green", 
                         annotation_text="目标55%")
            fig.add_hline(y=50, line_dash="dot", line_color="gray",
                         annotation_text="随机50%")
            
            fig.update_layout(
                title=title,
                yaxis_title="准确率(%)",
                height=400,
                template="plotly_white",
            )
            return fig
        
        elif MATPLOTLIB_AVAILABLE:
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(labels, [v * 100 for v in values], color=colors)
            
            # 添加数值标签
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                       f"{val*100:.1f}%", ha="center", va="bottom")
            
            # 添加基准线
            ax.axhline(y=55, linestyle="--", color="green", label="目标55%")
            ax.axhline(y=50, linestyle=":", color="gray", label="随机50%")
            
            ax.set_ylabel("准确率(%)")
            ax.set_title(title)
            ax.legend()
            ax.grid(True, axis="y", alpha=0.3)
            
            plt.tight_layout()
            return fig
        
        return None

    # ========================================================================
    # 多指数对比功能 (新增)
    # ========================================================================
    
    def plot_multi_index_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        chart_type: str = "price",
        normalize: bool = True,
        ma_periods: List[int] = [20, 60],
        title: str = "多指数对比",
        height: int = 600,
    ) -> Any:
        """
        绘制多指数对比图
        
        Args:
            data_dict: {指数名称: DataFrame} 字典，每个DataFrame需包含 open, high, low, close, volume
            chart_type: 图表类型 ("price", "return", "volatility", "correlation")
            normalize: 是否归一化（以第一天为基准100）
            ma_periods: 均线周期列表
            title: 图表标题
            height: 图表高度
        
        Returns:
            Figure对象
            
        使用示例:
            ce = ChartEngine()
            data = {
                "上证指数": df_sh,
                "深证成指": df_sz,
                "创业板指": df_cyb,
                "科创50": df_kc50,
            }
            fig = ce.plot_multi_index_comparison(data, chart_type="price")
        """
        if not data_dict:
            logger.warning("No data provided for multi-index comparison")
            return None
        
        if chart_type == "price":
            return self._plot_multi_price_comparison(data_dict, normalize, ma_periods, title, height)
        elif chart_type == "return":
            return self._plot_multi_return_comparison(data_dict, title, height)
        elif chart_type == "volatility":
            return self._plot_multi_volatility_comparison(data_dict, title, height)
        elif chart_type == "correlation":
            return self._plot_correlation_heatmap(data_dict, title)
        else:
            logger.warning(f"Unknown chart_type: {chart_type}")
            return None
    
    def _plot_multi_price_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        normalize: bool,
        ma_periods: List[int],
        title: str,
        height: int,
    ) -> Any:
        """多指数价格走势对比"""
        if not PLOTLY_AVAILABLE:
            logger.warning("Plotly not available for multi-index comparison")
            return None
        
        # 颜色配置
        index_colors = {
            "上证指数": "#F44336",   # 红色
            "深证成指": "#2196F3",   # 蓝色
            "创业板指": "#4CAF50",   # 绿色
            "科创50": "#FF9800",     # 橙色
            "default": ["#9C27B0", "#00BCD4", "#795548", "#607D8B"]
        }
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.7, 0.3],
            subplot_titles=[title, "相对强度 (RS)"]
        )
        
        color_idx = 0
        first_index_name = None
        first_close = None
        
        for idx_name, df in data_dict.items():
            if df is None or df.empty:
                continue
            
            # 获取颜色
            if idx_name in index_colors:
                color = index_colors[idx_name]
            else:
                color = index_colors["default"][color_idx % len(index_colors["default"])]
                color_idx += 1
            
            close = df["close"].copy()
            
            # 归一化
            if normalize:
                close = (close / close.iloc[0]) * 100
            
            # 价格曲线
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=close,
                    name=idx_name,
                    line=dict(color=color, width=2),
                    hovertemplate=f"{idx_name}<br>日期: %{{x}}<br>价格: %{{y:.2f}}<extra></extra>",
                ),
                row=1, col=1
            )
            
            # 计算相对强度（相对第一个指数）
            if first_close is None:
                first_index_name = idx_name
                first_close = close.copy()
            else:
                # 相对强度 = 当前指数 / 第一个指数 * 100
                rs = (close / first_close) * 100
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=rs,
                        name=f"{idx_name} vs {first_index_name}",
                        line=dict(color=color, width=1.5),
                        hovertemplate=f"{idx_name}/{first_index_name}<br>RS: %{{y:.2f}}<extra></extra>",
                    ),
                    row=2, col=1
                )
        
        # 添加RS=100基准线
        if first_close is not None:
            fig.add_hline(y=100, line_dash="dash", line_color="gray", 
                         annotation_text="RS=100", row=2, col=1)
        
        # 布局设置
        fig.update_layout(
            height=height,
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            hovermode="x unified",
        )
        
        fig.update_yaxes(title_text="价格" + (" (归一化=100)" if normalize else ""), row=1, col=1)
        fig.update_yaxes(title_text="相对强度", row=2, col=1)
        
        return fig
    
    def _plot_multi_return_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        title: str,
        height: int,
    ) -> Any:
        """多指数收益率对比"""
        if not PLOTLY_AVAILABLE:
            return None
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=["日收益率分布", "累计收益率", "滚动波动率(20日)", "收益率统计"]
        )
        
        index_colors = ["#F44336", "#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#00BCD4"]
        
        stats_data = []
        
        for i, (idx_name, df) in enumerate(data_dict.items()):
            if df is None or df.empty:
                continue
            
            color = index_colors[i % len(index_colors)]
            
            # 日收益率
            returns = df["close"].pct_change().dropna()
            
            # 收益率分布直方图
            fig.add_trace(
                go.Histogram(
                    x=returns * 100,
                    name=idx_name,
                    marker_color=color,
                    opacity=0.6,
                    nbinsx=50,
                ),
                row=1, col=1
            )
            
            # 累计收益率
            cum_returns = (1 + returns).cumprod() - 1
            fig.add_trace(
                go.Scatter(
                    x=df.index[1:],
                    y=cum_returns * 100,
                    name=idx_name,
                    line=dict(color=color, width=2),
                    showlegend=False,
                ),
                row=1, col=2
            )
            
            # 滚动波动率
            rolling_vol = returns.rolling(20).std() * np.sqrt(252) * 100
            fig.add_trace(
                go.Scatter(
                    x=df.index[1:],
                    y=rolling_vol,
                    name=idx_name,
                    line=dict(color=color, width=1.5),
                    showlegend=False,
                ),
                row=2, col=1
            )
            
            # 统计数据
            stats_data.append({
                "指数": idx_name,
                "年化收益": f"{cum_returns.iloc[-1] / len(returns) * 252 * 100:.2f}%",
                "年化波动": f"{returns.std() * np.sqrt(252) * 100:.2f}%",
                "夏普比率": f"{(returns.mean() / returns.std()) * np.sqrt(252):.2f}",
                "最大回撤": f"{(cum_returns.cummax() - cum_returns).max() * 100:.2f}%",
            })
        
        # 统计表格
        if stats_data:
            header = list(stats_data[0].keys())
            values = [[d[k] for d in stats_data] for k in header]
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=header,
                        fill_color='#f0f0f0',
                        align='center',
                        font=dict(size=12)
                    ),
                    cells=dict(
                        values=values,
                        align='center',
                        font=dict(size=11)
                    )
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            height=height,
            title=title,
            template="plotly_white",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        
        fig.update_xaxes(title_text="日收益率(%)", row=1, col=1)
        fig.update_yaxes(title_text="频次", row=1, col=1)
        fig.update_yaxes(title_text="累计收益(%)", row=1, col=2)
        fig.update_yaxes(title_text="年化波动率(%)", row=2, col=1)
        
        return fig
    
    def _plot_multi_volatility_comparison(
        self,
        data_dict: Dict[str, pd.DataFrame],
        title: str,
        height: int,
    ) -> Any:
        """多指数波动率对比"""
        if not PLOTLY_AVAILABLE:
            return None
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=["滚动波动率对比", "波动率区间分布"]
        )
        
        index_colors = ["#F44336", "#2196F3", "#4CAF50", "#FF9800"]
        vol_data = []
        
        for i, (idx_name, df) in enumerate(data_dict.items()):
            if df is None or df.empty:
                continue
            
            color = index_colors[i % len(index_colors)]
            returns = df["close"].pct_change().dropna()
            
            # 20日滚动波动率
            vol_20 = returns.rolling(20).std() * np.sqrt(252) * 100
            
            fig.add_trace(
                go.Scatter(
                    x=df.index[1:],
                    y=vol_20,
                    name=idx_name,
                    line=dict(color=color, width=1.5),
                ),
                row=1, col=1
            )
            
            vol_data.append(vol_20.dropna().values)
        
        # 波动率箱线图
        if vol_data:
            fig.add_trace(
                go.Box(
                    y=[v for vd in vol_data for v in vd],
                    x=[list(data_dict.keys())[i] for i, vd in enumerate(vol_data) for _ in vd],
                    marker_color="#607D8B",
                ),
                row=1, col=2
            )
        
        fig.update_layout(
            height=height,
            title=title,
            template="plotly_white",
            showlegend=True,
        )
        
        fig.update_yaxes(title_text="年化波动率(%)", row=1, col=1)
        fig.update_yaxes(title_text="年化波动率(%)", row=1, col=2)
        
        return fig
    
    def _plot_correlation_heatmap(
        self,
        data_dict: Dict[str, pd.DataFrame],
        title: str,
    ) -> Any:
        """多指数相关性热力图"""
        if not PLOTLY_AVAILABLE:
            return None
        
        # 构建收益率DataFrame
        returns_dict = {}
        for idx_name, df in data_dict.items():
            if df is not None and not df.empty:
                returns_dict[idx_name] = df["close"].pct_change()
        
        if len(returns_dict) < 2:
            logger.warning("Need at least 2 indices for correlation heatmap")
            return None
        
        returns_df = pd.DataFrame(returns_dict).dropna()
        corr_matrix = returns_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.index,
            colorscale="RdYlGn",
            zmid=0,
            zmin=-1,
            zmax=1,
            text=[[f"{v:.3f}" for v in row] for row in corr_matrix.values],
            texttemplate="%{text}",
            textfont=dict(size=14),
            colorbar=dict(title="相关系数"),
        ))
        
        fig.update_layout(
            title=title,
            height=500,
            template="plotly_white",
        )
        
        return fig
    
    def plot_multi_index_kline_grid(
        self,
        data_dict: Dict[str, pd.DataFrame],
        ma_periods: List[int] = [5, 20, 60],
        title: str = "四大指数K线图",
        height: int = 1000,
    ) -> Any:
        """
        绘制多指数K线图网格 (2x2布局)
        
        Args:
            data_dict: {指数名称: DataFrame} 字典
            ma_periods: 均线周期
            title: 图表标题
            height: 图表高度
        
        Returns:
            Figure对象
        """
        if not PLOTLY_AVAILABLE:
            return None
        
        indices = list(data_dict.keys())
        n = len(indices)
        
        if n == 0:
            return None
        
        # 确定网格布局
        if n <= 2:
            rows, cols = 1, n
        elif n <= 4:
            rows, cols = 2, 2
        else:
            rows = (n + 1) // 2
            cols = 2
        
        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=indices[:rows*cols],
            vertical_spacing=0.08,
            horizontal_spacing=0.05,
        )
        
        ma_colors = ["#2196F3", "#FF9800", "#9C27B0", "#795548"]
        
        for i, (idx_name, df) in enumerate(data_dict.items()):
            if df is None or df.empty or i >= rows * cols:
                continue
            
            row = i // cols + 1
            col = i % cols + 1
            
            # K线
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name=idx_name,
                    increasing_line_color=self.colors["up"],
                    decreasing_line_color=self.colors["down"],
                    showlegend=False,
                ),
                row=row, col=col
            )
            
            # 均线
            for j, period in enumerate(ma_periods):
                ma = df["close"].rolling(period).mean()
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=ma,
                        name=f"MA{period}" if i == 0 else None,
                        line=dict(color=ma_colors[j % len(ma_colors)], width=1),
                        showlegend=(i == 0),
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            height=height,
            title=title,
            template="plotly_white",
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        
        # 隐藏所有K线图的range slider
        for i in range(1, rows * cols + 1):
            fig.update_xaxes(rangeslider_visible=False, row=(i-1)//cols+1, col=(i-1)%cols+1)
        
        return fig






