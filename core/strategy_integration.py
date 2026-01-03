"""
策略集成模块
============

将市场环境评估与策略执行集成：
1. 仓位管理策略
2. 风格轮动策略
3. 风险控制策略
"""

import logging
from dataclasses import dataclass
from typing import Dict, Optional, List, Any
from datetime import datetime

from .dynamic_signals import (
    get_dynamic_signal_provider,
    DynamicSignals,
    suggested_position_ratio,
    allocation_style_shift,
    risk_exposure_score,
    trade_frequency_suggestion,
)
from .market_environment_evaluator import get_market_environment_evaluator

logger = logging.getLogger(__name__)


@dataclass
class PositionDecision:
    """仓位决策"""
    target_position: float  # 目标仓位 0-1
    current_position: float  # 当前仓位
    action: str  # "buy", "sell", "hold"
    adjustment_ratio: float  # 调整比例
    reason: str  # 决策原因


@dataclass
class StyleAllocation:
    """风格配置"""
    growth_weight: float  # 成长股权重
    value_weight: float  # 价值股权重
    dividend_weight: float  # 红利股权重
    defensive_weight: float  # 防御股权重
    style_description: str


@dataclass
class RiskControl:
    """风险控制"""
    stop_loss_pct: float  # 止损比例
    take_profit_pct: float  # 止盈比例
    max_single_position: float  # 单只股票最大仓位
    max_sector_exposure: float  # 单行业最大敞口
    risk_level: str  # "low", "medium", "high"


class PositionManager:
    """仓位管理器"""
    
    def __init__(self, signal_provider=None):
        self.signal_provider = signal_provider or get_dynamic_signal_provider()
        
    def calculate_target_position(
        self, 
        current_position: float = 0.0,
        index_code: str = "000001.XSHG"
    ) -> PositionDecision:
        """计算目标仓位"""
        
        # 获取信号
        signals = self.signal_provider.get_all_signals(index_code=index_code)
        target = signals.suggested_position_ratio
        
        # 确定操作
        diff = target - current_position
        if abs(diff) < 0.05:  # 5%以内不调整
            action = "hold"
            adjustment = 0
        elif diff > 0:
            action = "buy"
            adjustment = diff
        else:
            action = "sell"
            adjustment = abs(diff)
        
        # 生成原因
        reasons = []
        if signals.trend_score > 0.3:
            reasons.append("趋势向好")
        elif signals.trend_score < -0.3:
            reasons.append("趋势转弱")
        
        if signals.risk_exposure_score > 70:
            reasons.append("风险偏高")
        
        if signals.market_regime == "bull":
            reasons.append("牛市环境")
        elif signals.market_regime == "bear":
            reasons.append("熊市环境")
        
        reason = ", ".join(reasons) if reasons else "市场中性"
        
        return PositionDecision(
            target_position=target,
            current_position=current_position,
            action=action,
            adjustment_ratio=adjustment,
            reason=reason
        )


class StyleRotator:
    """风格轮动管理器"""
    
    def __init__(self, signal_provider=None):
        self.signal_provider = signal_provider or get_dynamic_signal_provider()
        
    def get_style_allocation(self, index_code: str = "000001.XSHG") -> StyleAllocation:
        """获取风格配置建议"""
        
        signals = self.signal_provider.get_all_signals(index_code=index_code)
        style = signals.allocation_style_shift
        
        # 根据风格建议分配权重
        if style == "growth":
            allocation = StyleAllocation(
                growth_weight=0.6,
                value_weight=0.2,
                dividend_weight=0.1,
                defensive_weight=0.1,
                style_description="偏成长配置：科技、新能源、医药等"
            )
        elif style == "value":
            allocation = StyleAllocation(
                growth_weight=0.2,
                value_weight=0.5,
                dividend_weight=0.2,
                defensive_weight=0.1,
                style_description="偏价值配置：银行、地产、建筑等"
            )
        elif style == "defensive":
            allocation = StyleAllocation(
                growth_weight=0.1,
                value_weight=0.2,
                dividend_weight=0.3,
                defensive_weight=0.4,
                style_description="防御配置：红利股、公用事业、消费等"
            )
        else:  # balanced
            allocation = StyleAllocation(
                growth_weight=0.3,
                value_weight=0.3,
                dividend_weight=0.2,
                defensive_weight=0.2,
                style_description="均衡配置：各风格均衡"
            )
        
        return allocation


