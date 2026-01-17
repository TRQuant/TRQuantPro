#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成策略代码页HTML"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

# 核心策略代码
CORE_STRATEGY_CODE = '''def vectorized_backtest(price_data: pd.DataFrame, config: dict) -> dict:
    """
    向量化回测引擎 - 十倍股动量策略核心实现
    
    策略逻辑：
    1. 每个调仓日计算所有股票的N日动量（收益率）
    2. 选择动量排名Top K的股票作为持仓标的
    3. 等权重分配资金，买入选中股票
    4. 执行止损止盈风控规则
    
    Parameters:
    -----------
    price_data : pd.DataFrame
        股票价格数据，包含 time, code, close 列
    config : dict
        策略参数配置
        - max_holdings: 最大持仓数量
        - momentum_period: 动量计算周期
        - rebalance_days: 调仓频率（天）
        - stop_loss: 止损线（负数）
        - take_profit: 止盈线（正数）
    
    Returns:
    --------
    dict: 回测结果，包含指标、净值曲线、交易记录
    """
    max_holdings = config.get('max_holdings', 2)
    momentum_period = config.get('momentum_period', 20)
    rebalance_days = config.get('rebalance_days', 3)
    stop_loss = config.get('stop_loss', -0.08)
    take_profit = config.get('take_profit', 0.50)
    
    # 转换为宽表格式
    close_df = price_data.pivot(index='time', columns='code', values='close')
    
    # 计算动量因子: Momentum = P(t) / P(t-N) - 1
    momentum = close_df.pct_change(momentum_period)
    
    dates = close_df.index
    initial_capital = 1_000_000  # 初始资金100万
    cash = initial_capital
    positions = {}  # 当前持仓 {stock: {shares, cost, highest}}
    equity_curve = []
    trades = []
    
    for i, date in enumerate(dates):
        # 1. 更新持仓市值和最高价
        portfolio_value = cash
        for stock, pos in positions.items():
            if stock in close_df.columns:
                price = close_df.loc[date, stock]
                if not pd.isna(price):
                    pos['current_price'] = price
                    pos['highest'] = max(pos.get('highest', price), price)
                    portfolio_value += pos['shares'] * price
        
        # 2. 执行止损止盈
        for stock in list(positions.keys()):
            pos = positions[stock]
            if 'current_price' not in pos:
                continue
            
            ret = pos['current_price'] / pos['cost'] - 1
            
            # 止损检查
            if ret <= stop_loss:
                cash += pos['shares'] * pos['current_price']
                trades.append({
                    'date': date, 'stock': stock, 'action': 'stop_loss',
                    'price': pos['current_price'], 'shares': pos['shares'],
                    'pnl': (pos['current_price'] - pos['cost']) * pos['shares']
                })
                del positions[stock]
            
            # 止盈检查
            elif ret >= take_profit:
                cash += pos['shares'] * pos['current_price']
                trades.append({
                    'date': date, 'stock': stock, 'action': 'take_profit',
                    'price': pos['current_price'], 'shares': pos['shares'],
                    'pnl': (pos['current_price'] - pos['cost']) * pos['shares']
                })
                del positions[stock]
        
        # 3. 调仓日选股
        if i % rebalance_days == 0 and i >= momentum_period:
            mom_today = momentum.loc[date].dropna()
            if len(mom_today) > 0:
                # 选择动量最高的K只股票
                top_stocks = mom_today.nlargest(max_holdings).index.tolist()
                
                # 清仓不在Top K中的股票
                for stock in list(positions.keys()):
                    if stock not in top_stocks:
                        pos = positions[stock]
                        cash += pos['shares'] * pos['current_price']
                        trades.append({
                            'date': date, 'stock': stock, 'action': 'rebalance_sell',
                            'price': pos['current_price'], 'shares': pos['shares'],
                            'pnl': (pos['current_price'] - pos['cost']) * pos['shares']
                        })
                        del positions[stock]
                
                # 买入新股票
                available_cash = cash
                stocks_to_buy = [s for s in top_stocks if s not in positions]
                if stocks_to_buy:
                    alloc_per_stock = available_cash / len(stocks_to_buy)
                    for stock in stocks_to_buy:
                        price = close_df.loc[date, stock]
                        if not pd.isna(price) and price > 0:
                            shares = int(alloc_per_stock / price / 100) * 100  # 整手
                            if shares > 0:
                                positions[stock] = {
                                    'shares': shares, 'cost': price,
                                    'current_price': price, 'highest': price
                                }
                                cash -= shares * price
                                trades.append({
                                    'date': date, 'stock': stock, 'action': 'buy',
                                    'price': price, 'shares': shares, 'pnl': 0
                                })
        
        # 记录净值
        equity_curve.append({'date': date, 'equity': portfolio_value})
    
    # 计算绩效指标
    equity_df = pd.DataFrame(equity_curve)
    returns = equity_df['equity'].pct_change().dropna()
    
    total_return = equity_df['equity'].iloc[-1] / initial_capital - 1
    annual_return = (1 + total_return) ** (252 / len(equity_df)) - 1
    sharpe = returns.mean() / returns.std() * (252 ** 0.5) if returns.std() > 0 else 0
    max_dd = (equity_df['equity'] / equity_df['equity'].cummax() - 1).min()
    
    return {
        'total_return': total_return,
        'annual_return': annual_return,
        'sharpe_ratio': sharpe,
        'max_drawdown': max_dd,
        'equity_curve': equity_df,
        'trades': trades
    }
'''

