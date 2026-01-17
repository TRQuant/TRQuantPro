"""
文件名: code_7_3_should_trigger_optimization.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.3/code_7_3_should_trigger_optimization.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: should_trigger_optimization

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class AutoOptimizationTrigger:
    """自动优化触发器"""
    
    def should_trigger_optimization(
        self,
        strategy: Dict[str, Any],
        backtest_result: Dict[str, Any] = None
    ) -> bool:
            """
    should_trigger_optimization函数
    
    **设计原理**：
    - **核心功能**：实现should_trigger_optimization的核心逻辑
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
        # 策略生成后自动触发首次优化
        if backtest_result is None:
            return True
        
        # 回测结果不满足要求时触发优化
        sharpe_ratio = backtest_result.get('sharpe_ratio', 0)
        max_drawdown = backtest_result.get('max_drawdown', 1.0)
        
        if sharpe_ratio < 1.5 or max_drawdown > 0.15:
            return True
        
        return False