class RiskManager:
    """风险管理器"""
    
    def __init__(self, signal_provider=None):
        self.signal_provider = signal_provider or get_dynamic_signal_provider()
        
    def get_risk_parameters(self, index_code: str = "000001.XSHG") -> RiskControl:
        """获取风险控制参数"""
        
        signals = self.signal_provider.get_all_signals(index_code=index_code)
        risk_score = signals.risk_exposure_score
        volatility = signals.volatility_regime
        
        # 根据风险等级调整参数
        if risk_score >= 70 or volatility == "extreme":
            # 高风险：收紧止损，降低仓位上限
            control = RiskControl(
                stop_loss_pct=0.05,  # 5%止损
                take_profit_pct=0.10,  # 10%止盈
                max_single_position=0.05,  # 单只最大5%
                max_sector_exposure=0.15,  # 行业最大15%
                risk_level="high"
            )
        elif risk_score >= 40 or volatility == "high":
            # 中等风险
            control = RiskControl(
                stop_loss_pct=0.08,  # 8%止损
                take_profit_pct=0.15,  # 15%止盈
                max_single_position=0.08,  # 单只最大8%
                max_sector_exposure=0.20,  # 行业最大20%
                risk_level="medium"
            )
        else:
            # 低风险：放宽限制
            control = RiskControl(
                stop_loss_pct=0.10,  # 10%止损
                take_profit_pct=0.20,  # 20%止盈
                max_single_position=0.10,  # 单只最大10%
                max_sector_exposure=0.25,  # 行业最大25%
                risk_level="low"
            )
        
        return control


class IntegratedStrategyManager:
    """综合策略管理器"""
    
    def __init__(self):
        self.signal_provider = get_dynamic_signal_provider()
        self.position_manager = PositionManager(self.signal_provider)
        self.style_rotator = StyleRotator(self.signal_provider)
        self.risk_manager = RiskManager(self.signal_provider)
        
        logger.info("✅ IntegratedStrategyManager 初始化完成")
    
    def get_comprehensive_strategy(
        self, 
        current_position: float = 0.0,
        index_code: str = "000001.XSHG"
    ) -> Dict[str, Any]:
        """获取综合策略建议"""
        
        # 获取各模块建议
        position_decision = self.position_manager.calculate_target_position(
            current_position=current_position,
            index_code=index_code
        )
        
        style_allocation = self.style_rotator.get_style_allocation(index_code=index_code)
        
        risk_control = self.risk_manager.get_risk_parameters(index_code=index_code)
        
        # 获取原始信号
        signals = self.signal_provider.get_all_signals(index_code=index_code)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "index_code": index_code,
            "signals": signals.to_dict(),
            "position": {
                "target": position_decision.target_position,
                "current": position_decision.current_position,
                "action": position_decision.action,
                "adjustment": position_decision.adjustment_ratio,
                "reason": position_decision.reason
            },
            "style": {
                "growth": style_allocation.growth_weight,
                "value": style_allocation.value_weight,
                "dividend": style_allocation.dividend_weight,
                "defensive": style_allocation.defensive_weight,
                "description": style_allocation.style_description
            },
            "risk": {
                "stop_loss": risk_control.stop_loss_pct,
                "take_profit": risk_control.take_profit_pct,
                "max_single": risk_control.max_single_position,
                "max_sector": risk_control.max_sector_exposure,
                "level": risk_control.risk_level
            }
        }
    
    def print_strategy_summary(self, strategy: Dict[str, Any]):
        """打印策略摘要"""
        
        print("\n" + "=" * 60)
        print("综合策略建议")
        print("=" * 60)
        
        signals = strategy["signals"]
        print(f"\n📊 市场信号:")
        print(f"  趋势得分: {signals['trend_score']:.3f}")
        print(f"  市场环境: {signals['market_regime']}")
        print(f"  风险得分: {signals['risk_exposure_score']:.1f}/100")
        
        pos = strategy["position"]
        print(f"\n💰 仓位建议:")
        print(f"  目标仓位: {pos['target']:.1%}")
        print(f"  操作: {pos['action']} ({pos['adjustment']:.1%})")
        print(f"  原因: {pos['reason']}")
        
        style = strategy["style"]
        print(f"\n🎨 风格配置:")
        print(f"  成长: {style['growth']:.0%} | 价值: {style['value']:.0%}")
        print(f"  红利: {style['dividend']:.0%} | 防御: {style['defensive']:.0%}")
        print(f"  {style['description']}")
        
        risk = strategy["risk"]
        print(f"\n⚠️ 风控参数:")
        print(f"  风险等级: {risk['level']}")
        print(f"  止损: {risk['stop_loss']:.1%} | 止盈: {risk['take_profit']:.1%}")
        print(f"  单只上限: {risk['max_single']:.1%} | 行业上限: {risk['max_sector']:.1%}")


# 便捷函数
def get_strategy_manager() -> IntegratedStrategyManager:
    """获取策略管理器实例"""
    global _strategy_manager
    if "_strategy_manager" not in globals():
        _strategy_manager = None
    if _strategy_manager is None:
        _strategy_manager = IntegratedStrategyManager()
    return _strategy_manager


def get_strategy_suggestion(current_position: float = 0.0, index_code: str = "000001.XSHG") -> Dict:
    """获取策略建议（便捷函数）"""
    manager = get_strategy_manager()
    return manager.get_comprehensive_strategy(current_position=current_position, index_code=index_code)
