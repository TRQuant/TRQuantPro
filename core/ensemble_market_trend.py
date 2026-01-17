#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
集成市场趋势分析器
================

多模型投票系统，集成以下模型：
1. HMM模型（Resonance V2）
2. 技术指标模型（TrendAnalyzer）
3. 市场宽度模型（MarketBreadthAnalyzer）
4. 情绪分析模型（JQDataSentimentAnalyzer）
5. 宏观指标模型（可选）

基于各模型的历史准确率动态调整权重，通过加权投票生成最终预测。

Author: TRQuant Team
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

from core.resonance_v2 import ResonanceHMMAnalyzer, MarketState
from core.trend_analyzer import TrendAnalyzer
from core.astock_indicators import MarketBreadthAnalyzer
from core.jqdata_sentiment_analyzer import JQDataSentimentAnalyzer

logger = logging.getLogger(__name__)


class TrendDirection(Enum):
    """趋势方向"""
    BULL = "bull"
    BEAR = "bear"
    SIDEWAYS = "sideways"


@dataclass
class ModelPrediction:
    """单个模型预测结果"""
    model_name: str
    trend: TrendDirection
    confidence: float  # 0-1
    details: Dict = field(default_factory=dict)


@dataclass
class EnsembleResult:
    """集成预测结果"""
    date: str
    index_code: str
    
    # 最终预测
    final_trend: TrendDirection
    final_confidence: float  # 0-1
    
    # 各模型预测
    model_predictions: List[ModelPrediction] = field(default_factory=list)
    
    # 投票统计
    bull_score: float = 0.0
    bear_score: float = 0.0
    sideways_score: float = 0.0
    
    # 一致性指标
    consistency: float = 0.0  # 模型一致性 (0-1)
    agreement_ratio: float = 0.0  # 同意最终预测的模型比例
    
    # 诊断信息
    weights: Dict[str, float] = field(default_factory=dict)
    diagnostics: Dict = field(default_factory=dict)
    
    def summary(self) -> str:
        """生成摘要"""
        return (
            f"【{self.date}】{self.index_code}\n"
            f"最终预测: {self.final_trend.value} (置信度: {self.final_confidence:.1%})\n"
            f"一致性: {self.consistency:.1%}\n"
            f"投票得分: 牛市={self.bull_score:.2f}, 熊市={self.bear_score:.2f}, 震荡={self.sideways_score:.2f}\n"
            f"模型同意率: {self.agreement_ratio:.1%}"
        )