def generate_html():
    """生成策略代码页HTML"""
    import html
    
    # 转义代码
    escaped_code = html.escape(CORE_STRATEGY_CODE)
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股策略 - 核心代码</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css" rel="stylesheet" />
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #1e1e1e; color: #d4d4d4; padding: 20px; }}
        h1 {{ color: #4ec9b0; }}
        h2 {{ color: #9cdcfe; margin-top: 30px; }}
        .card {{ background: #252526; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        pre[class*="language-"] {{ 
            margin: 0; padding: 20px; border-radius: 8px;
            font-size: 14px; line-height: 1.6;
        }}
        .line-numbers .line-numbers-rows {{ border-right: 1px solid #444; }}
        .param-table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        .param-table th {{ background: #3c3c3c; padding: 12px; text-align: left; color: #4ec9b0; }}
        .param-table td {{ padding: 10px; border-bottom: 1px solid #333; }}
        .highlight-value {{ color: #dcdcaa; }}
        code {{ background: #3c3c3c; padding: 2px 6px; border-radius: 3px; }}
    </style>
</head>
<body>
    <h1>🎯 十倍股动量策略 - 核心代码</h1>
    
    <div class="card">
        <h2>⚙️ 策略参数配置</h2>
        <table class="param-table">
            <tr>
                <th>参数名称</th>
                <th>符号</th>
                <th>最优值</th>
                <th>含义说明</th>
            </tr>
            <tr>
                <td>最大持仓数</td>
                <td><code>max_holdings</code></td>
                <td><strong class="highlight-value">2</strong></td>
                <td>同时持有的最大股票数量</td>
            </tr>
            <tr>
                <td>动量周期</td>
                <td><code>momentum_period</code></td>
                <td><strong class="highlight-value">20</strong></td>
                <td>计算动量的回溯天数</td>
            </tr>
            <tr>
                <td>调仓频率</td>
                <td><code>rebalance_days</code></td>
                <td><strong class="highlight-value">3</strong></td>
                <td>重新评估持仓的间隔天数</td>
            </tr>
            <tr>
                <td>止损线</td>
                <td><code>stop_loss</code></td>
                <td><strong class="highlight-value">-8%</strong></td>
                <td>触发强制平仓的亏损阈值</td>
            </tr>
            <tr>
                <td>止盈线</td>
                <td><code>take_profit</code></td>
                <td><strong class="highlight-value">+50%</strong></td>
                <td>触发获利了结的盈利阈值</td>
            </tr>
        </table>
    </div>
    
    <div class="card">
        <h2>💻 核心回测引擎代码</h2>
        <pre class="line-numbers"><code class="language-python">{escaped_code}</code></pre>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js"></script>
</body>
</html>'''
    
    # 保存文件
    output_path = "/home/taotao/dev/QuantTest/TRQuant/research/tenbagger_10x_strategy/outputs/strategy_code_page.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 策略代码页已生成: {output_path}")
    print(f"   代码行数: {len(CORE_STRATEGY_CODE.split(chr(10)))}")
    return output_path

if __name__ == "__main__":
    generate_html()
