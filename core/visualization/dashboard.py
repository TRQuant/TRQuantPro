"""
综合仪表盘组件
==============

提供市场状态的仪表盘可视化：
1. MarketGauge - 核心指标仪表盘
2. StatusTimeline - 状态转换时间轴
3. Dashboard - 综合仪表盘
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging
import json

logger = logging.getLogger(__name__)

# 尝试导入可视化库
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.collections import PatchCollection
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# 导入状态定义
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from core.market_state_definitions import (
        UnifiedMarketState,
        MarketRegime,
        TrendDirection,
        MarketPhase,
        IBDStatus,
        REGIME_DESCRIPTIONS,
        TREND_COLORS,
        PHASE_DESCRIPTIONS,
        IBD_STATUS_DESCRIPTIONS,
    )
except ImportError:
    logger.warning("Cannot import market_state_definitions, using defaults")
    UnifiedMarketState = None


class MarketGauge:
    """
    核心指标仪表盘
    
    显示关键指标的仪表盘样式图表。
    """
    
    def __init__(self):
        self.gauge_colors = {
            "red": "#F44336",
            "orange": "#FF9800",
            "yellow": "#FFEB3B",
            "lightgreen": "#8BC34A",
            "green": "#4CAF50",
        }
    
    def create_trend_gauge(
        self,
        score: float,
        title: str = "趋势得分",
        min_val: float = -100,
        max_val: float = 100,
    ) -> Any:
        """
        创建趋势得分仪表盘
        
        Args:
            score: 当前得分
            title: 标题
            min_val: 最小值
            max_val: 最大值
        
        Returns:
            Figure对象
        """
        if not PLOTLY_AVAILABLE:
            logger.warning("Plotly not available for gauge")
            return None
        
        # 定义颜色区间
        steps = [
            {"range": [-100, -60], "color": "#F44336"},
            {"range": [-60, -30], "color": "#FF5722"},
            {"range": [-30, -10], "color": "#FF9800"},
            {"range": [-10, 10], "color": "#FFC107"},
            {"range": [10, 30], "color": "#CDDC39"},
            {"range": [30, 60], "color": "#8BC34A"},
            {"range": [60, 100], "color": "#4CAF50"},
        ]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"size": 24}},
            delta={"reference": 0, "increasing": {"color": "#00C853"}, "decreasing": {"color": "#F44336"}},
            gauge={
                "axis": {"range": [min_val, max_val], "tickwidth": 1},
                "bar": {"color": "#2196F3"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": steps,
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        return fig
    
    def create_risk_gauge(
        self,
        risk_score: float,
        title: str = "风险水平",
    ) -> Any:
        """
        创建风险水平仪表盘
        
        Args:
            risk_score: 风险得分 (0-100)
            title: 标题
        
        Returns:
            Figure对象
        """
        if not PLOTLY_AVAILABLE:
            return None
        
        # 风险区间（反向：低分好）
        steps = [
            {"range": [0, 30], "color": "#4CAF50"},      # 低风险-绿色
            {"range": [30, 50], "color": "#CDDC39"},     # 中低风险
            {"range": [50, 70], "color": "#FFC107"},     # 中风险-黄色
            {"range": [70, 85], "color": "#FF9800"},     # 中高风险
            {"range": [85, 100], "color": "#F44336"},    # 高风险-红色
        ]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"size": 24}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": "#9E9E9E"},
                "steps": steps,
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 70,  # 高风险阈值
                },
            },
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        return fig
    
    def create_position_gauge(
        self,
        position: float,
        title: str = "建议仓位",
    ) -> Any:
        """
        创建仓位建议仪表盘
        
        Args:
            position: 建议仓位 (0-1)
            title: 标题
        
        Returns:
            Figure对象
        """
        if not PLOTLY_AVAILABLE:
            return None
        
        steps = [
            {"range": [0, 20], "color": "#FFCDD2"},      # 空仓
            {"range": [20, 40], "color": "#FFE0B2"},     # 低仓位
            {"range": [40, 60], "color": "#FFF9C4"},     # 中仓位
            {"range": [60, 80], "color": "#C8E6C9"},     # 高仓位
            {"range": [80, 100], "color": "#A5D6A7"},    # 满仓
        ]
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=position * 100,
            number={"suffix": "%"},
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title, "font": {"size": 24}},
            gauge={
                "axis": {"range": [0, 100], "ticksuffix": "%"},
                "bar": {"color": "#2196F3"},
                "steps": steps,
            },
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        return fig


class StatusTimeline:
    """
    状态转换时间轴
    
    显示市场状态随时间的变化。
    """
    
    def __init__(self):
        pass
    
    def create_timeline(
        self,
        history: List[Dict],
        key: str = "phase",
        title: str = "市场状态时间轴",
        height: int = 200,
    ) -> Any:
        """
        创建状态时间轴
        
        Args:
            history: 历史状态列表，每个元素包含 date, phase/regime 等
            key: 要显示的状态键
            title: 标题
            height: 图表高度
        
        Returns:
            Figure对象
        """
        if not history:
            return None
        
        if not PLOTLY_AVAILABLE:
            return self._matplotlib_timeline(history, key, title)
        
        dates = [h.get("date", "") for h in history]
        states = [h.get(key, "unknown") for h in history]
        
        # 获取颜色映射
        color_map = self._get_color_map(key)
        colors = [color_map.get(s, "#9E9E9E") for s in states]
        
        # 创建时间轴
        fig = go.Figure()
        
        # 使用散点图模拟时间轴
        fig.add_trace(go.Scatter(
            x=dates,
            y=[1] * len(dates),
            mode="markers+text",
            marker=dict(
                size=20,
                color=colors,
                line=dict(width=2, color="white"),
            ),
            text=states,
            textposition="bottom center",
            hovertemplate="%{x}<br>%{text}<extra></extra>",
        ))
        
        # 连接线
        fig.add_trace(go.Scatter(
            x=dates,
            y=[1] * len(dates),
            mode="lines",
            line=dict(color="#E0E0E0", width=2),
            showlegend=False,
        ))
        
        fig.update_layout(
            title=title,
            height=height,
            yaxis=dict(visible=False, range=[0, 2]),
            xaxis=dict(title="日期"),
            showlegend=False,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        
        return fig
    
    def _matplotlib_timeline(
        self,
        history: List[Dict],
        key: str,
        title: str,
    ) -> Any:
        """Matplotlib实现的时间轴"""
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        dates = [h.get("date", "") for h in history]
        states = [h.get(key, "unknown") for h in history]
        
        color_map = self._get_color_map(key)
        colors = [color_map.get(s, "#9E9E9E") for s in states]
        
        fig, ax = plt.subplots(figsize=(14, 3))
        
        for i, (date, state, color) in enumerate(zip(dates, states, colors)):
            ax.scatter([i], [0], c=[color], s=200, zorder=2)
            if i % max(1, len(dates) // 10) == 0:  # 每隔几个点显示标签
                ax.annotate(state, (i, 0), textcoords="offset points",
                           xytext=(0, -20), ha="center", fontsize=8, rotation=45)
        
        ax.plot(range(len(dates)), [0] * len(dates), "gray", alpha=0.3, zorder=1)
        ax.set_ylim(-1, 1)
        ax.set_xlim(-0.5, len(dates) - 0.5)
        ax.set_title(title)
        ax.axis("off")
        
        # X轴日期标签
        step = max(1, len(dates) // 10)
        ax.set_xticks(range(0, len(dates), step))
        ax.set_xticklabels([dates[i] for i in range(0, len(dates), step)], rotation=45)
        
        plt.tight_layout()
        return fig
    
    def _get_color_map(self, key: str) -> Dict[str, str]:
        """获取状态颜色映射"""
        if key == "phase":
            return {p.value: info["color"] for p, info in PHASE_DESCRIPTIONS.items()} if PHASE_DESCRIPTIONS else {}
        elif key == "regime":
            return {r.value: info["color"] for r, info in REGIME_DESCRIPTIONS.items()} if REGIME_DESCRIPTIONS else {}
        elif key == "ibd_status":
            return {s.value: info["color"] for s, info in IBD_STATUS_DESCRIPTIONS.items()} if IBD_STATUS_DESCRIPTIONS else {}
        else:
            return {}


class Dashboard:
    """
    综合仪表盘
    
    整合多个可视化组件，提供一站式市场状态展示。
    """
    
    def __init__(self):
        self.gauge = MarketGauge()
        self.timeline = StatusTimeline()
    
    def render_full_dashboard(
        self,
        state: "UnifiedMarketState",
        history: List[Dict] = None,
        title: str = "市场状态仪表盘",
    ) -> Any:
        """
        渲染完整仪表盘
        
        Args:
            state: 当前市场状态
            history: 历史状态列表
            title: 标题
        
        Returns:
            Figure对象 或 HTML字符串
        """
        if not PLOTLY_AVAILABLE:
            return self._text_dashboard(state, history)
        
        # 创建子图布局
        fig = make_subplots(
            rows=3, cols=3,
            specs=[
                [{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}],
                [{"type": "table", "colspan": 3}, None, None],
                [{"type": "scatter", "colspan": 3}, None, None],
            ],
            row_heights=[0.35, 0.3, 0.35],
            subplot_titles=[
                "趋势得分", "风险水平", "建议仓位",
                "状态摘要",
                "状态时间轴"
            ],
            vertical_spacing=0.1,
        )
        
        # 1. 趋势仪表
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=state.composite_score if state else 0,
                gauge={
                    "axis": {"range": [-100, 100]},
                    "bar": {"color": "#2196F3"},
                    "steps": [
                        {"range": [-100, -30], "color": "#FFCDD2"},
                        {"range": [-30, 30], "color": "#FFF9C4"},
                        {"range": [30, 100], "color": "#C8E6C9"},
                    ],
                },
            ),
            row=1, col=1
        )
        
        # 2. 风险仪表
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=state.risk_score if state else 50,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#9E9E9E"},
                    "steps": [
                        {"range": [0, 30], "color": "#C8E6C9"},
                        {"range": [30, 70], "color": "#FFF9C4"},
                        {"range": [70, 100], "color": "#FFCDD2"},
                    ],
                },
            ),
            row=1, col=2
        )
        
        # 3. 仓位仪表
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=(state.suggested_position * 100) if state else 50,
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2196F3"},
                },
            ),
            row=1, col=3
        )
        
        # 4. 状态摘要表格
        if state:
            table_data = self._create_state_table(state)
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=["指标", "状态", "说明"],
                        fill_color="#E3F2FD",
                        font=dict(size=12, color="black"),
                        align="left",
                    ),
                    cells=dict(
                        values=table_data,
                        fill_color="white",
                        font=dict(size=11),
                        align="left",
                    ),
                ),
                row=2, col=1
            )
        
        # 5. 时间轴
        if history:
            dates = [h.get("date", "") for h in history[-30:]]  # 最近30条
            scores = [h.get("composite_score", 0) for h in history[-30:]]
            
            fig.add_trace(
                go.Scatter(
                    x=dates,
                    y=scores,
                    mode="lines+markers",
                    name="趋势得分",
                    line=dict(color="#2196F3", width=2),
                    fill="tozeroy",
                ),
                row=3, col=1
            )
            
            fig.add_hline(y=0, line_dash="dash", line_color="gray", row=3, col=1)
        
        # 更新布局
        fig.update_layout(
            title=dict(text=title, font=dict(size=20)),
            height=900,
            showlegend=False,
            template="plotly_white",
        )
        
        return fig
    
    def _create_state_table(self, state: "UnifiedMarketState") -> List[List]:
        """创建状态摘要表格数据"""
        indicators = []
        states = []
        descriptions = []
        
        # 市场环境
        indicators.append("市场环境")
        states.append(state.regime.value if hasattr(state, 'regime') else "N/A")
        descriptions.append(REGIME_DESCRIPTIONS.get(state.regime, {}).get("description", "") if hasattr(state, 'regime') else "")
        
        # 趋势方向
        indicators.append("趋势方向")
        states.append(state.direction.value if hasattr(state, 'direction') else "N/A")
        descriptions.append(f"得分: {state.composite_score:.1f}" if hasattr(state, 'composite_score') else "")
        
        # 市场阶段
        indicators.append("市场阶段")
        states.append(state.phase.value if hasattr(state, 'phase') else "N/A")
        descriptions.append(PHASE_DESCRIPTIONS.get(state.phase, {}).get("action", "") if hasattr(state, 'phase') else "")
        
        # IBD状态
        indicators.append("IBD状态")
        states.append(state.ibd_status.value if hasattr(state, 'ibd_status') else "N/A")
        descriptions.append(IBD_STATUS_DESCRIPTIONS.get(state.ibd_status, {}).get("action", "") if hasattr(state, 'ibd_status') else "")
        
        # 多周期得分
        indicators.append("短期得分")
        states.append(f"{state.short_term_score:.1f}" if hasattr(state, 'short_term_score') else "N/A")
        descriptions.append("1-8周")
        
        indicators.append("中期得分")
        states.append(f"{state.medium_term_score:.1f}" if hasattr(state, 'medium_term_score') else "N/A")
        descriptions.append("9-24周")
        
        indicators.append("长期得分")
        states.append(f"{state.long_term_score:.1f}" if hasattr(state, 'long_term_score') else "N/A")
        descriptions.append("25-48周")
        
        return [indicators, states, descriptions]
    
    def _text_dashboard(
        self,
        state: "UnifiedMarketState",
        history: List[Dict],
    ) -> str:
        """文本格式的仪表盘"""
        lines = []
        lines.append("=" * 60)
        lines.append("市场状态仪表盘")
        lines.append("=" * 60)
        
        if state:
            lines.append(f"\n【核心指标】")
            lines.append(f"  趋势得分: {state.composite_score:.1f}")
            lines.append(f"  风险水平: {state.risk_score:.1f}")
            lines.append(f"  建议仓位: {state.suggested_position*100:.0f}%")
            
            lines.append(f"\n【四层状态】")
            lines.append(f"  市场环境: {state.regime.value}")
            lines.append(f"  趋势方向: {state.direction.value}")
            lines.append(f"  市场阶段: {state.phase.value}")
            lines.append(f"  IBD状态: {state.ibd_status.value}")
            
            lines.append(f"\n【多周期得分】")
            lines.append(f"  短期: {state.short_term_score:.1f}")
            lines.append(f"  中期: {state.medium_term_score:.1f}")
            lines.append(f"  长期: {state.long_term_score:.1f}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
    
    def render_comparison(
        self,
        states: List["UnifiedMarketState"],
        labels: List[str] = None,
        title: str = "多日状态对比",
    ) -> Any:
        """
        渲染多日状态对比
        
        Args:
            states: 状态列表
            labels: 标签列表（如日期）
            title: 标题
        
        Returns:
            Figure对象
        """
        if not states:
            return None
        
        if labels is None:
            labels = [f"Day {i+1}" for i in range(len(states))]
        
        if not PLOTLY_AVAILABLE:
            return None
        
        # 提取数据
        scores = [s.composite_score for s in states]
        risks = [s.risk_score for s in states]
        positions = [s.suggested_position * 100 for s in states]
        
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=["趋势得分", "风险水平", "建议仓位"],
        )
        
        # 趋势得分
        colors = ["#4CAF50" if s > 0 else "#F44336" for s in scores]
        fig.add_trace(
            go.Bar(x=labels, y=scores, marker_color=colors, name="趋势"),
            row=1, col=1
        )
        
        # 风险水平
        fig.add_trace(
            go.Bar(x=labels, y=risks, marker_color="#FF9800", name="风险"),
            row=1, col=2
        )
        
        # 建议仓位
        fig.add_trace(
            go.Bar(x=labels, y=positions, marker_color="#2196F3", name="仓位"),
            row=1, col=3
        )
        
        fig.update_layout(
            title=title,
            height=400,
            showlegend=False,
        )
        
        return fig
    
    def export_to_html(
        self,
        fig: Any,
        filepath: str,
        include_plotlyjs: bool = True,
    ) -> bool:
        """
        导出为HTML文件
        
        Args:
            fig: Plotly Figure对象
            filepath: 输出文件路径
            include_plotlyjs: 是否包含plotly.js
        
        Returns:
            是否成功
        """
        if not PLOTLY_AVAILABLE or fig is None:
            return False
        
        try:
            fig.write_html(
                filepath,
                include_plotlyjs="cdn" if not include_plotlyjs else True,
            )
            logger.info(f"Dashboard exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export dashboard: {e}")
            return False

