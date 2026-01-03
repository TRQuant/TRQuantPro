"""
统一可视化样式模块
==================

为研究 Notebooks 提供统一的可视化样式和交互控件。

特性：
- 统一的颜色方案
- 中文字体支持
- Plotly 和 Matplotlib 双模式
- 交互式控件（ipywidgets）

使用方式:
    from notebooks.lib.viz_style import apply_style, get_color_scheme, create_parameter_widgets
    
    apply_style()  # 应用统一样式
    colors = get_color_scheme()  # 获取颜色方案
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 尝试导入可视化库
try:
    import matplotlib.pyplot as plt
    import matplotlib
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    import plotly.graph_objects as go
    import plotly.io as pio
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

try:
    import ipywidgets as widgets
    from IPython.display import display
    HAS_WIDGETS = True
except ImportError:
    HAS_WIDGETS = False


# ==========================================
# 颜色方案
# ==========================================

@dataclass
class ColorScheme:
    """统一颜色方案"""
    # 趋势颜色
    bullish: str = "#26a69a"      # 看涨 (绿色)
    bearish: str = "#ef5350"      # 看跌 (红色)
    neutral: str = "#78909c"      # 中性 (灰色)
    
    # 警示颜色
    warning: str = "#ffc107"      # 警告 (黄色)
    success: str = "#4caf50"      # 成功 (绿色)
    danger: str = "#f44336"       # 危险 (红色)
    info: str = "#2196f3"         # 信息 (蓝色)
    
    # 主题颜色
    primary: str = "#667eea"      # 主色
    secondary: str = "#764ba2"    # 辅助色
    background: str = "#fafafa"   # 背景色
    grid: str = "#e0e0e0"         # 网格色
    text: str = "#212121"         # 文本色
    
    # 图表颜色序列
    sequence: List[str] = None
    
    def __post_init__(self):
        if self.sequence is None:
            self.sequence = [
                "#667eea", "#764ba2", "#26a69a", "#ffc107",
                "#ef5350", "#2196f3", "#9c27b0", "#ff9800",
            ]
    
    def get_trend_color(self, value: float) -> str:
        """根据值获取趋势颜色"""
        if value > 0.1:
            return self.bullish
        elif value < -0.1:
            return self.bearish
        else:
            return self.neutral
    
    def get_risk_color(self, value: float) -> str:
        """根据风险值获取颜色"""
        if value < 30:
            return self.success
        elif value < 60:
            return self.warning
        else:
            return self.danger


# 默认颜色方案
DEFAULT_COLORS = ColorScheme()


def get_color_scheme() -> ColorScheme:
    """获取默认颜色方案"""
    return DEFAULT_COLORS


# ==========================================
# Matplotlib 样式
# ==========================================

def apply_matplotlib_style(colors: ColorScheme = None):
    """应用 Matplotlib 统一样式"""
    if not HAS_MATPLOTLIB:
        logger.warning("Matplotlib 未安装")
        return
    
    colors = colors or DEFAULT_COLORS
    
    # 字体设置（支持中文）
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 颜色设置
    plt.rcParams['axes.facecolor'] = colors.background
    plt.rcParams['figure.facecolor'] = colors.background
    plt.rcParams['axes.edgecolor'] = colors.grid
    plt.rcParams['axes.labelcolor'] = colors.text
    plt.rcParams['xtick.color'] = colors.text
    plt.rcParams['ytick.color'] = colors.text
    plt.rcParams['text.color'] = colors.text
    plt.rcParams['grid.color'] = colors.grid
    
    # 图表大小
    plt.rcParams['figure.figsize'] = [14, 8]
    plt.rcParams['figure.dpi'] = 100
    
    # 字体大小
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    
    # 线条样式
    plt.rcParams['lines.linewidth'] = 1.5
    plt.rcParams['axes.linewidth'] = 1.0
    
    # 网格
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    
    logger.info("✅ Matplotlib 样式已应用")


def apply_plotly_style(colors: ColorScheme = None):
    """应用 Plotly 统一样式"""
    if not HAS_PLOTLY:
        logger.warning("Plotly 未安装")
        return
    
    colors = colors or DEFAULT_COLORS
    
    # 创建自定义模板
    custom_template = go.layout.Template(
        layout=go.Layout(
            font=dict(family="Microsoft YaHei, SimHei, sans-serif", size=12, color=colors.text),
            paper_bgcolor=colors.background,
            plot_bgcolor=colors.background,
            colorway=colors.sequence,
            xaxis=dict(
                gridcolor=colors.grid,
                showgrid=True,
                zeroline=False,
            ),
            yaxis=dict(
                gridcolor=colors.grid,
                showgrid=True,
                zeroline=False,
            ),
            title=dict(
                font=dict(size=16),
                x=0.5,
            ),
            legend=dict(
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor=colors.grid,
                borderwidth=1,
            ),
        )
    )
    
    pio.templates["trquant"] = custom_template
    pio.templates.default = "trquant"
    
    logger.info("✅ Plotly 样式已应用")


def apply_style(colors: ColorScheme = None):
    """应用所有可视化库的统一样式"""
    colors = colors or DEFAULT_COLORS
    
    if HAS_MATPLOTLIB:
        apply_matplotlib_style(colors)
    
    if HAS_PLOTLY:
        apply_plotly_style(colors)


# ==========================================
# 交互控件
# ==========================================

class ParameterWidgets:
    """
    参数控件管理器
    
    为 Notebook 创建交互式参数控件。
    """
    
    def __init__(self):
        if not HAS_WIDGETS:
            logger.warning("ipywidgets 未安装，交互控件不可用")
            return
        
        self.widgets = {}
        self.callbacks = {}
    
    def create_index_selector(
        self,
        default: str = "000001.XSHG",
        on_change: Callable = None
    ) -> Optional[Any]:
        """创建指数选择器"""
        if not HAS_WIDGETS:
            return None
        
        indices = {
            "上证指数": "000001.XSHG",
            "深证成指": "399001.XSHE",
            "沪深300": "000300.XSHG",
            "中证500": "000905.XSHG",
            "创业板指": "399006.XSHE",
            "科创50": "000688.XSHG",
        }
        
        dropdown = widgets.Dropdown(
            options=list(indices.items()),
            value=default,
            description="指数:",
            style={'description_width': '80px'},
        )
        
        if on_change:
            dropdown.observe(lambda change: on_change(change['new']), names='value')
        
        self.widgets['index'] = dropdown
        return dropdown
    
    def create_date_range_selector(
        self,
        start_default: str = None,
        end_default: str = None,
        on_change: Callable = None
    ) -> Optional[Any]:
        """创建日期范围选择器"""
        if not HAS_WIDGETS:
            return None
        
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        start_picker = widgets.DatePicker(
            description='开始日期:',
            value=datetime.strptime(start_default, "%Y-%m-%d").date() if start_default else start_date.date(),
            style={'description_width': '80px'},
        )
        
        end_picker = widgets.DatePicker(
            description='结束日期:',
            value=datetime.strptime(end_default, "%Y-%m-%d").date() if end_default else end_date.date(),
            style={'description_width': '80px'},
        )
        
        if on_change:
            start_picker.observe(lambda change: on_change(start_picker.value, end_picker.value), names='value')
            end_picker.observe(lambda change: on_change(start_picker.value, end_picker.value), names='value')
        
        self.widgets['start_date'] = start_picker
        self.widgets['end_date'] = end_picker
        
        return widgets.HBox([start_picker, end_picker])
    
    def create_threshold_slider(
        self,
        name: str,
        min_val: float = 0.0,
        max_val: float = 100.0,
        default: float = 50.0,
        step: float = 1.0,
        description: str = None,
        on_change: Callable = None
    ) -> Optional[Any]:
        """创建阈值滑块"""
        if not HAS_WIDGETS:
            return None
        
        slider = widgets.FloatSlider(
            value=default,
            min=min_val,
            max=max_val,
            step=step,
            description=description or name,
            continuous_update=False,
            style={'description_width': '100px'},
        )
        
        if on_change:
            slider.observe(lambda change: on_change(change['new']), names='value')
        
        self.widgets[name] = slider
        return slider
    
    def create_refresh_button(self, on_click: Callable) -> Optional[Any]:
        """创建刷新按钮"""
        if not HAS_WIDGETS:
            return None
        
        button = widgets.Button(
            description='刷新分析',
            button_style='primary',
            icon='refresh',
        )
        
        button.on_click(lambda b: on_click())
        
        self.widgets['refresh'] = button
        return button
    
    def create_control_panel(
        self,
        include_index: bool = True,
        include_dates: bool = True,
        include_refresh: bool = True,
        on_refresh: Callable = None
    ) -> Optional[Any]:
        """创建完整的控制面板"""
        if not HAS_WIDGETS:
            return None
        
        children = []
        
        if include_index:
            index_selector = self.create_index_selector()
            if index_selector:
                children.append(index_selector)
        
        if include_dates:
            date_selector = self.create_date_range_selector()
            if date_selector:
                children.append(date_selector)
        
        if include_refresh and on_refresh:
            refresh_btn = self.create_refresh_button(on_refresh)
            if refresh_btn:
                children.append(refresh_btn)
        
        if children:
            panel = widgets.VBox(children)
            return panel
        
        return None
    
    def get_values(self) -> Dict[str, Any]:
        """获取所有控件的当前值"""
        values = {}
        for name, widget in self.widgets.items():
            if hasattr(widget, 'value'):
                values[name] = widget.value
        return values
    
    def display(self, widget=None):
        """显示控件"""
        if not HAS_WIDGETS:
            print("⚠️ ipywidgets 未安装，无法显示交互控件")
            return
        
        if widget:
            display(widget)
        else:
            for w in self.widgets.values():
                display(w)


def create_parameter_widgets() -> ParameterWidgets:
    """创建参数控件管理器"""
    return ParameterWidgets()


# ==========================================
# 便捷函数
# ==========================================

def style_dataframe(df, columns: Dict[str, str] = None):
    """
    为 DataFrame 添加样式
    
    Args:
        df: DataFrame
        columns: 列名到样式类型的映射
                 类型: 'trend' (趋势颜色), 'risk' (风险颜色), 'percent' (百分比格式)
    
    Returns:
        Styled DataFrame
    """
    try:
        import pandas as pd
    except ImportError:
        return df
    
    colors = DEFAULT_COLORS
    
    def apply_trend_color(val):
        if isinstance(val, (int, float)):
            color = colors.get_trend_color(val)
            return f'color: {color}; font-weight: bold'
        return ''
    
    def apply_risk_color(val):
        if isinstance(val, (int, float)):
            color = colors.get_risk_color(val)
            return f'color: {color}; font-weight: bold'
        return ''
    
    styler = df.style
    
    if columns:
        for col, style_type in columns.items():
            if col in df.columns:
                if style_type == 'trend':
                    styler = styler.applymap(apply_trend_color, subset=[col])
                elif style_type == 'risk':
                    styler = styler.applymap(apply_risk_color, subset=[col])
                elif style_type == 'percent':
                    styler = styler.format({col: '{:.2%}'})
    
    return styler


if __name__ == '__main__':
    # 测试
    print("测试可视化样式模块")
    
    apply_style()
    
    colors = get_color_scheme()
    print(f"看涨颜色: {colors.bullish}")
    print(f"看跌颜色: {colors.bearish}")
    print(f"趋势颜色 (0.5): {colors.get_trend_color(0.5)}")
    print(f"风险颜色 (80): {colors.get_risk_color(80)}")

