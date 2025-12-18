"""
文件名: code_6_3_calculate_ir.py
保存路径: code_library/006_Chapter6_Factor_Library/6.3/code_6_3_calculate_ir.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.3_Factor_Optimization_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: calculate_ir

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def calculate_ir(self, ic_series: pd.Series) -> float:
        """
    calculate_ir函数
    
    **设计原理**：
    - **核心功能**：实现calculate_ir的核心逻辑
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
    if ic_series.empty or ic_series.std() == 0:
        return 0.0
    
    return ic_series.mean() / ic_series.std()