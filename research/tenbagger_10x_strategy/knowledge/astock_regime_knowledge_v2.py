#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A-Stock Market Regime Knowledge V2 - A股市场环境知识库V2
=======================================================

针对A股市场特色优化：
1. 政策市特征：政策驱动行情
2. 资金面指标：北向资金、融资余额
3. 板块轮动：行业轮动特征
4. 情绪指标：换手率、涨停板数量
5. 量价关系：成交量确认趋势

参考研究：
- K-Means + Bayesian Markov Switching (Li et al., 2025)
- Dynamic Stacking Ensemble Learning (Gao et al., 2025)
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


class AStockRegime(Enum):
    """A股市场环境（更细分）"""
    BULL_EARLY = "BULL_EARLY"           # 牛市初期（最佳介入）
    BULL_MID = "BULL_MID"               # 牛市中期（持股待涨）
    BULL_LATE = "BULL_LATE"             # 牛市末期（逐步减仓）
    BEAR_PANIC = "BEAR_PANIC"           # 熊市恐慌（空仓观望）
    BEAR_GRINDING = "BEAR_GRINDING"     # 熊市磨底（寻找机会）
    VOLATILE_UP = "VOLATILE_UP"         # 震荡向上（逢低吸纳）
    VOLATILE_DOWN = "VOLATILE_DOWN"     # 震荡向下（高抛低吸）
    VOLATILE_RANGE = "VOLATILE_RANGE"   # 区间震荡（网格策略）
    POLICY_DRIVEN = "POLICY_DRIVEN"     # 政策驱动（跟随政策）
    SECTOR_ROTATION = "SECTOR_ROTATION" # 板块轮动（追踪热点）


# ============== A股市场环境策略映射 ==============

ASTOCK_REGIME_STRATEGY = {
    AStockRegime.BULL_EARLY: {
        'position': 0.9,
        'strategy': 'aggressive_momentum',
        'stop_loss': 0.15,
        'take_profit': 0.80,
        'max_stocks': 5,
        'rebalance_freq': 10,
        'focus': ['growth', 'small_cap', 'tenbagger'],
        'description': '牛市初期：重仓进攻，追逐高弹性标的'
    },
    AStockRegime.BULL_MID: {
        'position': 0.5,  # 降低仓位，牛市中期风险增加
        'strategy': 'momentum_hold',
        'stop_loss': 0.10,  # 收紧止损
        'take_profit': 0.30,  # 合理止盈
        'max_stocks': 3,  # 减少持股
        'rebalance_freq': 10,
        'focus': ['momentum', 'sector_leader'],
        'description': '牛市中期：控制仓位，保住利润'
    },
    AStockRegime.BULL_LATE: {
        'position': 0.5,
        'strategy': 'profit_taking',
        'stop_loss': 0.08,
        'take_profit': 0.25,
        'max_stocks': 3,
        'rebalance_freq': 5,
        'focus': ['dividend', 'defensive'],
        'description': '牛市末期：逐步兑现利润'
    },
    AStockRegime.BEAR_PANIC: {
        'position': 0.0,  # 完全空仓
        'strategy': 'cash_only',
        'stop_loss': 0.05,
        'take_profit': 0.10,
        'max_stocks': 0,
        'rebalance_freq': 1,
        'focus': ['cash'],
        'description': '熊市恐慌：空仓观望，保存实力'
    },
    AStockRegime.BEAR_GRINDING: {
        'position': 0.10,  # 进一步降低仓位
        'strategy': 'oversold_bounce',
        'stop_loss': 0.05,
        'take_profit': 0.10,  # 降低预期，快速获利了结
        'max_stocks': 1,  # 只持有1只
        'rebalance_freq': 3,
        'focus': ['oversold', 'reversal'],
        'description': '熊市磨底：极小仓位，严格止盈'
    },
    AStockRegime.VOLATILE_UP: {
        'position': 0.35,  # 降低仓位，避免追高
        'strategy': 'buy_dips',
        'stop_loss': 0.08,  # 收紧止损
        'take_profit': 0.15,  # 降低预期，快进快出
        'max_stocks': 2,  # 减少持股
        'rebalance_freq': 3,  # 更频繁调仓
        'focus': ['value', 'support'],
        'description': '震荡向上：保守做多，快进快出'
    },
    AStockRegime.VOLATILE_DOWN: {
        'position': 0.2,
        'strategy': 'sell_rallies',
        'stop_loss': 0.08,
        'take_profit': 0.12,
        'max_stocks': 2,
        'rebalance_freq': 3,
        'focus': ['resistance', 'short_swing'],
        'description': '震荡向下：高抛低吸'
    },
    AStockRegime.VOLATILE_RANGE: {
        'position': 0.3,
        'strategy': 'mean_reversion',
        'stop_loss': 0.12,
        'take_profit': 0.15,
        'max_stocks': 2,
        'rebalance_freq': 3,
        'focus': ['range_trading', 'support_resistance'],
        'description': '区间震荡：高抛低吸网格'
    },
    AStockRegime.POLICY_DRIVEN: {
        'position': 0.6,
        'strategy': 'policy_follow',
        'stop_loss': 0.10,
        'take_profit': 0.30,
        'max_stocks': 4,
        'rebalance_freq': 5,
        'focus': ['policy_beneficiary', 'thematic'],
        'description': '政策驱动：跟随政策热点'
    },
    AStockRegime.SECTOR_ROTATION: {
        'position': 0.5,
        'strategy': 'sector_momentum',
        'stop_loss': 0.10,
        'take_profit': 0.25,
        'max_stocks': 4,
        'rebalance_freq': 5,
        'focus': ['hot_sector', 'rotation'],
        'description': '板块轮动：追踪热点板块'
    }
}


