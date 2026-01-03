#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MarketStateDefinitions - 市场状态量化定义
==========================================

本模块定义了14种市场状态的量化标准，用于：
1. 统一市场状态判断逻辑
2. 历史回测验证
3. 策略仓位指导

市场状态体系：
- 牛市系列(5种): 牛市确认(共振)、牛市确认、牛市震荡、牛市短期调整、牛市中期调整
- 熊市系列(5种): 熊市确认(共振)、熊市确认、熊市反弹、熊市技术反弹、熊市筑底
- 震荡系列(4种): 突破在即、破位风险、复苏初期、见顶回落

作者: TRQuant Team
日期: 2026-01-02
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ==================== 周期定义 ====================

class TrendPeriod(Enum):
    """趋势周期"""
    SHORT = "short"    # 短期: 1-8周, 5-40日
    MEDIUM = "medium"  # 中期: 9-24周, 45-120日
    LONG = "long"      # 长期: 25-48周, 125-240日


@dataclass
class PeriodConfig:
    """周期配置"""
    name: str
    min_days: int
    max_days: int
    default_days: int
    weight: float
    key_indicators: List[str]


PERIOD_CONFIGS: Dict[TrendPeriod, PeriodConfig] = {
    TrendPeriod.SHORT: PeriodConfig(
        name="短期",
        min_days=5,
        max_days=40,
        default_days=20,
        weight=0.20,
        key_indicators=["MA5", "MA10", "RSI14", "KDJ", "成交量变化"]
    ),
    TrendPeriod.MEDIUM: PeriodConfig(
        name="中期",
        min_days=45,
        max_days=120,
        default_days=60,
        weight=0.30,
        key_indicators=["MA20", "MA60", "MACD", "布林带", "ADX"]
    ),
    TrendPeriod.LONG: PeriodConfig(
        name="长期",
        min_days=125,
        max_days=240,
        default_days=120,
        weight=0.50,
        key_indicators=["MA120", "MA250", "月线趋势", "年线位置", "长期均线排列"]
    ),
}


# ==================== 市场状态枚举 ====================

class MarketState(Enum):
    """14种市场状态"""
    # 牛市系列 (5种)
    BULL_CONFIRMED_RESONANCE = "牛市确认(共振)"
    BULL_CONFIRMED = "牛市确认"
    BULL_VOLATILE = "牛市震荡"
    BULL_SHORT_CORRECTION = "牛市短期调整"
    BULL_MEDIUM_CORRECTION = "牛市中期调整"
    
    # 熊市系列 (5种)
    BEAR_CONFIRMED_RESONANCE = "熊市确认(共振)"
    BEAR_CONFIRMED = "熊市确认"
    BEAR_REBOUND = "熊市反弹"
    BEAR_TECHNICAL_REBOUND = "熊市技术反弹"
    BEAR_BOTTOMING = "熊市筑底"
    
    # 震荡系列 (4种)
    BREAKOUT_IMMINENT = "突破在即"
    BREAKDOWN_RISK = "破位风险"
    RECOVERY_EARLY = "复苏初期"
    TOPPING_OUT = "见顶回落"


class StateCategory(Enum):
    """状态类别"""
    BULL = "牛市"
    BEAR = "熊市"
    VOLATILE = "震荡"


# 状态类别映射
STATE_CATEGORIES: Dict[MarketState, StateCategory] = {
    MarketState.BULL_CONFIRMED_RESONANCE: StateCategory.BULL,
    MarketState.BULL_CONFIRMED: StateCategory.BULL,
    MarketState.BULL_VOLATILE: StateCategory.BULL,
    MarketState.BULL_SHORT_CORRECTION: StateCategory.BULL,
    MarketState.BULL_MEDIUM_CORRECTION: StateCategory.BULL,
    MarketState.BEAR_CONFIRMED_RESONANCE: StateCategory.BEAR,
    MarketState.BEAR_CONFIRMED: StateCategory.BEAR,
    MarketState.BEAR_REBOUND: StateCategory.BEAR,
    MarketState.BEAR_TECHNICAL_REBOUND: StateCategory.BEAR,
    MarketState.BEAR_BOTTOMING: StateCategory.BEAR,
    MarketState.BREAKOUT_IMMINENT: StateCategory.VOLATILE,
    MarketState.BREAKDOWN_RISK: StateCategory.VOLATILE,
    MarketState.RECOVERY_EARLY: StateCategory.VOLATILE,
    MarketState.TOPPING_OUT: StateCategory.VOLATILE,
}


