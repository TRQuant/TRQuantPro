"""
市场环境特征工程模块 v3.0

三周期特征计算：
- 周级别(5日): 短期操作参考
- 月级别(22日): 波段操作参考
- 季度级别(66日): 趋势判断参考
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


@dataclass
class PeriodConfig:
    """周期配置"""
    name: str
    days: int
    ma_periods: List[int]
    momentum_period: int
    rsi_period: int
    
    
# 三周期配置
PERIOD_CONFIGS = {
    'weekly': PeriodConfig(
        name='周级别',
        days=5,
        ma_periods=[5, 10, 20],
        momentum_period=5,
        rsi_period=5
    ),
    'monthly': PeriodConfig(
        name='月级别',
        days=22,
        ma_periods=[10, 20, 60],
        momentum_period=22,
        rsi_period=14
    ),
    'quarterly': PeriodConfig(
        name='季度级别',
        days=66,
        ma_periods=[20, 60, 120],
        momentum_period=66,
        rsi_period=21
    )
}


@dataclass
class PeriodFeatures:
    """单周期特征"""
    period: str
    period_name: str
    
    # 趋势指标
    momentum: float = 0.0          # 动量（收益率%）
    ma_alignment: float = 0.0      # 均线排列得分（-100到100）
    price_vs_ma: float = 0.0       # 价格vs主要均线偏离（%）
    trend_strength: float = 0.0    # 趋势强度（0-100）
    
    # 振荡指标
    rsi: float = 50.0              # RSI
    position_in_range: float = 50.0  # 区间位置（0-100）
    
    # 波动率
    volatility: float = 0.0        # 年化波动率（%）
    atr_ratio: float = 0.0         # ATR相对比率
    
    # MACD
    macd_histogram: float = 0.0    # MACD柱状图
    macd_signal: int = 0           # MACD信号（1=金叉，-1=死叉，0=无）
    
    # 布林带
    bb_position: float = 50.0      # 布林带位置（0-100）
    bb_width: float = 0.0          # 布林带宽度（%）
    
    def to_dict(self) -> dict:
        return {
            'period': self.period,
            'period_name': self.period_name,
            'momentum': round(self.momentum, 2),
            'ma_alignment': round(self.ma_alignment, 2),
            'price_vs_ma': round(self.price_vs_ma, 2),
            'trend_strength': round(self.trend_strength, 2),
            'rsi': round(self.rsi, 2),
            'position_in_range': round(self.position_in_range, 2),
            'volatility': round(self.volatility, 2),
            'atr_ratio': round(self.atr_ratio, 2),
            'macd_histogram': round(self.macd_histogram, 4),
            'macd_signal': self.macd_signal,
            'bb_position': round(self.bb_position, 2),
            'bb_width': round(self.bb_width, 2)
        }


@dataclass 
class MarketFeatures:
    """市场综合特征"""
    weekly: PeriodFeatures
    monthly: PeriodFeatures
    quarterly: PeriodFeatures
    
    # 综合指标
    multi_period_alignment: float = 0.0  # 多周期共振度（-100到100）
    overall_trend_score: float = 0.0     # 综合趋势得分（-100到100）
    
    def to_dict(self) -> dict:
        return {
            'weekly': self.weekly.to_dict(),
            'monthly': self.monthly.to_dict(),
            'quarterly': self.quarterly.to_dict(),
            'multi_period_alignment': round(self.multi_period_alignment, 2),
            'overall_trend_score': round(self.overall_trend_score, 2)
        }


class MarketFeatureCalculator:
    """
    市场特征计算器
    
    计算三周期（周/月/季度）的技术特征
    """
    
    def __init__(self):
        self.configs = PERIOD_CONFIGS
    
    def calculate(self, df: pd.DataFrame) -> MarketFeatures:
        """
        计算市场特征
        
        Args:
            df: OHLCV数据，需要至少250天历史数据
            
        Returns:
            MarketFeatures: 三周期特征
        """
        df = self._prepare_data(df)
        
        # 计算三个周期的特征
        weekly = self._calculate_period_features(df, 'weekly')
        monthly = self._calculate_period_features(df, 'monthly')
        quarterly = self._calculate_period_features(df, 'quarterly')
        
        # 计算多周期共振
        alignment = self._calculate_multi_period_alignment(weekly, monthly, quarterly)
        trend_score = self._calculate_overall_trend_score(weekly, monthly, quarterly)
        
        return MarketFeatures(
            weekly=weekly,
            monthly=monthly,
            quarterly=quarterly,
            multi_period_alignment=alignment,
            overall_trend_score=trend_score
        )
    
    def _prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """准备数据，计算基础指标"""
        df = df.copy()
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df.get('volume', pd.Series([1]*len(df), index=df.index))
        
        # 计算各周期均线
        for period in [5, 10, 20, 60, 120, 250]:
            df[f'ma{period}'] = close.rolling(period, min_periods=1).mean()
        
        # 计算动量
        for period in [5, 22, 66]:
            df[f'mom_{period}d'] = close.pct_change(period) * 100
        
        # 计算RSI
        for period in [5, 14, 21]:
            df[f'rsi_{period}'] = self._calculate_rsi(close, period)
        
        # 计算MACD
        df['ema12'] = close.ewm(span=12, adjust=False).mean()
        df['ema26'] = close.ewm(span=26, adjust=False).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        
        # 计算布林带
        for period in [20, 60]:
            df[f'bb_mid_{period}'] = close.rolling(period, min_periods=1).mean()
            df[f'bb_std_{period}'] = close.rolling(period, min_periods=1).std()
            df[f'bb_upper_{period}'] = df[f'bb_mid_{period}'] + 2 * df[f'bb_std_{period}']
            df[f'bb_lower_{period}'] = df[f'bb_mid_{period}'] - 2 * df[f'bb_std_{period}']
        
        # 计算ATR
        tr = pd.concat([
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ], axis=1).max(axis=1)
        df['atr_14'] = tr.rolling(14, min_periods=1).mean()
        
        # 计算波动率
        df['daily_return'] = close.pct_change()
        for period in [5, 22, 66]:
            df[f'vol_{period}d'] = df['daily_return'].rolling(period, min_periods=1).std() * np.sqrt(252) * 100
        
        # 计算区间位置
        for period in [20, 60, 250]:
            df[f'high_{period}d'] = high.rolling(period, min_periods=1).max()
            df[f'low_{period}d'] = low.rolling(period, min_periods=1).min()
            range_size = df[f'high_{period}d'] - df[f'low_{period}d']
            df[f'pos_{period}d'] = ((close - df[f'low_{period}d']) / range_size.replace(0, np.nan) * 100).fillna(50)
        
        return df
    
    def _calculate_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """计算RSI"""
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(period, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period, min_periods=1).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)
    
    def _calculate_period_features(self, df: pd.DataFrame, period_key: str) -> PeriodFeatures:
        """计算单周期特征"""
        config = self.configs[period_key]
        row = df.iloc[-1]
        close = df['close'].iloc[-1]
        
        # 动量
        momentum = row.get(f'mom_{config.momentum_period}d', 0)
        
        # 均线排列
        ma_alignment = self._calculate_ma_alignment(row, config.ma_periods)
        
        # 价格vs主均线
        main_ma_period = config.ma_periods[1]  # 中间均线
        main_ma = row.get(f'ma{main_ma_period}', close)
        price_vs_ma = (close / main_ma - 1) * 100 if main_ma > 0 else 0
        
        # 趋势强度
        trend_strength = self._calculate_trend_strength(df, config)
        
        # RSI
        rsi = row.get(f'rsi_{config.rsi_period}', 50)
        
        # 区间位置
        if period_key == 'weekly':
            pos_period = 20
        elif period_key == 'monthly':
            pos_period = 60
        else:
            pos_period = 250
        position_in_range = row.get(f'pos_{pos_period}d', 50)
        
        # 波动率
        volatility = row.get(f'vol_{config.days}d', 15)
        
        # ATR比率
        atr = row.get('atr_14', 0)
        atr_ratio = (atr / close * 100) if close > 0 else 0
        
        # MACD
        macd_hist = row.get('macd_hist', 0)
        prev_macd_hist = df['macd_hist'].iloc[-2] if len(df) > 1 else 0
        if macd_hist > 0 and prev_macd_hist <= 0:
            macd_signal = 1  # 金叉
        elif macd_hist < 0 and prev_macd_hist >= 0:
            macd_signal = -1  # 死叉
        else:
            macd_signal = 0
        
        # 布林带
        bb_period = 20 if period_key == 'weekly' else 60
        bb_upper = row.get(f'bb_upper_{bb_period}', close)
        bb_lower = row.get(f'bb_lower_{bb_period}', close)
        bb_mid = row.get(f'bb_mid_{bb_period}', close)
        
        bb_range = bb_upper - bb_lower
        bb_position = ((close - bb_lower) / bb_range * 100) if bb_range > 0 else 50
        bb_width = (bb_range / bb_mid * 100) if bb_mid > 0 else 0
        
        return PeriodFeatures(
            period=period_key,
            period_name=config.name,
            momentum=momentum,
            ma_alignment=ma_alignment,
            price_vs_ma=price_vs_ma,
            trend_strength=trend_strength,
            rsi=rsi,
            position_in_range=position_in_range,
            volatility=volatility,
            atr_ratio=atr_ratio,
            macd_histogram=macd_hist,
            macd_signal=macd_signal,
            bb_position=bb_position,
            bb_width=bb_width
        )
    
    def _calculate_ma_alignment(self, row, ma_periods: List[int]) -> float:
        """
        计算均线排列得分
        
        多头排列返回正值，空头排列返回负值
        """
        mas = [row.get(f'ma{p}', 0) for p in ma_periods]
        
        if any(m == 0 for m in mas):
            return 0
        
        # 检查是否完全多头排列（短均线 > 中均线 > 长均线）
        is_bullish = all(mas[i] >= mas[i+1] for i in range(len(mas)-1))
        # 检查是否完全空头排列
        is_bearish = all(mas[i] <= mas[i+1] for i in range(len(mas)-1))
        
        if is_bullish:
            # 计算排列强度
            spread = (mas[0] / mas[-1] - 1) * 100
            return min(100, max(0, spread * 10 + 50))
        elif is_bearish:
            spread = (mas[-1] / mas[0] - 1) * 100
            return max(-100, min(0, -spread * 10 - 50))
        else:
            # 混乱排列，返回接近0的值
            return 0
    
    def _calculate_trend_strength(self, df: pd.DataFrame, config: PeriodConfig) -> float:
        """
        计算趋势强度（0-100）
        
        综合考虑：动量、均线斜率、ADX等
        """
        close = df['close']
        n = config.days
        
        # 动量得分
        mom = close.pct_change(n).iloc[-1] * 100
        mom_score = min(100, max(0, (mom + 10) * 5))  # -10%到+10%映射到0-100
        
        # 均线斜率得分
        ma_period = config.ma_periods[1]
        ma = df[f'ma{ma_period}']
        ma_slope = (ma.iloc[-1] / ma.iloc[-n] - 1) * 100 if len(ma) > n else 0
        slope_score = min(100, max(0, (ma_slope + 5) * 10))
        
        # 价格连续性得分
        recent = close.tail(n)
        up_days = (recent.diff() > 0).sum()
        continuity_score = (up_days / n) * 100
        
        # 综合
        return (mom_score * 0.4 + slope_score * 0.4 + continuity_score * 0.2)
    
    def _calculate_multi_period_alignment(self, 
                                          weekly: PeriodFeatures,
                                          monthly: PeriodFeatures,
                                          quarterly: PeriodFeatures) -> float:
        """
        计算多周期共振度
        
        返回-100到100，正值表示多头共振，负值表示空头共振
        """
        # 各周期趋势方向
        weekly_dir = 1 if weekly.momentum > 0 else (-1 if weekly.momentum < 0 else 0)
        monthly_dir = 1 if monthly.momentum > 0 else (-1 if monthly.momentum < 0 else 0)
        quarterly_dir = 1 if quarterly.momentum > 0 else (-1 if quarterly.momentum < 0 else 0)
        
        # 方向一致性
        direction_sum = weekly_dir + monthly_dir + quarterly_dir
        
        # 强度加权
        strength = (
            abs(weekly.momentum) * 0.2 +
            abs(monthly.momentum) * 0.3 +
            abs(quarterly.momentum) * 0.5
        )
        
        # 共振度
        if direction_sum == 3:  # 全部看多
            return min(100, 50 + strength)
        elif direction_sum == -3:  # 全部看空
            return max(-100, -50 - strength)
        elif direction_sum == 2:  # 大部分看多
            return min(70, 30 + strength * 0.5)
        elif direction_sum == -2:  # 大部分看空
            return max(-70, -30 - strength * 0.5)
        else:
            return 0  # 分歧
    
    def _calculate_overall_trend_score(self,
                                       weekly: PeriodFeatures,
                                       monthly: PeriodFeatures,
                                       quarterly: PeriodFeatures) -> float:
        """
        计算综合趋势得分
        
        返回-100到100，权重：周20%，月30%，季度50%
        """
        # 各周期得分（基于动量和位置）
        def period_score(pf: PeriodFeatures) -> float:
            # 动量得分
            mom_score = min(50, max(-50, pf.momentum * 2))
            # 位置得分
            pos_score = (pf.position_in_range - 50)  # -50到50
            # RSI得分
            rsi_score = (pf.rsi - 50) * 0.5  # -25到25
            return mom_score * 0.5 + pos_score * 0.3 + rsi_score * 0.2
        
        weekly_score = period_score(weekly)
        monthly_score = period_score(monthly)
        quarterly_score = period_score(quarterly)
        
        # 加权综合
        return (
            weekly_score * 0.2 +
            monthly_score * 0.3 +
            quarterly_score * 0.5
        )


# 便捷函数
def calculate_market_features(df: pd.DataFrame) -> MarketFeatures:
    """
    计算市场特征
    
    Args:
        df: OHLCV数据
        
    Returns:
        MarketFeatures
    """
    calculator = MarketFeatureCalculator()
    return calculator.calculate(df)


def get_feature_summary(features: MarketFeatures) -> str:
    """
    生成特征摘要
    """
    lines = []
    lines.append("=" * 50)
    lines.append("市场特征摘要")
    lines.append("=" * 50)
    
    for period_key in ['weekly', 'monthly', 'quarterly']:
        pf = getattr(features, period_key)
        direction = "↑" if pf.momentum > 0 else ("↓" if pf.momentum < 0 else "→")
        lines.append(f"\n【{pf.period_name}】 {direction}")
        lines.append(f"  动量: {pf.momentum:+.2f}%")
        lines.append(f"  均线排列: {pf.ma_alignment:.1f}")
        lines.append(f"  RSI: {pf.rsi:.1f}")
        lines.append(f"  区间位置: {pf.position_in_range:.1f}%")
    
    lines.append(f"\n【综合】")
    lines.append(f"  多周期共振: {features.multi_period_alignment:+.1f}")
    lines.append(f"  趋势得分: {features.overall_trend_score:+.1f}")
    
    return "\n".join(lines)

