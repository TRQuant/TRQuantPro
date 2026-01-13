# -*- coding: utf-8 -*-
"""
动态风控管理器 V5.0
===================

功能:
1. 根据市场趋势动态调整止损止盈参数
2. 涨停板特殊处理规则
3. 实盘交易规则定义

作者: TRQuant Team
版本: V5.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class RiskAction(Enum):
    """风控动作"""
    HOLD = "持有"
    SELL_ALL = "全部卖出"
    SELL_HALF = "卖出一半"
    SELL_PARTIAL = "部分卖出"
    ADD_POSITION = "加仓"
    NO_ACTION = "无操作"


@dataclass
class RiskDecision:
    """风控决策"""
    action: RiskAction
    reason: str
    sell_ratio: float = 0.0  # 卖出比例 (0-1)
    priority: int = 0        # 优先级（数字越大越优先）
    
    def __str__(self):
        return f"{self.action.value}: {self.reason}"


@dataclass
class DynamicRiskParams:
    """动态风控参数"""
    # 硬止损
    hard_stop_loss: float = -0.10
    
    # 软止损
    soft_stop_loss: float = -0.08
    soft_stop_days: int = 3
    
    # 止盈
    take_profit_1: float = 0.20  # 第一批止盈
    take_profit_1_ratio: float = 0.50  # 第一批卖出比例
    take_profit_2: float = 0.40  # 全止盈
    
    # 移动止损
    trailing_trigger: float = 0.15  # 触发条件
    trailing_stop: float = -0.09    # 回撤止损
    
    # 时间止损
    time_stop_days: int = 20
    time_stop_loss: float = 0.0  # 时间止损条件（亏损中）
    
    # 涨停规则
    limit_up_no_sell: bool = True   # 涨停不卖
    first_limit_hold_days: int = 1  # 首板后持有天数
    consecutive_limit_add: bool = True  # 连板加仓
    
    # 仓位上限
    position_cap: float = 1.0


# ============ 策略模式对应的风控参数 ============

RISK_PARAMS_BY_MODE = {
    "激进": DynamicRiskParams(
        hard_stop_loss=-0.12,
        soft_stop_loss=-0.10,
        soft_stop_days=3,
        take_profit_1=0.25,
        take_profit_1_ratio=0.5,
        take_profit_2=0.50,
        trailing_trigger=0.20,
        trailing_stop=-0.12,
        time_stop_days=20,
        limit_up_no_sell=True,
        first_limit_hold_days=1,
        consecutive_limit_add=True,
        position_cap=1.0,
    ),
    "正常": DynamicRiskParams(
        hard_stop_loss=-0.10,
        soft_stop_loss=-0.08,
        soft_stop_days=3,
        take_profit_1=0.20,
        take_profit_1_ratio=0.5,
        take_profit_2=0.40,
        trailing_trigger=0.15,
        trailing_stop=-0.09,
        time_stop_days=18,
        limit_up_no_sell=True,
        first_limit_hold_days=1,
        consecutive_limit_add=False,
        position_cap=1.0,
    ),
    "保守": DynamicRiskParams(
        hard_stop_loss=-0.08,
        soft_stop_loss=-0.06,
        soft_stop_days=3,
        take_profit_1=0.15,
        take_profit_1_ratio=0.4,
        take_profit_2=0.30,
        trailing_trigger=0.12,
        trailing_stop=-0.07,
        time_stop_days=15,
        limit_up_no_sell=True,
        first_limit_hold_days=2,
        consecutive_limit_add=False,
        position_cap=0.8,
    ),
    "防御": DynamicRiskParams(
        hard_stop_loss=-0.06,
        soft_stop_loss=-0.05,
        soft_stop_days=2,
        take_profit_1=0.10,
        take_profit_1_ratio=0.3,
        take_profit_2=0.20,
        trailing_trigger=0.10,
        trailing_stop=-0.05,
        time_stop_days=10,
        limit_up_no_sell=False,
        first_limit_hold_days=0,
        consecutive_limit_add=False,
        position_cap=0.4,
    ),
}


@dataclass
class PositionState:
    """持仓状态"""
    stock_code: str
    cost_price: float
    current_price: float
    highest_price: float
    entry_date: datetime
    quantity: int
    
    # 状态标记
    is_limit_up_today: bool = False
    is_first_limit_up: bool = False
    consecutive_limit_up_days: int = 0
    partial_profit_done: bool = False
    
    @property
    def pnl_rate(self) -> float:
        """盈亏比例"""
        if self.cost_price <= 0:
            return 0.0
        return (self.current_price / self.cost_price - 1.0)
    
    @property
    def holding_days(self) -> int:
        """持仓天数"""
        if not self.entry_date:
            return 0
        return (datetime.now() - self.entry_date).days
    
    @property
    def drawdown_from_high(self) -> float:
        """从最高点回撤"""
        if self.highest_price <= 0:
            return 0.0
        return (self.current_price / self.highest_price - 1.0)


class DynamicRiskManager:
    """
    动态风控管理器
    
    核心功能:
    1. 根据市场状态选择风控参数
    2. 应用止损止盈规则
    3. 处理涨停板特殊情况
    4. 生成交易决策
    """
    
    def __init__(self, strategy_mode: str = "正常"):
        """
        初始化风控管理器
        
        Args:
            strategy_mode: 策略模式（激进/正常/保守/防御）
        """
        self.strategy_mode = strategy_mode
        self.params = RISK_PARAMS_BY_MODE.get(strategy_mode, DynamicRiskParams())
        
        logger.info(f"DynamicRiskManager 初始化: 模式={strategy_mode}")
    
    def update_mode(self, new_mode: str):
        """更新策略模式"""
        if new_mode in RISK_PARAMS_BY_MODE:
            self.strategy_mode = new_mode
            self.params = RISK_PARAMS_BY_MODE[new_mode]
            logger.info(f"风控模式切换: {new_mode}")
    
    def evaluate_position(self, position: PositionState) -> RiskDecision:
        """
        评估持仓并生成风控决策
        
        Args:
            position: 持仓状态
        
        Returns:
            RiskDecision: 风控决策
        """
        p = self.params
        pnl = position.pnl_rate
        
        # ========== 涨停板特殊处理 ==========
        if position.is_limit_up_today:
            if p.limit_up_no_sell and pnl > 0:
                return RiskDecision(
                    action=RiskAction.HOLD,
                    reason="涨停中，不触发止盈卖出",
                    priority=100,
                )
        
        # 首板后观察期
        if position.is_first_limit_up and position.holding_days < p.first_limit_hold_days:
            return RiskDecision(
                action=RiskAction.HOLD,
                reason=f"首板后观察期，持有{p.first_limit_hold_days}天",
                priority=90,
            )
        
        # 连板加仓（仅在激进模式）
        if p.consecutive_limit_add and position.consecutive_limit_up_days >= 2:
            return RiskDecision(
                action=RiskAction.ADD_POSITION,
                reason=f"连续{position.consecutive_limit_up_days}日涨停，考虑加仓",
                priority=80,
            )
        
        # ========== 止损逻辑 ==========
        # 1. 硬止损（最高优先级）
        if pnl <= p.hard_stop_loss:
            return RiskDecision(
                action=RiskAction.SELL_ALL,
                reason=f"触发硬止损 {pnl:.2%} <= {p.hard_stop_loss:.2%}",
                sell_ratio=1.0,
                priority=200,
            )
        
        # 2. 软止损（持仓满足天数条件）
        if pnl <= p.soft_stop_loss and position.holding_days >= p.soft_stop_days:
            return RiskDecision(
                action=RiskAction.SELL_HALF,
                reason=f"触发软止损 {pnl:.2%}, 持仓{position.holding_days}天",
                sell_ratio=0.5,
                priority=150,
            )
        
        # 3. 移动止损
        if pnl >= p.trailing_trigger:
            drawdown = position.drawdown_from_high
            if drawdown <= p.trailing_stop:
                return RiskDecision(
                    action=RiskAction.SELL_ALL,
                    reason=f"触发移动止损，从高点回撤 {drawdown:.2%}",
                    sell_ratio=1.0,
                    priority=180,
                )
        
        # 4. 时间止损
        if position.holding_days >= p.time_stop_days and pnl <= p.time_stop_loss:
            return RiskDecision(
                action=RiskAction.SELL_ALL,
                reason=f"触发时间止损，持仓{position.holding_days}天且亏损",
                sell_ratio=1.0,
                priority=140,
            )
        
        # ========== 止盈逻辑 ==========
        # 1. 全止盈
        if pnl >= p.take_profit_2:
            return RiskDecision(
                action=RiskAction.SELL_ALL,
                reason=f"触发全止盈 {pnl:.2%} >= {p.take_profit_2:.2%}",
                sell_ratio=1.0,
                priority=170,
            )
        
        # 2. 第一批止盈
        if pnl >= p.take_profit_1 and not position.partial_profit_done:
            return RiskDecision(
                action=RiskAction.SELL_PARTIAL,
                reason=f"触发第一批止盈 {pnl:.2%} >= {p.take_profit_1:.2%}",
                sell_ratio=p.take_profit_1_ratio,
                priority=160,
            )
        
        # 默认持有
        return RiskDecision(
            action=RiskAction.HOLD,
            reason="无触发条件，继续持有",
            priority=0,
        )
    
    def get_trading_rules_summary(self) -> str:
        """
        获取交易规则摘要（实盘参考）
        """
        p = self.params
        
        rules = f"""
