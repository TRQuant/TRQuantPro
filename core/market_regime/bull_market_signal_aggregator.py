#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市信号聚合器

聚合多维度信号（技术指标、资金面、情绪面），动态调整权重，输出牛市概率和强度等级。
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import numpy as np
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.market_regime.bull_market_detector import BullMarketDetector, BullMarketResult

logger = logging.getLogger(__name__)


@dataclass
class SignalWeight:
    """信号权重（动态调整）"""
    technical: float = 0.35      # 技术指标权重
    capital: float = 0.25        # 资金面权重
    sentiment: float = 0.20      # 情绪面权重
    macro: float = 0.20          # 宏观面权重
    
    def normalize(self):
        """归一化权重"""
        total = self.technical + self.capital + self.sentiment + self.macro
        if total > 0:
            self.technical /= total
            self.capital /= total
            self.sentiment /= total
            self.macro /= total


@dataclass
class AggregatedSignal:
    """聚合后的信号"""
    bull_probability: float      # 牛市概率（0-100%）
    strength_level: str          # 强度等级（STRONG/NORMAL/LATE/PULLBACK）
    strength_score: float        # 强度得分（0-100）
    confidence: float            # 置信度（0-1）
    
    # 分维度得分
    technical_score: float = 0.0
    capital_score: float = 0.0
    sentiment_score: float = 0.0
    macro_score: float = 0.0
    
    # 建议
    position_suggestion: float = 0.5
    strategy_suggestion: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'bull_probability': self.bull_probability,
            'strength_level': self.strength_level,
            'strength_score': self.strength_score,
            'confidence': self.confidence,
            'technical_score': self.technical_score,
            'capital_score': self.capital_score,
            'sentiment_score': self.sentiment_score,
            'macro_score': self.macro_score,
            'position_suggestion': self.position_suggestion,
            'strategy_suggestion': self.strategy_suggestion,
        }


