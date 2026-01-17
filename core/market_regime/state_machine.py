#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
市场情绪状态机
==============

每天自动判断市场状态，限制策略生成空间
"""

import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.market_regime.regime_knowledge_base import RegimeKnowledgeBase


class MarketRegime(Enum):
    """市场状态枚举"""
    COLD_START = "冷启动"
    RISING = "主升"
    OVERHEATED = "过热"
    RETREAT = "退潮"
    CRASH = "崩溃"


class MarketRegimeStateMachine:
    """市场情绪状态机"""
    
    def __init__(self):
        self.regime_kb = RegimeKnowledgeBase()
        self.current_regime: Optional[MarketRegime] = None
        self.regime_history: List[Dict[str, Any]] = []
    
    def judge_market_regime(
        self,
        indicators: Dict[str, float]
    ) -> MarketRegime:
        """
        基于多个指标判断市场状态
        
        Args:
            indicators: 市场指标字典
                - limit_up_count: 涨停家数
                - limit_down_count: 跌停家数
                - limit_up_height: 连板高度
                - limit_up_failure_rate: 炸板率
                - capital_net_inflow: 资金净流入（亿）
                - turnover_rate: 市场平均换手率
                - volume_ratio: 成交量比率（相对前5日均量）
        
        Returns:
            市场状态
        """
        limit_up_count = indicators.get('limit_up_count', 0)
        limit_down_count = indicators.get('limit_down_count', 0)
        limit_up_height = indicators.get('limit_up_height', 0)
        limit_up_failure_rate = indicators.get('limit_up_failure_rate', 0)
        capital_net_inflow = indicators.get('capital_net_inflow', 0)
        turnover_rate = indicators.get('turnover_rate', 0)
        volume_ratio = indicators.get('volume_ratio', 1.0)
        
        # 判断逻辑（基于知识库中的判定标准）
        
        # 1. 崩溃期判断（最优先）
        if limit_down_count > 20 or (limit_down_count > 10 and limit_up_count < 5):
            return MarketRegime.CRASH
        
        # 2. 退潮期判断
        if (limit_up_count < 10 and 
            limit_up_failure_rate > 0.3 and 
            limit_up_height < 3):
            return MarketRegime.RETREAT
        
        # 3. 过热期判断
        if (limit_up_count > 80 and 
            limit_up_height > 7 and 
            limit_up_failure_rate < 0.1):
            return MarketRegime.OVERHEATED
        
        # 4. 主升期判断
        if (30 <= limit_up_count <= 60 and
            4 <= limit_up_height <= 6 and
            0.1 <= limit_up_failure_rate <= 0.2 and
            capital_net_inflow > 0):
            return MarketRegime.RISING
        
        # 5. 冷启动判断（默认）
        return MarketRegime.COLD_START
    
    def get_strategy_constraints(self, regime: MarketRegime) -> Dict[str, Any]:
        """
        获取市场状态对应的策略生成约束
        
        Args:
            regime: 市场状态
            
        Returns:
            策略约束字典
        """
        constraints = {
            MarketRegime.COLD_START: {
                "max_position": 0.5,
                "allowed_strategies": ["趋势跟随", "低波动"],
                "forbidden_strategies": ["追涨", "连板"],
                "risk_level": "中等"
            },
            MarketRegime.RISING: {
                "max_position": 0.8,
                "allowed_strategies": ["趋势跟随", "主线轮动", "适度追涨"],
                "forbidden_strategies": [],
                "risk_level": "低"
            },
            MarketRegime.OVERHEATED: {
                "max_position": 0.5,
                "allowed_strategies": ["减仓", "防御"],
                "forbidden_strategies": ["追涨", "连板", "高位接盘"],
                "risk_level": "高"
            },
            MarketRegime.RETREAT: {
                "max_position": 0.3,
                "allowed_strategies": ["空仓", "防御", "低波动"],
                "forbidden_strategies": ["追涨", "连板", "短线"],
                "risk_level": "极高"
            },
            MarketRegime.CRASH: {
                "max_position": 0.1,
                "allowed_strategies": ["空仓", "防御"],
                "forbidden_strategies": ["所有进攻性策略"],
                "risk_level": "极高"
            }
        }
        
        return constraints.get(regime, {
            "max_position": 0.5,
            "allowed_strategies": [],
            "forbidden_strategies": [],
            "risk_level": "未知"
        })
    
    def update_regime(self, indicators: Dict[str, float]) -> Dict[str, Any]:
        """
        更新市场状态
        
        Args:
            indicators: 市场指标
            
        Returns:
            更新结果
        """
        new_regime = self.judge_market_regime(indicators)
        constraints = self.get_strategy_constraints(new_regime)
        
        # 记录历史
        self.regime_history.append({
            "date": datetime.now().strftime('%Y-%m-%d'),
            "regime": new_regime.value,
            "indicators": indicators,
            "constraints": constraints
        })
        
        self.current_regime = new_regime
        
        return {
            "regime": new_regime.value,
            "constraints": constraints,
            "knowledge": self.regime_kb.get_regime_strategy_suggestions(new_regime.value)
        }
    
    def can_generate_strategy(
        self,
        strategy_type: str
    ) -> tuple[bool, str]:
        """
        判断是否可以生成某类策略
        
        Args:
            strategy_type: 策略类型
            
        Returns:
            (是否允许, 原因)
        """
        if self.current_regime is None:
            return False, "市场状态未初始化"
        
        constraints = self.get_strategy_constraints(self.current_regime)
        
        if strategy_type in constraints.get("forbidden_strategies", []):
            return False, f"当前市场状态({self.current_regime.value})禁止生成{strategy_type}策略"
        
        if strategy_type in constraints.get("allowed_strategies", []):
            return True, f"当前市场状态({self.current_regime.value})允许生成{strategy_type}策略"
        
        # 默认允许，但给出警告
        return True, f"当前市场状态({self.current_regime.value})，策略类型{strategy_type}需谨慎"


def get_regime_state_machine() -> MarketRegimeStateMachine:
    """获取市场状态机实例"""
    return MarketRegimeStateMachine()
