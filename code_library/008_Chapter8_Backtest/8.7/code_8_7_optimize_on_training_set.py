"""
文件名: code_8_7_optimize_on_training_set.py
保存路径: code_library/008_Chapter8_Backtest/8.7/code_8_7_optimize_on_training_set.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/008_Chapter8_Backtest/8.7_Walk_Forward_Analysis_CN.md
提取时间: 2025-12-13 21:16:47
函数/类名: optimize_on_training_set

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.strategy_optimizer import StrategyOptimizer

class WalkForwardOptimizer:
    """Walk-Forward优化器"""
    
    def optimize_on_training_set(
        self,
        strategy: Any,
        train_start: str,
        train_end: str,
        optimization_config: Dict[str, Any]
    ) -> Dict[str, Any]:
            """
    optimize_on_training_set函数
    
    **设计原理**：
    - **核心功能**：实现optimize_on_training_set的核心逻辑
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
        # 在训练集上回测
        bt_engine = BulletTradeEngine(config)
        train_result = bt_engine.run_backtest(
            strategy_path=strategy_path,
            start_date=train_start,
            end_date=train_end
        )
        
        # 优化策略参数
        optimizer = StrategyOptimizer()
        optimized_strategy = optimizer.optimize(
            strategy=strategy,
            backtest_result=train_result,
            optimization_config=optimization_config
        )
        
        return {
            'optimized_strategy': optimized_strategy,
            'train_result': train_result,
            'optimization_metrics': optimizer.get_optimization_metrics()
        }