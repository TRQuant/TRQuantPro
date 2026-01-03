"""
TrendAnalyzer v2.0 - 动态阈值趋势分析器

核心改进：
1. 动态阈值：基于近期波动率自适应调整
2. 三周期独立判断
3. 多指标共振确认
4. 解决"低位震荡"误判问题
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import logging

from core.market_env_features import (
    MarketFeatureCalculator, 
    MarketFeatures, 
    PeriodFeatures,
    PERIOD_CONFIGS
)

logger = logging.getLogger(__name__)


class TrendState(Enum):
    """趋势状态"""
    STRONG_BULL = "强势上涨"
    BULL = "上涨"
    WEAK_BULL = "弱势上涨"
    NEUTRAL = "中性"
    WEAK_BEAR = "弱势下跌"
    BEAR = "下跌"
    STRONG_BEAR = "强势下跌"
    
    @property
    def direction(self) -> int:
        """方向: 1=多, -1=空, 0=中性"""
        if self in [TrendState.STRONG_BULL, TrendState.BULL, TrendState.WEAK_BULL]:
            return 1
        elif self in [TrendState.STRONG_BEAR, TrendState.BEAR, TrendState.WEAK_BEAR]:
            return -1
        return 0
    
    @property
    def strength(self) -> float:
        """强度: 0-1"""
        mapping = {
            TrendState.STRONG_BULL: 1.0,
            TrendState.BULL: 0.7,
            TrendState.WEAK_BULL: 0.4,
            TrendState.NEUTRAL: 0.0,
            TrendState.WEAK_BEAR: 0.4,
            TrendState.BEAR: 0.7,
            TrendState.STRONG_BEAR: 1.0
        }
        return mapping.get(self, 0)


@dataclass
class PeriodTrendResult:
    """单周期趋势结果"""
    period: str
    period_name: str
    state: TrendState
    score: float           # -100 到 100
    confidence: float      # 0 到 100
    signals: Dict = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'period': self.period,
            'period_name': self.period_name,
            'state': self.state.name,
            'state_name': self.state.value,
            'direction': self.state.direction,
            'score': round(self.score, 2),
            'confidence': round(self.confidence, 2),
            'signals': self.signals
        }


@dataclass
class TrendAnalysisResult:
    """趋势分析完整结果"""
    weekly: PeriodTrendResult
    monthly: PeriodTrendResult
    quarterly: PeriodTrendResult
    
    combined_state: TrendState
    combined_score: float
    combined_confidence: float
    
    multi_period_alignment: bool  # 多周期是否一致
    
    def to_dict(self) -> dict:
        return {
            'weekly': self.weekly.to_dict(),
            'monthly': self.monthly.to_dict(),
            'quarterly': self.quarterly.to_dict(),
            'combined': {
                'state': self.combined_state.name,
                'state_name': self.combined_state.value,
                'direction': self.combined_state.direction,
                'score': round(self.combined_score, 2),
                'confidence': round(self.combined_confidence, 2)
            },
            'multi_period_alignment': self.multi_period_alignment
        }


class DynamicThresholds:
    """
    动态阈值管理器
    
    根据近期波动率自适应调整阈值
    """
    
    # 基准阈值（标准波动率下）
    BASE_THRESHOLDS = {
        'momentum_strong': 8.0,    # 强势动量
        'momentum_medium': 3.0,    # 中等动量
        'momentum_weak': 1.0,      # 弱势动量
        'ma_deviation_strong': 5.0,  # 强势均线偏离
        'ma_deviation_medium': 2.0,  # 中等均线偏离
        'rsi_overbought': 70,
        'rsi_oversold': 30,
        'position_high': 70,
        'position_low': 30,
    }
    
    # 标准波动率（基准）
    STANDARD_VOLATILITY = 20.0  # 20%年化波动率
    
    def __init__(self, recent_volatility: float = None):
        """
        初始化动态阈值
        
        Args:
            recent_volatility: 近期波动率（年化%）
        """
        self.volatility = recent_volatility or self.STANDARD_VOLATILITY
        self.vol_ratio = self.volatility / self.STANDARD_VOLATILITY
        
    def get(self, key: str) -> float:
        """获取调整后的阈值"""
        base = self.BASE_THRESHOLDS.get(key, 0)
        
        # 波动率调整系数
        if key.startswith('momentum') or key.startswith('ma_deviation'):
            # 高波动率时提高阈值，低波动率时降低
            return base * self.vol_ratio
        else:
            return base
    
    def update_volatility(self, new_volatility: float):
        """更新波动率"""
        self.volatility = new_volatility
        self.vol_ratio = new_volatility / self.STANDARD_VOLATILITY


class TrendAnalyzerV2:
    """
    TrendAnalyzer v2.0
    
    核心改进：
    1. 动态阈值
    2. 三周期分析
    3. 多信号确认
    """
    
    # 权重配置
    PERIOD_WEIGHTS = {
        'weekly': 0.2,    # 周级别权重
        'monthly': 0.3,   # 月级别权重
        'quarterly': 0.5  # 季度级别权重
    }
    
    def __init__(self):
        self.feature_calculator = MarketFeatureCalculator()
        self.thresholds = DynamicThresholds()
        
    def analyze(self, df: pd.DataFrame) -> TrendAnalysisResult:
        """
        分析市场趋势
        
        Args:
            df: OHLCV数据
            
        Returns:
            TrendAnalysisResult: 完整分析结果
        """
        # 计算特征
        features = self.feature_calculator.calculate(df)
        
        # 更新动态阈值（使用月度波动率）
        self.thresholds.update_volatility(features.monthly.volatility)
        
        # 分析三个周期
        weekly_result = self._analyze_period(features.weekly)
        monthly_result = self._analyze_period(features.monthly)
        quarterly_result = self._analyze_period(features.quarterly)
        
        # 综合判断
        combined_score, combined_confidence = self._calculate_combined(
            weekly_result, monthly_result, quarterly_result
        )
        combined_state = self._score_to_state(combined_score)
        
        # 检查多周期一致性
        alignment = self._check_alignment(weekly_result, monthly_result, quarterly_result)
        
        return TrendAnalysisResult(
            weekly=weekly_result,
            monthly=monthly_result,
            quarterly=quarterly_result,
            combined_state=combined_state,
            combined_score=combined_score,
            combined_confidence=combined_confidence,
            multi_period_alignment=alignment
        )
    
    def _analyze_period(self, pf: PeriodFeatures) -> PeriodTrendResult:
        """分析单周期趋势"""
        signals = {}
        score_components = []
        
        # 1. 动量信号
        momentum_score = self._analyze_momentum(pf.momentum)
        signals['momentum'] = {
            'value': pf.momentum,
            'score': momentum_score,
            'signal': 'bullish' if momentum_score > 20 else ('bearish' if momentum_score < -20 else 'neutral')
        }
        score_components.append(('momentum', momentum_score, 0.30))
        
        # 2. 均线排列信号
        ma_score = pf.ma_alignment
        signals['ma_alignment'] = {
            'value': pf.ma_alignment,
            'score': ma_score,
            'signal': 'bullish' if ma_score > 30 else ('bearish' if ma_score < -30 else 'neutral')
        }
        score_components.append(('ma_alignment', ma_score, 0.20))
        
        # 3. 价格vs均线
        deviation_score = self._analyze_ma_deviation(pf.price_vs_ma)
        signals['price_vs_ma'] = {
            'value': pf.price_vs_ma,
            'score': deviation_score,
            'signal': 'bullish' if deviation_score > 20 else ('bearish' if deviation_score < -20 else 'neutral')
        }
        score_components.append(('price_vs_ma', deviation_score, 0.15))
        
        # 4. RSI信号
        rsi_score = self._analyze_rsi(pf.rsi)
        signals['rsi'] = {
            'value': pf.rsi,
            'score': rsi_score,
            'signal': 'overbought' if pf.rsi > 70 else ('oversold' if pf.rsi < 30 else 'neutral')
        }
        score_components.append(('rsi', rsi_score, 0.10))
        
        # 5. 区间位置信号
        position_score = self._analyze_position(pf.position_in_range)
        signals['position'] = {
            'value': pf.position_in_range,
            'score': position_score,
            'signal': 'high' if pf.position_in_range > 70 else ('low' if pf.position_in_range < 30 else 'mid')
        }
        score_components.append(('position', position_score, 0.15))
        
        # 6. MACD信号
        macd_score = self._analyze_macd(pf.macd_histogram, pf.macd_signal)
        signals['macd'] = {
            'histogram': pf.macd_histogram,
            'signal_type': pf.macd_signal,
            'score': macd_score,
            'signal': 'golden_cross' if pf.macd_signal == 1 else ('death_cross' if pf.macd_signal == -1 else 'neutral')
        }
        score_components.append(('macd', macd_score, 0.10))
        
        # 计算综合得分
        total_score = sum(score * weight for _, score, weight in score_components)
        
        # 计算置信度（基于信号一致性）
        bullish_count = sum(1 for _, s, _ in score_components if s > 20)
        bearish_count = sum(1 for _, s, _ in score_components if s < -20)
        max_count = max(bullish_count, bearish_count)
        confidence = (max_count / len(score_components)) * 100
        
        # 额外的置信度调整
        if abs(total_score) > 50:
            confidence = min(100, confidence * 1.2)
        
        state = self._score_to_state(total_score)
        
        return PeriodTrendResult(
            period=pf.period,
            period_name=pf.period_name,
            state=state,
            score=total_score,
            confidence=confidence,
            signals=signals
        )
    
    def _analyze_momentum(self, momentum: float) -> float:
        """分析动量，返回-100到100的得分"""
        strong_thresh = self.thresholds.get('momentum_strong')
        medium_thresh = self.thresholds.get('momentum_medium')
        
        if momentum >= strong_thresh:
            return min(100, 70 + (momentum - strong_thresh) * 3)
        elif momentum >= medium_thresh:
            return 40 + (momentum - medium_thresh) / (strong_thresh - medium_thresh) * 30
        elif momentum > 0:
            return momentum / medium_thresh * 40
        elif momentum >= -medium_thresh:
            return momentum / medium_thresh * 40
        elif momentum >= -strong_thresh:
            return -40 - (abs(momentum) - medium_thresh) / (strong_thresh - medium_thresh) * 30
        else:
            return max(-100, -70 - (abs(momentum) - strong_thresh) * 3)
    
    def _analyze_ma_deviation(self, deviation: float) -> float:
        """分析均线偏离，返回-100到100的得分"""
        strong_thresh = self.thresholds.get('ma_deviation_strong')
        medium_thresh = self.thresholds.get('ma_deviation_medium')
        
        if deviation >= strong_thresh:
            return min(100, 60 + (deviation - strong_thresh) * 4)
        elif deviation >= medium_thresh:
            return 30 + (deviation - medium_thresh) / (strong_thresh - medium_thresh) * 30
        elif deviation > 0:
            return deviation / medium_thresh * 30
        elif deviation >= -medium_thresh:
            return deviation / medium_thresh * 30
        elif deviation >= -strong_thresh:
            return -30 - (abs(deviation) - medium_thresh) / (strong_thresh - medium_thresh) * 30
        else:
            return max(-100, -60 - (abs(deviation) - strong_thresh) * 4)
    
    def _analyze_rsi(self, rsi: float) -> float:
        """分析RSI，返回-100到100的得分"""
        overbought = self.thresholds.get('rsi_overbought')
        oversold = self.thresholds.get('rsi_oversold')
        
        if rsi >= overbought:
            # 超买区间 - 趋势延续但可能反转
            return min(50, (rsi - overbought) * 2)
        elif rsi <= oversold:
            # 超卖区间
            return max(-50, -(oversold - rsi) * 2)
        elif rsi >= 50:
            # 强势区间
            return (rsi - 50) / (overbought - 50) * 30
        else:
            # 弱势区间
            return (rsi - 50) / (50 - oversold) * 30
    
    def _analyze_position(self, position: float) -> float:
        """分析区间位置，返回-100到100的得分"""
        high_thresh = self.thresholds.get('position_high')
        low_thresh = self.thresholds.get('position_low')
        
        if position >= high_thresh:
            return min(80, 40 + (position - high_thresh) * 1.5)
        elif position <= low_thresh:
            return max(-80, -40 - (low_thresh - position) * 1.5)
        else:
            # 中间区域
            mid = (high_thresh + low_thresh) / 2
            return (position - mid) / (high_thresh - mid) * 40
    
    def _analyze_macd(self, histogram: float, signal: int) -> float:
        """分析MACD，返回-100到100的得分"""
        base_score = 0
        
        # 柱状图方向
        if histogram > 0:
            base_score = min(50, histogram * 100)
        else:
            base_score = max(-50, histogram * 100)
        
        # 信号加成
        if signal == 1:  # 金叉
            base_score = min(100, base_score + 30)
        elif signal == -1:  # 死叉
            base_score = max(-100, base_score - 30)
        
        return base_score
    
    def _score_to_state(self, score: float) -> TrendState:
        """将得分转换为趋势状态"""
        if score >= 60:
            return TrendState.STRONG_BULL
        elif score >= 30:
            return TrendState.BULL
        elif score >= 10:
            return TrendState.WEAK_BULL
        elif score > -10:
            return TrendState.NEUTRAL
        elif score > -30:
            return TrendState.WEAK_BEAR
        elif score > -60:
            return TrendState.BEAR
        else:
            return TrendState.STRONG_BEAR
    
    def _calculate_combined(self, 
                           weekly: PeriodTrendResult,
                           monthly: PeriodTrendResult,
                           quarterly: PeriodTrendResult) -> Tuple[float, float]:
        """计算综合得分和置信度"""
        # 加权得分
        combined_score = (
            weekly.score * self.PERIOD_WEIGHTS['weekly'] +
            monthly.score * self.PERIOD_WEIGHTS['monthly'] +
            quarterly.score * self.PERIOD_WEIGHTS['quarterly']
        )
        
        # 置信度综合
        combined_confidence = (
            weekly.confidence * self.PERIOD_WEIGHTS['weekly'] +
            monthly.confidence * self.PERIOD_WEIGHTS['monthly'] +
            quarterly.confidence * self.PERIOD_WEIGHTS['quarterly']
        )
        
        # 多周期一致性加成
        directions = [weekly.state.direction, monthly.state.direction, quarterly.state.direction]
        if all(d == 1 for d in directions):  # 全部看多
            combined_confidence = min(100, combined_confidence * 1.3)
        elif all(d == -1 for d in directions):  # 全部看空
            combined_confidence = min(100, combined_confidence * 1.3)
        elif len(set(directions)) == 3:  # 完全分歧
            combined_confidence *= 0.7
        
        return combined_score, combined_confidence
    
    def _check_alignment(self,
                        weekly: PeriodTrendResult,
                        monthly: PeriodTrendResult,
                        quarterly: PeriodTrendResult) -> bool:
        """检查多周期是否一致"""
        directions = [weekly.state.direction, monthly.state.direction, quarterly.state.direction]
        # 至少2个方向一致
        return directions.count(1) >= 2 or directions.count(-1) >= 2


# 便捷函数
def analyze_trend(df: pd.DataFrame) -> TrendAnalysisResult:
    """
    分析市场趋势
    
    Args:
        df: OHLCV数据
        
    Returns:
        TrendAnalysisResult
    """
    analyzer = TrendAnalyzerV2()
    return analyzer.analyze(df)


def get_trend_summary(result: TrendAnalysisResult) -> str:
    """生成趋势分析摘要"""
    lines = []
    lines.append("=" * 50)
    lines.append("趋势分析摘要 (TrendAnalyzer v2)")
    lines.append("=" * 50)
    
    for period in ['weekly', 'monthly', 'quarterly']:
        pr = getattr(result, period)
        direction = "↑" if pr.state.direction > 0 else ("↓" if pr.state.direction < 0 else "→")
        lines.append(f"\n【{pr.period_name}】 {direction} {pr.state.value}")
        lines.append(f"  得分: {pr.score:+.1f}")
        lines.append(f"  置信度: {pr.confidence:.1f}%")
    
    lines.append(f"\n【综合判断】")
    direction = "↑" if result.combined_state.direction > 0 else ("↓" if result.combined_state.direction < 0 else "→")
    lines.append(f"  状态: {direction} {result.combined_state.value}")
    lines.append(f"  得分: {result.combined_score:+.1f}")
    lines.append(f"  置信度: {result.combined_confidence:.1f}%")
    lines.append(f"  多周期一致: {'是' if result.multi_period_alignment else '否'}")
    
    return "\n".join(lines)

