# -*- coding: utf-8 -*-
"""
Resonance V2 Strategy Layer
===========================

策略层：基于HMM状态和共振评分生成交易信号。

核心功能：
1. 信号生成: Signal = ResScore × StateWeight × RiskGate
2. 仓位管理: 根据状态动态调整仓位上限
3. 退出规则: 硬止损、ATR止损、状态切换止损

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

from .config import ResonanceV2Config, MarketState, DEFAULT_CONFIG
from .feature_layer import ResonanceScore
from .hmm_state_layer import HMMPrediction

logger = logging.getLogger(__name__)


class SignalType(Enum):
    """信号类型"""
    STRONG_BUY = "strong_buy"      # 强买入
    BUY = "buy"                    # 买入
    HOLD = "hold"                  # 持有
    REDUCE = "reduce"             # 减仓
    SELL = "sell"                  # 卖出
    STRONG_SELL = "strong_sell"    # 强卖出


class ExitReason(Enum):
    """退出原因"""
    NONE = "none"
    HARD_STOP = "hard_stop"        # 硬止损
    ATR_STOP = "atr_stop"          # ATR止损
    STATE_SWITCH = "state_switch"  # 状态切换止损
    TAKE_PROFIT = "take_profit"    # 止盈
    TRAILING_STOP = "trailing_stop"  # 移动止损
    TIME_EXIT = "time_exit"        # 时间止损


@dataclass
class TradingSignal:
    """交易信号"""
    signal_type: SignalType
    signal_strength: float         # 信号强度 (0-100)
    target_position: float         # 目标仓位 (0-1)
    
    # 信号来源
    resonance_score: float
    hmm_state: MarketState
    hmm_confidence: float
    
    # 风险控制
    stop_loss: float              # 止损价格
    take_profit: Optional[float]  # 止盈价格
    
    # 退出信号
    exit_signal: bool = False
    exit_reason: ExitReason = ExitReason.NONE
    
    # 元数据
    timestamp: str = ""
    details: Dict = field(default_factory=dict)


@dataclass
class Position:
    """持仓信息"""
    code: str
    entry_price: float
    entry_date: str
    quantity: float
    current_price: float
    
    # 止损止盈
    stop_loss_price: float
    take_profit_price: Optional[float]
    highest_price: float         # 用于移动止损
    
    # 状态
    entry_state: MarketState     # 入场时的市场状态
    
    @property
    def unrealized_pnl(self) -> float:
        """未实现盈亏"""
        return (self.current_price - self.entry_price) / self.entry_price
    
    @property
    def unrealized_pnl_amount(self) -> float:
        """未实现盈亏金额"""
        return (self.current_price - self.entry_price) * self.quantity


class ResonanceStrategy:
    """
    共振策略
    
    核心规则：
    1. 仅在Risk-On状态允许开仓
    2. Risk-Off状态强制降仓
    3. 共振评分决定仓位级别
    4. 状态切换触发止损
    """
    
    def __init__(self, config: Optional[ResonanceV2Config] = None):
        """
        初始化策略
        
        Args:
            config: 配置对象
        """
        self.config = config or DEFAULT_CONFIG
        
        # 持仓管理
        self.positions: Dict[str, Position] = {}
        
        # 状态权重映射
        self.state_weights = {
            MarketState.RISK_ON: 1.0,
            MarketState.SIDEWAYS: 0.6,
            MarketState.HIGH_VOL: 0.5,
            MarketState.RISK_OFF: 0.3,
        }
        
        logger.info("ResonanceStrategy初始化完成")
    
    def generate_signal(
        self,
        resonance_score: ResonanceScore,
        hmm_prediction: HMMPrediction,
        current_price: float,
        atr: Optional[float] = None
    ) -> TradingSignal:
        """
        生成交易信号
        
        公式: Signal = ResScore × StateWeight × RiskGate
        
        Args:
            resonance_score: 共振评分
            hmm_prediction: HMM预测结果
            current_price: 当前价格
            atr: ATR值（用于计算止损）
        
        Returns:
            TradingSignal: 交易信号
        """
        # 1. 获取基础参数
        res_score = resonance_score.total_score
        market_state = hmm_prediction.market_state
        hmm_confidence = hmm_prediction.confidence
        state_weight = self.state_weights.get(market_state, 0.5)
        
        # 2. 风险闸门
        risk_gate = self._calculate_risk_gate(market_state, hmm_confidence)
        
        # 3. 计算信号强度
        signal_strength = res_score * state_weight * risk_gate
        
        # 4. 确定信号类型
        signal_type = self._determine_signal_type(
            signal_strength, market_state, hmm_prediction.regime_change
        )
        
        # 5. 计算目标仓位
        target_position = self._calculate_target_position(
            signal_strength, market_state, resonance_score.level
        )
        
        # 6. 计算止损止盈
        stop_loss = self._calculate_stop_loss(current_price, atr)
        take_profit = self._calculate_take_profit(current_price, signal_strength)
        
        # 7. 检查退出信号
        exit_signal, exit_reason = self._check_exit_signals(
            market_state, hmm_prediction.regime_change
        )
        
        return TradingSignal(
            signal_type=signal_type,
            signal_strength=signal_strength,
            target_position=target_position if not exit_signal else 0.0,
            resonance_score=res_score,
            hmm_state=market_state,
            hmm_confidence=hmm_confidence,
            stop_loss=stop_loss,
            take_profit=take_profit,
            exit_signal=exit_signal,
            exit_reason=exit_reason,
            details={
                'state_weight': state_weight,
                'risk_gate': risk_gate,
                'resonance_level': resonance_score.level,
                'regime_change': hmm_prediction.regime_change,
            }
        )
    
    def _calculate_risk_gate(
        self,
        market_state: MarketState,
        hmm_confidence: float
    ) -> float:
        """
        计算风险闸门
        
        规则：
        - Risk-On + 高置信度: 1.0
        - Risk-Off: 0.3 (强制降低)
        - 低置信度: 降低权重
        """
        base_gate = 1.0
        
        # 状态调整
        if market_state == MarketState.RISK_OFF:
            base_gate *= 0.3
        elif market_state == MarketState.HIGH_VOL:
            base_gate *= 0.5
        elif market_state == MarketState.SIDEWAYS:
            base_gate *= 0.7
        
        # 置信度调整
        if hmm_confidence < 0.5:
            base_gate *= 0.7
        elif hmm_confidence < 0.7:
            base_gate *= 0.85
        
        return base_gate
    
    def _determine_signal_type(
        self,
        signal_strength: float,
        market_state: MarketState,
        regime_change: bool
    ) -> SignalType:
        """确定信号类型"""
        # 状态切换时强制减仓
        if regime_change and market_state == MarketState.RISK_OFF:
            return SignalType.STRONG_SELL
        
        if regime_change and market_state in [MarketState.HIGH_VOL, MarketState.SIDEWAYS]:
            return SignalType.REDUCE
        
        # 基于信号强度
        if signal_strength >= 80:
            return SignalType.STRONG_BUY
        elif signal_strength >= 60:
            return SignalType.BUY
        elif signal_strength >= 40:
            return SignalType.HOLD
        elif signal_strength >= 20:
            return SignalType.REDUCE
        elif signal_strength >= 10:
            return SignalType.SELL
        else:
            return SignalType.STRONG_SELL
    
    def _calculate_target_position(
        self,
        signal_strength: float,
        market_state: MarketState,
        resonance_level: str
    ) -> float:
        """
        计算目标仓位
        
        规则：
        - 基于共振级别确定基础仓位
        - 根据市场状态调整上限
        - 信号强度微调
        """
        # 基础仓位（基于共振级别）
        level_positions = {
            'full': 1.0,
            'add': 0.7,
            'trial': 0.4,
            'none': 0.0,
        }
        base_position = level_positions.get(resonance_level, 0.0)
        
        # 市场状态上限
        position_cap = self.config.get_position_cap(market_state)
        
        # 信号强度微调
        strength_factor = signal_strength / 100.0
        
        # 最终仓位
        target = min(base_position * strength_factor, position_cap)
        
        return max(0.0, min(target, 1.0))
    
    def _calculate_stop_loss(
        self,
        current_price: float,
        atr: Optional[float]
    ) -> float:
        """
        计算止损价格
        
        规则：
        - 硬止损: 8%
        - ATR止损: 2倍ATR
        - 取二者中更近的
        """
        # 硬止损
        hard_stop = current_price * (1 - self.config.hard_stop)
        
        # ATR止损
        if atr is not None and atr > 0:
            atr_stop = current_price - self.config.atr_stop_multiplier * atr
            return max(hard_stop, atr_stop)  # 取更近的止损
        
        return hard_stop
    
    def _calculate_take_profit(
        self,
        current_price: float,
        signal_strength: float
    ) -> Optional[float]:
        """
        计算止盈价格
        
        规则：
        - 强信号: 30%止盈
        - 中等信号: 20%止盈
        - 弱信号: 不设止盈
        """
        if signal_strength >= 70:
            return current_price * 1.30
        elif signal_strength >= 50:
            return current_price * 1.20
        else:
            return None
    
    def _check_exit_signals(
        self,
        market_state: MarketState,
        regime_change: bool
    ) -> Tuple[bool, ExitReason]:
        """
        检查退出信号
        
        规则：
        - Risk-On → Risk-Off: 立即降仓
        - Risk-On → High-Vol: 减仓
        """
        if regime_change:
            if market_state == MarketState.RISK_OFF:
                return True, ExitReason.STATE_SWITCH
            elif market_state == MarketState.HIGH_VOL:
                return True, ExitReason.STATE_SWITCH
        
        return False, ExitReason.NONE
    
    def check_position_exits(
        self,
        position: Position,
        current_price: float,
        current_state: MarketState
    ) -> Tuple[bool, ExitReason]:
        """
        检查持仓的退出条件
        
        Args:
            position: 持仓信息
            current_price: 当前价格
            current_state: 当前市场状态
        
        Returns:
            Tuple: (是否退出, 退出原因)
        """
        # 更新最高价
        position.highest_price = max(position.highest_price, current_price)
        position.current_price = current_price
        
        pnl = position.unrealized_pnl
        
        # 1. 硬止损
        if current_price <= position.stop_loss_price:
            return True, ExitReason.HARD_STOP
        
        # 2. 止盈
        if position.take_profit_price and current_price >= position.take_profit_price:
            return True, ExitReason.TAKE_PROFIT
        
        # 3. 移动止损（盈利超过15%后启用）
        if pnl >= self.config.trailing_stop_activate:
            trailing_stop = position.highest_price * (1 + self.config.trailing_stop_distance)
            if current_price <= trailing_stop:
                return True, ExitReason.TRAILING_STOP
        
        # 4. 状态切换止损
        if current_state == MarketState.RISK_OFF and position.entry_state == MarketState.RISK_ON:
            return True, ExitReason.STATE_SWITCH
        
        return False, ExitReason.NONE
    
    def update_position(
        self,
        code: str,
        entry_price: float,
        entry_date: str,
        quantity: float,
        stop_loss_price: float,
        take_profit_price: Optional[float],
        market_state: MarketState
    ):
        """更新持仓"""
        self.positions[code] = Position(
            code=code,
            entry_price=entry_price,
            entry_date=entry_date,
            quantity=quantity,
            current_price=entry_price,
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
            highest_price=entry_price,
            entry_state=market_state
        )
    
    def close_position(self, code: str) -> Optional[Position]:
        """关闭持仓"""
        return self.positions.pop(code, None)
    
    def get_position(self, code: str) -> Optional[Position]:
        """获取持仓"""
        return self.positions.get(code)
    
    def get_all_positions(self) -> Dict[str, Position]:
        """获取所有持仓"""
        return self.positions.copy()
    
    def get_total_exposure(self) -> float:
        """获取总敞口"""
        return sum(p.quantity * p.current_price for p in self.positions.values())


class SignalAggregator:
    """
    信号聚合器
    
    将多个标的的信号聚合为组合级别的决策
    """
    
    def __init__(self, config: Optional[ResonanceV2Config] = None):
        self.config = config or DEFAULT_CONFIG
    
    def aggregate_signals(
        self,
        signals: Dict[str, TradingSignal],
        max_positions: int = 10
    ) -> Dict[str, float]:
        """
        聚合信号，输出目标权重
        
        Args:
            signals: 股票代码 -> 信号 映射
            max_positions: 最大持仓数
        
        Returns:
            Dict[str, float]: 股票代码 -> 目标权重
        """
        # 筛选买入信号
        buy_signals = {
            code: sig for code, sig in signals.items()
            if sig.signal_type in [SignalType.STRONG_BUY, SignalType.BUY]
            and sig.target_position > 0
        }
        
        if not buy_signals:
            return {}
        
        # 按信号强度排序
        sorted_signals = sorted(
            buy_signals.items(),
            key=lambda x: x[1].signal_strength,
            reverse=True
        )[:max_positions]
        
        # 计算权重
        total_strength = sum(sig.signal_strength for _, sig in sorted_signals)
        
        if total_strength == 0:
            # 等权
            weight = 1.0 / len(sorted_signals)
            return {code: weight for code, _ in sorted_signals}
        
        # 按信号强度加权
        return {
            code: sig.signal_strength / total_strength
            for code, sig in sorted_signals
        }
    
    def generate_rebalance_orders(
        self,
        current_weights: Dict[str, float],
        target_weights: Dict[str, float],
        total_value: float,
        min_trade_value: float = 10000
    ) -> Dict[str, float]:
        """
        生成再平衡订单
        
        Args:
            current_weights: 当前权重
            target_weights: 目标权重
            total_value: 总资产价值
            min_trade_value: 最小交易金额
        
        Returns:
            Dict[str, float]: 股票代码 -> 交易金额（正=买入，负=卖出）
        """
        orders = {}
        
        all_codes = set(current_weights.keys()) | set(target_weights.keys())
        
        for code in all_codes:
            current = current_weights.get(code, 0)
            target = target_weights.get(code, 0)
            
            diff_weight = target - current
            diff_value = diff_weight * total_value
            
            if abs(diff_value) >= min_trade_value:
                orders[code] = diff_value
        
        return orders
