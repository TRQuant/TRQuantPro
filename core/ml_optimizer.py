"""
机器学习参数优化器

支持多种优化方法：
1. 网格搜索 + 贝叶斯优化 (Optuna)
2. 遗传算法
3. 集成学习特征重要性
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """优化结果"""
    method: str
    best_params: Dict
    best_score: float
    all_trials: List[Dict] = field(default_factory=list)
    optimization_time: float = 0.0
    
    def to_dict(self) -> dict:
        return {
            'method': self.method,
            'best_params': self.best_params,
            'best_score': round(self.best_score, 4),
            'n_trials': len(self.all_trials),
            'optimization_time': round(self.optimization_time, 2)
        }


@dataclass
class WalkForwardResult:
    """Walk-Forward验证结果"""
    periods: List[Dict]
    overall_accuracy: float
    overall_sharpe: float
    best_params_per_period: List[Dict]
    
    def to_dict(self) -> dict:
        return {
            'periods': self.periods,
            'overall_accuracy': round(self.overall_accuracy, 4),
            'overall_sharpe': round(self.overall_sharpe, 4),
            'n_periods': len(self.periods),
            'best_params_per_period': self.best_params_per_period
        }


class GridSearchOptimizer:
    """网格搜索优化器"""
    
    def __init__(self, param_grid: Dict[str, List]):
        """
        初始化
        
        Args:
            param_grid: 参数网格，如 {'momentum_thresh': [3, 5, 8], 'ma_period': [20, 60]}
        """
        self.param_grid = param_grid
    
    def optimize(self, 
                 objective_func: Callable[[Dict], float],
                 maximize: bool = True) -> OptimizationResult:
        """
        执行网格搜索
        
        Args:
            objective_func: 目标函数，接收参数字典，返回得分
            maximize: 是否最大化目标
            
        Returns:
            OptimizationResult
        """
        import itertools
        import time
        
        start_time = time.time()
        
        # 生成所有参数组合
        keys = list(self.param_grid.keys())
        values = list(self.param_grid.values())
        combinations = list(itertools.product(*values))
        
        all_trials = []
        best_score = -np.inf if maximize else np.inf
        best_params = None
        
        for combo in combinations:
            params = dict(zip(keys, combo))
            
            try:
                score = objective_func(params)
                all_trials.append({'params': params, 'score': score})
                
                if (maximize and score > best_score) or (not maximize and score < best_score):
                    best_score = score
                    best_params = params
                    
            except Exception as e:
                logger.warning(f"参数 {params} 评估失败: {e}")
                continue
        
        elapsed = time.time() - start_time
        
        return OptimizationResult(
            method='grid_search',
            best_params=best_params or {},
            best_score=best_score,
            all_trials=all_trials,
            optimization_time=elapsed
        )


class BayesianOptimizer:
    """贝叶斯优化器 (使用Optuna)"""
    
    def __init__(self, param_space: Dict[str, Tuple]):
        """
        初始化
        
        Args:
            param_space: 参数空间，如 
                {'momentum_thresh': (1.0, 10.0, 'float'), 
                 'ma_period': (10, 100, 'int')}
        """
        self.param_space = param_space
    
    def optimize(self,
                 objective_func: Callable[[Dict], float],
                 n_trials: int = 100,
                 maximize: bool = True) -> OptimizationResult:
        """
        执行贝叶斯优化
        """
        import time
        
        start_time = time.time()
        
        try:
            import optuna
            optuna.logging.set_verbosity(optuna.logging.WARNING)
        except ImportError:
            logger.warning("Optuna未安装，回退到网格搜索")
            # 回退到简化的随机搜索
            return self._random_search(objective_func, n_trials, maximize)
        
        all_trials = []
        
        def optuna_objective(trial):
            params = {}
            for name, (low, high, dtype) in self.param_space.items():
                if dtype == 'int':
                    params[name] = trial.suggest_int(name, int(low), int(high))
                elif dtype == 'float':
                    params[name] = trial.suggest_float(name, low, high)
                elif dtype == 'categorical':
                    params[name] = trial.suggest_categorical(name, low)  # low是选项列表
            
            score = objective_func(params)
            all_trials.append({'params': params, 'score': score})
            return score
        
        direction = 'maximize' if maximize else 'minimize'
        study = optuna.create_study(direction=direction)
        study.optimize(optuna_objective, n_trials=n_trials, show_progress_bar=False)
        
        elapsed = time.time() - start_time
        
        return OptimizationResult(
            method='bayesian_optuna',
            best_params=study.best_params,
            best_score=study.best_value,
            all_trials=all_trials,
            optimization_time=elapsed
        )
    
    def _random_search(self, objective_func, n_trials, maximize):
        """回退的随机搜索"""
        import time
        start_time = time.time()
        
        all_trials = []
        best_score = -np.inf if maximize else np.inf
        best_params = None
        
        for _ in range(n_trials):
            params = {}
            for name, (low, high, dtype) in self.param_space.items():
                if dtype == 'int':
                    params[name] = np.random.randint(int(low), int(high) + 1)
                elif dtype == 'float':
                    params[name] = np.random.uniform(low, high)
                elif dtype == 'categorical':
                    params[name] = np.random.choice(low)
            
            try:
                score = objective_func(params)
                all_trials.append({'params': params, 'score': score})
                
                if (maximize and score > best_score) or (not maximize and score < best_score):
                    best_score = score
                    best_params = params
            except:
                continue
        
        elapsed = time.time() - start_time
        
        return OptimizationResult(
            method='random_search',
            best_params=best_params or {},
            best_score=best_score,
            all_trials=all_trials,
            optimization_time=elapsed
        )


class GeneticOptimizer:
    """遗传算法优化器"""
    
    def __init__(self, param_space: Dict[str, Tuple]):
        """
        初始化
        
        Args:
            param_space: 参数空间
        """
        self.param_space = param_space
    
    def optimize(self,
                 objective_func: Callable[[Dict], float],
                 population_size: int = 50,
                 generations: int = 30,
                 maximize: bool = True) -> OptimizationResult:
        """
        执行遗传算法优化
        """
        import time
        start_time = time.time()
        
        all_trials = []
        
        # 初始化种群
        population = self._init_population(population_size)
        
        # 评估初始种群
        fitness = []
        for individual in population:
            params = self._decode_individual(individual)
            try:
                score = objective_func(params)
                all_trials.append({'params': params, 'score': score})
                fitness.append(score if maximize else -score)
            except:
                fitness.append(-np.inf)
        
        best_score = max(fitness) if maximize else -max(fitness)
        best_idx = fitness.index(max(fitness))
        best_params = self._decode_individual(population[best_idx])
        
        # 进化
        for gen in range(generations):
            # 选择
            parents = self._selection(population, fitness)
            
            # 交叉
            offspring = self._crossover(parents)
            
            # 变异
            offspring = self._mutation(offspring)
            
            # 评估新个体
            new_fitness = []
            for individual in offspring:
                params = self._decode_individual(individual)
                try:
                    score = objective_func(params)
                    all_trials.append({'params': params, 'score': score})
                    new_fitness.append(score if maximize else -score)
                except:
                    new_fitness.append(-np.inf)
            
            # 合并并选择最优
            all_individuals = population + offspring
            all_fitness = fitness + new_fitness
            
            # 精英选择
            sorted_idx = np.argsort(all_fitness)[::-1]
            population = [all_individuals[i] for i in sorted_idx[:population_size]]
            fitness = [all_fitness[i] for i in sorted_idx[:population_size]]
            
            # 更新最优
            if fitness[0] > (best_score if maximize else -best_score):
                best_score = fitness[0] if maximize else -fitness[0]
                best_params = self._decode_individual(population[0])
        
        elapsed = time.time() - start_time
        
        return OptimizationResult(
            method='genetic_algorithm',
            best_params=best_params,
            best_score=best_score,
            all_trials=all_trials,
            optimization_time=elapsed
        )
    
    def _init_population(self, size: int) -> List[List[float]]:
        """初始化种群"""
        population = []
        for _ in range(size):
            individual = []
            for name, (low, high, dtype) in self.param_space.items():
                if dtype == 'categorical':
                    individual.append(np.random.randint(0, len(low)))
                else:
                    individual.append(np.random.uniform(0, 1))
            population.append(individual)
        return population
    
    def _decode_individual(self, individual: List[float]) -> Dict:
        """解码个体为参数"""
        params = {}
        for i, (name, (low, high, dtype)) in enumerate(self.param_space.items()):
            gene = individual[i]
            if dtype == 'int':
                params[name] = int(low + gene * (high - low))
            elif dtype == 'float':
                params[name] = low + gene * (high - low)
            elif dtype == 'categorical':
                params[name] = low[int(gene) % len(low)]
        return params
    
    def _selection(self, population: List, fitness: List) -> List:
        """锦标赛选择"""
        selected = []
        for _ in range(len(population)):
            # 随机选择3个进行锦标赛
            candidates = np.random.choice(len(population), 3, replace=False)
            winner = candidates[np.argmax([fitness[i] for i in candidates])]
            selected.append(population[winner].copy())
        return selected
    
    def _crossover(self, parents: List, rate: float = 0.8) -> List:
        """均匀交叉"""
        offspring = []
        for i in range(0, len(parents) - 1, 2):
            p1, p2 = parents[i], parents[i + 1]
            if np.random.random() < rate:
                child1, child2 = p1.copy(), p2.copy()
                for j in range(len(p1)):
                    if np.random.random() < 0.5:
                        child1[j], child2[j] = child2[j], child1[j]
                offspring.extend([child1, child2])
            else:
                offspring.extend([p1.copy(), p2.copy()])
        return offspring
    
    def _mutation(self, offspring: List, rate: float = 0.1) -> List:
        """变异"""
        for individual in offspring:
            for i in range(len(individual)):
                if np.random.random() < rate:
                    individual[i] = np.random.uniform(0, 1)
        return offspring


class WalkForwardOptimizer:
    """Walk-Forward滚动前进验证优化器"""
    
    def __init__(self, 
                 train_window: int = 504,  # 2年
                 test_window: int = 252,   # 1年
                 step: int = 252):         # 每次前进1年
        """
        初始化
        
        Args:
            train_window: 训练窗口大小（交易日）
            test_window: 测试窗口大小
            step: 滚动步长
        """
        self.train_window = train_window
        self.test_window = test_window
        self.step = step
    
    def validate(self,
                 df: pd.DataFrame,
                 optimizer: Any,
                 objective_func: Callable[[Dict, pd.DataFrame], float],
                 evaluate_func: Callable[[Dict, pd.DataFrame], Dict]) -> WalkForwardResult:
        """
        执行Walk-Forward验证
        
        Args:
            df: 完整数据
            optimizer: 优化器实例
            objective_func: 目标函数（参数，训练数据）-> 得分
            evaluate_func: 评估函数（参数，测试数据）-> 结果字典
            
        Returns:
            WalkForwardResult
        """
        periods = []
        best_params_per_period = []
        
        n_samples = len(df)
        start_idx = 0
        
        while start_idx + self.train_window + self.test_window <= n_samples:
            # 划分训练集和测试集
            train_end = start_idx + self.train_window
            test_end = train_end + self.test_window
            
            train_df = df.iloc[start_idx:train_end]
            test_df = df.iloc[train_end:test_end]
            
            train_start_date = train_df.index[0] if hasattr(train_df.index[0], 'strftime') else train_df.index[0]
            train_end_date = train_df.index[-1] if hasattr(train_df.index[-1], 'strftime') else train_df.index[-1]
            test_start_date = test_df.index[0] if hasattr(test_df.index[0], 'strftime') else test_df.index[0]
            test_end_date = test_df.index[-1] if hasattr(test_df.index[-1], 'strftime') else test_df.index[-1]
            
            # 在训练集上优化参数
            def train_objective(params):
                return objective_func(params, train_df)
            
            opt_result = optimizer.optimize(train_objective)
            best_params = opt_result.best_params
            best_params_per_period.append(best_params)
            
            # 在测试集上评估
            test_result = evaluate_func(best_params, test_df)
            
            periods.append({
                'train_period': f"{train_start_date} - {train_end_date}",
                'test_period': f"{test_start_date} - {test_end_date}",
                'best_params': best_params,
                'train_score': opt_result.best_score,
                'test_result': test_result
            })
            
            # 前进
            start_idx += self.step
        
        # 计算总体指标
        accuracies = [p['test_result'].get('accuracy', 0) for p in periods]
        sharpes = [p['test_result'].get('sharpe', 0) for p in periods]
        
        return WalkForwardResult(
            periods=periods,
            overall_accuracy=np.mean(accuracies) if accuracies else 0,
            overall_sharpe=np.mean(sharpes) if sharpes else 0,
            best_params_per_period=best_params_per_period
        )


class EnsembleFeatureImportance:
    """集成学习特征重要性分析"""
    
    def analyze(self, 
                X: pd.DataFrame, 
                y: pd.Series,
                method: str = 'xgboost') -> Dict[str, float]:
        """
        分析特征重要性
        
        Args:
            X: 特征数据
            y: 目标变量
            method: 方法 ('xgboost', 'random_forest', 'both')
            
        Returns:
            特征重要性字典
        """
        importances = {}
        
        if method in ['xgboost', 'both']:
            try:
                import xgboost as xgb
                model = xgb.XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
                model.fit(X, y)
                for i, col in enumerate(X.columns):
                    importances[f'{col}_xgb'] = model.feature_importances_[i]
            except ImportError:
                logger.warning("XGBoost未安装")
        
        if method in ['random_forest', 'both']:
            try:
                from sklearn.ensemble import RandomForestClassifier
                model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
                model.fit(X, y)
                for i, col in enumerate(X.columns):
                    importances[f'{col}_rf'] = model.feature_importances_[i]
            except ImportError:
                logger.warning("Sklearn未安装")
        
        # 如果使用both，计算平均
        if method == 'both':
            combined = {}
            for col in X.columns:
                xgb_imp = importances.get(f'{col}_xgb', 0)
                rf_imp = importances.get(f'{col}_rf', 0)
                combined[col] = (xgb_imp + rf_imp) / 2
            return combined
        
        return importances


class MultiMethodOptimizer:
    """多方法对比优化器"""
    
    def __init__(self, param_space: Dict[str, Tuple]):
        """
        初始化
        
        Args:
            param_space: 参数空间
        """
        self.param_space = param_space
        
        # 转换为网格格式（用于网格搜索）
        self.param_grid = {}
        for name, (low, high, dtype) in param_space.items():
            if dtype == 'int':
                self.param_grid[name] = list(range(int(low), int(high) + 1, max(1, (int(high) - int(low)) // 5)))
            elif dtype == 'float':
                self.param_grid[name] = list(np.linspace(low, high, 5))
            elif dtype == 'categorical':
                self.param_grid[name] = low
    
    def optimize_all(self,
                     objective_func: Callable[[Dict], float],
                     n_trials: int = 50,
                     maximize: bool = True) -> Dict[str, OptimizationResult]:
        """
        使用所有方法优化并对比
        
        Args:
            objective_func: 目标函数
            n_trials: 试验次数
            maximize: 是否最大化
            
        Returns:
            各方法的优化结果
        """
        results = {}
        
        # 1. 网格搜索
        logger.info("执行网格搜索...")
        grid_opt = GridSearchOptimizer(self.param_grid)
        results['grid_search'] = grid_opt.optimize(objective_func, maximize)
        
        # 2. 贝叶斯优化
        logger.info("执行贝叶斯优化...")
        bayes_opt = BayesianOptimizer(self.param_space)
        results['bayesian'] = bayes_opt.optimize(objective_func, n_trials, maximize)
        
        # 3. 遗传算法
        logger.info("执行遗传算法优化...")
        genetic_opt = GeneticOptimizer(self.param_space)
        results['genetic'] = genetic_opt.optimize(
            objective_func, 
            population_size=30, 
            generations=20, 
            maximize=maximize
        )
        
        return results
    
    def get_best_method(self, results: Dict[str, OptimizationResult], maximize: bool = True) -> Tuple[str, OptimizationResult]:
        """获取最佳方法"""
        best_method = None
        best_result = None
        best_score = -np.inf if maximize else np.inf
        
        for method, result in results.items():
            if (maximize and result.best_score > best_score) or \
               (not maximize and result.best_score < best_score):
                best_score = result.best_score
                best_method = method
                best_result = result
        
        return best_method, best_result


# 便捷函数
def optimize_params(param_space: Dict[str, Tuple],
                   objective_func: Callable[[Dict], float],
                   method: str = 'all',
                   n_trials: int = 50) -> Dict:
    """
    参数优化
    
    Args:
        param_space: 参数空间
        objective_func: 目标函数
        method: 优化方法 ('grid', 'bayesian', 'genetic', 'all')
        n_trials: 试验次数
        
    Returns:
        优化结果
    """
    if method == 'all':
        optimizer = MultiMethodOptimizer(param_space)
        results = optimizer.optimize_all(objective_func, n_trials)
        best_method, best_result = optimizer.get_best_method(results)
        return {
            'all_results': {k: v.to_dict() for k, v in results.items()},
            'best_method': best_method,
            'best_params': best_result.best_params,
            'best_score': best_result.best_score
        }
    elif method == 'grid':
        # 转换参数空间为网格
        param_grid = {}
        for name, (low, high, dtype) in param_space.items():
            if dtype == 'int':
                param_grid[name] = list(range(int(low), int(high) + 1, max(1, (int(high) - int(low)) // 5)))
            elif dtype == 'float':
                param_grid[name] = list(np.linspace(low, high, 5))
        optimizer = GridSearchOptimizer(param_grid)
        result = optimizer.optimize(objective_func)
        return result.to_dict()
    elif method == 'bayesian':
        optimizer = BayesianOptimizer(param_space)
        result = optimizer.optimize(objective_func, n_trials)
        return result.to_dict()
    elif method == 'genetic':
        optimizer = GeneticOptimizer(param_space)
        result = optimizer.optimize(objective_func)
        return result.to_dict()
    else:
        raise ValueError(f"未知方法: {method}")