# ============== A股专业环境检测器 ==============

class AStockRegimeDetectorV2:
    """A股市场环境检测器V2
    
    多维度综合评分：
    1. 趋势维度 (30%)：均线系统、价格位置
    2. 动量维度 (20%)：RSI、MACD
    3. 资金维度 (20%)：成交量、换手率
    4. 情绪维度 (15%)：涨跌比、涨停数
    5. 宏观维度 (15%)：政策、外围
    """
    
    WEIGHTS = {
        'trend': 0.30,
        'momentum': 0.20,
        'volume': 0.20,
        'sentiment': 0.15,
        'macro': 0.15
    }
    
    def __init__(self):
        self._history = []
        self._score_history = []
        self._consecutive_days = {}  # 追踪连续天数
        
    def calculate_trend_score(self, prices: pd.Series) -> Tuple[float, Dict]:
        """趋势得分 (-100 ~ +100)"""
        if len(prices) < 120:
            return 0, {}
            
        ma5 = prices.rolling(5).mean().iloc[-1]
        ma10 = prices.rolling(10).mean().iloc[-1]
        ma20 = prices.rolling(20).mean().iloc[-1]
        ma60 = prices.rolling(60).mean().iloc[-1]
        ma120 = prices.rolling(120).mean().iloc[-1]
        current = prices.iloc[-1]
        
        score = 0
        details = {}
        
        # 价格位置得分 (40分)
        above_count = sum([
            current > ma5, current > ma10, current > ma20,
            current > ma60, current > ma120
        ])
        position_score = (above_count - 2.5) * 16  # -40 ~ +40
        score += position_score
        details['position'] = position_score
        
        # 均线排列得分 (40分)
        if ma5 > ma10 > ma20 > ma60:
            alignment_score = 40  # 完美多头
        elif ma5 > ma10 > ma20:
            alignment_score = 25  # 短期多头
        elif ma5 < ma10 < ma20 < ma60:
            alignment_score = -40  # 完美空头
        elif ma5 < ma10 < ma20:
            alignment_score = -25  # 短期空头
        else:
            alignment_score = 0  # 缠绕
        score += alignment_score
        details['alignment'] = alignment_score
        
        # 趋势斜率得分 (20分)
        slope_20 = (ma20 - prices.rolling(20).mean().iloc[-10]) / 10 / current * 1000
        slope_score = np.clip(slope_20 * 10, -20, 20)
        score += slope_score
        details['slope'] = slope_score
        
        return np.clip(score, -100, 100), details
    
    def calculate_momentum_score(self, prices: pd.Series) -> Tuple[float, Dict]:
        """动量得分 (-100 ~ +100)"""
        if len(prices) < 26:
            return 0, {}
            
        details = {}
        score = 0
        
        # RSI得分 (50分)
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-10)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        rsi_score = (rsi - 50) * 1.0  # -50 ~ +50
        score += rsi_score
        details['rsi'] = rsi
        details['rsi_score'] = rsi_score
        
        # MACD得分 (50分)
        exp12 = prices.ewm(span=12).mean()
        exp26 = prices.ewm(span=26).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9).mean()
        hist = macd - signal
        
        # MACD柱状图变化
        hist_change = hist.iloc[-1] - hist.iloc[-3] if len(hist) > 3 else 0
        macd_score = np.clip(hist_change / prices.iloc[-1] * 5000, -50, 50)
        score += macd_score
        details['macd_score'] = macd_score
        
        return np.clip(score, -100, 100), details
    
    def calculate_volume_score(self, prices: pd.Series, volumes: pd.Series) -> Tuple[float, Dict]:
        """成交量得分 (-100 ~ +100)"""
        if len(volumes) < 20:
            return 0, {}
            
        details = {}
        
        vol_ma5 = volumes.rolling(5).mean().iloc[-1]
        vol_ma20 = volumes.rolling(20).mean().iloc[-1]
        vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
        
        # 价格趋势
        price_change = prices.iloc[-1] / prices.iloc[-5] - 1 if len(prices) >= 5 else 0
        
        # 量价配合得分
        if vol_ratio > 1.5 and price_change > 0.03:
            score = 80  # 放量上涨，强势
        elif vol_ratio > 1.2 and price_change > 0:
            score = 40  # 温和放量上涨
        elif vol_ratio < 0.7 and price_change > 0:
            score = -20  # 缩量上涨，动力不足
        elif vol_ratio > 1.5 and price_change < -0.03:
            score = -80  # 放量下跌，恐慌
        elif vol_ratio > 1.2 and price_change < 0:
            score = -40  # 放量下跌
        elif vol_ratio < 0.7 and price_change < 0:
            score = 20  # 缩量下跌，抛压减少
        else:
            score = 0
            
        details['vol_ratio'] = vol_ratio
        details['price_change'] = price_change
        
        return np.clip(score, -100, 100), details
    
    def calculate_sentiment_score(self, prices: pd.Series, highs: pd.Series = None, 
                                   lows: pd.Series = None) -> Tuple[float, Dict]:
        """情绪得分 (-100 ~ +100)
        
        基于：
        1. 新高新低比
        2. 波动率变化
        3. 连续涨跌天数
        """
        if len(prices) < 20:
            return 0, {}
            
        details = {}
        score = 0
        
        # 近期收益率分布
        returns = prices.pct_change().dropna()
        up_days = (returns[-10:] > 0).sum()
        down_days = (returns[-10:] < 0).sum()
        
        # 涨跌天数得分 (50分)
        ratio_score = (up_days - down_days) * 5
        score += ratio_score
        details['up_down_ratio'] = up_days / max(down_days, 1)
        
        # 波动率变化 (50分)
        vol_recent = returns[-5:].std()
        vol_history = returns[-20:].std()
        vol_change = (vol_recent - vol_history) / vol_history if vol_history > 0 else 0
        
        # 波动率上升通常是风险信号
        vol_score = -np.clip(vol_change * 100, -50, 50)
        score += vol_score
        details['vol_change'] = vol_change
        
        return np.clip(score, -100, 100), details
    
    def calculate_macro_score(self, prices: pd.Series) -> Tuple[float, Dict]:
        """宏观得分 (-100 ~ +100)
        
        简化版：基于中长期趋势判断
        """
        if len(prices) < 120:
            return 0, {}
            
        details = {}
        
        # 年度位置
        high_252 = prices.rolling(min(252, len(prices))).max().iloc[-1]
        low_252 = prices.rolling(min(252, len(prices))).min().iloc[-1]
        current = prices.iloc[-1]
        
        position = (current - low_252) / (high_252 - low_252) if high_252 != low_252 else 0.5
        
        # 60日趋势
        ma60_slope = (prices.rolling(60).mean().iloc[-1] - prices.rolling(60).mean().iloc[-20]) / 20
        slope_direction = 1 if ma60_slope > 0 else -1
        
        # 综合得分
        score = (position - 0.5) * 100 * 0.5 + slope_direction * 30
        
        details['year_position'] = position
        details['ma60_slope'] = ma60_slope
        
        return np.clip(score, -100, 100), details
    
    def detect_regime(self, prices: pd.Series, volumes: pd.Series = None,
                      highs: pd.Series = None, lows: pd.Series = None) -> Tuple[AStockRegime, float, Dict]:
        """检测A股市场环境
        
        Returns:
            (环境类型, 综合得分, 详细信息)
        """
        if volumes is None:
            volumes = pd.Series([1] * len(prices))
            
        # 计算各维度得分
        trend_score, trend_detail = self.calculate_trend_score(prices)
        momentum_score, momentum_detail = self.calculate_momentum_score(prices)
        volume_score, volume_detail = self.calculate_volume_score(prices, volumes)
        sentiment_score, sentiment_detail = self.calculate_sentiment_score(prices, highs, lows)
        macro_score, macro_detail = self.calculate_macro_score(prices)
        
        # 综合得分
        total_score = (
            trend_score * self.WEIGHTS['trend'] +
            momentum_score * self.WEIGHTS['momentum'] +
            volume_score * self.WEIGHTS['volume'] +
            sentiment_score * self.WEIGHTS['sentiment'] +
            macro_score * self.WEIGHTS['macro']
        )
        
        # 判断环境
        regime = self._score_to_regime(total_score, prices, volumes)
        
        details = {
            'total': total_score,
            'trend': trend_score,
            'momentum': momentum_score,
            'volume': volume_score,
            'sentiment': sentiment_score,
            'macro': macro_score,
            'details': {
                'trend': trend_detail,
                'momentum': momentum_detail,
                'volume': volume_detail,
                'sentiment': sentiment_detail,
                'macro': macro_detail
            }
        }
        
        return regime, total_score, details
    
    def _score_to_regime(self, score: float, prices: pd.Series, volumes: pd.Series) -> AStockRegime:
        """将得分转换为具体环境
        
        调整阈值使检测更敏感：
        - 牛市：>30 (原>50)
        - 熊市：<-30 (原<-50)
        """
        
        # 计算辅助指标
        if len(prices) >= 60:
            ma20 = prices.rolling(20).mean().iloc[-1]
            ma60 = prices.rolling(60).mean().iloc[-1]
            current = prices.iloc[-1]
            
            # 短期趋势
            short_trend = current / ma20 - 1
            # 中期趋势
            mid_trend = ma20 / ma60 - 1
            
            # 波动率
            vol = prices.pct_change().rolling(20).std().iloc[-1] * np.sqrt(252)
        else:
            short_trend = 0
            mid_trend = 0
            vol = 0.2
        
        # 判断逻辑（降低阈值使检测更敏感）
        if score > 30:  # 牛市阈值从50降到30
            if score > 50 and short_trend > 0.03:
                return AStockRegime.BULL_EARLY
            elif score > 40 and mid_trend > 0:
                return AStockRegime.BULL_MID
            else:
                return AStockRegime.BULL_LATE
        elif score < -30:  # 熊市阈值从-50降到-30
            if score < -50 and vol > 0.25:
                return AStockRegime.BEAR_PANIC
            else:
                return AStockRegime.BEAR_GRINDING
        else:  # -30 ~ 30 震荡区间
            if score > 10 and short_trend > 0:
                return AStockRegime.VOLATILE_UP
            elif score < -10 and short_trend < 0:
                return AStockRegime.VOLATILE_DOWN
            else:
                return AStockRegime.VOLATILE_RANGE


