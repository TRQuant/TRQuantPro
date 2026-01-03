# -*- coding: utf-8 -*-
"""
回测结果可视化面板
==================

展示回测结果的图表和数据

功能:
- 权益曲线图
- 收益分布图
- 持仓分析
- 交易明细
- 风险指标
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter, QHeaderView, QGroupBox, QScrollArea,
    QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QFont

# Plotly图表（优先）
try:
    import plotly.graph_objects as go
    from gui.widgets.plotly_chart_widget import PlotlyChartWidget
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("Plotly未安装，将使用SimpleChart")
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)



class PlotlyChart(PlotlyChartWidget if PLOTLY_AVAILABLE else QFrame):
    """Plotly图表控件（优先使用Plotly，降级到SimpleChart）"""
    
    def __init__(self, parent=None):
        if PLOTLY_AVAILABLE:
            super().__init__(parent, title="图表")
        else:
            super().__init__(parent)
            self.setMinimumHeight(200)
            self.setStyleSheet("""
                QFrame {
                    background: #1e1e2e;
                    border: 1px solid #404050;
                    border-radius: 8px;
                }
            """)
        
        self._data: List[float] = []
        self._benchmark_data: List[float] = []
        self._title = ""
        self._x_labels: List[str] = []
    
    def set_data(self, data: List[float], benchmark: List[float] = None,
                 title: str = "", x_labels: List[str] = None):
        """设置图表数据"""
        self._data = data
        self._benchmark_data = benchmark or []
        self._title = title
        self._x_labels = x_labels or []
        
        if PLOTLY_AVAILABLE:
            self._plot_plotly()
        else:
            self.update()  # 触发paintEvent
    
    def _plot_plotly(self):
        """使用Plotly绘制图表"""
        if not self._data:
            return
        
        try:
            from gui.widgets.plotly_chart_widget import PlotlyChartFactory
            import pandas as pd
            
            # 准备数据
            dates = self._x_labels if self._x_labels else [str(i) for i in range(len(self._data))]
            
            # 创建折线图
            fig = PlotlyChartFactory.create_line_chart(
                x_data=dates,
                y_data=self._data,
                title=self._title,
                x_label="日期",
                y_label="收益率",
                series_name="策略",
                color="#00d9ff"
            )
            
            # 添加基准线
            if self._benchmark_data:
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=self._benchmark_data,
                    mode='lines',
                    name='基准',
                    line=dict(color='#888888', width=2)
                ))
            
            # 显示图表
            self.plot(fig)
            
        except Exception as e:
            logger.error(f"绘制Plotly图表失败: {e}")
            import traceback
            traceback.print_exc()
    
    def paintEvent(self, event):
        """绘制图表（降级模式）"""
        if PLOTLY_AVAILABLE:
            return  # Plotly模式不需要paintEvent
        
        super().paintEvent(event)
        
        if not self._data:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 边距
        margin = 50
        width = self.width() - 2 * margin
        height = self.height() - 2 * margin
        
        # 绘制标题
        painter.setPen(QColor("#e0e0e0"))
        painter.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        painter.drawText(margin, 25, self._title)
        
        # 计算数据范围
        all_data = self._data + self._benchmark_data
        min_val = min(all_data) if all_data else 0
        max_val = max(all_data) if all_data else 1
        val_range = max_val - min_val if max_val != min_val else 1
        
        # 绘制网格线
        painter.setPen(QPen(QColor("#404050"), 1, Qt.PenStyle.DashLine))
        for i in range(5):
            y = margin + i * height / 4
            painter.drawLine(int(margin), int(y), int(margin + width), int(y))
            
            # Y轴标签
            val = max_val - i * val_range / 4
            painter.setPen(QColor("#888"))
            painter.setFont(QFont("Consolas", 9))
            painter.drawText(5, int(y + 5), f"{val:.1%}")
            painter.setPen(QPen(QColor("#404050"), 1, Qt.PenStyle.DashLine))
        
        # 绘制基准线（如果有）
        if self._benchmark_data:
            painter.setPen(QPen(QColor("#888888"), 2))
            self._draw_line(painter, self._benchmark_data, margin, width, height, min_val, val_range)
        
        # 绘制主数据线
        painter.setPen(QPen(QColor("#00d9ff"), 2))
        self._draw_line(painter, self._data, margin, width, height, min_val, val_range)
    
    def _draw_line(self, painter, data, margin, width, height, min_val, val_range):
        """绘制折线"""
        if not data:
            return
        
        points = []
        for i, val in enumerate(data):
            x = margin + i * width / (len(data) - 1) if len(data) > 1 else margin
            y = margin + height - (val - min_val) / val_range * height
            points.append((int(x), int(y)))
        
        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])


class SimpleChart(QFrame):
    """简单图表控件（PyQt6原生绘制）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setStyleSheet("""
            QFrame {
                background: #1e1e2e;
                border: 1px solid #404050;
                border-radius: 8px;
            }
        """)
        
        self._data: List[float] = []
        self._benchmark_data: List[float] = []
        self._title = ""
        self._x_labels: List[str] = []
    
    def set_data(self, data: List[float], benchmark: List[float] = None,
                 title: str = "", x_labels: List[str] = None):
        """设置图表数据"""
        self._data = data
        self._benchmark_data = benchmark or []
        self._title = title
        self._x_labels = x_labels or []
        self.update()
    
    def paintEvent(self, event):
        """绘制图表"""
        super().paintEvent(event)
        
        if not self._data:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 边距
        margin = 50
        width = self.width() - 2 * margin
        height = self.height() - 2 * margin
        
        # 绘制标题
        painter.setPen(QColor("#e0e0e0"))
        painter.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        painter.drawText(margin, 25, self._title)
        
        # 计算数据范围
        all_data = self._data + self._benchmark_data
        min_val = min(all_data) if all_data else 0
        max_val = max(all_data) if all_data else 1
        val_range = max_val - min_val if max_val != min_val else 1
        
        # 绘制网格线
        painter.setPen(QPen(QColor("#404050"), 1, Qt.PenStyle.DashLine))
        for i in range(5):
            y = margin + i * height / 4
            painter.drawLine(int(margin), int(y), int(margin + width), int(y))
            
            # Y轴标签
            val = max_val - i * val_range / 4
            painter.setPen(QColor("#888"))
            painter.setFont(QFont("Consolas", 9))
            painter.drawText(5, int(y + 5), f"{val:.1%}")
            painter.setPen(QPen(QColor("#404050"), 1, Qt.PenStyle.DashLine))
        
        # 绘制基准线（如果有）
        if self._benchmark_data:
            painter.setPen(QPen(QColor("#888888"), 2))
            self._draw_line(painter, self._benchmark_data, margin, width, height, min_val, val_range)
        
        # 绘制主数据线
        painter.setPen(QPen(QColor("#00d9ff"), 2))
        self._draw_line(painter, self._data, margin, width, height, min_val, val_range)
        
        # 绘制图例
        painter.setFont(QFont("Microsoft YaHei", 9))
        legend_x = margin + width - 150
        painter.setPen(QColor("#00d9ff"))
        painter.drawLine(int(legend_x), int(margin - 15), int(legend_x + 20), int(margin - 15))
        painter.drawText(int(legend_x + 25), int(margin - 10), "策略")
        
        if self._benchmark_data:
            painter.setPen(QColor("#888888"))
            painter.drawLine(int(legend_x), int(margin - 0), int(legend_x + 20), int(margin - 0))
            painter.drawText(int(legend_x + 25), int(margin + 5), "基准")
    
    def _draw_line(self, painter: QPainter, data: List[float],
                   margin: int, width: int, height: int,
                   min_val: float, val_range: float):
        """绘制折线"""
        if len(data) < 2:
            return
        
        step = width / (len(data) - 1)
        
        for i in range(len(data) - 1):
            x1 = margin + i * step
            y1 = margin + height - (data[i] - min_val) / val_range * height
            x2 = margin + (i + 1) * step
            y2 = margin + height - (data[i + 1] - min_val) / val_range * height
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))


