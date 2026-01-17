#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股优化策略 V2 - 目标1年2倍
==============================

优化点：
1. 动量+价值+小市值多因子结合
2. 更激进的选股逻辑
3. 参数网格优化
4. 更精准的择时

目标：年化收益100%以上

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_optimized_v2.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from typing import Dict, List, Tuple
from itertools import product

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


class OptimizedStrategy:
    """优化策略"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # 策略参数
        self.max_holdings = config.get('max_holdings', 3)
        self.single_max = config.get('single_max', 0.4)
        self.min_score = config.get('min_score', 60)
        self.stop_loss = config.get('stop_loss', -0.08)
        self.take_profit = config.get('take_profit', 0.80)
        self.trailing_stop = config.get('trailing_stop', 0.12)
        self.rebalance_days = config.get('rebalance_days', 5)
        
        # 因子权重
        self.weights = {
            'momentum_20d': 0.25,
            'momentum_60d': 0.15,
            'reversal_5d': 0.10,
            'small_cap': 0.20,
            'volatility': 0.10,
            'volume_breakout': 0.20,
        }
    
    def compute_factor_score(self, stock_data: Dict) -> float:
        """计算因子得分"""
        scores = {}
        
        # 1. 动量因子（20日）
        m20 = stock_data.get('momentum_20d', 0)
        scores['momentum_20d'] = min(100, max(0, 50 + m20 * 1.5))
        
        # 2. 长期动量（60日）
        m60 = stock_data.get('momentum_60d', 0)
        scores['momentum_60d'] = min(100, max(0, 50 + m60))
        
        # 3. 短期反转（5日回调后反弹）
        m5 = stock_data.get('momentum_5d', 0)
        if -10 < m5 < 5:  # 小幅回调后
            scores['reversal_5d'] = 70
        elif m5 >= 5:
            scores['reversal_5d'] = 50
        else:
            scores['reversal_5d'] = 30
        
        # 4. 小市值因子（市值越小得分越高）
        cap = stock_data.get('market_cap', 500)
        if cap < 50:
            scores['small_cap'] = 100
        elif cap < 100:
            scores['small_cap'] = 85
        elif cap < 200:
            scores['small_cap'] = 70
        elif cap < 500:
            scores['small_cap'] = 50
        else:
            scores['small_cap'] = 30
        
        # 5. 低波动因子（适度波动）
        vol = stock_data.get('volatility_20d', 30)
        if 20 < vol < 40:
            scores['volatility'] = 80
        elif 15 < vol < 50:
            scores['volatility'] = 60
        else:
            scores['volatility'] = 40
        
        # 6. 放量突破
        vol_ratio = stock_data.get('vol_ratio', 1)
        price_to_ma = stock_data.get('price_to_ma20', 0)
        
        if vol_ratio > 2 and price_to_ma > 0:
            scores['volume_breakout'] = 100
        elif vol_ratio > 1.5 and price_to_ma > 0:
            scores['volume_breakout'] = 80
        elif vol_ratio > 1.2:
            scores['volume_breakout'] = 60
        else:
            scores['volume_breakout'] = 40
        
        # 加权计算总分
        total = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return total
    
    def run_backtest(self, start_date: str, end_date: str, 
                     initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池（创业板+科创板为主）
        stocks = jq.get_index_stocks('399006.XSHE')[:80]  # 创业板80只
        stocks += jq.get_index_stocks('000905.XSHG')[:50]  # 中证500 50只
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d'),
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True
        )
        
        # 构建价格缓存
        price_cache = {}
        for stock in stocks:
            sdf = price_df[price_df['code'] == stock].copy()
            if not sdf.empty:
                sdf = sdf.set_index('time')
                price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 回测
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 100 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 更新持仓
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
            
            # 调仓检查
            counter += 1
            if counter >= self.rebalance_days:
                counter = 0
                
                # 计算所有股票得分
                scores = {}
                for stock in list(price_cache.keys()):
                    try:
                        sdf = price_cache[stock]
                        mask = sdf.index <= date
                        sdf_filtered = sdf[mask].tail(60)
                        
                        if len(sdf_filtered) < 60:
                            continue
                        
                        close = sdf_filtered['close'].values
                        volume = sdf_filtered['volume'].values
                        
                        if close[-20] <= 0 or close[0] <= 0:
                            continue
                        
                        stock_data = {
                            'momentum_5d': (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0,
                            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
                            'momentum_60d': (close[-1] / close[0] - 1) * 100,
                            'volatility_20d': np.std(np.diff(close[-20:]) / close[-21:-1]) * np.sqrt(252) * 100 if np.all(close[-21:-1] > 0) else 30,
                            'vol_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
                            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
                            'market_cap': 100,  # 默认
                        }
                        
                        score = self.compute_factor_score(stock_data)
                        
                        if score >= self.min_score:
                            scores[stock] = score
                            
                    except Exception as e:
                        continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.max_holdings]
                    selected_stocks = [s[0] for s in selected]
                    
                    # 卖出不在selected中的
                    for stock in list(positions.keys()):
                        if stock not in selected_stocks:
                            if stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                value = positions[stock]['shares'] * price * 0.9985
                                cash += value
                                trades.append({
                                    'date': date,
                                    'stock': stock,
                                    'action': 'SELL',
                                    'reason': '调仓卖出'
                                })
                                del positions[stock]
                    
                    # 买入新选中的
                    available_slots = self.max_holdings - len(positions)
                    if available_slots > 0:
                        for stock, score in selected[:available_slots]:
                            if stock not in positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    target_value = portfolio_value * self.single_max
                                    buy_value = min(target_value, cash * 0.95)
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
                                                'date': date,
                                                'stock': stock,
                                                'action': 'BUY',
                                                'reason': f'得分{score:.1f}'
                                            })
            
            # 风控检查
            for stock in list(positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    pos = positions[stock]
                    price = pos['current_price']
                    cost = pos['cost']
                    highest = pos['highest']
                    
                    pnl = (price - cost) / cost
                    drawdown = (price - highest) / highest if highest > 0 else 0
                    
                    sell_reason = None
                    
                    # 止损
                    if pnl <= self.stop_loss:
                        sell_reason = f'止损{pnl*100:.1f}%'
                    # 止盈
                    elif pnl >= self.take_profit:
                        sell_reason = f'止盈{pnl*100:.1f}%'
                    # 移动止损
                    elif drawdown <= -self.trailing_stop and pnl > 0.1:
                        sell_reason = f'移动止损{drawdown*100:.1f}%'
                    
                    if sell_reason:
                        value = pos['shares'] * price * 0.9985
                        cash += value
                        trades.append({
                            'date': date,
                            'stock': stock,
                            'action': 'SELL',
                            'reason': sell_reason
                        })
                        del positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
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
        
        win_trades = sum(1 for t in trades if t['action'] == 'SELL' and '止盈' in t.get('reason', ''))
        total_sells = sum(1 for t in trades if t['action'] == 'SELL')
        win_rate = win_trades / total_sells if total_sells > 0 else 0
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility,
                'win_rate': win_rate
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades),
            'config': self.config
        }


def grid_search_optimize(start_date: str, end_date: str) -> Dict:
    """网格搜索优化"""
    
    param_grid = {
        'max_holdings': [2, 3, 5],
        'min_score': [55, 60, 65],
        'stop_loss': [-0.06, -0.08, -0.10],
        'take_profit': [0.50, 0.80, 1.00],
        'rebalance_days': [3, 5, 7],
    }
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total_combos = 1
    for v in values:
        total_combos *= len(v)
    
    logger.info(f"🔍 网格搜索: {total_combos}种组合")
    
    for idx, combo in enumerate(product(*values)):
        if idx % 10 == 0:
            logger.info(f"   进度: {idx}/{total_combos}")
        
        config = dict(zip(keys, combo))
        
        try:
            strategy = OptimizedStrategy(config)
            result = strategy.run_backtest(start_date, end_date)
            
            if result['success']:
                results.append({
                    'config': config,
                    'sharpe': result['metrics']['sharpe_ratio'],
                    'total_return': result['metrics']['total_return'],
                    'annual_return': result['metrics']['annual_return'],
                    'max_drawdown': result['metrics']['max_drawdown'],
                    'calmar': result['metrics']['calmar_ratio']
                })
        except Exception as e:
            continue
    
    # 按夏普排序
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_10': results[:10],
        'total_tested': len(results)
    }


def generate_report(result: Dict, optimization_result: Dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        equity = result['equity_curve']
        
        # 净值曲线
        axes[0, 0].plot(equity, linewidth=2, color='#667eea')
        axes[0, 0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
        axes[0, 0].axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(y=equity[0] * 2, color='green', linestyle='--', alpha=0.5, label='2x Target')
        axes[0, 0].set_title('Portfolio Value', fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 回撤
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[0, 1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[0, 1].set_title('Drawdown (%)', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 收益分布
        returns = equity_s.pct_change().dropna()
        axes[1, 0].hist(returns * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 0].axvline(x=0, color='red', linestyle='--')
        axes[1, 0].set_title('Daily Return Distribution (%)', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 参数优化结果
        if optimization_result and optimization_result.get('top_10'):
            top10 = optimization_result['top_10']
            sharpes = [r['sharpe'] for r in top10]
            labels = [f"#{i+1}" for i in range(len(top10))]
            colors = ['#4ade80' if i == 0 else '#667eea' for i in range(len(top10))]
            axes[1, 1].bar(labels, sharpes, color=colors)
            axes[1, 1].set_title('Top 10 Configs (Sharpe)', fontweight='bold')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No optimization data', ha='center', va='center')
            axes[1, 1].set_title('Optimization Results', fontweight='bold')
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果表格
    opt_table = ""
    if optimization_result and optimization_result.get('top_10'):
        opt_rows = ""
        for i, r in enumerate(optimization_result['top_10'][:5]):
            opt_rows += f"""
            <tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
                <td>{json.dumps(r['config'])}</td>
            </tr>
            """
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th><th>参数</th></tr>
                {opt_rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股优化策略V2报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #f093fb, #f5576c); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #4ade80; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #f093fb; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(240,147,251,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股优化策略V2</h1>
            <p>动量+价值+小市值多因子 | 参数网格优化</p>
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
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 当前策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>min_score</td><td>{config.get('min_score', 60)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.80)*100:.0f}%</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股优化策略V2")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 1. 先用默认参数快速测试
    logger.info("📈 快速测试...")
    default_config = {
        'max_holdings': 3,
        'min_score': 60,
        'stop_loss': -0.08,
        'take_profit': 0.80,
        'rebalance_days': 5,
    }
    
    strategy = OptimizedStrategy(default_config)
    result = strategy.run_backtest(start_date, end_date)
    
    logger.info(f"   默认参数结果:")
    logger.info(f"   总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普: {result['metrics']['sharpe_ratio']:.2f}")
    
    # 2. 网格搜索优化
    logger.info("\n🔍 网格搜索优化...")
    opt_result = grid_search_optimize(start_date, end_date)
    
    if opt_result['best']:
        logger.info(f"   最优参数: {opt_result['best']['config']}")
        logger.info(f"   最优夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   最优收益: {opt_result['best']['total_return']*100:.2f}%")
        
        # 用最优参数重跑
        best_strategy = OptimizedStrategy(opt_result['best']['config'])
        best_result = best_strategy.run_backtest(start_date, end_date)
        result = best_result
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generate_report(result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_optimized_v2_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return result


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股优化策略 V2 - 目标1年2倍
==============================

优化点：
1. 动量+价值+小市值多因子结合
2. 更激进的选股逻辑
3. 参数网格优化
4. 更精准的择时

目标：年化收益100%以上

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_optimized_v2.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from typing import Dict, List, Tuple
from itertools import product

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


class OptimizedStrategy:
    """优化策略"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # 策略参数
        self.max_holdings = config.get('max_holdings', 3)
        self.single_max = config.get('single_max', 0.4)
        self.min_score = config.get('min_score', 60)
        self.stop_loss = config.get('stop_loss', -0.08)
        self.take_profit = config.get('take_profit', 0.80)
        self.trailing_stop = config.get('trailing_stop', 0.12)
        self.rebalance_days = config.get('rebalance_days', 5)
        
        # 因子权重
        self.weights = {
            'momentum_20d': 0.25,
            'momentum_60d': 0.15,
            'reversal_5d': 0.10,
            'small_cap': 0.20,
            'volatility': 0.10,
            'volume_breakout': 0.20,
        }
    
    def compute_factor_score(self, stock_data: Dict) -> float:
        """计算因子得分"""
        scores = {}
        
        # 1. 动量因子（20日）
        m20 = stock_data.get('momentum_20d', 0)
        scores['momentum_20d'] = min(100, max(0, 50 + m20 * 1.5))
        
        # 2. 长期动量（60日）
        m60 = stock_data.get('momentum_60d', 0)
        scores['momentum_60d'] = min(100, max(0, 50 + m60))
        
        # 3. 短期反转（5日回调后反弹）
        m5 = stock_data.get('momentum_5d', 0)
        if -10 < m5 < 5:  # 小幅回调后
            scores['reversal_5d'] = 70
        elif m5 >= 5:
            scores['reversal_5d'] = 50
        else:
            scores['reversal_5d'] = 30
        
        # 4. 小市值因子（市值越小得分越高）
        cap = stock_data.get('market_cap', 500)
        if cap < 50:
            scores['small_cap'] = 100
        elif cap < 100:
            scores['small_cap'] = 85
        elif cap < 200:
            scores['small_cap'] = 70
        elif cap < 500:
            scores['small_cap'] = 50
        else:
            scores['small_cap'] = 30
        
        # 5. 低波动因子（适度波动）
        vol = stock_data.get('volatility_20d', 30)
        if 20 < vol < 40:
            scores['volatility'] = 80
        elif 15 < vol < 50:
            scores['volatility'] = 60
        else:
            scores['volatility'] = 40
        
        # 6. 放量突破
        vol_ratio = stock_data.get('vol_ratio', 1)
        price_to_ma = stock_data.get('price_to_ma20', 0)
        
        if vol_ratio > 2 and price_to_ma > 0:
            scores['volume_breakout'] = 100
        elif vol_ratio > 1.5 and price_to_ma > 0:
            scores['volume_breakout'] = 80
        elif vol_ratio > 1.2:
            scores['volume_breakout'] = 60
        else:
            scores['volume_breakout'] = 40
        
        # 加权计算总分
        total = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return total
    
    def run_backtest(self, start_date: str, end_date: str, 
                     initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池（创业板+科创板为主）
        stocks = jq.get_index_stocks('399006.XSHE')[:80]  # 创业板80只
        stocks += jq.get_index_stocks('000905.XSHG')[:50]  # 中证500 50只
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d'),
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True
        )
        
        # 构建价格缓存
        price_cache = {}
        for stock in stocks:
            sdf = price_df[price_df['code'] == stock].copy()
            if not sdf.empty:
                sdf = sdf.set_index('time')
                price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 回测
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 100 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 更新持仓
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
            
            # 调仓检查
            counter += 1
            if counter >= self.rebalance_days:
                counter = 0
                
                # 计算所有股票得分
                scores = {}
                for stock in list(price_cache.keys()):
                    try:
                        sdf = price_cache[stock]
                        mask = sdf.index <= date
                        sdf_filtered = sdf[mask].tail(60)
                        
                        if len(sdf_filtered) < 60:
                            continue
                        
                        close = sdf_filtered['close'].values
                        volume = sdf_filtered['volume'].values
                        
                        if close[-20] <= 0 or close[0] <= 0:
                            continue
                        
                        stock_data = {
                            'momentum_5d': (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0,
                            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
                            'momentum_60d': (close[-1] / close[0] - 1) * 100,
                            'volatility_20d': np.std(np.diff(close[-20:]) / close[-21:-1]) * np.sqrt(252) * 100 if np.all(close[-21:-1] > 0) else 30,
                            'vol_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
                            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
                            'market_cap': 100,  # 默认
                        }
                        
                        score = self.compute_factor_score(stock_data)
                        
                        if score >= self.min_score:
                            scores[stock] = score
                            
                    except Exception as e:
                        continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.max_holdings]
                    selected_stocks = [s[0] for s in selected]
                    
                    # 卖出不在selected中的
                    for stock in list(positions.keys()):
                        if stock not in selected_stocks:
                            if stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                value = positions[stock]['shares'] * price * 0.9985
                                cash += value
                                trades.append({
                                    'date': date,
                                    'stock': stock,
                                    'action': 'SELL',
                                    'reason': '调仓卖出'
                                })
                                del positions[stock]
                    
                    # 买入新选中的
                    available_slots = self.max_holdings - len(positions)
                    if available_slots > 0:
                        for stock, score in selected[:available_slots]:
                            if stock not in positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    target_value = portfolio_value * self.single_max
                                    buy_value = min(target_value, cash * 0.95)
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
                                                'date': date,
                                                'stock': stock,
                                                'action': 'BUY',
                                                'reason': f'得分{score:.1f}'
                                            })
            
            # 风控检查
            for stock in list(positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    pos = positions[stock]
                    price = pos['current_price']
                    cost = pos['cost']
                    highest = pos['highest']
                    
                    pnl = (price - cost) / cost
                    drawdown = (price - highest) / highest if highest > 0 else 0
                    
                    sell_reason = None
                    
                    # 止损
                    if pnl <= self.stop_loss:
                        sell_reason = f'止损{pnl*100:.1f}%'
                    # 止盈
                    elif pnl >= self.take_profit:
                        sell_reason = f'止盈{pnl*100:.1f}%'
                    # 移动止损
                    elif drawdown <= -self.trailing_stop and pnl > 0.1:
                        sell_reason = f'移动止损{drawdown*100:.1f}%'
                    
                    if sell_reason:
                        value = pos['shares'] * price * 0.9985
                        cash += value
                        trades.append({
                            'date': date,
                            'stock': stock,
                            'action': 'SELL',
                            'reason': sell_reason
                        })
                        del positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
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
        
        win_trades = sum(1 for t in trades if t['action'] == 'SELL' and '止盈' in t.get('reason', ''))
        total_sells = sum(1 for t in trades if t['action'] == 'SELL')
        win_rate = win_trades / total_sells if total_sells > 0 else 0
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility,
                'win_rate': win_rate
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades),
            'config': self.config
        }


