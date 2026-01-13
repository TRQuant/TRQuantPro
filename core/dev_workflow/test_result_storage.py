#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试结果MongoDB存储管理器
========================

使用MongoDB存储测试结果，支持：
- 增量测试结果记录
- 测试历史查询
- 测试覆盖率统计
- 测试趋势分析
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path
import json
import hashlib

# 配置日志
logger = logging.getLogger(__name__)

# 尝试导入pymongo
try:
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
    from bson import ObjectId
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logger.warning("pymongo未安装，MongoDB存储功能不可用")


@dataclass
class TestResult:
    """测试结果数据类"""
    test_id: str  # 测试唯一标识
    module_name: str  # 模块名称
    test_name: str  # 测试名称
    status: str  # passed/failed/skipped/error
    duration_ms: float  # 执行时间(毫秒)
    message: str = ""  # 结果消息
    error_traceback: str = ""  # 错误堆栈
    test_type: str = "unit"  # unit/integration/e2e
    tags: List[str] = field(default_factory=list)  # 标签
    assertions: int = 0  # 断言数量
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据
    created_at: str = ""  # 创建时间
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


@dataclass
class TestSession:
    """测试会话数据类"""
    session_id: str  # 会话ID
    task_id: str  # 关联的任务ID
    module_name: str  # 模块名称
    total_tests: int = 0  # 总测试数
    passed: int = 0  # 通过数
    failed: int = 0  # 失败数
    skipped: int = 0  # 跳过数
    errors: int = 0  # 错误数
    total_duration_ms: float = 0  # 总执行时间
    coverage_pct: float = 0.0  # 代码覆盖率
    status: str = "running"  # running/completed/failed
    started_at: str = ""  # 开始时间
    completed_at: str = ""  # 完成时间
    results: List[str] = field(default_factory=list)  # 测试结果ID列表
    metadata: Dict[str, Any] = field(default_factory=dict)  # 额外元数据
    
    def __post_init__(self):
        if not self.started_at:
            self.started_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)


