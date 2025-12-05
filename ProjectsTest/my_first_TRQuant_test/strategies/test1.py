# -*- coding: utf-8 -*-
"""
PTrade 动量+成长策略
====================

策略名称: test1
策略类型: 动量成长
生成时间: 2025-12-03
平台: PTrade

策略逻辑:
1. 动量因子: 选择近期涨幅领先的股票
2. 成长因子: 选择营收增长较快的股票
3. 综合排名选出TOP股票
4. 定期调仓，动态风控

适用场景:
- 牛市行情
- 结构性行情
- 成长风格占优的市场

风控规则:
- 单股止损: 8%
- 单股止盈: 20%
- 最大仓位: 80%
- 单股最大仓位: 10%
"""


def on_bar(engine, bars):
    """
    每个交易日执行的策略逻辑
    
    Args:
        engine: 回测引擎实例，提供交易接口
        bars: 当日行情数据 {symbol: {date, open, high, low, close, volume}}
    """
    # ===== 参数设置 =====
    MOMENTUM_DAYS = 20        # 动量计算周期
    TOP_N = 5                 # 选股数量
    POSITION_SIZE = 0.15      # 每只股票仓位
    STOP_LOSS = 0.08          # 止损线
    TAKE_PROFIT = 0.20        # 止盈线
    
    # ===== 计算动量得分 =====
    momentum_scores = {}
    
    for symbol, bar in bars.items():
        # 简化的动量计算：使用当日涨跌幅作为动量代理
        # 实际策略应使用历史数据计算N日涨幅
        daily_return = (bar['close'] - bar['open']) / bar['open'] if bar['open'] > 0 else 0
        
        # 成交量活跃度（成交量越大得分越高）
        volume_score = bar['volume'] / 1000000 if bar['volume'] > 0 else 0
        
        # 综合得分 = 动量 * 0.6 + 成交量 * 0.4
        momentum_scores[symbol] = daily_return * 0.6 + min(volume_score, 1) * 0.4
    
    # ===== 排名选股 =====
    ranked_stocks = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
    selected_stocks = [s[0] for s in ranked_stocks[:TOP_N]]
    
    # ===== 风控检查 =====
    for symbol, pos in list(engine.portfolio.positions.items()):
        if symbol not in bars:
            continue
            
        current_price = bars[symbol]['close']
        cost = pos.avg_cost
        
        if cost > 0:
            pnl_pct = (current_price - cost) / cost
            
            # 止损
            if pnl_pct < -STOP_LOSS:
                engine.sell(symbol, pos.quantity)
                continue
                
            # 止盈
            if pnl_pct > TAKE_PROFIT:
                # 部分止盈：卖出一半
                sell_qty = pos.quantity // 2
                if sell_qty > 0:
                    engine.sell(symbol, sell_qty)
    
    # ===== 调仓逻辑 =====
    # 获取当前持仓
    current_positions = set(engine.portfolio.positions.keys())
    
    # 卖出不在选股列表中的股票
    for symbol in current_positions:
        if symbol not in selected_stocks:
            pos = engine.portfolio.positions[symbol]
            engine.sell(symbol, pos.quantity)
    
    # 买入选中的股票
    for symbol in selected_stocks:
        if symbol not in engine.portfolio.positions:
            # 计算买入数量
            price = bars[symbol]['close']
            if price > 0:
                # 计算可用资金
                available_cash = engine.portfolio.cash * POSITION_SIZE
                quantity = int(available_cash / price / 100) * 100  # 整手
                
                if quantity >= 100:
                    engine.buy(symbol, quantity)


# ===== 策略信息（供回测系统读取）=====
STRATEGY_INFO = {
    'name': 'test1',
    'display_name': '动量成长策略',
    'version': '1.0.0',
    'author': 'TRQuant',
    'platform': 'ptrade',
    'style': 'momentum_growth',
    'description': '基于动量和成长因子的选股策略，适合牛市和结构性行情',
    'factors': ['momentum_20d', 'volume_ratio', 'daily_return'],
    'risk_params': {
        'max_position': 0.8,
        'single_stock_max': 0.15,
        'stop_loss': 0.08,
        'take_profit': 0.20
    },
    'rebalance': 'daily'
}


# ===== 测试入口 =====
if __name__ == '__main__':
    print(f"策略名称: {STRATEGY_INFO['display_name']}")
    print(f"策略版本: {STRATEGY_INFO['version']}")
    print(f"适用平台: {STRATEGY_INFO['platform']}")
    print(f"策略风格: {STRATEGY_INFO['style']}")
    print(f"使用因子: {', '.join(STRATEGY_INFO['factors'])}")




























































