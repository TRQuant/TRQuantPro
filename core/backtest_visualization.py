#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BacktestVisualization - 回测结果可视化
=========================================

功能:
1. 使用Plotly生成交互式图表
2. 生成HTML完整报告
3. 生成Markdown摘要 (Notebook嵌入)

图表内容:
- 市场状态时序图
- 准确率热力图
- 收益曲线对比
- 年度统计柱状图
- 信号分布饼图

作者: TRQuant Team
日期: 2026-01-02
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# 尝试导入可视化库
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False
    logger.warning("Plotly未安装，部分可视化功能不可用")


# 颜色配置 (Dark Mode) - 确保文字与背景有高对比度
COLORS = {
    'background': '#1E1E1E',      # 深色背景
    'paper': '#252525',           # 图表外背景（略浅）
    'text': '#FFFFFF',            # 白色文字（高对比度）
    'text_secondary': '#CCCCCC',  # 次要文字（略浅但仍清晰）
    'grid': '#444444',            # 网格线（增强可见性）
    'axis_line': '#666666',       # 坐标轴线
    'bullish': '#00C853',         # 看多（绿色）
    'bearish': '#FF5252',         # 看空（红色）
    'neutral': '#FFC107',         # 中性（黄色）
    'bull_state': '#4CAF50',      # 牛市状态
    'bear_state': '#F44336',      # 熊市状态
    'volatile_state': '#FF9800',  # 震荡状态
    'short': '#2196F3',           # 短期（蓝色）
    'medium': '#9C27B0',          # 中期（紫色）
    'long': '#FF5722',            # 长期（橙红色）
}


