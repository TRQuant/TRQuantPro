# -*- coding: utf-8 -*-
"""
Optuna策略优化集成
==================

整合Optuna进行专业的策略参数优化，支持：
- 网格搜索
- 随机搜索
- 贝叶斯优化（TPE）
- 多目标优化
- 分布式优化
"""
import logging
import time
from typing import Dict, Any, Optional, List, Callable, Tuple
from dataclasses import dataclass, field
import numpy as np

logger = logging.getLogger(__name__)

# 尝试导入optuna
OPTUNA_AVAILABLE = False
Trial = None  # 类型占位符
try:
    import optuna
    from optuna import Trial
    from optuna.samplers import TPESampler, RandomSampler, GridSampler
    OPTUNA_AVAILABLE = True
    logger.info("✅ Optuna已安装")
except ImportError:
    logger.warning("Optuna未安装，使用内置简化版本")
    # 定义占位类型
    class Trial:
        """Optuna Trial占位类"""
        pass


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, Any]
    best_value: float
    best_trial: int = 0
    all_trials: List[Dict[str, Any]] = field(default_factory=list)
    optimization_time: float = 0.0
    n_trials: int = 0
    convergence_history: List[float] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "best_params": self.best_params,
            "best_value": self.best_value,
            "best_trial": self.best_trial,
            "n_trials": self.n_trials,
            "optimization_time": f"{self.optimization_time:.2f}s",
            "top_5_trials": self.all_trials[:5] if self.all_trials else [],
        }


