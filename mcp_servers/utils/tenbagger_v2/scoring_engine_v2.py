"""
评分引擎 V2 (Scoring Engine V2)

可分布、可解释、可校准的评分引擎

核心改进:
1. 分布自检（防止方差≈0的无效因子）
2. 缺失惩罚（缺失数据≠高分）
3. 行业中性（不只在候选池内分位）
4. 置信度输出

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class ScoreDistribution:
    """得分分布"""
    min_val: float
    max_val: float
    mean: float
    std: float
    median: float
    q25: float
    q75: float
    
    @property
    def is_valid(self) -> bool:
        """分布是否有效（方差不为0）"""
        return self.std > 0.01
    
    def percentile(self, value: float) -> float:
        """计算分位数（近似）"""
        if self.std == 0:
            return 50.0
        z = (value - self.mean) / self.std
        # 简化的正态分布CDF近似
        percentile = 50 * (1 + math.erf(z / math.sqrt(2)))
        return max(0, min(100, percentile))


@dataclass
class FactorScore:
    """因子得分"""
    factor_id: str
    name: str
    raw_value: Any
    normalized_score: float  # 0-100
    weight: float
    weighted_score: float
    is_missing: bool = False
    is_placeholder: bool = False
    percentile: float = 50.0
    explanation: str = ""


@dataclass
class ScoreCardV2:
    """评分卡V2"""
    card_id: str
    symbol: str
    
    # 总分
    total_score: float
    adjusted_score: float  # 置信度调整后
    grade: str
    
    # 因子得分
    factors: List[FactorScore] = field(default_factory=list)
    
    # 数据质量
    missing_ratio: float = 0.0
    placeholder_count: int = 0
    confidence: float = 1.0
    quality_flag: str = "good"  # good/warning/poor
    
    # 分布检查
    distribution_warnings: List[str] = field(default_factory=list)
    
    # 元数据
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "v2"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "card_id": self.card_id,
            "symbol": self.symbol,
            "total_score": self.total_score,
            "adjusted_score": self.adjusted_score,
            "grade": self.grade,
            "factors": [
                {
                    "factor_id": f.factor_id,
                    "name": f.name,
                    "raw_value": f.raw_value,
                    "score": f.normalized_score,
                    "weight": f.weight,
                    "weighted": f.weighted_score,
                    "percentile": f.percentile,
                    "is_missing": f.is_missing
                }
                for f in self.factors
            ],
            "missing_ratio": self.missing_ratio,
            "confidence": self.confidence,
            "quality_flag": self.quality_flag,
            "distribution_warnings": self.distribution_warnings,
            "version": self.version
        }


class ScoringEngineV2:
    """
    评分引擎 V2
    
    设计原则:
    - 可分布: 所有因子输出必须有分布检查
    - 可解释: 每个因子输出原值/分位/得分
    - 可校准: 缺失值惩罚，不是默认高分
    """
    
    # 因子定义 (V3优化：权重调整，更注重成长性)
    FACTORS = {
        "revenue_growth": {
            "name": "营收增速",
            "weight": 0.18,  # 提高权重
            "missing_penalty": 10,  # 降低惩罚
            # V3：0%=40分, 15%=55分, 25%=70分, 40%=90分
            "score_func": lambda v: min(100, max(0, 40 + v * 1.25)) if v is not None else None,
            "thresholds": [(-10, 20), (0, 40), (15, 60), (25, 75), (40, 90)]
        },
        "profit_growth": {
            "name": "利润增速",
            "weight": 0.18,  # 提高权重
            "missing_penalty": 10,
            # V3：0%=40分, 20%=55分, 35%=70分, 50%=90分
            "score_func": lambda v: min(100, max(0, 40 + v * 1.0)) if v is not None else None,
            "thresholds": [(-20, 15), (0, 40), (20, 60), (35, 80), (50, 95)]
        },
        "gross_margin": {
            "name": "毛利率",
            "weight": 0.12,  # 提高权重
            "missing_penalty": 8,
            # V3：20%=50分, 30%=65分, 40%=80分
            "score_func": lambda v: min(100, max(0, 20 + v * 1.5)) if v is not None else None,
            "thresholds": [(10, 25), (20, 45), (30, 65), (40, 82), (50, 95)]
        },
        "roe": {
            "name": "ROE",
            "weight": 0.10,
            "missing_penalty": 8,
            # V3：3%=40分, 8%=55分, 15%=75分 (放宽早期成长股)
            "score_func": lambda v: min(100, max(0, 30 + v * 3)) if v is not None else None,
            "thresholds": [(0, 25), (3, 40), (8, 60), (15, 80), (20, 95)]
        },
        "cash_flow_ratio": {
            "name": "现金流/利润",
            "weight": 0.08,  # 降低权重（早期成长股可能现金流为负）
            "missing_penalty": 5,
            # V3：放宽，-0.5=30分, 0=45分, 0.8=70分
            "score_func": lambda v: min(100, max(0, 45 + v * 35)) if v is not None else None,
            "thresholds": [(-0.5, 30), (0, 45), (0.5, 60), (0.8, 75), (1.2, 90)]
        },
        "market_cap_small": {
            "name": "小市值",
            "weight": 0.12,  # 新增：小市值加分
            "missing_penalty": 5,
            # V3：<50亿=90分, <100亿=75分, <200亿=60分, <500亿=45分
            "score_func": lambda v: 90 if v is not None and v < 50 else (
                75 if v is not None and v < 100 else (
                    60 if v is not None and v < 200 else (
                        45 if v is not None and v < 500 else 30))) if v is not None else None,
            "thresholds": [(50, 90), (100, 75), (200, 60), (500, 45), (1000, 30)]
        },
        "pe_ratio_reasonable": {
            "name": "PE合理性",
            "weight": 0.08,
            "missing_penalty": 5,
            # V3：PE 15-50为高分区间（成长股）
            "score_func": lambda v: 80 if v is not None and 15 <= v <= 50 else (
                65 if v is not None and (10 <= v < 15 or 50 < v <= 80) else (
                    50 if v is not None and 80 < v <= 100 else 35)) if v is not None else None,
            "thresholds": [(15, 70), (30, 80), (50, 75), (80, 55), (100, 40)]
        },
        "volume_trend": {
            "name": "成交量趋势",
            "weight": 0.07,
            "missing_penalty": 3,
            # V3：量能放大加分
            "score_func": lambda v: min(100, max(0, 40 + v * 30)) if v is not None else None,
            "thresholds": [(0.5, 30), (1.0, 50), (1.5, 70), (2.0, 85), (3.0, 95)]
        },
        "price_trend": {
            "name": "价格趋势",
            "weight": 0.07,
            "missing_penalty": 3,
            # V3：相对强度
            "score_func": lambda v: min(100, max(0, v)) if v is not None else None,
            "thresholds": [(30, 30), (50, 50), (65, 70), (80, 85), (90, 95)]
        }
    }
    
    # 等级阈值 (V3优化：放宽阈值)
    GRADE_THRESHOLDS = [
        (80, "S+"),   # 降低：原85
        (70, "S"),    # 降低：原75
        (58, "A"),    # 降低：原65
        (45, "B"),    # 降低：原50
        (30, "C"),    # 降低：原35
        (0, "D")
    ]
    
    def __init__(self, market_distributions: Dict[str, ScoreDistribution] = None):
        """
        初始化评分引擎
        
        Args:
            market_distributions: 全市场因子分布（用于行业中性）
        """
        self.market_distributions = market_distributions or {}
        self._score_history: Dict[str, List[float]] = {}
        self._factor_distributions: Dict[str, List[float]] = {f: [] for f in self.FACTORS}
    
    def score(self, symbol: str, data: Dict[str, Any]) -> ScoreCardV2:
        """
        计算评分卡
        
        Args:
            symbol: 股票代码
            data: 财务数据
            
        Returns:
            ScoreCardV2
        """
        import uuid
        
        factors = []
        missing_count = 0
        placeholder_count = 0
        total_weight = 0
        weighted_sum = 0
        distribution_warnings = []
        
        for factor_id, config in self.FACTORS.items():
            raw_value = data.get(factor_id)
            weight = config["weight"]
            
            # 检查缺失
            is_missing = raw_value is None
            if is_missing:
                missing_count += 1
                # 缺失惩罚：给保守分
                normalized_score = 50 - config["missing_penalty"]
                explanation = f"数据缺失，应用惩罚-{config['missing_penalty']}"
            else:
                # 正常评分
                score_result = config["score_func"](raw_value)
                if score_result is None:
                    normalized_score = 35  # 计算失败给低分
                    is_missing = True
                    missing_count += 1
                    explanation = "评分计算失败"
                else:
                    normalized_score = score_result
                    explanation = self._generate_explanation(factor_id, raw_value, normalized_score)
                
                # 记录分布
                self._factor_distributions[factor_id].append(normalized_score)
            
            # 检查分布
            if len(self._factor_distributions[factor_id]) > 10:
                std = self._calc_std(self._factor_distributions[factor_id])
                if std < 5:
                    distribution_warnings.append(f"{config['name']}方差过低({std:.1f})")
            
            # 计算分位数
            percentile = self._calc_percentile(factor_id, normalized_score)
            
            weighted_score = normalized_score * weight
            weighted_sum += weighted_score
            total_weight += weight
            
            factors.append(FactorScore(
                factor_id=factor_id,
                name=config["name"],
                raw_value=raw_value,
                normalized_score=normalized_score,
                weight=weight,
                weighted_score=weighted_score,
                is_missing=is_missing,
                percentile=percentile,
                explanation=explanation
            ))
        
        # 计算总分
        total_score = weighted_sum / total_weight if total_weight > 0 else 0
        
        # 计算数据质量和置信度
        missing_ratio = missing_count / len(self.FACTORS)
        confidence = 1.0 - (missing_ratio * 0.5)
        confidence = max(0.3, min(1.0, confidence))
        
        # 置信度调整
        adjusted_score = total_score * confidence
        
        # 确定质量标志
        if confidence >= 0.8:
            quality_flag = "good"
        elif confidence >= 0.5:
            quality_flag = "warning"
        else:
            quality_flag = "poor"
        
        # 确定等级
        grade = self._determine_grade(adjusted_score)
        
        card = ScoreCardV2(
            card_id=f"scv2_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}",
            symbol=symbol,
            total_score=round(total_score, 2),
            adjusted_score=round(adjusted_score, 2),
            grade=grade,
            factors=factors,
            missing_ratio=round(missing_ratio, 2),
            placeholder_count=placeholder_count,
            confidence=round(confidence, 2),
            quality_flag=quality_flag,
            distribution_warnings=distribution_warnings
        )
        
        # 记录历史
        if symbol not in self._score_history:
            self._score_history[symbol] = []
        self._score_history[symbol].append(adjusted_score)
        
        return card
    
    def _generate_explanation(self, factor_id: str, raw_value: Any, score: float) -> str:
        """生成解释"""
        config = self.FACTORS[factor_id]
        thresholds = config.get("thresholds", [])
        
        level = "中等"
        for threshold, threshold_score in thresholds:
            if isinstance(raw_value, (int, float)):
                if raw_value >= threshold:
                    if threshold_score >= 80:
                        level = "优秀"
                    elif threshold_score >= 60:
                        level = "良好"
                    elif threshold_score >= 40:
                        level = "中等"
                    else:
                        level = "较差"
                    break
        
        return f"原值{raw_value}，{level}水平"
    
    def _calc_std(self, values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _calc_percentile(self, factor_id: str, score: float) -> float:
        """计算分位数"""
        history = self._factor_distributions.get(factor_id, [])
        if len(history) < 5:
            return 50.0
        
        sorted_history = sorted(history)
        rank = sum(1 for v in sorted_history if v < score)
        return (rank / len(sorted_history)) * 100
    
    def _determine_grade(self, score: float) -> str:
        """确定等级"""
        for threshold, grade in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "D"
    
    def batch_score(self, stocks: List[Dict[str, Any]]) -> List[ScoreCardV2]:
        """批量评分"""
        results = []
        for stock in stocks:
            result = self.score(
                symbol=stock.get("symbol", ""),
                data=stock.get("data", {})
            )
            results.append(result)
        return results
    
    def get_distribution_report(self) -> Dict[str, Any]:
        """获取分布报告"""
        report = {}
        for factor_id, values in self._factor_distributions.items():
            if len(values) < 5:
                report[factor_id] = {"status": "数据不足", "count": len(values)}
            else:
                std = self._calc_std(values)
                report[factor_id] = {
                    "status": "正常" if std > 5 else "方差过低",
                    "count": len(values),
                    "mean": sum(values) / len(values),
                    "std": std,
                    "min": min(values),
                    "max": max(values)
                }
        return report
    
    def reset(self):
        """重置统计"""
        self._score_history = {}
        self._factor_distributions = {f: [] for f in self.FACTORS}


# 全局实例
_engine: Optional[ScoringEngineV2] = None


def get_scoring_engine_v2() -> ScoringEngineV2:
    """获取评分引擎V2"""
    global _engine
    if _engine is None:
        _engine = ScoringEngineV2()
    return _engine

