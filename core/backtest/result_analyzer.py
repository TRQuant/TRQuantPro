# -*- coding: utf-8 -*-
"""
回测结果分析器
==============
增强功能：
1. 集成 BulletTrade HTML 报告系统
2. 净值曲线图表生成
3. PDF报告生成
4. 结果对比分析
5. 风险指标深度分析
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ChartConfig:
    """图表配置"""
    width: int = 12
    height: int = 8
    dpi: int = 100
    style: str = "seaborn-v0_8-darkgrid"
    colors: Dict[str, str] = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "equity": "#2196F3",
                "benchmark": "#9E9E9E",
                "drawdown": "#F44336",
                "profit": "#4CAF50",
                "loss": "#F44336",
            }


class BacktestResultAnalyzer:
    """回测结果分析器 - 集成 BulletTrade 报告系统"""
    
    def __init__(self, output_dir: str = "output/backtest_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.chart_config = ChartConfig()
        self._plt = None
        self._matplotlib_available = False
        self._bt_report_available = False
        self._check_dependencies()
    
    def _check_dependencies(self):
        """检查依赖"""
        # 检查 matplotlib
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            self._plt = plt
            self._matplotlib_available = True
            logger.info("✅ Matplotlib可用")
        except ImportError:
            logger.warning("⚠️ Matplotlib未安装")
        
        # 检查 BulletTrade 报告模块
        try:
            import sys
            from pathlib import Path as P
            ext_venv = P(__file__).parent.parent.parent / "extension" / "venv" / "lib" / "python3.12" / "site-packages"
            if ext_venv.exists() and str(ext_venv) not in sys.path:
                sys.path.insert(0, str(ext_venv))
            
            from bullet_trade.core.analysis import generate_report
            self._bt_generate_report = generate_report
            self._bt_report_available = True
            logger.info("✅ BulletTrade报告系统可用")
        except ImportError:
            logger.warning("⚠️ BulletTrade报告系统不可用")
    
    # ==================== BulletTrade 报告集成 ====================
    
    def generate_bt_report(
        self,
        bt_result,  # BTResult
        output_dir: str = None,
        gen_html: bool = True,
        gen_csv: bool = True,
        gen_images: bool = True
    ) -> Dict[str, str]:
        """
        使用 BulletTrade 原生系统生成报告
        
        Args:
            bt_result: BTResult 对象
            output_dir: 输出目录
            gen_html: 是否生成HTML
            gen_csv: 是否生成CSV
            gen_images: 是否生成图片
            
        Returns:
            报告文件路径字典
        """
        output_dir = Path(output_dir or self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        paths = {}
        
        # 如果已有 BulletTrade 生成的报告，直接使用
        if hasattr(bt_result, 'report_path') and bt_result.report_path:
            if os.path.exists(bt_result.report_path):
                paths["html_report"] = bt_result.report_path
                logger.info(f"✅ 使用已有 BulletTrade 报告: {bt_result.report_path}")
                return paths
        
        # 使用 BulletTrade 报告生成器
        if self._bt_report_available and hasattr(bt_result, 'raw_results') and bt_result.raw_results:
            try:
                self._bt_generate_report(
                    bt_result.raw_results,
                    output_dir=str(output_dir),
                    gen_html=gen_html,
                    gen_csv=gen_csv,
                    gen_images=gen_images,
                )
                
                if gen_html:
                    paths["html_report"] = str(output_dir / "report.html")
                if gen_csv:
                    paths["csv_report"] = str(output_dir / "daily_records.csv")
                if gen_images:
                    paths["images_dir"] = str(output_dir / "images")
                
                logger.info(f"✅ BulletTrade 报告已生成: {output_dir}")
                
            except Exception as e:
                logger.warning(f"BulletTrade 报告生成失败: {e}，使用备用报告")
                paths = self._generate_fallback_report(bt_result, output_dir)
        else:
            # 使用备用报告生成
            paths = self._generate_fallback_report(bt_result, output_dir)
        
        return paths
    
    def _generate_fallback_report(self, result, output_dir: Path) -> Dict[str, str]:
        """生成备用报告（当 BulletTrade 不可用时）"""
        paths = {}
        
        # 生成增强 HTML 报告
        html_path = self.generate_enhanced_html_report(result, output_dir)
        if html_path:
            paths["html_report"] = html_path
        
        return paths
    
    # ==================== 增强 HTML 报告 ====================
    
    def generate_enhanced_html_report(
        self,
        result,  # UnifiedBacktestResult or BTResult
        output_dir: Path = None,
        strategy_name: str = "策略"
    ) -> Optional[str]:
        """
        生成增强 HTML 报告（BulletTrade 风格 + 额外分析）
        """
        output_dir = Path(output_dir or self.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        html_path = output_dir / f"{strategy_name}_report_{timestamp}.html"
        
        # 提取指标
        metrics = self._extract_metrics(result)
        risk_metrics = self._calculate_risk_metrics_from_result(result)
        
        # 生成图表（如果可用）
        charts = {}
        if self._matplotlib_available:
            charts = self._generate_charts_for_report(result, strategy_name, output_dir)
        
        # 生成交易记录表格
        trades_html = self._generate_trades_table(result)
        
        # 生成每日持仓表格
        positions_html = self._generate_positions_table(result)
        
        # HTML 模板（BulletTrade 风格）
        html_content = self._render_bt_style_html(
            strategy_name=strategy_name,
            metrics=metrics,
            risk_metrics=risk_metrics,
            charts=charts,
            trades_html=trades_html,
            positions_html=positions_html,
            result=result
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ 增强 HTML 报告已生成: {html_path}")
        return str(html_path)
    
    def _render_bt_style_html(
        self,
        strategy_name: str,
        metrics: Dict,
        risk_metrics: Dict,
        charts: Dict,
        trades_html: str,
        positions_html: str,
        result
    ) -> str:
        """渲染 BulletTrade 风格的 HTML 报告"""
        
        # 图表部分
        charts_section = ""
        for chart_name, chart_path in charts.items():
            if os.path.exists(chart_path):
                rel_path = os.path.basename(chart_path)
                chart_title = {
                    "equity_chart": "📈 净值曲线",
                    "drawdown_chart": "📉 回撤曲线",
                    "returns_distribution": "📊 收益分布",
                    "monthly_heatmap": "📅 月度收益",
                }.get(chart_name, chart_name)
                
                charts_section += f'''
                <div class="chart-section">
                    <h3>{chart_title}</h3>
                    <img src="{rel_path}" alt="{chart_name}">
                </div>
                '''
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{strategy_name} - 回测报告</title>
    <style>
        :root {{
            --primary: #1976D2;
            --success: #4CAF50;
            --danger: #F44336;
            --warning: #FF9800;
            --bg-dark: #1a1a2e;
            --bg-card: #16213e;
            --text-primary: #eee;
            --text-secondary: #aaa;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, var(--bg-dark) 0%, #0f3460 100%);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        /* 头部 */
        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, #0d47a1 100%);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 8px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header .meta {{
            color: rgba(255,255,255,0.8);
            font-size: 0.9rem;
        }}
        
        /* 核心指标卡片 */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        
        .metric-card {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .metric-label {{
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        .positive {{ color: var(--success); }}
        .negative {{ color: var(--danger); }}
        .neutral {{ color: var(--warning); }}
        
        /* 区块 */
        .section {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        }}
        
        .section h2 {{
            font-size: 1.3rem;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--primary);
        }}
        
        /* 表格 */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        th {{
            background: rgba(25, 118, 210, 0.3);
            font-weight: 600;
        }}
        
        tr:hover {{
            background: rgba(255,255,255,0.05);
        }}
        
        /* 图表 */
        .chart-section {{
            margin-bottom: 24px;
        }}
        
        .chart-section h3 {{
            margin-bottom: 12px;
            color: var(--text-secondary);
        }}
        
        .chart-section img {{
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        }}
        
        /* 风险指标网格 */
        .risk-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
        }}
        
        .risk-item {{
            display: flex;
            justify-content: space-between;
            padding: 12px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }}
        
        .risk-item .label {{ color: var(--text-secondary); }}
        .risk-item .value {{ font-weight: 600; }}
        
        /* 页脚 */
        .footer {{
            text-align: center;
            padding: 24px;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}
        
        /* 响应式 */
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .metric-value {{ font-size: 1.5rem; }}
            .metrics-grid {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <h1>📊 {strategy_name}</h1>
            <div class="meta">
                回测报告 | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                回测区间: {metrics.get('start_date', 'N/A')} ~ {metrics.get('end_date', 'N/A')}
            </div>
        </div>
        
        <!-- 核心指标 -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value {'positive' if metrics.get('total_return', 0) >= 0 else 'negative'}">
                    {metrics.get('total_return', 0):.2f}%
                </div>
                <div class="metric-label">总收益率</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if metrics.get('annual_return', 0) >= 0 else 'negative'}">
                    {metrics.get('annual_return', 0):.2f}%
                </div>
                <div class="metric-label">年化收益率</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'positive' if metrics.get('sharpe_ratio', 0) >= 1 else 'neutral' if metrics.get('sharpe_ratio', 0) >= 0 else 'negative'}">
                    {metrics.get('sharpe_ratio', 0):.2f}
                </div>
                <div class="metric-label">夏普比率</div>
            </div>
            <div class="metric-card">
                <div class="metric-value negative">
                    {abs(metrics.get('max_drawdown', 0)):.2f}%
                </div>
                <div class="metric-label">最大回撤</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">
                    {metrics.get('win_rate', 0):.1f}%
                </div>
                <div class="metric-label">胜率</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">
                    {metrics.get('total_trades', 0)}
                </div>
                <div class="metric-label">交易次数</div>
            </div>
        </div>
        
        <!-- 资金信息 -->
        <div class="section">
            <h2>💰 资金信息</h2>
            <div class="risk-grid">
                <div class="risk-item">
                    <span class="label">初始资金</span>
                    <span class="value">¥{metrics.get('initial_capital', 0):,.2f}</span>
                </div>
                <div class="risk-item">
                    <span class="label">最终资金</span>
                    <span class="value">¥{metrics.get('final_capital', 0):,.2f}</span>
                </div>
                <div class="risk-item">
                    <span class="label">盈亏金额</span>
                    <span class="value {'positive' if metrics.get('final_capital', 0) >= metrics.get('initial_capital', 0) else 'negative'}">
                        ¥{metrics.get('final_capital', 0) - metrics.get('initial_capital', 0):,.2f}
                    </span>
                </div>
                <div class="risk-item">
                    <span class="label">交易天数</span>
                    <span class="value">{metrics.get('trading_days', 0)}</span>
                </div>
            </div>
        </div>
        
        <!-- 风险指标 -->
        <div class="section">
            <h2>⚠️ 风险分析</h2>
            <div class="risk-grid">
                <div class="risk-item">
                    <span class="label">年化波动率</span>
                    <span class="value">{risk_metrics.get('annual_volatility', 0) * 100:.2f}%</span>
                </div>
                <div class="risk-item">
                    <span class="label">下行波动率</span>
                    <span class="value">{risk_metrics.get('downside_volatility', 0) * 100:.2f}%</span>
                </div>
                <div class="risk-item">
                    <span class="label">VaR (95%)</span>
                    <span class="value">{risk_metrics.get('var_95', 0) * 100:.2f}%</span>
                </div>
                <div class="risk-item">
                    <span class="label">VaR (99%)</span>
                    <span class="value">{risk_metrics.get('var_99', 0) * 100:.2f}%</span>
                </div>
                <div class="risk-item">
                    <span class="label">最大连续亏损</span>
                    <span class="value">{risk_metrics.get('max_losing_streak', 0)} 天</span>
                </div>
                <div class="risk-item">
                    <span class="label">卡尔玛比率</span>
                    <span class="value">{metrics.get('calmar_ratio', 0):.2f}</span>
                </div>
                <div class="risk-item">
                    <span class="label">最佳单日</span>
                    <span class="value positive">{risk_metrics.get('best_day', 0) * 100:.2f}%</span>
                </div>
                <div class="risk-item">
                    <span class="label">最差单日</span>
                    <span class="value negative">{risk_metrics.get('worst_day', 0) * 100:.2f}%</span>
                </div>
            </div>
        </div>
        
        <!-- 图表 -->
        {f'<div class="section"><h2>📈 绩效图表</h2>{charts_section}</div>' if charts_section else ''}
        
        <!-- 交易记录 -->
        {f'<div class="section"><h2>📝 交易记录</h2>{trades_html}</div>' if trades_html else ''}
        
        <!-- 持仓记录 -->
        {f'<div class="section"><h2>📦 持仓记录</h2>{positions_html}</div>' if positions_html else ''}
        
        <!-- 页脚 -->
        <div class="footer">
            <p>TRQuant 韬睿量化系统 | BacktestResultAnalyzer (集成 BulletTrade)</p>
            <p>引擎: {getattr(result, 'engine_used', 'N/A')} | 耗时: {getattr(result, 'duration_seconds', getattr(result, 'runtime_seconds', 0)):.2f}秒</p>
        </div>
    </div>
</body>
</html>
'''
    
    def _extract_metrics(self, result) -> Dict[str, Any]:
        """从结果中提取指标"""
        metrics = {}
        
        # UnifiedBacktestResult
        if hasattr(result, 'total_return'):
            metrics['total_return'] = result.total_return * 100 if result.total_return < 10 else result.total_return
        if hasattr(result, 'annual_return'):
            metrics['annual_return'] = result.annual_return * 100 if result.annual_return < 10 else result.annual_return
        if hasattr(result, 'sharpe_ratio'):
            metrics['sharpe_ratio'] = result.sharpe_ratio
        if hasattr(result, 'max_drawdown'):
            metrics['max_drawdown'] = abs(result.max_drawdown) * 100 if abs(result.max_drawdown) < 1 else abs(result.max_drawdown)
        if hasattr(result, 'win_rate'):
            metrics['win_rate'] = result.win_rate * 100 if result.win_rate < 1 else result.win_rate
        if hasattr(result, 'total_trades'):
            metrics['total_trades'] = result.total_trades
        if hasattr(result, 'calmar_ratio'):
            metrics['calmar_ratio'] = result.calmar_ratio
        
        # BTResult 特有字段
        if hasattr(result, 'initial_capital'):
            metrics['initial_capital'] = result.initial_capital
        if hasattr(result, 'final_capital'):
            metrics['final_capital'] = result.final_capital
        if hasattr(result, 'trading_days'):
            metrics['trading_days'] = result.trading_days
        if hasattr(result, 'start_date'):
            metrics['start_date'] = result.start_date
        if hasattr(result, 'end_date'):
            metrics['end_date'] = result.end_date
        
        # 从 config 获取
        if hasattr(result, 'config') and result.config:
            if not metrics.get('initial_capital'):
                metrics['initial_capital'] = getattr(result.config, 'initial_capital', 1000000)
            if not metrics.get('start_date'):
                metrics['start_date'] = getattr(result.config, 'start_date', 'N/A')
            if not metrics.get('end_date'):
                metrics['end_date'] = getattr(result.config, 'end_date', 'N/A')
        
        # 计算最终资金（如果没有）
        if not metrics.get('final_capital') and metrics.get('initial_capital') and metrics.get('total_return'):
            metrics['final_capital'] = metrics['initial_capital'] * (1 + metrics['total_return'] / 100)
        
        return metrics
    
    def _calculate_risk_metrics_from_result(self, result) -> Dict[str, float]:
        """从结果计算风险指标"""
        risk_metrics = {
            'annual_volatility': 0,
            'downside_volatility': 0,
            'var_95': 0,
            'var_99': 0,
            'max_losing_streak': 0,
            'best_day': 0,
            'worst_day': 0,
        }
        
        # 从 daily_returns 计算
        daily_returns = None
        if hasattr(result, 'daily_returns') and result.daily_returns is not None:
            daily_returns = result.daily_returns
        elif hasattr(result, 'daily_records') and result.daily_records is not None:
            # BTResult 的 daily_records
            df = result.daily_records
            if hasattr(df, 'pct_change'):
                daily_returns = df['total_value'].pct_change().dropna() if 'total_value' in df.columns else None
        
        if daily_returns is not None and len(daily_returns) > 0:
            risk_metrics['annual_volatility'] = float(daily_returns.std() * np.sqrt(252))
            
            downside = daily_returns[daily_returns < 0]
            if len(downside) > 0:
                risk_metrics['downside_volatility'] = float(downside.std() * np.sqrt(252))
            
            risk_metrics['var_95'] = float(daily_returns.quantile(0.05))
            risk_metrics['var_99'] = float(daily_returns.quantile(0.01))
            risk_metrics['best_day'] = float(daily_returns.max())
            risk_metrics['worst_day'] = float(daily_returns.min())
            
            # 连续亏损
            streak = self._calculate_losing_streak(daily_returns)
            risk_metrics['max_losing_streak'] = streak['max_streak']
        
        return risk_metrics
    
    def _calculate_losing_streak(self, daily_returns: pd.Series) -> Dict[str, float]:
        """计算连续亏损统计"""
        is_loss = daily_returns < 0
        streaks = []
        current = 0
        
        for loss in is_loss:
            if loss:
                current += 1
            else:
                if current > 0:
                    streaks.append(current)
                current = 0
        
        if current > 0:
            streaks.append(current)
        
        if streaks:
            return {'max_streak': max(streaks), 'avg_streak': sum(streaks) / len(streaks)}
        return {'max_streak': 0, 'avg_streak': 0}
    
    def _generate_charts_for_report(self, result, strategy_name: str, output_dir: Path) -> Dict[str, str]:
        """为报告生成图表"""
        charts = {}
        
        if not self._matplotlib_available:
            return charts
        
        plt = self._plt
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 1. 净值曲线
        equity_curve = None
        if hasattr(result, 'equity_curve') and result.equity_curve is not None:
            equity_curve = result.equity_curve
        elif hasattr(result, 'daily_records') and result.daily_records is not None:
            df = result.daily_records
            if 'total_value' in df.columns:
                equity_curve = df['total_value'] / df['total_value'].iloc[0]
        
        if equity_curve is not None:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(equity_curve.values, color='#2196F3', linewidth=2)
            ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
            ax.set_title(f'{strategy_name} - 净值曲线', fontsize=14)
            ax.set_xlabel('交易日')
            ax.set_ylabel('净值')
            ax.grid(True, alpha=0.3)
            ax.fill_between(range(len(equity_curve)), 1, equity_curve.values, 
                           where=equity_curve.values >= 1, color='#4CAF50', alpha=0.3)
            ax.fill_between(range(len(equity_curve)), 1, equity_curve.values, 
                           where=equity_curve.values < 1, color='#F44336', alpha=0.3)
            
            path = output_dir / f'{strategy_name}_equity_{timestamp}.png'
            plt.savefig(path, dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close(fig)
            charts['equity_chart'] = str(path)
        
        # 2. 回撤曲线
        drawdown_curve = None
        if hasattr(result, 'drawdown_curve') and result.drawdown_curve is not None:
            drawdown_curve = result.drawdown_curve
        elif equity_curve is not None:
            running_max = equity_curve.cummax()
            drawdown_curve = (equity_curve - running_max) / running_max
        
        if drawdown_curve is not None:
            fig, ax = plt.subplots(figsize=(12, 4))
            ax.fill_between(range(len(drawdown_curve)), drawdown_curve.values * 100, 0, 
                           color='#F44336', alpha=0.5)
            ax.plot(drawdown_curve.values * 100, color='#F44336', linewidth=1)
            ax.set_title(f'{strategy_name} - 回撤曲线', fontsize=14)
            ax.set_xlabel('交易日')
            ax.set_ylabel('回撤 (%)')
            ax.grid(True, alpha=0.3)
            
            path = output_dir / f'{strategy_name}_drawdown_{timestamp}.png'
            plt.savefig(path, dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close(fig)
            charts['drawdown_chart'] = str(path)
        
        # 3. 收益分布
        daily_returns = None
        if hasattr(result, 'daily_returns') and result.daily_returns is not None:
            daily_returns = result.daily_returns
        elif equity_curve is not None:
            daily_returns = equity_curve.pct_change().dropna()
        
        if daily_returns is not None and len(daily_returns) > 10:
            fig, ax = plt.subplots(figsize=(10, 5))
            n, bins, patches = ax.hist(daily_returns.values * 100, bins=50, 
                                        edgecolor='white', alpha=0.7)
            for i, patch in enumerate(patches):
                if bins[i] < 0:
                    patch.set_facecolor('#F44336')
                else:
                    patch.set_facecolor('#4CAF50')
            
            mean_ret = daily_returns.mean() * 100
            ax.axvline(mean_ret, color='blue', linestyle='--', linewidth=2, label=f'均值: {mean_ret:.2f}%')
            ax.set_title(f'{strategy_name} - 日收益分布', fontsize=14)
            ax.set_xlabel('日收益率 (%)')
            ax.set_ylabel('频次')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            path = output_dir / f'{strategy_name}_returns_{timestamp}.png'
            plt.savefig(path, dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
            plt.close(fig)
            charts['returns_distribution'] = str(path)
        
        return charts
    
    def _generate_trades_table(self, result) -> str:
        """生成交易记录表格 HTML"""
        trades = None
        if hasattr(result, 'trades') and result.trades is not None:
            trades = result.trades
        
        if trades is None or (isinstance(trades, list) and len(trades) == 0):
            return ""
        
        if isinstance(trades, pd.DataFrame):
            # 限制显示前50条
            trades_display = trades.head(50)
            html = '<div style="overflow-x: auto;"><table>'
            html += '<tr>' + ''.join(f'<th>{col}</th>' for col in trades_display.columns) + '</tr>'
            for _, row in trades_display.iterrows():
                html += '<tr>' + ''.join(f'<td>{val}</td>' for val in row.values) + '</tr>'
            html += '</table></div>'
            if len(trades) > 50:
                html += f'<p style="color: #aaa;">... 共 {len(trades)} 条交易记录，仅显示前50条</p>'
            return html
        elif isinstance(trades, list) and len(trades) > 0:
            # 列表格式
            trades_display = trades[:50]
            if isinstance(trades_display[0], dict):
                keys = trades_display[0].keys()
                html = '<div style="overflow-x: auto;"><table>'
                html += '<tr>' + ''.join(f'<th>{k}</th>' for k in keys) + '</tr>'
                for t in trades_display:
                    html += '<tr>' + ''.join(f'<td>{t.get(k, "")}</td>' for k in keys) + '</tr>'
                html += '</table></div>'
                if len(trades) > 50:
                    html += f'<p style="color: #aaa;">... 共 {len(trades)} 条交易记录，仅显示前50条</p>'
                return html
        
        return ""
    
    def _generate_positions_table(self, result) -> str:
        """生成持仓记录表格 HTML"""
        positions = None
        if hasattr(result, 'daily_positions') and result.daily_positions is not None:
            positions = result.daily_positions
        
        if positions is None:
            return ""
        
        if isinstance(positions, pd.DataFrame) and len(positions) > 0:
            positions_display = positions.tail(20)  # 显示最后20天
            html = '<div style="overflow-x: auto;"><table>'
            html += '<tr>' + ''.join(f'<th>{col}</th>' for col in positions_display.columns) + '</tr>'
            for _, row in positions_display.iterrows():
                html += '<tr>' + ''.join(f'<td>{val}</td>' for val in row.values) + '</tr>'
            html += '</table></div>'
            html += f'<p style="color: #aaa;">显示最近20天持仓，共 {len(positions)} 条记录</p>'
            return html
        
        return ""
    
    # ==================== 结果对比 ====================
    
    def compare_strategies(
        self,
        results: Dict[str, Any],
        save_comparison: bool = True
    ) -> Tuple[pd.DataFrame, Optional[str]]:
        """对比多个策略结果"""
        comparison_data = []
        
        for name, result in results.items():
            metrics = self._extract_metrics(result)
            if metrics:
                comparison_data.append({
                    "策略": name,
                    "总收益%": metrics.get('total_return', 0),
                    "年化收益%": metrics.get('annual_return', 0),
                    "夏普比率": metrics.get('sharpe_ratio', 0),
                    "最大回撤%": metrics.get('max_drawdown', 0),
                    "胜率%": metrics.get('win_rate', 0),
                    "交易次数": metrics.get('total_trades', 0),
                })
        
        df = pd.DataFrame(comparison_data)
        
        chart_path = None
        if save_comparison and self._matplotlib_available and len(comparison_data) > 1:
            chart_path = self._generate_comparison_chart(results)
        
        return df, chart_path
    
    def _generate_comparison_chart(self, results: Dict[str, Any]) -> Optional[str]:
        """生成策略对比图"""
        if not self._matplotlib_available:
            return None
        
        plt = self._plt
        
        equity_curves = {}
        for name, result in results.items():
            if hasattr(result, 'equity_curve') and result.equity_curve is not None:
                equity_curves[name] = result.equity_curve
            elif hasattr(result, 'daily_records') and result.daily_records is not None:
                df = result.daily_records
                if 'total_value' in df.columns:
                    equity_curves[name] = df['total_value'] / df['total_value'].iloc[0]
        
        if len(equity_curves) < 2:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.tab10(range(len(equity_curves)))
        
        for (name, curve), color in zip(equity_curves.items(), colors):
            ax.plot(curve.values, label=name, linewidth=2, color=color)
        
        ax.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
        ax.set_title("策略净值对比", fontsize=14)
        ax.set_xlabel("交易日")
        ax.set_ylabel("净值")
        ax.legend(loc="upper left")
        ax.grid(True, alpha=0.3)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = self.output_dir / f"comparison_{timestamp}.png"
        plt.savefig(path, dpi=100, bbox_inches='tight', facecolor='#1a1a2e')
        plt.close(fig)
        
        logger.info(f"✅ 策略对比图已保存: {path}")
        return str(path)


# ==================== 便捷函数 ====================

def analyze_backtest_result(
    result,
    strategy_name: str = "策略",
    output_format: str = "html",
    output_dir: str = None
) -> Dict[str, Any]:
    """
    分析回测结果并生成报告
    
    Args:
        result: UnifiedBacktestResult 或 BTResult
        strategy_name: 策略名称
        output_format: 输出格式 (html/bt)
        output_dir: 输出目录
        
    Returns:
        分析结果字典
    """
    analyzer = BacktestResultAnalyzer(output_dir or "output/backtest_reports")
    
    output = {
        "success": True,
        "report_path": None,
        "charts": {},
    }
    
    # 判断结果类型
    is_bt_result = hasattr(result, 'raw_results') or hasattr(result, 'report_path')
    
    if output_format == "bt" and is_bt_result:
        # 使用 BulletTrade 报告系统
        paths = analyzer.generate_bt_report(result)
        output["report_path"] = paths.get("html_report")
    else:
        # 使用增强 HTML 报告
        output["report_path"] = analyzer.generate_enhanced_html_report(
            result, 
            output_dir=output_dir,
            strategy_name=strategy_name
        )
    
    return output


__all__ = [
    "BacktestResultAnalyzer",
    "ChartConfig",
    "analyze_backtest_result",
]
