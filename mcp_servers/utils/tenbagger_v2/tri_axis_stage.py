"""
三轴阶段状态机 (Tri-Axis Stage Machine)

把 S1/S2/S3 做成可复现的状态机，而不是"总分映射"

三轴:
- 基本面轴 (Fundamental Momentum): 收入/利润/毛利率加速度
- 资金轴 (Price/Volume & Positioning): 趋势结构、换手抬升
- 预期轴 (Expectation & Attention): 公告密度、研报覆盖

阶段定义:
- S1 验证期: 基本面真拐点 + 资金未趋势化 + 低关注
- S2 导入期: 基本面持续验证 + 资金趋势化 + 关注上升未拥挤
- S3 放量期: 资金共识强 + 波动放大 + 估值可能透支

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StageAxis(Enum):
    """三轴"""
    FUNDAMENTAL = "fundamental"   # 基本面轴
    FLOW = "flow"                 # 资金轴
    EXPECTATION = "expectation"   # 预期轴


class Stage(Enum):
    """阶段"""
    S0 = "S0"  # 观察期
    S1 = "S1"  # 验证期
    S2 = "S2"  # 导入期（最佳介入点）
    S3 = "S3"  # 放量期
    S4 = "S4"  # 加速期
    S5 = "S5"  # 成熟期


@dataclass
class AxisScore:
    """轴得分"""
    axis: StageAxis
    score: float  # 0-100
    signals: List[str] = field(default_factory=list)
    raw_values: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StageResult:
    """阶段判定结果"""
    symbol: str
    stage: Stage
    confidence: float  # 0-1
    axis_scores: List[AxisScore] = field(default_factory=list)
    transition_evidence: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "stage": self.stage.value,
            "confidence": self.confidence,
            "axis_scores": [
                {
                    "axis": a.axis.value,
                    "score": a.score,
                    "signals": a.signals
                }
                for a in self.axis_scores
            ],
            "transition_evidence": self.transition_evidence,
            "timestamp": self.timestamp
        }


class TriAxisStageMachine:
    """
    三轴阶段状态机
    
    设计原则:
    - 阶段由三轴组合确定，不是单一总分映射
    - 每个轴有独立的信号和阈值
    - 输出可解释的证据
    """
    
    # 基本面轴阈值
    FUNDAMENTAL_THRESHOLDS = {
        "revenue_growth_acceleration": 5,    # 收入增速加速度 > 5%
        "profit_growth_positive": 0,         # 利润增速 > 0
        "margin_improvement": 0,             # 毛利率改善
        "cash_flow_improvement": True,       # 现金流改善
        "consecutive_quarters": 2            # 连续改善季度数
    }
    
    # 资金轴阈值
    FLOW_THRESHOLDS = {
        "ma_trend": "bullish",               # 均线趋势
        "volume_increase_ratio": 1.5,        # 成交量放大倍数
        "turnover_from_low": 0.5,            # 换手率从低位抬升
        "price_above_ma20": True,            # 价格在20日均线上
        "breakout_signal": True              # 突破信号
    }
    
    # 预期轴阈值
    EXPECTATION_THRESHOLDS = {
        "announcement_density": 3,           # 公告密度（近3个月）
        "research_coverage_change": 0,       # 研报覆盖变化
        "analyst_rating_upgrade": False,     # 分析师评级上调
        "pe_rerating": False,                # 估值锚切换
        "event_frequency": 2                 # 事件频率
    }
    
    # 阶段判定规则（三轴组合）
    STAGE_RULES = {
        Stage.S1: {
            "fundamental": (50, 70),    # 基本面: 50-70分 (真拐点)
            "flow": (0, 50),            # 资金: 0-50分 (未趋势化)
            "expectation": (0, 40)      # 预期: 0-40分 (低关注)
        },
        Stage.S2: {
            "fundamental": (60, 90),    # 基本面: 60-90分 (持续验证)
            "flow": (40, 70),           # 资金: 40-70分 (趋势化介入)
            "expectation": (30, 60)     # 预期: 30-60分 (上升未拥挤)
        },
        Stage.S3: {
            "fundamental": (70, 100),   # 基本面: 70-100分 (确认)
            "flow": (60, 100),          # 资金: 60-100分 (共识强)
            "expectation": (50, 100)    # 预期: 50-100分 (关注度高)
        },
        Stage.S4: {
            "fundamental": (80, 100),
            "flow": (70, 100),
            "expectation": (70, 100)
        }
    }
    
    def __init__(self):
        self._history: Dict[str, List[StageResult]] = {}
    
    def _score_fundamental(self, data: Dict[str, Any]) -> AxisScore:
        """
        计算基本面轴得分
        
        指标:
        - 收入/利润/毛利率的"加速度"
        - 经营现金流改善
        """
        score = 0
        signals = []
        raw_values = {}
        
        # 1. 收入增速加速
        revenue_accel = data.get("revenue_growth_qoq_change", 0)
        raw_values["revenue_acceleration"] = revenue_accel
        if revenue_accel > self.FUNDAMENTAL_THRESHOLDS["revenue_growth_acceleration"]:
            score += 25
            signals.append(f"收入增速加速+{revenue_accel:.1f}%")
        elif revenue_accel > 0:
            score += 15
            signals.append(f"收入增速正向+{revenue_accel:.1f}%")
        
        # 2. 利润增速
        profit_growth = data.get("profit_growth", 0)
        raw_values["profit_growth"] = profit_growth
        if profit_growth > 30:
            score += 25
            signals.append(f"利润高增长{profit_growth:.1f}%")
        elif profit_growth > 10:
            score += 15
            signals.append(f"利润增长{profit_growth:.1f}%")
        elif profit_growth > 0:
            score += 10
        
        # 3. 毛利率改善
        margin_change = data.get("gross_margin_change", 0)
        raw_values["margin_change"] = margin_change
        if margin_change > 2:
            score += 20
            signals.append(f"毛利率提升+{margin_change:.1f}%")
        elif margin_change > 0:
            score += 10
        
        # 4. 经营现金流
        cash_flow_improve = data.get("cash_flow_improvement", False)
        raw_values["cash_flow_improvement"] = cash_flow_improve
        if cash_flow_improve:
            score += 15
            signals.append("经营现金流改善")
        
        # 5. 连续改善
        consecutive_q = data.get("consecutive_improvement_quarters", 0)
        raw_values["consecutive_quarters"] = consecutive_q
        if consecutive_q >= 2:
            score += 15
            signals.append(f"连续{consecutive_q}季度改善")
        
        return AxisScore(
            axis=StageAxis.FUNDAMENTAL,
            score=min(100, score),
            signals=signals,
            raw_values=raw_values
        )
    
    def _score_flow(self, data: Dict[str, Any]) -> AxisScore:
        """
        计算资金轴得分
        
        指标:
        - 趋势结构（均线/波动收敛后放量）
        - 换手与成交额从低位抬升
        """
        score = 0
        signals = []
        raw_values = {}
        
        # 1. 均线趋势
        ma_trend = data.get("ma_trend", "neutral")
        raw_values["ma_trend"] = ma_trend
        if ma_trend == "bullish":
            score += 25
            signals.append("均线多头排列")
        elif ma_trend == "turning_up":
            score += 15
            signals.append("均线开始向上")
        
        # 2. 成交量变化
        volume_ratio = data.get("volume_increase_ratio", 1.0)
        raw_values["volume_ratio"] = volume_ratio
        if volume_ratio > 2.0:
            score += 20
            signals.append(f"成交量放大{volume_ratio:.1f}倍")
        elif volume_ratio > 1.5:
            score += 15
            signals.append(f"成交量温和放大")
        
        # 3. 换手率从低位抬升
        turnover_change = data.get("turnover_from_low_pct", 0)
        raw_values["turnover_change"] = turnover_change
        if turnover_change > 100:
            score += 20
            signals.append("换手率从低位显著抬升")
        elif turnover_change > 50:
            score += 10
        
        # 4. 突破信号
        breakout = data.get("breakout_signal", False)
        raw_values["breakout"] = breakout
        if breakout:
            score += 20
            signals.append("价格突破信号")
        
        # 5. 相对强度
        rs = data.get("relative_strength", 50)
        raw_values["relative_strength"] = rs
        if rs > 70:
            score += 15
            signals.append(f"相对强度{rs}")
        elif rs > 50:
            score += 10
        
        return AxisScore(
            axis=StageAxis.FLOW,
            score=min(100, score),
            signals=signals,
            raw_values=raw_values
        )
    
    def _score_expectation(self, data: Dict[str, Any]) -> AxisScore:
        """
        计算预期轴得分
        
        指标:
        - 公告密度、研报覆盖"从无到有"
        - 估值从"传统锚"向"成长锚"切换
        """
        score = 0
        signals = []
        raw_values = {}
        
        # 1. 公告密度
        ann_count = data.get("announcement_count_3m", 0)
        raw_values["announcement_count"] = ann_count
        if ann_count >= 5:
            score += 20
            signals.append(f"近3月{ann_count}条公告")
        elif ann_count >= 3:
            score += 15
        
        # 2. 研报覆盖变化
        research_change = data.get("research_coverage_change", 0)
        raw_values["research_change"] = research_change
        if research_change > 5:
            score += 20
            signals.append(f"研报覆盖增加{research_change}")
        elif research_change > 0:
            score += 10
            signals.append("研报覆盖开始增加")
        
        # 3. 分析师评级
        rating_upgrade = data.get("analyst_rating_upgrade", False)
        raw_values["rating_upgrade"] = rating_upgrade
        if rating_upgrade:
            score += 15
            signals.append("分析师评级上调")
        
        # 4. 产业事件
        event_count = data.get("industry_event_count", 0)
        raw_values["event_count"] = event_count
        if event_count >= 3:
            score += 20
            signals.append(f"产业事件频繁({event_count})")
        elif event_count >= 1:
            score += 10
        
        # 5. 估值切换信号
        pe_rerating = data.get("pe_rerating_signal", False)
        raw_values["pe_rerating"] = pe_rerating
        if pe_rerating:
            score += 25
            signals.append("估值锚向成长切换")
        
        return AxisScore(
            axis=StageAxis.EXPECTATION,
            score=min(100, score),
            signals=signals,
            raw_values=raw_values
        )
    
    def _determine_stage(self, fund_score: float, flow_score: float, expect_score: float) -> Tuple[Stage, float]:
        """
        根据三轴得分确定阶段
        
        Returns:
            (stage, confidence)
        """
        best_stage = Stage.S0
        best_confidence = 0.0
        
        for stage, rules in self.STAGE_RULES.items():
            fund_range = rules["fundamental"]
            flow_range = rules["flow"]
            expect_range = rules["expectation"]
            
            # 计算每个轴的匹配度
            fund_match = 1.0 if fund_range[0] <= fund_score <= fund_range[1] else 0.0
            flow_match = 1.0 if flow_range[0] <= flow_score <= flow_range[1] else 0.0
            expect_match = 1.0 if expect_range[0] <= expect_score <= expect_range[1] else 0.0
            
            # 加权匹配度
            confidence = (fund_match * 0.4 + flow_match * 0.35 + expect_match * 0.25)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_stage = stage
        
        # S0: 没有明显匹配任何阶段
        if best_confidence < 0.5:
            return Stage.S0, best_confidence
        
        return best_stage, best_confidence
    
    def evaluate(self, symbol: str, data: Dict[str, Any]) -> StageResult:
        """
        评估股票阶段
        
        Args:
            symbol: 股票代码
            data: 评估数据
            
        Returns:
            StageResult
        """
        # 计算三轴得分
        fund_axis = self._score_fundamental(data)
        flow_axis = self._score_flow(data)
        expect_axis = self._score_expectation(data)
        
        # 确定阶段
        stage, confidence = self._determine_stage(
            fund_axis.score,
            flow_axis.score,
            expect_axis.score
        )
        
        # 生成转换证据
        evidence = []
        if fund_axis.signals:
            evidence.append(f"基本面: {', '.join(fund_axis.signals[:2])}")
        if flow_axis.signals:
            evidence.append(f"资金: {', '.join(flow_axis.signals[:2])}")
        if expect_axis.signals:
            evidence.append(f"预期: {', '.join(expect_axis.signals[:2])}")
        
        result = StageResult(
            symbol=symbol,
            stage=stage,
            confidence=confidence,
            axis_scores=[fund_axis, flow_axis, expect_axis],
            transition_evidence=evidence
        )
        
        # 保存历史
        if symbol not in self._history:
            self._history[symbol] = []
        self._history[symbol].append(result)
        
        return result
    
    def get_history(self, symbol: str) -> List[StageResult]:
        """获取历史记录"""
        return self._history.get(symbol, [])
    
    def batch_evaluate(self, stocks: List[Dict[str, Any]]) -> List[StageResult]:
        """批量评估"""
        results = []
        for stock in stocks:
            result = self.evaluate(
                symbol=stock.get("symbol", ""),
                data=stock.get("data", {})
            )
            results.append(result)
        return results
    
    def get_stage_distribution(self) -> Dict[str, int]:
        """获取阶段分布"""
        distribution = {s.value: 0 for s in Stage}
        for symbol, history in self._history.items():
            if history:
                latest = history[-1]
                distribution[latest.stage.value] += 1
        return distribution


# 全局实例
_stage_machine: Optional[TriAxisStageMachine] = None


def get_tri_axis_stage_machine() -> TriAxisStageMachine:
    """获取三轴阶段状态机"""
    global _stage_machine
    if _stage_machine is None:
        _stage_machine = TriAxisStageMachine()
    return _stage_machine

