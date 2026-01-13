# -*- coding: utf-8 -*-
"""
信号引擎 - 向量化选股条件
==========================

功能：
1. 生成entries布尔矩阵（T x N）：买入信号
2. 生成exits布尔矩阵（T x N）：卖出信号
3. 生成target_weights矩阵（T x N）：目标持仓权重
4. 支持周调仓逻辑

牛市策略信号条件：
- 买入信号：
  - mom_20d.between(min_mom, max_mom)
  - rel_position <= max_rel_position
  - vol_ratio >= min_volume_ratio
  - is_tradeable == True
- 卖出信号：
  - 止损：收益 < -stop_loss_pct
  - 止盈：收益 > take_profit_pct
  - 调仓日不在Top-K中
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd
import numpy as np

from .data_provider import DataMatrices
from .factors import FactorMatrices

logger = logging.getLogger(__name__)


@dataclass
class SignalParams:
    """信号参数
    
    牛市策略默认参数（使用已优化参数）
    
    参数来源：
    - 牛市策略优化: output/bull_market_optimization_vbt_v2/best_params_20260111_205302.json
    - 追涨策略优化: output/chase_rise_optimization/best_params_20260111_161516.json
    """
    # =========================================================================
    # 动量阈值（已优化）
    # =========================================================================
    min_mom_20d: float = -1.25   # 最小20日动量（几乎不限制）
    max_mom_20d: float = 25.0    # 最大20日动量（防止追高）
    
    # 相对位置阈值（已优化）
    max_rel_position: float = 80.0  # 最大相对位置（防止追高）
    
    # 量比阈值（已优化）
    min_vol_ratio: float = 1.0   # 最小量比（要求放量）
    
    # =========================================================================
    # 涨停因子阈值（来自追涨策略优化）
    # =========================================================================
    limit_up_threshold: float = 0.093     # 涨停判定阈值 (9.3%)
    vol_ratio_threshold_first: float = 2.5  # 首板量比阈值
    
    # =========================================================================
    # 突破因子阈值（来自追涨策略优化）
    # =========================================================================
    mom_5d_threshold_breakout: float = 16.0   # 突破动量阈值
    vol_ratio_threshold_breakout: float = 1.5 # 突破量比阈值
    breakout_ratio_min: float = 5.0           # 最小突破幅度（%）
    
    # =========================================================================
    # 量价齐升阈值（来自追涨策略优化，修复硬编码！）
    # =========================================================================
    mom_5d_threshold_volume: float = 10.0     # 量价齐升动量阈值
    vol_ratio_threshold_volume: float = 2.0   # 量价齐升量比阈值
    
    # =========================================================================
    # 资金流向因子阈值
    # =========================================================================
    min_flow_strength: float = 0.5   # 最小资金流向强度
    
    # =========================================================================
    # 信号评分阈值（来自追涨策略优化）
    # =========================================================================
    min_signal_score: float = 55.0   # 最小信号评分
    
    # =========================================================================
    # 持仓配置（已优化）
    # =========================================================================
    max_positions: int = 5           # 最大持仓数
    single_position_max: float = 0.2 # 单只股票最大权重
    
    # 调仓周期
    rebalance_period: int = 5        # 调仓周期（交易日），5=周调仓
    
    # =========================================================================
    # 止损止盈（已优化）
    # =========================================================================
    stop_loss_pct: float = -0.10           # 固定止损 (-10%)
    take_profit_pct: float = 0.30          # 固定止盈 (+30%)
    trailing_stop_pct: float = -0.09       # 移动止损回撤 (-9%)
    trailing_stop_trigger: float = 0.15    # 移动止损触发（盈利+15%后启用）
    time_stop_days: int = 20               # 时间止损（20个交易日）
    partial_profit_1_pct: float = 0.20     # 第一批止盈 (+20%)
    partial_profit_1_ratio: float = 0.50   # 第一批止盈比例（减仓50%）


# 信号类型枚举
class SignalType:
    """信号类型"""
    FIRST_LIMIT_UP = "FIRST_LIMIT_UP"        # 首板启动
    CONSECUTIVE_LIMIT = "CONSECUTIVE_LIMIT"  # 连板加速
    STRONG_BREAKOUT = "STRONG_BREAKOUT"      # 强势突破
    VOLUME_PRICE_RISE = "VOLUME_PRICE_RISE"  # 量价齐升
    NO_SIGNAL = "NO_SIGNAL"                  # 无信号


@dataclass 
class SignalMatrices:
    """信号矩阵容器
    
    所有矩阵格式: DataFrame(index=datetime, columns=symbol)
    """
    entries: pd.DataFrame      # 买入信号 (布尔矩阵)
    exits: pd.DataFrame        # 卖出信号 (布尔矩阵)
    scores: pd.DataFrame       # 评分矩阵 (用于排序)
    target_weights: pd.DataFrame  # 目标权重矩阵
    rebalance_mask: pd.Series     # 调仓日掩码
    
    @property
    def dates(self) -> pd.DatetimeIndex:
        return self.entries.index
    
    @property
    def symbols(self) -> List[str]:
        return list(self.entries.columns)


class SignalEngine:
    """信号引擎
    
    生成向量化交易信号
    
    使用示例：
    ```python
    engine = SignalEngine(params=SignalParams())
    signals = engine.generate_signals(data_matrices, factor_matrices)
    print(signals.entries.sum().sum())  # 总买入信号数
    ```
    """
    
    def __init__(self, params: Optional[SignalParams] = None):
        """
        初始化信号引擎
        
        Args:
            params: 信号参数
        """
        self.params = params or SignalParams()
    
    def generate_signals(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: Optional[SignalParams] = None,
    ) -> SignalMatrices:
        """
        生成交易信号
        
        Args:
            data: 数据矩阵
            factors: 因子矩阵
            params: 信号参数（覆盖默认）
        
        Returns:
            SignalMatrices: 信号矩阵
        """
        p = params or self.params
        
        # 1. 生成调仓日掩码
        rebalance_mask = self._generate_rebalance_mask(data.dates, p.rebalance_period)
        
        # 2. 生成买入条件
        entries = self._generate_entries(data, factors, p)
        
        # 3. 计算评分（用于排序）
        scores = self._generate_scores(factors)
        
        # 4. 生成目标权重
        target_weights = self._generate_target_weights(
            entries, scores, rebalance_mask, p
        )
        
        # 5. 生成卖出信号（暂时简化，vectorbt会自动处理）
        exits = pd.DataFrame(False, index=data.dates, columns=data.symbols)
        
        return SignalMatrices(
            entries=entries,
            exits=exits,
            scores=scores,
            target_weights=target_weights,
            rebalance_mask=rebalance_mask,
        )
    
    def _generate_rebalance_mask(
        self,
        dates: pd.DatetimeIndex,
        period: int,
    ) -> pd.Series:
        """
        生成调仓日掩码
        
        Args:
            dates: 日期索引
            period: 调仓周期
        
        Returns:
            布尔Series，True表示调仓日
        """
        mask = pd.Series(False, index=dates)
        
        # 简单实现：每隔period天调仓
        # 实际应用中可以改为"每周五"或"每月最后一个交易日"
        rebalance_indices = range(0, len(dates), period)
        mask.iloc[list(rebalance_indices)] = True
        
        return mask
    
    def _generate_entries(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: SignalParams,
    ) -> pd.DataFrame:
        """
        生成买入信号
        
        牛市策略买入条件（满足任一信号类型）：
        - 信号1: 首板启动 (is_first_limit_up & limit_up_vol_ratio > 2.5)
        - 信号2: 连板加速 (limit_up_count_5d >= 2)
        - 信号3: 强势突破 (breakout_60d & breakout_ratio > 5 & mom_5d > 16 & vol_ratio > 1.5)
        - 信号4: 量价齐升 (mom_5d > 10 & vol_ratio > 2.0 & flow_strength > 0.5)
        
        基础过滤条件：
        - rel_position <= max_rel_position（防止追高）
        - is_tradeable == True（可交易）
        """
        p = params
        
        # =====================================================================
        # 基础过滤条件
        # =====================================================================
        base_conditions = []
        
        # 相对位置条件（防止追高）
        if factors.rel_position is not None:
            pos_cond = factors.rel_position <= p.max_rel_position
            base_conditions.append(pos_cond)
        
        # 可交易条件
        if data.is_tradeable is not None:
            base_conditions.append(data.is_tradeable)
        
        # =====================================================================
        # 信号条件（满足任一即可）
        # =====================================================================
        signal_conditions = []
        
        # 信号1: 首板启动
        if factors.is_first_limit_up is not None and factors.limit_up_vol_ratio is not None:
            first_limit_cond = (
                factors.is_first_limit_up & 
                (factors.limit_up_vol_ratio > p.vol_ratio_threshold_first)
            )
            signal_conditions.append(first_limit_cond)
        
        # 信号2: 连板加速
        if factors.limit_up_count_5d is not None:
            consecutive_cond = factors.limit_up_count_5d >= 2
            signal_conditions.append(consecutive_cond)
        
        # 信号3: 强势突破
        if (factors.breakout_60d is not None and factors.breakout_ratio is not None and 
            factors.mom_5d is not None and factors.vol_ratio is not None):
            breakout_cond = (
                factors.breakout_60d & 
                (factors.breakout_ratio > p.breakout_ratio_min) & 
                (factors.mom_5d > p.mom_5d_threshold_breakout) & 
                (factors.vol_ratio > p.vol_ratio_threshold_breakout)
            )
            signal_conditions.append(breakout_cond)
        
        # 信号4: 量价齐升（使用参数化阈值，修复硬编码！）
        if factors.mom_5d is not None and factors.vol_ratio is not None:
            vol_price_cond = (
                (factors.mom_5d > p.mom_5d_threshold_volume) & 
                (factors.vol_ratio > p.vol_ratio_threshold_volume)
            )
            
            # 如果有资金流向因子，增加条件
            if factors.flow_strength is not None:
                vol_price_cond = vol_price_cond & (factors.flow_strength > p.min_flow_strength)
            
            signal_conditions.append(vol_price_cond)
        
        # =====================================================================
        # 备用条件：基础动量策略（如果没有任何高级信号因子）
        # =====================================================================
        if not signal_conditions:
            # 回退到基础动量策略
            if factors.mom_20d is not None:
                mom_cond = (
                    (factors.mom_20d >= p.min_mom_20d) & 
                    (factors.mom_20d <= p.max_mom_20d)
                )
                signal_conditions.append(mom_cond)
            
            if factors.vol_ratio is not None:
                vol_cond = factors.vol_ratio >= p.min_vol_ratio
                signal_conditions.append(vol_cond)
        
        # =====================================================================
        # 合并条件
        # =====================================================================
        # 信号条件：满足任一
        if signal_conditions:
            signal_mask = signal_conditions[0]
            for cond in signal_conditions[1:]:
                signal_mask = signal_mask | cond  # OR条件
        else:
            signal_mask = pd.DataFrame(True, index=data.dates, columns=data.symbols)
        
        # 基础条件：全部满足
        if base_conditions:
            base_mask = base_conditions[0]
            for cond in base_conditions[1:]:
                base_mask = base_mask & cond  # AND条件
        else:
            base_mask = pd.DataFrame(True, index=data.dates, columns=data.symbols)
        
        # 最终条件：基础条件 AND 信号条件
        entries = base_mask & signal_mask
        
        # 填充NaN为False
        entries = entries.fillna(False)
        
        logger.info(f"买入信号统计: 每日平均 {entries.sum(axis=1).mean():.1f} 只股票满足条件")
        
        return entries
    
    def _generate_scores(
        self,
        factors: FactorMatrices,
    ) -> pd.DataFrame:
        """
        生成多信号类型评分矩阵
        
        评分公式（按优先级）：
        1. 首板启动 (80-90分): is_first_limit_up & limit_up_vol_ratio > 2.5
        2. 连板加速 (70-80分): limit_up_count_5d >= 2
        3. 强势突破 (65-75分): breakout_60d & breakout_ratio > 5 & mom_5d > 16 & vol_ratio > 1.5
        4. 量价齐升 (60-70分): mom_5d > 10 & vol_ratio > 2.0 & flow_strength > 0.5
        """
        p = self.params
        
        # 获取因子引用
        is_first_limit_up = factors.is_first_limit_up
        limit_up_vol_ratio = factors.limit_up_vol_ratio
        limit_up_count_5d = factors.limit_up_count_5d
        breakout_60d = factors.breakout_60d
        breakout_ratio = factors.breakout_ratio
        mom_5d = factors.mom_5d
        mom_20d = factors.mom_20d
        vol_ratio = factors.vol_ratio
        flow_strength = factors.flow_strength
        
        # 初始化评分矩阵
        if mom_20d is not None:
            scores = pd.DataFrame(0.0, index=mom_20d.index, columns=mom_20d.columns)
        else:
            raise ValueError("需要mom_20d因子来生成评分")
        
        # =====================================================================
        # 信号1: 首板启动 (最高优先级, 80-90分)
        # =====================================================================
        if is_first_limit_up is not None and limit_up_vol_ratio is not None:
            first_limit_cond = is_first_limit_up & (limit_up_vol_ratio > p.vol_ratio_threshold_first)
            base_score = 80.0
            
            # 加分项：突破60日高点
            if breakout_60d is not None:
                bonus = breakout_60d.astype(float) * 10  # +10分
                first_limit_score = base_score + bonus
            else:
                first_limit_score = base_score
            
            scores = scores.where(~first_limit_cond, first_limit_score)
        
        # =====================================================================
        # 信号2: 连板加速 (70-80分)
        # =====================================================================
        if limit_up_count_5d is not None:
            consecutive_cond = (limit_up_count_5d >= 2) & (scores == 0)  # 只对未评分的
            base_score = 70.0
            bonus = (limit_up_count_5d - 2).clip(lower=0) * 5  # 每多一板+5分
            consecutive_score = base_score + bonus
            
            scores = scores.where(~consecutive_cond, consecutive_score.where(consecutive_cond, 0))
        
        # =====================================================================
        # 信号3: 强势突破 (65-75分)
        # =====================================================================
        if breakout_60d is not None and breakout_ratio is not None and mom_5d is not None and vol_ratio is not None:
            breakout_cond = (
                breakout_60d & 
                (breakout_ratio > p.breakout_ratio_min) & 
                (mom_5d > p.mom_5d_threshold_breakout) & 
                (vol_ratio > p.vol_ratio_threshold_breakout) &
                (scores == 0)  # 只对未评分的
            )
            base_score = 65.0
            
            # 加分项：突破幅度
            bonus = (breakout_ratio - p.breakout_ratio_min).clip(lower=0, upper=10)  # 最多+10分
            breakout_score = base_score + bonus
            
            scores = scores.where(~breakout_cond, breakout_score.where(breakout_cond, 0))
        
        # =====================================================================
        # 信号4: 量价齐升 (60-70分)
        # =====================================================================
        if mom_5d is not None and vol_ratio is not None:
            vol_price_cond = (
                (mom_5d > 10) & 
                (vol_ratio > 2.0) &
                (scores == 0)  # 只对未评分的
            )
            
            # 加分项：资金流向
            base_score = 60.0
            if flow_strength is not None:
                flow_cond = flow_strength > p.min_flow_strength
                bonus = flow_cond.astype(float) * 5  # 资金流向强则+5分
                vol_price_score = base_score + bonus
            else:
                vol_price_score = base_score
            
            scores = scores.where(~vol_price_cond, vol_price_score.where(vol_price_cond, 0))
        
        # =====================================================================
        # 补充评分：对于未匹配任何信号的，使用动量作为基础分
        # =====================================================================
        no_signal = scores == 0
        if mom_20d is not None:
            # 动量评分：0-50分，动量越高分越高（但不超过50以确保低于信号评分）
            mom_score = (mom_20d.clip(lower=0, upper=50) / 50) * 50
            scores = scores.where(~no_signal, mom_score)
        
        logger.info(f"评分统计: min={scores.min().min():.1f}, max={scores.max().max():.1f}, "
                   f"mean={scores.mean().mean():.1f}")
        
        return scores
    
    def _generate_target_weights(
        self,
        entries: pd.DataFrame,
        scores: pd.DataFrame,
        rebalance_mask: pd.Series,
        params: SignalParams,
    ) -> pd.DataFrame:
        """
        生成目标权重矩阵
        
        在调仓日：选择Top-K股票，等权分配
        非调仓日：保持前一天权重
        """
        target_weights = pd.DataFrame(0.0, index=entries.index, columns=entries.columns)
        
        n_positions = params.max_positions
        single_max = params.single_position_max
        
        prev_weights = None
        
        for i, date in enumerate(target_weights.index):
            if rebalance_mask.iloc[i]:
                # 调仓日：重新选股
                today_entries = entries.loc[date]
                today_scores = scores.loc[date]
                
                # 只考虑满足买入条件的股票
                valid_scores = today_scores.where(today_entries, np.nan)
                
                # 排序选择Top-K
                top_k = valid_scores.nlargest(n_positions)
                top_stocks = top_k.dropna().index.tolist()
                
                if top_stocks:
                    # 等权分配
                    weight = min(1.0 / len(top_stocks), single_max)
                    for stock in top_stocks:
                        target_weights.loc[date, stock] = weight
                
                prev_weights = target_weights.loc[date].copy()
            else:
                # 非调仓日：保持前一天权重
                if prev_weights is not None:
                    target_weights.loc[date] = prev_weights
        
        return target_weights


def generate_weekly_rebalance_signals(
    data: DataMatrices,
    factors: FactorMatrices,
    params: Optional[SignalParams] = None,
) -> SignalMatrices:
    """
    便捷函数：生成周调仓信号
    
    Args:
        data: 数据矩阵
        factors: 因子矩阵
        params: 信号参数
    
    Returns:
        SignalMatrices
    """
    if params is None:
        params = SignalParams(rebalance_period=5)  # 周调仓
    
    engine = SignalEngine(params=params)
    return engine.generate_signals(data, factors, params)
