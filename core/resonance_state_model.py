"""
Resonance State Model - A股多周期共振状态系统
==============================================

核心定位：状态识别/风险预算系统，不直接生成买卖点
输出：市场总开关、仓位上限、策略模式、行业TopN、个股过滤条件

本土化特点：
1. 涨跌停/跳空/ATR异常 → penalty
2. 持续性确认窗口：共振连续出现2~3次才升级仓位
3. 周期采样：指数日频、行业2~5日、个股周频

参考：IBD Market Pulse + A股特色
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple, Literal
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ 枚举定义 ============

class ResonancePhase(Enum):
    """共振阶段"""
    FULL_BULL = "全周期共振-牛"       # 所有周期共振向上
    PARTIAL_BULL = "部分共振-牛"     # 中长周期向上，短周期分歧
    DIVERGENT = "周期分歧"           # 各周期方向不一致
    PARTIAL_BEAR = "部分共振-熊"     # 中长周期向下，短周期分歧
    FULL_BEAR = "全周期共振-熊"      # 所有周期共振向下


class StrategyMode(Enum):
    """策略模式"""
    TREND_ONLY = "trend_only"           # 趋势策略优先
    DEFENSIVE = "defensive"             # 防守为主
    MEAN_REVERSION = "mean_reversion"   # 均值回归
    MIXED = "mixed"                     # 混合策略


class WeightStrategy(Enum):
    """权重策略"""
    EQUAL = "equal"                     # 等权
    DYNAMIC = "dynamic"                 # 动态（根据波动/流动性调整）
    TREND_WEIGHTED = "trend_weighted"   # 按趋势强度加权


# ============ 配置数据结构 ============

@dataclass
class ResonanceConfig:
    """
    共振系统配置
    
    核心参数可调，支持快速测试与长期回测切换
    """
    # ===== 周期定义（交易日口径）=====
    periods: Dict[str, int] = field(default_factory=lambda: {
        "short": 5,       # 短周期：5~10日
        "medium": 21,     # 中周期：20~30日
        "long": 63,       # 长周期：60~120日
    })
    
    # 采样频率（天）
    sampling_frequency: Dict[str, int] = field(default_factory=lambda: {
        "index": 1,       # 指数：日频
        "sector": 3,      # 行业：2~5日
        "stock": 5,       # 个股：周频
    })
    
    # ===== 持续性确认窗口 =====
    confirm_window: int = 2           # 连续N次共振才确认
    preconfirm_bonus: float = 0.3     # 预确认阶段的仓位调整系数
    
    # ===== RS相对强度 =====
    rs_windows: List[int] = field(default_factory=lambda: [20, 60, 120])
    rs_min_threshold: float = 0.0     # RS最小阈值（筛选用）
    
    # ===== 流动性过滤 =====
    min_turnover: float = 50_000_000  # 最小成交额（元），默认5000万
    min_market_cap: float = 5e9       # 最小市值（元），默认50亿
    
    # ===== 涨跌停/异常惩罚 =====
    limit_up_penalty: float = -20     # 连续涨停惩罚（风险高）
    limit_down_penalty: float = -30   # 连续跌停惩罚
    gap_penalty_threshold: float = 5.0  # 跳空阈值（%）
    gap_penalty: float = -15          # 跳空惩罚
    atr_abnormal_multiplier: float = 2.5  # ATR异常倍数
    atr_penalty: float = -10          # ATR异常惩罚
    
    # ===== 行业/主题轮动 =====
    sector_topn: int = 5              # 行业TopN
    theme_topn: int = 5               # 主题ETF TopN
    
    # ===== 仓位映射参数 =====
    position_cap_max: float = 1.0     # 最大仓位上限
    position_cap_min: float = 0.0     # 最小仓位上限
    
    def to_dict(self) -> Dict:
        return {
            "periods": self.periods,
            "sampling_frequency": self.sampling_frequency,
            "confirm_window": self.confirm_window,
            "preconfirm_bonus": self.preconfirm_bonus,
            "rs_windows": self.rs_windows,
            "rs_min_threshold": self.rs_min_threshold,
            "min_turnover": self.min_turnover,
            "min_market_cap": self.min_market_cap,
            "limit_up_penalty": self.limit_up_penalty,
            "limit_down_penalty": self.limit_down_penalty,
            "gap_penalty_threshold": self.gap_penalty_threshold,
            "gap_penalty": self.gap_penalty,
            "atr_abnormal_multiplier": self.atr_abnormal_multiplier,
            "atr_penalty": self.atr_penalty,
            "sector_topn": self.sector_topn,
            "theme_topn": self.theme_topn,
            "position_cap_max": self.position_cap_max,
            "position_cap_min": self.position_cap_min,
        }


@dataclass
class MarketSwitchSpec:
    """
    市场总开关规格
    
    默认：沪深300 + 中证1000（等权组合）
    """
    indices: List[str] = field(default_factory=lambda: [
        "000300.XSHG",  # 沪深300（偏大盘/机构）
        "000852.XSHG",  # 中证1000（偏小盘/弹性）
    ])
    
    # 指数权重
    index_weights: Dict[str, float] = field(default_factory=lambda: {
        "000300.XSHG": 0.5,
        "000852.XSHG": 0.5,
    })
    
    weight_strategy: WeightStrategy = WeightStrategy.EQUAL
    
    # 可选扩展指数（作为情绪因子，不参与主开关）
    auxiliary_indices: List[str] = field(default_factory=lambda: [
        "399006.XSHE",  # 创业板指（情绪/成长）
    ])
    
    def get_weight(self, index_code: str) -> float:
        """获取指数权重"""
        if self.weight_strategy == WeightStrategy.EQUAL:
            return 1.0 / len(self.indices) if index_code in self.indices else 0.0
        else:
            return self.index_weights.get(index_code, 0.0)
    
    def to_dict(self) -> Dict:
        return {
            "indices": self.indices,
            "index_weights": self.index_weights,
            "weight_strategy": self.weight_strategy.value,
            "auxiliary_indices": self.auxiliary_indices,
        }


# ============ 仓位映射函数 ============

def position_cap_mapping(
    regime_score: float,
    confirm_streak: int,
    config: ResonanceConfig = None,
) -> float:
    """
    仓位上限映射函数（优化版v2.1）
    
    输入：
    - regime_score: 综合共振得分 (-100 ~ +100)
    - confirm_streak: 连续确认次数
    - config: 配置对象
    
    输出：
    - position_cap: 仓位上限 (0 ~ 1)
    
    规则（A股本土化 - 优化版）：
    - 基础仓位与得分呈连续映射，避免阶梯跳跃
    - 无确认时保持合理基础仓位（保底20%，打8折而非5折）
    - 预确认阶段逐步提升（70%~90%）
    - 确认阶段完全释放 + 奖励
    
    优化点：
    1. 保底20%仓位：避免"弱势上涨却0%仓位"的逻辑矛盾
    2. 连续映射：使用分段线性插值，避免阈值边界跳跃
    3. 预确认逐步提升：confirm_streak=1时70%，=2时90%
    """
    config = config or ResonanceConfig()
    confirm_window = config.confirm_window
    
    # ===== 优化1：连续映射计算基础仓位 =====
    # 分段线性插值，避免阶梯跳跃
    if regime_score >= 60:
        # 60~100 -> 0.8~1.0
        base_cap = 0.8 + (regime_score - 60) / 40 * 0.2
    elif regime_score >= 40:
        # 40~60 -> 0.6~0.8
        base_cap = 0.6 + (regime_score - 40) / 20 * 0.2
    elif regime_score >= 20:
        # 20~40 -> 0.5~0.6
        base_cap = 0.5 + (regime_score - 20) / 20 * 0.1
    elif regime_score >= 0:
        # 0~20 -> 0.4~0.5
        base_cap = 0.4 + regime_score / 20 * 0.1
    elif regime_score >= -20:
        # -20~0 -> 0.3~0.4
        base_cap = 0.3 + (regime_score + 20) / 20 * 0.1
    elif regime_score >= -40:
        # -40~-20 -> 0.2~0.3
        base_cap = 0.2 + (regime_score + 40) / 20 * 0.1
    elif regime_score >= -60:
        # -60~-40 -> 0.1~0.2
        base_cap = 0.1 + (regime_score + 60) / 20 * 0.1
    else:
        # <-60 -> 0.05~0.1
        base_cap = max(0.05, 0.1 + (regime_score + 60) / 40 * 0.05)
    
    # ===== 优化2：持续性确认调整（更合理的系数）=====
    if confirm_streak >= confirm_window:
        # 确认阶段：提升仓位（每多确认一次+5%，最多+20%）
        confirm_bonus = min(0.2, (confirm_streak - confirm_window + 1) * 0.05)
        position_cap = base_cap + confirm_bonus
    elif confirm_streak > 0:
        # ===== 优化3：预确认阶段逐步提升 =====
        # confirm_streak=1 -> 70%, =2 -> 90% (而非固定30%)
        progress = confirm_streak / confirm_window
        position_cap = base_cap * (0.7 + progress * 0.2)
    else:
        # ===== 优化4：无确认时保底20%，打8折而非5折 =====
        position_cap = max(0.2, base_cap * 0.8)
    
    # 边界约束
    position_cap = max(config.position_cap_min, min(config.position_cap_max, position_cap))
    
    return position_cap


def determine_strategy_mode(
    regime_score: float,
    volatility: float,
    confirm_streak: int,
) -> StrategyMode:
    """
    确定策略模式
    
    输入：
    - regime_score: 综合共振得分
    - volatility: 市场波动率
    - confirm_streak: 连续确认次数
    
    输出：
    - strategy_mode: 策略模式枚举
    """
    if regime_score >= 40 and confirm_streak >= 2:
        return StrategyMode.TREND_ONLY
    elif regime_score <= -40:
        return StrategyMode.DEFENSIVE
    elif abs(regime_score) < 20 and volatility < 0.15:
        return StrategyMode.MEAN_REVERSION
    else:
        return StrategyMode.MIXED


def determine_resonance_phase(
    period_scores: Dict[str, float],
    threshold: float = 20.0,
) -> ResonancePhase:
    """
    确定共振阶段
    
    输入：
    - period_scores: {period: score} 各周期得分
    - threshold: 判断阈值
    
    输出：
    - ResonancePhase 枚举
    """
    if not period_scores:
        return ResonancePhase.DIVERGENT
    
    scores = list(period_scores.values())
    
    # 判断各周期方向
    bullish_count = sum(1 for s in scores if s > threshold)
    bearish_count = sum(1 for s in scores if s < -threshold)
    total = len(scores)
    
    if bullish_count == total:
        return ResonancePhase.FULL_BULL
    elif bearish_count == total:
        return ResonancePhase.FULL_BEAR
    elif bullish_count > bearish_count and bullish_count >= total / 2:
        return ResonancePhase.PARTIAL_BULL
    elif bearish_count > bullish_count and bearish_count >= total / 2:
        return ResonancePhase.PARTIAL_BEAR
    else:
        return ResonancePhase.DIVERGENT


# ============ 市场开关输出结构 ============

@dataclass
class MarketSwitchOutput:
    """
    市场总开关输出
    """
    date: str                               # 分析日期
    indices: List[str]                      # 参与指数列表
    index_scores: Dict[str, float]          # 各指数得分
    composite_score: float                  # 加权合成得分
    phase: ResonancePhase                   # 共振阶段
    confirm_streak: int                     # 连续确认次数
    position_cap: float                     # 仓位上限
    strategy_mode: StrategyMode             # 策略模式
    allowed_long: bool                      # 是否允许做多
    
    # 辅助信息
    auxiliary_scores: Dict[str, float] = field(default_factory=dict)  # 辅助指数得分
    volatility: float = 0.0                 # 市场波动率
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "indices": self.indices,
            "index_scores": self.index_scores,
            "composite_score": self.composite_score,
            "phase": self.phase.value,
            "confirm_streak": self.confirm_streak,
            "position_cap": self.position_cap,
            "strategy_mode": self.strategy_mode.value,
            "allowed_long": self.allowed_long,
            "auxiliary_scores": self.auxiliary_scores,
            "volatility": self.volatility,
        }


# ============ 扩展的投资标的筛选参数 ============

@dataclass
class ExtendedInvestmentFilters:
    """
    扩展的投资标的筛选参数（A股本土化）
    
    在原有 InvestmentUniverseFilters 基础上增加：
    - RS相对强度过滤
    - 流动性过滤
    - 涨跌停/极端波动修正
    """
    # 继承原有字段
    min_momentum_score: float = 20.0
    min_trend_score: float = 10.0
    max_volatility: float = 0.5
    sector_preferences: List[str] = field(default_factory=list)
    avoid_sectors: List[str] = field(default_factory=list)
    
    # RS相对强度
    rs_20d_min: float = 0.0           # 20日RS最小值
    rs_60d_min: float = 0.0           # 60日RS最小值
    rs_120d_min: float = 0.0          # 120日RS最小值
    
    # 流动性
    min_turnover: float = 50_000_000  # 最小成交额
    min_market_cap: float = 5e9       # 最小市值
    max_turnover_rate: float = 0.30   # 最大换手率（防庄股）
    
    # 涨跌停/极端波动修正
    max_limit_up_days: int = 3        # 近期最大连板天数（超过则降权）
    max_gap_pct: float = 8.0          # 最大跳空幅度
    max_atr_multiplier: float = 2.5   # ATR异常倍数
    
    # 可投资行业池（由行业轮动输出）
    investable_sectors: List[str] = field(default_factory=list)
    investable_etfs: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "min_momentum_score": self.min_momentum_score,
            "min_trend_score": self.min_trend_score,
            "max_volatility": self.max_volatility,
            "sector_preferences": self.sector_preferences,
            "avoid_sectors": self.avoid_sectors,
            "rs_20d_min": self.rs_20d_min,
            "rs_60d_min": self.rs_60d_min,
            "rs_120d_min": self.rs_120d_min,
            "min_turnover": self.min_turnover,
            "min_market_cap": self.min_market_cap,
            "max_turnover_rate": self.max_turnover_rate,
            "max_limit_up_days": self.max_limit_up_days,
            "max_gap_pct": self.max_gap_pct,
            "max_atr_multiplier": self.max_atr_multiplier,
            "investable_sectors": self.investable_sectors,
            "investable_etfs": self.investable_etfs,
        }


# ============ 行业/主题轮动输出结构 ============

@dataclass
class SectorRotationOutput:
    """
    行业/主题轮动输出
    """
    date: str
    
    # 行业层（申万一级）
    sector_scores: Dict[str, float]         # {sector_code: score}
    sector_topn: List[str]                  # TopN行业代码
    sector_scorecard: List[Dict]            # 详细评分卡
    
    # 主题层（主题ETF）
    theme_scores: Dict[str, float]          # {etf_code: score}
    theme_topn: List[str]                   # TopN主题ETF
    theme_scorecard: List[Dict]             # 详细评分卡
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "sector_scores": self.sector_scores,
            "sector_topn": self.sector_topn,
            "sector_scorecard": self.sector_scorecard,
            "theme_scores": self.theme_scores,
            "theme_topn": self.theme_topn,
            "theme_scorecard": self.theme_scorecard,
        }


# ============ 个股过滤器输出结构 ============

@dataclass
class StockFilterOutput:
    """
    个股过滤器输出
    """
    stock_code: str
    stock_name: str = ""
    
    # RS相对强度
    rs_20d: float = 0.0
    rs_60d: float = 0.0
    rs_120d: float = 0.0
    rs_composite: float = 0.0
    
    # 流动性
    avg_turnover: float = 0.0
    market_cap: float = 0.0
    turnover_rate: float = 0.0
    
    # 涨跌停/异常检测
    limit_up_days: int = 0
    limit_down_days: int = 0
    max_gap_pct: float = 0.0
    atr_ratio: float = 0.0
    
    # 惩罚/修正分
    penalty_score: float = 0.0
    
    # 过滤结果
    pass_filter: bool = True
    filter_reasons: List[str] = field(default_factory=list)
    
    # 排名特征（供后续因子组合用）
    ranking_features: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "rs_20d": self.rs_20d,
            "rs_60d": self.rs_60d,
            "rs_120d": self.rs_120d,
            "rs_composite": self.rs_composite,
            "avg_turnover": self.avg_turnover,
            "market_cap": self.market_cap,
            "turnover_rate": self.turnover_rate,
            "limit_up_days": self.limit_up_days,
            "limit_down_days": self.limit_down_days,
            "max_gap_pct": self.max_gap_pct,
            "atr_ratio": self.atr_ratio,
            "penalty_score": self.penalty_score,
            "pass_filter": self.pass_filter,
            "filter_reasons": self.filter_reasons,
            "ranking_features": self.ranking_features,
        }


# ============ 工具函数 ============

def calculate_rs(
    stock_returns: pd.Series,
    benchmark_returns: pd.Series,
    window: int = 20,
) -> float:
    """
    计算RS相对强度
    
    RS = stock_return(window) - benchmark_return(window)
    """
    if len(stock_returns) < window or len(benchmark_returns) < window:
        return 0.0
    
    stock_ret = (stock_returns.iloc[-1] / stock_returns.iloc[-window] - 1) * 100
    bench_ret = (benchmark_returns.iloc[-1] / benchmark_returns.iloc[-window] - 1) * 100
    
    return stock_ret - bench_ret


def detect_limit_days(
    df: pd.DataFrame,
    lookback: int = 10,
    limit_threshold: float = 9.5,
) -> Tuple[int, int]:
    """
    检测近期涨跌停天数
    
    返回：(涨停天数, 跌停天数)
    """
    if len(df) < 2:
        return 0, 0
    
    close = df['close'].tail(lookback + 1)
    pct_changes = close.pct_change() * 100
    
    limit_up_days = (pct_changes > limit_threshold).sum()
    limit_down_days = (pct_changes < -limit_threshold).sum()
    
    return int(limit_up_days), int(limit_down_days)


def detect_gap(
    df: pd.DataFrame,
    lookback: int = 5,
) -> float:
    """
    检测近期最大跳空幅度
    
    跳空 = (今日开盘 - 昨日收盘) / 昨日收盘 * 100
    """
    if len(df) < 2:
        return 0.0
    
    recent = df.tail(lookback + 1)
    gaps = (recent['open'].iloc[1:].values - recent['close'].iloc[:-1].values) / recent['close'].iloc[:-1].values * 100
    
    return float(np.max(np.abs(gaps))) if len(gaps) > 0 else 0.0


def detect_atr_abnormal(
    df: pd.DataFrame,
    period: int = 14,
    multiplier: float = 2.5,
) -> Tuple[float, bool]:
    """
    检测ATR异常
    
    返回：(ATR比率, 是否异常)
    """
    if len(df) < period + 1:
        return 1.0, False
    
    high = df['high']
    low = df['low']
    close = df['close']
    
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    
    atr = tr.rolling(period).mean()
    current_tr = tr.iloc[-1]
    current_atr = atr.iloc[-1]
    
    if current_atr > 0:
        ratio = current_tr / current_atr
    else:
        ratio = 1.0
    
    is_abnormal = ratio > multiplier
    
    return float(ratio), is_abnormal


def calculate_composite_score(
    index_scores: Dict[str, float],
    spec: MarketSwitchSpec,
) -> float:
    """
    计算加权合成得分
    """
    total_weight = 0.0
    weighted_score = 0.0
    
    for idx, score in index_scores.items():
        weight = spec.get_weight(idx)
        weighted_score += score * weight
        total_weight += weight
    
    if total_weight > 0:
        return weighted_score / total_weight * len(index_scores)  # 归一化
    return 0.0
