#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略QMT代码生成器

Phase 4: QMT代码转换
- 生成QMT回测代码
- 生成QMT实盘代码（集成passorder）
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ChaseRiseStrategyConfig:
    """追涨策略配置"""
    # 信号参数
    limit_up_threshold: float = 0.095
    vol_ratio_threshold_first: float = 3.0
    mom_5d_threshold_breakout: float = 15.0
    mom_5d_threshold_volume: float = 10.0
    vol_ratio_threshold_breakout: float = 1.5
    vol_ratio_threshold_volume: float = 2.0
    min_signal_score: float = 55.0
    
    # 交易参数
    max_positions: int = 2
    stop_loss_pct: float = -10.0
    take_profit_pct: float = 25.0
    rebalance_days: int = 5
    warmup_bars: int = 22


class ChaseRiseStrategyGenerator:
    """追涨策略QMT代码生成器"""
    
    def __init__(self, config: Optional[ChaseRiseStrategyConfig] = None):
        """
        初始化生成器
        
        Args:
            config: 策略配置
        """
        self.config = config or ChaseRiseStrategyConfig()
    
    def generate_backtest_code(self) -> str:
        """
        生成QMT回测代码
        
        Returns:
            str: QMT策略代码
        """
        code = f'''#coding:gbk
# -*- coding: utf-8 -*-
"""
TRQuant 追涨策略 V1.0 - QMT回测版本
==================================

策略说明:
- 追涨模式：涨停板信号、强势突破、量价齐升
- 周频调仓：每{self.config.rebalance_days}个交易日
- 最大持仓：{self.config.max_positions}只股票

信号类型:
1. 首板启动：首次涨停+放量>3倍 → 评分75
2. 连板加速：2+连板 → 评分65
3. 强势突破：5日动量>15%+量比>1.5 → 评分60
4. 量价齐升：5日动量>10%+量比>2 → 评分55

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ==================== 策略参数 ====================
MAX_POSITIONS = {self.config.max_positions}
STOP_LOSS_PCT = {self.config.stop_loss_pct}
TAKE_PROFIT_PCT = {self.config.take_profit_pct}
REBALANCE_DAYS = {self.config.rebalance_days}
WARMUP_BARS = {self.config.warmup_bars}
LIMIT_UP_THRESHOLD = {self.config.limit_up_threshold}
VOL_RATIO_THRESHOLD_FIRST = {self.config.vol_ratio_threshold_first}
MOM_5D_THRESHOLD_BREAKOUT = {self.config.mom_5d_threshold_breakout}
MOM_5D_THRESHOLD_VOLUME = {self.config.mom_5d_threshold_volume}
VOL_RATIO_THRESHOLD_BREAKOUT = {self.config.vol_ratio_threshold_breakout}
VOL_RATIO_THRESHOLD_VOLUME = {self.config.vol_ratio_threshold_volume}
MIN_SIGNAL_SCORE = {self.config.min_signal_score}

# ==================== 全局变量 ====================
g_holdings = {{}}  # {{code: {{'shares': int, 'cost': float, 'entry_date': str}}}}
g_last_rebalance_bar = -1

# ==================== 工具函数 ====================

def get_all_stock_data(ContextInfo, stocks, field, days):
    """
    获取所有股票的历史数据
    
    Args:
        ContextInfo: QMT上下文对象
        stocks: 股票列表
        field: 字段名 ('close', 'volume', 'high', 'low')
        days: 天数
    
    Returns:
        dict: {{code: [values]}}
    """
    try:
        # 使用参数0获取全部股票数据
        data = ContextInfo.get_history_data(days, '1d', field, 0)
        if data is None:
            return {{}}
        
        # 过滤到需要的股票
        result = {{}}
        for stock in stocks:
            if stock in data:
                result[stock] = data[stock]
        return result
    except Exception as e:
        print(f"[Error] 获取数据失败 {{field}}: {{e}}")
        return {{}}


def calculate_fee(shares, price, is_buy=True):
    """计算手续费"""
    trade_value = shares * price
    
    if is_buy:
        # 买入：佣金
        commission = max(trade_value * 0.0001, 5.0)
        return commission
    else:
        # 卖出：佣金 + 印花税
        commission = max(trade_value * 0.0001, 5.0)
        stamp_tax = trade_value * 0.001
        return commission + stamp_tax


def calculate_chase_rise_signal(close, volume):
    """
    计算追涨信号
    
    Args:
        close: 收盘价序列
        volume: 成交量序列
    
    Returns:
        tuple: (评分, 信号类型)
    """
    if len(close) < 21:
        return 0.0, 'NO_SIGNAL'
    
    score = 0.0
    signal_type = 'NO_SIGNAL'
    
    # 计算基础指标
    daily_return = close[-1] / close[-2] - 1 if len(close) >= 2 else 0
    is_limit_up = daily_return > LIMIT_UP_THRESHOLD
    
    # 近5日涨停计数
    limit_up_recent = 0
    for j in range(max(len(close)-5, 1), len(close)):
        if j > 0 and close[j] / close[j-1] - 1 > LIMIT_UP_THRESHOLD:
            limit_up_recent += 1
    
    # 5日动量
    mom_5d = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    
    # 量比
    vol_ratio = volume[-1] / np.mean(volume[-20:]) if len(volume) >= 20 and np.mean(volume[-20:]) > 0 else 1.0
    
    # 信号1: 首板启动
    if is_limit_up and limit_up_recent == 1:
        score = 75
        signal_type = 'FIRST_LIMIT_UP'
        if vol_ratio > VOL_RATIO_THRESHOLD_FIRST:
            score += 15
        return score, signal_type
    
    # 信号2: 连板加速
    if limit_up_recent >= 2:
        score = 65
        signal_type = 'CONSECUTIVE_LIMIT_UP'
        return score, signal_type
    
    # 信号3: 强势突破
    if mom_5d > MOM_5D_THRESHOLD_BREAKOUT and vol_ratio > VOL_RATIO_THRESHOLD_BREAKOUT:
        score = 60
        signal_type = 'STRONG_BREAKOUT'
        return score, signal_type
    
    # 信号4: 量价齐升
    if mom_5d > MOM_5D_THRESHOLD_VOLUME and vol_ratio > VOL_RATIO_THRESHOLD_VOLUME:
        score = 55
        signal_type = 'VOLUME_PRICE_RISE'
        return score, signal_type
    
    return score, signal_type


def init(ContextInfo):
    """初始化"""
    # 设置股票池（沪深300）
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # 初始化持仓
    ContextInfo.holdings = {{i: 0 for i in ContextInfo.s}}
    ContextInfo.money = ContextInfo.capital
    ContextInfo.accountID = 'testS'
    
    global g_holdings
    g_holdings = {{}}
    g_last_rebalance_bar = -1
    
    print(f"[Init] 策略初始化完成，股票池: {{len(ContextInfo.s)}}只")


def handlebar(ContextInfo):
    """主循环"""
    global g_holdings, g_last_rebalance_bar
    
    d = ContextInfo.barpos
    
    # 预热期检查
    if d < WARMUP_BARS:
        return
    
    # 调仓日检查
    if d % REBALANCE_DAYS != 0:
        # 非调仓日：检查止损止盈
        check_stop_loss_take_profit(ContextInfo)
        return
    
    # 调仓日：选股和调仓
    g_last_rebalance_bar = d
    
    # 1. 获取数据
    close_22 = get_all_stock_data(ContextInfo, ContextInfo.s, 'close', 22)
    volume_22 = get_all_stock_data(ContextInfo, ContextInfo.s, 'volume', 22)
    
    if not close_22 or not volume_22:
        print(f"[Warning] 数据获取失败")
        return
    
    # 2. 计算信号
    signals = []
    for stock in ContextInfo.s:
        if stock not in close_22 or stock not in volume_22:
            continue
        
        close = close_22[stock]
        volume = volume_22[stock]
        
        if len(close) < 21 or len(volume) < 21:
            continue
        
        score, signal_type = calculate_chase_rise_signal(close, volume)
        
        if signal_type != 'NO_SIGNAL' and score >= MIN_SIGNAL_SCORE:
            signals.append({{
                'code': stock,
                'score': score,
                'signal_type': signal_type,
                'price': close[-1],
            }})
    
    # 3. 排序选股
    signals.sort(key=lambda x: x['score'], reverse=True)
    target_stocks = [s['code'] for s in signals[:MAX_POSITIONS]]
    
    if not target_stocks:
        print(f"[Rebalance] 未选出股票")
        return
    
    print(f"[Rebalance] 选出 {{len(target_stocks)}} 只股票")
    
    # 4. 调仓
    rebalance(ContextInfo, target_stocks, close_22)


def rebalance(ContextInfo, target_stocks, current_prices):
    """调仓"""
    global g_holdings
    
    # 卖出不在目标列表的股票
    for code in list(g_holdings.keys()):
        if code not in target_stocks:
            pos = g_holdings[code]
            if code in current_prices and len(current_prices[code]) > 0:
                sell_price = current_prices[code][-1]
                sell_shares = pos['shares']
                fee = calculate_fee(sell_shares, sell_price, is_buy=False)
                
                ContextInfo.money += sell_shares * sell_price - fee
                del g_holdings[code]
                
                pnl = (sell_price - pos['cost']) * sell_shares
                pnl_pct = (sell_price / pos['cost'] - 1) * 100
                print(f"[Sell] {{code}} @ {{sell_price:.2f}}, P&L: {{pnl:.0f}} ({{pnl_pct:.1f}}%)")
    
    # 买入目标股票
    per_stock_value = ContextInfo.capital / MAX_POSITIONS
    
    for code in target_stocks:
        if code in g_holdings:
            continue
        
        if code not in current_prices or len(current_prices[code]) == 0:
            continue
        
        buy_price = current_prices[code][-1]
        shares = int(per_stock_value / buy_price / 100) * 100  # 整百股
        
        if shares > 0 and ContextInfo.money >= shares * buy_price:
            fee = calculate_fee(shares, buy_price, is_buy=True)
            total_cost = shares * buy_price + fee
            
            if ContextInfo.money >= total_cost:
                g_holdings[code] = {{
                    'shares': shares,
                    'cost': buy_price,
                    'entry_date': d,
                }}
                ContextInfo.money -= total_cost
                print(f"[Buy] {{code}} @ {{buy_price:.2f}}, {{shares}}股")


def check_stop_loss_take_profit(ContextInfo):
    """检查止损止盈"""
    global g_holdings
    
    close_22 = get_all_stock_data(ContextInfo, list(g_holdings.keys()), 'close', 1)
    
    for code in list(g_holdings.keys()):
        if code not in close_22 or len(close_22[code]) == 0:
            continue
        
        pos = g_holdings[code]
        current_price = close_22[code][-1]
        pnl_pct = (current_price / pos['cost'] - 1) * 100
        
        # 止损
        if pnl_pct <= STOP_LOSS_PCT:
            sell_shares = pos['shares']
            fee = calculate_fee(sell_shares, current_price, is_buy=False)
            ContextInfo.money += sell_shares * current_price - fee
            del g_holdings[code]
            print(f"[Stop Loss] {{code}} @ {{current_price:.2f}}, P&L: {{pnl_pct:.1f}}%")
        
        # 止盈
        elif pnl_pct >= TAKE_PROFIT_PCT:
            sell_shares = pos['shares']
            fee = calculate_fee(sell_shares, current_price, is_buy=False)
            ContextInfo.money += sell_shares * current_price - fee
            del g_holdings[code]
            print(f"[Take Profit] {{code}} @ {{current_price:.2f}}, P&L: {{pnl_pct:.1f}}%")
'''
        
        return code
    
    def generate_live_code(self) -> str:
        """
        生成QMT实盘代码（集成passorder）
        
        Returns:
            str: QMT实盘策略代码
        """
        # 实盘代码与回测代码基本相同，只是订单执行使用passorder
        backtest_code = self.generate_backtest_code()
        
        # 替换订单执行部分
        live_code = backtest_code.replace(
            'def rebalance(ContextInfo, target_stocks, current_prices):',
            '''def order_shares_live(stock_code, amount, price, ContextInfo):
    """实盘下单（使用passorder）"""
    try:
        account_id = getattr(ContextInfo, 'accountID', 'YOUR_ACCOUNT')
        order_direction = 23 if amount > 0 else 24  # 23=买, 24=卖
        price_type = 14  # 对手价
        
        passorder(
            order_direction, 1101, account_id,
            stock_code, price_type, -1, abs(amount),
            'TRQuant_ChaseRise_V1', 2, ContextInfo
        )
        return True
    except Exception as e:
        print(f"[Error] passorder失败 {{stock_code}}: {{e}}")
        return False

def rebalance(ContextInfo, target_stocks, current_prices):'''
        )
        
        # 替换买入逻辑
        live_code = live_code.replace(
            '                ContextInfo.money -= total_cost',
            '''                # 实盘下单
                if order_shares_live(code, shares, buy_price, ContextInfo):
                    ContextInfo.money -= total_cost'''
        )
        
        # 替换卖出逻辑
        live_code = live_code.replace(
            '                ContextInfo.money += sell_shares * sell_price - fee',
            '''                # 实盘下单
                if order_shares_live(code, -sell_shares, sell_price, ContextInfo):
                    ContextInfo.money += sell_shares * sell_price - fee'''
        )
        
        # 添加实盘标记
        live_code = live_code.replace(
            'TRQuant 追涨策略 V1.0 - QMT回测版本',
            'TRQuant 追涨策略 V1.0 - QMT实盘版本（使用passorder）'
        )
        
        return live_code
