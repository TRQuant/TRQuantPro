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


# 颜色配置 (Dark Mode)
COLORS = {
    'background': '#1E1E1E',
    'paper': '#252525',
    'text': '#FFFFFF',
    'grid': '#333333',
    'bullish': '#00C853',
    'bearish': '#FF5252',
    'neutral': '#FFC107',
    'bull_state': '#4CAF50',
    'bear_state': '#F44336',
    'volatile_state': '#FF9800',
    'short': '#2196F3',
    'medium': '#9C27B0',
    'long': '#FF5722',
}


class BacktestVisualization:
    """回测结果可视化"""
    
    def __init__(self, result: Any):
        """
        初始化可视化器
        
        Args:
            result: EnhancedBacktestResult 实例
        """
        self.result = result
        self.signals_df = self._signals_to_dataframe()
    
    def _signals_to_dataframe(self) -> pd.DataFrame:
        """将信号列表转换为DataFrame"""
        if not self.result.signals:
            return pd.DataFrame()
        
        data = []
        for s in self.result.signals:
            data.append({
                'date': pd.to_datetime(s.date),
                'signal_type': s.signal_type.value,
                'composite_score': s.composite_score,
                'short_score': s.short_term_score,
                'medium_score': s.medium_term_score,
                'long_score': s.long_term_score,
                'market_state': s.market_state,
                'state_category': s.state_category.value,
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
            textfont={"size": 14, "color": "white"},
            hovertemplate='%{y} %{x}: %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='准确率热力图 (各周期验证)',
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            height=400,
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
            title='信号分布',
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            height=400,
        )
        
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
        
        fig.update_layout(
            title='年度分周期准确率',
            xaxis_title='年份',
            yaxis_title='准确率 (%)',
            barmode='group',
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            xaxis=dict(gridcolor=COLORS['grid']),
            yaxis=dict(gridcolor=COLORS['grid'], range=[0, 100]),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
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
        
        fig.update_layout(
            title='信号得分与收益时序',
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            height=800,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(gridcolor=COLORS['grid'])
        fig.update_yaxes(gridcolor=COLORS['grid'])
        
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
            title='市场状态时间线',
            xaxis_title='日期',
            yaxis_title='状态类别',
            paper_bgcolor=COLORS['paper'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text']),
            xaxis=dict(gridcolor=COLORS['grid']),
            yaxis=dict(gridcolor=COLORS['grid']),
            height=300,
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

