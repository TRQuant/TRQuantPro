"""
文件名: code_10_2_calculate_returns.py
保存路径: code_library/010_Chapter10_Development_Guide/10.2/code_10_2_calculate_returns.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/010_Chapter10_Development_Guide/10.2_Development_Principles_CN.md
提取时间: 2025-12-13 21:16:52
函数/类名: calculate_returns

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import numpy as np

# ✅ 使用类型提示
from typing import Dict, List, Optional
import pandas as pd

def calculate_returns(
    prices: pd.Series,
    method: str = "simple"
) -> pd.Series:
        """
    calculate_returns函数
    
    **设计原理**：
    - **核心功能**：实现calculate_returns的核心逻辑
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
    if method == "simple":
        return prices.pct_change()
    elif method == "log":
        return pd.Series(np.log(prices / prices.shift(1)))
    else:
        raise ValueError(f"未知方法: {method}")