# -*- coding: utf-8 -*-
"""
多因子信号引擎 V7.0
==================

功能:
1. 因子权重动态调整（根据主题周期）
2. 信号组合优化（多信号加权融合）
3. 主线强度与个股信号融合
4. 支持不同周期的因子配置

信号类型:
- FIRST_LIMIT_UP: 首板启动
- CONSECUTIVE_LIMIT: 连板加速
- STRONG_BREAKOUT: 强势突破
- VOLUME_PRICE_RISE: 量价齐升

作者: TRQuant Team
版本: V7.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np

# 导入依赖
from .data_provider import DataMatrices
from .factors import FactorMatrices

logger = logging.getLogger(__name__)


# ============== 数据结构 ==============

class SignalType(Enum):
    """信号类型"""
    FIRST_LIMIT_UP = "first_limit_up"        # 首板启动
    CONSECUTIVE_LIMIT = "consecutive_limit"  # 连板加速
    STRONG_BREAKOUT = "strong_breakout"      # 强势突破
    VOLUME_PRICE_RISE = "vol_price_rise"     # 量价齐升
    NO_SIGNAL = "no_signal"                  # 无信号


class CombineMode(Enum):
    """信号组合模式"""
    WEIGHTED = "weighted"  # 加权融合
    OR = "or"              # 满足任一
    AND = "and"            # 满足全部


@dataclass
class SignalParamsV7:
    """V7信号参数（支持周期自适应）"""
    
    # =========================================================================
    # 基础动量阈值
    # =========================================================================
    min_mom_20d: float = -1.25   # 最小20日动量
    max_mom_20d: float = 25.0    # 最大20日动量
    max_rel_position: float = 80.0  # 最大相对位置
    min_vol_ratio: float = 1.0   # 最小量比
    
    # =========================================================================
    # 涨停因子阈值
    # =========================================================================
    limit_up_threshold: float = 0.093      # 涨停判定阈值 (9.3%)
    vol_ratio_threshold_first: float = 2.5 # 首板量比阈值
    consecutive_limit_min: int = 2         # 连板最小天数
    
    # =========================================================================
    # 突破因子阈值
    # =========================================================================
    mom_5d_threshold_breakout: float = 16.0   # 突破动量阈值
    vol_ratio_threshold_breakout: float = 1.5 # 突破量比阈值
    breakout_ratio_min: float = 5.0           # 最小突破幅度
    
    # =========================================================================
    # 量价齐升阈值
    # =========================================================================
    mom_5d_threshold_volume: float = 10.0     # 量价齐升动量阈值
    vol_ratio_threshold_volume: float = 2.0   # 量价齐升量比阈值
    min_flow_strength: float = 0.5            # 最小资金流向强度
    
    # =========================================================================
    # 信号配置
    # =========================================================================
    min_signal_score: float = 55.0   # 最小信号评分
    combine_mode: str = "weighted"   # 信号组合模式: weighted/or/and
    
    # 信号权重（根据周期调整）
    signal_weights: Dict[str, float] = field(default_factory=lambda: {
        SignalType.FIRST_LIMIT_UP.value: 0.25,
        SignalType.CONSECUTIVE_LIMIT.value: 0.25,
        SignalType.STRONG_BREAKOUT.value: 0.25,
        SignalType.VOLUME_PRICE_RISE.value: 0.25,
    })
    
    # =========================================================================
    # 持仓配置
    # =========================================================================
    max_positions: int = 5           # 最大持仓数
    single_position_max: float = 0.2 # 单只股票最大权重
    rebalance_period: int = 5        # 调仓周期
    
    # =========================================================================
    # 主线融合配置
    # =========================================================================
    mainline_weight: float = 0.6     # 主线得分权重
    signal_weight: float = 0.4       # 个股信号权重
    use_mainline_fusion: bool = True # 是否使用主线融合


@dataclass
class SignalMatricesV7:
    """V7信号矩阵容器"""
    entries: pd.DataFrame           # 买入信号 (布尔矩阵)
    exits: pd.DataFrame             # 卖出信号 (布尔矩阵)
    scores: pd.DataFrame            # 评分矩阵
    target_weights: pd.DataFrame    # 目标权重矩阵
    rebalance_mask: pd.Series       # 调仓日掩码
    
    # V7新增
    signal_types: pd.DataFrame      # 信号类型矩阵
    signal_strengths: pd.DataFrame  # 信号强度矩阵
    mainline_scores: Optional[pd.DataFrame] = None  # 主线得分矩阵
    combined_scores: Optional[pd.DataFrame] = None  # 融合得分矩阵
    
    @property
    def dates(self) -> pd.DatetimeIndex:
        return self.entries.index
    
    @property
    def symbols(self) -> List[str]:
        return list(self.entries.columns)


# ============== 信号引擎V7 ==============

class SignalEngineV7:
    """
    多因子信号引擎V7
    
    特性:
    1. 因子权重动态调整（根据主题周期）
    2. 信号组合优化（多信号加权融合）
    3. 主线强度与个股信号融合
    """
    
    def __init__(self, params: Optional[SignalParamsV7] = None):
        """
        初始化信号引擎V7
        
        Args:
            params: 信号参数
        """
        self.params = params or SignalParamsV7()
        logger.info("SignalEngineV7 初始化完成")
    
    def generate_signals(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: Optional[SignalParamsV7] = None,
        mainline_scores: Optional[pd.DataFrame] = None,
    ) -> SignalMatricesV7:
        """
        生成交易信号
        
        Args:
            data: 数据矩阵
            factors: 因子矩阵
            params: 信号参数（覆盖默认）
            mainline_scores: 主线得分矩阵（可选）
        
        Returns:
            SignalMatricesV7: 信号矩阵
        """
        p = params or self.params
        
        # 1. 生成调仓日掩码
        rebalance_mask = self._generate_rebalance_mask(data.dates, p.rebalance_period)
        
        # 2. 计算各信号类型的强度
        signal_strengths = self._calculate_signal_strengths(data, factors, p)
        
        # 3. 确定信号类型
        signal_types = self._determine_signal_types(signal_strengths)
        
        # 4. 组合信号生成买入条件
        entries, scores = self._combine_signals(signal_strengths, p)
        
        # 5. 融合主线得分
        if mainline_scores is not None and p.use_mainline_fusion:
            combined_scores = self._fuse_mainline_scores(scores, mainline_scores, p)
        else:
            combined_scores = scores
        
        # 6. 生成目标权重
        target_weights = self._generate_target_weights(
            entries, combined_scores, rebalance_mask, p
        )
        
        # 7. 生成卖出信号
        exits = self._generate_exits(data, factors, p)
        
        return SignalMatricesV7(
            entries=entries,
            exits=exits,
            scores=scores,
            target_weights=target_weights,
            rebalance_mask=rebalance_mask,
            signal_types=signal_types,
            signal_strengths=signal_strengths,
            mainline_scores=mainline_scores,
            combined_scores=combined_scores,
        )
    
    def _generate_rebalance_mask(
        self,
        dates: pd.DatetimeIndex,
        period: int,
    ) -> pd.Series:
        """生成调仓日掩码"""
        mask = pd.Series(False, index=dates)
        rebalance_indices = range(0, len(dates), period)
        mask.iloc[list(rebalance_indices)] = True
        return mask
    
    def _calculate_signal_strengths(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: SignalParamsV7,
    ) -> Dict[str, pd.DataFrame]:
        """
        计算各信号类型的强度
        
        Returns:
            Dict[信号类型, 强度矩阵(0-100)]
        """
        p = params
        strengths = {}
        
        # 创建空矩阵模板
        template = pd.DataFrame(0.0, index=data.dates, columns=data.symbols)
        
        # =====================================================================
        # 信号1: 首板启动强度
        # =====================================================================
        first_limit_strength = template.copy()
        
        if factors.is_first_limit_up is not None:
            # 首板 + 放量
            is_first = factors.is_first_limit_up.fillna(False)
            vol_ratio = factors.limit_up_vol_ratio if factors.limit_up_vol_ratio is not None else factors.vol_ratio
            
            if vol_ratio is not None:
                vol_ratio = vol_ratio.fillna(1.0)
                # 强度计算: 基础分50 + 量比加分(最多50)
                strength = is_first.astype(float) * (50 + np.minimum(vol_ratio / p.vol_ratio_threshold_first * 50, 50))
                first_limit_strength = strength.clip(0, 100)
        
        strengths[SignalType.FIRST_LIMIT_UP.value] = first_limit_strength
        
        # =====================================================================
        # 信号2: 连板加速强度
        # =====================================================================
        consecutive_strength = template.copy()
        
        if factors.limit_up_count_5d is not None:
            limit_count = factors.limit_up_count_5d.fillna(0)
            # 连板数量决定强度: 2板=60, 3板=80, 4板+=100
            strength = np.where(limit_count >= 4, 100,
                       np.where(limit_count >= 3, 80,
                       np.where(limit_count >= 2, 60, 0)))
            consecutive_strength = pd.DataFrame(strength, index=data.dates, columns=data.symbols)
        
        strengths[SignalType.CONSECUTIVE_LIMIT.value] = consecutive_strength
        
        # =====================================================================
        # 信号3: 强势突破强度
        # =====================================================================
        breakout_strength = template.copy()
        
        if factors.breakout_60d is not None and factors.mom_5d is not None:
            is_breakout = factors.breakout_60d.fillna(False)
            mom_5d = factors.mom_5d.fillna(0)
            vol_ratio = factors.vol_ratio.fillna(1.0) if factors.vol_ratio is not None else pd.DataFrame(1.0, index=data.dates, columns=data.symbols)
            
            # 突破 + 动量 + 量比 综合
            base_strength = is_breakout.astype(float) * 40
            mom_bonus = np.minimum(mom_5d / p.mom_5d_threshold_breakout * 30, 30)
            vol_bonus = np.minimum(vol_ratio / p.vol_ratio_threshold_breakout * 30, 30)
            
            breakout_strength = (base_strength + mom_bonus + vol_bonus).clip(0, 100)
        
        strengths[SignalType.STRONG_BREAKOUT.value] = breakout_strength
        
        # =====================================================================
        # 信号4: 量价齐升强度
        # =====================================================================
        vol_price_strength = template.copy()
        
        if factors.mom_5d is not None:
            mom_5d = factors.mom_5d.fillna(0)
            vol_ratio = factors.vol_ratio.fillna(1.0) if factors.vol_ratio is not None else pd.DataFrame(1.0, index=data.dates, columns=data.symbols)
            
            # 动量得分
            mom_score = np.minimum(mom_5d / p.mom_5d_threshold_volume * 50, 50)
            # 量比得分
            vol_score = np.minimum(vol_ratio / p.vol_ratio_threshold_volume * 50, 50)
            
            vol_price_strength = (mom_score + vol_score).clip(0, 100)
            
            # 如果有资金流向因子，额外加分
            if factors.flow_strength is not None:
                flow = factors.flow_strength.fillna(0)
                flow_bonus = np.minimum(flow / p.min_flow_strength * 20, 20)
                vol_price_strength = (vol_price_strength + flow_bonus).clip(0, 100)
        
        strengths[SignalType.VOLUME_PRICE_RISE.value] = vol_price_strength
        
        return strengths
    
    def _determine_signal_types(
        self,
        signal_strengths: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """确定每个股票的主要信号类型"""
        # 取强度最大的信号类型
        if not signal_strengths:
            return pd.DataFrame()
        
        # 堆叠所有信号强度
        first_df = list(signal_strengths.values())[0]
        signal_types = pd.DataFrame(
            SignalType.NO_SIGNAL.value,
            index=first_df.index,
            columns=first_df.columns
        )
        
        max_strength = pd.DataFrame(0.0, index=first_df.index, columns=first_df.columns)
        
        for signal_type, strength_df in signal_strengths.items():
            mask = strength_df > max_strength
            signal_types = signal_types.where(~mask, signal_type)
            max_strength = max_strength.where(~mask, strength_df)
        
        return signal_types
    
    def _combine_signals(
        self,
        signal_strengths: Dict[str, pd.DataFrame],
        params: SignalParamsV7,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        组合信号生成买入条件和评分
        
        Returns:
            (entries, scores)
        """
        if not signal_strengths:
            return pd.DataFrame(), pd.DataFrame()
        
        first_df = list(signal_strengths.values())[0]
        
        if params.combine_mode == "weighted":
            # 加权融合模式
            combined_score = pd.DataFrame(0.0, index=first_df.index, columns=first_df.columns)
            
            for signal_type, strength_df in signal_strengths.items():
                weight = params.signal_weights.get(signal_type, 0.25)
                combined_score += strength_df * weight
            
            # 满足最小评分即为买入信号
            entries = combined_score >= params.min_signal_score
            scores = combined_score
            
        elif params.combine_mode == "or":
            # 满足任一信号即可
            entries = pd.DataFrame(False, index=first_df.index, columns=first_df.columns)
            scores = pd.DataFrame(0.0, index=first_df.index, columns=first_df.columns)
            
            for signal_type, strength_df in signal_strengths.items():
                mask = strength_df >= params.min_signal_score
                entries = entries | mask
                scores = scores.where(~mask, np.maximum(scores, strength_df))
            
        else:  # and
            # 满足全部信号
            entries = pd.DataFrame(True, index=first_df.index, columns=first_df.columns)
            scores = pd.DataFrame(0.0, index=first_df.index, columns=first_df.columns)
            
            for signal_type, strength_df in signal_strengths.items():
                mask = strength_df >= params.min_signal_score
                entries = entries & mask
                scores += strength_df
        
        return entries, scores
    
    def _fuse_mainline_scores(
        self,
        signal_scores: pd.DataFrame,
        mainline_scores: pd.DataFrame,
        params: SignalParamsV7,
    ) -> pd.DataFrame:
        """融合主线得分和信号得分"""
        # 确保列对齐
        common_cols = signal_scores.columns.intersection(mainline_scores.columns)
        
        if len(common_cols) == 0:
            return signal_scores
        
        # 对齐
        signal_aligned = signal_scores[common_cols]
        mainline_aligned = mainline_scores.reindex(columns=common_cols).fillna(0)
        mainline_aligned = mainline_aligned.reindex(signal_scores.index, method='ffill').fillna(0)
        
        # 加权融合
        combined = (
            signal_aligned * params.signal_weight +
            mainline_aligned * params.mainline_weight
        )
        
        # 补回其他列
        result = signal_scores.copy()
        result[common_cols] = combined
        
        return result
    
    def _generate_target_weights(
        self,
        entries: pd.DataFrame,
        scores: pd.DataFrame,
        rebalance_mask: pd.Series,
        params: SignalParamsV7,
    ) -> pd.DataFrame:
        """生成目标权重矩阵"""
        target_weights = pd.DataFrame(0.0, index=entries.index, columns=entries.columns)
        
        for date in entries.index:
            if not rebalance_mask.get(date, False):
                continue
            
            # 获取当日有效信号
            valid = entries.loc[date]
            day_scores = scores.loc[date]
            
            # 筛选有信号的股票
            candidates = valid[valid].index.tolist()
            
            if not candidates:
                continue
            
            # 按评分排序，取TopN
            candidate_scores = day_scores[candidates].sort_values(ascending=False)
            top_n = candidate_scores.head(params.max_positions)
            
            if len(top_n) == 0:
                continue
            
            # 根据评分分配权重（评分加权）
            total_score = top_n.sum()
            if total_score > 0:
                weights = top_n / total_score
            else:
                weights = pd.Series(1.0 / len(top_n), index=top_n.index)
            
            # 限制单只上限
            weights = weights.clip(upper=params.single_position_max)
            
            # 归一化
            weights = weights / weights.sum()
            
            target_weights.loc[date, weights.index] = weights.values
        
        # 前向填充
        target_weights = target_weights.ffill()
        
        return target_weights
    
    def _generate_exits(
        self,
        data: DataMatrices,
        factors: FactorMatrices,
        params: SignalParamsV7,
    ) -> pd.DataFrame:
        """生成卖出信号（基本版，详细止损在回测引擎处理）"""
        exits = pd.DataFrame(False, index=data.dates, columns=data.symbols)
        
        # 简单的退出条件：相对位置过高
        if factors.rel_position is not None:
            exits = exits | (factors.rel_position > 95)
        
        return exits
    
    def update_params_for_cycle(
        self,
        cycle_params: Dict[str, float]
    ) -> SignalParamsV7:
        """根据周期参数更新信号参数"""
        new_params = SignalParamsV7(
            signal_weights=cycle_params.get('signal_weights', self.params.signal_weights),
            max_positions=int(cycle_params.get('max_positions', self.params.max_positions)),
            single_position_max=cycle_params.get('single_position_max', self.params.single_position_max),
        )
        
        # 复制其他参数
        for attr in ['min_mom_20d', 'max_mom_20d', 'max_rel_position', 'min_vol_ratio',
                     'limit_up_threshold', 'vol_ratio_threshold_first', 'min_signal_score',
                     'combine_mode', 'mainline_weight', 'signal_weight', 'use_mainline_fusion']:
            setattr(new_params, attr, getattr(self.params, attr))
        
        return new_params


