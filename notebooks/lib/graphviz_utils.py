"""
Graphviz 流程图工具模块
=======================

提供简洁的 Graphviz 流程图绑定，默认使用 Dark Mode 样式。

使用方式:
    from notebooks.lib.graphviz_utils import create_flowchart, add_node, add_edge, render
    
    # 方式1: 快速创建
    dot = create_flowchart('我的流程图')
    add_node(dot, 'A', '开始', 'success')
    add_node(dot, 'B', '处理', 'process')
    add_edge(dot, 'A', 'B')
    render(dot)
    
    # 方式2: 直接使用 graphviz
    import graphviz
    dot = graphviz.Digraph()
    ...
"""

import graphviz
from IPython.display import HTML, display
from typing import Optional, List, Tuple

# ==========================================
# Dark Mode 颜色方案
# ==========================================
DARK_COLORS = {
    # 节点颜色
    'success': '#2E7D32',      # 深绿色 - 成功/开始/结束
    'process': '#1565C0',      # 深蓝色 - 处理步骤
    'research': '#6A1B9A',     # 深紫色 - 研究阶段
    'live': '#D84315',         # 深橙色 - 实战阶段
    'data': '#00838F',         # 深青色 - 数据相关
    'warning': '#F9A825',      # 深黄色 - 警告
    'error': '#C62828',        # 深红色 - 错误
    'default': '#37474F',      # 深灰色 - 默认
    
    # 背景和边框
    'background': '#1E1E1E',   # 深色背景
    'edge': '#BDBDBD',         # 浅灰色边
    'text': '#FFFFFF',         # 白色文字
    'label': '#E0E0E0',        # 浅灰色标签
}


def create_flowchart(
    title: str = '',
    direction: str = 'TB',
    dark_mode: bool = True
) -> graphviz.Digraph:
    """
    创建流程图
    
    参数:
        title: 图表标题
        direction: 方向 ('TB'=从上到下, 'LR'=从左到右)
        dark_mode: 是否使用深色模式（默认 True）
    
    返回:
        graphviz.Digraph 对象
    """
    dot = graphviz.Digraph(comment=title, format='svg')
    
    bg_color = DARK_COLORS['background'] if dark_mode else '#FFFFFF'
    edge_color = DARK_COLORS['edge'] if dark_mode else '#333333'
    font_color = DARK_COLORS['text'] if dark_mode else '#212121'
    
    dot.attr(
        rankdir=direction,
        splines='spline',
        nodesep='0.6',
        ranksep='0.8',
        bgcolor=bg_color,
        fontname='Arial, SimHei, Microsoft YaHei',
        fontsize='14',
        fontcolor=font_color,
        label=title,
        labelloc='t',
    )
    
    dot.attr(
        'node',
        shape='box',
        style='rounded,filled',
        fontname='Arial, SimHei, Microsoft YaHei',
        fontsize='11',
        fontcolor=DARK_COLORS['text'] if dark_mode else '#212121',
        margin='0.3,0.15',
        penwidth='0',
    )
    
    dot.attr(
        'edge',
        fontname='Arial, SimHei, Microsoft YaHei',
        fontsize='9',
        fontcolor=DARK_COLORS['label'] if dark_mode else '#666666',
        color=edge_color,
        penwidth='1.5',
        arrowsize='0.8',
    )
    
    return dot


def add_node(
    dot: graphviz.Digraph,
    node_id: str,
    label: str,
    color_type: str = 'default',
    **kwargs
) -> None:
    """
    添加节点
    
    参数:
        dot: graphviz.Digraph 对象
        node_id: 节点 ID
        label: 节点标签
        color_type: 颜色类型 ('success', 'process', 'research', 'live', 'data', 'warning', 'error', 'default')
        **kwargs: 其他 graphviz 节点属性
    """
    fill_color = DARK_COLORS.get(color_type, DARK_COLORS['default'])
    dot.node(node_id, label, fillcolor=fill_color, **kwargs)


def add_edge(
    dot: graphviz.Digraph,
    source: str,
    target: str,
    label: str = '',
    **kwargs
) -> None:
    """
    添加边
    
    参数:
        dot: graphviz.Digraph 对象
        source: 源节点 ID
        target: 目标节点 ID
        label: 边标签（可选）
        **kwargs: 其他 graphviz 边属性
    """
    if label:
        dot.edge(source, target, label=label, **kwargs)
    else:
        dot.edge(source, target, **kwargs)


def render(dot: graphviz.Digraph, title: str = '') -> None:
    """
    渲染并显示流程图
    
    参数:
        dot: graphviz.Digraph 对象
        title: 显示标题（可选，会覆盖创建时的标题）
    """
    try:
        svg_data = dot.pipe(format='svg').decode('utf-8')
        
        # 如果有标题参数，使用它；否则从 dot 获取
        display_title = title if title else (dot.comment or '流程图')
        
        display(HTML(f"""
        <div style="padding: 20px; border-radius: 8px; background: {DARK_COLORS['background']}; margin: 10px 0;">
            <div style="text-align: center;">{svg_data}</div>
        </div>
        """))
    except Exception as e:
        print(f"❌ 渲染失败: {e}")
        print("请确保已安装系统 graphviz: sudo apt-get install graphviz")


def quick_flowchart(
    title: str,
    nodes: List[Tuple[str, str, str]],
    edges: List[Tuple[str, str]],
    direction: str = 'TB'
) -> None:
    """
    快速创建并显示流程图
    
    参数:
        title: 图表标题
        nodes: 节点列表 [(id, label, color_type), ...]
        edges: 边列表 [(source, target), ...]
        direction: 方向 ('TB' 或 'LR')
    
    示例:
        quick_flowchart(
            '测试流程',
            [('A', '开始', 'success'), ('B', '处理', 'process'), ('C', '结束', 'success')],
            [('A', 'B'), ('B', 'C')]
        )
    """
    dot = create_flowchart(title, direction)
    
    for node_id, label, color_type in nodes:
        add_node(dot, node_id, label, color_type)
    
    for source, target in edges:
        add_edge(dot, source, target)
    
    render(dot)


# ==========================================
# 导出
# ==========================================
__all__ = [
    'create_flowchart',
    'add_node',
    'add_edge',
    'render',
    'quick_flowchart',
    'DARK_COLORS',
]

