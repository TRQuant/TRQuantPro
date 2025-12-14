"""
文件名: code_2_1_store_market_data_to_timeseries.py
保存路径: code_library/002_Chapter2_Data_Source/2.1/002_Chapter2_Data_Source/2.1/code_2_1_store_market_data_to_timeseries.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.1_Data_Source_Management_CN.md
提取时间: 2025-12-13 20:30:08
函数/类名: store_market_data_to_timeseries

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd

def store_market_data_to_timeseries(symbol: str, data: pd.DataFrame, 
                                    source: str = "jqdata"):
        """
    store_market_data_to_timeseries函数
    
    **设计原理**：
    - **核心功能**：实现store_market_data_to_timeseries的核心逻辑
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
    from core.timeseries_db import get_timeseries_db
    
    ts_db = get_timeseries_db()
    
    # 准备数据
    records = []
    for date, row in data.iterrows():
        records.append({
            "symbol": symbol,
            "trade_date": date,
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"]),
            "volume": int(row["volume"]),
            "amount": float(row["amount"]),
            "source": source,
            "created_at": datetime.now()
        })
    
    # 批量插入
    ts_db.insert_batch("market_data_daily", records)