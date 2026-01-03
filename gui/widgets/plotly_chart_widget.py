# -*- coding: utf-8 -*-
"""
Plotly图表组件基类
================

提供统一的Plotly图表接口，通过QWebEngineView嵌入到PyQt6界面中。

功能:
- 统一的图表接口
- 主题和样式支持
- 交互式图表（缩放、平移、悬停等）
- 工具栏支持（下载、缩放、重置等）
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, pyqtSignal
import plotly.graph_objects as go
import plotly.offline as pyo
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# 尝试导入主题
try:
    from gui.styles.theme import Colors
except ImportError:
    # 默认主题
    class Colors:
        BG_PRIMARY = "#1a1a1a"
        BG_SECONDARY = "#2a2a2a"
        TEXT_PRIMARY = "#ffffff"
        TEXT_SECONDARY = "#cccccc"
        PRIMARY = "#3B82F6"
        SUCCESS = "#10B981"
        WARNING = "#F59E0B"
        ERROR = "#EF4444"


class PlotlyChartWidget(QWidget):
    """
    Plotly图表组件基类
    
    提供统一的Plotly图表接口，支持：
    - 交互式图表（缩放、平移、悬停）
    - 主题和样式自定义
    - 工具栏功能
    - 数据导出
    """
    
    # 信号：图表加载完成
    chart_loaded = pyqtSignal()
    # 信号：图表错误
    chart_error = pyqtSignal(str)
    
    def __init__(self, parent=None, title: str = ""):
        super().__init__(parent)
        self.title = title
        self.current_figure: Optional[go.Figure] = None
        self.web_view: Optional[QWebEngineView] = None
        
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建WebView
        try:
            self.web_view = QWebEngineView()
            self.web_view.setMinimumHeight(400)
            layout.addWidget(self.web_view)
        except Exception as e:
            logger.error(f"创建QWebEngineView失败: {e}")
            error_label = QLabel("⚠️ QWebEngineView未安装，无法显示图表")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet(f"color: {Colors.ERROR}; font-size: 14px; padding: 20px;")
            layout.addWidget(error_label)
            return
        
        # 工具栏（可选）
        self.toolbar = self._create_toolbar()
        if self.toolbar:
            layout.addWidget(self.toolbar)
    
    def _create_toolbar(self) -> Optional[QWidget]:
        """创建工具栏"""
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(8)
        
        # 重置按钮
        self.reset_btn = QPushButton("↩️ 重置")
        self.reset_btn.setToolTip("重置图表视图")
        self.reset_btn.clicked.connect(self.reset_view)
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BG_SECONDARY};
                border-radius: 4px;
                padding: 4px 12px;
            }}
            QPushButton:hover {{
                background-color: {Colors.PRIMARY};
            }}
        """)
        toolbar_layout.addWidget(self.reset_btn)
        
        toolbar_layout.addStretch()
        
        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px;")
        toolbar_layout.addWidget(self.status_label)
        
        return toolbar
    
    def plot(self, fig: go.Figure, config: Optional[Dict[str, Any]] = None):
        """
        显示Plotly图表
        
        Args:
            fig: Plotly图表对象
            config: Plotly配置选项
        """
        if self.web_view is None:
            logger.error("WebView未初始化")
            return
        
        try:
            self.current_figure = fig
            
            # 应用默认主题
            self._apply_theme(fig)
            
            # 默认配置
            default_config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': self.title or 'chart',
                    'height': 600,
                    'width': 1200,
                    'scale': 2
                }
            }
            
            if config:
                default_config.update(config)
            
            # 生成HTML
            html_str = pyo.plot(
                fig,
                output_type='div',
                include_plotlyjs='cdn',
                config=default_config,
                div_id=f"plotly-chart-{id(self)}"
            )
            
            # 设置HTML
            self.web_view.setHtml(html_str)
            
            # 更新状态
            if self.status_label:
                self.status_label.setText("图表已加载")
            
            self.chart_loaded.emit()
            
        except Exception as e:
            logger.error(f"绘制图表失败: {e}")
            if self.status_label:
                self.status_label.setText(f"错误: {str(e)}")
            self.chart_error.emit(str(e))
    
    def _apply_theme(self, fig: go.Figure):
        """
        应用主题样式
        
        Args:
            fig: Plotly图表对象
        """
        # 深色主题配置
        dark_template = {
            'layout': {
                'paper_bgcolor': Colors.BG_PRIMARY,
                'plot_bgcolor': Colors.BG_SECONDARY,
                'font': {
                    'color': Colors.TEXT_PRIMARY,
                    'family': 'Arial, sans-serif',
                    'size': 12
                },
                'xaxis': {
                    'gridcolor': '#404040',
                    'linecolor': Colors.TEXT_SECONDARY,
                    'zerolinecolor': '#404040'
                },
                'yaxis': {
                    'gridcolor': '#404040',
                    'linecolor': Colors.TEXT_SECONDARY,
                    'zerolinecolor': '#404040'
                },
                'colorway': [
                    Colors.PRIMARY,      # 蓝色
                    Colors.SUCCESS,      # 绿色
                    Colors.WARNING,      # 橙色
                    Colors.ERROR,        # 红色
                    '#8B5CF6',           # 紫色
                    '#EC4899',           # 粉色
                    '#14B8A6',           # 青色
                    '#F97316',           # 橘色
                ]
            }
        }
        
        # 更新布局
        fig.update_layout(**dark_template['layout'])
        
        # 如果有标题，设置标题样式
        if self.title:
            fig.update_layout(
                title={
                    'text': self.title,
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {
                        'size': 16,
                        'color': Colors.TEXT_PRIMARY
                    }
                }
            )
    
    def reset_view(self):
        """重置图表视图"""
        if self.current_figure and self.web_view:
            # 重新绘制图表以重置视图
            self.plot(self.current_figure)
            if self.status_label:
                self.status_label.setText("视图已重置")
    
    def export_image(self, filename: str = None, format: str = 'png'):
        """
        导出图表为图片
        
        Args:
            filename: 文件名（不含扩展名）
            format: 图片格式（png, svg, jpeg, webp）
        """
        if self.current_figure is None:
            logger.warning("没有可导出的图表")
            return
        
        try:
            if filename is None:
                filename = self.title or 'chart'
            
            # 使用plotly的write_image方法
            # 注意：需要安装kaleido: pip install kaleido
            try:
                self.current_figure.write_image(f"{filename}.{format}")
                if self.status_label:
                    self.status_label.setText(f"已导出: {filename}.{format}")
                logger.info(f"图表已导出: {filename}.{format}")
            except Exception as e:
                logger.warning(f"导出图片失败（可能需要安装kaleido）: {e}")
                if self.status_label:
                    self.status_label.setText("导出失败（需要安装kaleido）")
        except Exception as e:
            logger.error(f"导出图表失败: {e}")
            self.chart_error.emit(f"导出失败: {str(e)}")
    
    def get_figure(self) -> Optional[go.Figure]:
        """获取当前图表对象"""
        return self.current_figure
    
    def clear(self):
        """清空图表"""
        if self.web_view:
            self.web_view.setHtml("")
        self.current_figure = None
        if self.status_label:
            self.status_label.setText("已清空")


