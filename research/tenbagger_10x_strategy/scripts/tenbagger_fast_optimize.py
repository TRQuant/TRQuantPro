#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股快速优化策略 - 简化版
===========================

优化要点：
1. 减少参数组合
2. 向量化回测
3. 只保留核心因子

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_fast_optimize.py
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
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def vectorized_backtest(price_data: pd.DataFrame, config: dict) -> dict:
    """
    向量化回测 - 极速版
    
    策略：每周调仓，选择过去20日动量最强的N只股票
    """
    max_holdings = config.get('max_holdings', 3)
    momentum_period = config.get('momentum_period', 20)
    rebalance_days = config.get('rebalance_days', 5)
    stop_loss = config.get('stop_loss', -0.08)
    take_profit = config.get('take_profit', 0.50)
    
    # 转为宽表
    close_df = price_data.pivot(index='time', columns='code', values='close')
    
    # 计算动量
    momentum = close_df.pct_change(momentum_period)
    
    # 生成信号
    dates = close_df.index
    n_dates = len(dates)
    
    # 初始化
    initial_capital = 1000000
    cash = initial_capital
    positions = {}
    equity_curve = []
    trades = []
    
    for i, date in enumerate(dates):
        # 更新持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
        
        # 调仓检查
        if i % rebalance_days == 0 and i > momentum_period:
            # 获取当日动量排名
            mom_today = momentum.loc[date].dropna()
            
            if len(mom_today) > 0:
                # 选择动量最强的股票
                top_stocks = mom_today.nlargest(max_holdings).index.tolist()
                
                # 卖出不在top中的
                for stock in list(positions.keys()):
                    if stock not in top_stocks:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price):
                            value = positions[stock]['shares'] * price * 0.9985
                            cash += value
                            trades.append({
                                'date': str(date),
                                'stock': stock,
                                'action': 'SELL',
                                'reason': '调仓'
                            })
                            del positions[stock]
                
                # 买入新选中的
                for stock in top_stocks:
                    if stock not in positions:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price) and price > 0:
                            target_value = portfolio_value / max_holdings
                            buy_value = min(target_value, cash * 0.9)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': str(date),
                                        'stock': stock,
                                        'action': 'BUY',
                                        'reason': f'动量Top{max_holdings}'
                                    })
        
        # 风控
        for stock in list(positions.keys()):
            pos = positions[stock]
            price = pos.get('current_price', pos['cost'])
            cost = pos['cost']
            highest = pos.get('highest', price)
            
            pnl = (price - cost) / cost
            
            if pnl <= stop_loss:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止损{pnl*100:.1f}%'})
                del positions[stock]
            elif pnl >= take_profit:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止盈{pnl*100:.1f}%'})
                del positions[stock]
        
        # 记录净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    portfolio_value += pos['shares'] * price
        
        equity_curve.append(portfolio_value)
    
    # 计算指标
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    
    return {
        'metrics': {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'max_drawdown': max_dd,
            'volatility': volatility
        },
        'equity_curve': equity_curve,
        'trades': trades,
        'config': config
    }


def fast_grid_search(price_data: pd.DataFrame) -> dict:
    """快速网格搜索"""
    
    # 简化的参数网格
    param_grid = {
        'max_holdings': [2, 3, 5],
        'momentum_period': [10, 20],
        'rebalance_days': [3, 5],
        'stop_loss': [-0.08, -0.12],
        'take_profit': [0.50, 1.00],
    }
    
    from itertools import product
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total = 1
    for v in values:
        total *= len(v)
    
    logger.info(f"🔍 快速优化: {total}种组合")
    
    for idx, combo in enumerate(product(*values)):
        config = dict(zip(keys, combo))
        result = vectorized_backtest(price_data, config)
        
        results.append({
            'config': config,
            'sharpe': result['metrics']['sharpe_ratio'],
            'total_return': result['metrics']['total_return'],
            'annual_return': result['metrics']['annual_return'],
            'max_drawdown': result['metrics']['max_drawdown'],
            'calmar': result['metrics']['calmar_ratio']
        })
    
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_5': results[:5],
        'total_tested': len(results)
    }


