"""
动态参数接口体系
================

实现8个核心动态参数接口，供策略调用：

1. trend_score() - 趋势得分 (-1.0 ~ 1.0)
2. market_regime() - 市场阶段（枚举值）
3. reversal_signal() - 反转信号强度 (-1.0 ~ 1.0)
4. suggested_position_ratio() - 建议仓位比例 (0.0 ~ 1.0)
5. allocation_style_shift() - 风格轮动建议（枚举值）
6. risk_exposure_score() - 风险暴露得分 (0 ~ 100)
7. volatility_regime() - 波动率环境（枚举值）
8. trade_frequency_suggestion() - 交易频率建议（枚举值）

参考：A股市场趋势环境判别与预测方法研究.pdf
"""

import logging
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Dict, Optional, Any
from enum import Enum

from .market_environment_evaluator import (
    MarketEnvironmentEvaluator,
    get_market_environment_evaluator,
    EvaluationResult,
)

logger = logging.getLogger(__name__)


class MarketRegimeType(Enum):
    """市场阶段类型"""

    BULL = "bull"  # 牛市
    BEAR = "bear"  # 熊市
    VOLATILE = "volatile"  # 震荡市
    RECOVERY = "recovery"  # 复苏期（熊转牛）
    DISTRIBUTION = "distribution"  # 派发期（牛转熊）


class AllocationStyle(Enum):
    """配置风格"""

    GROWTH = "growth"  # 成长风格
    VALUE = "value"  # 价值风格
    BALANCED = "balanced"  # 平衡风格
    DEFENSIVE = "defensive"  # 防御风格


class VolatilityRegime(Enum):
    """波动率环境"""

    LOW = "low"  # 低波动
    MEDIUM = "medium"  # 中等波动
    HIGH = "high"  # 高波动
    EXTREME = "extreme"  # 极端波动


class TradeFrequency(Enum):
    """交易频率建议"""

    INTRADAY = "intraday"  # 日内
    DAILY = "daily"  # 日频
    WEEKLY = "weekly"  # 周频
    MONTHLY = "monthly"  # 月频


@dataclass
class DynamicSignals:
    """动态信号集合"""

    # 核心信号
    trend_score: float  # -1.0 ~ 1.0
    market_regime: str  # 市场阶段
    reversal_signal: float  # -1.0 ~ 1.0
    suggested_position_ratio: float  # 0.0 ~ 1.0
    allocation_style_shift: str  # 风格建议
    risk_exposure_score: float  # 0 ~ 100
    volatility_regime: str  # 波动率环境
    trade_frequency_suggestion: str  # 交易频率建议

    # 元数据
    timestamp: datetime
    index_code: str
    evaluation_date: str

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "trend_score": self.trend_score,
            "market_regime": self.market_regime,
            "reversal_signal": self.reversal_signal,
            "suggested_position_ratio": self.suggested_position_ratio,
            "allocation_style_shift": self.allocation_style_shift,
            "risk_exposure_score": self.risk_exposure_score,
            "volatility_regime": self.volatility_regime,
            "trade_frequency_suggestion": self.trade_frequency_suggestion,
            "timestamp": self.timestamp.isoformat(),
            "index_code": self.index_code,
            "evaluation_date": self.evaluation_date,
        }


