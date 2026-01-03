#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Batch Profit Taking Knowledge Base - 分批止盈知识库
==================================================

十倍股策略的核心：让利润奔跑，但也要适时锁定收益

策略原则：
1. 不要一次性全部卖出
2. 根据收益水平分批止盈
3. 保留部分筹码等待更大涨幅
4. 根据市场环境和股票阶段调整策略

Author: TRQuant Team
Date: 2025-12-27
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np


class ProfitLevel(Enum):
    """收益水平"""
    LOW = "LOW"           # < 30%
    MEDIUM = "MEDIUM"     # 30-50%
    HIGH = "HIGH"         # 50-100%
    VERY_HIGH = "VERY_HIGH"  # 100-200%
    EXTREME = "EXTREME"   # > 200%


@dataclass
class BatchProfitRule:
    """分批止盈规则"""
    profit_threshold: float  # 收益阈值（如0.5表示50%）
    sell_ratio: float        # 卖出比例（如0.3表示卖出30%）
    keep_ratio: float        # 保留比例（如0.7表示保留70%）
    reason: str              # 原因说明
    next_threshold: Optional[float] = None  # 下一档阈值


# 标准分批止盈规则
BATCH_PROFIT_RULES = [
    BatchProfitRule(
        profit_threshold=0.30,  # 30%收益
        sell_ratio=0.20,         # 卖出20%
        keep_ratio=0.80,         # 保留80%
        reason="首次止盈，锁定部分收益",
        next_threshold=0.50
    ),
    BatchProfitRule(
        profit_threshold=0.50,  # 50%收益
        sell_ratio=0.30,         # 再卖出30%（累计50%）
        keep_ratio=0.50,         # 保留50%
        reason="二次止盈，已锁定50%收益",
        next_threshold=1.00
    ),
    BatchProfitRule(
        profit_threshold=1.00,  # 100%收益（翻倍）
        sell_ratio=0.30,         # 再卖出30%（累计80%）
        keep_ratio=0.20,         # 保留20%
        reason="翻倍止盈，保留少量筹码等待十倍",
        next_threshold=2.00
    ),
    BatchProfitRule(
        profit_threshold=2.00,  # 200%收益（3倍）
        sell_ratio=0.15,         # 再卖出15%（累计95%）
        keep_ratio=0.05,        # 保留5%
        reason="三倍止盈，保留极少量筹码",
        next_threshold=5.00
    ),
    BatchProfitRule(
        profit_threshold=5.00,  # 500%收益（6倍）
        sell_ratio=0.05,         # 再卖出5%（累计100%）
        keep_ratio=0.00,        # 全部卖出
        reason="六倍止盈，全部卖出",
        next_threshold=None
    ),
]


# 根据市场环境调整的规则
REGIME_ADJUSTED_RULES = {
    "BULL": {
        # 牛市：更激进，保留更多筹码
        "profit_threshold_multiplier": 1.2,  # 阈值提高20%
        "sell_ratio_multiplier": 0.8,        # 卖出比例降低20%
    },
    "BEAR": {
        # 熊市：更保守，快速锁定收益
        "profit_threshold_multiplier": 0.8,  # 阈值降低20%
        "sell_ratio_multiplier": 1.2,        # 卖出比例提高20%
    },
    "VOLATILE": {
        # 震荡：标准规则
        "profit_threshold_multiplier": 1.0,
        "sell_ratio_multiplier": 1.0,
    },
}


# 根据股票阶段调整的规则
STAGE_ADJUSTED_RULES = {
    "S1_EMERGENCE": {
        # 萌芽期：保留更多，等待爆发
        "sell_ratio_multiplier": 0.7,
        "keep_ratio_bonus": 0.1,  # 额外保留10%
    },
    "S2_ACCELERATION": {
        # 加速期：标准规则
        "sell_ratio_multiplier": 1.0,
        "keep_ratio_bonus": 0.0,
    },
    "S3_EXPANSION": {
        # 扩张期：更积极止盈
        "sell_ratio_multiplier": 1.2,
        "keep_ratio_bonus": -0.1,  # 减少保留10%
    },
}


class BatchProfitManager:
    """分批止盈管理器"""
    
    def __init__(self):
        self.rules = BATCH_PROFIT_RULES
        self.regime_adjustments = REGIME_ADJUSTED_RULES
        self.stage_adjustments = STAGE_ADJUSTED_RULES
    
    def get_profit_level(self, gain: float) -> ProfitLevel:
        """获取收益水平"""
        if gain < 0.30:
            return ProfitLevel.LOW
        elif gain < 0.50:
            return ProfitLevel.MEDIUM
        elif gain < 1.00:
            return ProfitLevel.HIGH
        elif gain < 2.00:
            return ProfitLevel.VERY_HIGH
        else:
            return ProfitLevel.EXTREME
    
    def should_take_profit(
        self,
        gain: float,
        last_sell_threshold: float,
        regime: str = "VOLATILE",
        stage: str = "S2_ACCELERATION"
    ) -> Tuple[bool, Optional[BatchProfitRule]]:
        """判断是否应该止盈
        
        Args:
            gain: 当前收益（如0.5表示50%）
            last_sell_threshold: 上次卖出的收益阈值
            regime: 市场环境
            stage: 股票阶段
            
        Returns:
            (是否应该止盈, 止盈规则)
        """
        # 找到下一个应该触发的规则
        for rule in self.rules:
            # 检查是否达到阈值
            threshold = rule.profit_threshold
            
            # 根据市场环境调整阈值
            regime_adj = self.regime_adjustments.get(regime, {})
            threshold_mult = regime_adj.get("profit_threshold_multiplier", 1.0)
            adjusted_threshold = threshold * threshold_mult
            
            # 如果已经超过上次阈值，且达到当前阈值
            if gain >= adjusted_threshold and adjusted_threshold > last_sell_threshold:
                # 根据市场环境和阶段调整卖出比例
                sell_ratio = rule.sell_ratio
                regime_sell_mult = regime_adj.get("sell_ratio_multiplier", 1.0)
                stage_adj = self.stage_adjustments.get(stage, {})
                stage_sell_mult = stage_adj.get("sell_ratio_multiplier", 1.0)
                
                adjusted_sell_ratio = sell_ratio * regime_sell_mult * stage_sell_mult
                adjusted_sell_ratio = max(0.1, min(0.5, adjusted_sell_ratio))  # 限制在10%-50%
                
                # 创建调整后的规则
                adjusted_rule = BatchProfitRule(
                    profit_threshold=adjusted_threshold,
                    sell_ratio=adjusted_sell_ratio,
                    keep_ratio=1.0 - adjusted_sell_ratio,
                    reason=f"{rule.reason} (环境:{regime}, 阶段:{stage})",
                    next_threshold=rule.next_threshold
                )
                
                return True, adjusted_rule
        
        return False, None
    
    def calculate_sell_shares(
        self,
        total_shares: int,
        sell_ratio: float
    ) -> int:
        """计算应该卖出的股数
        
        Args:
            total_shares: 总股数
            sell_ratio: 卖出比例
            
        Returns:
            应该卖出的股数（整手）
        """
        sell_shares = int(total_shares * sell_ratio)
        # 取整手（100股的倍数）
        sell_shares = (sell_shares // 100) * 100
        return max(100, sell_shares)  # 至少100股


# 导出
__all__ = [
    'ProfitLevel',
    'BatchProfitRule',
    'BATCH_PROFIT_RULES',
    'REGIME_ADJUSTED_RULES',
    'STAGE_ADJUSTED_RULES',
    'BatchProfitManager',
]







