class OptunaOptimizer:
    """Optuna策略优化器"""
    
    def __init__(
        self,
        direction: str = "maximize",
        sampler: str = "tpe",
        n_jobs: int = 1,
        seed: int = 42,
    ):
        """
        初始化
        
        Args:
            direction: 优化方向 (maximize/minimize)
            sampler: 采样器类型 (tpe/random/grid)
            n_jobs: 并行数
            seed: 随机种子
        """
        self.direction = direction
        self.sampler_type = sampler
        self.n_jobs = n_jobs
        self.seed = seed
        self.use_optuna = OPTUNA_AVAILABLE
    
    def optimize(
        self,
        objective_func: Callable,
        param_space: Dict[str, Any],
        n_trials: int = 100,
        timeout: Optional[float] = None,
        callbacks: Optional[List[Callable]] = None,
    ) -> OptimizationResult:
        """
        执行优化
        
        Args:
            objective_func: 目标函数，接收参数字典，返回目标值
            param_space: 参数空间定义
            n_trials: 试验次数
            timeout: 超时时间（秒）
            callbacks: 回调函数列表
        
        Returns:
            优化结果
        """
        if self.use_optuna:
            return self._optimize_with_optuna(
                objective_func, param_space, n_trials, timeout, callbacks
            )
        else:
            return self._optimize_builtin(
                objective_func, param_space, n_trials, timeout
            )
    
    def _optimize_with_optuna(
        self,
        objective_func: Callable,
        param_space: Dict[str, Any],
        n_trials: int,
        timeout: Optional[float],
        callbacks: Optional[List[Callable]],
    ) -> OptimizationResult:
        """使用Optuna优化"""
        start_time = time.time()
        
        # 创建采样器
        sampler = self._create_sampler()
        
        # 创建study
        study = optuna.create_study(
            direction=self.direction,
            sampler=sampler,
        )
        
        # 定义optuna目标函数
        def optuna_objective(trial: Trial) -> float:
            params = {}
            for name, config in param_space.items():
                params[name] = self._suggest_param(trial, name, config)
            return objective_func(params)
        
        # 运行优化
        study.optimize(
            optuna_objective,
            n_trials=n_trials,
            timeout=timeout,
            n_jobs=self.n_jobs,
            callbacks=callbacks,
            show_progress_bar=False,
        )
        
        # 收集所有试验结果
        all_trials = []
        for trial in study.trials:
            if trial.state == optuna.trial.TrialState.COMPLETE:
                all_trials.append({
                    "trial": trial.number,
                    "params": trial.params,
                    "value": trial.value,
                })
        
        # 按目标值排序
        all_trials.sort(
            key=lambda x: x["value"],
            reverse=(self.direction == "maximize")
        )
        
        # 收集收敛历史
        convergence = []
        best_so_far = float('-inf') if self.direction == "maximize" else float('inf')
        for trial in study.trials:
            if trial.state == optuna.trial.TrialState.COMPLETE:
                if self.direction == "maximize":
                    best_so_far = max(best_so_far, trial.value)
                else:
                    best_so_far = min(best_so_far, trial.value)
                convergence.append(best_so_far)
        
        return OptimizationResult(
            best_params=study.best_params,
            best_value=study.best_value,
            best_trial=study.best_trial.number,
            all_trials=all_trials,
            optimization_time=time.time() - start_time,
            n_trials=len(study.trials),
            convergence_history=convergence,
        )
    
    def _optimize_builtin(
        self,
        objective_func: Callable,
        param_space: Dict[str, Any],
        n_trials: int,
        timeout: Optional[float],
    ) -> OptimizationResult:
        """内置简化优化（网格搜索 + 随机搜索）"""
        start_time = time.time()
        all_trials = []
        convergence = []
        
        best_value = float('-inf') if self.direction == "maximize" else float('inf')
        best_params = {}
        best_trial = 0
        
        # 生成参数组合
        param_combinations = self._generate_combinations(param_space, n_trials)
        
        for i, params in enumerate(param_combinations):
            # 检查超时
            if timeout and (time.time() - start_time) > timeout:
                break
            
            try:
                value = objective_func(params)
                
                all_trials.append({
                    "trial": i,
                    "params": params,
                    "value": value,
                })
                
                # 更新最佳结果
                if self.direction == "maximize":
                    if value > best_value:
                        best_value = value
                        best_params = params.copy()
                        best_trial = i
                    convergence.append(max(best_value, value))
                else:
                    if value < best_value:
                        best_value = value
                        best_params = params.copy()
                        best_trial = i
                    convergence.append(min(best_value, value))
                    
            except Exception as e:
                logger.warning(f"Trial {i} failed: {e}")
        
        # 排序
        all_trials.sort(
            key=lambda x: x["value"],
            reverse=(self.direction == "maximize")
        )
        
        return OptimizationResult(
            best_params=best_params,
            best_value=best_value,
            best_trial=best_trial,
            all_trials=all_trials,
            optimization_time=time.time() - start_time,
            n_trials=len(all_trials),
            convergence_history=convergence,
        )
    
    def _create_sampler(self):
        """创建Optuna采样器"""
        if not OPTUNA_AVAILABLE:
            return None
        
        if self.sampler_type == "tpe":
            return TPESampler(seed=self.seed)
        elif self.sampler_type == "random":
            return RandomSampler(seed=self.seed)
        elif self.sampler_type == "grid":
            return None  # GridSampler需要特殊处理
        else:
            return TPESampler(seed=self.seed)
    
    def _suggest_param(self, trial: Trial, name: str, config: Dict) -> Any:
        """根据配置建议参数值"""
        param_type = config.get("type", "float")
        
        if param_type == "float":
            return trial.suggest_float(
                name,
                config.get("low", 0.0),
                config.get("high", 1.0),
                step=config.get("step"),
                log=config.get("log", False),
            )
        elif param_type == "int":
            return trial.suggest_int(
                name,
                config.get("low", 0),
                config.get("high", 100),
                step=config.get("step", 1),
                log=config.get("log", False),
            )
        elif param_type == "categorical":
            return trial.suggest_categorical(
                name,
                config.get("choices", [])
            )
        else:
            return trial.suggest_float(name, 0.0, 1.0)
    
    def _generate_combinations(
        self,
        param_space: Dict[str, Any],
        max_trials: int
    ) -> List[Dict[str, Any]]:
        """生成参数组合"""
        import itertools
        
        # 构建参数值列表
        param_values = {}
        for name, config in param_space.items():
            param_type = config.get("type", "float")
            
            if param_type == "categorical":
                param_values[name] = config.get("choices", [])
            elif param_type in ["float", "int"]:
                low = config.get("low", 0)
                high = config.get("high", 1)
                step = config.get("step")
                
                if step:
                    if param_type == "int":
                        param_values[name] = list(range(low, high + 1, step))
                    else:
                        param_values[name] = list(np.arange(low, high + step, step))
                else:
                    # 生成均匀分布的点
                    n_points = min(10, max_trials // len(param_space))
                    if param_type == "int":
                        param_values[name] = list(np.linspace(low, high, n_points).astype(int))
                    else:
                        param_values[name] = list(np.linspace(low, high, n_points))
        
        # 生成组合
        keys = list(param_values.keys())
        values = list(param_values.values())
        
        all_combinations = list(itertools.product(*values))
        
        # 如果组合太多，随机采样
        if len(all_combinations) > max_trials:
            np.random.seed(self.seed)
            indices = np.random.choice(len(all_combinations), max_trials, replace=False)
            all_combinations = [all_combinations[i] for i in indices]
        
        return [dict(zip(keys, combo)) for combo in all_combinations]
    
    def optimize_strategy(
        self,
        backtest_func: Callable,
        param_space: Dict[str, Any],
        n_trials: int = 50,
        target_metric: str = "sharpe_ratio",
        constraints: Optional[Dict[str, Tuple[float, float]]] = None,
    ) -> OptimizationResult:
        """
        优化策略参数
        
        Args:
            backtest_func: 回测函数，接收参数字典，返回回测结果
            param_space: 参数空间
            n_trials: 试验次数
            target_metric: 目标指标
            constraints: 约束条件 {指标名: (最小值, 最大值)}
        
        Returns:
            优化结果
        """
        def objective(params: Dict) -> float:
            try:
                result = backtest_func(params)
                
                # 获取目标指标
                value = result.get(target_metric, 0.0)
                
                # 检查约束
                if constraints:
                    for metric, (min_val, max_val) in constraints.items():
                        metric_val = result.get(metric, 0.0)
                        if metric_val < min_val or metric_val > max_val:
                            return float('-inf') if self.direction == "maximize" else float('inf')
                
                return value
                
            except Exception as e:
                logger.warning(f"Backtest failed: {e}")
                return float('-inf') if self.direction == "maximize" else float('inf')
        
        return self.optimize(objective, param_space, n_trials)
