#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Professional Technical Indicators Knowledge Base - 专业技术指标知识库
===================================================================

基于网络研究构建的专业技术指标知识库，包含：
1. MACD专业用法（金叉死叉、零轴、背离）
2. RSI专业用法（超买超卖、背离、钝化）
3. 布林带策略（收口放口、突破反转）
4. KDJ指标（超买超卖、金叉死叉）
5. 量价关系分析
6. 均线系统分析

数据来源：网络搜索、学术研究、量化实践
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np
import pandas as pd


# ============== 信号类型 ==============

class SignalType(Enum):
    STRONG_BUY = "STRONG_BUY"       # 强烈买入
    BUY = "BUY"                     # 买入
    WEAK_BUY = "WEAK_BUY"           # 弱买入
    HOLD = "HOLD"                   # 持有观望
    WEAK_SELL = "WEAK_SELL"         # 弱卖出
    SELL = "SELL"                   # 卖出
    STRONG_SELL = "STRONG_SELL"     # 强烈卖出


@dataclass
class IndicatorSignal:
    """指标信号"""
    indicator: str
    signal: SignalType
    confidence: float  # 0-1
    reason: str
    value: float = 0


# ============== MACD 专业知识 ==============

class MACDKnowledge:
    """MACD专业知识库
    
    MACD = DIF - DEA
    DIF = EMA(12) - EMA(26)
    DEA = EMA(DIF, 9)
    
    专业用法：
    1. 金叉死叉：DIF上穿/下穿DEA
    2. 零轴位置：DIF在零轴上方/下方
    3. 背离：价格与MACD的背离
    4. 柱状图变化：红柱缩短/绿柱缩短
    """
    
    @staticmethod
    def calculate(prices: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算MACD"""
        exp12 = prices.ewm(span=12, adjust=False).mean()
        exp26 = prices.ewm(span=26, adjust=False).mean()
        dif = exp12 - exp26
        dea = dif.ewm(span=9, adjust=False).mean()
        macd = (dif - dea) * 2  # 柱状图
        return dif, dea, macd
    
    @staticmethod
    def analyze(prices: pd.Series) -> IndicatorSignal:
        """MACD综合分析"""
        if len(prices) < 35:
            return IndicatorSignal("MACD", SignalType.HOLD, 0.3, "数据不足")
        
        dif, dea, macd = MACDKnowledge.calculate(prices)
        
        current_dif = dif.iloc[-1]
        current_dea = dea.iloc[-1]
        current_macd = macd.iloc[-1]
        prev_macd = macd.iloc[-2]
        
        # 1. 金叉死叉判断
        is_golden_cross = dif.iloc[-2] < dea.iloc[-2] and current_dif > current_dea
        is_death_cross = dif.iloc[-2] > dea.iloc[-2] and current_dif < current_dea
        
        # 2. 零轴位置
        above_zero = current_dif > 0
        
        # 3. 柱状图变化
        macd_increasing = current_macd > prev_macd
        macd_positive = current_macd > 0
        
        # 4. 背离检测（简化版）
        price_higher = prices.iloc[-1] > prices.iloc[-10]
        dif_higher = current_dif > dif.iloc[-10]
        is_top_divergence = price_higher and not dif_higher  # 顶背离
        is_bottom_divergence = not price_higher and dif_higher  # 底背离
        
        # 综合判断
        if is_golden_cross and above_zero:
            return IndicatorSignal("MACD", SignalType.STRONG_BUY, 0.9, 
                                   "零轴上方金叉", current_dif)
        elif is_golden_cross:
            return IndicatorSignal("MACD", SignalType.BUY, 0.7,
                                   "零轴下方金叉", current_dif)
        elif is_death_cross and not above_zero:
            return IndicatorSignal("MACD", SignalType.STRONG_SELL, 0.9,
                                   "零轴下方死叉", current_dif)
        elif is_death_cross:
            return IndicatorSignal("MACD", SignalType.SELL, 0.7,
                                   "零轴上方死叉", current_dif)
        elif is_bottom_divergence:
            return IndicatorSignal("MACD", SignalType.BUY, 0.8,
                                   "底背离，反转信号", current_dif)
        elif is_top_divergence:
            return IndicatorSignal("MACD", SignalType.SELL, 0.8,
                                   "顶背离，见顶信号", current_dif)
        elif macd_positive and macd_increasing:
            return IndicatorSignal("MACD", SignalType.WEAK_BUY, 0.5,
                                   "红柱放大", current_dif)
        elif not macd_positive and not macd_increasing:
            return IndicatorSignal("MACD", SignalType.WEAK_SELL, 0.5,
                                   "绿柱放大", current_dif)
        else:
            return IndicatorSignal("MACD", SignalType.HOLD, 0.4, "观望", current_dif)


# ============== RSI 专业知识 ==============

class RSIKnowledge:
    """RSI专业知识库
    
    RSI = 100 - 100/(1+RS)
    RS = 平均上涨幅度 / 平均下跌幅度
    
    专业用法：
    1. 超买超卖：>80超买, <20超卖
    2. 背离：价格与RSI的背离
    3. 钝化：持续在高位或低位
    4. 中轴：50为多空分界线
    """
    
    @staticmethod
    def calculate(prices: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI"""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss.replace(0, 1e-10)
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    @staticmethod
    def analyze(prices: pd.Series) -> IndicatorSignal:
        """RSI综合分析"""
        if len(prices) < 20:
            return IndicatorSignal("RSI", SignalType.HOLD, 0.3, "数据不足")
        
        rsi = RSIKnowledge.calculate(prices)
        current_rsi = rsi.iloc[-1]
        
        # 1. 超买超卖
        is_overbought = current_rsi > 80
        is_oversold = current_rsi < 20
        is_highly_overbought = current_rsi > 90
        is_highly_oversold = current_rsi < 10
        
        # 2. RSI钝化检测
        recent_rsi = rsi.iloc[-5:]
        is_high_stagnation = all(r > 70 for r in recent_rsi)  # 高位钝化
        is_low_stagnation = all(r < 30 for r in recent_rsi)   # 低位钝化
        
        # 3. 背离检测
        price_higher = prices.iloc[-1] > prices.iloc[-10]
        rsi_higher = current_rsi > rsi.iloc[-10]
        is_top_divergence = price_higher and not rsi_higher
        is_bottom_divergence = not price_higher and rsi_higher
        
        # 4. 中轴判断
        above_50 = current_rsi > 50
        
        # 综合判断
        if is_highly_oversold:
            return IndicatorSignal("RSI", SignalType.STRONG_BUY, 0.85,
                                   f"极度超卖RSI={current_rsi:.1f}", current_rsi)
        elif is_oversold and is_bottom_divergence:
            return IndicatorSignal("RSI", SignalType.STRONG_BUY, 0.9,
                                   f"超卖+底背离RSI={current_rsi:.1f}", current_rsi)
        elif is_oversold:
            return IndicatorSignal("RSI", SignalType.BUY, 0.7,
                                   f"超卖RSI={current_rsi:.1f}", current_rsi)
        elif is_highly_overbought:
            return IndicatorSignal("RSI", SignalType.STRONG_SELL, 0.85,
                                   f"极度超买RSI={current_rsi:.1f}", current_rsi)
        elif is_overbought and is_top_divergence:
            return IndicatorSignal("RSI", SignalType.STRONG_SELL, 0.9,
                                   f"超买+顶背离RSI={current_rsi:.1f}", current_rsi)
        elif is_overbought:
            return IndicatorSignal("RSI", SignalType.SELL, 0.7,
                                   f"超买RSI={current_rsi:.1f}", current_rsi)
        elif is_high_stagnation:
            return IndicatorSignal("RSI", SignalType.WEAK_SELL, 0.6,
                                   "高位钝化，警惕回调", current_rsi)
        elif is_low_stagnation:
            return IndicatorSignal("RSI", SignalType.WEAK_BUY, 0.6,
                                   "低位钝化，可能反弹", current_rsi)
        elif above_50:
            return IndicatorSignal("RSI", SignalType.WEAK_BUY, 0.4,
                                   "多头区域", current_rsi)
        else:
            return IndicatorSignal("RSI", SignalType.WEAK_SELL, 0.4,
                                   "空头区域", current_rsi)


# ============== 布林带知识 ==============

class BollingerKnowledge:
    """布林带专业知识库
    
    中轨 = MA(20)
    上轨 = 中轨 + 2*STD(20)
    下轨 = 中轨 - 2*STD(20)
    
    专业用法：
    1. 收口放口：波动率变化
    2. 突破：价格突破上/下轨
    3. 回归：价格从轨道外回归
    4. 走势：沿轨道运行
    """
    
    @staticmethod
    def calculate(prices: pd.Series, period: int = 20, 
                  std_dev: float = 2) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
        """计算布林带"""
        middle = prices.rolling(period).mean()
        std = prices.rolling(period).std()
        upper = middle + std_dev * std
        lower = middle - std_dev * std
        width = (upper - lower) / middle  # 带宽
        return middle, upper, lower, width
    
    @staticmethod
    def analyze(prices: pd.Series) -> IndicatorSignal:
        """布林带综合分析"""
        if len(prices) < 25:
            return IndicatorSignal("BOLL", SignalType.HOLD, 0.3, "数据不足")
        
        middle, upper, lower, width = BollingerKnowledge.calculate(prices)
        current = prices.iloc[-1]
        prev = prices.iloc[-2]
        
        current_upper = upper.iloc[-1]
        current_lower = lower.iloc[-1]
        current_middle = middle.iloc[-1]
        current_width = width.iloc[-1]
        prev_width = width.iloc[-2]
        
        # 1. 位置判断
        above_upper = current > current_upper
        below_lower = current < current_lower
        near_upper = current > current_upper * 0.98
        near_lower = current < current_lower * 1.02
        
        # 2. 带宽变化
        width_expanding = current_width > prev_width * 1.05  # 放口
        width_contracting = current_width < prev_width * 0.95  # 收口
        narrow_band = current_width < 0.10  # 极窄带宽
        
        # 3. 突破判断
        breakout_up = current > current_upper and prev <= upper.iloc[-2]
        breakout_down = current < current_lower and prev >= lower.iloc[-2]
        
        # 综合判断
        if breakout_down and width_expanding:
            return IndicatorSignal("BOLL", SignalType.STRONG_SELL, 0.85,
                                   "放量下破下轨", current_width)
        elif below_lower and not width_expanding:
            return IndicatorSignal("BOLL", SignalType.BUY, 0.75,
                                   "触及下轨，可能反弹", current_width)
        elif breakout_up and width_expanding:
            return IndicatorSignal("BOLL", SignalType.STRONG_BUY, 0.85,
                                   "放量上破上轨", current_width)
        elif above_upper and not width_expanding:
            return IndicatorSignal("BOLL", SignalType.SELL, 0.75,
                                   "触及上轨，可能回调", current_width)
        elif narrow_band:
            return IndicatorSignal("BOLL", SignalType.HOLD, 0.6,
                                   "带宽收窄，等待方向选择", current_width)
        elif near_lower:
            return IndicatorSignal("BOLL", SignalType.WEAK_BUY, 0.5,
                                   "接近下轨", current_width)
        elif near_upper:
            return IndicatorSignal("BOLL", SignalType.WEAK_SELL, 0.5,
                                   "接近上轨", current_width)
        else:
            return IndicatorSignal("BOLL", SignalType.HOLD, 0.4,
                                   "中轨附近", current_width)


# ============== KDJ知识 ==============

class KDJKnowledge:
    """KDJ专业知识库
    
    RSV = (C-L9)/(H9-L9)*100
    K = SMA(RSV, 3)
    D = SMA(K, 3)
    J = 3*K - 2*D
    
    专业用法：
    1. 超买超卖：K/D>80超买, <20超卖
    2. 金叉死叉：K上穿/下穿D
    3. J值极端：J>100或J<0
    """
    
    @staticmethod
    def calculate(highs: pd.Series, lows: pd.Series, closes: pd.Series,
                  n: int = 9, m1: int = 3, m2: int = 3) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """计算KDJ"""
        low_n = lows.rolling(n).min()
        high_n = highs.rolling(n).max()
        rsv = (closes - low_n) / (high_n - low_n).replace(0, 1e-10) * 100
        
        k = rsv.ewm(span=m1, adjust=False).mean()
        d = k.ewm(span=m2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        return k, d, j
    
    @staticmethod
    def analyze(highs: pd.Series, lows: pd.Series, closes: pd.Series) -> IndicatorSignal:
        """KDJ综合分析"""
        if len(closes) < 15:
            return IndicatorSignal("KDJ", SignalType.HOLD, 0.3, "数据不足")
        
        k, d, j = KDJKnowledge.calculate(highs, lows, closes)
        
        current_k = k.iloc[-1]
        current_d = d.iloc[-1]
        current_j = j.iloc[-1]
        
        # 1. 金叉死叉
        is_golden_cross = k.iloc[-2] < d.iloc[-2] and current_k > current_d
        is_death_cross = k.iloc[-2] > d.iloc[-2] and current_k < current_d
        
        # 2. 超买超卖
        is_overbought = current_k > 80 and current_d > 80
        is_oversold = current_k < 20 and current_d < 20
        
        # 3. J值极端
        j_extreme_high = current_j > 100
        j_extreme_low = current_j < 0
        
        # 综合判断
        if is_golden_cross and is_oversold:
            return IndicatorSignal("KDJ", SignalType.STRONG_BUY, 0.9,
                                   f"低位金叉K={current_k:.1f}", current_k)
        elif is_golden_cross:
            return IndicatorSignal("KDJ", SignalType.BUY, 0.7,
                                   f"金叉K={current_k:.1f}", current_k)
        elif is_death_cross and is_overbought:
            return IndicatorSignal("KDJ", SignalType.STRONG_SELL, 0.9,
                                   f"高位死叉K={current_k:.1f}", current_k)
        elif is_death_cross:
            return IndicatorSignal("KDJ", SignalType.SELL, 0.7,
                                   f"死叉K={current_k:.1f}", current_k)
        elif j_extreme_low:
            return IndicatorSignal("KDJ", SignalType.BUY, 0.8,
                                   f"J值极低={current_j:.1f}", current_k)
        elif j_extreme_high:
            return IndicatorSignal("KDJ", SignalType.SELL, 0.8,
                                   f"J值极高={current_j:.1f}", current_k)
        elif is_oversold:
            return IndicatorSignal("KDJ", SignalType.WEAK_BUY, 0.6,
                                   "超卖区域", current_k)
        elif is_overbought:
            return IndicatorSignal("KDJ", SignalType.WEAK_SELL, 0.6,
                                   "超买区域", current_k)
        else:
            return IndicatorSignal("KDJ", SignalType.HOLD, 0.4,
                                   "中性区域", current_k)


# ============== 量价关系知识 ==============

class VolumeKnowledge:
    """量价关系专业知识库
    
    核心规则：
    1. 放量上涨：强势信号
    2. 缩量上涨：动力不足
    3. 放量下跌：恐慌信号
    4. 缩量下跌：抛压减轻
    5. 地量：可能见底
    6. 天量：可能见顶
    """
    
    @staticmethod
    def analyze(prices: pd.Series, volumes: pd.Series) -> IndicatorSignal:
        """量价关系分析"""
        if len(prices) < 20:
            return IndicatorSignal("VOL", SignalType.HOLD, 0.3, "数据不足")
        
        # 成交量指标
        vol_ma5 = volumes.rolling(5).mean().iloc[-1]
        vol_ma20 = volumes.rolling(20).mean().iloc[-1]
        vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
        
        current_vol = volumes.iloc[-1]
        avg_vol = volumes.rolling(20).mean().iloc[-1]
        vol_multiple = current_vol / avg_vol if avg_vol > 0 else 1
        
        # 价格变化
        price_change_1d = prices.iloc[-1] / prices.iloc[-2] - 1
        price_change_5d = prices.iloc[-1] / prices.iloc[-5] - 1 if len(prices) >= 5 else 0
        
        # 地量天量
        vol_percentile = (volumes.iloc[-1] / volumes.rolling(60).max().iloc[-1] 
                          if len(volumes) >= 60 else 0.5)
        is_low_volume = vol_percentile < 0.2
        is_high_volume = vol_percentile > 0.9
        
        # 综合判断
        if vol_multiple > 2 and price_change_1d > 0.03:
            return IndicatorSignal("VOL", SignalType.STRONG_BUY, 0.85,
                                   f"放量上涨，量比{vol_multiple:.1f}", vol_ratio)
        elif vol_multiple > 2 and price_change_1d < -0.03:
            return IndicatorSignal("VOL", SignalType.STRONG_SELL, 0.85,
                                   f"放量下跌，量比{vol_multiple:.1f}", vol_ratio)
        elif is_low_volume and price_change_5d < -0.05:
            return IndicatorSignal("VOL", SignalType.BUY, 0.7,
                                   "地量，可能见底", vol_ratio)
        elif is_high_volume and price_change_5d > 0.10:
            return IndicatorSignal("VOL", SignalType.SELL, 0.7,
                                   "天量，警惕见顶", vol_ratio)
        elif vol_ratio < 0.7 and price_change_1d > 0:
            return IndicatorSignal("VOL", SignalType.WEAK_SELL, 0.5,
                                   "缩量上涨，动力不足", vol_ratio)
        elif vol_ratio < 0.7 and price_change_1d < 0:
            return IndicatorSignal("VOL", SignalType.WEAK_BUY, 0.5,
                                   "缩量下跌，抛压减轻", vol_ratio)
        elif vol_ratio > 1.3 and price_change_1d > 0:
            return IndicatorSignal("VOL", SignalType.BUY, 0.6,
                                   "温和放量上涨", vol_ratio)
        else:
            return IndicatorSignal("VOL", SignalType.HOLD, 0.4,
                                   "量价正常", vol_ratio)


# ============== 综合技术分析 ==============

class ComprehensiveTechnicalAnalysis:
    """综合技术分析
    
    整合多个指标，生成综合信号
    """
    
    SIGNAL_WEIGHTS = {
        SignalType.STRONG_BUY: 2,
        SignalType.BUY: 1,
        SignalType.WEAK_BUY: 0.5,
        SignalType.HOLD: 0,
        SignalType.WEAK_SELL: -0.5,
        SignalType.SELL: -1,
        SignalType.STRONG_SELL: -2
    }
    
    @staticmethod
    def analyze_all(prices: pd.Series, volumes: pd.Series = None,
                    highs: pd.Series = None, lows: pd.Series = None) -> Dict:
        """综合分析所有指标"""
        if volumes is None:
            volumes = pd.Series([1] * len(prices))
        if highs is None:
            highs = prices
        if lows is None:
            lows = prices
            
        signals = {
            'MACD': MACDKnowledge.analyze(prices),
            'RSI': RSIKnowledge.analyze(prices),
            'BOLL': BollingerKnowledge.analyze(prices),
            'KDJ': KDJKnowledge.analyze(highs, lows, prices),
            'VOL': VolumeKnowledge.analyze(prices, volumes)
        }
        
        # 计算综合得分
        total_score = 0
        total_confidence = 0
        
        for name, signal in signals.items():
            weight = ComprehensiveTechnicalAnalysis.SIGNAL_WEIGHTS[signal.signal]
            total_score += weight * signal.confidence
            total_confidence += signal.confidence
        
        avg_score = total_score / len(signals) if signals else 0
        avg_confidence = total_confidence / len(signals) if signals else 0
        
        # 确定综合信号
        if avg_score > 1:
            overall_signal = SignalType.STRONG_BUY
        elif avg_score > 0.5:
            overall_signal = SignalType.BUY
        elif avg_score > 0.2:
            overall_signal = SignalType.WEAK_BUY
        elif avg_score > -0.2:
            overall_signal = SignalType.HOLD
        elif avg_score > -0.5:
            overall_signal = SignalType.WEAK_SELL
        elif avg_score > -1:
            overall_signal = SignalType.SELL
        else:
            overall_signal = SignalType.STRONG_SELL
        
        return {
            'signals': signals,
            'overall_signal': overall_signal,
            'score': avg_score,
            'confidence': avg_confidence
        }


# ============== 导出 ==============

__all__ = [
    'SignalType',
    'IndicatorSignal',
    'MACDKnowledge',
    'RSIKnowledge',
    'BollingerKnowledge',
    'KDJKnowledge',
    'VolumeKnowledge',
    'ComprehensiveTechnicalAnalysis'
]







