class MetricCard(QFrame):
    """指标卡片"""
    
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: #2d2d3d;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.value_label = QLabel("--")
        self.value_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00d9ff;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #888; font-size: 11px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
    
    def set_value(self, value: str, color: str = "#00d9ff"):
        """设置值"""
        self.value_label.setText(value)
        self.value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")


class BacktestResultPanel(QWidget):
    """回测结果可视化面板"""
    
    report_requested = pyqtSignal(str)  # report_path
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result: Dict = {}
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # === 顶部概览 ===
        overview_group = QGroupBox("绩效概览")
        overview_layout = QHBoxLayout(overview_group)
        
        self.metric_cards = {}
        metrics = [
            ("total_return", "总收益"),
            ("annual_return", "年化收益"),
            ("sharpe_ratio", "夏普比率"),
            ("max_drawdown", "最大回撤"),
            ("win_rate", "胜率"),
            ("trade_count", "交易次数"),
        ]
        
        for key, title in metrics:
            card = MetricCard(title)
            overview_layout.addWidget(card)
            self.metric_cards[key] = card
        
        layout.addWidget(overview_group)
        
        # === 标签页 ===
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #404050;
                border-radius: 5px;
                background: #1e1e2e;
            }
            QTabBar::tab {
                background: #2d2d3d;
                color: #888;
                padding: 8px 15px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background: #1e1e2e;
                color: #00d9ff;
            }
        """)
        
        # --- Tab1: 权益曲线 ---
        equity_tab = QWidget()
        equity_layout = QVBoxLayout(equity_tab)
        
        self.equity_chart = PlotlyChart() if PLOTLY_AVAILABLE else SimpleChart()
        equity_layout.addWidget(self.equity_chart)
        
        tabs.addTab(equity_tab, "📈 权益曲线")
        
        # --- Tab2: 收益分布 ---
        returns_tab = QWidget()
        returns_layout = QVBoxLayout(returns_tab)
        
        self.returns_chart = SimpleChart()
        returns_layout.addWidget(self.returns_chart)
        
        # 收益统计表
        returns_stats = QGroupBox("收益统计")
        stats_layout = QGridLayout(returns_stats)
        
        self.stats_labels = {}
        stat_items = [
            ("daily_return", "日均收益"),
            ("monthly_return", "月均收益"),
            ("best_day", "最佳单日"),
            ("worst_day", "最差单日"),
            ("volatility", "年化波动"),
            ("calmar_ratio", "卡玛比率"),
        ]
        
        for i, (key, title) in enumerate(stat_items):
            row, col = i // 3, (i % 3) * 2
            stats_layout.addWidget(QLabel(f"{title}:"), row, col)
            label = QLabel("--")
            label.setStyleSheet("font-weight: bold;")
            stats_layout.addWidget(label, row, col + 1)
            self.stats_labels[key] = label
        
        returns_layout.addWidget(returns_stats)
        
        tabs.addTab(returns_tab, "📊 收益分析")
        
        # --- Tab3: 持仓分析 ---
        position_tab = QWidget()
        position_layout = QVBoxLayout(position_tab)
        
        self.position_chart = SimpleChart()
        position_layout.addWidget(self.position_chart)
        
        # 持仓表格
        self.position_table = QTableWidget()
        self.position_table.setColumnCount(5)
        self.position_table.setHorizontalHeaderLabels([
            "股票代码", "股票名称", "持仓占比", "盈亏", "持有天数"
        ])
        self.position_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        position_layout.addWidget(self.position_table)
        
        tabs.addTab(position_tab, "📋 持仓分析")
        
        # --- Tab4: 交易明细 ---
        trade_tab = QWidget()
        trade_layout = QVBoxLayout(trade_tab)
        
        self.trade_table = QTableWidget()
        self.trade_table.setColumnCount(8)
        self.trade_table.setHorizontalHeaderLabels([
            "日期", "股票代码", "方向", "价格", "数量", "金额", "佣金", "盈亏"
        ])
        self.trade_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        trade_layout.addWidget(self.trade_table)
        
        tabs.addTab(trade_tab, "📝 交易明细")
        
        # --- Tab5: 风险分析 ---
        risk_tab = QWidget()
        risk_layout = QVBoxLayout(risk_tab)
        
        self.drawdown_chart = PlotlyChart() if PLOTLY_AVAILABLE else SimpleChart()
        risk_layout.addWidget(self.drawdown_chart)
        
        # 风险指标
        risk_group = QGroupBox("风险指标")
        risk_grid = QGridLayout(risk_group)
        
        self.risk_labels = {}
        risk_items = [
            ("max_drawdown", "最大回撤"),
            ("avg_drawdown", "平均回撤"),
            ("drawdown_days", "回撤天数"),
            ("var_95", "95% VaR"),
            ("cvar_95", "95% CVaR"),
            ("downside_risk", "下行风险"),
        ]
        
        for i, (key, title) in enumerate(risk_items):
            row, col = i // 3, (i % 3) * 2
            risk_grid.addWidget(QLabel(f"{title}:"), row, col)
            label = QLabel("--")
            label.setStyleSheet("font-weight: bold; color: #ff4444;")
            risk_grid.addWidget(label, row, col + 1)
            self.risk_labels[key] = label
        
        risk_layout.addWidget(risk_group)
        
        tabs.addTab(risk_tab, "⚠️ 风险分析")
        
        layout.addWidget(tabs)
        
        # === 底部按钮 ===
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        export_btn = QPushButton("📄 导出报告")
        export_btn.clicked.connect(self._export_report)
        btn_layout.addWidget(export_btn)
        
        compare_btn = QPushButton("📊 对比分析")
        compare_btn.clicked.connect(self._compare_results)
        btn_layout.addWidget(compare_btn)
        
        layout.addLayout(btn_layout)
    
    def load_result(self, result: Dict):
        """加载回测结果"""
        self._result = result
        
        # 更新指标卡片
        for key, card in self.metric_cards.items():
            value = result.get(key)
            if value is not None:
                if key in ["total_return", "annual_return", "max_drawdown", "win_rate"]:
                    text = f"{value*100:.2f}%"
                    if key == "max_drawdown":
                        color = "#ff4444"
                    elif value >= 0:
                        color = "#00ff88"
                    else:
                        color = "#ff4444"
                elif key == "sharpe_ratio":
                    text = f"{value:.2f}"
                    color = "#00d9ff" if value > 1 else "#ffaa00"
                else:
                    text = str(value)
                    color = "#e0e0e0"
                card.set_value(text, color)
        
        # 更新权益曲线
        equity_curve = result.get("equity_curve", [])
        benchmark_curve = result.get("benchmark_curve", [])
        if equity_curve:
            # 转换为累计收益率
            equity_returns = [(e / equity_curve[0]) - 1 for e in equity_curve]
            benchmark_returns = [(b / benchmark_curve[0]) - 1 for b in benchmark_curve] if benchmark_curve else []
            self.equity_chart.set_data(equity_returns, benchmark_returns, "累计收益曲线")
        
        # 更新回撤曲线
        drawdown_curve = result.get("drawdown_curve", [])
        if drawdown_curve:
            self.drawdown_chart.set_data(drawdown_curve, title="回撤曲线")
        
        # 更新交易明细
        trades = result.get("trades", [])
        self._load_trades(trades)
        
        logger.info(f"已加载回测结果: {len(trades)}笔交易")
    
    def _load_trades(self, trades: List[Dict]):
        """加载交易明细"""
        self.trade_table.setRowCount(len(trades))
        
        for i, trade in enumerate(trades):
            self.trade_table.setItem(i, 0, QTableWidgetItem(
                trade.get("date", "")
            ))
            self.trade_table.setItem(i, 1, QTableWidgetItem(
                trade.get("symbol", "")
            ))
            self.trade_table.setItem(i, 2, QTableWidgetItem(
                trade.get("direction", "")
            ))
            self.trade_table.setItem(i, 3, QTableWidgetItem(
                f"{trade.get('price', 0):.2f}"
            ))
            self.trade_table.setItem(i, 4, QTableWidgetItem(
                str(trade.get("volume", 0))
            ))
            self.trade_table.setItem(i, 5, QTableWidgetItem(
                f"{trade.get('amount', 0):.2f}"
            ))
            self.trade_table.setItem(i, 6, QTableWidgetItem(
                f"{trade.get('commission', 0):.2f}"
            ))
            
            pnl = trade.get("pnl", 0)
            pnl_item = QTableWidgetItem(f"{pnl:.2f}")
            if pnl > 0:
                pnl_item.setForeground(QColor("#00ff88"))
            elif pnl < 0:
                pnl_item.setForeground(QColor("#ff4444"))
            self.trade_table.setItem(i, 7, pnl_item)
    
    def _export_report(self):
        """导出报告"""
        if self._result:
            self.report_requested.emit(self._result.get("report_path", ""))
    
    def _compare_results(self):
        """对比分析"""
        # TODO: 实现多策略对比
        pass


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    panel = BacktestResultPanel()
    panel.setWindowTitle("回测结果")
    panel.resize(1000, 700)
    
    # 测试数据
    import random
    equity = [1000000]
    for _ in range(100):
        equity.append(equity[-1] * (1 + random.uniform(-0.02, 0.025)))
    
    test_result = {
        "total_return": 0.25,
        "annual_return": 0.35,
        "sharpe_ratio": 1.5,
        "max_drawdown": -0.12,
        "win_rate": 0.55,
        "trade_count": 120,
        "equity_curve": equity,
        "trades": [
            {"date": "2024-01-15", "symbol": "000001.SZ", "direction": "买入",
             "price": 10.5, "volume": 1000, "amount": 10500, "commission": 5, "pnl": 0},
            {"date": "2024-02-01", "symbol": "000001.SZ", "direction": "卖出",
             "price": 11.2, "volume": 1000, "amount": 11200, "commission": 5, "pnl": 695},
        ]
    }
    panel.load_result(test_result)
    
    panel.show()
    sys.exit(app.exec())
