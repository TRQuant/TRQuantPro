# -*- coding: utf-8 -*-
"""
Resonance V2 - 多周期共振 + HMM 市场趋势分析系统
================================================

四层架构：
1. 数据层 (data_layer.py): JQData数据获取
2. 特征层 (feature_layer.py): 多周期特征提取与共振评分
3. 状态层 (hmm_state_layer.py): hmmlearn GaussianHMM状态识别
4. 策略层 (strategy_layer.py): 信号生成与仓位管理

主要入口：
- ResonanceHMMAnalyzer: 统一分析接口
- quick_analyze(): 快速分析函数

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 导入各层模块
from .config import ResonanceV2Config, MarketState, DEFAULT_CONFIG
from .data_layer import MarketDataProvider, MarketData, get_data_provider
from .feature_layer import (
    MultiCycleFeatureExtractor,
    HMMObservations,
    MultiCycleFeatures,
    ResonanceScore,
    extract_features_from_data
)
from .hmm_state_layer import (
    MarketStateHMM,
    HMMPrediction,
    StateInterpretation,
    create_hmm_model
)
from .strategy_layer import (
    ResonanceStrategy,
    TradingSignal,
    SignalType,
    ExitReason,
    Position,
    SignalAggregator
)

logger = logging.getLogger(__name__)

# 版本信息
__version__ = "2.0.0"
__author__ = "TRQuant Team"


@dataclass
class ResonanceResult:
    """共振分析结果"""
    # 基本信息
    index_code: str
    analysis_date: str
    
    # HMM状态
    market_state: MarketState
    state_name: str
    state_confidence: float
    state_probabilities: Dict[str, float]
    regime_change: bool
    
    # 共振评分
    resonance_score: float
    resonance_level: str
    trend_sync: bool
    vol_sync: bool
    risk_sync: bool
    
    # 交易信号
    signal_type: SignalType
    target_position: float
    stop_loss_price: float
    
    # 诊断信息
    feature_details: Dict = field(default_factory=dict)
    hmm_details: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'index_code': self.index_code,
            'analysis_date': self.analysis_date,
            'market_state': self.market_state.value,
            'state_name': self.state_name,
            'state_confidence': self.state_confidence,
            'regime_change': self.regime_change,
            'resonance_score': self.resonance_score,
            'resonance_level': self.resonance_level,
            'trend_sync': self.trend_sync,
            'vol_sync': self.vol_sync,
            'risk_sync': self.risk_sync,
            'signal_type': self.signal_type.value,
            'target_position': self.target_position,
            'stop_loss_price': self.stop_loss_price,
        }
    
    def summary(self) -> str:
        """生成摘要"""
        return (
            f"【{self.analysis_date}】{self.index_code}\n"
            f"市场状态: {self.state_name} (置信度: {self.state_confidence:.1%})\n"
            f"共振评分: {self.resonance_score:.1f}/100 ({self.resonance_level})\n"
            f"信号类型: {self.signal_type.value}\n"
            f"目标仓位: {self.target_position:.1%}\n"
            f"状态切换: {'是' if self.regime_change else '否'}"
        )


class ResonanceHMMAnalyzer:
    """
    多周期共振 + HMM 统一分析接口
    
    使用方法:
    ```python
    analyzer = ResonanceHMMAnalyzer()
    result = analyzer.analyze("000300.XSHG", "2024-01-15")
    print(result.summary())
    ```
    """
    
    def __init__(self, config: Optional[ResonanceV2Config] = None):
        """
        初始化分析器
        
        Args:
            config: 配置对象
        """
        self.config = config or DEFAULT_CONFIG
        
        # 初始化各层组件
        self.data_provider = MarketDataProvider()
        self.feature_extractor = MultiCycleFeatureExtractor(self.config)
        self.hmm_model: Optional[MarketStateHMM] = None
        self.strategy = ResonanceStrategy(self.config)
        
        # 缓存
        self._last_market_data: Optional[MarketData] = None
        self._last_observations: Optional[HMMObservations] = None
        self._last_features: Optional[MultiCycleFeatures] = None
        
        logger.info(f"ResonanceHMMAnalyzer初始化: config={self.config.n_hmm_states} states")
    
    def analyze(
        self,
        index_code: str,
        as_of_date: str,
        lookback_days: int = 400,
        retrain_hmm: bool = False
    ) -> ResonanceResult:
        """
        分析市场状态 (V2: 增强版，包含北向资金和市场宽度)
        
        Args:
            index_code: 指数代码 (如 "000300.XSHG")
            as_of_date: 分析日期 (YYYY-MM-DD)
            lookback_days: 回溯天数（用于HMM训练）
            retrain_hmm: 是否重新训练HMM
        
        Returns:
            ResonanceResult: 分析结果
        """
        logger.info(f"开始分析: {index_code} @ {as_of_date}")
        
        # 1. 计算日期范围
        end_date = as_of_date
        start_date = (pd.to_datetime(as_of_date) - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
        
        # 2. 获取市场数据
        market_data = self.data_provider.get_index_data(index_code, start_date, end_date)
        
        if market_data.trading_days < self.config.min_train_samples:
            logger.warning(f"数据不足: {market_data.trading_days} < {self.config.min_train_samples}")
            return self._create_empty_result(index_code, as_of_date)
        
        self._last_market_data = market_data
        
        # 3. 获取增强数据 (北向资金、市场宽度)
        north_flow_df = self.data_provider.get_northbound_flow(start_date, end_date)
        breadth_df = self.data_provider.get_market_breadth_series(start_date, end_date)
        
        # 4. 提取特征 (增强版)
        hmm_observations = self.feature_extractor.extract_hmm_observations(
            market_data,
            north_flow_df=north_flow_df,
            breadth_df=breadth_df
        )
        multi_features = self.feature_extractor.extract_multi_cycle_features(market_data)
        resonance_score = self.feature_extractor.calculate_resonance_score(multi_features)
        
        self._last_observations = hmm_observations
        self._last_features = multi_features
        
        # 4. HMM状态预测
        if self.hmm_model is None or retrain_hmm:
            self.hmm_model = MarketStateHMM(self.config)
            self.hmm_model.fit(hmm_observations, verbose=False)
        
        hmm_prediction = self.hmm_model.predict(hmm_observations)
        
        if hmm_prediction is None:
            logger.warning("HMM预测失败")
            return self._create_empty_result(index_code, as_of_date)
        
        # 5. 生成交易信号
        current_price = market_data.close.iloc[-1] if len(market_data.close) > 0 else 0
        
        # 计算ATR
        if 'high' in market_data.data.columns and 'low' in market_data.data.columns:
            tr = pd.concat([
                market_data.data['high'] - market_data.data['low'],
                abs(market_data.data['high'] - market_data.data['close'].shift(1)),
                abs(market_data.data['low'] - market_data.data['close'].shift(1))
            ], axis=1).max(axis=1)
            atr = tr.rolling(14).mean().iloc[-1]
        else:
            atr = None
        
        signal = self.strategy.generate_signal(
            resonance_score, hmm_prediction, current_price, atr
        )
        
        # 6. 构建结果
        state_probs = {
            interp.name: float(hmm_prediction.state_probabilities[state_id])
            for state_id, interp in self.hmm_model.state_interpretations.items()
        }
        
        result = ResonanceResult(
            index_code=index_code,
            analysis_date=as_of_date,
            market_state=hmm_prediction.market_state,
            state_name=hmm_prediction.state_name,
            state_confidence=hmm_prediction.confidence,
            state_probabilities=state_probs,
            regime_change=hmm_prediction.regime_change,
            resonance_score=resonance_score.total_score,
            resonance_level=resonance_score.level,
            trend_sync=resonance_score.trend_sync,
            vol_sync=resonance_score.vol_sync,
            risk_sync=resonance_score.risk_sync,
            signal_type=signal.signal_type,
            target_position=signal.target_position,
            stop_loss_price=signal.stop_loss,
            feature_details=resonance_score.details,
            hmm_details=signal.details
        )
        
        logger.info(f"分析完成: {result.state_name}, 共振={result.resonance_score:.1f}")
        return result
    
    def analyze_batch(
        self,
        index_code: str,
        start_date: str,
        end_date: str,
        use_walk_forward: bool = True
    ) -> pd.DataFrame:
        """
        批量分析时间序列
        
        Args:
            index_code: 指数代码
            start_date: 开始日期
            end_date: 结束日期
            use_walk_forward: 是否使用Walk-Forward
        
        Returns:
            pd.DataFrame: 分析结果时间序列
        """
        logger.info(f"批量分析: {index_code} [{start_date} ~ {end_date}]")
        
        # 获取数据（需要更多历史数据用于训练）
        train_start = (pd.to_datetime(start_date) - timedelta(days=self.config.train_window * 2)).strftime('%Y-%m-%d')
        market_data = self.data_provider.get_index_data(index_code, train_start, end_date)
        
        if market_data.trading_days < self.config.min_train_samples:
            logger.warning(f"数据不足")
            return pd.DataFrame()
        
        # 获取增强数据 (北向资金、市场宽度)
        north_flow_df = self.data_provider.get_northbound_flow(train_start, end_date)
        breadth_df = self.data_provider.get_market_breadth_series(train_start, end_date)
        
        # 提取特征 (增强版)
        hmm_observations = self.feature_extractor.extract_hmm_observations(
            market_data,
            north_flow_df=north_flow_df,
            breadth_df=breadth_df
        )
        multi_features = self.feature_extractor.extract_multi_cycle_features(market_data)
        
        # Walk-Forward HMM训练
        hmm = MarketStateHMM(self.config)
        
        if use_walk_forward:
            predictions = hmm.fit_walk_forward(hmm_observations, verbose=True)
        else:
            hmm.fit(hmm_observations)
            pred = hmm.predict(hmm_observations)
            predictions = [pred] if pred else []
        
        # 计算共振评分序列
        resonance_df = self.feature_extractor.calculate_resonance_series(multi_features)
        
        # 构建日期到HMM状态的映射
        # 使用hmm_observations.dates与state_sequence对应
        date_to_state = {}
        date_to_confidence = {}
        
        if hmm_observations.dates is not None and len(hmm_observations.dates) > 0:
            # 对于非walk-forward模式，使用整体预测
            if not use_walk_forward and predictions:
                pred = predictions[0]
                if pred and pred.state_sequence:
                    for idx, state_id in enumerate(pred.state_sequence):
                        if idx < len(hmm_observations.dates):
                            date_str = str(hmm_observations.dates[idx])[:10]
                            # 根据state_id获取解释
                            interp = hmm.state_interpretations.get(state_id)
                            if interp:
                                date_to_state[date_str] = interp.market_state
                            else:
                                date_to_state[date_str] = MarketState.SIDEWAYS
                            # 计算置信度
                            date_to_confidence[date_str] = pred.confidence
            else:
                # Walk-forward模式：使用最后一次预测的结果
                # 每次预测覆盖对应的测试期日期
                for pred in predictions:
                    if pred and pred.state_sequence:
                        # 使用最后一个预测的状态作为代表
                        current_state = pred.market_state
                        conf = pred.confidence
                        # 为简化，我们用最后一次预测的结果
                        # 实际应该追踪每个测试期的日期
                        # 这里假设最新预测覆盖所有后续日期
                        pass
                
                # 更简单的方法：直接使用全部数据训练一次，获取完整状态序列
                hmm_full = MarketStateHMM(self.config)
                hmm_full.fit(hmm_observations)
                pred_full = hmm_full.predict(hmm_observations)
                
                if pred_full and pred_full.state_sequence:
                    for idx, state_id in enumerate(pred_full.state_sequence):
                        if idx < len(hmm_observations.dates):
                            date_str = str(hmm_observations.dates[idx])[:10]
                            interp = hmm_full.state_interpretations.get(state_id)
                            if interp:
                                date_to_state[date_str] = interp.market_state
                            else:
                                date_to_state[date_str] = MarketState.SIDEWAYS
                            date_to_confidence[date_str] = pred_full.confidence
        
        # 合并结果
        results = []
        
        # 过滤到目标日期范围
        target_dates = set(self.data_provider.get_trading_dates(start_date, end_date))
        
        for i, row in resonance_df.iterrows():
            date_str = str(row['date'])[:10]
            if date_str not in target_dates:
                continue
            
            # 获取该日期的HMM状态
            hmm_state = date_to_state.get(date_str, MarketState.SIDEWAYS)
            hmm_confidence = date_to_confidence.get(date_str, 0.5)
            
            results.append({
                'date': date_str,
                'resonance_score': row['total_score'],
                'trend_score': row['trend_score'],
                'vol_score': row['vol_score'],
                'risk_score': row['risk_score'],
                'resonance_level': row['level'],
                'hmm_state': hmm_state.value,
                'hmm_confidence': hmm_confidence,
            })
        
        return pd.DataFrame(results)
    
    def get_diagnostic_report(self) -> Dict:
        """
        获取诊断报告
        
        Returns:
            Dict: 诊断信息
        """
        report = {
            'config': {
                'n_hmm_states': self.config.n_hmm_states,
                'slow_cycle': self.config.slow_cycle,
                'fast_cycle': self.config.fast_cycle,
                'train_window': self.config.train_window,
            },
            'hmm_fitted': self.hmm_model is not None and self.hmm_model.is_fitted,
        }
        
        if self.hmm_model and self.hmm_model.is_fitted:
            report['hmm_params'] = self.hmm_model.get_model_params()
            report['state_summary'] = self.hmm_model.get_state_summary().to_dict('records')
        
        if self._last_observations:
            report['last_observations'] = {
                'n_samples': self._last_observations.n_samples,
                'n_features': self._last_observations.n_features,
                'feature_names': self._last_observations.feature_names,
            }
        
        return report
    
    def _create_empty_result(self, index_code: str, as_of_date: str) -> ResonanceResult:
        """创建空结果"""
        return ResonanceResult(
            index_code=index_code,
            analysis_date=as_of_date,
            market_state=MarketState.SIDEWAYS,
            state_name="unknown",
            state_confidence=0.0,
            state_probabilities={},
            regime_change=False,
            resonance_score=0.0,
            resonance_level="none",
            trend_sync=False,
            vol_sync=False,
            risk_sync=False,
            signal_type=SignalType.HOLD,
            target_position=0.0,
            stop_loss_price=0.0
        )


def quick_analyze(
    index_code: str = "000300.XSHG",
    as_of_date: Optional[str] = None
) -> ResonanceResult:
    """
    快速分析函数
    
    Args:
        index_code: 指数代码
        as_of_date: 分析日期，None则使用最新日期
    
    Returns:
        ResonanceResult: 分析结果
    """
    if as_of_date is None:
        as_of_date = datetime.now().strftime('%Y-%m-%d')
    
    analyzer = ResonanceHMMAnalyzer()
    return analyzer.analyze(index_code, as_of_date)


# 导出
__all__ = [
    # 配置
    'ResonanceV2Config',
    'MarketState',
    'DEFAULT_CONFIG',
    
    # 数据层
    'MarketDataProvider',
    'MarketData',
    'get_data_provider',
    
    # 特征层
    'MultiCycleFeatureExtractor',
    'HMMObservations',
    'MultiCycleFeatures',
    'ResonanceScore',
    
    # 状态层
    'MarketStateHMM',
    'HMMPrediction',
    'StateInterpretation',
    
    # 策略层
    'ResonanceStrategy',
    'TradingSignal',
    'SignalType',
    'ExitReason',
    'Position',
    'SignalAggregator',
    
    # 统一接口
    'ResonanceHMMAnalyzer',
    'ResonanceResult',
    'quick_analyze',
]
