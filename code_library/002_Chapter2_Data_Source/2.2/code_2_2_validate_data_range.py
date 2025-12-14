"""
文件名: code_2_2_validate_data_range.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_validate_data_range.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:34:17
函数/类名: validate_data_range

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def validate_data_range(self, data: pd.DataFrame, 
                       range_rules: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """
    validate_data_range函数
    
    **设计原理**：
    - **核心功能**：实现validate_data_range的核心逻辑
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
        "violations": [],
        "violation_count": 0,
        "accuracy_score": 1.0
    }
    
    for field, rules in range_rules.items():
        if field not in data.columns:
            continue
        
        min_val = rules.get("min")
        max_val = rules.get("max")
        
        # 检查最小值
        if min_val is not None:
            below_min = data[data[field] < min_val]
            if len(below_min) > 0:
                result["violations"].append({
                    "field": field,
                    "rule": f">= {min_val}",
                    "violation_count": len(below_min),
                    "violation_indices": below_min.index.tolist()
                })
        
        # 检查最大值
        if max_val is not None:
            above_max = data[data[field] > max_val]
            if len(above_max) > 0:
                result["violations"].append({
                    "field": field,
                    "rule": f"<= {max_val}",
                    "violation_count": len(above_max),
                    "violation_indices": above_max.index.tolist()
                })
    
    result["violation_count"] = len(result["violations"])
    
    # 计算准确性得分
    total_rows = len(data)
    if total_rows > 0:
        violation_rows = len(set(
            i<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.2/002_Chapter2_Data_Source/2.2/code_2_2_validate_business_logic.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：