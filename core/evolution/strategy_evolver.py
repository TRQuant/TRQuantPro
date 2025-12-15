# -*- coding: utf-8 -*-
"""策略进化框架 - 基于遗传算法"""

import logging
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from dataclasses import dataclass, field
import random
import numpy as np
from copy import deepcopy

logger = logging.getLogger(__name__)


@dataclass
class StrategyGene:
    gene_id: str
    params: Dict[str, Any]
    fitness: float = 0.0
    generation: int = 0


@dataclass
class EvolutionConfig:
    population_size: int = 20
    generations: int = 10
    mutation_rate: float = 0.2
    crossover_rate: float = 0.7
    elite_ratio: float = 0.1


class StrategyEvolver:
    """策略进化器"""
    
    PARAM_RANGES = {
        "momentum": {
            "mom_short": (3, 20, 1),
            "mom_long": (10, 60, 5),
            "top_n": (5, 20, 1),
            "rebalance_days": (1, 20, 1),
        }
    }
    
    def __init__(self, config: EvolutionConfig = None):
        self.config = config or EvolutionConfig()
        self.population: List[StrategyGene] = []
        self.history: List[Dict] = []
        self.best_gene: Optional[StrategyGene] = None
    
    def initialize_population(self, strategy_type: str = "momentum"):
        self.population = []
        param_ranges = self.PARAM_RANGES.get(strategy_type, {})
        
        for i in range(self.config.population_size):
            params = {}
            for param, (min_val, max_val, step) in param_ranges.items():
                if isinstance(min_val, float):
                    params[param] = round(random.uniform(min_val, max_val), 2)
                else:
                    params[param] = random.randint(min_val // step, max_val // step) * step
            
            gene = StrategyGene(gene_id=f"gen0_{i}", params=params, generation=0)
            self.population.append(gene)
    
    def evolve(self, securities: List[str], start_date: str, end_date: str, 
               strategy_type: str = "momentum") -> StrategyGene:
        if not self.population:
            self.initialize_population(strategy_type)
        
        for gen in range(self.config.generations):
            self._evaluate_fitness(securities, start_date, end_date, strategy_type)
            self._record_generation(gen)
            
            if gen < self.config.generations - 1:
                self.population = self._evolve_generation(gen + 1, strategy_type)
        
        return self.best_gene
    
    def _evaluate_fitness(self, securities, start_date, end_date, strategy_type):
        from core.backtest.fast_backtest_engine import quick_backtest
        
        for gene in self.population:
            try:
                result = quick_backtest(securities, start_date, end_date, strategy_type, **gene.params)
                gene.fitness = result.sharpe_ratio * 0.4 + result.total_return * 0.3 - abs(result.max_drawdown) * 0.2 + result.win_rate * 0.1
            except:
                gene.fitness = -999
        
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        self.best_gene = self.population[0]
    
    def _evolve_generation(self, new_gen: int, strategy_type: str) -> List[StrategyGene]:
        new_pop = []
        elite_count = max(1, int(self.config.population_size * self.config.elite_ratio))
        
        for i in range(elite_count):
            elite = deepcopy(self.population[i])
            elite.gene_id = f"gen{new_gen}_{i}_elite"
            new_pop.append(elite)
        
        while len(new_pop) < self.config.population_size:
            p1, p2 = random.sample(self.population[:5], 2)
            child_params = {k: p1.params[k] if random.random() < 0.5 else p2.params[k] for k in p1.params}
            
            if random.random() < self.config.mutation_rate:
                child_params = self._mutate(child_params, strategy_type)
            
            new_pop.append(StrategyGene(f"gen{new_gen}_{len(new_pop)}", child_params, generation=new_gen))
        
        return new_pop
    
    def _mutate(self, params: Dict, strategy_type: str) -> Dict:
        param_ranges = self.PARAM_RANGES.get(strategy_type, {})
        mutated = deepcopy(params)
        for key in mutated:
            if random.random() < 0.3 and key in param_ranges:
                min_val, max_val, step = param_ranges[key]
                mutated[key] = random.randint(min_val // step, max_val // step) * step
        return mutated
    
    def _record_generation(self, gen: int):
        fitness_list = [g.fitness for g in self.population]
        self.history.append({
            "generation": gen,
            "best": max(fitness_list),
            "avg": np.mean(fitness_list),
            "best_params": self.best_gene.params
        })
    
    def print_summary(self):
        print("\n策略进化摘要")
        for h in self.history:
            print(f"第{h['generation']+1}代: 最佳={h['best']:.4f}")
        if self.best_gene:
            print(f"最优参数: {self.best_gene.params}")
