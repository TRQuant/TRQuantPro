# -*- coding: utf-8 -*-
"""
Resonance V2 Feature Layer
==========================

特征层：多周期特征提取和共振评分。

包含：
1. HMM观测变量提取 (log_return, volatility, trend_strength, turnover)
2. 多周期特征 (慢周期60日 + 快周期10日)
3. 共振评分 (趋势共振40% + 波动共振30% + 风险共振30%)

Author: TRQuant Team
Version: 2.0
Date: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import pandas as pd
import numpy as np

from .config import ResonanceV2Config, DEFAULT_CONFIG
from .data_layer import MarketData

logger = logging.getLogger(__name__)


@dataclass
class HMMObservations:
    """HMM观测变量容器"""
    data: np.ndarray          # 观测矩阵 (n_samples, n_features)
    feature_names: List[str]  # 特征名称
    dates: List[str]          # 对应日期
    
    @property
    def n_samples(self) -> int:
        return self.data.shape[0] if self.data is not None else 0
    
    @property
    def n_features(self) -> int:
        return self.data.shape[1] if self.data is not None and len(self.data.shape) > 1 else 0


@dataclass
class MultiCycleFeatures:
    """多周期特征容器"""
    # 慢周期特征 (20-60日)
    slow_ma_trend: pd.Series      # 慢周期MA趋势 (MA斜率)
    slow_volatility: pd.Series    # 慢周期波动率
    slow_adx: pd.Series           # ADX趋势强度
    
    # 快周期特征 (5-10日)
    fast_momentum: pd.Series      # 快周期动量
    fast_breakout: pd.Series      # 突破质量
    fast_volume_ratio: pd.Series  # 量能结构
    
    # 元数据
    dates: pd.DatetimeIndex
    
    def to_dataframe(self) -> pd.DataFrame:
        """转换为DataFrame"""
        return pd.DataFrame({
            'slow_ma_trend': self.slow_ma_trend,
            'slow_volatility': self.slow_volatility,
            'slow_adx': self.slow_adx,
            'fast_momentum': self.fast_momentum,
            'fast_breakout': self.fast_breakout,
            'fast_volume_ratio': self.fast_volume_ratio,
        }, index=self.dates)


@dataclass
class ResonanceScore:
    """共振评分结果"""
    total_score: float           # 总分 (0-100)
    trend_score: float           # 趋势共振分 (0-100)
    vol_score: float             # 波动共振分 (0-100)
    risk_score: float            # 风险共振分 (0-100)
    
    trend_sync: bool             # 趋势是否同步
    vol_sync: bool               # 波动是否同步
    risk_sync: bool              # 风险是否同步
    
    level: str                   # 共振级别: full/add/trial/none
    
    # 详细信息
    details: Dict = field(default_factory=dict)


class MultiCycleFeatureExtractor:
    """
    多周期特征提取器
    
    负责：
    1. 提取HMM观测变量
    2. 计算多周期技术特征
    3. 计算共振评分
    """
    
    def __init__(self, config: Optional[ResonanceV2Config] = None):
        """
        初始化特征提取器
        
        Args:
            config: 配置对象，None则使用默认配置
        """
        self.config = config or DEFAULT_CONFIG
        
    def extract_hmm_observations(
        self,
        market_data: MarketData,
        lookback: int = 20,
        north_flow_df: Optional[pd.DataFrame] = None,
        breadth_df: Optional[pd.DataFrame] = None
    ) -> HMMObservations:
        """
        提取HMM观测变量 (V2: 增强版)
        
        观测变量（可解释且稳健）：
        1. log_return: 对数收益率
        2. volatility: 实现波动率 (rolling std)
        3. trend_strength: 趋势强度 (MA斜率/ADX)
        4. turnover_ratio: 流动性/量能
        5. momentum_20d: 20日动量 (新增)
        6. north_flow: 北向资金净流入标准化 (新增)
        7. breadth_score: 市场宽度得分 (新增)
        8. rsi_deviation: RSI与50的偏离度 (新增)
        
        Args:
            market_data: 市场数据
            lookback: 回溯期
            north_flow_df: 北向资金数据 (可选)
            breadth_df: 市场宽度数据 (可选)
        
        Returns:
            HMMObservations: 观测变量容器
        """
        df = market_data.data.copy()
        
        if df.empty or 'close' not in df.columns:
            logger.warning(f"数据为空或缺少close列: {market_data.code}")
            return HMMObservations(
                data=np.array([]),
                feature_names=[],
                dates=[]
            )
        
        # 确保有日期列
        if 'date' not in df.columns:
            df['date'] = df.index
        
        # 将date转为datetime用于合并
        df['date'] = pd.to_datetime(df['date'])
        
        # ========== 基础观测变量 ==========
        
        # 1. 对数收益率
        df['log_return'] = np.log(df['close'] / df['close'].shift(1))
        
        # 2. 实现波动率 (年化，20日滚动)
        df['volatility'] = df['log_return'].rolling(lookback).std() * np.sqrt(252)
        
        # 3. 趋势强度 (MA斜率标准化)
        ma = df['close'].rolling(lookback).mean()
        ma_slope = (ma - ma.shift(5)) / ma.shift(5)  # 5日MA变化率
        df['trend_strength'] = ma_slope
        
        # 4. 换手率/量能 (需要money字段)
        if 'money' in df.columns:
            avg_money = df['money'].rolling(lookback).mean()
            df['turnover_ratio'] = df['money'] / avg_money
        else:
            df['turnover_ratio'] = 1.0
        
        # ========== 新增观测变量 ==========
        
        # 5. 20日动量 (收益率)
        df['momentum_20d'] = df['close'].pct_change(20)
        
        # 6. RSI偏离度
        df['rsi_deviation'] = self._calculate_rsi_deviation(df['close'], period=14)
        
        # 7. 北向资金（如果提供）
        if north_flow_df is not None and not north_flow_df.empty:
            north_flow_df = north_flow_df.copy()
            north_flow_df['date'] = pd.to_datetime(north_flow_df['date'])
            df = df.merge(north_flow_df[['date', 'north_net']], on='date', how='left')
            df['north_flow'] = df['north_net'].fillna(0)
            # 标准化：用20日均值和标准差
            north_mean = df['north_flow'].rolling(lookback).mean()
            north_std = df['north_flow'].rolling(lookback).std()
            df['north_flow'] = (df['north_flow'] - north_mean) / (north_std + 1e-10)
        else:
            df['north_flow'] = 0.0
        
        # 8. 市场宽度（如果提供）
        if breadth_df is not None and not breadth_df.empty:
            breadth_df = breadth_df.copy()
            breadth_df['date'] = pd.to_datetime(breadth_df['date'])
            df = df.merge(breadth_df[['date', 'breadth_score']], on='date', how='left')
            df['breadth_score'] = df['breadth_score'].fillna(0)
        else:
            df['breadth_score'] = 0.0
        
        # 移除NaN行
        feature_cols = [
            'log_return', 'volatility', 'trend_strength', 'turnover_ratio',
            'momentum_20d', 'rsi_deviation', 'north_flow', 'breadth_score'
        ]
        
        # 确保所有特征列存在
        for col in feature_cols:
            if col not in df.columns:
                df[col] = 0.0
        
        df_clean = df.dropna(subset=feature_cols)
        
        if df_clean.empty:
            logger.warning(f"清洗后数据为空: {market_data.code}")
            return HMMObservations(
                data=np.array([]),
                feature_names=[],
                dates=[]
            )
        
        # 构建观测矩阵
        observations = df_clean[feature_cols].values
        
        # 标准化 (Z-score)
        obs_mean = observations.mean(axis=0)
        obs_std = observations.std(axis=0)
        obs_std[obs_std == 0] = 1  # 防止除零
        observations_normalized = (observations - obs_mean) / obs_std
        
        # 获取日期列表
        if 'date' in df_clean.columns:
            dates = df_clean['date'].astype(str).tolist()
        else:
            dates = df_clean.index.astype(str).tolist()
        
        logger.info(f"提取HMM观测变量: {len(feature_cols)} 个特征, {len(dates)} 个样本")
        
        return HMMObservations(
            data=observations_normalized,
            feature_names=feature_cols,
            dates=dates
        )
    
    def _calculate_rsi_deviation(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """
        计算RSI与50的偏离度
        
        偏离度 = (RSI - 50) / 50, 范围 [-1, 1]
        - 正值: 超买
        - 负值: 超卖
        """
        delta = prices.diff()
        
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        # 转换为偏离度 [-1, 1]
        rsi_deviation = (rsi - 50) / 50
        
        return rsi_deviation
    
    def extract_multi_cycle_features(
        self,
        market_data: MarketData
    ) -> MultiCycleFeatures:
        """
        提取多周期特征
        
        慢周期 (20-60日):
        - MA趋势: 长期均线斜率
        - 波动状态: 长期波动率分位
        - ADX: 趋势强度指标
        
        快周期 (5-10日):
        - 动量: 短期收益率
        - 突破质量: 突破新高的强度
        - 量能结构: 放量/缩量特征
        
        Args:
            market_data: 市场数据
        
        Returns:
            MultiCycleFeatures: 多周期特征
        """
        df = market_data.data.copy()
        
        slow = self.config.slow_cycle
        fast = self.config.fast_cycle
        
        # ========== 慢周期特征 ==========
        
        # 1. MA趋势 (60日MA的20日变化率)
        ma_slow = df['close'].rolling(slow).mean()
        slow_ma_trend = (ma_slow - ma_slow.shift(self.config.ma_short)) / ma_slow.shift(self.config.ma_short)
        
        # 2. 慢周期波动率 (60日rolling std年化)
        returns = df['close'].pct_change()
        slow_volatility = returns.rolling(slow).std() * np.sqrt(252)
        
        # 3. ADX计算
        slow_adx = self._calculate_adx(df, period=14)
        
        # ========== 快周期特征 ==========
        
        # 1. 快周期动量 (10日收益率)
        fast_momentum = df['close'].pct_change(fast)
        
        # 2. 突破质量 (当前价格相对N日高点的位置)
        high_n = df['high'].rolling(fast * 2).max()
        low_n = df['low'].rolling(fast * 2).min()
        fast_breakout = (df['close'] - low_n) / (high_n - low_n + 1e-10)
        
        # 3. 量能结构 (近期成交量/过去成交量)
        if 'volume' in df.columns:
            vol_short = df['volume'].rolling(fast // 2).mean()
            vol_long = df['volume'].rolling(fast).mean()
            fast_volume_ratio = vol_short / (vol_long + 1e-10)
        else:
            fast_volume_ratio = pd.Series(1.0, index=df.index)
        
        # 获取日期索引
        if 'date' in df.columns:
            dates = pd.to_datetime(df['date'])
        else:
            dates = df.index
        
        return MultiCycleFeatures(
            slow_ma_trend=slow_ma_trend,
            slow_volatility=slow_volatility,
            slow_adx=slow_adx,
            fast_momentum=fast_momentum,
            fast_breakout=fast_breakout,
            fast_volume_ratio=fast_volume_ratio,
            dates=dates
        )
    
    def calculate_resonance_score(
        self,
        features: MultiCycleFeatures,
        index: int = -1
    ) -> ResonanceScore:
        """
        计算共振评分
        
        评分规则（可工业化的模板）：
        
        趋势共振 (40%):
        - 日线: 收盘 > MA20 > MA60 且 MA20上行 → +50
        - 快周期: 动量 > 0 且突破 > 0.7 → +50
        
        量能共振 (30%):
        - 成交量 >= 过去20根分位数70% → +50
        - 回撤缩量、反弹放量 → +50
        
        风险共振 (30%):
        - ADX > 25 (趋势明确) → +50
        - 波动率在合理范围 → +50
        
        Args:
            features: 多周期特征
            index: 计算哪个时间点的分数，-1表示最新
        
        Returns:
            ResonanceScore: 共振评分结果
        """
        # 获取指定时间点的特征值
        slow_trend = self._get_value(features.slow_ma_trend, index)
        slow_vol = self._get_value(features.slow_volatility, index)
        slow_adx = self._get_value(features.slow_adx, index)
        fast_mom = self._get_value(features.fast_momentum, index)
        fast_break = self._get_value(features.fast_breakout, index)
        fast_vol_ratio = self._get_value(features.fast_volume_ratio, index)
        
        # ========== 趋势共振评分 (40%) ==========
        trend_score = 0
        trend_sync = False
        
        # 慢周期趋势向上 (+50)
        if slow_trend > 0:
            trend_score += 50
        elif slow_trend > -0.02:  # 轻微下跌也给部分分
            trend_score += 25
        
        # 快周期动量正且突破强 (+50)
        if fast_mom > 0 and fast_break > 0.7:
            trend_score += 50
            trend_sync = True
        elif fast_mom > 0 or fast_break > 0.5:
            trend_score += 25
        
        # ========== 量能共振评分 (30%) ==========
        vol_score = 0
        vol_sync = False
        
        # 放量 (+50)
        if fast_vol_ratio > 1.2:
            vol_score += 50
            vol_sync = True
        elif fast_vol_ratio > 1.0:
            vol_score += 25
        
        # 量价配合 (+50)
        if fast_mom > 0 and fast_vol_ratio > 1.0:  # 上涨放量
            vol_score += 50
        elif fast_mom < 0 and fast_vol_ratio < 1.0:  # 下跌缩量（健康回调）
            vol_score += 25
        
        # ========== 风险共振评分 (30%) ==========
        risk_score = 0
        risk_sync = False
        
        # ADX趋势明确 (+50)
        if slow_adx > 25:
            risk_score += 50
            risk_sync = True
        elif slow_adx > 15:
            risk_score += 25
        
        # 波动率适中 (+50)
        if 0.10 < slow_vol < 0.30:  # 年化10%-30%
            risk_score += 50
        elif 0.05 < slow_vol < 0.40:
            risk_score += 25
        
        # ========== 加权总分 ==========
        total_score = (
            trend_score * self.config.trend_weight +
            vol_score * self.config.vol_weight +
            risk_score * self.config.risk_weight
        )
        
        # 确定共振级别
        level = self.config.get_resonance_level(total_score)
        
        return ResonanceScore(
            total_score=total_score,
            trend_score=trend_score,
            vol_score=vol_score,
            risk_score=risk_score,
            trend_sync=trend_sync,
            vol_sync=vol_sync,
            risk_sync=risk_sync,
            level=level,
            details={
                'slow_trend': slow_trend,
                'slow_volatility': slow_vol,
                'slow_adx': slow_adx,
                'fast_momentum': fast_mom,
                'fast_breakout': fast_break,
                'fast_volume_ratio': fast_vol_ratio,
            }
        )
    
    def calculate_resonance_series(
        self,
        features: MultiCycleFeatures
    ) -> pd.DataFrame:
        """
        计算时间序列的共振评分
        
        Args:
            features: 多周期特征
        
        Returns:
            pd.DataFrame: 共振评分时间序列
        """
        n = len(features.dates)
        scores = []
        
        for i in range(n):
            score = self.calculate_resonance_score(features, index=i)
            scores.append({
                'date': features.dates[i],
                'total_score': score.total_score,
                'trend_score': score.trend_score,
                'vol_score': score.vol_score,
                'risk_score': score.risk_score,
                'trend_sync': score.trend_sync,
                'vol_sync': score.vol_sync,
                'risk_sync': score.risk_sync,
                'level': score.level,
            })
        
        return pd.DataFrame(scores)
    
    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """
        计算ADX (Average Directional Index)
        
        ADX衡量趋势强度，不区分方向：
        - ADX > 25: 趋势明确
        - ADX < 20: 无明显趋势
        """
        high = df['high']
        low = df['low']
        close = df['close']
        
        # True Range
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        # Directional Movement
        up_move = high - high.shift(1)
        down_move = low.shift(1) - low
        
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        
        # Smoothed values
        tr_smooth = pd.Series(tr).rolling(period).sum()
        plus_dm_smooth = pd.Series(plus_dm).rolling(period).sum()
        minus_dm_smooth = pd.Series(minus_dm).rolling(period).sum()
        
        # DI
        plus_di = 100 * plus_dm_smooth / (tr_smooth + 1e-10)
        minus_di = 100 * minus_dm_smooth / (tr_smooth + 1e-10)
        
        # DX and ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
        adx = pd.Series(dx).rolling(period).mean()
        
        return adx
    
    def _get_value(self, series: pd.Series, index: int) -> float:
        """安全获取Series值"""
        try:
            if index == -1:
                return series.iloc[-1] if len(series) > 0 else 0.0
            return series.iloc[index] if 0 <= index < len(series) else 0.0
        except:
            return 0.0


def extract_features_from_data(
    market_data: MarketData,
    config: Optional[ResonanceV2Config] = None
) -> Tuple[HMMObservations, MultiCycleFeatures, ResonanceScore]:
    """
    便捷函数：从市场数据提取所有特征
    
    Args:
        market_data: 市场数据
        config: 配置对象
    
    Returns:
        Tuple: (HMM观测变量, 多周期特征, 最新共振评分)
    """
    extractor = MultiCycleFeatureExtractor(config)
    
    hmm_obs = extractor.extract_hmm_observations(market_data)
    multi_features = extractor.extract_multi_cycle_features(market_data)
    resonance = extractor.calculate_resonance_score(multi_features)
    
    return hmm_obs, multi_features, resonance