# ============== A股专用策略类 ==============

class AStockBullStrategy:
    """A股牛市策略
    
    牛市三阶段：
    1. 初期：重仓小盘成长
    2. 中期：持股待涨
    3. 末期：逐步兑现
    """
    
    def select_stocks(self, data: Dict[str, pd.DataFrame], regime: AStockRegime, 
                      date: str) -> List[Tuple[str, float]]:
        """选股"""
        scores = []
        
        for stock, df in data.items():
            try:
                df_to_date = df[df.index <= date]
                if len(df_to_date) < 60:
                    continue
                    
                closes = df_to_date['close']
                volumes = df_to_date['volume'] if 'volume' in df_to_date else None
                
                score = 0
                
                if regime == AStockRegime.BULL_EARLY:
                    # 牛市初期：找突破股
                    ma20 = closes.rolling(20).mean().iloc[-1]
                    ma60 = closes.rolling(60).mean().iloc[-1]
                    current = closes.iloc[-1]
                    
                    # 突破20日线
                    if current > ma20 and closes.iloc[-2] < closes.rolling(20).mean().iloc[-2]:
                        score += 50
                    
                    # 成交量放大
                    if volumes is not None:
                        vol_ratio = volumes.iloc[-1] / volumes.rolling(20).mean().iloc[-1]
                        if vol_ratio > 1.5:
                            score += 30
                    
                    # 60日新高
                    if current >= closes.rolling(60).max().iloc[-1]:
                        score += 20
                        
                elif regime == AStockRegime.BULL_MID:
                    # 牛市中期：稳健动量策略（避免追高）
                    ret20 = closes.iloc[-1] / closes.iloc[-20] - 1
                    ret5 = closes.iloc[-1] / closes.iloc[-5] - 1
                    
                    # 计算回撤
                    high_20 = closes.rolling(20).max().iloc[-1]
                    current = closes.iloc[-1]
                    drawdown = (high_20 - current) / high_20
                    
                    # 只选择小幅回调的股票（非追高）
                    if ret20 > 0.05 and drawdown > 0.03 and drawdown < 0.10:
                        # 有动量但有回调空间
                        score = ret20 * 50 + (0.10 - drawdown) * 200
                    else:
                        score = 0
                    
                elif regime == AStockRegime.BULL_LATE:
                    # 牛市末期：防守型
                    # 选择回撤小的
                    high = closes.rolling(60).max().iloc[-1]
                    current = closes.iloc[-1]
                    drawdown = (high - current) / high
                    
                    if drawdown < 0.10:
                        score = (1 - drawdown) * 100
                
                if score > 0:
                    scores.append((stock, score))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:5]


