"""
文件名: code_2_2_clean_anomalies.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_clean_anomalies.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:34:17
函数/类名: clean_anomalies

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

def clean_anomalies(self, data: pd.DataFrame,
                   anomaly_indices: List,
                   method: str = "remove",
                   **kwargs) -> pd.DataFrame:
        """
    clean_anomalies函数
    
    **设计原理**：
    - **核心功能**：实现clean_anomalies的核心逻辑
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
    
    if method == "remove":
        # 删除异常值
        cleaned_data = cleaned_data.drop(index=anomaly_indices)
    
    elif method == "replace":
        # 替换异常值
        replace_value = kwargs.get("replace_value", None)
        if replace_value is None:
            # 用中位数替换
            for col in cleaned_data.columns:
                if col in cleaned_data.select_dtypes(include=[np.number]).columns:
                    median = cleaned_data[col].median()
                    cleaned_data.loc[anomaly_indices, col] = median
        else:
            cleaned_data.loc[anomaly_indices] = replace_value
    
    elif method == "clip":
        # 截断异常值
        lower_bound = kwargs.get("lower_bound", None)
        upper_bound = kwargs.get("upper_bound", None)
        for col in cleaned_data.columns:
            if col in cleaned_data.select_dtypes(include=[np.number]).columns:
                if lower_bound is not None:
                    cleaned_data.loc[anomaly_indices, col] = cleaned_data.loc[anomaly_indices, col].clip(lower=lower_bound)
                if upper_bound is not None:
                    cleaned_data.loc[anomaly_indices, col] = cleaned_data.loc[anomaly_indices, col].clip(upper=upper_bound)
    
    elif method<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_auto_clean.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：