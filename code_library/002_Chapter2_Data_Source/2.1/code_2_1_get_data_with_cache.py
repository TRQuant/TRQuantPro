"""
文件名: code_2_1_get_data_with_cache.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/code_2_1_get_data_with_cache.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:33:42
函数/类名: get_data_with_cache

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def get_data_with_cache(symbol: str, start_date: str, end_date: str, 
                        data_type: str = "daily") -> pd.DataFrame:
        """
    get_data_with_cache函数
    
    **设计原理**：
    - **核心功能**：实现get_data_with_cache的核心逻辑
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
    cache_key = f"market:{symbol}:{start_date}:{end_date}:{data_type}"
    
    # 1. 检查Redis缓存（L1缓存）
    if self.cache:
        cached = self.cache.get(cache_key)
        if cached is not None:
            logger.info(f"从Redis缓存获取: {cache_key}")
            return cached
    
    # 2. 检查Parquet文件缓存（L2缓存）
    parquet_path = f"cache/{symbol}_{start_date}_{end_date}.parquet"
    if os.path.exists(parquet_path):
        data = pd.read_parquet(parquet_path)
        # 更新Redis缓存
        if self.cache:
            self.cache.set(cache_key, data, ttl=3600)
        logger.info(f"从Parquet缓存获取: {parquet_path}")
        return data
    
    # 3. 从数据源获取
    data = self.get_data(symbol, start_date, end_date, data_type)
    
    # 4. 保存到缓存
    data.to_parquet(parquet_path, compression='snappy')
    if self.cache:
        self.cache.set(cache_key, data, ttl=3600)
    
    return data