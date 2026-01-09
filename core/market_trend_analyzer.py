"""
MarketTrendAnalyzer - 市场趋势分析器
====================================

基线实现：TrendAnalyzer + SimpleHMM (已回测验证)
周期口径：周/月/季 = 5/21/63 交易日
权重：Trend 0.8 + HMM 0.2

核心功能：
1. 多周期趋势分析 (周/月/季/半年/年 - 可扩展)
2. HMM隐状态识别
3. 加权融合输出
4. 生成workflow_params供下游使用
5. 生成investment_universe_filters供标的筛选
6. A股共振状态系统（市场总开关、仓位上限、策略模式）

参考：IBD Market Pulse, 贝莱德宏观分析框架
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging
import json

# 共振状态模型
from core.resonance_state_model import (
    ResonanceConfig,
    MarketSwitchSpec,
    ResonancePhase,
    StrategyMode,
    MarketSwitchOutput,
    ExtendedInvestmentFilters,
    position_cap_mapping,
    determine_strategy_mode,
    determine_resonance_phase,
    calculate_composite_score,
)

# 14种市场阶段定义
from core.market_state_definitions import (
    MarketPhase,
    determine_market_phase,
    PHASE_DESCRIPTIONS,
)

logger = logging.getLogger(__name__)


# ============ 枚举定义 ============

class TrendDirection(Enum):
    """趋势方向"""
    STRONG_UP = "强势上涨"
    UP = "上涨趋势"
    WEAK_UP = "弱势上涨"
    SIDEWAYS = "震荡盘整"
    WEAK_DOWN = "弱势下跌"
    DOWN = "下跌趋势"
    STRONG_DOWN = "强势下跌"


class MarketRegime(Enum):
    """市场状态"""
    BULL = "牛市"
    BEAR = "熊市"
    SIDEWAYS = "震荡"


# ============ 配置数据结构 ============

@dataclass
class MarketTrendAnalyzerConfig:
    """
    MarketTrendAnalyzer 配置
    
    Attributes:
        periods: 周期窗口配置 {period_name: days}
        active_periods: 当前激活的周期列表
        weights: 模型权重 {"trend": 0.8, "hmm": 0.2}
        data_source_priority: 数据源优先级
        indicator_weights: 8维指标权重
    """
    periods: Dict[str, int] = field(default_factory=lambda: {
        "week": 5,       # 周: 5交易日
        "month": 21,     # 月: 21交易日
        "quarter": 63,   # 季: 63交易日
        # 预留入口
        "half_year": 126,
        "year": 252,
        "multi_year": 756,
    })
    
    active_periods: List[str] = field(default_factory=lambda: ["week", "month", "quarter"])
    
    weights: Dict[str, float] = field(default_factory=lambda: {
        "trend": 0.8,
        "hmm": 0.2,
    })
    
    data_source_priority: List[str] = field(default_factory=lambda: ["jqdata", "akshare"])
    
    # 8维指标权重 (来自TrendAnalyzer)
    indicator_weights: Dict[str, float] = field(default_factory=lambda: {
        "ma": 0.20,      # 均线系统
        "macd": 0.18,    # MACD动能
        "rsi": 0.10,     # RSI超买超卖
        "bb": 0.10,      # 布林带
        "vol": 0.12,     # 成交量
        "kdj": 0.10,     # KDJ随机指标
        "adx": 0.10,     # ADX趋势强度
        "flow": 0.10,    # 资金流向
    })

    # 评分风格：
    # - legacy: 指标级加权（与当前实现一致，可能存在信息冗余/重复计分）
    # - smooth_grouped: 连续映射 + 因子分组聚合（更稳定、可迁移）
    scoring_style: str = "legacy"

    # 因子分组（用于 smooth_grouped）
    factor_groups: Dict[str, List[str]] = field(default_factory=lambda: {
        "trend": ["ma", "macd", "adx"],               # 趋势强弱
        "oscillator": ["rsi", "kdj", "flow"],         # 超买超卖/资金热度
        "volatility": ["bb"],                         # 波动/突破
        "volume": ["vol"],                            # 量价背景
    })

    # 组间权重（用于 smooth_grouped，和为1）
    factor_group_weights: Dict[str, float] = field(default_factory=lambda: {
        "trend": 0.45,
        "oscillator": 0.25,
        "volatility": 0.15,
        "volume": 0.15,
    })
    
    def to_dict(self) -> Dict:
        return {
            "periods": self.periods,
            "active_periods": self.active_periods,
            "weights": self.weights,
            "data_source_priority": self.data_source_priority,
            "indicator_weights": self.indicator_weights,
            "scoring_style": self.scoring_style,
            "factor_groups": self.factor_groups,
            "factor_group_weights": self.factor_group_weights,
        }


@dataclass
class PeriodSignal:
    """单周期趋势信号"""
    period: str                    # week/month/quarter
    period_days: int               # 窗口天数
    direction: TrendDirection      # 趋势方向
    score: float                   # -100 到 +100
    confidence: float              # 0 到 1
    indicators: Dict[str, float] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "period": self.period,
            "period_days": self.period_days,
            "direction": self.direction.value,
            "score": self.score,
            "confidence": self.confidence,
            "indicators": self.indicators,
        }


@dataclass
class HMMSignal:
    """HMM隐状态信号"""
    state: MarketRegime            # 当前状态
    state_probability: Dict[str, float]  # 各状态概率
    confidence: float              # 置信度
    regime_change_signal: bool     # 状态转换信号
    state_duration: int            # 当前状态持续天数
    
    def to_dict(self) -> Dict:
        return {
            "state": self.state.value,
            "state_probability": self.state_probability,
            "confidence": self.confidence,
            "regime_change_signal": self.regime_change_signal,
            "state_duration": self.state_duration,
        }


@dataclass
class WorkflowParams:
    """工作流参数 - 供下游模块直接使用"""
    position_target: float         # 目标仓位 0-1
    risk_budget: float             # 风险预算
    allowed_actions: Dict[str, bool]  # 允许的操作
    rebalance_frequency: str       # 建议调仓频率
    regime_tag: str                # 市场状态标签
    
    def to_dict(self) -> Dict:
        return {
            "position_target": self.position_target,
            "risk_budget": self.risk_budget,
            "allowed_actions": self.allowed_actions,
            "rebalance_frequency": self.rebalance_frequency,
            "regime_tag": self.regime_tag,
        }


@dataclass
class InvestmentUniverseFilters:
    """投资标的筛选参数"""
    min_momentum_score: float      # 最小动量得分
    min_trend_score: float         # 最小趋势得分
    max_volatility: float          # 最大波动率
    sector_preferences: List[str]  # 偏好板块
    avoid_sectors: List[str]       # 回避板块
    
    def to_dict(self) -> Dict:
        return {
            "min_momentum_score": self.min_momentum_score,
            "min_trend_score": self.min_trend_score,
            "max_volatility": self.max_volatility,
            "sector_preferences": self.sector_preferences,
            "avoid_sectors": self.avoid_sectors,
        }


@dataclass
class MarketTrendSignal:
    """
    MarketTrendAnalyzer 输出信号
    
    统一输出格式，包含：
    - 各周期趋势信号
    - HMM隐状态信号
    - 加权融合结果
    - 工作流参数
    - 投资标的筛选参数
    - 市场总开关（A股共振状态系统）
    - 元数据
    """
    date: str                      # 分析日期
    index_code: str                # 指数代码
    
    # 周期信号
    period_signals: Dict[str, PeriodSignal]  # {period: signal}
    
    # HMM信号
    hmm_signal: Optional[HMMSignal]
    
    # 加权融合结果
    ensemble_score: float          # 综合得分 -100 到 +100
    ensemble_direction: TrendDirection
    ensemble_confidence: float     # 综合置信度
    
    # 工作流参数
    workflow_params: WorkflowParams
    
    # 投资标的筛选
    investment_universe_filters: InvestmentUniverseFilters
    
    # ===== 新增：A股共振状态系统字段 =====
    # 市场总开关（多指数共振）
    market_switch: Optional[MarketSwitchOutput] = None
    
    # 仓位上限（0~1）
    position_cap: float = 0.5
    
    # 策略模式
    strategy_mode: StrategyMode = StrategyMode.MIXED
    
    # 扩展的投资标的筛选（含RS/流动性/涨跌停修正）
    extended_filters: Optional[ExtendedInvestmentFilters] = None
    
    # 共振阶段
    resonance_phase: ResonancePhase = ResonancePhase.DIVERGENT
    
    # 连续确认次数
    confirm_streak: int = 0
    
    # ===== 新增：14种市场阶段 =====
    market_phase: Optional[MarketPhase] = None
    market_phase_position: float = 0.5  # 来自PHASE_DESCRIPTIONS的建议仓位
    
    # 元数据
    config_hash: str = ""
    algorithm_version: str = "2.1"  # 版本升级：集成14种市场阶段
    data_source: str = ""
    
    def to_dict(self) -> Dict:
        result = {
            "date": self.date,
            "index_code": self.index_code,
            "period_signals": {k: v.to_dict() for k, v in self.period_signals.items()},
            "hmm_signal": self.hmm_signal.to_dict() if self.hmm_signal else None,
            "ensemble_score": self.ensemble_score,
            "ensemble_direction": self.ensemble_direction.value,
            "ensemble_confidence": self.ensemble_confidence,
            "workflow_params": self.workflow_params.to_dict(),
            "investment_universe_filters": self.investment_universe_filters.to_dict(),
            # 扁平化字段便于DataFrame
            "week_score": self.period_signals.get("week", PeriodSignal("week", 5, TrendDirection.SIDEWAYS, 0, 0)).score if "week" in self.period_signals else None,
            "month_score": self.period_signals.get("month", PeriodSignal("month", 21, TrendDirection.SIDEWAYS, 0, 0)).score if "month" in self.period_signals else None,
            "quarter_score": self.period_signals.get("quarter", PeriodSignal("quarter", 63, TrendDirection.SIDEWAYS, 0, 0)).score if "quarter" in self.period_signals else None,
            "hmm_state": self.hmm_signal.state.value if self.hmm_signal else None,
            # 新增共振状态字段
            "market_switch": self.market_switch.to_dict() if self.market_switch else None,
            "position_cap": self.position_cap,
            "strategy_mode": self.strategy_mode.value,
            "extended_filters": self.extended_filters.to_dict() if self.extended_filters else None,
            "resonance_phase": self.resonance_phase.value,
            "confirm_streak": self.confirm_streak,
            # 新增14种市场阶段
            "market_phase": self.market_phase.value if self.market_phase else None,
            "market_phase_name": self.market_phase.name if self.market_phase else None,
            "market_phase_position": self.market_phase_position,
            "config_hash": self.config_hash,
            "algorithm_version": self.algorithm_version,
            "data_source": self.data_source,
        }
        return result


# ============ 主分析器 ============

class MarketTrendAnalyzer:
    """
    市场趋势分析器
    
    基线实现：TrendAnalyzer + SimpleHMM
    周期口径：周/月/季 = 5/21/63 交易日
    权重：Trend 0.8 + HMM 0.2
    """
    
    # 周期指标参数配置 (根据窗口长度自适应)
    PERIOD_INDICATOR_CONFIG = {
        "week": {  # 5天窗口
            "ma_fast": 3,
            "ma_slow": 5,
            "macd_fast": 3,
            "macd_slow": 5,
            "macd_signal": 3,
            "rsi_period": 5,
        },
        "month": {  # 21天窗口
            "ma_fast": 5,
            "ma_slow": 20,
            "macd_fast": 8,
            "macd_slow": 17,
            "macd_signal": 9,
            "rsi_period": 14,
        },
        "quarter": {  # 63天窗口
            "ma_fast": 10,
            "ma_slow": 50,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9,
            "rsi_period": 21,
        },
    }
    
    def __init__(self, config: MarketTrendAnalyzerConfig = None):
        """
        初始化分析器
        
        Args:
            config: 配置对象，默认使用标准配置
        """
        self.config = config or MarketTrendAnalyzerConfig()
        self._jq = None
        self._hmm = None
        self._price_cache: Dict[str, pd.DataFrame] = {}
        
    def _ensure_jqdata(self):
        """确保JQData连接"""
        if self._jq is None:
            try:
                import jqdatasdk as jq
                from config.config_manager import get_config_manager
                
                config_mgr = get_config_manager()
                jq_config = config_mgr.get_config('jqdata')
                if jq_config:
                    jq.auth(jq_config.get('username'), jq_config.get('password'))
                    if jq.is_auth():
                        self._jq = jq
                        logger.info("MarketTrendAnalyzer: JQData连接成功")
            except Exception as e:
                logger.warning(f"JQData连接失败: {e}")
    
    def _ensure_hmm(self):
        """确保HMM模型初始化"""
        if self._hmm is None:
            try:
                from core.trend_ml import SimpleHMM
                self._hmm = SimpleHMM(use_astock_params=True)
                logger.info("MarketTrendAnalyzer: SimpleHMM初始化成功")
            except Exception as e:
                logger.warning(f"SimpleHMM初始化失败: {e}")
    
    def _get_price_data(self, index_code: str, as_of_date: str, days: int = 300) -> Optional[pd.DataFrame]:
        """
        获取价格数据
        
        Args:
            index_code: 指数代码
            as_of_date: 截止日期 (严格使用历史数据)
            days: 获取天数
        """
        cache_key = f"{index_code}_{as_of_date}_{days}"
        if cache_key in self._price_cache:
            return self._price_cache[cache_key]
        
        self._ensure_jqdata()
        if self._jq is None:
            logger.warning("JQData未连接，无法获取数据")
            return None
        
        try:
            df = self._jq.get_price(
                index_code,
                end_date=as_of_date,
                count=days,
                frequency='daily',
                fields=['open', 'high', 'low', 'close', 'volume']
            )
            
            if df is not None and not df.empty:
                df = df.reset_index()
                if 'index' in df.columns:
                    df = df.rename(columns={'index': 'date'})
                self._price_cache[cache_key] = df
                return df
            
        except Exception as e:
            logger.error(f"获取价格数据失败: {e}")
        
        return None
    
    def analyze(self, index_code: str, as_of_date: str, df: pd.DataFrame = None) -> Optional[MarketTrendSignal]:
        """
        执行市场趋势分析
        
        Args:
            index_code: 指数代码
            as_of_date: 分析日期 (回测时必须是历史日期)
            df: 可选的价格数据DataFrame
            
        Returns:
            MarketTrendSignal 或 None
        """
        try:
            # 获取数据
            if df is None:
                max_period = max(self.config.periods.get(p, 63) for p in self.config.active_periods)
                df = self._get_price_data(index_code, as_of_date, days=max_period + 100)
            
            if df is None or df.empty or len(df) < 20:
                logger.warning(f"数据不足: {index_code} @ {as_of_date}")
                return None
            
            # 分析各周期趋势
            period_signals = {}
            for period in self.config.active_periods:
                days = self.config.periods.get(period, 21)
                signal = self._analyze_period(df, period, days)
                if signal:
                    period_signals[period] = signal
            
            # HMM分析
            self._ensure_hmm()
            hmm_signal = None
            if self._hmm is not None:
                hmm_signal = self._analyze_hmm(df)
            
            # 加权融合
            ensemble_score, ensemble_direction, ensemble_confidence = self._ensemble_combine(
                period_signals, hmm_signal
            )
            
            # 生成工作流参数
            workflow_params = self._generate_workflow_params(
                ensemble_score, ensemble_direction, hmm_signal
            )
            
            # 生成投资标的筛选参数
            filters = self._generate_investment_filters(
                ensemble_score, ensemble_direction, period_signals
            )
            
            # ===== 新增：14种市场阶段判断 =====
            market_phase, phase_position = self._determine_market_phase(period_signals)
            
            return MarketTrendSignal(
                date=as_of_date,
                index_code=index_code,
                period_signals=period_signals,
                hmm_signal=hmm_signal,
                ensemble_score=ensemble_score,
                ensemble_direction=ensemble_direction,
                ensemble_confidence=ensemble_confidence,
                workflow_params=workflow_params,
                investment_universe_filters=filters,
                market_phase=market_phase,
                market_phase_position=phase_position,
                data_source="jqdata" if self._jq else "unknown",
            )
            
        except Exception as e:
            logger.error(f"分析失败 {index_code} @ {as_of_date}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _analyze_period(self, df: pd.DataFrame, period: str, days: int) -> Optional[PeriodSignal]:
        """
        分析单个周期的趋势
        
        使用TrendAnalyzer的8维指标体系
        """
        try:
            # 取对应周期的数据
            period_df = df.tail(days).copy()
            if len(period_df) < min(days, 10):
                return None
            
            # 获取指标配置
            ind_config = self.PERIOD_INDICATOR_CONFIG.get(period, self.PERIOD_INDICATOR_CONFIG["month"])
            
            indicators = {}
            
            # 1. 均线系统
            ma_score, ma_ind = self._calc_ma_score(period_df, ind_config)
            indicators.update(ma_ind)
            
            # 2. MACD
            macd_score, macd_ind = self._calc_macd_score(period_df, ind_config)
            indicators.update(macd_ind)
            
            # 3. RSI
            rsi_score, rsi_ind = self._calc_rsi_score(period_df, ind_config)
            indicators.update(rsi_ind)
            
            # 4. 布林带
            bb_score, bb_ind = self._calc_bollinger_score(period_df)
            indicators.update(bb_ind)
            
            # 5. 成交量
            vol_score, vol_ind = self._calc_volume_score(period_df)
            indicators.update(vol_ind)
            
            # 6. KDJ
            kdj_score, kdj_ind = self._calc_kdj_score(period_df)
            indicators.update(kdj_ind)
            
            # 7. ADX
            adx_score, adx_ind = self._calc_adx_score(period_df)
            indicators.update(adx_ind)
            
            # 8. 资金流向（OBV + MFI + 放量日模拟）
            flow_score, flow_ind = self._calc_mfi_flow_score(period_df)
            indicators.update(flow_ind)

            # ----------- 总分聚合 -----------
            raw_scores = {
                "ma": float(ma_score),
                "macd": float(macd_score),
                "rsi": float(rsi_score),
                "bb": float(bb_score),
                "vol": float(vol_score),
                "kdj": float(kdj_score),
                "adx": float(adx_score),
                "flow": float(flow_score),
            }

            if self.config.scoring_style == "smooth_grouped":
                total_score, group_scores = self._aggregate_grouped_scores(raw_scores)
                indicators["group_scores"] = group_scores
            else:
                weights = self.config.indicator_weights
                total_score = (
                    raw_scores["ma"] * weights.get("ma", 0.2) +
                    raw_scores["macd"] * weights.get("macd", 0.18) +
                    raw_scores["rsi"] * weights.get("rsi", 0.1) +
                    raw_scores["bb"] * weights.get("bb", 0.1) +
                    raw_scores["vol"] * weights.get("vol", 0.12) +
                    raw_scores["kdj"] * weights.get("kdj", 0.1) +
                    raw_scores["adx"] * weights.get("adx", 0.1) +
                    raw_scores["flow"] * weights.get("flow", 0.1)
                )

            total_score = float(np.clip(total_score, -100, 100))
            
            # 置信度 (基于指标一致性)
            scores = [ma_score, macd_score, rsi_score, bb_score, vol_score, kdj_score, adx_score, flow_score]
            confidence = 1 - (np.std(scores) / 100)
            confidence = max(0, min(1, confidence))
            
            # 方向判定
            direction = self._score_to_direction(total_score)
            
            return PeriodSignal(
                period=period,
                period_days=days,
                direction=direction,
                score=total_score,
                confidence=confidence,
                indicators=indicators,
            )
            
        except Exception as e:
            logger.debug(f"周期分析失败 {period}: {e}")
            return None

    @staticmethod
    def _piecewise_linear(x: float, points: List[Tuple[float, float]]) -> float:
        """
        分段线性映射：用于把连续指标值映射到连续得分，避免阈值跳变。
        points: [(x0,y0),(x1,y1),...] 必须按 x 升序
        """
        if not points:
            return 0.0
        if x <= points[0][0]:
            return float(points[0][1])
        if x >= points[-1][0]:
            return float(points[-1][1])
        for (x0, y0), (x1, y1) in zip(points[:-1], points[1:]):
            if x0 <= x <= x1:
                if x1 == x0:
                    return float(y1)
                t = (x - x0) / (x1 - x0)
                return float(y0 + t * (y1 - y0))
        return float(points[-1][1])

    def _aggregate_grouped_scores(self, raw_scores: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        """
        因子分组聚合：避免 MA/MACD/ADX 等趋势因子重复计分导致过拟合。

        规则：
        - 组内：简单平均（也可后续替换成相关性去重/PCA）
        - 组间：按 factor_group_weights 加权
        """
        group_scores: Dict[str, float] = {}
        total = 0.0
        weights = self.config.factor_group_weights

        for group, keys in self.config.factor_groups.items():
            vals = [raw_scores[k] for k in keys if k in raw_scores]
            if not vals:
                continue
            gs = float(np.mean(vals))
            group_scores[group] = float(np.clip(gs, -100, 100))
            total += group_scores[group] * float(weights.get(group, 0.0))

        return float(np.clip(total, -100, 100)), group_scores
    
    def _calc_ma_score(self, df: pd.DataFrame, config: Dict) -> Tuple[float, Dict]:
        """计算均线系统得分"""
        close = df['close']
        ma_fast = close.rolling(config['ma_fast']).mean()
        ma_slow = close.rolling(config['ma_slow']).mean()
        
        current_close = close.iloc[-1]
        current_ma_fast = ma_fast.iloc[-1]
        current_ma_slow = ma_slow.iloc[-1]
        
        score = 0
        
        # 价格vs均线
        if current_close > current_ma_fast:
            score += 25
        else:
            score -= 25
        
        if current_close > current_ma_slow:
            score += 25
        else:
            score -= 25
        
        # 均线排列
        if current_ma_fast > current_ma_slow:
            score += 30
        else:
            score -= 30
        
        # 斜率
        if len(ma_fast) >= 5:
            slope = (ma_fast.iloc[-1] - ma_fast.iloc[-5]) / ma_fast.iloc[-5] * 100 if ma_fast.iloc[-5] > 0 else 0
            score += np.clip(slope * 5, -20, 20)
        
        indicators = {
            'ma_fast': current_ma_fast,
            'ma_slow': current_ma_slow,
            'price_vs_ma_fast': (current_close / current_ma_fast - 1) * 100 if current_ma_fast > 0 else 0,
        }
        
        return np.clip(score, -100, 100), indicators
    
    def _calc_macd_score(self, df: pd.DataFrame, config: Dict) -> Tuple[float, Dict]:
        """计算MACD得分"""
        close = df['close']
        
        ema_fast = close.ewm(span=config['macd_fast'], adjust=False).mean()
        ema_slow = close.ewm(span=config['macd_slow'], adjust=False).mean()
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=config['macd_signal'], adjust=False).mean()
        histogram = macd - signal
        
        current_macd = macd.iloc[-1]
        current_signal = signal.iloc[-1]
        current_hist = histogram.iloc[-1]
        
        score = 0
        
        # MACD位置
        if current_macd > 0:
            score += 30
        else:
            score -= 30
        
        # MACD vs Signal
        if current_macd > current_signal:
            score += 30
        else:
            score -= 30
        
        # 柱状图趋势
        if len(histogram) >= 2:
            if histogram.iloc[-1] > histogram.iloc[-2]:
                score += 20
            else:
                score -= 20
        
        # 金叉死叉
        if len(macd) >= 2 and len(signal) >= 2:
            if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
                score += 20  # 金叉
            elif macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
                score -= 20  # 死叉
        
        indicators = {
            'macd': current_macd,
            'macd_signal': current_signal,
            'macd_histogram': current_hist,
        }
        
        return np.clip(score, -100, 100), indicators
    
    def _calc_rsi_score(self, df: pd.DataFrame, config: Dict) -> Tuple[float, Dict]:
        """计算RSI得分"""
        close = df['close']
        delta = close.diff()
        
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        
        period = config['rsi_period']
        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()
        
        rs = avg_gain / avg_loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1] if not np.isnan(rsi.iloc[-1]) else 50
        
        # RSI评分（连续映射，避免阈值跳变）
        # 参考锚点：
        # - RSI<=20: +30（超卖反弹）
        # - 30: +10
        # - 50: +20（健康强势）
        # - 70: 0
        # - 80: -40（过热风险）
        score = self._piecewise_linear(
            float(current_rsi),
            points=[
                (0, 30),
                (20, 30),
                (30, 10),
                (50, 20),
                (70, 0),
                (80, -40),
                (100, -60),
            ],
        )
        
        indicators = {'rsi': current_rsi}

        return float(np.clip(score, -100, 100)), indicators
    
    def _calc_bollinger_score(self, df: pd.DataFrame, period: int = 20) -> Tuple[float, Dict]:
        """计算布林带得分"""
        close = df['close']
        ma = close.rolling(period).mean()
        std = close.rolling(period).std()
        
        upper = ma + 2 * std
        lower = ma - 2 * std
        
        current_close = close.iloc[-1]
        current_upper = upper.iloc[-1]
        current_lower = lower.iloc[-1]
        current_ma = ma.iloc[-1]
        
        # 位置评分（连续）
        if current_upper != current_lower:
            position = (current_close - current_lower) / (current_upper - current_lower)
        else:
            position = 0.5

        pos_score = self._piecewise_linear(
            float(position),
            points=[
                (0.0, 20),   # 贴近下轨：偏反弹
                (0.2, 10),
                (0.5, 20),
                (0.7, 30),
                (0.8, 10),
                (1.0, -20),  # 贴近上轨：偏过热
            ],
        )
        
        # 带宽
        bandwidth = (current_upper - current_lower) / current_ma * 100 if current_ma > 0 else 0

        # 突破/超买优先级（明确互斥冲突）
        # - 价格上穿上轨：优先视为短期过热（扣分）
        # - 价格下穿下轨：优先视为超卖（加分）
        breakout_score = 0.0
        if current_close > current_upper:
            breakout_score = -30.0
        elif current_close < current_lower:
            breakout_score = 25.0

        # 带宽扩张：趋势/波动放大信号（轻量加成，避免与趋势组重复计分过强）
        bw_score = float(np.clip((bandwidth - 5) * 2, -10, 10))

        # 合成：突破优先，其次位置与带宽
        score = 0.6 * breakout_score + 0.3 * pos_score + 0.1 * bw_score
        
        indicators = {
            'bb_upper': current_upper,
            'bb_lower': current_lower,
            'bb_position': position,
            'bb_bandwidth': bandwidth,
            'bb_breakout': breakout_score,
        }

        return float(np.clip(score, -100, 100)), indicators
    
    def _calc_volume_score(self, df: pd.DataFrame) -> Tuple[float, Dict]:
        """计算成交量得分"""
        volume = df['volume']
        close = df['close']
        
        # 近5日平均量
        vol_ma5 = volume.rolling(5).mean()
        vol_ma20 = volume.rolling(20).mean()
        
        current_vol = volume.iloc[-1]
        current_vol_ma5 = vol_ma5.iloc[-1]
        current_vol_ma20 = vol_ma20.iloc[-1] if len(vol_ma20) >= 20 else current_vol_ma5
        
        score = 0
        
        # 量能变化（标准化背景：vol/vol_ma20，再做zscore）
        vol_ratio = current_vol / current_vol_ma20 if current_vol_ma20 > 0 else 1.0
        vol_ratio_series = (volume / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
        z_window = 60 if len(vol_ratio_series) >= 60 else max(20, len(vol_ratio_series))
        z = 0.0
        if z_window >= 10:
            vr = vol_ratio_series.tail(z_window)
            std = float(vr.std()) if float(vr.std()) > 0 else 0.0
            if std > 0:
                z = float((vr.iloc[-1] - float(vr.mean())) / std)
        
        # 结合价格判断
        price_change = (close.iloc[-1] / close.iloc[-2] - 1) if len(close) >= 2 else 0
        
        # zscore 贡献（避免不同市场环境下“同样50%放量”含义不同）
        score += float(np.clip(z * 12, -25, 25))

        # 结合价格方向：放量上涨/下跌的方向性
        if price_change > 0:
            score += float(np.clip((vol_ratio - 1.0) * 25, -15, 25))
        elif price_change < 0:
            score -= float(np.clip((vol_ratio - 1.0) * 25, -25, 15))
        
        # 量能趋势
        # 量能趋势（短均量 vs 长均量）
        if current_vol_ma5 > current_vol_ma20:
            score += 10
        else:
            score -= 10
        
        indicators = {
            'volume_ratio': vol_ratio,
            'volume_zscore': z,
            'vol_ma5': current_vol_ma5,
            'vol_ma20': current_vol_ma20,
        }
        
        return np.clip(score, -100, 100), indicators

    def _calc_kdj_score(
        self,
        df: pd.DataFrame,
        n: int = 9,
        m1: int = 3,
        m2: int = 3,
    ) -> Tuple[float, Dict]:
        """
        计算 KDJ 随机指标得分（完整逻辑）

        思路：
        - 超买超卖：J > 80 视为过热、J < 20 视为超卖
        - 金叉/死叉：K 上穿 D 加分，K 下穿 D 减分
        - 多空位置：K、D 位于 50 上方偏多，50 下方偏空
        """
        try:
            high = df["high"]
            low = df["low"]
            close = df["close"]

            low_min = low.rolling(n).min()
            high_max = high.rolling(n).max()
            denom = (high_max - low_min).replace(0, np.nan)
            rsv = (close - low_min) / denom * 100
            rsv = rsv.fillna(50)

            k = rsv.ewm(span=m1, adjust=False).mean()
            d = k.ewm(span=m2, adjust=False).mean()
            j = 3 * k - 2 * d

            k_now = float(k.iloc[-1])
            d_now = float(d.iloc[-1])
            j_now = float(j.iloc[-1])

            score = 0.0

            # 超买超卖（以 J 为主）
            if j_now >= 90:
                score -= 35
            elif j_now >= 80:
                score -= 25
            elif j_now <= 10:
                score += 35
            elif j_now <= 20:
                score += 25

            # K/D 多空位置
            if k_now >= 50 and d_now >= 50:
                score += 15
            elif k_now < 50 and d_now < 50:
                score -= 15

            # 金叉死叉（最近一根）
            cross = ""
            if len(k) >= 2 and len(d) >= 2:
                k_prev = float(k.iloc[-2])
                d_prev = float(d.iloc[-2])
                if k_prev < d_prev and k_now > d_now:
                    score += 25
                    cross = "golden"
                elif k_prev > d_prev and k_now < d_now:
                    score -= 25
                    cross = "death"

            # K 与 D 偏离度（拐点强弱）
            kd_gap = k_now - d_now
            score += float(np.clip(kd_gap * 0.8, -15, 15))

            indicators = {
                "kdj_k": k_now,
                "kdj_d": d_now,
                "kdj_j": j_now,
                "kdj_cross": cross,
                "kdj_gap": kd_gap,
                "kdj_zone": (
                    "overbought" if j_now >= 80 else ("oversold" if j_now <= 20 else "neutral")
                ),
            }

            return float(np.clip(score, -100, 100)), indicators
        except Exception:
            return 0.0, {}

    def _calc_adx_score(self, df: pd.DataFrame, period: int = 14) -> Tuple[float, Dict]:
        """
        计算 ADX 趋势强度得分（完整逻辑）

        ADX 只衡量趋势强度；方向用 +DI/-DI 来判断。
        """
        try:
            high = df["high"]
            low = df["low"]
            close = df["close"]

            tr = pd.concat(
                [
                    (high - low),
                    (high - close.shift()).abs(),
                    (low - close.shift()).abs(),
                ],
                axis=1,
            ).max(axis=1)
            atr = tr.rolling(period).mean()

            plus_dm = (high.diff()).where((high.diff() > low.diff().abs()) & (high.diff() > 0), 0.0)
            minus_dm = (-low.diff()).where((low.diff().abs() > high.diff()) & (low.diff() < 0), 0.0)

            plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
            minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

            denom = (plus_di + minus_di).replace(0, np.nan)
            dx = 100 * (plus_di - minus_di).abs() / denom
            adx = dx.rolling(period).mean()

            adx_now = float(adx.iloc[-1]) if not pd.isna(adx.iloc[-1]) else 15.0
            plus_now = float(plus_di.iloc[-1]) if not pd.isna(plus_di.iloc[-1]) else 20.0
            minus_now = float(minus_di.iloc[-1]) if not pd.isna(minus_di.iloc[-1]) else 20.0

            score = 0.0

            # 趋势强度（以 ADX 阈值分段）
            if adx_now >= 40:
                score += 40
                adx_trend = "strong"
            elif adx_now >= 25:
                score += 25
                adx_trend = "medium"
            elif adx_now >= 20:
                score += 10
                adx_trend = "weak"
            else:
                score -= 10
                adx_trend = "range"

            # 方向（+DI/-DI）
            if plus_now > minus_now:
                score += 20
                adx_dir = "bull"
            elif plus_now < minus_now:
                score -= 20
                adx_dir = "bear"
            else:
                adx_dir = "neutral"

            # 趋势增强/减弱（ADX 斜率）
            if len(adx) >= 3 and not pd.isna(adx.iloc[-3]):
                adx_prev = float(adx.iloc[-3])
                if adx_now - adx_prev >= 2:
                    score += 10
                elif adx_prev - adx_now >= 2:
                    score -= 10

            indicators = {
                "adx": adx_now,
                "plus_di": plus_now,
                "minus_di": minus_now,
                "adx_trend": adx_trend,
                "adx_direction": adx_dir,
            }

            return float(np.clip(score, -100, 100)), indicators
        except Exception:
            return 0.0, {}

    def _calc_mfi_flow_score(self, df: pd.DataFrame, mfi_period: int = 14) -> Tuple[float, Dict]:
        """
        计算资金流向得分（MFI + OBV + 放量日模拟）

        - OBV 反映“量价合成”的资金趋势
        - MFI 反映超买/超卖与资金热度
        - 放量日数量模拟“主力”介入/出货
        """
        try:
            close = df["close"]
            volume = df["volume"]
            high = df["high"]
            low = df["low"]

            # OBV（能量潮）
            obv = (volume * np.sign(close.diff())).fillna(0).cumsum()
            obv_ma5 = obv.rolling(5).mean()
            obv_ma20 = obv.rolling(20).mean()

            # MFI（资金流量指标）
            typical_price = (high + low + close) / 3
            money_flow = typical_price * volume

            positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
            negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

            positive_mf = positive_flow.rolling(mfi_period).sum()
            negative_mf = negative_flow.rolling(mfi_period).sum().replace(0, np.nan)
            mfi = 100 - (100 / (1 + positive_mf / negative_mf))
            mfi_now = float(mfi.iloc[-1]) if not pd.isna(mfi.iloc[-1]) else 50.0

            score = 0.0

            # OBV 趋势
            flow_trend = "in" if obv_ma5.iloc[-1] > obv_ma20.iloc[-1] else "out"
            score += 30 if flow_trend == "in" else -30

            # MFI 区间（资金热度/枯竭）
            if mfi_now >= 80:
                score += 10  # 过热（延续性强，但也可能过热）
                mfi_zone = "overbought"
            elif mfi_now >= 50:
                score += 25
                mfi_zone = "inflow"
            elif mfi_now >= 20:
                score -= 25
                mfi_zone = "outflow"
            else:
                score -= 10
                mfi_zone = "oversold"

            # 放量日模拟（近5日中，量能>2倍20日均量）
            vol_ma20 = volume.rolling(20).mean()
            vol_ratio = (volume / vol_ma20.replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(1.0)
            big_volume_days = float((vol_ratio > 2).rolling(5).sum().iloc[-1]) if len(vol_ratio) >= 5 else 0.0

            if big_volume_days >= 2 and len(close) >= 6:
                if close.iloc[-1] > close.iloc[-6]:
                    score += 20
                elif close.iloc[-1] < close.iloc[-6]:
                    score -= 20

            indicators = {
                "obv": float(obv.iloc[-1]),
                "obv_ma5": float(obv_ma5.iloc[-1]) if not pd.isna(obv_ma5.iloc[-1]) else float(obv.iloc[-1]),
                "obv_ma20": float(obv_ma20.iloc[-1]) if not pd.isna(obv_ma20.iloc[-1]) else float(obv.iloc[-1]),
                "mfi": mfi_now,
                "mfi_zone": mfi_zone,
                "big_volume_days": big_volume_days,
                "flow_trend": "流入" if flow_trend == "in" else "流出",
            }

            return float(np.clip(score, -100, 100)), indicators
        except Exception:
            return 0.0, {}
    
    def _calc_kdj_score_simple(self, df: pd.DataFrame, n: int = 9) -> float:
        """简化版KDJ得分"""
        try:
            low_min = df['low'].rolling(n).min()
            high_max = df['high'].rolling(n).max()
            
            rsv = (df['close'] - low_min) / (high_max - low_min) * 100
            rsv = rsv.fillna(50)
            
            k = rsv.ewm(span=3, adjust=False).mean()
            d = k.ewm(span=3, adjust=False).mean()
            j = 3 * k - 2 * d
            
            current_k = k.iloc[-1]
            current_j = j.iloc[-1]
            
            if current_j > 80:
                return -30  # 超买
            elif current_j < 20:
                return 30   # 超卖
            elif current_k > 50:
                return 20
            else:
                return -20
        except:
            return 0
    
    def _calc_adx_score_simple(self, df: pd.DataFrame, n: int = 14) -> float:
        """简化版ADX得分"""
        try:
            high = df['high']
            low = df['low']
            close = df['close']
            
            tr = pd.concat([
                high - low,
                (high - close.shift()).abs(),
                (low - close.shift()).abs()
            ], axis=1).max(axis=1)
            
            atr = tr.rolling(n).mean()
            
            # 简化：用ATR比率判断趋势强度
            atr_ratio = atr.iloc[-1] / close.iloc[-1] * 100 if close.iloc[-1] > 0 else 0
            
            if atr_ratio > 3:
                return 30  # 强趋势
            elif atr_ratio > 2:
                return 20
            elif atr_ratio > 1:
                return 0
            else:
                return -20  # 弱趋势
        except:
            return 0
    
    def _score_to_direction(self, score: float) -> TrendDirection:
        """得分转方向"""
        if score > 50:
            return TrendDirection.STRONG_UP
        elif score > 20:
            return TrendDirection.UP
        elif score > 0:
            return TrendDirection.WEAK_UP
        elif score > -20:
            return TrendDirection.SIDEWAYS
        elif score > -50:
            return TrendDirection.WEAK_DOWN
        else:
            return TrendDirection.STRONG_DOWN
    
    def _determine_market_phase(
        self, 
        period_signals: Dict[str, PeriodSignal]
    ) -> Tuple[Optional[MarketPhase], float]:
        """
        根据三周期得分确定14种市场阶段
        
        Args:
            period_signals: 各周期信号字典
            
        Returns:
            (market_phase, position_suggestion) 元组
        """
        try:
            # 获取三周期得分（映射到short/medium/long）
            # week -> short, month -> medium, quarter -> long
            short_score = period_signals.get("week", PeriodSignal("week", 5, TrendDirection.SIDEWAYS, 0, 0)).score
            medium_score = period_signals.get("month", PeriodSignal("month", 21, TrendDirection.SIDEWAYS, 0, 0)).score
            long_score = period_signals.get("quarter", PeriodSignal("quarter", 63, TrendDirection.SIDEWAYS, 0, 0)).score
            
            # 调用14种阶段判定函数
            market_phase = determine_market_phase(short_score, medium_score, long_score)
            
            # 获取阶段建议仓位
            phase_info = PHASE_DESCRIPTIONS.get(market_phase, {})
            position_suggestion = phase_info.get("position_suggestion", 0.5)
            
            logger.debug(
                f"市场阶段判定: short={short_score:.1f}, medium={medium_score:.1f}, "
                f"long={long_score:.1f} -> {market_phase.value} (仓位建议: {position_suggestion})"
            )
            
            return market_phase, position_suggestion
            
        except Exception as e:
            logger.warning(f"市场阶段判定失败: {e}")
            return None, 0.5
    
    def _analyze_hmm(self, df: pd.DataFrame) -> Optional[HMMSignal]:
        """HMM状态分析"""
        if self._hmm is None:
            return None
        
        try:
            result = self._hmm.analyze(df)
            if result is None:
                return None
            
            # 转换状态
            state_map = {
                'bull': MarketRegime.BULL,
                '牛市': MarketRegime.BULL,
                'bear': MarketRegime.BEAR,
                '熊市': MarketRegime.BEAR,
                'sideways': MarketRegime.SIDEWAYS,
                '震荡': MarketRegime.SIDEWAYS,
            }
            
            state_str = result.current_state.value if hasattr(result.current_state, 'value') else str(result.current_state)
            state = state_map.get(state_str.lower(), MarketRegime.SIDEWAYS)
            
            return HMMSignal(
                state=state,
                state_probability=result.state_probability,
                confidence=result.confidence,
                regime_change_signal=result.regime_change_signal,
                state_duration=result.state_duration,
            )
        except Exception as e:
            logger.debug(f"HMM分析失败: {e}")
            return None
    
    def _ensemble_combine(
        self,
        period_signals: Dict[str, PeriodSignal],
        hmm_signal: Optional[HMMSignal]
    ) -> Tuple[float, TrendDirection, float]:
        """
        加权融合
        
        权重：Trend 0.8 + HMM 0.2
        """
        trend_weight = self.config.weights.get("trend", 0.8)
        hmm_weight = self.config.weights.get("hmm", 0.2)
        
        # 趋势得分加权平均 (周期间等权)
        if period_signals:
            period_scores = [s.score for s in period_signals.values()]
            trend_score = np.mean(period_scores)
            trend_confidence = np.mean([s.confidence for s in period_signals.values()])
        else:
            trend_score = 0
            trend_confidence = 0
        
        # HMM得分
        if hmm_signal:
            hmm_state_score = {
                MarketRegime.BULL: 60,
                MarketRegime.BEAR: -60,
                MarketRegime.SIDEWAYS: 0,
            }
            hmm_score = hmm_state_score.get(hmm_signal.state, 0)
            hmm_confidence = hmm_signal.confidence
        else:
            hmm_score = 0
            hmm_confidence = 0
            hmm_weight = 0
            trend_weight = 1.0  # 无HMM时，全部用趋势
        
        # 加权融合
        ensemble_score = trend_score * trend_weight + hmm_score * hmm_weight
        ensemble_confidence = trend_confidence * trend_weight + hmm_confidence * hmm_weight
        
        # 一致性加成
        if period_signals and hmm_signal:
            trend_direction = 1 if trend_score > 20 else (-1 if trend_score < -20 else 0)
            hmm_direction = 1 if hmm_signal.state == MarketRegime.BULL else (-1 if hmm_signal.state == MarketRegime.BEAR else 0)
            
            if trend_direction == hmm_direction and trend_direction != 0:
                ensemble_confidence = min(1.0, ensemble_confidence + 0.1)  # 一致性加成
        
        direction = self._score_to_direction(ensemble_score)
        
        return ensemble_score, direction, ensemble_confidence
    
    def _generate_workflow_params(
        self,
        ensemble_score: float,
        ensemble_direction: TrendDirection,
        hmm_signal: Optional[HMMSignal]
    ) -> WorkflowParams:
        """生成工作流参数"""
        
        # 目标仓位
        if ensemble_score > 60:
            position_target = 0.9
        elif ensemble_score > 30:
            position_target = 0.7
        elif ensemble_score > 0:
            position_target = 0.5
        elif ensemble_score > -30:
            position_target = 0.3
        else:
            position_target = 0.1
        
        # 风险预算
        risk_budget = 0.02 if ensemble_score > 0 else 0.01
        
        # 允许的操作
        allowed_actions = {
            "allow_buy": ensemble_score > -20,
            "allow_add": ensemble_score > 20,
            "allow_reduce": ensemble_score < 30,
            "allow_sell": ensemble_score < -20,
            "allow_new_positions": ensemble_score > 0,
        }
        
        # 调仓频率
        if hmm_signal and hmm_signal.regime_change_signal:
            rebalance_frequency = "immediate"
        elif abs(ensemble_score) > 50:
            rebalance_frequency = "weekly"
        else:
            rebalance_frequency = "monthly"
        
        # 市场状态标签
        regime_tag = ensemble_direction.value
        
        return WorkflowParams(
            position_target=position_target,
            risk_budget=risk_budget,
            allowed_actions=allowed_actions,
            rebalance_frequency=rebalance_frequency,
            regime_tag=regime_tag,
        )
    
    def _generate_investment_filters(
        self,
        ensemble_score: float,
        ensemble_direction: TrendDirection,
        period_signals: Dict[str, PeriodSignal]
    ) -> InvestmentUniverseFilters:
        """生成投资标的筛选参数"""
        
        # 根据市场状态调整筛选条件
        if ensemble_score > 30:
            # 牛市：放宽条件，追求进攻
            min_momentum = 20
            min_trend = 10
            max_vol = 0.5
            prefer_sectors = ["科技", "消费", "新能源"]
            avoid_sectors = []
        elif ensemble_score > 0:
            # 震荡偏多：均衡
            min_momentum = 30
            min_trend = 20
            max_vol = 0.4
            prefer_sectors = ["消费", "医药"]
            avoid_sectors = ["周期"]
        elif ensemble_score > -30:
            # 震荡偏空：防守
            min_momentum = 40
            min_trend = 30
            max_vol = 0.3
            prefer_sectors = ["公用事业", "消费"]
            avoid_sectors = ["科技", "周期"]
        else:
            # 熊市：高门槛
            min_momentum = 60
            min_trend = 50
            max_vol = 0.25
            prefer_sectors = ["公用事业", "银行"]
            avoid_sectors = ["科技", "周期", "新能源"]
        
        return InvestmentUniverseFilters(
            min_momentum_score=min_momentum,
            min_trend_score=min_trend,
            max_volatility=max_vol,
            sector_preferences=prefer_sectors,
            avoid_sectors=avoid_sectors,
        )
    
    # ============ A股共振状态系统方法 ============
    
    def analyze_composite(
        self,
        as_of_date: str,
        switch_spec: MarketSwitchSpec = None,
        resonance_config: ResonanceConfig = None,
        confirm_history: Dict[str, int] = None,
    ) -> Optional[MarketTrendSignal]:
        """
        多指数共振分析（市场总开关）
        
        Args:
            as_of_date: 分析日期
            switch_spec: 市场开关规格（默认沪深300+中证1000）
            resonance_config: 共振配置
            confirm_history: 确认历史 {date: confirm_streak}
        
        Returns:
            MarketTrendSignal with market_switch populated
        """
        switch_spec = switch_spec or MarketSwitchSpec()
        resonance_config = resonance_config or ResonanceConfig()
        confirm_history = confirm_history or {}
        
        # 分析各指数
        index_signals: Dict[str, MarketTrendSignal] = {}
        index_scores: Dict[str, float] = {}
        auxiliary_scores: Dict[str, float] = {}
        
        for idx in switch_spec.indices:
            signal = self.analyze(idx, as_of_date)
            if signal:
                index_signals[idx] = signal
                index_scores[idx] = signal.ensemble_score
        
        # 分析辅助指数（不参与主开关）
        for idx in switch_spec.auxiliary_indices:
            signal = self.analyze(idx, as_of_date)
            if signal:
                auxiliary_scores[idx] = signal.ensemble_score
        
        if not index_scores:
            logger.warning(f"无有效指数信号: {as_of_date}")
            return None
        
        # 计算加权合成得分
        composite_score = calculate_composite_score(index_scores, switch_spec)
        
        # 确定共振阶段
        period_scores_all = {}
        for idx, sig in index_signals.items():
            for period, ps in sig.period_signals.items():
                key = f"{idx}_{period}"
                period_scores_all[key] = ps.score
        
        phase = determine_resonance_phase(period_scores_all)
        
        # 获取确认streak
        prev_date = self._get_prev_trading_date(as_of_date)
        prev_streak = confirm_history.get(prev_date, 0)
        
        # 判断是否确认
        if self._is_resonance_confirmed(phase, composite_score):
            confirm_streak = prev_streak + 1
        else:
            confirm_streak = 0
        
        # 计算仓位上限
        pos_cap = position_cap_mapping(composite_score, confirm_streak, resonance_config)
        
        # 计算波动率（用于策略模式判断）
        volatility = self._estimate_market_volatility(index_signals)
        
        # 确定策略模式
        strat_mode = determine_strategy_mode(composite_score, volatility, confirm_streak)
        
        # 构建市场开关输出
        market_switch = MarketSwitchOutput(
            date=as_of_date,
            indices=list(switch_spec.indices),
            index_scores=index_scores,
            composite_score=composite_score,
            phase=phase,
            confirm_streak=confirm_streak,
            position_cap=pos_cap,
            strategy_mode=strat_mode,
            allowed_long=composite_score > -20 and confirm_streak >= 0,
            auxiliary_scores=auxiliary_scores,
            volatility=volatility,
        )
        
        # 生成扩展的投资标的筛选参数
        extended_filters = self._generate_extended_filters(
            composite_score, phase, confirm_streak, resonance_config
        )
        
        # 取第一个指数的信号作为基础（保持兼容）
        first_idx = switch_spec.indices[0]
        base_signal = index_signals.get(first_idx)
        
        if base_signal is None:
            # 如果第一个指数无信号，用空的基础结构
            return None
        
        # 更新基础信号的共振状态字段
        base_signal.market_switch = market_switch
        base_signal.position_cap = pos_cap
        base_signal.strategy_mode = strat_mode
        base_signal.extended_filters = extended_filters
        base_signal.resonance_phase = phase
        base_signal.confirm_streak = confirm_streak
        
        # ===== 新增：基于合成得分计算14种市场阶段 =====
        # 使用各指数的平均周期得分
        avg_period_scores = self._calculate_avg_period_scores(index_signals)
        if avg_period_scores:
            market_phase, phase_position = self._determine_market_phase(avg_period_scores)
            base_signal.market_phase = market_phase
            base_signal.market_phase_position = phase_position
        
        base_signal.algorithm_version = "2.1-resonance"
        
        return base_signal
    
    def _is_resonance_confirmed(
        self,
        phase: ResonancePhase,
        score: float,
        threshold: float = 20.0,
    ) -> bool:
        """判断是否达到共振确认条件"""
        if phase in [ResonancePhase.FULL_BULL, ResonancePhase.FULL_BEAR]:
            return True
        if phase in [ResonancePhase.PARTIAL_BULL, ResonancePhase.PARTIAL_BEAR]:
            return abs(score) > threshold
        return False
    
    def _get_prev_trading_date(self, date_str: str) -> str:
        """获取前一交易日（简化版，实际应调用交易日历）"""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            # 简化：直接减1天（实际应用需要交易日历）
            prev_dt = dt - timedelta(days=1)
            return prev_dt.strftime("%Y-%m-%d")
        except:
            return date_str
    
    def _estimate_market_volatility(
        self,
        index_signals: Dict[str, MarketTrendSignal],
    ) -> float:
        """估计市场波动率（基于各指数信号）"""
        if not index_signals:
            return 0.15  # 默认
        
        # 用各指数得分的标准差作为波动率代理
        scores = [sig.ensemble_score for sig in index_signals.values()]
        if len(scores) < 2:
            return 0.15
        
        std = np.std(scores) / 100  # 归一化
        return max(0.05, min(0.50, std + 0.10))  # 基础波动 + 调整
    
    def _calculate_avg_period_scores(
        self,
        index_signals: Dict[str, MarketTrendSignal],
    ) -> Dict[str, PeriodSignal]:
        """
        计算各指数的平均周期得分
        
        用于多指数共振分析时的14种市场阶段判断
        """
        if not index_signals:
            return {}
        
        # 收集各周期的平均得分
        period_scores: Dict[str, List[float]] = {
            "week": [],
            "month": [],
            "quarter": [],
        }
        
        for idx_code, signal in index_signals.items():
            for period in ["week", "month", "quarter"]:
                if period in signal.period_signals:
                    period_scores[period].append(signal.period_signals[period].score)
        
        # 构建平均PeriodSignal
        avg_signals = {}
        for period, scores in period_scores.items():
            if scores:
                avg_score = np.mean(scores)
                direction = self._score_to_direction(avg_score)
                avg_signals[period] = PeriodSignal(
                    period=period,
                    period_days=self.config.periods.get(period, 21),
                    direction=direction,
                    score=avg_score,
                    confidence=1 - (np.std(scores) / 100) if len(scores) > 1 else 0.5,
                )
        
        return avg_signals
    
    def _generate_extended_filters(
        self,
        composite_score: float,
        phase: ResonancePhase,
        confirm_streak: int,
        config: ResonanceConfig,
    ) -> ExtendedInvestmentFilters:
        """
        生成扩展的投资标的筛选参数（A股本土化）
        """
        # 基础参数（根据市场状态）
        if composite_score >= 40 and confirm_streak >= 2:
            # 确认牛市：放宽条件
            min_mom = 10
            min_trend = 5
            max_vol = 0.50
            rs_min = -5.0
            prefer = ["科技", "消费", "新能源", "半导体"]
            avoid = []
        elif composite_score >= 20:
            # 偏强
            min_mom = 20
            min_trend = 10
            max_vol = 0.45
            rs_min = 0.0
            prefer = ["科技", "消费"]
            avoid = []
        elif composite_score >= 0:
            # 震荡偏多
            min_mom = 30
            min_trend = 20
            max_vol = 0.40
            rs_min = 5.0
            prefer = ["消费", "医药"]
            avoid = ["周期"]
        elif composite_score >= -20:
            # 震荡偏空
            min_mom = 40
            min_trend = 30
            max_vol = 0.35
            rs_min = 10.0
            prefer = ["公用事业", "消费"]
            avoid = ["科技", "周期"]
        else:
            # 熊市
            min_mom = 60
            min_trend = 50
            max_vol = 0.25
            rs_min = 20.0
            prefer = ["公用事业", "银行"]
            avoid = ["科技", "周期", "新能源"]
        
        return ExtendedInvestmentFilters(
            min_momentum_score=min_mom,
            min_trend_score=min_trend,
            max_volatility=max_vol,
            sector_preferences=prefer,
            avoid_sectors=avoid,
            rs_20d_min=rs_min,
            rs_60d_min=rs_min * 0.8,
            rs_120d_min=rs_min * 0.6,
            min_turnover=config.min_turnover,
            min_market_cap=config.min_market_cap,
            max_turnover_rate=0.30,
            max_limit_up_days=3,
            max_gap_pct=8.0,
            max_atr_multiplier=config.atr_abnormal_multiplier,
        )
    
    def batch_analyze_composite(
        self,
        dates: List[str],
        switch_spec: MarketSwitchSpec = None,
        resonance_config: ResonanceConfig = None,
    ) -> List[MarketTrendSignal]:
        """
        批量多日共振分析（带确认streak传递）
        
        Args:
            dates: 日期列表（升序）
            switch_spec: 市场开关规格
            resonance_config: 共振配置
        
        Returns:
            List[MarketTrendSignal]
        """
        results = []
        confirm_history = {}
        
        for date in sorted(dates):
            signal = self.analyze_composite(
                as_of_date=date,
                switch_spec=switch_spec,
                resonance_config=resonance_config,
                confirm_history=confirm_history,
            )
            
            if signal:
                results.append(signal)
                confirm_history[date] = signal.confirm_streak
        
        return results
    
    # ============ 诊断方法 ============
    
    def get_diagnostic_details(self, signal: MarketTrendSignal) -> Dict[str, Any]:
        """
        获取信号的详细诊断信息
        
        用于验证计算过程和调试
        
        Args:
            signal: MarketTrendSignal对象
            
        Returns:
            包含详细诊断信息的字典
        """
        if signal is None:
            return {"error": "无信号数据"}
        
        # 基础信息
        diag = {
            "date": signal.date,
            "index_code": signal.index_code,
            "algorithm_version": signal.algorithm_version,
            "data_source": signal.data_source,
        }
        
        # 各周期原始得分
        period_details = {}
        for period, ps in signal.period_signals.items():
            period_details[period] = {
                "score": round(ps.score, 2),
                "direction": ps.direction.value,
                "confidence": round(ps.confidence, 3),
                "days": ps.period_days,
                "indicators": {k: round(v, 2) if isinstance(v, (int, float)) else v 
                              for k, v in ps.indicators.items()},
            }
        diag["period_details"] = period_details
        
        # HMM状态
        if signal.hmm_signal:
            diag["hmm"] = {
                "state": signal.hmm_signal.state.value,
                "confidence": round(signal.hmm_signal.confidence, 3),
                "state_probability": {k: round(v, 3) for k, v in signal.hmm_signal.state_probability.items()},
                "regime_change": signal.hmm_signal.regime_change_signal,
                "duration": signal.hmm_signal.state_duration,
            }
        else:
            diag["hmm"] = None
        
        # 综合评分
        diag["ensemble"] = {
            "score": round(signal.ensemble_score, 2),
            "direction": signal.ensemble_direction.value,
            "confidence": round(signal.ensemble_confidence, 3),
        }
        
        # 共振状态
        diag["resonance"] = {
            "phase": signal.resonance_phase.value,
            "confirm_streak": signal.confirm_streak,
            "position_cap": round(signal.position_cap, 3),
            "strategy_mode": signal.strategy_mode.value,
        }
        
        # 14种市场阶段
        if signal.market_phase:
            diag["market_phase"] = {
                "phase": signal.market_phase.value,
                "phase_name": signal.market_phase.name,
                "suggested_position": round(signal.market_phase_position, 3),
            }
            # 获取阶段详细描述
            phase_info = PHASE_DESCRIPTIONS.get(signal.market_phase, {})
            if phase_info:
                diag["market_phase"]["description"] = phase_info.get("description", "")
                diag["market_phase"]["action"] = phase_info.get("action", "")
        else:
            diag["market_phase"] = None
        
        # 仓位计算过程
        diag["position_calc"] = {
            "base_position_from_phase": round(signal.market_phase_position, 3) if signal.market_phase else 0.5,
            "position_cap_from_resonance": round(signal.position_cap, 3),
            "final_recommendation": round(signal.workflow_params.position_target, 3),
        }
        
        # 工作流参数
        diag["workflow"] = {
            "position_target": round(signal.workflow_params.position_target, 3),
            "risk_budget": round(signal.workflow_params.risk_budget, 3),
            "allowed_actions": signal.workflow_params.allowed_actions,
            "rebalance_frequency": signal.workflow_params.rebalance_frequency,
            "regime_tag": signal.workflow_params.regime_tag,
        }
        
        return diag
    
    def print_diagnostic(self, signal: MarketTrendSignal) -> str:
        """
        打印格式化的诊断信息
        
        Args:
            signal: MarketTrendSignal对象
            
        Returns:
            格式化的诊断字符串
        """
        diag = self.get_diagnostic_details(signal)
        
        if "error" in diag:
            return f"诊断失败: {diag['error']}"
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"市场趋势分析诊断报告 - {diag['date']}")
        lines.append(f"指数: {diag['index_code']} | 版本: {diag['algorithm_version']}")
        lines.append("=" * 60)
        
        # 综合评分
        ens = diag["ensemble"]
        lines.append(f"\n【综合评分】{ens['score']} ({ens['direction']})")
        lines.append(f"  置信度: {ens['confidence']:.1%}")
        
        # 各周期得分
        lines.append("\n【各周期得分】")
        for period, detail in diag["period_details"].items():
            lines.append(f"  {period}: {detail['score']:+.1f} ({detail['direction']})")
        
        # HMM
        if diag["hmm"]:
            hmm = diag["hmm"]
            lines.append(f"\n【HMM隐状态】{hmm['state']} (置信度: {hmm['confidence']:.1%})")
            probs = hmm["state_probability"]
            lines.append(f"  概率分布: 牛={probs.get('牛市', 0):.1%} 震荡={probs.get('震荡', 0):.1%} 熊={probs.get('熊市', 0):.1%}")
        
        # 共振状态
        res = diag["resonance"]
        lines.append(f"\n【共振状态】{res['phase']}")
        lines.append(f"  确认次数: {res['confirm_streak']}")
        lines.append(f"  仓位上限: {res['position_cap']:.0%}")
        lines.append(f"  策略模式: {res['strategy_mode']}")
        
        # 14种市场阶段
        if diag["market_phase"]:
            mp = diag["market_phase"]
            lines.append(f"\n【14种市场阶段】{mp['phase']}")
            lines.append(f"  阶段代码: {mp['phase_name']}")
            lines.append(f"  建议仓位: {mp['suggested_position']:.0%}")
            if "description" in mp:
                lines.append(f"  描述: {mp['description']}")
            if "action" in mp:
                lines.append(f"  建议操作: {mp['action']}")
        
        # 仓位建议
        pc = diag["position_calc"]
        lines.append("\n【仓位建议】")
        lines.append(f"  阶段建议: {pc['base_position_from_phase']:.0%}")
        lines.append(f"  共振调整: {pc['position_cap_from_resonance']:.0%}")
        lines.append(f"  最终目标: {pc['final_recommendation']:.0%}")
        
        # 工作流
        wf = diag["workflow"]
        lines.append("\n【工作流参数】")
        lines.append(f"  目标仓位: {wf['position_target']:.0%}")
        lines.append(f"  调仓频率: {wf['rebalance_frequency']}")
        lines.append(f"  允许操作: 买入={wf['allowed_actions'].get('allow_buy', False)} "
                    f"加仓={wf['allowed_actions'].get('allow_add', False)} "
                    f"减仓={wf['allowed_actions'].get('allow_reduce', False)}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)