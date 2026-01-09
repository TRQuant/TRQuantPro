"""
V3.0 统一数据管理模块
=====================

MongoDB统一数据管理，支持:
1. 工作流数据存储
2. 推荐结果归档
3. 回测记录
4. 配置管理
5. 缓存管理

集合结构:
- advisor_v3_market_trend   - 市场趋势分析
- advisor_v3_mainlines      - 主线识别结果
- advisor_v3_momentum       - 动量评分
- advisor_v3_recommendations - 推荐结果
- advisor_v3_backtests      - 回测记录
- advisor_v3_configs        - 配置管理
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import logging
import json

logger = logging.getLogger(__name__)


def _convert_numpy_types(obj):
    """递归转换numpy类型为Python原生类型"""
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_numpy_types(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(_convert_numpy_types(item) for item in obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Series):
        return obj.tolist()
    elif isinstance(obj, pd.DataFrame):
        return obj.to_dict('records')
    else:
        return obj


# ============ 数据结构 ============

@dataclass
class WorkflowStep:
    """工作流步骤数据"""
    step_name: str
    status: str  # "pending" / "running" / "completed" / "failed"
    input_data: Dict = None
    output_data: Dict = None
    start_time: datetime = None
    end_time: datetime = None
    error_message: str = None
    
    def to_dict(self) -> Dict:
        return {
            "step_name": self.step_name,
            "status": self.status,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "error_message": self.error_message,
        }


@dataclass
class WorkflowRecord:
    """工作流记录"""
    workflow_id: str
    workflow_type: str  # "weekly_recommendation" / "backtest" / "optimization"
    created_at: datetime
    updated_at: datetime
    status: str  # "pending" / "running" / "completed" / "failed"
    steps: List[WorkflowStep] = None
    metadata: Dict = None
    
    def to_dict(self) -> Dict:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status,
            "steps": [s.to_dict() for s in (self.steps or [])],
            "metadata": self.metadata,
        }


# ============ MongoDB数据管理器 ============

class DataManagerV3:
    """
    V3.0 MongoDB数据管理器
    
    统一管理所有工作流数据
    """
    
    # 集合名称
    COLLECTIONS = {
        "market_trend": "advisor_v3_market_trend",
        "mainlines": "advisor_v3_mainlines",
        "momentum": "advisor_v3_momentum",
        "recommendations": "advisor_v3_recommendations",
        "backtests": "advisor_v3_backtests",
        "workflows": "advisor_v3_workflows",
        "configs": "advisor_v3_configs",
        "cache": "advisor_v3_cache",
    }
    
    def __init__(
        self,
        mongo_uri: str = None,
        database: str = "trquant",
        use_cache: bool = True,
        cache_ttl_minutes: int = 30,
    ):
        """
        初始化
        
        Args:
            mongo_uri: MongoDB连接URI
            database: 数据库名
            use_cache: 是否使用缓存
            cache_ttl_minutes: 缓存TTL (分钟)
        """
        self.mongo_uri = mongo_uri or "mongodb://localhost:27017/"
        self.database = database
        self.use_cache = use_cache
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        
        self._client = None
        self._db = None
        self._memory_cache: Dict[str, Dict] = {}
    
    def _ensure_connection(self):
        """确保MongoDB连接"""
        if self._client is None:
            try:
                from pymongo import MongoClient
                self._client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
                self._db = self._client[self.database]
                # 测试连接
                self._client.server_info()
                logger.info(f"DataManagerV3: MongoDB连接成功 - {self.database}")
            except Exception as e:
                logger.warning(f"DataManagerV3: MongoDB连接失败 - {e}, 使用内存缓存")
                self._client = None
                self._db = None
    
    def _get_collection(self, name: str):
        """获取集合"""
        self._ensure_connection()
        if self._db is None:
            return None
        return self._db[self.COLLECTIONS.get(name, name)]
    
    # ============ 市场趋势 ============
    
    def save_market_trend(self, date: str, data: Dict):
        """保存市场趋势分析"""
        collection = self._get_collection("market_trend")
        
        # 转换numpy类型
        safe_data = _convert_numpy_types(data)
        
        record = {
            "date": date,
            "data": safe_data,
            "created_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"date": date},
                {"$set": record},
                upsert=True,
            )
        
        # 内存缓存
        cache_key = f"market_trend_{date}"
        self._memory_cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now(),
        }
    
    def get_market_trend(self, date: str) -> Optional[Dict]:
        """获取市场趋势分析"""
        # 检查内存缓存
        cache_key = f"market_trend_{date}"
        if cache_key in self._memory_cache:
            cached = self._memory_cache[cache_key]
            if datetime.now() - cached["timestamp"] < self.cache_ttl:
                return cached["data"]
        
        # 从MongoDB获取
        collection = self._get_collection("market_trend")
        if collection is not None:
            doc = collection.find_one({"date": date})
            if doc:
                return doc.get("data")
        
        return None
    
    # ============ 主线识别 ============
    
    def save_mainlines(self, date: str, data: List[Dict]):
        """保存主线识别结果"""
        collection = self._get_collection("mainlines")
        
        # 转换numpy类型
        safe_data = _convert_numpy_types(data)
        
        record = {
            "date": date,
            "data": safe_data,
            "count": len(data),
            "created_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"date": date},
                {"$set": record},
                upsert=True,
            )
        
        # 内存缓存
        cache_key = f"mainlines_{date}"
        self._memory_cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now(),
        }
    
    def get_mainlines(self, date: str) -> Optional[List[Dict]]:
        """获取主线识别结果"""
        cache_key = f"mainlines_{date}"
        if cache_key in self._memory_cache:
            cached = self._memory_cache[cache_key]
            if datetime.now() - cached["timestamp"] < self.cache_ttl:
                return cached["data"]
        
        collection = self._get_collection("mainlines")
        if collection is not None:
            doc = collection.find_one({"date": date})
            if doc:
                return doc.get("data")
        
        return None
    
    # ============ 动量评分 ============
    
    def save_momentum(self, date: str, data: List[Dict]):
        """保存动量评分"""
        collection = self._get_collection("momentum")
        
        # 转换numpy类型
        safe_data = _convert_numpy_types(data)
        
        record = {
            "date": date,
            "data": safe_data,
            "count": len(data),
            "created_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"date": date},
                {"$set": record},
                upsert=True,
            )
        
        cache_key = f"momentum_{date}"
        self._memory_cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now(),
        }
    
    def get_momentum(self, date: str) -> Optional[List[Dict]]:
        """获取动量评分"""
        cache_key = f"momentum_{date}"
        if cache_key in self._memory_cache:
            cached = self._memory_cache[cache_key]
            if datetime.now() - cached["timestamp"] < self.cache_ttl:
                return cached["data"]
        
        collection = self._get_collection("momentum")
        if collection is not None:
            doc = collection.find_one({"date": date})
            if doc:
                return doc.get("data")
        
        return None
    
    # ============ 推荐结果 ============
    
    def save_recommendations(self, date: str, data: Dict):
        """保存推荐结果"""
        collection = self._get_collection("recommendations")
        
        # 转换numpy类型
        safe_data = _convert_numpy_types(data)
        
        record = {
            "date": date,
            "data": safe_data,
            "created_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"date": date},
                {"$set": record},
                upsert=True,
            )
        
        cache_key = f"recommendations_{date}"
        self._memory_cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now(),
        }
    
    def get_recommendations(self, date: str) -> Optional[Dict]:
        """获取推荐结果"""
        cache_key = f"recommendations_{date}"
        if cache_key in self._memory_cache:
            cached = self._memory_cache[cache_key]
            if datetime.now() - cached["timestamp"] < self.cache_ttl:
                return cached["data"]
        
        collection = self._get_collection("recommendations")
        if collection is not None:
            doc = collection.find_one({"date": date})
            if doc:
                return doc.get("data")
        
        return None
    
    def get_recent_recommendations(self, days: int = 7) -> List[Dict]:
        """获取最近N天的推荐结果"""
        collection = self._get_collection("recommendations")
        
        if collection is None:
            return []
        
        cutoff = datetime.now() - timedelta(days=days)
        docs = collection.find(
            {"created_at": {"$gte": cutoff}}
        ).sort("date", -1)
        
        return [doc.get("data") for doc in docs]
    
    # ============ 回测记录 ============
    
    def save_backtest(self, backtest_id: str, data: Dict):
        """保存回测记录"""
        collection = self._get_collection("backtests")
        
        # 转换numpy类型
        safe_data = _convert_numpy_types(data)
        
        record = {
            "backtest_id": backtest_id,
            "data": safe_data,
            "created_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"backtest_id": backtest_id},
                {"$set": record},
                upsert=True,
            )
    
    def get_backtest(self, backtest_id: str) -> Optional[Dict]:
        """获取回测记录"""
        collection = self._get_collection("backtests")
        
        if collection is None:
            return None
        
        doc = collection.find_one({"backtest_id": backtest_id})
        if doc:
            return doc.get("data")
        
        return None
    
    def list_backtests(self, limit: int = 20) -> List[Dict]:
        """列出回测记录"""
        collection = self._get_collection("backtests")
        
        if collection is None:
            return []
        
        docs = collection.find().sort("created_at", -1).limit(limit)
        return [{"id": doc.get("backtest_id"), **doc.get("data", {})} for doc in docs]
    
    # ============ 工作流管理 ============
    
    def create_workflow(self, workflow_type: str, metadata: Dict = None) -> str:
        """创建工作流"""
        import uuid
        
        workflow_id = str(uuid.uuid4())[:8]
        
        record = WorkflowRecord(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            status="pending",
            steps=[],
            metadata=metadata or {},
        )
        
        collection = self._get_collection("workflows")
        if collection is not None:
            collection.insert_one(record.to_dict())
        
        self._memory_cache[f"workflow_{workflow_id}"] = record
        
        return workflow_id
    
    def update_workflow_step(
        self,
        workflow_id: str,
        step_name: str,
        status: str,
        output_data: Dict = None,
        error_message: str = None,
    ):
        """更新工作流步骤"""
        step = WorkflowStep(
            step_name=step_name,
            status=status,
            output_data=output_data,
            start_time=datetime.now() if status == "running" else None,
            end_time=datetime.now() if status in ["completed", "failed"] else None,
            error_message=error_message,
        )
        
        collection = self._get_collection("workflows")
        if collection is not None:
            collection.update_one(
                {"workflow_id": workflow_id},
                {
                    "$push": {"steps": step.to_dict()},
                    "$set": {
                        "updated_at": datetime.now().isoformat(),
                        "status": status if status in ["failed"] else "running",
                    },
                }
            )
    
    def complete_workflow(self, workflow_id: str, final_result: Dict = None):
        """完成工作流"""
        collection = self._get_collection("workflows")
        if collection is not None:
            collection.update_one(
                {"workflow_id": workflow_id},
                {
                    "$set": {
                        "status": "completed",
                        "updated_at": datetime.now().isoformat(),
                        "final_result": final_result,
                    }
                }
            )
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """获取工作流"""
        collection = self._get_collection("workflows")
        if collection is None:
            return None
        
        doc = collection.find_one({"workflow_id": workflow_id})
        return doc
    
    # ============ 配置管理 ============
    
    def save_config(self, config_name: str, config_data: Dict):
        """保存配置"""
        collection = self._get_collection("configs")
        
        record = {
            "name": config_name,
            "data": config_data,
            "updated_at": datetime.now(),
        }
        
        if collection is not None:
            collection.update_one(
                {"name": config_name},
                {"$set": record},
                upsert=True,
            )
    
    def get_config(self, config_name: str) -> Optional[Dict]:
        """获取配置"""
        collection = self._get_collection("configs")
        
        if collection is None:
            return None
        
        doc = collection.find_one({"name": config_name})
        if doc:
            return doc.get("data")
        
        return None
    
    # ============ 缓存管理 ============
    
    def clear_cache(self, pattern: str = None):
        """清除缓存"""
        if pattern:
            keys_to_remove = [k for k in self._memory_cache if pattern in k]
            for k in keys_to_remove:
                del self._memory_cache[k]
        else:
            self._memory_cache.clear()
        
        logger.info(f"DataManagerV3: 缓存已清除 - {pattern or 'all'}")
    
    def get_cache_stats(self) -> Dict:
        """获取缓存统计"""
        return {
            "memory_cache_size": len(self._memory_cache),
            "cache_keys": list(self._memory_cache.keys())[:20],
        }
    
    # ============ 数据导出 ============
    
    def export_recommendations_to_csv(self, date: str, filepath: str):
        """导出推荐结果到CSV"""
        data = self.get_recommendations(date)
        if not data:
            logger.warning(f"无推荐数据: {date}")
            return
        
        stocks = data.get("recommended_stocks", [])
        if not stocks:
            logger.warning(f"无推荐股票: {date}")
            return
        
        df = pd.DataFrame(stocks)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        logger.info(f"导出成功: {filepath}")
    
    def export_backtest_to_json(self, backtest_id: str, filepath: str):
        """导出回测结果到JSON"""
        data = self.get_backtest(backtest_id)
        if not data:
            logger.warning(f"无回测数据: {backtest_id}")
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"导出成功: {filepath}")
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None


# ============ 便捷函数 ============

_default_manager: DataManagerV3 = None


def get_data_manager() -> DataManagerV3:
    """获取默认数据管理器"""
    global _default_manager
    if _default_manager is None:
        _default_manager = DataManagerV3()
    return _default_manager


def save_recommendation(date: str, data: Dict):
    """保存推荐结果"""
    get_data_manager().save_recommendations(date, data)


def get_recommendation(date: str) -> Optional[Dict]:
    """获取推荐结果"""
    return get_data_manager().get_recommendations(date)
