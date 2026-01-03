"""
十倍股评估器 V2 (Tenbagger Evaluator V2)

整合三层漏斗、双引擎、三轴阶段状态机的完整评估系统

设计原则:
- 目标是"十倍股早期识别"，不是"优质大盘股筛选"
- 低通过率（5%-20%）才现实
- 输出可解释、可追溯

Author: TRQuant Team
Date: 2025-12-19
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import uuid

from .candidate_funnel import CandidateFunnel, FunnelLevel, FunnelResult, get_candidate_funnel
from .rule_engine import RuleEngine, VetoResult, get_rule_engine
from .scoring_engine_v2 import ScoringEngineV2, ScoreCardV2, get_scoring_engine_v2
from .tri_axis_stage import TriAxisStageMachine, Stage, StageResult, get_tri_axis_stage_machine
from .pass_rate_controller import PassRateController, ConsistencyReport, get_pass_rate_controller

logger = logging.getLogger(__name__)


@dataclass
class TenbaggerReportV2:
    """十倍股评估报告V2"""
    report_id: str
    symbol: str
    name: str
    
    # 最终结果
    is_recommended: bool
    recommendation_level: str  # S+/S/A/B/C/D/REJECTED
    final_score: float
    
    # 漏斗结果
    funnel_level: str  # L0/L1/L2/REJECTED
    funnel_result: Dict[str, Any] = field(default_factory=dict)
    
    # 否决检查
    is_vetoed: bool = False
    veto_reasons: List[str] = field(default_factory=list)
    
    # 阶段判定
    stage: str = "S0"
    stage_confidence: float = 0.0
    stage_evidence: List[str] = field(default_factory=list)
    
    # 评分卡
    scorecard: Dict[str, Any] = field(default_factory=dict)
    
    # 数据质量
    data_quality: float = 1.0
    quality_flag: str = "good"
    
    # 解释
    recommendation_reason: str = ""
    risk_warnings: List[str] = field(default_factory=list)
    
    # 元数据
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = "v2"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "symbol": self.symbol,
            "name": self.name,
            "is_recommended": self.is_recommended,
            "recommendation_level": self.recommendation_level,
            "final_score": self.final_score,
            "funnel_level": self.funnel_level,
            "is_vetoed": self.is_vetoed,
            "veto_reasons": self.veto_reasons,
            "stage": self.stage,
            "stage_confidence": self.stage_confidence,
            "stage_evidence": self.stage_evidence,
            "scorecard": self.scorecard,
            "data_quality": self.data_quality,
            "quality_flag": self.quality_flag,
            "recommendation_reason": self.recommendation_reason,
            "risk_warnings": self.risk_warnings,
            "timestamp": self.timestamp,
            "version": self.version
        }


class TenbaggerEvaluatorV2:
    """
    十倍股评估器 V2
    
    完整评估流程:
    1. 规则引擎检查（一票否决）
    2. 三层漏斗筛选
    3. 三轴阶段判定
    4. 评分引擎V2评分
    5. 通过率控制
    6. 生成报告
    """
    
    # 推荐等级阈值
    RECOMMENDATION_THRESHOLDS = {
        "S+": {"min_score": 85, "min_stage": "S1", "max_stage": "S3"},
        "S": {"min_score": 75, "min_stage": "S1", "max_stage": "S3"},
        "A": {"min_score": 65, "min_stage": "S1", "max_stage": "S4"},
        "B": {"min_score": 50, "min_stage": "S0", "max_stage": "S5"},
        "C": {"min_score": 35, "min_stage": "S0", "max_stage": "S5"},
        "D": {"min_score": 0, "min_stage": "S0", "max_stage": "S5"}
    }
    
    def __init__(
        self,
        funnel: CandidateFunnel = None,
        rule_engine: RuleEngine = None,
        scoring_engine: ScoringEngineV2 = None,
        stage_machine: TriAxisStageMachine = None,
        pass_controller: PassRateController = None
    ):
        """
        初始化评估器
        
        Args:
            funnel: 候选池漏斗
            rule_engine: 规则引擎
            scoring_engine: 评分引擎
            stage_machine: 阶段状态机
            pass_controller: 通过率控制器
        """
        self.funnel = funnel or get_candidate_funnel()
        self.rule_engine = rule_engine or get_rule_engine()
        self.scoring_engine = scoring_engine or get_scoring_engine_v2()
        self.stage_machine = stage_machine or get_tri_axis_stage_machine()
        self.pass_controller = pass_controller or get_pass_rate_controller()
        
        self._reports: Dict[str, TenbaggerReportV2] = {}
    
    def evaluate(self, symbol: str, name: str, data: Dict[str, Any]) -> TenbaggerReportV2:
        """
        完整评估单只股票
        
        Args:
            symbol: 股票代码
            name: 股票名称
            data: 评估数据
            
        Returns:
            TenbaggerReportV2
        """
        report_id = f"tb2_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # 1. 规则引擎检查（一票否决）
        veto_result = self.rule_engine.check(symbol, data)
        
        if veto_result.is_vetoed:
            self.pass_controller.record_evaluation("REJECTED")
            report = TenbaggerReportV2(
                report_id=report_id,
                symbol=symbol,
                name=name,
                is_recommended=False,
                recommendation_level="REJECTED",
                final_score=0,
                funnel_level="REJECTED",
                is_vetoed=True,
                veto_reasons=veto_result.messages,
                recommendation_reason="触发一票否决规则",
                risk_warnings=veto_result.messages
            )
            self._reports[symbol] = report
            return report
        
        # 2. 三层漏斗筛选
        funnel_result = self.funnel.evaluate(symbol, name, data)
        
        if funnel_result.level == FunnelLevel.REJECTED:
            self.pass_controller.record_evaluation("REJECTED")
            report = TenbaggerReportV2(
                report_id=report_id,
                symbol=symbol,
                name=name,
                is_recommended=False,
                recommendation_level="REJECTED",
                final_score=0,
                funnel_level=funnel_result.level.value,
                funnel_result={"failed_filters": funnel_result.failed_filters},
                recommendation_reason="未通过漏斗筛选",
                risk_warnings=funnel_result.rejection_reasons
            )
            self._reports[symbol] = report
            return report
        
        # 记录漏斗层级
        self.pass_controller.record_evaluation(funnel_result.level.value)
        
        # 3. 三轴阶段判定
        stage_result = self.stage_machine.evaluate(symbol, data)
        
        # 4. 评分引擎V2评分
        scorecard = self.scoring_engine.score(symbol, data)
        
        # 5. 综合计算最终得分
        final_score = self._calculate_final_score(
            funnel_result,
            stage_result,
            scorecard
        )
        
        # 6. 确定推荐等级
        recommendation_level = self._determine_level(
            final_score,
            stage_result.stage
        )
        
        # 是否推荐
        is_recommended = (
            funnel_result.level == FunnelLevel.L2_TENBAGGER and
            recommendation_level in ["S+", "S", "A"] and
            stage_result.stage in [Stage.S1, Stage.S2, Stage.S3]
        )
        
        # 生成推荐理由
        recommendation_reason = self._generate_recommendation(
            is_recommended,
            recommendation_level,
            stage_result.stage,
            final_score
        )
        
        # 收集风险警告
        risk_warnings = []
        if scorecard.distribution_warnings:
            risk_warnings.extend(scorecard.distribution_warnings)
        if scorecard.quality_flag == "poor":
            risk_warnings.append("数据质量较差，评估置信度低")
        if stage_result.confidence < 0.5:
            risk_warnings.append(f"阶段判定置信度较低({stage_result.confidence:.1%})")
        
        report = TenbaggerReportV2(
            report_id=report_id,
            symbol=symbol,
            name=name,
            is_recommended=is_recommended,
            recommendation_level=recommendation_level,
            final_score=round(final_score, 2),
            funnel_level=funnel_result.level.value,
            funnel_result={"scores": funnel_result.scores},
            stage=stage_result.stage.value,
            stage_confidence=round(stage_result.confidence, 2),
            stage_evidence=stage_result.transition_evidence,
            scorecard=scorecard.to_dict(),
            data_quality=scorecard.confidence,
            quality_flag=scorecard.quality_flag,
            recommendation_reason=recommendation_reason,
            risk_warnings=risk_warnings
        )
        
        self._reports[symbol] = report
        return report
    
    def _calculate_final_score(
        self,
        funnel_result: FunnelResult,
        stage_result: StageResult,
        scorecard: ScoreCardV2
    ) -> float:
        """
        计算最终得分
        
        权重:
        - 漏斗得分: 30%
        - 阶段得分: 30%
        - 评分卡: 40%
        """
        # 漏斗得分（从L1分数转换）
        funnel_score = funnel_result.scores.get("L2调整后", 50)
        
        # 阶段得分
        stage_scores = {
            "S0": 20, "S1": 50, "S2": 80, "S3": 70, "S4": 50, "S5": 30
        }
        stage_score = stage_scores.get(stage_result.stage.value, 30)
        stage_score = stage_score * stage_result.confidence
        
        # 评分卡得分（已经调整过置信度）
        scorecard_score = scorecard.adjusted_score
        
        # 加权计算
        final = (funnel_score * 0.30 + stage_score * 0.30 + scorecard_score * 0.40)
        
        return final
    
    def _determine_level(self, score: float, stage: Stage) -> str:
        """确定推荐等级"""
        stage_value = stage.value
        
        for level, thresholds in self.RECOMMENDATION_THRESHOLDS.items():
            if score >= thresholds["min_score"]:
                # 检查阶段约束
                min_stage = thresholds["min_stage"]
                max_stage = thresholds["max_stage"]
                
                stage_order = ["S0", "S1", "S2", "S3", "S4", "S5"]
                if stage_order.index(stage_value) >= stage_order.index(min_stage):
                    if stage_order.index(stage_value) <= stage_order.index(max_stage):
                        return level
        
        return "D"
    
    def _generate_recommendation(
        self,
        is_recommended: bool,
        level: str,
        stage: Stage,
        score: float
    ) -> str:
        """生成推荐理由"""
        stage_names = {
            "S0": "观察期",
            "S1": "验证期",
            "S2": "导入期（最佳介入点）",
            "S3": "放量期",
            "S4": "加速期",
            "S5": "成熟期"
        }
        
        stage_name = stage_names.get(stage.value, stage.value)
        
        if is_recommended:
            if level in ["S+", "S"]:
                return f"强烈推荐：{level}级，{stage_name}，综合评分{score:.1f}，具备十倍股早期特征"
            else:
                return f"建议关注：{level}级，{stage_name}，评分{score:.1f}，值得持续跟踪"
        else:
            if level == "REJECTED":
                return "不推荐：触发否决规则或未通过筛选"
            elif stage.value in ["S4", "S5"]:
                return f"暂不推荐：{stage_name}，已非早期阶段"
            else:
                return f"暂不推荐：{level}级，评分{score:.1f}，未达到早期识别标准"
    
    def batch_evaluate(self, stocks: List[Dict[str, Any]]) -> List[TenbaggerReportV2]:
        """批量评估"""
        # 开始新的运行
        run_id = self.pass_controller.start_run()
        logger.info(f"开始批量评估 run_id={run_id}, 股票数={len(stocks)}")
        
        results = []
        for stock in stocks:
            result = self.evaluate(
                symbol=stock.get("symbol", ""),
                name=stock.get("name", ""),
                data=stock.get("data", {})
            )
            results.append(result)
        
        # 检查通过率
        needs_adjust, msg = self.pass_controller.check_and_adjust()
        if needs_adjust:
            logger.warning(msg)
        
        return results
    
    def get_recommendations(self, min_level: str = "A") -> List[TenbaggerReportV2]:
        """
        获取推荐列表
        
        Args:
            min_level: 最低等级 (S+/S/A/B/C/D)
            
        Returns:
            推荐列表
        """
        level_order = {"S+": 0, "S": 1, "A": 2, "B": 3, "C": 4, "D": 5, "REJECTED": 6}
        min_order = level_order.get(min_level, 2)
        
        recommendations = [
            r for r in self._reports.values()
            if r.is_recommended and level_order.get(r.recommendation_level, 6) <= min_order
        ]
        
        # 按分数排序
        recommendations.sort(key=lambda x: x.final_score, reverse=True)
        return recommendations
    
    def get_report(self, symbol: str) -> Optional[TenbaggerReportV2]:
        """获取单只股票报告"""
        return self._reports.get(symbol)
    
    def generate_consistency_report(self) -> ConsistencyReport:
        """生成一致性报告"""
        # 统计等级分布
        grade_distribution = {}
        for report in self._reports.values():
            level = report.recommendation_level
            grade_distribution[level] = grade_distribution.get(level, 0) + 1
        
        return self.pass_controller.generate_report(grade_distribution)
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_evaluated": len(self._reports),
            "recommended": sum(1 for r in self._reports.values() if r.is_recommended),
            "rejected": sum(1 for r in self._reports.values() if r.recommendation_level == "REJECTED"),
            "by_level": {
                level: sum(1 for r in self._reports.values() if r.recommendation_level == level)
                for level in ["S+", "S", "A", "B", "C", "D", "REJECTED"]
            },
            "by_stage": {
                stage: sum(1 for r in self._reports.values() if r.stage == stage)
                for stage in ["S0", "S1", "S2", "S3", "S4", "S5"]
            },
            "funnel_stats": self.funnel.get_stats(),
            "rule_engine_stats": self.rule_engine.get_stats(),
            "pass_rate_stats": self.pass_controller.stats.__dict__
        }
    
    def reset(self):
        """重置所有状态"""
        self._reports.clear()
        self.funnel.reset_stats()
        self.rule_engine.reset_stats()
        self.scoring_engine.reset()
        self.pass_controller.reset()


# 全局实例
_evaluator: Optional[TenbaggerEvaluatorV2] = None


def get_evaluator_v2() -> TenbaggerEvaluatorV2:
    """获取评估器V2"""
    global _evaluator
    if _evaluator is None:
        _evaluator = TenbaggerEvaluatorV2()
    return _evaluator

