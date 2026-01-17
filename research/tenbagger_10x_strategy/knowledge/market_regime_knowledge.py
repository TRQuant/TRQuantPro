#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Market Regime Knowledge Base - 市场环境知识库
============================================

专业的市场环境判断知识库，包含：
1. 市场环境定义与特征
2. 专业指标体系
3. 判断算法
4. 策略映射

参考文献：
- Hamilton (1989): Markov Regime Switching
- Ang & Bekaert (2002): International Asset Allocation with Regime Shifts
- Stockformer (2024): Wavelet + Multi-task Self-Attention
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd


class MarketRegime(Enum):
    """市场环境枚举"""
    BULL = "BULL"           # 牛市
    BEAR = "BEAR"           # 熊市
    VOLATILE = "VOLATILE"   # 震荡市
    RECOVERY = "RECOVERY"   # 复苏期
    DISTRIBUTION = "DISTRIBUTION"  # 派发期
    

@dataclass
class RegimeCharacteristics:
    """市场环境特征"""
    name: str
    description: str
    typical_duration_days: Tuple[int, int]  # (min, max)
    trend_direction: str  # up/down/sideways
    volatility_level: str  # low/medium/high
    volume_pattern: str   # increasing/decreasing/stable
    
    # 技术指标特征
    ma_pattern: str       # above/below/cross
    rsi_range: Tuple[int, int]
    macd_signal: str      # bullish/bearish/neutral
    
    # 策略建议
    position_range: Tuple[float, float]  # (min, max) 仓位
    strategy_type: List[str]
    risk_level: str


# ============== 市场环境特征知识库 ==============

REGIME_CHARACTERISTICS = {
    MarketRegime.BULL: RegimeCharacteristics(
        name="牛市",
        description="市场整体上涨趋势明确，赚钱效应强，增量资金持续入场",
        typical_duration_days=(60, 365),
        trend_direction="up",
        volatility_level="medium",
        volume_pattern="increasing",
        ma_pattern="MA5 > MA20 > MA60",
        rsi_range=(50, 80),
        macd_signal="bullish",
        position_range=(0.7, 1.0),
        strategy_type=["momentum", "growth", "breakout"],
        risk_level="medium"
    ),
    
    MarketRegime.BEAR: RegimeCharacteristics(
        name="熊市",
        description="市场整体下跌趋势明确，避险情绪主导，资金持续流出",
        typical_duration_days=(60, 365),
        trend_direction="down",
        volatility_level="high",
        volume_pattern="decreasing",
        ma_pattern="MA5 < MA20 < MA60",
        rsi_range=(20, 45),
        macd_signal="bearish",
        position_range=(0.0, 0.2),
        strategy_type=["defensive", "cash", "hedge"],
        risk_level="high"
    ),
    
    MarketRegime.VOLATILE: RegimeCharacteristics(
        name="震荡市",
        description="市场缺乏明确方向，在区间内波动，主力资金博弈",
        typical_duration_days=(20, 120),
        trend_direction="sideways",
        volatility_level="medium",
        volume_pattern="stable",
        ma_pattern="MA系统缠绕",
        rsi_range=(40, 60),
        macd_signal="neutral",
        position_range=(0.3, 0.5),
        strategy_type=["mean_reversion", "range_trading", "dividend"],
        risk_level="medium"
    ),
    
    MarketRegime.RECOVERY: RegimeCharacteristics(
        name="复苏期",
        description="市场从底部开始企稳回升，先知先觉资金入场",
        typical_duration_days=(20, 60),
        trend_direction="up",
        volatility_level="medium",
        volume_pattern="increasing",
        ma_pattern="MA5上穿MA20",
        rsi_range=(35, 55),
        macd_signal="turning_bullish",
        position_range=(0.5, 0.7),
        strategy_type=["value", "contrarian", "tenbagger_early"],
        risk_level="medium"
    ),
    
    MarketRegime.DISTRIBUTION: RegimeCharacteristics(
        name="派发期",
        description="市场从高点开始派发筹码，主力资金出货",
        typical_duration_days=(20, 60),
        trend_direction="down",
        volatility_level="high",
        volume_pattern="high_but_decreasing",
        ma_pattern="MA5下穿MA20",
        rsi_range=(55, 75),
        macd_signal="turning_bearish",
        position_range=(0.2, 0.4),
        strategy_type=["momentum_exit", "protective_put"],
        risk_level="high"
    )
}


