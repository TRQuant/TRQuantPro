"""
多模型融合机制
==============

实现多种信号融合策略：
1. 加权平均融合
2. 投票机制融合
3. 信号一致性检验

用于提高评估结果的准确性和稳定性。
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from .market_environment_evaluator import EvaluationResult

logger = logging.getLogger(__name__)


class FusionMethod(Enum):
    """融合方法"""

    WEIGHTED_AVERAGE = "weighted_average"  # 加权平均
    VOTING = "voting"  # 投票机制
    CONSENSUS = "consensus"  # 一致性融合


@dataclass
class ModelWeight:
    """模型权重配置"""

    trend_analyzer: float = 0.35  # TrendAnalyzer权重
    regime_detector: float = 0.30  # MarketRegimeDetector权重
    ibd_analyzer: float = 0.20  # IBDStyleAnalyzer权重
    hmm_classifier: float = 0.15  # HMM/Classifier权重

    def normalize(self):
        """归一化权重"""
        total = (
            self.trend_analyzer
            + self.regime_detector
            + self.ibd_analyzer
            + self.hmm_classifier
        )
        if total > 0:
            self.trend_analyzer /= total
            self.regime_detector /= total
            self.ibd_analyzer /= total
            self.hmm_classifier /= total


@dataclass
class FusionResult:
    """融合结果"""

    fused_trend_score: float  # 融合后的趋势得分
    fused_market_regime: str  # 融合后的市场环境
    confidence: float  # 融合置信度 (0-1)
    consistency: float  # 信号一致性 (0-1)
    method: str  # 使用的融合方法
    details: Dict[str, Any] = None  # 详细信息


class SignalFusion:
    """
    信号融合器

    提供多种融合策略，整合多个模型的输出。
    """

    def __init__(self, weights: Optional[ModelWeight] = None):
        """
        初始化

        Args:
            weights: 模型权重配置（可选）
        """
        self.weights = weights or ModelWeight()
        self.weights.normalize()

    def fuse(
        self, eval_result: EvaluationResult, method: FusionMethod = FusionMethod.WEIGHTED_AVERAGE
    ) -> FusionResult:
        """
        融合多个模型的信号

        Args:
            eval_result: 评估结果
            method: 融合方法

        Returns:
            FusionResult: 融合结果
        """
        if method == FusionMethod.WEIGHTED_AVERAGE:
            return self._weighted_average_fusion(eval_result)
        elif method == FusionMethod.VOTING:
            return self._voting_fusion(eval_result)
        elif method == FusionMethod.CONSENSUS:
            return self._consensus_fusion(eval_result)
        else:
            raise ValueError(f"Unknown fusion method: {method}")

    def _weighted_average_fusion(self, eval_result: EvaluationResult) -> FusionResult:
        """
        加权平均融合

        基于模型权重对各个模型的输出进行加权平均。
        """
        scores = []
        regimes = []
        weights_list = []

        # 收集TrendAnalyzer的信号
        if eval_result.trend_result:
            score = eval_result.trend_score
            scores.append(score)
            # 根据得分推断市场环境
            if score > 0.5:
                regimes.append("bull")
            elif score < -0.5:
                regimes.append("bear")
            else:
                regimes.append("volatile")
            weights_list.append(self.weights.trend_analyzer)

        # 收集MarketRegimeDetector的信号
        if eval_result.regime_result:
            # 将regime转换为数值
            regime_map = {
                "bull": 0.7,
                "bear": -0.7,
                "volatile": 0.0,
                "recovery": 0.3,
                "distribution": -0.3,
            }
            regime_val = regime_map.get(eval_result.market_regime.lower(), 0.0)
            scores.append(regime_val)
            regimes.append(eval_result.market_regime)
            weights_list.append(self.weights.regime_detector)

        # 收集IBDStyleAnalyzer的信号（主要影响反转信号）
        if eval_result.ibd_result:
            reversal = eval_result.reversal_signal
            # 反转信号可以作为趋势调整因子
            scores.append(reversal * 0.5)  # 降低权重
            weights_list.append(self.weights.ibd_analyzer)
            # IBD主要识别反转，不直接贡献regime

        # 收集HMM/Classifier的信号
        if eval_result.hmm_result:
            state_map = {"牛市": 0.6, "熊市": -0.6, "震荡": 0.0}
            state_val = state_map.get(eval_result.hmm_result.current_state.value, 0.0)
            scores.append(state_val)
            weights_list.append(self.weights.hmm_classifier)
            if eval_result.hmm_result.current_state.value == "牛市":
                regimes.append("bull")
            elif eval_result.hmm_result.current_state.value == "熊市":
                regimes.append("bear")

        # 计算加权平均得分
        if len(scores) > 0 and sum(weights_list) > 0:
            # 归一化权重
            total_weight = sum(weights_list)
            normalized_weights = [w / total_weight for w in weights_list]

            fused_score = sum(s * w for s, w in zip(scores, normalized_weights))
            fused_score = max(-1.0, min(1.0, fused_score))  # 限制在[-1, 1]
        else:
            fused_score = eval_result.trend_score  # 回退到原始得分

        # 计算市场环境（投票机制）
        if len(regimes) > 0:
            regime_counts = {}
            for r in regimes:
                regime_counts[r] = regime_counts.get(r, 0) + 1
            fused_regime = max(regime_counts, key=regime_counts.get)
        else:
            fused_regime = eval_result.market_regime

        # 计算一致性
        consistency = self._calculate_consistency(eval_result)

        # 计算置信度
        confidence = min(1.0, len([s for s in scores if s != 0]) / 4.0)

        return FusionResult(
            fused_trend_score=fused_score,
            fused_market_regime=fused_regime,
            confidence=confidence,
            consistency=consistency,
            method=FusionMethod.WEIGHTED_AVERAGE.value,
            details={
                "component_scores": scores,
                "component_weights": weights_list,
                "regime_votes": regimes,
            },
        )

    def _voting_fusion(self, eval_result: EvaluationResult) -> FusionResult:
        """
        投票机制融合

        各个模型投票决定最终结果。
        """
        votes = []
        scores = []

        # TrendAnalyzer投票
        if eval_result.trend_result:
            score = eval_result.trend_score
            scores.append(score)
            if score > 0.3:
                votes.append("bull")
            elif score < -0.3:
                votes.append("bear")
            else:
                votes.append("volatile")

        # MarketRegimeDetector投票
        if eval_result.regime_result:
            votes.append(eval_result.market_regime)

        # HMM投票
        if eval_result.hmm_result:
            state = eval_result.hmm_result.current_state.value
            if state == "牛市":
                votes.append("bull")
            elif state == "熊市":
                votes.append("bear")
            else:
                votes.append("volatile")

        # 统计投票
        if len(votes) > 0:
            vote_counts = {}
            for v in votes:
                vote_counts[v] = vote_counts.get(v, 0) + 1
            fused_regime = max(vote_counts, key=vote_counts.get)
            consistency = max(vote_counts.values()) / len(votes)
        else:
            fused_regime = eval_result.market_regime
            consistency = 0.5

        # 得分取平均
        if len(scores) > 0:
            fused_score = sum(scores) / len(scores)
        else:
            fused_score = eval_result.trend_score

        return FusionResult(
            fused_trend_score=fused_score,
            fused_market_regime=fused_regime,
            confidence=consistency,
            consistency=consistency,
            method=FusionMethod.VOTING.value,
            details={"votes": votes, "vote_counts": vote_counts if len(votes) > 0 else {}},
        )

    def _consensus_fusion(self, eval_result: EvaluationResult) -> FusionResult:
        """
        一致性融合

        只在多个模型达成一致时才输出信号，否则输出中性信号。
        """
        # 先计算一致性
        consistency = self._calculate_consistency(eval_result)

        # 如果一致性高，使用加权平均
        if consistency > 0.6:
            return self._weighted_average_fusion(eval_result)
        else:
            # 一致性低，输出中性信号
            return FusionResult(
                fused_trend_score=0.0,
                fused_market_regime="volatile",
                confidence=1.0 - consistency,  # 一致性低时置信度也低
                consistency=consistency,
                method=FusionMethod.CONSENSUS.value,
                details={"reason": "low_consistency"},
            )

    def _calculate_consistency(self, eval_result: EvaluationResult) -> float:
        """
        计算信号一致性

        Returns:
            float: 一致性得分 (0-1)，1表示完全一致
        """
        signals = []

        # 收集各模型的趋势方向信号
        if eval_result.trend_result:
            signals.append(1 if eval_result.trend_score > 0 else -1)

        if eval_result.regime_result:
            regime_map = {"bull": 1, "bear": -1, "volatile": 0, "recovery": 1, "distribution": -1}
            signals.append(regime_map.get(eval_result.market_regime.lower(), 0))

        if eval_result.hmm_result:
            state_map = {"牛市": 1, "熊市": -1, "震荡": 0}
            signals.append(state_map.get(eval_result.hmm_result.current_state.value, 0))

        # 计算一致性：信号相同越多，一致性越高
        if len(signals) < 2:
            return 0.5  # 信号不足

        # 计算信号的标准差（归一化）
        signal_std = abs(sum(signals) / len(signals))  # 平均信号的绝对值
        consistency = signal_std  # 越接近1或-1，一致性越高

        return max(0.0, min(1.0, consistency))


def get_signal_fusion(weights: Optional[ModelWeight] = None) -> SignalFusion:
    """
    获取信号融合器实例

    Args:
        weights: 模型权重配置

    Returns:
        SignalFusion实例
    """
    return SignalFusion(weights=weights)
