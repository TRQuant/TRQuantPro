"""
文件名: code_8_2_compare_strategies.py
保存路径: code_library/008_Chapter8_Backtest/8.2/code_8_2_compare_strategies.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.2_Backtest_Analyzer_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: compare_strategies

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class ComparisonAnalyzer:
    """对比分析器"""
    
    def compare_strategies(
        self,
        strategy1_result: BacktestResult,
        strategy2_result: BacktestResult
    ) -> Dict[str, Any]:
            """
    compare_strategies函数
    
    **设计原理**：
    - **核心功能**：实现compare_strategies的核心逻辑
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
        return {
            'strategy1': strategy1_result.metrics.to_dict(),
            'strategy2': strategy2_result.metrics.to_dict(),
            'comparison': self._compare_metrics(
                strategy1_result.metrics,
                strategy2_result.metrics
            )
        }