#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Strategy Switching Knowledge Base - 策略切换知识库
=================================================

基于网络研究构建的策略切换知识库：
1. 环境切换条件
2. 切换冷却期
3. 切换确认机制
4. 策略过渡逻辑
5. 风险控制规则
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np
import pandas as pd

from .astock_regime_knowledge_v2 import AStockRegime, ASTOCK_REGIME_STRATEGY


# ============== 切换条件知识 ==============

@dataclass
class SwitchCondition:
    """切换条件"""
    from_regime: AStockRegime
    to_regime: AStockRegime
    score_threshold: float      # 分数阈值
    confirm_days: int           # 确认天数
    cooldown_days: int          # 冷却期
    position_adjustment: str    # 仓位调整策略: immediate/gradual/none
    risk_level: str             # 风险等级: low/medium/high


# 切换条件矩阵
SWITCH_CONDITIONS = {
    # 从牛市初期切换
    (AStockRegime.BULL_EARLY, AStockRegime.BULL_MID): SwitchCondition(
        AStockRegime.BULL_EARLY, AStockRegime.BULL_MID,
        score_threshold=35, confirm_days=1, cooldown_days=3,
        position_adjustment="none", risk_level="low"
    ),
    (AStockRegime.BULL_EARLY, AStockRegime.BULL_LATE): SwitchCondition(
        AStockRegime.BULL_EARLY, AStockRegime.BULL_LATE,
        score_threshold=25, confirm_days=2, cooldown_days=5,
        position_adjustment="gradual", risk_level="medium"
    ),
    (AStockRegime.BULL_EARLY, AStockRegime.BEAR_PANIC): SwitchCondition(
        AStockRegime.BULL_EARLY, AStockRegime.BEAR_PANIC,
        score_threshold=-60, confirm_days=1, cooldown_days=0,  # 紧急！无冷却期
        position_adjustment="immediate", risk_level="high"
    ),
    
    # 从牛市中期切换
    (AStockRegime.BULL_MID, AStockRegime.BULL_LATE): SwitchCondition(
        AStockRegime.BULL_MID, AStockRegime.BULL_LATE,
        score_threshold=25, confirm_days=2, cooldown_days=3,
        position_adjustment="gradual", risk_level="low"
    ),
    (AStockRegime.BULL_MID, AStockRegime.VOLATILE_DOWN): SwitchCondition(
        AStockRegime.BULL_MID, AStockRegime.VOLATILE_DOWN,
        score_threshold=-15, confirm_days=2, cooldown_days=5,
        position_adjustment="gradual", risk_level="medium"
    ),
    (AStockRegime.BULL_MID, AStockRegime.BEAR_PANIC): SwitchCondition(
        AStockRegime.BULL_MID, AStockRegime.BEAR_PANIC,
        score_threshold=-60, confirm_days=1, cooldown_days=0,
        position_adjustment="immediate", risk_level="high"
    ),
    
    # 从熊市切换
    (AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING): SwitchCondition(
        AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING,
        score_threshold=-40, confirm_days=3, cooldown_days=10,
        position_adjustment="gradual", risk_level="high"
    ),
    (AStockRegime.BEAR_GRINDING, AStockRegime.VOLATILE_UP): SwitchCondition(
        AStockRegime.BEAR_GRINDING, AStockRegime.VOLATILE_UP,
        score_threshold=15, confirm_days=3, cooldown_days=10,
        position_adjustment="gradual", risk_level="medium"
    ),
    (AStockRegime.BEAR_GRINDING, AStockRegime.BULL_EARLY): SwitchCondition(
        AStockRegime.BEAR_GRINDING, AStockRegime.BULL_EARLY,
        score_threshold=40, confirm_days=5, cooldown_days=15,  # 需要更多确认
        position_adjustment="gradual", risk_level="medium"
    ),
    
    # 震荡市切换
    (AStockRegime.VOLATILE_RANGE, AStockRegime.VOLATILE_UP): SwitchCondition(
        AStockRegime.VOLATILE_RANGE, AStockRegime.VOLATILE_UP,
        score_threshold=15, confirm_days=2, cooldown_days=5,
        position_adjustment="gradual", risk_level="low"
    ),
    (AStockRegime.VOLATILE_RANGE, AStockRegime.VOLATILE_DOWN): SwitchCondition(
        AStockRegime.VOLATILE_RANGE, AStockRegime.VOLATILE_DOWN,
        score_threshold=-15, confirm_days=2, cooldown_days=5,
        position_adjustment="gradual", risk_level="low"
    ),
    (AStockRegime.VOLATILE_UP, AStockRegime.BULL_LATE): SwitchCondition(
        AStockRegime.VOLATILE_UP, AStockRegime.BULL_LATE,
        score_threshold=35, confirm_days=3, cooldown_days=5,
        position_adjustment="gradual", risk_level="low"
    ),
    (AStockRegime.VOLATILE_DOWN, AStockRegime.BEAR_GRINDING): SwitchCondition(
        AStockRegime.VOLATILE_DOWN, AStockRegime.BEAR_GRINDING,
        score_threshold=-35, confirm_days=3, cooldown_days=5,
        position_adjustment="gradual", risk_level="medium"
    ),
}


