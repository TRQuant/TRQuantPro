"""
文件名: code_2_3_save_to_parquet.py
保存路径: code_library/002_Chapter2_Data_Source/2.3/002_Chapter2_Data_Source/2.3/code_2_3_save_to_parquet.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/002_Chapter2_Data_Source/2.3_Data_Storage_Architecture_CN.md
提取时间: 2025-12-13 20:30:10
函数/类名: save_to_parquet

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

from typing import Dict, List, Optional

import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path

CACHE_DIR = Path("data/cache/parquet")

def save_to_parquet(symbol: str, data: pd.DataFrame, data_type: str = "daily"):
        """
    save_to_parquet函数
    
    **设计原理**：
    - **核心功能**：实现save_to_parquet的核心逻辑
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
    cache_file = CACHE_DIR / f"{symbol}_{data_type}.parquet"
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    
    # 保存为Parquet格式（压缩）
    data.to_parquet(cache_file, compression='snappy', index=False)
    
def load_from_parquet(symbol: str, data_type: str = "daily") -> pd.DataFrame:
    """从Parquet文件加载数据"""
    cache_file = CACHE_DIR / f"{symbol}_{data_type}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    return None