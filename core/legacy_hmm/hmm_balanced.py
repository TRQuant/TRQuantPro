# -*- coding: utf-8 -*-
"""
平衡版HMM V4.0 - 解决震荡偏见问题
=================================

核心思路：
- 原版HMM偏向震荡（75%预测震荡）-> 牛熊识别差
- V3版HMM过于激进（几乎不预测震荡）-> 准确率低

V4解决方案：
1. 使用原版HMM作为基础（稳定性）
2. 添加动量修正层（提高牛熊识别）
3. 使用贝叶斯后验调整（平衡保守和激进）
4. 引入信号确认机制（减少误判）

作者: TRQuant Team
版本: V4.0
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


@dataclass
class HMMResultV4:
    """HMM V4分析结果"""
    current_state: MarketState
    state_probability: Dict[str, float]
    transition_prob: Dict[str, float]
    confidence: float
    history_states: List[str]
    
    # V4增强字段
    state_duration: int = 0
    regime_change_signal: bool = False
    predicted_next_state: Optional[str] = None
    observation_scores: Dict[str, float] = field(default_factory=dict)
    analysis_date: str = ""
    
    # V4特有
    base_state: str = ""  # 原版HMM基础状态
    correction_applied: str = ""  # 应用的修正类型
    momentum_score: float = 0.0  # 综合动量得分
    signal_strength: int = 0  # 信号强度(0-4)
    
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
            'base_state': self.base_state,
            'correction_applied': self.correction_applied,
            'momentum_score': self.momentum_score,
            'signal_strength': self.signal_strength,
        }


class BalancedHMM:
    """
    平衡版HMM V4.0
    
    核心策略：
    1. 原版HMM提供基础状态判断
    2. 动量分析提供修正信号
    3. 贝叶斯后验调整最终概率
    4. 信号确认机制减少误判
    """
    
    STATES = [MarketState.BULL, MarketState.BEAR, MarketState.SIDEWAYS]
    
    # 动量信号阈值（用于修正震荡判断）
    MOMENTUM_THRESHOLDS = {
        "strong_bull": {  # 强牛市信号
            "momentum_5d": 3.0,     # 5日动量>3%
            "momentum_20d": 8.0,    # 20日动量>8%
            "weekly_return": 2.5,   # 周收益>2.5%
            "price_vs_ma20": 3.0,   # MA20偏离>3%
        },
        "weak_bull": {  # 弱牛市信号
            "momentum_5d": 1.0,
            "momentum_20d": 3.0,
            "weekly_return": 1.0,
            "price_vs_ma20": 1.0,
        },
        "strong_bear": {  # 强熊市信号
            "momentum_5d": -3.0,
            "momentum_20d": -8.0,
            "weekly_return": -2.5,
            "price_vs_ma20": -3.0,
        },
        "weak_bear": {  # 弱熊市信号
            "momentum_5d": -1.0,
            "momentum_20d": -3.0,
            "weekly_return": -1.0,
            "price_vs_ma20": -1.0,
        },
    }
    
    # 修正强度 (V4.1 优化)
    CORRECTION_STRENGTHS = {
        "strong_bull": 0.45,   # 强牛市修正45%概率 (增强)
        "weak_bull": 0.35,     # 弱牛市修正35%概率 (增强)
        "strong_bear": 0.45,
        "weak_bear": 0.35,
        "none": 0.0,
    }
    
    def __init__(self, correction_mode: str = "balanced"):
        """
        初始化平衡版HMM
        
        Args:
            correction_mode: 修正模式
                - "conservative": 保守（仅修正强信号）
                - "balanced": 平衡（默认）
                - "aggressive": 激进（积极修正）
        """
        self.correction_mode = correction_mode
        self._history: List[HMMResultV4] = []
        
        # 导入原版HMM
        from core.trend_ml import SimpleHMM
        self._base_hmm = SimpleHMM(use_astock_params=True)
        
    def analyze(self, df: pd.DataFrame) -> Optional[HMMResultV4]:
        """
        分析市场状态 V4
        
        流程：
        1. 原版HMM获取基础状态
        2. 计算动量指标
        3. 判断是否需要修正
        4. 应用贝叶斯后验调整
        5. 确定最终状态
        """
        try:
            if df is None or len(df) < 25:
                logger.warning("数据不足")
                return None
            
            # Step 1: 获取原版HMM基础判断
            base_result = self._base_hmm.analyze(df)
            if base_result is None:
                return None
            
            base_state = base_result.current_state
            base_probs = base_result.state_probability.copy()
            
            # Step 2: 计算动量指标
            momentum_indicators = self._calculate_momentum_indicators(df)
            
            # Step 3: 判断信号类型和强度
            signal_type, signal_strength = self._detect_signal(momentum_indicators)
            
            # Step 4: 决定是否修正
            correction_type = self._decide_correction(base_state, signal_type, signal_strength)
            
            # Step 5: 应用修正（贝叶斯后验调整）
            adjusted_probs = self._apply_correction(base_probs, correction_type, momentum_indicators)
            
            # Step 6: 确定最终状态
            final_state = self._determine_final_state(adjusted_probs)
            
            # 计算转移概率
            state_idx = self.STATES.index(final_state)
            base_trans = base_result.transition_prob
            
            # 计算置信度
            confidence = self._calculate_confidence(adjusted_probs, signal_strength)
            
            # 其他信息
            momentum_score = self._calculate_momentum_score(momentum_indicators)
            state_duration = self._calculate_state_duration(base_result.history_states, final_state.value)
            
            result = HMMResultV4(
                current_state=final_state,
                state_probability=adjusted_probs,
                transition_prob=base_trans,
                confidence=confidence,
                history_states=base_result.history_states,
                state_duration=state_duration,
                regime_change_signal=base_result.regime_change_signal,
                predicted_next_state=base_result.predicted_next_state,
                observation_scores=self._get_observation_scores(momentum_indicators),
                analysis_date=date.today().strftime("%Y-%m-%d"),
                base_state=base_state.value,
                correction_applied=correction_type,
                momentum_score=momentum_score,
                signal_strength=signal_strength,
            )
            
            self._history.append(result)
            if len(self._history) > 500:
                self._history = self._history[-500:]
            
            return result
            
        except Exception as e:
            logger.error(f"HMM V4分析失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _calculate_momentum_indicators(self, df: pd.DataFrame) -> Dict[str, float]:
        """计算动量指标"""
        close = df['close']
        volume = df['volume']
        
        # 各种动量指标
        indicators = {}
        
        # 5日动量
        if len(close) >= 6:
            indicators['momentum_5d'] = (close.iloc[-1] / close.iloc[-6] - 1) * 100
        else:
            indicators['momentum_5d'] = 0
        
        # 20日动量
        if len(close) >= 21:
            indicators['momentum_20d'] = (close.iloc[-1] / close.iloc[-21] - 1) * 100
        else:
            indicators['momentum_20d'] = 0
        
        # 周收益（5日）
        indicators['weekly_return'] = indicators['momentum_5d']
        
        # MA偏离
        ma20 = close.rolling(20).mean()
        if len(ma20) >= 20 and ma20.iloc[-1] > 0:
            indicators['price_vs_ma20'] = (close.iloc[-1] / ma20.iloc[-1] - 1) * 100
        else:
            indicators['price_vs_ma20'] = 0
        
        # MA60偏离
        if len(close) >= 60:
            ma60 = close.rolling(60).mean()
            if ma60.iloc[-1] > 0:
                indicators['price_vs_ma60'] = (close.iloc[-1] / ma60.iloc[-1] - 1) * 100
            else:
                indicators['price_vs_ma60'] = 0
        else:
            indicators['price_vs_ma60'] = 0
        
        # 加速度（动量的变化）
        if len(close) >= 11:
            prev_momentum = (close.iloc[-6] / close.iloc[-11] - 1) * 100
            indicators['acceleration'] = indicators['momentum_5d'] - prev_momentum
        else:
            indicators['acceleration'] = 0
        
        # 波动率
        returns = close.pct_change()
        if len(returns) >= 20:
            indicators['volatility'] = returns.rolling(20).std().iloc[-1] * np.sqrt(252) * 100
        else:
            indicators['volatility'] = 15
        
        return indicators
    
    def _detect_signal(self, indicators: Dict[str, float]) -> Tuple[str, int]:
        """
        检测信号类型和强度
        
        Returns:
            (signal_type, signal_strength)
            signal_type: "strong_bull", "weak_bull", "strong_bear", "weak_bear", "none"
            signal_strength: 0-4 (满足的条件数)
        """
        # 检测强牛市信号
        strong_bull_count = 0
        for key, threshold in self.MOMENTUM_THRESHOLDS["strong_bull"].items():
            if indicators.get(key, 0) >= threshold:
                strong_bull_count += 1
        
        if strong_bull_count >= 3:
            return "strong_bull", strong_bull_count
        
        # 检测弱牛市信号
        weak_bull_count = 0
        for key, threshold in self.MOMENTUM_THRESHOLDS["weak_bull"].items():
            if indicators.get(key, 0) >= threshold:
                weak_bull_count += 1
        
        if weak_bull_count >= 3:
            return "weak_bull", weak_bull_count
        
        # 检测强熊市信号
        strong_bear_count = 0
        for key, threshold in self.MOMENTUM_THRESHOLDS["strong_bear"].items():
            if indicators.get(key, 0) <= threshold:
                strong_bear_count += 1
        
        if strong_bear_count >= 3:
            return "strong_bear", strong_bear_count
        
        # 检测弱熊市信号
        weak_bear_count = 0
        for key, threshold in self.MOMENTUM_THRESHOLDS["weak_bear"].items():
            if indicators.get(key, 0) <= threshold:
                weak_bear_count += 1
        
        if weak_bear_count >= 3:
            return "weak_bear", weak_bear_count
        
        return "none", 0
    
    def _decide_correction(self, base_state: MarketState, signal_type: str, signal_strength: int) -> str:
        """决定是否需要修正"""
        # 如果原版判断已经和信号一致，不需要修正
        if base_state == MarketState.BULL and signal_type in ["strong_bull", "weak_bull"]:
            return "none"
        if base_state == MarketState.BEAR and signal_type in ["strong_bear", "weak_bear"]:
            return "none"
        
        # 根据修正模式决定
        if self.correction_mode == "conservative":
            # 保守模式：只修正强信号
            if signal_type in ["strong_bull", "strong_bear"]:
                return signal_type
        elif self.correction_mode == "balanced":
            # 平衡模式：修正所有信号
            if signal_strength >= 2:  # 至少2个条件满足
                return signal_type
        elif self.correction_mode == "aggressive":
            # 激进模式：只要有信号就修正
            return signal_type
        
        return "none"
    
    def _apply_correction(self, base_probs: Dict[str, float], correction_type: str, 
                         indicators: Dict[str, float]) -> Dict[str, float]:
        """应用贝叶斯后验修正"""
        if correction_type == "none":
            return base_probs
        
        adjusted = base_probs.copy()
        strength = self.CORRECTION_STRENGTHS.get(correction_type, 0)
        
        if correction_type in ["strong_bull", "weak_bull"]:
            # 增加牛市概率
            boost = strength
            adjusted["牛市"] = min(0.85, adjusted["牛市"] + boost)
            
            # 相应减少其他概率
            remaining = 1.0 - adjusted["牛市"]
            old_remaining = adjusted["熊市"] + adjusted["震荡"]
            if old_remaining > 0:
                adjusted["熊市"] = adjusted["熊市"] / old_remaining * remaining
                adjusted["震荡"] = adjusted["震荡"] / old_remaining * remaining
            else:
                adjusted["熊市"] = remaining / 2
                adjusted["震荡"] = remaining / 2
                
        elif correction_type in ["strong_bear", "weak_bear"]:
            # 增加熊市概率
            boost = strength
            adjusted["熊市"] = min(0.85, adjusted["熊市"] + boost)
            
            remaining = 1.0 - adjusted["熊市"]
            old_remaining = adjusted["牛市"] + adjusted["震荡"]
            if old_remaining > 0:
                adjusted["牛市"] = adjusted["牛市"] / old_remaining * remaining
                adjusted["震荡"] = adjusted["震荡"] / old_remaining * remaining
            else:
                adjusted["牛市"] = remaining / 2
                adjusted["震荡"] = remaining / 2
        
        return adjusted
    
    def _determine_final_state(self, probs: Dict[str, float]) -> MarketState:
        """确定最终状态"""
        max_prob = 0
        final_state = MarketState.SIDEWAYS
        
        for state in self.STATES:
            if probs.get(state.value, 0) > max_prob:
                max_prob = probs[state.value]
                final_state = state
        
        return final_state
    
    def _calculate_confidence(self, probs: Dict[str, float], signal_strength: int) -> float:
        """计算置信度"""
        max_prob = max(probs.values())
        
        # 信号强度加成
        strength_bonus = signal_strength * 0.05
        
        # 概率差异加成
        sorted_probs = sorted(probs.values(), reverse=True)
        if len(sorted_probs) >= 2:
            gap_bonus = (sorted_probs[0] - sorted_probs[1]) * 0.3
        else:
            gap_bonus = 0
        
        confidence = min(0.95, max_prob + strength_bonus + gap_bonus)
        return max(0.3, confidence)
    
    def _calculate_momentum_score(self, indicators: Dict[str, float]) -> float:
        """计算综合动量得分"""
        score = 0.0
        
        # 各指标权重
        score += indicators.get('momentum_5d', 0) * 10
        score += indicators.get('momentum_20d', 0) * 5
        score += indicators.get('price_vs_ma20', 0) * 8
        score += indicators.get('acceleration', 0) * 15
        
        return float(np.clip(score, -100, 100))
    
    def _calculate_state_duration(self, history: List[str], current_state: str) -> int:
        """计算状态持续天数"""
        duration = 1
        for i in range(len(history) - 1, -1, -1):
            if history[i] == current_state:
                duration += 1
            else:
                break
        return duration
    
    def _get_observation_scores(self, indicators: Dict[str, float]) -> Dict[str, float]:
        """获取观测变量得分"""
        scores = {}
        scores['momentum_5d'] = np.clip(indicators.get('momentum_5d', 0) * 15, -100, 100)
        scores['momentum_20d'] = np.clip(indicators.get('momentum_20d', 0) * 8, -100, 100)
        scores['ma20_deviation'] = np.clip(indicators.get('price_vs_ma20', 0) * 10, -100, 100)
        scores['acceleration'] = np.clip(indicators.get('acceleration', 0) * 30, -100, 100)
        return scores


# ============== 测试函数 ==============

def test_balanced_hmm():
    """测试平衡版HMM"""
    import sys
    sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")
    
    print("=" * 60)
    print("平衡版HMM V4.0 测试")
    print("=" * 60)
    
    import json
    import jqdatasdk as jq
    
    with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
        config = json.load(f)
    jq.auth(config['username'], config['password'])
    print("✅ JQData认证成功")
    
    # 获取最近数据
    from datetime import datetime
    end_date = datetime.now().strftime('%Y-%m-%d')
    df = jq.get_price(
        "000300.XSHG",
        end_date=end_date,
        count=200,
        frequency='daily',
        fields=['open', 'high', 'low', 'close', 'volume']
    )
    print(f"✅ 获取数据: {len(df)} 条")
    
    # 测试V4
    hmm_v4 = BalancedHMM(correction_mode="balanced")
    result = hmm_v4.analyze(df)
    
    if result:
        print(f"\n【V4分析结果】")
        print(f"当前状态: {result.current_state.value}")
        print(f"基础状态: {result.base_state}")
        print(f"修正类型: {result.correction_applied}")
        print(f"信号强度: {result.signal_strength}/4")
        print(f"状态概率:")
        print(f"  牛市: {result.state_probability['牛市']:.2%}")
        print(f"  震荡: {result.state_probability['震荡']:.2%}")
        print(f"  熊市: {result.state_probability['熊市']:.2%}")
        print(f"置信度: {result.confidence:.2%}")
        print(f"动量得分: {result.momentum_score:.1f}")
    
    # 对比原版
    from core.trend_ml import SimpleHMM
    hmm_old = SimpleHMM(use_astock_params=True)
    result_old = hmm_old.analyze(df)
    
    if result_old:
        print(f"\n【原版HMM】")
        print(f"当前状态: {result_old.current_state.value}")
        print(f"状态概率:")
        print(f"  牛市: {result_old.state_probability.get('牛市', 0):.2%}")
        print(f"  震荡: {result_old.state_probability.get('震荡', 0):.2%}")
        print(f"  熊市: {result_old.state_probability.get('熊市', 0):.2%}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_balanced_hmm()
