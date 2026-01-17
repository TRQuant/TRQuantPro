"""
文件名: code_4_2_filter_by_min_score.py
保存路径: code_library/004_Chapter4_Mainline_Identification/4.2/code_4_2_filter_by_min_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/004_Chapter4_Mainline_Identification/4.2_Mainline_Filtering_CN.md
提取时间: 2025-12-13 21:16:42
函数/类名: filter_by_min_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import List
from core.base_mainline import Mainline

def filter_by_min_score(
    mainlines: List[Mainline],
    min_score: float = 60.0
) -> List[Mainline]:
        """
    filter_by_min_score函数
    
    **设计原理**：
    - **核心功能**：实现filter_by_min_score的核心逻辑
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
    filtered = [
        mainline for mainline in mainlines
        if mainline.score.total_score >= min_score
    ]
    return filtered

# 使用示例
mainlines = get_all_mainlines()
filtered_mainlines = filter_by_min_score(mainlines, min_score=75.0)
print(f"筛选出{len(filtered_mainlines)}条主线（评分≥75分）")