# -*- coding: utf-8 -*-
"""
MCP 服务器性能优化模块
====================
Phase 2 Task 2.2.1: MCP服务器性能优化

提供:
1. 请求缓存机制 (LRU + TTL)
2. 响应速度优化
3. 数据库连接池
4. 异步批处理
5. 性能监控
"""

import time
import json
import hashlib
import asyncio
import functools
import threading
import logging
from typing import Dict, Any, Optional, Callable, List, TypeVar
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


# ==================== LRU + TTL 缓存 ====================

@dataclass
class CacheEntry:
    """缓存条目"""
    value: Any
    created_at: float
    ttl: float
    hits: int = 0
    
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() - self.created_at > self.ttl


class MCPCache:
    """
    MCP 缓存管理器
    
    特性:
    - LRU 淘汰策略
    - TTL 过期控制
    - 线程安全
    - 命中率统计
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: float = 300):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            default_ttl: 默认 TTL（秒）
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        
        # 统计
        self._stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "expirations": 0,
        }
    
    def _generate_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        """生成缓存键"""
        # 移除 trace_id 等非业务参数
        cache_args = {k: v for k, v in args.items() if k not in ('trace_id', 'timestamp')}
        args_str = json.dumps(cache_args, sort_keys=True, ensure_ascii=False)
        return f"{tool_name}:{hashlib.md5(args_str.encode()).hexdigest()[:16]}"
    
    def get(self, tool_name: str, args: Dict[str, Any]) -> Optional[Any]:
        """
        获取缓存
        
        Args:
            tool_name: 工具名称
            args: 参数
            
        Returns:
            缓存值，如果不存在或过期返回 None
        """
        key = self._generate_key(tool_name, args)
        
        with self._lock:
            if key not in self._cache:
                self._stats["misses"] += 1
                return None
            
            entry = self._cache[key]
            
            if entry.is_expired():
                del self._cache[key]
                self._stats["expirations"] += 1
                self._stats["misses"] += 1
                return None
            
            # LRU: 移到末尾
            self._cache.move_to_end(key)
            entry.hits += 1
            self._stats["hits"] += 1
            
            return entry.value
    
    def set(self, tool_name: str, args: Dict[str, Any], value: Any, ttl: float = None):
        """
        设置缓存
        
        Args:
            tool_name: 工具名称
            args: 参数
            value: 缓存值
            ttl: TTL（秒），默认使用 default_ttl
        """
        key = self._generate_key(tool_name, args)
        ttl = ttl or self.default_ttl
        
        with self._lock:
            # 淘汰旧条目
            while len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
                self._stats["evictions"] += 1
            
            self._cache[key] = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl=ttl
            )
    
    def invalidate(self, tool_name: str, args: Dict[str, Any] = None):
        """
        使缓存失效
        
        Args:
            tool_name: 工具名称
            args: 参数，如果为 None 则清除该工具所有缓存
        """
        with self._lock:
            if args:
                key = self._generate_key(tool_name, args)
                if key in self._cache:
                    del self._cache[key]
            else:
                # 清除所有匹配 tool_name 的缓存
                prefix = f"{tool_name}:"
                keys_to_delete = [k for k in self._cache if k.startswith(prefix)]
                for key in keys_to_delete:
                    del self._cache[key]
    
    def clear(self):
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self._lock:
            total = self._stats["hits"] + self._stats["misses"]
            hit_rate = self._stats["hits"] / total if total > 0 else 0
            
            return {
                **self._stats,
                "total_requests": total,
                "hit_rate": round(hit_rate * 100, 2),
                "current_size": len(self._cache),
                "max_size": self.max_size,
            }
    
    def cleanup_expired(self):
        """清理过期缓存"""
        with self._lock:
            expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
            for key in expired_keys:
                del self._cache[key]
                self._stats["expirations"] += 1
            return len(expired_keys)


# 全局缓存实例
_global_cache: Optional[MCPCache] = None


def get_cache(max_size: int = 1000, default_ttl: float = 300) -> MCPCache:
    """获取全局缓存实例"""
    global _global_cache
    if _global_cache is None:
        _global_cache = MCPCache(max_size, default_ttl)
    return _global_cache


# ==================== 缓存装饰器 ====================

def cached(ttl: float = 300, cache_key: Callable = None):
    """
    缓存装饰器
    
    Args:
        ttl: 缓存 TTL（秒）
        cache_key: 自定义缓存键生成函数
    
    使用方式:
        @cached(ttl=60)
        async def my_handler(args: Dict) -> Dict:
            return expensive_computation(args)
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(args: Dict[str, Any]) -> Any:
            cache = get_cache()
            tool_name = func.__name__
            
            # 尝试从缓存获取
            cached_value = cache.get(tool_name, args)
            if cached_value is not None:
                logger.debug(f"缓存命中: {tool_name}")
                if isinstance(cached_value, dict):
                    cached_value["_cached"] = True
                return cached_value
            
            # 执行并缓存
            result = await func(args)
            
            # 只缓存成功的响应
            if isinstance(result, dict) and result.get("success", True):
                cache.set(tool_name, args, result, ttl)
            
            return result
        
        return wrapper
    return decorator


