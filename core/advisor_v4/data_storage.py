# -*- coding: utf-8 -*-
"""
V4.0投资推荐系统数据存储模块
============================

基于现有MongoDB存储模块设计，提供V4.0系统专用存储：
- 策略代码存储
- 回测结果存储
- 推荐记录存储
- 模型参数存储

复用项目现有模块：
- core/market_trend_storage.py - 市场趋势存储
- core/factors/factor_storage.py - 因子存储
- core/time_dimension_manager.py - 时间维度存储

数据库结构:
- trquant_v4.strategy_codes     - 策略代码
- trquant_v4.backtest_results   - 回测结果
- trquant_v4.recommendations    - 推荐记录
- trquant_v4.model_params       - 模型参数
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, asdict, field
import json
import hashlib
import inspect

logger = logging.getLogger(__name__)

# MongoDB可用性检测
try:
    from pymongo import MongoClient, DESCENDING, ASCENDING
    from pymongo.errors import ConnectionFailure
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("pymongo未安装，MongoDB存储功能不可用")


@dataclass
class StrategyCodeRecord:
    """策略代码记录"""
    strategy_id: str                  # 策略ID
    strategy_name: str                # 策略名称
    strategy_code: str                # 策略代码（聚宽格式）
    strategy_type: str = "multi_factor"  # 策略类型
    
    # 策略配置
    config: Dict = field(default_factory=dict)
    
    # 元数据
    created_at: str = ""
    updated_at: str = ""
    version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        now = datetime.now().isoformat()
        if not d['created_at']:
            d['created_at'] = now
        d['updated_at'] = now
        return d


@dataclass
class BacktestResultRecord:
    """回测结果记录"""
    backtest_id: str                  # 回测ID
    strategy_id: str                  # 策略ID
    
    # 回测配置
    start_date: str
    end_date: str
    initial_capital: float = 1000000.0
    backtest_level: str = "fast"      # fast/standard/precise
    engine: str = "fast"              # fast/bullettrade/qmt

    # 去重/版本管理（phase4-cache）
    config_hash: str = ""             # 参数哈希（用于缓存查找）
    algorithm_version: str = ""       # 算法版本（基于关键代码哈希）
    version_tag: Optional[str] = None # 用户自定义版本标签（可选）
    config: Dict = field(default_factory=dict)  # 回测配置（可序列化）
    
    # 回测结果
    total_return: float = 0.0
    annualized_return: float = 0.0
    max_drawdown: float = 0.0
    sharpe_ratio: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    
    # 详细指标
    metrics: Dict = field(default_factory=dict)
    
    # 交易记录
    trades: List[Dict] = field(default_factory=list)
    
    # 元数据
    created_at: str = ""
    duration_seconds: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d['created_at']:
            d['created_at'] = datetime.now().isoformat()
        return d


@dataclass
class RecommendationRecord:
    """推荐记录"""
    recommendation_id: str            # 推荐ID
    date: str                         # 推荐日期
    
    # 推荐标的
    stocks: List[Dict] = field(default_factory=list)  # [{code, name, score, weight, reason}]
    
    # 市场状态
    market_trend: str = "neutral"     # bullish/bearish/neutral
    market_score: float = 0.0
    
    # 仓位建议
    position_advice: float = 0.5      # 0-1
    
    # 策略配置
    strategy_id: str = ""
    config: Dict = field(default_factory=dict)
    
    # 元数据
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d['created_at']:
            d['created_at'] = datetime.now().isoformat()
        return d


@dataclass
class ModelParamsRecord:
    """模型参数记录"""
    model_id: str                     # 模型ID
    model_type: str = "xgboost"       # xgboost/lightgbm/etc
    
    # 模型参数
    params: Dict = field(default_factory=dict)
    
    # 特征列表
    features: List[str] = field(default_factory=list)
    
    # 训练信息
    train_start: str = ""
    train_end: str = ""
    train_samples: int = 0
    
    # 性能指标
    train_score: float = 0.0
    valid_score: float = 0.0
    feature_importance: Dict = field(default_factory=dict)
    
    # 元数据
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d['created_at']:
            d['created_at'] = datetime.now().isoformat()
        return d


class V4DataStorage:
    """
    V4.0投资推荐系统数据存储
    
    使用MongoDB存储策略代码、回测结果、推荐记录和模型参数
    支持文件存储作为备份
    """
    
    # MongoDB配置
    MONGO_URI = "mongodb://localhost:27017"
    DB_NAME = "trquant_v4"
    
    # 集合名称
    STRATEGY_COLLECTION = "strategy_codes"
    BACKTEST_COLLECTION = "backtest_results"
    RECOMMENDATION_COLLECTION = "recommendations"
    MODEL_COLLECTION = "model_params"
    
    def __init__(self, mongo_uri: str = None, db_name: str = None, 
                 use_file_fallback: bool = True):
        """
        初始化存储
        
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
        
        # 文件存储路径
        self.file_storage_dir = Path.home() / ".local/share/trquant/v4"
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
            
            logger.info(f"MongoDB连接成功: {self.db_name}")
            
        except Exception as e:
            logger.warning(f"MongoDB连接失败: {e}，使用文件存储")
            self._connected = False
    
    def _create_indexes(self):
        """创建索引"""
        if not self._connected:
            return
        
        try:
            # 策略代码索引
            self.db[self.STRATEGY_COLLECTION].create_index(
                [("strategy_id", ASCENDING)], unique=True
            )
            self.db[self.STRATEGY_COLLECTION].create_index([("created_at", DESCENDING)])
            
            # 回测结果索引
            self.db[self.BACKTEST_COLLECTION].create_index(
                [("backtest_id", ASCENDING)], unique=True
            )
            self.db[self.BACKTEST_COLLECTION].create_index([("strategy_id", ASCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([("created_at", DESCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([("backtest_level", ASCENDING)])
            # phase4-cache: 缓存索引（backtest_level + config_hash + algorithm_version）
            self.db[self.BACKTEST_COLLECTION].create_index([("config_hash", ASCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index([("algorithm_version", ASCENDING)])
            self.db[self.BACKTEST_COLLECTION].create_index(
                [("backtest_level", ASCENDING), ("config_hash", ASCENDING), ("algorithm_version", ASCENDING)],
                name="idx_level_hash_ver",
            )
            
            # 推荐记录索引
            self.db[self.RECOMMENDATION_COLLECTION].create_index(
                [("recommendation_id", ASCENDING)], unique=True
            )
            self.db[self.RECOMMENDATION_COLLECTION].create_index([("date", DESCENDING)])
            
            # 模型参数索引
            self.db[self.MODEL_COLLECTION].create_index(
                [("model_id", ASCENDING)], unique=True
            )
            self.db[self.MODEL_COLLECTION].create_index([("created_at", DESCENDING)])
            
            logger.debug("MongoDB索引已创建")
            
        except Exception as e:
            logger.warning(f"创建索引失败: {e}")
    
    def is_connected(self) -> bool:
        """检查是否已连接MongoDB"""
        return self._connected
    
    # ==================== 策略代码存储 ====================
    
    def save_strategy(self, record: StrategyCodeRecord) -> bool:
        """保存策略代码"""
        doc = record.to_dict()
        
        if self._connected:
            try:
                result = self.db[self.STRATEGY_COLLECTION].update_one(
                    {"strategy_id": record.strategy_id},
                    {"$set": doc},
                    upsert=True
                )
                logger.info(f"策略代码已保存: {record.strategy_id}")
                return True
            except Exception as e:
                logger.error(f"保存策略代码失败: {e}")
                if self.use_file_fallback:
                    return self._save_to_file("strategies", record.strategy_id, doc)
                return False
        elif self.use_file_fallback:
            return self._save_to_file("strategies", record.strategy_id, doc)
        
        return False
    
    def get_strategy(self, strategy_id: str) -> Optional[Dict]:
        """获取策略代码"""
        if self._connected:
            try:
                result = self.db[self.STRATEGY_COLLECTION].find_one(
                    {"strategy_id": strategy_id}
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取策略代码失败: {e}")
        
        # 尝试从文件读取
        if self.use_file_fallback:
            return self._load_from_file("strategies", strategy_id)
        
        return None
    
    def list_strategies(self, limit: int = 100) -> List[Dict]:
        """列出所有策略"""
        if self._connected:
            try:
                cursor = self.db[self.STRATEGY_COLLECTION].find().sort(
                    "created_at", DESCENDING
                ).limit(limit)
                results = []
                for doc in cursor:
                    doc.pop("_id", None)
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"列出策略失败: {e}")
        
        return []
    
    # ==================== 回测结果存储 ====================
    
    def save_backtest_result(self, record: BacktestResultRecord) -> bool:
        """保存回测结果"""
        doc = record.to_dict()
        
        if self._connected:
            try:
                result = self.db[self.BACKTEST_COLLECTION].update_one(
                    {"backtest_id": record.backtest_id},
                    {"$set": doc},
                    upsert=True
                )
                logger.info(f"回测结果已保存: {record.backtest_id}")
                return True
            except Exception as e:
                logger.error(f"保存回测结果失败: {e}")
                if self.use_file_fallback:
                    return self._save_to_file("backtests", record.backtest_id, doc)
                return False
        elif self.use_file_fallback:
            return self._save_to_file("backtests", record.backtest_id, doc)
        
        return False

    def find_cached_backtest(
        self,
        config_hash: str,
        backtest_level: str,
        algorithm_version: str,
        strategy_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """根据 (level, config_hash, algorithm_version) 查找缓存回测结果（最新一条）。"""
        if not self._connected:
            return None
        try:
            query: Dict[str, Any] = {
                "config_hash": config_hash,
                "backtest_level": backtest_level,
                "algorithm_version": algorithm_version,
            }
            if strategy_id:
                query["strategy_id"] = strategy_id

            doc = self.db[self.BACKTEST_COLLECTION].find_one(query, sort=[("created_at", DESCENDING)])
            if doc:
                doc.pop("_id", None)
                return doc
            return None
        except Exception as e:
            logger.error(f"查找缓存回测结果失败: {e}")
            return None

    
    def get_backtest_result(self, backtest_id: str) -> Optional[Dict]:
        """获取回测结果"""
        if self._connected:
            try:
                result = self.db[self.BACKTEST_COLLECTION].find_one(
                    {"backtest_id": backtest_id}
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取回测结果失败: {e}")
        
        if self.use_file_fallback:
            return self._load_from_file("backtests", backtest_id)
        
        return None
    
    def list_backtest_results(self, strategy_id: str = None, 
                               backtest_level: str = None,
                               limit: int = 100) -> List[Dict]:
        """列出回测结果"""
        if self._connected:
            try:
                query = {}
                if strategy_id:
                    query["strategy_id"] = strategy_id
                if backtest_level:
                    query["backtest_level"] = backtest_level
                
                cursor = self.db[self.BACKTEST_COLLECTION].find(query).sort(
                    "created_at", DESCENDING
                ).limit(limit)
                
                results = []
                for doc in cursor:
                    doc.pop("_id", None)
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"列出回测结果失败: {e}")
        
        return []
    
    # ==================== 推荐记录存储 ====================
    
    def save_recommendation(self, record: RecommendationRecord) -> bool:
        """保存推荐记录"""
        doc = record.to_dict()
        
        if self._connected:
            try:
                result = self.db[self.RECOMMENDATION_COLLECTION].update_one(
                    {"recommendation_id": record.recommendation_id},
                    {"$set": doc},
                    upsert=True
                )
                logger.info(f"推荐记录已保存: {record.recommendation_id}")
                return True
            except Exception as e:
                logger.error(f"保存推荐记录失败: {e}")
                if self.use_file_fallback:
                    return self._save_to_file("recommendations", record.recommendation_id, doc)
                return False
        elif self.use_file_fallback:
            return self._save_to_file("recommendations", record.recommendation_id, doc)
        
        return False
    
    def get_recommendation(self, recommendation_id: str) -> Optional[Dict]:
        """获取推荐记录"""
        if self._connected:
            try:
                result = self.db[self.RECOMMENDATION_COLLECTION].find_one(
                    {"recommendation_id": recommendation_id}
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取推荐记录失败: {e}")
        
        if self.use_file_fallback:
            return self._load_from_file("recommendations", recommendation_id)
        
        return None
    
    def get_latest_recommendation(self) -> Optional[Dict]:
        """获取最新推荐"""
        if self._connected:
            try:
                result = self.db[self.RECOMMENDATION_COLLECTION].find_one(
                    sort=[("date", DESCENDING)]
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取最新推荐失败: {e}")
        
        return None
    
    def list_recommendations(self, start_date: str = None, 
                              end_date: str = None,
                              limit: int = 100) -> List[Dict]:
        """列出推荐记录"""
        if self._connected:
            try:
                query = {}
                if start_date:
                    query["date"] = {"$gte": start_date}
                if end_date:
                    if "date" in query:
                        query["date"]["$lte"] = end_date
                    else:
                        query["date"] = {"$lte": end_date}
                
                cursor = self.db[self.RECOMMENDATION_COLLECTION].find(query).sort(
                    "date", DESCENDING
                ).limit(limit)
                
                results = []
                for doc in cursor:
                    doc.pop("_id", None)
                    results.append(doc)
                return results
            except Exception as e:
                logger.error(f"列出推荐记录失败: {e}")
        
        return []
    
    # ==================== 模型参数存储 ====================
    
    def save_model_params(self, record: ModelParamsRecord) -> bool:
        """保存模型参数"""
        doc = record.to_dict()
        
        if self._connected:
            try:
                result = self.db[self.MODEL_COLLECTION].update_one(
                    {"model_id": record.model_id},
                    {"$set": doc},
                    upsert=True
                )
                logger.info(f"模型参数已保存: {record.model_id}")
                return True
            except Exception as e:
                logger.error(f"保存模型参数失败: {e}")
                if self.use_file_fallback:
                    return self._save_to_file("models", record.model_id, doc)
                return False
        elif self.use_file_fallback:
            return self._save_to_file("models", record.model_id, doc)
        
        return False
    
    def get_model_params(self, model_id: str) -> Optional[Dict]:
        """获取模型参数"""
        if self._connected:
            try:
                result = self.db[self.MODEL_COLLECTION].find_one(
                    {"model_id": model_id}
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取模型参数失败: {e}")
        
        if self.use_file_fallback:
            return self._load_from_file("models", model_id)
        
        return None
    
    def get_latest_model(self, model_type: str = None) -> Optional[Dict]:
        """获取最新模型"""
        if self._connected:
            try:
                query = {}
                if model_type:
                    query["model_type"] = model_type
                
                result = self.db[self.MODEL_COLLECTION].find_one(
                    query, sort=[("created_at", DESCENDING)]
                )
                if result:
                    result.pop("_id", None)
                return result
            except Exception as e:
                logger.error(f"获取最新模型失败: {e}")
        
        return None
    
    # ==================== 文件存储（备份） ====================
    
    def _save_to_file(self, category: str, record_id: str, data: Dict) -> bool:
        """保存到文件"""
        try:
            category_dir = self.file_storage_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            filepath = category_dir / f"{record_id}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            
            logger.debug(f"已保存到文件: {filepath}")
            return True
        except Exception as e:
            logger.error(f"保存到文件失败: {e}")
            return False
    
    def _load_from_file(self, category: str, record_id: str) -> Optional[Dict]:
        """从文件加载"""
        try:
            filepath = self.file_storage_dir / category / f"{record_id}.json"
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"从文件加载失败: {e}")
        
        return None
    
    # ==================== 统计方法 ====================
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取存储统计"""
        stats = {
            "mongodb_connected": self._connected,
            "file_storage_dir": str(self.file_storage_dir),
            "collections": {}
        }
        
        if self._connected:
            try:
                stats["collections"]["strategies"] = self.db[self.STRATEGY_COLLECTION].count_documents({})
                stats["collections"]["backtests"] = self.db[self.BACKTEST_COLLECTION].count_documents({})
                stats["collections"]["recommendations"] = self.db[self.RECOMMENDATION_COLLECTION].count_documents({})
                stats["collections"]["models"] = self.db[self.MODEL_COLLECTION].count_documents({})
            except Exception as e:
                logger.error(f"获取统计失败: {e}")
        
        return stats


# ==================== phase4-cache: 配置哈希 & 算法版本 ====================

_ALGO_VERSION_CACHE: Optional[str] = None


def compute_config_hash(config: Dict[str, Any]) -> str:
    """计算配置哈希（用于缓存查找）。"""
    key_params = {k: v for k, v in (config or {}).items() if k not in {"created_at", "updated_at", "timestamp"}}
    s = json.dumps(key_params, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def compute_algorithm_version() -> str:
    """计算算法版本（基于关键回测/策略代码片段哈希）。"""
    global _ALGO_VERSION_CACHE
    if _ALGO_VERSION_CACHE:
        return _ALGO_VERSION_CACHE

    try:
        from core.advisor_v4.backtest_engine import BacktestEngine, V4StrategyAdapter
        from core.backtest.unified_backtest_manager import UnifiedBacktestManager

        parts = [
            inspect.getsource(V4StrategyAdapter.generate_weights),
            inspect.getsource(BacktestEngine._run_unified_backtest),
            inspect.getsource(UnifiedBacktestManager.run_fast),
        ]
        code = "\n\n".join(parts)
        h = hashlib.md5(code.encode("utf-8")).hexdigest()
        _ALGO_VERSION_CACHE = f"v{h[:8]}"
        return _ALGO_VERSION_CACHE
    except Exception as e:
        logger.warning(f"计算algorithm_version失败，回退vlegacy: {e}")
        _ALGO_VERSION_CACHE = "vlegacy"
        return _ALGO_VERSION_CACHE


# 便捷函数
_storage_instance: Optional[V4DataStorage] = None

def get_v4_storage() -> V4DataStorage:
    """获取V4数据存储单例"""
    global _storage_instance
    if _storage_instance is None:
        _storage_instance = V4DataStorage()
    return _storage_instance


def save_strategy_code(strategy_id: str, strategy_name: str, 
                       strategy_code: str, config: Dict = None) -> bool:
    """便捷函数：保存策略代码"""
    storage = get_v4_storage()
    record = StrategyCodeRecord(
        strategy_id=strategy_id,
        strategy_name=strategy_name,
        strategy_code=strategy_code,
        config=config or {}
    )
    return storage.save_strategy(record)


def save_backtest_result(backtest_id: str, strategy_id: str,
                         start_date: str, end_date: str,
                         metrics: Dict, **kwargs) -> bool:
    """便捷函数：保存回测结果"""
    storage = get_v4_storage()
    record = BacktestResultRecord(
        backtest_id=backtest_id,
        strategy_id=strategy_id,
        start_date=start_date,
        end_date=end_date,
        total_return=metrics.get("total_return", 0),
        annualized_return=metrics.get("annualized_return", 0),
        max_drawdown=metrics.get("max_drawdown", 0),
        sharpe_ratio=metrics.get("sharpe_ratio", 0),
        win_rate=metrics.get("win_rate", 0),
        total_trades=metrics.get("total_trades", 0),
        metrics=metrics,
        **kwargs
    )
    return storage.save_backtest_result(record)


def save_recommendation(recommendation_id: str, date: str,
                        stocks: List[Dict], market_trend: str = "neutral",
                        position_advice: float = 0.5, **kwargs) -> bool:
    """便捷函数：保存推荐记录"""
    storage = get_v4_storage()
    record = RecommendationRecord(
        recommendation_id=recommendation_id,
        date=date,
        stocks=stocks,
        market_trend=market_trend,
        position_advice=position_advice,
        **kwargs
    )
    return storage.save_recommendation(record)