class BullMarketSignalAggregator:
    """牛市信号聚合器"""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.detector = BullMarketDetector(verbose=False)
        self.weights = SignalWeight()
        self.history_accuracy = []  # 历史准确性（用于动态调整权重）
    
    def aggregate(self, date: str = None) -> AggregatedSignal:
        """
        聚合信号
        
        Args:
            date: 日期（None表示今天）
        
        Returns:
            AggregatedSignal
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # 1. 获取基础检测结果
        bull_result = self.detector.detect(date)
        
        # 2. 计算各维度得分
        technical_score = self._calc_technical_score(bull_result)
        capital_score = self._calc_capital_score(bull_result)
        sentiment_score = self._calc_sentiment_score(bull_result)
        macro_score = self._calc_macro_score(bull_result)
        
        # 3. 动态调整权重（基于历史准确性）
        adjusted_weights = self._adjust_weights()
        
        # 4. 加权聚合
        composite_score = (
            technical_score * adjusted_weights.technical +
            capital_score * adjusted_weights.capital +
            sentiment_score * adjusted_weights.sentiment +
            macro_score * adjusted_weights.macro
        )
        
        # 5. 计算牛市概率（0-100%）
        bull_probability = max(0, min(100, 50 + composite_score))
        
        # 6. 确定强度等级和得分
        strength_level, strength_score = self._determine_strength(composite_score, bull_result)
        
        # 7. 计算置信度
        confidence = self._calculate_confidence(
            technical_score, capital_score, sentiment_score, macro_score
        )
        
        # 8. 生成建议
        position_suggestion = self._get_position_suggestion(strength_score)
        strategy_suggestion = self._get_strategy_suggestion(strength_level, strength_score)
        
        signal = AggregatedSignal(
            bull_probability=bull_probability,
            strength_level=strength_level,
            strength_score=strength_score,
            confidence=confidence,
            technical_score=technical_score,
            capital_score=capital_score,
            sentiment_score=sentiment_score,
            macro_score=macro_score,
            position_suggestion=position_suggestion,
            strategy_suggestion=strategy_suggestion,
        )
        
        if self.verbose:
            print(f"\n✅ 信号聚合结果 ({date})")
            print(f"  牛市概率: {bull_probability:.1f}%")
            print(f"  强度等级: {strength_level}")
            print(f"  强度得分: {strength_score:.1f}/100")
            print(f"  置信度: {confidence:.2f}")
            print(f"  分维度得分:")
            print(f"    技术: {technical_score:.1f} (权重: {adjusted_weights.technical:.2f})")
            print(f"    资金: {capital_score:.1f} (权重: {adjusted_weights.capital:.2f})")
            print(f"    情绪: {sentiment_score:.1f} (权重: {adjusted_weights.sentiment:.2f})")
            print(f"    宏观: {macro_score:.1f} (权重: {adjusted_weights.macro:.2f})")
            print(f"  仓位建议: {position_suggestion*100:.0f}%")
            print(f"  策略建议: {strategy_suggestion}")
        
        return signal
    
    def _calc_technical_score(self, bull_result: BullMarketResult) -> float:
        """计算技术指标得分（-50到+50）"""
        if not bull_result.is_bull:
            return -20.0
        
        indicators = bull_result.indicators
        score = 0.0
        
        # 趋势（20分）
        if indicators.index_price > indicators.index_ma20 > indicators.index_ma60:
            score += 20.0
        elif indicators.index_price > indicators.index_ma20:
            score += 10.0
        else:
            score -= 10.0
        
        # RSI（10分）
        if indicators.rsi > 60:
            score += 10.0
        elif indicators.rsi > 50:
            score += 5.0
        else:
            score -= 5.0
        
        # MACD（10分）
        if indicators.macd_hist > 0:
            score += 10.0
        else:
            score -= 5.0
        
        # 成交量（10分）
        if indicators.volume_ratio > 1.3:
            score += 10.0
        elif indicators.volume_ratio > 1.0:
            score += 5.0
        else:
            score -= 5.0
        
        return np.clip(score, -50, 50)
    
    def _calc_capital_score(self, bull_result: BullMarketResult) -> float:
        """计算资金面得分（-50到+50）"""
        if not bull_result.is_bull:
            return -20.0
        
        indicators = bull_result.indicators
        score = 0.0
        
        # 融资余额增长（15分）
        if indicators.margin_balance_growth > 5.0:
            score += 15.0
        elif indicators.margin_balance_growth > 0:
            score += 8.0
        else:
            score -= 5.0
        
        # 成交量趋势（15分）
        if indicators.volume_trend > 10.0:
            score += 15.0
        elif indicators.volume_trend > 0:
            score += 8.0
        else:
            score -= 5.0
        
        # 涨跌比（20分）
        if indicators.advance_decline_ratio > 0.7:
            score += 20.0
        elif indicators.advance_decline_ratio > 0.6:
            score += 10.0
        else:
            score -= 5.0
        
        return np.clip(score, -50, 50)
    
    def _calc_sentiment_score(self, bull_result: BullMarketResult) -> float:
        """计算情绪面得分（-50到+50）"""
        if not bull_result.is_bull:
            return -20.0
        
        indicators = bull_result.indicators
        score = 0.0
        
        # 换手率（15分）
        if indicators.turnover_rate > 3.0:
            score += 15.0
        elif indicators.turnover_rate > 2.0:
            score += 8.0
        else:
            score -= 5.0
        
        # 涨停数量（20分）
        if indicators.limit_up_count > 50:
            score += 20.0
        elif indicators.limit_up_count > 30:
            score += 10.0
        else:
            score -= 5.0
        
        # 板块轮动（15分）
        if indicators.sector_rotation_score > 70:
            score += 15.0
        elif indicators.sector_rotation_score > 50:
            score += 8.0
        else:
            score -= 5.0
        
        return np.clip(score, -50, 50)
    
    def _calc_macro_score(self, bull_result: BullMarketResult) -> float:
        """计算宏观面得分（-50到+50，简化版）"""
        # 基于base_score估算
        base_score = bull_result.base_score
        if base_score > 60:
            return 30.0
        elif base_score > 40:
            return 15.0
        else:
            return -10.0
    
    def _adjust_weights(self) -> SignalWeight:
        """动态调整权重（基于历史准确性）"""
        # 简化：使用固定权重，未来可以根据历史准确性调整
        weights = SignalWeight()
        weights.normalize()
        return weights
    
    def _determine_strength(self, composite_score: float, bull_result: BullMarketResult) -> Tuple[str, float]:
        """确定强度等级和得分"""
        strength_score = bull_result.strength_score
        strength = bull_result.strength.value if isinstance(bull_result.strength, type) else str(bull_result.strength)
        return strength, strength_score
    
    def _calculate_confidence(self, tech: float, capital: float, sentiment: float, macro: float) -> float:
        """计算置信度（基于信号一致性）"""
        scores = [tech, capital, sentiment, macro]
        # 信号一致性：标准差越小，置信度越高
        std = np.std(scores)
        confidence = 1.0 - (std / 100.0)
        return np.clip(confidence, 0.0, 1.0)
    
    def _get_position_suggestion(self, strength_score: float) -> float:
        """获取仓位建议（0-1）"""
        if strength_score > 80:
            return 0.9
        elif strength_score > 60:
            return 0.7
        elif strength_score > 40:
            return 0.5
        else:
            return 0.3
    
    def _get_strategy_suggestion(self, strength_level: str, strength_score: float) -> str:
        """获取策略建议"""
        if strength_level == 'BULL_STRONG':
            return "激进做多：主线赛道龙头，高成长科技股"
        elif strength_level == 'BULL_NORMAL':
            return "积极做多：优质成长股，适度分散"
        elif strength_level == 'BULL_LATE':
            return "谨慎做多：逐步减仓，锁定利润"
        elif strength_level == 'BULL_PULLBACK':
            return "逢低布局：回调买入机会"
        else:
            return "观望为主：等待信号明确"


def main():
    """主函数：示例用法"""
    aggregator = BullMarketSignalAggregator(verbose=True)
    signal = aggregator.aggregate()
    print("\n聚合信号:")
    print(signal.to_dict())


if __name__ == '__main__':
    main()
