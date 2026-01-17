#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进化反馈分析器

分析回测结果，识别失败原因，生成优化建议，并反馈到下一轮进化。
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
import numpy as np
import logging

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

from core.bullettrade.recursive_backtest_engine import StandardizedBacktestResult
from core.evolution.bull_market_strategy_evolver import Individual

logger = logging.getLogger(__name__)


@dataclass
class FailureReason:
    """失败原因"""
    reason_type: str            # 原因类型（'low_return', 'high_drawdown', 'low_sharpe', 'factor_failure', 'parameter_issue'）
    description: str            # 描述
    severity: float             # 严重程度（0-1）
    affected_params: List[str]  # 受影响的参数


@dataclass
class OptimizationSuggestion:
    """优化建议"""
    suggestion_type: str        # 建议类型（'adjust_param', 'modify_logic', 'change_weight'）
    target_param: Optional[str]  # 目标参数
    direction: str              # 调整方向（'increase', 'decrease', 'modify'）
    magnitude: float            # 调整幅度（0-1）
    description: str            # 描述
    confidence: float           # 置信度（0-1）


@dataclass
class FeedbackAnalysis:
    """反馈分析结果"""
    # 分析结果
    success_rate: float         # 成功率（满足目标的个体比例）
    avg_monthly_return: float   # 平均月收益率
    avg_max_drawdown: float     # 平均最大回撤
    avg_sharpe_ratio: float     # 平均夏普比率
    
    # 失败分析
    failure_reasons: List[FailureReason] = field(default_factory=list)
    
    # 优化建议
    suggestions: List[OptimizationSuggestion] = field(default_factory=list)
    
    # 参数相关性分析
    param_correlations: Dict[str, float] = field(default_factory=dict)  # 参数与月收益率的相关性
    
    # 下一轮调整建议
    param_adjustments: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # 参数空间调整建议


