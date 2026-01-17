# -*- coding: utf-8 -*-
"""
牛市高回报策略 V4.0 策略引擎
=============================

核心特点：
1. 市场趋势开关：整合MarketTrendAnalyzerV3，根据市场状态调整策略
2. 涨停因子优先：首板启动 > 连板加速 > 强势突破 > 量价齐升
3. 分级止损止盈：硬止损(-10%) / 软止损(-8%) / 移动止损(-9%)
4. 全A股支持：分批获取和计算

开发记录：
- 2026-01-12: 创建V4策略引擎，整合市场趋势分析模块
"""

from __future__ import annotations

import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

# 导入V4参数
from core.strategy.bull_market_params_v4 import (
    SignalParamsV4,
    StrategyMode,
    DEFAULT_PARAMS_V4,
    load_best_params_v4,
)

logger = logging.getLogger(__name__)


@dataclass
class MarketContext:
    """市场上下文信息"""
    date: str
    ensemble_score: float
    direction: str  # "强势上涨" / "上涨趋势" / "震荡盘整" / "下跌趋势" / "强势下跌"
    hmm_state: str  # "牛市" / "震荡" / "熊市"
    resonance_phase: str  # "全周期共振-牛" / "部分共振" / "周期分歧"
    position_cap: float
    strategy_mode: StrategyMode
    is_bull_market: bool
    period_scores: Dict[str, float]  # {"week": 30, "month": 25, "quarter": 20}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "ensemble_score": self.ensemble_score,
            "direction": self.direction,
            "hmm_state": self.hmm_state,
            "resonance_phase": self.resonance_phase,
            "position_cap": self.position_cap,
            "strategy_mode": self.strategy_mode.value,
            "is_bull_market": self.is_bull_market,
            "period_scores": self.period_scores,
        }


@dataclass
class SignalResult:
    """信号生成结果"""
    entries: pd.DataFrame      # 买入信号矩阵 (T x N)
    scores: pd.DataFrame       # 评分矩阵 (T x N)
    target_weights: pd.DataFrame  # 目标权重矩阵 (T x N)
    signal_count: int
    top_stocks: List[str]      # 当日Top股票列表