# ==================== 状态阈值定义 ====================

@dataclass
class ScoreRange:
    """得分范围"""
    min_val: Optional[float] = None  # None表示不限制
    max_val: Optional[float] = None  # None表示不限制
    
    def contains(self, score: float) -> bool:
        """检查得分是否在范围内"""
        if self.min_val is not None and score < self.min_val:
            return False
        if self.max_val is not None and score > self.max_val:
            return False
        return True
    
    def __repr__(self) -> str:
        if self.min_val is None and self.max_val is None:
            return "任意"
        elif self.min_val is None:
            return f"<{self.max_val}"
        elif self.max_val is None:
            return f">{self.min_val}"
        else:
            return f"{self.min_val}~{self.max_val}"


@dataclass
class StateThreshold:
    """市场状态阈值"""
    state: MarketState
    long_score: ScoreRange
    medium_score: ScoreRange
    short_score: ScoreRange
    position_min: float  # 建议最低仓位
    position_max: float  # 建议最高仓位
    description: str = ""
    
    def match(self, long: float, medium: float, short: float) -> bool:
        """检查得分是否匹配该状态"""
        return (self.long_score.contains(long) and 
                self.medium_score.contains(medium) and 
                self.short_score.contains(short))


# 14种市场状态的量化定义
STATE_THRESHOLDS: List[StateThreshold] = [
    # 牛市系列 (优先级从高到低)
    StateThreshold(
        state=MarketState.BULL_CONFIRMED_RESONANCE,
        long_score=ScoreRange(min_val=30),
        medium_score=ScoreRange(min_val=20),
        short_score=ScoreRange(min_val=10),
        position_min=0.80, position_max=1.00,
        description="全周期共振看多，强势上涨格局"
    ),
    StateThreshold(
        state=MarketState.BULL_CONFIRMED,
        long_score=ScoreRange(min_val=30),
        medium_score=ScoreRange(min_val=20),
        short_score=ScoreRange(),  # 任意
        position_min=0.70, position_max=0.90,
        description="长中期看多，短期波动不改趋势"
    ),
    StateThreshold(
        state=MarketState.BULL_SHORT_CORRECTION,
        long_score=ScoreRange(min_val=30),
        medium_score=ScoreRange(),  # 任意
        short_score=ScoreRange(max_val=-20),
        position_min=0.40, position_max=0.60,
        description="长期牛市中的短期调整，可逢低布局"
    ),
    StateThreshold(
        state=MarketState.BULL_MEDIUM_CORRECTION,
        long_score=ScoreRange(min_val=30),
        medium_score=ScoreRange(max_val=0),
        short_score=ScoreRange(),  # 任意
        position_min=0.30, position_max=0.50,
        description="长期牛市中的中期调整，谨慎观望"
    ),
    StateThreshold(
        state=MarketState.BULL_VOLATILE,
        long_score=ScoreRange(min_val=30),
        medium_score=ScoreRange(min_val=0, max_val=20),
        short_score=ScoreRange(),  # 任意
        position_min=0.50, position_max=0.70,
        description="牛市震荡整理阶段"
    ),
    
    # 熊市系列 (优先级从高到低)
    StateThreshold(
        state=MarketState.BEAR_CONFIRMED_RESONANCE,
        long_score=ScoreRange(max_val=-30),
        medium_score=ScoreRange(max_val=-20),
        short_score=ScoreRange(max_val=-10),
        position_min=0.00, position_max=0.10,
        description="全周期共振看空，强势下跌格局"
    ),
    StateThreshold(
        state=MarketState.BEAR_CONFIRMED,
        long_score=ScoreRange(max_val=-30),
        medium_score=ScoreRange(max_val=-20),
        short_score=ScoreRange(),  # 任意
        position_min=0.00, position_max=0.20,
        description="长中期看空，回避风险"
    ),
    StateThreshold(
        state=MarketState.BEAR_TECHNICAL_REBOUND,
        long_score=ScoreRange(max_val=-30),
        medium_score=ScoreRange(),  # 任意
        short_score=ScoreRange(min_val=20),
        position_min=0.20, position_max=0.40,
        description="熊市中的技术反弹，可短线参与"
    ),
    StateThreshold(
        state=MarketState.BEAR_BOTTOMING,
        long_score=ScoreRange(max_val=-30),
        medium_score=ScoreRange(min_val=0),
        short_score=ScoreRange(),  # 任意
        position_min=0.20, position_max=0.40,
        description="熊市筑底阶段，可能出现转机"
    ),
    StateThreshold(
        state=MarketState.BEAR_REBOUND,
        long_score=ScoreRange(max_val=-30),
        medium_score=ScoreRange(min_val=-20, max_val=0),
        short_score=ScoreRange(),  # 任意
        position_min=0.10, position_max=0.30,
        description="熊市反弹，持续性存疑"
    ),
    
    # 震荡系列 (优先级从高到低)
    StateThreshold(
        state=MarketState.BREAKOUT_IMMINENT,
        long_score=ScoreRange(min_val=-30, max_val=30),
        medium_score=ScoreRange(min_val=10),
        short_score=ScoreRange(min_val=10),
        position_min=0.50, position_max=0.70,
        description="震荡区间上沿，突破在即"
    ),
    StateThreshold(
        state=MarketState.BREAKDOWN_RISK,
        long_score=ScoreRange(min_val=-30, max_val=30),
        medium_score=ScoreRange(max_val=-10),
        short_score=ScoreRange(max_val=-10),
        position_min=0.10, position_max=0.30,
        description="震荡区间下沿，破位风险"
    ),
    StateThreshold(
        state=MarketState.RECOVERY_EARLY,
        long_score=ScoreRange(min_val=-30, max_val=30),
        medium_score=ScoreRange(min_val=0),
        short_score=ScoreRange(min_val=20),
        position_min=0.40, position_max=0.60,
        description="复苏初期，短期走强"
    ),
    StateThreshold(
        state=MarketState.TOPPING_OUT,
        long_score=ScoreRange(min_val=-30, max_val=30),
        medium_score=ScoreRange(max_val=0),
        short_score=ScoreRange(max_val=-20),
        position_min=0.20, position_max=0.40,
        description="见顶回落迹象，减仓观望"
    ),
]


