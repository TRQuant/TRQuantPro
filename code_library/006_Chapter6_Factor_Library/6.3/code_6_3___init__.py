"""
文件名: code_6_3___init__.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

import schedule
import time
from datetime import datetime

class FactorOptimizationPipeline:
    """因子优化流水线"""
    
    def __init__(self, factor_manager: FactorManager, evaluator: FactorEvaluator):
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        self.factor_manager = factor_manager
        self.evaluator = evaluator
        self.neutralizer = FactorNeutralizer()
        self.correlation_analyzer = FactorCorrelationAnalyzer()
    
    def run_optimization(
        self,
        stocks: List[str],
        date: Union[str, datetime],
        factor_categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        运行完整优化流程
        
        Args:
            stocks: 股票列表
            date: 评估日期
            factor_categories: 因子类别列表
        
        Returns:
            优化结果字典
        """
        logger.info("开始因子优化流程...")
        
        # 1. 计算因子
        logger.info("步骤1: 计算因子...")
        factor_results = self.factor_manager.calculate_all_factors(
            stocks, date, categories=factor_categories
        )
        
        # 2. 因子中性化
        logger.info("步骤2: 因子中性化...")
        neutralized_results = {}
        for name, result in factor_results.items():
            neutralized = self.neutralizer.neutralize(
                result.values,
                stocks,
                date,
                neutralize_industry=True,
                neutralize_size=True
            )
            neutralized_results[name] = FactorResult(
                name=result.name,
                date=result.date,
                values=neutralized,
                raw_values=result.values,
                metadata=result.metadata
            )
        
        # 3. 因子有效性评估
        logger.info("步骤3: 因子有效性评估...")
        performances = {}
        for name, result in neutralized_results.items():
            # 计算IC时间序列（需要历史数据）
            # 这里简化处理，只计算单期IC
            performance = self._evaluate_factor(result, stocks, date)
            performances[name] = performance
        
        # 4. 因子相关性分析
        logger.info("步骤4: 因子相关性分析...")
        corr_matrix = self.correlation_analyzer.calculate_correlation(neutralized_results)
        redundant_pairs = self.correlation_analyzer.detect_redundant_factors(
            corr_matrix, threshold=0.7
        )
        
        # 5. 因子选择
        logger.info("步骤5: 因子选择...")
        selected_factors = self.correlation_analyzer.recommend_factor_selection(
            neutralized_results,
            performances,
            max_factors=5,
            correlation_threshold=0.7
        )
        
        # 6. 因子组合优化
        logger.info("步骤6: 因子组合优化...")
        selected_results = {
            name: neutralized_results[name]
            for name in selected_factors
        }
        selected_performances = {
            name: performances[name]
            for name in selected_factors
        }
        
        # IC加权组合
        combined_factor = self.factor_manager.combine_factors_ic_weighted(
            selected_results,
            selected_performances
        )
        
        return {
            "selected_factors": selected_factors,
            "performances": {k: v.to_dict() for k, v in performances.items()},
            "correlation_matrix": corr_matrix.to_dict(),
            "redundant_pairs": redundant_pairs,
            "combined_factor": combined_factor.to_dict(),
            "optimization_date": datetime.now().isoformat()
        }
    
    def _evaluate_factor(
        self,
        factor_result: FactorResult,
        stocks: List[str],
        date: Union[str, datetime]
    ) -> FactorPerformance:
        """评估单个因子（简化版本）"""
        # 这里需要计算IC时间序列，简化处理
        return FactorPerformance(
            factor_name=factor_result.name,
            category=factor_result.metadata.get("category", "unknown"),
            description=factor_result.metadata.get("description", ""),
            evaluation_date=datetime.now(),
            ic_mean=0.0,
            ic_std=0.0,
            ic_ir=0.0,
            ic_positive_ratio=0.0,
            long_short_return=0.0,
            long_short_sharpe=0.0,
            top_group_excess_return=0.0,
            turnover=0.0,
            max_drawdown=0.0,
            is_monotonic=False
        )
    
    def start_auto_optimization(self, interval_days: int = 7):
        """
        启动自动优化
        
        Args:
            interval_days: 优化间隔（天数）
        """
        schedule.every(interval_days).days.do(self.run_optimization)
        
        # 立即执行一次
        stocks = self._get_candidate_stocks()
        self.run_optimization(stocks, datetime.now())
        
        # 持续运行
        while True:
            schedule.run_pending()
            time.sleep(3600)  # 每小时检查一次