"""
市场趋势环境综合评估引擎
=======================

整合多个分析模块，提供统一的市场环境评估接口。

模块整合：
1. TrendAnalyzer - 多周期趋势分析
2. MarketRegimeDetector - 市场环境检测
3. IBDStyleAnalyzer - IBD反转信号识别
4. TrendClassifier (HMM) - 机器学习趋势分类

提供8个动态参数接口的基础数据。
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from datetime import date as date_module
from typing import Dict, Optional, Any, List
from enum import Enum

from .trend_analyzer import TrendAnalyzer, MarketTrendResult
from .market_regime.market_regime_detector import (
    MarketRegimeDetector,
    get_market_regime_detector,
    RegimeResult,
    MarketRegime,
)
from .ibd_style_analyzer import IBDStyleAnalyzer, IBDAnalysisResult, MarketStatus
from .trend_ml import SimpleHMM, TrendClassifier, HMMResult

logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """市场环境评估结果"""

    # 分析时间
    evaluation_date: str
    timestamp: datetime = field(default_factory=datetime.now)

    # 各模块原始结果
    trend_result: Optional[MarketTrendResult] = None
    regime_result: Optional[RegimeResult] = None
    ibd_result: Optional[IBDAnalysisResult] = None
    hmm_result: Optional[HMMResult] = None
    classifier_result: Optional[Dict] = None

    # 综合评估指标
    trend_score: float = 0.0  # -1.0 ~ 1.0
    market_regime: str = "unknown"  # bull/bear/volatile/recovery/distribution
    reversal_signal: float = 0.0  # -1.0 ~ 1.0
    risk_score: float = 0.0  # 0 ~ 100

    # 元数据
    index_code: str = "000001.XSHG"
    success: bool = True
    error_message: str = ""
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            "evaluation_date": self.evaluation_date,
            "timestamp": self.timestamp.isoformat(),
            "index_code": self.index_code,
            "success": self.success,
            "error_message": self.error_message,
            "warnings": self.warnings,
            # 综合指标
            "trend_score": self.trend_score,
            "market_regime": self.market_regime,
            "reversal_signal": self.reversal_signal,
            "risk_score": self.risk_score,
            # 原始结果（简化）
            "trend_result": self.trend_result.to_dict() if self.trend_result else None,
            "regime_result": self.regime_result.to_dict() if self.regime_result else None,
            "ibd_result": self._ibd_to_dict() if self.ibd_result else None,
            "hmm_result": self._hmm_to_dict() if self.hmm_result else None,
            "classifier_result": self.classifier_result,
        }
        return result

    def _ibd_to_dict(self) -> Dict[str, Any]:
        """IBD结果转字典"""
        if not self.ibd_result:
            return None
        return {
            "market_status": self.ibd_result.market_status.value,
            "distribution_count": self.ibd_result.distribution_count,
            "follow_through_days": len(self.ibd_result.follow_through_days),
            "recommendation": self.ibd_result.recommendation,
        }

    def _hmm_to_dict(self) -> Dict[str, Any]:
        """HMM结果转字典"""
        if not self.hmm_result:
            return None
        return {
            "current_state": self.hmm_result.current_state.value,
            "state_probability": self.hmm_result.state_probability,
            "confidence": self.hmm_result.confidence,
        }


class MarketEnvironmentEvaluator:
    """
    市场趋势环境综合评估引擎

    整合多个分析模块，提供统一的评估接口。
    """

    def __init__(
        self,
        jq_client=None,
        trend_analyzer: Optional[TrendAnalyzer] = None,
        regime_detector: Optional[MarketRegimeDetector] = None,
        ibd_analyzer: Optional[IBDStyleAnalyzer] = None,
    ):
        """
        初始化评估引擎

        Args:
            jq_client: JQData客户端（可选）
            trend_analyzer: TrendAnalyzer实例（可选，会自动创建）
            regime_detector: MarketRegimeDetector实例（可选，会自动创建）
            ibd_analyzer: IBDStyleAnalyzer实例（可选，会自动创建）
        """
        self.jq_client = jq_client

        # 初始化各分析模块
        if trend_analyzer:
            self.trend_analyzer = trend_analyzer
        else:
            self.trend_analyzer = TrendAnalyzer(jq_client=jq_client)

        if regime_detector:
            self.regime_detector = regime_detector
        else:
            self.regime_detector = get_market_regime_detector()

        if ibd_analyzer:
            self.ibd_analyzer = ibd_analyzer
        else:
            self.ibd_analyzer = IBDStyleAnalyzer()

        # 初始化HMM和分类器
        self.hmm_model = SimpleHMM()
        self.trend_classifier = TrendClassifier()

        logger.info("✅ MarketEnvironmentEvaluator 初始化完成")

    def evaluate(
        self, index_code: str = "000001.XSHG", date: Optional[str] = None
    ) -> EvaluationResult:
        """
        执行综合评估

        Args:
            index_code: 指数代码（默认上证指数）
            date: 分析日期（格式：YYYY-MM-DD），None表示使用最新日期

        Returns:
            EvaluationResult: 评估结果
        """
        eval_date = date if date else date_module.today().strftime("%Y-%m-%d")
        logger.info(f"🔍 开始市场环境综合评估: {index_code}, 日期: {eval_date}")

        result = EvaluationResult(
            evaluation_date=eval_date,
            index_code=index_code,
            success=True,
        )

        try:
            # 1. 趋势分析（TrendAnalyzer）
            try:
                result.trend_result = self.trend_analyzer.analyze_market(
                    index_code=index_code, date=date
                )
                if result.trend_result:
                    # 将综合得分归一化到 -1.0 ~ 1.0
                    result.trend_score = max(
                        -1.0, min(1.0, result.trend_result.composite_score / 100.0)
                    )
                else:
                    result.warnings.append("趋势分析返回空结果")
            except Exception as e:
                logger.warning(f"趋势分析失败: {e}")
                result.warnings.append(f"趋势分析失败: {str(e)}")

            # 2. 市场环境检测（MarketRegimeDetector）
            try:
                result.regime_result = self.regime_detector.detect_regime(date=date)
                if result.regime_result:
                    result.market_regime = result.regime_result.regime.value.lower()
                else:
                    result.warnings.append("市场环境检测返回空结果")
            except Exception as e:
                logger.warning(f"市场环境检测失败: {e}")
                result.warnings.append(f"市场环境检测失败: {str(e)}")

            # 3. IBD反转信号分析（IBDStyleAnalyzer）
            try:
                result.ibd_result = self.ibd_analyzer.analyze(
                    index_code=index_code, lookback_days=60
                )
                if result.ibd_result:
                    # 计算反转信号强度
                    result.reversal_signal = self._calculate_reversal_signal(
                        result.ibd_result
                    )
                else:
                    result.warnings.append("IBD分析返回空结果")
            except Exception as e:
                logger.warning(f"IBD分析失败: {e}")
                result.warnings.append(f"IBD分析失败: {str(e)}")

            # 4. HMM状态识别
            try:
                if result.trend_result and hasattr(result.trend_result, "analysis_date"):
                    # 获取价格数据用于HMM分析
                    df = self._get_price_data_for_hmm(index_code, date)
                    if df is not None and len(df) >= 20:
                        result.hmm_result = self.hmm_model.analyze(df)
                    else:
                        result.warnings.append("HMM分析数据不足")
            except Exception as e:
                logger.warning(f"HMM分析失败: {e}")
                result.warnings.append(f"HMM分析失败: {str(e)}")

            # 5. 趋势分类器
            try:
                df = self._get_price_data_for_hmm(index_code, date)
                if df is not None and len(df) >= 50:
                    result.classifier_result = self.trend_classifier.classify(df)
                else:
                    result.warnings.append("趋势分类器数据不足")
            except Exception as e:
                logger.warning(f"趋势分类器失败: {e}")
                result.warnings.append(f"趋势分类器失败: {str(e)}")

            # 6. 计算风险得分（简化版本，后续会增强）
            result.risk_score = self._calculate_risk_score(result)

            logger.info(f"✅ 市场环境评估完成: trend_score={result.trend_score:.3f}, "
                       f"regime={result.market_regime}, reversal={result.reversal_signal:.3f}")

        except Exception as e:
            logger.error(f"❌ 市场环境评估失败: {e}", exc_info=True)
            result.success = False
            result.error_message = str(e)

        return result

    def get_all_signals(self, index_code: str = "000001.XSHG", date: Optional[str] = None) -> Dict[str, Any]:
        """
        获取所有信号（简化接口）

        Args:
            index_code: 指数代码
            date: 分析日期

        Returns:
            包含所有信号的字典
        """
        result = self.evaluate(index_code=index_code, date=date)
        return result.to_dict()

    def _calculate_reversal_signal(self, ibd_result: IBDAnalysisResult) -> float:
        """
        计算反转信号强度 (-1.0 ~ 1.0)

        Args:
            ibd_result: IBD分析结果

        Returns:
            反转信号强度
        """
        signal = 0.0

        # 跟踪日：正向信号
        if len(ibd_result.follow_through_days) > 0:
            # 最近跟踪日的强度
            latest_ftd = ibd_result.follow_through_days[-1]
            if latest_ftd.is_valid:
                # 基于涨幅和成交量计算信号强度
                gain_score = min(1.0, latest_ftd.gain_pct / 2.0)  # 涨幅2%以上为强信号
                volume_score = min(1.0, latest_ftd.volume_ratio / 1.5)  # 成交量1.5倍以上为强信号
                signal = max(signal, (gain_score + volume_score) / 2.0)

        # 分布日：负向信号
        if ibd_result.distribution_count > 0:
            # 分布日越多，负向信号越强
            dist_score = min(1.0, ibd_result.distribution_count / 5.0)  # 5个分布日为强信号
            signal = signal - dist_score

        # 市场状态影响
        if ibd_result.market_status == MarketStatus.CONFIRMED_UPTREND:
            signal = max(signal, 0.5)  # 确认上涨时增强正向信号
        elif ibd_result.market_status == MarketStatus.MARKET_IN_CORRECTION:
            signal = min(signal, -0.5)  # 市场调整时增强负向信号

        return max(-1.0, min(1.0, signal))

    def _calculate_risk_score(self, result: EvaluationResult) -> float:
        """
        计算风险得分 (0 ~ 100)

        简化版本，后续会增强

        Args:
            result: 评估结果

        Returns:
            风险得分
        """
        risk = 50.0  # 默认中性风险

        # 基于趋势得分：负向趋势增加风险
        if result.trend_score < -0.5:
            risk += 20
        elif result.trend_score < -0.2:
            risk += 10

        # 基于市场环境
        if result.regime_result:
            if result.regime_result.regime == MarketRegime.BEAR:
                risk += 30
            elif result.regime_result.regime == MarketRegime.VOLATILE:
                risk += 15

        # 基于分布日数量
        if result.ibd_result and result.ibd_result.distribution_count >= 3:
            risk += min(20, result.ibd_result.distribution_count * 5)

        return min(100.0, max(0.0, risk))

    def _get_price_data_for_hmm(self, index_code: str, date: Optional[str] = None) -> Optional[Any]:
        """获取价格数据用于HMM和分类器分析"""
        try:
            if self.jq_client:
                # 使用JQData获取数据
                from datetime import timedelta
                end_date = date if date else date_module.today().strftime("%Y-%m-%d")
                start_date = (date_module.today() - timedelta(days=300)).strftime("%Y-%m-%d") if not date else None
                # 这里需要根据实际的jq_client接口调整
                # 暂时返回None，由调用方处理
                return None
            else:
                # 可以尝试从TrendAnalyzer获取数据
                if hasattr(self.trend_analyzer, "_get_price_data"):
                    return self.trend_analyzer._get_price_data(index_code, date, days=300)
        except Exception as e:
            logger.warning(f"获取价格数据失败: {e}")
        return None


def get_market_environment_evaluator(jq_client=None) -> MarketEnvironmentEvaluator:
    """
    获取市场环境评估器实例（单例模式）

    Args:
        jq_client: JQData客户端

    Returns:
        MarketEnvironmentEvaluator实例
    """
    global _evaluator
    if "_evaluator" not in globals():
        _evaluator = None

    if _evaluator is None or (jq_client and _evaluator.jq_client != jq_client):
        _evaluator = MarketEnvironmentEvaluator(jq_client=jq_client)

    return _evaluator
