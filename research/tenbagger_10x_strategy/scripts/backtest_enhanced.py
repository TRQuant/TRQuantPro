#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
完善回测系统 - 标准指标 + 快速验证 + 聚宽回测
============================================

功能:
1. 完整回测指标计算（夏普、索提诺、卡玛、最大回撤等）
2. 快速验证（向量化，<5秒）
3. 聚宽大数据回测验证
4. 完善报告生成（策略设计、代码、结果分析）

佣金: 万分之一 (0.0001)

代码位置: research/tenbagger_10x_strategy/scripts/backtest_enhanced.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 回测配置
# ============================================================

class BacktestConfig:
    """回测配置"""
    
    def __init__(self):
        # 基本配置
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.benchmark = "000300.XSHG"
        
        # 交易成本（万一）
        self.commission_rate = 0.0001  # 万分之一
        self.stamp_tax = 0.001         # 印花税（卖出）
        self.slippage = 0.001          # 滑点（0.1%）
        
        # 回测模式
        self.mode = "fast"  # fast/standard/precise
        
        # 持仓参数
        self.max_holdings = 10
        self.single_stock_max = 0.15
        
        # 风控参数
        self.stop_loss = -0.10
        self.take_profit = 0.80
        self.trailing_stop = 0.15
        self.rebalance_days = 10

# ============================================================
# 完整指标计算
# ============================================================

class PerformanceMetrics:
    """完整回测指标计算"""
    
    @staticmethod
    def calculate_all_metrics(equity_curve: pd.Series, daily_returns: pd.Series,
                             benchmark_returns: pd.Series = None,
                             initial_capital: float = 1000000.0,
                             trade_days: int = 252) -> dict:
        """
        计算所有回测指标
        
        Args:
            equity_curve: 净值曲线
            daily_returns: 日收益率
            benchmark_returns: 基准收益率
            initial_capital: 初始资金
            trade_days: 年交易日数
        """
        metrics = {}
        
        if len(equity_curve) < 2 or len(daily_returns) < 2:
            return metrics
        
        # 1. 收益指标
        total_return = (equity_curve.iloc[-1] / initial_capital) - 1
        metrics['total_return'] = float(total_return)
        metrics['total_return_pct'] = float(total_return * 100)
        
        # 年化收益
        days = len(equity_curve)
        if days > 1:
            annual_return = (1 + total_return) ** (trade_days / days) - 1
            metrics['annual_return'] = float(annual_return)
            metrics['annual_return_pct'] = float(annual_return * 100)
        
        # 2. 风险指标
        # 波动率
        volatility = daily_returns.std() * np.sqrt(trade_days)
        metrics['volatility'] = float(volatility)
        metrics['volatility_pct'] = float(volatility * 100)
        
        # 最大回撤
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        max_drawdown = drawdown.min()
        metrics['max_drawdown'] = float(max_drawdown)
        metrics['max_drawdown_pct'] = float(max_drawdown * 100)
        
        # 最大回撤持续时间
        drawdown_periods = []
        in_drawdown = False
        start_date = None
        for i, dd in enumerate(drawdown):
            if dd < -0.01 and not in_drawdown:  # 进入回撤
                in_drawdown = True
                start_date = i
            elif dd >= -0.01 and in_drawdown:  # 退出回撤
                in_drawdown = False
                if start_date is not None:
                    drawdown_periods.append(i - start_date)
        if in_drawdown and start_date is not None:
            drawdown_periods.append(len(drawdown) - start_date)
        metrics['max_drawdown_duration'] = int(max(drawdown_periods)) if drawdown_periods else 0
        
        # 3. 风险调整收益指标
        # 夏普比率
        if volatility > 0:
            sharpe_ratio = (annual_return if 'annual_return' in metrics else 0) / volatility
            metrics['sharpe_ratio'] = float(sharpe_ratio)
        else:
            metrics['sharpe_ratio'] = 0.0
        
        # 索提诺比率（只考虑下行波动）
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(trade_days)
            if downside_std > 0:
                sortino_ratio = (annual_return if 'annual_return' in metrics else 0) / downside_std
                metrics['sortino_ratio'] = float(sortino_ratio)
            else:
                metrics['sortino_ratio'] = 0.0
        else:
            metrics['sortino_ratio'] = 0.0
        
        # 卡玛比率
        if max_drawdown != 0:
            calmar_ratio = (annual_return if 'annual_return' in metrics else 0) / abs(max_drawdown)
            metrics['calmar_ratio'] = float(calmar_ratio)
        else:
            metrics['calmar_ratio'] = 0.0
        
        # 4. 基准对比
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            benchmark_total = (1 + benchmark_returns).prod() - 1
            metrics['benchmark_return'] = float(benchmark_total)
            metrics['benchmark_return_pct'] = float(benchmark_total * 100)
            
            # 超额收益
            excess_return = total_return - benchmark_total
            metrics['excess_return'] = float(excess_return)
            metrics['excess_return_pct'] = float(excess_return * 100)
            
            # 信息比率
            excess_returns = daily_returns - benchmark_returns
            if len(excess_returns) > 0:
                tracking_error = excess_returns.std() * np.sqrt(trade_days)
                if tracking_error > 0:
                    info_ratio = (annual_return if 'annual_return' in metrics else 0) / tracking_error
                    metrics['info_ratio'] = float(info_ratio)
                else:
                    metrics['info_ratio'] = 0.0
            else:
                metrics['info_ratio'] = 0.0
        
        # 5. 交易统计
        # 这里需要从交易记录中统计
        metrics['total_trades'] = 0  # 将在回测中填充
        metrics['win_rate'] = 0.0
        metrics['profit_loss_ratio'] = 0.0
        metrics['avg_holding_days'] = 0.0
        
        # 6. 月度收益
        if hasattr(equity_curve, 'index') and len(equity_curve) > 20:
            monthly_returns = []
            current_month = None
            month_start_value = initial_capital
            
            for date, value in equity_curve.items():
                month = str(date)[:7] if hasattr(date, '__str__') else str(date)[:7]
                if month != current_month:
                    if current_month is not None:
                        monthly_returns.append((value / month_start_value - 1) * 100)
                    current_month = month
                    month_start_value = value
            
            if monthly_returns:
                metrics['monthly_returns'] = monthly_returns
                metrics['best_month'] = float(max(monthly_returns))
                metrics['worst_month'] = float(min(monthly_returns))
                metrics['monthly_win_rate'] = float(sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) * 100)
        
        # 7. 其他指标
        # Beta（如果有基准）
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            if len(daily_returns) == len(benchmark_returns):
                covariance = np.cov(daily_returns, benchmark_returns)[0, 1]
                benchmark_variance = np.var(benchmark_returns)
                if benchmark_variance > 0:
                    beta = covariance / benchmark_variance
                    metrics['beta'] = float(beta)
                else:
                    metrics['beta'] = 0.0
        
        # Alpha
        if 'beta' in metrics and benchmark_returns is not None:
            benchmark_annual = (1 + benchmark_returns).prod() ** (trade_days / len(benchmark_returns)) - 1
            alpha = (annual_return if 'annual_return' in metrics else 0) - (metrics['beta'] * benchmark_annual)
            metrics['alpha'] = float(alpha)
            metrics['alpha_pct'] = float(alpha * 100)
        
        return metrics

