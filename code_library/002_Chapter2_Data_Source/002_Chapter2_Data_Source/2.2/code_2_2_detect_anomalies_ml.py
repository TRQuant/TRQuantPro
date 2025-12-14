"""
文件名: code_2_2_detect_anomalies_ml.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_detect_anomalies_ml.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:30:09
函数/类名: detect_anomalies_ml

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional

from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def detect_anomalies_ml(self, data: pd.DataFrame,
                       fields: List[str] = None,
                       method: str = "isolation_forest",
                       **kwargs) -> Dict[str, Any]:
        """
    detect_anomalies_ml函数
    
    **设计原理**：
    - **核心功能**：实现detect_anomalies_ml的核心逻辑
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
        "anomaly_indices": [],
        "method": method
    }
    
    if fields is None:
        fields = data.select_dtypes(include=[np.number]).columns.tolist()
    
    # 准备数据
    X = data[fields].dropna()
    if len(X) == 0:
        return result
    
    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    if method == "isolation_forest":
        # Isolation Forest
        contamination = kwargs.get("contamination", 0.1)
        model = IsolationForest(contamination=contamination, random_state=42)
        predictions = model.fit_predict(X_scaled)
        anomaly_mask = predictions == -1
    
    elif method == "dbscan":
        # DBSCAN
        eps = kwargs.get("eps", 0.5)
        min_samples = kwargs.get("min_samples", 5)
        model = DBSCAN(eps=eps, min_samples=min_samples)
        predictions = model.fit_predict(X_scaled)
        anomaly_mask = predictions == -1
    
    # 获取异常索引
    anomaly_indices = X.index[anomaly_mask].tolist()
    result["anomaly_indices"] = anomaly_indices
    result["anomaly_count"] = len(anomaly_indices)
    
    # 详细信息
    if len(anomaly_indices) > 0:
        anomaly_data = data.loc[anomaly_indices, fields]
        result["anomalies"] = anomaly_data.to_dict('records')
    
    return result