#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略 - QMT代码生成器

基于递归迭代优化的最优参数，生成QMT回测和实盘代码
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


@dataclass
class BullMarketParams:
    """牛市策略参数"""
    # 追涨信号参数
    limit_up_threshold: float = 0.093
    vol_ratio_threshold_first: float = 2.5
    mom_5d_threshold_breakout: float = 16.0
    
    # 7因子选股参数
    min_momentum_20d: float = 5.0
    max_momentum_20d: float = 50.0
    max_rel_position: float = 95.0
    min_volume_ratio: float = 1.5
    
    # 交易参数
    max_positions: int = 5
    stop_loss_pct: float = -8.0
    take_profit_pct: float = 30.0
    rebalance_days: int = 5
    
    @classmethod
    def from_json(cls, json_path: str) -> 'BullMarketParams':
        """从JSON文件加载参数"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            limit_up_threshold=data.get('limit_up_threshold', 0.093),
            vol_ratio_threshold_first=data.get('vol_ratio_threshold_first', 2.5),
            mom_5d_threshold_breakout=data.get('mom_5d_threshold_breakout', 16.0),
            min_momentum_20d=data.get('min_momentum_20d', 5.0),
            max_momentum_20d=data.get('max_momentum_20d', 50.0),
            max_rel_position=data.get('max_rel_position', 95.0),
            min_volume_ratio=data.get('min_volume_ratio', 1.5),
            max_positions=data.get('max_positions', 5),
            stop_loss_pct=data.get('stop_loss_pct', -8.0),
            take_profit_pct=data.get('take_profit_pct', 30.0),
            rebalance_days=data.get('rebalance_days', 5),
        )


class BullMarketStrategyGenerator:
    """牛市极端高收益策略 - QMT代码生成器"""
    
    def __init__(self, params: Optional[BullMarketParams] = None):
        """
        初始化生成器
        
        Args:
            params: 策略参数，如果为None则使用默认参数
        """
        self.params = params or BullMarketParams()
    
    def generate_backtest_code(self) -> str:
        """生成QMT回测代码"""
        p = self.params
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        code = f'''#coding:gbk
# -*- coding: utf-8 -*-
"""
TRQuant 牛市极端高收益策略 V1.0 - QMT回测版本
==============================================

策略说明:
- 目标：周收益10%+ (激进策略)
- 选股：融合追涨信号 + 7因子综合评分
- 调仓：每{p.rebalance_days}个交易日
- 最大持仓：{p.max_positions}只股票

信号类型:
1. 首板启动：涨停+放量>{p.vol_ratio_threshold_first:.1f}倍
2. 强势突破：5日动量>{p.mom_5d_threshold_breakout:.0f}%
3. 7因子综合得分排序

生成时间: {timestamp}
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ==================== 策略参数 ====================
MAX_POSITIONS = {p.max_positions}
STOP_LOSS_PCT = {p.stop_loss_pct}
TAKE_PROFIT_PCT = {p.take_profit_pct}
REBALANCE_DAYS = {p.rebalance_days}
WARMUP_BARS = 25

# 追涨信号参数
LIMIT_UP_THRESHOLD = {p.limit_up_threshold}
VOL_RATIO_THRESHOLD_FIRST = {p.vol_ratio_threshold_first}
MOM_5D_THRESHOLD_BREAKOUT = {p.mom_5d_threshold_breakout}

# 7因子选股参数
MIN_MOMENTUM_20D = {p.min_momentum_20d}
MAX_MOMENTUM_20D = {p.max_momentum_20d}
MAX_REL_POSITION = {p.max_rel_position}
MIN_VOLUME_RATIO = {p.min_volume_ratio}

# 佣金设置（华泰证券标准）
COMMISSION_RATE = 0.0001
STAMP_TAX_RATE = 0.001
MIN_COMMISSION = 5.0

# ==================== 全局变量 ====================
g_holdings = {{}}  # 当前持仓 {{code: {{'shares': x, 'cost': y, 'entry_date': z}}}}
g_cash = 0.0
g_last_rebalance = 0


def init(ContextInfo):
    """初始化"""
    # 股票池：沪深300
    ContextInfo.s = ContextInfo.get_sector('000300.SH')
    ContextInfo.set_universe(ContextInfo.s)
    
    # 初始化全局变量
    global g_holdings, g_cash, g_last_rebalance
    g_holdings = {{}}
    g_cash = ContextInfo.capital
    g_last_rebalance = 0
    
    # 账户ID
    ContextInfo.accountID = 'testS'
    
    print("[初始化] 牛市极端高收益策略 V1.0")
    print("[参数] 最大持仓=%d, 止损=%.1f%%, 止盈=%.1f%%" % (MAX_POSITIONS, STOP_LOSS_PCT, TAKE_PROFIT_PCT))
    print("[参数] 调仓周期=%d天" % REBALANCE_DAYS)


