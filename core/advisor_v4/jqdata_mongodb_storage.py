#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JQData MongoDB存储模块
=====================

功能：
1. 将JQData下载的数据存入MongoDB
2. 后续直接调用，不用重复下载
3. 支持数据版本管理和去重
4. 支持增量更新
"""

from __future__ import annotations

import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# MongoDB可用性检查
try:
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.errors import DuplicateKeyError
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("pymongo未安装，MongoDB存储功能不可用")


class JQDataMongoDBStorage:
    """
    JQData数据MongoDB存储管理器
    
    将JQData下载的数据存入MongoDB，后续直接调用，不用重复下载
    """
    
    # MongoDB配置
    MONGO_URI = "mongodb://localhost:27017"
    DB_NAME = "trquant_jqdata"
    
    # 集合名称
    COLLECTIONS = {
        "daily_prices": "jqdata_daily_prices",
        "valuation": "jqdata_valuation",
        "indicator": "jqdata_indicator",
        "trade_days": "jqdata_trade_days",
        "index_stocks": "jqdata_index_stocks",
        "metadata": "jqdata_metadata",
    }
    
    def __init__(
        self,
        mongo_uri: str = None,
        db_name: str = None,
        use_file_fallback: bool = True
    ):
        """
        初始化存储管理器
        
        Args:
            mongo_uri: MongoDB连接URI
            db_name: 数据库名称
            use_file_fallback: MongoDB不可用时使用文件存储
        """
        self.mongo_uri = mongo_uri or self.MONGO_URI
        self.db_name = db_name or self.DB_NAME
        self.use_file_fallback = use_file_fallback
        
        self.client = None
        self.db = None
        self._connected = False
        
        # 文件存储路径（备用）
        self.file_storage_dir = Path.home() / ".local/share/trquant/jqdata"
        self.file_storage_dir.mkdir(parents=True, exist_ok=True)
        
        self._connect()
    
    def _connect(self):
        """连接MongoDB"""
        if not MONGODB_AVAILABLE:
            logger.warning("pymongo不可用，使用文件存储")
            return
        
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            # 测试连接
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self._connected = True
            
            # 创建索引
            self._create_indexes()
            
            logger.info(f"JQData MongoDB连接成功: {self.db_name}")
            
        except Exception as e:
            logger.warning(f"JQData MongoDB连接失败: {e}，使用文件存储")
            self._connected = False
    
    def _create_indexes(self):
        """创建索引"""
        if not self._connected:
            return
        
        try:
            # 价格数据索引
            self.db[self.COLLECTIONS["daily_prices"]].create_index(
                [("code", ASCENDING), ("date", ASCENDING)], unique=True
            )
            self.db[self.COLLECTIONS["daily_prices"]].create_index([("date", DESCENDING)])
            self.db[self.COLLECTIONS["daily_prices"]].create_index([("period_key", ASCENDING)])
            
            # 估值数据索引
            self.db[self.COLLECTIONS["valuation"]].create_index(
                [("code", ASCENDING), ("date", ASCENDING)], unique=True
            )
            self.db[self.COLLECTIONS["valuation"]].create_index([("date", DESCENDING)])
            self.db[self.COLLECTIONS["valuation"]].create_index([("period_key", ASCENDING)])
            
            # 财务指标索引
            self.db[self.COLLECTIONS["indicator"]].create_index(
                [("code", ASCENDING), ("date", ASCENDING)], unique=True
            )
            self.db[self.COLLECTIONS["indicator"]].create_index([("date", DESCENDING)])
            self.db[self.COLLECTIONS["indicator"]].create_index([("period_key", ASCENDING)])
            
            # 交易日索引
            self.db[self.COLLECTIONS["trade_days"]].create_index(
                [("period_key", ASCENDING)], unique=True
            )
            
            # 指数成分股索引
            self.db[self.COLLECTIONS["index_stocks"]].create_index(
                [("index_code", ASCENDING), ("date", ASCENDING)], unique=True
            )
            
            logger.debug("JQData MongoDB索引已创建")
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def _generate_data_hash(self, data: pd.DataFrame) -> str:
        """生成数据哈希值（用于去重）"""
        # 使用数据的shape和列名生成哈希
        hash_str = f"{data.shape}_{','.join(sorted(data.columns))}"
        return hashlib.md5(hash_str.encode()).hexdigest()
    
    def save_daily_prices(
        self,
        df: pd.DataFrame,
        period_key: str,
        start_date: str,
        end_date: str
    ) -> bool:
        """
        保存日线价格数据
        
        Args:
            df: 价格数据DataFrame
            period_key: 时间段键（如"2024H2"）
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            是否成功
        """
        if df is None or df.empty:
            return False
        
        try:
            if self._connected:
                # 转换为字典列表
                records = df.to_dict('records')
                
                # 批量插入（使用upsert避免重复）
                collection = self.db[self.COLLECTIONS["daily_prices"]]
                
                # 先删除该时间段的数据
                collection.delete_many({"period_key": period_key})
                
                # 插入新数据
                for record in records:
                    record["period_key"] = period_key
                    record["start_date"] = start_date
                    record["end_date"] = end_date
                    record["created_at"] = datetime.now()
                    # 确保date字段是字符串
                    if "date" in record and isinstance(record["date"], datetime):
                        record["date"] = record["date"].strftime("%Y-%m-%d")
                    elif "time" in record and isinstance(record["time"], datetime):
                        record["date"] = record["time"].strftime("%Y-%m-%d")
                
                collection.insert_many(records)
                logger.info(f"✅ 价格数据已保存到MongoDB: {len(records)}条，period_key={period_key}")
                return True
            else:
                # 文件存储
                cache_file = self.file_storage_dir / f"daily_prices_{period_key}.parquet"
                df.to_parquet(cache_file, index=False)
                logger.info(f"✅ 价格数据已保存到文件: {cache_file}")
                return True
        except Exception as e:
            logger.error(f"保存价格数据失败: {e}")
            return False
    
    def load_daily_prices(
        self,
        period_key: str = None,
        start_date: str = None,
        end_date: str = None,
        codes: List[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        加载日线价格数据
        
        Args:
            period_key: 时间段键（优先）
            start_date: 开始日期
            end_date: 结束日期
            codes: 股票代码列表（可选）
        
        Returns:
            DataFrame or None
        """
        try:
            if self._connected:
                collection = self.db[self.COLLECTIONS["daily_prices"]]
                
                # 构建查询条件
                query = {}
                if period_key:
                    query["period_key"] = period_key
                elif start_date and end_date:
                    query["date"] = {"$gte": start_date, "$lte": end_date}
                
                if codes:
                    query["code"] = {"$in": codes}
                
                # 查询数据
                cursor = collection.find(query)
                records = list(cursor)
                
                if not records:
                    return None
                
                # 转换为DataFrame
                df = pd.DataFrame(records)
                
                # 删除MongoDB特有的字段
                df = df.drop(columns=["_id", "period_key", "start_date", "end_date", "created_at"], errors="ignore")
                
                logger.info(f"✅ 从MongoDB加载价格数据: {len(df)}条")
                return df
            else:
                # 文件存储
                if period_key:
                    cache_file = self.file_storage_dir / f"daily_prices_{period_key}.parquet"
                    if cache_file.exists():
                        df = pd.read_parquet(cache_file)
                        logger.info(f"✅ 从文件加载价格数据: {len(df)}条")
                        return df
                return None
        except Exception as e:
            logger.error(f"加载价格数据失败: {e}")
            return None
    
    def save_fundamentals(
        self,
        df: pd.DataFrame,
        data_type: str,  # "valuation" or "indicator"
        period_key: str,
        date: str
    ) -> bool:
        """
        保存基本面数据
        
        Args:
            df: 基本面数据DataFrame
            data_type: 数据类型（"valuation"或"indicator"）
            period_key: 时间段键
            date: 数据日期
        
        Returns:
            是否成功
        """
        if df is None or df.empty:
            return False
        
        if data_type not in ["valuation", "indicator"]:
            logger.error(f"不支持的基本面数据类型: {data_type}")
            return False
        
        try:
            if self._connected:
                collection = self.db[self.COLLECTIONS[data_type]]
                
                # 转换为字典列表
                records = df.to_dict('records')
                
                # 先删除该时间段的数据
                collection.delete_many({"period_key": period_key, "date": date})
                
                # 插入新数据
                for record in records:
                    record["period_key"] = period_key
                    record["date"] = date
                    record["created_at"] = datetime.now()
                
                collection.insert_many(records)
                logger.info(f"✅ {data_type}数据已保存到MongoDB: {len(records)}条，date={date}")
                return True
            else:
                # 文件存储
                cache_file = self.file_storage_dir / f"{data_type}_{period_key}_{date}.parquet"
                df.to_parquet(cache_file, index=False)
                logger.info(f"✅ {data_type}数据已保存到文件: {cache_file}")
                return True
        except Exception as e:
            logger.error(f"保存{data_type}数据失败: {e}")
            return False
    
    def load_fundamentals(
        self,
        data_type: str,
        period_key: str = None,
        date: str = None,
        codes: List[str] = None
    ) -> Optional[pd.DataFrame]:
        """
        加载基本面数据
        
        Args:
            data_type: 数据类型（"valuation"或"indicator"）
            period_key: 时间段键
            date: 数据日期
            codes: 股票代码列表（可选）
        
        Returns:
            DataFrame or None
        """
        if data_type not in ["valuation", "indicator"]:
            return None
        
        try:
            if self._connected:
                collection = self.db[self.COLLECTIONS[data_type]]
                
                # 构建查询条件
                query = {}
                if period_key:
                    query["period_key"] = period_key
                if date:
                    query["date"] = date
                if codes:
                    query["code"] = {"$in": codes}
                
                # 查询数据
                cursor = collection.find(query)
                records = list(cursor)
                
                if not records:
                    return None
                
                # 转换为DataFrame
                df = pd.DataFrame(records)
                
                # 删除MongoDB特有的字段
                df = df.drop(columns=["_id", "period_key", "created_at"], errors="ignore")
                
                logger.info(f"✅ 从MongoDB加载{data_type}数据: {len(df)}条")
                return df
            else:
                # 文件存储
                if period_key and date:
                    cache_file = self.file_storage_dir / f"{data_type}_{period_key}_{date}.parquet"
                    if cache_file.exists():
                        df = pd.read_parquet(cache_file)
                        logger.info(f"✅ 从文件加载{data_type}数据: {len(df)}条")
                        return df
                return None
        except Exception as e:
            logger.error(f"加载{data_type}数据失败: {e}")
            return None
    
    def save_trade_days(
        self,
        trade_days: List[datetime],
        period_key: str,
        start_date: str,
        end_date: str
    ) -> bool:
        """
        保存交易日数据
        
        Args:
            trade_days: 交易日列表
            period_key: 时间段键
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            是否成功
        """
        try:
            if self._connected:
                collection = self.db[self.COLLECTIONS["trade_days"]]
                
                # 转换为字符串列表
                trade_days_str = [d.strftime("%Y-%m-%d") if isinstance(d, datetime) else str(d) for d in trade_days]
                
                # 使用upsert
                collection.update_one(
                    {"period_key": period_key},
                    {
                        "$set": {
                            "trade_days": trade_days_str,
                            "start_date": start_date,
                            "end_date": end_date,
                            "updated_at": datetime.now()
                        }
                    },
                    upsert=True
                )
                
                logger.info(f"✅ 交易日数据已保存到MongoDB: {len(trade_days)}天，period_key={period_key}")
                return True
            else:
                # 文件存储
                df = pd.DataFrame({
                    "date": trade_days_str,
                    "datetime": trade_days
                })
                cache_file = self.file_storage_dir / f"trade_days_{period_key}.parquet"
                df.to_parquet(cache_file, index=False)
                logger.info(f"✅ 交易日数据已保存到文件: {cache_file}")
                return True
        except Exception as e:
            logger.error(f"保存交易日数据失败: {e}")
            return False
    
    def load_trade_days(
        self,
        period_key: str = None,
        start_date: str = None,
        end_date: str = None
    ) -> Optional[List[str]]:
        """
        加载交易日数据
        
        Args:
            period_key: 时间段键（优先）
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            交易日字符串列表 or None
        """
        try:
            if self._connected:
                collection = self.db[self.COLLECTIONS["trade_days"]]
                
                # 构建查询条件
                query = {}
                if period_key:
                    query["period_key"] = period_key
                elif start_date and end_date:
                    query["start_date"] = {"$lte": end_date}
                    query["end_date"] = {"$gte": start_date}
                
                # 查询数据
                doc = collection.find_one(query)
                
                if doc and "trade_days" in doc:
                    logger.info(f"✅ 从MongoDB加载交易日数据: {len(doc['trade_days'])}天")
                    return doc["trade_days"]
                return None
            else:
                # 文件存储
                if period_key:
                    cache_file = self.file_storage_dir / f"trade_days_{period_key}.parquet"
                    if cache_file.exists():
                        df = pd.read_parquet(cache_file)
                        trade_days = df["date"].tolist()
                        logger.info(f"✅ 从文件加载交易日数据: {len(trade_days)}天")
                        return trade_days
                return None
        except Exception as e:
            logger.error(f"加载交易日数据失败: {e}")
            return None
    
    def check_data_exists(
        self,
        data_type: str,
        period_key: str,
        date: str = None
    ) -> bool:
        """
        检查数据是否存在
        
        Args:
            data_type: 数据类型（"daily_prices", "valuation", "indicator", "trade_days"）
            period_key: 时间段键
            date: 数据日期（可选）
        
        Returns:
            是否存在
        """
        try:
            if self._connected:
                if data_type == "trade_days":
                    collection = self.db[self.COLLECTIONS["trade_days"]]
                    return collection.count_documents({"period_key": period_key}) > 0
                else:
                    collection = self.db[self.COLLECTIONS[data_type]]
                    query = {"period_key": period_key}
                    if date:
                        query["date"] = date
                    return collection.count_documents(query) > 0
            else:
                # 文件存储
                if data_type == "trade_days":
                    cache_file = self.file_storage_dir / f"trade_days_{period_key}.parquet"
                elif date:
                    cache_file = self.file_storage_dir / f"{data_type}_{period_key}_{date}.parquet"
                else:
                    cache_file = self.file_storage_dir / f"{data_type}_{period_key}.parquet"
                return cache_file.exists()
        except Exception as e:
            logger.error(f"检查数据存在性失败: {e}")
            return False
    
    def get_storage_stats(self) -> Dict[str, Any]:
        """获取存储统计信息"""
        stats = {
            "connected": self._connected,
            "db_name": self.db_name if self._connected else None,
            "collections": {}
        }
        
        if self._connected:
            for name, collection_name in self.COLLECTIONS.items():
                try:
                    count = self.db[collection_name].count_documents({})
                    stats["collections"][name] = {
                        "count": count,
                        "collection": collection_name
                    }
                except Exception as e:
                    stats["collections"][name] = {"error": str(e)}
        
        return stats
