"""
M4: Tenbagger评估体系

整合Stage/ScoreCard/AltData的综合评估系统
用于识别和跟踪潜在十倍股

Author: TRQuant Team
Date: 2025-12-18
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EvalLevel(Enum):
    """评估等级"""
    S_PLUS = "S+"       # 极高潜力
    S = "S"             # 高潜力
    A = "A"             # 较高潜力
    B = "B"             # 中等潜力
    C = "C"             # 一般
    D = "D"             # 较低


class SignalStrength(Enum):
    """信号强度"""
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    NONE = "none"


@dataclass
class EvalDimension:
    """评估维度"""
    name: str                   # 维度名称
    score: float                # 得分 (0-100)
    weight: float               # 权重
    signals: List[str] = field(default_factory=list)  # 信号说明
    
    @property
    def weighted_score(self) -> float:
        return self.score * self.weight


@dataclass
class TenbaggerReport:
    """十倍股评估报告"""
    symbol: str                 # 股票代码
    name: str                   # 股票名称
    eval_level: EvalLevel       # 评估等级
    total_score: float          # 总分
    stage: str                  # 当前阶段
    dimensions: List[EvalDimension] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)   # 优势
    weaknesses: List[str] = field(default_factory=list)  # 劣势
    catalysts: List[str] = field(default_factory=list)   # 催化剂
    risks: List[str] = field(default_factory=list)       # 风险
    recommendation: str = ""    # 投资建议
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "name": self.name,
            "eval_level": self.eval_level.value,
            "total_score": self.total_score,
            "stage": self.stage,
            "dimensions": [
                {"name": d.name, "score": d.score, "weight": d.weight, 
                 "weighted": d.weighted_score, "signals": d.signals}
                for d in self.dimensions
            ],
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "catalysts": self.catalysts,
            "risks": self.risks,
            "recommendation": self.recommendation,
            "generated_at": self.generated_at.isoformat()
        }


class TenbaggerEvaluator:
    """十倍股评估引擎"""
    
    # 评估维度权重配置
    DIMENSION_WEIGHTS = {
        "stage": 0.20,          # 阶段评估
        "scorecard": 0.25,      # 7维评分卡
        "growth": 0.15,         # 成长性
        "industry": 0.15,       # 行业地位
        "altdata": 0.10,        # 另类数据信号
        "momentum": 0.10,       # 市场动量
        "risk": 0.05            # 风险调整
    }
    
    # 等级划分阈值
    LEVEL_THRESHOLDS = {
        "S+": 85,
        "S": 75,
        "A": 65,
        "B": 50,
        "C": 35,
        "D": 0
    }
    
    def __init__(self):
        self._reports: Dict[str, TenbaggerReport] = {}
        self._history: Dict[str, List[TenbaggerReport]] = {}
    
    def evaluate(self, symbol: str, name: str, data: Dict[str, Any]) -> TenbaggerReport:
        """
        综合评估股票
        
        Args:
            symbol: 股票代码
            name: 股票名称
            data: 评估数据，包含:
                - stage: 当前阶段 (S0-S5)
                - scorecard: 7维评分卡数据
                - financials: 财务数据
                - industry: 行业数据
                - altdata: 另类数据信号
                - technicals: 技术指标
        """
        dimensions = []
        
        # 1. 阶段评估
        stage_dim = self._eval_stage(data.get("stage", "S0"))
        dimensions.append(stage_dim)
        
        # 2. 评分卡评估
        scorecard_dim = self._eval_scorecard(data.get("scorecard", {}))
        dimensions.append(scorecard_dim)
        
        # 3. 成长性评估
        growth_dim = self._eval_growth(data.get("financials", {}))
        dimensions.append(growth_dim)
        
        # 4. 行业地位评估
        industry_dim = self._eval_industry(data.get("industry", {}))
        dimensions.append(industry_dim)
        
        # 5. 另类数据评估
        altdata_dim = self._eval_altdata(data.get("altdata", {}))
        dimensions.append(altdata_dim)
        
        # 6. 动量评估
        momentum_dim = self._eval_momentum(data.get("technicals", {}))
        dimensions.append(momentum_dim)
        
        # 7. 风险评估
        risk_dim = self._eval_risk(data)
        dimensions.append(risk_dim)
        
        # 计算总分
        total_score = sum(d.weighted_score for d in dimensions)
        
        # 确定等级
        eval_level = self._determine_level(total_score)
        
        # 生成报告
        report = TenbaggerReport(
            symbol=symbol,
            name=name,
            eval_level=eval_level,
            total_score=total_score,
            stage=data.get("stage", "S0"),
            dimensions=dimensions,
            strengths=self._identify_strengths(dimensions),
            weaknesses=self._identify_weaknesses(dimensions),
            catalysts=self._identify_catalysts(data),
            risks=self._identify_risks(data),
            recommendation=self._generate_recommendation(eval_level, total_score, data)
        )
        
        # 保存报告
        self._reports[symbol] = report
        if symbol not in self._history:
            self._history[symbol] = []
        self._history[symbol].append(report)
        
        return report
    
    def _eval_stage(self, stage: str) -> EvalDimension:
        """评估阶段"""
        stage_scores = {"S0": 20, "S1": 40, "S2": 60, "S3": 80, "S4": 90, "S5": 50}
        score = stage_scores.get(stage, 20)
        signals = []
        
        if stage in ["S2", "S3"]:
            signals.append(f"处于成长黄金期({stage})")
        elif stage == "S4":
            signals.append("接近成熟期，注意估值")
        elif stage == "S1":
            signals.append("早期阶段，潜力待验证")
        
        return EvalDimension(
            name="stage",
            score=score,
            weight=self.DIMENSION_WEIGHTS["stage"],
            signals=signals
        )
    
    def _eval_scorecard(self, scorecard: Dict) -> EvalDimension:
        """评估7维评分卡"""
        total = scorecard.get("total_score", 50)
        signals = []
        
        # 识别突出维度
        dims = scorecard.get("dimensions", {})
        for dim, score in dims.items():
            if score >= 80:
                signals.append(f"{dim}维度突出({score})")
        
        return EvalDimension(
            name="scorecard",
            score=min(total, 100),
            weight=self.DIMENSION_WEIGHTS["scorecard"],
            signals=signals
        )
    
    def _eval_growth(self, financials: Dict) -> EvalDimension:
        """评估成长性"""
        revenue_growth = financials.get("revenue_growth", 0)
        profit_growth = financials.get("profit_growth", 0)
        
        # 成长性得分
        score = 50
        signals = []
        
        if revenue_growth > 50:
            score += 25
            signals.append(f"营收高增长{revenue_growth:.0f}%")
        elif revenue_growth > 20:
            score += 15
            signals.append(f"营收稳健增长{revenue_growth:.0f}%")
        
        if profit_growth > 50:
            score += 25
            signals.append(f"利润高增长{profit_growth:.0f}%")
        elif profit_growth > 20:
            score += 15
        
        return EvalDimension(
            name="growth",
            score=min(score, 100),
            weight=self.DIMENSION_WEIGHTS["growth"],
            signals=signals
        )
    
    def _eval_industry(self, industry: Dict) -> EvalDimension:
        """评估行业地位"""
        market_share = industry.get("market_share", 0)
        industry_rank = industry.get("rank", 10)
        industry_growth = industry.get("industry_growth", 0)
        
        score = 50
        signals = []
        
        if industry_rank <= 3:
            score += 30
            signals.append(f"行业龙头(排名{industry_rank})")
        elif industry_rank <= 5:
            score += 20
            signals.append(f"行业领先(排名{industry_rank})")
        
        if industry_growth > 20:
            score += 20
            signals.append(f"高景气行业(增长{industry_growth:.0f}%)")
        
        return EvalDimension(
            name="industry",
            score=min(score, 100),
            weight=self.DIMENSION_WEIGHTS["industry"],
            signals=signals
        )
    
    def _eval_altdata(self, altdata: Dict) -> EvalDimension:
        """评估另类数据"""
        bid_trend = altdata.get("bid_trend", "stable")
        job_trend = altdata.get("job_trend", "stable")
        expansion_signal = altdata.get("expansion_signal", False)
        
        score = 50
        signals = []
        
        if bid_trend == "growing":
            score += 20
            signals.append("招投标活动增长")
        
        if job_trend == "expanding":
            score += 20
            signals.append("招聘扩张")
        
        if expansion_signal:
            score += 10
            signals.append("业务扩张信号")
        
        return EvalDimension(
            name="altdata",
            score=min(score, 100),
            weight=self.DIMENSION_WEIGHTS["altdata"],
            signals=signals
        )
    
    def _eval_momentum(self, technicals: Dict) -> EvalDimension:
        """评估市场动量"""
        ma_trend = technicals.get("ma_trend", "neutral")
        volume_trend = technicals.get("volume_trend", "normal")
        relative_strength = technicals.get("relative_strength", 50)
        
        score = 50
        signals = []
        
        if ma_trend == "bullish":
            score += 20
            signals.append("均线多头排列")
        
        if volume_trend == "increasing":
            score += 15
            signals.append("成交量放大")
        
        if relative_strength > 70:
            score += 15
            signals.append(f"相对强度{relative_strength}")
        
        return EvalDimension(
            name="momentum",
            score=min(score, 100),
            weight=self.DIMENSION_WEIGHTS["momentum"],
            signals=signals
        )
    
    def _eval_risk(self, data: Dict) -> EvalDimension:
        """评估风险(风险越低得分越高)"""
        score = 70  # 基础分
        signals = []
        
        # 检查各种风险因素
        financials = data.get("financials", {})
        
        debt_ratio = financials.get("debt_ratio", 50)
        if debt_ratio > 70:
            score -= 20
            signals.append(f"负债率较高({debt_ratio:.0f}%)")
        
        pe_ratio = financials.get("pe_ratio", 30)
        if pe_ratio > 100:
            score -= 15
            signals.append(f"估值偏高(PE{pe_ratio:.0f})")
        
        return EvalDimension(
            name="risk",
            score=max(score, 0),
            weight=self.DIMENSION_WEIGHTS["risk"],
            signals=signals
        )
    
    def _determine_level(self, score: float) -> EvalLevel:
        """确定评估等级"""
        for level, threshold in self.LEVEL_THRESHOLDS.items():
            if score >= threshold:
                return EvalLevel(level)
        return EvalLevel.D
    
    def _identify_strengths(self, dimensions: List[EvalDimension]) -> List[str]:
        """识别优势"""
        strengths = []
        for d in dimensions:
            if d.score >= 70:
                strengths.append(f"{d.name}: {d.score:.0f}分")
        return strengths
    
    def _identify_weaknesses(self, dimensions: List[EvalDimension]) -> List[str]:
        """识别劣势"""
        weaknesses = []
        for d in dimensions:
            if d.score < 40:
                weaknesses.append(f"{d.name}: {d.score:.0f}分")
        return weaknesses
    
    def _identify_catalysts(self, data: Dict) -> List[str]:
        """识别催化剂"""
        catalysts = []
        
        if data.get("events"):
            for event in data["events"][:3]:
                catalysts.append(event.get("title", ""))
        
        if data.get("industry", {}).get("policy_support"):
            catalysts.append("政策支持")
        
        return catalysts
    
    def _identify_risks(self, data: Dict) -> List[str]:
        """识别风险"""
        risks = []
        
        financials = data.get("financials", {})
        if financials.get("debt_ratio", 0) > 60:
            risks.append("财务杠杆较高")
        
        if financials.get("pe_ratio", 0) > 80:
            risks.append("估值压力")
        
        return risks
    
    def _generate_recommendation(self, level: EvalLevel, score: float, data: Dict) -> str:
        """生成投资建议"""
        stage = data.get("stage", "S0")
        
        if level in [EvalLevel.S_PLUS, EvalLevel.S]:
            return f"强烈推荐关注，当前处于{stage}阶段，综合评分{score:.1f}，具备十倍股潜质"
        elif level == EvalLevel.A:
            return f"值得关注，当前处于{stage}阶段，评分{score:.1f}，建议持续跟踪"
        elif level == EvalLevel.B:
            return f"中等潜力，评分{score:.1f}，建议观察等待更多信号"
        else:
            return f"潜力有限，评分{score:.1f}，暂不建议重点关注"
    
    def get_report(self, symbol: str) -> Optional[TenbaggerReport]:
        """获取评估报告"""
        return self._reports.get(symbol)
    
    def get_history(self, symbol: str) -> List[TenbaggerReport]:
        """获取历史评估"""
        return self._history.get(symbol, [])
    
    def rank_all(self) -> List[Tuple[str, float, EvalLevel]]:
        """排名所有已评估股票"""
        rankings = [
            (symbol, report.total_score, report.eval_level)
            for symbol, report in self._reports.items()
        ]
        return sorted(rankings, key=lambda x: x[1], reverse=True)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        level_counts = {}
        for report in self._reports.values():
            level = report.eval_level.value
            level_counts[level] = level_counts.get(level, 0) + 1
        
        return {
            "total_evaluated": len(self._reports),
            "by_level": level_counts,
            "avg_score": sum(r.total_score for r in self._reports.values()) / max(len(self._reports), 1)
        }


# 全局实例
_evaluator: Optional[TenbaggerEvaluator] = None


def get_evaluator() -> TenbaggerEvaluator:
    global _evaluator
    if _evaluator is None:
        _evaluator = TenbaggerEvaluator()
    return _evaluator