def handlebar(ContextInfo):
    """主函数"""
    global g_holdings, g_cash, g_last_rebalance
    
    d = ContextInfo.barpos
    
    # 预热期
    if d < WARMUP_BARS:
        return
    
    # 获取历史数据
    close_dict = ContextInfo.get_history_data(25, '1d', 'close', 0)
    volume_dict = ContextInfo.get_history_data(25, '1d', 'volume', 0)
    high_dict = ContextInfo.get_history_data(25, '1d', 'high', 0)
    low_dict = ContextInfo.get_history_data(25, '1d', 'low', 0)
    
    if not close_dict:
        return
    
    # 1. 止损止盈检查
    check_stop_loss_take_profit(ContextInfo, close_dict)
    
    # 2. 调仓日检查
    if d - g_last_rebalance < REBALANCE_DAYS:
        return
    g_last_rebalance = d
    
    # 3. 计算信号和评分
    signals = {{}}
    
    for code in ContextInfo.s:
        try:
            if code not in close_dict or len(close_dict[code]) < 22:
                continue
            
            close = np.array(close_dict[code])
            volume = np.array(volume_dict.get(code, []))
            high = np.array(high_dict.get(code, []))
            low = np.array(low_dict.get(code, []))
            
            if len(close) < 22 or len(volume) < 22:
                continue
            
            # 计算因子
            mom_20d = (close[-1] / close[-21] - 1) * 100
            mom_5d = (close[-1] / close[-6] - 1) * 100
            
            price_range = np.max(close[-20:]) - np.min(close[-20:])
            rel_position = (close[-1] - np.min(close[-20:])) / (price_range + 1e-6) * 100 if price_range > 0 else 50
            
            avg_vol = np.mean(volume[-20:])
            vol_ratio = volume[-1] / avg_vol if avg_vol > 0 else 1.0
            
            daily_return = close[-1] / close[-2] - 1 if close[-2] > 0 else 0
            
            # 筛选条件
            if mom_20d < MIN_MOMENTUM_20D or mom_20d > MAX_MOMENTUM_20D:
                continue
            if rel_position > MAX_REL_POSITION:
                continue
            if vol_ratio < MIN_VOLUME_RATIO:
                continue
            
            # 计算综合评分
            score = 0
            
            # 追涨信号加分
            if daily_return >= LIMIT_UP_THRESHOLD and vol_ratio >= VOL_RATIO_THRESHOLD_FIRST:
                score += 30  # 首板启动
            elif mom_5d >= MOM_5D_THRESHOLD_BREAKOUT and vol_ratio >= 1.5:
                score += 20  # 强势突破
            
            # 基础因子评分
            score += min(mom_20d / 10, 3) * 10  # 动量
            score += (100 - rel_position) / 20  # 相对位置
            score += min(vol_ratio, 3) * 5  # 量比
            
            if score > 20:
                signals[code] = {{'score': score, 'mom_20d': mom_20d, 'vol_ratio': vol_ratio}}
        
        except Exception:
            continue
    
    # 4. 选择Top N股票
    sorted_signals = sorted(signals.items(), key=lambda x: x[1]['score'], reverse=True)
    target_stocks = [x[0] for x in sorted_signals[:MAX_POSITIONS]]
    
    # 5. 执行交易
    execute_trades(ContextInfo, target_stocks, close_dict)


def check_stop_loss_take_profit(ContextInfo, close_dict):
    """止损止盈检查"""
    global g_holdings, g_cash
    
    sell_list = []
    
    for code, info in g_holdings.items():
        if code not in close_dict or not close_dict[code]:
            continue
        
        current_price = close_dict[code][-1]
        cost = info['cost']
        pnl_pct = (current_price / cost - 1) * 100
        
        if pnl_pct <= STOP_LOSS_PCT:
            sell_list.append((code, 'stop_loss', pnl_pct))
        elif pnl_pct >= TAKE_PROFIT_PCT:
            sell_list.append((code, 'take_profit', pnl_pct))
    
    for code, reason, pnl_pct in sell_list:
        info = g_holdings[code]
        price = close_dict[code][-1]
        
        # 计算卖出收益
        sell_value = info['shares'] * price
        commission = max(sell_value * COMMISSION_RATE, MIN_COMMISSION)
        stamp_tax = sell_value * STAMP_TAX_RATE
        net_value = sell_value - commission - stamp_tax
        
        g_cash += net_value
        del g_holdings[code]
        
        print("[%s] 卖出 %s | 盈亏=%.1f%% | 回收=%.0f" % (reason, code, pnl_pct, net_value))