# ============== 专业指标体系 ==============

@dataclass
class TechnicalIndicators:
    """技术指标"""
    # 趋势指标
    ma5: float
    ma10: float
    ma20: float
    ma60: float
    ma250: float
    
    # 动量指标
    rsi14: float
    macd: float
    macd_signal: float
    macd_hist: float
    
    # 波动率指标
    atr14: float
    bollinger_width: float
    
    # 成交量指标
    volume_ma5: float
    volume_ma20: float
    volume_ratio: float
    
    # 市场宽度
    advance_decline_ratio: float  # 涨跌比
    new_high_low_ratio: float     # 新高新低比


@dataclass 
class MacroIndicators:
    """宏观指标"""
    pmi: float              # 制造业PMI
    m2_growth: float        # M2增速
    credit_growth: float    # 信贷增速
    interest_rate: float    # 利率水平
    exchange_rate: float    # 汇率
    cpi: float              # 通胀


@dataclass
class SentimentIndicators:
    """情绪指标"""
    turnover_rate: float    # 换手率
    margin_balance: float   # 融资余额
    fund_flow: float        # 资金流向
    new_accounts: float     # 新开户数


# ============== 市场环境判断算法 ==============

class ProfessionalRegimeDetector:
    """专业市场环境检测器
    
    采用多因子综合评分方法：
    1. 趋势因子 (40%)
    2. 动量因子 (25%)
    3. 波动率因子 (20%)
    4. 成交量因子 (15%)
    """
    
    # 因子权重
    WEIGHTS = {
        'trend': 0.40,
        'momentum': 0.25,
        'volatility': 0.20,
        'volume': 0.15
    }
    
    # 环境分数阈值
    THRESHOLDS = {
        'bull': 40,           # >40 = 牛市
        'bear': -40,          # <-40 = 熊市
        'recovery': 10,       # 0~40 且从低位上来 = 复苏
        'distribution': -10,  # -40~0 且从高位下来 = 派发
    }
    
    def __init__(self):
        self._history = []  # 历史环境记录
        self._score_history = []  # 历史分数
        
    def calculate_trend_score(self, prices: pd.Series) -> float:
        """计算趋势因子得分 (-100 ~ +100)"""
        if len(prices) < 60:
            return 0
            
        ma5 = prices.rolling(5).mean().iloc[-1]
        ma20 = prices.rolling(20).mean().iloc[-1]
        ma60 = prices.rolling(60).mean().iloc[-1]
        current = prices.iloc[-1]
        
        score = 0
        
        # 价格与均线关系 (50分)
        if current > ma5:
            score += 15
        if current > ma20:
            score += 20
        if current > ma60:
            score += 15
            
        if current < ma5:
            score -= 15
        if current < ma20:
            score -= 20
        if current < ma60:
            score -= 15
            
        # 均线排列 (50分)
        if ma5 > ma20 > ma60:
            score += 50  # 多头排列
        elif ma5 < ma20 < ma60:
            score -= 50  # 空头排列
        else:
            # 缠绕状态，根据斜率判断
            ma20_slope = (ma20 - prices.rolling(20).mean().iloc[-5]) / 5
            if ma20_slope > 0:
                score += 20
            elif ma20_slope < 0:
                score -= 20
                
        return np.clip(score, -100, 100)
    
    def calculate_momentum_score(self, prices: pd.Series) -> float:
        """计算动量因子得分 (-100 ~ +100)"""
        if len(prices) < 20:
            return 0
            
        # RSI
        delta = prices.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-10)
        rsi = 100 - (100 / (1 + rs.iloc[-1]))
        
        # RSI得分 (50分)
        rsi_score = (rsi - 50) * 2  # 0->-100, 50->0, 100->100
        
        # MACD
        exp12 = prices.ewm(span=12).mean()
        exp26 = prices.ewm(span=26).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9).mean()
        hist = macd - signal
        
        # MACD得分 (50分)
        macd_score = 0
        if hist.iloc[-1] > 0:
            macd_score = min(50, hist.iloc[-1] / prices.iloc[-1] * 5000)
        else:
            macd_score = max(-50, hist.iloc[-1] / prices.iloc[-1] * 5000)
            
        return np.clip(rsi_score * 0.5 + macd_score, -100, 100)
    
    def calculate_volatility_score(self, prices: pd.Series) -> float:
        """计算波动率因子得分 (-100 ~ +100)
        
        高波动率在上涨趋势中为正，在下跌趋势中为负
        """
        if len(prices) < 20:
            return 0
            
        returns = prices.pct_change().dropna()
        vol_20 = returns.rolling(20).std().iloc[-1] * np.sqrt(252) * 100  # 年化波动率%
        vol_5 = returns.rolling(5).std().iloc[-1] * np.sqrt(252) * 100
        
        # 判断趋势方向
        trend = 1 if prices.iloc[-1] > prices.iloc[-20] else -1
        
        # 波动率变化
        vol_change = vol_5 - vol_20
        
        score = 0
        if vol_20 < 15:  # 低波动
            score = 30 * trend
        elif vol_20 < 25:  # 中波动
            score = 0
        else:  # 高波动
            score = -30 * trend  # 高波动通常是风险信号
            
        # 波动率扩张/收缩
        if vol_change > 0:  # 波动率扩张
            score -= 20  # 不确定性增加
        else:
            score += 10
            
        return np.clip(score, -100, 100)
    
    def calculate_volume_score(self, prices: pd.Series, volumes: pd.Series) -> float:
        """计算成交量因子得分 (-100 ~ +100)"""
        if len(volumes) < 20:
            return 0
            
        vol_ma5 = volumes.rolling(5).mean().iloc[-1]
        vol_ma20 = volumes.rolling(20).mean().iloc[-1]
        
        # 量比
        vol_ratio = vol_ma5 / vol_ma20 if vol_ma20 > 0 else 1
        
        # 价格趋势
        price_up = prices.iloc[-1] > prices.iloc[-5]
        
        score = 0
        if vol_ratio > 1.5:  # 放量
            score = 50 if price_up else -50  # 放量上涨好，放量下跌坏
        elif vol_ratio > 1.2:
            score = 25 if price_up else -25
        elif vol_ratio < 0.8:  # 缩量
            score = -25 if price_up else 25  # 缩量上涨弱，缩量下跌企稳
            
        return np.clip(score, -100, 100)
    
    def detect_regime(self, prices: pd.Series, volumes: pd.Series = None) -> Tuple[MarketRegime, float, Dict]:
        """检测市场环境
        
        Returns:
            (环境类型, 综合得分, 详细分数)
        """
        if volumes is None:
            volumes = pd.Series([1] * len(prices))
            
        # 计算各因子得分
        trend_score = self.calculate_trend_score(prices)
        momentum_score = self.calculate_momentum_score(prices)
        volatility_score = self.calculate_volatility_score(prices)
        volume_score = self.calculate_volume_score(prices, volumes)
        
        # 综合得分
        total_score = (
            trend_score * self.WEIGHTS['trend'] +
            momentum_score * self.WEIGHTS['momentum'] +
            volatility_score * self.WEIGHTS['volatility'] +
            volume_score * self.WEIGHTS['volume']
        )
        
        # 判断环境
        regime = self._score_to_regime(total_score, prices)
        
        # 记录历史
        self._score_history.append(total_score)
        self._history.append(regime)
        
        details = {
            'trend': trend_score,
            'momentum': momentum_score,
            'volatility': volatility_score,
            'volume': volume_score,
            'total': total_score
        }
        
        return regime, total_score, details
    
    def _score_to_regime(self, score: float, prices: pd.Series) -> MarketRegime:
        """将分数转换为市场环境"""
        # 计算价格位置（相对于52周高低点）
        if len(prices) >= 252:
            high_52w = prices.rolling(252).max().iloc[-1]
            low_52w = prices.rolling(252).min().iloc[-1]
            position = (prices.iloc[-1] - low_52w) / (high_52w - low_52w) if high_52w != low_52w else 0.5
        else:
            position = 0.5
            
        if score > self.THRESHOLDS['bull']:
            return MarketRegime.BULL
        elif score < self.THRESHOLDS['bear']:
            return MarketRegime.BEAR
        elif score > self.THRESHOLDS['recovery'] and position < 0.4:
            return MarketRegime.RECOVERY
        elif score < self.THRESHOLDS['distribution'] and position > 0.6:
            return MarketRegime.DISTRIBUTION
        else:
            return MarketRegime.VOLATILE


