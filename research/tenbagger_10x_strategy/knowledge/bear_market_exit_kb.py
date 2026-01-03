#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bear Market Early Exit Knowledge Base - 熊市早期退出知识库
==========================================================

基于历史研究和技术分析构建的熊市早期识别与退出机制：

1. 熊市早期信号识别
2. 动态止损机制（ATR止损、跟踪止损）
3. 市场广度指标
4. 分阶段退出策略
5. 资金保护规则

参考研究：
- 市场顶部信号研究
- 技术指标综合应用
- A股历史熊市特征
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import numpy as np
import pandas as pd


# ============== 熊市阶段定义 ==============

class BearPhase(Enum):
    """熊市阶段"""
    NORMAL = "正常市况"              # 市场正常，无熊市信号
    WARNING = "预警阶段"             # 出现早期警告信号
    DISTRIBUTION = "派发阶段"         # 主力派发，头部形成
    PANIC = "恐慌阶段"               # 急速下跌，恐慌抛售
    GRINDING = "磨底阶段"            # 缓慢下跌，底部震荡


# ============== 熊市早期预警信号 ==============

@dataclass
class BearWarningSignal:
    """熊市预警信号"""
    name: str
    description: str
    weight: float           # 权重 (0-1)
    threshold: Any          # 触发阈值
    action: str             # 建议动作
    severity: str           # 严重程度: low/medium/high/critical


BEAR_WARNING_SIGNALS = {
    # ============ 技术面信号 ============
    
    # 1. 均线死叉
    "ma_death_cross": BearWarningSignal(
        name="均线死叉",
        description="短期均线下穿长期均线，趋势转空",
        weight=0.15,
        threshold={"ma5_below_ma20": True, "ma20_below_ma60": True},
        action="减仓30%，设置跟踪止损",
        severity="medium"
    ),
    
    # 2. MACD顶背离
    "macd_divergence": BearWarningSignal(
        name="MACD顶背离",
        description="价格创新高但MACD未创新高",
        weight=0.20,
        threshold={"price_high": True, "macd_high": False},
        action="减仓50%，准备离场",
        severity="high"
    ),
    
    # 3. RSI超买后回落
    "rsi_overbought_drop": BearWarningSignal(
        name="RSI超买回落",
        description="RSI从超买区（>70）回落至50以下",
        weight=0.12,
        threshold={"rsi_from": 70, "rsi_to": 50},
        action="减仓20%",
        severity="medium"
    ),
    
    # 4. 布林带收窄后向下突破
    "bollinger_breakdown": BearWarningSignal(
        name="布林带下轨突破",
        description="价格跌破布林带下轨",
        weight=0.10,
        threshold={"price_below_lower_band": True},
        action="立即止损",
        severity="high"
    ),
    
    # ============ 量价信号 ============
    
    # 5. 放量滞涨
    "volume_price_divergence": BearWarningSignal(
        name="放量滞涨",
        description="成交量放大但价格上涨乏力或下跌",
        weight=0.18,
        threshold={"volume_ratio": 1.5, "price_change": 0.02},
        action="减仓40%，主力可能在出货",
        severity="high"
    ),
    
    # 6. 天量天价
    "climax_volume": BearWarningSignal(
        name="天量天价",
        description="成交量创阶段新高伴随价格见顶",
        weight=0.15,
        threshold={"volume_percentile": 95, "price_near_high": 0.98},
        action="减仓60%，可能是顶部",
        severity="critical"
    ),
    
    # ============ 市场广度信号 ============
    
    # 7. 涨跌比恶化
    "advance_decline_deterioration": BearWarningSignal(
        name="涨跌比恶化",
        description="上涨股票数量持续减少",
        weight=0.12,
        threshold={"ad_ratio": 0.4, "consecutive_days": 3},
        action="减仓30%，市场广度变差",
        severity="medium"
    ),
    
    # 8. 新低增加
    "new_lows_increase": BearWarningSignal(
        name="新低家数增加",
        description="创新低的股票数量超过创新高",
        weight=0.10,
        threshold={"new_low_ratio": 2.0},
        action="减仓25%",
        severity="medium"
    ),
    
    # ============ 情绪信号 ============
    
    # 9. 恐惧指标升高
    "fear_index_high": BearWarningSignal(
        name="恐惧指标升高",
        description="波动率指数（VIX等价物）快速上升",
        weight=0.08,
        threshold={"vix_percentile": 80, "vix_change_5d": 0.5},
        action="减仓20%，设置严格止损",
        severity="medium"
    ),
}