def execute_trades(ContextInfo, target_stocks, close_dict):
    """执行交易"""
    global g_holdings, g_cash
    
    # 计算需要卖出的股票（不在目标列表中）
    for code in list(g_holdings.keys()):
        if code not in target_stocks:
            if code in close_dict and close_dict[code]:
                info = g_holdings[code]
                price = close_dict[code][-1]
                
                sell_value = info['shares'] * price
                commission = max(sell_value * COMMISSION_RATE, MIN_COMMISSION)
                stamp_tax = sell_value * STAMP_TAX_RATE
                net_value = sell_value - commission - stamp_tax
                
                g_cash += net_value
                del g_holdings[code]
                
                print("[轮动] 卖出 %s | 回收=%.0f" % (code, net_value))
    
    # 计算可买入的股票
    new_stocks = [s for s in target_stocks if s not in g_holdings]
    
    if not new_stocks:
        return
    
    # 计算每只股票的目标金额
    total_value = g_cash
    for code, info in g_holdings.items():
        if code in close_dict and close_dict[code]:
            total_value += info['shares'] * close_dict[code][-1]
    
    available_slots = MAX_POSITIONS - len(g_holdings)
    if available_slots <= 0:
        return
    
    per_stock_value = min(g_cash / available_slots * 0.95, total_value / MAX_POSITIONS)
    
    for code in new_stocks[:available_slots]:
        if code not in close_dict or not close_dict[code]:
            continue
        
        price = close_dict[code][-1]
        if price <= 0:
            continue
        
        # 计算可买数量（100股整数倍）
        shares = int(per_stock_value / price / 100) * 100
        if shares < 100:
            continue
        
        # 计算买入成本
        buy_value = shares * price
        commission = max(buy_value * COMMISSION_RATE, MIN_COMMISSION)
        total_cost = buy_value + commission
        
        if total_cost > g_cash:
            continue
        
        g_cash -= total_cost
        g_holdings[code] = {{
            'shares': shares,
            'cost': price,
            'entry_date': ContextInfo.barpos,
        }}
        
        print("[买入] %s | 数量=%d | 成本=%.2f | 花费=%.0f" % (code, shares, price, total_cost))
'''
        return code
    
    def generate_live_code(self) -> str:
        """生成QMT实盘代码（使用passorder）"""
        backtest_code = self.generate_backtest_code()
        
        # 替换模拟交易为真实下单
        live_code = backtest_code.replace(
            "ContextInfo.accountID = 'testS'",
            "ContextInfo.accountID = 'YOUR_REAL_ACCOUNT'  # TODO: 替换为真实账户"
        )
        
        # 添加passorder下单函数
        passorder_code = '''

def order_shares_live(stock_code, amount, price, ContextInfo):
    """实盘下单（使用passorder）"""
    account_id = getattr(ContextInfo, 'accountID', 'YOUR_ACCOUNT')
    
    if amount > 0:
        # 买入
        order_direction = 23  # 买入
        passorder(
            order_direction, 1101, account_id,
            stock_code, 14, -1, abs(amount),
            'TRQuant_Bull_V1', 2, ContextInfo
        )
    elif amount < 0:
        # 卖出
        order_direction = 24  # 卖出
        passorder(
            order_direction, 1101, account_id,
            stock_code, 14, -1, abs(amount),
            'TRQuant_Bull_V1', 2, ContextInfo
        )
'''
        
        live_code = live_code.replace(
            "# ==================== 全局变量 ====================",
            passorder_code + "\n# ==================== 全局变量 ===================="
        )
        
        return live_code
    
    def save_code(self, output_dir: str, filename_prefix: str = "TRQuant_BullMarket_Optimized") -> Dict[str, str]:
        """
        保存生成的代码
        
        Args:
            output_dir: 输出目录
            filename_prefix: 文件名前缀
        
        Returns:
            Dict: {'backtest': 回测代码路径, 'live': 实盘代码路径}
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存回测代码
        backtest_path = output_path / f"{filename_prefix}_{timestamp}.py"
        with open(backtest_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_backtest_code())
        
        # 保存实盘代码
        live_path = output_path / f"{filename_prefix}_Live_{timestamp}.py"
        with open(live_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_live_code())
        
        return {
            'backtest': str(backtest_path),
            'live': str(live_path),
        }


def main():
    """测试代码生成"""
    import sys
    from pathlib import Path
    
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # 尝试加载优化后的参数
    params_path = PROJECT_ROOT / 'output' / 'bull_market_optimization'
    json_files = list(params_path.glob('best_params_*.json')) if params_path.exists() else []
    
    if json_files:
        latest_params = sorted(json_files)[-1]
        print(f"加载参数: {latest_params}")
        params = BullMarketParams.from_json(str(latest_params))
    else:
        print("使用默认参数")
        params = BullMarketParams()
    
    # 生成代码
    generator = BullMarketStrategyGenerator(params)
    
    output_dir = PROJECT_ROOT / 'output' / 'bull_market_optimization'
    paths = generator.save_code(str(output_dir))
    
    print(f"\n✅ 回测代码: {paths['backtest']}")
    print(f"✅ 实盘代码: {paths['live']}")


if __name__ == '__main__':
    main()
