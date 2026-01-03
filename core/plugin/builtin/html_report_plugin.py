# -*- coding: utf-8 -*-
"""
HTML报告插件
===========

生成美观的HTML回测报告
"""

import logging
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime

from core.plugin import VisualizationPlugin, PluginInfo, PluginType

logger = logging.getLogger(__name__)


class HtmlReportPlugin(VisualizationPlugin):
    """
    HTML报告生成插件
    
    功能:
    - 权益曲线图
    - 收益分布图
    - 绩效指标表
    - 交易明细
    """
    
    @property
    def info(self) -> PluginInfo:
        return PluginInfo(
            name="html_report",
            type=PluginType.VISUALIZATION,
            version="1.0.0",
            author="TRQuant",
            description="生成HTML格式的回测报告",
            dependencies=[],
            config_schema={
                "template": {"type": "string", "default": "default"},
                "output_dir": {"type": "string", "default": "reports"},
            }
        )
    
    def __init__(self):
        super().__init__()
        self._output_dir = "reports"
    
    def initialize(self) -> bool:
        self._output_dir = self._config.get("output_dir", "reports")
        Path(self._output_dir).mkdir(parents=True, exist_ok=True)
        return True
    
    def start(self) -> bool:
        return True
    
    def stop(self) -> bool:
        return True
    
    def plot_equity_curve(self, equity_data: List[Dict], output_path: str = ""):
        """绘制权益曲线（内嵌在报告中）"""
        # 在generate_report中实现
        pass
    
    def plot_returns(self, returns_data: List[float], output_path: str = ""):
        """绘制收益分布（内嵌在报告中）"""
        pass
    
    def generate_report(self, backtest_result: Dict, output_path: str = "") -> str:
        """
        生成完整的HTML回测报告
        
        Args:
            backtest_result: 回测结果字典
            output_path: 输出路径（可选）
            
        Returns:
            报告文件路径
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{self._output_dir}/report_{timestamp}.html"
        
        # 提取数据
        total_return = backtest_result.get("total_return", 0)
        annual_return = backtest_result.get("annual_return", 0)
        sharpe_ratio = backtest_result.get("sharpe_ratio", 0)
        max_drawdown = backtest_result.get("max_drawdown", 0)
        win_rate = backtest_result.get("win_rate", 0)
        total_trades = backtest_result.get("total_trades", 0)
        run_time = backtest_result.get("run_time", 0)
        
        equity_curve = backtest_result.get("equity_curve", {})
        
        # 生成HTML
        html = self._generate_html(
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=total_trades,
            run_time=run_time,
            equity_curve=equity_curve,
        )
        
        # 保存文件
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"报告已生成: {output_path}")
        return output_path
    
    def _generate_html(self, **kwargs) -> str:
        """生成HTML内容"""
        total_return = kwargs.get("total_return", 0)
        annual_return = kwargs.get("annual_return", 0)
        sharpe_ratio = kwargs.get("sharpe_ratio", 0)
        max_drawdown = kwargs.get("max_drawdown", 0)
        win_rate = kwargs.get("win_rate", 0)
        total_trades = kwargs.get("total_trades", 0)
        run_time = kwargs.get("run_time", 0)
        equity_curve = kwargs.get("equity_curve", {})
        
        # 生成权益曲线数据
        equity_data = equity_curve.get("equity", {})
        dates = list(equity_data.keys()) if isinstance(equity_data, dict) else []
        values = list(equity_data.values()) if isinstance(equity_data, dict) else []
        
        # 格式化日期
        dates_str = [str(d)[:10] for d in dates]
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>韬睿量化 - 回测报告</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #e8e8e8;
            min-height: 100vh;
            padding: 2rem;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }}
        .header h1 {{
            font-size: 2.5rem;
            background: linear-gradient(90deg, #00d9ff, #00ff88);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        .header .subtitle {{
            color: #888;
            font-size: 1rem;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0, 217, 255, 0.2);
        }}
        .metric-card .value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        .metric-card .label {{
            color: #888;
            font-size: 0.9rem;
        }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4444; }}
        .neutral {{ color: #00d9ff; }}
        .chart-container {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .chart-container h2 {{
            margin-bottom: 1.5rem;
            color: #00d9ff;
        }}
        .chart-wrapper {{
            position: relative;
            height: 400px;
        }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 韬睿量化回测报告</h1>
            <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="value {'positive' if total_return > 0 else 'negative'}">{total_return:.2%}</div>
                <div class="label">总收益率</div>
            </div>
            <div class="metric-card">
                <div class="value {'positive' if annual_return > 0 else 'negative'}">{annual_return:.2%}</div>
                <div class="label">年化收益</div>
            </div>
            <div class="metric-card">
                <div class="value neutral">{sharpe_ratio:.2f}</div>
                <div class="label">夏普比率</div>
            </div>
            <div class="metric-card">
                <div class="value negative">{max_drawdown:.2%}</div>
                <div class="label">最大回撤</div>
            </div>
            <div class="metric-card">
                <div class="value {'positive' if win_rate > 0.5 else 'neutral'}">{win_rate:.1%}</div>
                <div class="label">胜率</div>
            </div>
            <div class="metric-card">
                <div class="value neutral">{total_trades}</div>
                <div class="label">交易次数</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h2>📈 权益曲线</h2>
            <div class="chart-wrapper">
                <canvas id="equityChart"></canvas>
            </div>
        </div>
        
        <div class="footer">
            <p>韬睿量化系统 TRQuant © 2025 | 运行耗时: {run_time:.2f}秒</p>
        </div>
    </div>
    
    <script>
        const ctx = document.getElementById('equityChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {dates_str},
                datasets: [{{
                    label: '净值',
                    data: {values},
                    borderColor: '#00d9ff',
                    backgroundColor: 'rgba(0, 217, 255, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        labels: {{ color: '#888' }}
                    }}
                }},
                scales: {{
                    x: {{
                        ticks: {{ color: '#888', maxTicksLimit: 10 }},
                        grid: {{ color: 'rgba(255,255,255,0.05)' }}
                    }},
                    y: {{
                        ticks: {{ color: '#888' }},
                        grid: {{ color: 'rgba(255,255,255,0.05)' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
        
        return html

