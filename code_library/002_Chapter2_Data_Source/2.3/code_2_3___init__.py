"""
文件名: code_2_3___init__.py
保存路径: code_library/002_Chapter2_Data_Source/2.3/code_2_3___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.3_Data_Storage_Architecture_CN.md
提取时间: 2025-12-13 20:34:05
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class DataStorageManager:
    """数据存储管理器"""
    
    def __init__(self):
        self.pg_client = PostgreSQLClient()
        self.ch_client = ClickHouseClient()
        self.redis_client = RedisClient()
        self.cache_dir = Path("data/cache/parquet")
    
    def get_data(self, symbol: str, start_date: str, end_date: str, 
                 data_type: str = "daily", use_cache: bool = True) -> pd.DataFrame:
            """
    __init__函数
    
    **设计原理**：
    - **核心功能**：实现__init__的核心逻辑
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
        
        # 1. 检查Redis缓存（仅实时数据）
        if data_type == "snapshot" and use_cache:
            cached = self.redis_client.get_market_snapshot(symbol)
            if cached:
                return pd.DataFrame([cached])
        
        # 2. 检查文件缓存
        if use_cache:
            cached = self.load_from_parquet(symbol, data_type)
            if cached is not None:
                # 检查日期范围
                if (cached['trade_date'].min() <= start_date and 
                    cached['trade_date'].max() >= end_date):
                    return cached
        
        # 3. 从时序库查询
        data = self.ch_client.query_market_data(
            symbol, start_date, end_date, data_type
        )
        
        if data is not None and len(data) > 0:
            # 4. 更新缓存
            if use_cache:
                self.save_to_parquet(symbol, data, data_type)
            
            # 5. 记录审计日志
            self.pg_client.log_data_fetch(
                symbol=symbol,
                data_type=data_type,
                start_date=start_date,
                end_date=end_date,
                record_count=len(data),
                status="success"
            )
            
            return data
        
        # 6. 从数据源获取（如果时序库也没有）
        data = self.fetch_from_source(symbol, start_date, end_date, data_type)
        
        if data is not None and len(data) > 0:
            # 7. 存储到时序库
            self.ch_client.store_market_data(symbol, data, data_type)
            
            # 8. 更新缓存
            if use_cache:
                self.save_to_parquet(symbol, data, data_type)
            
            # 9. 记录审计日志
            self.pg_client.log_data_fetch(
                symbol=symbol,
                data_type=data_type,
                start_date=start_date,
                end_date=end_date,
                record_count=len(data),
                status="success"
            )
            
            return data
        
        return pd.DataFrame()