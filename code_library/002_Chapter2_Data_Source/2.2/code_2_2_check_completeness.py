"""
文件名: code_2_2_check_completeness.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_check_completeness.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:36:52
函数/类名: check_completeness

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any

class DataQualityChecker:
    """数据质量检查器"""
    
    def check_completeness(self, data: pd.DataFrame, 
                          required_fields: List[str] = None) -> Dict[str, Any]:
            """
    check_completeness函数
    
    **设计原理**：
    - **核心功能**：实现check_completeness的核心逻辑
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
            "missing_values": 0,
            "missing_fields": [],
            "time_series_continuous": True,
            "completeness_score": 0.0,
            "details": {}
        }
        
        # 1. 检查缺失值
        missing_count = data.isnull().sum()
        result["missing_values"] = int(missing_count.sum())
        result["details"]["missing_by_field"] = missing_count.to_dict()
        
        # 2. 检查必需字段
        if required_fields:
            missing_fields = [f for f in required_fields if f not in data.columns]
            result["missing_fields"] = missing_fields
        
        # 3. 检查时间序列连续性
        if 'date' in data.columns or data.index.name == 'date':
            result["time_series_continuous"] = self._check_time_series_continuity(data)
        
        # 4. 计算完整性得分
        total_cells = data.shape[0] * data.shape[1]
        if total_cells > 0:
            result["completeness_score"] = 1.0 - (result["missing_values"] / total_cells)
        
        return result
    
    def _check_time_series_continuity(self, data: pd.DataFrame) -> bool:
        """检查时间序列连续性"""
        # 获取日期索引
        if data.index.name == 'date' or 'date' in data.columns:
            if data.index.name == 'date':
                dates = pd.to_datetime(data.index)
            else:
                dates = pd.to_datetime(data['date'])
            
            # 生成完整的交易日序列
            start_date = dates.min()
            end_date = dates.max()
            # 这里需要根据实际情况生成交易日序列
            # 简化示例：检查是否有缺失的日期
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            missing_dates = set(date_range) <CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_check_time_series_continuity.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：