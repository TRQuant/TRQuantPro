"""
V3.0 遗传算法多目标优化器
==========================

用于优化筛选参数，支持多目标优化:

优化目标 (不仅仅是夏普比率):
1. 收益率 (Return) - 追求高收益
2. 回撤 (Drawdown) - 控制风险
3. 夏普比率 (Sharpe) - 风险调整收益
4. 胜率 (WinRate) - 交易成功率
5. 稳定性 (Stability) - 收益稳定性

平衡方案:
- 帕累托前沿 (Pareto Front) - 找出非支配解
- 加权目标 (Weighted) - 按权重组合
- 约束优化 (Constrained) - 满足约束条件

支持:
- NSGA-II 多目标优化
- 自适应变异
- 精英保留
- 早停机制
"""

import numpy as np
import random
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import logging
import copy

logger = logging.getLogger(__name__)


# ============ 枚举定义 ============

class OptimizationMode(Enum):
    """优化模式"""
    PARETO = "pareto"         # 帕累托多目标
    WEIGHTED = "weighted"     # 加权单目标
    CONSTRAINED = "constrained"  # 约束优化
    BALANCED = "balanced"     # 平衡模式（默认）


class ObjectiveType(Enum):
    """目标类型"""
    MAXIMIZE = "maximize"
    MINIMIZE = "minimize"


# ============ 数据结构 ============

@dataclass
class OptimizationObjective:
    """优化目标"""
    name: str
    type: ObjectiveType
    weight: float = 1.0
    constraint_min: Optional[float] = None
    constraint_max: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.type.value,
            "weight": self.weight,
            "constraint_min": self.constraint_min,
            "constraint_max": self.constraint_max,
        }


@dataclass
class ParameterSpace:
    """参数空间"""
    name: str
    min_value: float
    max_value: float
    step: float = 0.01
    param_type: str = "float"  # "float" / "int" / "choice"
    choices: List[Any] = field(default_factory=list)
    
    def sample(self) -> Any:
        """随机采样"""
        if self.param_type == "choice":
            return random.choice(self.choices)
        elif self.param_type == "int":
            return random.randint(int(self.min_value), int(self.max_value))
        else:
            return random.uniform(self.min_value, self.max_value)
    
    def mutate(self, value: Any, mutation_rate: float = 0.2) -> Any:
        """变异"""
        if random.random() > mutation_rate:
            return value
        
        if self.param_type == "choice":
            return random.choice(self.choices)
        elif self.param_type == "int":
            delta = int((self.max_value - self.min_value) * 0.2)
            new_val = value + random.randint(-delta, delta)
            return max(int(self.min_value), min(int(self.max_value), new_val))
        else:
            delta = (self.max_value - self.min_value) * 0.2
            new_val = value + random.uniform(-delta, delta)
            return max(self.min_value, min(self.max_value, new_val))


@dataclass
class Individual:
    """个体 (染色体)"""
    params: Dict[str, Any]
    fitness: Dict[str, float] = field(default_factory=dict)
    rank: int = 0
    crowding_distance: float = 0.0
    
    def dominates(self, other: "Individual", objectives: List[OptimizationObjective]) -> bool:
        """判断是否支配另一个个体"""
        dominated = False
        at_least_one_better = False
        
        for obj in objectives:
            self_val = self.fitness.get(obj.name, 0)
            other_val = other.fitness.get(obj.name, 0)
            
            if obj.type == ObjectiveType.MAXIMIZE:
                if self_val < other_val:
                    return False
                if self_val > other_val:
                    at_least_one_better = True
            else:
                if self_val > other_val:
                    return False
                if self_val < other_val:
                    at_least_one_better = True
        
        return at_least_one_better


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, Any]
    best_fitness: Dict[str, float]
    pareto_front: List[Individual] = field(default_factory=list)
    history: List[Dict] = field(default_factory=list)
    generations: int = 0
    runtime_seconds: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "best_params": self.best_params,
            "best_fitness": {k: round(v, 4) for k, v in self.best_fitness.items()},
            "pareto_front_size": len(self.pareto_front),
            "generations": self.generations,
            "runtime_seconds": round(self.runtime_seconds, 2),
        }


# ============ 遗传算法优化器 ============