# ============== 策略映射 ==============

REGIME_STRATEGY_MAP = {
    MarketRegime.BULL: {
        'position': 0.8,
        'strategies': ['momentum', 'growth', 'breakout'],
        'stop_loss': 0.15,
        'take_profit': 0.50,
        'rebalance_freq': 10,
        'max_stocks': 5,
    },
    MarketRegime.BEAR: {
        'position': 0.1,  # 熊市只保留10%仓位
        'strategies': ['defensive', 'dividend', 'cash'],
        'stop_loss': 0.08,
        'take_profit': 0.20,
        'rebalance_freq': 5,
        'max_stocks': 2,
    },
    MarketRegime.VOLATILE: {
        'position': 0.3,  # 降低仓位
        'strategies': ['mean_reversion', 'range_trading', 'dividend'],
        'stop_loss': 0.15,  # 放宽止损，避免频繁止损
        'take_profit': 0.15,  # 降低止盈，快进快出
        'rebalance_freq': 3,  # 更频繁调仓
        'max_stocks': 2,  # 减少持股数
    },
    MarketRegime.RECOVERY: {
        'position': 0.6,
        'strategies': ['value', 'tenbagger_early', 'contrarian'],
        'stop_loss': 0.12,
        'take_profit': 0.40,
        'rebalance_freq': 10,
        'max_stocks': 5,
    },
    MarketRegime.DISTRIBUTION: {
        'position': 0.3,
        'strategies': ['momentum_exit', 'protective'],
        'stop_loss': 0.08,
        'take_profit': 0.15,
        'rebalance_freq': 3,
        'max_stocks': 3,
    }
}


