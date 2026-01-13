# -*- coding: utf-8 -*-
"""
牛市高回报策略 V5.0 - 完整版
==============================

整合所有V5模块:
1. 市场特征分类器 (MarketCharacterClassifier)
2. 题材识别器 (ThemeSectorIdentifier)
3. 动态风控管理器 (DynamicRiskManager)
4. 投资标的构建器 (InvestmentTargetBuilder)
5. V5回测引擎 (VBTBacktestV5)

核心特性:
- 市场趋势自动识别和策略切换
- 知识库驱动的题材因子
- 涨停板特殊处理
- 2019年等特殊时段适配

作者: TRQuant Team
版本: V5.0
日期: 2026-01-12
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import pandas as pd
import numpy as np

# V5模块导入
from .market_character_classifier import (
    MarketCharacterClassifier,
    MarketCharacter,
    MarketType,
    StrategyMode,
)
from .theme_sector_identifier import (
    ThemeSectorIdentifier,
    StockThemeProfile,
)
from .dynamic_risk_manager import (
    DynamicRiskManager,
    DynamicRiskParams,
    RiskDecision,
    RiskAction,
)
from .investment_target_builder import (
    InvestmentTargetBuilder,
    FilterConfig,
    BuilderResult,
    TargetStock,
)

logger = logging.getLogger(__name__)


# ============ V5参数类 ============

@dataclass
class SignalParamsV5:
    """
    V5策略参数
    
    整合所有已优化参数，并增加V5新特性参数
    """
    # ========== 因子筛选参数 ==========
    min_mom_20d: float = -1.25      # 20日动量下限(%)
    max_mom_20d: float = 25.0       # 20日动量上限(%)
    max_rel_position: float = 80.0  # 相对位置上限(%)
    min_vol_ratio: float = 1.0      # 量比下限
    
    # ========== 涨停因子参数（追涨策略核心） ==========
    limit_up_threshold: float = 0.093      # 涨停阈值(9.3%)
    vol_ratio_threshold_first: float = 2.5 # 首板量比阈值
    
    # ========== 突破因子参数 ==========
    mom_5d_threshold_breakout: float = 16.0   # 5日动量阈值(%)
    vol_ratio_threshold_breakout: float = 1.5 # 突破量比阈值
    breakout_ratio_min: float = 5.0           # 突破幅度下限(%)
    
    # ========== 资金流向参数 ==========
    min_flow_strength: float = 0.0  # 资金流向强度下限
    
    # ========== 信号参数 ==========
    min_signal_score: float = 52.0  # 最低信号评分
    
    # ========== 仓位管理参数 ==========
    max_positions: int = 5          # 最大持仓数
    single_position_max: float = 0.4  # 单只最大仓位
    rebalance_period: int = 5       # 调仓周期(天)
    
    # ========== 止损止盈参数（动态调整） ==========
    stop_loss_pct: float = -0.10    # 硬止损
    take_profit_pct: float = 0.40   # 全止盈
    trailing_stop_pct: float = -0.09  # 移动止损
    trailing_stop_trigger: float = 0.15  # 移动止损触发
    time_stop_days: int = 20        # 时间止损
    
    # 分批止盈
    partial_profit_1_pct: float = 0.20    # 第一批止盈
    partial_profit_1_ratio: float = 0.50  # 第一批比例
    
    # 软止损
    soft_stop_loss_pct: float = -0.08  # 软止损
    soft_stop_loss_days: int = 3       # 软止损天数
    
    # ========== 市场趋势参数 ==========
    market_trend_score_bullish: float = 30.0   # 牛市阈值
    market_trend_score_bearish: float = -30.0  # 熊市阈值
    
    # ========== V5新参数 ==========
    enable_theme_factor: bool = True      # 启用题材因子
    theme_weight: float = 0.3             # 题材因子权重
    enable_limit_up_hold: bool = True     # 涨停不卖
    first_limit_hold_days: int = 1        # 首板观察期
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {k: v for k, v in self.__dict__.items()}


# ============ V5策略引擎 ============

class BullMarketStrategyV5:
    """
    牛市高回报策略 V5.0 引擎
    
    核心特性:
    1. 整合市场特征分类器，自动识别市场类型
    2. 根据市场类型自动切换策略模式和参数
    3. 知识库驱动的题材因子
    4. 完整的止损止盈和涨停板处理
    5. 两阶段投资标的筛选
    """
    
    def __init__(
        self,
        params: Optional[SignalParamsV5] = None,
        enable_auto_switch: bool = True,
    ):
        """
        初始化V5策略
        
        Args:
            params: 策略参数
            enable_auto_switch: 是否启用自动策略切换
        """
        self.params = params or SignalParamsV5()
        self.enable_auto_switch = enable_auto_switch
        
        # 初始化子模块
        self.market_classifier = MarketCharacterClassifier()
        self.theme_identifier = ThemeSectorIdentifier()
        self.risk_manager = DynamicRiskManager("正常")
        self.target_builder = InvestmentTargetBuilder(
            theme_identifier=self.theme_identifier
        )
        
        # 状态
        self._current_market: Optional[MarketCharacter] = None
        self._current_mode: StrategyMode = StrategyMode.NORMAL
        self._decision_history: List[Dict] = []
        
        logger.info("BullMarketStrategyV5 初始化完成")
    
    def analyze_market(
        self,
        as_of_date: str,
        index_code: str = "000300.XSHG",
        price_df: Optional[pd.DataFrame] = None,
    ) -> MarketCharacter:
        """
        分析市场状态
        
        Args:
            as_of_date: 分析日期
            index_code: 指数代码
            price_df: 价格数据
        
        Returns:
            MarketCharacter: 市场特征
        """
        result = self.market_classifier.classify(
            as_of_date=as_of_date,
            index_code=index_code,
            price_df=price_df,
        )
        
        self._current_market = result
        
        # 自动切换策略模式
        if self.enable_auto_switch:
            self._switch_strategy_mode(result.strategy_mode)
        
        return result
    
    def _switch_strategy_mode(self, new_mode: StrategyMode):
        """切换策略模式"""
        if new_mode == self._current_mode:
            return
        
        old_mode = self._current_mode
        self._current_mode = new_mode
        
        # 更新风控参数
        self.risk_manager.update_mode(new_mode.value)
        
        # 更新策略参数
        suggested_params = self._current_market.suggested_params if self._current_market else {}
        
        for key, value in suggested_params.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
        
        logger.info(f"策略模式切换: {old_mode.value} -> {new_mode.value}")
        
        # 记录决策
        self._decision_history.append({
            "time": datetime.now().isoformat(),
            "action": "mode_switch",
            "from": old_mode.value,
            "to": new_mode.value,
            "params": suggested_params,
        })
    
    def make_decision(
        self,
        as_of_date: str,
        signals: Optional[pd.DataFrame] = None,
        scores: Optional[pd.DataFrame] = None,
    ) -> Dict[str, Any]:
        """
        生成交易决策
        
        Args:
            as_of_date: 决策日期
            signals: 信号数据
            scores: 评分数据
        
        Returns:
            决策结果
        """
        # 分析市场
        if self._current_market is None:
            self.analyze_market(as_of_date)
        
        market = self._current_market
        
        # 检查是否允许交易
        allow_trade = True
        reason = ""
        
        if market.strategy_mode == StrategyMode.STOP:
            allow_trade = False
            reason = "熊市/特殊时段，停止交易"
        elif market.strategy_mode == StrategyMode.DEFENSIVE:
            allow_trade = True
            reason = "防御模式，低仓位交易"
        elif market.is_special_period:
            allow_trade = True
            reason = f"特殊时段: {market.special_note}"
        else:
            reason = f"{market.market_type.value}市场，{market.strategy_mode.value}模式"
        
        return {
            "allow_trade": allow_trade,
            "reason": reason,
            "market_type": market.market_type.value,
            "strategy_mode": market.strategy_mode.value,
            "confidence": market.confidence,
            "position_cap": market.suggested_params.get("position_cap", 1.0),
            "params": self.params.to_dict(),
        }
    
    def get_trading_rules(self) -> str:
        """获取当前交易规则"""
        return self.risk_manager.get_trading_rules_summary()
    
    def get_ai_mainline_summary(self) -> str:
        """获取AI主线摘要"""
        return self.theme_identifier.get_ai_mainline_summary()
    
    def get_status_report(self) -> str:
        """获取策略状态报告"""
        market = self._current_market or MarketCharacter(
            market_type=MarketType.VOLATILE,
            strategy_mode=StrategyMode.NORMAL,
            confidence=0.5,
        )
        
        report = f"""
