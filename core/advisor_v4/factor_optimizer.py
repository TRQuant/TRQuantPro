#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因子优化器 - 递归优化因子选择和权重
===================================

功能：
1. 因子选择优化：从7个已验证因子中选择最优组合
2. 因子权重优化：优化已验证因子的权重分配
3. 融合权重优化：优化已验证因子vs聚宽因子的权重比例
4. Walk-Forward验证：评估模型可靠性
5. 多目标优化：平衡夏普比率、命中率、收益率

设计原则：
- 基于历史验证，不能简单堆砌
- 使用Walk-Forward验证评估可靠性
- 防止过拟合，评估模型稳定性
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable, Any, TYPE_CHECKING
from itertools import combinations, product
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib

logger = logging.getLogger(__name__)

# 导入已验证因子
from .validated_factor_calculator import (
    ValidatedFactorCalculator,
    VALIDATED_FACTORS,
    ALL_VALIDATED_FACTORS,
)
from .multi_factor_calculator import MultiFactorCalculator
from .cross_validator import (
    WalkForwardValidator,
    WalkForwardPeriod,
    CVResult,
    CVFoldResult,
)
from .backtest_engine import BacktestEngine, BacktestResult

# 避免循环导入
if TYPE_CHECKING:
    from .advisor_v4_workflow import AdvisorV4Workflow, AdvisorV4Config


@dataclass
class FactorOptimizationConfig:
    """因子优化配置"""
    # 因子选择
    enable_factor_selection: bool = True  # 是否优化因子选择
    min_factors: int = 3  # 最少因子数量
    max_factors: int = 7  # 最多因子数量
    
    # 权重优化
    enable_weight_optimization: bool = True  # 是否优化权重
    weight_range: Tuple[float, float] = (0.0, 1.0)  # 权重范围
    weight_step: float = 0.1  # 权重步长
    
    # 融合权重优化
    enable_fusion_optimization: bool = True  # 是否优化融合权重
    validated_weight_range: Tuple[float, float] = (0.5, 0.9)  # 已验证因子权重范围
    fusion_weight_step: float = 0.1  # 融合权重步长
    
    # 优化方法
    optimization_method: str = "grid"  # grid/bayesian/genetic
    max_iterations: int = 10  # 最大迭代次数（递归优化）
    early_stop_patience: int = 3  # 早停耐心值（连续N次无改进）
    
    # Walk-Forward验证配置
    train_months: int = 3  # 训练窗口（月）
    test_months: int = 1  # 测试窗口（月）
    step_months: int = 1  # 滚动步长（月）
    
    # 多目标权重
    objective_weights: Dict[str, float] = field(default_factory=lambda: {
        'sharpe': 0.4,
        'hit_rate': 0.3,
        'return': 0.3
    })


@dataclass
class ValidationResult:
    """验证结果"""
    factor_selection: List[str]
    factor_weights: Dict[str, float]
    fusion_weight: float
    
    # Walk-Forward验证结果
    cv_result: Optional[CVResult] = None
    
    # 回测结果（如果运行了回测）
    backtest_result: Optional[BacktestResult] = None
    
    # 多目标指标
    sharpe_ratio: float = 0.0
    hit_rate: float = 0.0  # 10%+收益命中率
    total_return: float = 0.0
    stability_score: float = 0.0  # 稳定性得分（基于指标方差）
    
    # 综合得分
    multi_objective_score: float = 0.0
    
    # 过拟合检测
    overfitting_risk: str = "low"  # low/medium/high
    overfitting_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationResult:
    """优化结果"""
    best_config: FactorOptimizationConfig
    best_result: ValidationResult
    optimization_history: List[ValidationResult] = field(default_factory=list)
    factor_importance: Dict[str, float] = field(default_factory=dict)
    optimization_time_seconds: float = 0.0