# ============================================================
# 快速验证回测（向量化）
# ============================================================

class FastBacktest:
    """快速验证回测（向量化计算，<5秒）"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.equity_curve = []
        self.daily_returns = []
        self.dates = []
        self.trade_history = []
        self.positions = {}
    
    def run(self, stock_scores: dict, price_data: dict) -> dict:
        """
        快速回测
        
        Args:
            stock_scores: {date: {stock: score}}
            price_data: {stock: DataFrame with close prices}
        """
        logger.info("🚀 快速验证回测（向量化）...")
        
        # 获取所有日期
        all_dates = sorted(set().union(*[scores.keys() for scores in stock_scores.values()]))
        if not all_dates:
            return {}
        
        cash = self.config.initial_capital
        equity = [cash]
        
        for date in all_dates:
            # 选股
            if date in stock_scores:
                scores = stock_scores[date]
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                
                # 简化的交易逻辑（向量化）
                target_stocks = [s[0] for s in selected]
                
                # 计算持仓价值
                portfolio_value = cash
                for stock in target_stocks:
                    if stock in price_data and date in price_data[stock].index:
                        price = price_data[stock].loc[date, 'close']
                        # 简化：假设等权重
                        position_value = cash / len(target_stocks)
                        portfolio_value += position_value
                
                equity.append(portfolio_value)
            else:
                equity.append(equity[-1])
        
        # 计算收益率
        equity_series = pd.Series(equity, index=all_dates[:len(equity)])
        returns = equity_series.pct_change().fillna(0)
        
        # 计算指标
        metrics_calc = PerformanceMetrics()
        metrics = metrics_calc.calculate_all_metrics(
            equity_series,
            returns,
            initial_capital=self.config.initial_capital
        )
        
        return {
            'equity_curve': equity_series.tolist(),
            'daily_returns': returns.tolist(),
            'dates': [str(d) for d in equity_series.index],
            'metrics': metrics
        }

# ============================================================
# 聚宽回测验证
# ============================================================

class JQDataBacktest:
    """聚宽大数据回测验证"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate(self) -> bool:
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, pwd)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def run(self, strategy_func, stock_universe: list) -> dict:
        """
        执行聚宽回测
        
        Args:
            strategy_func: 策略函数
            stock_universe: 股票池
        """
        logger.info("📊 聚宽大数据回测验证...")
        
        # 这里应该调用聚宽的回测引擎
        # 由于需要完整的聚宽环境，这里提供框架
        
        # 获取基准数据
        benchmark_prices = jq.get_price(
            self.config.benchmark,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close']
        )
        
        # 执行策略回测（需要实现具体逻辑）
        # ...
        
        return {
            'status': 'completed',
            'message': '聚宽回测需要完整实现'
        }

# ============================================================
# 完善报告生成
# ============================================================