def generate_report(result: dict, opt_result: dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        equity = result['equity_curve']
        
        axes[0].plot(equity, linewidth=2, color='#10b981')
        axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#10b981')
        axes[0].axhline(y=equity[0] * 2, color='gold', linestyle='--', label='2x Target')
        axes[0].set_title('Portfolio Value', fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[1].set_title('Drawdown (%)', fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果
    opt_table = ""
    if opt_result and opt_result.get('top_5'):
        rows = ""
        for i, r in enumerate(opt_result['top_5']):
            rows += f"""<tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
            </tr>"""
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th></tr>
                {rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股快速优化报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #10b981, #059669); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #10b981; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #10b981; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(16,185,129,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 十倍股快速优化策略</h1>
            <p>动量选股 + 向量化回测 + 参数优化</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 最优参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>momentum_period</td><td>{config.get('momentum_period', 20)}</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.50)*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("⚡ 十倍股快速优化策略")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 获取股票池
    logger.info("📥 获取数据...")
    stocks = jq.get_index_stocks('399006.XSHE')[:50]  # 创业板50只
    stocks += jq.get_index_stocks('000905.XSHG')[:30]  # 中证500 30只
    stocks = list(set(stocks))
    
    logger.info(f"   股票池: {len(stocks)}只")
    
    # 加载数据
    price_data = jq.get_price(
        stocks,
        start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
        end_date=end_date,
        frequency='daily',
        fields=['close'],
        panel=False,
        skip_paused=True
    )
    
    logger.info(f"   数据行数: {len(price_data)}")
    
    # 网格搜索
    opt_result = fast_grid_search(price_data)
    
    if opt_result['best']:
        logger.info(f"✅ 最优参数: {opt_result['best']['config']}")
        logger.info(f"   夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   总收益: {opt_result['best']['total_return']*100:.2f}%")
        logger.info(f"   年化: {opt_result['best']['annual_return']*100:.2f}%")
        
        # 用最优参数运行
        best_result = vectorized_backtest(price_data, opt_result['best']['config'])
    else:
        best_result = vectorized_backtest(price_data, {})
    
    # 生成报告
    logger.info("📝 生成报告...")
    html = generate_report(best_result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_fast_optimize_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {best_result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {best_result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {best_result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return best_result


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股快速优化策略 - 简化版
===========================

优化要点：
1. 减少参数组合
2. 向量化回测
3. 只保留核心因子

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_fast_optimize.py
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
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def vectorized_backtest(price_data: pd.DataFrame, config: dict) -> dict:
    """
    向量化回测 - 极速版
    
    策略：每周调仓，选择过去20日动量最强的N只股票
    """
    max_holdings = config.get('max_holdings', 3)
    momentum_period = config.get('momentum_period', 20)
    rebalance_days = config.get('rebalance_days', 5)
    stop_loss = config.get('stop_loss', -0.08)
    take_profit = config.get('take_profit', 0.50)
    
    # 转为宽表
    close_df = price_data.pivot(index='time', columns='code', values='close')
    
    # 计算动量
    momentum = close_df.pct_change(momentum_period)
    
    # 生成信号
    dates = close_df.index
    n_dates = len(dates)
    
    # 初始化
    initial_capital = 1000000
    cash = initial_capital
    positions = {}
    equity_curve = []
    trades = []
    
    for i, date in enumerate(dates):
        # 更新持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
        
        # 调仓检查
        if i % rebalance_days == 0 and i > momentum_period:
            # 获取当日动量排名
            mom_today = momentum.loc[date].dropna()
            
            if len(mom_today) > 0:
                # 选择动量最强的股票
                top_stocks = mom_today.nlargest(max_holdings).index.tolist()
                
                # 卖出不在top中的
                for stock in list(positions.keys()):
                    if stock not in top_stocks:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price):
                            value = positions[stock]['shares'] * price * 0.9985
                            cash += value
                            trades.append({
                                'date': str(date),
                                'stock': stock,
                                'action': 'SELL',
                                'reason': '调仓'
                            })
                            del positions[stock]
                
                # 买入新选中的
                for stock in top_stocks:
                    if stock not in positions:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price) and price > 0:
                            target_value = portfolio_value / max_holdings
                            buy_value = min(target_value, cash * 0.9)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': str(date),
                                        'stock': stock,
                                        'action': 'BUY',
                                        'reason': f'动量Top{max_holdings}'
                                    })
        
        # 风控
        for stock in list(positions.keys()):
            pos = positions[stock]
            price = pos.get('current_price', pos['cost'])
            cost = pos['cost']
            highest = pos.get('highest', price)
            
            pnl = (price - cost) / cost
            
            if pnl <= stop_loss:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止损{pnl*100:.1f}%'})
                del positions[stock]
            elif pnl >= take_profit:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止盈{pnl*100:.1f}%'})
                del positions[stock]
        
        # 记录净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    portfolio_value += pos['shares'] * price
        
        equity_curve.append(portfolio_value)
    
    # 计算指标
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    
    return {
        'metrics': {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'max_drawdown': max_dd,
            'volatility': volatility
        },
        'equity_curve': equity_curve,
        'trades': trades,
        'config': config
    }


def fast_grid_search(price_data: pd.DataFrame) -> dict:
    """快速网格搜索"""
    
    # 简化的参数网格
    param_grid = {
        'max_holdings': [2, 3, 5],
        'momentum_period': [10, 20],
        'rebalance_days': [3, 5],
        'stop_loss': [-0.08, -0.12],
        'take_profit': [0.50, 1.00],
    }
    
    from itertools import product
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total = 1
    for v in values:
        total *= len(v)
    
    logger.info(f"🔍 快速优化: {total}种组合")
    
    for idx, combo in enumerate(product(*values)):
        config = dict(zip(keys, combo))
        result = vectorized_backtest(price_data, config)
        
        results.append({
            'config': config,
            'sharpe': result['metrics']['sharpe_ratio'],
            'total_return': result['metrics']['total_return'],
            'annual_return': result['metrics']['annual_return'],
            'max_drawdown': result['metrics']['max_drawdown'],
            'calmar': result['metrics']['calmar_ratio']
        })
    
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_5': results[:5],
        'total_tested': len(results)
    }


def generate_report(result: dict, opt_result: dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        equity = result['equity_curve']
        
        axes[0].plot(equity, linewidth=2, color='#10b981')
        axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#10b981')
        axes[0].axhline(y=equity[0] * 2, color='gold', linestyle='--', label='2x Target')
        axes[0].set_title('Portfolio Value', fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[1].set_title('Drawdown (%)', fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果
    opt_table = ""
    if opt_result and opt_result.get('top_5'):
        rows = ""
        for i, r in enumerate(opt_result['top_5']):
            rows += f"""<tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
            </tr>"""
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th></tr>
                {rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股快速优化报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #10b981, #059669); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #10b981; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #10b981; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(16,185,129,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 十倍股快速优化策略</h1>
            <p>动量选股 + 向量化回测 + 参数优化</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 最优参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>momentum_period</td><td>{config.get('momentum_period', 20)}</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.50)*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("⚡ 十倍股快速优化策略")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 获取股票池
    logger.info("📥 获取数据...")
    stocks = jq.get_index_stocks('399006.XSHE')[:50]  # 创业板50只
    stocks += jq.get_index_stocks('000905.XSHG')[:30]  # 中证500 30只
    stocks = list(set(stocks))
    
    logger.info(f"   股票池: {len(stocks)}只")
    
    # 加载数据
    price_data = jq.get_price(
        stocks,
        start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
        end_date=end_date,
        frequency='daily',
        fields=['close'],
        panel=False,
        skip_paused=True
    )
    
    logger.info(f"   数据行数: {len(price_data)}")
    
    # 网格搜索
    opt_result = fast_grid_search(price_data)
    
    if opt_result['best']:
        logger.info(f"✅ 最优参数: {opt_result['best']['config']}")
        logger.info(f"   夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   总收益: {opt_result['best']['total_return']*100:.2f}%")
        logger.info(f"   年化: {opt_result['best']['annual_return']*100:.2f}%")
        
        # 用最优参数运行
        best_result = vectorized_backtest(price_data, opt_result['best']['config'])
    else:
        best_result = vectorized_backtest(price_data, {})
    
    # 生成报告
    logger.info("📝 生成报告...")
    html = generate_report(best_result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_fast_optimize_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {best_result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {best_result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {best_result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return best_result


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
十倍股快速优化策略 - 简化版
===========================

优化要点：
1. 减少参数组合
2. 向量化回测
3. 只保留核心因子

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_fast_optimize.py
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
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def vectorized_backtest(price_data: pd.DataFrame, config: dict) -> dict:
    """
    向量化回测 - 极速版
    
    策略：每周调仓，选择过去20日动量最强的N只股票
    """
    max_holdings = config.get('max_holdings', 3)
    momentum_period = config.get('momentum_period', 20)
    rebalance_days = config.get('rebalance_days', 5)
    stop_loss = config.get('stop_loss', -0.08)
    take_profit = config.get('take_profit', 0.50)
    
    # 转为宽表
    close_df = price_data.pivot(index='time', columns='code', values='close')
    
    # 计算动量
    momentum = close_df.pct_change(momentum_period)
    
    # 生成信号
    dates = close_df.index
    n_dates = len(dates)
    
    # 初始化
    initial_capital = 1000000
    cash = initial_capital
    positions = {}
    equity_curve = []
    trades = []
    
    for i, date in enumerate(dates):
        # 更新持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
        
        # 调仓检查
        if i % rebalance_days == 0 and i > momentum_period:
            # 获取当日动量排名
            mom_today = momentum.loc[date].dropna()
            
            if len(mom_today) > 0:
                # 选择动量最强的股票
                top_stocks = mom_today.nlargest(max_holdings).index.tolist()
                
                # 卖出不在top中的
                for stock in list(positions.keys()):
                    if stock not in top_stocks:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price):
                            value = positions[stock]['shares'] * price * 0.9985
                            cash += value
                            trades.append({
                                'date': str(date),
                                'stock': stock,
                                'action': 'SELL',
                                'reason': '调仓'
                            })
                            del positions[stock]
                
                # 买入新选中的
                for stock in top_stocks:
                    if stock not in positions:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price) and price > 0:
                            target_value = portfolio_value / max_holdings
                            buy_value = min(target_value, cash * 0.9)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': str(date),
                                        'stock': stock,
                                        'action': 'BUY',
                                        'reason': f'动量Top{max_holdings}'
                                    })
        
        # 风控
        for stock in list(positions.keys()):
            pos = positions[stock]
            price = pos.get('current_price', pos['cost'])
            cost = pos['cost']
            highest = pos.get('highest', price)
            
            pnl = (price - cost) / cost
            
            if pnl <= stop_loss:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止损{pnl*100:.1f}%'})
                del positions[stock]
            elif pnl >= take_profit:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止盈{pnl*100:.1f}%'})
                del positions[stock]
        
        # 记录净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    portfolio_value += pos['shares'] * price
        
        equity_curve.append(portfolio_value)
    
    # 计算指标
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    
    return {
        'metrics': {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'max_drawdown': max_dd,
            'volatility': volatility
        },
        'equity_curve': equity_curve,
        'trades': trades,
        'config': config
    }


def fast_grid_search(price_data: pd.DataFrame) -> dict:
    """快速网格搜索"""
    
    # 简化的参数网格
    param_grid = {
        'max_holdings': [2, 3, 5],
        'momentum_period': [10, 20],
        'rebalance_days': [3, 5],
        'stop_loss': [-0.08, -0.12],
        'take_profit': [0.50, 1.00],
    }
    
    from itertools import product
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total = 1
    for v in values:
        total *= len(v)
    
    logger.info(f"🔍 快速优化: {total}种组合")
    
    for idx, combo in enumerate(product(*values)):
        config = dict(zip(keys, combo))
        result = vectorized_backtest(price_data, config)
        
        results.append({
            'config': config,
            'sharpe': result['metrics']['sharpe_ratio'],
            'total_return': result['metrics']['total_return'],
            'annual_return': result['metrics']['annual_return'],
            'max_drawdown': result['metrics']['max_drawdown'],
            'calmar': result['metrics']['calmar_ratio']
        })
    
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_5': results[:5],
        'total_tested': len(results)
    }


def generate_report(result: dict, opt_result: dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        equity = result['equity_curve']
        
        axes[0].plot(equity, linewidth=2, color='#10b981')
        axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#10b981')
        axes[0].axhline(y=equity[0] * 2, color='gold', linestyle='--', label='2x Target')
        axes[0].set_title('Portfolio Value', fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[1].set_title('Drawdown (%)', fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果
    opt_table = ""
    if opt_result and opt_result.get('top_5'):
        rows = ""
        for i, r in enumerate(opt_result['top_5']):
            rows += f"""<tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
            </tr>"""
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th></tr>
                {rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股快速优化报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #10b981, #059669); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #10b981; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #10b981; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(16,185,129,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 十倍股快速优化策略</h1>
            <p>动量选股 + 向量化回测 + 参数优化</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 最优参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>momentum_period</td><td>{config.get('momentum_period', 20)}</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.50)*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("⚡ 十倍股快速优化策略")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 获取股票池
    logger.info("📥 获取数据...")
    stocks = jq.get_index_stocks('399006.XSHE')[:50]  # 创业板50只
    stocks += jq.get_index_stocks('000905.XSHG')[:30]  # 中证500 30只
    stocks = list(set(stocks))
    
    logger.info(f"   股票池: {len(stocks)}只")
    
    # 加载数据
    price_data = jq.get_price(
        stocks,
        start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
        end_date=end_date,
        frequency='daily',
        fields=['close'],
        panel=False,
        skip_paused=True
    )
    
    logger.info(f"   数据行数: {len(price_data)}")
    
    # 网格搜索
    opt_result = fast_grid_search(price_data)
    
    if opt_result['best']:
        logger.info(f"✅ 最优参数: {opt_result['best']['config']}")
        logger.info(f"   夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   总收益: {opt_result['best']['total_return']*100:.2f}%")
        logger.info(f"   年化: {opt_result['best']['annual_return']*100:.2f}%")
        
        # 用最优参数运行
        best_result = vectorized_backtest(price_data, opt_result['best']['config'])
    else:
        best_result = vectorized_backtest(price_data, {})
    
    # 生成报告
    logger.info("📝 生成报告...")
    html = generate_report(best_result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_fast_optimize_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {best_result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {best_result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {best_result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return best_result


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股快速优化策略 - 简化版
===========================

优化要点：
1. 减少参数组合
2. 向量化回测
3. 只保留核心因子

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_fast_optimize.py
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
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


def authenticate_jqdata() -> bool:
    """认证JQData"""
    try:
        cfg_path = PROJECT_ROOT / "config" / "jqdata_13327806797.json"
        if cfg_path.exists():
            with open(cfg_path, 'r') as f:
                pwd = json.load(f).get('password')
        jq.auth("13327806797", pwd)
        logger.info("✅ JQData认证成功")
        return True
    except Exception as e:
        logger.error(f"❌ 认证失败: {e}")
        return False


def vectorized_backtest(price_data: pd.DataFrame, config: dict) -> dict:
    """
    向量化回测 - 极速版
    
    策略：每周调仓，选择过去20日动量最强的N只股票
    """
    max_holdings = config.get('max_holdings', 3)
    momentum_period = config.get('momentum_period', 20)
    rebalance_days = config.get('rebalance_days', 5)
    stop_loss = config.get('stop_loss', -0.08)
    take_profit = config.get('take_profit', 0.50)
    
    # 转为宽表
    close_df = price_data.pivot(index='time', columns='code', values='close')
    
    # 计算动量
    momentum = close_df.pct_change(momentum_period)
    
    # 生成信号
    dates = close_df.index
    n_dates = len(dates)
    
    # 初始化
    initial_capital = 1000000
    cash = initial_capital
    positions = {}
    equity_curve = []
    trades = []
    
    for i, date in enumerate(dates):
        # 更新持仓价值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
        
        # 调仓检查
        if i % rebalance_days == 0 and i > momentum_period:
            # 获取当日动量排名
            mom_today = momentum.loc[date].dropna()
            
            if len(mom_today) > 0:
                # 选择动量最强的股票
                top_stocks = mom_today.nlargest(max_holdings).index.tolist()
                
                # 卖出不在top中的
                for stock in list(positions.keys()):
                    if stock not in top_stocks:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price):
                            value = positions[stock]['shares'] * price * 0.9985
                            cash += value
                            trades.append({
                                'date': str(date),
                                'stock': stock,
                                'action': 'SELL',
                                'reason': '调仓'
                            })
                            del positions[stock]
                
                # 买入新选中的
                for stock in top_stocks:
                    if stock not in positions:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price) and price > 0:
                            target_value = portfolio_value / max_holdings
                            buy_value = min(target_value, cash * 0.9)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': str(date),
                                        'stock': stock,
                                        'action': 'BUY',
                                        'reason': f'动量Top{max_holdings}'
                                    })
        
        # 风控
        for stock in list(positions.keys()):
            pos = positions[stock]
            price = pos.get('current_price', pos['cost'])
            cost = pos['cost']
            highest = pos.get('highest', price)
            
            pnl = (price - cost) / cost
            
            if pnl <= stop_loss:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止损{pnl*100:.1f}%'})
                del positions[stock]
            elif pnl >= take_profit:
                value = pos['shares'] * price * 0.9985
                cash += value
                trades.append({'date': str(date), 'stock': stock, 'action': 'SELL', 'reason': f'止盈{pnl*100:.1f}%'})
                del positions[stock]
        
        # 记录净值
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    portfolio_value += pos['shares'] * price
        
        equity_curve.append(portfolio_value)
    
    # 计算指标
    equity = pd.Series(equity_curve)
    returns = equity.pct_change().fillna(0)
    
    total_return = (equity.iloc[-1] / initial_capital) - 1
    days = len(equity)
    annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
    volatility = returns.std() * np.sqrt(252)
    sharpe = annual_return / volatility if volatility > 0 else 0
    
    peak = equity.cummax()
    drawdown = (equity - peak) / peak
    max_dd = abs(drawdown.min())
    
    calmar = annual_return / max_dd if max_dd > 0 else 0
    
    return {
        'metrics': {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'max_drawdown': max_dd,
            'volatility': volatility
        },
        'equity_curve': equity_curve,
        'trades': trades,
        'config': config
    }


def fast_grid_search(price_data: pd.DataFrame) -> dict:
    """快速网格搜索"""
    
    # 简化的参数网格
    param_grid = {
        'max_holdings': [2, 3, 5],
        'momentum_period': [10, 20],
        'rebalance_days': [3, 5],
        'stop_loss': [-0.08, -0.12],
        'take_profit': [0.50, 1.00],
    }
    
    from itertools import product
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total = 1
    for v in values:
        total *= len(v)
    
    logger.info(f"🔍 快速优化: {total}种组合")
    
    for idx, combo in enumerate(product(*values)):
        config = dict(zip(keys, combo))
        result = vectorized_backtest(price_data, config)
        
        results.append({
            'config': config,
            'sharpe': result['metrics']['sharpe_ratio'],
            'total_return': result['metrics']['total_return'],
            'annual_return': result['metrics']['annual_return'],
            'max_drawdown': result['metrics']['max_drawdown'],
            'calmar': result['metrics']['calmar_ratio']
        })
    
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_5': results[:5],
        'total_tested': len(results)
    }


def generate_report(result: dict, opt_result: dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        equity = result['equity_curve']
        
        axes[0].plot(equity, linewidth=2, color='#10b981')
        axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#10b981')
        axes[0].axhline(y=equity[0] * 2, color='gold', linestyle='--', label='2x Target')
        axes[0].set_title('Portfolio Value', fontweight='bold')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[1].set_title('Drawdown (%)', fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果
    opt_table = ""
    if opt_result and opt_result.get('top_5'):
        rows = ""
        for i, r in enumerate(opt_result['top_5']):
            rows += f"""<tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
            </tr>"""
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th></tr>
                {rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股快速优化报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #10b981, #059669); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #10b981; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #10b981; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(16,185,129,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ 十倍股快速优化策略</h1>
            <p>动量选股 + 向量化回测 + 参数优化</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">波动率</div>
                <div class="value">{metrics.get('volatility', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 最优参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>momentum_period</td><td>{config.get('momentum_period', 20)}</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.50)*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("⚡ 十倍股快速优化策略")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 获取股票池
    logger.info("📥 获取数据...")
    stocks = jq.get_index_stocks('399006.XSHE')[:50]  # 创业板50只
    stocks += jq.get_index_stocks('000905.XSHG')[:30]  # 中证500 30只
    stocks = list(set(stocks))
    
    logger.info(f"   股票池: {len(stocks)}只")
    
    # 加载数据
    price_data = jq.get_price(
        stocks,
        start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
        end_date=end_date,
        frequency='daily',
        fields=['close'],
        panel=False,
        skip_paused=True
    )
    
    logger.info(f"   数据行数: {len(price_data)}")
    
    # 网格搜索
    opt_result = fast_grid_search(price_data)
    
    if opt_result['best']:
        logger.info(f"✅ 最优参数: {opt_result['best']['config']}")
        logger.info(f"   夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   总收益: {opt_result['best']['total_return']*100:.2f}%")
        logger.info(f"   年化: {opt_result['best']['annual_return']*100:.2f}%")
        
        # 用最优参数运行
        best_result = vectorized_backtest(price_data, opt_result['best']['config'])
    else:
        best_result = vectorized_backtest(price_data, {})
    
    # 生成报告
    logger.info("📝 生成报告...")
    html = generate_report(best_result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_fast_optimize_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {best_result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {best_result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {best_result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return best_result


if __name__ == "__main__":
    main()









