# ==================== A股特色指标阈值 ====================

class AStockSignalLevel(Enum):
    """A股指标信号级别"""
    STRONG_BULLISH = "强看多"
    BULLISH = "看多"
    NEUTRAL = "中性"
    BEARISH = "看空"
    STRONG_BEARISH = "强看空"


@dataclass
class AStockIndicatorThreshold:
    """A股指标阈值"""
    strong_bullish: Tuple[float, float]  # (min, max)
    bullish: Tuple[float, float]
    neutral: Tuple[float, float]
    bearish: Tuple[float, float]
    strong_bearish: Tuple[float, float]
    
    def get_level(self, value: float) -> AStockSignalLevel:
        """获取信号级别"""
        if self.strong_bullish[0] <= value <= self.strong_bullish[1]:
            return AStockSignalLevel.STRONG_BULLISH
        elif self.bullish[0] <= value <= self.bullish[1]:
            return AStockSignalLevel.BULLISH
        elif self.neutral[0] <= value <= self.neutral[1]:
            return AStockSignalLevel.NEUTRAL
        elif self.bearish[0] <= value <= self.bearish[1]:
            return AStockSignalLevel.BEARISH
        else:
            return AStockSignalLevel.STRONG_BEARISH
    
    def get_score(self, value: float) -> float:
        """获取标准化得分 (-100 ~ 100)"""
        level = self.get_level(value)
        score_map = {
            AStockSignalLevel.STRONG_BULLISH: 80,
            AStockSignalLevel.BULLISH: 40,
            AStockSignalLevel.NEUTRAL: 0,
            AStockSignalLevel.BEARISH: -40,
            AStockSignalLevel.STRONG_BEARISH: -80,
        }
        return score_map[level]


