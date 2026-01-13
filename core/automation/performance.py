# -*- coding: utf-8 -*-
"""
性能优化模块
===========
提供浏览器连接池、请求缓存、并行处理等性能优化功能

功能:
1. BrowserPool - 浏览器连接池
2. RequestCache - 请求缓存
3. ParallelExecutor - 并行执行器

使用方式:
    from core.automation.performance import BrowserPool, RequestCache
    
    # 使用浏览器连接池
    async with BrowserPool(max_size=5) as pool:
        browser = await pool.acquire()
        # 使用浏览器...
        await pool.release(browser)
    
    # 使用请求缓存
    cache = RequestCache(ttl=300)
    cache.set("key", data)
    data = cache.get("key")
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable, TypeVar
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

# 配置日志
logger = logging.getLogger(__name__)

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent

T = TypeVar('T')


@dataclass
class CacheEntry:
    """缓存条目"""
    key: str
    value: Any
    created_at: float
    ttl: int  # 秒
    hits: int = 0
    
    @property
    def is_expired(self) -> bool:
        """检查是否过期"""
        return time.time() - self.created_at > self.ttl


class RequestCache:
    """
    请求缓存
    
    提供简单的内存缓存功能，支持TTL过期
    
    Attributes:
        ttl: 默认TTL（秒）
        max_size: 最大缓存条目数
    """
    
    def __init__(self, ttl: int = 300, max_size: int = 1000):
        """
        初始化缓存
        
        Args:
            ttl: 默认TTL（秒）
            max_size: 最大缓存条目数
        """
        self.ttl = ttl
        self.max_size = max_size
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = asyncio.Lock()
    
    @staticmethod
    def generate_key(*args, **kwargs) -> str:
        """生成缓存键"""
        key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值
        
        Args:
            key: 缓存键
        
        Returns:
            缓存值，如果不存在或已过期则返回None
        """
        entry = self._cache.get(key)
        if entry is None:
            return None
        
        if entry.is_expired:
            del self._cache[key]
            return None
        
        entry.hits += 1
        return entry.value
    
    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """
        设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            ttl: TTL（秒），不指定则使用默认值
        """
        # 检查缓存大小
        if len(self._cache) >= self.max_size:
            self._evict()
        
        self._cache[key] = CacheEntry(
            key=key,
            value=value,
            created_at=time.time(),
            ttl=ttl or self.ttl
        )
    
    def delete(self, key: str) -> bool:
        """
        删除缓存
        
        Args:
            key: 缓存键
        
        Returns:
            是否删除成功
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """清空缓存"""
        self._cache.clear()
    
    def _evict(self) -> None:
        """淘汰过期或最少使用的缓存"""
        # 首先清理过期的
        expired_keys = [k for k, v in self._cache.items() if v.is_expired]
        for key in expired_keys:
            del self._cache[key]
        
        # 如果还是满了，删除hits最少的
        if len(self._cache) >= self.max_size:
            # 按hits排序，删除最少使用的25%
            sorted_entries = sorted(self._cache.items(), key=lambda x: x[1].hits)
            to_remove = len(sorted_entries) // 4 or 1
            for key, _ in sorted_entries[:to_remove]:
                del self._cache[key]
    
    @property
    def stats(self) -> Dict:
        """获取缓存统计"""
        total = len(self._cache)
        expired = sum(1 for v in self._cache.values() if v.is_expired)
        total_hits = sum(v.hits for v in self._cache.values())
        return {
            "total": total,
            "expired": expired,
            "active": total - expired,
            "total_hits": total_hits,
            "max_size": self.max_size
        }


def cached(cache: RequestCache, ttl: int = None):
    """
    缓存装饰器
    
    用于缓存函数调用结果
    
    Args:
        cache: RequestCache实例
        ttl: TTL（秒）
    
    Usage:
        cache = RequestCache()
        
        @cached(cache, ttl=60)
        async def fetch_data(url):
            ...
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            key = RequestCache.generate_key(func.__name__, *args, **kwargs)
            
            # 尝试从缓存获取
            result = cache.get(key)
            if result is not None:
                logger.debug(f"缓存命中: {func.__name__}")
                return result
            
            # 调用原函数
            result = await func(*args, **kwargs)
            
            # 存入缓存
            cache.set(key, result, ttl)
            return result
        
        return wrapper
    return decorator


