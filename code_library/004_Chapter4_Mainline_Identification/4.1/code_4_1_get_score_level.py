"""
文件名: code_4_1_get_score_level.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.1/code_4_1_get_score_level.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.1_Mainline_Scoring_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: get_score_level

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

class ScoreLevel(Enum):
    """评分等级"""
    VERY_HIGH = "very_high"    # 90-100：强烈推荐
    HIGH = "high"              # 75-89：推荐
    MEDIUM = "medium"          # 60-74：中性
    LOW = "low"                # 40-59：谨慎
    VERY_LOW = "very_low"      # 0-39：不推荐

def get_score_level(score: float) -> ScoreLevel:
        """
    get_score_level函数
    
    **设计原理**：
    - **核心功能**：实现get_score_level的核心逻辑
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
    if score >= 90:
        return ScoreLevel.VERY_HIGH
    elif score >= 75:
        return ScoreLevel.HIGH
    elif score >= 60:
        return ScoreLevel.MEDIUM
    elif score >= 40:
        return ScoreLevel.LOW
    else:
        return ScoreLevel.VERY_LOW