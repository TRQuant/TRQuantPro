"""报告生成模块

基于 BulletTrade 官方 `bullet-trade report` 命令
实现回测和实盘报告生成

官方命令格式:
bullet-trade report --input backtest_results --format html
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
import subprocess
import json
import logging
import os

logger = logging.getLogger(__name__)

# BulletTrade CLI
BT_CLI = "bullet-trade"


@dataclass
class ReportConfig:
    """报告配置
    
    Attributes:
        input_dir: 回测结果目录
        output_dir: 报告输出目录
        format: 报告格式 ('html', 'markdown', 'json')
        title: 报告标题
        include_charts: 是否包含图表
        include_trades: 是否包含交易明细
    """
    input_dir: str
    output_dir: Optional[str] = None
    format: str = "html"
    title: str = "策略回测报告"
    include_charts: bool = True
    include_trades: bool = True
    
    def __post_init__(self):
        if not self.output_dir:
            self.output_dir = f"{self.input_dir}/reports"


@dataclass
class ReportResult:
    """报告生成结果
    
    Attributes:
        success: 是否成功
        report_path: 报告文件路径
        error: 错误信息
    """
    success: bool = False
    report_path: Optional[str] = None
    error: Optional[str] = None


class ReportGenerator:
    """报告生成器
    
    封装 BulletTrade 的报告生成功能
    
    Example:
        >>> config = ReportConfig(
        ...     input_dir="backtest_results/my_strategy",
        ...     format="html"
        ... )
        >>> generator = ReportGenerator(config)
        >>> result = generator.generate()
    """
    
    def __init__(self, config: ReportConfig):
        """初始化报告生成器
        
        Args:
            config: 报告配置
        """
        self.config = config
        self._bt_available = self._check_bt()
    
    def _check_bt(self) -> bool:
        """检查 BulletTrade CLI 是否可用"""
        try:
            result = subprocess.run(
                [BT_CLI, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def generate(self) -> ReportResult:
        """生成报告
        
        Returns:
            报告生成结果
        """
        if self._bt_available:
            return self._generate_with_bt()
        else:
            return self._generate_fallback()
    
    def _generate_with_bt(self) -> ReportResult:
        """使用 BulletTrade CLI 生成报告"""
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        
        cmd = [
            BT_CLI, "report",
            "--input", self.config.input_dir,
            "--format", self.config.format
        ]
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,
                cwd=os.getcwd()
            )
            
            if result.returncode == 0:
                # 查找生成的报告文件
                ext = "html" if self.config.format == "html" else "md"
                report_files = list(Path(self.config.input_dir).glob(f"*.{ext}"))
                
                return ReportResult(
                    success=True,
                    report_path=str(report_files[0]) if report_files else None
                )
            else:
                return ReportResult(
                    success=False,
                    error=result.stderr or "报告生成失败"
                )
        except Exception as e:
            return ReportResult(
                success=False,
                error=str(e)
            )
    
    def _generate_fallback(self) -> ReportResult:
        """回退方案：手动生成报告"""
        try:
            Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
            
            if self.config.format == "html":
                return self._generate_html_report()
            else:
                return self._generate_markdown_report()
        except Exception as e:
            return ReportResult(
                success=False,
                error=str(e)
            )
    
    def _generate_html_report(self) -> ReportResult:
        """生成 HTML 报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"{self.config.output_dir}/report_{timestamp}.html"
        
        # 尝试读取回测结果
        metrics = self._load_metrics()
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.title}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --success: #10b981;
            --danger: #ef4444;
            --bg: #0f172a;
            --card: #1e293b;
            --text: #f8fafc;
            --muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{
            font-size: 2rem;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, var(--primary), #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .metric-card {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .metric-label {{ color: var(--muted); font-size: 0.875rem; }}
        .metric-value {{ font-size: 1.5rem; font-weight: 600; margin-top: 0.5rem; }}
        .positive {{ color: var(--success); }}
        .negative {{ color: var(--danger); }}
        .section {{
            background: var(--card);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .section-title {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 0.75rem; text-align: left; }}
        th {{ color: var(--muted); font-weight: 500; }}
        tr:not(:last-child) {{ border-bottom: 1px solid rgba(255,255,255,0.05); }}
        .footer {{
            text-align: center;
            color: var(--muted);
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 {self.config.title}</h1>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">总收益率</div>
                <div class="metric-value {'positive' if metrics.get('total_return', 0) >= 0 else 'negative'}">
                    {metrics.get('total_return', 0):.2f}%
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">年化收益率</div>
                <div class="metric-value {'positive' if metrics.get('annual_return', 0) >= 0 else 'negative'}">
                    {metrics.get('annual_return', 0):.2f}%
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-label">夏普比率</div>
                <div class="metric-value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">最大回撤</div>
                <div class="metric-value negative">{metrics.get('max_drawdown', 0):.2f}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">胜率</div>
                <div class="metric-value">{metrics.get('win_rate', 0):.2f}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">交易次数</div>
                <div class="metric-value">{metrics.get('total_trades', 0)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2 class="section-title">📈 收益曲线</h2>
            <p style="color: var(--muted);">请使用 BulletTrade 官方报告功能获取完整图表</p>
        </div>
        
        <div class="section">
            <h2 class="section-title">📋 策略配置</h2>
            <table>
                <tr><th>回测区间</th><td>{metrics.get('start_date', '-')} ~ {metrics.get('end_date', '-')}</td></tr>
                <tr><th>初始资金</th><td>{metrics.get('initial_cash', 1000000):,.0f}</td></tr>
                <tr><th>基准指数</th><td>{metrics.get('benchmark', '000300.XSHG')}</td></tr>
            </table>
        </div>
        
        <div class="footer">
            <p>由 TRQuant + BulletTrade 生成</p>
            <p>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return ReportResult(
            success=True,
            report_path=report_path
        )
    
    def _generate_markdown_report(self) -> ReportResult:
        """生成 Markdown 报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f"{self.config.output_dir}/report_{timestamp}.md"
        
        metrics = self._load_metrics()
        
        md_content = f"""# {self.config.title}

## 📊 绩效概览

| 指标 | 数值 |
|------|------|
| 总收益率 | {metrics.get('total_return', 0):.2f}% |
| 年化收益率 | {metrics.get('annual_return', 0):.2f}% |
| 夏普比率 | {metrics.get('sharpe_ratio', 0):.2f} |
| 最大回撤 | {metrics.get('max_drawdown', 0):.2f}% |
| 胜率 | {metrics.get('win_rate', 0):.2f}% |
| 交易次数 | {metrics.get('total_trades', 0)} |

## 📋 策略配置

- **回测区间**：{metrics.get('start_date', '-')} ~ {metrics.get('end_date', '-')}
- **初始资金**：{metrics.get('initial_cash', 1000000):,.0f}
- **基准指数**：{metrics.get('benchmark', '000300.XSHG')}

## 📈 收益曲线

> 请使用 BulletTrade 官方报告功能获取完整图表

---

*由 TRQuant + BulletTrade 生成*
*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        return ReportResult(
            success=True,
            report_path=report_path
        )
    
    def _load_metrics(self) -> Dict[str, Any]:
        """加载回测指标"""
        metrics = {
            "total_return": 0,
            "annual_return": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0,
            "win_rate": 0,
            "total_trades": 0,
            "start_date": "-",
            "end_date": "-",
            "initial_cash": 1000000,
            "benchmark": "000300.XSHG"
        }
        
        # 尝试读取结果文件
        result_files = [
            Path(self.config.input_dir) / "metrics.json",
            Path(self.config.input_dir) / "result.json",
            Path(self.config.input_dir) / "summary.json"
        ]
        
        for f in result_files:
            if f.exists():
                try:
                    with open(f, 'r', encoding='utf-8') as fp:
                        data = json.load(fp)
                        metrics.update(data)
                        break
                except Exception:
                    continue
        
        return metrics


def generate_report(
    input_dir: str,
    output_format: str = "html",
    title: str = "策略回测报告"
) -> ReportResult:
    """生成报告便捷函数
    
    Args:
        input_dir: 回测结果目录
        output_format: 报告格式 ('html', 'markdown')
        title: 报告标题
        
    Returns:
        报告生成结果
        
    Example:
        >>> result = generate_report("backtest_results/my_strategy")
        >>> print(result.report_path)
    """
    config = ReportConfig(
        input_dir=input_dir,
        format=output_format,
        title=title
    )
    
    generator = ReportGenerator(config)
    return generator.generate()



