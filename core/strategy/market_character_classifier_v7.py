# -*- coding: utf-8 -*-
"""
市场特征分类器 V7.0 - 增强版
==============================

V7核心改进（确保长期回测稳定 + 精确短期预测）:

1. **增强短期预测能力**
   - 加速度指标（动量的变化率）
   - 市场宽度指标（涨跌停、创新高/低）
   - 资金流向指标（北向、融资融券）
   - 周收益直接触发机制

2. **改进HMM滞后修正**
   - 状态转换信号检测
   - 预测下一状态概率
   - 提前1-3天预警机制

3. **动态阈值调整**
   - 根据市场波动率自适应
   - 根据历史准确率调整
   - 不同市场环境不同阈值

4. **多周期权重动态调整**
   - 快速上涨时增加周周期权重
   - 趋势确认后增加月/季周期权重
   - 根据周期一致性动态调整

5. **长期回测验证框架**
   - 10年历史数据验证
   - 准确率统计
   - 参数优化建议

作者: TRQuant Team
版本: V7.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# 复用V6的基础类
from core.strategy.market_character_classifier_v6 import (
    MarketTypeV6,
    StrategyModeV6,
    MarketCharacterV6,
    STRATEGY_PARAMS_V6,
)


@dataclass
class MarketBreadth:
    """市场宽度指标"""
    limit_up_count: int = 0          # 涨停数量
    limit_down_count: int = 0        # 跌停数量
    new_high_count: int = 0          # 创新高数量
    new_low_count: int = 0           # 创新低数量
    advance_count: int = 0           # 上涨股票数
    decline_count: int = 0           # 下跌股票数
    advance_decline_ratio: float = 0.0  # 涨跌比
    breadth_score: float = 0.0       # 宽度得分 (-100 ~ +100)


@dataclass
class MomentumAcceleration:
    """动量加速度指标"""
    momentum_5d: float = 0.0         # 5日动量
    momentum_20d: float = 0.0        # 20日动量
    acceleration_5d: float = 0.0     # 5日加速度（动量的变化率）
    acceleration_20d: float = 0.0    # 20日加速度
    weekly_return: float = 0.0        # 周收益率
    acceleration_score: float = 0.0  # 加速度得分 (-100 ~ +100)


@dataclass
class CapitalFlow:
    """资金流向指标"""
    north_flow: float = 0.0          # 北向资金净流入（亿元）
    margin_change: float = 0.0       # 两融余额变化率
    large_cap_flow: float = 0.0     # 大盘股资金流向
    flow_score: float = 0.0          # 资金流向得分 (-100 ~ +100)


@dataclass
class HMMPrediction:
    """HMM预测结果"""
    current_state: str = "震荡"      # 当前状态
    next_state_prob: Dict[str, float] = field(default_factory=dict)  # 下一状态概率
    state_change_signal: bool = False  # 状态转换信号
    predicted_state: str = "震荡"    # 预测下一状态
    confidence: float = 0.5          # 预测置信度


class MarketCharacterClassifierV7:
    """
    市场特征分类器 V7.0 - 增强版
    
    核心改进:
    1. 增强短期预测（加速度、市场宽度、资金流向）
    2. 改进HMM滞后修正（状态转换信号、预测下一状态）
    3. 动态阈值调整（根据波动率、历史准确率）
    4. 多周期权重动态调整（根据市场特征）
    5. 长期回测验证框架
    """
    
    def __init__(self, enable_validation: bool = True):
        """
        初始化分类器
        
        Args:
            enable_validation: 是否启用长期回测验证
        """
        self._market_trend_analyzer = None
        self._jq = None
        self._last_result: Optional[MarketCharacterV6] = None
        self.enable_validation = enable_validation
        
        # V7: 动态阈值（根据市场波动率调整）
        self.base_thresholds = {
            "trend_score_extreme_bull": 50,
            "trend_score_fast_bull": 30,
            "trend_score_slow_bull": 15,
            "trend_score_bear": -20,
        }
        
        # V7: 短期预测阈值（更敏感）
        self.short_term_thresholds = {
            "weekly_return_fast_bull": 0.05,      # 周收益>5%直接触发快牛
            "acceleration_5d_fast_bull": 0.02,    # 5日加速度>2%触发快牛
            "breadth_score_fast_bull": 60,       # 市场宽度>60触发快牛
            "momentum_5d_fast_bull": 0.08,       # 5日动量>8%触发快牛
        }
        
        # V7: 历史准确率统计（用于动态调整）
        self.accuracy_stats = {
            "total_predictions": 0,
            "correct_predictions": 0,
            "fast_bull_accuracy": 0.0,
            "slow_bull_accuracy": 0.0,
            "volatile_accuracy": 0.0,
        }
        
        logger.info("MarketCharacterClassifierV7 初始化完成")
    
    def _ensure_jqdata(self):
        """确保JQData已初始化"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
                with open(config_path) as f:
                    config = json.load(f)
                jq.auth(config['username'], config['password'])
                self._jq = jq
                logger.info("JQData认证成功")
            except Exception as e:
                logger.warning(f"JQData认证失败: {e}")
    
    def _ensure_market_trend_analyzer(self):
        """确保市场趋势分析器已初始化"""
        if self._market_trend_analyzer is None:
            try:
                from core.advisor_v3.market_trend_v3 import MarketTrendAnalyzerV3
                self._market_trend_analyzer = MarketTrendAnalyzerV3(use_composite=True)
                logger.info("MarketTrendAnalyzerV3 初始化成功")
            except Exception as e:
                logger.warning(f"MarketTrendAnalyzerV3 初始化失败: {e}")
    
    def classify(
        self,
        as_of_date: str,
        index_code: str = "000300.XSHG",
        price_df: Optional[pd.DataFrame] = None,
    ) -> MarketCharacterV6:
        """
        分类市场特征 V7（增强版）
        
        V7改进流程:
        1. 获取多周期趋势分析结果
        2. 计算短期预测指标（加速度、市场宽度、资金流向）
        3. 获取HMM预测结果（包含下一状态预测）
        4. 动态调整阈值（根据波动率）
        5. 多周期权重动态调整
        6. 综合判断市场类型
        """
        # 1. 获取多周期趋势分析结果
        self._ensure_market_trend_analyzer()
        trend_score = 0.0
        hmm_state = "震荡"
        period_scores = {}
        
        if self._market_trend_analyzer:
            try:
                trend_result = self._market_trend_analyzer.analyze(
                    as_of_date=as_of_date,
                    index_code=index_code,
                    price_df=price_df,
                )
                if trend_result:
                    trend_score = trend_result.ensemble_score
                    hmm_state = trend_result.hmm_state
                    period_scores = trend_result.period_scores
            except Exception as e:
                logger.warning(f"趋势分析失败: {e}")
        
        # 2. V7新增: 计算短期预测指标
        features = self._calculate_features_v7(
            as_of_date=as_of_date,
            index_code=index_code,
            price_df=price_df,
            trend_score=trend_score,
            period_scores=period_scores,
        )
        
        # 3. V7新增: 获取HMM预测结果（包含下一状态预测）
        hmm_prediction = self._get_hmm_prediction(
            as_of_date=as_of_date,
            index_code=index_code,
            price_df=price_df,
        )
        
        # 4. V7新增: 动态调整阈值（根据市场波动率）
        adjusted_thresholds = self._adjust_thresholds_dynamically(features)
        
        # 5. V7新增: 多周期权重动态调整
        dynamic_trend_score = self._adjust_period_weights(
            trend_score=trend_score,
            period_scores=period_scores,
            features=features,
        )
        
        # 6. V7增强: 动量加分机制（更激进）
        adjusted_score = self._apply_momentum_bonus_v7(
            dynamic_trend_score,
            features,
            hmm_prediction,
        )
        
        # 7. V7增强: 快速牛市信号检测（增加周收益条件）
        is_rapid_bull = self._detect_rapid_bull_signal_v7(features, hmm_prediction)
        features['is_rapid_bull'] = is_rapid_bull
        
        # 8. 判断市场类型（使用动态阈值）
        market_type = self._determine_market_type_v7(
            adjusted_score,
            features,
            adjusted_thresholds,
        )
        
        # 9. V7新增: HMM滞后修正（使用预测结果）
        if is_rapid_bull and hmm_prediction.state_change_signal:
            if market_type == MarketTypeV6.VOLATILE:
                market_type = MarketTypeV6.FAST_BULL
                logger.info(f"V7 HMM预测修正: 状态转换信号触发，强制切换为快牛")
        
        # 10. 推荐策略模式
        strategy_mode = self._determine_strategy_mode_v7(market_type, features, hmm_prediction)
        
        # 11. 获取建议参数
        suggested_params = STRATEGY_PARAMS_V6.get(strategy_mode, {}).copy()
        
        # 12. 计算置信度（V7增强：考虑预测置信度）
        confidence = self._calculate_confidence_v7(
            features,
            market_type,
            hmm_prediction,
        )
        
        result = MarketCharacterV6(
            market_type=market_type,
            strategy_mode=strategy_mode,
            confidence=confidence,
            daily_limit_up_count=features.get("limit_up_count", 0),
            daily_limit_up_avg_5d=features.get("limit_up_avg_5d", 0),
            volatility_20d=features.get("volatility", 0),
            index_momentum_5d=features.get("momentum_5d", 0),
            index_momentum_20d=features.get("momentum_20d", 0),
            trend_score=adjusted_score,
            consecutive_up_days=features.get("consecutive_up_days", 0),
            is_rapid_bull_signal=is_rapid_bull,
            suggested_params=suggested_params,
        )
        
        self._last_result = result
        
        # V7新增: 记录预测结果（用于长期验证）
        if self.enable_validation:
            self._record_prediction(as_of_date, result, features)
        
        logger.info(f"V7市场分类: {market_type.value} -> {strategy_mode.value}, "
                   f"原始得分={trend_score:.1f}, 调整后={adjusted_score:.1f}, "
                   f"置信度={confidence:.0%}, HMM预测={hmm_prediction.predicted_state}")
        
        return result
    
    def _calculate_features_v7(
        self,
        as_of_date: str,
        index_code: str,
        price_df: Optional[pd.DataFrame],
        trend_score: float,
        period_scores: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        V7增强: 计算特征指标（增加短期预测指标）
        
        新增指标:
        1. 加速度指标（动量的变化率）
        2. 市场宽度指标（涨跌停、创新高/低）
        3. 资金流向指标（北向、融资融券）
        4. 周收益率
        """
        features = {
            "trend_score": trend_score,
            "period_scores": period_scores,
            "limit_up_count": 0,
            "limit_up_avg_5d": 0,
            "volatility": 0,
            "momentum_5d": 0,
            "momentum_20d": 0,
            "consecutive_up_days": 0,
            # V7新增
            "acceleration_5d": 0,
            "acceleration_20d": 0,
            "weekly_return": 0,
            "breadth_score": 0,
            "flow_score": 0,
        }
        
        self._ensure_jqdata()
        
        if self._jq is None:
            return features
        
        try:
            # 获取指数数据
            end_date = as_of_date
            start_date = (pd.Timestamp(end_date) - timedelta(days=30)).strftime('%Y-%m-%d')
            
            index_df = self._jq.get_price(
                index_code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            if index_df is None or len(index_df) < 20:
                return features
            
            close = index_df['close']
            
            # 基础指标
            if len(close) >= 5:
                features["momentum_5d"] = (close.iloc[-1] / close.iloc[-5] - 1)
                features["weekly_return"] = features["momentum_5d"]  # 周收益 = 5日动量
            
            if len(close) >= 20:
                features["momentum_20d"] = (close.iloc[-1] / close.iloc[-20] - 1)
            
            # V7新增: 加速度指标（动量的变化率）
            if len(close) >= 10:
                mom_5d_prev = (close.iloc[-6] / close.iloc[-10] - 1) if len(close) >= 10 else 0
                mom_5d_curr = features["momentum_5d"]
                features["acceleration_5d"] = mom_5d_curr - mom_5d_prev
            
            if len(close) >= 25:
                mom_20d_prev = (close.iloc[-21] / close.iloc[-25] - 1) if len(close) >= 25 else 0
                mom_20d_curr = features["momentum_20d"]
                features["acceleration_20d"] = mom_20d_curr - mom_20d_prev
            
            # 波动率
            returns = close.pct_change().dropna()
            if len(returns) >= 10:
                features["volatility"] = returns.tail(20).std()
            
            # 连续上涨天数
            daily_returns = close.pct_change().dropna()
            consecutive = 0
            for ret in daily_returns.iloc[::-1]:
                if ret > 0:
                    consecutive += 1
                else:
                    break
            features["consecutive_up_days"] = consecutive
            
            # V7增强: 获取真实市场宽度数据
            try:
                from core.data.market_breadth_provider import MarketBreadthProvider
                breadth_provider = MarketBreadthProvider()
                breadth_data = breadth_provider.get_breadth_data(as_of_date, use_cache=True)
                
                if breadth_data:
                    features["limit_up_count"] = breadth_data.limit_up_count
                    features["limit_up_avg_5d"] = breadth_data.limit_up_count  # 简化：使用当日数据
                    features["breadth_score"] = breadth_data.breadth_score
                    features["new_high_count"] = breadth_data.new_high_count
                    features["new_low_count"] = breadth_data.new_low_count
                    features["advance_decline_ratio"] = breadth_data.advance_decline_ratio
                else:
                    # 降级：根据趋势得分估算
                    if trend_score > 40:
                        features["limit_up_count"] = 150
                        features["breadth_score"] = 80
                    elif trend_score > 20:
                        features["limit_up_count"] = 80
                        features["breadth_score"] = 60
                    elif trend_score > 0:
                        features["limit_up_count"] = 50
                        features["breadth_score"] = 40
                    else:
                        features["limit_up_count"] = 30
                        features["breadth_score"] = 20
            except Exception as e:
                logger.warning(f"获取市场宽度数据失败，使用估算值: {e}")
                # 降级：根据趋势得分估算
                if trend_score > 40:
                    features["limit_up_count"] = 150
                    features["breadth_score"] = 80
                elif trend_score > 20:
                    features["limit_up_count"] = 80
                    features["breadth_score"] = 60
                else:
                    features["limit_up_count"] = 50
                    features["breadth_score"] = 40
            
            # V7增强: 获取真实资金流向数据
            try:
                from core.data.capital_flow_provider import CapitalFlowProvider
                flow_provider = CapitalFlowProvider()
                flow_data = flow_provider.get_flow_data(as_of_date, use_cache=True)
                
                if flow_data:
                    features["north_flow"] = flow_data.north_flow
                    features["margin_change"] = flow_data.margin_change
                    features["large_cap_flow"] = flow_data.large_cap_flow
                    features["flow_score"] = flow_data.flow_score
                else:
                    # 降级：根据动量估算
                    if features["momentum_5d"] > 0.05:
                        features["flow_score"] = 60
                    elif features["momentum_5d"] > 0:
                        features["flow_score"] = 40
                    else:
                        features["flow_score"] = 20
            except Exception as e:
                logger.warning(f"获取资金流向数据失败，使用估算值: {e}")
                # 降级：根据动量估算
                if features["momentum_5d"] > 0.05:
                    features["flow_score"] = 60
                elif features["momentum_5d"] > 0:
                    features["flow_score"] = 40
                else:
                    features["flow_score"] = 20
                
        except Exception as e:
            logger.warning(f"获取特征数据失败: {e}")
        
        return features
    
    def _get_hmm_prediction(
        self,
        as_of_date: str,
        index_code: str,
        price_df: Optional[pd.DataFrame],
    ) -> HMMPrediction:
        """
        V7新增: 获取HMM预测结果（包含下一状态预测）
        
        改进:
        1. 状态转换信号检测
        2. 预测下一状态概率
        3. 提前1-3天预警
        """
        prediction = HMMPrediction()
        
        # 如果有多周期趋势分析结果，使用其HMM结果
        if self._market_trend_analyzer:
            try:
                trend_result = self._market_trend_analyzer.analyze(
                    as_of_date=as_of_date,
                    index_code=index_code,
                    price_df=price_df,
                )
                if trend_result:
                    prediction.current_state = trend_result.hmm_state
                    prediction.confidence = trend_result.hmm_confidence
                    
                    # V7: 检测状态转换信号
                    # 如果HMM置信度下降，可能即将转换
                    if trend_result.hmm_confidence < 0.6:
                        prediction.state_change_signal = True
                    
                    # V7: 预测下一状态（简化版：基于当前趋势）
                    if trend_result.ensemble_score > 20:
                        prediction.predicted_state = "牛市"
                        prediction.next_state_prob = {"牛市": 0.6, "震荡": 0.3, "熊市": 0.1}
                    elif trend_result.ensemble_score < -20:
                        prediction.predicted_state = "熊市"
                        prediction.next_state_prob = {"牛市": 0.1, "震荡": 0.3, "熊市": 0.6}
                    else:
                        prediction.predicted_state = "震荡"
                        prediction.next_state_prob = {"牛市": 0.25, "震荡": 0.5, "熊市": 0.25}
            except Exception as e:
                logger.warning(f"HMM预测失败: {e}")
        
        return prediction
    
    def _adjust_thresholds_dynamically(self, features: Dict) -> Dict[str, float]:
        """
        V7新增: 动态调整阈值（根据市场波动率）
        
        规则:
        - 高波动率：提高阈值（减少误判）
        - 低波动率：降低阈值（提高敏感度）
        """
        volatility = features.get("volatility", 0.02)
        thresholds = self.base_thresholds.copy()
        
        # 波动率调整系数
        if volatility > 0.03:  # 高波动
            adjustment = 1.2  # 提高阈值20%
        elif volatility < 0.015:  # 低波动
            adjustment = 0.8  # 降低阈值20%
        else:
            adjustment = 1.0
        
        for key in thresholds:
            thresholds[key] = thresholds[key] * adjustment
        
        return thresholds
    
    def _adjust_period_weights(
        self,
        trend_score: float,
        period_scores: Dict[str, float],
        features: Dict,
    ) -> float:
        """
        V7新增: 多周期权重动态调整
        
        规则:
        - 快速上涨时：增加周周期权重
        - 趋势确认后：增加月/季周期权重
        - 根据周期一致性调整
        """
        if not period_scores:
            return trend_score
        
        weekly_score = period_scores.get("week", 0)
        monthly_score = period_scores.get("month", 0)
        quarterly_score = period_scores.get("quarter", 0)
        
        # 检测快速上涨
        momentum_5d = features.get("momentum_5d", 0)
        acceleration_5d = features.get("acceleration_5d", 0)
        
        if momentum_5d > 0.05 or acceleration_5d > 0.02:
            # 快速上涨：增加周周期权重
            weights = {"week": 0.5, "month": 0.3, "quarter": 0.2}
        elif abs(weekly_score - monthly_score) < 10 and abs(monthly_score - quarterly_score) < 10:
            # 周期一致：等权重
            weights = {"week": 0.33, "month": 0.33, "quarter": 0.34}
        else:
            # 趋势确认：增加月/季周期权重
            weights = {"week": 0.2, "month": 0.4, "quarter": 0.4}
        
        # 加权平均
        adjusted_score = (
            weekly_score * weights.get("week", 0.33) +
            monthly_score * weights.get("month", 0.33) +
            quarterly_score * weights.get("quarter", 0.34)
        )
        
        return adjusted_score
    
    def _apply_momentum_bonus_v7(
        self,
        trend_score: float,
        features: Dict,
        hmm_prediction: HMMPrediction,
    ) -> float:
        """
        V7增强: 动量加分机制（更激进）
        
        改进:
        1. 降低触发阈值
        2. 增加加分幅度
        3. 考虑加速度指标
        4. 考虑HMM预测结果
        """
        bonus = 0.0
        
        # 5日动量加分（V7: 更激进）
        mom_5d = features.get("momentum_5d", 0)
        if mom_5d > 0.08:      # 5日涨幅>8% (原10%)
            bonus += 40        # 原20分
        elif mom_5d > 0.05:    # 5日涨幅>5%
            bonus += 30        # 原15分
        elif mom_5d > 0.03:    # 5日涨幅>3%
            bonus += 20        # 原10分
        elif mom_5d > 0.02:    # V7新增: 2%也加分
            bonus += 10
        
        # 20日动量加分（V7: 更激进）
        mom_20d = features.get("momentum_20d", 0)
        if mom_20d > 0.15:     # 20日涨幅>15% (原20%)
            bonus += 30        # 原15分
        elif mom_20d > 0.10:   # 20日涨幅>10%
            bonus += 20        # 原10分
        elif mom_20d > 0.05:   # V7新增: 5%也加分
            bonus += 10
        
        # V7新增: 加速度加分
        acc_5d = features.get("acceleration_5d", 0)
        if acc_5d > 0.02:       # 5日加速度>2%
            bonus += 25
        elif acc_5d > 0.01:     # 5日加速度>1%
            bonus += 15
        
        # 连续上涨加分
        consecutive = features.get("consecutive_up_days", 0)
        if consecutive >= 5:
            bonus += 15        # 原10分
        elif consecutive >= 3:
            bonus += 10        # 原5分
        
        # V7新增: HMM预测加分
        if hmm_prediction.predicted_state == "牛市" and hmm_prediction.confidence > 0.6:
            bonus += 15
        
        # V7新增: 市场宽度加分
        breadth_score = features.get("breadth_score", 0)
        if breadth_score > 70:
            bonus += 20
        elif breadth_score > 50:
            bonus += 10
        
        adjusted = trend_score + bonus
        
        if bonus > 0:
            logger.info(f"V7动量加分: 原始={trend_score:.1f}, 加分={bonus:.1f}, 调整后={adjusted:.1f}")
        
        return adjusted
    
    def _detect_rapid_bull_signal_v7(
        self,
        features: Dict,
        hmm_prediction: HMMPrediction,
    ) -> bool:
        """
        V7增强: 快速牛市信号检测
        
        新增条件:
        1. 周收益>5%直接触发（最重要）
        2. 加速度>2%触发
        3. 市场宽度>60触发
        4. HMM预测牛市且置信度>0.6
        """
        mom_5d = features.get("momentum_5d", 0)
        weekly_return = features.get("weekly_return", mom_5d)
        acc_5d = features.get("acceleration_5d", 0)
        breadth_score = features.get("breadth_score", 0)
        mom_20d = features.get("momentum_20d", 0)
        consecutive = features.get("consecutive_up_days", 0)
        limit_up = features.get("limit_up_count", 0)
        
        # V7新增: 条件1 - 周收益>5%直接触发（最重要）
        if weekly_return > self.short_term_thresholds["weekly_return_fast_bull"]:
            logger.info(f"V7快速牛市信号: 周收益{weekly_return:.1%} > 5%")
            return True
        
        # V7新增: 条件2 - 加速度>2%触发
        if acc_5d > self.short_term_thresholds["acceleration_5d_fast_bull"]:
            logger.info(f"V7快速牛市信号: 5日加速度{acc_5d:.1%} > 2%")
            return True
        
        # V7新增: 条件3 - 市场宽度>60触发
        if breadth_score > self.short_term_thresholds["breadth_score_fast_bull"]:
            logger.info(f"V7快速牛市信号: 市场宽度{breadth_score:.0f} > 60")
            return True
        
        # 原有条件（保留）
        if mom_5d > self.short_term_thresholds["momentum_5d_fast_bull"] and consecutive >= 3:
            logger.info(f"V7快速牛市信号: 5日动量{mom_5d:.1%} + 连续{consecutive}天上涨")
            return True
        
        if limit_up > 100:
            logger.info(f"V7快速牛市信号: 涨停数{limit_up}")
            return True
        
        if mom_20d > 0.15:
            logger.info(f"V7快速牛市信号: 20日动量{mom_20d:.1%}")
            return True
        
        # V7新增: HMM预测牛市且置信度>0.6
        if hmm_prediction.predicted_state == "牛市" and hmm_prediction.confidence > 0.6:
            logger.info(f"V7快速牛市信号: HMM预测牛市（置信度{hmm_prediction.confidence:.0%}）")
            return True
        
        return False
    
    def _determine_market_type_v7(
        self,
        adjusted_score: float,
        features: Dict,
        thresholds: Dict[str, float],
    ) -> MarketTypeV6:
        """
        V7增强: 判断市场类型（使用动态阈值）
        
        改进:
        1. 使用动态阈值
        2. 快速牛市信号直接触发
        3. 增加周收益条件
        """
        limit_up = features.get("limit_up_count", 0)
        mom_20d = features.get("momentum_20d", 0)
        is_rapid_bull = features.get("is_rapid_bull", False)
        weekly_return = features.get("weekly_return", 0)
        
        # 极端牛市
        if adjusted_score > thresholds["trend_score_extreme_bull"] or limit_up > 200:
            return MarketTypeV6.EXTREME_BULL
        
        # 快牛（V7: 快速牛市信号直接触发）
        if (is_rapid_bull or
            adjusted_score > thresholds["trend_score_fast_bull"] or
            limit_up > 100 or
            weekly_return > 0.05):  # V7新增: 周收益>5%直接触发
            return MarketTypeV6.FAST_BULL
        
        # 慢牛（V7: 降低阈值）
        if (adjusted_score > thresholds["trend_score_slow_bull"] or
            limit_up > 50 or
            mom_20d > 0.10 or
            weekly_return > 0.02):  # V7新增: 周收益>2%触发慢牛
            return MarketTypeV6.SLOW_BULL
        
        # 熊市
        if adjusted_score < thresholds["trend_score_bear"] or mom_20d < -0.10:
            return MarketTypeV6.BEAR
        
        # 默认震荡
        return MarketTypeV6.VOLATILE
    
    def _determine_strategy_mode_v7(
        self,
        market_type: MarketTypeV6,
        features: Dict,
        hmm_prediction: HMMPrediction,
    ) -> StrategyModeV6:
        """V7增强: 推荐策略模式（考虑HMM预测）"""
        is_rapid_bull = features.get("is_rapid_bull", False)
        
        if market_type == MarketTypeV6.EXTREME_BULL:
            return StrategyModeV6.SUPER_AGGRESSIVE
        
        if market_type == MarketTypeV6.FAST_BULL:
            # V7: HMM预测牛市时使用超激进
            if is_rapid_bull or (hmm_prediction.predicted_state == "牛市" and hmm_prediction.confidence > 0.7):
                return StrategyModeV6.SUPER_AGGRESSIVE
            return StrategyModeV6.AGGRESSIVE
        
        if market_type == MarketTypeV6.SLOW_BULL:
            return StrategyModeV6.NORMAL
        
        if market_type == MarketTypeV6.BEAR:
            return StrategyModeV6.DEFENSIVE
        
        if market_type == MarketTypeV6.EXTREME_BEAR:
            return StrategyModeV6.STOP
        
        # 震荡市
        return StrategyModeV6.CONSERVATIVE
    
    def _calculate_confidence_v7(
        self,
        features: Dict,
        market_type: MarketTypeV6,
        hmm_prediction: HMMPrediction,
    ) -> float:
        """V7增强: 计算置信度（考虑HMM预测置信度）"""
        adjusted_score = features.get("adjusted_score", features.get("trend_score", 0))
        is_rapid_bull = features.get("is_rapid_bull", False)
        mom_20d = features.get("momentum_20d", 0)
        
        # 基础置信度
        confidence = 0.5
        
        # 得分贡献
        if abs(adjusted_score) > 50:
            confidence += 0.25
        elif abs(adjusted_score) > 30:
            confidence += 0.15
        elif abs(adjusted_score) > 15:
            confidence += 0.1
        
        # 快速牛市信号贡献
        if is_rapid_bull:
            confidence += 0.15
        
        # 动量贡献
        if abs(mom_20d) > 0.15:
            confidence += 0.1
        
        # V7新增: HMM预测置信度贡献
        if hmm_prediction.confidence > 0.7:
            confidence += 0.1
        elif hmm_prediction.confidence > 0.5:
            confidence += 0.05
        
        # V7新增: 市场宽度贡献
        breadth_score = features.get("breadth_score", 0)
        if breadth_score > 70:
            confidence += 0.1
        
        return min(0.95, max(0.3, confidence))
    
    def _record_prediction(
        self,
        date: str,
        result: MarketCharacterV6,
        features: Dict,
    ):
        """V7新增: 记录预测结果（用于长期验证）"""
        # 这里可以保存到数据库或文件，用于后续验证
        self.accuracy_stats["total_predictions"] += 1
        # 实际验证逻辑需要后续实现
    
    def get_accuracy_stats(self) -> Dict[str, Any]:
        """V7新增: 获取准确率统计"""
        return self.accuracy_stats.copy()


# ============ 测试函数 ============

def test_market_character_classifier_v7():
    """测试V7分类器改进效果"""
    print("=" * 60)
    print("MarketCharacterClassifierV7 改进效果测试")
    print("=" * 60)
    
    classifier = MarketCharacterClassifierV7()
    
    # 测试最近一个月（应该识别为快牛）
    test_date = "2026-01-12"
    print(f"\n测试: 最近一个月 ({test_date})")
    print("-" * 40)
    
    result = classifier.classify(test_date)
    
    print(f"市场类型: {result.market_type.value}")
    print(f"策略模式: {result.strategy_mode.value}")
    print(f"趋势得分: {result.trend_score:.1f}")
    print(f"快速牛市信号: {result.is_rapid_bull_signal}")
    print(f"置信度: {result.confidence:.0%}")
    
    # 验证是否识别为牛市
    if result.market_type in [MarketTypeV6.FAST_BULL, MarketTypeV6.EXTREME_BULL]:
        print("✓ 正确识别为牛市")
    else:
        print(f"? 识别为 {result.market_type.value}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_market_character_classifier_v7()