# ==================== 性能监控 ====================

@dataclass
class PerformanceMetric:
    """性能指标"""
    tool_name: str
    start_time: float
    end_time: float = 0
    success: bool = True
    error: str = None
    
    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000


class PerformanceMonitor:
    """
    性能监控器
    
    记录:
    - 调用次数
    - 响应时间
    - 错误率
    - 慢请求
    """
    
    SLOW_THRESHOLD_MS = 500  # 慢请求阈值
    
    def __init__(self, max_history: int = 10000):
        self._metrics: List[PerformanceMetric] = []
        self._max_history = max_history
        self._lock = threading.Lock()
        
        # 按工具统计
        self._tool_stats: Dict[str, Dict[str, Any]] = {}
    
    def start(self, tool_name: str) -> PerformanceMetric:
        """开始记录"""
        return PerformanceMetric(tool_name=tool_name, start_time=time.time())
    
    def end(self, metric: PerformanceMetric, success: bool = True, error: str = None):
        """结束记录"""
        metric.end_time = time.time()
        metric.success = success
        metric.error = error
        
        with self._lock:
            self._metrics.append(metric)
            
            # 限制历史记录大小
            if len(self._metrics) > self._max_history:
                self._metrics = self._metrics[-self._max_history:]
            
            # 更新工具统计
            self._update_tool_stats(metric)
            
            # 慢请求告警
            if metric.duration_ms > self.SLOW_THRESHOLD_MS:
                logger.warning(
                    f"慢请求: {metric.tool_name} 耗时 {metric.duration_ms:.2f}ms"
                )
    
    def _update_tool_stats(self, metric: PerformanceMetric):
        """更新工具统计"""
        if metric.tool_name not in self._tool_stats:
            self._tool_stats[metric.tool_name] = {
                "total_calls": 0,
                "success_calls": 0,
                "error_calls": 0,
                "total_time_ms": 0,
                "max_time_ms": 0,
                "min_time_ms": float('inf'),
                "slow_calls": 0,
            }
        
        stats = self._tool_stats[metric.tool_name]
        stats["total_calls"] += 1
        stats["total_time_ms"] += metric.duration_ms
        stats["max_time_ms"] = max(stats["max_time_ms"], metric.duration_ms)
        stats["min_time_ms"] = min(stats["min_time_ms"], metric.duration_ms)
        
        if metric.success:
            stats["success_calls"] += 1
        else:
            stats["error_calls"] += 1
        
        if metric.duration_ms > self.SLOW_THRESHOLD_MS:
            stats["slow_calls"] += 1
    
    def get_stats(self, tool_name: str = None) -> Dict[str, Any]:
        """获取统计信息"""
        with self._lock:
            if tool_name:
                stats = self._tool_stats.get(tool_name, {})
                if stats:
                    stats["avg_time_ms"] = (
                        stats["total_time_ms"] / stats["total_calls"]
                        if stats["total_calls"] > 0 else 0
                    )
                    stats["success_rate"] = (
                        stats["success_calls"] / stats["total_calls"] * 100
                        if stats["total_calls"] > 0 else 0
                    )
                return stats
            
            # 全局统计
            total_calls = sum(s["total_calls"] for s in self._tool_stats.values())
            total_errors = sum(s["error_calls"] for s in self._tool_stats.values())
            total_time = sum(s["total_time_ms"] for s in self._tool_stats.values())
            total_slow = sum(s["slow_calls"] for s in self._tool_stats.values())
            
            return {
                "total_calls": total_calls,
                "total_errors": total_errors,
                "error_rate": total_errors / total_calls * 100 if total_calls > 0 else 0,
                "avg_time_ms": total_time / total_calls if total_calls > 0 else 0,
                "slow_calls": total_slow,
                "slow_rate": total_slow / total_calls * 100 if total_calls > 0 else 0,
                "tools": list(self._tool_stats.keys()),
            }
    
    def get_slow_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的慢请求"""
        with self._lock:
            slow = [m for m in self._metrics if m.duration_ms > self.SLOW_THRESHOLD_MS]
            slow.sort(key=lambda m: m.duration_ms, reverse=True)
            return [
                {
                    "tool": m.tool_name,
                    "duration_ms": round(m.duration_ms, 2),
                    "success": m.success,
                    "time": datetime.fromtimestamp(m.start_time).isoformat(),
                }
                for m in slow[:limit]
            ]


# 全局监控实例
_global_monitor: Optional[PerformanceMonitor] = None


def get_monitor() -> PerformanceMonitor:
    """获取全局监控实例"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor()
    return _global_monitor


