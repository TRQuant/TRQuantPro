"""
市场状态预测器 - 短期/中期/长期预测

提供三个周期的市场预测：
- 短期(5-10天): 操作信号
- 中期(20-60天): 波段方向
- 长期(120天+): 趋势判断
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import logging
from datetime import datetime

from core.market_state_lib import (
    MarketState, MarketStateIdentifier, MarketIndicators,
    STATE_DEFINITIONS, identify_market_state
)

logger = logging.getLogger(__name__)


class PredictionDirection(Enum):
    """预测方向"""
    STRONG_UP = "强烈看涨"
    UP = "看涨"
    SLIGHT_UP = "偏多"
    NEUTRAL = "中性"
    SLIGHT_DOWN = "偏空"
    DOWN = "看跌"
    STRONG_DOWN = "强烈看跌"
    
    @property
    def score(self) -> int:
        """方向得分 -3到+3"""
        mapping = {
            PredictionDirection.STRONG_UP: 3,
            PredictionDirection.UP: 2,
            PredictionDirection.SLIGHT_UP: 1,
            PredictionDirection.NEUTRAL: 0,
            PredictionDirection.SLIGHT_DOWN: -1,
            PredictionDirection.DOWN: -2,
            PredictionDirection.STRONG_DOWN: -3
        }
        return mapping.get(self, 0)


@dataclass
class PeriodPrediction:
    """单周期预测"""
    period: str              # short/medium/long
    period_name: str         # 短期/中期/长期
    days: int               # 预测天数
    direction: PredictionDirection
    confidence: float        # 0-100
    expected_return: float   # 预期收益%
    risk_level: str         # low/medium/high
    signal: str             # 操作信号
    key_factors: List[str]  # 关键因素
    
    def to_dict(self) -> dict:
        return {
            'period': self.period,
            'period_name': self.period_name,
            'days': self.days,
            'direction': self.direction.name,
            'direction_name': self.direction.value,
            'direction_score': self.direction.score,
            'confidence': round(self.confidence, 1),
            'expected_return': round(self.expected_return, 2),
            'risk_level': self.risk_level,
            'signal': self.signal,
            'key_factors': self.key_factors
        }


@dataclass
class ComprehensivePrediction:
    """综合预测结果"""
    # 当前状态
    current_state: MarketState
    current_confidence: float
    
    # 三周期预测
    short_term: PeriodPrediction   # 5-10天
    medium_term: PeriodPrediction  # 20-60天
    long_term: PeriodPrediction    # 120天+
    
    # 综合判断
    overall_direction: PredictionDirection
    overall_confidence: float
    overall_signal: str
    
    # 下游参数
    position_suggestion: float     # 建议仓位
    stop_loss: float              # 止损位
    take_profit: float            # 止盈位
    strategy_type: str            # 策略类型
    
    # 元数据
    timestamp: datetime = field(default_factory=datetime.now)
    data_source: str = 'unknown'
    
    def to_dict(self) -> dict:
        return {
            'current_state': {
                'state': self.current_state.name,
                'state_name': self.current_state.value,
                'confidence': round(self.current_confidence, 1)
            },
            'predictions': {
                'short_term': self.short_term.to_dict(),
                'medium_term': self.medium_term.to_dict(),
                'long_term': self.long_term.to_dict()
            },
            'overall': {
                'direction': self.overall_direction.name,
                'direction_name': self.overall_direction.value,
                'confidence': round(self.overall_confidence, 1),
                'signal': self.overall_signal
            },
            'parameters': {
                'position': round(self.position_suggestion, 2),
                'stop_loss': round(self.stop_loss, 3),
                'take_profit': round(self.take_profit, 3),
                'strategy': self.strategy_type
            },
            'metadata': {
                'timestamp': self.timestamp.isoformat(),
                'data_source': self.data_source
            }
        }


class MarketStatePredictor:
    """
    市场状态预测器
    
    基于当前状态和技术指标，预测短期/中期/长期走势
    """
    
    def __init__(self):
        self.identifier = MarketStateIdentifier(use_akshare=False)
    
    def predict(self, 
                df: pd.DataFrame = None,
                symbol: str = '000001.XSHG') -> ComprehensivePrediction:
        """
        综合预测
        
        Args:
            df: OHLCV数据
            symbol: 指数代码
            
        Returns:
            ComprehensivePrediction
        """
        # 获取当前状态
        state_result = self.identifier.identify(df=df, symbol=symbol)
        current_state = state_result.state
        indicators = state_result.indicators
        
        # 三周期预测
        short_pred = self._predict_short_term(indicators, current_state)
        medium_pred = self._predict_medium_term(indicators, current_state)
        long_pred = self._predict_long_term(indicators, current_state)
        
        # 综合判断
        overall_dir, overall_conf = self._combine_predictions(
            short_pred, medium_pred, long_pred
        )
        overall_signal = self._generate_signal(overall_dir, overall_conf)
        
        # 计算下游参数
        position = self._calculate_position(overall_dir, overall_conf, current_state)
        stop_loss, take_profit = self._calculate_stops(current_state, indicators)
        strategy = self._determine_strategy(current_state, overall_dir)
        
        return ComprehensivePrediction(
            current_state=current_state,
            current_confidence=state_result.confidence,
            short_term=short_pred,
            medium_term=medium_pred,
            long_term=long_pred,
            overall_direction=overall_dir,
            overall_confidence=overall_conf,
            overall_signal=overall_signal,
            position_suggestion=position,
            stop_loss=stop_loss,
            take_profit=take_profit,
            strategy_type=strategy,
            data_source=state_result.data_source
        )
    
    def _predict_short_term(self, 
                           ind: MarketIndicators,
                           state: MarketState) -> PeriodPrediction:
        """短期预测 (5-10天)"""
        factors = []
        score = 0
        
        # 5日动量
        if ind.mom_5d > 2:
            score += 2
            factors.append(f"5日动量强势({ind.mom_5d:+.1f}%)")
        elif ind.mom_5d < -2:
            score -= 2
            factors.append(f"5日动量弱势({ind.mom_5d:+.1f}%)")
        
        # 价格vs短期均线
        if ind.vs_ma5 > 1:
            score += 1
            factors.append("站上5日线")
        elif ind.vs_ma5 < -1:
            score -= 1
            factors.append("跌破5日线")
        
        # 10日动量
        if ind.mom_10d > 3:
            score += 1
            factors.append(f"10日动量正面({ind.mom_10d:+.1f}%)")
        elif ind.mom_10d < -3:
            score -= 1
            factors.append(f"10日动量负面({ind.mom_10d:+.1f}%)")
        
        # 基于当前状态调整
        if state.category == 'bull':
            score += 1
            factors.append("处于牛市状态")
        elif state.category == 'bear':
            score -= 1
            factors.append("处于熊市状态")
        
        # 波动率影响
        if ind.volatility_20d > 25:
            factors.append(f"高波动({ind.volatility_20d:.1f}%)")
            risk = 'high'
        elif ind.volatility_20d < 15:
            risk = 'low'
        else:
            risk = 'medium'
        
        # 确定方向
        direction = self._score_to_direction(score, max_score=5)
        confidence = min(90, 50 + abs(score) * 8)
        expected_return = score * 0.5  # 预期收益估算
        
        # 信号
        if score >= 2:
            signal = "短线买入"
        elif score <= -2:
            signal = "短线卖出"
        elif score > 0:
            signal = "轻仓试多"
        elif score < 0:
            signal = "减仓观望"
        else:
            signal = "观望"
        
        return PeriodPrediction(
            period='short',
            period_name='短期',
            days=5,
            direction=direction,
            confidence=confidence,
            expected_return=expected_return,
            risk_level=risk,
            signal=signal,
            key_factors=factors
        )
    
    def _predict_medium_term(self,
                            ind: MarketIndicators,
                            state: MarketState) -> PeriodPrediction:
        """中期预测 (20-60天)"""
        factors = []
        score = 0
        
        # 20日动量
        if ind.mom_20d > 5:
            score += 2
            factors.append(f"20日动量强劲({ind.mom_20d:+.1f}%)")
        elif ind.mom_20d > 2:
            score += 1
            factors.append(f"20日动量正面({ind.mom_20d:+.1f}%)")
        elif ind.mom_20d < -5:
            score -= 2
            factors.append(f"20日动量疲软({ind.mom_20d:+.1f}%)")
        elif ind.mom_20d < -2:
            score -= 1
            factors.append(f"20日动量负面({ind.mom_20d:+.1f}%)")
        
        # 60日动量
        if ind.mom_60d > 8:
            score += 2
            factors.append(f"60日趋势向上({ind.mom_60d:+.1f}%)")
        elif ind.mom_60d > 3:
            score += 1
        elif ind.mom_60d < -8:
            score -= 2
            factors.append(f"60日趋势向下({ind.mom_60d:+.1f}%)")
        elif ind.mom_60d < -3:
            score -= 1
        
        # 均线关系
        if ind.vs_ma60 > 3:
            score += 1
            factors.append(f"高于60日线({ind.vs_ma60:+.1f}%)")
        elif ind.vs_ma60 < -3:
            score -= 1
            factors.append(f"低于60日线({ind.vs_ma60:+.1f}%)")
        
        # 60日位置
        if ind.pos_60d > 70:
            factors.append("处于60日高位")
        elif ind.pos_60d < 30:
            factors.append("处于60日低位")
            score += 0.5  # 低位有支撑
        
        # 均线排列
        if ind.ma_bull:
            score += 1
            factors.append("均线多头排列")
        elif ind.ma_bear:
            score -= 1
            factors.append("均线空头排列")
        
        # 风险评估
        if abs(ind.mom_60d) > 15 or ind.volatility_20d > 30:
            risk = 'high'
        elif abs(ind.mom_60d) < 5 and ind.volatility_20d < 18:
            risk = 'low'
        else:
            risk = 'medium'
        
        direction = self._score_to_direction(score, max_score=6)
        confidence = min(85, 45 + abs(score) * 7)
        expected_return = score * 1.5
        
        # 信号
        if score >= 3:
            signal = "波段做多"
        elif score <= -3:
            signal = "波段做空/离场"
        elif score > 0:
            signal = "持有观察"
        elif score < 0:
            signal = "减仓待机"
        else:
            signal = "区间操作"
        
        return PeriodPrediction(
            period='medium',
            period_name='中期',
            days=20,
            direction=direction,
            confidence=confidence,
            expected_return=expected_return,
            risk_level=risk,
            signal=signal,
            key_factors=factors
        )
    
    def _predict_long_term(self,
                          ind: MarketIndicators,
                          state: MarketState) -> PeriodPrediction:
        """长期预测 (120天+)"""
        factors = []
        score = 0
        
        # 120日动量
        if ind.mom_120d > 15:
            score += 3
            factors.append(f"120日强势上涨({ind.mom_120d:+.1f}%)")
        elif ind.mom_120d > 8:
            score += 2
            factors.append(f"120日稳健上涨({ind.mom_120d:+.1f}%)")
        elif ind.mom_120d > 0:
            score += 1
        elif ind.mom_120d < -15:
            score -= 3
            factors.append(f"120日深度下跌({ind.mom_120d:+.1f}%)")
        elif ind.mom_120d < -8:
            score -= 2
            factors.append(f"120日明显下跌({ind.mom_120d:+.1f}%)")
        elif ind.mom_120d < 0:
            score -= 1
        
        # 年线偏离
        if ind.vs_ma250 > 10:
            score += 2
            factors.append(f"远高于年线({ind.vs_ma250:+.1f}%)")
        elif ind.vs_ma250 > 5:
            score += 1
            factors.append(f"高于年线({ind.vs_ma250:+.1f}%)")
        elif ind.vs_ma250 < -10:
            score -= 2
            factors.append(f"远低于年线({ind.vs_ma250:+.1f}%)")
        elif ind.vs_ma250 < -5:
            score -= 1
            factors.append(f"低于年线({ind.vs_ma250:+.1f}%)")
        
        # 250日位置
        if ind.pos_250d > 80:
            factors.append(f"处于年内高位({ind.pos_250d:.0f}%)")
        elif ind.pos_250d < 20:
            factors.append(f"处于年内低位({ind.pos_250d:.0f}%)")
            score += 1  # 低位有长期价值
        
        # 当前状态影响
        if state in [MarketState.BULL_STRONG, MarketState.BULL_NORMAL]:
            score += 1
            factors.append(f"当前牛市状态")
        elif state in [MarketState.BEAR_STRONG, MarketState.BEAR_NORMAL]:
            score -= 1
            factors.append(f"当前熊市状态")
        elif state == MarketState.TURNING_UP:
            score += 2
            factors.append("底部反转信号")
        elif state == MarketState.TURNING_DOWN:
            score -= 2
            factors.append("顶部反转信号")
        
        # 风险
        if state.category == 'bear' or ind.pos_250d > 90:
            risk = 'high'
        elif state.category == 'bull' and ind.pos_250d < 80:
            risk = 'low'
        else:
            risk = 'medium'
        
        direction = self._score_to_direction(score, max_score=7)
        confidence = min(80, 40 + abs(score) * 6)
        expected_return = score * 3
        
        # 信号
        if score >= 4:
            signal = "长期看多，逢低布局"
        elif score >= 2:
            signal = "趋势向上，持有为主"
        elif score <= -4:
            signal = "长期看空，控制仓位"
        elif score <= -2:
            signal = "趋势向下，谨慎操作"
        else:
            signal = "趋势不明，灵活应对"
        
        return PeriodPrediction(
            period='long',
            period_name='长期',
            days=120,
            direction=direction,
            confidence=confidence,
            expected_return=expected_return,
            risk_level=risk,
            signal=signal,
            key_factors=factors
        )
    
    def _score_to_direction(self, score: float, max_score: float) -> PredictionDirection:
        """分数转方向"""
        ratio = score / max_score
        if ratio >= 0.7:
            return PredictionDirection.STRONG_UP
        elif ratio >= 0.4:
            return PredictionDirection.UP
        elif ratio >= 0.15:
            return PredictionDirection.SLIGHT_UP
        elif ratio > -0.15:
            return PredictionDirection.NEUTRAL
        elif ratio > -0.4:
            return PredictionDirection.SLIGHT_DOWN
        elif ratio > -0.7:
            return PredictionDirection.DOWN
        else:
            return PredictionDirection.STRONG_DOWN
    
    def _combine_predictions(self,
                            short: PeriodPrediction,
                            medium: PeriodPrediction,
                            long: PeriodPrediction) -> Tuple[PredictionDirection, float]:
        """综合三周期预测"""
        # 加权得分 (短期20%, 中期30%, 长期50%)
        weighted_score = (
            short.direction.score * 0.20 +
            medium.direction.score * 0.30 +
            long.direction.score * 0.50
        )
        
        # 归一化到-3到+3
        max_score = 3
        direction = self._score_to_direction(weighted_score, max_score / 3)
        
        # 置信度（考虑一致性）
        scores = [short.direction.score, medium.direction.score, long.direction.score]
        same_sign = all(s >= 0 for s in scores) or all(s <= 0 for s in scores)
        
        base_conf = (short.confidence * 0.2 + medium.confidence * 0.3 + long.confidence * 0.5)
        if same_sign:
            confidence = min(95, base_conf * 1.2)
        else:
            confidence = base_conf * 0.8
        
        return direction, confidence
    
    def _generate_signal(self, direction: PredictionDirection, confidence: float) -> str:
        """生成综合信号"""
        if confidence < 50:
            return "信号不明确，建议观望"
        
        signals = {
            PredictionDirection.STRONG_UP: "强烈买入信号",
            PredictionDirection.UP: "买入信号",
            PredictionDirection.SLIGHT_UP: "偏多操作",
            PredictionDirection.NEUTRAL: "中性，观望或区间操作",
            PredictionDirection.SLIGHT_DOWN: "偏空操作",
            PredictionDirection.DOWN: "卖出信号",
            PredictionDirection.STRONG_DOWN: "强烈卖出信号"
        }
        return signals.get(direction, "观望")
    
    def _calculate_position(self,
                           direction: PredictionDirection,
                           confidence: float,
                           state: MarketState) -> float:
        """计算建议仓位"""
        # 基础仓位
        base_positions = {
            PredictionDirection.STRONG_UP: 0.9,
            PredictionDirection.UP: 0.7,
            PredictionDirection.SLIGHT_UP: 0.5,
            PredictionDirection.NEUTRAL: 0.3,
            PredictionDirection.SLIGHT_DOWN: 0.2,
            PredictionDirection.DOWN: 0.1,
            PredictionDirection.STRONG_DOWN: 0.0
        }
        base = base_positions.get(direction, 0.3)
        
        # 根据置信度调整
        if confidence >= 70:
            base *= 1.1
        elif confidence < 50:
            base *= 0.8
        
        # 根据状态调整
        state_def = STATE_DEFINITIONS.get(state, {})
        pos_range = state_def.get('position', (0.3, 0.5))
        
        # 综合
        return max(pos_range[0], min(pos_range[1], base))
    
    def _calculate_stops(self,
                        state: MarketState,
                        ind: MarketIndicators) -> Tuple[float, float]:
        """计算止损止盈"""
        # 基于波动率
        vol_factor = ind.volatility_20d / 100
        
        # 止损
        if state.category == 'bull':
            stop_loss = 0.05 + vol_factor  # 5% + 波动率
        elif state.category == 'bear':
            stop_loss = 0.03 + vol_factor * 0.5  # 更紧的止损
        else:
            stop_loss = 0.04 + vol_factor * 0.8
        
        # 止盈
        if state.category == 'bull':
            take_profit = 0.10 + vol_factor * 2
        elif state.category == 'bear':
            take_profit = 0.05 + vol_factor
        else:
            take_profit = 0.08 + vol_factor * 1.5
        
        return min(stop_loss, 0.15), min(take_profit, 0.30)
    
    def _determine_strategy(self,
                           state: MarketState,
                           direction: PredictionDirection) -> str:
        """确定策略类型"""
        if direction in [PredictionDirection.STRONG_UP, PredictionDirection.UP]:
            if state.category == 'bull':
                return "趋势追踪-积极"
            else:
                return "反转做多"
        elif direction in [PredictionDirection.STRONG_DOWN, PredictionDirection.DOWN]:
            if state.category == 'bear':
                return "趋势追踪-防守"
            else:
                return "高位减仓"
        elif state.category == 'range':
            return "区间交易"
        else:
            return "灵活配置"


# 便捷函数
def predict_market(symbol: str = '000001.XSHG',
                   df: pd.DataFrame = None) -> ComprehensivePrediction:
    """
    市场预测
    
    Args:
        symbol: 指数代码
        df: OHLCV数据
        
    Returns:
        ComprehensivePrediction
    """
    predictor = MarketStatePredictor()
    return predictor.predict(df=df, symbol=symbol)


def get_prediction_params(symbol: str = '000001.XSHG') -> Dict:
    """
    获取预测参数（供下游使用）
    """
    result = predict_market(symbol)
    return result.to_dict()


def print_prediction_summary(pred: ComprehensivePrediction) -> str:
    """打印预测摘要"""
    lines = []
    lines.append("=" * 70)
    lines.append("📈 市场状态预测报告")
    lines.append("=" * 70)
    
    # 当前状态
    lines.append(f"\n【当前状态】 {pred.current_state.value}")
    lines.append(f"  置信度: {pred.current_confidence:.1f}%")
    
    # 三周期预测
    lines.append(f"\n【短期预测】 {pred.short_term.days}天")
    lines.append(f"  方向: {pred.short_term.direction.value}")
    lines.append(f"  信号: {pred.short_term.signal}")
    lines.append(f"  预期收益: {pred.short_term.expected_return:+.1f}%")
    lines.append(f"  关键因素: {', '.join(pred.short_term.key_factors[:3])}")
    
    lines.append(f"\n【中期预测】 {pred.medium_term.days}天")
    lines.append(f"  方向: {pred.medium_term.direction.value}")
    lines.append(f"  信号: {pred.medium_term.signal}")
    lines.append(f"  预期收益: {pred.medium_term.expected_return:+.1f}%")
    lines.append(f"  关键因素: {', '.join(pred.medium_term.key_factors[:3])}")
    
    lines.append(f"\n【长期预测】 {pred.long_term.days}天+")
    lines.append(f"  方向: {pred.long_term.direction.value}")
    lines.append(f"  信号: {pred.long_term.signal}")
    lines.append(f"  预期收益: {pred.long_term.expected_return:+.1f}%")
    lines.append(f"  关键因素: {', '.join(pred.long_term.key_factors[:3])}")
    
    # 综合判断
    lines.append(f"\n{'='*50}")
    lines.append(f"【综合判断】")
    lines.append(f"  方向: {pred.overall_direction.value}")
    lines.append(f"  信号: {pred.overall_signal}")
    lines.append(f"  置信度: {pred.overall_confidence:.1f}%")
    
    # 操作参数
    lines.append(f"\n【操作参数】")
    lines.append(f"  建议仓位: {pred.position_suggestion:.0%}")
    lines.append(f"  止损位: {pred.stop_loss:.1%}")
    lines.append(f"  止盈位: {pred.take_profit:.1%}")
    lines.append(f"  策略类型: {pred.strategy_type}")
    
    return "\n".join(lines)

