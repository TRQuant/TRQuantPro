"""
文件名: code_7_3_first_optimization.py
保存路径: code_library/007_Chapter7_Strategy_Development/7.3/code_7_3_first_optimization.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/007_Chapter7_Strategy_Development/7.3_Strategy_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: first_optimization

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

from core.strategy_optimizer import StrategyOptimizer
from core.factor_weight_optimizer import FactorWeightOptimizer

def first_optimization(
    strategy: Dict[str, Any],
    market_context: Dict[str, Any],
    mainlines: List[Dict],
    candidate_pool: List[str],
    factor_recommendations: List[Dict]
) -> Dict[str, Any]:
        """
    first_optimization函数
    
    **设计原理**：
    - **核心功能**：实现first_optimization的核心逻辑
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
    optimizer = StrategyOptimizer()
    
    # 1. 分析前序信息
    market_regime = market_context.get('regime', 'neutral')
    mainline_names = [m.get('name', '') for m in mainlines]
    factors = [f.get('name', '') for f in factor_recommendations]
    
    # 2. 配置优化目标
    optimization_config = {
        'target_metric': 'sharpe_ratio',
        'direction': 'maximize',
        'min_sharpe': 1.5,
        'max_drawdown_limit': 0.15,
        'algorithm': 'grid_search'
    }
    
    # 3. 执行优化
    result = optimizer.optimize(
        strategy=strategy,
        market_context=market_context,
        mainlines=mainlines,
        candidate_pool=candidate_pool,
        factors=factor_recommendations,
        optimization_config=optimization_config
    )
    
    return result