class EnsembleMarketTrendAnalyzer:
    """
    集成市场趋势分析器
    
    使用多模型投票系统，基于历史准确率动态调整权重。
    """
    
    # 默认权重（基于经验，后续会根据验证结果调整）
    DEFAULT_WEIGHTS = {
        'HMM': 0.20,          # HMM准确率约58%，权重较低
        'Technical': 0.25,   # 技术指标通常更稳定
        'Breadth': 0.25,     # 市场宽度在A股很有效
        'Sentiment': 0.15,   # 情绪指标作为辅助
        'Macro': 0.15,       # 宏观指标长期有效（暂未实现）
    }
    
    # 最小置信度阈值
    MIN_CONFIDENCE_THRESHOLD = 0.55  # 只有准确率>=55%的模型才纳入
    
    def __init__(
        self,
        model_weights: Optional[Dict[str, float]] = None,
        min_confidence: float = 0.55
    ):
        """
        初始化集成分析器
        
        Args:
            model_weights: 各模型权重（如果为None，使用默认权重）
            min_confidence: 最小置信度阈值（只有准确率>=此值的模型才纳入）
        """
        self.model_weights = model_weights or self.DEFAULT_WEIGHTS.copy()
        self.min_confidence = min_confidence
        
        # 初始化各模型
        self.hmm_analyzer = ResonanceHMMAnalyzer()
        self.technical_analyzer = TrendAnalyzer()
        self.breadth_analyzer = MarketBreadthAnalyzer()
        self.sentiment_analyzer = JQDataSentimentAnalyzer()
        
        # 模型准确率（从验证结果加载，初始使用默认值）
        self.model_accuracies = {
            'HMM': 0.58,          # 待验证后更新
            'Technical': 0.65,   # 待验证后更新
            'Breadth': 0.60,     # 待验证后更新
            'Sentiment': 0.55,   # 待验证后更新
        }
        
        # 动态调整权重
        self._update_weights()
        
        logger.info(f"集成分析器初始化: 权重={self.model_weights}")
    
    def _update_weights(self):
        """根据模型准确率动态调整权重"""
        # 过滤掉准确率低于阈值的模型
        valid_models = {
            name: acc for name, acc in self.model_accuracies.items()
            if acc >= self.min_confidence
        }
        
        if not valid_models:
            logger.warning("没有模型达到最小置信度阈值，使用默认权重")
            return
        
        # 归一化权重（基于准确率）
        total_accuracy = sum(valid_models.values())
        if total_accuracy > 0:
            for name in self.model_weights:
                if name in valid_models:
                    # 权重 = 准确率 / 总准确率 * 原始权重比例
                    self.model_weights[name] = (
                        valid_models[name] / total_accuracy * 
                        self.DEFAULT_WEIGHTS.get(name, 0.2)
                    )
                else:
                    # 未通过验证的模型权重设为0
                    self.model_weights[name] = 0.0
        
        # 重新归一化
        total_weight = sum(self.model_weights.values())
        if total_weight > 0:
            for name in self.model_weights:
                self.model_weights[name] /= total_weight
        
        logger.info(f"权重已更新: {self.model_weights}")
    
    def update_model_accuracy(self, model_name: str, accuracy: float):
        """
        更新模型准确率（从验证结果加载）
        
        Args:
            model_name: 模型名称
            accuracy: 准确率 (0-1)
        """
        if model_name in self.model_accuracies:
            self.model_accuracies[model_name] = accuracy
            self._update_weights()
            logger.info(f"模型 {model_name} 准确率更新为 {accuracy:.1%}")
    
    def analyze(
        self,
        index_code: str = "000300.XSHG",
        date: Optional[str] = None
    ) -> EnsembleResult:
        """
        集成分析市场趋势
        
        Args:
            index_code: 指数代码
            date: 分析日期（默认最新）
        
        Returns:
            EnsembleResult: 集成预测结果
        """
        if date is None:
            from datetime import date as dt_date
            date = dt_date.today().strftime('%Y-%m-%d')
        
        logger.info(f"开始集成分析: {index_code} @ {date}")
        
        # 1. 各模型独立预测
        predictions = []
        
        # HMM模型
        hmm_pred = self._predict_hmm(index_code, date)
        if hmm_pred:
            predictions.append(hmm_pred)
        
        # 技术指标模型
        tech_pred = self._predict_technical(index_code, date)
        if tech_pred:
            predictions.append(tech_pred)
        
        # 市场宽度模型
        breadth_pred = self._predict_breadth(date)
        if breadth_pred:
            predictions.append(breadth_pred)
        
        # 情绪分析模型
        sentiment_pred = self._predict_sentiment(index_code, date)
        if sentiment_pred:
            predictions.append(sentiment_pred)
        
        if not predictions:
            logger.warning("所有模型预测失败")
            return self._create_empty_result(index_code, date)
        
        # 2. 加权投票
        bull_score = 0.0
        bear_score = 0.0
        sideways_score = 0.0
        
        for pred in predictions:
            weight = self.model_weights.get(pred.model_name, 0.0)
            if weight == 0:
                continue
            
            weighted_confidence = pred.confidence * weight
            
            if pred.trend == TrendDirection.BULL:
                bull_score += weighted_confidence
            elif pred.trend == TrendDirection.BEAR:
                bear_score += weighted_confidence
            else:
                sideways_score += weighted_confidence
        
        # 3. 计算一致性
        consistency = self._calculate_consistency(predictions)
        
        # 4. 确定最终趋势
        scores = {
            TrendDirection.BULL: bull_score,
            TrendDirection.BEAR: bear_score,
            TrendDirection.SIDEWAYS: sideways_score
        }
        
        final_trend = max(scores.items(), key=lambda x: x[1])[0]
        max_score = scores[final_trend]
        total_score = sum(scores.values())
        
        # 最终置信度 = 最大得分 / 总得分 * 一致性
        final_confidence = (max_score / total_score if total_score > 0 else 0.0) * consistency
        
        # 需要明显优势才确定趋势（避免震荡）
        if max_score < total_score * 0.4:  # 如果最大得分<40%，判定为震荡
            final_trend = TrendDirection.SIDEWAYS
            final_confidence = max(0.5, final_confidence)
        
        # 5. 计算同意率
        agreement_ratio = sum(
            1 for p in predictions 
            if p.trend == final_trend
        ) / len(predictions) if predictions else 0.0
        
        # 6. 构建结果
        result = EnsembleResult(
            date=date,
            index_code=index_code,
            final_trend=final_trend,
            final_confidence=final_confidence,
            model_predictions=predictions,
            bull_score=bull_score,
            bear_score=bear_score,
            sideways_score=sideways_score,
            consistency=consistency,
            agreement_ratio=agreement_ratio,
            weights=self.model_weights.copy(),
            diagnostics={
                'total_models': len(predictions),
                'active_models': sum(1 for w in self.model_weights.values() if w > 0),
                'model_accuracies': self.model_accuracies.copy()
            }
        )
        
        logger.info(f"集成分析完成: {final_trend.value} (置信度: {final_confidence:.1%})")
        
        return result
    
    def _predict_hmm(self, index_code: str, date: str) -> Optional[ModelPrediction]:
        """HMM模型预测"""
        try:
            result = self.hmm_analyzer.analyze(index_code, date, lookback_days=400)
            if result is None:
                return None
            
            # 映射HMM状态到趋势
            if result.market_state == MarketState.RISK_ON:
                trend = TrendDirection.BULL
            elif result.market_state == MarketState.RISK_OFF:
                trend = TrendDirection.BEAR
            else:
                trend = TrendDirection.SIDEWAYS
            
            return ModelPrediction(
                model_name='HMM',
                trend=trend,
                confidence=result.state_confidence,
                details={
                    'state': result.state_name,
                    'resonance_score': result.resonance_score
                }
            )
        except Exception as e:
            logger.debug(f"HMM预测失败: {e}")
            return None
    
    def _predict_technical(self, index_code: str, date: str) -> Optional[ModelPrediction]:
        """技术指标模型预测"""
        try:
            result = self.technical_analyzer.analyze_market(index_code, date)
            if result is None:
                return None
            
            # 根据综合得分判断趋势
            composite = result.composite_score
            if composite > 30:
                trend = TrendDirection.BULL
            elif composite < -30:
                trend = TrendDirection.BEAR
            else:
                trend = TrendDirection.SIDEWAYS
            
            confidence = min(abs(composite) / 100.0, 1.0)
            
            return ModelPrediction(
                model_name='Technical',
                trend=trend,
                confidence=confidence,
                details={
                    'composite_score': composite,
                    'short_term': result.short_term.score,
                    'medium_term': result.medium_term.score,
                    'long_term': result.long_term.score
                }
            )
        except Exception as e:
            logger.debug(f"技术指标预测失败: {e}")
            return None
    
    def _predict_breadth(self, date: str) -> Optional[ModelPrediction]:
        """市场宽度模型预测"""
        try:
            result = self.breadth_analyzer.analyze(date)
            if result is None:
                return None
            
            # 根据市场宽度得分判断趋势
            score = result.signal_score
            if score > 20:
                trend = TrendDirection.BULL
            elif score < -20:
                trend = TrendDirection.BEAR
            else:
                trend = TrendDirection.SIDEWAYS
            
            confidence = min(abs(score) / 100.0, 1.0)
            
            return ModelPrediction(
                model_name='Breadth',
                trend=trend,
                confidence=confidence,
                details={
                    'signal_score': score,
                    'limit_up_down_ratio': result.limit_up_down_ratio,
                    'up_down_ratio': result.up_down_ratio,
                    'new_high_low_ratio': result.new_high_low_ratio
                }
            )
        except Exception as e:
            logger.debug(f"市场宽度预测失败: {e}")
            return None
    
    def _predict_sentiment(self, index_code: str, date: str) -> Optional[ModelPrediction]:
        """情绪分析模型预测"""
        try:
            result = self.sentiment_analyzer.analyze(date, index_code)
            if result is None:
                return None
            
            # 根据情绪信号判断趋势（注意：极度贪婪/恐慌时反向）
            signal = result.signal
            if signal == "bullish":
                trend = TrendDirection.BULL
            elif signal == "bearish":
                trend = TrendDirection.BEAR
            else:
                trend = TrendDirection.SIDEWAYS
            
            confidence = min(abs(result.composite_score) / 100.0, 1.0)
            
            return ModelPrediction(
                model_name='Sentiment',
                trend=trend,
                confidence=confidence,
                details={
                    'composite_score': result.composite_score,
                    'sentiment_level': result.sentiment_level.value,
                    'signal': signal
                }
            )
        except Exception as e:
            logger.debug(f"情绪分析预测失败: {e}")
            return None
    
    def _calculate_consistency(self, predictions: List[ModelPrediction]) -> float:
        """计算模型一致性"""
        if not predictions:
            return 0.0
        
        # 统计各趋势的投票数
        trend_counts = {}
        for pred in predictions:
            trend = pred.trend
            trend_counts[trend] = trend_counts.get(trend, 0) + 1
        
        # 一致性 = 最大投票数 / 总模型数
        max_count = max(trend_counts.values()) if trend_counts else 0
        consistency = max_count / len(predictions)
        
        return consistency
    
    def _create_empty_result(self, index_code: str, date: str) -> EnsembleResult:
        """创建空结果"""
        return EnsembleResult(
            date=date,
            index_code=index_code,
            final_trend=TrendDirection.SIDEWAYS,
            final_confidence=0.0
        )


# 便捷函数
def analyze_market_trend(
    index_code: str = "000300.XSHG",
    date: Optional[str] = None,
    model_weights: Optional[Dict[str, float]] = None
) -> EnsembleResult:
    """
    分析市场趋势（便捷函数）
    
    Args:
        index_code: 指数代码
        date: 分析日期
        model_weights: 模型权重（可选）
    
    Returns:
        EnsembleResult: 集成预测结果
    """
    analyzer = EnsembleMarketTrendAnalyzer(model_weights=model_weights)
    return analyzer.analyze(index_code, date)
