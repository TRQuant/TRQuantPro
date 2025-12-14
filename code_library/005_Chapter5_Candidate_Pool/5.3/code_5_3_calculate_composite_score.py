"""
文件名: code_5_3_calculate_composite_score.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_calculate_composite_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: calculate_composite_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def calculate_composite_score(
    technical_score: float,
    capital_score: float,
    fundamental_score: float,
    sentiment_score: float,
    mainline_heat: float = 0.0,
    weights: Dict = None
) -> float:
        """
    calculate_composite_score函数
    
    **设计原理**：
    - **核心功能**：实现calculate_composite_score的核心逻辑
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
    
    # 第一步：计算个股因子得分
    stock_factor = (
        technical_score * weights['technical'] +
        capital_score * weights['capital'] +
        fundamental_score * weights['fundamental'] +
        sentiment_score * weights['sentiment']
    )
    
    # 第二步：结合主线热度（如果提供）
    if mainline_heat > 0:
        # 主线热度权重15%，个股因子权重85%
        composite_score = (
            mainline_heat * 100 * 0.15 +  # 主线热度转换为0-100分
            stock_factor * 0.85
        )
    else:
        composite_score = stock_factor
    
    return min(100, max(0, composite_score))