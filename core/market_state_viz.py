"""
市场状态可视化模块 - Pro v4.0

集成组件：
- ChartEngine: 技术走势、共振热力图
- MarketGauge: 核心仪表盘
- 智能2x2布局
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Any

from core.market_state_lib import MarketState, MarketStateResult, get_all_states
from core.market_state_predictor import ComprehensivePrediction, PredictionDirection
from core.visualization.chart_engine import ChartEngine
from core.visualization.dashboard import MarketGauge


# ============ 配色方案 ============
COLORS = {
    'bull': '#00C853', 'bear': '#FF5252', 'range': '#FFB300', 'turning': '#448AFF',
    'bg': '#0d1117', 'card_bg': '#161b22', 'grid': '#21262d',
    'text': '#c9d1d9', 'text_secondary': '#8b949e', 'border': '#30363d',
    'positive': '#238636', 'negative': '#da3633', 'accent-blue': '#448AFF',
}

STATE_COLORS = {
    'BULL_STRONG': '#00E676', 'BULL_NORMAL': '#00C853', 'BULL_LATE': '#69F0AE', 'BULL_PULLBACK': '#B9F6CA',
    'BEAR_STRONG': '#FF1744', 'BEAR_NORMAL': '#FF5252', 'BEAR_LATE': '#FF8A80', 'BEAR_BOUNCE': '#FFCDD2',
    'RANGE_HIGH': '#FFD54F', 'RANGE_MID': '#FFC107', 'RANGE_LOW': '#FFCA28', 'RANGE_WIDE': '#FFE082',
    'TURNING_UP': '#448AFF', 'TURNING_DOWN': '#F44336'
}

PHASE_DESCRIPTIONS = {
    'BULL_STRONG': {'phase': '加速期', 'stage': '上升趋势第3阶段', 'action': '持股待涨,逢低加仓'},
    'BULL_NORMAL': {'phase': '主升期', 'stage': '上升趋势第2阶段', 'action': '积极持有,跟随趋势'},
    'BULL_LATE': {'phase': '高位期', 'stage': '上升趋势第4阶段', 'action': '逐步减仓,锁定利润'},
    'BULL_PULLBACK': {'phase': '回撤期', 'stage': '趋势内中继调整', 'action': '缩量企稳后补仓'},
    'BEAR_STRONG': {'phase': '加速跌', 'stage': '下降趋势第3阶段', 'action': '空仓观望,严格避险'},
    'BEAR_NORMAL': {'phase': '主跌期', 'stage': '下降趋势第2阶段', 'action': '控制仓位,防守至上'},
    'BEAR_LATE': {'phase': '筑底期', 'stage': '下降趋势第4阶段', 'action': '关注背离,分批回补'},
    'BEAR_BOUNCE': {'phase': '反弹期', 'stage': '趋势内技术修正', 'action': '减仓机会,不宜追高'},
    'RANGE_HIGH': {'phase': '压制区', 'stage': '震荡区间上沿', 'action': '波段止盈,等待突破'},
    'RANGE_MID': {'phase': '均衡区', 'stage': '价值中枢整理', 'action': '高抛低吸,中性配置'},
    'RANGE_LOW': {'phase': '支撑区', 'stage': '震荡区间下沿', 'action': '逢低吸纳,注意破位'},
    'RANGE_WIDE': {'phase': '扩张期', 'stage': '波动率放大阶段', 'action': '轻仓交易,扩大止损'},
    'TURNING_UP': {'phase': '反转点', 'stage': '趋势由降转升', 'action': '确认信号,右侧建仓'},
    'TURNING_DOWN': {'phase': '派发点', 'stage': '趋势由升转降', 'action': '果断离场,现金为王'}
}

INDEX_CONFIG = {
    '000001.XSHG': {'name': '上证指数', 'icon': '🔴', 'desc': '权重蓝筹'},
    '399001.XSHE': {'name': '深证成指', 'icon': '🔵', 'desc': '综合市场'},
    '399006.XSHE': {'name': '创业板指', 'icon': '🟢', 'desc': '科技成长'},
    '000688.XSHG': {'name': '科创50', 'icon': '🟣', 'desc': '硬核科技'}
}


# ============ 核心可视化函数 ============

def plot_multi_index_state(results: Dict[str, MarketStateResult],
                           title: str = "A股四大指数市场状态") -> go.Figure:
    """智能2x2状态矩阵"""
    valid = [s for s in INDEX_CONFIG if s in results]
    n = len(valid)
    rows, cols = (2, 2) if n > 2 else (1, min(n, 2))
    
    fig = make_subplots(rows=rows, cols=cols,
                        specs=[[{"type": "table"}]*cols for _ in range(rows)],
                        vertical_spacing=0.04, horizontal_spacing=0.03)
    
    for idx, sym in enumerate(valid[:4]):
        r, c = (idx // cols) + 1, (idx % cols) + 1
        res = results[sym]
        cfg = INDEX_CONFIG[sym]
        sc = STATE_COLORS.get(res.state.name, '#888')
        ph = PHASE_DESCRIPTIONS.get(res.state.name, {'phase': '-', 'stage': '-', 'action': '-'})
        ind = res.indicators.to_dict()
        
        fig.add_trace(go.Table(
            header=dict(values=[f"<b>{cfg['icon']} {cfg['name']}</b>", cfg['desc']],
                       fill_color=COLORS['card_bg'], font=dict(color=COLORS['text'], size=15),
                       align=['left', 'right'], height=40, line_color=COLORS['border']),
            cells=dict(
                values=[[
                    f"<b style='color:{sc};font-size:20px'>{res.state.value}</b>",
                    f"阶段: <b>{ph['phase']}</b> | {ph['stage']}",
                    f"策略: <b style='color:{COLORS['accent-blue']}'>{ph['action']}</b>",
                    f"得分: <b style='color:{sc}'>{res.score:+.0f}</b> | 置信: {res.confidence:.0f}%",
                    f"仓位: {res.position_range[0]:.0%}-{res.position_range[1]:.0%}"
                ], [
                    "",
                    f"<span style='color:{COLORS['positive'] if ind.get('mom_5d',0)>0 else COLORS['negative']}'>5D: {ind.get('mom_5d',0):+.1f}%</span>",
                    f"<span style='color:{COLORS['positive'] if ind.get('mom_20d',0)>0 else COLORS['negative']}'>20D: {ind.get('mom_20d',0):+.1f}%</span>",
                    f"<span style='color:{COLORS['positive'] if ind.get('mom_60d',0)>0 else COLORS['negative']}'>60D: {ind.get('mom_60d',0):+.1f}%</span>",
                    f"波动: {ind.get('volatility_20d',0):.1f}%"
                ]],
                fill_color=COLORS['bg'], font=dict(color=COLORS['text'], size=13),
                align=['left', 'right'], height=30, line_color=COLORS['border']
            )
        ), row=r, col=c)
    
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=24, color=COLORS['text']), x=0.5),
        paper_bgcolor=COLORS['bg'], height=400 if rows==1 else 700,
        margin=dict(t=70, b=20, l=20, r=20), autosize=True
    )
    return fig


def plot_multi_prediction_dashboard(predictions: Dict[str, ComprehensivePrediction],
                                     title: str = "四指数三周期预测矩阵") -> go.Figure:
    """三周期预测矩阵"""
    valid = [s for s in INDEX_CONFIG if s in predictions]
    headers = ["<b>指数</b>", "<b>短期(5D)</b>", "<b>中期(20D)</b>", "<b>长期(120D+)</b>", "<b>综合信号</b>"]
    
    def fmt(p):
        c = COLORS['bull'] if p.direction.score > 0 else (COLORS['bear'] if p.direction.score < 0 else COLORS['range'])
        return f"<span style='color:{c}'>{p.direction.value}</span><br><small>{p.expected_return:+.1f}%</small>"
    
    rows = []
    for sym in valid:
        pred = predictions[sym]
        cfg = INDEX_CONFIG[sym]
        rows.append([
            f"{cfg['icon']} <b>{cfg['name']}</b>",
            fmt(pred.short_term), fmt(pred.medium_term), fmt(pred.long_term),
            f"<b>{pred.overall_signal}</b>"
        ])
    
    fig = go.Figure(go.Table(
        columnwidth=[100, 130, 130, 130, 150],
        header=dict(values=headers, fill_color=COLORS['card_bg'],
                   font=dict(color=COLORS['text'], size=14), align='center', height=40),
        cells=dict(values=list(zip(*rows)), fill_color=COLORS['bg'],
                  font=dict(color=COLORS['text'], size=13), align='center', height=55)
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=22, color=COLORS['text']), x=0.5),
        paper_bgcolor=COLORS['bg'], height=120+len(valid)*60, margin=dict(t=70, b=20, l=20, r=20)
    )
    return fig


def plot_market_overview_gauges(result: MarketStateResult, title: str = "核心指标概览") -> go.Figure:
    """核心仪表盘 (MarketGauge)"""
    mg = MarketGauge()
    fig_t = mg.create_trend_gauge(result.score, title="趋势动能")
    fig_r = mg.create_risk_gauge(result.indicators.volatility_20d, title="风险水平")
    pos = (result.position_range[0] + result.position_range[1]) / 2
    fig_p = mg.create_position_gauge(pos, title="建议仓位")
    
    fig = make_subplots(rows=1, cols=3,
                        specs=[[{"type": "indicator"}]*3], horizontal_spacing=0.05)
    fig.add_trace(fig_t.data[0], row=1, col=1)
    fig.add_trace(fig_r.data[0], row=1, col=2)
    fig.add_trace(fig_p.data[0], row=1, col=3)
    
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=22, color=COLORS['text']), x=0.5),
        paper_bgcolor=COLORS['bg'], height=320, margin=dict(t=80, b=20, l=20, r=20)
    )
    return fig


def plot_market_technical_charts(df: pd.DataFrame, title: str = "技术走势分析") -> go.Figure:
    """技术走势图 (ChartEngine)"""
    ce = ChartEngine(backend="plotly")
    fig = ce.plot_candlestick_with_indicators(df, ma_periods=[5,20,60,120], 
                                               show_volume=True, show_macd=True, 
                                               title=title, height=800)
    fig.update_layout(paper_bgcolor=COLORS['bg'], plot_bgcolor=COLORS['bg'],
                     font=dict(color=COLORS['text']))
    return fig


def plot_market_resonance_matrix(history: List[Dict], title: str = "多周期共振热力图") -> go.Figure:
    """共振热力图 (ChartEngine)"""
    ce = ChartEngine(backend="plotly")
    fig = ce.plot_resonance_heatmap(history, title=title)
    if fig:
        fig.update_layout(paper_bgcolor=COLORS['bg'], plot_bgcolor=COLORS['bg'],
                         font=dict(color=COLORS['text']), height=350)
    return fig


def plot_multi_params_table(params_dict: Dict[str, dict], title: str = "操作参数对比") -> go.Figure:
    """操作参数对比表"""
    valid = [s for s in INDEX_CONFIG if s in params_dict]
    headers = ["<b>参数</b>"] + [f"<b>{INDEX_CONFIG[s]['name']}</b>" for s in valid]
    
    metrics = [('状态', 'current_state', 'state_name'), ('策略', 'parameters', 'strategy'),
               ('仓位', 'parameters', 'position'), ('止损', 'parameters', 'stop_loss')]
    rows = []
    for label, k1, k2 in metrics:
        row = [f"<b>{label}</b>"]
        for s in valid:
            v = params_dict[s].get(k1, {}).get(k2, '-')
            if isinstance(v, float) and k2 in ['position', 'stop_loss']:
                v = f"{v*100:.0f}%"
            row.append(str(v))
        rows.append(row)
    
    fig = go.Figure(go.Table(
        columnwidth=[100] + [90]*len(valid),
        header=dict(values=headers, fill_color=COLORS['card_bg'],
                   font=dict(color=COLORS['text'], size=14), align='center', height=38),
        cells=dict(values=list(zip(*rows)), fill_color=COLORS['bg'],
                  font=dict(color=COLORS['text'], size=13), align=['left']+['center']*len(valid), height=35)
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=22, color=COLORS['text']), x=0.5),
        paper_bgcolor=COLORS['bg'], height=120+len(metrics)*40, margin=dict(t=70, b=20, l=20, r=20)
    )
    return fig


def plot_14_states_definition(title: str = "14种市场状态定义") -> go.Figure:
    """14种状态定义表"""
    states = get_all_states()
    headers = ["<b>类别</b>", "<b>状态</b>", "<b>特征</b>", "<b>操作</b>", "<b>仓位</b>"]
    rows = []
    for s in states:
        sc = s['state']
        ph = PHASE_DESCRIPTIONS.get(sc, {'phase': '-', 'stage': '-', 'action': '-'})
        cat = {'bull': '🟢牛', 'bear': '🔴熊', 'range': '🟡震荡', 'turning': '🔵转折'}.get(s['category'], '')
        pos_range = s.get('position', (0, 0))
        rows.append([cat, f"<b style='color:{STATE_COLORS.get(sc,'#888')}'>{s['name']}</b>",
                    ph['stage'], ph['action'], f"{pos_range[0]:.0%}-{pos_range[1]:.0%}"])
    
    fig = go.Figure(go.Table(
        columnwidth=[70, 110, 140, 140, 80],
        header=dict(values=headers, fill_color=COLORS['card_bg'],
                   font=dict(color=COLORS['text'], size=13), align='center', height=38),
        cells=dict(values=list(zip(*rows)), fill_color=COLORS['bg'],
                  font=dict(color=COLORS['text'], size=12), align=['center','left','left','left','center'], height=30)
    ))
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=20, color=COLORS['text']), x=0.5),
        paper_bgcolor=COLORS['bg'], height=600, margin=dict(t=70, b=20, l=20, r=20)
    )
    return fig


# 兼容别名
plot_4index_state = plot_multi_index_state
plot_4index_prediction = plot_multi_prediction_dashboard
plot_4index_params = plot_multi_params_table
