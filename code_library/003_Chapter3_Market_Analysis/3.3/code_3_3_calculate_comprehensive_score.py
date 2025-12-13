from typing import Dict, List, Optional

def calculate_comprehensive_score(scores: dict, weights: dict = None) -> float:
    """
    calculate_comprehensive_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_comprehensive_score的核心逻辑
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
    if weights is None:
        weights = DEFAULT_WEIGHTS
    
    # 计算加权平均
    weighted_sum = sum(scores[dim] * weights[dim] for dim in scores if dim in weights)
    total_weight = sum(weights[dim] for dim in scores if dim in weights)
    
    if total_weight == 0:
        return 0.0
    
    comprehensive_score = weighted_sum / total_weight
    return min(100, max(0, comprehensive_score))