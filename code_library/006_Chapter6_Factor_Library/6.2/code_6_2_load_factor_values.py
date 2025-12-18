"""
文件名: code_6_2_load_factor_values.py
保存路径: code_library/006_Chapter6_Factor_Library/6.2/code_6_2_load_factor_values.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.2_Factor_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: load_factor_values

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

def load_factor_values(
    self,
    factor_name: str,
    date: Union[str, datetime],
    stocks: Optional[List[str]] = None
) -> Optional[pd.Series]:
        """
    load_factor_values函数
    
    **设计原理**：
    - **核心功能**：实现load_factor_values的核心逻辑
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
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
    
    date_str = date.strftime("%Y-%m-%d")
    
    if self._connected:
        # 从MongoDB加载
        try:
            collection = self.db.factor_data
            
            query = {
                "factor_name": factor_name,
                "date": date_str
            }
            
            if stocks:
                query["stock_id"] = {"$in": stocks}
            
            cursor = collection.find(query)
            data = {doc["stock_id"]: doc["value"] for doc in cursor}
            
            if data:
                result = pd.Series(data)
                if stocks:
                    result = result.reindex(stocks)
                return result
        
        except Exception as e:
            logger.error(f"MongoDB加载失败: {e}")
    
    # 从文件加载（降级）
    if self.use_file_fallback:
        return self._load_from_file(factor_name, date_str, stocks)
    
    return None

def load_factor_history(
    self,
    factor_name: str,
    stock: str,
    start_date: Union[str, datetime],
    end_date: Union[str, datetime]
) -> Optional[pd.Series]:
    """
    加载因子历史值
    
    Args:
        factor_name: 因子名称
        stock: 股票代码
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        pd.Series: 因子历史值（index为日期）
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    if self._connected:
        try:
            collection = self.db.factor_data
            
            cursor = collection.find({
                "factor_name": factor_name,
                "stock_id": stock,
                "date": {
                    "$gte": start_date.strftime("%Y-%m-%d"),
                    "$lte": end_date.strftime("%Y-%m-%d")
                }
            }).sort("date", 1)
            
            data = {doc["date"]: doc["value"] for doc in cursor}
            
            if data:
                result = pd.Series(data)
                result.index = pd.to_datetime(result.index)
                return result
        
        except Exception as e:
            logger.error(f"MongoDB加载历史失败: {e}")
    
    return None