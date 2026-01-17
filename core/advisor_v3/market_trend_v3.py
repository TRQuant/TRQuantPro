"""
V3.0 市场趋势分析模块
=====================

整合现有的 MarketTrendAnalyzer (多周期共振 + HMM)，提供V3专用接口。

核心功能:
1. 多周期趋势分析 (周/月/季 = 5/21/63交易日)
2. HMM隐状态识别 (牛/熊/震荡) - 权重0.2
3. TrendAnalyzer技术指标 - 权重0.8  
4. 共振判断输出仓位上限和策略模式
5. 自适应持仓周期建议

已回测验证: 10年期验证，权重配比 Trend:HMM = 0.8:0.2
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


# ============ V3 专用数据结构 ============

@dataclass
class MarketTrendResultV3:
    """
    V3.0 市场趋势分析结果
    
    统一输出格式，包含所有下游模块需要的信息
    """
    # 基础信息
    date: str
    index_code: str
    
    # 综合评分 (-100 ~ +100)
    ensemble_score: float
    
    # 趋势方向
    direction: str  # "强势上涨" / "上涨趋势" / "弱势上涨" / "震荡盘整" / "弱势下跌" / "下跌趋势" / "强势下跌"
    
    # HMM状态
    hmm_state: str  # "牛市" / "震荡" / "熊市"
    hmm_confidence: float  # 0~1
    
    # 共振阶段
    resonance_phase: str  # "全周期共振-牛" / "部分共振-牛" / "周期分歧" / "部分共振-熊" / "全周期共振-熊"
    
    # 仓位建议
    position_cap: float  # 0~1 仓位上限
    strategy_mode: str  # "trend_only" / "defensive" / "mean_reversion" / "mixed"
    
    # 各周期得分
    period_scores: Dict[str, float] = field(default_factory=dict)  # {"week": 30, "month": 25, "quarter": 20}
    
    # 允许的操作
    allowed_actions: Dict[str, bool] = field(default_factory=lambda: {
        "allow_buy": True,
        "allow_add": False,
        "allow_reduce": True,
        "allow_sell": False,
        "allow_new_positions": True,
    })
    
    # 建议调仓频率
    rebalance_frequency: str = "weekly"  # "immediate" / "weekly" / "monthly"
    
    # 持仓周期建议
    holding_period_days: Tuple[int, int] = (5, 20)  # (min_days, max_days)
    
    # 偏好/回避板块
    sector_preferences: List[str] = field(default_factory=list)
    avoid_sectors: List[str] = field(default_factory=list)
    
    # ===== 新增：14种市场阶段 =====
    market_phase: str = ""  # 如 "牛市确认(全周期共振)" / "熊市筑底" / "震荡整理" 等14种
    market_phase_position: float = 0.5  # 来自PHASE_DESCRIPTIONS的建议仓位
    
    # 元数据
    algorithm_version: str = "3.1"
    data_source: str = "jqdata"
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "index_code": self.index_code,
            "ensemble_score": self.ensemble_score,
            "direction": self.direction,
            "hmm_state": self.hmm_state,
            "hmm_confidence": self.hmm_confidence,
            "resonance_phase": self.resonance_phase,
            "position_cap": self.position_cap,
            "position_limit": self.position_cap,  # 兼容workflow_v3
            "strategy_mode": self.strategy_mode,
            "period_scores": self.period_scores,
            "allowed_actions": self.allowed_actions,
            "rebalance_frequency": self.rebalance_frequency,
            "holding_period_days": self.holding_period_days,
            "sector_preferences": self.sector_preferences,
            "avoid_sectors": self.avoid_sectors,
            # 新增14种市场阶段
            "market_phase": self.market_phase,
            "market_phase_position": self.market_phase_position,
            "algorithm_version": self.algorithm_version,
            "data_source": self.data_source,
        }
    
    @property
    def is_bullish(self) -> bool:
        """是否看多"""
        return self.ensemble_score > 20
    
    @property
    def is_bearish(self) -> bool:
        """是否看空"""
        return self.ensemble_score < -20
    
    @property
    def is_sideways(self) -> bool:
        """是否震荡"""
        return -20 <= self.ensemble_score <= 20
    
    @property
    def signal_strength(self) -> str:
        """信号强度"""
        score = abs(self.ensemble_score)
        if score >= 60:
            return "极强"
        elif score >= 40:
            return "强"
        elif score >= 20:
            return "中等"
        else:
            return "弱"


class MarketTrendAnalyzerV3:
    """
    V3.0 市场趋势分析器
    
    封装现有 MarketTrendAnalyzer，提供V3专用接口
    
    核心特性:
    1. 多周期共振分析 (80% 权重)
    2. HMM隐状态识别 (20% 权重)
    3. 仓位上限映射
    4. 策略模式推荐
    5. 持仓周期建议
    """
    
    def __init__(self, use_composite: bool = True):
        """
        初始化分析器
        
        Args:
            use_composite: 是否使用多指数共振分析 (默认True)
        """
        self.use_composite = use_composite
        self._analyzer = None
        self._last_result: Optional[MarketTrendResultV3] = None
        
    def _ensure_analyzer(self):
        """确保底层分析器已初始化"""
        if self._analyzer is None:
            try:
                from core.market_trend_analyzer import (
                    MarketTrendAnalyzer,
                    MarketTrendAnalyzerConfig,
                )
                
                # 使用 smooth_grouped 评分风格（更稳定）
                config = MarketTrendAnalyzerConfig(
                    scoring_style="smooth_grouped",
                    active_periods=["week", "month", "quarter"],
                )
                
                self._analyzer = MarketTrendAnalyzer(config)
                logger.info("MarketTrendAnalyzerV3: 底层分析器初始化成功")
                
            except Exception as e:
                logger.error(f"MarketTrendAnalyzerV3: 初始化失败 - {e}")
                raise
    
    def analyze(
        self,
        as_of_date: str = None,
        index_code: str = "000300.XSHG",
        price_df: pd.DataFrame = None,
    ) -> Optional[MarketTrendResultV3]:
        """
        执行市场趋势分析
        
        Args:
            as_of_date: 分析日期 (默认今天)
            index_code: 指数代码 (默认沪深300)
            price_df: 可选的价格数据
            
        Returns:
            MarketTrendResultV3 或 None
        """
        self._ensure_analyzer()
        
        if as_of_date is None:
            as_of_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            if self.use_composite:
                # 使用多指数共振分析
                signal = self._analyzer.analyze_composite(as_of_date)
            else:
                # 使用单指数分析
                signal = self._analyzer.analyze(index_code, as_of_date, df=price_df)
            
            if signal is None:
                logger.warning(f"MarketTrendAnalyzerV3: 分析失败 @ {as_of_date}")
                return None
            
            # 转换为V3格式
            result = self._convert_to_v3(signal)
            self._last_result = result
            
            return result
            
        except Exception as e:
            logger.error(f"MarketTrendAnalyzerV3: 分析异常 - {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _convert_to_v3(self, signal) -> MarketTrendResultV3:
        """将内部信号转换为V3格式"""
        
        # 提取各周期得分
        period_scores = {}
        for period, ps in signal.period_signals.items():
            period_scores[period] = ps.score
        
        # HMM状态
        hmm_state = "震荡"
        hmm_confidence = 0.5
        if signal.hmm_signal:
            hmm_state = signal.hmm_signal.state.value
            hmm_confidence = signal.hmm_signal.confidence
        
        # 共振阶段
        resonance_phase = "周期分歧"
        if hasattr(signal, 'resonance_phase') and signal.resonance_phase:
            resonance_phase = signal.resonance_phase.value
        
        # 仓位上限
        position_cap = getattr(signal, 'position_cap', 0.5)
        
        # 策略模式
        strategy_mode = "mixed"
        if hasattr(signal, 'strategy_mode') and signal.strategy_mode:
            strategy_mode = signal.strategy_mode.value
        
        # 持仓周期建议
        holding_period = self._suggest_holding_period(signal.ensemble_score, hmm_state)
        
        # 板块偏好
        sector_prefs = signal.investment_universe_filters.sector_preferences
        avoid_sectors = signal.investment_universe_filters.avoid_sectors
        
        # ===== 新增：提取14种市场阶段 =====
        market_phase = ""
        market_phase_position = 0.5
        if hasattr(signal, 'market_phase') and signal.market_phase:
            market_phase = signal.market_phase.value
            market_phase_position = getattr(signal, 'market_phase_position', 0.5)
        
        return MarketTrendResultV3(
            date=signal.date,
            index_code=signal.index_code,
            ensemble_score=signal.ensemble_score,
            direction=signal.ensemble_direction.value,
            hmm_state=hmm_state,
            hmm_confidence=hmm_confidence,
            resonance_phase=resonance_phase,
            position_cap=position_cap,
            strategy_mode=strategy_mode,
            period_scores=period_scores,
            allowed_actions=signal.workflow_params.allowed_actions,
            rebalance_frequency=signal.workflow_params.rebalance_frequency,
            holding_period_days=holding_period,
            sector_preferences=sector_prefs,
            avoid_sectors=avoid_sectors,
            market_phase=market_phase,
            market_phase_position=market_phase_position,
            data_source=signal.data_source,
        )
    
    def _suggest_holding_period(self, score: float, hmm_state: str) -> Tuple[int, int]:
        """
        建议持仓周期
        
        规则：
        - 强趋势 + 牛市确认：可中长期持有 (10-40天)
        - 中等趋势：中期持有 (5-20天)
        - 弱趋势/震荡：短期操作 (1-10天)
        - 熊市：极短期或空仓 (1-5天)
        """
        if score >= 40 and hmm_state == "牛市":
            return (10, 40)  # 中长期
        elif score >= 20:
            return (5, 20)   # 中期
        elif score >= 0:
            return (3, 15)   # 中短期
        elif score >= -20:
            return (1, 10)   # 短期
        else:
            return (1, 5)    # 极短期
    
    def get_position_advice(self, current_position: float = 0.0) -> Dict[str, Any]:
        """
        获取仓位调整建议
        
        Args:
            current_position: 当前仓位 (0~1)
            
        Returns:
            包含调仓建议的字典
        """
        if self._last_result is None:
            return {"action": "hold", "reason": "无分析结果"}
        
        result = self._last_result
        target = result.position_cap
        diff = target - current_position
        
        advice = {
            "current_position": current_position,
            "target_position": target,
            "position_cap": result.position_cap,
            "diff": diff,
            "action": "hold",
            "reason": "",
            "urgency": "low",
        }
        
        if diff > 0.2 and result.allowed_actions.get("allow_add", False):
            advice["action"] = "add"
            advice["reason"] = f"仓位低于目标 {diff*100:.0f}%，建议加仓"
            advice["urgency"] = "medium" if diff > 0.4 else "low"
        elif diff < -0.2 and result.allowed_actions.get("allow_reduce", False):
            advice["action"] = "reduce"
            advice["reason"] = f"仓位高于目标 {-diff*100:.0f}%，建议减仓"
            advice["urgency"] = "high" if diff < -0.4 else "medium"
        elif abs(diff) <= 0.1:
            advice["action"] = "hold"
            advice["reason"] = "仓位合理，继续持有"
        else:
            advice["action"] = "adjust"
            advice["reason"] = f"建议调整仓位至 {target*100:.0f}%"
        
        return advice
    
    def get_summary(self) -> str:
        """获取分析摘要文本"""
        if self._last_result is None:
            return "暂无分析结果"
        
        r = self._last_result
        
        summary = f"""