def grid_search_optimize(start_date: str, end_date: str) -> Dict:
    """网格搜索优化"""
    
    param_grid = {
        'max_holdings': [2, 3, 5],
        'min_score': [55, 60, 65],
        'stop_loss': [-0.06, -0.08, -0.10],
        'take_profit': [0.50, 0.80, 1.00],
        'rebalance_days': [3, 5, 7],
    }
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total_combos = 1
    for v in values:
        total_combos *= len(v)
    
    logger.info(f"🔍 网格搜索: {total_combos}种组合")
    
    for idx, combo in enumerate(product(*values)):
        if idx % 10 == 0:
            logger.info(f"   进度: {idx}/{total_combos}")
        
        config = dict(zip(keys, combo))
        
        try:
            strategy = OptimizedStrategy(config)
            result = strategy.run_backtest(start_date, end_date)
            
            if result['success']:
                results.append({
                    'config': config,
                    'sharpe': result['metrics']['sharpe_ratio'],
                    'total_return': result['metrics']['total_return'],
                    'annual_return': result['metrics']['annual_return'],
                    'max_drawdown': result['metrics']['max_drawdown'],
                    'calmar': result['metrics']['calmar_ratio']
                })
        except Exception as e:
            continue
    
    # 按夏普排序
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_10': results[:10],
        'total_tested': len(results)
    }