# ============== 动态止损机制 ==============

@dataclass
class DynamicStopLoss:
    """动态止损配置"""
    method: str             # 止损方法
    params: Dict            # 参数
    description: str        # 描述


DYNAMIC_STOP_LOSS_METHODS = {
    # 1. ATR止损（Chandelier Exit）
    "atr_stop": DynamicStopLoss(
        method="ATR止损",
        params={
            "atr_period": 14,
            "multiplier": 3.0,      # 3倍ATR
            "use_high_anchor": True  # 从最高点计算
        },
        description="从最高点减去3倍ATR作为止损位，随价格上涨自动抬升"
    ),
    
    # 2. 跟踪止损（Trailing Stop）
    "trailing_stop": DynamicStopLoss(
        method="跟踪止损",
        params={
            "trail_percent": 0.08,   # 8%回撤止损
            "min_profit_to_trail": 0.05  # 盈利5%后才启用
        },
        description="价格上涨时止损位跟随上移，回撤8%时触发"
    ),
    
    # 3. 波动率自适应止损
    "volatility_adaptive": DynamicStopLoss(
        method="波动率自适应",
        params={
            "vol_lookback": 20,
            "vol_multiplier": 2.0,
            "min_stop": 0.05,
            "max_stop": 0.15
        },
        description="根据近期波动率动态调整止损幅度，高波动放宽、低波动收紧"
    ),
    
    # 4. 支撑位止损
    "support_based": DynamicStopLoss(
        method="支撑位止损",
        params={
            "support_lookback": 20,
            "buffer_percent": 0.02   # 支撑位下方2%
        },
        description="以近期低点作为支撑位，跌破支撑位2%时止损"
    ),
    
    # 5. 时间止损
    "time_based": DynamicStopLoss(
        method="时间止损",
        params={
            "max_holding_days": 60,
            "min_return": 0.05       # 60天内未达5%收益则卖出
        },
        description="持仓超过60天且收益低于5%时止损，避免资金占用"
    ),
}


# ============== 分阶段退出策略 ==============

@dataclass
class ExitStrategy:
    """退出策略"""
    phase: BearPhase
    position_target: float      # 目标仓位
    exit_speed: str            # 退出速度: immediate/fast/gradual
    priority_sell: List[str]   # 优先卖出的股票类型
    stop_loss_adjustment: float # 止损调整幅度
    description: str


PHASE_EXIT_STRATEGIES = {
    BearPhase.NORMAL: ExitStrategy(
        phase=BearPhase.NORMAL,
        position_target=0.8,
        exit_speed="none",
        priority_sell=[],
        stop_loss_adjustment=1.0,
        description="正常持仓，使用标准止损"
    ),
    
    BearPhase.WARNING: ExitStrategy(
        phase=BearPhase.WARNING,
        position_target=0.5,
        exit_speed="gradual",
        priority_sell=["high_beta", "small_cap", "loss_positions"],
        stop_loss_adjustment=0.8,  # 收紧止损20%
        description="预警阶段：减仓至50%，优先卖出高风险品种，收紧止损"
    ),
    
    BearPhase.DISTRIBUTION: ExitStrategy(
        phase=BearPhase.DISTRIBUTION,
        position_target=0.2,
        exit_speed="fast",
        priority_sell=["all_except_profit", "weak_momentum"],
        stop_loss_adjustment=0.6,  # 收紧止损40%
        description="派发阶段：快速减仓至20%，只保留盈利仓位，严格止损"
    ),
    
    BearPhase.PANIC: ExitStrategy(
        phase=BearPhase.PANIC,
        position_target=0.0,
        exit_speed="immediate",
        priority_sell=["all"],
        stop_loss_adjustment=0.0,  # 不设止损，全部清仓
        description="恐慌阶段：立即清仓，保存实力"
    ),
    
    BearPhase.GRINDING: ExitStrategy(
        phase=BearPhase.GRINDING,
        position_target=0.1,
        exit_speed="gradual",
        priority_sell=["weak_fundamentals"],
        stop_loss_adjustment=0.5,
        description="磨底阶段：极小仓位试探，严格止损"
    ),
}


