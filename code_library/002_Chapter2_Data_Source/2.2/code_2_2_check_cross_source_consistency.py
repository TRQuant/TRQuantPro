"""
文件名: code_2_2_check_cross_source_consistency.py
保存路径: code_library/002_Chapter2_Data_Source/2.2/code_2_2_check_cross_source_consistency.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.2_Data_Quality_CN.md
提取时间: 2025-12-13 20:36:52
函数/类名: check_cross_source_consistency

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def check_cross_source_consistency(self, data_sources: Dict[str, pd.DataFrame],
                                   tolerance: float = 0.01) -> Dict[str, Any]:
        """
    check_cross_source_consistency函数
    
    **设计原理**：
    - **核心功能**：实现check_cross_source_consistency的核心逻辑
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
        "inconsistent_fields": [],
        "inconsistency_count": 0,
        "consistency_score": 1.0
    }
    
    if len(data_sources) < 2:
        return result
    
    # 获取所有数据源的公共字段和公共索引
    sources_list = list(data_sources.values())
    common_fields = set(sources_list[0].columns)
    for source_data in sources_list[1:]:
        common_fields &= set(source_data.columns)
    
    common_index = set(sources_list[0].index)
    for source_data in sources_list[1:]:
        common_index &= set(source_data.index)
    
    # 比较每个字段
    for field in common_fields:
        field_data = {}
        for source_name, source_data in data_sources.items():
            field_data[source_name] = source_data.loc[list(common_index), field]
        
        # 计算差异
        source_names = list(field_data.keys())
        for i in range(len(source_names)):
            for j in range(i + 1, len(source_names)):
                source1 = source_names[i]
                source2 = source_names[j]
                data1 = field_data[source1]
                data2 = field_data[source2]
                
                # 计算相对差异
                diff = abs(data1 - data2) / (data1 + 1e-10)
                inconsistent = diff > tolerance
                
                if inconsistent.any():
                    inconsistent_indices = diff[inconsistent].index.tolist()
                    result["inconsistent_fields"].append({
                        "field": field,
                        "source1": source1,
                        "source2": source2,
                        "inconsistent_count": len(inconsistent_indices),
                        "inconsistent_indices": inconsistent_indices,
                        "max_diff": float(diff.max())
                    })
    
    result["inconsistency_count"] = len(result["inconsistent_fields"])
    
    # 计算一致性得分
    total_comparisons = len(common_fields) * len(common_index) * (len(data_sources) - 1) / 2
    if total_compariso<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.2/code_2_2_detect_anomalies_statistical.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：