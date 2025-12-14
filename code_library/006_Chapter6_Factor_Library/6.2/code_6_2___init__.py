"""
文件名: code_6_2___init__.py
保存路径: code_library/006_Chapter6_Factor_Library/6.2/code_6_2___init__.py
来源文件: extension/AShare-manual/src/pages/ashare-book6/006_Chapter6_Factor_Library/6.2_Factor_Management_CN.md
提取时间: 2025-12-13 21:16:46
函数/类名: __init__

说明：
此文件由代码提取脚本自动生成，从Markdown文档中提取的代码块。
如需修改代码，请直接编辑此文件，修改后网页会自动更新（通过Vite HMR机制）。
"""

import pandas as pd
from typing import Dict, List, Optional

class FactorStorage:
    """
    因子数据存储
    
    使用MongoDB存储因子数据、元信息和绩效记录
    """
    
    def __init__(
        self,
        mongo_uri: str = "mongodb://localhost:27017/",
        db_name: str = "trquant_factors",
        use_file_fallback: bool = True,
    ):
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
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.use_file_fallback = use_file_fallback
        
        self.client = None
        self.db = None
        self._connected = False
        
        # 文件存储路径
        self.file_storage_dir = Path.home() / ".local/share/trquant/factors"
        self.file_storage_dir.mkdir(parents=True, exist_ok=True)
        
        # 尝试连接MongoDB
        self._connect()
    
    def _connect(self):
        """连接MongoDB"""
        try:
            from pymongo import MongoClient
            
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            # 测试连接
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self._connected = True
            
            # 创建索引
            self._create_indexes()
            
            logger.info(f"MongoDB连接成功: {self.db_name}")
        
        except Exception as e:
            logger.warning(f"MongoDB连接失败: {e}，使用文件存储")
            self._connected = False
    
    def _create_indexes(self):
        """创建索引"""
        if not self._connected:
            return
        
        from pymongo import ASCENDING, DESCENDING
        
        try:
            # factor_data索引
            self.db.factor_data.create_index(
                [("date", DESCENDING), ("factor_name", ASCENDING), ("stock_id", ASCENDING)]
            )
            
            # factor_info索引
            self.db.factor_info.create_index([("factor_name", ASCENDING)], unique=True)
            
            # factor_performance索引
            self.db.factor_performance.create_index(
                [("factor_name", ASCENDING), ("date", DESCENDING)]
            )
        
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def save_factor_values(
        self,
        factor_name: str,
        date: Union[str, datetime],
        values: pd.Series,
        overwrite: bool = True,
    ) -> bool:
        """
        保存因子值
        
        Args:
            factor_name: 因子名称
            date: 日期
            values: 因子值（index为股票代码）
            overwrite: 是否覆盖已有数据
        
        Returns:
            bool: 是否成功
        """
        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        
        date_str = date.strftime("%Y-%m-%d")
        
        if self._connected:
            # MongoDB存储
            try:
                collection = self.db.factor_data
                
                # 删除旧数据（如果覆盖）
                if overwrite:
                    collection.delete_many({
                        "factor_name": factor_name,
                        "date": date_str
                    })
                
                # 插入新数据
                documents = [
                    {
                        "factor_name": factor_name,
                        "date": date_str,
                        "stock_id": stock,
                        "value": float(value) if not pd.isna(value) else None
                    }
                    for stock, value in values.items()
                ]
                
                if documents:
                    collection.insert_many(documents)
                
                logger.info(f"保存因子值到MongoDB: {factor_name} @ {date_str}")
                return True
            
            except Exception as e:
                logger.error(f"MongoDB保存失败: {e}")
                if not self.use_file_fallback:
                    raise
        
        # 文件存储（降级）
        if self.use_file_fallback:
            return self._save_to_file(factor_name, date_str, values)
        
        return False
    
    def _save_to_file(
        self,
        factor_name: str,
        date_str: str,
        values: pd.Series
    ) -> bool:
        """保存到文件"""
        try:
            factor_dir = self.file_storage_dir / factor_name
            factor_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = factor_dir / f"{date_str}.parquet"
            values.to_frame("value").to_parquet(file_path)
            
            logger.info(f"保存因子值到文件: {factor_name} @ {date_str}")
            return True
        
        except Exception as e:
            logger.error(f"文件保存失败: {e}")
            return False