class BullMarketStrategyV4:
    """
    牛市高回报策略 V4.0
    
    核心架构：
    1. MarketTrendSwitch - 市场趋势开关（根据趋势调整策略）
    2. FactorCalculator - 因子计算（涨停、突破、量价）
    3. SignalEngine - 信号生成（4种信号类型）
    4. RiskManager - 风控（分级止损止盈）
    5. VBTBacktest - 回测（向量化回测）
    """
    
    def __init__(self, params: SignalParamsV4 = None):
        """
        初始化策略引擎
        
        Args:
            params: 策略参数，默认使用最优参数
        """
        self.params = params or load_best_params_v4()
        self._market_analyzer = None
        self._last_market_context: Optional[MarketContext] = None
        
        # 统计
        self._signal_stats = {
            "first_limit_up": 0,
            "consecutive_limit": 0,
            "strong_breakout": 0,
            "volume_price_rise": 0,
        }
        
    # =========================================================================
    # 市场趋势开关
    # =========================================================================
    
    def _ensure_market_analyzer(self):
        """确保市场分析器已初始化"""
        if self._market_analyzer is None:
            try:
                from core.advisor_v3.market_trend_v3 import MarketTrendAnalyzerV3
                self._market_analyzer = MarketTrendAnalyzerV3(use_composite=True)
                logger.info("BullMarketStrategyV4: 市场趋势分析器初始化成功")
            except Exception as e:
                logger.warning(f"市场趋势分析器初始化失败: {e}")
                self._market_analyzer = None
    
    def analyze_market(self, as_of_date: str) -> Optional[MarketContext]:
        """
        分析市场状态（策略开关核心）
        
        Args:
            as_of_date: 分析日期
            
        Returns:
            MarketContext: 市场上下文
        """
        if not self.params.market_trend_enabled:
            # 未启用市场趋势开关，默认牛市模式
            return MarketContext(
                date=as_of_date,
                ensemble_score=50.0,
                direction="上涨趋势",
                hmm_state="牛市",
                resonance_phase="部分共振",
                position_cap=1.0,
                strategy_mode=StrategyMode.BULL_NORMAL,
                is_bull_market=True,
                period_scores={"week": 30, "month": 25, "quarter": 20},
            )
        
        self._ensure_market_analyzer()
        if self._market_analyzer is None:
            logger.warning("市场分析器不可用，使用默认市场状态")
            return self._default_market_context(as_of_date)
        
        try:
            result = self._market_analyzer.analyze(as_of_date=as_of_date)
            if result is None:
                return self._default_market_context(as_of_date)
            
            # 获取策略模式
            strategy_mode = self.params.get_strategy_mode(result.ensemble_score)
            position_cap = self.params.get_position_cap(result.ensemble_score)
            
            # 判断是否牛市
            is_bull = result.ensemble_score >= self.params.bull_threshold
            
            context = MarketContext(
                date=as_of_date,
                ensemble_score=result.ensemble_score,
                direction=result.direction,
                hmm_state=result.hmm_state,
                resonance_phase=result.resonance_phase,
                position_cap=position_cap,
                strategy_mode=strategy_mode,
                is_bull_market=is_bull,
                period_scores=result.period_scores,
            )
            
            self._last_market_context = context
            return context
            
        except Exception as e:
            logger.error(f"市场分析失败: {e}")
            return self._default_market_context(as_of_date)
    
    def _default_market_context(self, date: str) -> MarketContext:
        """默认市场上下文（用于分析失败时）"""
        return MarketContext(
            date=date,
            ensemble_score=0.0,
            direction="震荡盘整",
            hmm_state="震荡",
            resonance_phase="周期分歧",
            position_cap=0.6,
            strategy_mode=StrategyMode.MIXED,
            is_bull_market=False,
            period_scores={},
        )
    
    # =========================================================================
    # 策略决策
    # =========================================================================
    
    def should_trade(self, market_context: MarketContext) -> Tuple[bool, str]:
        """
        根据市场状态决定是否交易
        
        Args:
            market_context: 市场上下文
            
        Returns:
            (should_trade, reason)
        """
        mode = market_context.strategy_mode
        
        if mode == StrategyMode.STOP:
            return False, f"市场趋势得分{market_context.ensemble_score:.1f}，停止交易"
        
        if mode == StrategyMode.DEFENSIVE:
            return True, f"防御模式，仓位上限{market_context.position_cap:.0%}"
        
        if mode == StrategyMode.MIXED:
            return True, f"混合模式，仓位上限{market_context.position_cap:.0%}"
        
        if mode == StrategyMode.BULL_NORMAL:
            return True, f"牛市正常模式，仓位上限{market_context.position_cap:.0%}"
        
        if mode == StrategyMode.BULL_AGGRESSIVE:
            return True, f"牛市激进模式，全仓操作"
        
        return True, "默认允许交易"
    
    def adjust_params_by_market(
        self, 
        market_context: MarketContext
    ) -> SignalParamsV4:
        """
        根据市场状态调整参数
        
        Args:
            market_context: 市场上下文
            
        Returns:
            调整后的参数
        """
        params = SignalParamsV4(**self.params.to_dict())  # 复制参数
        mode = market_context.strategy_mode
        
        if mode == StrategyMode.BULL_AGGRESSIVE:
            # 牛市激进：放宽条件，增加持仓
            params.max_positions = min(8, params.max_positions + 2)
            params.min_signal_score = max(45.0, params.min_signal_score - 5)
            params.stop_loss_pct = -0.12  # 放宽止损
            
        elif mode == StrategyMode.DEFENSIVE:
            # 防御模式：收紧条件，减少持仓
            params.max_positions = max(2, params.max_positions - 2)
            params.min_signal_score = min(65.0, params.min_signal_score + 5)
            params.stop_loss_pct = -0.08  # 收紧止损
            
        elif mode == StrategyMode.MIXED:
            # 混合模式：中等调整
            params.max_positions = max(3, params.max_positions - 1)
        
        # 应用仓位上限
        params.position_cap_bull = market_context.position_cap
        
        return params
    
    # =========================================================================
    # 实盘规则
    # =========================================================================
    
    def get_trading_rules(self, market_context: MarketContext) -> Dict[str, Any]:
        """
        获取实盘交易规则
        
        Args:
            market_context: 市场上下文
            
        Returns:
            交易规则字典
        """
        params = self.adjust_params_by_market(market_context)
        
        rules = {
            # 买入规则
            "buy_rules": {
                "signal_threshold": params.min_signal_score,
                "max_positions": params.max_positions,
                "single_position_max": params.single_position_max,
                "rebalance_period": params.rebalance_period,
                "position_cap": market_context.position_cap,
            },
            
            # 卖出规则 - 止损
            "stop_loss_rules": {
                "hard_stop": {
                    "trigger": params.stop_loss_pct,
                    "action": "全仓卖出",
                    "description": f"亏损超过{abs(params.stop_loss_pct):.0%}，立即止损",
                },
                "soft_stop": {
                    "trigger": params.soft_stop_loss_pct,
                    "holding_days": params.soft_stop_days,
                    "action": f"减仓{params.soft_stop_ratio:.0%}",
                    "description": f"亏损{abs(params.soft_stop_loss_pct):.0%}且持仓>{params.soft_stop_days}天，减仓",
                },
                "trailing_stop": {
                    "trigger_profit": params.trailing_stop_trigger,
                    "drawdown": params.trailing_stop_pct,
                    "action": "全仓卖出",
                    "description": f"盈利超{params.trailing_stop_trigger:.0%}后，从高点回撤{abs(params.trailing_stop_pct):.0%}止损",
                },
            },
            
            # 卖出规则 - 止盈
            "take_profit_rules": {
                "partial_1": {
                    "trigger": params.partial_profit_1_pct,
                    "action": f"减仓{params.partial_profit_1_ratio:.0%}",
                    "description": f"盈利{params.partial_profit_1_pct:.0%}，先卖{params.partial_profit_1_ratio:.0%}",
                },
                "partial_2": {
                    "trigger": params.partial_profit_2_pct,
                    "action": f"减仓{params.partial_profit_2_ratio:.0%}",
                    "description": f"盈利{params.partial_profit_2_pct:.0%}，再卖{params.partial_profit_2_ratio:.0%}",
                },
                "full": {
                    "trigger": params.take_profit_pct,
                    "action": "全仓卖出",
                    "description": f"盈利{params.take_profit_pct:.0%}，全部卖出",
                },
                "time_stop": {
                    "days": params.time_stop_days,
                    "action": "全仓卖出",
                    "description": f"持仓超{params.time_stop_days}天，无论盈亏平仓",
                },
            },
            
            # 信号优先级
            "signal_priority": [
                {"type": "首板启动", "score_range": "80-90", "description": "首次涨停+放量"},
                {"type": "连板加速", "score_range": "70-80", "description": "近5日2次以上涨停"},
                {"type": "强势突破", "score_range": "65-75", "description": "突破60日高点+放量"},
                {"type": "量价齐升", "score_range": "60-70", "description": "5日动量+量比放大"},
            ],
            
            # 市场状态
            "market_context": market_context.to_dict(),
        }
        
        return rules
    
    def print_trading_rules(self, market_context: MarketContext):
        """打印交易规则"""
        rules = self.get_trading_rules(market_context)
        
        print("\n" + "=" * 70)
        print("牛市高回报策略 V4.0 - 实盘交易规则")
        print("=" * 70)
        
        print(f"\n【市场状态】")
        mc = market_context
        print(f"  日期: {mc.date}")
        print(f"  趋势得分: {mc.ensemble_score:.1f}")
        print(f"  市场方向: {mc.direction}")
        print(f"  HMM状态: {mc.hmm_state}")
        print(f"  策略模式: {mc.strategy_mode.value}")
        print(f"  仓位上限: {mc.position_cap:.0%}")
        
        print(f"\n【买入规则】")
        br = rules["buy_rules"]
        print(f"  信号阈值: {br['signal_threshold']:.0f}分")
        print(f"  最大持仓: {br['max_positions']}只")
        print(f"  单只上限: {br['single_position_max']:.0%}")
        print(f"  调仓周期: {br['rebalance_period']}天")
        
        print(f"\n【止损规则】")
        for name, rule in rules["stop_loss_rules"].items():
            print(f"  {name}: {rule['description']}")
        
        print(f"\n【止盈规则】")
        for name, rule in rules["take_profit_rules"].items():
            print(f"  {name}: {rule['description']}")
        
        print(f"\n【信号优先级】")
        for i, sig in enumerate(rules["signal_priority"], 1):
            print(f"  {i}. {sig['type']} ({sig['score_range']}分): {sig['description']}")
        
        print("\n" + "=" * 70)


