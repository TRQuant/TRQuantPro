# -*- coding: utf-8 -*-
"""
参数优化框架
============

基于网格搜索和交叉验证优化市场类型判断参数

功能:
1. 网格搜索最优参数
2. 交叉验证避免过拟合
3. 参数敏感性分析
4. 性能优化（并行计算、缓存）

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
import numpy as np
from itertools import product

logger = logging.getLogger(__name__)


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, float]
    best_score: float
    optimization_history: List[Dict] = field(default_factory=list)
    param_importance: Dict[str, float] = field(default_factory=dict)


class ParameterOptimizer:
    """
    参数优化器
    
    使用网格搜索和交叉验证优化参数
    """
    
    def __init__(self):
        """初始化优化器"""
        self.optimization_history: List[Dict] = []
    
    def grid_search(
        self,
        classifier_class,
        train_periods: List[Tuple[str, str]],
        validate_periods: List[Tuple[str, str]],
        param_grid: Dict[str, List[float]],
        score_metric: str = "accuracy",
    ) -> OptimizationResult:
        """
        网格搜索最优参数
        
        Args:
            classifier_class: 分类器类
            train_periods: 训练时间段列表
            validate_periods: 验证时间段列表
            param_grid: 参数网格 {param_name: [values]}
            score_metric: 评分指标 ("accuracy", "f1_score", "custom")
        
        Returns:
            OptimizationResult
        """
        logger.info("="*60)
        logger.info("参数网格搜索优化")
        logger.info("="*60)
        
        # 生成所有参数组合
        param_names = list(param_grid.keys())
        param_values = list(param_grid.values())
        param_combinations = list(product(*param_values))
        
        total_combinations = len(param_combinations)
        logger.info(f"参数组合数: {total_combinations}")
        
        best_score = -np.inf
        best_params = None
        optimization_history = []
        
        for i, param_values_tuple in enumerate(param_combinations, 1):
            params = dict(zip(param_names, param_values_tuple))
            
            if i % 10 == 0:
                logger.info(f"进度: {i}/{total_combinations} ({i*100//total_combinations}%)")
            
            # 交叉验证
            scores = []
            for train_period, validate_period in zip(train_periods, validate_periods):
                try:
                    # 创建分类器（使用当前参数）
                    classifier = self._create_classifier_with_params(
                        classifier_class,
                        params,
                    )
                    
                    # 验证
                    score = self._validate_classifier(
                        classifier,
                        validate_period[0],
                        validate_period[1],
                        score_metric,
                    )
                    
                    if score is not None:
                        scores.append(score)
                except Exception as e:
                    logger.warning(f"参数组合 {params} 验证失败: {e}")
                    continue
            
            if scores:
                avg_score = np.mean(scores)
                optimization_history.append({
                    "params": params,
                    "score": avg_score,
                    "scores": scores,
                })
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_params = params.copy()
                    logger.info(f"  新最优参数: {params}, 得分: {avg_score:.4f}")
        
        # 计算参数重要性
        param_importance = self._calculate_param_importance(optimization_history)
        
        result = OptimizationResult(
            best_params=best_params or {},
            best_score=best_score,
            optimization_history=optimization_history,
            param_importance=param_importance,
        )
        
        logger.info(f"\n优化完成:")
        logger.info(f"  最优参数: {best_params}")
        logger.info(f"  最优得分: {best_score:.4f}")
        
        return result
    
    def _create_classifier_with_params(
        self,
        classifier_class,
        params: Dict[str, float],
    ):
        """使用指定参数创建分类器"""
        # 这里需要根据实际分类器实现调整
        # 假设分类器可以通过参数初始化
        classifier = classifier_class()
        
        # 更新阈值
        if hasattr(classifier, 'base_thresholds'):
            for key, value in params.items():
                if key in classifier.base_thresholds:
                    classifier.base_thresholds[key] = value
        
        return classifier
    
    def _validate_classifier(
        self,
        classifier,
        start_date: str,
        end_date: str,
        score_metric: str,
    ) -> Optional[float]:
        """验证分类器并返回得分"""
        # 这里需要实现验证逻辑
        # 简化版：返回随机得分（实际应调用验证框架）
        return None
    
    def _calculate_param_importance(
        self,
        optimization_history: List[Dict],
    ) -> Dict[str, float]:
        """计算参数重要性"""
        if not optimization_history:
            return {}
        
        # 使用相关性分析计算参数重要性
        param_importance = {}
        
        # 提取参数和得分
        param_names = set()
        for record in optimization_history:
            param_names.update(record["params"].keys())
        
        for param_name in param_names:
            param_values = []
            scores = []
            
            for record in optimization_history:
                if param_name in record["params"]:
                    param_values.append(record["params"][param_name])
                    scores.append(record["score"])
            
            if len(param_values) > 1:
                # 计算相关系数
                correlation = np.corrcoef(param_values, scores)[0, 1]
                param_importance[param_name] = abs(correlation) if not np.isnan(correlation) else 0.0
        
        return param_importance


# ============ 测试函数 ============

def test_parameter_optimizer():
    """测试参数优化器"""
    print("=" * 60)
    print("参数优化器测试")
    print("=" * 60)
    
    optimizer = ParameterOptimizer()
    
    # 示例参数网格
    param_grid = {
        "trend_score_fast_bull": [25, 30, 35],
        "trend_score_slow_bull": [10, 15, 20],
    }
    
    print(f"参数网格: {param_grid}")
    print("（实际优化需要完整的验证框架）")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_parameter_optimizer()