# ============== 测试函数 ==============

def test_signal_engine_v7():
    """测试SignalEngineV7"""
    print("="*60)
    print("SignalEngineV7 测试")
    print("="*60)
    
    # 创建模拟数据
    dates = pd.date_range('2024-09-20', '2024-10-15', freq='D')
    stocks = ['000001', '000002', '000003', '000004', '000005']
    
    # 模拟收盘价
    close = pd.DataFrame(
        np.random.randn(len(dates), len(stocks)).cumsum(axis=0) * 0.02 + 10,
        index=dates,
        columns=stocks
    )
    
    # 创建DataMatrices
    data = DataMatrices(
        close=close,
        open=close * 0.99,
        high=close * 1.02,
        low=close * 0.98,
        volume=pd.DataFrame(np.random.rand(len(dates), len(stocks)) * 1e6, index=dates, columns=stocks)
    )
    
    # 创建模拟因子
    factors = FactorMatrices(
        mom_20d=pd.DataFrame(np.random.rand(len(dates), len(stocks)) * 20, index=dates, columns=stocks),
        mom_5d=pd.DataFrame(np.random.rand(len(dates), len(stocks)) * 15, index=dates, columns=stocks),
        rel_position=pd.DataFrame(np.random.rand(len(dates), len(stocks)) * 80, index=dates, columns=stocks),
        vol_ratio=pd.DataFrame(np.random.rand(len(dates), len(stocks)) * 3 + 0.5, index=dates, columns=stocks),
    )
    
    # 初始化引擎
    engine = SignalEngineV7()
    
    # 生成信号
    signals = engine.generate_signals(data, factors)
    
    print(f"\n信号矩阵形状: {signals.entries.shape}")
    print(f"买入信号数: {signals.entries.sum().sum()}")
    print(f"调仓日数: {signals.rebalance_mask.sum()}")
    print(f"\n各信号类型强度统计:")
    for sig_type, strength in signals.signal_strengths.items():
        print(f"  {sig_type}: 平均={strength.mean().mean():.1f}, 最大={strength.max().max():.1f}")
    
    print("\n✅ SignalEngineV7 测试通过")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_signal_engine_v7()
