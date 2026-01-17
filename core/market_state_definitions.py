"""
统一市场状态定义体系
====================

整合项目中所有市场状态定义，建立4层统一层次结构：

层级结构：
├── 一级：市场环境 (5种) - MarketRegime
│   ├── BULL / BEAR / VOLATILE / RECOVERY / DISTRIBUTION
│
├── 二级：趋势方向 (7种) - TrendDirection
│   ├── STRONG_UP → STRONG_DOWN (得分阈值: 60/30/10/-10/-30/-60)
│
├── 三级：市场阶段 (14种) - MarketPhase
│   ├── 基于多周期共振判定
│
└── 四级：IBD状态 (4种) - IBDStatus
    └── 反转点专用判定

参考文档: docs/MARKET_TREND_ALGORITHMS.md
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


# =============================================================================
# 一级定义：市场环境 (MarketRegime)
# =============================================================================

class MarketRegime(Enum):
    """
    一级：市场环境（5种）
    
    用于判断市场大周期所处位置，指导策略选择。
    """
    BULL = "BULL"                    # 牛市：上升趋势，成交活跃，做多策略
    BEAR = "BEAR"                    # 熊市：下降趋势，避险为主，防守策略
    VOLATILE = "VOLATILE"            # 震荡市：无明显趋势，区间操作
    RECOVERY = "RECOVERY"            # 复苏期：熊转牛过渡，布局时机
    DISTRIBUTION = "DISTRIBUTION"    # 派发期：牛转熊过渡，减仓时机


REGIME_DESCRIPTIONS = {
    MarketRegime.BULL: {
        "name": "牛市",
        "description": "市场处于上升趋势，成交活跃，适合做多策略",
        "strategy": "进攻型配置，偏好成长股",
        "position_range": (0.7, 1.0),
        "color": "#27ae60"
    },
    MarketRegime.BEAR: {
        "name": "熊市",
        "description": "市场处于下降趋势，避险为主",
        "strategy": "防守型配置，保持低仓位",
        "position_range": (0.0, 0.3),
        "color": "#e74c3c"
    },
    MarketRegime.VOLATILE: {
        "name": "震荡市",
        "description": "市场无明显趋势，区间波动",
        "strategy": "高抛低吸，控制仓位",
        "position_range": (0.3, 0.6),
        "color": "#f39c12"
    },
    MarketRegime.RECOVERY: {
        "name": "复苏期",
        "description": "熊转牛过渡阶段，布局时机",
        "strategy": "逐步加仓，关注反转信号",
        "position_range": (0.4, 0.7),
        "color": "#3498db"
    },
    MarketRegime.DISTRIBUTION: {
        "name": "派发期",
        "description": "牛转熊过渡阶段，减仓时机",
        "strategy": "逐步减仓，锁定收益",
        "position_range": (0.3, 0.5),
        "color": "#9b59b6"
    },
}


# =============================================================================
# 二级定义：趋势方向 (TrendDirection)
# =============================================================================

class TrendDirection(Enum):
    """
    二级：趋势方向（7种）
    
    基于综合得分判定，得分范围 -100 到 +100。
    """
    STRONG_UP = "强势上涨"       # score > 60
    UP = "上涨趋势"             # 30 < score <= 60
    WEAK_UP = "弱势上涨"        # 10 < score <= 30
    SIDEWAYS = "震荡盘整"       # -10 <= score <= 10
    WEAK_DOWN = "弱势下跌"      # -30 <= score < -10
    DOWN = "下跌趋势"           # -60 <= score < -30
    STRONG_DOWN = "强势下跌"    # score < -60


# 趋势方向阈值配置
TREND_THRESHOLDS = {
    TrendDirection.STRONG_UP: (60, 100),
    TrendDirection.UP: (30, 60),
    TrendDirection.WEAK_UP: (10, 30),
    TrendDirection.SIDEWAYS: (-10, 10),
    TrendDirection.WEAK_DOWN: (-30, -10),
    TrendDirection.DOWN: (-60, -30),
    TrendDirection.STRONG_DOWN: (-100, -60),
}


TREND_COLORS = {
    TrendDirection.STRONG_UP: "#00C853",
    TrendDirection.UP: "#4CAF50",
    TrendDirection.WEAK_UP: "#8BC34A",
    TrendDirection.SIDEWAYS: "#FFC107",
    TrendDirection.WEAK_DOWN: "#FF9800",
    TrendDirection.DOWN: "#FF5722",
    TrendDirection.STRONG_DOWN: "#F44336",
}


def score_to_trend_direction(score: float) -> TrendDirection:
    """将得分转换为趋势方向"""
    if score > 60:
        return TrendDirection.STRONG_UP
    elif score > 30:
        return TrendDirection.UP
    elif score > 10:
        return TrendDirection.WEAK_UP
    elif score > -10:
        return TrendDirection.SIDEWAYS
    elif score > -30:
        return TrendDirection.WEAK_DOWN
    elif score > -60:
        return TrendDirection.DOWN
    else:
        return TrendDirection.STRONG_DOWN


# =============================================================================
# 三级定义：市场阶段 (MarketPhase)
# =============================================================================

class MarketPhase(Enum):
    """
    三级：市场阶段（14种）
    
    基于多周期共振分析判定，需要短/中/长三个周期的趋势信号。
    """
    # 牛市系列（5种）
    BULL_CONFIRM_RESONANCE = "牛市确认(全周期共振)"  # 短+中+长全部看涨
    BULL_CONFIRM = "牛市确认"                        # 长期>30, 中期>20, 短期>0
    BULL_SHAKE = "牛市震荡"                          # 长期>30, 中期>0
    BULL_SHORT_ADJUST = "牛市短期调整"               # 长期>30, 短期<-20
    BULL_MID_ADJUST = "牛市中期调整"                 # 长期>30, 其他
    
    # 熊市系列（5种）
    BEAR_CONFIRM_RESONANCE = "熊市确认(全周期共振)"  # 短+中+长全部看跌
    BEAR_CONFIRM = "熊市确认"                        # 长期<-30, 中期<-20, 短期<0
    BEAR_BOUNCE = "熊市反弹"                         # 长期<-30, 中期<0
    BEAR_TECH_BOUNCE = "熊市技术反弹"                # 长期<-30, 短期>20
    BEAR_BOTTOM = "熊市筑底"                         # 长期<-30, 其他
    
    # 震荡系列（4种）
    BREAKTHROUGH = "突破在即"                        # 震荡中，全周期转多
    BREAK_RISK = "破位风险"                          # 震荡中，全周期转空
    RECOVERY_EARLY = "复苏初期"                      # 短期>20, 中期>0
    TOP_FALL = "见顶回落"                            # 短期<-20, 中期<0
    NARROW_RANGE = "窄幅震荡"                        # |短期|<15, |中期|<15
    WIDE_RANGE = "宽幅震荡"                          # 其他情况


PHASE_DESCRIPTIONS = {
    # 牛市系列
    MarketPhase.BULL_CONFIRM_RESONANCE: {
        "name": "牛市确认(全周期共振)",
        "description": "短中长期全部看涨，趋势最强",
        "action": "全仓持有，追强势股",
        "position_suggestion": 1.0,
        "color": "#00C853"
    },
    MarketPhase.BULL_CONFIRM: {
        "name": "牛市确认",
        "description": "长期和中期看涨，短期跟随",
        "action": "高仓位持有",
        "position_suggestion": 0.8,
        "color": "#4CAF50"
    },
    MarketPhase.BULL_SHAKE: {
        "name": "牛市震荡",
        "description": "长期看涨但中期不确定",
        "action": "持仓观望，等待方向",
        "position_suggestion": 0.6,
        "color": "#8BC34A"
    },
    MarketPhase.BULL_SHORT_ADJUST: {
        "name": "牛市短期调整",
        "description": "长期看涨但短期下跌",
        "action": "短期避险，逢低加仓",
        "position_suggestion": 0.5,
        "color": "#CDDC39"
    },
    MarketPhase.BULL_MID_ADJUST: {
        "name": "牛市中期调整",
        "description": "长期看涨，中期调整",
        "action": "控制仓位，耐心等待",
        "position_suggestion": 0.5,
        "color": "#FFEB3B"
    },
    
    # 熊市系列
    MarketPhase.BEAR_CONFIRM_RESONANCE: {
        "name": "熊市确认(全周期共振)",
        "description": "短中长期全部看跌，风险最大",
        "action": "空仓观望，保护本金",
        "position_suggestion": 0.0,
        "color": "#F44336"
    },
    MarketPhase.BEAR_CONFIRM: {
        "name": "熊市确认",
        "description": "长期和中期看跌",
        "action": "低仓位防守",
        "position_suggestion": 0.1,
        "color": "#E53935"
    },
    MarketPhase.BEAR_BOUNCE: {
        "name": "熊市反弹",
        "description": "长期看跌但中期企稳",
        "action": "反弹减仓",
        "position_suggestion": 0.2,
        "color": "#FF5722"
    },
    MarketPhase.BEAR_TECH_BOUNCE: {
        "name": "熊市技术反弹",
        "description": "长期看跌但短期强势反弹",
        "action": "快进快出",
        "position_suggestion": 0.3,
        "color": "#FF7043"
    },
    MarketPhase.BEAR_BOTTOM: {
        "name": "熊市筑底",
        "description": "长期看跌，正在筑底",
        "action": "观察企稳信号",
        "position_suggestion": 0.15,
        "color": "#FF8A65"
    },
    
    # 震荡系列
    MarketPhase.BREAKTHROUGH: {
        "name": "突破在即",
        "description": "震荡中全周期转多",
        "action": "准备加仓",
        "position_suggestion": 0.6,
        "color": "#03A9F4"
    },
    MarketPhase.BREAK_RISK: {
        "name": "破位风险",
        "description": "震荡中全周期转空",
        "action": "准备减仓",
        "position_suggestion": 0.3,
        "color": "#9C27B0"
    },
    MarketPhase.RECOVERY_EARLY: {
        "name": "复苏初期",
        "description": "短期转强，中期跟随",
        "action": "逐步加仓",
        "position_suggestion": 0.5,
        "color": "#00BCD4"
    },
    MarketPhase.TOP_FALL: {
        "name": "见顶回落",
        "description": "短期转弱，中期跟随",
        "action": "逐步减仓",
        "position_suggestion": 0.4,
        "color": "#673AB7"
    },
    MarketPhase.NARROW_RANGE: {
        "name": "窄幅震荡",
        "description": "各周期均无明显趋势",
        "action": "观望为主",
        "position_suggestion": 0.4,
        "color": "#9E9E9E"
    },
    MarketPhase.WIDE_RANGE: {
        "name": "宽幅震荡",
        "description": "短期波动大，中期方向不明",
        "action": "高抛低吸",
        "position_suggestion": 0.4,
        "color": "#607D8B"
    },
}


def determine_market_phase(
    short_score: float, 
    medium_score: float, 
    long_score: float
) -> MarketPhase:
    """
    根据三周期得分判定市场阶段
    
    Args:
        short_score: 短期得分 (-100 to 100)
        medium_score: 中期得分 (-100 to 100)
        long_score: 长期得分 (-100 to 100)
    
    Returns:
        MarketPhase: 市场阶段
    """
    # 检查全周期共振
    all_bullish = all(s > 10 for s in [short_score, medium_score, long_score])
    all_bearish = all(s < -10 for s in [short_score, medium_score, long_score])
    
    # 基于长期趋势判断大方向
    if long_score > 30:
        # 牛市系列
        if all_bullish:
            return MarketPhase.BULL_CONFIRM_RESONANCE
        elif medium_score > 20 and short_score > 0:
            return MarketPhase.BULL_CONFIRM
        elif medium_score > 0:
            return MarketPhase.BULL_SHAKE
        elif short_score < -20:
            return MarketPhase.BULL_SHORT_ADJUST
        else:
            return MarketPhase.BULL_MID_ADJUST
    
    elif long_score < -30:
        # 熊市系列
        if all_bearish:
            return MarketPhase.BEAR_CONFIRM_RESONANCE
        elif medium_score < -20 and short_score < 0:
            return MarketPhase.BEAR_CONFIRM
        elif medium_score < 0:
            return MarketPhase.BEAR_BOUNCE
        elif short_score > 20:
            return MarketPhase.BEAR_TECH_BOUNCE
        else:
            return MarketPhase.BEAR_BOTTOM
    
    else:
        # 震荡系列
        if all_bullish:
            return MarketPhase.BREAKTHROUGH
        elif all_bearish:
            return MarketPhase.BREAK_RISK
        elif short_score > 20 and medium_score > 0:
            return MarketPhase.RECOVERY_EARLY
        elif short_score < -20 and medium_score < 0:
            return MarketPhase.TOP_FALL
        elif abs(short_score) < 15 and abs(medium_score) < 15:
            return MarketPhase.NARROW_RANGE
        else:
            return MarketPhase.WIDE_RANGE


# =============================================================================
# 四级定义：IBD状态 (IBDStatus)
# =============================================================================

class IBDStatus(Enum):
    """
    四级：IBD市场状态（4种）
    
    基于IBD (Investor's Business Daily) 方法论，
    用于反转点识别和精准入场。
    """
    CONFIRMED_UPTREND = "confirmed_uptrend"   # 确认上涨：出现跟踪日，分布日<5
    UPTREND_UNDER_PRESSURE = "uptrend_pressure"  # 上涨承压：分布日3-5个
    MARKET_IN_CORRECTION = "correction"       # 市场调整：分布日>5或技术破位
    RALLY_ATTEMPT = "rally_attempt"           # 反弹尝试：底部反弹中，未确认


IBD_STATUS_DESCRIPTIONS = {
    IBDStatus.CONFIRMED_UPTREND: {
        "name": "确认上涨",
        "description": "出现有效跟踪日，分布日少于5个",
        "action": "积极做多，追强势股",
        "position_suggestion": 0.8,
        "color": "#27ae60"
    },
    IBDStatus.UPTREND_UNDER_PRESSURE: {
        "name": "上涨承压",
        "description": "出现3-5个分布日，注意风险",
        "action": "谨慎持仓，警惕调整",
        "position_suggestion": 0.5,
        "color": "#f39c12"
    },
    IBDStatus.MARKET_IN_CORRECTION: {
        "name": "市场调整",
        "description": "分布日超过5个或技术破位",
        "action": "降低仓位，保护本金",
        "position_suggestion": 0.2,
        "color": "#e74c3c"
    },
    IBDStatus.RALLY_ATTEMPT: {
        "name": "反弹尝试",
        "description": "底部反弹中，等待跟踪日确认",
        "action": "观望为主，等待信号",
        "position_suggestion": 0.3,
        "color": "#3498db"
    },
}


# =============================================================================
# 综合状态数据结构
# =============================================================================

@dataclass
class UnifiedMarketState:
    """统一市场状态"""
    
    # 分析时间
    timestamp: datetime = field(default_factory=datetime.now)
    analysis_date: str = ""
    index_code: str = "000001.XSHG"
    
    # 四层状态
    regime: MarketRegime = MarketRegime.VOLATILE
    direction: TrendDirection = TrendDirection.SIDEWAYS
    phase: MarketPhase = MarketPhase.NARROW_RANGE
    ibd_status: IBDStatus = IBDStatus.RALLY_ATTEMPT
    
    # 核心得分
    composite_score: float = 0.0      # 综合得分 -100 to 100
    short_term_score: float = 0.0     # 短期得分
    medium_term_score: float = 0.0    # 中期得分
    long_term_score: float = 0.0      # 长期得分
    
    # 风险指标
    risk_score: float = 50.0          # 风险得分 0-100
    volatility: float = 0.0           # 波动率
    distribution_count: int = 0        # 分布日数量
    
    # 建议
    suggested_position: float = 0.5    # 建议仓位 0-1
    suggested_style: str = "balanced"  # 建议风格
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "analysis_date": self.analysis_date,
            "index_code": self.index_code,
            "regime": self.regime.value,
            "regime_name": REGIME_DESCRIPTIONS[self.regime]["name"],
            "direction": self.direction.value,
            "phase": self.phase.value,
            "phase_name": PHASE_DESCRIPTIONS[self.phase]["name"],
            "ibd_status": self.ibd_status.value,
            "ibd_status_name": IBD_STATUS_DESCRIPTIONS[self.ibd_status]["name"],
            "composite_score": self.composite_score,
            "short_term_score": self.short_term_score,
            "medium_term_score": self.medium_term_score,
            "long_term_score": self.long_term_score,
            "risk_score": self.risk_score,
            "volatility": self.volatility,
            "distribution_count": self.distribution_count,
            "suggested_position": self.suggested_position,
            "suggested_style": self.suggested_style,
        }
    
    def get_colors(self) -> Dict[str, str]:
        """获取各层级颜色"""
        return {
            "regime": REGIME_DESCRIPTIONS[self.regime]["color"],
            "direction": TREND_COLORS[self.direction],
            "phase": PHASE_DESCRIPTIONS[self.phase]["color"],
            "ibd_status": IBD_STATUS_DESCRIPTIONS[self.ibd_status]["color"],
        }
    
    def get_action_summary(self) -> str:
        """获取操作建议摘要"""
        phase_action = PHASE_DESCRIPTIONS[self.phase]["action"]
        ibd_action = IBD_STATUS_DESCRIPTIONS[self.ibd_status]["action"]
        return f"阶段建议: {phase_action} | IBD建议: {ibd_action}"


# =============================================================================
# 状态转换矩阵
# =============================================================================

# 市场环境转换概率矩阵 (基于历史统计)
REGIME_TRANSITION_MATRIX = {
    # from -> {to: probability}
    MarketRegime.BULL: {
        MarketRegime.BULL: 0.80,
        MarketRegime.DISTRIBUTION: 0.15,
        MarketRegime.VOLATILE: 0.05,
    },
    MarketRegime.BEAR: {
        MarketRegime.BEAR: 0.75,
        MarketRegime.RECOVERY: 0.15,
        MarketRegime.VOLATILE: 0.10,
    },
    MarketRegime.VOLATILE: {
        MarketRegime.VOLATILE: 0.60,
        MarketRegime.BULL: 0.15,
        MarketRegime.BEAR: 0.15,
        MarketRegime.RECOVERY: 0.05,
        MarketRegime.DISTRIBUTION: 0.05,
    },
    MarketRegime.RECOVERY: {
        MarketRegime.BULL: 0.50,
        MarketRegime.VOLATILE: 0.30,
        MarketRegime.RECOVERY: 0.15,
        MarketRegime.BEAR: 0.05,
    },
    MarketRegime.DISTRIBUTION: {
        MarketRegime.BEAR: 0.45,
        MarketRegime.VOLATILE: 0.30,
        MarketRegime.DISTRIBUTION: 0.15,
        MarketRegime.BULL: 0.10,
    },
}


def get_transition_probability(from_regime: MarketRegime, to_regime: MarketRegime) -> float:
    """获取状态转换概率"""
    return REGIME_TRANSITION_MATRIX.get(from_regime, {}).get(to_regime, 0.0)


# =============================================================================
# 辅助函数
# =============================================================================

def map_regime_to_phase(regime: MarketRegime) -> List[MarketPhase]:
    """获取市场环境对应的可能阶段"""
    mapping = {
        MarketRegime.BULL: [
            MarketPhase.BULL_CONFIRM_RESONANCE,
            MarketPhase.BULL_CONFIRM,
            MarketPhase.BULL_SHAKE,
            MarketPhase.BULL_SHORT_ADJUST,
            MarketPhase.BULL_MID_ADJUST,
        ],
        MarketRegime.BEAR: [
            MarketPhase.BEAR_CONFIRM_RESONANCE,
            MarketPhase.BEAR_CONFIRM,
            MarketPhase.BEAR_BOUNCE,
            MarketPhase.BEAR_TECH_BOUNCE,
            MarketPhase.BEAR_BOTTOM,
        ],
        MarketRegime.VOLATILE: [
            MarketPhase.NARROW_RANGE,
            MarketPhase.WIDE_RANGE,
        ],
        MarketRegime.RECOVERY: [
            MarketPhase.BREAKTHROUGH,
            MarketPhase.RECOVERY_EARLY,
        ],
        MarketRegime.DISTRIBUTION: [
            MarketPhase.BREAK_RISK,
            MarketPhase.TOP_FALL,
        ],
    }
    return mapping.get(regime, [])


def get_all_phases() -> List[Dict[str, Any]]:
    """获取所有阶段的详细信息"""
    return [
        {
            "phase": phase,
            "name": info["name"],
            "description": info["description"],
            "action": info["action"],
            "position": info["position_suggestion"],
            "color": info["color"],
        }
        for phase, info in PHASE_DESCRIPTIONS.items()
    ]


def get_position_by_phase(phase: MarketPhase) -> float:
    """根据市场阶段获取建议仓位"""
    return PHASE_DESCRIPTIONS.get(phase, {}).get("position_suggestion", 0.5)


def get_color_by_score(score: float) -> str:
    """根据得分获取颜色"""
    direction = score_to_trend_direction(score)
    return TREND_COLORS.get(direction, "#9E9E9E")


# 导出
__all__ = [
    # 枚举类
    "MarketRegime",
    "TrendDirection", 
    "MarketPhase",
    "IBDStatus",
    # 数据结构
    "UnifiedMarketState",
    # 配置字典
    "REGIME_DESCRIPTIONS",
    "TREND_THRESHOLDS",
    "TREND_COLORS",
    "PHASE_DESCRIPTIONS",
    "IBD_STATUS_DESCRIPTIONS",
    "REGIME_TRANSITION_MATRIX",
    # 函数
    "score_to_trend_direction",
    "determine_market_phase",
    "get_transition_probability",
    "map_regime_to_phase",
    "get_all_phases",
    "get_position_by_phase",
    "get_color_by_score",
]
