"""
功能增强模块
- 缓存预热
- 智能重试
- 超时控制
- 详细性能指标
"""
import asyncio
import time
import logging
from functools import wraps
from typing import Any, Callable, Optional, TypeVar, Dict
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)

# ============== 1. 智能重试机制 ==============

T = TypeVar('T')

def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    智能重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始延迟（秒）
        backoff: 退避倍数
        exceptions: 要捕获的异常类型
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"[RETRY] {func.__name__} 失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}"
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"[RETRY] {func.__name__} 最终失败: {e}")
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"[RETRY] {func.__name__} 失败 (尝试 {attempt + 1}/{max_retries + 1}): {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"[RETRY] {func.__name__} 最终失败: {e}")
            
            raise last_exception
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator


# ============== 2. 超时控制 ==============

def with_timeout(seconds: float):
    """
    超时控制装饰器
    
    Args:
        seconds: 超时时间（秒）
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            try:
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=seconds
                )
            except asyncio.TimeoutError:
                logger.error(f"[TIMEOUT] {func.__name__} 超时 ({seconds}s)")
                raise TimeoutError(f"{func.__name__} 超时 ({seconds}s)")
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return func  # 同步函数不支持此装饰器
    
    return decorator


# ============== 3. 详细性能指标 ==============

@dataclass
class PerformanceMetrics:
    """性能指标收集器"""
    
    call_counts: Dict[str, int] = field(default_factory=dict)
    total_times: Dict[str, float] = field(default_factory=dict)
    min_times: Dict[str, float] = field(default_factory=dict)
    max_times: Dict[str, float] = field(default_factory=dict)
    error_counts: Dict[str, int] = field(default_factory=dict)
    last_called: Dict[str, datetime] = field(default_factory=dict)
    
    def record(self, name: str, duration: float, success: bool = True):
        """记录一次调用"""
        if name not in self.call_counts:
            self.call_counts[name] = 0
            self.total_times[name] = 0
            self.min_times[name] = float('inf')
            self.max_times[name] = 0
            self.error_counts[name] = 0
        
        self.call_counts[name] += 1
        self.total_times[name] += duration
        self.min_times[name] = min(self.min_times[name], duration)
        self.max_times[name] = max(self.max_times[name], duration)
        self.last_called[name] = datetime.now()
        
        if not success:
            self.error_counts[name] += 1
    
    def get_stats(self, name: str = None) -> Dict:
        """获取性能统计"""
        if name:
            if name not in self.call_counts:
                return {"error": f"无记录: {name}"}
            
            avg_time = self.total_times[name] / self.call_counts[name] if self.call_counts[name] > 0 else 0
            return {
                "name": name,
                "calls": self.call_counts[name],
                "avg_ms": round(avg_time, 2),
                "min_ms": round(self.min_times[name], 2),
                "max_ms": round(self.max_times[name], 2),
                "errors": self.error_counts[name],
                "error_rate": f"{self.error_counts[name] / self.call_counts[name] * 100:.1f}%",
                "last_called": self.last_called[name].isoformat() if name in self.last_called else None
            }
        
        # 返回所有统计
        all_stats = []
        for n in sorted(self.call_counts.keys()):
            all_stats.append(self.get_stats(n))
        return {"metrics": all_stats, "total_functions": len(self.call_counts)}
    
    def reset(self):
        """重置所有统计"""
        self.call_counts.clear()
        self.total_times.clear()
        self.min_times.clear()
        self.max_times.clear()
        self.error_counts.clear()
        self.last_called.clear()


# 全局性能指标实例
_global_metrics = PerformanceMetrics()

def get_metrics() -> PerformanceMetrics:
    """获取全局性能指标实例"""
    return _global_metrics


def track_detailed(func: Callable) -> Callable:
    """详细性能跟踪装饰器"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.perf_counter()
        success = True
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            success = False
            raise
        finally:
            duration = (time.perf_counter() - start) * 1000
            _global_metrics.record(func.__name__, duration, success)
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.perf_counter()
        success = True
        try:
            return func(*args, **kwargs)
        except Exception as e:
            success = False
            raise
        finally:
            duration = (time.perf_counter() - start) * 1000
            _global_metrics.record(func.__name__, duration, success)
    
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper


# ============== 4. 缓存预热 ==============

class CacheWarmer:
    """缓存预热器"""
    
    def __init__(self):
        self.warmup_tasks: list = []
        self.warmed_up: bool = False
    
    def register(self, func: Callable, *args, **kwargs):
        """注册预热任务"""
        self.warmup_tasks.append((func, args, kwargs))
    
    async def warmup(self) -> Dict:
        """执行缓存预热"""
        if self.warmed_up:
            return {"status": "already_warmed", "tasks": 0}
        
        results = []
        start = time.perf_counter()
        
        for func, args, kwargs in self.warmup_tasks:
            task_start = time.perf_counter()
            try:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
                success = True
            except Exception as e:
                logger.warning(f"[WARMUP] {func.__name__} 失败: {e}")
                success = False
            
            task_duration = (time.perf_counter() - task_start) * 1000
            results.append({
                "task": func.__name__,
                "success": success,
                "duration_ms": round(task_duration, 2)
            })
        
        total_duration = (time.perf_counter() - start) * 1000
        self.warmed_up = True
        
        return {
            "status": "completed",
            "tasks": len(results),
            "successful": sum(1 for r in results if r["success"]),
            "failed": sum(1 for r in results if not r["success"]),
            "total_duration_ms": round(total_duration, 2),
            "details": results
        }


# 全局缓存预热器
_cache_warmer = CacheWarmer()

def get_warmer() -> CacheWarmer:
    """获取全局缓存预热器"""
    return _cache_warmer