# ============== 震荡市专用策略 ==============

class VolatileMarketStrategy:
    """震荡市专用策略
    
    特点：
    1. 箱体交易：在支撑位买入，压力位卖出
    2. 均值回归：偏离均值时反向操作
    3. 低仓位运行：控制风险
    """
    
    def __init__(self):
        self.position_limit = 0.4  # 最大仓位40%
        
    def calculate_support_resistance(self, prices: pd.Series, window: int = 20) -> Tuple[float, float]:
        """计算支撑位和压力位"""
        high = prices.rolling(window).max().iloc[-1]
        low = prices.rolling(window).min().iloc[-1]
        return low, high
    
    def get_signal(self, prices: pd.Series) -> str:
        """获取交易信号"""
        support, resistance = self.calculate_support_resistance(prices)
        current = prices.iloc[-1]
        
        # 计算位置
        if resistance == support:
            position_ratio = 0.5
        else:
            position_ratio = (current - support) / (resistance - support)
        
        # 均值
        ma20 = prices.rolling(20).mean().iloc[-1]
        deviation = (current - ma20) / ma20
        
        if position_ratio < 0.2 or deviation < -0.05:
            return "BUY"  # 接近支撑位或明显低于均值
        elif position_ratio > 0.8 or deviation > 0.05:
            return "SELL"  # 接近压力位或明显高于均值
        else:
            return "HOLD"
    
    def select_stocks(self, stock_data: Dict[str, pd.DataFrame]) -> List[Tuple[str, float, str]]:
        """选股（均值回归策略）
        
        Returns:
            [(stock, score, signal), ...]
        """
        candidates = []
        
        for stock, df in stock_data.items():
            if len(df) < 20:
                continue
                
            prices = df['close']
            ma20 = prices.rolling(20).mean().iloc[-1]
            current = prices.iloc[-1]
            deviation = (current - ma20) / ma20
            
            # RSI
            delta = prices.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, 1e-10)
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            # 超跌反弹信号
            if deviation < -0.05 and rsi < 35:
                score = abs(deviation) * 100 + (35 - rsi)
                candidates.append((stock, score, "BUY"))
            # 超涨回落信号
            elif deviation > 0.05 and rsi > 65:
                score = deviation * 100 + (rsi - 65)
                candidates.append((stock, score, "SELL"))
                
        return sorted(candidates, key=lambda x: x[1], reverse=True)