class BrowserPool:
    """
    浏览器连接池
    
    管理多个浏览器实例，提供连接复用
    
    Attributes:
        max_size: 最大连接数
        headless: 是否无头模式
    """
    
    def __init__(self, max_size: int = 5, headless: bool = True):
        """
        初始化连接池
        
        Args:
            max_size: 最大连接数
            headless: 是否无头模式
        """
        self.max_size = max_size
        self.headless = headless
        self._available: List = []
        self._in_use: List = []
        self._lock = asyncio.Lock()
        self._playwright = None
    
    async def _ensure_playwright(self):
        """确保Playwright已初始化"""
        if self._playwright is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
    
    async def acquire(self):
        """
        获取一个浏览器上下文
        
        Returns:
            浏览器上下文
        """
        async with self._lock:
            await self._ensure_playwright()
            
            # 如果有可用的，直接返回
            if self._available:
                context = self._available.pop()
                self._in_use.append(context)
                logger.debug(f"复用浏览器上下文, 可用: {len(self._available)}, 使用中: {len(self._in_use)}")
                return context
            
            # 如果还没达到上限，创建新的
            if len(self._in_use) < self.max_size:
                browser = await self._playwright.chromium.launch(headless=self.headless)
                context = await browser.new_context()
                self._in_use.append(context)
                logger.info(f"创建新浏览器上下文, 使用中: {len(self._in_use)}")
                return context
            
            # 达到上限，等待
            logger.warning("浏览器连接池已满，等待释放...")
            while not self._available:
                await asyncio.sleep(0.1)
            
            context = self._available.pop()
            self._in_use.append(context)
            return context
    
    async def release(self, context) -> None:
        """
        释放浏览器上下文
        
        Args:
            context: 要释放的上下文
        """
        async with self._lock:
            if context in self._in_use:
                self._in_use.remove(context)
                self._available.append(context)
                logger.debug(f"释放浏览器上下文, 可用: {len(self._available)}, 使用中: {len(self._in_use)}")
    
    async def close(self) -> None:
        """关闭连接池"""
        async with self._lock:
            # 关闭所有上下文
            for context in self._available + self._in_use:
                try:
                    await context.close()
                except:
                    pass
            
            self._available.clear()
            self._in_use.clear()
            
            # 关闭Playwright
            if self._playwright:
                await self._playwright.stop()
                self._playwright = None
            
            logger.info("浏览器连接池已关闭")
    
    @property
    def stats(self) -> Dict:
        """获取连接池统计"""
        return {
            "max_size": self.max_size,
            "available": len(self._available),
            "in_use": len(self._in_use),
            "total": len(self._available) + len(self._in_use)
        }
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class ParallelExecutor:
    """
    并行执行器
    
    支持并行执行多个异步任务
    
    Attributes:
        max_workers: 最大并行数
    """
    
    def __init__(self, max_workers: int = 10):
        """
        初始化执行器
        
        Args:
            max_workers: 最大并行数
        """
        self.max_workers = max_workers
        self._semaphore = asyncio.Semaphore(max_workers)
    
    async def execute(self, tasks: List[Callable], *args) -> List[Any]:
        """
        并行执行任务
        
        Args:
            tasks: 任务列表（协程函数）
            *args: 传递给每个任务的参数
        
        Returns:
            结果列表
        """
        async def run_with_semaphore(task, *task_args):
            async with self._semaphore:
                return await task(*task_args)
        
        results = await asyncio.gather(
            *[run_with_semaphore(task, *args) for task in tasks],
            return_exceptions=True
        )
        
        return results
    
    async def map(self, func: Callable, items: List[Any]) -> List[Any]:
        """
        并行映射执行
        
        Args:
            func: 处理函数（协程）
            items: 要处理的项目列表
        
        Returns:
            结果列表
        """
        async def run_with_semaphore(item):
            async with self._semaphore:
                return await func(item)
        
        results = await asyncio.gather(
            *[run_with_semaphore(item) for item in items],
            return_exceptions=True
        )
        
        return results


class PerformanceMonitor:
    """
    性能监控器
    
    监控和记录执行时间
    """
    
    def __init__(self):
        self._records: List[Dict] = []
    
    def record(self, name: str, duration: float, success: bool = True, **metadata):
        """记录性能数据"""
        self._records.append({
            "name": name,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            **metadata
        })
    
    def context(self, name: str):
        """
        性能监控上下文管理器
        
        Usage:
            with monitor.context("fetch_data") as ctx:
                result = await fetch()
            # 自动记录执行时间
        """
        return _PerformanceContext(self, name)
    
    @property
    def stats(self) -> Dict:
        """获取性能统计"""
        if not self._records:
            return {"total": 0}
        
        durations = [r["duration"] for r in self._records]
        success_count = sum(1 for r in self._records if r["success"])
        
        return {
            "total": len(self._records),
            "success": success_count,
            "failed": len(self._records) - success_count,
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations)
        }
    
    def get_records(self, name: str = None, limit: int = 100) -> List[Dict]:
        """获取性能记录"""
        records = self._records if name is None else [r for r in self._records if r["name"] == name]
        return records[-limit:]


class _PerformanceContext:
    """性能监控上下文"""
    
    def __init__(self, monitor: PerformanceMonitor, name: str):
        self.monitor = monitor
        self.name = name
        self.start_time = None
        self.success = True
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.success = exc_type is None
        self.monitor.record(self.name, duration, self.success)


# 全局实例
_global_cache = RequestCache(ttl=300, max_size=1000)
_global_monitor = PerformanceMonitor()


def get_global_cache() -> RequestCache:
    """获取全局缓存"""
    return _global_cache


def get_global_monitor() -> PerformanceMonitor:
    """获取全局性能监控器"""
    return _global_monitor
