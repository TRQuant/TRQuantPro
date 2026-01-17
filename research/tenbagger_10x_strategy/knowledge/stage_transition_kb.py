"""
阶段转换判断知识库 - 十倍股生命周期阶段识别与转换预测

基于StageMachine模型，增强阶段转换的预判能力
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import numpy as np


class TenbaggerStage(Enum):
    """十倍股生命周期阶段"""
    S0_SEED = "S0_SEED"               # 种子期：尚未显现
    S1_EMERGENCE = "S1_EMERGENCE"     # 萌芽期：开始显现潜力
    S2_ACCELERATION = "S2_ACCELERATION"  # 加速期：业绩爆发
    S3_EXPANSION = "S3_EXPANSION"     # 扩张期：稳定增长
    S4_MATURITY = "S4_MATURITY"       # 成熟期：增速放缓
    S5_DECLINE = "S5_DECLINE"         # 衰退期：业绩下滑


class TransitionDirection(Enum):
    """转换方向"""
    UPGRADE = "UPGRADE"       # 升级（向更好的阶段）
    DOWNGRADE = "DOWNGRADE"   # 降级（向更差的阶段）
    STABLE = "STABLE"         # 稳定（保持当前阶段）


@dataclass
class StageTransitionSignal:
    """阶段转换信号"""
    current_stage: TenbaggerStage
    predicted_stage: TenbaggerStage
    direction: TransitionDirection
    confidence: float           # 置信度 0-1
    time_horizon: int          # 预测时间范围（天）
    key_factors: List[str]     # 关键因素
    action_suggestion: str     # 行动建议


# 阶段转换条件定义
STAGE_TRANSITION_CONDITIONS = {
    # S0 → S1: 种子期 → 萌芽期
    "S0_to_S1": {
        "name": "潜力显现",
        "conditions": {
            "revenue_growth": "> 0.20",       # 营收增速>20%
            "profit_growth": "> 0.15",        # 利润增速>15%
            "market_cap": "< 100亿",          # 市值<100亿
            "roe": "> 0.08",                  # ROE>8%
        },
        "early_signals": [
            "新产品/服务获得市场认可",
            "客户数量快速增长",
            "行业景气度上升",
            "管理层增持",
        ],
        "confidence_boost": {
            "insider_buying": 0.10,           # 管理层买入
            "institutional_inflow": 0.15,     # 机构流入
            "industry_uptrend": 0.10,         # 行业上行
        }
    },
    
    # S1 → S2: 萌芽期 → 加速期
    "S1_to_S2": {
        "name": "业绩爆发",
        "conditions": {
            "revenue_growth": "> 0.30",       # 营收增速>30%
            "profit_growth": "> 0.40",        # 利润增速>40%
            "roe": "> 0.12",                  # ROE>12%
            "gross_margin_trend": "上升",     # 毛利率趋势上升
        },
        "early_signals": [
            "订单/合同大幅增加",
            "产能扩张计划",
            "新市场/渠道突破",
            "研发成果落地",
        ],
        "confidence_boost": {
            "order_surge": 0.20,              # 订单激增
            "capacity_expansion": 0.15,       # 产能扩张
            "new_market_entry": 0.10,         # 新市场进入
        }
    },
    
    # S2 → S3: 加速期 → 扩张期
    "S2_to_S3": {
        "name": "稳定扩张",
        "conditions": {
            "revenue_growth": "0.15-0.30",    # 营收增速15-30%
            "profit_growth": "0.20-0.40",     # 利润增速20-40%
            "market_cap": "100-500亿",        # 市值100-500亿
            "roe": "> 0.15",                  # ROE>15%
        },
        "early_signals": [
            "增速从高位回落但仍稳健",
            "市场份额稳定增加",
            "开始关注分红/回购",
            "估值趋于合理",
        ],
        "confidence_boost": {
            "stable_growth": 0.15,            # 稳定增长
            "market_share_gain": 0.10,        # 市场份额提升
            "dividend_policy": 0.10,          # 分红政策
        }
    },
    
    # S3 → S4: 扩张期 → 成熟期
    "S3_to_S4": {
        "name": "增速放缓",
        "conditions": {
            "revenue_growth": "< 0.15",       # 营收增速<15%
            "profit_growth": "< 0.15",        # 利润增速<15%
            "market_cap": "> 500亿",          # 市值>500亿
        },
        "warning_signals": [
            "连续2-3个季度增速下滑",
            "行业竞争加剧",
            "新业务进展缓慢",
            "管理层减持",
        ],
        "confidence_boost": {
            "growth_deceleration": 0.20,      # 增速下滑
            "competition_increase": 0.15,     # 竞争加剧
            "insider_selling": 0.15,          # 内部人减持
        }
    },
    
    # S4 → S5: 成熟期 → 衰退期
    "S4_to_S5": {
        "name": "业绩下滑",
        "conditions": {
            "revenue_growth": "< 0",          # 营收负增长
            "profit_growth": "< -0.10",       # 利润大幅下滑
            "roe_trend": "持续下降",          # ROE持续下降
        },
        "warning_signals": [
            "核心业务萎缩",
            "客户流失",
            "成本上升利润下滑",
            "现金流恶化",
        ],
        "confidence_boost": {
            "revenue_decline": 0.25,          # 营收下滑
            "customer_loss": 0.20,            # 客户流失
            "cash_flow_deterioration": 0.15,  # 现金流恶化
        }
    }
}


# 阶段特征指标
STAGE_CHARACTERISTICS = {
    TenbaggerStage.S0_SEED: {
        "revenue_growth_range": (0, 0.20),
        "profit_growth_range": (-0.10, 0.15),
        "market_cap_range": (0, 50),          # 亿元
        "roe_range": (0, 0.08),
        "typical_pe_range": (0, 100),         # 可能亏损
        "investment_suggestion": "观察等待",
    },
    TenbaggerStage.S1_EMERGENCE: {
        "revenue_growth_range": (0.15, 0.40),
        "profit_growth_range": (0.10, 0.50),
        "market_cap_range": (20, 100),
        "roe_range": (0.08, 0.15),
        "typical_pe_range": (30, 60),
        "investment_suggestion": "重点关注，择机介入",
    },
    TenbaggerStage.S2_ACCELERATION: {
        "revenue_growth_range": (0.25, 0.60),
        "profit_growth_range": (0.30, 1.00),
        "market_cap_range": (50, 300),
        "roe_range": (0.12, 0.25),
        "typical_pe_range": (40, 80),
        "investment_suggestion": "核心持仓，享受成长",
    },
    TenbaggerStage.S3_EXPANSION: {
        "revenue_growth_range": (0.10, 0.30),
        "profit_growth_range": (0.15, 0.40),
        "market_cap_range": (100, 500),
        "roe_range": (0.15, 0.25),
        "typical_pe_range": (25, 50),
        "investment_suggestion": "持有为主，逐步减仓",
    },
    TenbaggerStage.S4_MATURITY: {
        "revenue_growth_range": (0, 0.15),
        "profit_growth_range": (0, 0.15),
        "market_cap_range": (300, 2000),
        "roe_range": (0.10, 0.20),
        "typical_pe_range": (15, 30),
        "investment_suggestion": "清仓离场",
    },
    TenbaggerStage.S5_DECLINE: {
        "revenue_growth_range": (-0.30, 0.05),
        "profit_growth_range": (-0.50, 0),
        "market_cap_range": (0, 500),
        "roe_range": (0, 0.10),
        "typical_pe_range": (0, 20),
        "investment_suggestion": "坚决回避",
    }
}


class StageTransitionPredictor:
    """阶段转换预测器"""
    
    def __init__(self):
        self.conditions = STAGE_TRANSITION_CONDITIONS
        self.characteristics = STAGE_CHARACTERISTICS
    
    def identify_current_stage(
        self,
        revenue_growth: float,
        profit_growth: float,
        market_cap: float,
        roe: float,
    ) -> Tuple[TenbaggerStage, float]:
        """识别当前阶段
        
        Returns:
            (阶段, 置信度)
        """
        best_stage = TenbaggerStage.S0_SEED
        best_score = 0
        
        for stage, chars in self.characteristics.items():
            score = 0
            total = 4
            
            # 检查各指标是否在范围内
            rg_min, rg_max = chars["revenue_growth_range"]
            if rg_min <= revenue_growth <= rg_max:
                score += 1
            
            pg_min, pg_max = chars["profit_growth_range"]
            if pg_min <= profit_growth <= pg_max:
                score += 1
            
            mc_min, mc_max = chars["market_cap_range"]
            if mc_min <= market_cap <= mc_max:
                score += 1
            
            roe_min, roe_max = chars["roe_range"]
            if roe_min <= roe <= roe_max:
                score += 1
            
            confidence = score / total
            if confidence > best_score:
                best_score = confidence
                best_stage = stage
        
        return best_stage, best_score
    
    def predict_transition(
        self,
        current_stage: TenbaggerStage,
        revenue_growth: float,
        profit_growth: float,
        revenue_growth_trend: float,  # 增速变化趋势
        profit_growth_trend: float,
        roe: float,
        market_cap: float,
        additional_signals: List[str] = None,
    ) -> StageTransitionSignal:
        """预测阶段转换
        
        Args:
            current_stage: 当前阶段
            revenue_growth: 营收增速
            profit_growth: 利润增速
            revenue_growth_trend: 营收增速趋势（正=加速，负=减速）
            profit_growth_trend: 利润增速趋势
            roe: ROE
            market_cap: 市值（亿元）
            additional_signals: 额外信号
            
        Returns:
            阶段转换信号
        """
        additional_signals = additional_signals or []
        
        # 判断转换方向
        direction = TransitionDirection.STABLE
        predicted_stage = current_stage
        confidence = 0.5
        key_factors = []
        
        # 根据当前阶段判断可能的转换
        stage_order = list(TenbaggerStage)
        current_idx = stage_order.index(current_stage)
        
        # 检查升级条件
        if current_idx < len(stage_order) - 1:
            next_stage = stage_order[current_idx + 1]
            transition_key = f"{current_stage.value}_to_{next_stage.value}"
            
            # 简化的转换key
            simple_key = f"S{current_idx}_to_S{current_idx + 1}"
            
            if simple_key in self.conditions:
                cond = self.conditions[simple_key]
                
                # 检查基本条件
                upgrade_score = 0
                
                # 增速趋势向好
                if revenue_growth_trend > 0 and profit_growth_trend > 0:
                    upgrade_score += 0.3
                    key_factors.append("增速加速")
                
                # 检查特定阶段条件
                if current_stage == TenbaggerStage.S1_EMERGENCE:
                    if profit_growth > 0.40:
                        upgrade_score += 0.3
                        key_factors.append(f"利润增速{profit_growth*100:.0f}%>40%")
                    if revenue_growth > 0.30:
                        upgrade_score += 0.2
                        key_factors.append(f"营收增速{revenue_growth*100:.0f}%>30%")
                
                if upgrade_score > 0.5:
                    direction = TransitionDirection.UPGRADE
                    predicted_stage = next_stage
                    confidence = min(0.9, 0.5 + upgrade_score)
        
        # 检查降级条件
        if current_idx > 0:
            # 增速持续下滑
            if revenue_growth_trend < -0.05 and profit_growth_trend < -0.05:
                direction = TransitionDirection.DOWNGRADE
                predicted_stage = stage_order[current_idx - 1] if current_idx > 0 else current_stage
                confidence = 0.6
                key_factors.append("增速持续下滑")
            
            # 利润转负
            if profit_growth < -0.10:
                direction = TransitionDirection.DOWNGRADE
                predicted_stage = TenbaggerStage.S5_DECLINE
                confidence = 0.8
                key_factors.append("利润大幅下滑")
        
        # 生成行动建议
        if direction == TransitionDirection.UPGRADE:
            action = f"关注{predicted_stage.value}转换机会，可适当加仓"
        elif direction == TransitionDirection.DOWNGRADE:
            action = f"警惕向{predicted_stage.value}转换，建议减仓"
        else:
            action = "保持当前仓位，继续观察"
        
        return StageTransitionSignal(
            current_stage=current_stage,
            predicted_stage=predicted_stage,
            direction=direction,
            confidence=confidence,
            time_horizon=60,  # 60天预测
            key_factors=key_factors,
            action_suggestion=action,
        )
    
    def get_stage_investment_suggestion(self, stage: TenbaggerStage) -> Dict:
        """获取阶段投资建议"""
        chars = self.characteristics.get(stage, {})
        return {
            "stage": stage.value,
            "suggestion": chars.get("investment_suggestion", "观察"),
            "typical_pe": chars.get("typical_pe_range", (0, 100)),
            "characteristics": chars,
        }


# 导出
__all__ = [
    'TenbaggerStage',
    'TransitionDirection',
    'StageTransitionSignal',
    'StageTransitionPredictor',
    'STAGE_TRANSITION_CONDITIONS',
    'STAGE_CHARACTERISTICS',
]







