# ============== 熊市早期识别器 ==============

class BearMarketDetector:
    """熊市早期识别器
    
    综合多个信号判断是否进入熊市，并确定熊市阶段
    """
    
    def __init__(self):
        self.signal_history = []
        self.current_phase = BearPhase.NORMAL
        self.phase_days = 0
        self.warning_score = 0
        
    def calculate_warning_score(self, prices: pd.Series, volumes: pd.Series = None) -> Tuple[float, Dict]:
        """计算熊市预警分数 (0-100, 越高越危险)"""
        if len(prices) < 60:
            return 0, {}
            
        signals_triggered = {}
        total_weight = 0
        warning_score = 0
        
        current = prices.iloc[-1]
        
        # 1. 均线死叉检测
        ma5 = prices.rolling(5).mean().iloc[-1]
        ma20 = prices.rolling(20).mean().iloc[-1]
        ma60 = prices.rolling(60).mean().iloc[-1]
        
        ma5_below_ma20 = ma5 < ma20
        ma20_below_ma60 = ma20 < ma60
        
        if ma5_below_ma20 and ma20_below_ma60:
            signals_triggered["ma_death_cross"] = True
            warning_score += 0.15 * 100
            
        # 2. MACD顶背离检测
        exp12 = prices.ewm(span=12).mean()
        exp26 = prices.ewm(span=26).mean()
        macd = exp12 - exp26
        
        # 简化版背离检测：价格20日新高但MACD不是
        price_20d_high = prices.iloc[-1] >= prices.rolling(20).max().iloc[-1]
        macd_20d_high = macd.iloc[-1] >= macd.rolling(20).max().iloc[-1]
        
        if price_20d_high and not macd_20d_high:
            signals_triggered["macd_divergence"] = True
            warning_score += 0.20 * 100
            
        # 3. RSI超买后回落
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        rsi_current = rsi.iloc[-1]
        rsi_5d_ago = rsi.iloc[-5] if len(rsi) > 5 else 50
        
        if rsi_5d_ago > 70 and rsi_current < 50:
            signals_triggered["rsi_overbought_drop"] = True
            warning_score += 0.12 * 100
            
        # 4. 布林带下轨突破
        ma20_bb = prices.rolling(20).mean()
        std20 = prices.rolling(20).std()
        lower_band = ma20_bb - 2 * std20
        
        if current < lower_band.iloc[-1]:
            signals_triggered["bollinger_breakdown"] = True
            warning_score += 0.10 * 100
            
        # 5. 放量滞涨
        if volumes is not None:
            vol_ma5 = volumes.rolling(5).mean().iloc[-1]
            vol_ma20 = volumes.rolling(20).mean().iloc[-1]
            vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
            
            price_change_5d = prices.iloc[-1] / prices.iloc[-5] - 1 if len(prices) > 5 else 0
            
            if vol_ratio > 1.5 and price_change_5d < 0.02:
                signals_triggered["volume_price_divergence"] = True
                warning_score += 0.18 * 100
                
            # 6. 天量天价
            vol_percentile = (volumes.iloc[-1] > volumes.rolling(60).quantile(0.95).iloc[-1])
            price_near_high = current > prices.rolling(60).max().iloc[-1] * 0.98
            
            if vol_percentile and price_near_high:
                signals_triggered["climax_volume"] = True
                warning_score += 0.15 * 100
                
        # 7. 波动率升高
        vol_recent = prices.pct_change()[-10:].std() * np.sqrt(252)
        vol_history = prices.pct_change()[-60:].std() * np.sqrt(252)
        
        if vol_recent > vol_history * 1.5:
            signals_triggered["volatility_spike"] = True
            warning_score += 0.08 * 100
            
        return min(warning_score, 100), signals_triggered
    
    def detect_phase(self, prices: pd.Series, volumes: pd.Series = None) -> Tuple[BearPhase, float, Dict]:
        """检测熊市阶段
        
        Returns:
            (阶段, 预警分数, 触发的信号)
        """
        warning_score, signals = self.calculate_warning_score(prices, volumes)
        
        self.signal_history.append(warning_score)
        avg_score = np.mean(self.signal_history[-5:]) if len(self.signal_history) >= 5 else warning_score
        
        # 根据分数判断阶段
        old_phase = self.current_phase
        
        if avg_score >= 70:
            self.current_phase = BearPhase.PANIC
        elif avg_score >= 50:
            self.current_phase = BearPhase.DISTRIBUTION
        elif avg_score >= 30:
            self.current_phase = BearPhase.WARNING
        elif avg_score >= 15 and self.current_phase in [BearPhase.PANIC, BearPhase.DISTRIBUTION]:
            self.current_phase = BearPhase.GRINDING
        else:
            self.current_phase = BearPhase.NORMAL
            
        # 统计连续天数
        if self.current_phase == old_phase:
            self.phase_days += 1
        else:
            self.phase_days = 1
            
        return self.current_phase, warning_score, signals
    
    def get_exit_strategy(self) -> ExitStrategy:
        """获取当前阶段的退出策略"""
        return PHASE_EXIT_STRATEGIES.get(self.current_phase, PHASE_EXIT_STRATEGIES[BearPhase.NORMAL])


