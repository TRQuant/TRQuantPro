"""
文件名: code_8_7_evaluate_robustness.py
保存路径: code_library/008_Chapter8_Backtest/8.7/code_8_7_evaluate_robustness.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.7_Walk_Forward_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: evaluate_robustness

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np
from typing import Dict, List, Optional

class RobustnessEvaluator:
    """稳健性评估器"""
    
    def evaluate_robustness(
        self,
        walk_forward_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
            """
    evaluate_robustness函数
    
    **设计原理**：
    - **核心功能**：实现evaluate_robustness的核心逻辑
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
        # 提取性能指标
        returns = [r['performance_metrics']['total_return'] for r in walk_forward_results]
        sharpe_ratios = [r['performance_metrics']['sharpe_ratio'] for r in walk_forward_results]
        max_drawdowns = [r['performance_metrics']['max_drawdown'] for r in walk_forward_results]
        
        # 计算稳健性指标
        return {
            'return_consistency': {
                'mean': np.mean(returns),
                'std': np.std(returns),
                'cv': np.std(returns) / abs(np.mean(returns)) if np.mean(returns) != 0 else 0,  # 变异系数
                'positive_ratio': len([r for r in returns if r > 0]) / len(returns)
            },
            'sharpe_consistency': {
                'mean': np.mean(sharpe_ratios),
                'std': np.std(sharpe_ratios),
                'min': np.min(sharpe_ratios),
                'max': np.max(sharpe_ratios)
            },
            'drawdown_consistency': {
                'mean': np.mean(max_drawdowns),
                'std': np.std(max_drawdowns),
                'max': np.max(max_drawdowns)
            },
            'overall_robustness': self._calculate_overall_robustness(
                returns, sharpe_ratios, max_drawdowns
            )
        }
    
    def _calculate_overall_robustness(
        self,
        returns: List[float],
        sharpe_ratios: List[float],
        max_drawdowns: List[float]
    ) -> float:
        """计算整体稳健性得分"""
        # 收益稳定性
        return_cv = np.std(returns) / abs(np.mean(returns)) if np.mean(returns) != 0 else 1
        return_stability = 1 / (1 + return_cv)
        
        # 夏普比率稳定性
        sharpe_stability = 1 - (np.std(sharpe_ratios) / (abs(np.mean(sharpe_ratios)) + 1))
        
        # 回撤稳定性
        drawdown_stability = 1 - (np.std(max_drawdowns) / (abs(np.mean(max_drawdowns)) + 1))
        
        # 综合稳健性
        overall = (return_stability + sharpe_stability + drawdown_stability) / 3
        
        return overall