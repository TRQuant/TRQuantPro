#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AdaptiveStrategyManager - 自适应策略管理器
==========================================

核心功能：
1. 根据市场环境自动切换策略
2. 管理多策略组合
3. 动态调整仓位
4. 风险控制集成

策略切换逻辑：
- BULL (牛市): 动量策略、成长策略、十倍股策略
- BEAR (熊市): 防守策略、现金管理、对冲策略
- VOLATILE (震荡): 波段策略、均值回归、网格交易
- RECOVERY (复苏): 价值策略、早期布局、逆向投资
- DISTRIBUTION (派发): 减仓策略、锁利策略、防御转换
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """策略类型"""
    MOMENTUM = "momentum"           # 动量策略
    GROWTH = "growth"               # 成长策略
    TENBAGGER = "tenbagger"         # 十倍股策略
    VALUE = "value"                 # 价值策略
    DIVIDEND = "dividend"           # 高股息策略
    SWING = "swing"                 # 波段策略
    MEAN_REVERSION = "mean_reversion"  # 均值回归
    DEFENSIVE = "defensive"         # 防守策略
    HEDGING = "hedging"             # 对冲策略
    CASH = "cash"                   # 现金策略


@dataclass
class StrategyConfig:
    """策略配置"""
    strategy_type: StrategyType
    weight: float = 1.0             # 策略权重
    max_position: float = 1.0       # 最大仓位
    min_position: float = 0.0       # 最小仓位
    stop_loss: float = 0.08         # 止损比例
    take_profit: float = 0.20       # 止盈比例
    holding_period: int = 20        # 持仓周期(天)
    enabled: bool = True
    
    # 策略参数
    params: Dict = field(default_factory=dict)


@dataclass
class PositionAdvice:
    """仓位建议"""
    target_position: float          # 目标仓位
    current_regime: str             # 当前市场环境
    strategy_weights: Dict[str, float]  # 策略权重
    risk_level: str                 # 风险等级
    action: str                     # 建议操作 (BUY/SELL/HOLD)
    reason: str                     # 建议原因
    timestamp: str = ""


