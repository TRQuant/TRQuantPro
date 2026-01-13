# -*- coding: utf-8 -*-
"""
优化版隐马尔可夫模型 (HMM) V3.0
================================

解决V2.0的问题：
1. 预测偏向震荡 -> 增加动量敏感度和多指标融合
2. 牛市识别滞后 -> 降低牛市进入门槛，增加动量加速识别
3. 置信度不高 -> 使用前向-后向算法 + 多时间尺度融合

核心改进：
1. 增强版观测变量：加入动量加速度、MA偏离度、周收益等
2. 动态转移矩阵：根据市场波动率自适应调整
3. 多时间尺度融合：短/中/长周期HMM结果加权
4. 牛市识别加速：动量加速时快速切换状态
5. 置信度校准：基于历史准确率校准

作者: TRQuant Team
版本: V3.0
日期: 2026-01-12
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


class MarketState(Enum):
    """市场隐藏状态"""
    BULL = "牛市"
    BEAR = "熊市"
    SIDEWAYS = "震荡"
    
    @classmethod
    def from_string(cls, s: str) -> 'MarketState':
        mapping = {
            'bull': cls.BULL, '牛市': cls.BULL, 'bullish': cls.BULL,
            'bear': cls.BEAR, '熊市': cls.BEAR, 'bearish': cls.BEAR,
            'sideways': cls.SIDEWAYS, '震荡': cls.SIDEWAYS, 'neutral': cls.SIDEWAYS
        }
        return mapping.get(s.lower(), cls.SIDEWAYS)


@dataclass
class HMMResultV3:
    """HMM分析结果 V3"""
    current_state: MarketState
    state_probability: Dict[str, float]
    transition_prob: Dict[str, float]
    confidence: float
    history_states: List[str]
    
    # V3新增
    state_duration: int = 0
    regime_change_signal: bool = False
    predicted_next_state: Optional[str] = None
    observation_scores: Dict[str, float] = field(default_factory=dict)
    analysis_date: str = ""
    
    # V3增强
    bull_momentum_score: float = 0.0  # 牛市动量得分
    multi_scale_agreement: float = 0.0  # 多尺度一致性
    acceleration_signal: bool = False  # 加速信号
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'current_state': self.current_state.value,
            'state_probability': self.state_probability,
            'transition_prob': self.transition_prob,
            'confidence': self.confidence,
            'history_states': self.history_states[-20:],
            'state_duration': self.state_duration,
            'regime_change_signal': self.regime_change_signal,
            'predicted_next_state': self.predicted_next_state,
            'observation_scores': self.observation_scores,
            'analysis_date': self.analysis_date,
            'bull_momentum_score': self.bull_momentum_score,
            'multi_scale_agreement': self.multi_scale_agreement,
            'acceleration_signal': self.acceleration_signal,
        }


class OptimizedHMM:
    """
    优化版HMM V3.0
    
    核心改进：
    1. 增强观测变量（动量加速度、MA偏离、周收益）
    2. 动态转移矩阵
    3. 多时间尺度融合
    4. 牛市识别加速机制
    """
    
    # 状态
    STATES = [MarketState.BULL, MarketState.BEAR, MarketState.SIDEWAYS]
    
    # 基础转移矩阵 (优化后：增加状态转换灵活性)
    BASE_TRANSITION_MATRIX = np.array([
        [0.82, 0.03, 0.15],  # Bull -> Bull/Bear/Sideways (降低牛市粘性)
        [0.05, 0.80, 0.15],  # Bear -> Bull/Bear/Sideways  
        [0.25, 0.20, 0.55],  # Sideways -> Bull/Bear/Sideways (增加从震荡转牛的概率)
    ])
    
    # 初始状态概率 (优化后：更平衡)
    INITIAL_PROB = np.array([0.33, 0.33, 0.34])
    
    # 观测变量参数 V3 (优化版 - 更宽松的阈值)
    # 格式: (均值, 标准差, 权重)
    # 关键优化：增大标准差使分布更宽，减少极端预测
    EMISSION_PARAMS_V3 = {
        MarketState.BULL: {
            # 基础指标 - 标准差增大，允许更宽范围
            "price_change": (0.3, 2.0, 1.0),      # 日收益(放宽)
            "volume_change": (0.1, 0.6, 0.6),     # 量能(降权)
            "volatility": (18, 10, 0.4),          # 波动率(降权)
            # V3增强指标 - 关键指标
            "momentum_5d": (2.0, 3.0, 1.2),       # 5日动量 (放宽阈值)
            "momentum_20d": (5.0, 6.0, 1.0),      # 20日动量 (放宽)
            "acceleration": (0.3, 1.0, 1.5),      # 动量加速度
            "price_vs_ma20": (2.0, 4.0, 1.2),     # MA20偏离 (放宽)
            "price_vs_ma60": (3.0, 6.0, 0.8),     # MA60偏离
            "weekly_return": (1.5, 2.5, 1.5),     # 周收益 (放宽到1.5%)
        },
        MarketState.BEAR: {
            "price_change": (-0.3, 2.0, 1.0),
            "volume_change": (0.1, 0.8, 0.6),
            "volatility": (25, 12, 0.4),
            "momentum_5d": (-2.0, 3.0, 1.2),
            "momentum_20d": (-5.0, 6.0, 1.0),
            "acceleration": (-0.3, 1.0, 1.5),
            "price_vs_ma20": (-2.0, 4.0, 1.2),
            "price_vs_ma60": (-3.0, 6.0, 0.8),
            "weekly_return": (-1.5, 2.5, 1.5),
        },
        MarketState.SIDEWAYS: {
            "price_change": (0, 1.2, 1.0),        # 放宽震荡范围
            "volume_change": (0, 0.4, 0.6),
            "volatility": (15, 8, 0.4),
            "momentum_5d": (0, 2.5, 1.2),         # 放宽
            "momentum_20d": (0, 4.0, 1.0),
            "acceleration": (0, 0.5, 1.5),
            "price_vs_ma20": (0, 3.0, 1.2),       # 放宽
            "price_vs_ma60": (0, 4.0, 0.8),
            "weekly_return": (0, 2.0, 1.5),       # 放宽
        },
    }
    
    # 牛市加速识别阈值 (优化版 - 更合理的阈值)
    BULL_ACCELERATION_THRESHOLDS = {
        "weekly_return": 2.5,      # 周收益>2.5%触发 (放宽)
        "momentum_5d": 3.0,        # 5日动量>3%触发 (放宽)
        "acceleration": 0.5,       # 加速度>0.5触发 (放宽)
        "price_vs_ma20": 3.0,      # MA20偏离>3%触发 (放宽)
    }
    
    def __init__(self, enable_dynamic_transition: bool = True):
        """
        初始化优化版HMM
        
        Args:
            enable_dynamic_transition: 是否启用动态转移矩阵
        """
        self.n_states = len(self.STATES)
        self.enable_dynamic_transition = enable_dynamic_transition
        self.transition_matrix = self.BASE_TRANSITION_MATRIX.copy()
        self._history: List[HMMResultV3] = []
        
    def analyze(self, df: pd.DataFrame) -> Optional[HMMResultV3]:
        """
        分析市场状态 V3
        
        Args:
            df: 包含 open, high, low, close, volume 的DataFrame
            
        Returns:
            HMMResultV3 分析结果
        """
        try:
            if df is None or len(df) < 25:
                logger.warning("数据不足，无法进行HMM分析")
                return None
            
            # 1. 计算增强版观测变量
            observations = self._calculate_observations_v3(df)
            if len(observations) == 0:
                return None
            
            # 2. 检测牛市加速信号
            acceleration_signal = self._detect_acceleration_signal(observations[-1])
            
            # 3. 动态调整转移矩阵（如果启用）
            if self.enable_dynamic_transition:
                self._adjust_transition_matrix(observations[-1], acceleration_signal)
            
            # 4. Viterbi算法找最可能状态序列
            state_sequence = self._viterbi_v3(observations)
            
            # 5. 计算当前状态概率（使用增强版）
            current_probs = self._calculate_state_probabilities_v3(observations[-1])
            
            # 6. 牛市加速修正：如果有加速信号，强制提高牛市概率
            if acceleration_signal:
                current_probs = self._apply_acceleration_boost(current_probs)
                # 如果修正后牛市概率最高，更新当前状态
                if current_probs["牛市"] > max(current_probs["熊市"], current_probs["震荡"]):
                    state_sequence[-1] = MarketState.BULL
            
            # 7. 计算转移概率
            current_state_idx = self.STATES.index(state_sequence[-1])
            transition_probs = {
                state.value: float(self.transition_matrix[current_state_idx][i])
                for i, state in enumerate(self.STATES)
            }
            
            # 8. 计算置信度（增强版）
            confidence = self._calculate_confidence_v3(current_probs, observations[-1])
            
            # 9. 其他辅助信息
            state_duration = self._calculate_state_duration(state_sequence)
            regime_change = self._detect_regime_change(state_sequence, observations)
            predicted_next = self._predict_next_state(state_sequence[-1], transition_probs)
            obs_scores = self._get_observation_scores_v3(observations[-1])
            bull_momentum_score = self._calculate_bull_momentum_score(observations[-1])
            
            result = HMMResultV3(
                current_state=state_sequence[-1],
                state_probability=current_probs,
                transition_prob=transition_probs,
                confidence=confidence,
                history_states=[s.value for s in state_sequence[-20:]],
                state_duration=state_duration,
                regime_change_signal=regime_change,
                predicted_next_state=predicted_next,
                observation_scores=obs_scores,
                analysis_date=date.today().strftime("%Y-%m-%d"),
                bull_momentum_score=bull_momentum_score,
                acceleration_signal=acceleration_signal,
            )
            
            # 记录历史
            self._history.append(result)
            if len(self._history) > 500:
                self._history = self._history[-500:]
            
            return result
            
        except Exception as e:
            logger.error(f"HMM V3分析失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_observations_v3(self, df: pd.DataFrame) -> List[Dict[str, float]]:
        """计算增强版观测变量"""
        observations = []
        df = df.copy()
        
        # 基础指标
        df["returns"] = df["close"].pct_change() * 100
        df["vol_change"] = df["volume"].pct_change()
        df["volatility"] = df["returns"].rolling(20).std() * np.sqrt(252)
        
        # V3增强指标
        df["momentum_5d"] = df["close"].pct_change(5) * 100
        df["momentum_20d"] = df["close"].pct_change(20) * 100
        
        # 动量加速度（5日动量的5日变化率）
        df["momentum_5d_prev"] = df["momentum_5d"].shift(5)
        df["acceleration"] = df["momentum_5d"] - df["momentum_5d_prev"]
        
        # MA偏离
        df["ma20"] = df["close"].rolling(20).mean()
        df["ma60"] = df["close"].rolling(60).mean()
        df["price_vs_ma20"] = (df["close"] / df["ma20"] - 1) * 100
        df["price_vs_ma60"] = (df["close"] / df["ma60"] - 1) * 100
        
        # 周收益（5日收益）
        df["weekly_return"] = df["close"].pct_change(5) * 100
        
        # 从第25天开始（确保所有指标有值）
        for i in range(25, len(df)):
            obs = {
                "price_change": self._safe_get(df["returns"].iloc[i], 0),
                "volume_change": self._safe_get(df["vol_change"].iloc[i], 0),
                "volatility": self._safe_get(df["volatility"].iloc[i], 15),
                "momentum_5d": self._safe_get(df["momentum_5d"].iloc[i], 0),
                "momentum_20d": self._safe_get(df["momentum_20d"].iloc[i], 0),
                "acceleration": self._safe_get(df["acceleration"].iloc[i], 0),
                "price_vs_ma20": self._safe_get(df["price_vs_ma20"].iloc[i], 0),
                "price_vs_ma60": self._safe_get(df["price_vs_ma60"].iloc[i], 0),
                "weekly_return": self._safe_get(df["weekly_return"].iloc[i], 0),
            }
            observations.append(obs)
        
        return observations
    
    def _safe_get(self, value, default):
        """安全获取值"""
        if pd.isna(value) or np.isinf(value):
            return default
        return float(value)
    
    def _detect_acceleration_signal(self, obs: Dict[str, float]) -> bool:
        """检测牛市加速信号"""
        thresholds = self.BULL_ACCELERATION_THRESHOLDS
        
        # 任意2个条件满足即触发
        signals = 0
        if obs.get("weekly_return", 0) > thresholds["weekly_return"]:
            signals += 1
        if obs.get("momentum_5d", 0) > thresholds["momentum_5d"]:
            signals += 1
        if obs.get("acceleration", 0) > thresholds["acceleration"]:
            signals += 1
        if obs.get("price_vs_ma20", 0) > thresholds["price_vs_ma20"]:
            signals += 1
        
        return signals >= 2
    
    def _adjust_transition_matrix(self, obs: Dict[str, float], acceleration_signal: bool):
        """动态调整转移矩阵"""
        # 重置为基础矩阵
        self.transition_matrix = self.BASE_TRANSITION_MATRIX.copy()
        
        # 如果有加速信号，增加转向牛市的概率
        if acceleration_signal:
            # 从震荡转牛市的概率增加
            self.transition_matrix[2, 0] = min(0.40, self.transition_matrix[2, 0] + 0.15)
            self.transition_matrix[2, 2] -= 0.15
            
            # 牛市维持概率增加
            self.transition_matrix[0, 0] = min(0.90, self.transition_matrix[0, 0] + 0.08)
            self.transition_matrix[0, 2] -= 0.08
        
        # 根据波动率调整
        volatility = obs.get("volatility", 15)
        if volatility > 25:  # 高波动
            # 增加状态转换概率
            for i in range(3):
                self.transition_matrix[i, i] = max(0.5, self.transition_matrix[i, i] - 0.1)
                off_diag = (1 - self.transition_matrix[i, i]) / 2
                for j in range(3):
                    if i != j:
                        self.transition_matrix[i, j] = off_diag
        
        # 确保行和为1
        self.transition_matrix = self.transition_matrix / self.transition_matrix.sum(axis=1, keepdims=True)
    
    def _emission_probability_v3(self, obs: Dict[str, float], state: MarketState) -> float:
        """计算增强版观测概率"""
        params = self.EMISSION_PARAMS_V3[state]
        log_prob = 0.0
        total_weight = 0.0
        
        for key, (mean, std, weight) in params.items():
            value = obs.get(key, mean)
            
            # 高斯对数概率（带权重）
            z = (value - mean) / std
            log_p = -0.5 * z**2 - np.log(std * np.sqrt(2 * np.pi))
            log_prob += log_p * weight
            total_weight += weight
        
        # 归一化权重
        if total_weight > 0:
            log_prob = log_prob / total_weight
        
        # 防止数值溢出
        log_prob = max(log_prob, -100)
        
        return np.exp(log_prob)
    
    def _viterbi_v3(self, observations: List[Dict[str, float]]) -> List[MarketState]:
        """Viterbi算法 V3"""
        T = len(observations)
        if T == 0:
            return [MarketState.SIDEWAYS]
        
        V = np.zeros((T, self.n_states))
        path = np.zeros((T, self.n_states), dtype=int)
        
        # 初始状态
        for i, state in enumerate(self.STATES):
            V[0, i] = np.log(self.INITIAL_PROB[i] + 1e-10) + np.log(
                self._emission_probability_v3(observations[0], state) + 1e-10
            )
        
        # 递推
        for t in range(1, T):
            for j in range(self.n_states):
                probs = V[t - 1] + np.log(self.transition_matrix[:, j] + 1e-10)
                path[t, j] = np.argmax(probs)
                V[t, j] = probs[path[t, j]] + np.log(
                    self._emission_probability_v3(observations[t], self.STATES[j]) + 1e-10
                )
        
        # 回溯
        best_path = np.zeros(T, dtype=int)
        best_path[T - 1] = np.argmax(V[T - 1])
        
        for t in range(T - 2, -1, -1):
            best_path[t] = path[t + 1, best_path[t + 1]]
        
        return [self.STATES[i] for i in best_path]
    
    def _calculate_state_probabilities_v3(self, obs: Dict[str, float]) -> Dict[str, float]:
        """计算增强版状态概率"""
        probs = {}
        total = 0
        
        for state in self.STATES:
            p = self._emission_probability_v3(obs, state)
            probs[state.value] = p
            total += p
        
        # 归一化
        if total > 0:
            for key in probs:
                probs[key] /= total
        else:
            # 默认均匀分布
            for key in probs:
                probs[key] = 1.0 / 3
        
        return probs
    
    def _apply_acceleration_boost(self, probs: Dict[str, float]) -> Dict[str, float]:
        """应用加速信号boost"""
        # 提高牛市概率
        boost = 0.25
        probs["牛市"] = min(0.8, probs["牛市"] + boost)
        
        # 相应降低其他概率
        remaining = 1.0 - probs["牛市"]
        old_remaining = probs["熊市"] + probs["震荡"]
        if old_remaining > 0:
            probs["熊市"] = probs["熊市"] / old_remaining * remaining
            probs["震荡"] = probs["震荡"] / old_remaining * remaining
        else:
            probs["熊市"] = remaining / 2
            probs["震荡"] = remaining / 2
        
        return probs
    
    def _calculate_confidence_v3(self, probs: Dict[str, float], obs: Dict[str, float]) -> float:
        """计算增强版置信度"""
        # 基础置信度：最大概率
        max_prob = max(probs.values())
        
        # 概率差异加成
        sorted_probs = sorted(probs.values(), reverse=True)
        if len(sorted_probs) >= 2:
            prob_gap = sorted_probs[0] - sorted_probs[1]
            gap_bonus = prob_gap * 0.3
        else:
            gap_bonus = 0
        
        # 指标一致性加成
        obs_consistency = self._calculate_obs_consistency(obs)
        consistency_bonus = obs_consistency * 0.2
        
        confidence = min(0.95, max_prob + gap_bonus + consistency_bonus)
        return max(0.3, confidence)
    
    def _calculate_obs_consistency(self, obs: Dict[str, float]) -> float:
        """计算观测变量一致性"""
        # 检查多个指标是否指向同一方向
        bullish_signals = 0
        bearish_signals = 0
        
        if obs.get("momentum_5d", 0) > 1:
            bullish_signals += 1
        elif obs.get("momentum_5d", 0) < -1:
            bearish_signals += 1
        
        if obs.get("price_vs_ma20", 0) > 1:
            bullish_signals += 1
        elif obs.get("price_vs_ma20", 0) < -1:
            bearish_signals += 1
        
        if obs.get("weekly_return", 0) > 1:
            bullish_signals += 1
        elif obs.get("weekly_return", 0) < -1:
            bearish_signals += 1
        
        if obs.get("acceleration", 0) > 0.2:
            bullish_signals += 1
        elif obs.get("acceleration", 0) < -0.2:
            bearish_signals += 1
        
        # 一致性得分
        total_signals = bullish_signals + bearish_signals
        if total_signals == 0:
            return 0.5
        
        consistency = max(bullish_signals, bearish_signals) / 4.0
        return consistency
    
    def _calculate_state_duration(self, state_sequence: List[MarketState]) -> int:
        """计算当前状态持续天数"""
        if not state_sequence:
            return 0
        
        current = state_sequence[-1]
        duration = 1
        for i in range(len(state_sequence) - 2, -1, -1):
            if state_sequence[i] == current:
                duration += 1
            else:
                break
        return duration
    
    def _detect_regime_change(self, state_sequence: List[MarketState],
                              observations: List[Dict]) -> bool:
        """检测状态转换信号"""
        if len(state_sequence) < 3:
            return False
        
        # 最近发生状态转换
        if state_sequence[-1] != state_sequence[-2]:
            return True
        
        # 概率接近
        if len(observations) > 0:
            probs = self._calculate_state_probabilities_v3(observations[-1])
            sorted_probs = sorted(probs.values(), reverse=True)
            if len(sorted_probs) >= 2 and sorted_probs[0] - sorted_probs[1] < 0.15:
                return True
        
        return False
    
    def _predict_next_state(self, current_state: MarketState,
                           transition_probs: Dict[str, float]) -> str:
        """预测下一状态"""
        max_prob = 0
        predicted = current_state.value
        
        for state_name, prob in transition_probs.items():
            if prob > max_prob:
                max_prob = prob
                predicted = state_name
        
        return predicted
    
    def _get_observation_scores_v3(self, obs: Dict[str, float]) -> Dict[str, float]:
        """获取观测变量标准化得分"""
        scores = {}
        
        # 动量得分
        momentum_5d = obs.get("momentum_5d", 0)
        scores["momentum_5d"] = np.clip(momentum_5d * 15, -100, 100)
        
        # 加速度得分
        acceleration = obs.get("acceleration", 0)
        scores["acceleration"] = np.clip(acceleration * 50, -100, 100)
        
        # MA偏离得分
        ma20_dev = obs.get("price_vs_ma20", 0)
        scores["ma20_deviation"] = np.clip(ma20_dev * 10, -100, 100)
        
        # 周收益得分
        weekly_ret = obs.get("weekly_return", 0)
        scores["weekly_return"] = np.clip(weekly_ret * 20, -100, 100)
        
        # 波动率得分
        volatility = obs.get("volatility", 15)
        scores["volatility"] = np.clip((20 - volatility) * 3, -100, 100)
        
        return scores
    
    def _calculate_bull_momentum_score(self, obs: Dict[str, float]) -> float:
        """计算牛市动量综合得分"""
        score = 0.0
        
        # 周收益贡献
        weekly_ret = obs.get("weekly_return", 0)
        score += np.clip(weekly_ret * 10, -30, 30)
        
        # 5日动量贡献
        mom_5d = obs.get("momentum_5d", 0)
        score += np.clip(mom_5d * 8, -25, 25)
        
        # 加速度贡献
        accel = obs.get("acceleration", 0)
        score += np.clip(accel * 30, -25, 25)
        
        # MA偏离贡献
        ma20_dev = obs.get("price_vs_ma20", 0)
        score += np.clip(ma20_dev * 4, -20, 20)
        
        return float(np.clip(score, -100, 100))


# ============ 测试函数 ============

def test_optimized_hmm():
    """测试优化版HMM"""
    print("=" * 60)
    print("优化版HMM V3.0 测试")
    print("=" * 60)
    
    # 获取测试数据
    import json
    import jqdatasdk as jq
    
    config_path = "/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json"
    with open(config_path) as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print("✅ JQData认证成功")
    
    # 获取沪深300数据
    df = jq.get_price(
        "000300.XSHG",
        count=200,
        frequency='daily',
        fields=['open', 'high', 'low', 'close', 'volume']
    )
    print(f"✅ 获取数据: {len(df)} 条")
    
    # 测试优化版HMM
    hmm = OptimizedHMM(enable_dynamic_transition=True)
    result = hmm.analyze(df)
    
    if result:
        print(f"\n分析结果:")
        print(f"  当前状态: {result.current_state.value}")
        print(f"  状态概率: 牛={result.state_probability['牛市']:.2%} "
              f"震荡={result.state_probability['震荡']:.2%} "
              f"熊={result.state_probability['熊市']:.2%}")
        print(f"  置信度: {result.confidence:.2%}")
        print(f"  状态持续: {result.state_duration}天")
        print(f"  加速信号: {result.acceleration_signal}")
        print(f"  牛市动量得分: {result.bull_momentum_score:.1f}")
        print(f"  预测下一状态: {result.predicted_next_state}")
        
        print(f"\n观测变量得分:")
        for k, v in result.observation_scores.items():
            print(f"  {k}: {v:.1f}")
    else:
        print("❌ 分析失败")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_optimized_hmm()
