"""
修复版HMM - 使用正确的观测变量和发射参数
支持GPU加速（可选）
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# 尝试导入GPU加速库
try:
    import cupy as cp
    HAS_GPU = True
    logger.info("GPU加速可用 (CuPy)")
except ImportError:
    HAS_GPU = False
    cp = None

try:
    import torch
    HAS_TORCH = torch.cuda.is_available()
    if HAS_TORCH:
        logger.info(f"GPU加速可用 (PyTorch CUDA: {torch.cuda.get_device_name(0)})")
except ImportError:
    HAS_TORCH = False


class MarketState(Enum):
    BULL = "牛市"
    BEAR = "熊市"
    SIDEWAYS = "震荡"
    
    def to_english(self) -> str:
        return {'牛市': 'bull', '熊市': 'bear', '震荡': 'sideways'}[self.value]


@dataclass
class HMMResult:
    current_state: MarketState
    state_probability: Dict[str, float]
    confidence: float
    history_states: List[str] = field(default_factory=list)
    
    def is_bullish(self) -> bool:
        return self.current_state == MarketState.BULL
    
    def is_bearish(self) -> bool:
        return self.current_state == MarketState.BEAR


class FixedHMM:
    """
    修复版隐马尔可夫模型
    
    修复内容:
    1. 发射参数基于A股实际数据校准
    2. 使用趋势指标（momentum, MA位置）作为核心观测变量
    3. 降低状态粘性，提高状态转换敏感度
    4. 可选GPU加速
    """
    
    # 修正后的状态转移矩阵（降低粘性）
    TRANSITION_MATRIX = np.array([
        [0.75, 0.10, 0.15],  # Bull -> Bull/Bear/Sideways
        [0.10, 0.75, 0.15],  # Bear -> Bull/Bear/Sideways
        [0.20, 0.20, 0.60],  # Sideways -> Bull/Bear/Sideways
    ])
    
    # 初始状态概率（A股偏震荡）
    INITIAL_PROB = np.array([0.25, 0.30, 0.45])
    
    # 修正后的发射参数 - 基于A股2014-2024实际数据
    EMISSION_PARAMS = {
        MarketState.BULL: {
            'price_change': (0.15, 0.8),      # 牛市日均+0.15%
            'momentum_20d': (3.0, 4.0),       # 20日累计涨3%
            'price_vs_ma20': (2.0, 3.0),      # 价格高于MA20 2%
            'price_vs_ma60': (5.0, 5.0),      # 价格高于MA60 5%
            'volatility': (18, 8),
            'volume_change': (0.1, 0.4),
        },
        MarketState.BEAR: {
            'price_change': (-0.15, 0.8),
            'momentum_20d': (-3.0, 4.0),
            'price_vs_ma20': (-2.0, 3.0),
            'price_vs_ma60': (-5.0, 5.0),
            'volatility': (25, 10),
            'volume_change': (0.15, 0.5),
        },
        MarketState.SIDEWAYS: {
            'price_change': (0.0, 0.5),
            'momentum_20d': (0.0, 2.0),
            'price_vs_ma20': (0.0, 1.5),
            'price_vs_ma60': (0.0, 3.0),
            'volatility': (14, 5),
            'volume_change': (-0.05, 0.3),
        }
    }
    
    # 核心观测变量（用于发射概率计算）
    CORE_OBS_KEYS = ['price_change', 'momentum_20d', 'price_vs_ma20', 'price_vs_ma60', 'volatility']
    
    def __init__(self, use_gpu: bool = False):
        self.states = [MarketState.BULL, MarketState.BEAR, MarketState.SIDEWAYS]
        self.n_states = 3
        self.transition_matrix = self.TRANSITION_MATRIX.copy()
        self.use_gpu = use_gpu and (HAS_GPU or HAS_TORCH)
        
        if self.use_gpu:
            logger.info("启用GPU加速")
    
    def analyze(self, df: pd.DataFrame) -> Optional[HMMResult]:
        """分析市场状态"""
        try:
            if df is None or len(df) < 30:
                return None
            
            observations = self._calculate_observations(df)
            if len(observations) == 0:
                return None
            
            # Viterbi算法
            if self.use_gpu and HAS_TORCH:
                state_sequence = self._viterbi_gpu(observations)
            else:
                state_sequence = self._viterbi(observations)
            
            # 计算当前状态概率
            current_probs = self._calculate_state_probabilities(observations[-1])
            confidence = max(current_probs.values())
            
            return HMMResult(
                current_state=state_sequence[-1],
                state_probability=current_probs,
                confidence=confidence,
                history_states=[s.value for s in state_sequence[-20:]]
            )
            
        except Exception as e:
            logger.error(f"HMM分析失败: {e}")
            return None
    
    def _calculate_observations(self, df: pd.DataFrame) -> List[Dict[str, float]]:
        """计算观测变量"""
        observations = []
        df = df.copy()
        
        # 计算指标
        df['returns'] = df['close'].pct_change() * 100
        df['vol_change'] = df['volume'].pct_change()
        df['volatility'] = df['returns'].rolling(20).std() * np.sqrt(252)
        df['momentum_20d'] = df['close'].pct_change(20) * 100
        df['ma20'] = df['close'].rolling(20).mean()
        df['ma60'] = df['close'].rolling(60).mean()
        df['price_vs_ma20'] = (df['close'] / df['ma20'] - 1) * 100
        df['price_vs_ma60'] = (df['close'] / df['ma60'] - 1) * 100
        
        for i in range(60, len(df)):
            obs = {
                'price_change': df['returns'].iloc[i] if not pd.isna(df['returns'].iloc[i]) else 0,
                'momentum_20d': df['momentum_20d'].iloc[i] if not pd.isna(df['momentum_20d'].iloc[i]) else 0,
                'price_vs_ma20': df['price_vs_ma20'].iloc[i] if not pd.isna(df['price_vs_ma20'].iloc[i]) else 0,
                'price_vs_ma60': df['price_vs_ma60'].iloc[i] if not pd.isna(df['price_vs_ma60'].iloc[i]) else 0,
                'volatility': df['volatility'].iloc[i] if not pd.isna(df['volatility'].iloc[i]) else 15,
                'volume_change': df['vol_change'].iloc[i] if not pd.isna(df['vol_change'].iloc[i]) else 0,
            }
            observations.append(obs)
        
        return observations
    
    def _emission_probability(self, obs: Dict[str, float], state: MarketState) -> float:
        """计算发射概率 - 使用所有核心观测变量"""
        params = self.EMISSION_PARAMS[state]
        prob = 1.0
        
        for key in self.CORE_OBS_KEYS:
            if key not in params:
                continue
            mean, std = params[key]
            value = obs.get(key, mean)
            z = (value - mean) / std
            p = np.exp(-0.5 * z**2) / (std * np.sqrt(2 * np.pi))
            prob *= max(p, 1e-10)
        
        return prob
    
    def _viterbi(self, observations: List[Dict]) -> List[MarketState]:
        """Viterbi算法（CPU版）"""
        T = len(observations)
        if T == 0:
            return [MarketState.SIDEWAYS]
        
        V = np.zeros((T, self.n_states))
        path = np.zeros((T, self.n_states), dtype=int)
        
        # 初始化
        for i, state in enumerate(self.states):
            V[0, i] = np.log(self.INITIAL_PROB[i] + 1e-10) + \
                      np.log(self._emission_probability(observations[0], state) + 1e-10)
        
        # 递推
        for t in range(1, T):
            for j in range(self.n_states):
                probs = V[t-1] + np.log(self.transition_matrix[:, j] + 1e-10)
                path[t, j] = np.argmax(probs)
                V[t, j] = probs[path[t, j]] + \
                          np.log(self._emission_probability(observations[t], self.states[j]) + 1e-10)
        
        # 回溯
        best_path = np.zeros(T, dtype=int)
        best_path[T-1] = np.argmax(V[T-1])
        
        for t in range(T-2, -1, -1):
            best_path[t] = path[t+1, best_path[t+1]]
        
        return [self.states[i] for i in best_path]
    
    def _viterbi_gpu(self, observations: List[Dict]) -> List[MarketState]:
        """Viterbi算法（GPU版，使用PyTorch）"""
        if not HAS_TORCH:
            return self._viterbi(observations)
        
        T = len(observations)
        if T == 0:
            return [MarketState.SIDEWAYS]
        
        device = torch.device('cuda')
        
        # 预计算所有发射概率
        emission_matrix = np.zeros((T, self.n_states))
        for t in range(T):
            for j, state in enumerate(self.states):
                emission_matrix[t, j] = np.log(self._emission_probability(observations[t], state) + 1e-10)
        
        # 转换到GPU
        V = torch.zeros((T, self.n_states), device=device)
        path = torch.zeros((T, self.n_states), dtype=torch.long, device=device)
        trans = torch.tensor(np.log(self.transition_matrix + 1e-10), device=device, dtype=torch.float32)
        emission = torch.tensor(emission_matrix, device=device, dtype=torch.float32)
        init_prob = torch.tensor(np.log(self.INITIAL_PROB + 1e-10), device=device, dtype=torch.float32)
        
        # 初始化
        V[0] = init_prob + emission[0]
        
        # 递推（GPU并行）
        for t in range(1, T):
            for j in range(self.n_states):
                probs = V[t-1] + trans[:, j]
                path[t, j] = torch.argmax(probs)
                V[t, j] = probs[path[t, j]] + emission[t, j]
        
        # 回溯
        best_path = torch.zeros(T, dtype=torch.long, device=device)
        best_path[T-1] = torch.argmax(V[T-1])
        
        for t in range(T-2, -1, -1):
            best_path[t] = path[t+1, best_path[t+1]]
        
        best_path = best_path.cpu().numpy()
        return [self.states[i] for i in best_path]
    
    def _calculate_state_probabilities(self, obs: Dict) -> Dict[str, float]:
        """计算状态后验概率"""
        probs = {}
        total = 0
        
        for state in self.states:
            p = self._emission_probability(obs, state)
            probs[state.value] = p
            total += p
        
        if total > 0:
            for key in probs:
                probs[key] /= total
        
        return probs


def test_fixed_hmm():
    """测试修复版HMM"""
    import jqdatasdk as jq
    import json
    
    with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
        cfg = json.load(f)
    jq.auth(cfg['username'], cfg['password'])
    
    df = jq.get_price('000001.XSHG', start_date='2023-09-01', end_date='2024-03-01',
                      frequency='daily', fields=['open', 'high', 'low', 'close', 'volume'])
    df.index = pd.to_datetime(df.index)
    
    print("=" * 60)
    print("🧪 测试修复版HMM")
    print("=" * 60)
    
    hmm = FixedHMM(use_gpu=False)
    
    # 测试几个关键日期
    dates = ['2024-01-25', '2024-02-06', '2024-02-08']
    
    for date in dates:
        idx = df.index.get_indexer([pd.to_datetime(date)], method='nearest')[0]
        if idx >= 60:
            window_df = df.iloc[:idx+1].copy()
            result = hmm.analyze(window_df)
            if result:
                print(f"\n{date}:")
                print(f"  状态: {result.current_state.value} ({result.current_state.to_english()})")
                print(f"  置信度: {result.confidence:.1%}")
                print(f"  概率分布: 牛={result.state_probability['牛市']:.1%}, "
                      f"熊={result.state_probability['熊市']:.1%}, "
                      f"震荡={result.state_probability['震荡']:.1%}")


if __name__ == "__main__":
    test_fixed_hmm()
