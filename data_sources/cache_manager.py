# -*- coding: utf-8 -*-
"""
MongoDB数据缓存管理器
=====================

提供统一的数据缓存接口，支持：
- 行情数据缓存（日线、分钟线、Tick）
- 财务数据缓存
- 资讯数据缓存
- 投资主线缓存
"""

from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class MongoDBCache:
    """MongoDB数据缓存管理器"""
    
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "taorui_quant"):
        """
        初始化MongoDB连接
        
        Args:
            uri: MongoDB连接URI
            db_name: 数据库名称
        """
        self.uri = uri
        self.db_name = db_name
        self._client = None
        self._db = None
    
    @property
    def client(self) -> MongoClient:
        """懒加载MongoDB客户端"""
        if self._client is None:
            self._client = MongoClient(self.uri)
        return self._client
    
    @property
    def db(self):
        """获取数据库对象"""
        if self._db is None:
            self._db = self.client[self.db_name]
        return self._db
    
    def is_connected(self) -> bool:
        """检查MongoDB连接状态"""
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False
    
    def get_status(self) -> Dict:
        """获取缓存状态"""
        try:
            if not self.is_connected():
                return {"status": "disconnected", "error": "无法连接MongoDB"}
            
            stats = {
                "status": "connected",
                "database": self.db_name,
                "collections": {}
            }
            
            for coll_name in self.db.list_collection_names():
                count = self.db[coll_name].count_documents({})
                stats["collections"][coll_name] = count
            
            return stats
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    # ============================================================
    # 行情数据
    # ============================================================
    def save_market_data(self, symbol: str, data: pd.DataFrame, 
                         period: str = "1d", source: str = "unknown"):
        """
        保存行情数据
        
        Args:
            symbol: 股票代码
            data: 行情数据DataFrame
            period: 数据周期 (1d, 1m, 5m, tick)
            source: 数据来源
        """
        if data.empty:
            return
        
        collection = self.db.market_data
        records = data.to_dict('records')
        
        for record in records:
            record['symbol'] = symbol
            record['period'] = period
            record['source'] = source
            record['updated_at'] = datetime.now()
            
            # 确保date字段存在
            if 'date' not in record and 'datetime' in record:
                record['date'] = record['datetime']
            
            collection.update_one(
                {"symbol": symbol, "date": record.get('date'), "period": period},
                {"$set": record},
                upsert=True
            )
        
        logger.info(f"保存{symbol}的{period}数据: {len(records)}条")
    
    def get_market_data(self, symbol: str, start_date: str = None, 
                        end_date: str = None, period: str = "1d") -> pd.DataFrame:
        """
        获取行情数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期
            end_date: 结束日期
            period: 数据周期
            
        Returns:
            行情数据DataFrame
        """
        collection = self.db.market_data
        query = {"symbol": symbol, "period": period}
        
        if start_date or end_date:
            query["date"] = {}
            if start_date:
                query["date"]["$gte"] = start_date
            if end_date:
                query["date"]["$lte"] = end_date
        
        cursor = collection.find(query).sort("date", ASCENDING)
        data = list(cursor)
        
        if data:
            df = pd.DataFrame(data)
            # 移除MongoDB的_id字段
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)
            return df
        
        return pd.DataFrame()
    
    def get_cache_info(self, symbol: str, period: str = "1d") -> Dict:
        """获取缓存信息"""
        collection = self.db.market_data
        
        latest = collection.find_one(
            {"symbol": symbol, "period": period},
            sort=[("date", DESCENDING)]
        )
        earliest = collection.find_one(
            {"symbol": symbol, "period": period},
            sort=[("date", ASCENDING)]
        )
        count = collection.count_documents({"symbol": symbol, "period": period})
        
        return {
            "symbol": symbol,
            "period": period,
            "count": count,
            "earliest": earliest.get('date') if earliest else None,
            "latest": latest.get('date') if latest else None,
            "source": latest.get('source') if latest else None,
        }
    
    def get_missing_dates(self, symbol: str, start_date: str, 
                          end_date: str, period: str = "1d") -> List[str]:
        """获取缺失的日期列表"""
        # 获取已缓存的日期
        cached = self.get_market_data(symbol, start_date, end_date, period)
        if cached.empty:
            # 全部缺失，返回日期范围
            return [start_date, end_date]
        
        cached_dates = set(cached['date'].tolist())
        
        # 生成完整日期列表（简化处理，实际应考虑交易日）
        # 这里返回缓存的最新日期，让调用方决定是否需要更新
        return {
            "cached_latest": max(cached_dates) if cached_dates else None,
            "requested_end": end_date,
            "need_update": max(cached_dates) < end_date if cached_dates else True
        }
    
    # ============================================================
    # 财务数据
    # ============================================================
    def save_fundamental_data(self, symbol: str, data: Dict, 
                              report_date: str, report_type: str = "quarterly"):
        """保存财务数据"""
        collection = self.db.fundamental_data
        
        record = {
            "symbol": symbol,
            "report_date": report_date,
            "report_type": report_type,
            "data": data,
            "updated_at": datetime.now()
        }
        
        collection.update_one(
            {"symbol": symbol, "report_date": report_date},
            {"$set": record},
            upsert=True
        )
    
    def get_fundamental_data(self, symbol: str, 
                             report_date: str = None) -> Optional[Dict]:
        """获取财务数据"""
        collection = self.db.fundamental_data
        
        if report_date:
            return collection.find_one({"symbol": symbol, "report_date": report_date})
        else:
            # 获取最新的财务数据
            return collection.find_one(
                {"symbol": symbol},
                sort=[("report_date", DESCENDING)]
            )
    
    # ============================================================
    # 资讯数据
    # ============================================================
    def save_news(self, news_list: List[Dict]):
        """保存资讯"""
        if not news_list:
            return
        
        collection = self.db.news_data
        
        for news in news_list:
            news['created_at'] = datetime.now()
            collection.update_one(
                {"title": news.get('title'), "source": news.get('source')},
                {"$set": news},
                upsert=True
            )
        
        logger.info(f"保存资讯: {len(news_list)}条")
    
    def get_recent_news(self, tags: List[str] = None, 
                        limit: int = 50, 
                        hours: int = 24) -> List[Dict]:
        """获取最新资讯"""
        collection = self.db.news_data
        
        query = {}
        if tags:
            query['tags'] = {"$in": tags}
        
        # 只获取最近N小时的
        if hours:
            cutoff = datetime.now() - timedelta(hours=hours)
            query['publish_time'] = {"$gte": cutoff}
        
        cursor = collection.find(query).sort("publish_time", DESCENDING).limit(limit)
        return list(cursor)
    
    def search_news(self, keyword: str, limit: int = 50) -> List[Dict]:
        """搜索资讯"""
        collection = self.db.news_data
        
        # 简单的文本搜索
        query = {
            "$or": [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"content": {"$regex": keyword, "$options": "i"}}
            ]
        }
        
        cursor = collection.find(query).sort("publish_time", DESCENDING).limit(limit)
        return list(cursor)
    
    # ============================================================
    # 投资主线
    # ============================================================
    def save_theme(self, theme: Dict):
        """保存投资主线"""
        collection = self.db.investment_themes
        
        theme['updated_at'] = datetime.now()
        collection.update_one(
            {"name": theme.get('name')},
            {"$set": theme},
            upsert=True
        )
    
    def get_hot_themes(self, limit: int = 10) -> List[Dict]:
        """获取热门主线"""
        collection = self.db.investment_themes
        cursor = collection.find().sort("heat_score", DESCENDING).limit(limit)
        return list(cursor)
    
    def get_theme_by_name(self, name: str) -> Optional[Dict]:
        """根据名称获取主线"""
        collection = self.db.investment_themes
        return collection.find_one({"name": name})
    
    def update_theme_heat(self, name: str, heat_score: int):
        """更新主线热度"""
        collection = self.db.investment_themes
        collection.update_one(
            {"name": name},
            {"$set": {"heat_score": heat_score, "updated_at": datetime.now()}}
        )
    
    # ============================================================
    # 观察池
    # ============================================================
    def save_watchlist(self, name: str, symbols: List[str], 
                       notes: str = "", theme_name: str = None):
        """保存观察池"""
        collection = self.db.watchlist
        
        record = {
            "name": name,
            "symbols": symbols,
            "notes": notes,
            "theme_name": theme_name,
            "updated_at": datetime.now()
        }
        
        collection.update_one(
            {"name": name},
            {"$set": record},
            upsert=True
        )
    
    def get_watchlists(self) -> List[Dict]:
        """获取所有观察池"""
        collection = self.db.watchlist
        return list(collection.find())
    
    def get_watchlist(self, name: str) -> Optional[Dict]:
        """获取指定观察池"""
        collection = self.db.watchlist
        return collection.find_one({"name": name})
    
    def delete_watchlist(self, name: str):
        """删除观察池"""
        collection = self.db.watchlist
        collection.delete_one({"name": name})
    
    # ============================================================
    # 数据源状态
    # ============================================================
    def save_source_status(self, source_name: str, status: Dict):
        """保存数据源状态"""
        collection = self.db.data_source_status
        
        record = {
            "source": source_name,
            "status": status.get('status', 'unknown'),
            "latency": status.get('latency'),
            "last_check": datetime.now(),
            "error": status.get('error'),
            "quota": status.get('quota')
        }
        
        collection.update_one(
            {"source": source_name},
            {"$set": record},
            upsert=True
        )
    
    def get_source_status(self, source_name: str = None) -> Any:
        """获取数据源状态"""
        collection = self.db.data_source_status
        
        if source_name:
            return collection.find_one({"source": source_name})
        else:
            return list(collection.find())
    
    # ============================================================
    # 清理
    # ============================================================
    def clear_old_data(self, days: int = 365):
        """清理旧数据"""
        cutoff = datetime.now() - timedelta(days=days)
        
        # 清理旧资讯
        result = self.db.news_data.delete_many({"publish_time": {"$lt": cutoff}})
        logger.info(f"清理旧资讯: {result.deleted_count}条")
        
        return {"news_deleted": result.deleted_count}
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None





