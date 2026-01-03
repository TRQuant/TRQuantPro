# -*- coding: utf-8 -*-
"""动量策略 - 自动生成"""
from jqdata import *

# 参数
SHORT_PERIOD = 5
LONG_PERIOD = 20
MAX_STOCKS = 10
REBALANCE_DAYS = 5
STOP_LOSS = 0.08
TAKE_PROFIT = 0.2

def initialize(context):
    set_benchmark('000300.XSHG')
    set_slippage(FixedSlippage(0.001))
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001, 
                            open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    g.trade_count = 0
    run_daily(rebalance, time='09:35')

def rebalance(context):
    g.trade_count += 1
    if g.trade_count % REBALANCE_DAYS != 0:
        return
    
    stocks = get_index_stocks('000300.XSHG')
    df = get_price(stocks, end_date=context.current_dt, frequency='daily', fields=['close'], count=LONG_PERIOD+5, panel=False)
    pivot = df.pivot(index='time', columns='code', values='close')
    
    mom_short = pivot.pct_change(SHORT_PERIOD).iloc[-1]
    mom_long = pivot.pct_change(LONG_PERIOD).iloc[-1]
    score = (mom_short * 0.5 + mom_long * 0.5)
    score = score[(mom_short > 0) & (mom_long > 0)].dropna()
    
    targets = score.nlargest(MAX_STOCKS).index.tolist()
    
    # 卖出不在目标的
    for stock in list(context.portfolio.positions.keys()):
        if stock not in targets:
            order_target_value(stock, 0)
    
    # 买入目标
    cash = context.portfolio.total_value / MAX_STOCKS
    for stock in targets:
        order_target_value(stock, cash)
