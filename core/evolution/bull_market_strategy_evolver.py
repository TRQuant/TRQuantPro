#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市策略进化器

基于遗传算法的策略参数优化，目标：最大化月回报率（target: 30%）
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import random
import numpy as np
import logging
from copy import deepcopy

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.evolution.param_space_bull_market import (
    BULL_MARKET_PARAM_SPACE,
    decode_individual,
    encode_params
)
from core.bullettrade.recursive_backtest_engine import RecursiveBacktestEngine, BacktestConfig, StandardizedBacktestResult

logger = logging.getLogger(__name__)


@dataclass
class EvolutionConfig:
    """进化配置"""
    population_size: int = 50          # 种群大小
    generations: int = 10              # 进化代数
    elite_ratio: float = 0.1           # 精英比例（保留前10%）
    crossover_rate: float = 0.7        # 交叉率
    mutation_rate: float = 0.3         # 变异率
    mutation_strength: float = 0.1     # 变异强度
    
    # 目标
    target_monthly_return: float = 0.30  # 目标月回报率（30%）
    max_drawdown_limit: float = -0.20    # 最大回撤限制（-20%）
    min_sharpe_ratio: float = 2.0        # 最小夏普比率


@dataclass
class Individual:
    """个体（策略参数组合）"""
    params: Dict[str, any]             # 参数字典
    fitness: float = -999.0            # 适应度（月回报率）
    backtest_result: Optional[StandardizedBacktestResult] = None
    generation: int = 0
    individual_id: str = field(default_factory=lambda: f"ind_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}")
    
    def to_dict(self) -> Dict:
        return {
            'individual_id': self.individual_id,
            'generation': self.generation,
            'params': self.params,
            'fitness': self.fitness,
            'monthly_return': self.backtest_result.monthly_return if self.backtest_result else 0.0,
            'max_drawdown': self.backtest_result.max_drawdown if self.backtest_result else 0.0,
            'sharpe_ratio': self.backtest_result.sharpe_ratio if self.backtest_result else 0.0,
        }