# ==================== 性能监控装饰器 ====================

def monitored(func: Callable):
    """
    性能监控装饰器
    
    使用方式:
        @monitored
        async def my_handler(args: Dict) -> Dict:
            return do_something(args)
    """
    @functools.wraps(func)
    async def wrapper(args: Dict[str, Any]) -> Any:
        monitor = get_monitor()
        metric = monitor.start(func.__name__)
        
        try:
            result = await func(args)
            success = isinstance(result, dict) and result.get("success", True)
            monitor.end(metric, success=success)
            return result
        except Exception as e:
            monitor.end(metric, success=False, error=str(e))
            raise
    
    return wrapper


# ==================== 数据库连接池 ====================

class ConnectionPool:
    """
    数据库连接池
    
    支持:
    - MongoDB
    - SQLite
    - Redis (可选)
    """
    
    _pools: Dict[str, Any] = {}
    _lock = threading.Lock()
    
    @classmethod
    def get_mongo(cls, uri: str = "mongodb://localhost:27017", database: str = "trquant"):
        """获取 MongoDB 连接"""
        key = f"mongo:{uri}/{database}"
        
        with cls._lock:
            if key not in cls._pools:
                try:
                    from pymongo import MongoClient
                    client = MongoClient(uri, serverSelectionTimeoutMS=2000, maxPoolSize=10)
                    # 测试连接
                    client.admin.command('ping')
                    cls._pools[key] = {"client": client, "db": client[database]}
                    logger.info(f"MongoDB 连接池创建: {database}")
                except Exception as e:
                    logger.warning(f"MongoDB 连接失败: {e}")
                    return None
            
            pool = cls._pools.get(key)
            return pool["db"] if pool else None
    
    @classmethod
    def get_sqlite(cls, db_path: str = "data/trquant.db"):
        """获取 SQLite 连接"""
        key = f"sqlite:{db_path}"
        
        with cls._lock:
            if key not in cls._pools:
                try:
                    import sqlite3
                    conn = sqlite3.connect(db_path, check_same_thread=False)
                    conn.row_factory = sqlite3.Row
                    cls._pools[key] = conn
                    logger.info(f"SQLite 连接创建: {db_path}")
                except Exception as e:
                    logger.warning(f"SQLite 连接失败: {e}")
                    return None
            
            return cls._pools[key]
    
    @classmethod
    def close_all(cls):
        """关闭所有连接"""
        with cls._lock:
            for key, pool in cls._pools.items():
                try:
                    if hasattr(pool, 'close'):
                        pool.close()
                except:
                    pass
            cls._pools.clear()