class DynamicSignalProvider:
    """
    动态参数接口提供者

    封装评估引擎，提供8个核心接口。
    """

    def __init__(self, evaluator: Optional[MarketEnvironmentEvaluator] = None):
        """
        初始化

        Args:
            evaluator: MarketEnvironmentEvaluator实例（可选）
        """
        self.evaluator = evaluator or get_market_environment_evaluator()
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = timedelta(hours=1)  # 缓存1小时

    def get_all_signals(
        self, index_code: str = "000001.XSHG", date: Optional[str] = None
    ) -> DynamicSignals:
        """
        获取所有动态信号

        Args:
            index_code: 指数代码
            date: 分析日期

        Returns:
            DynamicSignals: 所有信号的集合
        """
        # 检查缓存
        cache_key = f"{index_code}_{date or 'latest'}"
        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if datetime.now() - cached_time < self._cache_ttl:
                return cached_data

        # 执行评估
        eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        # 提取所有信号
        signals = DynamicSignals(
            trend_score=self.trend_score(index_code=index_code, date=date, eval_result=eval_result),
            market_regime=self.market_regime(index_code=index_code, date=date, eval_result=eval_result),
            reversal_signal=self.reversal_signal(index_code=index_code, date=date, eval_result=eval_result),
            suggested_position_ratio=self.suggested_position_ratio(
                index_code=index_code, date=date, eval_result=eval_result
            ),
            allocation_style_shift=self.allocation_style_shift(
                index_code=index_code, date=date, eval_result=eval_result
            ),
            risk_exposure_score=self.risk_exposure_score(
                index_code=index_code, date=date, eval_result=eval_result
            ),
            volatility_regime=self.volatility_regime(
                index_code=index_code, date=date, eval_result=eval_result
            ),
            trade_frequency_suggestion=self.trade_frequency_suggestion(
                index_code=index_code, date=date, eval_result=eval_result
            ),
            timestamp=datetime.now(),
            index_code=index_code,
            evaluation_date=eval_result.evaluation_date,
        )

        # 更新缓存
        self._cache[cache_key] = (signals, datetime.now())

        return signals

    def trend_score(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> float:
        """
        趋势得分

        取值范围: -1.0 ~ 1.0
        正值表示上行趋势，负值表示下行趋势，绝对值表示强度。

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选，避免重复计算）

        Returns:
            float: 趋势得分
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        return eval_result.trend_score

    def market_regime(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> str:
        """
        市场阶段

        返回: 'bull', 'bear', 'volatile', 'recovery', 'distribution'

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            str: 市场阶段
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        return eval_result.market_regime

    def reversal_signal(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> float:
        """
        反转信号强度

        取值范围: -1.0 ~ 1.0
        +1表示强烈看涨反转，-1表示强烈看跌反转，0表示无明显反转。

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            float: 反转信号强度
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        return eval_result.reversal_signal

    def suggested_position_ratio(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> float:
        """
        建议仓位比例

        取值范围: 0.0 ~ 1.0
        1.0表示全仓持有风险资产，0.0表示空仓。

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            float: 建议仓位比例
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        # 计算逻辑：trend_score - risk_score归一化
        trend_score = eval_result.trend_score  # -1.0 ~ 1.0
        risk_score_normalized = eval_result.risk_score / 100.0  # 0.0 ~ 1.0

        # 基础仓位：趋势得分映射到0-1
        base_position = (trend_score + 1.0) / 2.0  # -1~1 -> 0~1

        # 风险调整：风险高时降低仓位
        adjusted_position = base_position * (1.0 - risk_score_normalized * 0.5)  # 最多降低50%

        # 确保在合理范围内
        position = max(0.0, min(1.0, adjusted_position))

        return position

    def allocation_style_shift(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> str:
        """
        风格轮动建议

        返回: 'growth', 'value', 'balanced', 'defensive'

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            str: 风格建议
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        trend_score = eval_result.trend_score
        regime = eval_result.market_regime.lower()

        # 基于趋势和市场环境判断风格
        if regime == "bear" or trend_score < -0.5:
            return AllocationStyle.DEFENSIVE.value
        elif regime == "bull" and trend_score > 0.5:
            return AllocationStyle.GROWTH.value
        elif trend_score > 0.2:
            # 上涨趋势，偏好成长
            return AllocationStyle.GROWTH.value
        elif trend_score < -0.2:
            # 下跌趋势，偏好价值
            return AllocationStyle.VALUE.value
        else:
            return AllocationStyle.BALANCED.value

    def risk_exposure_score(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> float:
        """
        风险暴露得分

        取值范围: 0 ~ 100
        分数越高，风险越大。

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            float: 风险得分
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        return eval_result.risk_score

    def volatility_regime(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> str:
        """
        波动率环境

        返回: 'low', 'medium', 'high', 'extreme'

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            str: 波动率环境
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        # 简化实现：基于风险得分判断波动率
        # 后续可以增强：计算ATR、历史波动率分位数等
        risk_score = eval_result.risk_score

        if risk_score >= 80:
            return VolatilityRegime.EXTREME.value
        elif risk_score >= 60:
            return VolatilityRegime.HIGH.value
        elif risk_score >= 40:
            return VolatilityRegime.MEDIUM.value
        else:
            return VolatilityRegime.LOW.value

    def trade_frequency_suggestion(
        self,
        index_code: str = "000001.XSHG",
        date: Optional[str] = None,
        eval_result: Optional[EvaluationResult] = None,
    ) -> str:
        """
        交易频率建议

        返回: 'intraday', 'daily', 'weekly', 'monthly'

        Args:
            index_code: 指数代码
            date: 分析日期
            eval_result: 评估结果（可选）

        Returns:
            str: 交易频率建议
        """
        if eval_result is None:
            eval_result = self.evaluator.evaluate(index_code=index_code, date=date)

        trend_score = abs(eval_result.trend_score)  # 趋势强度
        volatility = self.volatility_regime(index_code=index_code, date=date, eval_result=eval_result)

        # 趋势明确且波动率低：降低频率（持仓坐享趋势）
        if trend_score > 0.7 and volatility == "low":
            return TradeFrequency.WEEKLY.value
        # 趋势不明确且波动率高：提高频率（快进快出）
        elif trend_score < 0.3 and volatility in ["high", "extreme"]:
            return TradeFrequency.DAILY.value
        # 其他情况：日频或周频
        elif trend_score > 0.5:
            return TradeFrequency.WEEKLY.value
        else:
            return TradeFrequency.DAILY.value


# 全局实例
_provider: Optional[DynamicSignalProvider] = None


def get_dynamic_signal_provider() -> DynamicSignalProvider:
    """
    获取动态信号提供者实例（单例）

    Returns:
        DynamicSignalProvider实例
    """
    global _provider
    if _provider is None:
        _provider = DynamicSignalProvider()
    return _provider


# 便捷函数接口
def trend_score(index_code: str = "000001.XSHG", date: Optional[str] = None) -> float:
    """趋势得分接口"""
    provider = get_dynamic_signal_provider()
    return provider.trend_score(index_code=index_code, date=date)


def market_regime(index_code: str = "000001.XSHG", date: Optional[str] = None) -> str:
    """市场阶段接口"""
    provider = get_dynamic_signal_provider()
    return provider.market_regime(index_code=index_code, date=date)


def reversal_signal(index_code: str = "000001.XSHG", date: Optional[str] = None) -> float:
    """反转信号接口"""
    provider = get_dynamic_signal_provider()
    return provider.reversal_signal(index_code=index_code, date=date)


def suggested_position_ratio(
    index_code: str = "000001.XSHG", date: Optional[str] = None
) -> float:
    """建议仓位比例接口"""
    provider = get_dynamic_signal_provider()
    return provider.suggested_position_ratio(index_code=index_code, date=date)


def allocation_style_shift(index_code: str = "000001.XSHG", date: Optional[str] = None) -> str:
    """风格轮动建议接口"""
    provider = get_dynamic_signal_provider()
    return provider.allocation_style_shift(index_code=index_code, date=date)


def risk_exposure_score(index_code: str = "000001.XSHG", date: Optional[str] = None) -> float:
    """风险暴露得分接口"""
    provider = get_dynamic_signal_provider()
    return provider.risk_exposure_score(index_code=index_code, date=date)


def volatility_regime(index_code: str = "000001.XSHG", date: Optional[str] = None) -> str:
    """波动率环境接口"""
    provider = get_dynamic_signal_provider()
    return provider.volatility_regime(index_code=index_code, date=date)


def trade_frequency_suggestion(
    index_code: str = "000001.XSHG", date: Optional[str] = None
) -> str:
    """交易频率建议接口"""
    provider = get_dynamic_signal_provider()
    return provider.trade_frequency_suggestion(index_code=index_code, date=date)