class BullMarketStrategyEvolver:
    """牛市策略进化器"""
    
    def __init__(
        self,
        backtest_config: BacktestConfig,
        evolution_config: Optional[EvolutionConfig] = None,
        verbose: bool = True,
        use_mongodb: Optional[bool] = None,
        use_gpu: Optional[bool] = None,
        max_workers: Optional[int] = None
    ):
        """
        初始化进化器
        
        Args:
            backtest_config: 回测配置
            evolution_config: 进化配置
            verbose: 是否输出详细信息
            use_mongodb: 是否使用MongoDB存储（默认True）
            use_gpu: 是否使用GPU加速（默认True）
            max_workers: 最大并行工作数（安全模式：3）
        """
        self.backtest_config = backtest_config
        self.evolution_config = evolution_config or EvolutionConfig()
        self.verbose = verbose
        self.use_mongodb = use_mongodb if use_mongodb is not None else True
        self.use_gpu = use_gpu if use_gpu is not None else True
        self.max_workers = max_workers if max_workers is not None else 3
        
        # 创建回测引擎（传递优化参数）
        self.backtest_engine = RecursiveBacktestEngine(
            base_config=backtest_config,
            verbose=False,  # 进化过程中不输出详细日志
            use_mongodb=use_mongodb,
            use_gpu=use_gpu,
            max_workers=max_workers
        )
        
        # 种群
        self.population: List[Individual] = []
        self.best_individual: Optional[Individual] = None
        self.generation_history: List[Dict] = []
    
    def initialize_population(self) -> List[Individual]:
        """初始化种群"""
        self.population = []
        
        for i in range(self.evolution_config.population_size):
            # 随机生成参数
            params = {}
            for param_name, param_range in BULL_MARKET_PARAM_SPACE.items():
                if param_range.param_type == 'int':
                    value = random.randint(
                        int(param_range.min / param_range.step),
                        int(param_range.max / param_range.step)
                    ) * param_range.step
                else:
                    value = random.uniform(param_range.min, param_range.max)
                    value = round(value / param_range.step) * param_range.step
                params[param_name] = value
            
            # 归一化因子权重
            weight_params = [k for k in params.keys() if k.endswith('_weight')]
            if weight_params:
                total_weight = sum([params[k] for k in weight_params])
                if total_weight > 0:
                    for k in weight_params:
                        params[k] = params[k] / total_weight
            
            individual = Individual(
                params=params,
                generation=0,
                individual_id=f"gen0_ind{i}"
            )
            self.population.append(individual)
        
        if self.verbose:
            print(f"✅ 初始化种群: {len(self.population)} 个个体")
        
        return self.population
    
    def evaluate_fitness(self, individual: Individual) -> float:
        """评估个体适应度（通过回测）"""
        try:
            # 执行回测
            result = self.backtest_engine.run_backtest(
                strategy_params=individual.params,
                backtest_id=individual.individual_id
            )
            
            individual.backtest_result = result
            
            # 计算适应度（目标：最大化月回报率，同时满足约束）
            monthly_return = result.monthly_return
            max_dd = result.max_drawdown
            sharpe = result.sharpe_ratio
            
            # 基础适应度：月回报率
            fitness = monthly_return * 100.0  # 转换为百分比形式
            
            # 惩罚项：不满足约束时降低适应度
            if max_dd < self.evolution_config.max_drawdown_limit:
                fitness -= 50.0  # 回撤过大，严重惩罚
            if sharpe < self.evolution_config.min_sharpe_ratio:
                fitness -= 20.0  # 夏普比率过低，惩罚
            if monthly_return < 0:
                fitness -= 100.0  # 负收益，严重惩罚
            
            # 奖励项：达到目标时额外奖励
            if result.meets_target(
                target_monthly_return=self.evolution_config.target_monthly_return,
                max_dd=self.evolution_config.max_drawdown_limit,
                min_sharpe=self.evolution_config.min_sharpe_ratio
            ):
                fitness += 50.0  # 达到目标，额外奖励
            
            individual.fitness = fitness
            
            return fitness
            
        except Exception as e:
            logger.error(f"评估个体适应度失败: {e}")
            individual.fitness = -999.0
            return -999.0
    
    def evaluate_population(self):
        """评估整个种群（支持并行评估）"""
        if self.verbose:
            print(f"\n评估种群 ({len(self.population)} 个个体)...")
        
        # 如果种群较大且支持并行，使用并行评估
        if len(self.population) > 5 and self.max_workers > 1:
            self._evaluate_population_parallel()
        else:
            # 串行评估（小种群或单线程）
            for i, individual in enumerate(self.population):
                if self.verbose and (i + 1) % 10 == 0:
                    print(f"  评估进度: {i+1}/{len(self.population)}")
                
                self.evaluate_fitness(individual)
        
        # 排序（适应度从高到低）
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # 更新最佳个体
        if not self.best_individual or self.population[0].fitness > self.best_individual.fitness:
            self.best_individual = deepcopy(self.population[0])
        
        if self.verbose:
            best = self.population[0]
            print(f"\n✅ 种群评估完成")
            print(f"  最佳适应度: {best.fitness:.2f}")
            if best.backtest_result:
                print(f"  最佳月收益率: {best.backtest_result.monthly_return*100:.2f}%")
                print(f"  最佳最大回撤: {best.backtest_result.max_drawdown*100:.2f}%")
                print(f"  最佳夏普比率: {best.backtest_result.sharpe_ratio:.2f}")
    
    def _evaluate_population_parallel(self):
        """并行评估种群（使用ThreadPoolExecutor）"""
        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            from tqdm import tqdm
            
            if self.verbose:
                print(f"  使用并行评估（{self.max_workers}个线程）...")
            
            # 使用线程池并行评估
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(self.population))) as executor:
                futures = {
                    executor.submit(self.evaluate_fitness, individual): individual
                    for individual in self.population
                }
                
                # 使用tqdm显示进度
                with tqdm(total=len(self.population), desc="评估种群", disable=not self.verbose) as pbar:
                    for future in as_completed(futures):
                        individual = futures[future]
                        try:
                            future.result()  # 获取结果（可能抛出异常）
                        except Exception as e:
                            logger.warning(f"个体 {individual.individual_id} 评估失败: {e}")
                        pbar.update(1)
        except Exception as e:
            logger.warning(f"并行评估失败，降级到串行: {e}")
            # 降级到串行评估
            for individual in self.population:
                self.evaluate_fitness(individual)
    
    def select_parents(self, n: int = 2) -> List[Individual]:
        """选择父代（轮盘赌选择）"""
        # 适应度转正（用于概率计算）
        fitnesses = [max(0, ind.fitness + 1000) for ind in self.population]
        total_fitness = sum(fitnesses)
        
        if total_fitness == 0:
            # 如果所有适应度都很差，随机选择
            return random.sample(self.population, min(n, len(self.population)))
        
        # 轮盘赌选择
        parents = []
        for _ in range(n):
            r = random.uniform(0, total_fitness)
            cumulative = 0
            for i, fitness in enumerate(fitnesses):
                cumulative += fitness
                if cumulative >= r:
                    parents.append(self.population[i])
                    break
        
        return parents
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """交叉（单点交叉）"""
        # 编码为向量
        encoded1 = encode_params(parent1.params)
        encoded2 = encode_params(parent2.params)
        
        # 单点交叉
        crossover_point = random.randint(1, len(encoded1) - 1)
        child_encoded = encoded1[:crossover_point] + encoded2[crossover_point:]
        
        # 解码
        child_params = decode_individual(child_encoded)
        
        return Individual(
            params=child_params,
            generation=max(parent1.generation, parent2.generation) + 1
        )
    
    def mutate(self, individual: Individual) -> Individual:
        """变异"""
        # 编码为向量
        encoded = encode_params(individual.params)
        
        # 随机变异
        for i in range(len(encoded)):
            if random.random() < self.evolution_config.mutation_rate:
                # 高斯变异
                mutation = random.gauss(0, self.evolution_config.mutation_strength)
                encoded[i] = max(0.0, min(1.0, encoded[i] + mutation))
        
        # 解码
        mutated_params = decode_individual(encoded)
        
        return Individual(
            params=mutated_params,
            generation=individual.generation + 1
        )
    
    def evolve_generation(self, generation: int) -> List[Individual]:
        """进化一代"""
        new_population = []
        
        # 精英保留
        elite_count = max(1, int(self.evolution_config.population_size * self.evolution_config.elite_ratio))
        for i in range(elite_count):
            elite = deepcopy(self.population[i])
            elite.generation = generation
            elite.individual_id = f"gen{generation}_elite{i}"
            new_population.append(elite)
        
        # 生成新个体
        while len(new_population) < self.evolution_config.population_size:
            # 选择父代
            if random.random() < self.evolution_config.crossover_rate:
                parents = self.select_parents(2)
                if len(parents) >= 2:
                    child = self.crossover(parents[0], parents[1])
                else:
                    child = deepcopy(random.choice(self.population))
            else:
                # 直接复制
                child = deepcopy(random.choice(self.population[:elite_count * 2]))
            
            # 变异
            if random.random() < self.evolution_config.mutation_rate:
                child = self.mutate(child)
            
            child.generation = generation
            child.individual_id = f"gen{generation}_ind{len(new_population)}"
            new_population.append(child)
        
        return new_population
    
    def evolve(self) -> Individual:
        """执行进化"""
        if self.verbose:
            print("="*70)
            print("开始策略参数进化优化")
            print("="*70)
            print(f"目标: 月回报率 {self.evolution_config.target_monthly_return*100:.0f}%")
            print(f"约束: 最大回撤 >= {self.evolution_config.max_drawdown_limit*100:.0f}%, 夏普 >= {self.evolution_config.min_sharpe_ratio:.1f}")
            print(f"种群大小: {self.evolution_config.population_size}")
            print(f"进化代数: {self.evolution_config.generations}")
        
        # 初始化种群
        self.initialize_population()
        
        # 评估初始种群
        self.evaluate_population()
        
        # 记录第0代
        self._record_generation(0)
        
        # 进化循环
        for gen in range(1, self.evolution_config.generations + 1):
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"第 {gen} 代进化")
                print(f"{'='*70}")
            
            # 进化生成新种群
            self.population = self.evolve_generation(gen)
            
            # 评估新种群
            self.evaluate_population()
            
            # 记录
            self._record_generation(gen)
            
            # 早停检查：如果达到目标，可以提前停止
            if self.best_individual and self.best_individual.backtest_result:
                if self.best_individual.backtest_result.meets_target(
                    target_monthly_return=self.evolution_config.target_monthly_return,
                    max_dd=self.evolution_config.max_drawdown_limit,
                    min_sharpe=self.evolution_config.min_sharpe_ratio
                ):
                    if self.verbose:
                        print(f"\n✅ 达到目标！提前停止进化。")
                    break
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("进化完成")
            print(f"{'='*70}")
            if self.best_individual:
                print(f"最佳个体 ID: {self.best_individual.individual_id}")
                print(f"最佳适应度: {self.best_individual.fitness:.2f}")
                if self.best_individual.backtest_result:
                    result = self.best_individual.backtest_result
                    print(f"月收益率: {result.monthly_return*100:.2f}%")
                    print(f"最大回撤: {result.max_drawdown*100:.2f}%")
                    print(f"夏普比率: {result.sharpe_ratio:.2f}")
                    print(f"是否达标: {result.meets_target()}")
        
        return self.best_individual
    
    def _record_generation(self, generation: int):
        """记录每一代的信息"""
        if not self.population:
            return
        
        gen_info = {
            'generation': generation,
            'population_size': len(self.population),
            'best_fitness': self.population[0].fitness,
            'avg_fitness': np.mean([ind.fitness for ind in self.population]),
            'worst_fitness': self.population[-1].fitness,
        }
        
        if self.population[0].backtest_result:
            result = self.population[0].backtest_result
            gen_info.update({
                'best_monthly_return': result.monthly_return,
                'best_max_drawdown': result.max_drawdown,
                'best_sharpe_ratio': result.sharpe_ratio,
                'meets_target': result.meets_target(),
            })
        
        self.generation_history.append(gen_info)
    
    def save_results(self, output_path: str):
        """保存进化结果"""
        import json
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        results_data = {
            'evolution_config': {
                'population_size': self.evolution_config.population_size,
                'generations': self.evolution_config.generations,
                'target_monthly_return': self.evolution_config.target_monthly_return,
                'max_drawdown_limit': self.evolution_config.max_drawdown_limit,
                'min_sharpe_ratio': self.evolution_config.min_sharpe_ratio,
            },
            'best_individual': self.best_individual.to_dict() if self.best_individual else None,
            'generation_history': self.generation_history,
            'top_10_individuals': [ind.to_dict() for ind in self.population[:10]],
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_data, f, ensure_ascii=False, indent=2)
        
        if self.verbose:
            print(f"\n✅ 进化结果已保存到: {output_file}")


def main():
    """主函数：示例用法"""
    backtest_config = BacktestConfig(
        start_date='2024-10-01',
        end_date='2024-12-31',
        initial_capital=1000000.0,
        cache_dir='output/evolution_backtest_cache'
    )
    
    evolution_config = EvolutionConfig(
        population_size=20,  # 测试用小种群
        generations=5,       # 测试用少代数
        target_monthly_return=0.30,
    )
    
    evolver = BullMarketStrategyEvolver(
        backtest_config=backtest_config,
        evolution_config=evolution_config,
        verbose=True
    )
    
    # 执行进化
    best_individual = evolver.evolve()
    
    # 保存结果
    evolver.save_results('output/evolution_results.json')
    
    print(f"\n最佳参数: {best_individual.params}")


if __name__ == '__main__':
    main()
