# -*- coding: utf-8 -*-
"""
事件驱动交易引擎 V6.0
======================

核心改进: 从固定周频调仓改为条件触发交易

触发买入条件:
1. 首板涨停信号 + 量比>2.5 → 次日开盘买入
2. 连板股开板 + 量价配合 → 低吸
3. 强势突破60日高点 + 资金流入 → 买入
4. 板块轮动龙头 + 首板 → 买入

触发卖出条件:
1. 涨停不卖（持有等待）
2. 跌破成本价止损线 → 止损
3. 盈利达到止盈点 → 分批止盈
4. 连板中断 + 量价背离 → 卖出

作者: TRQuant Team
版本: V6.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class TriggerType(Enum):
    """触发类型"""
    FIRST_LIMIT_UP = "首板涨停"        # 首次涨停信号
    CONSECUTIVE_LIMIT_UP = "连板加速"   # 连续涨停
    BREAKOUT = "强势突破"              # 突破60日高点
    VOLUME_PRICE_RISE = "量价齐升"     # 量价配合上涨
    SECTOR_LEADER = "板块龙头"         # 板块轮动龙头
    CAPITAL_INFLOW = "资金流入"        # 大单资金流入
    
    # 卖出触发
    STOP_LOSS = "止损"
    TAKE_PROFIT = "止盈"
    TRAILING_STOP = "移动止损"
    TIME_STOP = "时间止损"
    LIMIT_UP_BREAK = "涨停开板"


class TradeAction(Enum):
    """交易动作"""
    BUY = "买入"
    SELL = "卖出"
    HOLD = "持有"
    ADD = "加仓"
    REDUCE = "减仓"


@dataclass
class TradeSignal:
    """交易信号"""
    stock: str
    action: TradeAction
    trigger_type: TriggerType
    trigger_time: datetime
    
    # 信号详情
    signal_score: float = 0.0           # 信号强度 0-100
    target_weight: float = 0.0          # 目标仓位比例
    price: float = 0.0                  # 触发价格
    
    # 触发条件详情
    trigger_details: Dict[str, Any] = field(default_factory=dict)
    
    # 执行建议
    execution_price_type: str = "open"  # open/close/limit
    limit_price: Optional[float] = None
    urgency: str = "normal"             # urgent/normal/low
    
    def to_dict(self) -> Dict:
        return {
            "stock": self.stock,
            "action": self.action.value,
            "trigger_type": self.trigger_type.value,
            "trigger_time": self.trigger_time.isoformat(),
            "signal_score": self.signal_score,
            "target_weight": self.target_weight,
            "price": self.price,
            "trigger_details": self.trigger_details,
            "execution_price_type": self.execution_price_type,
            "limit_price": self.limit_price,
            "urgency": self.urgency,
        }


@dataclass
class Position:
    """持仓信息"""
    stock: str
    entry_date: datetime
    entry_price: float
    current_weight: float
    quantity: int = 0
    
    # 追踪信息
    highest_price: float = 0.0
    cost_price: float = 0.0
    partial_profit_done: bool = False
    consecutive_limit_up_days: int = 0
    
    # 标记
    is_limit_up_today: bool = False
    last_limit_up_date: Optional[datetime] = None
    
    def update_highest(self, price: float):
        if price > self.highest_price:
            self.highest_price = price
    
    def get_pnl_rate(self, current_price: float) -> float:
        if self.cost_price > 0:
            return current_price / self.cost_price - 1
        return 0.0
    
    def get_holding_days(self, current_date: datetime) -> int:
        return (current_date - self.entry_date).days


class EventDrivenEngineV6:
    """
    事件驱动交易引擎 V6.0
    
    核心特性:
    1. 实时信号监测
    2. 条件触发交易（非固定周期）
    3. 涨停板特殊处理
    4. 动态仓位管理
    5. 多信号融合决策
    """
    
    def __init__(self, strategy_params: Dict[str, Any] = None):
        """
        初始化引擎
        
        Args:
            strategy_params: 策略参数（来自MarketCharacterClassifierV6）
        """
        self.params = strategy_params or self._default_params()
        self.positions: Dict[str, Position] = {}
        self.pending_signals: List[TradeSignal] = []
        self.executed_signals: List[TradeSignal] = []
        
        # 信号阈值
        self.signal_thresholds = {
            TriggerType.FIRST_LIMIT_UP: {
                "min_vol_ratio": 2.5,
                "min_score": 80,
            },
            TriggerType.CONSECUTIVE_LIMIT_UP: {
                "min_consecutive_days": 2,
                "min_score": 75,
            },
            TriggerType.BREAKOUT: {
                "breakout_ratio": 0.05,  # 突破幅度>5%
                "min_mom_5d": 0.10,
                "min_vol_ratio": 1.5,
                "min_score": 65,
            },
            TriggerType.VOLUME_PRICE_RISE: {
                "min_mom_5d": 0.08,
                "min_vol_ratio": 2.0,
                "min_flow_strength": 0.3,
                "min_score": 60,
            },
        }
        
        logger.info("EventDrivenEngineV6 初始化完成")
    
    def _default_params(self) -> Dict[str, Any]:
        """默认参数"""
        return {
            "stop_loss_pct": -0.10,
            "take_profit_pct": 0.40,
            "partial_profit_1_pct": 0.20,
            "partial_profit_1_ratio": 0.5,
            "trailing_stop_trigger": 0.15,
            "trailing_stop_pct": -0.09,
            "time_stop_days": 20,
            "max_positions": 5,
            "single_position_max": 0.25,
            "position_cap": 1.0,
            "min_signal_score": 55,
            "limit_up_not_sell": True,
            "allow_chase_limit_up": True,
        }
    
    def update_params(self, params: Dict[str, Any]):
        """更新策略参数"""
        self.params.update(params)
        logger.info(f"策略参数已更新")
    
    def scan_buy_signals(
        self,
        factors: pd.DataFrame,
        date: datetime,
        market_data: Dict[str, pd.DataFrame] = None,
    ) -> List[TradeSignal]:
        """
        扫描买入信号
        
        Args:
            factors: 因子矩阵 (index=date, columns=stocks)
            date: 当前日期
            market_data: 市场数据
        
        Returns:
            买入信号列表
        """
        signals = []
        
        if factors is None or factors.empty:
            return signals
        
        date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
        
        # 确保有当日数据
        if date_str not in factors.index:
            # 使用最近的日期
            available_dates = [d for d in factors.index if d <= date_str]
            if not available_dates:
                return signals
            date_str = max(available_dates)
        
        # 获取当日因子
        try:
            day_factors = factors.loc[date_str]
        except:
            return signals
        
        stocks = factors.columns.tolist() if hasattr(factors, 'columns') else []
        
        for stock in stocks:
            try:
                # 提取股票因子
                stock_factors = self._extract_stock_factors(factors, stock, date_str)
                
                # 检测各类信号
                signal = self._detect_buy_signal(stock, stock_factors, date)
                
                if signal and signal.signal_score >= self.params.get("min_signal_score", 55):
                    signals.append(signal)
                    
            except Exception as e:
                continue
        
        # 按信号强度排序
        signals.sort(key=lambda x: x.signal_score, reverse=True)
        
        # 限制信号数量
        max_signals = self.params.get("max_positions", 5) * 2
        signals = signals[:max_signals]
        
        logger.info(f"扫描到 {len(signals)} 个买入信号")
        
        return signals
    
    def _extract_stock_factors(
        self, 
        factors: pd.DataFrame, 
        stock: str, 
        date_str: str,
    ) -> Dict[str, float]:
        """提取单只股票的因子"""
        result = {}
        
        # 常用因子列表
        factor_names = [
            'is_limit_up', 'is_first_limit_up', 'limit_up_count_5d', 
            'limit_up_vol_ratio', 'mom_5d', 'mom_20d', 'vol_ratio',
            'breakout_60d', 'breakout_ratio', 'flow_strength', 'rel_position'
        ]
        
        for name in factor_names:
            try:
                if name in factors.columns or (isinstance(factors, dict) and name in factors):
                    if isinstance(factors, dict):
                        df = factors[name]
                    else:
                        df = factors
                    
                    if hasattr(df, 'loc') and stock in df.columns:
                        val = df.loc[date_str, stock] if date_str in df.index else 0
                        result[name] = float(val) if pd.notna(val) else 0
                    else:
                        result[name] = 0
                else:
                    result[name] = 0
            except:
                result[name] = 0
        
        return result
    
    def _detect_buy_signal(
        self, 
        stock: str, 
        factors: Dict[str, float],
        date: datetime,
    ) -> Optional[TradeSignal]:
        """检测买入信号"""
        
        # 信号1: 首板涨停
        if factors.get('is_first_limit_up', 0) and factors.get('limit_up_vol_ratio', 0) > 2.5:
            score = 85 + min(factors.get('limit_up_vol_ratio', 0) - 2.5, 2) * 5
            return TradeSignal(
                stock=stock,
                action=TradeAction.BUY,
                trigger_type=TriggerType.FIRST_LIMIT_UP,
                trigger_time=date,
                signal_score=min(score, 100),
                target_weight=self.params.get("single_position_max", 0.25),
                trigger_details={
                    "is_first_limit_up": True,
                    "limit_up_vol_ratio": factors.get('limit_up_vol_ratio', 0),
                },
                urgency="urgent",
            )
        
        # 信号2: 连板加速
        if factors.get('limit_up_count_5d', 0) >= 2:
            score = 75 + factors.get('limit_up_count_5d', 0) * 3
            return TradeSignal(
                stock=stock,
                action=TradeAction.BUY,
                trigger_type=TriggerType.CONSECUTIVE_LIMIT_UP,
                trigger_time=date,
                signal_score=min(score, 90),
                target_weight=self.params.get("single_position_max", 0.25) * 0.8,
                trigger_details={
                    "limit_up_count_5d": factors.get('limit_up_count_5d', 0),
                },
                urgency="urgent",
            )
        
        # 信号3: 强势突破
        breakout = factors.get('breakout_60d', 0)
        breakout_ratio = factors.get('breakout_ratio', 0)
        mom_5d = factors.get('mom_5d', 0)
        vol_ratio = factors.get('vol_ratio', 0)
        
        if breakout and breakout_ratio > 0.05 and mom_5d > 0.10 and vol_ratio > 1.5:
            score = 65 + breakout_ratio * 100 + mom_5d * 50
            return TradeSignal(
                stock=stock,
                action=TradeAction.BUY,
                trigger_type=TriggerType.BREAKOUT,
                trigger_time=date,
                signal_score=min(score, 85),
                target_weight=self.params.get("single_position_max", 0.25) * 0.7,
                trigger_details={
                    "breakout_ratio": breakout_ratio,
                    "mom_5d": mom_5d,
                    "vol_ratio": vol_ratio,
                },
                urgency="normal",
            )
        
        # 信号4: 量价齐升
        flow_strength = factors.get('flow_strength', 0)
        if mom_5d > 0.08 and vol_ratio > 2.0 and flow_strength > 0.3:
            score = 60 + mom_5d * 80 + flow_strength * 20
            return TradeSignal(
                stock=stock,
                action=TradeAction.BUY,
                trigger_type=TriggerType.VOLUME_PRICE_RISE,
                trigger_time=date,
                signal_score=min(score, 80),
                target_weight=self.params.get("single_position_max", 0.25) * 0.6,
                trigger_details={
                    "mom_5d": mom_5d,
                    "vol_ratio": vol_ratio,
                    "flow_strength": flow_strength,
                },
                urgency="normal",
            )
        
        return None
    
    def scan_sell_signals(
        self,
        current_prices: pd.Series,
        date: datetime,
        factors: pd.DataFrame = None,
    ) -> List[TradeSignal]:
        """
        扫描卖出信号
        
        Args:
            current_prices: 当前价格
            date: 当前日期
            factors: 因子矩阵（检测涨停等）
        
        Returns:
            卖出信号列表
        """
        signals = []
        
        for stock, position in self.positions.items():
            if stock not in current_prices.index:
                continue
            
            current_price = current_prices[stock]
            pnl_rate = position.get_pnl_rate(current_price)
            holding_days = position.get_holding_days(date)
            
            # 更新最高价
            position.update_highest(current_price)
            
            # 检测是否涨停
            is_limit_up = self._check_limit_up(stock, factors, date) if factors is not None else False
            position.is_limit_up_today = is_limit_up
            
            # 涨停不卖规则
            if is_limit_up and self.params.get("limit_up_not_sell", True):
                logger.debug(f"{stock} 涨停中，不触发卖出")
                continue
            
            # 1. 硬止损
            stop_loss_pct = self.params.get("stop_loss_pct", -0.10)
            if pnl_rate <= stop_loss_pct:
                signals.append(TradeSignal(
                    stock=stock,
                    action=TradeAction.SELL,
                    trigger_type=TriggerType.STOP_LOSS,
                    trigger_time=date,
                    signal_score=100,
                    target_weight=0,
                    price=current_price,
                    trigger_details={"pnl_rate": pnl_rate, "stop_loss_pct": stop_loss_pct},
                    urgency="urgent",
                ))
                continue
            
            # 2. 移动止损
            trailing_trigger = self.params.get("trailing_stop_trigger", 0.15)
            trailing_pct = self.params.get("trailing_stop_pct", -0.09)
            
            if position.highest_price > 0:
                from_highest = current_price / position.highest_price - 1
                if pnl_rate >= trailing_trigger and from_highest <= trailing_pct:
                    signals.append(TradeSignal(
                        stock=stock,
                        action=TradeAction.SELL,
                        trigger_type=TriggerType.TRAILING_STOP,
                        trigger_time=date,
                        signal_score=95,
                        target_weight=0,
                        price=current_price,
                        trigger_details={
                            "pnl_rate": pnl_rate,
                            "from_highest": from_highest,
                        },
                        urgency="urgent",
                    ))
                    continue
            
            # 3. 全止盈
            take_profit_pct = self.params.get("take_profit_pct", 0.40)
            if pnl_rate >= take_profit_pct:
                signals.append(TradeSignal(
                    stock=stock,
                    action=TradeAction.SELL,
                    trigger_type=TriggerType.TAKE_PROFIT,
                    trigger_time=date,
                    signal_score=90,
                    target_weight=0,
                    price=current_price,
                    trigger_details={"pnl_rate": pnl_rate, "take_profit_pct": take_profit_pct},
                    urgency="normal",
                ))
                continue
            
            # 4. 第一批止盈
            partial_1_pct = self.params.get("partial_profit_1_pct", 0.20)
            partial_1_ratio = self.params.get("partial_profit_1_ratio", 0.5)
            
            if pnl_rate >= partial_1_pct and not position.partial_profit_done:
                new_weight = position.current_weight * (1 - partial_1_ratio)
                signals.append(TradeSignal(
                    stock=stock,
                    action=TradeAction.REDUCE,
                    trigger_type=TriggerType.TAKE_PROFIT,
                    trigger_time=date,
                    signal_score=85,
                    target_weight=new_weight,
                    price=current_price,
                    trigger_details={
                        "pnl_rate": pnl_rate,
                        "partial_profit_1_pct": partial_1_pct,
                        "reduce_ratio": partial_1_ratio,
                    },
                    urgency="normal",
                ))
                position.partial_profit_done = True
                continue
            
            # 5. 时间止损
            time_stop_days = self.params.get("time_stop_days", 20)
            if holding_days >= time_stop_days and pnl_rate < 0:
                signals.append(TradeSignal(
                    stock=stock,
                    action=TradeAction.SELL,
                    trigger_type=TriggerType.TIME_STOP,
                    trigger_time=date,
                    signal_score=70,
                    target_weight=0,
                    price=current_price,
                    trigger_details={
                        "holding_days": holding_days,
                        "pnl_rate": pnl_rate,
                    },
                    urgency="low",
                ))
        
        return signals
    
    def _check_limit_up(
        self, 
        stock: str, 
        factors: pd.DataFrame, 
        date: datetime,
    ) -> bool:
        """检查是否涨停"""
        try:
            date_str = date.strftime('%Y-%m-%d') if isinstance(date, datetime) else date
            
            if 'is_limit_up' in factors.columns or (isinstance(factors, dict) and 'is_limit_up' in factors):
                if isinstance(factors, dict):
                    df = factors['is_limit_up']
                else:
                    df = factors
                
                if hasattr(df, 'loc') and stock in df.columns:
                    val = df.loc[date_str, stock] if date_str in df.index else False
                    return bool(val) if pd.notna(val) else False
        except:
            pass
        return False
    
    def execute_signals(
        self,
        buy_signals: List[TradeSignal],
        sell_signals: List[TradeSignal],
        current_portfolio_value: float,
    ) -> Tuple[List[TradeSignal], List[TradeSignal]]:
        """
        执行交易信号
        
        Args:
            buy_signals: 买入信号
            sell_signals: 卖出信号
            current_portfolio_value: 当前组合价值
        
        Returns:
            (executed_buys, executed_sells)
        """
        executed_buys = []
        executed_sells = []
        
        # 1. 先执行卖出信号（释放资金）
        for signal in sell_signals:
            if signal.stock in self.positions:
                if signal.action == TradeAction.SELL:
                    del self.positions[signal.stock]
                    executed_sells.append(signal)
                    logger.info(f"执行卖出: {signal.stock} ({signal.trigger_type.value})")
                    
                elif signal.action == TradeAction.REDUCE:
                    self.positions[signal.stock].current_weight = signal.target_weight
                    executed_sells.append(signal)
                    logger.info(f"执行减仓: {signal.stock} -> {signal.target_weight:.1%}")
        
        # 2. 计算可用仓位
        current_position_sum = sum(p.current_weight for p in self.positions.values())
        position_cap = self.params.get("position_cap", 1.0)
        available_position = position_cap - current_position_sum
        
        # 3. 执行买入信号
        max_positions = self.params.get("max_positions", 5)
        
        for signal in buy_signals:
            # 检查持仓数量限制
            if len(self.positions) >= max_positions:
                break
            
            # 检查是否已持有
            if signal.stock in self.positions:
                continue
            
            # 检查可用仓位
            target_weight = min(signal.target_weight, available_position)
            if target_weight < 0.05:  # 最小仓位5%
                continue
            
            # 创建持仓
            self.positions[signal.stock] = Position(
                stock=signal.stock,
                entry_date=signal.trigger_time,
                entry_price=signal.price,
                current_weight=target_weight,
                cost_price=signal.price,
                highest_price=signal.price,
            )
            
            available_position -= target_weight
            executed_buys.append(signal)
            logger.info(f"执行买入: {signal.stock} ({signal.trigger_type.value}) 仓位={target_weight:.1%}")
        
        return executed_buys, executed_sells
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """获取组合摘要"""
        total_weight = sum(p.current_weight for p in self.positions.values())
        
        return {
            "total_positions": len(self.positions),
            "total_weight": total_weight,
            "positions": {
                stock: {
                    "weight": p.current_weight,
                    "entry_date": p.entry_date.isoformat() if isinstance(p.entry_date, datetime) else p.entry_date,
                    "entry_price": p.entry_price,
                    "cost_price": p.cost_price,
                    "highest_price": p.highest_price,
                }
                for stock, p in self.positions.items()
            },
        }
    
    def get_trading_rules_summary(self) -> str:
        """获取交易规则摘要"""
        p = self.params
        
        return f"""