class PlotlyChartFactory:
    """Plotly图表工厂类，提供常用图表的快速创建方法"""
    
    @staticmethod
    def create_line_chart(
        x_data,
        y_data,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        series_name: str = "数据",
        color: str = None
    ) -> go.Figure:
        """创建折线图"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=x_data,
            y=y_data,
            mode='lines+markers',
            name=series_name,
            line=dict(color=color or Colors.PRIMARY, width=2),
            marker=dict(size=4)
        ))
        
        if x_label:
            fig.update_xaxes(title_text=x_label)
        if y_label:
            fig.update_yaxes(title_text=y_label)
        if title:
            fig.update_layout(title=title)
        
        return fig
    
    @staticmethod
    def create_candlestick_chart(
        dates,
        open_prices,
        high_prices,
        low_prices,
        close_prices,
        title: str = "K线图",
        volume: Optional[list] = None
    ) -> go.Figure:
        """创建K线图"""
        from plotly.subplots import make_subplots
        
        if volume is not None:
            # 带成交量的K线图
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(title, '成交量'),
                row_heights=[0.7, 0.3]
            )
            
            # K线
            fig.add_trace(
                go.Candlestick(
                    x=dates,
                    open=open_prices,
                    high=high_prices,
                    low=low_prices,
                    close=close_prices,
                    name='K线'
                ),
                row=1, col=1
            )
            
            # 成交量
            fig.add_trace(
                go.Bar(
                    x=dates,
                    y=volume,
                    name='成交量',
                    marker_color=Colors.SUCCESS
                ),
                row=2, col=1
            )
            
            fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
            fig.update_xaxes(title_text="日期", row=2, col=1)
            fig.update_yaxes(title_text="价格", row=1, col=1)
            fig.update_yaxes(title_text="成交量", row=2, col=1)
        else:
            # 简单K线图
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=dates,
                open=open_prices,
                high=high_prices,
                low=low_prices,
                close=close_prices,
                name='K线'
            ))
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(title=title)
        
        return fig
    
    @staticmethod
    def create_bar_chart(
        categories,
        values,
        title: str = "",
        x_label: str = "",
        y_label: str = "",
        color: str = None
    ) -> go.Figure:
        """创建柱状图"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name="数据",
            marker_color=color or Colors.PRIMARY
        ))
        
        if x_label:
            fig.update_xaxes(title_text=x_label)
        if y_label:
            fig.update_yaxes(title_text=y_label)
        if title:
            fig.update_layout(title=title)
        
        return fig
    
    @staticmethod
    def create_pie_chart(
        labels,
        values,
        title: str = ""
    ) -> go.Figure:
        """创建饼图"""
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.3,  # 环形图
            textinfo='label+percent',
            textposition='outside'
        ))
        
        if title:
            fig.update_layout(title=title)
        
        return fig
    
    @staticmethod
    def create_heatmap(
        z_data,
        x_labels=None,
        y_labels=None,
        title: str = "",
        colorscale: str = "Viridis"
    ) -> go.Figure:
        """创建热力图"""
        fig = go.Figure()
        
        fig.add_trace(go.Heatmap(
            z=z_data,
            x=x_labels,
            y=y_labels,
            colorscale=colorscale,
            showscale=True
        ))
        
        if title:
            fig.update_layout(title=title)
        
        return fig
    
    @staticmethod
    def create_radar_chart(
        categories,
        values_list: list,
        series_names: list = None,
        title: str = ""
    ) -> go.Figure:
        """创建雷达图"""
        fig = go.Figure()
        
        if series_names is None:
            series_names = [f"系列{i+1}" for i in range(len(values_list))]
        
        for i, (values, name) in enumerate(zip(values_list, series_names)):
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=name,
                line_color=Colors.PRIMARY if i == 0 else None
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            title=title
        )
        
        return fig