========================================
{self.strategy_mode}模式 - 交易规则清单
========================================

【止损规则】
1. 硬止损: 亏损 {abs(p.hard_stop_loss):.0%} 立即全部卖出
2. 软止损: 亏损 {abs(p.soft_stop_loss):.0%} 且持仓满 {p.soft_stop_days} 天，卖出50%
3. 移动止损: 盈利超 {p.trailing_trigger:.0%} 后，从最高点回撤 {abs(p.trailing_stop):.0%} 全部卖出
4. 时间止损: 持仓满 {p.time_stop_days} 天且亏损，全部卖出

【止盈规则】
1. 第一批止盈: 盈利 {p.take_profit_1:.0%}，卖出 {p.take_profit_1_ratio:.0%}
2. 全止盈: 盈利 {p.take_profit_2:.0%}，全部卖出

【涨停特殊处理】
1. 涨停不卖: {'是' if p.limit_up_no_sell else '否'} - 涨停当日不触发止盈
2. 首板观察期: {p.first_limit_hold_days} 天 - 首板后不触发止损
3. 连板加仓: {'是' if p.consecutive_limit_add else '否'} - 连续涨停可考虑加仓

【仓位管理】
1. 仓位上限: {p.position_cap:.0%}

【执行优先级】（数字大优先）
硬止损(200) > 移动止损(180) > 全止盈(170) > 第一批止盈(160) > 
软止损(150) > 时间止损(140) > 涨停持有(100)

