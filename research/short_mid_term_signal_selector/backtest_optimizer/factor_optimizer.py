# -*- coding: utf-8 -*-
"""
因子权重优化器 (Factor Weight Optimizer)

核心功能：
1. 基于回测结果优化因子权重
2. 防过拟合机制：正则化 + 交叉验证
3. 贝叶斯优化 / 网格搜索
4. 因子重要性分析
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
import warnings
from scipy import optimize
from sklearn.model_selection import TimeSeriesSplit

from .backtest_engine import BacktestEngine, BacktestResult, BACKTEST_PERIODS


@dataclass
class OptimizationConfig:
    """优化配置"""
    # 优化目标
    target_period: str = 'month'            # 目标优化周期
    target_metric: str = 'sharpe'           # 目标指标: return/sharpe/win_rate/excess
    
    # 防过拟合
    regularization: float = 0.1             # L2正则化强度
    min_weight: float = 0.0                 # 最小权重
    max_weight: float = 1.0                 # 最大权重
    
    # 交叉验证
    cv_splits: int = 5                      # 时序交叉验证折数
    train_ratio: float = 0.7                # 训练集比例
    
    # 优化方法
    method: str = 'bayesian'                # bayesian/grid/random
    max_iterations: int = 100               # 最大迭代次数


@dataclass
class FactorDefinition:
    """因子定义"""
    name: str               # 因子名称
    description: str        # 因子描述
    category: str           # 类别: fundamental/growth/valuation/technical/sector
    default_weight: float   # 默认权重
    min_weight: float = 0.0
    max_weight: float = 1.0


# 默认因子定义
DEFAULT_FACTORS = {
    # 基本面因子
    'roe': FactorDefinition('ROE', 'ROE得分', 'fundamental', 0.15),
    'gross_margin': FactorDefinition('毛利率', '毛利率得分', 'fundamental', 0.10),
    
    # 成长因子
    'revenue_growth': FactorDefinition('营收增长', '营收增长率得分', 'growth', 0.15),
    'profit_growth': FactorDefinition('利润增长', '净利润增长率得分', 'growth', 0.15),
    
    # 估值因子
    'pe_score': FactorDefinition('PE估值', 'PE估值得分', 'valuation', 0.10),
    'peg_score': FactorDefinition('PEG', 'PEG得分', 'valuation', 0.10),
    
    # 技术因子
    'trend_score': FactorDefinition('趋势', '趋势强度得分', 'technical', 0.10),
    'momentum_score': FactorDefinition('动量', '动量得分', 'technical', 0.05),
    
    # 板块因子
    'sector_weight': FactorDefinition('板块权重', '主线板块权重', 'sector', 0.10),
}


@dataclass 
class OptimizationResult:
    """优化结果"""
    optimized_weights: Dict[str, float]     # 优化后权重
    improvement: float                       # 相对默认权重的提升
    train_score: float                      # 训练集得分
    val_score: float                        # 验证集得分
    cv_scores: List[float]                  # 交叉验证得分
    
    # 因子重要性
    factor_importance: Dict[str, float] = field(default_factory=dict)
    
    # 元数据
    optimization_config: OptimizationConfig = None
    optimization_history: List[Dict] = field(default_factory=list)


class FactorOptimizer:
    """
    因子权重优化器
    
    设计原则：
    1. 基于历史回测结果学习最优权重
    2. 时序交叉验证防止过拟合
    3. L2正则化惩罚极端权重
    4. 支持多种优化算法
    """
    
    def __init__(self,
                 backtest_engine: BacktestEngine,
                 factor_definitions: Dict[str, FactorDefinition] = None,
                 config: OptimizationConfig = None):
        """
        Args:
            backtest_engine: 回测引擎实例
            factor_definitions: 因子定义
            config: 优化配置
        """
        self.engine = backtest_engine
        self.factors = factor_definitions or DEFAULT_FACTORS
        self.config = config or OptimizationConfig()
        
        # 因子名称列表
        self.factor_names = list(self.factors.keys())
        
    def optimize(self,
                 start_date: str,
                 end_date: str,
                 initial_weights: Dict[str, float] = None) -> OptimizationResult:
        """
        执行因子权重优化
        
        Args:
            start_date: 回测开始日期
            end_date: 回测结束日期
            initial_weights: 初始权重（可选）
            
        Returns:
            OptimizationResult: 优化结果
        """
        print(f"\n{'='*60}")
        print(f"🔧 因子权重优化")
        print(f"{'='*60}")
        print(f"📅 回测区间: {start_date} -> {end_date}")
        print(f"🎯 优化目标: {self.config.target_period} {self.config.target_metric}")
        print(f"🛡️ 正则化强度: {self.config.regularization}")
        
        # 初始化权重
        if initial_weights is None:
            initial_weights = {name: f.default_weight for name, f in self.factors.items()}
        
        # 获取回测数据用于优化
        print(f"\n📊 运行历史回测...")
        backtest_results = self.engine.run_rolling_backtest(
            start_date=start_date,
            end_date=end_date,
            frequency='month',
            top_n=30,
            factor_weights=initial_weights
        )
        
        if not backtest_results:
            raise ValueError("回测未产生有效结果")
        
        # 划分训练/验证集
        split_idx = int(len(backtest_results) * self.config.train_ratio)
        train_results = backtest_results[:split_idx]
        val_results = backtest_results[split_idx:]
        
        print(f"\n📊 训练集: {len(train_results)} 个回测点")
        print(f"📊 验证集: {len(val_results)} 个回测点")
        
        # 执行优化
        if self.config.method == 'bayesian':
            optimized_weights = self._bayesian_optimize(train_results, initial_weights)
        elif self.config.method == 'grid':
            optimized_weights = self._grid_search(train_results, initial_weights)
        else:
            optimized_weights = self._random_search(train_results, initial_weights)
        
        # 评估结果
        train_score = self._evaluate_weights(optimized_weights, train_results)
        val_score = self._evaluate_weights(optimized_weights, val_results)
        baseline_score = self._evaluate_weights(initial_weights, val_results)
        
        improvement = (val_score - baseline_score) / abs(baseline_score) * 100 if baseline_score != 0 else 0
        
        # 交叉验证
        cv_scores = self._cross_validate(backtest_results, optimized_weights)
        
        # 因子重要性分析
        factor_importance = self._analyze_factor_importance(optimized_weights, val_results)
        
        # 构建结果
        result = OptimizationResult(
            optimized_weights=optimized_weights,
            improvement=improvement,
            train_score=train_score,
            val_score=val_score,
            cv_scores=cv_scores,
            factor_importance=factor_importance,
            optimization_config=self.config
        )
        
        self._print_optimization_result(result, initial_weights)
        
        return result
    
    def _bayesian_optimize(self, 
                          results: List[BacktestResult],
                          initial_weights: Dict[str, float]) -> Dict[str, float]:
        """贝叶斯优化"""
        print(f"\n🔍 贝叶斯优化...")
        
        # 转换为数组形式
        x0 = np.array([initial_weights.get(name, 0.5) for name in self.factor_names])
        
        # 边界约束
        bounds = [(self.factors[name].min_weight, self.factors[name].max_weight) 
                  for name in self.factor_names]
        
        def objective(weights_array):
            weights_dict = {name: w for name, w in zip(self.factor_names, weights_array)}
            # 负值因为scipy最小化
            score = -self._evaluate_weights(weights_dict, results)
            # 添加L2正则化
            reg_penalty = self.config.regularization * np.sum(weights_array ** 2)
            return score + reg_penalty
        
        # 使用L-BFGS-B优化
        result = optimize.minimize(
            objective,
            x0,
            method='L-BFGS-B',
            bounds=bounds,
            options={'maxiter': self.config.max_iterations}
        )
        
        optimized = {name: w for name, w in zip(self.factor_names, result.x)}
        
        # 归一化权重
        total = sum(optimized.values())
        if total > 0:
            optimized = {k: v/total for k, v in optimized.items()}
        
        return optimized
    
    def _grid_search(self,
                    results: List[BacktestResult],
                    initial_weights: Dict[str, float]) -> Dict[str, float]:
        """网格搜索"""
        print(f"\n🔍 网格搜索...")
        
        # 简化的网格搜索（只调整类别权重）
        categories = set(f.category for f in self.factors.values())
        
        best_score = float('-inf')
        best_weights = initial_weights.copy()
        
        # 类别权重组合
        weight_options = [0.1, 0.2, 0.3, 0.4, 0.5]
        
        for cat_weights in self._generate_category_combinations(categories, weight_options):
            # 将类别权重分配到具体因子
            weights = self._category_to_factor_weights(cat_weights)
            score = self._evaluate_weights(weights, results)
            
            if score > best_score:
                best_score = score
                best_weights = weights
                
        return best_weights
    
    def _random_search(self,
                      results: List[BacktestResult],
                      initial_weights: Dict[str, float]) -> Dict[str, float]:
        """随机搜索"""
        print(f"\n🔍 随机搜索...")
        
        best_score = float('-inf')
        best_weights = initial_weights.copy()
        
        for _ in range(self.config.max_iterations):
            # 随机生成权重
            weights = {}
            for name, factor in self.factors.items():
                weights[name] = np.random.uniform(factor.min_weight, factor.max_weight)
            
            # 归一化
            total = sum(weights.values())
            if total > 0:
                weights = {k: v/total for k, v in weights.items()}
            
            score = self._evaluate_weights(weights, results)
            
            if score > best_score:
                best_score = score
                best_weights = weights
                
        return best_weights
    
    def _evaluate_weights(self, 
                         weights: Dict[str, float],
                         results: List[BacktestResult]) -> float:
        """评估权重组合的表现"""
        if not results:
            return 0.0
            
        scores = []
        for result in results:
            period_key = self.config.target_period
            
            if self.config.target_metric == 'return':
                score = result.avg_returns.get(period_key, 0) or 0
            elif self.config.target_metric == 'sharpe':
                # 使用风险调整收益近似
                ret = result.avg_returns.get(period_key, 0) or 0
                excess = result.excess_returns.get(period_key, 0) or 0
                score = excess if excess > 0 else ret * 0.5
            elif self.config.target_metric == 'win_rate':
                score = result.win_rates.get(period_key, 0) or 0
            elif self.config.target_metric == 'excess':
                score = result.excess_returns.get(period_key, 0) or 0
            else:
                score = result.avg_returns.get(period_key, 0) or 0
                
            scores.append(score)
            
        return np.mean(scores) if scores else 0.0
    
    def _cross_validate(self, 
                       results: List[BacktestResult],
                       weights: Dict[str, float]) -> List[float]:
        """时序交叉验证"""
        n = len(results)
        if n < self.config.cv_splits * 2:
            return []
            
        scores = []
        fold_size = n // self.config.cv_splits
        
        for i in range(self.config.cv_splits):
            val_start = i * fold_size
            val_end = (i + 1) * fold_size if i < self.config.cv_splits - 1 else n
            
            val_results = results[val_start:val_end]
            score = self._evaluate_weights(weights, val_results)
            scores.append(score)
            
        return scores
    
    def _analyze_factor_importance(self,
                                   weights: Dict[str, float],
                                   results: List[BacktestResult]) -> Dict[str, float]:
        """分析因子重要性"""
        importance = {}
        base_score = self._evaluate_weights(weights, results)
        
        for factor_name in self.factor_names:
            # 移除该因子
            modified_weights = weights.copy()
            modified_weights[factor_name] = 0
            
            # 重新归一化
            total = sum(modified_weights.values())
            if total > 0:
                modified_weights = {k: v/total for k, v in modified_weights.items()}
            
            # 评估影响
            modified_score = self._evaluate_weights(modified_weights, results)
            importance[factor_name] = base_score - modified_score
            
        return importance
    
    def _generate_category_combinations(self, categories, options):
        """生成类别权重组合"""
        import itertools
        cats = list(categories)
        for combo in itertools.product(options, repeat=len(cats)):
            yield dict(zip(cats, combo))
    
    def _category_to_factor_weights(self, cat_weights: Dict[str, float]) -> Dict[str, float]:
        """将类别权重转换为因子权重"""
        weights = {}
        for name, factor in self.factors.items():
            cat_weight = cat_weights.get(factor.category, 0.2)
            # 类别内平均分配
            cat_factors = [n for n, f in self.factors.items() if f.category == factor.category]
            weights[name] = cat_weight / len(cat_factors) if cat_factors else 0
        return weights
    
    def _print_optimization_result(self, result: OptimizationResult, initial_weights: Dict[str, float]):
        """打印优化结果"""
        print(f"\n{'='*60}")
        print(f"📈 优化结果")
        print(f"{'='*60}")
        
        print(f"\n🎯 性能指标:")
        print(f"   训练集得分: {result.train_score:.2f}")
        print(f"   验证集得分: {result.val_score:.2f}")
        print(f"   提升幅度: {result.improvement:+.1f}%")
        
        if result.cv_scores:
            print(f"   交叉验证: {np.mean(result.cv_scores):.2f} ± {np.std(result.cv_scores):.2f}")
        
        print(f"\n📊 优化后权重:")
        for name in sorted(result.optimized_weights.keys()):
            old_w = initial_weights.get(name, 0)
            new_w = result.optimized_weights[name]
            change = (new_w - old_w) / old_w * 100 if old_w > 0 else 0
            arrow = "↑" if change > 5 else "↓" if change < -5 else "→"
            print(f"   {name}: {old_w:.2f} -> {new_w:.2f} {arrow}")
        
        print(f"\n🔍 因子重要性:")
        sorted_importance = sorted(result.factor_importance.items(), 
                                  key=lambda x: abs(x[1]), reverse=True)
        for name, imp in sorted_importance[:5]:
            bar = "█" * int(abs(imp) * 10)
            sign = "+" if imp > 0 else "-"
            print(f"   {name}: {sign}{abs(imp):.2f} {bar}")


class AdaptiveWeightManager:
    """
    自适应权重管理器
    
    根据历史表现动态调整权重，支持：
    1. 指数移动平均更新
    2. 表现奖励机制
    3. 权重衰减
    """
    
    def __init__(self, 
                 initial_weights: Dict[str, float],
                 learning_rate: float = 0.1,
                 decay_rate: float = 0.01):
        """
        Args:
            initial_weights: 初始权重
            learning_rate: 学习率
            decay_rate: 衰减率
        """
        self.weights = initial_weights.copy()
        self.lr = learning_rate
        self.decay = decay_rate
        self.history = []
        
    def update(self, performance: Dict[str, float]):
        """
        根据表现更新权重
        
        Args:
            performance: 各因子的表现评分
        """
        # 归一化表现
        perf_values = list(performance.values())
        if not perf_values:
            return
            
        mean_perf = np.mean(perf_values)
        std_perf = np.std(perf_values) + 1e-8
        
        for factor_name, perf in performance.items():
            if factor_name in self.weights:
                # 标准化表现
                normalized_perf = (perf - mean_perf) / std_perf
                
                # 更新权重（带衰减）
                old_weight = self.weights[factor_name]
                new_weight = old_weight * (1 - self.decay) + self.lr * normalized_perf
                
                # 限制范围
                self.weights[factor_name] = np.clip(new_weight, 0.01, 0.5)
        
        # 归一化
        total = sum(self.weights.values())
        if total > 0:
            self.weights = {k: v/total for k, v in self.weights.items()}
        
        # 记录历史
        self.history.append(self.weights.copy())
        
    def get_weights(self) -> Dict[str, float]:
        """获取当前权重"""
        return self.weights.copy()
    
    def get_history(self) -> List[Dict[str, float]]:
        """获取权重历史"""
        return self.history


if __name__ == '__main__':
    print("🧪 因子优化器测试...")
    
    # 需要真实的回测引擎来测试
    # optimizer = FactorOptimizer(engine)
    # result = optimizer.optimize('2023-01-01', '2024-01-01')
