"""
三层漏斗候选池 (Candidate Funnel)

L0: 可交易宇宙（硬过滤）
L1: 早期结构候选（不只靠热门主线）
L2: 十倍路径精评（通过率5%-20%）

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FunnelLevel(Enum):
    """漏斗层级"""
    L0_UNIVERSE = "L0"      # 可交易宇宙
    L1_EARLY = "L1"         # 早期结构候选
    L2_TENBAGGER = "L2"     # 十倍路径精评
    REJECTED = "REJECTED"   # 被拒绝


@dataclass
class FunnelResult:
    """漏斗结果"""
    symbol: str
    name: str
    level: FunnelLevel
    passed_filters: List[str] = field(default_factory=list)
    failed_filters: List[str] = field(default_factory=list)
    rejection_reasons: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    data_quality: float = 1.0  # 数据质量 0-1
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class CandidateFunnel:
    """
    三层漏斗候选池
    
    设计原则:
    - 从"能给分"升级为"能拒绝"
    - 低通过率才现实（目标5%-20%）
    - 早期性约束（把成熟大票踢出）
    """
    
    # L0 硬过滤配置
    L0_HARD_FILTERS = {
        "st_check": {
            "name": "ST/退市风险",
            "check": lambda d: not d.get("is_st", False) and not d.get("delisting_risk", False)
        },
        "major_violation": {
            "name": "重大违规",
            "check": lambda d: not d.get("major_violation", False)
        },
        "trading_status": {
            "name": "长期停牌",
            "check": lambda d: d.get("trading_days_ratio", 1.0) >= 0.8
        },
        "financial_report": {
            "name": "财报完整性",
            "check": lambda d: d.get("financial_report_count", 4) >= 3
        },
        "liquidity": {
            "name": "流动性下限",
            "check": lambda d: d.get("avg_turnover", 0.02) >= 0.001 or d.get("turnover_ratio", 0) >= 0.1  # 日均换手>0.1%或turnover_ratio>0.1%
        },
        "data_quality": {
            "name": "数据质量",
            "check": lambda d: d.get("missing_ratio", 0) <= 0.5  # 缺失率<50%
        }
    }
    
    # L1 早期结构信号配置 (V3优化：基于成长性而非仅加速度)
    L1_EARLY_SIGNALS = {
        "revenue_growth": {
            "name": "营收增长",
            "weight": 0.20,
            "check": lambda d: d.get("revenue_growth", 0) > 10,  # 营收增速>10%
            # 评分：0%=30分, 10%=50分, 25%=70分, 40%=90分
            "score": lambda d: min(100, max(0, 30 + d.get("revenue_growth", 0) * 1.5))
        },
        "profit_growth": {
            "name": "利润增长",
            "weight": 0.20,
            "check": lambda d: d.get("profit_growth", 0) > 15,  # 利润增速>15%
            # 评分：0%=30分, 15%=50分, 30%=70分, 50%=90分
            "score": lambda d: min(100, max(0, 30 + d.get("profit_growth", 0) * 1.2))
        },
        "revenue_acceleration": {
            "name": "收入加速",
            "weight": 0.15,
            "check": lambda d: d.get("revenue_growth_qoq_change", 0) > -5,  # 放宽：不大幅下滑即可
            "score": lambda d: min(100, max(0, 50 + d.get("revenue_growth_qoq_change", 0) * 2))
        },
        "gross_margin": {
            "name": "毛利率水平",
            "weight": 0.15,
            "check": lambda d: d.get("gross_margin", 0) > 20,  # 毛利率>20%
            # 评分：20%=50分, 30%=65分, 40%=80分, 50%=95分
            "score": lambda d: min(100, max(0, 20 + d.get("gross_margin", 0) * 1.5))
        },
        "roe_level": {
            "name": "ROE水平",
            "weight": 0.15,
            "check": lambda d: d.get("roe", 0) > 3,  # ROE>3%（早期成长股可较低）
            # 评分：3%=40分, 8%=55分, 15%=70分, 25%=90分
            "score": lambda d: min(100, max(0, 30 + d.get("roe", 0) * 2.5))
        },
        "small_cap_bonus": {
            "name": "小市值加成",
            "weight": 0.15,
            "check": lambda d: d.get("market_cap", 1000) < 300,  # 市值<300亿
            # 小市值加分：<50亿=90分, <100亿=75分, <200亿=60分, <300亿=50分
            "score": lambda d: 90 if d.get("market_cap", 1000) < 50 else (
                75 if d.get("market_cap", 1000) < 100 else (
                    60 if d.get("market_cap", 1000) < 200 else (
                        50 if d.get("market_cap", 1000) < 300 else 30)))
        }
    }
    
    # L2 早期性约束（V3优化：放宽约束，避免误拒）
    L2_EARLY_CONSTRAINTS = {
        "market_cap_ceiling": {
            "name": "市值上限",
            "check": lambda d: d.get("market_cap_percentile", 0) <= 0.9,  # 放宽：市值分位<90%
            "penalty": 15  # 降低惩罚
        },
        "recent_surge_penalty": {
            "name": "近期涨幅过大",
            "check": lambda d: d.get("price_change_24m", 0) <= 3.0,  # 放宽：24个月涨幅<300%
            "penalty": 15
        },
        "institutional_coverage": {
            "name": "机构覆盖过高",
            "check": lambda d: d.get("analyst_coverage", 0) <= 30,  # 放宽：分析师覆盖<30
            "penalty": 10
        },
        "small_cap_early_bonus": {
            "name": "小市值早期",
            "check": lambda d: d.get("market_cap", 1000) < 100,  # 市值<100亿
            "bonus": 15  # 小市值加分
        },
        "high_growth_bonus": {
            "name": "高成长加成",
            "check": lambda d: d.get("revenue_growth", 0) > 25 or d.get("profit_growth", 0) > 30,  # 高增速
            "bonus": 10  # 高成长加分
        },
        "consecutive_improve_bonus": {
            "name": "连续改善",
            "check": lambda d: d.get("consecutive_improvement_quarters", 0) >= 2,  # 连续2季度改善
            "bonus": 10
        }
    }
    
    def __init__(self, target_pass_rate: float = 0.15):
        """
        初始化漏斗
        
        Args:
            target_pass_rate: 目标通过率 (默认15%，范围5%-20%)
        """
        self.target_pass_rate = max(0.05, min(0.20, target_pass_rate))
        self._stats = {
            "l0_input": 0,
            "l0_passed": 0,
            "l1_passed": 0,
            "l2_passed": 0,
            "rejected": 0
        }
    
    def filter_l0(self, symbol: str, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        L0层过滤：硬过滤
        
        Returns:
            (passed, passed_filters, failed_filters)
        """
        passed_filters = []
        failed_filters = []
        
        for filter_id, config in self.L0_HARD_FILTERS.items():
            try:
                if config["check"](data):
                    passed_filters.append(config["name"])
                else:
                    failed_filters.append(config["name"])
            except Exception as e:
                logger.warning(f"L0 filter {filter_id} failed for {symbol}: {e}")
                failed_filters.append(f"{config['name']}(检查失败)")
        
        passed = len(failed_filters) == 0
        return passed, passed_filters, failed_filters
    
    def score_l1(self, symbol: str, data: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """
        L1层评分：早期结构信号
        
        Returns:
            (total_score, dimension_scores)
        """
        scores = {}
        total_weight = 0
        weighted_sum = 0
        
        for signal_id, config in self.L1_EARLY_SIGNALS.items():
            try:
                score = config["score"](data)
                weight = config["weight"]
                scores[config["name"]] = score
                weighted_sum += score * weight
                total_weight += weight
            except Exception as e:
                logger.warning(f"L1 signal {signal_id} failed for {symbol}: {e}")
                scores[config["name"]] = 0
        
        total_score = weighted_sum / total_weight if total_weight > 0 else 0
        return total_score, scores
    
    def apply_l2_constraints(self, symbol: str, data: Dict[str, Any], base_score: float) -> Tuple[float, List[str]]:
        """
        L2层约束：早期性约束
        
        Returns:
            (adjusted_score, constraint_notes)
        """
        adjusted_score = base_score
        notes = []
        
        for constraint_id, config in self.L2_EARLY_CONSTRAINTS.items():
            try:
                passed = config["check"](data)
                
                if not passed and "penalty" in config:
                    adjusted_score -= config["penalty"]
                    notes.append(f"{config['name']}: -{ config['penalty']}分")
                
                if passed and "bonus" in config:
                    adjusted_score += config["bonus"]
                    notes.append(f"{config['name']}: +{config['bonus']}分")
                    
            except Exception as e:
                logger.warning(f"L2 constraint {constraint_id} failed for {symbol}: {e}")
        
        return max(0, adjusted_score), notes
    
    def evaluate(self, symbol: str, name: str, data: Dict[str, Any]) -> FunnelResult:
        """
        完整漏斗评估
        
        Args:
            symbol: 股票代码
            name: 股票名称
            data: 评估数据
            
        Returns:
            FunnelResult
        """
        self._stats["l0_input"] += 1
        
        # L0: 硬过滤
        l0_passed, passed_filters, failed_filters = self.filter_l0(symbol, data)
        
        if not l0_passed:
            self._stats["rejected"] += 1
            return FunnelResult(
                symbol=symbol,
                name=name,
                level=FunnelLevel.REJECTED,
                passed_filters=passed_filters,
                failed_filters=failed_filters,
                rejection_reasons=failed_filters,
                data_quality=data.get("data_quality", 1.0)
            )
        
        self._stats["l0_passed"] += 1
        
        # L1: 早期结构评分
        l1_score, l1_scores = self.score_l1(symbol, data)
        
        # L1 通过阈值：40分（V3放宽：原50分）
        if l1_score < 40:
            self._stats["rejected"] += 1
            return FunnelResult(
                symbol=symbol,
                name=name,
                level=FunnelLevel.L0_UNIVERSE,  # 停留在L0
                passed_filters=passed_filters,
                failed_filters=[f"L1评分不足: {l1_score:.1f}<40"],
                scores=l1_scores,
                data_quality=data.get("data_quality", 1.0)
            )
        
        self._stats["l1_passed"] += 1
        
        # L2: 早期性约束
        l2_score, constraint_notes = self.apply_l2_constraints(symbol, data, l1_score)
        
        # 合并评分
        all_scores = {**l1_scores, "L2调整后": l2_score}
        
        # L2 通过阈值：50分（V3放宽：原65分）
        if l2_score >= 50:
            self._stats["l2_passed"] += 1
            return FunnelResult(
                symbol=symbol,
                name=name,
                level=FunnelLevel.L2_TENBAGGER,
                passed_filters=passed_filters + constraint_notes,
                scores=all_scores,
                data_quality=data.get("data_quality", 1.0)
            )
        else:
            return FunnelResult(
                symbol=symbol,
                name=name,
                level=FunnelLevel.L1_EARLY,  # 停留在L1
                passed_filters=passed_filters,
                failed_filters=[f"L2评分不足: {l2_score:.1f}<65"],
                scores=all_scores,
                data_quality=data.get("data_quality", 1.0)
            )
    
    def batch_evaluate(self, stocks: List[Dict[str, Any]]) -> List[FunnelResult]:
        """批量评估"""
        results = []
        for stock in stocks:
            result = self.evaluate(
                symbol=stock.get("symbol", ""),
                name=stock.get("name", ""),
                data=stock.get("data", {})
            )
            results.append(result)
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        l0_rate = self._stats["l0_passed"] / max(1, self._stats["l0_input"])
        l1_rate = self._stats["l1_passed"] / max(1, self._stats["l0_passed"])
        l2_rate = self._stats["l2_passed"] / max(1, self._stats["l0_input"])
        
        return {
            **self._stats,
            "l0_pass_rate": f"{l0_rate:.1%}",
            "l1_pass_rate": f"{l1_rate:.1%}",
            "l2_pass_rate": f"{l2_rate:.1%}",
            "target_pass_rate": f"{self.target_pass_rate:.1%}",
            "pass_rate_status": "正常" if l2_rate <= self.target_pass_rate else "过高，需收紧"
        }
    
    def reset_stats(self):
        """重置统计"""
        self._stats = {
            "l0_input": 0,
            "l0_passed": 0,
            "l1_passed": 0,
            "l2_passed": 0,
            "rejected": 0
        }


# 全局实例
_funnel: Optional[CandidateFunnel] = None


def get_candidate_funnel(target_pass_rate: float = 0.15) -> CandidateFunnel:
    """获取候选池漏斗"""
    global _funnel
    if _funnel is None:
        _funnel = CandidateFunnel(target_pass_rate)
    return _funnel

