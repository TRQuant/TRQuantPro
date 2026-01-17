"""
V3.0 本周投资推荐系统
=====================

核心模块:
1. market_trend_v3 - 市场趋势分析 (多周期共振+HMM)
2. mainline_five_dim_v3 - 五维主线识别 (资金/热度/动量/政策/龙头)
3. momentum_scorer_v3 - A股动量评分 (可扩展接口)
4. filter_options_v3 - 筛选条件选项 (A股特征适配)
5. backtest_verifier_v3 - 筛选条件回测验证
6. genetic_optimizer_v3 - 遗传算法多目标优化
7. data_manager_v3 - MongoDB统一数据管理
8. report_generator_v3 - HTML报告生成 (含交易策略)
9. workflow_v3 - 主工作流

版本: 3.0
日期: 2026-01-07
"""

# 市场趋势分析
from .market_trend_v3 import MarketTrendAnalyzerV3, MarketTrendResultV3

# 五维主线识别
from .mainline_five_dim_v3 import (
    MainlineFiveDimScorerV3,
    MainlineResultV3,
    MainlineSignal,
    analyze_mainlines,
    get_top_mainlines,
    get_strong_mainlines,
)

# A股动量评分
from .momentum_scorer_v3 import (
    MomentumScorerV3,
    MomentumScoreV3,
    MomentumFactorBase,
    score_momentum,
    get_top_momentum,
)

# 筛选条件选项
from .filter_options_v3 import (
    FilterOptionsV3,
    FilterPresets,
    FilterStyle,
    MarketCondition,
    StockFilterV3,
    filter_stocks,
    get_filter_options,
)

# 回测验证
from .backtest_verifier_v3 import (
    BacktestVerifierV3,
    BacktestResult,
    BacktestMetrics,
    verify_filter,
    compare_filters,
)

# 遗传算法优化
from .genetic_optimizer_v3 import (
    GeneticOptimizerV3,
    OptimizationResult,
    OptimizationObjective,
    OptimizationMode,
    ObjectiveType,
    optimize_filter_params,
)

# 数据管理
from .data_manager_v3 import (
    DataManagerV3,
    get_data_manager,
    save_recommendation,
    get_recommendation,
)

# HTML报告生成
from .report_generator_v3 import (
    ReportGeneratorV3,
    generate_report,
)

# 主工作流
from .workflow_v3 import (
    WeeklyAdvisorV3,
    WorkflowConfig,
    run_weekly_advisor,
)

# 滚动验证（Walk-forward Validation）
from .rolling_validator import (
    RollingValidator,
    ValidationSummary,
    RollingPeriodResult,
    RecommendationResult,
    quick_validate,
)

# 高收益推荐器（基于10%+因子研究）
from .high_return_recommender import (
    HighReturnRecommender,
    HighReturnConfig,
    SelectionMode,
    RecommendedStock,
    get_high_return_recommendations,
)

__version__ = "3.0.0"
__all__ = [
    # 市场趋势
    "MarketTrendAnalyzerV3",
    "MarketTrendResultV3",
    # 五维主线
    "MainlineFiveDimScorerV3",
    "MainlineResultV3",
    "MainlineSignal",
    "analyze_mainlines",
    "get_top_mainlines",
    "get_strong_mainlines",
    # 动量评分
    "MomentumScorerV3",
    "MomentumScoreV3",
    "MomentumFactorBase",
    "score_momentum",
    "get_top_momentum",
    # 筛选条件
    "FilterOptionsV3",
    "FilterPresets",
    "FilterStyle",
    "MarketCondition",
    "StockFilterV3",
    "filter_stocks",
    "get_filter_options",
    # 回测验证
    "BacktestVerifierV3",
    "BacktestResult",
    "BacktestMetrics",
    "verify_filter",
    "compare_filters",
    # 遗传算法
    "GeneticOptimizerV3",
    "OptimizationResult",
    "OptimizationObjective",
    "OptimizationMode",
    "ObjectiveType",
    "optimize_filter_params",
    # 数据管理
    "DataManagerV3",
    "get_data_manager",
    "save_recommendation",
    "get_recommendation",
    # 报告生成
    "ReportGeneratorV3",
    "generate_report",
    # 主工作流
    "WeeklyAdvisorV3",
    "WorkflowConfig",
    "run_weekly_advisor",
    # 滚动验证
    "RollingValidator",
    "ValidationSummary",
    "RollingPeriodResult",
    "RecommendationResult",
    "quick_validate",
    # 高收益推荐器
    "HighReturnRecommender",
    "HighReturnConfig",
    "SelectionMode",
    "RecommendedStock",
    "get_high_return_recommendations",
]
