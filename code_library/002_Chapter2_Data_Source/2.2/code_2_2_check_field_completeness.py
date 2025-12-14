"""
文件名: code_2_2_check_field_completeness.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_check_field_completeness.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:33:44
函数/类名: check_field_completeness

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def check_field_completeness(self, data: pd.DataFrame, 
                             required_fields: List[str],
                             field_types: Dict[str, type] = None) -> Dict[str, Any]:
        """
    check_field_completeness函数
    
    **设计原理**：
    - **核心功能**：实现check_field_completeness的核心逻辑
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
        "missing_fields": [],
        "type_mismatches": [],
        "completeness_score": 1.0
    }
    
    # 检查必需字段
    for field in required_fields:
        if field not in data.columns:
            result["missing_fields"].append(field)
    
    # 检查字段类型
    if field_types:
        for field, expected_type in field_types.items():
            if field in data.columns:
                actual_type = data[field].dtype
                if not self._is_type_compatible(actual_type, expected_type):
                    result["type_mismatches"].append({
                        "field": field,
                        "expected": str(expected_type),
                        "actual": str(actual_type)
                    })
    
    # 计算完整性得分
    total_fields = len(required_fields)
    if total_fields > 0:
        missing_count = len(result["missing_fields"])
        type_mismatch_count = len(result["type_mismatches"])
        result["completeness_score"] = 1.0 - (missing_count + type_mismatch_count) / total_fields
    
    return result