# -*- coding: utf-8 -*-
"""
回测任务管理器
==============
T1.7.3 任务实现：
1. 回测队列管理 - 异步任务队列，支持优先级
2. 进度跟踪 - 实时进度回调，状态监控
3. 历史记录查询 - MongoDB/文件存储，支持查询过滤
4. 结果自动归档 - 定期清理，自动压缩归档
"""

import logging
import os
import json
import uuid
import time
import threading
import shutil
from enum import Enum
from queue import PriorityQueue, Empty
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


# ==================== 枚举定义 ====================

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"       # 等待执行
    RUNNING = "running"       # 执行中
    COMPLETED = "completed"   # 已完成
    FAILED = "failed"         # 失败
    CANCELLED = "cancelled"   # 已取消


class TaskPriority(Enum):
    """任务优先级"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


# ==================== 数据类 ====================

@dataclass
class BacktestTask:
    """回测任务"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    strategy_type: str = "momentum"
    strategy_params: Dict[str, Any] = field(default_factory=dict)
    securities: List[str] = field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    
    # 执行信息
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    
    # 进度
    progress: float = 0.0
    progress_message: str = ""
    
    # 结果
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    # 元数据
    tags: List[str] = field(default_factory=list)
    user_id: str = "default"
    
    def __lt__(self, other):
        """用于优先级队列排序"""
        return self.priority.value < other.priority.value
    
    def to_dict(self) -> Dict[str, Any]:
        """转为字典"""
        return {
            "task_id": self.task_id,
            "name": self.name,
            "strategy_type": self.strategy_type,
            "strategy_params": self.strategy_params,
            "securities": self.securities,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "progress": self.progress,
            "progress_message": self.progress_message,
            "result": self.result,
            "error": self.error,
            "tags": self.tags,
            "user_id": self.user_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BacktestTask":
        """从字典创建"""
        task = cls()
        task.task_id = data.get("task_id", task.task_id)
        task.name = data.get("name", "")
        task.strategy_type = data.get("strategy_type", "momentum")
        task.strategy_params = data.get("strategy_params", {})
        task.securities = data.get("securities", [])
        task.start_date = data.get("start_date", "")
        task.end_date = data.get("end_date", "")
        task.priority = TaskPriority(data.get("priority", 2))
        task.status = TaskStatus(data.get("status", "pending"))
        task.created_at = data.get("created_at", task.created_at)
        task.started_at = data.get("started_at")
        task.completed_at = data.get("completed_at")
        task.progress = data.get("progress", 0.0)
        task.progress_message = data.get("progress_message", "")
        task.result = data.get("result")
        task.error = data.get("error")
        task.tags = data.get("tags", [])
        task.user_id = data.get("user_id", "default")
        return task


@dataclass
class TaskHistory:
    """任务历史记录"""
    task_id: str
    name: str
    strategy_type: str
    start_date: str
    end_date: str
    status: str
    created_at: str
    completed_at: str
    duration_seconds: float
    
    # 结果摘要
    total_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    
    # 归档信息
    archived: bool = False
    archive_path: Optional[str] = None


# ==================== 任务管理器 ====================

class BacktestTaskManager:
    """
    回测任务管理器
    
    功能：
    1. 异步任务队列管理
    2. 实时进度跟踪
    3. 历史记录存储与查询
    4. 自动归档
    """
    
    def __init__(
        self,
        max_workers: int = 2,
        storage_dir: str = "output/backtest_tasks",
        archive_dir: str = "output/backtest_archive",
        use_mongodb: bool = True
    ):
        self.max_workers = max_workers
        self.storage_dir = Path(storage_dir)
        self.archive_dir = Path(archive_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # 任务队列
        self._queue: PriorityQueue = PriorityQueue()
        self._tasks: Dict[str, BacktestTask] = {}
        self._lock = threading.Lock()
        
        # 工作线程
        self._workers: List[threading.Thread] = []
        self._running = False
        
        # 进度回调
        self._progress_callbacks: Dict[str, Callable] = {}
        
        # MongoDB
        self._mongo_db = None
        if use_mongodb:
            self._init_mongodb()
        
        # 加载未完成的任务
        self._load_pending_tasks()
    
    def _init_mongodb(self):
        """初始化 MongoDB 连接"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=2000)
            client.admin.command('ping')
            self._mongo_db = client.get_database("trquant")
            logger.info("✅ MongoDB 已连接")
        except Exception as e:
            logger.warning(f"⚠️ MongoDB 连接失败，使用文件存储: {e}")
    
    def _load_pending_tasks(self):
        """加载未完成的任务"""
        tasks_file = self.storage_dir / "pending_tasks.json"
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for task_data in data:
                        task = BacktestTask.from_dict(task_data)
                        if task.status in [TaskStatus.PENDING, TaskStatus.RUNNING]:
                            task.status = TaskStatus.PENDING
                            self._tasks[task.task_id] = task
                            self._queue.put(task)
                logger.info(f"✅ 已加载 {len(self._tasks)} 个未完成任务")
            except Exception as e:
                logger.warning(f"加载任务失败: {e}")
    
    def _save_pending_tasks(self):
        """保存未完成的任务"""
        tasks_file = self.storage_dir / "pending_tasks.json"
        pending = [t.to_dict() for t in self._tasks.values() 
                   if t.status in [TaskStatus.PENDING, TaskStatus.RUNNING]]
        try:
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump(pending, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存任务失败: {e}")
    
    # ==================== 队列管理 ====================
    
    def submit_task(
        self,
        name: str,
        strategy_type: str,
        securities: List[str],
        start_date: str,
        end_date: str,
        strategy_params: Dict[str, Any] = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        tags: List[str] = None,
        user_id: str = "default"
    ) -> str:
        """
        提交回测任务
        
        Returns:
            task_id: 任务ID
        """
        task = BacktestTask(
            name=name,
            strategy_type=strategy_type,
            strategy_params=strategy_params or {},
            securities=securities,
            start_date=start_date,
            end_date=end_date,
            priority=priority,
            tags=tags or [],
            user_id=user_id
        )
        
        with self._lock:
            self._tasks[task.task_id] = task
            self._queue.put(task)
            self._save_pending_tasks()
        
        logger.info(f"✅ 任务已提交: {task.task_id} - {name}")
        return task.task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        with self._lock:
            if task_id in self._tasks:
                task = self._tasks[task_id]
                if task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.CANCELLED
                    self._save_pending_tasks()
                    logger.info(f"✅ 任务已取消: {task_id}")
                    return True
                elif task.status == TaskStatus.RUNNING:
                    logger.warning(f"⚠️ 任务正在执行中，无法取消: {task_id}")
                    return False
        return False
    
    def get_task(self, task_id: str) -> Optional[BacktestTask]:
        """获取任务信息"""
        return self._tasks.get(task_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """获取队列状态"""
        with self._lock:
            pending = sum(1 for t in self._tasks.values() if t.status == TaskStatus.PENDING)
            running = sum(1 for t in self._tasks.values() if t.status == TaskStatus.RUNNING)
            completed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.COMPLETED)
            failed = sum(1 for t in self._tasks.values() if t.status == TaskStatus.FAILED)
            
            return {
                "queue_size": self._queue.qsize(),
                "pending": pending,
                "running": running,
                "completed": completed,
                "failed": failed,
                "total": len(self._tasks),
                "workers": len(self._workers),
                "is_running": self._running,
            }
    
    def list_tasks(
        self,
        status: TaskStatus = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[BacktestTask]:
        """列出任务"""
        tasks = list(self._tasks.values())
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        # 按创建时间倒序
        tasks.sort(key=lambda t: t.created_at, reverse=True)
        
        return tasks[offset:offset + limit]
    
    # ==================== 进度跟踪 ====================
    
    def register_progress_callback(self, task_id: str, callback: Callable[[float, str], None]):
        """注册进度回调"""
        self._progress_callbacks[task_id] = callback
    
    def unregister_progress_callback(self, task_id: str):
        """注销进度回调"""
        if task_id in self._progress_callbacks:
            del self._progress_callbacks[task_id]
    
    def _update_progress(self, task_id: str, progress: float, message: str):
        """更新进度"""
        if task_id in self._tasks:
            task = self._tasks[task_id]
            task.progress = progress
            task.progress_message = message
            
            # 触发回调
            if task_id in self._progress_callbacks:
                try:
                    self._progress_callbacks[task_id](progress, message)
                except Exception as e:
                    logger.warning(f"进度回调异常: {e}")
    
    # ==================== 工作线程 ====================
    
    def start(self):
        """启动任务管理器"""
        if self._running:
            logger.warning("任务管理器已在运行")
            return
        
        self._running = True
        
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker_loop, name=f"BacktestWorker-{i}")
            worker.daemon = True
            worker.start()
            self._workers.append(worker)
        
        logger.info(f"✅ 任务管理器已启动，{self.max_workers} 个工作线程")
    
    def stop(self):
        """停止任务管理器"""
        self._running = False
        self._save_pending_tasks()
        logger.info("✅ 任务管理器已停止")
    
    def _worker_loop(self):
        """工作线程主循环"""
        while self._running:
            try:
                task = self._queue.get(timeout=1.0)
                
                if task.status == TaskStatus.CANCELLED:
                    continue
                
                self._execute_task(task)
                
            except Empty:
                continue
            except Exception as e:
                logger.error(f"工作线程异常: {e}")
    
    def _execute_task(self, task: BacktestTask):
        """执行任务"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        
        logger.info(f"🚀 开始执行任务: {task.task_id} - {task.name}")
        
        try:
            # 创建进度回调
            def progress_callback(progress: float, message: str):
                self._update_progress(task.task_id, progress, message)
            
            # 执行回测
            result = self._run_backtest(task, progress_callback)
            
            # 更新任务状态
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.progress = 1.0
            task.progress_message = "完成"
            task.result = result
            
            logger.info(f"✅ 任务完成: {task.task_id}")
            
            # 保存历史记录
            self._save_history(task)
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now().isoformat()
            task.error = str(e)
            logger.error(f"❌ 任务失败: {task.task_id} - {e}")
        
        finally:
            self._save_pending_tasks()
    
    def _run_backtest(self, task: BacktestTask, progress_callback: Callable) -> Dict[str, Any]:
        """运行回测"""
        from core.backtest.unified_backtest_manager import UnifiedBacktestManager, UnifiedBacktestConfig, BacktestLevel
        
        # 创建配置
        config = UnifiedBacktestConfig(
            start_date=task.start_date,
            end_date=task.end_date,
            securities=task.securities,
            use_mock=True,
        )
        
        manager = UnifiedBacktestManager(config)
        manager.set_progress_callback(progress_callback)
        
        # 运行回测
        results = manager.run_full_pipeline(
            strategy_type=task.strategy_type,
            strategy_params=task.strategy_params,
            levels=[BacktestLevel.FAST]
        )
        
        # 提取结果
        fast_result = results.get("fast")
        if fast_result:
            return fast_result.to_dict()
        
        return {"error": "回测无结果"}
    
    # ==================== 历史记录 ====================
    
    def _save_history(self, task: BacktestTask):
        """保存历史记录"""
        # 计算耗时
        duration = 0.0
        if task.started_at and task.completed_at:
            start = datetime.fromisoformat(task.started_at)
            end = datetime.fromisoformat(task.completed_at)
            duration = (end - start).total_seconds()
        
        history = TaskHistory(
            task_id=task.task_id,
            name=task.name,
            strategy_type=task.strategy_type,
            start_date=task.start_date,
            end_date=task.end_date,
            status=task.status.value,
            created_at=task.created_at,
            completed_at=task.completed_at or "",
            duration_seconds=duration,
            total_return=task.result.get("total_return", 0) if task.result else 0,
            sharpe_ratio=task.result.get("sharpe_ratio", 0) if task.result else 0,
            max_drawdown=task.result.get("max_drawdown", 0) if task.result else 0,
        )
        
        # 保存到 MongoDB
        if self._mongo_db is not None:
            try:
                self._mongo_db.backtest_history.insert_one({
                    **asdict(history),
                    "task_data": task.to_dict(),
                })
            except Exception as e:
                logger.warning(f"保存历史记录到 MongoDB 失败: {e}")
        
        # 保存到文件
        history_dir = self.storage_dir / "history"
        history_dir.mkdir(exist_ok=True)
        
        history_file = history_dir / f"{task.task_id}.json"
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(task.to_dict(), f, ensure_ascii=False, indent=2)
    
    def query_history(
        self,
        strategy_type: str = None,
        status: str = None,
        start_date: str = None,
        end_date: str = None,
        min_return: float = None,
        min_sharpe: float = None,
        tags: List[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Dict], int]:
        """
        查询历史记录
        
        Args:
            strategy_type: 策略类型筛选
            status: 状态筛选
            start_date: 创建时间开始
            end_date: 创建时间结束
            min_return: 最小收益率
            min_sharpe: 最小夏普
            tags: 标签筛选
            limit: 返回数量
            offset: 偏移量
            
        Returns:
            (记录列表, 总数)
        """
        # 优先使用 MongoDB
        if self._mongo_db is not None:
            return self._query_history_mongo(
                strategy_type, status, start_date, end_date,
                min_return, min_sharpe, tags, limit, offset
            )
        
        # 文件存储查询
        return self._query_history_file(
            strategy_type, status, start_date, end_date,
            min_return, min_sharpe, tags, limit, offset
        )
    
    def _query_history_mongo(self, strategy_type, status, start_date, end_date,
                              min_return, min_sharpe, tags, limit, offset) -> Tuple[List[Dict], int]:
        """MongoDB 查询"""
        query = {}
        
        if strategy_type:
            query["strategy_type"] = strategy_type
        if status:
            query["status"] = status
        if start_date:
            query["created_at"] = {"$gte": start_date}
        if end_date:
            query.setdefault("created_at", {})["$lte"] = end_date
        if min_return is not None:
            query["total_return"] = {"$gte": min_return}
        if min_sharpe is not None:
            query["sharpe_ratio"] = {"$gte": min_sharpe}
        if tags:
            query["task_data.tags"] = {"$in": tags}
        
        try:
            total = self._mongo_db.backtest_history.count_documents(query)
            cursor = self._mongo_db.backtest_history.find(
                query,
                {"_id": 0}
            ).sort("created_at", -1).skip(offset).limit(limit)
            
            return list(cursor), total
        except Exception as e:
            logger.error(f"MongoDB 查询失败: {e}")
            return [], 0
    
    def _query_history_file(self, strategy_type, status, start_date, end_date,
                             min_return, min_sharpe, tags, limit, offset) -> Tuple[List[Dict], int]:
        """文件存储查询"""
        history_dir = self.storage_dir / "history"
        if not history_dir.exists():
            return [], 0
        
        results = []
        
        for file in history_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 筛选
                if strategy_type and data.get("strategy_type") != strategy_type:
                    continue
                if status and data.get("status") != status:
                    continue
                if start_date and data.get("created_at", "") < start_date:
                    continue
                if end_date and data.get("created_at", "") > end_date:
                    continue
                if min_return is not None:
                    ret = data.get("result", {}).get("total_return", 0)
                    if ret < min_return:
                        continue
                if min_sharpe is not None:
                    sharpe = data.get("result", {}).get("sharpe_ratio", 0)
                    if sharpe < min_sharpe:
                        continue
                if tags:
                    if not set(tags) & set(data.get("tags", [])):
                        continue
                
                results.append(data)
                
            except Exception as e:
                logger.warning(f"读取历史文件失败 {file}: {e}")
        
        # 排序
        results.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        total = len(results)
        return results[offset:offset + limit], total
    
    def get_history_stats(self) -> Dict[str, Any]:
        """获取历史统计"""
        if self._mongo_db is not None:
            try:
                total = self._mongo_db.backtest_history.count_documents({})
                completed = self._mongo_db.backtest_history.count_documents({"status": "completed"})
                failed = self._mongo_db.backtest_history.count_documents({"status": "failed"})
                
                # 平均指标
                pipeline = [
                    {"$match": {"status": "completed"}},
                    {"$group": {
                        "_id": None,
                        "avg_return": {"$avg": "$total_return"},
                        "avg_sharpe": {"$avg": "$sharpe_ratio"},
                        "avg_drawdown": {"$avg": "$max_drawdown"},
                        "avg_duration": {"$avg": "$duration_seconds"},
                    }}
                ]
                stats = list(self._mongo_db.backtest_history.aggregate(pipeline))
                
                return {
                    "total": total,
                    "completed": completed,
                    "failed": failed,
                    "success_rate": completed / total if total > 0 else 0,
                    "avg_return": stats[0]["avg_return"] if stats else 0,
                    "avg_sharpe": stats[0]["avg_sharpe"] if stats else 0,
                    "avg_drawdown": stats[0]["avg_drawdown"] if stats else 0,
                    "avg_duration": stats[0]["avg_duration"] if stats else 0,
                }
            except Exception as e:
                logger.error(f"获取统计失败: {e}")
        
        return {"total": 0, "completed": 0, "failed": 0}
    
    # ==================== 自动归档 ====================
    
    def archive_old_tasks(self, days_old: int = 30) -> int:
        """
        归档旧任务
        
        Args:
            days_old: 多少天前的任务
            
        Returns:
            归档数量
        """
        cutoff_date = (datetime.now() - timedelta(days=days_old)).isoformat()
        archived_count = 0
        
        history_dir = self.storage_dir / "history"
        if not history_dir.exists():
            return 0
        
        # 按月份创建归档目录
        for file in history_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data.get("created_at", "") < cutoff_date:
                    # 归档
                    created = datetime.fromisoformat(data["created_at"])
                    archive_month_dir = self.archive_dir / f"{created.year}-{created.month:02d}"
                    archive_month_dir.mkdir(exist_ok=True)
                    
                    # 移动文件
                    shutil.move(str(file), str(archive_month_dir / file.name))
                    archived_count += 1
                    
            except Exception as e:
                logger.warning(f"归档文件失败 {file}: {e}")
        
        if archived_count > 0:
            logger.info(f"✅ 已归档 {archived_count} 个旧任务")
        
        return archived_count
    
    def cleanup_archives(self, months_old: int = 6) -> int:
        """
        清理旧归档（可选压缩）
        
        Args:
            months_old: 多少月前的归档
            
        Returns:
            清理数量
        """
        cutoff = datetime.now() - timedelta(days=months_old * 30)
        cleaned = 0
        
        for month_dir in self.archive_dir.iterdir():
            if month_dir.is_dir():
                try:
                    year, month = map(int, month_dir.name.split('-'))
                    dir_date = datetime(year, month, 1)
                    
                    if dir_date < cutoff:
                        # 压缩归档
                        archive_path = self.archive_dir / f"{month_dir.name}.tar.gz"
                        shutil.make_archive(
                            str(archive_path).replace('.tar.gz', ''),
                            'gztar',
                            month_dir
                        )
                        
                        # 删除原目录
                        shutil.rmtree(month_dir)
                        cleaned += 1
                        
                except Exception as e:
                    logger.warning(f"清理归档失败 {month_dir}: {e}")
        
        if cleaned > 0:
            logger.info(f"✅ 已压缩 {cleaned} 个旧归档")
        
        return cleaned


# ==================== 单例 ====================

_task_manager: Optional[BacktestTaskManager] = None


def get_task_manager() -> BacktestTaskManager:
    """获取任务管理器单例"""
    global _task_manager
    if _task_manager is None:
        _task_manager = BacktestTaskManager()
    return _task_manager


# ==================== 便捷函数 ====================

def submit_backtest(
    name: str,
    strategy_type: str,
    securities: List[str],
    start_date: str,
    end_date: str,
    **kwargs
) -> str:
    """提交回测任务"""
    manager = get_task_manager()
    if not manager._running:
        manager.start()
    return manager.submit_task(name, strategy_type, securities, start_date, end_date, **kwargs)


def get_task_status(task_id: str) -> Optional[Dict]:
    """获取任务状态"""
    manager = get_task_manager()
    task = manager.get_task(task_id)
    return task.to_dict() if task else None


def query_backtest_history(**kwargs) -> Tuple[List[Dict], int]:
    """查询回测历史"""
    manager = get_task_manager()
    return manager.query_history(**kwargs)


__all__ = [
    "BacktestTaskManager",
    "BacktestTask",
    "TaskStatus",
    "TaskPriority",
    "TaskHistory",
    "get_task_manager",
    "submit_backtest",
    "get_task_status",
    "query_backtest_history",
]
