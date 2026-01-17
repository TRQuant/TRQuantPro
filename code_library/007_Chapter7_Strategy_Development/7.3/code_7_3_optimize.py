"""
文件名: code_7_3_optimize.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.3/code_7_3_optimize.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: optimize

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from deap import base, creator, tools
import random

class GeneticAlgorithmOptimizer:
    """遗传算法优化器"""
    
    def optimize(
        self,
        parameter_ranges: Dict[str, Tuple[float, float]],
        eval_func: Callable[[Dict[str, float]], float],
        population_size: int = 50,
        generations: int = 50
    ) -> OptimizationResult:
            """
    optimize函数
    
    **设计原理**：
    - **核心功能**：实现optimize的核心逻辑
    - **设计思路**：通过XXX方式实现XXX功能
    - **性能考虑**：使用XXX方法提高效率
    
    **为什么这样设计**：
    1. **原因1**：说明设计原因
    2. **原因2**：说明设计原因
    3. **原因3**：说明设计原因
    
    **使用场景**：
    - 场景1：使用场景说明
    - 场景2：使用场景说明
    
    Args:
        # 参数说明
    
    Returns:
        # 返回值说明
    """
        # 创建类型
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        # 初始化工具箱
        toolbox = base.Toolbox()
        
        # 定义参数生成函数
        param_names = list(parameter_ranges.keys())
        for i, (name, (min_val, max_val)) in enumerate(parameter_ranges.items()):
            toolbox.register(
                f"attr_{i}",
                random.uniform,
                min_val,
                max_val
            )
        
        # 创建个体和种群
        toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            [getattr(toolbox, f"attr_{i}") for i in range(len(param_names))],
            n=1
        )
        toolbox.register(
            "population",
            tools.initRepeat,
            list,
            toolbox.individual
        )
        
        # 定义评估函数
        def evaluate(individual):
            params = dict(zip(param_names, individual))
            return (eval_func(params),)
        
        toolbox.register("evaluate", evaluate)
        toolbox.register("mate", tools.cxBlend, alpha=0.5)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)
        
        # 创建初始种群
        population = toolbox.population(n=population_size)
        
        # 评估初始种群
        fitnesses = list(map(toolbox.evaluate, population))
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit
        
        # 进化
        for generation in range(generations):
            # 选择
            offspring = toolbox.select(population, len(population))
            offspring = list(map(toolbox.clone, offspring))
            
            # 交叉
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.5:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values
            
            # 变异
            for mutant in offspring:
                if random.random() < 0.2:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
            
            # 评估新个体
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            
            # 更新种群
            population[:] = offspring
        
        # 提取最优个体
        best_ind = tools.selBest(population, 1)[0]
        best_params = dict(zip(param_names, best_ind))
        best_score = best_ind.fitness.values[0]
        
        return OptimizationResult(
            best_weights=best_params,
            best_performance=best_score,
            all_results=[(best_params, best_score)],
            optimization_method="genetic",
            iterations=population_size * generations
        )