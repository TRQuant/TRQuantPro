# region imports
from AlgorithmImports import *
# endregion
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

def create_cognitive_bias_chart_plotly():
    """使用Plotly创建认知偏差统计图"""
    
    # 认知偏差数据 - 测试中文显示
    biases = ['过度自信', '确认偏误', '损失厌恶', 
              '锚定偏差', '代表性偏差', '从众心理']
    frequency = [85, 78, 92, 65, 72, 68]
    impact = [8.5, 7.8, 9.2, 6.5, 7.2, 6.8]
    
    # 创建子图
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('投资者认知偏差发生频率', 
                       '认知偏差对投资决策的影响程度'),
        specs=[[{"type": "bar"}, {"type": "bar"}]],
        horizontal_spacing=0.1  # 减少子图间距
    )
    
    # 左侧：发生频率图
    fig.add_trace(
        go.Bar(
            y=biases,
            x=frequency,
            orientation='h',
            name='发生频率',
            marker_color='#2E86AB',
            text=[f'{f}%' for f in frequency],
            textposition='auto',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{y}</b><br>发生频率: %{x}%<extra></extra>'
        ),
        row=1, col=1
    )
    
    # 右侧：影响程度图
    fig.add_trace(
        go.Bar(
            y=biases,
            x=impact,
            orientation='h',
            name='影响程度',
            marker_color='#A23B72',
            text=[f'{i}' for i in impact],
            textposition='auto',
            textfont=dict(size=14, color='white'),
            hovertemplate='<b>%{y}</b><br>影响程度: %{x}/10<extra></extra>'
        ),
        row=1, col=2
    )
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '投资认知偏差分析',
            'y':0.95,  # 调整标题位置
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 28, 'color': 'black', 'weight': 'bold'}
        },
        showlegend=False,
        height=500,  # 减少高度，减少留白
        width=1200,
        font=dict(size=18),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=60, r=60, t=80, b=60),  # 减少边距
        # 移除滚动条
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', fixedrange=True),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', fixedrange=True)
    )
    
    # 更新子图标题字体和位置
    fig.update_annotations(font_size=20, font_color='black')
    
    # 更新x轴
    fig.update_xaxes(
        title_text="发生频率 (%)", 
        row=1, col=1, 
        range=[0, 100],
        title_font=dict(size=16),
        tickfont=dict(size=14)
    )
    fig.update_xaxes(
        title_text="影响程度 (1-10)", 
        row=1, col=2, 
        range=[0, 10],
        title_font=dict(size=16),
        tickfont=dict(size=14)
    )
    
    # 更新y轴字体
    fig.update_yaxes(tickfont=dict(size=14), row=1, col=1)
    fig.update_yaxes(tickfont=dict(size=14), row=1, col=2)
    
    # 保存为HTML文件
    fig.write_html('public/images/001_Chapter1/generated/cognitive_biases_analysis.html')
    
    # 保存为PNG文件
    fig.write_image('public/images/001_Chapter1/generated/cognitive_biases_analysis_plotly.png', 
                   width=1200, height=500)
    
    print("认知偏差统计图已生成（Plotly版本）")

def create_investment_tools_chart_plotly():
    """使用Plotly创建简化的投资工具分析图 - 单y轴显示不同单位"""
    
    # 投资工具数据 - 测试中文显示
    tools = ['彭博终端', 'TradingView', 'GuruFocus', 
             'Morningstar', 'Seeking Alpha', '雅虎财经']
    usage_frequency = [95, 88, 72, 68, 65, 82]
    professionalism = [9.8, 8.5, 8.2, 8.7, 7.5, 6.8]
    cost_effectiveness = [6.5, 9.2, 8.8, 7.5, 8.0, 9.5]
    
    # 创建单图，使用单y轴
    fig = go.Figure()
    
    # 添加第一根柱子（市场采用率）
    fig.add_trace(go.Bar(
        name='市场采用率 (%)',
        x=tools,
        y=usage_frequency,
        marker_color='#2E86AB',
        text=[f'{f}%' for f in usage_frequency],
        textposition='auto',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{x}</b><br>市场采用率: %{y}%<extra></extra>'
    ))
    
    # 添加第二根柱子（专业度评分）
    fig.add_trace(go.Bar(
        name='专业度评分 (1-10)',
        x=tools,
        y=professionalism,
        marker_color='#A23B72',
        text=[f'{p}' for p in professionalism],
        textposition='auto',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{x}</b><br>专业度评分: %{y}/10<extra></extra>'
    ))
    
    # 添加第三根柱子（成本效益比）
    fig.add_trace(go.Bar(
        name='成本效益比 (1-10)',
        x=tools,
        y=cost_effectiveness,
        marker_color='#F18F01',
        text=[f'{c}' for c in cost_effectiveness],
        textposition='auto',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>%{x}</b><br>成本效益比: %{y}/10<extra></extra>'
    ))
    
    # 更新布局
    fig.update_layout(
        title={
            'text': '投资工具分析对比',
            'y':0.95,  # 调整标题位置
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 28, 'color': 'black', 'weight': 'bold'}
        },
        barmode='group',  # 分组显示，让所有柱子并列
        height=500,  # 减少高度，减少留白
        width=1200,
        font=dict(size=18),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="投资工具",
        xaxis_title_font=dict(size=16),
        yaxis_title="数值",
        yaxis_title_font=dict(size=16),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",  # 图例居中
            x=0.5,  # 图例居中
            font=dict(size=14)
        ),
        margin=dict(l=80, r=80, t=80, b=60),  # 左右边距相等，居中显示
        # y轴设置
        yaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#f0f0f0',
            tickfont=dict(size=12),
            range=[0, 100],  # 使用百分比范围
            tickmode='linear',
            dtick=20,  # 每20个单位显示一个刻度
            tickformat='.0f',
            fixedrange=True  # 禁用滚动
        ),
        # x轴设置
        xaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#f0f0f0',
            tickfont=dict(size=12),
            fixedrange=True  # 禁用滚动
        )
    )
    
    # 保存为HTML文件
    fig.write_html('public/images/001_Chapter1/generated/investment_tools_analysis.html')
    
    # 保存为PNG文件
    fig.write_image('public/images/001_Chapter1/generated/investment_tools_analysis_plotly.png', 
                   width=1200, height=500)
    
    print("投资工具分析图已生成（Plotly版本）")

if __name__ == "__main__":
    create_cognitive_bias_chart_plotly()
    create_investment_tools_chart_plotly() 