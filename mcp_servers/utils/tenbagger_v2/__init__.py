"""
十倍股早期识别系统 V2

核心组件:
1. CandidateFunnel - 三层漏斗候选池
2. RuleEngine - 规则引擎（一票否决）
3. ScoringEngineV2 - 评分引擎V2（可校准）
4. TriAxisStageMachine - 三轴阶段状态机
5. PassRateController - 通过率控制器

设计原则:
- 目标是"十倍股早期识别"，不是"优质大盘股筛选"
- 低通过率（5%-20%）才现实
- 缺失数据 = 惩罚，不是高分
- 可分布、可解释、可校准

Author: TRQuant Team
Date: 2025-12-19
Version: 2.0
"""

from .candidate_funnel import CandidateFunnel, FunnelLevel, get_candidate_funnel
from .rule_engine import RuleEngine, VetoRule, get_rule_engine
from .scoring_engine_v2 import ScoringEngineV2, ScoreDistribution, get_scoring_engine_v2
from .tri_axis_stage import TriAxisStageMachine, StageAxis, Stage, get_tri_axis_stage_machine
from .pass_rate_controller import PassRateController, get_pass_rate_controller
from .evaluator_v2 import TenbaggerEvaluatorV2, TenbaggerReportV2, get_evaluator_v2
from .report_generator import ReportGenerator

__all__ = [
    # 候选池漏斗
    'CandidateFunnel',
    'FunnelLevel',
    'get_candidate_funnel',
    # 规则引擎
    'RuleEngine',
    'VetoRule',
    'get_rule_engine',
    # 评分引擎V2
    'ScoringEngineV2',
    'ScoreDistribution',
    'get_scoring_engine_v2',
    # 三轴阶段状态机
    'TriAxisStageMachine',
    'StageAxis',
    'Stage',
    'get_tri_axis_stage_machine',
    # 通过率控制
    'PassRateController',
    'get_pass_rate_controller',
    # 评估器V2
    'TenbaggerEvaluatorV2',
    'TenbaggerReportV2',
    'get_evaluator_v2',
    # 报告生成器
    'ReportGenerator'
]

__version__ = "2.0.0"

