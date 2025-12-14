"""
文件名: code_2_1_get_data_with_load_balance.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1_get_data_with_load_balance.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:30:08
函数/类名: get_data_with_load_balance

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def get_data_with_load_balance(self, symbol: str, start_date: str, 
                               end_date: str, data_type: str) -> pd.DataFrame:
        """
    get_data_with_load_balance函数
    
    **设计原理**：
    - **核心功能**：实现get_data_with_load_balance的核心逻辑
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
    # 获取可用数据源及其负载
    available_sources = []
    for name, source in self.sources.items():
        health = source.health_check()
        if health["status"] == "ok":
            load = self._get_source_load(name)
            available_sources.append((name, load))
    
    # 按负载排序，选择负载最低的
    available_sources.sort(key=lambda x: x[1])
    
    for source_name, _ in available_sources:
        try:
            return self._fetch_from_source(source_name, symbol, start_date, end_date, data_type)
        except Exception as e:
            logger.warning(f"数据源 {source_name} 获取失败: {e}")
            continue
    
    raise Exception("所有数据源都不可用")