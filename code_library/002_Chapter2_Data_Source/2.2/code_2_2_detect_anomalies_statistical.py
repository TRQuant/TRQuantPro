"""
文件名: code_2_2_detect_anomalies_statistical.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_detect_anomalies_statistical.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:34:05
函数/类名: detect_anomalies_statistical

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

import numpy as np
from scipy import stats

def detect_anomalies_statistical(self, data: pd.DataFrame, 
                                fields: List[str] = None,
                                method: str = "zscore",
                                threshold: float = 3.0) -> Dict[str, Any]:
        """
    detect_anomalies_statistical函数
    
    **设计原理**：
    - **核心功能**：实现detect_anomalies_statistical的核心逻辑
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
    result = {
        "anomalies": [],
        "anomaly_count": 0,
        "anomaly_indices": set(),
        "method": method
    }
    
    if fields is None:
        fields = data.select_dtypes(include=[np.number]).columns.tolist()
    
    for field in fields:
        if field not in data.columns:
            continue
        
        values = data[field].dropna()
        
        if method == "zscore":
            # Z-score方法
            z_scores = np.abs(stats.zscore(values))
            anomalies = values[z_scores > threshold]
        
        elif method == "iqr":
            # IQR方法
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            anomalies = values[(values < lower_bound) | (values > upper_bound)]
        
        elif method == "3sigma":
            # 3σ原则
            mean = values.mean()
            std = values.std()
            anomalies = values[(values < mean - threshold * std) | 
                              (values > mean + threshold * std)]
        
        if len(anomalies) > 0:
            anomaly_indices = anomalies.index.tolist()
            result["anomalies"].append({
                "field": field,
                "anomaly_count": len(anomalies),
                "anomaly_indices": anomaly_indices,
                "anomaly_values":<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_detect_anomalies_ml.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：