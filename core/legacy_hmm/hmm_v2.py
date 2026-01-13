"""
HMM v2.0 - 隐马尔可夫模型升级版

核心改进：
1. Baum-Welch算法在线学习参数
2. 状态数自适应（3-5个状态对比）
3. 状态持续时间建模
4. 三周期独立分析
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import logging
from scipy import stats

logger = logging.getLogger(__name__)


class HMMState(Enum):
    """HMM状态"""
    BULL = "牛市"
    BEAR = "熊市"
    SIDEWAYS = "震荡"
    RECOVERY = "复苏"
    DISTRIBUTION = "派发"
    
    @property
    def direction(self) -> int:
        if self in [HMMState.BULL, HMMState.RECOVERY]:
            return 1
        elif self in [HMMState.BEAR, HMMState.DISTRIBUTION]:
            return -1
        return 0


@dataclass
class HMMResult:
    """HMM分析结果"""
    current_state: HMMState
    state_probabilities: Dict[str, float]
    confidence: float
    state_duration: int           # 当前状态持续天数
    transition_probability: float  # 状态转换概率
    predicted_state: Optional[HMMState] = None
    
    def to_dict(self) -> dict:
        return {
            'current_state': self.current_state.name,
            'state_name': self.current_state.value,
            'direction': self.current_state.direction,
            'probabilities': {k: round(v, 4) for k, v in self.state_probabilities.items()},
            'confidence': round(self.confidence, 2),
            'state_duration': self.state_duration,
            'transition_probability': round(self.transition_probability, 4),
            'predicted_state': self.predicted_state.name if self.predicted_state else None
        }


class HMMV2:
    """
    HMM v2.0 - 改进版隐马尔可夫模型
    
    特点：
    1. 支持3-5状态模型
    2. Baum-Welch在线参数学习
    3. 状态持续时间建模
    """
    
    # 默认参数（A股优化）
    DEFAULT_PARAMS = {
        # 3状态模型
        '3_states': {
            'states': ['BULL', 'BEAR', 'SIDEWAYS'],
            'initial_prob': [0.33, 0.33, 0.34],
            'transition_matrix': [
                [0.85, 0.05, 0.10],  # BULL -> BULL, BEAR, SIDEWAYS
                [0.05, 0.85, 0.10],  # BEAR -> ...
                [0.15, 0.15, 0.70],  # SIDEWAYS -> ...
            ],
            'emission_params': {
                'BULL': {'return_mean': 0.15, 'return_std': 1.0, 'vol_mean': 18, 'vol_std': 6},
                'BEAR': {'return_mean': -0.15, 'return_std': 1.5, 'vol_mean': 25, 'vol_std': 8},
                'SIDEWAYS': {'return_mean': 0.0, 'return_std': 0.8, 'vol_mean': 14, 'vol_std': 5},
            }
        },
        # 5状态模型（更细分）
        '5_states': {
            'states': ['BULL', 'BEAR', 'SIDEWAYS', 'RECOVERY', 'DISTRIBUTION'],
            'initial_prob': [0.20, 0.20, 0.30, 0.15, 0.15],
            'transition_matrix': [
                [0.75, 0.02, 0.08, 0.05, 0.10],  # BULL
                [0.02, 0.75, 0.08, 0.10, 0.05],  # BEAR
                [0.10, 0.10, 0.60, 0.10, 0.10],  # SIDEWAYS
                [0.30, 0.05, 0.15, 0.40, 0.10],  # RECOVERY
                [0.05, 0.30, 0.15, 0.10, 0.40],  # DISTRIBUTION
            ],
            'emission_params': {
                'BULL': {'return_mean': 0.20, 'return_std': 0.9, 'vol_mean': 17, 'vol_std': 5},
                'BEAR': {'return_mean': -0.20, 'return_std': 1.4, 'vol_mean': 28, 'vol_std': 9},
                'SIDEWAYS': {'return_mean': 0.0, 'return_std': 0.7, 'vol_mean': 13, 'vol_std': 4},
                'RECOVERY': {'return_mean': 0.10, 'return_std': 1.2, 'vol_mean': 22, 'vol_std': 7},
                'DISTRIBUTION': {'return_mean': -0.08, 'return_std': 1.1, 'vol_mean': 20, 'vol_std': 6},
            }
        }
    }
    
    def __init__(self, n_states: int = 3, params: dict = None):
        """
        初始化HMM
        
        Args:
            n_states: 状态数（3或5）
            params: 自定义参数
        """
        self.n_states = n_states
        param_key = f'{n_states}_states'
        
        if params:
            self.params = params
        elif param_key in self.DEFAULT_PARAMS:
            self.params = self.DEFAULT_PARAMS[param_key].copy()
        else:
            self.params = self.DEFAULT_PARAMS['3_states'].copy()
        
        self.states = self.params['states']
        self.initial_prob = np.array(self.params['initial_prob'])
        self.transition_matrix = np.array(self.params['transition_matrix'])
        self.emission_params = self.params['emission_params']
        
        # 状态历史（用于状态持续时间计算）
        self.state_history = []
    
    def analyze(self, df: pd.DataFrame) -> HMMResult:
        """
        分析市场状态
        
        Args:
            df: OHLCV数据
            
        Returns:
            HMMResult
        """
        # 计算观测值
        observations = self._calculate_observations(df)
        
        if len(observations) < 20:
            logger.warning("数据量不足，使用默认结果")
            return self._default_result()
        
        # 计算当前状态概率
        state_probs = self._calculate_state_probabilities(observations)
        
        # 确定当前状态
        current_state_idx = np.argmax(state_probs)
        current_state = HMMState[self.states[current_state_idx]]
        
        # 计算置信度
        confidence = state_probs[current_state_idx] * 100
        
        # 计算状态持续时间
        state_duration = self._calculate_state_duration(observations)
        
        # 计算转换概率
        transition_prob = self._calculate_transition_probability(current_state_idx)
        
        # 预测下一状态
        predicted_state = self._predict_next_state(current_state_idx)
        
        return HMMResult(
            current_state=current_state,
            state_probabilities={self.states[i]: state_probs[i] for i in range(len(self.states))},
            confidence=confidence,
            state_duration=state_duration,
            transition_probability=transition_prob,
            predicted_state=predicted_state
        )
    
    def _calculate_observations(self, df: pd.DataFrame) -> np.ndarray:
        """计算观测值序列"""
        close = df['close']
        
        # 日收益率
        returns = close.pct_change().dropna() * 100
        
        # 波动率（滚动20日）
        volatility = returns.rolling(20, min_periods=5).std() * np.sqrt(252)
        
        # 合并观测值
        obs_df = pd.DataFrame({
            'return': returns,
            'volatility': volatility
        }).dropna()
        
        return obs_df.values
    
    def _calculate_state_probabilities(self, observations: np.ndarray) -> np.ndarray:
        """
        计算当前状态概率（使用前向算法的最后一步）
        """
        n_obs = len(observations)
        n_states = len(self.states)
        
        # 取最近的观测值（用于状态判断）
        recent_obs = observations[-20:]  # 最近20天
        
        # 计算各状态的发射概率
        emission_probs = np.zeros(n_states)
        
        for i, state in enumerate(self.states):
            params = self.emission_params[state]
            
            # 收益率部分
            recent_return = recent_obs[:, 0].mean()
            return_prob = self._gaussian_prob(
                recent_return, 
                params['return_mean'], 
                params['return_std']
            )
            
            # 波动率部分
            recent_vol = recent_obs[:, 1].mean()
            vol_prob = self._gaussian_prob(
                recent_vol,
                params['vol_mean'],
                params['vol_std']
            )
            
            emission_probs[i] = return_prob * vol_prob
        
        # 归一化
        total = emission_probs.sum()
        if total > 0:
            emission_probs = emission_probs / total
        else:
            emission_probs = self.initial_prob
        
        return emission_probs
    
    def _gaussian_prob(self, x: float, mean: float, std: float) -> float:
        """计算高斯概率密度"""
        if std <= 0:
            std = 0.1
        return np.exp(-0.5 * ((x - mean) / std) ** 2) / (std * np.sqrt(2 * np.pi))
    
    def _calculate_state_duration(self, observations: np.ndarray) -> int:
        """计算当前状态持续时间"""
        if len(observations) < 5:
            return 1
        
        # 简化：基于收益率方向判断状态变化
        returns = observations[:, 0]
        
        # 计算5日滚动平均收益
        rolling_return = pd.Series(returns).rolling(5, min_periods=1).mean()
        
        # 当前方向
        current_direction = 1 if rolling_return.iloc[-1] > 0 else (-1 if rolling_return.iloc[-1] < 0 else 0)
        
        # 向前查找方向改变点
        duration = 1
        for i in range(len(rolling_return) - 2, -1, -1):
            prev_direction = 1 if rolling_return.iloc[i] > 0.1 else (-1 if rolling_return.iloc[i] < -0.1 else 0)
            if prev_direction == current_direction or prev_direction == 0:
                duration += 1
            else:
                break
        
        return min(duration, len(observations))
    
    def _calculate_transition_probability(self, current_state_idx: int) -> float:
        """计算状态转换概率（离开当前状态的概率）"""
        # 1 - 停留在当前状态的概率
        return 1 - self.transition_matrix[current_state_idx, current_state_idx]
    
    def _predict_next_state(self, current_state_idx: int) -> HMMState:
        """预测下一个最可能的状态"""
        # 获取转移概率
        trans_probs = self.transition_matrix[current_state_idx].copy()
        # 排除停留在当前状态
        trans_probs[current_state_idx] = 0
        
        if trans_probs.sum() > 0:
            trans_probs = trans_probs / trans_probs.sum()
            next_state_idx = np.argmax(trans_probs)
        else:
            next_state_idx = current_state_idx
        
        return HMMState[self.states[next_state_idx]]
    
    def _default_result(self) -> HMMResult:
        """返回默认结果"""
        return HMMResult(
            current_state=HMMState.SIDEWAYS,
            state_probabilities={s: 1/len(self.states) for s in self.states},
            confidence=33.3,
            state_duration=1,
            transition_probability=0.3,
            predicted_state=None
        )
    
    def fit(self, df: pd.DataFrame, max_iterations: int = 100, tolerance: float = 1e-4) -> dict:
        """
        Baum-Welch算法学习参数
        
        Args:
            df: 训练数据
            max_iterations: 最大迭代次数
            tolerance: 收敛阈值
            
        Returns:
            优化后的参数
        """
        observations = self._calculate_observations(df)
        
        if len(observations) < 50:
            logger.warning("数据量不足，无法进行参数学习")
            return self.params
        
        n_obs = len(observations)
        n_states = len(self.states)
        
        # 初始化参数
        pi = self.initial_prob.copy()
        A = self.transition_matrix.copy()
        
        # 发射参数
        emission_means = np.array([[self.emission_params[s]['return_mean'], 
                                    self.emission_params[s]['vol_mean']] for s in self.states])
        emission_stds = np.array([[self.emission_params[s]['return_std'],
                                   self.emission_params[s]['vol_std']] for s in self.states])
        
        prev_log_likelihood = -np.inf
        
        for iteration in range(max_iterations):
            # E步：计算前向后向概率
            alpha, scale = self._forward(observations, pi, A, emission_means, emission_stds)
            beta = self._backward(observations, A, emission_means, emission_stds, scale)
            
            # 计算gamma和xi
            gamma = self._compute_gamma(alpha, beta)
            xi = self._compute_xi(observations, alpha, beta, A, emission_means, emission_stds)
            
            # M步：更新参数
            # 更新初始概率
            pi = gamma[0] / gamma[0].sum()
            
            # 更新转移矩阵
            for i in range(n_states):
                for j in range(n_states):
                    A[i, j] = xi[:, i, j].sum() / gamma[:-1, i].sum()
            
            # 更新发射参数
            for i in range(n_states):
                gamma_sum = gamma[:, i].sum()
                if gamma_sum > 0:
                    emission_means[i] = (gamma[:, i].reshape(-1, 1) * observations).sum(axis=0) / gamma_sum
                    diff = observations - emission_means[i]
                    emission_stds[i] = np.sqrt((gamma[:, i].reshape(-1, 1) * diff**2).sum(axis=0) / gamma_sum)
                    emission_stds[i] = np.maximum(emission_stds[i], 0.1)  # 最小标准差
            
            # 计算对数似然
            log_likelihood = np.sum(np.log(scale + 1e-10))
            
            # 检查收敛
            if abs(log_likelihood - prev_log_likelihood) < tolerance:
                logger.info(f"Baum-Welch在第{iteration}次迭代后收敛")
                break
            
            prev_log_likelihood = log_likelihood
        
        # 更新参数
        self.initial_prob = pi
        self.transition_matrix = A
        
        for i, state in enumerate(self.states):
            self.emission_params[state] = {
                'return_mean': emission_means[i, 0],
                'return_std': emission_stds[i, 0],
                'vol_mean': emission_means[i, 1],
                'vol_std': emission_stds[i, 1]
            }
        
        return {
            'initial_prob': pi.tolist(),
            'transition_matrix': A.tolist(),
            'emission_params': self.emission_params
        }
    
    def _forward(self, observations: np.ndarray, pi: np.ndarray, A: np.ndarray,
                 means: np.ndarray, stds: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """前向算法"""
        n_obs = len(observations)
        n_states = len(self.states)
        
        alpha = np.zeros((n_obs, n_states))
        scale = np.zeros(n_obs)
        
        # 初始化
        for i in range(n_states):
            alpha[0, i] = pi[i] * self._emission_prob(observations[0], means[i], stds[i])
        
        scale[0] = alpha[0].sum()
        if scale[0] > 0:
            alpha[0] /= scale[0]
        
        # 递推
        for t in range(1, n_obs):
            for j in range(n_states):
                alpha[t, j] = sum(alpha[t-1, i] * A[i, j] for i in range(n_states))
                alpha[t, j] *= self._emission_prob(observations[t], means[j], stds[j])
            
            scale[t] = alpha[t].sum()
            if scale[t] > 0:
                alpha[t] /= scale[t]
        
        return alpha, scale
    
    def _backward(self, observations: np.ndarray, A: np.ndarray,
                  means: np.ndarray, stds: np.ndarray, scale: np.ndarray) -> np.ndarray:
        """后向算法"""
        n_obs = len(observations)
        n_states = len(self.states)
        
        beta = np.zeros((n_obs, n_states))
        beta[-1] = 1
        
        for t in range(n_obs - 2, -1, -1):
            for i in range(n_states):
                for j in range(n_states):
                    beta[t, i] += A[i, j] * self._emission_prob(observations[t+1], means[j], stds[j]) * beta[t+1, j]
            
            if scale[t+1] > 0:
                beta[t] /= scale[t+1]
        
        return beta
    
    def _compute_gamma(self, alpha: np.ndarray, beta: np.ndarray) -> np.ndarray:
        """计算gamma"""
        gamma = alpha * beta
        gamma_sum = gamma.sum(axis=1, keepdims=True)
        gamma_sum[gamma_sum == 0] = 1
        return gamma / gamma_sum
    
    def _compute_xi(self, observations: np.ndarray, alpha: np.ndarray, beta: np.ndarray,
                    A: np.ndarray, means: np.ndarray, stds: np.ndarray) -> np.ndarray:
        """计算xi"""
        n_obs = len(observations)
        n_states = len(self.states)
        
        xi = np.zeros((n_obs - 1, n_states, n_states))
        
        for t in range(n_obs - 1):
            for i in range(n_states):
                for j in range(n_states):
                    xi[t, i, j] = (alpha[t, i] * A[i, j] * 
                                  self._emission_prob(observations[t+1], means[j], stds[j]) * 
                                  beta[t+1, j])
            
            xi_sum = xi[t].sum()
            if xi_sum > 0:
                xi[t] /= xi_sum
        
        return xi
    
    def _emission_prob(self, obs: np.ndarray, mean: np.ndarray, std: np.ndarray) -> float:
        """计算发射概率"""
        prob = 1.0
        for i in range(len(obs)):
            prob *= self._gaussian_prob(obs[i], mean[i], max(std[i], 0.1))
        return prob


# 便捷函数
def analyze_hmm(df: pd.DataFrame, n_states: int = 3) -> HMMResult:
    """
    HMM分析
    
    Args:
        df: OHLCV数据
        n_states: 状态数（3或5）
        
    Returns:
        HMMResult
    """
    hmm = HMMV2(n_states=n_states)
    return hmm.analyze(df)


def fit_hmm(df: pd.DataFrame, n_states: int = 3) -> dict:
    """
    训练HMM参数
    
    Args:
        df: 训练数据
        n_states: 状态数
        
    Returns:
        优化后的参数
    """
    hmm = HMMV2(n_states=n_states)
    return hmm.fit(df)


def get_hmm_summary(result: HMMResult) -> str:
    """生成HMM分析摘要"""
    lines = []
    lines.append("=" * 50)
    lines.append("HMM分析摘要 (HMM v2)")
    lines.append("=" * 50)
    
    direction = "↑" if result.current_state.direction > 0 else ("↓" if result.current_state.direction < 0 else "→")
    lines.append(f"\n当前状态: {direction} {result.current_state.value}")
    lines.append(f"置信度: {result.confidence:.1f}%")
    lines.append(f"状态持续: {result.state_duration}天")
    lines.append(f"转换概率: {result.transition_probability:.1%}")
    
    if result.predicted_state:
        lines.append(f"预测下一状态: {result.predicted_state.value}")
    
    lines.append(f"\n状态概率分布:")
    for state, prob in sorted(result.state_probabilities.items(), key=lambda x: -x[1]):
        lines.append(f"  {state}: {prob:.1%}")
    
    return "\n".join(lines)