# A股特色指标阈值定义
ASTOCK_THRESHOLDS = {
    "north_fund_5d": AStockIndicatorThreshold(
        strong_bullish=(100, float('inf')),
        bullish=(50, 100),
        neutral=(-50, 50),
        bearish=(-100, -50),
        strong_bearish=(float('-inf'), -100)
    ),
    "margin_change_rate": AStockIndicatorThreshold(
        strong_bullish=(2, float('inf')),
        bullish=(1, 2),
        neutral=(-1, 1),
        bearish=(-2, -1),
        strong_bearish=(float('-inf'), -2)
    ),
    "limit_up_down_ratio": AStockIndicatorThreshold(
        strong_bullish=(3, float('inf')),
        bullish=(2, 3),
        neutral=(0.5, 2),
        bearish=(0.3, 0.5),
        strong_bearish=(0, 0.3)
    ),
    "up_down_ratio": AStockIndicatorThreshold(
        strong_bullish=(2, float('inf')),
        bullish=(1.5, 2),
        neutral=(0.7, 1.5),
        bearish=(0.5, 0.7),
        strong_bearish=(0, 0.5)
    ),
}


# ==================== 状态判断函数 ====================

def determine_market_state(
    long_score: float, 
    medium_score: float, 
    short_score: float
) -> MarketState:
    """
    根据短中长周期得分判断市场状态
    
    Args:
        long_score: 长期得分 (-100 ~ 100)
        medium_score: 中期得分 (-100 ~ 100)
        short_score: 短期得分 (-100 ~ 100)
        
    Returns:
        MarketState: 市场状态
    """
    # 按优先级遍历阈值定义
    for threshold in STATE_THRESHOLDS:
        if threshold.match(long_score, medium_score, short_score):
            return threshold.state
    
    # 默认返回震荡状态
    logger.warning(f"无法匹配市场状态: L={long_score:.1f}, M={medium_score:.1f}, S={short_score:.1f}")
    return MarketState.RECOVERY_EARLY  # 默认复苏初期


def get_state_threshold(state: MarketState) -> Optional[StateThreshold]:
    """获取状态的阈值定义"""
    for threshold in STATE_THRESHOLDS:
        if threshold.state == state:
            return threshold
    return None


def get_position_advice(state: MarketState) -> Tuple[float, float]:
    """获取仓位建议"""
    threshold = get_state_threshold(state)
    if threshold:
        return (threshold.position_min, threshold.position_max)
    return (0.3, 0.5)  # 默认中性仓位


def get_state_category(state: MarketState) -> StateCategory:
    """获取状态类别"""
    return STATE_CATEGORIES.get(state, StateCategory.VOLATILE)


# ==================== 验证标准 ====================

@dataclass
class ValidationCriteria:
    """回测验证标准"""
    # 短期验证 (5日)
    short_holding_days: int = 5
    short_bullish_threshold: float = 0.0  # 涨幅>0%算正确
    short_bearish_threshold: float = 0.0  # 跌幅>0%算正确
    
    # 中期验证 (20日)
    medium_holding_days: int = 20
    medium_bullish_threshold: float = 0.0
    medium_bearish_threshold: float = 0.0
    
    # 长期验证 (60日)
    long_holding_days: int = 60
    long_bullish_threshold: float = 0.0
    long_bearish_threshold: float = 0.0
    
    # 市场状态验证 (60日)
    state_holding_days: int = 60
    bull_state_threshold: float = 5.0   # 牛市系列: 后续涨幅>5%
    bear_state_threshold: float = -5.0  # 熊市系列: 后续跌幅>5%
    volatile_range: float = 5.0         # 震荡系列: 波动<5%