========================================
"""
        return rules


def apply_risk_rules_to_weights(
    weights: pd.DataFrame,
    close: pd.DataFrame,
    risk_manager: DynamicRiskManager,
) -> pd.DataFrame:
    """
    将风控规则应用到权重矩阵
    
    Args:
        weights: 原始权重矩阵 (T x N)
        close: 收盘价矩阵 (T x N)
        risk_manager: 风控管理器
    
    Returns:
        调整后的权重矩阵
    """
    adjusted = weights.copy()
    params = risk_manager.params
    
    # 计算涨停标记
    daily_returns = close / close.shift(1) - 1
    is_limit_up = daily_returns > 0.09
    
    # 跟踪持仓信息
    cost_prices = {}
    highest_prices = {}
    entry_dates = {}
    partial_done = {}
    
    for i, date in enumerate(weights.index):
        if i == 0:
            continue
        
        prev_weights = adjusted.iloc[i-1]
        
        for stock in weights.columns:
            prev_w = prev_weights.get(stock, 0)
            curr_price = close.loc[date, stock] if stock in close.columns else np.nan
            
            if pd.isna(curr_price) or curr_price <= 0:
                continue
            
            # 新建仓
            if prev_w < 0.001 and weights.loc[date, stock] > 0.001:
                cost_prices[stock] = curr_price
                highest_prices[stock] = curr_price
                entry_dates[stock] = date
                partial_done[stock] = False
                continue
            
            # 已有持仓
            if prev_w > 0.001:
                highest_prices[stock] = max(highest_prices.get(stock, curr_price), curr_price)
                cost = cost_prices.get(stock, curr_price)
                
                if cost <= 0:
                    continue
                
                pnl = (curr_price / cost - 1.0)
                stock_limit_up = is_limit_up.loc[date, stock] if stock in is_limit_up.columns else False
                
                # 涨停不卖
                if stock_limit_up and params.limit_up_no_sell and pnl > 0:
                    adjusted.loc[date, stock] = prev_w
                    continue
                
                # 硬止损
                if pnl <= params.hard_stop_loss:
                    adjusted.loc[date, stock] = 0
                    cost_prices.pop(stock, None)
                    continue
                
                # 全止盈
                if pnl >= params.take_profit_2:
                    adjusted.loc[date, stock] = 0
                    cost_prices.pop(stock, None)
                    continue
                
                # 第一批止盈
                if pnl >= params.take_profit_1 and not partial_done.get(stock, False):
                    adjusted.loc[date, stock] = prev_w * (1 - params.take_profit_1_ratio)
                    partial_done[stock] = True
                    continue
                
                # 移动止损
                high = highest_prices.get(stock, curr_price)
                if pnl >= params.trailing_trigger and high > 0:
                    drawdown = (curr_price / high - 1.0)
                    if drawdown <= params.trailing_stop:
                        adjusted.loc[date, stock] = 0
                        cost_prices.pop(stock, None)
                        continue
                
                # 保持
                adjusted.loc[date, stock] = prev_w
    
    return adjusted


# ============ 测试函数 ============

def test_dynamic_risk_manager():
    """测试动态风控管理器"""
    print("=" * 60)
    print("DynamicRiskManager 单元测试")
    print("=" * 60)
    
    # 测试1: 不同模式参数
    print("\n1. 测试不同策略模式...")
    for mode in ["激进", "正常", "保守", "防御"]:
        manager = DynamicRiskManager(mode)
        p = manager.params
        print(f"   {mode}: 硬止损={p.hard_stop_loss:.0%}, 全止盈={p.take_profit_2:.0%}, 仓位上限={p.position_cap:.0%}")
    print("   ✓ 通过")
    
    # 测试2: 止损决策
    print("\n2. 测试止损决策...")
    manager = DynamicRiskManager("正常")
    
    position = PositionState(
        stock_code="000001.XSHE",
        cost_price=10.0,
        current_price=8.5,  # -15%
        highest_price=11.0,
        entry_date=datetime(2026, 1, 1),
        quantity=1000,
    )
    
    decision = manager.evaluate_position(position)
    print(f"   持仓盈亏: {position.pnl_rate:.2%}")
    print(f"   决策: {decision}")
    assert decision.action == RiskAction.SELL_ALL, "应触发硬止损"
    print("   ✓ 通过")
    
    # 测试3: 涨停不卖
    print("\n3. 测试涨停不卖...")
    position_limit_up = PositionState(
        stock_code="000002.XSHE",
        cost_price=10.0,
        current_price=12.5,  # +25%
        highest_price=12.5,
        entry_date=datetime(2026, 1, 1),
        quantity=1000,
        is_limit_up_today=True,
    )
    
    decision2 = manager.evaluate_position(position_limit_up)
    print(f"   持仓盈亏: {position_limit_up.pnl_rate:.2%}")
    print(f"   涨停中: {position_limit_up.is_limit_up_today}")
    print(f"   决策: {decision2}")
    assert decision2.action == RiskAction.HOLD, "涨停应持有不卖"
    print("   ✓ 通过")
    
    # 测试4: 规则摘要
    print("\n4. 测试规则摘要...")
    rules = manager.get_trading_rules_summary()
    print(f"   规则摘要前300字:\n{rules[:300]}...")
    assert "硬止损" in rules, "规则应包含硬止损"
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_dynamic_risk_manager()