# ============== 仓位调整策略 ==============

class PositionAdjustmentStrategy:
    """仓位调整策略
    
    三种模式：
    1. immediate: 立即调整到目标仓位
    2. gradual: 分3-5天逐步调整
    3. none: 不主动调整，等待自然换仓
    """
    
    @staticmethod
    def calculate_target_position(current_regime: AStockRegime, 
                                  new_regime: AStockRegime,
                                  current_position: float,
                                  adjustment_type: str,
                                  days_since_switch: int = 0) -> float:
        """计算目标仓位"""
        target = ASTOCK_REGIME_STRATEGY[new_regime]['position']
        
        if adjustment_type == "immediate":
            return target
        elif adjustment_type == "gradual":
            # 5天内逐步调整
            progress = min(days_since_switch / 5, 1.0)
            return current_position + (target - current_position) * progress
        else:  # none
            return current_position
    
    @staticmethod
    def should_force_sell(current_regime: AStockRegime, 
                          new_regime: AStockRegime) -> bool:
        """是否应该强制卖出"""
        # 进入熊市恐慌期必须强制清仓
        if new_regime == AStockRegime.BEAR_PANIC:
            return True
        
        # 从牛市进入熊市也要减仓
        bull_regimes = {AStockRegime.BULL_EARLY, AStockRegime.BULL_MID, AStockRegime.BULL_LATE}
        bear_regimes = {AStockRegime.BEAR_PANIC, AStockRegime.BEAR_GRINDING}
        
        if current_regime in bull_regimes and new_regime in bear_regimes:
            return True
        
        return False


# ============== 风险控制规则 ==============

@dataclass
class RiskControlRule:
    """风险控制规则"""
    name: str
    condition: str
    action: str
    priority: int  # 1最高


RISK_CONTROL_RULES = [
    RiskControlRule(
        name="熊市恐慌清仓",
        condition="regime == BEAR_PANIC",
        action="立即清空所有仓位",
        priority=1
    ),
    RiskControlRule(
        name="单日大跌止损",
        condition="单日跌幅 > 5%",
        action="减仓50%",
        priority=2
    ),
    RiskControlRule(
        name="连续亏损保护",
        condition="连续3笔交易亏损",
        action="暂停交易3天",
        priority=3
    ),
    RiskControlRule(
        name="最大回撤保护",
        condition="当前回撤 > 15%",
        action="减仓至20%",
        priority=2
    ),
    RiskControlRule(
        name="单股止损",
        condition="单股亏损 > 止损阈值",
        action="立即平仓该股",
        priority=4
    ),
    RiskControlRule(
        name="环境恶化减仓",
        condition="环境评分下降 > 30分",
        action="减仓30%",
        priority=3
    ),
]


# ============== 策略过渡逻辑 ==============

