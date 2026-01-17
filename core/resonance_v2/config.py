# -*- coding: utf-8 -*-
"""
Resonance V2 Configuration
==========================

可配置参数，支持回测优化与实盘调整。

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class MarketState(Enum):
    """市场状态枚举"""
    RISK_ON = "risk_on"           # 牛市/风险偏好
    RISK_OFF = "risk_off"         # 熊市/风险规避
    SIDEWAYS = "sideways"         # 震荡
    HIGH_VOL = "high_vol"         # 高波动转换期


@dataclass
class ResonanceV2Config:
    """
    多周期共振 + HMM 系统配置
    
    所有参数可作为回测优化变量
    """
    
    # ========== HMM 参数 ==========
    n_hmm_states: int = 3                    # HMM状态数 (3: 牛/熊/震荡, 4: +高波动)
    hmm_covariance_type: str = "full"        # 协方差类型: full/diag/spherical/tied
    hmm_n_iter: int = 100                    # EM算法最大迭代次数
    hmm_random_state: int = 42               # 随机种子
    
    # ========== 训练参数 (Walk-Forward) V2: 优化后 ==========
    train_window: int = 252                  # 训练窗口 (约1年) - 更快响应市场变化
    test_window: int = 42                    # 测试窗口 (约2个月) - 更频繁更新
    retrain_frequency: int = 10              # 重训练频率 (约2周) - 更频繁重训练
    min_train_samples: int = 126             # 最小训练样本 (6个月) - 降低最小样本要求
    
    # ========== 周期参数 ==========
    slow_cycle: int = 60                     # 慢周期窗口 (日)
    fast_cycle: int = 10                     # 快周期窗口 (日)
    ma_short: int = 20                       # 短期均线
    ma_long: int = 60                        # 长期均线
    
    # ========== 共振权重 ==========
    trend_weight: float = 0.4                # 趋势共振权重
    vol_weight: float = 0.3                  # 波动共振权重
    risk_weight: float = 0.3                 # 风险共振权重
    
    # ========== 共振阈值 ==========
    resonance_threshold_full: float = 80     # 满仓阈值
    resonance_threshold_add: float = 60      # 加仓阈值
    resonance_threshold_trial: float = 40    # 试仓阈值
    
    # ========== 仓位管理 ==========
    position_risk_on: float = 1.0            # Risk-On 最大仓位
    position_risk_off: float = 0.3           # Risk-Off 最大仓位
    position_sideways: float = 0.6           # 震荡 最大仓位
    position_high_vol: float = 0.5           # 高波动 最大仓位
    
    # ========== 止损止盈 ==========
    hard_stop: float = 0.08                  # 硬止损 (8%)
    atr_stop_multiplier: float = 2.0         # ATR止损倍数
    trailing_stop_activate: float = 0.15     # 移动止损启动 (15%盈利后)
    trailing_stop_distance: float = 0.09     # 移动止损距离 (9%)
    
    # ========== 交易成本 (华泰证券标准) ==========
    commission_rate: float = 0.0001          # 佣金率 (万一)
    stamp_tax_rate: float = 0.001            # 印花税 (千一, 仅卖出)
    slippage: float = 0.001                  # 滑点 (0.1%)
    transfer_fee_rate: float = 0.00001       # 过户费
    min_commission: float = 5.0              # 最低佣金
    
    # ========== 观测变量配置 (V2: 增强版) ==========
    observation_features: List[str] = field(default_factory=lambda: [
        "log_return",      # 对数收益率
        "volatility",      # 实现波动率
        "trend_strength",  # 趋势强度 (MA斜率/ADX)
        "turnover_ratio",  # 换手率
        "momentum_20d",    # 20日动量 (新增)
        "rsi_deviation",   # RSI偏离度 (新增)
        "north_flow",      # 北向资金标准化 (新增)
        "breadth_score",   # 市场宽度得分 (新增)
    ])
    
    # ========== 数据源配置 ==========
    default_index: str = "000300.XSHG"       # 默认指数 (沪深300)
    benchmark_indices: List[str] = field(default_factory=lambda: [
        "000300.XSHG",  # 沪深300
        "000905.XSHG",  # 中证500
        "000852.XSHG",  # 中证1000
    ])
    
    def get_position_cap(self, state: MarketState) -> float:
        """根据市场状态返回仓位上限"""
        caps = {
            MarketState.RISK_ON: self.position_risk_on,
            MarketState.RISK_OFF: self.position_risk_off,
            MarketState.SIDEWAYS: self.position_sideways,
            MarketState.HIGH_VOL: self.position_high_vol,
        }
        return caps.get(state, self.position_sideways)
    
    def get_resonance_level(self, score: float) -> str:
        """根据共振分数返回仓位级别"""
        if score >= self.resonance_threshold_full:
            return "full"
        elif score >= self.resonance_threshold_add:
            return "add"
        elif score >= self.resonance_threshold_trial:
            return "trial"
        else:
            return "none"


# 默认配置实例
DEFAULT_CONFIG = ResonanceV2Config()