📊 市场趋势分析摘要 ({r.date})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 综合评分: {r.ensemble_score:.1f} ({r.direction})
🎯 信号强度: {r.signal_strength}
🔮 HMM状态: {r.hmm_state} (置信度: {r.hmm_confidence:.1%})
⚡ 共振阶段: {r.resonance_phase}

💰 仓位建议:
   • 仓位上限: {r.position_cap:.0%}
   • 策略模式: {r.strategy_mode}
   • 持仓周期: {r.holding_period_days[0]}-{r.holding_period_days[1]}天
   • 调仓频率: {r.rebalance_frequency}

📊 各周期得分:
   • 周线(5日): {r.period_scores.get('week', 0):.1f}
   • 月线(21日): {r.period_scores.get('month', 0):.1f}
   • 季线(63日): {r.period_scores.get('quarter', 0):.1f}

🎯 操作建议:
   • 允许买入: {'✅' if r.allowed_actions.get('allow_buy') else '❌'}
   • 允许加仓: {'✅' if r.allowed_actions.get('allow_add') else '❌'}
   • 允许减仓: {'✅' if r.allowed_actions.get('allow_reduce') else '❌'}
   • 允许卖出: {'✅' if r.allowed_actions.get('allow_sell') else '❌'}

📌 板块偏好: {', '.join(r.sector_preferences) if r.sector_preferences else '无'}
⚠️ 回避板块: {', '.join(r.avoid_sectors) if r.avoid_sectors else '无'}
"""
        return summary.strip()


# ============ 便捷函数 ============

def analyze_market_trend(
    as_of_date: str = None,
    use_composite: bool = True,
) -> Optional[MarketTrendResultV3]:
    """
    便捷函数：执行市场趋势分析
    
    Args:
        as_of_date: 分析日期 (默认今天)
        use_composite: 是否使用多指数共振 (默认True)
        
    Returns:
        MarketTrendResultV3 或 None
    """
    analyzer = MarketTrendAnalyzerV3(use_composite=use_composite)
    return analyzer.analyze(as_of_date=as_of_date)


def get_market_position_cap(as_of_date: str = None) -> float:
    """
    便捷函数：获取当前市场仓位上限
    
    Args:
        as_of_date: 分析日期
        
    Returns:
        仓位上限 (0~1)
    """
    result = analyze_market_trend(as_of_date)
    if result:
        return result.position_cap
    return 0.5  # 默认50%


def is_market_bullish(as_of_date: str = None) -> bool:
    """
    便捷函数：判断市场是否看多
    """
    result = analyze_market_trend(as_of_date)
    return result.is_bullish if result else False