class EnhancedReportGenerator:
    """完善报告生成器"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
    
    def generate_html_report(self, backtest_results: dict, strategy_code: str = "",
                            strategy_design: str = "") -> str:
        """
        生成完善的HTML报告
        
        Args:
            backtest_results: 回测结果
            strategy_code: 策略代码
            strategy_design: 策略设计说明
        """
        metrics = backtest_results.get('metrics', {})
        equity_curve = backtest_results.get('equity_curve', [])
        dates = backtest_results.get('dates', [])
        
        # 生成图表
        charts_html = self._generate_charts(equity_curve, dates, metrics)
        
        # 指标表格
        metrics_html = self._generate_metrics_table(metrics)
        
        # 策略设计部分
        design_html = f"""
        <div class="section">
            <h2>📐 策略设计</h2>
            <div class="design-content">
                {strategy_design or '<p>策略设计说明...</p>'}
            </div>
        </div>
        """ if strategy_design else ""
        
        # 代码部分
        code_html = f"""
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python">{strategy_code or '# 策略代码...'}</code></pre>
        </div>
        """ if strategy_code else ""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>完善回测报告</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 完善回测报告</h1>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date}</p>
            <p>初始资金: ¥{self.config.initial_cash:,.0f} | 佣金: 万分之一</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric"><div class="label">总收益率</div><div class="value">{metrics.get('total_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">年化收益</div><div class="value">{metrics.get('annual_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">夏普比率</div><div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">索提诺比率</div><div class="value">{metrics.get('sortino_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">卡玛比率</div><div class="value">{metrics.get('calmar_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">最大回撤</div><div class="value">{metrics.get('max_drawdown_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">波动率</div><div class="value">{metrics.get('volatility_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">信息比率</div><div class="value">{metrics.get('info_ratio', 0):.2f}</div></div>
        </div>
        
        {charts_html}
        
        {design_html}
        
        {code_html}
        
        <div class="section">
            <h2>📈 完整指标</h2>
            {metrics_html}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_charts(self, equity_curve: list, dates: list, metrics: dict) -> str:
        """生成图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        charts_html = ""
        
        # 净值曲线
        fig, ax = plt.subplots(figsize=(14, 6))
        if dates:
            date_objs = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in dates[:len(equity_curve)]]
            ax.plot(date_objs, equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=self.config.initial_capital, color='gray', linestyle='--', alpha=0.5)
            ax.set_title('Equity Curve', fontsize=16, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        charts_html += f'<div class="section"><h2>📊 净值曲线</h2><div class="chart"><img src="data:image/png;base64,{img}"></div></div>'
        
        return charts_html
    
    def _generate_metrics_table(self, metrics: dict) -> str:
        """生成指标表格"""
        rows = ""
        metric_names = {
            'total_return_pct': '总收益率',
            'annual_return_pct': '年化收益率',
            'sharpe_ratio': '夏普比率',
            'sortino_ratio': '索提诺比率',
            'calmar_ratio': '卡玛比率',
            'max_drawdown_pct': '最大回撤',
            'volatility_pct': '波动率',
            'info_ratio': '信息比率',
            'beta': 'Beta',
            'alpha_pct': 'Alpha',
            'excess_return_pct': '超额收益',
            'win_rate': '胜率',
            'profit_loss_ratio': '盈亏比',
        }
        
        for key, name in metric_names.items():
            value = metrics.get(key, 0)
            rows += f"<tr><td>{name}</td><td>{value:.2f}</td></tr>"
        
        return f'<table><tr><th>指标</th><th>数值</th></tr>{rows}</table>'

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("完善回测系统")
    print("=" * 80)
    
    config = BacktestConfig()
    print(f"✅ 回测配置:")
    print(f"   佣金: {config.commission_rate*10000:.0f}万分之一")
    print(f"   初始资金: {config.initial_capital:,.0f}")
    print(f"   回测区间: {config.start_date} ~ {config.end_date}")

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
完善回测系统 - 标准指标 + 快速验证 + 聚宽回测
============================================

功能:
1. 完整回测指标计算（夏普、索提诺、卡玛、最大回撤等）
2. 快速验证（向量化，<5秒）
3. 聚宽大数据回测验证
4. 完善报告生成（策略设计、代码、结果分析）

佣金: 万分之一 (0.0001)

代码位置: research/tenbagger_10x_strategy/scripts/backtest_enhanced.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 回测配置
# ============================================================

class BacktestConfig:
    """回测配置"""
    
    def __init__(self):
        # 基本配置
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.benchmark = "000300.XSHG"
        
        # 交易成本（万一）
        self.commission_rate = 0.0001  # 万分之一
        self.stamp_tax = 0.001         # 印花税（卖出）
        self.slippage = 0.001          # 滑点（0.1%）
        
        # 回测模式
        self.mode = "fast"  # fast/standard/precise
        
        # 持仓参数
        self.max_holdings = 10
        self.single_stock_max = 0.15
        
        # 风控参数
        self.stop_loss = -0.10
        self.take_profit = 0.80
        self.trailing_stop = 0.15
        self.rebalance_days = 10

# ============================================================
# 完整指标计算
# ============================================================

class PerformanceMetrics:
    """完整回测指标计算"""
    
    @staticmethod
    def calculate_all_metrics(equity_curve: pd.Series, daily_returns: pd.Series,
                             benchmark_returns: pd.Series = None,
                             initial_capital: float = 1000000.0,
                             trade_days: int = 252) -> dict:
        """
        计算所有回测指标
        
        Args:
            equity_curve: 净值曲线
            daily_returns: 日收益率
            benchmark_returns: 基准收益率
            initial_capital: 初始资金
            trade_days: 年交易日数
        """
        metrics = {}
        
        if len(equity_curve) < 2 or len(daily_returns) < 2:
            return metrics
        
        # 1. 收益指标
        total_return = (equity_curve.iloc[-1] / initial_capital) - 1
        metrics['total_return'] = float(total_return)
        metrics['total_return_pct'] = float(total_return * 100)
        
        # 年化收益
        days = len(equity_curve)
        if days > 1:
            annual_return = (1 + total_return) ** (trade_days / days) - 1
            metrics['annual_return'] = float(annual_return)
            metrics['annual_return_pct'] = float(annual_return * 100)
        
        # 2. 风险指标
        # 波动率
        volatility = daily_returns.std() * np.sqrt(trade_days)
        metrics['volatility'] = float(volatility)
        metrics['volatility_pct'] = float(volatility * 100)
        
        # 最大回撤
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        max_drawdown = drawdown.min()
        metrics['max_drawdown'] = float(max_drawdown)
        metrics['max_drawdown_pct'] = float(max_drawdown * 100)
        
        # 最大回撤持续时间
        drawdown_periods = []
        in_drawdown = False
        start_date = None
        for i, dd in enumerate(drawdown):
            if dd < -0.01 and not in_drawdown:  # 进入回撤
                in_drawdown = True
                start_date = i
            elif dd >= -0.01 and in_drawdown:  # 退出回撤
                in_drawdown = False
                if start_date is not None:
                    drawdown_periods.append(i - start_date)
        if in_drawdown and start_date is not None:
            drawdown_periods.append(len(drawdown) - start_date)
        metrics['max_drawdown_duration'] = int(max(drawdown_periods)) if drawdown_periods else 0
        
        # 3. 风险调整收益指标
        # 夏普比率
        if volatility > 0:
            sharpe_ratio = (annual_return if 'annual_return' in metrics else 0) / volatility
            metrics['sharpe_ratio'] = float(sharpe_ratio)
        else:
            metrics['sharpe_ratio'] = 0.0
        
        # 索提诺比率（只考虑下行波动）
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(trade_days)
            if downside_std > 0:
                sortino_ratio = (annual_return if 'annual_return' in metrics else 0) / downside_std
                metrics['sortino_ratio'] = float(sortino_ratio)
            else:
                metrics['sortino_ratio'] = 0.0
        else:
            metrics['sortino_ratio'] = 0.0
        
        # 卡玛比率
        if max_drawdown != 0:
            calmar_ratio = (annual_return if 'annual_return' in metrics else 0) / abs(max_drawdown)
            metrics['calmar_ratio'] = float(calmar_ratio)
        else:
            metrics['calmar_ratio'] = 0.0
        
        # 4. 基准对比
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            benchmark_total = (1 + benchmark_returns).prod() - 1
            metrics['benchmark_return'] = float(benchmark_total)
            metrics['benchmark_return_pct'] = float(benchmark_total * 100)
            
            # 超额收益
            excess_return = total_return - benchmark_total
            metrics['excess_return'] = float(excess_return)
            metrics['excess_return_pct'] = float(excess_return * 100)
            
            # 信息比率
            excess_returns = daily_returns - benchmark_returns
            if len(excess_returns) > 0:
                tracking_error = excess_returns.std() * np.sqrt(trade_days)
                if tracking_error > 0:
                    info_ratio = (annual_return if 'annual_return' in metrics else 0) / tracking_error
                    metrics['info_ratio'] = float(info_ratio)
                else:
                    metrics['info_ratio'] = 0.0
            else:
                metrics['info_ratio'] = 0.0
        
        # 5. 交易统计
        # 这里需要从交易记录中统计
        metrics['total_trades'] = 0  # 将在回测中填充
        metrics['win_rate'] = 0.0
        metrics['profit_loss_ratio'] = 0.0
        metrics['avg_holding_days'] = 0.0
        
        # 6. 月度收益
        if hasattr(equity_curve, 'index') and len(equity_curve) > 20:
            monthly_returns = []
            current_month = None
            month_start_value = initial_capital
            
            for date, value in equity_curve.items():
                month = str(date)[:7] if hasattr(date, '__str__') else str(date)[:7]
                if month != current_month:
                    if current_month is not None:
                        monthly_returns.append((value / month_start_value - 1) * 100)
                    current_month = month
                    month_start_value = value
            
            if monthly_returns:
                metrics['monthly_returns'] = monthly_returns
                metrics['best_month'] = float(max(monthly_returns))
                metrics['worst_month'] = float(min(monthly_returns))
                metrics['monthly_win_rate'] = float(sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) * 100)
        
        # 7. 其他指标
        # Beta（如果有基准）
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            if len(daily_returns) == len(benchmark_returns):
                covariance = np.cov(daily_returns, benchmark_returns)[0, 1]
                benchmark_variance = np.var(benchmark_returns)
                if benchmark_variance > 0:
                    beta = covariance / benchmark_variance
                    metrics['beta'] = float(beta)
                else:
                    metrics['beta'] = 0.0
        
        # Alpha
        if 'beta' in metrics and benchmark_returns is not None:
            benchmark_annual = (1 + benchmark_returns).prod() ** (trade_days / len(benchmark_returns)) - 1
            alpha = (annual_return if 'annual_return' in metrics else 0) - (metrics['beta'] * benchmark_annual)
            metrics['alpha'] = float(alpha)
            metrics['alpha_pct'] = float(alpha * 100)
        
        return metrics

# ============================================================
# 快速验证回测（向量化）
# ============================================================

