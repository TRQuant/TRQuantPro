"""
文件名: code_2_3_store_market_data.py
保存路径: code_library/002_Chapter2_Data_Source/2.3/code_2_3_store_market_data.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.3_Data_Storage_Architecture_CN.md
提取时间: 2025-12-13 20:36:52
函数/类名: store_market_data

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

from core.data_center import DataCenter

dc = DataCenter()

# 存储行情数据到ClickHouse
def store_market_data(symbol: str, data: pd.DataFrame, source: str = "jqdata"):
        """
    store_market_data函数
    
    **设计原理**：
    - **核心功能**：实现store_market_data的核心逻辑
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
    # 添加数据源标识
    data['source'] = source
    data['created_at'] = pd.Timestamp.now()
    
    # 存储到ClickHouse
    dc.clickhouse_client.insert(
        'market_data_daily',
        data.to_dict('records')
    )
    
    # 更新元数据
    dc.update_metadata(
        source_name=source,
        data_type="daily",
        symbol=symbol,
        start_date=data['trade_date'].min(),
        end_date=data['trade_date'].max(),
        record_count=len(data)
    )

# 查询行情数据
def query_market_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """从时序库查询行情数据"""
    query = f"""
    SELECT * FROM market_data_daily
    WHERE symbol = '{symbol}'
      AND trade_date >= '{start_date}'
      AND trade_date <= '{end_date}'
    ORDER BY trade_date
    """
    return dc.clickhouse_client.qu<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.3/002_Chapter2_Data_Source/2.3/code_2_3_cache_market_snapshot.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留<CodeFromFile 
  filePath="code_library/002_Chapter2_Data_Source/2.3/code_2_3_cache_market_snapshot.py"
  language="python"
  showDesignPrinciples="true"
/>

<!-- 原始代码（保留作为备份）：