# ==================== 异步批处理 ====================

class BatchProcessor:
    """
    异步批处理器
    
    将多个请求合并处理，减少 IO 开销
    """
    
    def __init__(self, batch_size: int = 10, max_wait: float = 0.1):
        """
        初始化批处理器
        
        Args:
            batch_size: 批大小
            max_wait: 最大等待时间（秒）
        """
        self.batch_size = batch_size
        self.max_wait = max_wait
        self._queue: asyncio.Queue = None
        self._results: Dict[str, asyncio.Future] = {}
        self._lock = asyncio.Lock()
        self._running = False
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    async def _ensure_queue(self):
        """确保队列已创建"""
        if self._queue is None:
            self._queue = asyncio.Queue()
    
    async def submit(self, request_id: str, handler: Callable, args: Dict[str, Any]) -> Any:
        """
        提交请求
        
        Args:
            request_id: 请求 ID
            handler: 处理函数
            args: 参数
            
        Returns:
            处理结果
        """
        await self._ensure_queue()
        
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        
        async with self._lock:
            self._results[request_id] = future
        
        await self._queue.put((request_id, handler, args))
        
        return await future
    
    async def process_batch(self, handler: Callable, items: List[Dict[str, Any]]) -> List[Any]:
        """
        批量处理
        
        Args:
            handler: 处理函数
            items: 参数列表
            
        Returns:
            结果列表
        """
        tasks = [handler(item) for item in items]
        return await asyncio.gather(*tasks, return_exceptions=True)


# ==================== 性能优化上下文 ====================

class PerformanceContext:
    """
    性能优化上下文管理器
    
    提供:
    - 缓存
    - 监控
    - 计时
    """
    
    def __init__(self, tool_name: str, args: Dict[str, Any], use_cache: bool = True):
        self.tool_name = tool_name
        self.args = args
        self.use_cache = use_cache
        self.cache = get_cache() if use_cache else None
        self.monitor = get_monitor()
        self.metric = None
        self.cached_result = None
    
    async def __aenter__(self):
        # 开始监控
        self.metric = self.monitor.start(self.tool_name)
        
        # 检查缓存
        if self.cache:
            self.cached_result = self.cache.get(self.tool_name, self.args)
        
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 结束监控
        self.monitor.end(
            self.metric,
            success=exc_type is None,
            error=str(exc_val) if exc_val else None
        )
        return False
    
    def is_cached(self) -> bool:
        """是否命中缓存"""
        return self.cached_result is not None
    
    def get_cached(self) -> Any:
        """获取缓存结果"""
        return self.cached_result
    
    def set_cache(self, result: Any, ttl: float = None):
        """设置缓存"""
        if self.cache:
            self.cache.set(self.tool_name, self.args, result, ttl)


# ==================== 导出 ====================

__all__ = [
    # 缓存
    "MCPCache",
    "CacheEntry",
    "get_cache",
    "cached",
    # 监控
    "PerformanceMonitor",
    "PerformanceMetric",
    "get_monitor",
    "monitored",
    # 连接池
    "ConnectionPool",
    # 批处理
    "BatchProcessor",
    # 上下文
    "PerformanceContext",
]
