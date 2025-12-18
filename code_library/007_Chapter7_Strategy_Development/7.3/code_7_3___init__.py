"""
文件名: code_7_3___init__.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.3/code_7_3___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.factor_weight_optimizer import FactorWeightOptimizer, MarketScenario

class FactorWeightOptimizer:
    """因子权重优化器"""
    
    def __init__(self):
        self.scenario_library = SCENARIO_WEIGHT_LIBRARY
    
    def optimize_by_scenario(
        self,
        factors: List[str],
        market_scenario: MarketScenario
    ) -> Dict[str, float]:
        """
        根据市场情景优化因子权重
        
        **设计原理**：
        - **情景库驱动**：基于预设的市场情景库，为不同市场环境配置最优因子权重
        - **类型映射**：将具体因子映射到因子类型，使用类型级别的权重配置
        - **权重归一化**：确保所有权重之和为1，保证权重分配的合理性
        
        **为什么这样设计**：
        1. **适应性**：不同市场环境（牛市、熊市、震荡市）需要不同的因子权重
        2. **可维护性**：情景库集中管理，便于调整和扩展
        3. **灵活性**：支持因子类型映射，适应不同因子组合
        
        **使用场景**：
        - 根据当前市场状态（risk_on/risk_off/neutral）调整因子权重
        - 不同市场阶段（牛市、熊市、震荡市）使用不同权重配置
        - 策略优化时，根据市场情景选择最优权重
        
        **注意事项**：
        - 情景库需要定期更新，反映市场变化
        - 因子类型映射需要准确，否则权重分配可能不合理
        - 默认等权作为降级方案，保证系统可用性
        
        Args:
            factors: 因子列表
            scenario: 市场情景
        
        Returns:
            Dict: 优化后的因子权重（已归一化）
        """
        # 设计原理：从情景库获取配置
        # 原因：不同市场情景需要不同的因子权重配置
        scenario_config = self.scenario_library.get(market_scenario)
        if not scenario_config:
            # 设计原理：默认等权作为降级方案
            # 原因：情景库未配置时，使用等权保证系统可用性
            return {factor: 1.0 / len(factors) for factor in factors}
        
        base_weights = scenario_config['weights']
        
        # 设计原理：因子类型映射
        # 原因：情景库配置的是因子类型权重，需要映射到具体因子
        # 实现方式：根据因子类型匹配权重，未匹配的使用默认权重
        optimized_weights = {}
        for factor in factors:
            # 根据因子类型匹配权重
            factor_type = self._get_factor_type(factor)
            weight = base_weights.get(factor_type, 1.0 / len(factors))
            optimized_weights[factor] = weight
        
        # 设计原理：权重归一化
        # 原因：确保所有权重之和为1，保证权重分配的合理性
        # 实现方式：计算总和，按比例缩放
        total = sum(optimized_weights.values())
        if total > 0:
            optimized_weights = {
                k: v / total for k, v in optimized_weights.items()
            }
        
        return optimized_weights
    
    def grid_search_optimize(
        self,
        factors: List[str],
        eval_func: Callable[[Dict[str, float]], float],
        weight_range: Tuple[float, float] = (0.0, 0.5),
        step: float = 0.1
    ) -> OptimizationResult:
        """
        网格搜索优化因子权重
        
        **设计原理**：
        - **穷举搜索**：遍历所有权重组合，找到全局最优解
        - **权重归一化**：每个组合都归一化，确保权重之和为1
        - **结果排序**：保留所有结果并排序，便于分析
        
        **为什么这样设计**：
        1. **全局最优**：穷举搜索保证找到全局最优解（在搜索空间内）
        2. **可解释性**：保留所有结果，便于分析权重对性能的影响
        3. **鲁棒性**：评估失败时继续搜索，不中断优化过程
        
        **使用场景**：
        - 因子数量较少（<5）时，计算量可接受
        - 需要找到全局最优解时
        - 需要分析权重对性能的影响时
        
        **注意事项**：
        - **计算复杂度**：O(n^m)，n为候选权重数，m为因子数
        - **步长选择**：步长越小，搜索越精细，但计算量越大
        - **权重范围**：默认0.0-0.5，避免单个因子权重过大
        
        **替代方案对比**：
        - **方案A：随机搜索**
          - 优点：计算量小
          - 缺点：可能错过最优解
        - **方案B：贝叶斯优化**
          - 优点：智能搜索，效率高
          - 缺点：实现复杂，需要调参
        - **当前方案：网格搜索**
          - 优点：全局最优，结果可解释
          - 缺点：计算量大，仅适用于少量因子
        
        Args:
            factors: 因子列表
            eval_func: 评估函数（输入权重字典，返回性能分数）
            weight_range: 权重范围（默认0.0-0.5）
            step: 步长（默认0.1，即0.0, 0.1, 0.2, ..., 0.5）
        
        Returns:
            OptimizationResult: 优化结果，包含最优权重、最佳性能、所有结果等
        """
        from itertools import product
        import numpy as np
        
        # 设计原理：生成候选权重序列
        # 原因：网格搜索需要遍历所有可能的权重组合
        min_w, max_w = weight_range
        weight_candidates = np.arange(min_w, max_w + step, step)
        
        best_weights = None
        best_score = float("-inf")
        all_results = []
        iterations = 0
        
        # 设计原理：使用product生成所有权重组合
        # 原因：穷举搜索需要遍历所有可能的权重组合
        # 复杂度：O(n^m)，n为候选权重数，m为因子数
        for weights_tuple in product(weight_candidates, repeat=len(factors)):
            weights = list(weights_tuple)
            
            # 设计原理：权重归一化
            # 原因：确保权重之和为1，保证权重分配的合理性
            total = sum(weights)
            if total == 0:
                continue
            weights = [w / total for w in weights]
            
            # 构建权重字典
            weight_dict = dict(zip(factors, weights))
            
            # 设计原理：评估每个权重组合
            # 原因：找到性能最优的权重组合
            # 容错性：评估失败时继续搜索，不中断优化过程
            try:
                score = eval_func(weight_dict)
                iterations += 1
                
                # 设计原理：保留所有结果
                # 原因：便于分析权重对性能的影响
                all_results.append((weight_dict.copy(), score))
                
                if score > best_score:
                    best_score = score
                    best_weights = weight_dict.copy()
            except Exception as e:
                logger.warning(f"评估失败: {e}")
                continue
        
        return OptimizationResult(
            best_weights=best_weights or {},
            best_performance=best_score,
            all_results=sorted(all_results, key=lambda x: x[1], reverse=True)[:20],
            optimization_method="grid_search",
            iterations=iterations
        )
    
    def ic_weighted_optimize(
        self,
        factor_ic_dict: Dict[str, float],
        min_weight: float = 0.05,
        max_weight: float = 0.40
    ) -> Dict[str, float]:
        """
        IC加权优化
        
        Args:
            factor_ic_dict: 因子IC值字典
            min_weight: 最小权重
            max_weight: 最大权重
        
        Returns:
            Dict: 优化后的因子权重
        """
        if not factor_ic_dict:
            return {}
        
        # 计算IC绝对值
        ic_abs = {k: abs(v) for k, v in factor_ic_dict.items()}
        total_ic = sum(ic_abs.values())
        
        if total_ic == 0:
            # 等权
            return {k: 1.0 / len(factor_ic_dict) for k in factor_ic_dict.keys()}
        
        # IC加权
        weights = {k: v / total_ic for k, v in ic_abs.items()}
        
        # 应用权重限制
        weights = {
            k: max(min_weight, min(max_weight, v))
            for k, v in weights.items()
        }
        
        # 重新归一化
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        
        return weights