class AStockBearStrategy:
    """A股熊市策略
    
    熊市两阶段：
    1. 恐慌期：完全空仓
    2. 磨底期：小仓位博反弹
    """
    
    def should_stay_cash(self, regime: AStockRegime) -> bool:
        """是否应该空仓"""
        return regime == AStockRegime.BEAR_PANIC
    
    def select_stocks(self, data: Dict[str, pd.DataFrame], date: str) -> List[Tuple[str, float]]:
        """选择超跌反弹标的"""
        scores = []
        
        for stock, df in data.items():
            try:
                df_to_date = df[df.index <= date]
                if len(df_to_date) < 60:
                    continue
                    
                closes = df_to_date['close']
                volumes = df_to_date['volume'] if 'volume' in df_to_date else None
                
                # 计算超跌程度
                high_60 = closes.rolling(60).max().iloc[-1]
                current = closes.iloc[-1]
                drawdown = (high_60 - current) / high_60
                
                # RSI
                delta = closes.diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss.replace(0, 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))
                
                # 缩量企稳
                vol_shrink = 1.0
                if volumes is not None:
                    vol_ma5 = volumes.rolling(5).mean().iloc[-1]
                    vol_ma20 = volumes.rolling(20).mean().iloc[-1]
                    vol_shrink = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
                
                # 极度超跌 + RSI极低 + 缩量 = 反弹信号
                if drawdown > 0.30 and rsi < 25 and vol_shrink < 0.8:
                    score = drawdown * 100 + (25 - rsi) * 2 + (0.8 - vol_shrink) * 50
                    scores.append((stock, score))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:2]  # 最多2只