class StrategyTransitionManager:
    """策略过渡管理器
    
    管理从一个环境切换到另一个环境的过渡过程
    """
    
    def __init__(self):
        self.transition_in_progress = False
        self.transition_start_date = None
        self.transition_days = 0
        self.from_regime = None
        self.to_regime = None
        
    def start_transition(self, from_regime: AStockRegime, 
                         to_regime: AStockRegime,
                         current_date: str):
        """开始过渡"""
        self.transition_in_progress = True
        self.transition_start_date = current_date
        self.transition_days = 0
        self.from_regime = from_regime
        self.to_regime = to_regime
        
    def update_transition(self) -> bool:
        """更新过渡状态，返回是否完成"""
        if not self.transition_in_progress:
            return True
            
        self.transition_days += 1
        
        # 获取切换条件
        key = (self.from_regime, self.to_regime)
        condition = SWITCH_CONDITIONS.get(key)
        
        if condition:
            transition_duration = 5 if condition.position_adjustment == "gradual" else 1
            if self.transition_days >= transition_duration:
                self.transition_in_progress = False
                return True
        else:
            # 默认3天过渡
            if self.transition_days >= 3:
                self.transition_in_progress = False
                return True
                
        return False
    
    def get_blended_params(self) -> Dict:
        """获取混合参数（过渡期间使用）"""
        if not self.transition_in_progress:
            return ASTOCK_REGIME_STRATEGY.get(self.to_regime, {})
            
        from_params = ASTOCK_REGIME_STRATEGY.get(self.from_regime, {})
        to_params = ASTOCK_REGIME_STRATEGY.get(self.to_regime, {})
        
        # 线性混合
        progress = min(self.transition_days / 5, 1.0)
        
        blended = {}
        for key in ['position', 'stop_loss', 'take_profit']:
            if key in from_params and key in to_params:
                blended[key] = from_params[key] + (to_params[key] - from_params[key]) * progress
                
        # 其他参数使用目标环境
        for key in to_params:
            if key not in blended:
                blended[key] = to_params[key]
                
        return blended


# ============== 环境切换决策器 ==============

class RegimeSwitchDecider:
    """环境切换决策器
    
    综合考虑：
    1. 评分变化
    2. 切换条件
    3. 冷却期
    4. 确认天数
    5. 风险控制
    """
    
    def __init__(self):
        self.current_regime = AStockRegime.VOLATILE_RANGE
        self.regime_days = 0
        self.pending_regime = None
        self.pending_count = 0
        self.last_switch_date = None
        self.score_history = []
        
    def should_switch(self, score: float, current_date: str) -> Tuple[bool, Optional[AStockRegime]]:
        """判断是否应该切换环境"""
        self.score_history.append(score)
        
        # 计算得分对应的环境
        detected = self._score_to_regime(score)
        
        # 如果与当前环境相同，重置pending
        if detected == self.current_regime:
            self.pending_regime = None
            self.pending_count = 0
            self.regime_days += 1
            return False, None
        
        # 获取切换条件
        key = (self.current_regime, detected)
        condition = SWITCH_CONDITIONS.get(key)
        
        if condition is None:
            # 使用默认条件
            cooldown = 5
            confirm = 2
        else:
            cooldown = condition.cooldown_days
            confirm = condition.confirm_days
        
        # 检查冷却期
        if self.regime_days < cooldown:
            self.regime_days += 1
            return False, None
        
        # 紧急情况（熊市恐慌）跳过确认
        if detected == AStockRegime.BEAR_PANIC and score < -60:
            self._do_switch(detected, current_date)
            return True, detected
        
        # 确认机制
        if detected == self.pending_regime:
            self.pending_count += 1
            if self.pending_count >= confirm:
                self._do_switch(detected, current_date)
                return True, detected
        else:
            self.pending_regime = detected
            self.pending_count = 1
        
        self.regime_days += 1
        return False, None
    
    def _do_switch(self, new_regime: AStockRegime, current_date: str):
        """执行切换"""
        self.current_regime = new_regime
        self.regime_days = 0
        self.pending_regime = None
        self.pending_count = 0
        self.last_switch_date = current_date
    
    def _score_to_regime(self, score: float) -> AStockRegime:
        """将分数转换为环境"""
        if score > 50:
            return AStockRegime.BULL_EARLY
        elif score > 35:
            return AStockRegime.BULL_MID
        elif score > 25:
            return AStockRegime.BULL_LATE
        elif score < -50:
            return AStockRegime.BEAR_PANIC
        elif score < -35:
            return AStockRegime.BEAR_GRINDING
        elif score > 10:
            return AStockRegime.VOLATILE_UP
        elif score < -10:
            return AStockRegime.VOLATILE_DOWN
        else:
            return AStockRegime.VOLATILE_RANGE


# ============== 导出 ==============

__all__ = [
    'SwitchCondition',
    'SWITCH_CONDITIONS',
    'PositionAdjustmentStrategy',
    'RiskControlRule',
    'RISK_CONTROL_RULES',
    'StrategyTransitionManager',
    'RegimeSwitchDecider'
]







