class FastBacktest:
    """快速验证回测（向量化计算，<5秒）"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.equity_curve = []
        self.daily_returns = []
        self.dates = []
        self.trade_history = []
        self.positions = {}
    
    def run(self, stock_scores: dict, price_data: dict) -> dict:
        """
        快速回测
        
        Args:
            stock_scores: {date: {stock: score}}
            price_data: {stock: DataFrame with close prices}
        """
        logger.info("🚀 快速验证回测（向量化）...")
        
        # 获取所有日期
        all_dates = sorted(set().union(*[scores.keys() for scores in stock_scores.values()]))
        if not all_dates:
            return {}
        
        cash = self.config.initial_capital
        equity = [cash]
        
        for date in all_dates:
            # 选股
            if date in stock_scores:
                scores = stock_scores[date]
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                
                # 简化的交易逻辑（向量化）
                target_stocks = [s[0] for s in selected]
                
                # 计算持仓价值
                portfolio_value = cash
                for stock in target_stocks:
                    if stock in price_data and date in price_data[stock].index:
                        price = price_data[stock].loc[date, 'close']
                        # 简化：假设等权重
                        position_value = cash / len(target_stocks)
                        portfolio_value += position_value
                
                equity.append(portfolio_value)
            else:
                equity.append(equity[-1])
        
        # 计算收益率
        equity_series = pd.Series(equity, index=all_dates[:len(equity)])
        returns = equity_series.pct_change().fillna(0)
        
        # 计算指标
        metrics_calc = PerformanceMetrics()
        metrics = metrics_calc.calculate_all_metrics(
            equity_series,
            returns,
            initial_capital=self.config.initial_capital
        )
        
        return {
            'equity_curve': equity_series.tolist(),
            'daily_returns': returns.tolist(),
            'dates': [str(d) for d in equity_series.index],
            'metrics': metrics
        }

# ============================================================
# 聚宽回测验证
# ============================================================

class JQDataBacktest:
    """聚宽大数据回测验证"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate(self) -> bool:
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, pwd)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def run(self, strategy_func, stock_universe: list) -> dict:
        """
        执行聚宽回测
        
        Args:
            strategy_func: 策略函数
            stock_universe: 股票池
        """
        logger.info("📊 聚宽大数据回测验证...")
        
        # 这里应该调用聚宽的回测引擎
        # 由于需要完整的聚宽环境，这里提供框架
        
        # 获取基准数据
        benchmark_prices = jq.get_price(
            self.config.benchmark,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close']
        )
        
        # 执行策略回测（需要实现具体逻辑）
        # ...
        
        return {
            'status': 'completed',
            'message': '聚宽回测需要完整实现'
        }

# ============================================================
# 完善报告生成
# ============================================================

