"""
参数优化器 - 使用遗传算法优化策略参数

优化目标：
- 最大化夏普比率
- 最大化10%+命中率
- 最小化最大回撤

优化参数：
- 模型预测阈值
- 止盈止损参数
- 因子权重
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from tqdm import tqdm
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict
    best_fitness: float
    best_metrics: Dict
    history: List[Dict]
    generation_best: List[float]


@dataclass
class ParamSpace:
    """参数空间"""
    name: str
    min_val: float
    max_val: float
    step: float = 0.01
    param_type: str = "float"  # float/int


class ParamOptimizer:
    """参数优化器"""
    
    # 默认参数空间
    DEFAULT_PARAM_SPACE = [
        ParamSpace("min_probability", 0.3, 0.8, 0.05),
        ParamSpace("min_score", 50, 80, 5),
        ParamSpace("target_return", 0.05, 0.15, 0.01),
        ParamSpace("stop_loss", -0.10, -0.03, 0.01),
        ParamSpace("trailing_stop", 0.02, 0.05, 0.01),
        ParamSpace("max_holding_days", 3, 10, 1, "int"),
        ParamSpace("position_size", 0.05, 0.15, 0.01),
    ]
    
    def __init__(self,
                 param_space: List[ParamSpace] = None,
                 population_size: int = 20,
                 generations: int = 10,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7,
                 elite_ratio: float = 0.1,
                 verbose: bool = True):
        """
        Args:
            param_space: 参数空间定义
            population_size: 种群大小
            generations: 迭代代数
            mutation_rate: 变异率
            crossover_rate: 交叉率
            elite_ratio: 精英比例
            verbose: 是否打印详细信息
        """
        self.param_space = param_space or self.DEFAULT_PARAM_SPACE
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elite_ratio = elite_ratio
        self.verbose = verbose
        
        self.population = []
        self.fitness_history = []
        self.best_individual = None
        self.best_fitness = float('-inf')
    
    def _create_individual(self) -> Dict:
        """创建随机个体"""
        individual = {}
        for param in self.param_space:
            if param.param_type == "int":
                individual[param.name] = np.random.randint(int(param.min_val), int(param.max_val) + 1)
            else:
                individual[param.name] = np.random.uniform(param.min_val, param.max_val)
        return individual
    
    def _mutate(self, individual: Dict) -> Dict:
        """变异操作"""
        mutated = individual.copy()
        for param in self.param_space:
            if np.random.random() < self.mutation_rate:
                if param.param_type == "int":
                    mutated[param.name] = np.random.randint(int(param.min_val), int(param.max_val) + 1)
                else:
                    # 高斯变异
                    sigma = (param.max_val - param.min_val) * 0.2
                    new_val = mutated[param.name] + np.random.normal(0, sigma)
                    mutated[param.name] = np.clip(new_val, param.min_val, param.max_val)
        return mutated
    
    def _crossover(self, parent1: Dict, parent2: Dict) -> Tuple[Dict, Dict]:
        """交叉操作"""
        if np.random.random() > self.crossover_rate:
            return parent1.copy(), parent2.copy()
        
        child1, child2 = {}, {}
        for param in self.param_space:
            if np.random.random() < 0.5:
                child1[param.name] = parent1[param.name]
                child2[param.name] = parent2[param.name]
            else:
                child1[param.name] = parent2[param.name]
                child2[param.name] = parent1[param.name]
        
        return child1, child2
    
    def _selection(self, population: List[Dict], fitness_scores: List[float]) -> List[Dict]:
        """选择操作（轮盘赌）"""
        # 归一化适应度
        min_fitness = min(fitness_scores)
        shifted_fitness = [f - min_fitness + 1e-6 for f in fitness_scores]
        total = sum(shifted_fitness)
        probabilities = [f / total for f in shifted_fitness]
        
        # 选择
        selected_indices = np.random.choice(
            len(population),
            size=len(population),
            replace=True,
            p=probabilities
        )
        
        return [population[i].copy() for i in selected_indices]
    
    def _calculate_fitness(self, 
                           individual: Dict,
                           fitness_func: Callable,
                           optimization_mode: str = "sharpe") -> Tuple[float, Dict]:
        """计算适应度
        
        Args:
            individual: 参数个体
            fitness_func: 适应度函数，接收参数字典，返回(fitness, metrics)
            optimization_mode: 优化模式 (sharpe/hit_rate/balanced)
        """
        try:
            fitness, metrics = fitness_func(individual)
            
            # 根据优化模式调整适应度
            if optimization_mode == "sharpe":
                final_fitness = metrics.get('sharpe_ratio', 0)
            elif optimization_mode == "hit_rate":
                final_fitness = metrics.get('hit_10pct_rate', 0)
            elif optimization_mode == "balanced":
                # 多目标加权
                sharpe = metrics.get('sharpe_ratio', 0)
                hit_rate = metrics.get('hit_10pct_rate', 0)
                drawdown = metrics.get('max_drawdown', 1)
                
                # 归一化并加权
                final_fitness = (
                    0.4 * max(sharpe, 0) +
                    0.3 * hit_rate * 100 +
                    0.3 * (1 - drawdown) * 100
                ) / 100
            else:
                final_fitness = fitness
            
            return final_fitness, metrics
            
        except Exception as e:
            logger.warning(f"适应度计算失败: {e}")
            return float('-inf'), {}
    
    def optimize(self,
                 fitness_func: Callable,
                 optimization_mode: str = "balanced") -> OptimizationResult:
        """执行优化
        
        Args:
            fitness_func: 适应度函数，接收参数字典，返回(fitness, metrics)
            optimization_mode: 优化模式
        """
        print(f"\n{'='*60}")
        print(f"【参数优化】")
        print(f"种群大小: {self.population_size}")
        print(f"迭代代数: {self.generations}")
        print(f"优化模式: {optimization_mode}")
        print(f"{'='*60}\n")
        
        # 初始化种群
        self.population = [self._create_individual() for _ in range(self.population_size)]
        
        elite_count = max(1, int(self.population_size * self.elite_ratio))
        history = []
        generation_best = []
        
        for gen in tqdm(range(self.generations), desc="优化进度", ncols=80):
            # 评估适应度
            fitness_results = []
            for ind in self.population:
                fitness, metrics = self._calculate_fitness(ind, fitness_func, optimization_mode)
                fitness_results.append((fitness, metrics))
            
            fitness_scores = [f[0] for f in fitness_results]
            
            # 记录最佳
            gen_best_idx = np.argmax(fitness_scores)
            gen_best_fitness = fitness_scores[gen_best_idx]
            gen_best_params = self.population[gen_best_idx]
            gen_best_metrics = fitness_results[gen_best_idx][1]
            
            generation_best.append(gen_best_fitness)
            
            if gen_best_fitness > self.best_fitness:
                self.best_fitness = gen_best_fitness
                self.best_individual = gen_best_params.copy()
                self.best_metrics = gen_best_metrics.copy()
            
            # 记录历史
            history.append({
                'generation': gen,
                'best_fitness': gen_best_fitness,
                'avg_fitness': np.mean(fitness_scores),
                'best_params': gen_best_params,
            })
            
            if self.verbose:
                tqdm.write(f"  Gen {gen+1}: Best={gen_best_fitness:.4f}, Avg={np.mean(fitness_scores):.4f}")
            
            # 精英保留
            sorted_indices = np.argsort(fitness_scores)[::-1]
            elites = [self.population[i].copy() for i in sorted_indices[:elite_count]]
            
            # 选择
            selected = self._selection(self.population, fitness_scores)
            
            # 交叉和变异
            new_population = elites.copy()
            
            while len(new_population) < self.population_size:
                idx1, idx2 = np.random.choice(len(selected), 2, replace=False)
                child1, child2 = self._crossover(selected[idx1], selected[idx2])
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                new_population.extend([child1, child2])
            
            self.population = new_population[:self.population_size]
        
        # 最终结果
        result = OptimizationResult(
            best_params=self.best_individual,
            best_fitness=self.best_fitness,
            best_metrics=self.best_metrics if hasattr(self, 'best_metrics') else {},
            history=history,
            generation_best=generation_best,
        )
        
        self._print_result(result)
        
        return result
    
    def _print_result(self, result: OptimizationResult):
        """打印优化结果"""
        print(f"\n{'='*60}")
        print(f"【优化结果】")
        print(f"{'='*60}")
        print(f"最佳适应度: {result.best_fitness:.4f}")
        print(f"\n最佳参数:")
        for name, value in result.best_params.items():
            if isinstance(value, float):
                print(f"  {name}: {value:.4f}")
            else:
                print(f"  {name}: {value}")
        
        if result.best_metrics:
            print(f"\n最佳指标:")
            for name, value in result.best_metrics.items():
                if isinstance(value, float):
                    print(f"  {name}: {value:.4f}")
                else:
                    print(f"  {name}: {value}")
        
        print(f"{'='*60}")
    
    def save_result(self, result: OptimizationResult, path: str):
        """保存优化结果"""
        data = {
            'best_params': result.best_params,
            'best_fitness': result.best_fitness,
            'best_metrics': result.best_metrics,
            'generation_best': result.generation_best,
        }
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"优化结果已保存: {path}")


class GridSearchOptimizer:
    """网格搜索优化器（简单但全面）"""
    
    def __init__(self, param_grid: Dict, verbose: bool = True):
        """
        Args:
            param_grid: 参数网格 {param_name: [values]}
        """
        self.param_grid = param_grid
        self.verbose = verbose
    
    def search(self, fitness_func: Callable) -> OptimizationResult:
        """执行网格搜索"""
        from itertools import product
        
        param_names = list(self.param_grid.keys())
        param_values = list(self.param_grid.values())
        
        combinations = list(product(*param_values))
        print(f"网格搜索: {len(combinations)} 种组合")
        
        best_params = None
        best_fitness = float('-inf')
        best_metrics = {}
        history = []
        
        for combo in tqdm(combinations, desc="网格搜索", ncols=80):
            params = dict(zip(param_names, combo))
            
            try:
                fitness, metrics = fitness_func(params)
                
                history.append({
                    'params': params,
                    'fitness': fitness,
                    'metrics': metrics,
                })
                
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_params = params.copy()
                    best_metrics = metrics.copy()
                    
                    if self.verbose:
                        tqdm.write(f"  新最佳: {fitness:.4f}")
                        
            except Exception as e:
                logger.warning(f"评估失败: {e}")
        
        return OptimizationResult(
            best_params=best_params,
            best_fitness=best_fitness,
            best_metrics=best_metrics,
            history=history,
            generation_best=[],
        )


def main():
    """测试参数优化器"""
    # 定义测试适应度函数
    def test_fitness(params):
        """模拟适应度函数"""
        # 模拟收益随参数变化
        sharpe = (
            0.5 * params.get('min_probability', 0.5) +
            0.3 * (1 - abs(params.get('target_return', 0.1) - 0.08)) +
            0.2 * (1 + params.get('stop_loss', -0.05))
        )
        
        sharpe += np.random.normal(0, 0.1)  # 添加噪声
        
        metrics = {
            'sharpe_ratio': sharpe,
            'hit_10pct_rate': 0.15 + params.get('min_probability', 0.5) * 0.1,
            'max_drawdown': 0.1 - params.get('stop_loss', -0.05) * 0.5,
        }
        
        return sharpe, metrics
    
    # 遗传算法优化
    optimizer = ParamOptimizer(
        population_size=10,
        generations=5,
        verbose=True
    )
    
    result = optimizer.optimize(test_fitness, optimization_mode="balanced")
    
    print(f"\n最佳参数: {result.best_params}")
    print(f"最佳适应度: {result.best_fitness:.4f}")


if __name__ == '__main__':
    main()