========================================
事件驱动交易引擎 V6.0 - 交易规则
========================================

【买入触发条件】(满足任一即可触发)
1. 首板涨停: is_first_limit_up + 量比>2.5 → 次日买入
2. 连板加速: 近5日涨停>=2次 → 追涨
3. 强势突破: 突破60日高点>5% + 5日动量>10% + 量比>1.5
4. 量价齐升: 5日动量>8% + 量比>2.0 + 资金流入>0.3

【卖出触发条件】
1. 涨停不卖: {p.get('limit_up_not_sell', True)}
2. 硬止损: 亏损 {abs(p.get('stop_loss_pct', 0))*100:.0f}%
3. 移动止损: 盈利>{p.get('trailing_stop_trigger', 0)*100:.0f}%后回撤{abs(p.get('trailing_stop_pct', 0))*100:.0f}%
4. 第一批止盈: 盈利{p.get('partial_profit_1_pct', 0)*100:.0f}% 卖{p.get('partial_profit_1_ratio', 0)*100:.0f}%
5. 全止盈: 盈利{p.get('take_profit_pct', 0)*100:.0f}%
6. 时间止损: 持仓{p.get('time_stop_days', 0)}天且亏损

【仓位管理】
- 最大持仓: {p.get('max_positions', 0)}只
- 单只上限: {p.get('single_position_max', 0)*100:.0f}%
- 总仓位上限: {p.get('position_cap', 0)*100:.0f}%