class TestResultStorage:
    """
    测试结果MongoDB存储管理器
    
    功能：
    - 存储测试结果到MongoDB
    - 查询测试历史
    - 统计测试覆盖率和趋势
    - 支持文件存储作为备份
    """
    
    # MongoDB配置
    MONGO_URI = "mongodb://localhost:27017"
    DB_NAME = "trquant_dev"
    
    # 集合名称
    RESULTS_COLLECTION = "test_results"
    SESSIONS_COLLECTION = "test_sessions"
    COVERAGE_COLLECTION = "test_coverage"
    
    def __init__(
        self,
        mongo_uri: str = None,
        db_name: str = None,
        use_file_fallback: bool = True
    ):
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
        self.file_storage_dir = Path.home() / ".local/share/trquant/test_results"
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
            # 测试结果索引
            self.db[self.RESULTS_COLLECTION].create_index("test_id", unique=True)
            self.db[self.RESULTS_COLLECTION].create_index("module_name")
            self.db[self.RESULTS_COLLECTION].create_index("status")
            self.db[self.RESULTS_COLLECTION].create_index("created_at")
            self.db[self.RESULTS_COLLECTION].create_index([("module_name", 1), ("created_at", -1)])
            
            # 测试会话索引
            self.db[self.SESSIONS_COLLECTION].create_index("session_id", unique=True)
            self.db[self.SESSIONS_COLLECTION].create_index("task_id")
            self.db[self.SESSIONS_COLLECTION].create_index("module_name")
            self.db[self.SESSIONS_COLLECTION].create_index("started_at")
            
            logger.info("索引创建成功")
        except Exception as e:
            logger.warning(f"索引创建失败: {e}")
    
    def _gen_test_id(self, module_name: str, test_name: str) -> str:
        """生成测试ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        content = f"{module_name}_{test_name}_{timestamp}"
        return f"test_{hashlib.md5(content.encode()).hexdigest()[:12]}"
    
    def _gen_session_id(self, module_name: str, task_id: str) -> str:
        """生成会话ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"session_{module_name}_{timestamp}"
    
    # ==================== 测试结果操作 ====================
    
    def save_test_result(self, result: TestResult) -> Dict[str, Any]:
        """
        保存测试结果
        
        Args:
            result: TestResult对象
            
        Returns:
            Dict: {"success": True, "test_id": "..."}
        """
        try:
            doc = result.to_dict()
            
            if self._connected:
                # 存储到MongoDB
                self.db[self.RESULTS_COLLECTION].replace_one(
                    {"test_id": result.test_id},
                    doc,
                    upsert=True
                )
                logger.info(f"测试结果已存储到MongoDB: {result.test_id}")
            else:
                # 存储到文件
                self._save_to_file("results", result.test_id, doc)
                logger.info(f"测试结果已存储到文件: {result.test_id}")
            
            return {"success": True, "test_id": result.test_id}
            
        except Exception as e:
            logger.error(f"保存测试结果失败: {e}")
            return {"success": False, "error": str(e)}
    
    def record_test(
        self,
        module_name: str,
        test_name: str,
        status: str,
        duration_ms: float = 0,
        message: str = "",
        error_traceback: str = "",
        test_type: str = "unit",
        tags: List[str] = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        快速记录测试结果
        
        Args:
            module_name: 模块名称
            test_name: 测试名称
            status: 状态 (passed/failed/skipped/error)
            duration_ms: 执行时间
            message: 结果消息
            error_traceback: 错误堆栈
            test_type: 测试类型
            tags: 标签列表
            metadata: 额外元数据
            
        Returns:
            Dict: {"success": True, "test_id": "..."}
        """
        test_id = self._gen_test_id(module_name, test_name)
        
        result = TestResult(
            test_id=test_id,
            module_name=module_name,
            test_name=test_name,
            status=status,
            duration_ms=duration_ms,
            message=message,
            error_traceback=error_traceback,
            test_type=test_type,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        return self.save_test_result(result)
    
    def query_test_results(
        self,
        module_name: str = None,
        status: str = None,
        test_type: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        查询测试结果
        
        Args:
            module_name: 模块名称过滤
            status: 状态过滤
            test_type: 测试类型过滤
            start_date: 开始日期 (ISO格式)
            end_date: 结束日期 (ISO格式)
            limit: 返回数量限制
            
        Returns:
            Dict: {"success": True, "results": [...], "total": N}
        """
        try:
            if self._connected:
                # 从MongoDB查询
                query = {}
                if module_name:
                    query["module_name"] = module_name
                if status:
                    query["status"] = status
                if test_type:
                    query["test_type"] = test_type
                if start_date:
                    query["created_at"] = {"$gte": start_date}
                if end_date:
                    if "created_at" in query:
                        query["created_at"]["$lte"] = end_date
                    else:
                        query["created_at"] = {"$lte": end_date}
                
                cursor = self.db[self.RESULTS_COLLECTION].find(
                    query
                ).sort("created_at", -1).limit(limit)
                
                results = []
                for doc in cursor:
                    doc.pop("_id", None)
                    results.append(doc)
                
                total = self.db[self.RESULTS_COLLECTION].count_documents(query)
                
            else:
                # 从文件查询
                results = self._query_from_files("results", module_name, status, limit)
                total = len(results)
            
            return {"success": True, "results": results, "total": total}
            
        except Exception as e:
            logger.error(f"查询测试结果失败: {e}")
            return {"success": False, "error": str(e), "results": [], "total": 0}
    
    def get_test_result(self, test_id: str) -> Dict[str, Any]:
        """获取单个测试结果详情"""
        try:
            if self._connected:
                doc = self.db[self.RESULTS_COLLECTION].find_one({"test_id": test_id})
                if doc:
                    doc.pop("_id", None)
                    return {"success": True, "result": doc}
                return {"success": False, "error": f"测试结果不存在: {test_id}"}
            else:
                result = self._load_from_file("results", test_id)
                if result:
                    return {"success": True, "result": result}
                return {"success": False, "error": f"测试结果不存在: {test_id}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 测试会话操作 ====================
    
    def start_test_session(
        self,
        task_id: str,
        module_name: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        开始测试会话
        
        Args:
            task_id: 关联的任务ID
            module_name: 模块名称
            metadata: 额外元数据
            
        Returns:
            Dict: {"success": True, "session_id": "..."}
        """
        session_id = self._gen_session_id(module_name, task_id)
        
        session = TestSession(
            session_id=session_id,
            task_id=task_id,
            module_name=module_name,
            status="running",
            metadata=metadata or {}
        )
        
        try:
            doc = session.to_dict()
            
            if self._connected:
                self.db[self.SESSIONS_COLLECTION].insert_one(doc)
            else:
                self._save_to_file("sessions", session_id, doc)
            
            logger.info(f"测试会话已开始: {session_id}")
            return {"success": True, "session_id": session_id}
            
        except Exception as e:
            logger.error(f"开始测试会话失败: {e}")
            return {"success": False, "error": str(e)}
    
    def complete_test_session(
        self,
        session_id: str,
        total_tests: int,
        passed: int,
        failed: int,
        skipped: int = 0,
        errors: int = 0,
        total_duration_ms: float = 0,
        coverage_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        完成测试会话
        
        Args:
            session_id: 会话ID
            total_tests: 总测试数
            passed: 通过数
            failed: 失败数
            skipped: 跳过数
            errors: 错误数
            total_duration_ms: 总执行时间
            coverage_pct: 代码覆盖率
            
        Returns:
            Dict: {"success": True, "session": {...}}
        """
        try:
            status = "completed" if failed == 0 and errors == 0 else "failed"
            completed_at = datetime.now().isoformat()
            
            update_data = {
                "status": status,
                "total_tests": total_tests,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "errors": errors,
                "total_duration_ms": total_duration_ms,
                "coverage_pct": coverage_pct,
                "completed_at": completed_at
            }
            
            if self._connected:
                self.db[self.SESSIONS_COLLECTION].update_one(
                    {"session_id": session_id},
                    {"$set": update_data}
                )
                doc = self.db[self.SESSIONS_COLLECTION].find_one({"session_id": session_id})
                doc.pop("_id", None)
            else:
                session = self._load_from_file("sessions", session_id)
                session.update(update_data)
                self._save_to_file("sessions", session_id, session)
                doc = session
            
            logger.info(f"测试会话已完成: {session_id} - {status}")
            return {"success": True, "session": doc}
            
        except Exception as e:
            logger.error(f"完成测试会话失败: {e}")
            return {"success": False, "error": str(e)}
    
    def get_test_session(self, session_id: str) -> Dict[str, Any]:
        """获取测试会话详情"""
        try:
            if self._connected:
                doc = self.db[self.SESSIONS_COLLECTION].find_one({"session_id": session_id})
                if doc:
                    doc.pop("_id", None)
                    return {"success": True, "session": doc}
                return {"success": False, "error": f"会话不存在: {session_id}"}
            else:
                session = self._load_from_file("sessions", session_id)
                if session:
                    return {"success": True, "session": session}
                return {"success": False, "error": f"会话不存在: {session_id}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def query_test_sessions(
        self,
        task_id: str = None,
        module_name: str = None,
        status: str = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """查询测试会话"""
        try:
            if self._connected:
                query = {}
                if task_id:
                    query["task_id"] = task_id
                if module_name:
                    query["module_name"] = module_name
                if status:
                    query["status"] = status
                
                cursor = self.db[self.SESSIONS_COLLECTION].find(
                    query
                ).sort("started_at", -1).limit(limit)
                
                sessions = []
                for doc in cursor:
                    doc.pop("_id", None)
                    sessions.append(doc)
                
                total = self.db[self.SESSIONS_COLLECTION].count_documents(query)
            else:
                sessions = self._query_from_files("sessions", module_name, status, limit)
                total = len(sessions)
            
            return {"success": True, "sessions": sessions, "total": total}
            
        except Exception as e:
            return {"success": False, "error": str(e), "sessions": [], "total": 0}
    
    # ==================== 统计分析 ====================
    
    def get_module_test_stats(self, module_name: str) -> Dict[str, Any]:
        """
        获取模块测试统计
        
        Args:
            module_name: 模块名称
            
        Returns:
            Dict: 统计信息
        """
        try:
            if self._connected:
                pipeline = [
                    {"$match": {"module_name": module_name}},
                    {"$group": {
                        "_id": "$status",
                        "count": {"$sum": 1},
                        "avg_duration": {"$avg": "$duration_ms"}
                    }}
                ]
                
                results = list(self.db[self.RESULTS_COLLECTION].aggregate(pipeline))
                
                stats = {
                    "module_name": module_name,
                    "total": 0,
                    "passed": 0,
                    "failed": 0,
                    "skipped": 0,
                    "errors": 0,
                    "pass_rate": 0.0,
                    "avg_duration_ms": 0.0
                }
                
                total_duration = 0
                for r in results:
                    status = r["_id"]
                    count = r["count"]
                    stats["total"] += count
                    if status == "passed":
                        stats["passed"] = count
                    elif status == "failed":
                        stats["failed"] = count
                    elif status == "skipped":
                        stats["skipped"] = count
                    elif status == "error":
                        stats["errors"] = count
                    total_duration += r.get("avg_duration", 0) * count
                
                if stats["total"] > 0:
                    stats["pass_rate"] = round(stats["passed"] / stats["total"] * 100, 2)
                    stats["avg_duration_ms"] = round(total_duration / stats["total"], 2)
                
                return {"success": True, "stats": stats}
            else:
                # 文件模式简化统计
                results = self._query_from_files("results", module_name, None, 1000)
                stats = {
                    "module_name": module_name,
                    "total": len(results),
                    "passed": len([r for r in results if r.get("status") == "passed"]),
                    "failed": len([r for r in results if r.get("status") == "failed"]),
                    "skipped": len([r for r in results if r.get("status") == "skipped"]),
                    "errors": len([r for r in results if r.get("status") == "error"])
                }
                stats["pass_rate"] = round(stats["passed"] / max(stats["total"], 1) * 100, 2)
                return {"success": True, "stats": stats}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_test_trend(
        self,
        module_name: str = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        获取测试趋势
        
        Args:
            module_name: 模块名称（可选）
            days: 天数
            
        Returns:
            Dict: 趋势数据
        """
        try:
            from datetime import timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            if self._connected:
                query = {"created_at": {"$gte": start_date.isoformat()}}
                if module_name:
                    query["module_name"] = module_name
                
                pipeline = [
                    {"$match": query},
                    {"$addFields": {
                        "date": {"$substr": ["$created_at", 0, 10]}
                    }},
                    {"$group": {
                        "_id": {"date": "$date", "status": "$status"},
                        "count": {"$sum": 1}
                    }},
                    {"$sort": {"_id.date": 1}}
                ]
                
                results = list(self.db[self.RESULTS_COLLECTION].aggregate(pipeline))
                
                # 整理为日期维度
                trend_data = {}
                for r in results:
                    date = r["_id"]["date"]
                    status = r["_id"]["status"]
                    if date not in trend_data:
                        trend_data[date] = {"passed": 0, "failed": 0, "skipped": 0, "error": 0}
                    trend_data[date][status] = r["count"]
                
                # 转换为列表
                trend_list = [
                    {"date": date, **counts}
                    for date, counts in sorted(trend_data.items())
                ]
                
                return {"success": True, "trend": trend_list, "days": days}
            else:
                return {"success": True, "trend": [], "days": days, "note": "文件模式暂不支持趋势分析"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== 文件存储辅助方法 ====================
    
    def _save_to_file(self, category: str, item_id: str, data: Dict):
        """保存到文件"""
        category_dir = self.file_storage_dir / category
        category_dir.mkdir(exist_ok=True)
        
        filepath = category_dir / f"{item_id}.json"
        filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    def _load_from_file(self, category: str, item_id: str) -> Optional[Dict]:
        """从文件加载"""
        filepath = self.file_storage_dir / category / f"{item_id}.json"
        if filepath.exists():
            return json.loads(filepath.read_text(encoding='utf-8'))
        return None
    
    def _query_from_files(
        self,
        category: str,
        module_name: str = None,
        status: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """从文件查询"""
        category_dir = self.file_storage_dir / category
        if not category_dir.exists():
            return []
        
        results = []
        for filepath in sorted(category_dir.glob("*.json"), reverse=True):
            if len(results) >= limit:
                break
            
            try:
                data = json.loads(filepath.read_text(encoding='utf-8'))
                
                # 过滤
                if module_name and data.get("module_name") != module_name:
                    continue
                if status and data.get("status") != status:
                    continue
                
                results.append(data)
            except:
                continue
        
        return results
    
    def close(self):
        """关闭连接"""
        if self.client:
            self.client.close()
            self._connected = False


# ==================== 全局单例 ====================

_test_storage: Optional[TestResultStorage] = None

def get_test_storage() -> TestResultStorage:
    """获取测试结果存储单例"""
    global _test_storage
    if _test_storage is None:
        _test_storage = TestResultStorage()
    return _test_storage


# ==================== 便捷函数 ====================

def record_test_result(
    module_name: str,
    test_name: str,
    status: str,
    duration_ms: float = 0,
    message: str = "",
    **kwargs
) -> Dict[str, Any]:
    """快速记录测试结果"""
    storage = get_test_storage()
    return storage.record_test(
        module_name=module_name,
        test_name=test_name,
        status=status,
        duration_ms=duration_ms,
        message=message,
        **kwargs
    )


def query_tests(
    module_name: str = None,
    status: str = None,
    limit: int = 50
) -> Dict[str, Any]:
    """快速查询测试结果"""
    storage = get_test_storage()
    return storage.query_test_results(
        module_name=module_name,
        status=status,
        limit=limit
    )


def get_module_stats(module_name: str) -> Dict[str, Any]:
    """获取模块测试统计"""
    storage = get_test_storage()
    return storage.get_module_test_stats(module_name)


if __name__ == "__main__":
    # 测试代码
    logging.basicConfig(level=logging.INFO)
    
    storage = TestResultStorage()
    
    # 记录测试结果
    result = storage.record_test(
        module_name="core.dev_workflow",
        test_name="test_storage_connection",
        status="passed",
        duration_ms=150.5,
        message="MongoDB连接测试通过"
    )
    print(f"记录结果: {result}")
    
    # 查询
    results = storage.query_test_results(module_name="core.dev_workflow", limit=10)
    print(f"查询结果: {results}")
    
    # 统计
    stats = storage.get_module_test_stats("core.dev_workflow")
    print(f"统计信息: {stats}")