========================================
牛市高回报策略 V5.0 状态报告
========================================

【市场状态】
类型: {market.market_type.value}
策略模式: {market.strategy_mode.value}
置信度: {market.confidence:.1%}
日均涨停: {market.daily_limit_up_avg:.0f}
趋势得分: {market.trend_score:.1f}

【当前参数】
止损: {self.params.stop_loss_pct:.1%}
止盈: {self.params.take_profit_pct:.1%}
最大持仓: {self.params.max_positions}
单仓上限: {self.params.single_position_max:.1%}
题材因子: {'启用' if self.params.enable_theme_factor else '禁用'}
涨停不卖: {'是' if self.params.enable_limit_up_hold else '否'}

【特殊处理】
是否特殊时段: {'是' if market.is_special_period else '否'}
{'备注: ' + market.special_note if market.special_note else ''}

========================================
"""
        return report


# ============ 测试函数 ============

def test_bull_market_strategy_v5():
    """测试V5策略"""
    print("=" * 60)
    print("BullMarketStrategyV5 单元测试")
    print("=" * 60)
    
    # 测试1: 初始化
    print("\n1. 测试策略初始化...")
    strategy = BullMarketStrategyV5()
    print(f"   当前模式: {strategy._current_mode.value}")
    print(f"   题材因子: {strategy.params.enable_theme_factor}")
    print("   ✓ 通过")
    
    # 测试2: 市场分析
    print("\n2. 测试市场分析...")
    market = strategy.analyze_market("2024-10-01")
    print(f"   市场类型: {market.market_type.value}")
    print(f"   策略模式: {market.strategy_mode.value}")
    print(f"   置信度: {market.confidence:.1%}")
    print("   ✓ 通过")
    
    # 测试3: 2019年特殊时段
    print("\n3. 测试2019年特殊时段...")
    market_2019 = strategy.analyze_market("2019-03-15")
    print(f"   市场类型: {market_2019.market_type.value}")
    print(f"   策略模式: {market_2019.strategy_mode.value}")
    print(f"   特殊时段: {market_2019.is_special_period}")
    assert market_2019.is_special_period, "2019年3月应为特殊时段"
    print("   ✓ 通过")
    
    # 测试4: 交易决策
    print("\n4. 测试交易决策...")
    decision = strategy.make_decision("2024-10-05")
    print(f"   允许交易: {decision['allow_trade']}")
    print(f"   原因: {decision['reason']}")
    print(f"   仓位上限: {decision['position_cap']:.0%}")
    print("   ✓ 通过")
    
    # 测试5: 状态报告
    print("\n5. 测试状态报告...")
    report = strategy.get_status_report()
    print(f"   报告前300字:\n{report[:300]}...")
    assert "V5.0" in report, "报告应包含V5.0"
    print("   ✓ 通过")
    
    # 测试6: 交易规则
    print("\n6. 测试交易规则...")
    rules = strategy.get_trading_rules()
    print(f"   规则前200字:\n{rules[:200]}...")
    assert "止损规则" in rules, "规则应包含止损"
    print("   ✓ 通过")
    
    print("\n" + "=" * 60)
    print("所有测试通过!")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_bull_market_strategy_v5()