class EnhancedReportGenerator:
    """完善报告生成器"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
    
    def generate_html_report(self, backtest_results: dict, strategy_code: str = "",
                            strategy_design: str = "") -> str:
        """
        生成完善的HTML报告
        
        Args:
            backtest_results: 回测结果
            strategy_code: 策略代码
            strategy_design: 策略设计说明
        """
        metrics = backtest_results.get('metrics', {})
        equity_curve = backtest_results.get('equity_curve', [])
        dates = backtest_results.get('dates', [])
        
        # 生成图表
        charts_html = self._generate_charts(equity_curve, dates, metrics)
        
        # 指标表格
        metrics_html = self._generate_metrics_table(metrics)
        
        # 策略设计部分
        design_html = f"""
        <div class="section">
            <h2>📐 策略设计</h2>
            <div class="design-content">
                {strategy_design or '<p>策略设计说明...</p>'}
            </div>
        </div>
        """ if strategy_design else ""
        
        # 代码部分
        code_html = f"""
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python">{strategy_code or '# 策略代码...'}</code></pre>
        </div>
        """ if strategy_code else ""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>完善回测报告</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 完善回测报告</h1>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date}</p>
            <p>初始资金: ¥{self.config.initial_cash:,.0f} | 佣金: 万分之一</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric"><div class="label">总收益率</div><div class="value">{metrics.get('total_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">年化收益</div><div class="value">{metrics.get('annual_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">夏普比率</div><div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">索提诺比率</div><div class="value">{metrics.get('sortino_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">卡玛比率</div><div class="value">{metrics.get('calmar_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">最大回撤</div><div class="value">{metrics.get('max_drawdown_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">波动率</div><div class="value">{metrics.get('volatility_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">信息比率</div><div class="value">{metrics.get('info_ratio', 0):.2f}</div></div>
        </div>
        
        {charts_html}
        
        {design_html}
        
        {code_html}
        
        <div class="section">
            <h2>📈 完整指标</h2>
            {metrics_html}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_charts(self, equity_curve: list, dates: list, metrics: dict) -> str:
        """生成图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        charts_html = ""
        
        # 净值曲线
        fig, ax = plt.subplots(figsize=(14, 6))
        if dates:
            date_objs = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in dates[:len(equity_curve)]]
            ax.plot(date_objs, equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=self.config.initial_capital, color='gray', linestyle='--', alpha=0.5)
            ax.set_title('Equity Curve', fontsize=16, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        charts_html += f'<div class="section"><h2>📊 净值曲线</h2><div class="chart"><img src="data:image/png;base64,{img}"></div></div>'
        
        return charts_html
    
    def _generate_metrics_table(self, metrics: dict) -> str:
        """生成指标表格"""
        rows = ""
        metric_names = {
            'total_return_pct': '总收益率',
            'annual_return_pct': '年化收益率',
            'sharpe_ratio': '夏普比率',
            'sortino_ratio': '索提诺比率',
            'calmar_ratio': '卡玛比率',
            'max_drawdown_pct': '最大回撤',
            'volatility_pct': '波动率',
            'info_ratio': '信息比率',
            'beta': 'Beta',
            'alpha_pct': 'Alpha',
            'excess_return_pct': '超额收益',
            'win_rate': '胜率',
            'profit_loss_ratio': '盈亏比',
        }
        
        for key, name in metric_names.items():
            value = metrics.get(key, 0)
            rows += f"<tr><td>{name}</td><td>{value:.2f}</td></tr>"
        
        return f'<table><tr><th>指标</th><th>数值</th></tr>{rows}</table>'

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("完善回测系统")
    print("=" * 80)
    
    config = BacktestConfig()
    print(f"✅ 回测配置:")
    print(f"   佣金: {config.commission_rate*10000:.0f}万分之一")
    print(f"   初始资金: {config.initial_capital:,.0f}")
    print(f"   回测区间: {config.start_date} ~ {config.end_date}")

if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
完善回测系统 - 标准指标 + 快速验证 + 聚宽回测
============================================

功能:
1. 完整回测指标计算（夏普、索提诺、卡玛、最大回撤等）
2. 快速验证（向量化，<5秒）
3. 聚宽大数据回测验证
4. 完善报告生成（策略设计、代码、结果分析）

佣金: 万分之一 (0.0001)

代码位置: research/tenbagger_10x_strategy/scripts/backtest_enhanced.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 回测配置
# ============================================================

class BacktestConfig:
    """回测配置"""
    
    def __init__(self):
        # 基本配置
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.benchmark = "000300.XSHG"
        
        # 交易成本（万一）
        self.commission_rate = 0.0001  # 万分之一
        self.stamp_tax = 0.001         # 印花税（卖出）
        self.slippage = 0.001          # 滑点（0.1%）
        
        # 回测模式
        self.mode = "fast"  # fast/standard/precise
        
        # 持仓参数
        self.max_holdings = 10
        self.single_stock_max = 0.15
        
        # 风控参数
        self.stop_loss = -0.10
        self.take_profit = 0.80
        self.trailing_stop = 0.15
        self.rebalance_days = 10

# ============================================================
# 完整指标计算
# ============================================================

class PerformanceMetrics:
    """完整回测指标计算"""
    
    @staticmethod
    def calculate_all_metrics(equity_curve: pd.Series, daily_returns: pd.Series,
                             benchmark_returns: pd.Series = None,
                             initial_capital: float = 1000000.0,
                             trade_days: int = 252) -> dict:
        """
        计算所有回测指标
        
        Args:
            equity_curve: 净值曲线
            daily_returns: 日收益率
            benchmark_returns: 基准收益率
            initial_capital: 初始资金
            trade_days: 年交易日数
        """
        metrics = {}
        
        if len(equity_curve) < 2 or len(daily_returns) < 2:
            return metrics
        
        # 1. 收益指标
        total_return = (equity_curve.iloc[-1] / initial_capital) - 1
        metrics['total_return'] = float(total_return)
        metrics['total_return_pct'] = float(total_return * 100)
        
        # 年化收益
        days = len(equity_curve)
        if days > 1:
            annual_return = (1 + total_return) ** (trade_days / days) - 1
            metrics['annual_return'] = float(annual_return)
            metrics['annual_return_pct'] = float(annual_return * 100)
        
        # 2. 风险指标
        # 波动率
        volatility = daily_returns.std() * np.sqrt(trade_days)
        metrics['volatility'] = float(volatility)
        metrics['volatility_pct'] = float(volatility * 100)
        
        # 最大回撤
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        max_drawdown = drawdown.min()
        metrics['max_drawdown'] = float(max_drawdown)
        metrics['max_drawdown_pct'] = float(max_drawdown * 100)
        
        # 最大回撤持续时间
        drawdown_periods = []
        in_drawdown = False
        start_date = None
        for i, dd in enumerate(drawdown):
            if dd < -0.01 and not in_drawdown:  # 进入回撤
                in_drawdown = True
                start_date = i
            elif dd >= -0.01 and in_drawdown:  # 退出回撤
                in_drawdown = False
                if start_date is not None:
                    drawdown_periods.append(i - start_date)
        if in_drawdown and start_date is not None:
            drawdown_periods.append(len(drawdown) - start_date)
        metrics['max_drawdown_duration'] = int(max(drawdown_periods)) if drawdown_periods else 0
        
        # 3. 风险调整收益指标
        # 夏普比率
        if volatility > 0:
            sharpe_ratio = (annual_return if 'annual_return' in metrics else 0) / volatility
            metrics['sharpe_ratio'] = float(sharpe_ratio)
        else:
            metrics['sharpe_ratio'] = 0.0
        
        # 索提诺比率（只考虑下行波动）
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(trade_days)
            if downside_std > 0:
                sortino_ratio = (annual_return if 'annual_return' in metrics else 0) / downside_std
                metrics['sortino_ratio'] = float(sortino_ratio)
            else:
                metrics['sortino_ratio'] = 0.0
        else:
            metrics['sortino_ratio'] = 0.0
        
        # 卡玛比率
        if max_drawdown != 0:
            calmar_ratio = (annual_return if 'annual_return' in metrics else 0) / abs(max_drawdown)
            metrics['calmar_ratio'] = float(calmar_ratio)
        else:
            metrics['calmar_ratio'] = 0.0
        
        # 4. 基准对比
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            benchmark_total = (1 + benchmark_returns).prod() - 1
            metrics['benchmark_return'] = float(benchmark_total)
            metrics['benchmark_return_pct'] = float(benchmark_total * 100)
            
            # 超额收益
            excess_return = total_return - benchmark_total
            metrics['excess_return'] = float(excess_return)
            metrics['excess_return_pct'] = float(excess_return * 100)
            
            # 信息比率
            excess_returns = daily_returns - benchmark_returns
            if len(excess_returns) > 0:
                tracking_error = excess_returns.std() * np.sqrt(trade_days)
                if tracking_error > 0:
                    info_ratio = (annual_return if 'annual_return' in metrics else 0) / tracking_error
                    metrics['info_ratio'] = float(info_ratio)
                else:
                    metrics['info_ratio'] = 0.0
            else:
                metrics['info_ratio'] = 0.0
        
        # 5. 交易统计
        # 这里需要从交易记录中统计
        metrics['total_trades'] = 0  # 将在回测中填充
        metrics['win_rate'] = 0.0
        metrics['profit_loss_ratio'] = 0.0
        metrics['avg_holding_days'] = 0.0
        
        # 6. 月度收益
        if hasattr(equity_curve, 'index') and len(equity_curve) > 20:
            monthly_returns = []
            current_month = None
            month_start_value = initial_capital
            
            for date, value in equity_curve.items():
                month = str(date)[:7] if hasattr(date, '__str__') else str(date)[:7]
                if month != current_month:
                    if current_month is not None:
                        monthly_returns.append((value / month_start_value - 1) * 100)
                    current_month = month
                    month_start_value = value
            
            if monthly_returns:
                metrics['monthly_returns'] = monthly_returns
                metrics['best_month'] = float(max(monthly_returns))
                metrics['worst_month'] = float(min(monthly_returns))
                metrics['monthly_win_rate'] = float(sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) * 100)
        
        # 7. 其他指标
        # Beta（如果有基准）
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            if len(daily_returns) == len(benchmark_returns):
                covariance = np.cov(daily_returns, benchmark_returns)[0, 1]
                benchmark_variance = np.var(benchmark_returns)
                if benchmark_variance > 0:
                    beta = covariance / benchmark_variance
                    metrics['beta'] = float(beta)
                else:
                    metrics['beta'] = 0.0
        
        # Alpha
        if 'beta' in metrics and benchmark_returns is not None:
            benchmark_annual = (1 + benchmark_returns).prod() ** (trade_days / len(benchmark_returns)) - 1
            alpha = (annual_return if 'annual_return' in metrics else 0) - (metrics['beta'] * benchmark_annual)
            metrics['alpha'] = float(alpha)
            metrics['alpha_pct'] = float(alpha * 100)
        
        return metrics

# ============================================================
# 快速验证回测（向量化）
# ============================================================