========================================
"""


# ============ 测试函数 ============

def test_event_driven_engine():
    """测试事件驱动引擎"""
    print("=" * 60)
    print("EventDrivenEngineV6 测试")
    print("=" * 60)
    
    # 使用激进参数
    params = {
        "stop_loss_pct": -0.12,
        "take_profit_pct": 0.50,
        "partial_profit_1_pct": 0.25,
        "partial_profit_1_ratio": 0.5,
        "trailing_stop_trigger": 0.20,
        "trailing_stop_pct": -0.12,
        "max_positions": 5,
        "single_position_max": 0.30,
        "position_cap": 1.0,
        "min_signal_score": 50,
        "limit_up_not_sell": True,
        "allow_chase_limit_up": True,
    }
    
    engine = EventDrivenEngineV6(params)
    
    # 打印交易规则
    print(engine.get_trading_rules_summary())
    
    # 模拟信号检测
    print("\n模拟信号检测:")
    print("-" * 40)
    
    # 模拟因子数据
    mock_factors = {
        "is_first_limit_up": True,
        "limit_up_vol_ratio": 3.2,
        "limit_up_count_5d": 1,
        "mom_5d": 0.12,
        "vol_ratio": 2.5,
    }
    
    signal = engine._detect_buy_signal(
        stock="000001.XSHE",
        factors=mock_factors,
        date=datetime.now(),
    )
    
    if signal:
        print(f"检测到信号:")
        print(f"  股票: {signal.stock}")
        print(f"  类型: {signal.trigger_type.value}")
        print(f"  得分: {signal.signal_score:.1f}")
        print(f"  目标仓位: {signal.target_weight:.1%}")
        print(f"  紧急度: {signal.urgency}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_event_driven_engine()
