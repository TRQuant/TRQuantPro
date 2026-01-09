"""
Investment Advisor V4.0 - 多因子预测投资系统

核心特点：
1. 预测性因子：使用T-5时刻数据预测T时刻的高收益
2. 机器学习模型：XGBoost自动学习因子组合
3. 完整交易系统：入场、出场、仓位、风控一体化
4. 参数进化：根据回测结果自动优化

使用方法：
    from core.advisor_v4 import AdvisorV4Workflow
    
    advisor = AdvisorV4Workflow()
    advisor.train()  # 训练模型
    advisor.backtest()  # 回测验证
    recommendations = advisor.recommend()  # 生成推荐
"""

__version__ = "4.0.0"

# 延迟导入避免循环依赖
def __getattr__(name):
    if name == "PredictorFactorExtractor":
        from .predictor_factor_extractor import PredictorFactorExtractor
        return PredictorFactorExtractor
    elif name == "PredictiveFeature":
        from .predictor_factor_extractor import PredictiveFeature
        return PredictiveFeature
    elif name == "MultiFactorCalculator":
        from .multi_factor_calculator import MultiFactorCalculator
        return MultiFactorCalculator
    elif name == "FactorDimension":
        from .multi_factor_calculator import FactorDimension
        return FactorDimension
    elif name == "XGBoostPredictor":
        from .xgboost_predictor import XGBoostPredictor
        return XGBoostPredictor
    elif name == "PredictionResult":
        from .xgboost_predictor import PredictionResult
        return PredictionResult
    elif name == "TradingStrategy":
        from .trading_strategy import TradingStrategy
        return TradingStrategy
    elif name == "TradeSignal":
        from .trading_strategy import TradeSignal
        return TradeSignal
    elif name == "Position":
        from .trading_strategy import Position
        return Position
    elif name == "TradingConfig":
        from .trading_strategy import TradingConfig
        return TradingConfig
    elif name == "BacktestEngine":
        from .backtest_engine import BacktestEngine
        return BacktestEngine
    elif name == "BacktestResult":
        from .backtest_engine import BacktestResult
        return BacktestResult
    elif name == "ParamOptimizer":
        from .param_optimizer import ParamOptimizer
        return ParamOptimizer
    elif name == "OptimizationResult":
        from .param_optimizer import OptimizationResult
        return OptimizationResult
    elif name == "AdvisorV4Workflow":
        from .advisor_v4_workflow import AdvisorV4Workflow
        return AdvisorV4Workflow
    elif name == "AdvisorV4Config":
        from .advisor_v4_workflow import AdvisorV4Config
        return AdvisorV4Config
    elif name == "JoinQuantStrategyGenerator":
        from .joinquant_strategy_generator import JoinQuantStrategyGenerator
        return JoinQuantStrategyGenerator
    elif name == "V4DataStorage":
        from .data_storage import V4DataStorage
        return V4DataStorage
    elif name == "get_v4_storage":
        from .data_storage import get_v4_storage
        return get_v4_storage
    # 进化优化模块
    elif name == "ModelEvolver":
        from .model_evolver import ModelEvolver
        return ModelEvolver
    elif name == "EvolutionConfig":
        from .model_evolver import EvolutionConfig
        return EvolutionConfig
    elif name == "EvolutionResult":
        from .model_evolver import EvolutionResult
        return EvolutionResult
    elif name == "FeatureExpander":
        from .feature_expander import FeatureExpander
        return FeatureExpander
    elif name == "HyperparameterOptimizer":
        from .hyperparameter_optimizer import HyperparameterOptimizer
        return HyperparameterOptimizer
    elif name == "DataAugmenter":
        from .data_augmenter import DataAugmenter
        return DataAugmenter
    elif name == "EnsemblePredictor":
        from .ensemble_predictor import EnsemblePredictor
        return EnsemblePredictor
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # 版本
    "__version__",
    # 因子提取
    "PredictorFactorExtractor",
    "PredictiveFeature",
    # 因子计算
    "MultiFactorCalculator", 
    "FactorDimension",
    # 预测模型
    "XGBoostPredictor",
    "PredictionResult",
    # 交易策略
    "TradingStrategy",
    "TradeSignal",
    "Position",
    "TradingConfig",
    # 回测
    "BacktestEngine",
    "BacktestResult",
    # 优化
    "ParamOptimizer",
    "OptimizationResult",
    # 工作流
    "AdvisorV4Workflow",
    "AdvisorV4Config",
    # 策略生成
    "JoinQuantStrategyGenerator",
    # 数据存储
    "V4DataStorage",
    "get_v4_storage",
    # 进化优化
    "ModelEvolver",
    "EvolutionConfig",
    "EvolutionResult",
    "FeatureExpander",
    "HyperparameterOptimizer",
    "DataAugmenter",
    "EnsemblePredictor",
]
