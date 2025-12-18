"""
文件名: code_5_3_sort_by_factor_score.py
保存路径: code_library/005_Chapter5_Candidate_Pool/5.3/code_5_3_sort_by_factor_score.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/005_Chapter5_Candidate_Pool/5.3_Stock_Scoring_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: sort_by_factor_score

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

def sort_by_factor_score(
    stocks: List[CandidateStock],
    factor: str = 'technical'
) -> List[CandidateStock]:
        """
    sort_by_factor_score函数
    
    **设计原理**：
    - **核心功能**：实现sort_by_factor_score的核心逻辑
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
    factor_map = {
        'technical': 'technical_score',
        'capital': 'capital_score',
        'fundamental': 'fundamental_score',
        'sentiment': 'sentiment_score'
    }
    
    factor_key = factor_map.get(factor, 'composite_score')
    return sorted(stocks, key=lambda x: getattr(x, factor_key, 0), reverse=True)