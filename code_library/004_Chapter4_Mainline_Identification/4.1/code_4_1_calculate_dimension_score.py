"""
文件名: code_4_1_calculate_dimension_score.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_calculate_dimension_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: calculate_dimension_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def calculate_dimension_score(
    dimension_name: str,
    dimension_data: Dict[str, float],
    dimension_weight: float
) -> DimensionScore:
        """
    calculate_dimension_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_dimension_score的核心逻辑
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
    factors = []
    total_score = 0.0
    
    # 获取维度因子配置
    factor_configs = SCORING_CONFIG[f"{dimension_name}_factors"]
    
    # 计算各因子得分
    for factor_name, factor_config in factor_configs.items():
        raw_value = dimension_data.get(factor_name, 0)
        factor_score = calculate_factor_score(
            factor_name, raw_value, factor_config
        )
        factors.append(factor_score)
        total_score += factor_score.weighted_score
    
    # 确定评分等级
    level = get_score_level(total_score)
    
    return DimensionScore(
        dimension=dimension_name,
        factors=factors,
        total_score=total_score,
        weight=dimension_weight,
        weighted_score=total_score * dimension_weight,
        level=level,
        interpretation=f"{dimension_name}得分{total_score:.2f}"
    )