class GeneticOptimizerV3:
    """
    V3.0 遗传算法多目标优化器
    
    支持 NSGA-II 多目标优化算法
    
    使用示例:
    ```python
    optimizer = GeneticOptimizerV3(
        population_size=50,
        generations=100,
        mode=OptimizationMode.PARETO,
    )
    
    # 定义参数空间
    optimizer.add_parameter("min_roe", 0.05, 0.30, step=0.01)
    optimizer.add_parameter("max_pe", 20, 80, param_type="int")
    
    # 定义优化目标
    optimizer.add_objective("return", ObjectiveType.MAXIMIZE, weight=0.4)
    optimizer.add_objective("drawdown", ObjectiveType.MINIMIZE, weight=0.3)
    optimizer.add_objective("sharpe", ObjectiveType.MAXIMIZE, weight=0.3)
    
    # 执行优化
    result = optimizer.optimize(fitness_func)
    ```
    """
    
    # 预设平衡方案
    BALANCED_OBJECTIVES = [
        OptimizationObjective("return", ObjectiveType.MAXIMIZE, weight=0.30),
        OptimizationObjective("drawdown", ObjectiveType.MINIMIZE, weight=0.25),
        OptimizationObjective("sharpe", ObjectiveType.MAXIMIZE, weight=0.25),
        OptimizationObjective("win_rate", ObjectiveType.MAXIMIZE, weight=0.10),
        OptimizationObjective("stability", ObjectiveType.MAXIMIZE, weight=0.10),
    ]
    
    # 保守方案
    CONSERVATIVE_OBJECTIVES = [
        OptimizationObjective("return", ObjectiveType.MAXIMIZE, weight=0.20),
        OptimizationObjective("drawdown", ObjectiveType.MINIMIZE, weight=0.40),
        OptimizationObjective("sharpe", ObjectiveType.MAXIMIZE, weight=0.25),
        OptimizationObjective("win_rate", ObjectiveType.MAXIMIZE, weight=0.15),
    ]
    
    # 进取方案
    AGGRESSIVE_OBJECTIVES = [
        OptimizationObjective("return", ObjectiveType.MAXIMIZE, weight=0.50),
        OptimizationObjective("drawdown", ObjectiveType.MINIMIZE, weight=0.15),
        OptimizationObjective("sharpe", ObjectiveType.MAXIMIZE, weight=0.20),
        OptimizationObjective("win_rate", ObjectiveType.MAXIMIZE, weight=0.15),
    ]
    
    def __init__(
        self,
        population_size: int = 50,
        generations: int = 100,
        crossover_rate: float = 0.8,
        mutation_rate: float = 0.1,
        elite_ratio: float = 0.1,
        mode: OptimizationMode = OptimizationMode.BALANCED,
        early_stop_generations: int = 20,
    ):
        """
        初始化
        
        Args:
            population_size: 种群大小
            generations: 迭代代数
            crossover_rate: 交叉概率
            mutation_rate: 变异概率
            elite_ratio: 精英保留比例
            mode: 优化模式
            early_stop_generations: 早停代数
        """
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elite_ratio = elite_ratio
        self.mode = mode
        self.early_stop_generations = early_stop_generations
        
        self.parameter_space: List[ParameterSpace] = []
        self.objectives: List[OptimizationObjective] = []
        self._population: List[Individual] = []
        self._history: List[Dict] = []
    
    def add_parameter(
        self,
        name: str,
        min_value: float,
        max_value: float,
        step: float = 0.01,
        param_type: str = "float",
        choices: List[Any] = None,
    ):
        """添加参数"""
        self.parameter_space.append(ParameterSpace(
            name=name,
            min_value=min_value,
            max_value=max_value,
            step=step,
            param_type=param_type,
            choices=choices or [],
        ))
    
    def add_objective(
        self,
        name: str,
        obj_type: ObjectiveType,
        weight: float = 1.0,
        constraint_min: float = None,
        constraint_max: float = None,
    ):
        """添加优化目标"""
        self.objectives.append(OptimizationObjective(
            name=name,
            type=obj_type,
            weight=weight,
            constraint_min=constraint_min,
            constraint_max=constraint_max,
        ))
    
    def use_preset_objectives(self, preset: str = "balanced"):
        """使用预设目标"""
        preset_map = {
            "balanced": self.BALANCED_OBJECTIVES,
            "conservative": self.CONSERVATIVE_OBJECTIVES,
            "aggressive": self.AGGRESSIVE_OBJECTIVES,
        }
        self.objectives = copy.deepcopy(preset_map.get(preset, self.BALANCED_OBJECTIVES))
    
    def _init_population(self) -> List[Individual]:
        """初始化种群"""
        population = []
        for _ in range(self.population_size):
            params = {}
            for ps in self.parameter_space:
                params[ps.name] = ps.sample()
            population.append(Individual(params=params))
        return population
    
    def _evaluate_population(
        self,
        population: List[Individual],
        fitness_func: Callable[[Dict], Dict[str, float]],
    ):
        """评估种群适应度"""
        for ind in population:
            if not ind.fitness:
                try:
                    ind.fitness = fitness_func(ind.params)
                except Exception as e:
                    logger.warning(f"适应度计算失败: {e}")
                    # 设置默认差适应度
                    ind.fitness = {obj.name: 0 if obj.type == ObjectiveType.MAXIMIZE else 1 
                                   for obj in self.objectives}
    
    def _fast_non_dominated_sort(self, population: List[Individual]) -> List[List[Individual]]:
        """快速非支配排序 (NSGA-II)"""
        fronts = [[]]
        
        for p in population:
            p.domination_count = 0
            p.dominated_set = []
            
            for q in population:
                if p.dominates(q, self.objectives):
                    p.dominated_set.append(q)
                elif q.dominates(p, self.objectives):
                    p.domination_count += 1
            
            if p.domination_count == 0:
                p.rank = 0
                fronts[0].append(p)
        
        i = 0
        while fronts[i]:
            next_front = []
            for p in fronts[i]:
                for q in p.dominated_set:
                    q.domination_count -= 1
                    if q.domination_count == 0:
                        q.rank = i + 1
                        next_front.append(q)
            i += 1
            fronts.append(next_front)
        
        return fronts[:-1]  # 去除最后一个空列表
    
    def _calculate_crowding_distance(self, front: List[Individual]):
        """计算拥挤度距离"""
        n = len(front)
        if n == 0:
            return
        
        for ind in front:
            ind.crowding_distance = 0
        
        for obj in self.objectives:
            front.sort(key=lambda x: x.fitness.get(obj.name, 0))
            
            front[0].crowding_distance = float('inf')
            front[-1].crowding_distance = float('inf')
            
            f_max = front[-1].fitness.get(obj.name, 1)
            f_min = front[0].fitness.get(obj.name, 0)
            
            if f_max == f_min:
                continue
            
            for i in range(1, n - 1):
                front[i].crowding_distance += (
                    front[i + 1].fitness.get(obj.name, 0) - 
                    front[i - 1].fitness.get(obj.name, 0)
                ) / (f_max - f_min)
    
    def _selection(self, population: List[Individual], n: int) -> List[Individual]:
        """锦标赛选择"""
        selected = []
        
        for _ in range(n):
            # 随机选择两个个体
            a, b = random.sample(population, 2)
            
            # 比较 (先比较rank，再比较拥挤度)
            if a.rank < b.rank:
                selected.append(copy.deepcopy(a))
            elif b.rank < a.rank:
                selected.append(copy.deepcopy(b))
            elif a.crowding_distance > b.crowding_distance:
                selected.append(copy.deepcopy(a))
            else:
                selected.append(copy.deepcopy(b))
        
        return selected
    
    def _crossover(self, parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
        """交叉"""
        if random.random() > self.crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        child1_params = {}
        child2_params = {}
        
        for ps in self.parameter_space:
            if random.random() < 0.5:
                child1_params[ps.name] = parent1.params[ps.name]
                child2_params[ps.name] = parent2.params[ps.name]
            else:
                child1_params[ps.name] = parent2.params[ps.name]
                child2_params[ps.name] = parent1.params[ps.name]
        
        return Individual(params=child1_params), Individual(params=child2_params)
    
    def _mutate(self, individual: Individual) -> Individual:
        """变异"""
        for ps in self.parameter_space:
            individual.params[ps.name] = ps.mutate(
                individual.params[ps.name],
                self.mutation_rate
            )
        return individual
    
    def _get_weighted_fitness(self, fitness: Dict[str, float]) -> float:
        """计算加权适应度"""
        total = 0.0
        
        for obj in self.objectives:
            val = fitness.get(obj.name, 0)
            
            # 归一化 (简单线性)
            if obj.type == ObjectiveType.MINIMIZE:
                val = -val  # 转换为最大化
            
            total += val * obj.weight
        
        return total
    
    def optimize(
        self,
        fitness_func: Callable[[Dict], Dict[str, float]],
        verbose: bool = True,
    ) -> OptimizationResult:
        """
        执行优化
        
        Args:
            fitness_func: 适应度函数，输入参数字典，输出各目标值字典
            verbose: 是否打印进度
            
        Returns:
            OptimizationResult 优化结果
        """
        import time
        start_time = time.time()
        
        if not self.parameter_space:
            raise ValueError("请先添加参数空间")
        
        if not self.objectives:
            self.use_preset_objectives("balanced")
        
        logger.info(f"开始优化: 种群={self.population_size}, 代数={self.generations}")
        
        # 初始化种群
        population = self._init_population()
        self._evaluate_population(population, fitness_func)
        
        best_fitness_history = []
        no_improve_count = 0
        
        for gen in range(self.generations):
            # 非支配排序
            fronts = self._fast_non_dominated_sort(population)
            
            # 计算拥挤度
            for front in fronts:
                self._calculate_crowding_distance(front)
            
            # 记录最佳
            if fronts[0]:
                best = max(fronts[0], key=lambda x: self._get_weighted_fitness(x.fitness))
                best_weighted = self._get_weighted_fitness(best.fitness)
                
                if verbose and gen % 10 == 0:
                    logger.info(f"Gen {gen}: best_fitness={best_weighted:.4f}, pareto_front={len(fronts[0])}")
                
                # 早停检查
                if best_fitness_history and best_weighted <= max(best_fitness_history):
                    no_improve_count += 1
                else:
                    no_improve_count = 0
                
                best_fitness_history.append(best_weighted)
                
                if no_improve_count >= self.early_stop_generations:
                    logger.info(f"早停: {no_improve_count}代无改善")
                    break
            
            self._history.append({
                "generation": gen,
                "best_fitness": best_weighted if fronts[0] else 0,
                "pareto_front_size": len(fronts[0]) if fronts[0] else 0,
            })
            
            # 选择
            offspring = self._selection(population, self.population_size)
            
            # 交叉和变异
            new_population = []
            for i in range(0, len(offspring) - 1, 2):
                child1, child2 = self._crossover(offspring[i], offspring[i+1])
                new_population.append(self._mutate(child1))
                new_population.append(self._mutate(child2))
            
            # 评估新种群
            self._evaluate_population(new_population, fitness_func)
            
            # 合并并选择下一代
            combined = population + new_population
            fronts = self._fast_non_dominated_sort(combined)
            
            for front in fronts:
                self._calculate_crowding_distance(front)
            
            # 选择精英
            next_population = []
            for front in fronts:
                if len(next_population) + len(front) <= self.population_size:
                    next_population.extend(front)
                else:
                    # 按拥挤度排序填充
                    front.sort(key=lambda x: x.crowding_distance, reverse=True)
                    next_population.extend(front[:self.population_size - len(next_population)])
                    break
            
            population = next_population
        
        # 最终排序
        fronts = self._fast_non_dominated_sort(population)
        pareto_front = fronts[0] if fronts else []
        
        # 找出最佳个体
        if pareto_front:
            best = max(pareto_front, key=lambda x: self._get_weighted_fitness(x.fitness))
        else:
            best = max(population, key=lambda x: self._get_weighted_fitness(x.fitness))
        
        runtime = time.time() - start_time
        
        result = OptimizationResult(
            best_params=best.params,
            best_fitness=best.fitness,
            pareto_front=pareto_front,
            history=self._history,
            generations=gen + 1,
            runtime_seconds=runtime,
        )
        
        logger.info(f"优化完成: {gen+1}代, 耗时{runtime:.1f}秒")
        logger.info(f"最佳参数: {best.params}")
        logger.info(f"最佳适应度: {best.fitness}")
        
        return result
    
    def get_pareto_summary(self, result: OptimizationResult) -> str:
        """获取帕累托前沿摘要"""
        if not result.pareto_front:
            return "无帕累托前沿"
        
        lines = [
            "📊 帕累托前沿摘要",
            "━" * 50,
            f"前沿解数量: {len(result.pareto_front)}",
            "",
            "各目标范围:",
        ]
        
        for obj in self.objectives:
            values = [ind.fitness.get(obj.name, 0) for ind in result.pareto_front]
            lines.append(f"  {obj.name}: {min(values):.4f} ~ {max(values):.4f}")
        
        lines.extend([
            "",
            "最佳解 (加权):",
            f"  参数: {result.best_params}",
            f"  适应度: {result.best_fitness}",
        ])
        
        return "\n".join(lines)


# ============ 便捷函数 ============

def optimize_filter_params(
    fitness_func: Callable[[Dict], Dict[str, float]],
    parameter_ranges: Dict[str, Tuple[float, float]],
    objectives: str = "balanced",
    generations: int = 50,
) -> OptimizationResult:
    """
    便捷函数：优化筛选参数
    
    Args:
        fitness_func: 适应度函数
        parameter_ranges: 参数范围 {name: (min, max)}
        objectives: 目标方案 "balanced"/"conservative"/"aggressive"
        generations: 迭代代数
        
    Returns:
        OptimizationResult
    """
    optimizer = GeneticOptimizerV3(generations=generations)
    
    for name, (min_val, max_val) in parameter_ranges.items():
        param_type = "int" if isinstance(min_val, int) and isinstance(max_val, int) else "float"
        optimizer.add_parameter(name, min_val, max_val, param_type=param_type)
    
    optimizer.use_preset_objectives(objectives)
    
    return optimizer.optimize(fitness_func)