# ============== 动态止损计算器 ==============

class DynamicStopLossCalculator:
    """动态止损计算器"""
    
    @staticmethod
    def calculate_atr_stop(prices: pd.Series, highs: pd.Series = None, 
                           lows: pd.Series = None, period: int = 14, 
                           multiplier: float = 3.0) -> float:
        """计算ATR止损位（Chandelier Exit）"""
        if len(prices) < period + 1:
            return prices.iloc[-1] * 0.9  # 默认10%止损
            
        if highs is None:
            highs = prices
        if lows is None:
            lows = prices
            
        # 计算ATR
        tr = pd.concat([
            highs - lows,
            abs(highs - prices.shift(1)),
            abs(lows - prices.shift(1))
        ], axis=1).max(axis=1)
        
        atr = tr.rolling(period).mean().iloc[-1]
        
        # 从最高点减去ATR倍数
        highest = prices.rolling(period).max().iloc[-1]
        stop = highest - multiplier * atr
        
        return max(stop, prices.iloc[-1] * 0.85)  # 最多15%止损
    
    @staticmethod
    def calculate_trailing_stop(prices: pd.Series, entry_price: float,
                                trail_percent: float = 0.08,
                                min_profit_to_trail: float = 0.05) -> float:
        """计算跟踪止损位"""
        highest = prices.max()
        current = prices.iloc[-1]
        profit = (highest - entry_price) / entry_price
        
        if profit >= min_profit_to_trail:
            # 已盈利足够，启用跟踪止损
            stop = highest * (1 - trail_percent)
        else:
            # 尚未盈利或盈利不足，使用入场价止损
            stop = entry_price * (1 - trail_percent)
            
        return stop
    
    @staticmethod
    def calculate_volatility_adaptive_stop(prices: pd.Series, 
                                           vol_lookback: int = 20,
                                           vol_multiplier: float = 2.0,
                                           min_stop: float = 0.05,
                                           max_stop: float = 0.15) -> float:
        """计算波动率自适应止损位"""
        if len(prices) < vol_lookback:
            return prices.iloc[-1] * (1 - 0.10)  # 默认10%
            
        volatility = prices.pct_change().rolling(vol_lookback).std().iloc[-1] * np.sqrt(252)
        
        # 基于波动率计算止损幅度
        stop_percent = volatility * vol_multiplier
        stop_percent = np.clip(stop_percent, min_stop, max_stop)
        
        return prices.iloc[-1] * (1 - stop_percent)
    
    @staticmethod
    def calculate_support_stop(prices: pd.Series, 
                              support_lookback: int = 20,
                              buffer_percent: float = 0.02) -> float:
        """计算支撑位止损"""
        if len(prices) < support_lookback:
            return prices.iloc[-1] * 0.95
            
        support = prices.rolling(support_lookback).min().iloc[-1]
        stop = support * (1 - buffer_percent)
        
        return stop
    
    def get_best_stop(self, prices: pd.Series, entry_price: float,
                      highs: pd.Series = None, lows: pd.Series = None,
                      bear_phase: BearPhase = BearPhase.NORMAL) -> Tuple[float, str]:
        """获取最佳止损位
        
        根据熊市阶段选择合适的止损方法
        
        Returns:
            (止损价格, 使用的方法)
        """
        stops = {}
        
        # 计算各种止损
        stops['atr'] = self.calculate_atr_stop(prices, highs, lows)
        stops['trailing'] = self.calculate_trailing_stop(prices, entry_price)
        stops['volatility'] = self.calculate_volatility_adaptive_stop(prices)
        stops['support'] = self.calculate_support_stop(prices)
        
        # 根据熊市阶段选择止损策略
        if bear_phase == BearPhase.PANIC:
            # 恐慌阶段：使用最激进的止损（最高的止损价）
            best_method = max(stops, key=stops.get)
            return stops[best_method], best_method
            
        elif bear_phase == BearPhase.DISTRIBUTION:
            # 派发阶段：收紧止损
            stop = max(stops['trailing'], stops['volatility'])
            return stop, 'distribution_tight'
            
        elif bear_phase == BearPhase.WARNING:
            # 预警阶段：平衡止损
            stop = (stops['atr'] + stops['trailing']) / 2
            return stop, 'warning_balanced'
            
        else:
            # 正常/磨底：标准ATR止损
            return stops['atr'], 'atr'