class EvolutionFeedbackAnalyzer:
    """进化反馈分析器"""
    
    def __init__(self, target_monthly_return: float = 0.30, verbose: bool = True):
        """
        初始化反馈分析器
        
        Args:
            target_monthly_return: 目标月回报率
            verbose: 是否输出详细信息
        """
        self.target_monthly_return = target_monthly_return
        self.verbose = verbose
    
    def analyze_population(self, population: List[Individual]) -> FeedbackAnalysis:
        """
        分析种群结果
        
        Args:
            population: 种群个体列表
        
        Returns:
            FeedbackAnalysis
        """
        if not population:
            return FeedbackAnalysis(
                success_rate=0.0,
                avg_monthly_return=0.0,
                avg_max_drawdown=0.0,
                avg_sharpe_ratio=0.0
            )
        
        # 提取有效结果
        valid_results = [
            ind.backtest_result for ind in population
            if ind.backtest_result and ind.backtest_result.monthly_return >= -1.0
        ]
        
        if not valid_results:
            return FeedbackAnalysis(
                success_rate=0.0,
                avg_monthly_return=0.0,
                avg_max_drawdown=0.0,
                avg_sharpe_ratio=0.0
            )
        
        # 计算基本统计
        monthly_returns = [r.monthly_return for r in valid_results]
        max_drawdowns = [r.max_drawdown for r in valid_results]
        sharpe_ratios = [r.sharpe_ratio for r in valid_results]
        
        success_count = sum([r.meets_target(target_monthly_return=self.target_monthly_return) for r in valid_results])
        success_rate = success_count / len(valid_results)
        
        # 识别失败原因
        failure_reasons = self._identify_failure_reasons(population, valid_results)
        
        # 生成优化建议
        suggestions = self._generate_suggestions(population, valid_results, failure_reasons)
        
        # 参数相关性分析
        param_correlations = self._analyze_param_correlations(population, valid_results)
        
        # 参数空间调整建议
        param_adjustments = self._suggest_param_adjustments(population, valid_results, param_correlations)
        
        analysis = FeedbackAnalysis(
            success_rate=success_rate,
            avg_monthly_return=np.mean(monthly_returns),
            avg_max_drawdown=np.mean(max_drawdowns),
            avg_sharpe_ratio=np.mean(sharpe_ratios),
            failure_reasons=failure_reasons,
            suggestions=suggestions,
            param_correlations=param_correlations,
            param_adjustments=param_adjustments,
        )
        
        if self.verbose:
            self._print_analysis(analysis)
        
        return analysis
    
    def _identify_failure_reasons(
        self,
        population: List[Individual],
        results: List[StandardizedBacktestResult]
    ) -> List[FailureReason]:
        """识别失败原因"""
        reasons = []
        
        # 分析每个失败的个体
        for i, result in enumerate(results):
            if result.meets_target(target_monthly_return=self.target_monthly_return):
                continue
            
            individual = population[i] if i < len(population) else None
            
            # 原因1: 月收益率过低
            if result.monthly_return < self.target_monthly_return * 0.5:
                reasons.append(FailureReason(
                    reason_type='low_return',
                    description=f"月收益率过低: {result.monthly_return*100:.2f}% < {self.target_monthly_return*100:.0f}%",
                    severity=1.0 - (result.monthly_return / self.target_monthly_return),
                    affected_params=['min_total_score', 'max_stocks', 'momentum_20d_weight', 'rebalance_days']
                ))
            
            # 原因2: 最大回撤过大
            if result.max_drawdown < -0.20:
                reasons.append(FailureReason(
                    reason_type='high_drawdown',
                    description=f"最大回撤过大: {result.max_drawdown*100:.2f}% < -20%",
                    severity=abs(result.max_drawdown + 0.20) / 0.20,
                    affected_params=['stop_loss', 'trailing_stop', 'single_position_max']
                ))
            
            # 原因3: 夏普比率过低
            if result.sharpe_ratio < 2.0:
                reasons.append(FailureReason(
                    reason_type='low_sharpe',
                    description=f"夏普比率过低: {result.sharpe_ratio:.2f} < 2.0",
                    severity=1.0 - (result.sharpe_ratio / 2.0),
                    affected_params=['rebalance_days', 'stop_loss', 'take_profit']
                ))
            
            # 原因4: 交易次数过少（可能选股质量有问题）
            if result.total_trades < 10:
                reasons.append(FailureReason(
                    reason_type='few_trades',
                    description=f"交易次数过少: {result.total_trades} < 10",
                    severity=0.5,
                    affected_params=['min_total_score', 'max_stocks', 'rebalance_days']
                ))
        
        # 去重并汇总
        unique_reasons = {}
        for reason in reasons:
            key = reason.reason_type
            if key not in unique_reasons or reason.severity > unique_reasons[key].severity:
                unique_reasons[key] = reason
        
        return list(unique_reasons.values())
    
    def _generate_suggestions(
        self,
        population: List[Individual],
        results: List[StandardizedBacktestResult],
        failure_reasons: List[FailureReason]
    ) -> List[OptimizationSuggestion]:
        """生成优化建议"""
        suggestions = []
        
        # 基于失败原因生成建议
        for reason in failure_reasons:
            if reason.reason_type == 'low_return':
                # 月收益率过低：提高选股标准、增加持仓数量、提高动量权重
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='min_total_score',
                    direction='increase',
                    magnitude=0.1,
                    description=f"提高最低选股分数，提升选股质量",
                    confidence=0.7
                ))
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='momentum_20d_weight',
                    direction='increase',
                    magnitude=0.05,
                    description=f"提高动量因子权重，捕捉趋势机会",
                    confidence=0.6
                ))
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='max_stocks',
                    direction='increase',
                    magnitude=0.1,
                    description=f"增加持仓数量，分散风险同时提高收益潜力",
                    confidence=0.5
                ))
            
            elif reason.reason_type == 'high_drawdown':
                # 最大回撤过大：收紧止损、降低仓位
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='stop_loss',
                    direction='increase',  # stop_loss是负数，increase表示更严格的止损（如-8% -> -6%）
                    magnitude=0.1,
                    description=f"收紧止损阈值，控制回撤",
                    confidence=0.8
                ))
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='single_position_max',
                    direction='decrease',
                    magnitude=0.1,
                    description=f"降低单票最大仓位，分散风险",
                    confidence=0.7
                ))
            
            elif reason.reason_type == 'low_sharpe':
                # 夏普比率过低：优化调仓频率、平衡收益和风险
                suggestions.append(OptimizationSuggestion(
                    suggestion_type='adjust_param',
                    target_param='rebalance_days',
                    direction='modify',
                    magnitude=0.2,
                    description=f"优化调仓频率，平衡交易成本和收益",
                    confidence=0.6
                ))
        
        # 基于参数相关性生成建议
        # （将在_analyze_param_correlations中实现）
        
        return suggestions
    
    def _analyze_param_correlations(
        self,
        population: List[Individual],
        results: List[StandardizedBacktestResult]
    ) -> Dict[str, float]:
        """分析参数与月收益率的相关性"""
        correlations = {}
        
        if len(population) != len(results) or len(population) < 3:
            return correlations
        
        # 提取所有参数名
        param_names = list(population[0].params.keys()) if population else []
        
        # 月收益率列表
        monthly_returns = [r.monthly_return for r in results]
        
        # 计算每个参数与月收益率的相关性
        for param_name in param_names:
            param_values = [ind.params.get(param_name, 0.0) for ind in population]
            
            if len(param_values) == len(monthly_returns) and len(set(param_values)) > 1:
                try:
                    correlation = np.corrcoef(param_values, monthly_returns)[0, 1]
                    if not np.isnan(correlation):
                        correlations[param_name] = float(correlation)
                except Exception as e:
                    logger.debug(f"计算参数{param_name}相关性失败: {e}")
        
        return correlations
    
    def _suggest_param_adjustments(
        self,
        population: List[Individual],
        results: List[StandardizedBacktestResult],
        correlations: Dict[str, float]
    ) -> Dict[str, Dict[str, Any]]:
        """建议参数空间调整"""
        adjustments = {}
        
        # 找出与月收益率正相关和负相关的参数
        positive_params = [p for p, c in correlations.items() if c > 0.3]
        negative_params = [p for p, c in correlations.items() if c < -0.3]
        
        # 对于正相关参数：如果当前值偏低，建议提高上限
        for param in positive_params:
            current_values = [ind.params.get(param, 0.0) for ind in population]
            avg_value = np.mean(current_values)
            max_value = np.max(current_values)
            
            # 如果平均值和最大值都比较低，建议提高上限
            if avg_value < max_value * 0.7:
                adjustments[param] = {
                    'action': 'increase_max',
                    'current_max': max_value,
                    'suggested_max': max_value * 1.2,
                    'reason': f"正相关参数，当前值偏低，建议提高上限"
                }
        
        # 对于负相关参数：如果当前值偏高，建议降低下限
        for param in negative_params:
            current_values = [ind.params.get(param, 0.0) for ind in population]
            avg_value = np.mean(current_values)
            min_value = np.min(current_values)
            
            # 如果平均值和最小值都比较高，建议降低下限
            if avg_value > min_value * 1.3:
                adjustments[param] = {
                    'action': 'decrease_min',
                    'current_min': min_value,
                    'suggested_min': min_value * 0.8,
                    'reason': f"负相关参数，当前值偏高，建议降低下限"
                }
        
        return adjustments
    
    def _print_analysis(self, analysis: FeedbackAnalysis):
        """打印分析结果"""
        print(f"\n{'='*70}")
        print("进化反馈分析")
        print(f"{'='*70}")
        print(f"成功率: {analysis.success_rate*100:.1f}% ({len([r for r in analysis.failure_reasons if not r])}/{len(analysis.failure_reasons) if analysis.failure_reasons else 1})")
        print(f"平均月收益率: {analysis.avg_monthly_return*100:.2f}%")
        print(f"平均最大回撤: {analysis.avg_max_drawdown*100:.2f}%")
        print(f"平均夏普比率: {analysis.avg_sharpe_ratio:.2f}")
        
        if analysis.failure_reasons:
            print(f"\n失败原因 ({len(analysis.failure_reasons)}):")
            for i, reason in enumerate(analysis.failure_reasons, 1):
                print(f"  {i}. [{reason.reason_type}] {reason.description}")
                print(f"     严重程度: {reason.severity:.2f}, 影响参数: {', '.join(reason.affected_params[:3])}")
        
        if analysis.suggestions:
            print(f"\n优化建议 ({len(analysis.suggestions)}):")
            for i, suggestion in enumerate(analysis.suggestions[:5], 1):  # 只显示前5个
                print(f"  {i}. [{suggestion.suggestion_type}] {suggestion.description}")
                if suggestion.target_param:
                    print(f"     参数: {suggestion.target_param}, 方向: {suggestion.direction}, 置信度: {suggestion.confidence:.2f}")
        
        if analysis.param_correlations:
            print(f"\n参数相关性 (Top 5):")
            sorted_corr = sorted(analysis.param_correlations.items(), key=lambda x: abs(x[1]), reverse=True)
            for param, corr in sorted_corr[:5]:
                print(f"  {param}: {corr:+.3f}")
        
        if analysis.param_adjustments:
            print(f"\n参数空间调整建议 ({len(analysis.param_adjustments)}):")
            for param, adj in list(analysis.param_adjustments.items())[:3]:  # 只显示前3个
                print(f"  {param}: {adj['action']} - {adj['reason']}")


