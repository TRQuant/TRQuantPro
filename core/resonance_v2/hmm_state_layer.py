# -*- coding: utf-8 -*-
"""
Resonance V2 HMM State Layer
============================

状态层：使用hmmlearn的GaussianHMM进行市场状态识别。

核心功能：
1. Walk-forward训练（滚动训练/预测）
2. 状态预测与概率输出
3. 状态解释（映射为交易语言）
4. 状态变化信号检测

基于开源hmmlearn库，避免自建HMM的过拟合问题。

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
import warnings

import numpy as np
import pandas as pd

try:
    from hmmlearn.hmm import GaussianHMM
    HMMLEARN_AVAILABLE = True
except ImportError:
    HMMLEARN_AVAILABLE = False
    GaussianHMM = None

from .config import ResonanceV2Config, MarketState, DEFAULT_CONFIG
from .feature_layer import HMMObservations

logger = logging.getLogger(__name__)

# 忽略hmmlearn的收敛警告
warnings.filterwarnings('ignore', category=DeprecationWarning)


@dataclass
class StateInterpretation:
    """状态解释"""
    state_id: int
    name: str                      # 状态名称
    market_state: MarketState      # 映射的市场状态
    avg_return: float              # 平均收益率
    volatility: float              # 波动率
    avg_duration: float            # 平均持续时间（天）
    transition_probs: Dict[int, float]  # 转移概率
    description: str               # 描述


@dataclass
class HMMPrediction:
    """HMM预测结果"""
    current_state: int             # 当前状态ID
    state_name: str                # 状态名称
    market_state: MarketState      # 映射的市场状态
    state_probabilities: np.ndarray  # 各状态概率
    confidence: float              # 置信度
    state_sequence: List[int]      # 状态序列
    regime_change: bool            # 是否发生状态切换
    prev_state: Optional[int]      # 前一状态
    
    # 诊断信息
    train_log_likelihood: float = 0.0
    n_train_samples: int = 0
    interpretation: Optional[StateInterpretation] = None


class MarketStateHMM:
    """
    市场状态HMM
    
    使用hmmlearn的GaussianHMM进行市场状态识别。
    支持Walk-Forward训练，避免前瞻偏差。
    
    状态映射规则（基于统计特征）：
    - Risk-On (牛市): 平均收益>0.5%, 低波动
    - Risk-Off (熊市): 平均收益<-0.3%, 高波动
    - Sideways (震荡): 平均收益~0%, 中等波动
    - High-Vol (高波动转换): 任意收益, 极高波动
    """
    
    def __init__(self, config: Optional[ResonanceV2Config] = None):
        """
        初始化HMM
        
        Args:
            config: 配置对象
        """
        if not HMMLEARN_AVAILABLE:
            raise ImportError("hmmlearn未安装，请运行: pip install hmmlearn")
        
        self.config = config or DEFAULT_CONFIG
        self.n_states = self.config.n_hmm_states
        
        # HMM模型
        self.model: Optional[GaussianHMM] = None
        self._is_fitted = False
        
        # 状态解释
        self.state_interpretations: Dict[int, StateInterpretation] = {}
        
        # 训练历史
        self._train_history: List[Dict] = []
        self._last_state: Optional[int] = None
        
        logger.info(f"MarketStateHMM初始化: n_states={self.n_states}")
    
    def fit(
        self,
        observations: HMMObservations,
        verbose: bool = False
    ) -> bool:
        """
        训练HMM模型
        
        Args:
            observations: 观测变量
            verbose: 是否输出详细信息
        
        Returns:
            bool: 是否训练成功
        """
        if observations.n_samples < self.config.min_train_samples:
            logger.warning(f"样本数不足: {observations.n_samples} < {self.config.min_train_samples}")
            return False
        
        try:
            self.model = GaussianHMM(
                n_components=self.n_states,
                covariance_type=self.config.hmm_covariance_type,
                n_iter=self.config.hmm_n_iter,
                random_state=self.config.hmm_random_state,
                verbose=verbose
            )
            
            # 训练
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.model.fit(observations.data)
            
            self._is_fitted = True
            
            # 解释状态
            self._interpret_states(observations)
            
            # 记录训练历史
            self._train_history.append({
                'timestamp': datetime.now(),
                'n_samples': observations.n_samples,
                'score': self.model.score(observations.data),
            })
            
            if verbose:
                logger.info(f"HMM训练完成: score={self.model.score(observations.data):.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"HMM训练失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def fit_walk_forward(
        self,
        observations: HMMObservations,
        train_window: Optional[int] = None,
        test_window: Optional[int] = None,
        verbose: bool = False
    ) -> List[HMMPrediction]:
        """
        Walk-Forward训练与预测
        
        滚动方式：
        1. 使用前train_window个样本训练
        2. 预测后test_window个样本
        3. 滑动窗口，重复
        
        Args:
            observations: 全部观测变量
            train_window: 训练窗口大小
            test_window: 测试窗口大小
            verbose: 是否输出详细信息
        
        Returns:
            List[HMMPrediction]: 所有测试期的预测结果
        """
        train_window = train_window or self.config.train_window
        test_window = test_window or self.config.test_window
        
        n_samples = observations.n_samples
        predictions = []
        
        if n_samples < train_window + test_window:
            logger.warning(f"样本数不足进行walk-forward: {n_samples} < {train_window + test_window}")
            # 使用全部数据训练
            if self.fit(observations, verbose):
                pred = self.predict(observations)
                if pred:
                    predictions.append(pred)
            return predictions
        
        # Walk-forward循环
        start_idx = 0
        step = 0
        
        while start_idx + train_window + test_window <= n_samples:
            step += 1
            
            # 划分训练和测试数据
            train_end = start_idx + train_window
            test_end = min(train_end + test_window, n_samples)
            
            train_obs = HMMObservations(
                data=observations.data[start_idx:train_end],
                feature_names=observations.feature_names,
                dates=observations.dates[start_idx:train_end]
            )
            
            test_obs = HMMObservations(
                data=observations.data[train_end:test_end],
                feature_names=observations.feature_names,
                dates=observations.dates[train_end:test_end]
            )
            
            # 训练
            if self.fit(train_obs, verbose=False):
                # 预测
                pred = self.predict(test_obs)
                if pred:
                    pred.n_train_samples = train_obs.n_samples
                    pred.train_log_likelihood = self.model.score(train_obs.data)
                    predictions.append(pred)
                    
                    if verbose and step % 10 == 0:
                        logger.info(f"Walk-forward step {step}: "
                                  f"train [{start_idx}:{train_end}], "
                                  f"test [{train_end}:{test_end}], "
                                  f"state={pred.current_state}")
            
            # 滑动窗口
            start_idx += self.config.retrain_frequency
        
        logger.info(f"Walk-forward完成: {len(predictions)} 个预测周期")
        return predictions
    
    def predict(
        self,
        observations: HMMObservations,
        return_sequence: bool = True
    ) -> Optional[HMMPrediction]:
        """
        预测市场状态
        
        Args:
            observations: 观测变量
            return_sequence: 是否返回完整状态序列
        
        Returns:
            HMMPrediction: 预测结果
        """
        if not self._is_fitted or self.model is None:
            logger.warning("HMM模型未训练")
            return None
        
        if observations.n_samples == 0:
            logger.warning("观测数据为空")
            return None
        
        try:
            # 预测状态序列
            state_sequence = self.model.predict(observations.data)
            
            # 计算状态概率
            state_probs = self.model.predict_proba(observations.data)
            
            # 当前状态（最后一个）
            current_state = int(state_sequence[-1])
            current_probs = state_probs[-1]
            
            # 检测状态切换
            prev_state = self._last_state
            regime_change = prev_state is not None and prev_state != current_state
            self._last_state = current_state
            
            # 获取状态解释
            interpretation = self.state_interpretations.get(current_state)
            market_state = interpretation.market_state if interpretation else MarketState.SIDEWAYS
            state_name = interpretation.name if interpretation else f"State_{current_state}"
            
            # 计算置信度
            confidence = float(current_probs[current_state])
            
            return HMMPrediction(
                current_state=current_state,
                state_name=state_name,
                market_state=market_state,
                state_probabilities=current_probs,
                confidence=confidence,
                state_sequence=list(state_sequence) if return_sequence else [],
                regime_change=regime_change,
                prev_state=prev_state,
                interpretation=interpretation
            )
            
        except Exception as e:
            logger.error(f"HMM预测失败: {e}")
            return None
    
    def _interpret_states(
        self, 
        observations: HMMObservations,
        forward_returns: Optional[np.ndarray] = None
    ):
        """
        解释HMM状态 (V2: 基于波动率和前瞻收益)
        
        修复说明:
        原始实现使用训练期收益排序，但高收益训练期往往对应高波动（反转前兆）
        新实现：
        1. 如果有前瞻收益数据，按前瞻收益排序（最准确）
        2. 否则，使用波动率反向排序（低波动=稳定=risk_on倾向）
        
        映射规则：
        - Risk-On: 低波动状态（更稳定，往往对应后续上涨）
        - Risk-Off: 高波动状态（不稳定，往往对应后续下跌）
        - Sideways: 中等波动状态
        - High-Vol: 极高波动转换期
        """
        if not self._is_fitted or self.model is None:
            return
        
        # 获取状态序列
        states = self.model.predict(observations.data)
        
        # 提取log_return特征（假设是第一个特征）
        returns = observations.data[:, 0] if observations.n_features > 0 else np.zeros(len(states))
        
        # 提取volatility特征（假设是第二个特征）
        volatility = observations.data[:, 1] if observations.n_features > 1 else np.zeros(len(states))
        
        # 转移矩阵
        transmat = self.model.transmat_
        
        # 为每个状态计算统计特征
        state_stats = []
        for s in range(self.n_states):
            mask = states == s
            if mask.sum() > 0:
                avg_ret = returns[mask].mean()
                avg_vol = volatility[mask].mean()
                
                # 计算平均持续时间
                durations = self._calculate_state_durations(states, s)
                avg_duration = np.mean(durations) if durations else 0
                
                # 如果有前瞻收益，计算该状态的平均前瞻收益
                avg_forward_return = 0.0
                if forward_returns is not None and len(forward_returns) == len(states):
                    avg_forward_return = forward_returns[mask].mean()
                
                state_stats.append({
                    'state': s,
                    'avg_return': avg_ret,
                    'volatility': avg_vol,
                    'avg_duration': avg_duration,
                    'count': mask.sum(),
                    'avg_forward_return': avg_forward_return
                })
            else:
                state_stats.append({
                    'state': s,
                    'avg_return': 0,
                    'volatility': 0,
                    'avg_duration': 0,
                    'count': 0,
                    'avg_forward_return': 0
                })
        
        # 排序并映射状态 (V2: 基于波动率或前瞻收益)
        if forward_returns is not None and len(forward_returns) == len(states):
            # 方法1: 有前瞻收益时，按前瞻收益降序（最准确）
            sorted_stats = sorted(state_stats, key=lambda x: -x['avg_forward_return'])
            logger.info("状态解释：使用前瞻收益排序")
        else:
            # 方法2: 无前瞻收益时，按波动率升序（低波动=更稳定=risk_on）
            # 这比使用训练期收益更可靠，因为低波动期往往对应后续稳定上涨
            sorted_stats = sorted(state_stats, key=lambda x: x['volatility'])
            logger.info("状态解释：使用波动率反向排序（低波动=risk_on）")
        
        market_states = [MarketState.RISK_ON, MarketState.SIDEWAYS, MarketState.RISK_OFF]
        if self.n_states == 4:
            market_states = [MarketState.RISK_ON, MarketState.SIDEWAYS, MarketState.RISK_OFF, MarketState.HIGH_VOL]
        
        for idx, stats in enumerate(sorted_stats):
            state_id = stats['state']
            market_state = market_states[min(idx, len(market_states) - 1)]
            
            # 创建状态解释
            self.state_interpretations[state_id] = StateInterpretation(
                state_id=state_id,
                name=market_state.value,
                market_state=market_state,
                avg_return=stats['avg_return'],
                volatility=stats['volatility'],
                avg_duration=stats['avg_duration'],
                transition_probs={j: transmat[state_id, j] for j in range(self.n_states)},
                description=self._generate_state_description(market_state, stats)
            )
        
        logger.info(f"状态解释完成: {[s.name for s in self.state_interpretations.values()]}")
    
    def _calculate_state_durations(self, states: np.ndarray, target_state: int) -> List[int]:
        """计算状态持续时间"""
        durations = []
        current_duration = 0
        
        for s in states:
            if s == target_state:
                current_duration += 1
            else:
                if current_duration > 0:
                    durations.append(current_duration)
                current_duration = 0
        
        if current_duration > 0:
            durations.append(current_duration)
        
        return durations
    
    def _generate_state_description(self, market_state: MarketState, stats: Dict) -> str:
        """生成状态描述"""
        descriptions = {
            MarketState.RISK_ON: f"牛市/风险偏好: 平均收益{stats['avg_return']:.2%}, 低波动",
            MarketState.RISK_OFF: f"熊市/风险规避: 平均收益{stats['avg_return']:.2%}, 高波动",
            MarketState.SIDEWAYS: f"震荡市: 平均收益{stats['avg_return']:.2%}, 中等波动",
            MarketState.HIGH_VOL: f"高波动转换期: 波动率显著上升",
        }
        return descriptions.get(market_state, f"状态{stats['state']}")
    
    def get_state_summary(self) -> pd.DataFrame:
        """
        获取状态摘要
        
        Returns:
            pd.DataFrame: 状态统计表
        """
        if not self.state_interpretations:
            return pd.DataFrame()
        
        rows = []
        for state_id, interp in self.state_interpretations.items():
            rows.append({
                'State ID': state_id,
                'Name': interp.name,
                'Avg Return': f"{interp.avg_return:.2%}",
                'Volatility': f"{interp.volatility:.2f}",
                'Avg Duration': f"{interp.avg_duration:.1f}d",
                'Description': interp.description
            })
        
        return pd.DataFrame(rows)
    
    def score(self, observations: HMMObservations) -> float:
        """计算模型得分（对数似然）"""
        if not self._is_fitted or self.model is None:
            return float('-inf')
        return self.model.score(observations.data)
    
    @property
    def is_fitted(self) -> bool:
        return self._is_fitted
    
    def get_model_params(self) -> Dict:
        """获取模型参数"""
        if not self._is_fitted or self.model is None:
            return {}
        
        return {
            'n_states': self.n_states,
            'means': self.model.means_.tolist(),
            'covars': self.model.covars_.tolist(),
            'transmat': self.model.transmat_.tolist(),
            'startprob': self.model.startprob_.tolist(),
        }


def create_hmm_model(
    observations: HMMObservations,
    config: Optional[ResonanceV2Config] = None,
    walk_forward: bool = True,
    verbose: bool = False
) -> Tuple[MarketStateHMM, List[HMMPrediction]]:
    """
    便捷函数：创建并训练HMM模型
    
    Args:
        observations: 观测变量
        config: 配置
        walk_forward: 是否使用walk-forward训练
        verbose: 是否详细输出
    
    Returns:
        Tuple: (HMM模型, 预测结果列表)
    """
    hmm = MarketStateHMM(config)
    
    if walk_forward:
        predictions = hmm.fit_walk_forward(observations, verbose=verbose)
    else:
        hmm.fit(observations, verbose=verbose)
        pred = hmm.predict(observations)
        predictions = [pred] if pred else []
    
    return hmm, predictions