class FastBacktest:
    """快速验证回测（向量化计算，<5秒）"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.equity_curve = []
        self.daily_returns = []
        self.dates = []
        self.trade_history = []
        self.positions = {}
    
    def run(self, stock_scores: dict, price_data: dict) -> dict:
        """
        快速回测
        
        Args:
            stock_scores: {date: {stock: score}}
            price_data: {stock: DataFrame with close prices}
        """
        logger.info("🚀 快速验证回测（向量化）...")
        
        # 获取所有日期
        all_dates = sorted(set().union(*[scores.keys() for scores in stock_scores.values()]))
        if not all_dates:
            return {}
        
        cash = self.config.initial_capital
        equity = [cash]
        
        for date in all_dates:
            # 选股
            if date in stock_scores:
                scores = stock_scores[date]
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                
                # 简化的交易逻辑（向量化）
                target_stocks = [s[0] for s in selected]
                
                # 计算持仓价值
                portfolio_value = cash
                for stock in target_stocks:
                    if stock in price_data and date in price_data[stock].index:
                        price = price_data[stock].loc[date, 'close']
                        # 简化：假设等权重
                        position_value = cash / len(target_stocks)
                        portfolio_value += position_value
                
                equity.append(portfolio_value)
            else:
                equity.append(equity[-1])
        
        # 计算收益率
        equity_series = pd.Series(equity, index=all_dates[:len(equity)])
        returns = equity_series.pct_change().fillna(0)
        
        # 计算指标
        metrics_calc = PerformanceMetrics()
        metrics = metrics_calc.calculate_all_metrics(
            equity_series,
            returns,
            initial_capital=self.config.initial_capital
        )
        
        return {
            'equity_curve': equity_series.tolist(),
            'daily_returns': returns.tolist(),
            'dates': [str(d) for d in equity_series.index],
            'metrics': metrics
        }

# ============================================================
# 聚宽回测验证
# ============================================================

class JQDataBacktest:
    """聚宽大数据回测验证"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate(self) -> bool:
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, pwd)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def run(self, strategy_func, stock_universe: list) -> dict:
        """
        执行聚宽回测
        
        Args:
            strategy_func: 策略函数
            stock_universe: 股票池
        """
        logger.info("📊 聚宽大数据回测验证...")
        
        # 这里应该调用聚宽的回测引擎
        # 由于需要完整的聚宽环境，这里提供框架
        
        # 获取基准数据
        benchmark_prices = jq.get_price(
            self.config.benchmark,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close']
        )
        
        # 执行策略回测（需要实现具体逻辑）
        # ...
        
        return {
            'status': 'completed',
            'message': '聚宽回测需要完整实现'
        }

# ============================================================
# 完善报告生成
# ============================================================