def main():
    """主函数：示例用法"""
    # 创建模拟数据
    from core.evolution.bull_market_strategy_evolver import Individual
    
    population = []
    for i in range(10):
        individual = Individual(
            params={
                'max_stocks': 10,
                'min_total_score': 30.0,
                'momentum_20d_weight': 0.20,
                'rebalance_days': 5,
            },
            fitness=10.0 + i * 2.0
        )
        
        # 模拟回测结果
        from core.bullettrade.recursive_backtest_engine import StandardizedBacktestResult
        individual.backtest_result = StandardizedBacktestResult(
            backtest_id=f"bt_{i}",
            start_date='2024-10-01',
            end_date='2024-12-31',
            initial_capital=1000000.0,
            total_return=0.10 + i * 0.02,
            annual_return=0.30,
            monthly_return=0.05 + i * 0.01,  # 0.05 ~ 0.14
            sharpe_ratio=1.5 + i * 0.2,
            max_drawdown=-0.15 - i * 0.02,
            win_rate=0.5 + i * 0.02,
            total_trades=20 + i * 5,
            avg_holding_period=10.0,
            volatility=0.20,
            calmar_ratio=2.0,
            strategy_params=individual.params,
        )
        population.append(individual)
    
    # 分析
    analyzer = EvolutionFeedbackAnalyzer(target_monthly_return=0.30, verbose=True)
    analysis = analyzer.analyze_population(population)
    
    print(f"\n分析完成，共 {len(analysis.suggestions)} 条优化建议")


if __name__ == '__main__':
    main()