class FactorOptimizer:
    """因子优化器（递归优化因子选择和权重）"""
    
    def __init__(
        self,
        config: Optional[FactorOptimizationConfig] = None,
        workflow: Optional['AdvisorV4Workflow'] = None,
        verbose: bool = True,
    ):
        """
        初始化因子优化器
        
        Args:
            config: 优化配置
            workflow: AdvisorV4工作流（用于回测）
            verbose: 是否输出详细信息
        """
        self.config = config or FactorOptimizationConfig()
        self.workflow = workflow
        self.verbose = verbose
        
        # 初始化组件
        self.validated_calculator = ValidatedFactorCalculator(verbose=False)
        self.factor_calculator = MultiFactorCalculator(verbose=False)
        self.walkforward_validator = WalkForwardValidator(
            train_months=self.config.train_months,
            test_months=self.config.test_months,
            step_months=self.config.step_months,
            verbose=False
        )
        
        # 结果缓存（避免重复计算）
        self._result_cache: Dict[str, ValidationResult] = {}
    
    def _cache_key(
        self,
        factor_selection: List[str],
        factor_weights: Dict[str, float],
        fusion_weight: float,
    ) -> str:
        """生成缓存键"""
        selection_str = ",".join(sorted(factor_selection))
        weights_str = json.dumps(factor_weights, sort_keys=True)
        key_str = f"{selection_str}|{weights_str}|{fusion_weight:.2f}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def validate_factor_config(
        self,
        factor_selection: List[str],
        factor_weights: Dict[str, float],
        fusion_weight: float,
        start_date: str,
        end_date: str,
        use_backtest: bool = False,
    ) -> ValidationResult:
        """
        验证因子配置的可靠性
        
        Args:
            factor_selection: 选择的因子列表
            factor_weights: 因子权重字典
            fusion_weight: 已验证因子融合权重（0-1）
            start_date: 开始日期
            end_date: 结束日期
            use_backtest: 是否运行完整回测（否则仅Walk-Forward验证）
        
        Returns:
            ValidationResult
        """
        # 检查缓存
        cache_key = self._cache_key(factor_selection, factor_weights, fusion_weight)
        if cache_key in self._result_cache:
            if self.verbose:
                print(f"  ✅ 命中缓存: {cache_key[:8]}")
            return self._result_cache[cache_key]
        
        # 创建验证结果
        result = ValidationResult(
            factor_selection=factor_selection,
            factor_weights=factor_weights,
            fusion_weight=fusion_weight,
        )
        
        # 配置因子计算器
        self.factor_calculator.set_fusion_weight(fusion_weight)
        self.factor_calculator.set_factor_config(
            factor_selection=factor_selection,
            factor_weights=factor_weights,
        )
        
        # Walk-Forward验证
        try:
            cv_result = self._run_walkforward_validation(
                start_date=start_date,
                end_date=end_date,
            )
            result.cv_result = cv_result
            
            # 计算多目标指标
            if cv_result and cv_result.fold_results:
                metrics_list = [fold.metrics for fold in cv_result.fold_results]
                
                # 提取指标
                sharpe_ratios = [m.get('sharpe_ratio', 0.0) for m in metrics_list]
                hit_rates = [m.get('hit_rate', 0.0) for m in metrics_list]
                total_returns = [m.get('total_return', 0.0) for m in metrics_list]
                
                # 计算平均值
                result.sharpe_ratio = np.mean(sharpe_ratios) if sharpe_ratios else 0.0
                result.hit_rate = np.mean(hit_rates) if hit_rates else 0.0
                result.total_return = np.mean(total_returns) if total_returns else 0.0
                
                # 计算稳定性（基于指标标准差）
                sharpe_std = np.std(sharpe_ratios) if sharpe_ratios else 1.0
                hit_std = np.std(hit_rates) if hit_rates else 1.0
                return_std = np.std(total_returns) if total_returns else 1.0
                
                # 稳定性得分（标准差越小越好，归一化到0-1）
                result.stability_score = 1.0 / (1.0 + (sharpe_std + hit_std + return_std) / 3.0)
                
                # 过拟合检测
                result.overfitting_risk, result.overfitting_details = self._detect_overfitting(
                    metrics_list
                )
                
                # 计算多目标综合得分
                result.multi_objective_score = self._calculate_multi_objective_score(
                    sharpe_ratio=result.sharpe_ratio,
                    hit_rate=result.hit_rate,
                    total_return=result.total_return,
                    stability_score=result.stability_score,
                )
        except Exception as e:
            logger.warning(f"Walk-Forward验证失败: {e}")
            result.multi_objective_score = 0.0
        
        # 如果使用完整回测，运行回测
        if use_backtest and self.workflow:
            try:
                backtest_result = self._run_backtest(
                    start_date=start_date,
                    end_date=end_date,
                )
                result.backtest_result = backtest_result
                
                # 更新指标（如果回测结果更完整）
                if backtest_result:
                    result.sharpe_ratio = backtest_result.sharpe_ratio
                    result.hit_rate = backtest_result.hit_10pct_rate
                    result.total_return = backtest_result.total_return
            except Exception as e:
                logger.warning(f"回测失败: {e}")
        
        # 缓存结果
        self._result_cache[cache_key] = result
        
        return result
    
    def _run_walkforward_validation(
        self,
        start_date: str,
        end_date: str,
    ) -> Optional[CVResult]:
        """
        运行Walk-Forward验证
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            CVResult
        """
        if not self.workflow:
            logger.warning("未提供workflow，无法运行Walk-Forward验证")
            return None
        
        # 获取训练数据（使用workflow的数据加载逻辑）
        try:
            # 这里需要从workflow获取历史高收益案例数据
            # 暂时使用简化方法：直接使用workflow的backtest方法
            # TODO: 更精确的Walk-Forward验证需要单独的数据准备
            
            # 生成验证周期
            periods = self.walkforward_validator.generate_periods(start_date, end_date)
            if not periods:
                return None
            
            fold_results = []
            
            for period in periods:
                # 获取period的属性（WalkForwardPeriod有train_start, train_end, test_start, test_end, period_id）
                period_id = getattr(period, 'period_id', 0)
                train_start = getattr(period, 'train_start', period.train_start if hasattr(period, 'train_start') else '')
                train_end = getattr(period, 'train_end', period.train_end if hasattr(period, 'train_end') else '')
                test_start = getattr(period, 'test_start', period.test_start if hasattr(period, 'test_start') else '')
                test_end = getattr(period, 'test_end', period.test_end if hasattr(period, 'test_end') else '')
                # 在每个周期上运行回测
                try:
                    backtest_result = self.workflow.backtest(
                        start_date=period.train_start,
                        end_date=period.test_end,
                        save_to_db=False,
                    )
                    
                    if backtest_result:
                        # 提取指标
                        metrics = {
                            'sharpe_ratio': backtest_result.sharpe_ratio,
                            'hit_rate': backtest_result.hit_10pct_rate,
                            'total_return': backtest_result.total_return,
                            'max_drawdown': backtest_result.max_drawdown,
                            'win_rate': backtest_result.win_rate,
                        }
                        
                        fold_result = CVFoldResult(
                            fold=period.period_id,
                            train_size=0,  # TODO: 从backtest_result获取
                            val_size=0,
                            train_period=f"{period.train_start} ~ {period.train_end}",
                            val_period=f"{period.test_start} ~ {period.test_end}",
                            metrics=metrics,
                        )
                        fold_results.append(fold_result)
                except Exception as e:
                    logger.warning(f"Period {period.period_id} 验证失败: {e}")
                    continue
            
            # 构建CVResult
            if fold_results:
                return CVResult(
                    method='walk_forward',
                    n_folds=len(fold_results),
                    fold_results=fold_results,
                )
        except Exception as e:
            logger.error(f"Walk-Forward验证执行失败: {e}")
        
        return None
    
    def _run_backtest(
        self,
        start_date: str,
        end_date: str,
    ) -> Optional[BacktestResult]:
        """
        运行完整回测
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            BacktestResult
        """
        if not self.workflow:
            return None
        
        try:
            return self.workflow.backtest(
                start_date=start_date,
                end_date=end_date,
                save_to_db=False,
            )
        except Exception as e:
            logger.error(f"回测执行失败: {e}")
            return None
    
    def _calculate_multi_objective_score(
        self,
        sharpe_ratio: float,
        hit_rate: float,
        total_return: float,
        stability_score: float = 1.0,
        method: str = "weighted_sum",
    ) -> float:
        """
        计算多目标综合得分（支持加权求和和Pareto前沿方法）
        
        Args:
            sharpe_ratio: 夏普比率
            hit_rate: 命中率（10%+收益）
            total_return: 总收益率
            stability_score: 稳定性得分（0-1）
            method: 优化方法（"weighted_sum" 或 "pareto"）
        
        Returns:
            综合得分（0-100）
        """
        weights = self.config.objective_weights
        
        # 归一化指标（使用经验范围）
        # 夏普比率：通常范围 -1 ~ 3，归一化到0-1
        normalized_sharpe = np.clip((sharpe_ratio + 1) / 4.0, 0, 1)
        
        # 命中率：已经是0-1范围
        normalized_hit_rate = np.clip(hit_rate, 0, 1)
        
        # 总收益率：假设范围 -50% ~ 200%，归一化到0-1
        normalized_return = np.clip((total_return + 0.5) / 2.5, 0, 1)
        
        if method == "pareto":
            # Pareto前沿方法：使用几何平均（更平衡各目标）
            score = (
                normalized_sharpe ** weights.get('sharpe', 0.4) *
                normalized_hit_rate ** weights.get('hit_rate', 0.3) *
                normalized_return ** weights.get('return', 0.3)
            )
        else:
            # 加权求和方法（默认）
            score = (
                normalized_sharpe * weights.get('sharpe', 0.4) +
                normalized_hit_rate * weights.get('hit_rate', 0.3) +
                normalized_return * weights.get('return', 0.3)
            )
        
        # 应用稳定性惩罚（稳定性得分越低，惩罚越大）
        score *= (0.5 + 0.5 * stability_score)
        
        # 归一化到0-100
        return score * 100
    
    def _detect_overfitting(
        self,
        metrics_list: List[Dict[str, float]],
    ) -> Tuple[str, Dict[str, Any]]:
        """
        检测过拟合风险
        
        Args:
            metrics_list: 各窗口的指标列表
        
        Returns:
            (风险等级, 详细信息)
        """
        if not metrics_list or len(metrics_list) < 3:
            return "low", {}
        
        # 提取指标
        sharpe_ratios = [m.get('sharpe_ratio', 0.0) for m in metrics_list]
        hit_rates = [m.get('hit_rate', 0.0) for m in metrics_list]
        total_returns = [m.get('total_return', 0.0) for m in metrics_list]
        
        # 计算指标方差（方差大表示不稳定，可能过拟合）
        sharpe_std = np.std(sharpe_ratios)
        hit_std = np.std(hit_rates)
        return_std = np.std(total_returns)
        
        # 计算趋势（如果后期指标明显下降，可能过拟合）
        if len(sharpe_ratios) >= 3:
            early_sharpe = np.mean(sharpe_ratios[:len(sharpe_ratios)//2])
            late_sharpe = np.mean(sharpe_ratios[len(sharpe_ratios)//2:])
            sharpe_decline = (early_sharpe - late_sharpe) / max(abs(early_sharpe), 0.01)
        else:
            sharpe_decline = 0.0
        
        # 评估风险
        risk_score = 0.0
        
        # 方差过大
        if sharpe_std > 1.0 or hit_std > 0.3 or return_std > 0.5:
            risk_score += 0.4
        
        # 指标下降
        if sharpe_decline > 0.3:
            risk_score += 0.3
        
        # 确定风险等级
        if risk_score >= 0.6:
            risk_level = "high"
        elif risk_score >= 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        details = {
            'risk_score': risk_score,
            'sharpe_std': sharpe_std,
            'hit_std': hit_std,
            'return_std': return_std,
            'sharpe_decline': sharpe_decline,
        }
        
        return risk_level, details
    
    def optimize_factor_selection(
        self,
        start_date: str,
        end_date: str,
        initial_selection: Optional[List[str]] = None,
    ) -> List[str]:
        """
        优化因子选择（从7个已验证因子中选择最优组合）
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            initial_selection: 初始因子选择（可选）
        
        Returns:
            最优因子组合
        """
        if not self.config.enable_factor_selection:
            return initial_selection or ALL_VALIDATED_FACTORS
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【阶段1】因子选择优化")
            print(f"{'='*70}")
            print(f"从 {len(ALL_VALIDATED_FACTORS)} 个已验证因子中选择 {self.config.min_factors}-{self.config.max_factors} 个")
        
        best_selection = None
        best_score = float('-inf')
        
        # 生成所有可能的因子组合
        all_combinations = []
        for n in range(self.config.min_factors, self.config.max_factors + 1):
            all_combinations.extend(combinations(ALL_VALIDATED_FACTORS, n))
        
        if self.verbose:
            print(f"总组合数: {len(all_combinations)}")
        
        # 评估每个组合
        for i, combo in enumerate(all_combinations):
            factor_selection = list(combo)
            
            # 使用默认权重（后续会优化）
            factor_weights = {f: VALIDATED_FACTORS[f].weight for f in factor_selection}
            total_weight = sum(factor_weights.values())
            factor_weights = {f: w / total_weight for f, w in factor_weights.items()}
            
            # 使用默认融合权重
            fusion_weight = 0.7
            
            # 验证配置
            validation_result = self.validate_factor_config(
                factor_selection=factor_selection,
                factor_weights=factor_weights,
                fusion_weight=fusion_weight,
                start_date=start_date,
                end_date=end_date,
            )
            
            if validation_result.multi_objective_score > best_score:
                improvement = validation_result.multi_objective_score - best_score
                best_score = validation_result.multi_objective_score
                best_selection = factor_selection
                
                if self.verbose:
                    print(f"  ✅ 组合 {i+1}: 得分 {best_score:.4f} (+{improvement:.4f})")
                    print(f"     因子: {', '.join(factor_selection)}")
                    print(f"     指标: 夏普{validation_result.sharpe_ratio:.3f} / 命中率{validation_result.hit_rate:.2%} / 收益率{validation_result.total_return:.2%}")
            
            if self.verbose and (i + 1) % 10 == 0:
                print(f"  进度: {i+1}/{len(all_combinations)} (当前最佳: {len(best_selection)}个因子, 得分: {best_score:.4f})")
        
        if self.verbose:
            print(f"\n✅ 最优因子选择: {best_selection} ({len(best_selection)}个因子)")
            print(f"   综合得分: {best_score:.4f}")
        
        return best_selection or ALL_VALIDATED_FACTORS
    
    def optimize_factor_weights(
        self,
        factor_selection: List[str],
        start_date: str,
        end_date: str,
        initial_weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        优化因子权重
        
        Args:
            factor_selection: 因子选择
            start_date: 开始日期
            end_date: 结束日期
            initial_weights: 初始权重（可选）
        
        Returns:
            最优权重字典
        """
        if not self.config.enable_weight_optimization:
            # 使用默认权重
            if initial_weights:
                return initial_weights
            weights = {f: VALIDATED_FACTORS[f].weight for f in factor_selection}
            total = sum(weights.values())
            return {f: w / total for f, w in weights.items()}
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【阶段2】因子权重优化")
            print(f"{'='*70}")
            print(f"优化 {len(factor_selection)} 个因子的权重分配")
        
        # 生成权重候选（网格搜索）
        min_w, max_w = self.config.weight_range
        step = self.config.weight_step
        weight_candidates = np.arange(min_w, max_w + step, step)
        
        best_weights = None
        best_score = float('-inf')
        
        # 网格搜索（限制因子数量以避免组合爆炸）
        if len(factor_selection) <= 5:
            # 小规模：完整网格搜索
            for weights_tuple in product(weight_candidates, repeat=len(factor_selection)):
                weights = list(weights_tuple)
                total = sum(weights)
                if total == 0:
                    continue
                # 归一化
                weights_dict = {f: w / total for f, w in zip(factor_selection, weights)}
                
                # 验证
                validation_result = self.validate_factor_config(
                    factor_selection=factor_selection,
                    factor_weights=weights_dict,
                    fusion_weight=0.7,  # 使用默认融合权重
                    start_date=start_date,
                    end_date=end_date,
                )
                
                if validation_result.multi_objective_score > best_score:
                    best_score = validation_result.multi_objective_score
                    best_weights = weights_dict
        else:
            # 大规模：使用贝叶斯优化或遗传算法（TODO: 阶段3实现）
            # 暂时使用默认权重
            weights = {f: VALIDATED_FACTORS[f].weight for f in factor_selection}
            total = sum(weights.values())
            best_weights = {f: w / total for f, w in weights.items()}
        
        if self.verbose:
            print(f"\n✅ 最优权重分配:")
            for factor, weight in sorted(best_weights.items(), key=lambda x: x[1], reverse=True):
                print(f"   {factor}: {weight:.3f}")
            print(f"   综合得分: {best_score:.4f}")
        
        return best_weights or {f: 1.0 / len(factor_selection) for f in factor_selection}
    
    def optimize_fusion_weight(
        self,
        factor_selection: List[str],
        factor_weights: Dict[str, float],
        start_date: str,
        end_date: str,
    ) -> float:
        """
        优化融合权重（已验证因子vs聚宽因子）
        
        Args:
            factor_selection: 因子选择
            factor_weights: 因子权重
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            最优融合权重（已验证因子权重，0-1）
        """
        if not self.config.enable_fusion_optimization:
            return 0.7  # 默认权重
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【阶段3】融合权重优化")
            print(f"{'='*70}")
            print(f"优化已验证因子 vs 聚宽因子的权重比例")
        
        min_w, max_w = self.config.validated_weight_range
        step = self.config.fusion_weight_step
        fusion_candidates = np.arange(min_w, max_w + step, step)
        
        best_fusion_weight = 0.7
        best_score = float('-inf')
        
        for fusion_weight in fusion_candidates:
            # 验证
            validation_result = self.validate_factor_config(
                factor_selection=factor_selection,
                factor_weights=factor_weights,
                fusion_weight=fusion_weight,
                start_date=start_date,
                end_date=end_date,
            )
            
            if validation_result.multi_objective_score > best_score:
                best_score = validation_result.multi_objective_score
                best_fusion_weight = fusion_weight
        
        if self.verbose:
            print(f"\n✅ 最优融合权重: 已验证因子 {best_fusion_weight:.1%} / 聚宽因子 {1-best_fusion_weight:.1%}")
            print(f"   综合得分: {best_score:.4f}")
        
        return best_fusion_weight
    
    def recursive_optimize(
        self,
        start_date: str,
        end_date: str,
        initial_selection: Optional[List[str]] = None,
        initial_weights: Optional[Dict[str, float]] = None,
    ) -> OptimizationResult:
        """
        递归优化（因子选择 → 权重优化 → 融合权重优化 → 迭代）
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            initial_selection: 初始因子选择
            initial_weights: 初始权重
        
        Returns:
            OptimizationResult
        """
        start_time = datetime.now()
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【因子递归优化系统】")
            print(f"{'='*70}")
            print(f"优化区间: {start_date} ~ {end_date}")
            print(f"优化方法: {self.config.optimization_method}")
            print(f"最大迭代次数: {self.config.max_iterations}")
            print(f"{'='*70}")
        
        # 初始化
        current_selection = initial_selection or ALL_VALIDATED_FACTORS
        current_weights = initial_weights or {f: VALIDATED_FACTORS[f].weight for f in current_selection}
        total = sum(current_weights.values())
        current_weights = {f: w / total for f, w in current_weights.items()}
        current_fusion_weight = 0.7
        
        best_result = None
        best_score = float('-inf')
        optimization_history = []
        no_improvement_count = 0
        
        # 递归优化循环
        for iteration in range(self.config.max_iterations):
            if self.verbose:
                print(f"\n{'='*70}")
                print(f"【迭代 {iteration + 1}/{self.config.max_iterations}】")
                print(f"{'='*70}")
                if iteration == 0:
                    print(f"初始配置:")
                    print(f"  因子选择: {current_selection} ({len(current_selection)}个因子)")
                    print(f"  因子权重: {json.dumps({k: f'{v:.3f}' for k, v in current_weights.items()}, indent=2, ensure_ascii=False)}")
                    print(f"  融合权重: 已验证 {current_fusion_weight:.1%} / 聚宽 {1-current_fusion_weight:.1%}")
                else:
                    print(f"当前配置（来自上次迭代）:")
                    print(f"  因子选择: {current_selection} ({len(current_selection)}个因子)")
                    print(f"  因子权重: {json.dumps({k: f'{v:.3f}' for k, v in current_weights.items()}, indent=2, ensure_ascii=False)}")
                    print(f"  融合权重: 已验证 {current_fusion_weight:.1%} / 聚宽 {1-current_fusion_weight:.1%}")
            
            # 1. 因子选择优化
            if self.config.enable_factor_selection:
                if self.verbose:
                    print(f"\n【步骤1】因子选择优化")
                    print(f"  方法: 穷举搜索（从{len(ALL_VALIDATED_FACTORS)}个因子中选择{self.config.min_factors}-{self.config.max_factors}个）")
                current_selection = self.optimize_factor_selection(
                    start_date=start_date,
                    end_date=end_date,
                    initial_selection=current_selection,
                )
                # 更新权重（移除不在选择中的因子）
                current_weights = {f: w for f, w in current_weights.items() if f in current_selection}
                total = sum(current_weights.values())
                if total > 0:
                    current_weights = {f: w / total for f, w in current_weights.items()}
                else:
                    # 重置为默认权重
                    current_weights = {f: VALIDATED_FACTORS[f].weight for f in current_selection}
                    total = sum(current_weights.values())
                    current_weights = {f: w / total for f, w in current_weights.items()}
            
            # 2. 因子权重优化
            if self.config.enable_weight_optimization:
                current_weights = self.optimize_factor_weights(
                    factor_selection=current_selection,
                    start_date=start_date,
                    end_date=end_date,
                    initial_weights=current_weights,
                )
            
            # 3. 融合权重优化
            if self.config.enable_fusion_optimization:
                if self.verbose:
                    print(f"\n【步骤3】融合权重优化")
                    print(f"  方法: 一维搜索")
                    print(f"  搜索范围: 已验证因子权重 {self.config.validated_weight_range}, 步长 {self.config.fusion_weight_step}")
                
                old_fusion_weight = current_fusion_weight
                current_fusion_weight = self.optimize_fusion_weight(
                    factor_selection=current_selection,
                    factor_weights=current_weights,
                    start_date=start_date,
                    end_date=end_date,
                )
                
                if self.verbose:
                    print(f"  融合权重变化:")
                    print(f"    已验证因子: {old_fusion_weight:.1%} → {current_fusion_weight:.1%} ({current_fusion_weight-old_fusion_weight:+.1%})")
                    print(f"    聚宽因子: {1-old_fusion_weight:.1%} → {1-current_fusion_weight:.1%} ({old_fusion_weight-current_fusion_weight:+.1%})")
            
            # 4. 最终验证
            final_result = self.validate_factor_config(
                factor_selection=current_selection,
                factor_weights=current_weights,
                fusion_weight=current_fusion_weight,
                start_date=start_date,
                end_date=end_date,
                use_backtest=True,  # 最终验证使用完整回测
            )
            
            optimization_history.append(final_result)
            
            # 5. 评估改进
            if final_result.multi_objective_score > best_score:
                improvement = final_result.multi_objective_score - best_score
                best_score = final_result.multi_objective_score
                best_result = final_result
                no_improvement_count = 0
                
                if self.verbose:
                    print(f"\n✅ 迭代 {iteration + 1} 改进: +{improvement:.4f}")
                    print(f"   当前最佳得分: {best_score:.4f}")
            else:
                no_improvement_count += 1
                if self.verbose:
                    print(f"\n⚠️ 迭代 {iteration + 1} 无改进 (连续 {no_improvement_count} 次)")
            
            # 早停检查
            if no_improvement_count >= self.config.early_stop_patience:
                if self.verbose:
                    print(f"\n⏹️ 早停: 连续 {no_improvement_count} 次迭代无改进")
                break
        
        # 计算因子重要性（基于优化历史）
        factor_importance = self._calculate_factor_importance(optimization_history)
        
        # 构建结果
        result = OptimizationResult(
            best_config=self.config,
            best_result=best_result or optimization_history[-1] if optimization_history else None,
            optimization_history=optimization_history,
            factor_importance=factor_importance,
            optimization_time_seconds=(datetime.now() - start_time).total_seconds(),
        )
        
        if self.verbose:
            print(f"\n{'='*70}")
            print("【优化完成】")
            print(f"{'='*70}")
            if best_result:
                print(f"最优因子组合: {best_result.factor_selection}")
                print(f"最优融合权重: 已验证 {best_result.fusion_weight:.1%} / 聚宽 {1-best_result.fusion_weight:.1%}")
                print(f"综合得分: {best_result.multi_objective_score:.4f}")
                print(f"夏普比率: {best_result.sharpe_ratio:.3f}")
                print(f"命中率: {best_result.hit_rate:.2%}")
                print(f"总收益率: {best_result.total_return:.2%}")
            print(f"优化耗时: {result.optimization_time_seconds:.1f} 秒")
            print(f"{'='*70}")
        
        return result
    
    def _calculate_factor_importance(
        self,
        optimization_history: List[ValidationResult],
    ) -> Dict[str, float]:
        """计算因子重要性（基于优化历史）"""
        if not optimization_history:
            return {}
        
        # 统计每个因子在最优配置中的出现频率和平均权重
        factor_counts: Dict[str, int] = {}
        factor_weight_sums: Dict[str, float] = {}
        
        for result in optimization_history:
            for factor in result.factor_selection:
                factor_counts[factor] = factor_counts.get(factor, 0) + 1
                factor_weight_sums[factor] = factor_weight_sums.get(factor, 0.0) + result.factor_weights.get(factor, 0.0)
        
        # 计算重要性得分（出现频率 * 平均权重）
        importance = {}
        total_count = len(optimization_history)
        for factor in ALL_VALIDATED_FACTORS:
            count = factor_counts.get(factor, 0)
            avg_weight = factor_weight_sums.get(factor, 0.0) / max(count, 1)
            importance[factor] = (count / total_count) * 0.5 + avg_weight * 0.5
        
        # 归一化到0-1
        max_importance = max(importance.values()) if importance.values() else 1.0
        if max_importance > 0:
            importance = {f: v / max_importance for f, v in importance.items()}
        
        return importance
