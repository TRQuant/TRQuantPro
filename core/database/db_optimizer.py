# -*- coding: utf-8 -*-
"""
数据库优化器
============

优化MongoDB存储结构、创建索引、数据归档

功能:
- 集合结构优化
- 索引管理
- 数据归档
- 查询性能分析
- 备份恢复
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import json
import os

logger = logging.getLogger(__name__)

# 尝试导入pymongo
try:
    from pymongo import MongoClient, ASCENDING, DESCENDING
    from pymongo.database import Database
    from pymongo.collection import Collection
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False
    logger.warning("pymongo不可用，数据库功能受限")


@dataclass
class IndexSpec:
    """索引规格"""
    name: str
    keys: List[tuple]  # [(field, direction), ...]
    unique: bool = False
    sparse: bool = False
    background: bool = True
    ttl_seconds: Optional[int] = None


@dataclass
class CollectionConfig:
    """集合配置"""
    name: str
    description: str
    indexes: List[IndexSpec] = field(default_factory=list)
    archive_days: Optional[int] = None
    capped: bool = False
    capped_size: int = 0
    capped_max: int = 0


# ==================== 集合配置定义 ====================

COLLECTION_CONFIGS: Dict[str, CollectionConfig] = {
    "market_status": CollectionConfig(
        name="market_status",
        description="市场状态快照",
        indexes=[
            IndexSpec("idx_date", [("date", -1)]),
            IndexSpec("idx_regime", [("regime", 1)]),
        ],
        archive_days=365
    ),
    
    "mainlines": CollectionConfig(
        name="mainlines",
        description="投资主线数据",
        indexes=[
            IndexSpec("idx_date", [("date", -1)]),
            IndexSpec("idx_score", [("score", -1)]),
        ],
        archive_days=180
    ),
    
    "factors": CollectionConfig(
        name="factors",
        description="因子库",
        indexes=[
            IndexSpec("idx_name", [("name", 1)], unique=True),
            IndexSpec("idx_category", [("category", 1)]),
        ]
    ),
    
    "strategies": CollectionConfig(
        name="strategies",
        description="策略元数据",
        indexes=[
            IndexSpec("idx_name", [("name", 1)]),
            IndexSpec("idx_platform", [("platform", 1)]),
            IndexSpec("idx_updated", [("updated_at", -1)]),
        ]
    ),
    
    "backtest_results": CollectionConfig(
        name="backtest_results",
        description="回测结果",
        indexes=[
            IndexSpec("idx_strategy", [("strategy_id", 1)]),
            IndexSpec("idx_date", [("created_at", -1)]),
            IndexSpec("idx_return", [("total_return", -1)]),
        ],
        archive_days=180
    ),
    
    "trades": CollectionConfig(
        name="trades",
        description="交易记录",
        indexes=[
            IndexSpec("idx_date", [("date", -1)]),
            IndexSpec("idx_symbol", [("symbol", 1)]),
        ],
        archive_days=365
    ),
    
    "reports": CollectionConfig(
        name="reports",
        description="回测报告",
        indexes=[
            IndexSpec("idx_date", [("created_at", -1)]),
            IndexSpec("idx_strategy", [("strategy_id", 1)]),
        ],
        archive_days=365
    ),
    
    "workflow_states": CollectionConfig(
        name="workflow_states",
        description="工作流状态",
        indexes=[
            IndexSpec("idx_workflow_id", [("workflow_id", 1)], unique=True),
            IndexSpec("idx_status", [("status", 1)]),
        ],
        archive_days=30
    ),
    
    "context_cache": CollectionConfig(
        name="context_cache",
        description="上下文缓存",
        indexes=[
            IndexSpec("idx_path", [("file_path", 1)], unique=True),
        ]
    ),
    
    "system_logs": CollectionConfig(
        name="system_logs",
        description="系统日志",
        indexes=[
            IndexSpec("idx_time", [("timestamp", -1)]),
            IndexSpec("idx_level", [("level", 1)]),
        ],
        archive_days=30,
        capped=True,
        capped_size=100 * 1024 * 1024,
        capped_max=100000
    ),
}


class DatabaseOptimizer:
    """数据库优化器"""
    
    def __init__(self, connection_string: str = None, database_name: str = "trquant"):
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", "mongodb://localhost:27017"
        )
        self.database_name = database_name
        self._client = None
        self._db = None
        
    def connect(self):
        """连接数据库"""
        if not PYMONGO_AVAILABLE:
            raise ImportError("pymongo未安装")
            
        if self._client is None:
            self._client = MongoClient(self.connection_string)
            self._db = self._client[self.database_name]
            logger.info(f"已连接: {self.database_name}")
        return self._db
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
    
    def create_indexes(self, collection_name: str = None) -> Dict[str, List[str]]:
        """创建索引"""
        db = self.connect()
        result = {}
        
        configs = {collection_name: COLLECTION_CONFIGS[collection_name]} if collection_name else COLLECTION_CONFIGS
        
        for name, config in configs.items():
            if not config.indexes:
                continue
            
            collection = db[config.name]
            created = []
            
            for idx_spec in config.indexes:
                try:
                    options = {"name": idx_spec.name, "background": idx_spec.background}
                    if idx_spec.unique:
                        options["unique"] = True
                    if idx_spec.sparse:
                        options["sparse"] = True
                    
                    collection.create_index(idx_spec.keys, **options)
                    created.append(idx_spec.name)
                except Exception as e:
                    logger.warning(f"创建索引失败 {config.name}.{idx_spec.name}: {e}")
            
            if created:
                result[name] = created
        
        return result
    
    def archive_old_data(self, collection_name: str = None, dry_run: bool = True) -> Dict[str, int]:
        """归档旧数据"""
        db = self.connect()
        result = {}
        
        configs = {collection_name: COLLECTION_CONFIGS[collection_name]} if collection_name else COLLECTION_CONFIGS
        
        for name, config in configs.items():
            if not config.archive_days:
                continue
            
            collection = db[config.name]
            cutoff_date = datetime.utcnow() - timedelta(days=config.archive_days)
            
            # 查找日期字段
            date_field = self._get_date_field(config)
            if not date_field:
                continue
            
            query = {date_field: {"$lt": cutoff_date}}
            count = collection.count_documents(query)
            
            if count > 0:
                if dry_run:
                    logger.info(f"[试运行] {name}: 将归档 {count} 条")
                else:
                    archive_coll = db[f"{config.name}_archive"]
                    docs = list(collection.find(query))
                    
                    for doc in docs:
                        doc["_archived_at"] = datetime.utcnow()
                    
                    if docs:
                        archive_coll.insert_many(docs)
                    collection.delete_many(query)
                    logger.info(f"已归档 {name}: {count} 条")
                
                result[name] = count
        
        return result
    
    def _get_date_field(self, config: CollectionConfig) -> Optional[str]:
        """获取日期字段"""
        date_fields = ["date", "created_at", "timestamp", "updated_at"]
        for idx in config.indexes:
            for key, _ in idx.keys:
                if key in date_fields:
                    return key
        return None
    
    def analyze_collection(self, collection_name: str) -> Dict[str, Any]:
        """分析集合"""
        db = self.connect()
        stats = db.command("collStats", collection_name)
        
        return {
            "name": collection_name,
            "count": stats.get("count", 0),
            "size": stats.get("size", 0),
            "avgObjSize": stats.get("avgObjSize", 0),
            "storageSize": stats.get("storageSize", 0),
            "totalIndexSize": stats.get("totalIndexSize", 0),
            "nindexes": stats.get("nindexes", 0),
        }
    
    def backup_collection(self, collection_name: str, output_path: str) -> str:
        """备份集合"""
        db = self.connect()
        collection = db[collection_name]
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        documents = list(collection.find())
        
        def convert_doc(doc):
            for key, value in doc.items():
                if key == '_id':
                    doc[key] = str(value)
                elif isinstance(value, datetime):
                    doc[key] = value.isoformat()
            return doc
        
        documents = [convert_doc(doc) for doc in documents]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
        
        logger.info(f"已备份 {collection_name}: {len(documents)} 条")
        return output_path
    
    def restore_collection(self, collection_name: str, input_path: str) -> int:
        """恢复集合"""
        db = self.connect()
        collection = db[collection_name]
        
        with open(input_path, 'r', encoding='utf-8') as f:
            documents = json.load(f)
        
        if documents:
            for doc in documents:
                doc.pop('_id', None)
            collection.insert_many(documents)
        
        logger.info(f"已恢复 {collection_name}: {len(documents)} 条")
        return len(documents)
    
    def ensure_collections(self) -> List[str]:
        """确保集合存在"""
        db = self.connect()
        existing = set(db.list_collection_names())
        created = []
        
        for name, config in COLLECTION_CONFIGS.items():
            if config.name not in existing:
                if config.capped:
                    db.create_collection(
                        config.name,
                        capped=True,
                        size=config.capped_size,
                        max=config.capped_max
                    )
                else:
                    db.create_collection(config.name)
                created.append(config.name)
        
        return created
    
    def get_database_stats(self) -> Dict[str, Any]:
        """获取数据库统计"""
        db = self.connect()
        stats = db.command("dbStats")
        
        return {
            "database": self.database_name,
            "collections": stats.get("collections", 0),
            "objects": stats.get("objects", 0),
            "dataSize": stats.get("dataSize", 0),
            "storageSize": stats.get("storageSize", 0),
            "indexSize": stats.get("indexSize", 0),
        }
    
    def run_full_optimization(self, dry_run: bool = True) -> Dict[str, Any]:
        """执行完整优化"""
        result = {
            "started_at": datetime.utcnow().isoformat(),
            "dry_run": dry_run,
            "steps": {}
        }
        
        logger.info("步骤1: 确保集合存在")
        result["steps"]["ensure_collections"] = self.ensure_collections()
        
        logger.info("步骤2: 创建索引")
        result["steps"]["create_indexes"] = self.create_indexes()
        
        logger.info("步骤3: 归档旧数据")
        result["steps"]["archive_data"] = self.archive_old_data(dry_run=dry_run)
        
        logger.info("步骤4: 数据库统计")
        result["steps"]["db_stats"] = self.get_database_stats()
        
        result["completed_at"] = datetime.utcnow().isoformat()
        return result


def get_optimizer() -> DatabaseOptimizer:
    """获取优化器实例"""
    return DatabaseOptimizer()


def optimize_database(dry_run: bool = True) -> Dict[str, Any]:
    """执行数据库优化"""
    optimizer = get_optimizer()
    try:
        return optimizer.run_full_optimization(dry_run=dry_run)
    finally:
        optimizer.close()
