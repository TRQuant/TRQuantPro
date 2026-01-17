# -*- coding: utf-8 -*-
"""
my_first_TRQuant_test - multi_factor 策略
====================================

平台: PTrade
股票池: HS300, ZZ500, ZZ800, ZZ1000
回测周期: 2024-12-03 ~ 2025-12-03
初始资金: 1000000

风控参数:
- 单票最大仓位: 10%
- 止损线: 8%
- 止盈线: 20%

创建时间: 2025-12-03T04:44:47.321Z
"""

# ============ 全局变量 ============
g = None

# ============ 风控参数 ============
MAX_POSITION = 0.1  # 单票最大仓位
STOP_LOSS = 0.08        # 止损线
TAKE_PROFIT = 0.2    # 止盈线

# ============ 初始化函数 ============
def initialize(context):
    """
    策略初始化函数
    在回测开始时调用一次
    """
    global g
    g = context.global_data
    
    # 设置基准
    set_benchmark('000300.XSHG')
    
    # 设置滑点
    set_slippage(PriceRelatedSlippage(0.002))
    
    # 设置手续费
    set_commission(PerOrder(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    
    # 股票池
    g.universe = ["HS300","ZZ500","ZZ800","ZZ1000"]
    
    # 持仓记录
    g.positions = {}
    
    # 买入价格记录（用于止损止盈）
    g.buy_prices = {}
    
    log.info("策略初始化完成")


# ============ 选股逻辑 ============
def get_signals(context):
    """
    获取选股信号
    返回: dict {股票代码: 信号强度}
    """
    signals = {}
    
    # TODO: 在这里实现你的选股逻辑
    # 示例：基于动量的选股
    # for stock in g.universe:
    #     momentum = calculate_momentum(stock)
    #     if momentum > 0:
    #         signals[stock] = momentum
    
    return signals


# ============ 风控检查 ============
def check_risk(context, stock, current_price):
    """
    风控检查：止损止盈
    """
    if stock not in g.buy_prices:
        return None
    
    buy_price = g.buy_prices[stock]
    pnl = (current_price - buy_price) / buy_price
    
    if pnl <= -STOP_LOSS:
        log.warn(f"触发止损: {stock}, 亏损 {pnl*100:.2f}%")
        return 'stop_loss'
    
    if pnl >= TAKE_PROFIT:
        log.info(f"触发止盈: {stock}, 盈利 {pnl*100:.2f}%")
        return 'take_profit'
    
    return None


# ============ 主交易逻辑 ============
def handle_data(context, data):
    """
    主交易函数
    每个交易周期调用一次
    """
    # 1. 风控检查 - 止损止盈
    for stock in list(context.portfolio.positions.keys()):
        current_price = data[stock].close
        risk_signal = check_risk(context, stock, current_price)
        
        if risk_signal:
            order_target_percent(stock, 0)
            if stock in g.buy_prices:
                del g.buy_prices[stock]
    
    # 2. 获取选股信号
    signals = get_signals(context)
    
    # 3. 调仓
    if signals:
        # 按信号强度排序
        sorted_stocks = sorted(signals.items(), key=lambda x: x[1], reverse=True)
        
        # 计算目标持仓
        target_count = min(10, len(sorted_stocks))  # 最多持有10只
        target_weight = min(MAX_POSITION, 1.0 / target_count)
        
        # 买入
        for stock, signal in sorted_stocks[:target_count]:
            if stock not in context.portfolio.positions:
                order_target_percent(stock, target_weight)
                g.buy_prices[stock] = data[stock].close
                log.info(f"买入: {stock}, 权重 {target_weight*100:.1f}%")


# ============ 辅助函数 ============
def calculate_momentum(stock, period=20):
    """
    计算动量因子
    """
    # TODO: 实现动量计算
    return 0


def calculate_factor_score(stock, factors):
    """
    计算综合因子得分
    """
    # TODO: 实现因子评分
    return 0
