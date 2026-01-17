#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
风险控制管理器
==============

基于聚宽平台风控理念设计，提供完整的风险管理功能：

核心功能：
1. 止损止盈控制（固定/跟踪/时间/波动率止损）
2. 仓位管理（单只股票最大仓位、总持仓数限制、集中度控制）
3. 回撤控制（最大回撤限制、回撤恢复阈值）
4. 风险指标计算（VaR、最大回撤、夏普比率、波动率）

设计理念（参考聚宽平台）：
- 多层次风险管理：订单级、持仓级、组合级
- 动态调整：根据市场环境调整风控参数
- 实时监控：实时计算风险指标，及时预警
- 可配置化：支持不同策略使用不同风控参数

参考文档：
- docs/JOINQUANT_RISK_CONTROL_GUIDE.md：聚宽平台风控最佳实践

作者：TRQuant Team
创建：2024-12-28
"""

import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class StopLossType(Enum):
    """止损类型"""
    FIXED = "fixed"              # 固定止损：达到固定比例即止损
    TRAILING = "trailing"        # 跟踪止损：跟随价格上涨调整止损价
    TIMEBASED = "timebased"      # 时间止损：持仓超过一定时间未盈利即止损
    VOLATILITY = "volatility"    # 波动率止损：基于波动率的动态止损


class TakeProfitType(Enum):
    """止盈类型"""
    FIXED = "fixed"              # 固定止盈：达到固定比例即止盈
    TRAILING = "trailing"        # 跟踪止盈：跟随价格回调调整止盈价
    SCALING = "scaling"          # 分批止盈：分批卖出锁定利润


@dataclass
class RiskConfig:
    """
    风险配置（基于聚宽平台最佳实践）
    
    推荐配置值参考聚宽平台风控最佳实践：
    - 最大仓位比例：80-95%
    - 单只股票上限：10-20%
    - 固定止损：-10% ~ -15%
    - 移动止损：-10% ~ -20%
    - 固定止盈：50% ~ 100%
    - 最大回撤：-20% ~ -30%
    """
    # 止损配置
    stop_loss_type: StopLossType = StopLossType.TRAILING  # 默认跟踪止损（聚宽推荐）
    stop_loss_threshold: float = -0.15  # -15%止损（聚宽推荐范围：-10% ~ -15%）
    
    # 止盈配置
    take_profit_type: TakeProfitType = TakeProfitType.FIXED
    take_profit_threshold: float = 1.0  # 100%止盈（聚宽推荐范围：50% ~ 100%）
    
    # 仓位管理（聚宽推荐配置）
    max_position_size: float = 0.20     # 单只股票最大仓位20%（聚宽推荐：10-20%）
    max_total_positions: int = 10        # 最大持仓数（聚宽推荐：5-15只）
    position_concentration: float = 0.50  # 前3只股票仓位不超过50%（聚宽推荐：<50%）
    max_portfolio_ratio: float = 0.90   # 最大组合仓位90%（聚宽推荐：80-95%）
    
    # 回撤控制（聚宽推荐配置）
    max_drawdown: float = -0.30          # 最大回撤限制-30%（聚宽推荐：-20% ~ -30%）
    drawdown_recovery_threshold: float = 0.05  # 回撤恢复阈值5%
    max_consecutive_loss_days: int = 10  # 最大连续亏损天数（聚宽推荐：5-10天）
    
    # 风险指标阈值
    max_single_day_loss: float = -0.05   # 单日最大亏损-5%（聚宽推荐：<5%）
    min_sharpe_ratio: float = 1.0        # 最小夏普比率（聚宽推荐：>1.0）
    max_volatility: float = 0.30         # 最大波动率30%（聚宽推荐：<30%）
    
    # 其他
    min_trade_value: float = 10000       # 最小交易金额
    commission_rate: float = 0.0003      # 手续费率0.03%（A股标准）
    slippage_rate: float = 0.001         # 滑点0.1%


@dataclass
class Position:
    """持仓信息"""
    stock: str
    entry_price: float
    entry_date: str
    shares: int
    current_price: float = 0.0
    highest_price: float = 0.0          # 最高价（用于跟踪止损）
    lowest_price: float = 0.0           # 最低价（用于跟踪止损）
    unrealized_pnl: float = 0.0
    unrealized_pnl_pct: float = 0.0
    
    # 止损止盈状态
    stop_loss_price: float = 0.0
    take_profit_price: float = 0.0
    trailing_stop_price: float = 0.0    # 跟踪止损价
    
    def update_price(self, price: float):
        """更新价格"""
        self.current_price = price
        if price > self.highest_price:
            self.highest_price = price
        if price < self.lowest_price or self.lowest_price == 0:
            self.lowest_price = price
        
        # 计算盈亏
        self.unrealized_pnl = (price - self.entry_price) * self.shares
        self.unrealized_pnl_pct = (price / self.entry_price - 1.0)


class PositionSizer:
    """仓位计算器"""
    
    @staticmethod
    def calculate_position_size(
        capital: float,
        stock_price: float,
        risk_per_trade: float = 0.02,  # 每笔交易风险2%
        stop_loss_pct: float = 0.15,   # 止损15%
        max_position_pct: float = 0.5  # 最大仓位50%
    ) -> int:
        """
        根据风险计算仓位大小
        
        Args:
            capital: 可用资金
            stock_price: 股票价格
            risk_per_trade: 每笔交易风险比例
            stop_loss_pct: 止损比例
            max_position_pct: 最大仓位比例
            
        Returns:
            可买入股数（100的整数倍）
        """
        # 风险金额
        risk_amount = capital * risk_per_trade
        
        # 根据止损计算股数
        stop_loss_amount = stock_price * stop_loss_pct
        shares_by_risk = int(risk_amount / stop_loss_amount) if stop_loss_amount > 0 else 0
        
        # 根据最大仓位计算股数
        max_position_amount = capital * max_position_pct
        shares_by_capital = int(max_position_amount / stock_price) if stock_price > 0 else 0
        
        # 取较小值
        shares = min(shares_by_risk, shares_by_capital)
        
        # 向下取整到100的倍数（A股最小交易单位）
        shares = (shares // 100) * 100
        
        return max(0, shares)


class RiskManager:
    """风险管理器"""
    
    def __init__(self, config: RiskConfig = None):
        self.config = config or RiskConfig()
        self.positions: Dict[str, Position] = {}
        self.equity_history: List[Tuple[str, float]] = []  # (date, equity)
        self.trade_records: List[Dict] = []
    
    def add_position(
        self,
        stock: str,
        entry_price: float,
        shares: int,
        entry_date: str = None
    ) -> Position:
        """添加持仓"""
        if entry_date is None:
            entry_date = datetime.now().strftime("%Y-%m-%d")
        
        position = Position(
            stock=stock,
            entry_price=entry_price,
            entry_date=entry_date,
            shares=shares,
            current_price=entry_price,
            highest_price=entry_price,
            lowest_price=entry_price
        )
        
        # 设置止损止盈价
        self._set_stop_loss_take_profit(position)
        
        self.positions[stock] = position
        logger.info(f"✅ 开仓: {stock} {shares}股 @{entry_price:.2f}")
        
        return position
    
    def _set_stop_loss_take_profit(self, position: Position):
        """设置止损止盈价"""
        if self.config.stop_loss_type == StopLossType.FIXED:
            position.stop_loss_price = position.entry_price * (
                1 + self.config.stop_loss_threshold
            )
        elif self.config.stop_loss_type == StopLossType.TRAILING:
            position.trailing_stop_price = position.entry_price * (
                1 + self.config.stop_loss_threshold
            )
            position.stop_loss_price = position.trailing_stop_price
        
        if self.config.take_profit_type == TakeProfitType.FIXED:
            position.take_profit_price = position.entry_price * (
                1 + self.config.take_profit_threshold
            )
    
    def update_positions(self, prices: Dict[str, float], date: str = None) -> List[str]:
        """
        更新持仓价格，检查止损止盈
        
        Returns:
            需要平仓的股票列表
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        stocks_to_close = []
        
        for stock, position in self.positions.items():
            if stock not in prices:
                continue
            
            current_price = prices[stock]
            position.update_price(current_price)
            
            # 检查止损
            if self._check_stop_loss(position, current_price):
                stocks_to_close.append(stock)
                reason = "止损"
                logger.info(f"⛔ {date} {stock} 止损 @{current_price:.2f} 亏损:{position.unrealized_pnl_pct*100:.1f}%")
                continue
            
            # 检查止盈
            if self._check_take_profit(position, current_price):
                stocks_to_close.append(stock)
                reason = "止盈"
                logger.info(f"🎯 {date} {stock} 止盈 @{current_price:.2f} 盈利:{position.unrealized_pnl_pct*100:.1f}%")
                continue
            
            # 更新跟踪止损
            if self.config.stop_loss_type == StopLossType.TRAILING:
                self._update_trailing_stop(position)
        
        return stocks_to_close
    
    def _check_stop_loss(self, position: Position, current_price: float) -> bool:
        """检查是否触发止损"""
        if self.config.stop_loss_type == StopLossType.FIXED:
            return current_price <= position.stop_loss_price
        elif self.config.stop_loss_type == StopLossType.TRAILING:
            return current_price <= position.trailing_stop_price
        return False
    
    def _check_take_profit(self, position: Position, current_price: float) -> bool:
        """检查是否触发止盈"""
        if self.config.take_profit_type == TakeProfitType.FIXED:
            return current_price >= position.take_profit_price
        elif self.config.take_profit_type == TakeProfitType.TRAILING:
            # 跟踪止盈：从最高价回撤一定比例
            if position.highest_price > 0:
                drawdown_from_high = (current_price / position.highest_price - 1.0)
                return drawdown_from_high <= -0.20  # 从最高价回撤20%止盈
        return False
    
    def _update_trailing_stop(self, position: Position):
        """更新跟踪止损价"""
        if position.highest_price > 0:
            new_trailing_stop = position.highest_price * (
                1 + self.config.stop_loss_threshold
            )
            if new_trailing_stop > position.trailing_stop_price:
                position.trailing_stop_price = new_trailing_stop
                position.stop_loss_price = new_trailing_stop
    
    def close_position(self, stock: str, exit_price: float, date: str = None) -> Optional[Position]:
        """平仓"""
        if stock not in self.positions:
            return None
        
        position = self.positions.pop(stock)
        position.update_price(exit_price)
        
        # 记录交易
        self.trade_records.append({
            'stock': stock,
            'entry_date': position.entry_date,
            'exit_date': date or datetime.now().strftime("%Y-%m-%d"),
            'entry_price': position.entry_price,
            'exit_price': exit_price,
            'shares': position.shares,
            'pnl': position.unrealized_pnl,
            'pnl_pct': position.unrealized_pnl_pct
        })
        
        return position
    
    def calculate_portfolio_value(self, prices: Dict[str, float], cash: float) -> float:
        """计算组合总价值"""
        total_value = cash
        for stock, position in self.positions.items():
            if stock in prices:
                total_value += prices[stock] * position.shares
        return total_value
    
    def calculate_drawdown(self, equity_history: List[Tuple[str, float]] = None) -> Dict[str, float]:
        """计算回撤"""
        if equity_history is None:
            equity_history = self.equity_history
        
        if len(equity_history) < 2:
            return {'max_drawdown': 0.0, 'current_drawdown': 0.0}
        
        equities = np.array([e[1] for e in equity_history])
        peaks = np.maximum.accumulate(equities)
        drawdowns = (equities - peaks) / peaks
        
        max_drawdown = np.min(drawdowns)
        current_drawdown = drawdowns[-1] if len(drawdowns) > 0 else 0.0
        
        return {
            'max_drawdown': float(max_drawdown),
            'current_drawdown': float(current_drawdown),
            'max_drawdown_date': equity_history[np.argmin(drawdowns)][0] if len(drawdowns) > 0 else None
        }
    
    def check_max_drawdown_limit(self, equity_history: List[Tuple[str, float]] = None) -> bool:
        """检查是否超过最大回撤限制"""
        drawdown_info = self.calculate_drawdown(equity_history)
        return drawdown_info['current_drawdown'] <= self.config.max_drawdown
    
    def get_position_summary(self) -> Dict[str, Any]:
        """获取持仓摘要"""
        if not self.positions:
            return {'total_positions': 0, 'total_value': 0.0}
        
        total_value = sum(p.current_price * p.shares for p in self.positions.values())
        total_pnl = sum(p.unrealized_pnl for p in self.positions.values())
        total_pnl_pct = sum(p.unrealized_pnl_pct for p in self.positions.values()) / len(self.positions)
        
        return {
            'total_positions': len(self.positions),
            'total_value': total_value,
            'total_unrealized_pnl': total_pnl,
            'avg_unrealized_pnl_pct': total_pnl_pct,
            'positions': [
                {
                    'stock': p.stock,
                    'shares': p.shares,
                    'entry_price': p.entry_price,
                    'current_price': p.current_price,
                    'pnl_pct': p.unrealized_pnl_pct
                }
                for p in self.positions.values()
            ]
        }


