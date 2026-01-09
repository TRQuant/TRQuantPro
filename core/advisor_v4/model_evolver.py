# -*- coding: utf-8 -*-
"""
模型进化器 - 递归优化预测模型直到达到目标性能

功能：
1. 自动化迭代优化循环
2. 动态策略生成与应用
3. 性能跟踪与早停机制
4. 最佳模型保存

目标：AUC >= 0.70
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Callable
import pickle
import json
import logging
from tqdm import tqdm

logger = logging.getLogger(__name__)

# 导入依赖模块
try:
    from .xgboost_predictor import XGBoostPredictor, ModelMetrics
    from .feature_pipeline import FeaturePipeline, FeaturePipelineConfig
    from .cross_validator import TimeSeriesCrossValidator, WalkForwardValidator
except ImportError:
    pass


# ============================================================
# 数据类
# ============================================================

@dataclass
class EvolutionConfig:
    """进化配置"""
    target_auc: float = 0.70          # 目标AUC
    max_iterations: int = 20          # 最大迭代次数
    patience: int = 5                 # 早停耐心值
    min_improvement: float = 0.01     # 最小改进阈值
    
    # 策略权重
    feature_expansion_weight: float = 0.3
    hyperparameter_weight: float = 0.3
    data_augmentation_weight: float = 0.2
    ensemble_weight: float = 0.2


@dataclass
class IterationResult:
    """单次迭代结果"""
    iteration: int
    strategy_name: str
    strategy_config: Dict
    
    # 指标
    train_auc: float
    val_auc: float
    test_auc: float = 0.0
    
    train_precision: float = 0.0
    val_precision: float = 0.0
    
    train_f1: float = 0.0
    val_f1: float = 0.0
    
    # 改进
    improvement: float = 0.0
    
    # 时间
    duration_seconds: float = 0.0
    timestamp: str = ""
    
    # 模型路径
    model_path: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'iteration': self.iteration,
            'strategy_name': self.strategy_name,
            'strategy_config': self.strategy_config,
            'train_auc': self.train_auc,
            'val_auc': self.val_auc,
            'test_auc': self.test_auc,
            'train_precision': self.train_precision,
            'val_precision': self.val_precision,
            'train_f1': self.train_f1,
            'val_f1': self.val_f1,
            'improvement': self.improvement,
            'duration_seconds': self.duration_seconds,
            'timestamp': self.timestamp,
            'model_path': self.model_path,
        }


@dataclass
class EvolutionResult:
    """进化结果"""
    success: bool
    total_iterations: int
    best_auc: float
    best_iteration: int
    best_config: Dict
    best_model_path: str
    
    history: List[IterationResult] = field(default_factory=list)
    reason: str = ""  # 'target_reached', 'patience_exceeded', 'max_iterations'
    
    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'total_iterations': self.total_iterations,
            'best_auc': self.best_auc,
            'best_iteration': self.best_iteration,
            'best_config': self.best_config,
            'best_model_path': self.best_model_path,
            'reason': self.reason,
            'history': [h.to_dict() for h in self.history],
        }


# ============================================================
# 优化策略
# ============================================================

class OptimizationStrategy:
    """优化策略基类"""
    
    def __init__(self, name: str, config: Dict = None):
        self.name = name
        self.config = config or {}
    
    def apply(self, train_df: pd.DataFrame, val_df: pd.DataFrame, 
              current_config: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
        """应用策略
        
        Args:
            train_df: 训练数据
            val_df: 验证数据
            current_config: 当前模型配置
            
        Returns:
            (modified_train_df, modified_val_df, updated_config)
        """
        raise NotImplementedError


class FeatureExpansionStrategy(OptimizationStrategy):
    """特征扩展策略"""
    
    def __init__(self, config: Dict = None):
        super().__init__("feature_expansion", config)
    
    def apply(self, train_df, val_df, current_config):
        from .feature_expander import FeatureExpander
        
        expander = FeatureExpander()
        
        # 扩展特征
        train_df = expander.expand_features(train_df)
        val_df = expander.expand_features(val_df)
        
        # 更新配置
        current_config['feature_columns'] = expander.get_all_feature_columns()
        current_config['expanded_features'] = expander.get_expanded_features()
        
        return train_df, val_df, current_config


class FeatureSelectionStrategy(OptimizationStrategy):
    """特征选择策略"""
    
    def __init__(self, config: Dict = None):
        super().__init__("feature_selection", config)
        self.top_k = config.get('top_k', 15) if config else 15
        self.method = config.get('method', 'combined') if config else 'combined'
    
    def apply(self, train_df, val_df, current_config):
        pipeline_config = FeaturePipelineConfig(
            top_k_features=self.top_k,
            select_method=self.method
        )
        
        pipeline = FeaturePipeline(pipeline_config)
        
        # 获取特征列
        feature_cols = current_config.get('feature_columns', XGBoostPredictor.FEATURE_COLUMNS)
        available_cols = [c for c in feature_cols if c in train_df.columns]
        
        X_train = train_df[available_cols].copy()
        y_train = train_df['label'].copy()
        
        # Fit transform
        X_train_transformed = pipeline.fit_transform(X_train, y_train)
        X_val_transformed = pipeline.transform(val_df[available_cols])
        
        # 更新数据
        for col in X_train_transformed.columns:
            train_df[col] = X_train_transformed[col].values
            val_df[col] = X_val_transformed[col].values
        
        current_config['selected_features'] = pipeline.get_selected_features()
        current_config['feature_scores'] = pipeline.get_feature_importance()
        current_config['feature_pipeline'] = pipeline
        
        return train_df, val_df, current_config


class HyperparameterTuningStrategy(OptimizationStrategy):
    """超参数调优策略"""
    
    def __init__(self, config: Dict = None):
        super().__init__("hyperparameter_tuning", config)
        self.n_trials = config.get('n_trials', 30) if config else 30
    
    def apply(self, train_df, val_df, current_config):
        from .hyperparameter_optimizer import HyperparameterOptimizer
        
        optimizer = HyperparameterOptimizer()
        
        # 获取特征列
        feature_cols = current_config.get('selected_features') or \
                       current_config.get('feature_columns') or \
                       XGBoostPredictor.FEATURE_COLUMNS
        
        best_params = optimizer.optimize(
            train_df, val_df, 
            feature_cols=feature_cols,
            n_trials=self.n_trials
        )
        
        current_config['model_params'] = best_params
        current_config['tuning_history'] = optimizer.get_history()
        
        return train_df, val_df, current_config


class DataAugmentationStrategy(OptimizationStrategy):
    """数据增强策略"""
    
    def __init__(self, config: Dict = None):
        super().__init__("data_augmentation", config)
        self.target_ratio = config.get('target_ratio', 2.0) if config else 2.0
    
    def apply(self, train_df, val_df, current_config):
        from .data_augmenter import DataAugmenter
        
        augmenter = DataAugmenter()
        
        # 增强训练数据
        train_df = augmenter.augment(train_df, target_ratio=self.target_ratio)
        
        current_config['augmentation_info'] = augmenter.get_info()
        
        return train_df, val_df, current_config


class EnsembleStrategy(OptimizationStrategy):
    """集成方法策略"""
    
    def __init__(self, config: Dict = None):
        super().__init__("ensemble", config)
        self.n_models = config.get('n_models', 3) if config else 3
    
    def apply(self, train_df, val_df, current_config):
        current_config['ensemble'] = True
        current_config['n_models'] = self.n_models
        
        return train_df, val_df, current_config


# ============================================================
# 模型进化器（主类）
# ============================================================

class ModelEvolver:
    """模型进化器 - 递归优化直到达到目标性能"""
    
    def __init__(self, config: EvolutionConfig = None, verbose: bool = True):
        """
        Args:
            config: 进化配置
            verbose: 是否打印详细信息
        """
        self.config = config or EvolutionConfig()
        self.verbose = verbose
        
        # 状态
        self.iteration_history: List[IterationResult] = []
        self.best_model = None
        self.best_auc = 0.0
        self.best_config = {}
        self.best_iteration = 0
        
        # 策略池
        self.strategies = self._init_strategies()
        
        # 输出目录
        self.output_dir = Path("results/evolution")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_strategies(self) -> Dict[str, List[OptimizationStrategy]]:
        """初始化策略池"""
        return {
            'phase1': [  # 迭代1-3：特征工程
                FeatureExpansionStrategy({'level': 1}),
                FeatureSelectionStrategy({'top_k': 12, 'method': 'combined'}),
            ],
            'phase2': [  # 迭代4-6：特征工程 + 数据增强
                FeatureExpansionStrategy({'level': 2}),
                FeatureSelectionStrategy({'top_k': 15, 'method': 'combined'}),
                DataAugmentationStrategy({'target_ratio': 2.0}),
            ],
            'phase3': [  # 迭代7-10：超参数调优
                HyperparameterTuningStrategy({'n_trials': 30}),
            ],
            'phase4': [  # 迭代11-15：更激进的调优
                HyperparameterTuningStrategy({'n_trials': 50}),
                FeatureSelectionStrategy({'top_k': 20, 'method': 'combined'}),
            ],
            'phase5': [  # 迭代16+：集成方法
                EnsembleStrategy({'n_models': 3}),
            ],
        }
    
    def _get_phase(self, iteration: int) -> str:
        """根据迭代次数获取阶段"""
        if iteration <= 3:
            return 'phase1'
        elif iteration <= 6:
            return 'phase2'
        elif iteration <= 10:
            return 'phase3'
        elif iteration <= 15:
            return 'phase4'
        else:
            return 'phase5'
    
    def evolve(self, 
               train_df: pd.DataFrame,
               val_df: pd.DataFrame,
               test_df: pd.DataFrame = None) -> EvolutionResult:
        """执行迭代优化
        
        Args:
            train_df: 训练数据
            val_df: 验证数据
            test_df: 测试数据（可选，用于最终评估）
            
        Returns:
            EvolutionResult
        """
        print(f"\n{'='*70}")
        print(f"【模型进化器】目标 AUC >= {self.config.target_auc}")
        print(f"最大迭代: {self.config.max_iterations} | 早停耐心: {self.config.patience}")
        print(f"{'='*70}\n")
        
        iteration = 0
        no_improve_count = 0
        current_config = {}
        
        while iteration < self.config.max_iterations:
            iteration += 1
            start_time = datetime.now()
            
            print(f"\n{'='*60}")
            print(f"【迭代 {iteration}/{self.config.max_iterations}】")
            print(f"{'='*60}")
            
            # 1. 获取当前阶段的策略
            phase = self._get_phase(iteration)
            strategies = self.strategies.get(phase, [])
            
            print(f"阶段: {phase}")
            print(f"策略: {[s.name for s in strategies]}")
            
            # 2. 应用策略
            modified_train = train_df.copy()
            modified_val = val_df.copy()
            
            for strategy in strategies:
                try:
                    print(f"\n  应用策略: {strategy.name}...")
                    modified_train, modified_val, current_config = strategy.apply(
                        modified_train, modified_val, current_config
                    )
                except Exception as e:
                    logger.warning(f"策略 {strategy.name} 应用失败: {e}")
                    continue
            
            # 3. 训练模型
            print(f"\n  训练模型...")
            try:
                result = self._train_and_evaluate(
                    modified_train, modified_val, test_df, 
                    current_config, iteration
                )
            except Exception as e:
                logger.error(f"训练失败: {e}")
                continue
            
            # 4. 计算改进
            improvement = result.val_auc - self.best_auc
            result.improvement = improvement
            result.duration_seconds = (datetime.now() - start_time).total_seconds()
            result.timestamp = datetime.now().isoformat()
            
            # 5. 记录结果
            self.iteration_history.append(result)
            
            # 6. 打印结果
            print(f"\n  结果:")
            print(f"    训练 AUC: {result.train_auc:.4f}")
            print(f"    验证 AUC: {result.val_auc:.4f} ({improvement:+.4f})")
            if result.test_auc > 0:
                print(f"    测试 AUC: {result.test_auc:.4f}")
            print(f"    耗时: {result.duration_seconds:.1f}秒")
            
            # 7. 检查是否达到目标
            if result.val_auc >= self.config.target_auc:
                print(f"\n✅ 达到目标! AUC = {result.val_auc:.4f} >= {self.config.target_auc}")
                
                self.best_auc = result.val_auc
                self.best_config = current_config
                self.best_iteration = iteration
                
                # 保存最佳模型
                model_path = self._save_best_model(current_config, iteration)
                
                return EvolutionResult(
                    success=True,
                    total_iterations=iteration,
                    best_auc=result.val_auc,
                    best_iteration=iteration,
                    best_config=self._serialize_config(current_config),
                    best_model_path=model_path,
                    history=self.iteration_history,
                    reason='target_reached',
                )
            
            # 8. 更新最佳模型
            if result.val_auc > self.best_auc:
                self.best_auc = result.val_auc
                self.best_config = current_config.copy()
                self.best_iteration = iteration
                self.best_model = current_config.get('model')
                no_improve_count = 0
                print(f"  🎯 新最佳! AUC = {result.val_auc:.4f}")
            else:
                no_improve_count += 1
                print(f"  无改进 ({no_improve_count}/{self.config.patience})")
            
            # 9. 早停检查
            if no_improve_count >= self.config.patience:
                print(f"\n⚠️ 早停触发: 连续 {self.config.patience} 次无改进")
                
                model_path = self._save_best_model(self.best_config, self.best_iteration)
                
                return EvolutionResult(
                    success=False,
                    total_iterations=iteration,
                    best_auc=self.best_auc,
                    best_iteration=self.best_iteration,
                    best_config=self._serialize_config(self.best_config),
                    best_model_path=model_path,
                    history=self.iteration_history,
                    reason='patience_exceeded',
                )
        
        # 达到最大迭代
        print(f"\n⚠️ 达到最大迭代次数: {self.config.max_iterations}")
        
        model_path = self._save_best_model(self.best_config, self.best_iteration)
        
        return EvolutionResult(
            success=False,
            total_iterations=iteration,
            best_auc=self.best_auc,
            best_iteration=self.best_iteration,
            best_config=self._serialize_config(self.best_config),
            best_model_path=model_path,
            history=self.iteration_history,
            reason='max_iterations',
        )
    
    def _train_and_evaluate(self,
                            train_df: pd.DataFrame,
                            val_df: pd.DataFrame,
                            test_df: pd.DataFrame,
                            config: Dict,
                            iteration: int) -> IterationResult:
        """训练并评估模型"""
        
        # 获取模型参数
        model_params = config.get('model_params', None)
        selected_features = config.get('selected_features', None)
        
        # 使用集成方法
        if config.get('ensemble', False):
            return self._train_ensemble(train_df, val_df, test_df, config, iteration)
        
        # 创建预测器
        predictor = XGBoostPredictor(
            model_path=str(self.output_dir / f"model_iter_{iteration}.pkl"),
            model_params=model_params,
            use_regularization=True,
            verbose=False
        )
        
        # 如果有选定的特征，更新
        if selected_features:
            predictor.FEATURE_COLUMNS = selected_features
        
        # 训练
        predictor.train(train_df, val_df, early_stopping_rounds=20)
        
        # 获取指标
        train_metrics = predictor.train_metrics
        val_metrics = predictor.val_metrics or predictor.metrics
        
        # 测试集评估
        test_auc = 0.0
        if test_df is not None and len(test_df) > 0:
            test_metrics = predictor.evaluate(test_df, 'label')
            test_auc = test_metrics.auc
        
        # 保存模型到配置
        config['model'] = predictor
        
        # 创建策略名称
        strategy_name = f"phase_{self._get_phase(iteration)}"
        
        return IterationResult(
            iteration=iteration,
            strategy_name=strategy_name,
            strategy_config=self._serialize_config(config),
            train_auc=train_metrics.auc if train_metrics else 0.0,
            val_auc=val_metrics.auc if val_metrics else 0.0,
            test_auc=test_auc,
            train_precision=train_metrics.precision if train_metrics else 0.0,
            val_precision=val_metrics.precision if val_metrics else 0.0,
            train_f1=train_metrics.f1 if train_metrics else 0.0,
            val_f1=val_metrics.f1 if val_metrics else 0.0,
            model_path=str(self.output_dir / f"model_iter_{iteration}.pkl"),
        )
    
    def _train_ensemble(self,
                        train_df: pd.DataFrame,
                        val_df: pd.DataFrame,
                        test_df: pd.DataFrame,
                        config: Dict,
                        iteration: int) -> IterationResult:
        """训练集成模型"""
        from .ensemble_predictor import EnsemblePredictor
        
        n_models = config.get('n_models', 3)
        ensemble = EnsemblePredictor(n_models=n_models)
        
        # 训练集成
        ensemble.train(train_df, val_df)
        
        # 评估
        val_metrics = ensemble.evaluate(val_df)
        train_metrics = ensemble.evaluate(train_df)
        
        test_auc = 0.0
        if test_df is not None and len(test_df) > 0:
            test_metrics = ensemble.evaluate(test_df)
            test_auc = test_metrics.get('auc', 0)
        
        config['model'] = ensemble
        
        return IterationResult(
            iteration=iteration,
            strategy_name="ensemble",
            strategy_config={'n_models': n_models},
            train_auc=train_metrics.get('auc', 0),
            val_auc=val_metrics.get('auc', 0),
            test_auc=test_auc,
            train_precision=train_metrics.get('precision', 0),
            val_precision=val_metrics.get('precision', 0),
            train_f1=train_metrics.get('f1', 0),
            val_f1=val_metrics.get('f1', 0),
            model_path=str(self.output_dir / f"ensemble_iter_{iteration}.pkl"),
        )
    
    def _save_best_model(self, config: Dict, iteration: int) -> str:
        """保存最佳模型"""
        model = config.get('model')
        if model is None:
            return ""
        
        model_path = str(self.output_dir / f"best_model_iter_{iteration}.pkl")
        
        try:
            if hasattr(model, 'save'):
                model.save(model_path)
            else:
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
            
            print(f"最佳模型已保存: {model_path}")
        except Exception as e:
            logger.error(f"保存模型失败: {e}")
            return ""
        
        return model_path
    
    def _serialize_config(self, config: Dict) -> Dict:
        """序列化配置（移除不可序列化对象）"""
        serializable = {}
        
        for key, value in config.items():
            if key in ['model', 'feature_pipeline']:
                continue
            
            if isinstance(value, (str, int, float, bool, list, dict)):
                serializable[key] = value
            elif hasattr(value, 'to_dict'):
                serializable[key] = value.to_dict()
            else:
                serializable[key] = str(value)
        
        return serializable
    
    def save_report(self, result: EvolutionResult, path: str = None):
        """保存进化报告"""
        path = path or str(self.output_dir / f"evolution_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        report = result.to_dict()
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"进化报告已保存: {path}")
        
        return path
    
    def get_progress_summary(self) -> str:
        """获取进度摘要"""
        if not self.iteration_history:
            return "无进化历史"
        
        lines = [
            f"总迭代: {len(self.iteration_history)}",
            f"最佳AUC: {self.best_auc:.4f} (迭代 {self.best_iteration})",
            f"目标AUC: {self.config.target_auc}",
            f"差距: {self.config.target_auc - self.best_auc:+.4f}",
        ]
        
        return "\n".join(lines)


# ============================================================
# 便捷函数
# ============================================================

def evolve_model(train_df: pd.DataFrame,
                 val_df: pd.DataFrame,
                 test_df: pd.DataFrame = None,
                 target_auc: float = 0.70,
                 max_iterations: int = 20) -> EvolutionResult:
    """便捷函数：执行模型进化"""
    config = EvolutionConfig(
        target_auc=target_auc,
        max_iterations=max_iterations
    )
    
    evolver = ModelEvolver(config)
    result = evolver.evolve(train_df, val_df, test_df)
    evolver.save_report(result)
    
    return result


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试模型进化器...")
    
    # 创建模拟数据
    np.random.seed(42)
    n_samples = 1000
    
    df = pd.DataFrame({
        'code': [f'stock_{i}' for i in range(n_samples)],
        'prediction_date': pd.date_range('2024-01-01', periods=n_samples, freq='D').strftime('%Y-%m-%d').tolist(),
        'market_cap': np.random.uniform(10, 1000, n_samples),
        'roe': np.random.uniform(-10, 30, n_samples),
        'growth': np.random.uniform(-20, 50, n_samples),
        'momentum_5d': np.random.uniform(-10, 20, n_samples),
        'momentum_10d': np.random.uniform(-15, 25, n_samples),
        'momentum_20d': np.random.uniform(-20, 30, n_samples),
        'rel_strength': np.random.uniform(0, 100, n_samples),
        'rsi': np.random.uniform(20, 80, n_samples),
        'volume_ratio': np.random.uniform(0.5, 3, n_samples),
        'fin_change': np.random.uniform(-10, 20, n_samples),
        'turnover_rate': np.random.uniform(1, 20, n_samples),
        'on_billboard': np.random.randint(0, 2, n_samples),
        'concept_count': np.random.randint(0, 10, n_samples),
        'market_trend': np.random.uniform(-5, 5, n_samples),
        'label': np.random.randint(0, 2, n_samples),
    })
    
    # 划分数据
    train_df = df.iloc[:700]
    val_df = df.iloc[700:850]
    test_df = df.iloc[850:]
    
    print(f"训练集: {len(train_df)} | 验证集: {len(val_df)} | 测试集: {len(test_df)}")
    
    # 测试进化器（简化版）
    config = EvolutionConfig(
        target_auc=0.60,  # 降低目标以测试
        max_iterations=3,
        patience=2
    )
    
    evolver = ModelEvolver(config, verbose=True)
    
    print("\n开始进化测试...")
    # result = evolver.evolve(train_df, val_df, test_df)
    
    print("\n测试完成!")