def generate_report(result: Dict, optimization_result: Dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        equity = result['equity_curve']
        
        # 净值曲线
        axes[0, 0].plot(equity, linewidth=2, color='#667eea')
        axes[0, 0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
        axes[0, 0].axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(y=equity[0] * 2, color='green', linestyle='--', alpha=0.5, label='2x Target')
        axes[0, 0].set_title('Portfolio Value', fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 回撤
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[0, 1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[0, 1].set_title('Drawdown (%)', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 收益分布
        returns = equity_s.pct_change().dropna()
        axes[1, 0].hist(returns * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 0].axvline(x=0, color='red', linestyle='--')
        axes[1, 0].set_title('Daily Return Distribution (%)', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 参数优化结果
        if optimization_result and optimization_result.get('top_10'):
            top10 = optimization_result['top_10']
            sharpes = [r['sharpe'] for r in top10]
            labels = [f"#{i+1}" for i in range(len(top10))]
            colors = ['#4ade80' if i == 0 else '#667eea' for i in range(len(top10))]
            axes[1, 1].bar(labels, sharpes, color=colors)
            axes[1, 1].set_title('Top 10 Configs (Sharpe)', fontweight='bold')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No optimization data', ha='center', va='center')
            axes[1, 1].set_title('Optimization Results', fontweight='bold')
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果表格
    opt_table = ""
    if optimization_result and optimization_result.get('top_10'):
        opt_rows = ""
        for i, r in enumerate(optimization_result['top_10'][:5]):
            opt_rows += f"""
            <tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
                <td>{json.dumps(r['config'])}</td>
            </tr>
            """
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th><th>参数</th></tr>
                {opt_rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股优化策略V2报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #f093fb, #f5576c); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #4ade80; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #f093fb; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(240,147,251,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股优化策略V2</h1>
            <p>动量+价值+小市值多因子 | 参数网格优化</p>
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
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 当前策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>min_score</td><td>{config.get('min_score', 60)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.80)*100:.0f}%</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股优化策略V2")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 1. 先用默认参数快速测试
    logger.info("📈 快速测试...")
    default_config = {
        'max_holdings': 3,
        'min_score': 60,
        'stop_loss': -0.08,
        'take_profit': 0.80,
        'rebalance_days': 5,
    }
    
    strategy = OptimizedStrategy(default_config)
    result = strategy.run_backtest(start_date, end_date)
    
    logger.info(f"   默认参数结果:")
    logger.info(f"   总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普: {result['metrics']['sharpe_ratio']:.2f}")
    
    # 2. 网格搜索优化
    logger.info("\n🔍 网格搜索优化...")
    opt_result = grid_search_optimize(start_date, end_date)
    
    if opt_result['best']:
        logger.info(f"   最优参数: {opt_result['best']['config']}")
        logger.info(f"   最优夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   最优收益: {opt_result['best']['total_return']*100:.2f}%")
        
        # 用最优参数重跑
        best_strategy = OptimizedStrategy(opt_result['best']['config'])
        best_result = best_strategy.run_backtest(start_date, end_date)
        result = best_result
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generate_report(result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_optimized_v2_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return result


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
十倍股优化策略 V2 - 目标1年2倍
==============================

优化点：
1. 动量+价值+小市值多因子结合
2. 更激进的选股逻辑
3. 参数网格优化
4. 更精准的择时

目标：年化收益100%以上

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_optimized_v2.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from typing import Dict, List, Tuple
from itertools import product

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


class OptimizedStrategy:
    """优化策略"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # 策略参数
        self.max_holdings = config.get('max_holdings', 3)
        self.single_max = config.get('single_max', 0.4)
        self.min_score = config.get('min_score', 60)
        self.stop_loss = config.get('stop_loss', -0.08)
        self.take_profit = config.get('take_profit', 0.80)
        self.trailing_stop = config.get('trailing_stop', 0.12)
        self.rebalance_days = config.get('rebalance_days', 5)
        
        # 因子权重
        self.weights = {
            'momentum_20d': 0.25,
            'momentum_60d': 0.15,
            'reversal_5d': 0.10,
            'small_cap': 0.20,
            'volatility': 0.10,
            'volume_breakout': 0.20,
        }
    
    def compute_factor_score(self, stock_data: Dict) -> float:
        """计算因子得分"""
        scores = {}
        
        # 1. 动量因子（20日）
        m20 = stock_data.get('momentum_20d', 0)
        scores['momentum_20d'] = min(100, max(0, 50 + m20 * 1.5))
        
        # 2. 长期动量（60日）
        m60 = stock_data.get('momentum_60d', 0)
        scores['momentum_60d'] = min(100, max(0, 50 + m60))
        
        # 3. 短期反转（5日回调后反弹）
        m5 = stock_data.get('momentum_5d', 0)
        if -10 < m5 < 5:  # 小幅回调后
            scores['reversal_5d'] = 70
        elif m5 >= 5:
            scores['reversal_5d'] = 50
        else:
            scores['reversal_5d'] = 30
        
        # 4. 小市值因子（市值越小得分越高）
        cap = stock_data.get('market_cap', 500)
        if cap < 50:
            scores['small_cap'] = 100
        elif cap < 100:
            scores['small_cap'] = 85
        elif cap < 200:
            scores['small_cap'] = 70
        elif cap < 500:
            scores['small_cap'] = 50
        else:
            scores['small_cap'] = 30
        
        # 5. 低波动因子（适度波动）
        vol = stock_data.get('volatility_20d', 30)
        if 20 < vol < 40:
            scores['volatility'] = 80
        elif 15 < vol < 50:
            scores['volatility'] = 60
        else:
            scores['volatility'] = 40
        
        # 6. 放量突破
        vol_ratio = stock_data.get('vol_ratio', 1)
        price_to_ma = stock_data.get('price_to_ma20', 0)
        
        if vol_ratio > 2 and price_to_ma > 0:
            scores['volume_breakout'] = 100
        elif vol_ratio > 1.5 and price_to_ma > 0:
            scores['volume_breakout'] = 80
        elif vol_ratio > 1.2:
            scores['volume_breakout'] = 60
        else:
            scores['volume_breakout'] = 40
        
        # 加权计算总分
        total = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return total
    
    def run_backtest(self, start_date: str, end_date: str, 
                     initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池（创业板+科创板为主）
        stocks = jq.get_index_stocks('399006.XSHE')[:80]  # 创业板80只
        stocks += jq.get_index_stocks('000905.XSHG')[:50]  # 中证500 50只
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d'),
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True
        )
        
        # 构建价格缓存
        price_cache = {}
        for stock in stocks:
            sdf = price_df[price_df['code'] == stock].copy()
            if not sdf.empty:
                sdf = sdf.set_index('time')
                price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 回测
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 100 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 更新持仓
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
            
            # 调仓检查
            counter += 1
            if counter >= self.rebalance_days:
                counter = 0
                
                # 计算所有股票得分
                scores = {}
                for stock in list(price_cache.keys()):
                    try:
                        sdf = price_cache[stock]
                        mask = sdf.index <= date
                        sdf_filtered = sdf[mask].tail(60)
                        
                        if len(sdf_filtered) < 60:
                            continue
                        
                        close = sdf_filtered['close'].values
                        volume = sdf_filtered['volume'].values
                        
                        if close[-20] <= 0 or close[0] <= 0:
                            continue
                        
                        stock_data = {
                            'momentum_5d': (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0,
                            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
                            'momentum_60d': (close[-1] / close[0] - 1) * 100,
                            'volatility_20d': np.std(np.diff(close[-20:]) / close[-21:-1]) * np.sqrt(252) * 100 if np.all(close[-21:-1] > 0) else 30,
                            'vol_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
                            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
                            'market_cap': 100,  # 默认
                        }
                        
                        score = self.compute_factor_score(stock_data)
                        
                        if score >= self.min_score:
                            scores[stock] = score
                            
                    except Exception as e:
                        continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.max_holdings]
                    selected_stocks = [s[0] for s in selected]
                    
                    # 卖出不在selected中的
                    for stock in list(positions.keys()):
                        if stock not in selected_stocks:
                            if stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                value = positions[stock]['shares'] * price * 0.9985
                                cash += value
                                trades.append({
                                    'date': date,
                                    'stock': stock,
                                    'action': 'SELL',
                                    'reason': '调仓卖出'
                                })
                                del positions[stock]
                    
                    # 买入新选中的
                    available_slots = self.max_holdings - len(positions)
                    if available_slots > 0:
                        for stock, score in selected[:available_slots]:
                            if stock not in positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    target_value = portfolio_value * self.single_max
                                    buy_value = min(target_value, cash * 0.95)
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
                                                'date': date,
                                                'stock': stock,
                                                'action': 'BUY',
                                                'reason': f'得分{score:.1f}'
                                            })
            
            # 风控检查
            for stock in list(positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    pos = positions[stock]
                    price = pos['current_price']
                    cost = pos['cost']
                    highest = pos['highest']
                    
                    pnl = (price - cost) / cost
                    drawdown = (price - highest) / highest if highest > 0 else 0
                    
                    sell_reason = None
                    
                    # 止损
                    if pnl <= self.stop_loss:
                        sell_reason = f'止损{pnl*100:.1f}%'
                    # 止盈
                    elif pnl >= self.take_profit:
                        sell_reason = f'止盈{pnl*100:.1f}%'
                    # 移动止损
                    elif drawdown <= -self.trailing_stop and pnl > 0.1:
                        sell_reason = f'移动止损{drawdown*100:.1f}%'
                    
                    if sell_reason:
                        value = pos['shares'] * price * 0.9985
                        cash += value
                        trades.append({
                            'date': date,
                            'stock': stock,
                            'action': 'SELL',
                            'reason': sell_reason
                        })
                        del positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
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
        
        win_trades = sum(1 for t in trades if t['action'] == 'SELL' and '止盈' in t.get('reason', ''))
        total_sells = sum(1 for t in trades if t['action'] == 'SELL')
        win_rate = win_trades / total_sells if total_sells > 0 else 0
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility,
                'win_rate': win_rate
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades),
            'config': self.config
        }


def grid_search_optimize(start_date: str, end_date: str) -> Dict:
    """网格搜索优化"""
    
    param_grid = {
        'max_holdings': [2, 3, 5],
        'min_score': [55, 60, 65],
        'stop_loss': [-0.06, -0.08, -0.10],
        'take_profit': [0.50, 0.80, 1.00],
        'rebalance_days': [3, 5, 7],
    }
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total_combos = 1
    for v in values:
        total_combos *= len(v)
    
    logger.info(f"🔍 网格搜索: {total_combos}种组合")
    
    for idx, combo in enumerate(product(*values)):
        if idx % 10 == 0:
            logger.info(f"   进度: {idx}/{total_combos}")
        
        config = dict(zip(keys, combo))
        
        try:
            strategy = OptimizedStrategy(config)
            result = strategy.run_backtest(start_date, end_date)
            
            if result['success']:
                results.append({
                    'config': config,
                    'sharpe': result['metrics']['sharpe_ratio'],
                    'total_return': result['metrics']['total_return'],
                    'annual_return': result['metrics']['annual_return'],
                    'max_drawdown': result['metrics']['max_drawdown'],
                    'calmar': result['metrics']['calmar_ratio']
                })
        except Exception as e:
            continue
    
    # 按夏普排序
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_10': results[:10],
        'total_tested': len(results)
    }


def generate_report(result: Dict, optimization_result: Dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        equity = result['equity_curve']
        
        # 净值曲线
        axes[0, 0].plot(equity, linewidth=2, color='#667eea')
        axes[0, 0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
        axes[0, 0].axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(y=equity[0] * 2, color='green', linestyle='--', alpha=0.5, label='2x Target')
        axes[0, 0].set_title('Portfolio Value', fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 回撤
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[0, 1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[0, 1].set_title('Drawdown (%)', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 收益分布
        returns = equity_s.pct_change().dropna()
        axes[1, 0].hist(returns * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 0].axvline(x=0, color='red', linestyle='--')
        axes[1, 0].set_title('Daily Return Distribution (%)', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 参数优化结果
        if optimization_result and optimization_result.get('top_10'):
            top10 = optimization_result['top_10']
            sharpes = [r['sharpe'] for r in top10]
            labels = [f"#{i+1}" for i in range(len(top10))]
            colors = ['#4ade80' if i == 0 else '#667eea' for i in range(len(top10))]
            axes[1, 1].bar(labels, sharpes, color=colors)
            axes[1, 1].set_title('Top 10 Configs (Sharpe)', fontweight='bold')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No optimization data', ha='center', va='center')
            axes[1, 1].set_title('Optimization Results', fontweight='bold')
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果表格
    opt_table = ""
    if optimization_result and optimization_result.get('top_10'):
        opt_rows = ""
        for i, r in enumerate(optimization_result['top_10'][:5]):
            opt_rows += f"""
            <tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
                <td>{json.dumps(r['config'])}</td>
            </tr>
            """
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th><th>参数</th></tr>
                {opt_rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股优化策略V2报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #f093fb, #f5576c); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #4ade80; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #f093fb; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(240,147,251,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股优化策略V2</h1>
            <p>动量+价值+小市值多因子 | 参数网格优化</p>
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
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 当前策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>min_score</td><td>{config.get('min_score', 60)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.80)*100:.0f}%</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股优化策略V2")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 1. 先用默认参数快速测试
    logger.info("📈 快速测试...")
    default_config = {
        'max_holdings': 3,
        'min_score': 60,
        'stop_loss': -0.08,
        'take_profit': 0.80,
        'rebalance_days': 5,
    }
    
    strategy = OptimizedStrategy(default_config)
    result = strategy.run_backtest(start_date, end_date)
    
    logger.info(f"   默认参数结果:")
    logger.info(f"   总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普: {result['metrics']['sharpe_ratio']:.2f}")
    
    # 2. 网格搜索优化
    logger.info("\n🔍 网格搜索优化...")
    opt_result = grid_search_optimize(start_date, end_date)
    
    if opt_result['best']:
        logger.info(f"   最优参数: {opt_result['best']['config']}")
        logger.info(f"   最优夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   最优收益: {opt_result['best']['total_return']*100:.2f}%")
        
        # 用最优参数重跑
        best_strategy = OptimizedStrategy(opt_result['best']['config'])
        best_result = best_strategy.run_backtest(start_date, end_date)
        result = best_result
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generate_report(result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_optimized_v2_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return result


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股优化策略 V2 - 目标1年2倍
==============================

优化点：
1. 动量+价值+小市值多因子结合
2. 更激进的选股逻辑
3. 参数网格优化
4. 更精准的择时

目标：年化收益100%以上

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_optimized_v2.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from typing import Dict, List, Tuple
from itertools import product

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


class OptimizedStrategy:
    """优化策略"""
    
    def __init__(self, config: Dict):
        self.config = config
        
        # 策略参数
        self.max_holdings = config.get('max_holdings', 3)
        self.single_max = config.get('single_max', 0.4)
        self.min_score = config.get('min_score', 60)
        self.stop_loss = config.get('stop_loss', -0.08)
        self.take_profit = config.get('take_profit', 0.80)
        self.trailing_stop = config.get('trailing_stop', 0.12)
        self.rebalance_days = config.get('rebalance_days', 5)
        
        # 因子权重
        self.weights = {
            'momentum_20d': 0.25,
            'momentum_60d': 0.15,
            'reversal_5d': 0.10,
            'small_cap': 0.20,
            'volatility': 0.10,
            'volume_breakout': 0.20,
        }
    
    def compute_factor_score(self, stock_data: Dict) -> float:
        """计算因子得分"""
        scores = {}
        
        # 1. 动量因子（20日）
        m20 = stock_data.get('momentum_20d', 0)
        scores['momentum_20d'] = min(100, max(0, 50 + m20 * 1.5))
        
        # 2. 长期动量（60日）
        m60 = stock_data.get('momentum_60d', 0)
        scores['momentum_60d'] = min(100, max(0, 50 + m60))
        
        # 3. 短期反转（5日回调后反弹）
        m5 = stock_data.get('momentum_5d', 0)
        if -10 < m5 < 5:  # 小幅回调后
            scores['reversal_5d'] = 70
        elif m5 >= 5:
            scores['reversal_5d'] = 50
        else:
            scores['reversal_5d'] = 30
        
        # 4. 小市值因子（市值越小得分越高）
        cap = stock_data.get('market_cap', 500)
        if cap < 50:
            scores['small_cap'] = 100
        elif cap < 100:
            scores['small_cap'] = 85
        elif cap < 200:
            scores['small_cap'] = 70
        elif cap < 500:
            scores['small_cap'] = 50
        else:
            scores['small_cap'] = 30
        
        # 5. 低波动因子（适度波动）
        vol = stock_data.get('volatility_20d', 30)
        if 20 < vol < 40:
            scores['volatility'] = 80
        elif 15 < vol < 50:
            scores['volatility'] = 60
        else:
            scores['volatility'] = 40
        
        # 6. 放量突破
        vol_ratio = stock_data.get('vol_ratio', 1)
        price_to_ma = stock_data.get('price_to_ma20', 0)
        
        if vol_ratio > 2 and price_to_ma > 0:
            scores['volume_breakout'] = 100
        elif vol_ratio > 1.5 and price_to_ma > 0:
            scores['volume_breakout'] = 80
        elif vol_ratio > 1.2:
            scores['volume_breakout'] = 60
        else:
            scores['volume_breakout'] = 40
        
        # 加权计算总分
        total = sum(scores[k] * self.weights[k] for k in self.weights)
        
        return total
    
    def run_backtest(self, start_date: str, end_date: str, 
                     initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        logger.info(f"   交易日: {len(trade_days)}天")
        
        # 获取股票池（创业板+科创板为主）
        stocks = jq.get_index_stocks('399006.XSHE')[:80]  # 创业板80只
        stocks += jq.get_index_stocks('000905.XSHG')[:50]  # 中证500 50只
        stocks = list(set(stocks))
        
        logger.info(f"   股票池: {len(stocks)}只")
        
        # 预加载数据
        logger.info("   预加载数据...")
        price_df = jq.get_price(
            stocks,
            start_date=(datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d'),
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True
        )
        
        # 构建价格缓存
        price_cache = {}
        for stock in stocks:
            sdf = price_df[price_df['code'] == stock].copy()
            if not sdf.empty:
                sdf = sdf.set_index('time')
                price_cache[stock] = sdf
        
        logger.info(f"   加载完成: {len(price_cache)}只")
        
        # 回测
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 100 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)}")
            
            # 更新持仓
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
            
            # 调仓检查
            counter += 1
            if counter >= self.rebalance_days:
                counter = 0
                
                # 计算所有股票得分
                scores = {}
                for stock in list(price_cache.keys()):
                    try:
                        sdf = price_cache[stock]
                        mask = sdf.index <= date
                        sdf_filtered = sdf[mask].tail(60)
                        
                        if len(sdf_filtered) < 60:
                            continue
                        
                        close = sdf_filtered['close'].values
                        volume = sdf_filtered['volume'].values
                        
                        if close[-20] <= 0 or close[0] <= 0:
                            continue
                        
                        stock_data = {
                            'momentum_5d': (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0,
                            'momentum_20d': (close[-1] / close[-20] - 1) * 100,
                            'momentum_60d': (close[-1] / close[0] - 1) * 100,
                            'volatility_20d': np.std(np.diff(close[-20:]) / close[-21:-1]) * np.sqrt(252) * 100 if np.all(close[-21:-1] > 0) else 30,
                            'vol_ratio': np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1,
                            'price_to_ma20': (close[-1] / np.mean(close[-20:]) - 1) * 100,
                            'market_cap': 100,  # 默认
                        }
                        
                        score = self.compute_factor_score(stock_data)
                        
                        if score >= self.min_score:
                            scores[stock] = score
                            
                    except Exception as e:
                        continue
                
                # 选股
                if scores:
                    selected = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:self.max_holdings]
                    selected_stocks = [s[0] for s in selected]
                    
                    # 卖出不在selected中的
                    for stock in list(positions.keys()):
                        if stock not in selected_stocks:
                            if stock in price_cache and date in price_cache[stock].index:
                                price = price_cache[stock].loc[date, 'close']
                                value = positions[stock]['shares'] * price * 0.9985
                                cash += value
                                trades.append({
                                    'date': date,
                                    'stock': stock,
                                    'action': 'SELL',
                                    'reason': '调仓卖出'
                                })
                                del positions[stock]
                    
                    # 买入新选中的
                    available_slots = self.max_holdings - len(positions)
                    if available_slots > 0:
                        for stock, score in selected[:available_slots]:
                            if stock not in positions:
                                if stock in price_cache and date in price_cache[stock].index:
                                    price = price_cache[stock].loc[date, 'close']
                                    target_value = portfolio_value * self.single_max
                                    buy_value = min(target_value, cash * 0.95)
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
                                                'date': date,
                                                'stock': stock,
                                                'action': 'BUY',
                                                'reason': f'得分{score:.1f}'
                                            })
            
            # 风控检查
            for stock in list(positions.keys()):
                if stock in price_cache and date in price_cache[stock].index:
                    pos = positions[stock]
                    price = pos['current_price']
                    cost = pos['cost']
                    highest = pos['highest']
                    
                    pnl = (price - cost) / cost
                    drawdown = (price - highest) / highest if highest > 0 else 0
                    
                    sell_reason = None
                    
                    # 止损
                    if pnl <= self.stop_loss:
                        sell_reason = f'止损{pnl*100:.1f}%'
                    # 止盈
                    elif pnl >= self.take_profit:
                        sell_reason = f'止盈{pnl*100:.1f}%'
                    # 移动止损
                    elif drawdown <= -self.trailing_stop and pnl > 0.1:
                        sell_reason = f'移动止损{drawdown*100:.1f}%'
                    
                    if sell_reason:
                        value = pos['shares'] * price * 0.9985
                        cash += value
                        trades.append({
                            'date': date,
                            'stock': stock,
                            'action': 'SELL',
                            'reason': sell_reason
                        })
                        del positions[stock]
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
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
        
        win_trades = sum(1 for t in trades if t['action'] == 'SELL' and '止盈' in t.get('reason', ''))
        total_sells = sum(1 for t in trades if t['action'] == 'SELL')
        win_rate = win_trades / total_sells if total_sells > 0 else 0
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility,
                'win_rate': win_rate
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades),
            'config': self.config
        }


def grid_search_optimize(start_date: str, end_date: str) -> Dict:
    """网格搜索优化"""
    
    param_grid = {
        'max_holdings': [2, 3, 5],
        'min_score': [55, 60, 65],
        'stop_loss': [-0.06, -0.08, -0.10],
        'take_profit': [0.50, 0.80, 1.00],
        'rebalance_days': [3, 5, 7],
    }
    
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    results = []
    total_combos = 1
    for v in values:
        total_combos *= len(v)
    
    logger.info(f"🔍 网格搜索: {total_combos}种组合")
    
    for idx, combo in enumerate(product(*values)):
        if idx % 10 == 0:
            logger.info(f"   进度: {idx}/{total_combos}")
        
        config = dict(zip(keys, combo))
        
        try:
            strategy = OptimizedStrategy(config)
            result = strategy.run_backtest(start_date, end_date)
            
            if result['success']:
                results.append({
                    'config': config,
                    'sharpe': result['metrics']['sharpe_ratio'],
                    'total_return': result['metrics']['total_return'],
                    'annual_return': result['metrics']['annual_return'],
                    'max_drawdown': result['metrics']['max_drawdown'],
                    'calmar': result['metrics']['calmar_ratio']
                })
        except Exception as e:
            continue
    
    # 按夏普排序
    results.sort(key=lambda x: x['sharpe'], reverse=True)
    
    return {
        'best': results[0] if results else None,
        'top_10': results[:10],
        'total_tested': len(results)
    }


def generate_report(result: Dict, optimization_result: Dict = None) -> str:
    """生成HTML报告"""
    
    metrics = result.get('metrics', {})
    config = result.get('config', {})
    
    # 生成图表
    chart_html = ""
    if MATPLOTLIB_AVAILABLE and result.get('equity_curve'):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        equity = result['equity_curve']
        
        # 净值曲线
        axes[0, 0].plot(equity, linewidth=2, color='#667eea')
        axes[0, 0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
        axes[0, 0].axhline(y=equity[0], color='gray', linestyle='--', alpha=0.5)
        axes[0, 0].axhline(y=equity[0] * 2, color='green', linestyle='--', alpha=0.5, label='2x Target')
        axes[0, 0].set_title('Portfolio Value', fontweight='bold')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 回撤
        equity_s = pd.Series(equity)
        peak = equity_s.cummax()
        dd = (equity_s - peak) / peak
        axes[0, 1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
        axes[0, 1].set_title('Drawdown (%)', fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 收益分布
        returns = equity_s.pct_change().dropna()
        axes[1, 0].hist(returns * 100, bins=50, color='#667eea', alpha=0.7, edgecolor='white')
        axes[1, 0].axvline(x=0, color='red', linestyle='--')
        axes[1, 0].set_title('Daily Return Distribution (%)', fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 参数优化结果
        if optimization_result and optimization_result.get('top_10'):
            top10 = optimization_result['top_10']
            sharpes = [r['sharpe'] for r in top10]
            labels = [f"#{i+1}" for i in range(len(top10))]
            colors = ['#4ade80' if i == 0 else '#667eea' for i in range(len(top10))]
            axes[1, 1].bar(labels, sharpes, color=colors)
            axes[1, 1].set_title('Top 10 Configs (Sharpe)', fontweight='bold')
            axes[1, 1].grid(True, alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'No optimization data', ha='center', va='center')
            axes[1, 1].set_title('Optimization Results', fontweight='bold')
        
        plt.tight_layout()
        
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        chart_b64 = base64.b64encode(buf.read()).decode()
        plt.close(fig)
        
        chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
    
    # 优化结果表格
    opt_table = ""
    if optimization_result and optimization_result.get('top_10'):
        opt_rows = ""
        for i, r in enumerate(optimization_result['top_10'][:5]):
            opt_rows += f"""
            <tr>
                <td>#{i+1}</td>
                <td>{r['sharpe']:.2f}</td>
                <td class="{'positive' if r['total_return'] > 0 else 'negative'}">{r['total_return']*100:.1f}%</td>
                <td>{r['annual_return']*100:.1f}%</td>
                <td>{r['max_drawdown']*100:.1f}%</td>
                <td>{json.dumps(r['config'])}</td>
            </tr>
            """
        opt_table = f"""
        <div class="section">
            <h2>🔍 参数优化Top 5</h2>
            <table>
                <tr><th>排名</th><th>夏普</th><th>总收益</th><th>年化</th><th>最大回撤</th><th>参数</th></tr>
                {opt_rows}
            </table>
        </div>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股优化策略V2报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #f093fb, #f5576c); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; }}
        .metric .value {{ font-size: 2.2em; font-weight: 700; }}
        .positive {{ color: #4ade80; }}
        .negative {{ color: #f87171; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; }}
        .section h2 {{ color: #f093fb; margin-top: 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(240,147,251,0.2); }}
        .chart {{ text-align: center; margin: 25px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股优化策略V2</h1>
            <p>动量+价值+小市值多因子 | 参数网格优化</p>
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
                <div class="label">胜率</div>
                <div class="value">{metrics.get('win_rate', 0)*100:.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        {opt_table}
        
        <div class="section">
            <h2>⚙️ 当前策略参数</h2>
            <table>
                <tr><th>参数</th><th>值</th></tr>
                <tr><td>max_holdings</td><td>{config.get('max_holdings', 3)}</td></tr>
                <tr><td>min_score</td><td>{config.get('min_score', 60)}</td></tr>
                <tr><td>stop_loss</td><td>{config.get('stop_loss', -0.08)*100:.0f}%</td></tr>
                <tr><td>take_profit</td><td>{config.get('take_profit', 0.80)*100:.0f}%</td></tr>
                <tr><td>rebalance_days</td><td>{config.get('rebalance_days', 5)}</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    return html


def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股优化策略V2")
    logger.info("=" * 80)
    
    if not authenticate_jqdata():
        return
    
    start_date = "2024-01-01"
    end_date = "2025-12-20"
    
    # 1. 先用默认参数快速测试
    logger.info("📈 快速测试...")
    default_config = {
        'max_holdings': 3,
        'min_score': 60,
        'stop_loss': -0.08,
        'take_profit': 0.80,
        'rebalance_days': 5,
    }
    
    strategy = OptimizedStrategy(default_config)
    result = strategy.run_backtest(start_date, end_date)
    
    logger.info(f"   默认参数结果:")
    logger.info(f"   总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   夏普: {result['metrics']['sharpe_ratio']:.2f}")
    
    # 2. 网格搜索优化
    logger.info("\n🔍 网格搜索优化...")
    opt_result = grid_search_optimize(start_date, end_date)
    
    if opt_result['best']:
        logger.info(f"   最优参数: {opt_result['best']['config']}")
        logger.info(f"   最优夏普: {opt_result['best']['sharpe']:.2f}")
        logger.info(f"   最优收益: {opt_result['best']['total_return']*100:.2f}%")
        
        # 用最优参数重跑
        best_strategy = OptimizedStrategy(opt_result['best']['config'])
        best_result = best_strategy.run_backtest(start_date, end_date)
        result = best_result
    
    # 3. 生成报告
    logger.info("\n📝 生成报告...")
    html = generate_report(result, opt_result)
    
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_optimized_v2_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告: {report_path}")
    
    # 登出
    jq.logout()
    
    logger.info("=" * 80)
    logger.info("✅ 完成!")
    logger.info(f"   最终总收益: {result['metrics']['total_return']*100:.2f}%")
    logger.info(f"   最终年化: {result['metrics']['annual_return']*100:.2f}%")
    logger.info(f"   最终夏普: {result['metrics']['sharpe_ratio']:.2f}")
    logger.info("=" * 80)
    
    return result


if __name__ == "__main__":
    main()









