class AdaptiveStrategyManager:
    """
    自适应策略管理器
    
    根据市场环境动态调整策略配置
    """
    
    def __init__(self):
        # 市场环境到策略配置的映射
        self._regime_strategies: Dict[str, List[StrategyConfig]] = {
            "BULL": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.8),
            ],
            "BEAR": [
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.3),
                StrategyConfig(StrategyType.DIVIDEND, weight=0.3, max_position=0.3),
                StrategyConfig(StrategyType.CASH, weight=0.3, max_position=0.0),
            ],
            "VOLATILE": [
                StrategyConfig(StrategyType.SWING, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.MEAN_REVERSION, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.2, max_position=0.3),
            ],
            "RECOVERY": [
                StrategyConfig(StrategyType.VALUE, weight=0.3, max_position=0.7),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.6),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.6),
            ],
            "DISTRIBUTION": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.2, max_position=0.4, 
                             params={"exit_mode": True}),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.4),
                StrategyConfig(StrategyType.CASH, weight=0.4, max_position=0.0),
            ]
        }
        
        # 当前激活的策略
        self._active_strategies: List[StrategyConfig] = []
        self._current_regime: str = ""
        self._regime_history: List[Dict] = []
        
        # 仓位管理
        self._current_position: float = 0.0
        self._target_position: float = 0.0
        
        # 策略执行器
        self._strategy_executors: Dict[StrategyType, Callable] = {}
        
    def update_regime(self, regime: str, confidence: float = 0.5) -> Dict[str, Any]:
        """
        更新市场环境，触发策略切换
        
        Args:
            regime: 市场环境
            confidence: 置信度
            
        Returns:
            切换结果
        """
        old_regime = self._current_regime
        
        # 检查是否需要切换
        if regime == self._current_regime:
            return {
                "switched": False,
                "regime": regime,
                "message": "市场环境未变化"
            }
        
        # 根据置信度决定切换幅度
        transition_speed = self._calc_transition_speed(confidence)
        
        # 更新策略配置
        self._current_regime = regime
        self._active_strategies = self._regime_strategies.get(regime, [])
        
        # 记录历史
        self._regime_history.append({
            "from": old_regime,
            "to": regime,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "strategies": [s.strategy_type.value for s in self._active_strategies]
        })
        
        # 计算新的目标仓位
        self._target_position = self._calc_target_position()
        
        logger.info(f"策略切换: {old_regime} -> {regime}, 目标仓位: {self._target_position:.1%}")
        
        return {
            "switched": True,
            "from_regime": old_regime,
            "to_regime": regime,
            "confidence": confidence,
            "transition_speed": transition_speed,
            "active_strategies": [s.strategy_type.value for s in self._active_strategies],
            "target_position": self._target_position,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_position_advice(self, current_holdings: float = 0.0) -> PositionAdvice:
        """
        获取仓位建议
        
        Args:
            current_holdings: 当前持仓比例
            
        Returns:
            PositionAdvice实例
        """
        # 计算目标仓位
        target = self._target_position
        
        # 计算差异
        diff = target - current_holdings
        
        # 确定操作
        if diff > 0.1:
            action = "BUY"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议加仓{diff:.1%}"
        elif diff < -0.1:
            action = "SELL"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议减仓{abs(diff):.1%}"
        else:
            action = "HOLD"
            reason = f"仓位接近目标({target:.1%})，维持不变"
        
        # 策略权重
        weights = {s.strategy_type.value: s.weight for s in self._active_strategies}
        
        # 风险等级
        if target > 0.7:
            risk_level = "aggressive"
        elif target > 0.4:
            risk_level = "moderate"
        else:
            risk_level = "conservative"
        
        return PositionAdvice(
            target_position=target,
            current_regime=self._current_regime,
            strategy_weights=weights,
            risk_level=risk_level,
            action=action,
            reason=reason,
            timestamp=datetime.now().isoformat()
        )
    
    def get_stock_signals(self, stocks: List[str], date: str = None) -> List[Dict[str, Any]]:
        """
        获取股票信号
        
        根据当前激活的策略组合生成股票信号
        
        Args:
            stocks: 股票列表
            date: 日期
            
        Returns:
            信号列表
        """
        signals = []
        
        for stock in stocks:
            signal = {
                "stock": stock,
                "regime": self._current_regime,
                "composite_score": 0.0,
                "strategy_scores": {},
                "action": "HOLD",
                "weight": 0.0
            }
            
            # 遍历激活的策略计算信号
            total_weight = 0.0
            for strategy_config in self._active_strategies:
                if not strategy_config.enabled:
                    continue
                
                # 获取策略信号
                strategy_signal = self._get_strategy_signal(
                    stock, strategy_config, date
                )
                
                signal["strategy_scores"][strategy_config.strategy_type.value] = strategy_signal
                signal["composite_score"] += strategy_signal * strategy_config.weight
                total_weight += strategy_config.weight
            
            # 归一化
            if total_weight > 0:
                signal["composite_score"] /= total_weight
            
            # 确定操作
            if signal["composite_score"] > 0.6:
                signal["action"] = "BUY"
                signal["weight"] = min(0.2, signal["composite_score"] / 5)
            elif signal["composite_score"] < 0.3:
                signal["action"] = "SELL"
                signal["weight"] = 0.0
            else:
                signal["action"] = "HOLD"
                signal["weight"] = 0.1
            
            signals.append(signal)
        
        # 按得分排序
        signals.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return signals
    
    def _get_strategy_signal(self, stock: str, config: StrategyConfig, date: str = None) -> float:
        """获取单一策略信号"""
        # 这里应该调用具体的策略实现
        # 暂时返回模拟信号
        
        if config.strategy_type == StrategyType.MOMENTUM:
            return self._momentum_signal(stock, date)
        elif config.strategy_type == StrategyType.GROWTH:
            return self._growth_signal(stock, date)
        elif config.strategy_type == StrategyType.TENBAGGER:
            return self._tenbagger_signal(stock, date)
        elif config.strategy_type == StrategyType.VALUE:
            return self._value_signal(stock, date)
        elif config.strategy_type == StrategyType.DIVIDEND:
            return self._dividend_signal(stock, date)
        elif config.strategy_type == StrategyType.SWING:
            return self._swing_signal(stock, date)
        elif config.strategy_type == StrategyType.MEAN_REVERSION:
            return self._mean_reversion_signal(stock, date)
        elif config.strategy_type == StrategyType.DEFENSIVE:
            return self._defensive_signal(stock, date)
        
        return 0.5  # 默认中性
    
    def _momentum_signal(self, stock: str, date: str = None) -> float:
        """动量策略信号"""
        try:
            import jqdatasdk as jq
            
            # 获取价格数据
            df = jq.get_price(stock, count=60, end_date=date, 
                            fields=['close', 'volume'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            # 计算动量
            close = df['close'].values
            mom_20 = (close[-1] / close[-20] - 1) * 100
            mom_60 = (close[-1] / close[0] - 1) * 100
            
            # 成交量趋势
            vol_ratio = np.mean(df['volume'].values[-5:]) / np.mean(df['volume'].values[-20:])
            
            # 综合评分
            score = 0.5
            score += min(0.25, max(-0.25, mom_20 / 40))  # 20日动量
            score += min(0.15, max(-0.15, mom_60 / 60))  # 60日动量
            score += min(0.1, max(-0.1, (vol_ratio - 1) * 0.5))  # 成交量
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _growth_signal(self, stock: str, date: str = None) -> float:
        """成长策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            # 获取财务数据
            q = query(
                indicator.code,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.roe
            ).filter(indicator.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            revenue_growth = df['inc_revenue_year_on_year'].iloc[0] or 0
            profit_growth = df['inc_net_profit_year_on_year'].iloc[0] or 0
            roe = df['roe'].iloc[0] or 0
            
            # 评分
            score = 0.5
            score += min(0.2, revenue_growth / 100)
            score += min(0.2, profit_growth / 100)
            score += min(0.1, roe / 30)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _tenbagger_signal(self, stock: str, date: str = None) -> float:
        """十倍股策略信号"""
        try:
            from mcp_servers.utils.stage_machine import get_stage_machine
            
            machine = get_stage_machine()
            record = machine.get_stage(stock)
            
            if record is None:
                return 0.5
            
            # 根据阶段评分
            stage_scores = {
                "S0": 0.4,
                "S1": 0.6,
                "S2": 0.8,  # 最佳买入阶段
                "S3": 0.7,
                "S4": 0.5,
                "S5": 0.3
            }
            
            base_score = stage_scores.get(record.current_stage, 0.5)
            
            # 置信度加成
            score = base_score * (0.7 + record.confidence * 0.3)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _value_signal(self, stock: str, date: str = None) -> float:
        """价值策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio
            ).filter(valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            pe = df['pe_ratio'].iloc[0] or 100
            pb = df['pb_ratio'].iloc[0] or 10
            ps = df['ps_ratio'].iloc[0] or 10
            
            # 低估值加分
            score = 0.5
            if 5 < pe < 20:
                score += 0.2
            elif pe > 50:
                score -= 0.1
            
            if 0.5 < pb < 2:
                score += 0.15
            elif pb > 5:
                score -= 0.1
            
            if ps < 2:
                score += 0.15
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _dividend_signal(self, stock: str, date: str = None) -> float:
        """高股息策略信号"""
        # 简化实现
        return 0.5
    
    def _swing_signal(self, stock: str, date: str = None) -> float:
        """波段策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=20, end_date=date,
                            fields=['close', 'high', 'low'])
            
            if df is None or len(df) < 20:
                return 0.5
            
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # 计算位置
            current = close[-1]
            period_high = np.max(high)
            period_low = np.min(low)
            
            if period_high > period_low:
                position = (current - period_low) / (period_high - period_low)
            else:
                position = 0.5
            
            # 低位买入，高位卖出
            if position < 0.3:
                score = 0.7 + (0.3 - position)
            elif position > 0.7:
                score = 0.3 - (position - 0.7)
            else:
                score = 0.5
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _mean_reversion_signal(self, stock: str, date: str = None) -> float:
        """均值回归策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=60, end_date=date, fields=['close'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            close = df['close'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            
            # 偏离度
            dev_20 = (current / ma20 - 1) * 100
            dev_60 = (current / ma60 - 1) * 100
            
            # 偏离越大，回归信号越强
            score = 0.5
            if dev_20 < -10:  # 低于均线10%
                score += min(0.25, abs(dev_20) / 40)
            elif dev_20 > 10:  # 高于均线10%
                score -= min(0.25, dev_20 / 40)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _defensive_signal(self, stock: str, date: str = None) -> float:
        """防守策略信号"""
        # 偏好低波动、高股息股票
        return 0.5
    
    def _calc_transition_speed(self, confidence: float) -> str:
        """计算切换速度"""
        if confidence > 0.8:
            return "fast"
        elif confidence > 0.5:
            return "normal"
        else:
            return "slow"
    
    def _calc_target_position(self) -> float:
        """计算目标仓位"""
        if not self._active_strategies:
            return 0.0
        
        # 加权平均最大仓位
        total_weight = sum(s.weight for s in self._active_strategies)
        if total_weight == 0:
            return 0.0
        
        weighted_position = sum(
            s.max_position * s.weight for s in self._active_strategies
        )
        
        return weighted_position / total_weight
    
    def get_regime_history(self) -> List[Dict]:
        """获取环境切换历史"""
        return self._regime_history
    
    def get_active_strategies(self) -> List[Dict]:
        """获取当前激活策略"""
        return [
            {
                "type": s.strategy_type.value,
                "weight": s.weight,
                "max_position": s.max_position,
                "enabled": s.enabled
            }
            for s in self._active_strategies
        ]


# 全局实例
_manager: Optional[AdaptiveStrategyManager] = None


def get_adaptive_strategy_manager() -> AdaptiveStrategyManager:
    """获取策略管理器"""
    global _manager
    if _manager is None:
        _manager = AdaptiveStrategyManager()
    return _manager


# -*- coding: utf-8 -*-
"""
AdaptiveStrategyManager - 自适应策略管理器
==========================================

核心功能：
1. 根据市场环境自动切换策略
2. 管理多策略组合
3. 动态调整仓位
4. 风险控制集成

策略切换逻辑：
- BULL (牛市): 动量策略、成长策略、十倍股策略
- BEAR (熊市): 防守策略、现金管理、对冲策略
- VOLATILE (震荡): 波段策略、均值回归、网格交易
- RECOVERY (复苏): 价值策略、早期布局、逆向投资
- DISTRIBUTION (派发): 减仓策略、锁利策略、防御转换
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """策略类型"""
    MOMENTUM = "momentum"           # 动量策略
    GROWTH = "growth"               # 成长策略
    TENBAGGER = "tenbagger"         # 十倍股策略
    VALUE = "value"                 # 价值策略
    DIVIDEND = "dividend"           # 高股息策略
    SWING = "swing"                 # 波段策略
    MEAN_REVERSION = "mean_reversion"  # 均值回归
    DEFENSIVE = "defensive"         # 防守策略
    HEDGING = "hedging"             # 对冲策略
    CASH = "cash"                   # 现金策略


@dataclass
class StrategyConfig:
    """策略配置"""
    strategy_type: StrategyType
    weight: float = 1.0             # 策略权重
    max_position: float = 1.0       # 最大仓位
    min_position: float = 0.0       # 最小仓位
    stop_loss: float = 0.08         # 止损比例
    take_profit: float = 0.20       # 止盈比例
    holding_period: int = 20        # 持仓周期(天)
    enabled: bool = True
    
    # 策略参数
    params: Dict = field(default_factory=dict)


@dataclass
class PositionAdvice:
    """仓位建议"""
    target_position: float          # 目标仓位
    current_regime: str             # 当前市场环境
    strategy_weights: Dict[str, float]  # 策略权重
    risk_level: str                 # 风险等级
    action: str                     # 建议操作 (BUY/SELL/HOLD)
    reason: str                     # 建议原因
    timestamp: str = ""


class AdaptiveStrategyManager:
    """
    自适应策略管理器
    
    根据市场环境动态调整策略配置
    """
    
    def __init__(self):
        # 市场环境到策略配置的映射
        self._regime_strategies: Dict[str, List[StrategyConfig]] = {
            "BULL": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.8),
            ],
            "BEAR": [
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.3),
                StrategyConfig(StrategyType.DIVIDEND, weight=0.3, max_position=0.3),
                StrategyConfig(StrategyType.CASH, weight=0.3, max_position=0.0),
            ],
            "VOLATILE": [
                StrategyConfig(StrategyType.SWING, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.MEAN_REVERSION, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.2, max_position=0.3),
            ],
            "RECOVERY": [
                StrategyConfig(StrategyType.VALUE, weight=0.3, max_position=0.7),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.6),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.6),
            ],
            "DISTRIBUTION": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.2, max_position=0.4, 
                             params={"exit_mode": True}),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.4),
                StrategyConfig(StrategyType.CASH, weight=0.4, max_position=0.0),
            ]
        }
        
        # 当前激活的策略
        self._active_strategies: List[StrategyConfig] = []
        self._current_regime: str = ""
        self._regime_history: List[Dict] = []
        
        # 仓位管理
        self._current_position: float = 0.0
        self._target_position: float = 0.0
        
        # 策略执行器
        self._strategy_executors: Dict[StrategyType, Callable] = {}
        
    def update_regime(self, regime: str, confidence: float = 0.5) -> Dict[str, Any]:
        """
        更新市场环境，触发策略切换
        
        Args:
            regime: 市场环境
            confidence: 置信度
            
        Returns:
            切换结果
        """
        old_regime = self._current_regime
        
        # 检查是否需要切换
        if regime == self._current_regime:
            return {
                "switched": False,
                "regime": regime,
                "message": "市场环境未变化"
            }
        
        # 根据置信度决定切换幅度
        transition_speed = self._calc_transition_speed(confidence)
        
        # 更新策略配置
        self._current_regime = regime
        self._active_strategies = self._regime_strategies.get(regime, [])
        
        # 记录历史
        self._regime_history.append({
            "from": old_regime,
            "to": regime,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "strategies": [s.strategy_type.value for s in self._active_strategies]
        })
        
        # 计算新的目标仓位
        self._target_position = self._calc_target_position()
        
        logger.info(f"策略切换: {old_regime} -> {regime}, 目标仓位: {self._target_position:.1%}")
        
        return {
            "switched": True,
            "from_regime": old_regime,
            "to_regime": regime,
            "confidence": confidence,
            "transition_speed": transition_speed,
            "active_strategies": [s.strategy_type.value for s in self._active_strategies],
            "target_position": self._target_position,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_position_advice(self, current_holdings: float = 0.0) -> PositionAdvice:
        """
        获取仓位建议
        
        Args:
            current_holdings: 当前持仓比例
            
        Returns:
            PositionAdvice实例
        """
        # 计算目标仓位
        target = self._target_position
        
        # 计算差异
        diff = target - current_holdings
        
        # 确定操作
        if diff > 0.1:
            action = "BUY"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议加仓{diff:.1%}"
        elif diff < -0.1:
            action = "SELL"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议减仓{abs(diff):.1%}"
        else:
            action = "HOLD"
            reason = f"仓位接近目标({target:.1%})，维持不变"
        
        # 策略权重
        weights = {s.strategy_type.value: s.weight for s in self._active_strategies}
        
        # 风险等级
        if target > 0.7:
            risk_level = "aggressive"
        elif target > 0.4:
            risk_level = "moderate"
        else:
            risk_level = "conservative"
        
        return PositionAdvice(
            target_position=target,
            current_regime=self._current_regime,
            strategy_weights=weights,
            risk_level=risk_level,
            action=action,
            reason=reason,
            timestamp=datetime.now().isoformat()
        )
    
    def get_stock_signals(self, stocks: List[str], date: str = None) -> List[Dict[str, Any]]:
        """
        获取股票信号
        
        根据当前激活的策略组合生成股票信号
        
        Args:
            stocks: 股票列表
            date: 日期
            
        Returns:
            信号列表
        """
        signals = []
        
        for stock in stocks:
            signal = {
                "stock": stock,
                "regime": self._current_regime,
                "composite_score": 0.0,
                "strategy_scores": {},
                "action": "HOLD",
                "weight": 0.0
            }
            
            # 遍历激活的策略计算信号
            total_weight = 0.0
            for strategy_config in self._active_strategies:
                if not strategy_config.enabled:
                    continue
                
                # 获取策略信号
                strategy_signal = self._get_strategy_signal(
                    stock, strategy_config, date
                )
                
                signal["strategy_scores"][strategy_config.strategy_type.value] = strategy_signal
                signal["composite_score"] += strategy_signal * strategy_config.weight
                total_weight += strategy_config.weight
            
            # 归一化
            if total_weight > 0:
                signal["composite_score"] /= total_weight
            
            # 确定操作
            if signal["composite_score"] > 0.6:
                signal["action"] = "BUY"
                signal["weight"] = min(0.2, signal["composite_score"] / 5)
            elif signal["composite_score"] < 0.3:
                signal["action"] = "SELL"
                signal["weight"] = 0.0
            else:
                signal["action"] = "HOLD"
                signal["weight"] = 0.1
            
            signals.append(signal)
        
        # 按得分排序
        signals.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return signals
    
    def _get_strategy_signal(self, stock: str, config: StrategyConfig, date: str = None) -> float:
        """获取单一策略信号"""
        # 这里应该调用具体的策略实现
        # 暂时返回模拟信号
        
        if config.strategy_type == StrategyType.MOMENTUM:
            return self._momentum_signal(stock, date)
        elif config.strategy_type == StrategyType.GROWTH:
            return self._growth_signal(stock, date)
        elif config.strategy_type == StrategyType.TENBAGGER:
            return self._tenbagger_signal(stock, date)
        elif config.strategy_type == StrategyType.VALUE:
            return self._value_signal(stock, date)
        elif config.strategy_type == StrategyType.DIVIDEND:
            return self._dividend_signal(stock, date)
        elif config.strategy_type == StrategyType.SWING:
            return self._swing_signal(stock, date)
        elif config.strategy_type == StrategyType.MEAN_REVERSION:
            return self._mean_reversion_signal(stock, date)
        elif config.strategy_type == StrategyType.DEFENSIVE:
            return self._defensive_signal(stock, date)
        
        return 0.5  # 默认中性
    
    def _momentum_signal(self, stock: str, date: str = None) -> float:
        """动量策略信号"""
        try:
            import jqdatasdk as jq
            
            # 获取价格数据
            df = jq.get_price(stock, count=60, end_date=date, 
                            fields=['close', 'volume'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            # 计算动量
            close = df['close'].values
            mom_20 = (close[-1] / close[-20] - 1) * 100
            mom_60 = (close[-1] / close[0] - 1) * 100
            
            # 成交量趋势
            vol_ratio = np.mean(df['volume'].values[-5:]) / np.mean(df['volume'].values[-20:])
            
            # 综合评分
            score = 0.5
            score += min(0.25, max(-0.25, mom_20 / 40))  # 20日动量
            score += min(0.15, max(-0.15, mom_60 / 60))  # 60日动量
            score += min(0.1, max(-0.1, (vol_ratio - 1) * 0.5))  # 成交量
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _growth_signal(self, stock: str, date: str = None) -> float:
        """成长策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            # 获取财务数据
            q = query(
                indicator.code,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.roe
            ).filter(indicator.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            revenue_growth = df['inc_revenue_year_on_year'].iloc[0] or 0
            profit_growth = df['inc_net_profit_year_on_year'].iloc[0] or 0
            roe = df['roe'].iloc[0] or 0
            
            # 评分
            score = 0.5
            score += min(0.2, revenue_growth / 100)
            score += min(0.2, profit_growth / 100)
            score += min(0.1, roe / 30)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _tenbagger_signal(self, stock: str, date: str = None) -> float:
        """十倍股策略信号"""
        try:
            from mcp_servers.utils.stage_machine import get_stage_machine
            
            machine = get_stage_machine()
            record = machine.get_stage(stock)
            
            if record is None:
                return 0.5
            
            # 根据阶段评分
            stage_scores = {
                "S0": 0.4,
                "S1": 0.6,
                "S2": 0.8,  # 最佳买入阶段
                "S3": 0.7,
                "S4": 0.5,
                "S5": 0.3
            }
            
            base_score = stage_scores.get(record.current_stage, 0.5)
            
            # 置信度加成
            score = base_score * (0.7 + record.confidence * 0.3)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _value_signal(self, stock: str, date: str = None) -> float:
        """价值策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio
            ).filter(valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            pe = df['pe_ratio'].iloc[0] or 100
            pb = df['pb_ratio'].iloc[0] or 10
            ps = df['ps_ratio'].iloc[0] or 10
            
            # 低估值加分
            score = 0.5
            if 5 < pe < 20:
                score += 0.2
            elif pe > 50:
                score -= 0.1
            
            if 0.5 < pb < 2:
                score += 0.15
            elif pb > 5:
                score -= 0.1
            
            if ps < 2:
                score += 0.15
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _dividend_signal(self, stock: str, date: str = None) -> float:
        """高股息策略信号"""
        # 简化实现
        return 0.5
    
    def _swing_signal(self, stock: str, date: str = None) -> float:
        """波段策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=20, end_date=date,
                            fields=['close', 'high', 'low'])
            
            if df is None or len(df) < 20:
                return 0.5
            
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # 计算位置
            current = close[-1]
            period_high = np.max(high)
            period_low = np.min(low)
            
            if period_high > period_low:
                position = (current - period_low) / (period_high - period_low)
            else:
                position = 0.5
            
            # 低位买入，高位卖出
            if position < 0.3:
                score = 0.7 + (0.3 - position)
            elif position > 0.7:
                score = 0.3 - (position - 0.7)
            else:
                score = 0.5
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _mean_reversion_signal(self, stock: str, date: str = None) -> float:
        """均值回归策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=60, end_date=date, fields=['close'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            close = df['close'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            
            # 偏离度
            dev_20 = (current / ma20 - 1) * 100
            dev_60 = (current / ma60 - 1) * 100
            
            # 偏离越大，回归信号越强
            score = 0.5
            if dev_20 < -10:  # 低于均线10%
                score += min(0.25, abs(dev_20) / 40)
            elif dev_20 > 10:  # 高于均线10%
                score -= min(0.25, dev_20 / 40)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _defensive_signal(self, stock: str, date: str = None) -> float:
        """防守策略信号"""
        # 偏好低波动、高股息股票
        return 0.5
    
    def _calc_transition_speed(self, confidence: float) -> str:
        """计算切换速度"""
        if confidence > 0.8:
            return "fast"
        elif confidence > 0.5:
            return "normal"
        else:
            return "slow"
    
    def _calc_target_position(self) -> float:
        """计算目标仓位"""
        if not self._active_strategies:
            return 0.0
        
        # 加权平均最大仓位
        total_weight = sum(s.weight for s in self._active_strategies)
        if total_weight == 0:
            return 0.0
        
        weighted_position = sum(
            s.max_position * s.weight for s in self._active_strategies
        )
        
        return weighted_position / total_weight
    
    def get_regime_history(self) -> List[Dict]:
        """获取环境切换历史"""
        return self._regime_history
    
    def get_active_strategies(self) -> List[Dict]:
        """获取当前激活策略"""
        return [
            {
                "type": s.strategy_type.value,
                "weight": s.weight,
                "max_position": s.max_position,
                "enabled": s.enabled
            }
            for s in self._active_strategies
        ]


# 全局实例
_manager: Optional[AdaptiveStrategyManager] = None


def get_adaptive_strategy_manager() -> AdaptiveStrategyManager:
    """获取策略管理器"""
    global _manager
    if _manager is None:
        _manager = AdaptiveStrategyManager()
    return _manager





















# -*- coding: utf-8 -*-
"""
AdaptiveStrategyManager - 自适应策略管理器
==========================================

核心功能：
1. 根据市场环境自动切换策略
2. 管理多策略组合
3. 动态调整仓位
4. 风险控制集成

策略切换逻辑：
- BULL (牛市): 动量策略、成长策略、十倍股策略
- BEAR (熊市): 防守策略、现金管理、对冲策略
- VOLATILE (震荡): 波段策略、均值回归、网格交易
- RECOVERY (复苏): 价值策略、早期布局、逆向投资
- DISTRIBUTION (派发): 减仓策略、锁利策略、防御转换
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """策略类型"""
    MOMENTUM = "momentum"           # 动量策略
    GROWTH = "growth"               # 成长策略
    TENBAGGER = "tenbagger"         # 十倍股策略
    VALUE = "value"                 # 价值策略
    DIVIDEND = "dividend"           # 高股息策略
    SWING = "swing"                 # 波段策略
    MEAN_REVERSION = "mean_reversion"  # 均值回归
    DEFENSIVE = "defensive"         # 防守策略
    HEDGING = "hedging"             # 对冲策略
    CASH = "cash"                   # 现金策略


@dataclass
class StrategyConfig:
    """策略配置"""
    strategy_type: StrategyType
    weight: float = 1.0             # 策略权重
    max_position: float = 1.0       # 最大仓位
    min_position: float = 0.0       # 最小仓位
    stop_loss: float = 0.08         # 止损比例
    take_profit: float = 0.20       # 止盈比例
    holding_period: int = 20        # 持仓周期(天)
    enabled: bool = True
    
    # 策略参数
    params: Dict = field(default_factory=dict)


@dataclass
class PositionAdvice:
    """仓位建议"""
    target_position: float          # 目标仓位
    current_regime: str             # 当前市场环境
    strategy_weights: Dict[str, float]  # 策略权重
    risk_level: str                 # 风险等级
    action: str                     # 建议操作 (BUY/SELL/HOLD)
    reason: str                     # 建议原因
    timestamp: str = ""


class AdaptiveStrategyManager:
    """
    自适应策略管理器
    
    根据市场环境动态调整策略配置
    """
    
    def __init__(self):
        # 市场环境到策略配置的映射
        self._regime_strategies: Dict[str, List[StrategyConfig]] = {
            "BULL": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.8),
            ],
            "BEAR": [
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.3),
                StrategyConfig(StrategyType.DIVIDEND, weight=0.3, max_position=0.3),
                StrategyConfig(StrategyType.CASH, weight=0.3, max_position=0.0),
            ],
            "VOLATILE": [
                StrategyConfig(StrategyType.SWING, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.MEAN_REVERSION, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.2, max_position=0.3),
            ],
            "RECOVERY": [
                StrategyConfig(StrategyType.VALUE, weight=0.3, max_position=0.7),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.6),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.6),
            ],
            "DISTRIBUTION": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.2, max_position=0.4, 
                             params={"exit_mode": True}),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.4),
                StrategyConfig(StrategyType.CASH, weight=0.4, max_position=0.0),
            ]
        }
        
        # 当前激活的策略
        self._active_strategies: List[StrategyConfig] = []
        self._current_regime: str = ""
        self._regime_history: List[Dict] = []
        
        # 仓位管理
        self._current_position: float = 0.0
        self._target_position: float = 0.0
        
        # 策略执行器
        self._strategy_executors: Dict[StrategyType, Callable] = {}
        
    def update_regime(self, regime: str, confidence: float = 0.5) -> Dict[str, Any]:
        """
        更新市场环境，触发策略切换
        
        Args:
            regime: 市场环境
            confidence: 置信度
            
        Returns:
            切换结果
        """
        old_regime = self._current_regime
        
        # 检查是否需要切换
        if regime == self._current_regime:
            return {
                "switched": False,
                "regime": regime,
                "message": "市场环境未变化"
            }
        
        # 根据置信度决定切换幅度
        transition_speed = self._calc_transition_speed(confidence)
        
        # 更新策略配置
        self._current_regime = regime
        self._active_strategies = self._regime_strategies.get(regime, [])
        
        # 记录历史
        self._regime_history.append({
            "from": old_regime,
            "to": regime,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "strategies": [s.strategy_type.value for s in self._active_strategies]
        })
        
        # 计算新的目标仓位
        self._target_position = self._calc_target_position()
        
        logger.info(f"策略切换: {old_regime} -> {regime}, 目标仓位: {self._target_position:.1%}")
        
        return {
            "switched": True,
            "from_regime": old_regime,
            "to_regime": regime,
            "confidence": confidence,
            "transition_speed": transition_speed,
            "active_strategies": [s.strategy_type.value for s in self._active_strategies],
            "target_position": self._target_position,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_position_advice(self, current_holdings: float = 0.0) -> PositionAdvice:
        """
        获取仓位建议
        
        Args:
            current_holdings: 当前持仓比例
            
        Returns:
            PositionAdvice实例
        """
        # 计算目标仓位
        target = self._target_position
        
        # 计算差异
        diff = target - current_holdings
        
        # 确定操作
        if diff > 0.1:
            action = "BUY"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议加仓{diff:.1%}"
        elif diff < -0.1:
            action = "SELL"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议减仓{abs(diff):.1%}"
        else:
            action = "HOLD"
            reason = f"仓位接近目标({target:.1%})，维持不变"
        
        # 策略权重
        weights = {s.strategy_type.value: s.weight for s in self._active_strategies}
        
        # 风险等级
        if target > 0.7:
            risk_level = "aggressive"
        elif target > 0.4:
            risk_level = "moderate"
        else:
            risk_level = "conservative"
        
        return PositionAdvice(
            target_position=target,
            current_regime=self._current_regime,
            strategy_weights=weights,
            risk_level=risk_level,
            action=action,
            reason=reason,
            timestamp=datetime.now().isoformat()
        )
    
    def get_stock_signals(self, stocks: List[str], date: str = None) -> List[Dict[str, Any]]:
        """
        获取股票信号
        
        根据当前激活的策略组合生成股票信号
        
        Args:
            stocks: 股票列表
            date: 日期
            
        Returns:
            信号列表
        """
        signals = []
        
        for stock in stocks:
            signal = {
                "stock": stock,
                "regime": self._current_regime,
                "composite_score": 0.0,
                "strategy_scores": {},
                "action": "HOLD",
                "weight": 0.0
            }
            
            # 遍历激活的策略计算信号
            total_weight = 0.0
            for strategy_config in self._active_strategies:
                if not strategy_config.enabled:
                    continue
                
                # 获取策略信号
                strategy_signal = self._get_strategy_signal(
                    stock, strategy_config, date
                )
                
                signal["strategy_scores"][strategy_config.strategy_type.value] = strategy_signal
                signal["composite_score"] += strategy_signal * strategy_config.weight
                total_weight += strategy_config.weight
            
            # 归一化
            if total_weight > 0:
                signal["composite_score"] /= total_weight
            
            # 确定操作
            if signal["composite_score"] > 0.6:
                signal["action"] = "BUY"
                signal["weight"] = min(0.2, signal["composite_score"] / 5)
            elif signal["composite_score"] < 0.3:
                signal["action"] = "SELL"
                signal["weight"] = 0.0
            else:
                signal["action"] = "HOLD"
                signal["weight"] = 0.1
            
            signals.append(signal)
        
        # 按得分排序
        signals.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return signals
    
    def _get_strategy_signal(self, stock: str, config: StrategyConfig, date: str = None) -> float:
        """获取单一策略信号"""
        # 这里应该调用具体的策略实现
        # 暂时返回模拟信号
        
        if config.strategy_type == StrategyType.MOMENTUM:
            return self._momentum_signal(stock, date)
        elif config.strategy_type == StrategyType.GROWTH:
            return self._growth_signal(stock, date)
        elif config.strategy_type == StrategyType.TENBAGGER:
            return self._tenbagger_signal(stock, date)
        elif config.strategy_type == StrategyType.VALUE:
            return self._value_signal(stock, date)
        elif config.strategy_type == StrategyType.DIVIDEND:
            return self._dividend_signal(stock, date)
        elif config.strategy_type == StrategyType.SWING:
            return self._swing_signal(stock, date)
        elif config.strategy_type == StrategyType.MEAN_REVERSION:
            return self._mean_reversion_signal(stock, date)
        elif config.strategy_type == StrategyType.DEFENSIVE:
            return self._defensive_signal(stock, date)
        
        return 0.5  # 默认中性
    
    def _momentum_signal(self, stock: str, date: str = None) -> float:
        """动量策略信号"""
        try:
            import jqdatasdk as jq
            
            # 获取价格数据
            df = jq.get_price(stock, count=60, end_date=date, 
                            fields=['close', 'volume'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            # 计算动量
            close = df['close'].values
            mom_20 = (close[-1] / close[-20] - 1) * 100
            mom_60 = (close[-1] / close[0] - 1) * 100
            
            # 成交量趋势
            vol_ratio = np.mean(df['volume'].values[-5:]) / np.mean(df['volume'].values[-20:])
            
            # 综合评分
            score = 0.5
            score += min(0.25, max(-0.25, mom_20 / 40))  # 20日动量
            score += min(0.15, max(-0.15, mom_60 / 60))  # 60日动量
            score += min(0.1, max(-0.1, (vol_ratio - 1) * 0.5))  # 成交量
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _growth_signal(self, stock: str, date: str = None) -> float:
        """成长策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            # 获取财务数据
            q = query(
                indicator.code,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.roe
            ).filter(indicator.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            revenue_growth = df['inc_revenue_year_on_year'].iloc[0] or 0
            profit_growth = df['inc_net_profit_year_on_year'].iloc[0] or 0
            roe = df['roe'].iloc[0] or 0
            
            # 评分
            score = 0.5
            score += min(0.2, revenue_growth / 100)
            score += min(0.2, profit_growth / 100)
            score += min(0.1, roe / 30)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _tenbagger_signal(self, stock: str, date: str = None) -> float:
        """十倍股策略信号"""
        try:
            from mcp_servers.utils.stage_machine import get_stage_machine
            
            machine = get_stage_machine()
            record = machine.get_stage(stock)
            
            if record is None:
                return 0.5
            
            # 根据阶段评分
            stage_scores = {
                "S0": 0.4,
                "S1": 0.6,
                "S2": 0.8,  # 最佳买入阶段
                "S3": 0.7,
                "S4": 0.5,
                "S5": 0.3
            }
            
            base_score = stage_scores.get(record.current_stage, 0.5)
            
            # 置信度加成
            score = base_score * (0.7 + record.confidence * 0.3)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _value_signal(self, stock: str, date: str = None) -> float:
        """价值策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio
            ).filter(valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            pe = df['pe_ratio'].iloc[0] or 100
            pb = df['pb_ratio'].iloc[0] or 10
            ps = df['ps_ratio'].iloc[0] or 10
            
            # 低估值加分
            score = 0.5
            if 5 < pe < 20:
                score += 0.2
            elif pe > 50:
                score -= 0.1
            
            if 0.5 < pb < 2:
                score += 0.15
            elif pb > 5:
                score -= 0.1
            
            if ps < 2:
                score += 0.15
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _dividend_signal(self, stock: str, date: str = None) -> float:
        """高股息策略信号"""
        # 简化实现
        return 0.5
    
    def _swing_signal(self, stock: str, date: str = None) -> float:
        """波段策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=20, end_date=date,
                            fields=['close', 'high', 'low'])
            
            if df is None or len(df) < 20:
                return 0.5
            
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # 计算位置
            current = close[-1]
            period_high = np.max(high)
            period_low = np.min(low)
            
            if period_high > period_low:
                position = (current - period_low) / (period_high - period_low)
            else:
                position = 0.5
            
            # 低位买入，高位卖出
            if position < 0.3:
                score = 0.7 + (0.3 - position)
            elif position > 0.7:
                score = 0.3 - (position - 0.7)
            else:
                score = 0.5
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _mean_reversion_signal(self, stock: str, date: str = None) -> float:
        """均值回归策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=60, end_date=date, fields=['close'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            close = df['close'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            
            # 偏离度
            dev_20 = (current / ma20 - 1) * 100
            dev_60 = (current / ma60 - 1) * 100
            
            # 偏离越大，回归信号越强
            score = 0.5
            if dev_20 < -10:  # 低于均线10%
                score += min(0.25, abs(dev_20) / 40)
            elif dev_20 > 10:  # 高于均线10%
                score -= min(0.25, dev_20 / 40)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _defensive_signal(self, stock: str, date: str = None) -> float:
        """防守策略信号"""
        # 偏好低波动、高股息股票
        return 0.5
    
    def _calc_transition_speed(self, confidence: float) -> str:
        """计算切换速度"""
        if confidence > 0.8:
            return "fast"
        elif confidence > 0.5:
            return "normal"
        else:
            return "slow"
    
    def _calc_target_position(self) -> float:
        """计算目标仓位"""
        if not self._active_strategies:
            return 0.0
        
        # 加权平均最大仓位
        total_weight = sum(s.weight for s in self._active_strategies)
        if total_weight == 0:
            return 0.0
        
        weighted_position = sum(
            s.max_position * s.weight for s in self._active_strategies
        )
        
        return weighted_position / total_weight
    
    def get_regime_history(self) -> List[Dict]:
        """获取环境切换历史"""
        return self._regime_history
    
    def get_active_strategies(self) -> List[Dict]:
        """获取当前激活策略"""
        return [
            {
                "type": s.strategy_type.value,
                "weight": s.weight,
                "max_position": s.max_position,
                "enabled": s.enabled
            }
            for s in self._active_strategies
        ]


# 全局实例
_manager: Optional[AdaptiveStrategyManager] = None


def get_adaptive_strategy_manager() -> AdaptiveStrategyManager:
    """获取策略管理器"""
    global _manager
    if _manager is None:
        _manager = AdaptiveStrategyManager()
    return _manager


# -*- coding: utf-8 -*-
"""
AdaptiveStrategyManager - 自适应策略管理器
==========================================

核心功能：
1. 根据市场环境自动切换策略
2. 管理多策略组合
3. 动态调整仓位
4. 风险控制集成

策略切换逻辑：
- BULL (牛市): 动量策略、成长策略、十倍股策略
- BEAR (熊市): 防守策略、现金管理、对冲策略
- VOLATILE (震荡): 波段策略、均值回归、网格交易
- RECOVERY (复苏): 价值策略、早期布局、逆向投资
- DISTRIBUTION (派发): 减仓策略、锁利策略、防御转换
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class StrategyType(Enum):
    """策略类型"""
    MOMENTUM = "momentum"           # 动量策略
    GROWTH = "growth"               # 成长策略
    TENBAGGER = "tenbagger"         # 十倍股策略
    VALUE = "value"                 # 价值策略
    DIVIDEND = "dividend"           # 高股息策略
    SWING = "swing"                 # 波段策略
    MEAN_REVERSION = "mean_reversion"  # 均值回归
    DEFENSIVE = "defensive"         # 防守策略
    HEDGING = "hedging"             # 对冲策略
    CASH = "cash"                   # 现金策略


@dataclass
class StrategyConfig:
    """策略配置"""
    strategy_type: StrategyType
    weight: float = 1.0             # 策略权重
    max_position: float = 1.0       # 最大仓位
    min_position: float = 0.0       # 最小仓位
    stop_loss: float = 0.08         # 止损比例
    take_profit: float = 0.20       # 止盈比例
    holding_period: int = 20        # 持仓周期(天)
    enabled: bool = True
    
    # 策略参数
    params: Dict = field(default_factory=dict)


@dataclass
class PositionAdvice:
    """仓位建议"""
    target_position: float          # 目标仓位
    current_regime: str             # 当前市场环境
    strategy_weights: Dict[str, float]  # 策略权重
    risk_level: str                 # 风险等级
    action: str                     # 建议操作 (BUY/SELL/HOLD)
    reason: str                     # 建议原因
    timestamp: str = ""


class AdaptiveStrategyManager:
    """
    自适应策略管理器
    
    根据市场环境动态调整策略配置
    """
    
    def __init__(self):
        # 市场环境到策略配置的映射
        self._regime_strategies: Dict[str, List[StrategyConfig]] = {
            "BULL": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.9),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.8),
            ],
            "BEAR": [
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.3),
                StrategyConfig(StrategyType.DIVIDEND, weight=0.3, max_position=0.3),
                StrategyConfig(StrategyType.CASH, weight=0.3, max_position=0.0),
            ],
            "VOLATILE": [
                StrategyConfig(StrategyType.SWING, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.MEAN_REVERSION, weight=0.4, max_position=0.5),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.2, max_position=0.3),
            ],
            "RECOVERY": [
                StrategyConfig(StrategyType.VALUE, weight=0.3, max_position=0.7),
                StrategyConfig(StrategyType.TENBAGGER, weight=0.4, max_position=0.6),
                StrategyConfig(StrategyType.GROWTH, weight=0.3, max_position=0.6),
            ],
            "DISTRIBUTION": [
                StrategyConfig(StrategyType.MOMENTUM, weight=0.2, max_position=0.4, 
                             params={"exit_mode": True}),
                StrategyConfig(StrategyType.DEFENSIVE, weight=0.4, max_position=0.4),
                StrategyConfig(StrategyType.CASH, weight=0.4, max_position=0.0),
            ]
        }
        
        # 当前激活的策略
        self._active_strategies: List[StrategyConfig] = []
        self._current_regime: str = ""
        self._regime_history: List[Dict] = []
        
        # 仓位管理
        self._current_position: float = 0.0
        self._target_position: float = 0.0
        
        # 策略执行器
        self._strategy_executors: Dict[StrategyType, Callable] = {}
        
    def update_regime(self, regime: str, confidence: float = 0.5) -> Dict[str, Any]:
        """
        更新市场环境，触发策略切换
        
        Args:
            regime: 市场环境
            confidence: 置信度
            
        Returns:
            切换结果
        """
        old_regime = self._current_regime
        
        # 检查是否需要切换
        if regime == self._current_regime:
            return {
                "switched": False,
                "regime": regime,
                "message": "市场环境未变化"
            }
        
        # 根据置信度决定切换幅度
        transition_speed = self._calc_transition_speed(confidence)
        
        # 更新策略配置
        self._current_regime = regime
        self._active_strategies = self._regime_strategies.get(regime, [])
        
        # 记录历史
        self._regime_history.append({
            "from": old_regime,
            "to": regime,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "strategies": [s.strategy_type.value for s in self._active_strategies]
        })
        
        # 计算新的目标仓位
        self._target_position = self._calc_target_position()
        
        logger.info(f"策略切换: {old_regime} -> {regime}, 目标仓位: {self._target_position:.1%}")
        
        return {
            "switched": True,
            "from_regime": old_regime,
            "to_regime": regime,
            "confidence": confidence,
            "transition_speed": transition_speed,
            "active_strategies": [s.strategy_type.value for s in self._active_strategies],
            "target_position": self._target_position,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_position_advice(self, current_holdings: float = 0.0) -> PositionAdvice:
        """
        获取仓位建议
        
        Args:
            current_holdings: 当前持仓比例
            
        Returns:
            PositionAdvice实例
        """
        # 计算目标仓位
        target = self._target_position
        
        # 计算差异
        diff = target - current_holdings
        
        # 确定操作
        if diff > 0.1:
            action = "BUY"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议加仓{diff:.1%}"
        elif diff < -0.1:
            action = "SELL"
            reason = f"目标仓位{target:.1%}，当前{current_holdings:.1%}，建议减仓{abs(diff):.1%}"
        else:
            action = "HOLD"
            reason = f"仓位接近目标({target:.1%})，维持不变"
        
        # 策略权重
        weights = {s.strategy_type.value: s.weight for s in self._active_strategies}
        
        # 风险等级
        if target > 0.7:
            risk_level = "aggressive"
        elif target > 0.4:
            risk_level = "moderate"
        else:
            risk_level = "conservative"
        
        return PositionAdvice(
            target_position=target,
            current_regime=self._current_regime,
            strategy_weights=weights,
            risk_level=risk_level,
            action=action,
            reason=reason,
            timestamp=datetime.now().isoformat()
        )
    
    def get_stock_signals(self, stocks: List[str], date: str = None) -> List[Dict[str, Any]]:
        """
        获取股票信号
        
        根据当前激活的策略组合生成股票信号
        
        Args:
            stocks: 股票列表
            date: 日期
            
        Returns:
            信号列表
        """
        signals = []
        
        for stock in stocks:
            signal = {
                "stock": stock,
                "regime": self._current_regime,
                "composite_score": 0.0,
                "strategy_scores": {},
                "action": "HOLD",
                "weight": 0.0
            }
            
            # 遍历激活的策略计算信号
            total_weight = 0.0
            for strategy_config in self._active_strategies:
                if not strategy_config.enabled:
                    continue
                
                # 获取策略信号
                strategy_signal = self._get_strategy_signal(
                    stock, strategy_config, date
                )
                
                signal["strategy_scores"][strategy_config.strategy_type.value] = strategy_signal
                signal["composite_score"] += strategy_signal * strategy_config.weight
                total_weight += strategy_config.weight
            
            # 归一化
            if total_weight > 0:
                signal["composite_score"] /= total_weight
            
            # 确定操作
            if signal["composite_score"] > 0.6:
                signal["action"] = "BUY"
                signal["weight"] = min(0.2, signal["composite_score"] / 5)
            elif signal["composite_score"] < 0.3:
                signal["action"] = "SELL"
                signal["weight"] = 0.0
            else:
                signal["action"] = "HOLD"
                signal["weight"] = 0.1
            
            signals.append(signal)
        
        # 按得分排序
        signals.sort(key=lambda x: x["composite_score"], reverse=True)
        
        return signals
    
    def _get_strategy_signal(self, stock: str, config: StrategyConfig, date: str = None) -> float:
        """获取单一策略信号"""
        # 这里应该调用具体的策略实现
        # 暂时返回模拟信号
        
        if config.strategy_type == StrategyType.MOMENTUM:
            return self._momentum_signal(stock, date)
        elif config.strategy_type == StrategyType.GROWTH:
            return self._growth_signal(stock, date)
        elif config.strategy_type == StrategyType.TENBAGGER:
            return self._tenbagger_signal(stock, date)
        elif config.strategy_type == StrategyType.VALUE:
            return self._value_signal(stock, date)
        elif config.strategy_type == StrategyType.DIVIDEND:
            return self._dividend_signal(stock, date)
        elif config.strategy_type == StrategyType.SWING:
            return self._swing_signal(stock, date)
        elif config.strategy_type == StrategyType.MEAN_REVERSION:
            return self._mean_reversion_signal(stock, date)
        elif config.strategy_type == StrategyType.DEFENSIVE:
            return self._defensive_signal(stock, date)
        
        return 0.5  # 默认中性
    
    def _momentum_signal(self, stock: str, date: str = None) -> float:
        """动量策略信号"""
        try:
            import jqdatasdk as jq
            
            # 获取价格数据
            df = jq.get_price(stock, count=60, end_date=date, 
                            fields=['close', 'volume'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            # 计算动量
            close = df['close'].values
            mom_20 = (close[-1] / close[-20] - 1) * 100
            mom_60 = (close[-1] / close[0] - 1) * 100
            
            # 成交量趋势
            vol_ratio = np.mean(df['volume'].values[-5:]) / np.mean(df['volume'].values[-20:])
            
            # 综合评分
            score = 0.5
            score += min(0.25, max(-0.25, mom_20 / 40))  # 20日动量
            score += min(0.15, max(-0.15, mom_60 / 60))  # 60日动量
            score += min(0.1, max(-0.1, (vol_ratio - 1) * 0.5))  # 成交量
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _growth_signal(self, stock: str, date: str = None) -> float:
        """成长策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, indicator
            
            # 获取财务数据
            q = query(
                indicator.code,
                indicator.inc_revenue_year_on_year,
                indicator.inc_net_profit_year_on_year,
                indicator.roe
            ).filter(indicator.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            revenue_growth = df['inc_revenue_year_on_year'].iloc[0] or 0
            profit_growth = df['inc_net_profit_year_on_year'].iloc[0] or 0
            roe = df['roe'].iloc[0] or 0
            
            # 评分
            score = 0.5
            score += min(0.2, revenue_growth / 100)
            score += min(0.2, profit_growth / 100)
            score += min(0.1, roe / 30)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _tenbagger_signal(self, stock: str, date: str = None) -> float:
        """十倍股策略信号"""
        try:
            from mcp_servers.utils.stage_machine import get_stage_machine
            
            machine = get_stage_machine()
            record = machine.get_stage(stock)
            
            if record is None:
                return 0.5
            
            # 根据阶段评分
            stage_scores = {
                "S0": 0.4,
                "S1": 0.6,
                "S2": 0.8,  # 最佳买入阶段
                "S3": 0.7,
                "S4": 0.5,
                "S5": 0.3
            }
            
            base_score = stage_scores.get(record.current_stage, 0.5)
            
            # 置信度加成
            score = base_score * (0.7 + record.confidence * 0.3)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _value_signal(self, stock: str, date: str = None) -> float:
        """价值策略信号"""
        try:
            import jqdatasdk as jq
            from jqdatasdk import query, valuation
            
            q = query(
                valuation.code,
                valuation.pe_ratio,
                valuation.pb_ratio,
                valuation.ps_ratio
            ).filter(valuation.code == stock)
            
            df = jq.get_fundamentals(q, date=date)
            
            if df is None or len(df) == 0:
                return 0.5
            
            pe = df['pe_ratio'].iloc[0] or 100
            pb = df['pb_ratio'].iloc[0] or 10
            ps = df['ps_ratio'].iloc[0] or 10
            
            # 低估值加分
            score = 0.5
            if 5 < pe < 20:
                score += 0.2
            elif pe > 50:
                score -= 0.1
            
            if 0.5 < pb < 2:
                score += 0.15
            elif pb > 5:
                score -= 0.1
            
            if ps < 2:
                score += 0.15
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _dividend_signal(self, stock: str, date: str = None) -> float:
        """高股息策略信号"""
        # 简化实现
        return 0.5
    
    def _swing_signal(self, stock: str, date: str = None) -> float:
        """波段策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=20, end_date=date,
                            fields=['close', 'high', 'low'])
            
            if df is None or len(df) < 20:
                return 0.5
            
            close = df['close'].values
            high = df['high'].values
            low = df['low'].values
            
            # 计算位置
            current = close[-1]
            period_high = np.max(high)
            period_low = np.min(low)
            
            if period_high > period_low:
                position = (current - period_low) / (period_high - period_low)
            else:
                position = 0.5
            
            # 低位买入，高位卖出
            if position < 0.3:
                score = 0.7 + (0.3 - position)
            elif position > 0.7:
                score = 0.3 - (position - 0.7)
            else:
                score = 0.5
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _mean_reversion_signal(self, stock: str, date: str = None) -> float:
        """均值回归策略信号"""
        try:
            import jqdatasdk as jq
            
            df = jq.get_price(stock, count=60, end_date=date, fields=['close'])
            
            if df is None or len(df) < 60:
                return 0.5
            
            close = df['close'].values
            ma20 = np.mean(close[-20:])
            ma60 = np.mean(close[-60:])
            current = close[-1]
            
            # 偏离度
            dev_20 = (current / ma20 - 1) * 100
            dev_60 = (current / ma60 - 1) * 100
            
            # 偏离越大，回归信号越强
            score = 0.5
            if dev_20 < -10:  # 低于均线10%
                score += min(0.25, abs(dev_20) / 40)
            elif dev_20 > 10:  # 高于均线10%
                score -= min(0.25, dev_20 / 40)
            
            return max(0, min(1, score))
        except:
            return 0.5
    
    def _defensive_signal(self, stock: str, date: str = None) -> float:
        """防守策略信号"""
        # 偏好低波动、高股息股票
        return 0.5
    
    def _calc_transition_speed(self, confidence: float) -> str:
        """计算切换速度"""
        if confidence > 0.8:
            return "fast"
        elif confidence > 0.5:
            return "normal"
        else:
            return "slow"
    
    def _calc_target_position(self) -> float:
        """计算目标仓位"""
        if not self._active_strategies:
            return 0.0
        
        # 加权平均最大仓位
        total_weight = sum(s.weight for s in self._active_strategies)
        if total_weight == 0:
            return 0.0
        
        weighted_position = sum(
            s.max_position * s.weight for s in self._active_strategies
        )
        
        return weighted_position / total_weight
    
    def get_regime_history(self) -> List[Dict]:
        """获取环境切换历史"""
        return self._regime_history
    
    def get_active_strategies(self) -> List[Dict]:
        """获取当前激活策略"""
        return [
            {
                "type": s.strategy_type.value,
                "weight": s.weight,
                "max_position": s.max_position,
                "enabled": s.enabled
            }
            for s in self._active_strategies
        ]


# 全局实例
_manager: Optional[AdaptiveStrategyManager] = None


def get_adaptive_strategy_manager() -> AdaptiveStrategyManager:
    """获取策略管理器"""
    global _manager
    if _manager is None:
        _manager = AdaptiveStrategyManager()
    return _manager








































