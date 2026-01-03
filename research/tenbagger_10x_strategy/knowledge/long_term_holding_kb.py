"""
长期持有知识库 - 十倍股长期持有策略
基于投资大师经验和历史十倍股特征构建

核心理念：十倍股需要"让利润奔跑"，但也要有明确的退出机制
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import numpy as np


class HoldingSignal(Enum):
    """持有信号"""
    STRONG_HOLD = "STRONG_HOLD"       # 强烈持有
    HOLD = "HOLD"                     # 继续持有
    REDUCE = "REDUCE"                 # 减仓
    EXIT = "EXIT"                     # 退出


class ExitReason(Enum):
    """退出原因"""
    FUNDAMENTAL_DETERIORATION = "基本面恶化"
    STAGE_TRANSITION = "阶段转换（进入成熟/衰退期）"
    VALUATION_EXTREME = "估值极端（泡沫化）"
    MARKET_REGIME_CHANGE = "市场环境恶化"
    STOP_LOSS = "止损触发"
    TRAILING_STOP = "跟踪止盈触发"
    BETTER_OPPORTUNITY = "更好的机会出现"
    POSITION_LIMIT = "仓位限制"


@dataclass
class LongTermHoldingCriteria:
    """长期持有标准"""
    # 基本面标准
    min_revenue_growth: float = 0.15      # 最低营收增速
    min_profit_growth: float = 0.20       # 最低利润增速
    min_roe: float = 0.15                 # 最低ROE
    max_debt_ratio: float = 0.60          # 最高负债率
    
    # 估值标准
    max_pe: float = 80                    # 最高PE（成长股可以更高）
    max_peg: float = 2.0                  # 最高PEG
    
    # 技术标准
    min_ma_support: int = 60              # 最低均线支撑（60日）
    max_drawdown_from_high: float = 0.30  # 从最高点最大回撤
    
    # 阶段标准
    preferred_stages: List[str] = None    # 优选阶段
    
    def __post_init__(self):
        if self.preferred_stages is None:
            self.preferred_stages = ["S1_EMERGENCE", "S2_ACCELERATION", "S3_EXPANSION"]


# 十倍股长期持有核心原则
LONG_TERM_HOLDING_PRINCIPLES = {
    "原则1_让利润奔跑": {
        "description": "不要过早止盈，十倍股需要时间发酵",
        "rules": [
            "收益<50%时不主动卖出",
            "收益50-100%时可减仓20-30%锁定部分利润",
            "收益>100%后保留核心仓位继续持有",
        ],
        "exceptions": [
            "基本面显著恶化",
            "市场进入熊市恐慌",
            "阶段转换到S4/S5",
        ]
    },
    
    "原则2_阶段跟踪": {
        "description": "根据股票所处阶段调整持有策略",
        "stages": {
            "S1_EMERGENCE": {
                "action": "重仓持有",
                "position": 0.8,
                "reason": "萌芽期是最佳介入时机，潜在收益最大"
            },
            "S2_ACCELERATION": {
                "action": "持有为主",
                "position": 0.6,
                "reason": "加速期业绩兑现中，继续享受成长"
            },
            "S3_EXPANSION": {
                "action": "逐步减仓",
                "position": 0.4,
                "reason": "扩张期增速放缓，开始锁定利润"
            },
            "S4_MATURITY": {
                "action": "清仓",
                "position": 0.0,
                "reason": "成熟期成长故事结束"
            },
            "S5_DECLINE": {
                "action": "立即清仓",
                "position": 0.0,
                "reason": "衰退期风险大于收益"
            }
        }
    },
    
    "原则3_基本面监控": {
        "description": "定期检查基本面，发现恶化及时退出",
        "check_frequency": "每季度财报后",
        "warning_signals": [
            "连续2个季度营收增速下滑",
            "利润增速由正转负",
            "ROE下降超过5个百分点",
            "负债率上升超过10个百分点",
            "经营现金流转负",
        ],
        "exit_signals": [
            "连续2个季度利润下滑",
            "ROE<10%",
            "负债率>70%",
            "出现重大诉讼或财务造假",
        ]
    },
    
    "原则4_市场环境适应": {
        "description": "根据市场环境调整持有策略",
        "regimes": {
            "BULL": {
                "action": "满仓持有",
                "stop_loss_adjustment": 1.2,  # 放宽止损
            },
            "VOLATILE": {
                "action": "正常持有",
                "stop_loss_adjustment": 1.0,
            },
            "BEAR_GRINDING": {
                "action": "减仓观望",
                "stop_loss_adjustment": 0.8,  # 收紧止损
            },
            "BEAR_PANIC": {
                "action": "清仓避险",
                "stop_loss_adjustment": 0.5,
            }
        }
    }
}


# 历史十倍股持有周期参考
HISTORICAL_TENBAGGER_HOLDING_PERIODS = {
    "贵州茅台": {
        "period": "2003-2012",
        "holding_years": 9,
        "return": "50x",
        "key_factors": ["消费升级", "品牌垄断", "提价能力"]
    },
    "格力电器": {
        "period": "2005-2015",
        "holding_years": 10,
        "return": "30x",
        "key_factors": ["行业龙头", "渠道优势", "分红稳定"]
    },
    "恒瑞医药": {
        "period": "2010-2020",
        "holding_years": 10,
        "return": "20x",
        "key_factors": ["研发投入", "创新药", "政策支持"]
    },
    "宁德时代": {
        "period": "2018-2021",
        "holding_years": 3,
        "return": "15x",
        "key_factors": ["新能源", "技术领先", "产能扩张"]
    },
    "隆基绿能": {
        "period": "2017-2021",
        "holding_years": 4,
        "return": "20x",
        "key_factors": ["光伏", "成本优势", "技术迭代"]
    }
}


class LongTermHoldingManager:
    """长期持有管理器"""
    
    def __init__(self, criteria: LongTermHoldingCriteria = None):
        self.criteria = criteria or LongTermHoldingCriteria()
        self.principles = LONG_TERM_HOLDING_PRINCIPLES
    
    def evaluate_holding_signal(
        self,
        current_gain: float,
        max_gain: float,
        stage: str,
        regime: str,
        fundamentals: Dict,
    ) -> Tuple[HoldingSignal, Optional[ExitReason], str]:
        """评估持有信号
        
        Args:
            current_gain: 当前收益率
            max_gain: 历史最高收益率
            stage: 当前阶段
            regime: 市场环境
            fundamentals: 基本面数据
            
        Returns:
            (持有信号, 退出原因, 建议说明)
        """
        
        # 1. 检查阶段
        stage_config = self.principles["原则2_阶段跟踪"]["stages"].get(stage, {})
        if stage in ["S4_MATURITY", "S5_DECLINE"]:
            return (
                HoldingSignal.EXIT,
                ExitReason.STAGE_TRANSITION,
                f"股票进入{stage}阶段，建议清仓"
            )
        
        # 2. 检查市场环境
        regime_config = self.principles["原则4_市场环境适应"]["regimes"]
        if regime == "BEAR_PANIC":
            return (
                HoldingSignal.EXIT,
                ExitReason.MARKET_REGIME_CHANGE,
                "市场进入恐慌，建议清仓避险"
            )
        
        # 3. 检查基本面
        if fundamentals:
            profit_growth = fundamentals.get("profit_growth", 0)
            revenue_growth = fundamentals.get("revenue_growth", 0)
            roe = fundamentals.get("roe", 0)
            
            # 严重恶化
            if profit_growth < -0.20 or roe < 0.10:
                return (
                    HoldingSignal.EXIT,
                    ExitReason.FUNDAMENTAL_DETERIORATION,
                    f"基本面恶化：利润增速{profit_growth*100:.1f}%, ROE{roe*100:.1f}%"
                )
            
            # 轻度恶化
            if profit_growth < self.criteria.min_profit_growth:
                return (
                    HoldingSignal.REDUCE,
                    None,
                    f"利润增速放缓至{profit_growth*100:.1f}%，建议减仓"
                )
        
        # 4. 检查回撤
        if max_gain > 0:
            drawdown = (max_gain - current_gain) / (1 + max_gain)
            if drawdown > self.criteria.max_drawdown_from_high:
                return (
                    HoldingSignal.EXIT,
                    ExitReason.TRAILING_STOP,
                    f"从最高点{max_gain*100:.1f}%回撤{drawdown*100:.1f}%"
                )
        
        # 5. 根据收益水平给出持有建议
        if current_gain > 1.0:  # 翻倍
            return (
                HoldingSignal.STRONG_HOLD,
                None,
                f"收益{current_gain*100:.1f}%已翻倍，保留核心仓位继续持有"
            )
        elif current_gain > 0.5:  # 50%以上
            return (
                HoldingSignal.HOLD,
                None,
                f"收益{current_gain*100:.1f}%，可考虑减仓20-30%锁定部分利润"
            )
        else:
            return (
                HoldingSignal.HOLD,
                None,
                f"收益{current_gain*100:.1f}%，继续持有等待爆发"
            )
    
    def get_position_adjustment(
        self,
        current_position: float,
        signal: HoldingSignal,
        stage: str,
    ) -> float:
        """获取仓位调整建议
        
        Returns:
            目标仓位比例
        """
        stage_config = self.principles["原则2_阶段跟踪"]["stages"].get(stage, {})
        stage_position = stage_config.get("position", 0.5)
        
        if signal == HoldingSignal.EXIT:
            return 0.0
        elif signal == HoldingSignal.REDUCE:
            return min(current_position * 0.5, stage_position)
        elif signal == HoldingSignal.STRONG_HOLD:
            return max(current_position, stage_position * 0.8)
        else:  # HOLD
            return stage_position
    
    def get_holding_duration_target(self, stage: str) -> Tuple[int, int]:
        """获取目标持有周期（月）
        
        Returns:
            (最短持有月数, 建议持有月数)
        """
        duration_map = {
            "S1_EMERGENCE": (12, 36),      # 萌芽期：1-3年
            "S2_ACCELERATION": (6, 24),    # 加速期：6个月-2年
            "S3_EXPANSION": (3, 12),       # 扩张期：3个月-1年
            "S4_MATURITY": (0, 0),         # 成熟期：不建议持有
            "S5_DECLINE": (0, 0),          # 衰退期：不建议持有
        }
        return duration_map.get(stage, (6, 12))


# 导出
__all__ = [
    'HoldingSignal',
    'ExitReason', 
    'LongTermHoldingCriteria',
    'LongTermHoldingManager',
    'LONG_TERM_HOLDING_PRINCIPLES',
    'HISTORICAL_TENBAGGER_HOLDING_PERIODS',
]







































