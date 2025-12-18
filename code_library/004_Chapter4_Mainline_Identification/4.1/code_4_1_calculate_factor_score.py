"""
文件名: code_4_1_calculate_factor_score.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_calculate_factor_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: calculate_factor_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def calculate_factor_score(
    factor_name: str,
    raw_value: float,
    factor_config: Dict
) -> FactorScore:
        """
    calculate_factor_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_factor_score的核心逻辑
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
    thresholds = factor_config["thresholds"]
    inverse = factor_config.get("inverse", False)
    weight = factor_config["weight"]
    
    # 标准化得分
    normalized_score = normalize_factor_value(raw_value, thresholds, inverse)
    
    # 加权得分
    weighted_score = normalized_score * weight
    
    # 计算置信度（基于数据质量）
    confidence = calculate_confidence(factor_config)
    
    return FactorScore(
        name=factor_name,
        raw_value=raw_value,
        normalized_score=normalized_score,
        weight=weight,
        weighted_score=weighted_score,
        data_source=factor_config["data_source"],
        calculation_method=factor_config["calculation"],
        confidence=confidence
    )