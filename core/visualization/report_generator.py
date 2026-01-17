# -*- coding: utf-8 -*-
"""回测报告生成器 - 生成HTML可视化报告"""

import logging
from typing import Dict, Optional, Any, List
from datetime import datetime
from pathlib import Path
import json

logger = logging.getLogger(__name__)


class ReportGenerator:
    """回测报告生成器"""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(__file__).parent.parent.parent / "reports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate(self, metrics: Dict[str, Any], daily_returns: Optional[List[float]] = None,
                 trades: Optional[List[Dict]] = None, title: str = "回测报告") -> str:
        html = self._generate_html(metrics, daily_returns, title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = self.output_dir / f"report_{timestamp}.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        logger.info(f"报告已生成: {filepath}")
        return str(filepath)
    
    def _generate_html(self, metrics: Dict, daily_returns: Optional[List[float]], title: str) -> str:
        total_return = metrics.get("total_return", 0)
        annual_return = metrics.get("annual_return", 0)
        sharpe_ratio = metrics.get("sharpe_ratio", 0)
        max_drawdown = metrics.get("max_drawdown", 0)
        win_rate = metrics.get("win_rate", 0)
        total_trades = metrics.get("total_trades", 0)
        
        cumulative_data = "[]"
        if daily_returns:
            cumulative = []
            cum = 1.0
            for r in daily_returns:
                cum *= (1 + r)
                cumulative.append(round((cum - 1) * 100, 4))
            cumulative_data = json.dumps(cumulative)
        
        pos_class = 'positive' if total_return > 0 else 'negative'
        ann_class = 'positive' if annual_return > 0 else 'negative'
        
        return f'''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eee; min-height: 100vh; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ text-align: center; margin-bottom: 30px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metric-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; margin-bottom: 8px; }}
        .metric-label {{ color: #888; font-size: 0.9em; }}
        .positive {{ color: #00ff88; }}
        .negative {{ color: #ff4757; }}
        .neutral {{ color: #3498db; }}
        .chart-container {{ background: rgba(255,255,255,0.03); border-radius: 12px; padding: 20px; margin-bottom: 30px; }}
        .chart-title {{ font-size: 1.2em; margin-bottom: 15px; color: #ddd; }}
        .footer {{ text-align: center; color: #666; margin-top: 30px; font-size: 0.85em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {title}</h1>
        <div class="metrics-grid">
            <div class="metric-card"><div class="metric-value {pos_class}">{total_return*100:.2f}%</div><div class="metric-label">总收益率</div></div>
            <div class="metric-card"><div class="metric-value {ann_class}">{annual_return*100:.2f}%</div><div class="metric-label">年化收益</div></div>
            <div class="metric-card"><div class="metric-value neutral">{sharpe_ratio:.2f}</div><div class="metric-label">夏普比率</div></div>
            <div class="metric-card"><div class="metric-value negative">{abs(max_drawdown)*100:.2f}%</div><div class="metric-label">最大回撤</div></div>
            <div class="metric-card"><div class="metric-value neutral">{win_rate*100:.1f}%</div><div class="metric-label">胜率</div></div>
            <div class="metric-card"><div class="metric-value neutral">{total_trades}</div><div class="metric-label">交易次数</div></div>
        </div>
        <div class="chart-container">
            <div class="chart-title">📈 累计收益曲线</div>
            <canvas id="returnChart" height="300"></canvas>
        </div>
        <div class="footer">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 韬睿量化系统</div>
    </div>
    <script>
        const ctx = document.getElementById('returnChart').getContext('2d');
        const cumData = {cumulative_data};
        new Chart(ctx, {{
            type: 'line',
            data: {{ labels: cumData.map((_, i) => i + 1), datasets: [{{ label: '累计收益 (%)', data: cumData, borderColor: '#00d2ff', backgroundColor: 'rgba(0, 210, 255, 0.1)', fill: true, tension: 0.4, pointRadius: 0 }}] }},
            options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#888' }} }}, y: {{ grid: {{ color: 'rgba(255,255,255,0.05)' }}, ticks: {{ color: '#888', callback: function(value) {{ return value + '%'; }} }} }} }} }}
        }});
    </script>
</body>
</html>'''


def generate_html_report(metrics: Dict[str, Any], daily_returns: Optional[List[float]] = None, title: str = "回测报告") -> str:
    generator = ReportGenerator()
    return generator.generate(metrics, daily_returns, None, title)