def validate_signal_accuracy(
    signal_type: str,  # "bullish", "bearish", "neutral"
    actual_return: float,
    criteria: ValidationCriteria,
    period: str = "short"  # "short", "medium", "long"
) -> bool:
    """
    验证信号准确性
    
    Args:
        signal_type: 信号类型
        actual_return: 实际收益率 (%)
        criteria: 验证标准
        period: 验证周期
        
    Returns:
        bool: 是否准确
    """
    if period == "short":
        bullish_threshold = criteria.short_bullish_threshold
        bearish_threshold = criteria.short_bearish_threshold
    elif period == "medium":
        bullish_threshold = criteria.medium_bullish_threshold
        bearish_threshold = criteria.medium_bearish_threshold
    else:  # long
        bullish_threshold = criteria.long_bullish_threshold
        bearish_threshold = criteria.long_bearish_threshold
    
    if signal_type == "bullish":
        return actual_return > bullish_threshold
    elif signal_type == "bearish":
        return actual_return < bearish_threshold
    else:  # neutral
        return abs(actual_return) < 2.0  # 中性信号波动<2%算正确


def validate_state_accuracy(
    state: MarketState,
    actual_return_60d: float,
    criteria: ValidationCriteria
) -> bool:
    """
    验证市场状态准确性
    
    Args:
        state: 预测的市场状态
        actual_return_60d: 60日实际收益率 (%)
        criteria: 验证标准
        
    Returns:
        bool: 是否准确
    """
    category = get_state_category(state)
    
    if category == StateCategory.BULL:
        return actual_return_60d > criteria.bull_state_threshold
    elif category == StateCategory.BEAR:
        return actual_return_60d < criteria.bear_state_threshold
    else:  # VOLATILE
        return abs(actual_return_60d) < criteria.volatile_range


# ==================== 辅助函数 ====================

def get_all_states() -> List[MarketState]:
    """获取所有市场状态"""
    return list(MarketState)


def get_bull_states() -> List[MarketState]:
    """获取所有牛市状态"""
    return [s for s, c in STATE_CATEGORIES.items() if c == StateCategory.BULL]


def get_bear_states() -> List[MarketState]:
    """获取所有熊市状态"""
    return [s for s, c in STATE_CATEGORIES.items() if c == StateCategory.BEAR]


def get_volatile_states() -> List[MarketState]:
    """获取所有震荡状态"""
    return [s for s, c in STATE_CATEGORIES.items() if c == StateCategory.VOLATILE]


def state_to_signal_type(state: MarketState) -> str:
    """将市场状态转换为信号类型"""
    category = get_state_category(state)
    if category == StateCategory.BULL:
        return "bullish"
    elif category == StateCategory.BEAR:
        return "bearish"
    else:
        return "neutral"


def print_state_definitions():
    """打印所有市场状态定义"""
    print("\n" + "=" * 80)
    print("市场状态量化定义")
    print("=" * 80)
    
    for threshold in STATE_THRESHOLDS:
        print(f"\n{threshold.state.value}")
        print(f"  长期: {threshold.long_score}")
        print(f"  中期: {threshold.medium_score}")
        print(f"  短期: {threshold.short_score}")
        print(f"  仓位: {threshold.position_min*100:.0f}%-{threshold.position_max*100:.0f}%")
        print(f"  说明: {threshold.description}")


if __name__ == "__main__":
    # 测试
    print_state_definitions()
    
    # 测试状态判断
    print("\n" + "=" * 80)
    print("状态判断测试")
    print("=" * 80)
    
    test_cases = [
        (50, 30, 20, "全周期看多"),
        (40, 25, -30, "牛市短期调整"),
        (-40, -30, -20, "全周期看空"),
        (-35, -5, 25, "熊市技术反弹"),
        (10, 15, 15, "震荡突破"),
        (0, -15, -15, "震荡破位"),
    ]
    
    for long_s, med_s, short_s, desc in test_cases:
        state = determine_market_state(long_s, med_s, short_s)
        pos = get_position_advice(state)
        print(f"\n{desc}: L={long_s}, M={med_s}, S={short_s}")
        print(f"  -> {state.value}, 仓位: {pos[0]*100:.0f}%-{pos[1]*100:.0f}%")