# ============== 熊市专用策略 ==============

class BearMarketStrategy:
    """熊市专用策略
    
    特点：
    1. 极低仓位：最多10%
    2. 只做确定性机会：超跌反弹
    3. 快进快出：严格止损止盈
    """
    
    def __init__(self):
        self.position_limit = 0.1  # 最大仓位10%
        self.stop_loss = 0.05      # 5%止损
        self.take_profit = 0.10    # 10%止盈
        
    def get_oversold_stocks(self, stock_data: Dict[str, pd.DataFrame]) -> List[Tuple[str, float]]:
        """寻找超跌股票"""
        candidates = []
        
        for stock, df in stock_data.items():
            if len(df) < 60:
                continue
                
            prices = df['close']
            
            # 计算跌幅
            high_60 = prices.rolling(60).max().iloc[-1]
            current = prices.iloc[-1]
            drawdown = (high_60 - current) / high_60
            
            # RSI
            delta = prices.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, 1e-10)
            rsi = 100 - (100 / (1 + rs.iloc[-1]))
            
            # 超跌条件：跌幅>30%且RSI<25
            if drawdown > 0.30 and rsi < 25:
                score = drawdown * 100 + (25 - rsi)
                candidates.append((stock, score))
                
        return sorted(candidates, key=lambda x: x[1], reverse=True)[:3]  # 最多3只
    
    def should_exit_all(self, index_prices: pd.Series) -> bool:
        """判断是否应该清仓"""
        if len(index_prices) < 20:
            return False
            
        ma5 = index_prices.rolling(5).mean().iloc[-1]
        ma20 = index_prices.rolling(20).mean().iloc[-1]
        
        # 如果均线向下发散，清仓
        if ma5 < ma20 * 0.98:  # MA5低于MA20超过2%
            return True
            
        # 加速下跌
        ret_5 = index_prices.iloc[-1] / index_prices.iloc[-5] - 1
        if ret_5 < -0.05:  # 5日跌幅超过5%
            return True
            
        return False


# ============== 导出 ==============

__all__ = [
    'MarketRegime',
    'RegimeCharacteristics',
    'REGIME_CHARACTERISTICS',
    'TechnicalIndicators',
    'MacroIndicators',
    'SentimentIndicators',
    'ProfessionalRegimeDetector',
    'REGIME_STRATEGY_MAP',
    'VolatileMarketStrategy',
    'BearMarketStrategy'
]