class AStockVolatileStrategy:
    """A股震荡市策略
    
    三种模式：
    1. 震荡向上：逢低吸纳
    2. 震荡向下：高抛低吸
    3. 区间震荡：网格策略
    """
    
    def select_stocks(self, data: Dict[str, pd.DataFrame], regime: AStockRegime,
                      date: str) -> List[Tuple[str, float]]:
        """选股"""
        scores = []
        
        for stock, df in data.items():
            try:
                df_to_date = df[df.index <= date]
                if len(df_to_date) < 30:
                    continue
                    
                closes = df_to_date['close']
                
                # 计算支撑压力
                support = closes.rolling(20).min().iloc[-1]
                resistance = closes.rolling(20).max().iloc[-1]
                current = closes.iloc[-1]
                
                if resistance == support:
                    continue
                    
                position = (current - support) / (resistance - support)
                
                # 均值
                ma20 = closes.rolling(20).mean().iloc[-1]
                deviation = (current - ma20) / ma20
                
                # RSI
                delta = closes.diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss.replace(0, 1e-10)
                rsi = 100 - (100 / (1 + rs.iloc[-1]))
                
                score = 0
                
                if regime == AStockRegime.VOLATILE_UP:
                    # 震荡向上：在支撑位买入
                    if position < 0.3 and rsi < 40:
                        score = (0.3 - position) * 100 + (40 - rsi)
                        
                elif regime == AStockRegime.VOLATILE_DOWN:
                    # 震荡向下：只有极度超跌才买
                    if position < 0.15 and rsi < 30:
                        score = (0.15 - position) * 200 + (30 - rsi) * 2
                        
                elif regime == AStockRegime.VOLATILE_RANGE:
                    # 区间震荡：均值回归
                    if deviation < -0.05 and rsi < 35:
                        score = abs(deviation) * 100 + (35 - rsi)
                
                if score > 0:
                    scores.append((stock, score))
            except:
                pass
        
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 震荡市限制持股
        max_stocks = 2 if regime in [AStockRegime.VOLATILE_DOWN, AStockRegime.VOLATILE_RANGE] else 3
        return scores[:max_stocks]


# ============== 导出 ==============

__all__ = [
    'AStockRegime',
    'ASTOCK_REGIME_STRATEGY',
    'AStockRegimeDetectorV2',
    'AStockBullStrategy',
    'AStockBearStrategy',
    'AStockVolatileStrategy'
]