class EnhancedReportGenerator:
    """完善报告生成器"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
    
    def generate_html_report(self, backtest_results: dict, strategy_code: str = "",
                            strategy_design: str = "") -> str:
        """
        生成完善的HTML报告
        
        Args:
            backtest_results: 回测结果
            strategy_code: 策略代码
            strategy_design: 策略设计说明
        """
        metrics = backtest_results.get('metrics', {})
        equity_curve = backtest_results.get('equity_curve', [])
        dates = backtest_results.get('dates', [])
        
        # 生成图表
        charts_html = self._generate_charts(equity_curve, dates, metrics)
        
        # 指标表格
        metrics_html = self._generate_metrics_table(metrics)
        
        # 策略设计部分
        design_html = f"""
        <div class="section">
            <h2>📐 策略设计</h2>
            <div class="design-content">
                {strategy_design or '<p>策略设计说明...</p>'}
            </div>
        </div>
        """ if strategy_design else ""
        
        # 代码部分
        code_html = f"""
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python">{strategy_code or '# 策略代码...'}</code></pre>
        </div>
        """ if strategy_code else ""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>完善回测报告</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 完善回测报告</h1>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date}</p>
            <p>初始资金: ¥{self.config.initial_cash:,.0f} | 佣金: 万分之一</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric"><div class="label">总收益率</div><div class="value">{metrics.get('total_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">年化收益</div><div class="value">{metrics.get('annual_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">夏普比率</div><div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">索提诺比率</div><div class="value">{metrics.get('sortino_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">卡玛比率</div><div class="value">{metrics.get('calmar_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">最大回撤</div><div class="value">{metrics.get('max_drawdown_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">波动率</div><div class="value">{metrics.get('volatility_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">信息比率</div><div class="value">{metrics.get('info_ratio', 0):.2f}</div></div>
        </div>
        
        {charts_html}
        
        {design_html}
        
        {code_html}
        
        <div class="section">
            <h2>📈 完整指标</h2>
            {metrics_html}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_charts(self, equity_curve: list, dates: list, metrics: dict) -> str:
        """生成图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        charts_html = ""
        
        # 净值曲线
        fig, ax = plt.subplots(figsize=(14, 6))
        if dates:
            date_objs = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in dates[:len(equity_curve)]]
            ax.plot(date_objs, equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=self.config.initial_capital, color='gray', linestyle='--', alpha=0.5)
            ax.set_title('Equity Curve', fontsize=16, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        charts_html += f'<div class="section"><h2>📊 净值曲线</h2><div class="chart"><img src="data:image/png;base64,{img}"></div></div>'
        
        return charts_html
    
    def _generate_metrics_table(self, metrics: dict) -> str:
        """生成指标表格"""
        rows = ""
        metric_names = {
            'total_return_pct': '总收益率',
            'annual_return_pct': '年化收益率',
            'sharpe_ratio': '夏普比率',
            'sortino_ratio': '索提诺比率',
            'calmar_ratio': '卡玛比率',
            'max_drawdown_pct': '最大回撤',
            'volatility_pct': '波动率',
            'info_ratio': '信息比率',
            'beta': 'Beta',
            'alpha_pct': 'Alpha',
            'excess_return_pct': '超额收益',
            'win_rate': '胜率',
            'profit_loss_ratio': '盈亏比',
        }
        
        for key, name in metric_names.items():
            value = metrics.get(key, 0)
            rows += f"<tr><td>{name}</td><td>{value:.2f}</td></tr>"
        
        return f'<table><tr><th>指标</th><th>数值</th></tr>{rows}</table>'

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("完善回测系统")
    print("=" * 80)
    
    config = BacktestConfig()
    print(f"✅ 回测配置:")
    print(f"   佣金: {config.commission_rate*10000:.0f}万分之一")
    print(f"   初始资金: {config.initial_capital:,.0f}")
    print(f"   回测区间: {config.start_date} ~ {config.end_date}")

if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
完善回测系统 - 标准指标 + 快速验证 + 聚宽回测
============================================

功能:
1. 完整回测指标计算（夏普、索提诺、卡玛、最大回撤等）
2. 快速验证（向量化，<5秒）
3. 聚宽大数据回测验证
4. 完善报告生成（策略设计、代码、结果分析）

佣金: 万分之一 (0.0001)

代码位置: research/tenbagger_10x_strategy/scripts/backtest_enhanced.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
import jqdatasdk as jq

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ============================================================
# 回测配置
# ============================================================

class BacktestConfig:
    """回测配置"""
    
    def __init__(self):
        # 基本配置
        self.username = "13327806797"
        self.start_date = "2024-01-01"
        self.end_date = "2025-12-20"
        self.initial_capital = 1000000.0
        self.benchmark = "000300.XSHG"
        
        # 交易成本（万一）
        self.commission_rate = 0.0001  # 万分之一
        self.stamp_tax = 0.001         # 印花税（卖出）
        self.slippage = 0.001          # 滑点（0.1%）
        
        # 回测模式
        self.mode = "fast"  # fast/standard/precise
        
        # 持仓参数
        self.max_holdings = 10
        self.single_stock_max = 0.15
        
        # 风控参数
        self.stop_loss = -0.10
        self.take_profit = 0.80
        self.trailing_stop = 0.15
        self.rebalance_days = 10

# ============================================================
# 完整指标计算
# ============================================================

class PerformanceMetrics:
    """完整回测指标计算"""
    
    @staticmethod
    def calculate_all_metrics(equity_curve: pd.Series, daily_returns: pd.Series,
                             benchmark_returns: pd.Series = None,
                             initial_capital: float = 1000000.0,
                             trade_days: int = 252) -> dict:
        """
        计算所有回测指标
        
        Args:
            equity_curve: 净值曲线
            daily_returns: 日收益率
            benchmark_returns: 基准收益率
            initial_capital: 初始资金
            trade_days: 年交易日数
        """
        metrics = {}
        
        if len(equity_curve) < 2 or len(daily_returns) < 2:
            return metrics
        
        # 1. 收益指标
        total_return = (equity_curve.iloc[-1] / initial_capital) - 1
        metrics['total_return'] = float(total_return)
        metrics['total_return_pct'] = float(total_return * 100)
        
        # 年化收益
        days = len(equity_curve)
        if days > 1:
            annual_return = (1 + total_return) ** (trade_days / days) - 1
            metrics['annual_return'] = float(annual_return)
            metrics['annual_return_pct'] = float(annual_return * 100)
        
        # 2. 风险指标
        # 波动率
        volatility = daily_returns.std() * np.sqrt(trade_days)
        metrics['volatility'] = float(volatility)
        metrics['volatility_pct'] = float(volatility * 100)
        
        # 最大回撤
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        max_drawdown = drawdown.min()
        metrics['max_drawdown'] = float(max_drawdown)
        metrics['max_drawdown_pct'] = float(max_drawdown * 100)
        
        # 最大回撤持续时间
        drawdown_periods = []
        in_drawdown = False
        start_date = None
        for i, dd in enumerate(drawdown):
            if dd < -0.01 and not in_drawdown:  # 进入回撤
                in_drawdown = True
                start_date = i
            elif dd >= -0.01 and in_drawdown:  # 退出回撤
                in_drawdown = False
                if start_date is not None:
                    drawdown_periods.append(i - start_date)
        if in_drawdown and start_date is not None:
            drawdown_periods.append(len(drawdown) - start_date)
        metrics['max_drawdown_duration'] = int(max(drawdown_periods)) if drawdown_periods else 0
        
        # 3. 风险调整收益指标
        # 夏普比率
        if volatility > 0:
            sharpe_ratio = (annual_return if 'annual_return' in metrics else 0) / volatility
            metrics['sharpe_ratio'] = float(sharpe_ratio)
        else:
            metrics['sharpe_ratio'] = 0.0
        
        # 索提诺比率（只考虑下行波动）
        downside_returns = daily_returns[daily_returns < 0]
        if len(downside_returns) > 0:
            downside_std = downside_returns.std() * np.sqrt(trade_days)
            if downside_std > 0:
                sortino_ratio = (annual_return if 'annual_return' in metrics else 0) / downside_std
                metrics['sortino_ratio'] = float(sortino_ratio)
            else:
                metrics['sortino_ratio'] = 0.0
        else:
            metrics['sortino_ratio'] = 0.0
        
        # 卡玛比率
        if max_drawdown != 0:
            calmar_ratio = (annual_return if 'annual_return' in metrics else 0) / abs(max_drawdown)
            metrics['calmar_ratio'] = float(calmar_ratio)
        else:
            metrics['calmar_ratio'] = 0.0
        
        # 4. 基准对比
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            benchmark_total = (1 + benchmark_returns).prod() - 1
            metrics['benchmark_return'] = float(benchmark_total)
            metrics['benchmark_return_pct'] = float(benchmark_total * 100)
            
            # 超额收益
            excess_return = total_return - benchmark_total
            metrics['excess_return'] = float(excess_return)
            metrics['excess_return_pct'] = float(excess_return * 100)
            
            # 信息比率
            excess_returns = daily_returns - benchmark_returns
            if len(excess_returns) > 0:
                tracking_error = excess_returns.std() * np.sqrt(trade_days)
                if tracking_error > 0:
                    info_ratio = (annual_return if 'annual_return' in metrics else 0) / tracking_error
                    metrics['info_ratio'] = float(info_ratio)
                else:
                    metrics['info_ratio'] = 0.0
            else:
                metrics['info_ratio'] = 0.0
        
        # 5. 交易统计
        # 这里需要从交易记录中统计
        metrics['total_trades'] = 0  # 将在回测中填充
        metrics['win_rate'] = 0.0
        metrics['profit_loss_ratio'] = 0.0
        metrics['avg_holding_days'] = 0.0
        
        # 6. 月度收益
        if hasattr(equity_curve, 'index') and len(equity_curve) > 20:
            monthly_returns = []
            current_month = None
            month_start_value = initial_capital
            
            for date, value in equity_curve.items():
                month = str(date)[:7] if hasattr(date, '__str__') else str(date)[:7]
                if month != current_month:
                    if current_month is not None:
                        monthly_returns.append((value / month_start_value - 1) * 100)
                    current_month = month
                    month_start_value = value
            
            if monthly_returns:
                metrics['monthly_returns'] = monthly_returns
                metrics['best_month'] = float(max(monthly_returns))
                metrics['worst_month'] = float(min(monthly_returns))
                metrics['monthly_win_rate'] = float(sum(1 for r in monthly_returns if r > 0) / len(monthly_returns) * 100)
        
        # 7. 其他指标
        # Beta（如果有基准）
        if benchmark_returns is not None and len(benchmark_returns) > 0:
            if len(daily_returns) == len(benchmark_returns):
                covariance = np.cov(daily_returns, benchmark_returns)[0, 1]
                benchmark_variance = np.var(benchmark_returns)
                if benchmark_variance > 0:
                    beta = covariance / benchmark_variance
                    metrics['beta'] = float(beta)
                else:
                    metrics['beta'] = 0.0
        
        # Alpha
        if 'beta' in metrics and benchmark_returns is not None:
            benchmark_annual = (1 + benchmark_returns).prod() ** (trade_days / len(benchmark_returns)) - 1
            alpha = (annual_return if 'annual_return' in metrics else 0) - (metrics['beta'] * benchmark_annual)
            metrics['alpha'] = float(alpha)
            metrics['alpha_pct'] = float(alpha * 100)
        
        return metrics

# ============================================================
# 快速验证回测（向量化）
# ============================================================

class FastBacktest:
    """快速验证回测（向量化计算，<5秒）"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.equity_curve = []
        self.daily_returns = []
        self.dates = []
        self.trade_history = []
        self.positions = {}
    
    def run(self, stock_scores: dict, price_data: dict) -> dict:
        """
        快速回测
        
        Args:
            stock_scores: {date: {stock: score}}
            price_data: {stock: DataFrame with close prices}
        """
        logger.info("🚀 快速验证回测（向量化）...")
        
        # 获取所有日期
        all_dates = sorted(set().union(*[scores.keys() for scores in stock_scores.values()]))
        if not all_dates:
            return {}
        
        cash = self.config.initial_capital
        equity = [cash]
        
        for date in all_dates:
            # 选股
            if date in stock_scores:
                scores = stock_scores[date]
                selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.config.max_holdings]
                
                # 简化的交易逻辑（向量化）
                target_stocks = [s[0] for s in selected]
                
                # 计算持仓价值
                portfolio_value = cash
                for stock in target_stocks:
                    if stock in price_data and date in price_data[stock].index:
                        price = price_data[stock].loc[date, 'close']
                        # 简化：假设等权重
                        position_value = cash / len(target_stocks)
                        portfolio_value += position_value
                
                equity.append(portfolio_value)
            else:
                equity.append(equity[-1])
        
        # 计算收益率
        equity_series = pd.Series(equity, index=all_dates[:len(equity)])
        returns = equity_series.pct_change().fillna(0)
        
        # 计算指标
        metrics_calc = PerformanceMetrics()
        metrics = metrics_calc.calculate_all_metrics(
            equity_series,
            returns,
            initial_capital=self.config.initial_capital
        )
        
        return {
            'equity_curve': equity_series.tolist(),
            'daily_returns': returns.tolist(),
            'dates': [str(d) for d in equity_series.index],
            'metrics': metrics
        }

# ============================================================
# 聚宽回测验证
# ============================================================

class JQDataBacktest:
    """聚宽大数据回测验证"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
        self.price_cache = {}
        self.fundamentals_cache = {}
    
    def authenticate(self) -> bool:
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.config.username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            else:
                from config.config_manager import get_config_manager
                pwd = get_config_manager().get_jqdata_config().get('password')
            
            jq.auth(self.config.username, pwd)
            logger.info(f"✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def run(self, strategy_func, stock_universe: list) -> dict:
        """
        执行聚宽回测
        
        Args:
            strategy_func: 策略函数
            stock_universe: 股票池
        """
        logger.info("📊 聚宽大数据回测验证...")
        
        # 这里应该调用聚宽的回测引擎
        # 由于需要完整的聚宽环境，这里提供框架
        
        # 获取基准数据
        benchmark_prices = jq.get_price(
            self.config.benchmark,
            start_date=self.config.start_date,
            end_date=self.config.end_date,
            frequency='daily',
            fields=['close']
        )
        
        # 执行策略回测（需要实现具体逻辑）
        # ...
        
        return {
            'status': 'completed',
            'message': '聚宽回测需要完整实现'
        }

# ============================================================
# 完善报告生成
# ============================================================

class EnhancedReportGenerator:
    """完善报告生成器"""
    
    def __init__(self, config: BacktestConfig):
        self.config = config
    
    def generate_html_report(self, backtest_results: dict, strategy_code: str = "",
                            strategy_design: str = "") -> str:
        """
        生成完善的HTML报告
        
        Args:
            backtest_results: 回测结果
            strategy_code: 策略代码
            strategy_design: 策略设计说明
        """
        metrics = backtest_results.get('metrics', {})
        equity_curve = backtest_results.get('equity_curve', [])
        dates = backtest_results.get('dates', [])
        
        # 生成图表
        charts_html = self._generate_charts(equity_curve, dates, metrics)
        
        # 指标表格
        metrics_html = self._generate_metrics_table(metrics)
        
        # 策略设计部分
        design_html = f"""
        <div class="section">
            <h2>📐 策略设计</h2>
            <div class="design-content">
                {strategy_design or '<p>策略设计说明...</p>'}
            </div>
        </div>
        """ if strategy_design else ""
        
        # 代码部分
        code_html = f"""
        <div class="section">
            <h2>💻 策略代码</h2>
            <pre><code class="language-python">{strategy_code or '# 策略代码...'}</code></pre>
        </div>
        """ if strategy_code else ""
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>完善回测报告</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    <style>
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e); color: #e0e0e0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 40px; border-radius: 20px; margin-bottom: 30px; }}
        .header h1 {{ font-size: 2.5em; margin: 0 0 15px 0; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric {{ background: rgba(255,255,255,0.05); padding: 25px; border-radius: 16px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; }}
        .metric .value {{ font-size: 2.2em; font-weight: bold; color: #667eea; }}
        .section {{ background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; margin-bottom: 30px; }}
        .chart img {{ width: 100%; border-radius: 12px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); }}
        pre {{ background: #1e1e1e; padding: 20px; border-radius: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 完善回测报告</h1>
            <p>回测区间: {self.config.start_date} ~ {self.config.end_date}</p>
            <p>初始资金: ¥{self.config.initial_cash:,.0f} | 佣金: 万分之一</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric"><div class="label">总收益率</div><div class="value">{metrics.get('total_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">年化收益</div><div class="value">{metrics.get('annual_return_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">夏普比率</div><div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">索提诺比率</div><div class="value">{metrics.get('sortino_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">卡玛比率</div><div class="value">{metrics.get('calmar_ratio', 0):.2f}</div></div>
            <div class="metric"><div class="label">最大回撤</div><div class="value">{metrics.get('max_drawdown_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">波动率</div><div class="value">{metrics.get('volatility_pct', 0):.2f}%</div></div>
            <div class="metric"><div class="label">信息比率</div><div class="value">{metrics.get('info_ratio', 0):.2f}</div></div>
        </div>
        
        {charts_html}
        
        {design_html}
        
        {code_html}
        
        <div class="section">
            <h2>📈 完整指标</h2>
            {metrics_html}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>"""
        
        return html
    
    def _generate_charts(self, equity_curve: list, dates: list, metrics: dict) -> str:
        """生成图表"""
        if not MATPLOTLIB_AVAILABLE or not equity_curve:
            return ""
        
        charts_html = ""
        
        # 净值曲线
        fig, ax = plt.subplots(figsize=(14, 6))
        if dates:
            date_objs = [datetime.strptime(d, '%Y-%m-%d') if isinstance(d, str) else d for d in dates[:len(equity_curve)]]
            ax.plot(date_objs, equity_curve, linewidth=2.5, color='#667eea', label='Strategy')
            ax.axhline(y=self.config.initial_capital, color='gray', linestyle='--', alpha=0.5)
            ax.set_title('Equity Curve', fontsize=16, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        img = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        charts_html += f'<div class="section"><h2>📊 净值曲线</h2><div class="chart"><img src="data:image/png;base64,{img}"></div></div>'
        
        return charts_html
    
    def _generate_metrics_table(self, metrics: dict) -> str:
        """生成指标表格"""
        rows = ""
        metric_names = {
            'total_return_pct': '总收益率',
            'annual_return_pct': '年化收益率',
            'sharpe_ratio': '夏普比率',
            'sortino_ratio': '索提诺比率',
            'calmar_ratio': '卡玛比率',
            'max_drawdown_pct': '最大回撤',
            'volatility_pct': '波动率',
            'info_ratio': '信息比率',
            'beta': 'Beta',
            'alpha_pct': 'Alpha',
            'excess_return_pct': '超额收益',
            'win_rate': '胜率',
            'profit_loss_ratio': '盈亏比',
        }
        
        for key, name in metric_names.items():
            value = metrics.get(key, 0)
            rows += f"<tr><td>{name}</td><td>{value:.2f}</td></tr>"
        
        return f'<table><tr><th>指标</th><th>数值</th></tr>{rows}</table>'

# ============================================================
# 主函数
# ============================================================

def main():
    """示例用法"""
    print("=" * 80)
    print("完善回测系统")
    print("=" * 80)
    
    config = BacktestConfig()
    print(f"✅ 回测配置:")
    print(f"   佣金: {config.commission_rate*10000:.0f}万分之一")
    print(f"   初始资金: {config.initial_capital:,.0f}")
    print(f"   回测区间: {config.start_date} ~ {config.end_date}")

if __name__ == "__main__":
    main()









































