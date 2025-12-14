"""
文件名: code_2_2_clean_missing_values.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_clean_missing_values.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:34:17
函数/类名: clean_missing_values

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def clean_missing_values(self, data: pd.DataFrame,
                       method: str = "forward_fill",
                       **kwargs) -> pd.DataFrame:
        """
    clean_missing_values函数
    
    **设计原理**：
    - **核心功能**：实现clean_missing_values的核心逻辑
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
    cleaned_data = data.copy()
    
    if method == "forward_fill":
        # 前向填充
        cleaned_data = cleaned_data.fillna(method='ffill')
    
    elif method == "backward_fill":
        # 后向填充
        cleaned_data = cleaned_data.fillna(method='bfill')
    
    elif method == "interpolate":
        # 插值
        method_type = kwargs.get("interpolation_method", "linear")
        cleaned_data = cleaned_data.interpolate(method=method_type)
    
    elif method == "drop":
        # 删除缺失值
        cleaned_data = cleaned_data.dropna()
    
    elif method == "mean":
        # 用均值填充
        cleaned_data = cleaned_data.fillna(cleaned_data.mean())
    
    elif method == "median":
        # 用中位数填充
        cleaned_data = cleaned_data.fillna(cleaned_data.median())
    
    return cleaned_data