class BacktestVisualization:
    """回测结果可视化"""
    
    @staticmethod
    def _get_dark_layout(title: str = '', height: int = 400, **kwargs) -> Dict[str, Any]:
        """
        获取统一的Dark Mode布局配置
        确保所有文字颜色与背景有明显对比度
        
        Args:
            title: 图表标题
            height: 图表高度
            **kwargs: 其他布局参数（会覆盖默认值）
            
        Returns:
            布局字典
        """
        layout = {
            'title': {
                'text': title,
                'font': {
                    'color': COLORS['text'],      # 白色标题
                    'size': 16,
                    'family': 'Arial, Microsoft YaHei, sans-serif'
                },
                'x': 0.5,
                'xanchor': 'center'
            },
            'paper_bgcolor': COLORS['paper'],      # 图表外背景
            'plot_bgcolor': COLORS['background'],  # 图表内背景
            'font': {
                'color': COLORS['text'],           # 所有文字为白色
                'size': 12,
                'family': 'Arial, Microsoft YaHei, sans-serif'
            },
            'xaxis': {
                'gridcolor': COLORS['grid'],       # 网格线
                'linecolor': COLORS.get('axis_line', COLORS['grid']),  # 坐标轴线
                'zerolinecolor': COLORS['grid'],
                'title': {
                    'font': {'color': COLORS['text']}
                },
                'tickfont': {'color': COLORS['text']}
            },
            'yaxis': {
                'gridcolor': COLORS['grid'],
                'linecolor': COLORS.get('axis_line', COLORS['grid']),
                'zerolinecolor': COLORS['grid'],
                'title': {
                    'font': {'color': COLORS['text']}
                },
                'tickfont': {'color': COLORS['text']}
            },
            'legend': {
                'font': {'color': COLORS['text']},
                'bgcolor': 'rgba(37, 37, 37, 0.8)',  # 半透明背景
                'bordercolor': COLORS['grid'],
                'borderwidth': 1
            },
            'height': height
        }
        
        # 合并用户自定义参数
        layout.update(kwargs)
        return layout
    
    @staticmethod
    def _to_bool(value: Any) -> bool:
        """将值转换为布尔值，支持字符串'true'/'false'"""
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() == 'true'
        return bool(value)
    
    def __init__(self, result: Any, version_info: Optional[Dict[str, Any]] = None):
        """
        初始化可视化器
        
        Args:
            result: EnhancedBacktestResult 实例
            version_info: 版本信息字典（可选，包含algorithm_version, version_tag等）
        """
        self.result = result
        self.version_info = version_info or {}
        self.signals_df = self._signals_to_dataframe()
    
    @classmethod
    def from_database(
        cls,
        result_id: str,
        version: Optional[str] = None
    ) -> 'BacktestVisualization':
        """
        从数据库加载结果并创建可视化对象
        
        Args:
            result_id: 结果ID（MongoDB _id的字符串形式）
            version: 版本标签（可选，用于过滤）
            
        Returns:
            BacktestVisualization实例
            
        Raises:
            ValueError: 如果结果不存在或加载失败
        """
        from core.market_trend_storage import MarketTrendStorage
        
        storage = MarketTrendStorage()
        if not storage.is_connected():
            raise ValueError("MongoDB未连接，无法从数据库加载")
        
        result = storage.load_backtest_result(result_id)
        if not result:
            raise ValueError(f"未找到回测结果: {result_id}")
        
        # 获取版本信息
        from bson import ObjectId
        doc = storage.db[storage.BACKTEST_COLLECTION].find_one({'_id': ObjectId(result_id)})
        version_info = {}
        if doc:
            version_info = {
                'algorithm_version': doc.get('algorithm_version'),
                'version_tag': doc.get('version_tag'),
                'migrated_from': doc.get('migrated_from'),
                'created_at': doc.get('created_at')
            }
        
        return cls(result, version_info=version_info)
    
    @classmethod
    def from_cache(
        cls,
        config: Dict[str, Any],
        backtest_type: str,
        version: Optional[str] = None
    ) -> Optional['BacktestVisualization']:
        """
        从缓存查找结果并创建可视化对象
        
        Args:
            config: 配置字典
            backtest_type: 回测类型
            version: 算法版本（可选）
            
        Returns:
            BacktestVisualization实例，未找到返回None
        """
        from core.market_trend_storage import MarketTrendStorage
        
        storage = MarketTrendStorage()
        if not storage.is_connected():
            logger.warning("MongoDB未连接，无法从缓存加载")
            return None
        
        cached = storage.find_cached_backtest(config, backtest_type, algorithm_version=version)
        if not cached:
            return None
        
        result = storage.load_backtest_result(cached['_id'])
        if not result:
            return None
        
        # 获取版本信息
        version_info = {
            'algorithm_version': cached.get('algorithm_version'),
            'version_tag': cached.get('version_tag'),
            'migrated_from': cached.get('migrated_from'),
            'created_at': cached.get('created_at')
        }
        
        return cls(result, version_info=version_info)
    
    def get_version_info(self) -> Dict[str, Any]:
        """
        返回结果的版本信息
        
        Returns:
            版本信息字典
        """
        return self.version_info.copy() if self.version_info else {}
    
    def _signals_to_dataframe(self) -> pd.DataFrame:
        """将信号列表转换为DataFrame
        
        支持两种格式：
        1. EnhancedSignalRecord对象列表（直接从回测得到）
        2. 字典列表（从数据库加载）
        """
        if not self.result.signals:
            return pd.DataFrame()
        
        data = []
        for s in self.result.signals:
            # 判断是对象还是字典
            if isinstance(s, dict):
                # 从数据库加载的字典格式
                signal_type_val = s.get('signal_type', 'neutral')
                state_category_val = s.get('state_category', '震荡')
                data.append({
                    'date': pd.to_datetime(s.get('date', '')),
                    'signal_type': signal_type_val if isinstance(signal_type_val, str) else signal_type_val.value if hasattr(signal_type_val, 'value') else str(signal_type_val),
                    'composite_score': s.get('composite_score', 0.0),
                    'short_score': s.get('short_term_score', 0.0),
                    'medium_score': s.get('medium_term_score', 0.0),
                    'long_score': s.get('long_term_score', 0.0),
                    'market_state': s.get('market_state', ''),
                    'state_category': state_category_val if isinstance(state_category_val, str) else state_category_val.value if hasattr(state_category_val, 'value') else str(state_category_val),
                    'returns_5d': float(s.get('returns_5d', 0.0)) if s.get('returns_5d') not in [None, ''] else 0.0,
                    'returns_20d': float(s.get('returns_20d', 0.0)) if s.get('returns_20d') not in [None, ''] else 0.0,
                    'returns_60d': float(s.get('returns_60d', 0.0)) if s.get('returns_60d') not in [None, ''] else 0.0,
                    'correct_5d': self._to_bool(s.get('correct_5d', False)),
                    'correct_20d': self._to_bool(s.get('correct_20d', False)),
                    'correct_60d': self._to_bool(s.get('correct_60d', False)),
                    'short_correct': self._to_bool(s.get('short_correct_5d', False)),
                    'medium_correct': self._to_bool(s.get('medium_correct_20d', False)),
                    'long_correct': self._to_bool(s.get('long_correct_60d', False)),
                    'state_correct': self._to_bool(s.get('state_correct_60d', False)),
                })
            else:
                # EnhancedSignalRecord对象格式
                data.append({
                    'date': pd.to_datetime(s.date),
                    'signal_type': s.signal_type.value if hasattr(s.signal_type, 'value') else str(s.signal_type),
                    'composite_score': s.composite_score,
                    'short_score': s.short_term_score,
                    'medium_score': s.medium_term_score,
                    'long_score': s.long_term_score,
                    'market_state': s.market_state,
                    'state_category': s.state_category.value if hasattr(s.state_category, 'value') else str(s.state_category),
                    'returns_5d': s.returns_5d,
                    'returns_20d': s.returns_20d,
                    'returns_60d': s.returns_60d,
                    'correct_5d': s.correct_5d,
                    'correct_20d': s.correct_20d,
                    'correct_60d': s.correct_60d,
                    'short_correct': s.short_correct_5d,
                    'medium_correct': s.medium_correct_20d,
                    'long_correct': s.long_correct_60d,
                    'state_correct': s.state_correct_60d,
                })
        
        df = pd.DataFrame(data)
        df['year'] = df['date'].dt.year
        return df
    
    def create_accuracy_heatmap(self) -> Optional[go.Figure]:
        """创建准确率热力图"""
        if not HAS_PLOTLY:
            return None
        
        # 数据准备
        categories = ['综合', '短期', '中期', '长期', '市场状态']
        periods = ['5日', '20日', '60日']
        
        z = [
            [self.result.accuracy_5d, self.result.accuracy_20d, self.result.accuracy_60d],
            [self.result.short_accuracy_5d, 0, 0],  # 短期只验证5日
            [0, self.result.medium_accuracy_20d, 0],  # 中期只验证20日
            [0, 0, self.result.long_accuracy_60d],  # 长期只验证60日
            [0, 0, self.result.state_accuracy_60d],  # 状态验证60日
        ]
        
        # 创建热力图
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=periods,
            y=categories,
            colorscale='RdYlGn',
            zmin=0,
            zmax=100,
            text=[[f'{v:.1f}%' if v > 0 else '' for v in row] for row in z],
            texttemplate="%{text}",
            textfont={"size": 14, "color": COLORS['text']},  # 使用配置的白色文字
            hovertemplate='%{y} %{x}: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            self._get_dark_layout(
                title='准确率热力图 (各周期验证)',
                height=400
            )
        )
        
        return fig
    
    def create_signal_distribution_pie(self) -> Optional[go.Figure]:
        """创建信号分布饼图"""
        if not HAS_PLOTLY or self.signals_df.empty:
            return None
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "pie"}, {"type": "pie"}]],
            subplot_titles=('综合信号分布', '市场状态分布')
        )
        
        # 综合信号分布
        signal_counts = self.signals_df['signal_type'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=signal_counts.index,
                values=signal_counts.values,
                marker=dict(colors=[
                    COLORS['bullish'] if x == 'bullish' else 
                    COLORS['bearish'] if x == 'bearish' else 
                    COLORS['neutral'] for x in signal_counts.index
                ]),
                hole=0.4
            ),
            row=1, col=1
        )
        
        # 市场状态分布
        state_counts = self.signals_df['state_category'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=state_counts.index,
                values=state_counts.values,
                marker=dict(colors=[
                    COLORS['bull_state'] if x == '牛市' else 
                    COLORS['bear_state'] if x == '熊市' else 
                    COLORS['volatile_state'] for x in state_counts.index
                ]),
                hole=0.4
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            self._get_dark_layout(
                title='信号分布',
                height=400
            )
        )
        
        # 更新subplot标题颜色
        fig.update_annotations(font_color=COLORS['text'])
        
        return fig
    
    def create_yearly_accuracy_bar(self) -> Optional[go.Figure]:
        """创建年度准确率柱状图"""
        if not HAS_PLOTLY or not self.result.yearly_stats:
            return None
        
        years = sorted(self.result.yearly_stats.keys())
        
        acc_5d = []
        acc_20d = []
        acc_60d = []
        short_acc = []
        medium_acc = []
        long_acc = []
        
        for year in years:
            stats = self.result.yearly_stats[year]
            total = stats['total']
            if total > 0:
                acc_5d.append(stats['correct_5d'] / total * 100)
                acc_20d.append(stats['correct_20d'] / total * 100)
                acc_60d.append(stats['correct_60d'] / total * 100)
                short_acc.append(stats['short_correct'] / total * 100)
                medium_acc.append(stats['medium_correct'] / total * 100)
                long_acc.append(stats['long_correct'] / total * 100)
            else:
                acc_5d.append(0)
                acc_20d.append(0)
                acc_60d.append(0)
                short_acc.append(0)
                medium_acc.append(0)
                long_acc.append(0)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(name='短期(5日)', x=years, y=short_acc, marker_color=COLORS['short']))
        fig.add_trace(go.Bar(name='中期(20日)', x=years, y=medium_acc, marker_color=COLORS['medium']))
        fig.add_trace(go.Bar(name='长期(60日)', x=years, y=long_acc, marker_color=COLORS['long']))
        
        layout = self._get_dark_layout(
            title='年度分周期准确率',
            height=400,
            xaxis_title='年份',
            yaxis_title='准确率 (%)',
            barmode='group',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font={'color': COLORS['text']}
            )
        )
        # 更新y轴范围
        layout['yaxis']['range'] = [0, 100]
        fig.update_layout(layout)
        
        return fig
    
    def create_score_timeseries(self) -> Optional[go.Figure]:
        """创建得分时序图"""
        if not HAS_PLOTLY or self.signals_df.empty:
            return None
        
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('综合得分', '分周期得分', '未来收益')
        )
        
        # 综合得分
        fig.add_trace(
            go.Scatter(
                x=self.signals_df['date'],
                y=self.signals_df['composite_score'],
                mode='lines',
                name='综合得分',
                line=dict(color=COLORS['text'], width=1),
                fill='tozeroy',
                fillcolor='rgba(255,255,255,0.1)'
            ),
            row=1, col=1
        )
        
        # 添加阈值线
        fig.add_hline(y=30, line_dash="dash", line_color=COLORS['bullish'], row=1, col=1)
        fig.add_hline(y=-30, line_dash="dash", line_color=COLORS['bearish'], row=1, col=1)
        
        # 分周期得分
        fig.add_trace(
            go.Scatter(x=self.signals_df['date'], y=self.signals_df['short_score'],
                      mode='lines', name='短期', line=dict(color=COLORS['short'], width=1)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=self.signals_df['date'], y=self.signals_df['medium_score'],
                      mode='lines', name='中期', line=dict(color=COLORS['medium'], width=1)),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=self.signals_df['date'], y=self.signals_df['long_score'],
                      mode='lines', name='长期', line=dict(color=COLORS['long'], width=1)),
            row=2, col=1
        )
        
        # 未来收益
        fig.add_trace(
            go.Scatter(x=self.signals_df['date'], y=self.signals_df['returns_5d'],
                      mode='lines', name='5日收益', line=dict(color=COLORS['short'], width=1)),
            row=3, col=1
        )
        fig.add_trace(
            go.Scatter(x=self.signals_df['date'], y=self.signals_df['returns_60d'],
                      mode='lines', name='60日收益', line=dict(color=COLORS['long'], width=1)),
            row=3, col=1
        )
        
        fig.add_hline(y=0, line_dash="solid", line_color=COLORS['grid'], row=3, col=1)
        
        layout = self._get_dark_layout(
            title='信号得分与收益时序',
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font={'color': COLORS['text']}
            )
        )
        fig.update_layout(layout)
        
        # 更新所有subplot的坐标轴
        fig.update_xaxes(
            gridcolor=COLORS['grid'],
            linecolor=COLORS.get('axis_line', COLORS['grid']),
            tickfont={'color': COLORS['text']}
        )
        fig.update_yaxes(
            gridcolor=COLORS['grid'],
            linecolor=COLORS.get('axis_line', COLORS['grid']),
            tickfont={'color': COLORS['text']}
        )
        
        # 更新subplot标题颜色
        fig.update_annotations(font_color=COLORS['text'])
        
        return fig
    
    def create_market_state_timeline(self) -> Optional[go.Figure]:
        """创建市场状态时间线"""
        if not HAS_PLOTLY or self.signals_df.empty:
            return None
        
        # 状态颜色映射
        state_colors = {
            '牛市': COLORS['bull_state'],
            '熊市': COLORS['bear_state'],
            '震荡': COLORS['volatile_state'],
        }
        
        df = self.signals_df.copy()
        df['color'] = df['state_category'].map(state_colors)
        
        fig = go.Figure()
        
        # 为每个状态类别添加散点
        for category in ['牛市', '熊市', '震荡']:
            mask = df['state_category'] == category
            subset = df[mask]
            
            fig.add_trace(go.Scatter(
                x=subset['date'],
                y=[category] * len(subset),
                mode='markers',
                name=category,
                marker=dict(
                    size=10,
                    color=state_colors[category],
                    opacity=0.7
                ),
                hovertemplate='%{x}<br>状态: %{text}<extra></extra>',
                text=subset['market_state']
            ))
        
        fig.update_layout(
            self._get_dark_layout(
                title='市场状态时间线',
                xaxis_title='日期',
                yaxis_title='状态类别',
                height=300
            )
        )
        
        return fig
    
    def generate_html_report(self, output_path: str = None) -> str:
        """
        生成完整HTML报告
        
        Args:
            output_path: 输出文件路径 (可选，不提供则返回HTML字符串)
            
        Returns:
            HTML字符串
        """
        if not HAS_PLOTLY:
            return "<p>Plotly未安装，无法生成可视化报告</p>"
        
        # 生成各个图表
        accuracy_heatmap = self.create_accuracy_heatmap()
        signal_pie = self.create_signal_distribution_pie()
        yearly_bar = self.create_yearly_accuracy_bar()
        score_ts = self.create_score_timeseries()
        state_timeline = self.create_market_state_timeline()
        
        # 构建HTML
        html_parts = [
            """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>市场趋势回测报告</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            background-color: #1E1E1E;
            color: #FFFFFF;
            font-family: 'Microsoft YaHei', sans-serif;
            margin: 20px;
        }
        h1, h2, h3 { color: #4CAF50; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #333;
            padding: 10px;
            text-align: left;
        }
        th { background-color: #333; }
        .container { max-width: 1400px; margin: 0 auto; }
        .chart-container { margin: 30px 0; }
        .summary-box {
            background: #252525;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
        .good { color: #4CAF50; }
        .bad { color: #F44336; }
        .neutral { color: #FFC107; }
    </style>
</head>
<body>
<div class="container">
"""
        ]
        
        # 标题和摘要
        html_parts.append(f"""
<h1>📊 市场趋势信号回测报告</h1>

<div class="summary-box">
    <h2>回测概况</h2>
    <table>
        <tr><th>项目</th><th>值</th></tr>
        <tr><td>回测时间</td><td>{self.result.backtest_time}</td></tr>
        <tr><td>回测区间</td><td>{self.result.config.start_date} ~ {self.result.config.end_date}</td></tr>
        <tr><td>基准指数</td><td>{self.result.config.benchmark}</td></tr>
        <tr><td>总信号数</td><td>{self.result.total_signals}</td></tr>
        <tr><td>看多信号</td><td class="good">{self.result.bullish_signals}</td></tr>
        <tr><td>看空信号</td><td class="bad">{self.result.bearish_signals}</td></tr>
        <tr><td>中性信号</td><td class="neutral">{self.result.neutral_signals}</td></tr>
    </table>
</div>

<div class="summary-box">
    <h2>准确率概览</h2>
    <table>
        <tr><th>周期</th><th>准确率</th><th>评价</th></tr>
        <tr>
            <td>短期 (5日)</td>
            <td>{self.result.short_accuracy_5d:.1f}%</td>
            <td class="{'good' if self.result.short_accuracy_5d > 60 else 'bad'}">
                {'✅ 良好' if self.result.short_accuracy_5d > 60 else '⚠️ 需优化'}
            </td>
        </tr>
        <tr>
            <td>中期 (20日)</td>
            <td>{self.result.medium_accuracy_20d:.1f}%</td>
            <td class="{'good' if self.result.medium_accuracy_20d > 60 else 'bad'}">
                {'✅ 良好' if self.result.medium_accuracy_20d > 60 else '⚠️ 需优化'}
            </td>
        </tr>
        <tr>
            <td>长期 (60日)</td>
            <td>{self.result.long_accuracy_60d:.1f}%</td>
            <td class="{'good' if self.result.long_accuracy_60d > 60 else 'bad'}">
                {'✅ 良好' if self.result.long_accuracy_60d > 60 else '⚠️ 需优化'}
            </td>
        </tr>
        <tr>
            <td>市场状态</td>
            <td>{self.result.state_accuracy_60d:.1f}%</td>
            <td class="{'good' if self.result.state_accuracy_60d > 60 else 'bad'}">
                {'✅ 良好' if self.result.state_accuracy_60d > 60 else '⚠️ 需优化'}
            </td>
        </tr>
    </table>
</div>
""")
        
        # 添加图表
        if accuracy_heatmap:
            html_parts.append('<div class="chart-container">')
            html_parts.append(accuracy_heatmap.to_html(full_html=False, include_plotlyjs=False))
            html_parts.append('</div>')
        
        if signal_pie:
            html_parts.append('<div class="chart-container">')
            html_parts.append(signal_pie.to_html(full_html=False, include_plotlyjs=False))
            html_parts.append('</div>')
        
        if yearly_bar:
            html_parts.append('<div class="chart-container">')
            html_parts.append(yearly_bar.to_html(full_html=False, include_plotlyjs=False))
            html_parts.append('</div>')
        
        if state_timeline:
            html_parts.append('<div class="chart-container">')
            html_parts.append(state_timeline.to_html(full_html=False, include_plotlyjs=False))
            html_parts.append('</div>')
        
        if score_ts:
            html_parts.append('<div class="chart-container">')
            html_parts.append(score_ts.to_html(full_html=False, include_plotlyjs=False))
            html_parts.append('</div>')
        
        # 年度统计表
        if self.result.yearly_stats:
            html_parts.append("""
<div class="summary-box">
    <h2>年度统计</h2>
    <table>
        <tr>
            <th>年份</th>
            <th>信号数</th>
            <th>5日准确</th>
            <th>20日准确</th>
            <th>60日准确</th>
            <th>短期准确</th>
            <th>中期准确</th>
            <th>长期准确</th>
        </tr>
""")
            for year in sorted(self.result.yearly_stats.keys()):
                stats = self.result.yearly_stats[year]
                total = stats['total']
                if total > 0:
                    html_parts.append(f"""
        <tr>
            <td>{year}</td>
            <td>{total}</td>
            <td>{stats['correct_5d'] / total * 100:.0f}%</td>
            <td>{stats['correct_20d'] / total * 100:.0f}%</td>
            <td>{stats['correct_60d'] / total * 100:.0f}%</td>
            <td>{stats['short_correct'] / total * 100:.0f}%</td>
            <td>{stats['medium_correct'] / total * 100:.0f}%</td>
            <td>{stats['long_correct'] / total * 100:.0f}%</td>
        </tr>
""")
            html_parts.append("</table></div>")
        
        # 结束
        html_parts.append(f"""
<div class="summary-box">
    <h2>生成时间</h2>
    <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>

</div>
</body>
</html>
""")
        
        html_content = ''.join(html_parts)
        
        # 保存文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML报告已保存: {output_path}")
        
        return html_content
    
    def generate_notebook_summary(self) -> str:
        """生成Notebook嵌入的Markdown摘要"""
        summary = f"""
## 📊 回测结果摘要

### 基本信息
- **回测区间**: {self.result.config.start_date} ~ {self.result.config.end_date}
- **总信号数**: {self.result.total_signals}
- **回测耗时**: {self.result.duration_seconds:.1f}秒

### 准确率统计

| 周期 | 准确率 | 评价 |
|------|--------|------|
| 短期 (5日) | {self.result.short_accuracy_5d:.1f}% | {'✅' if self.result.short_accuracy_5d > 60 else '⚠️'} |
| 中期 (20日) | {self.result.medium_accuracy_20d:.1f}% | {'✅' if self.result.medium_accuracy_20d > 60 else '⚠️'} |
| 长期 (60日) | {self.result.long_accuracy_60d:.1f}% | {'✅' if self.result.long_accuracy_60d > 60 else '⚠️'} |
| 市场状态 | {self.result.state_accuracy_60d:.1f}% | {'✅' if self.result.state_accuracy_60d > 60 else '⚠️'} |

### 分类准确率

| 信号类型 | 短期看多 | 短期看空 | 中期看多 | 中期看空 | 长期看多 | 长期看空 |
|----------|----------|----------|----------|----------|----------|----------|
| 准确率 | {self.result.short_bullish_accuracy:.0f}% | {self.result.short_bearish_accuracy:.0f}% | {self.result.medium_bullish_accuracy:.0f}% | {self.result.medium_bearish_accuracy:.0f}% | {self.result.long_bullish_accuracy:.0f}% | {self.result.long_bearish_accuracy:.0f}% |

### 市场状态识别

| 状态类别 | 牛市 | 熊市 | 震荡 |
|----------|------|------|------|
| 60日准确率 | {self.result.bull_state_accuracy:.0f}% | {self.result.bear_state_accuracy:.0f}% | {self.result.volatile_state_accuracy:.0f}% |
"""
        return summary
    
    def display_in_notebook(self):
        """在Notebook中显示图表"""
        if not HAS_PLOTLY:
            print("Plotly未安装，无法显示图表")
            return
        
        from IPython.display import display, Markdown
        
        # 显示摘要
        display(Markdown(self.generate_notebook_summary()))
        
        # 显示图表
        figs = [
            self.create_accuracy_heatmap(),
            self.create_signal_distribution_pie(),
            self.create_yearly_accuracy_bar(),
            self.create_market_state_timeline(),
            self.create_score_timeseries(),
        ]
        
        for fig in figs:
            if fig:
                fig.show()


def visualize_backtest_result(result: Any, output_html: str = None) -> BacktestVisualization:
    """
    便捷函数：可视化回测结果
    
    Args:
        result: EnhancedBacktestResult 实例
        output_html: HTML报告输出路径 (可选)
        
    Returns:
        BacktestVisualization 实例
    """
    viz = BacktestVisualization(result)
    
    if output_html:
        viz.generate_html_report(output_html)
    
    return viz


if __name__ == "__main__":
    # 测试
    from core.signal_backtest import run_phase1_backtest
    
    logging.basicConfig(level=logging.INFO)
    
    print("运行Phase 1回测...")
    result = run_phase1_backtest(sample_interval=10)
    
    print("\n生成可视化...")
    viz = BacktestVisualization(result)
    
    # 生成HTML报告
    html_path = "/home/taotao/dev/QuantTest/TRQuant/output/backtest_report.html"
    viz.generate_html_report(html_path)
    
    print(f"\nHTML报告已保存: {html_path}")
    print("\nMarkdown摘要:")
    print(viz.generate_notebook_summary())