# ============================================================================
# 测试函数
# ============================================================================

def test_strategy_v4():
    """测试V4策略引擎"""
    print("=" * 60)
    print("测试 BullMarketStrategyV4")
    print("=" * 60)
    
    # 创建策略
    strategy = BullMarketStrategyV4()
    
    # 测试市场分析
    print("\n1. 测试市场分析:")
    test_date = "2024-10-08"  # 牛市启动日
    context = strategy.analyze_market(test_date)
    if context:
        print(f"   日期: {context.date}")
        print(f"   趋势得分: {context.ensemble_score:.1f}")
        print(f"   策略模式: {context.strategy_mode.value}")
        print(f"   仓位上限: {context.position_cap:.0%}")
    else:
        print("   市场分析失败，使用默认上下文")
        context = strategy._default_market_context(test_date)
    
    # 测试交易决策
    print("\n2. 测试交易决策:")
    should_trade, reason = strategy.should_trade(context)
    print(f"   是否交易: {should_trade}")
    print(f"   原因: {reason}")
    
    # 测试参数调整
    print("\n3. 测试参数调整:")
    adjusted = strategy.adjust_params_by_market(context)
    print(f"   原始持仓数: {strategy.params.max_positions}")
    print(f"   调整后持仓数: {adjusted.max_positions}")
    print(f"   原始止损: {strategy.params.stop_loss_pct:.0%}")
    print(f"   调整后止损: {adjusted.stop_loss_pct:.0%}")
    
    # 打印交易规则
    print("\n4. 打印实盘规则:")
    strategy.print_trading_rules(context)
    
    print("\n" + "=" * 60)
    print("测试完成")


if __name__ == "__main__":
    test_strategy_v4()