# ============== 资金保护规则 ==============

@dataclass
class CapitalProtectionRule:
    """资金保护规则"""
    name: str
    trigger_condition: str
    action: str
    priority: int
    recovery_condition: str


CAPITAL_PROTECTION_RULES = [
    CapitalProtectionRule(
        name="最大回撤保护",
        trigger_condition="当前回撤 > 15%",
        action="强制减仓至20%，暂停新建仓",
        priority=1,
        recovery_condition="回撤恢复至10%以内"
    ),
    CapitalProtectionRule(
        name="连续亏损保护",
        trigger_condition="连续3笔交易亏损",
        action="暂停交易5个交易日",
        priority=2,
        recovery_condition="等待5个交易日后重新评估市场"
    ),
    CapitalProtectionRule(
        name="单日大跌保护",
        trigger_condition="投资组合单日跌幅 > 5%",
        action="立即减仓50%",
        priority=1,
        recovery_condition="波动率回归正常后逐步恢复"
    ),
    CapitalProtectionRule(
        name="年度亏损保护",
        trigger_condition="年度累计亏损 > 20%",
        action="清仓观望至年底",
        priority=1,
        recovery_condition="新年度重新开始"
    ),
    CapitalProtectionRule(
        name="熊市空仓保护",
        trigger_condition="进入熊市恐慌阶段",
        action="全部清仓，持有现金",
        priority=1,
        recovery_condition="熊市阶段确认结束，进入磨底或复苏"
    ),
]


# ============== 导出 ==============

__all__ = [
    'BearPhase',
    'BearWarningSignal',
    'BEAR_WARNING_SIGNALS',
    'DynamicStopLoss',
    'DYNAMIC_STOP_LOSS_METHODS',
    'ExitStrategy',
    'PHASE_EXIT_STRATEGIES',
    'BearMarketDetector',
    'DynamicStopLossCalculator',
    'CapitalProtectionRule',
    'CAPITAL_PROTECTION_RULES'
]







































