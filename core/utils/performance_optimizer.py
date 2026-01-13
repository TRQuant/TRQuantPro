# -*- coding: utf-8 -*-
"""
性能优化工具
============

提供缓存、批量处理、异步等性能优化功能

作者: TRQuant Team
版本: V1.0
日期: 2026-01-12
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from functools import lru_cache, wraps
from datetime import datetime, timedelta
import time
import threading
from collections import OrderedDict
import numpy as np

logger = logging.getLogger(__name__)


class LRUCache:
    """
    LRU缓存实现
    
    用于缓存计算结果，提高性能
    """
    
    def __init__(self, max_size: int = 100):
        """
        初始化缓存
        
        Args:
            max_size: 最大缓存大小
        """
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值"""
        with self.lock:
            if key in self.cache:
                # 移动到末尾（最近使用）
                self.cache.move_to_end(key)
                return self.cache[key]
            return None
    
    def set(self, key: str, value: Any):
        """设置缓存值"""
        with self.lock:
            if key in self.cache:
                # 更新现有值
                self.cache.move_to_end(key)
                self.cache[key] = value
            else:
                # 添加新值
                if len(self.cache) >= self.max_size:
                    # 删除最旧的（最前面的）
                    self.cache.popitem(last=False)
                self.cache[key] = value
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
    
    def size(self) -> int:
        """获取缓存大小"""
        return len(self.cache)


class BatchProcessor:
    """
    批量处理器
    
    批量处理数据，减少API调用次数
    """
    
    def __init__(self, batch_size: int = 100):
        """
        初始化批量处理器
        
        Args:
            batch_size: 批次大小
        """
        self.batch_size = batch_size
    
    def process_batch(
        self,
        items: List[Any],
        process_func: Callable,
        **kwargs
    ) -> List[Any]:
        """
        批量处理
        
        Args:
            items: 待处理项列表
            process_func: 处理函数
            **kwargs: 传递给处理函数的额外参数
        
        Returns:
            处理结果列表
        """
        results = []
        total = len(items)
        
        for i in range(0, total, self.batch_size):
            batch = items[i:i + self.batch_size]
            batch_results = process_func(batch, **kwargs)
            results.extend(batch_results)
            
            if (i + self.batch_size) % (self.batch_size * 10) == 0:
                logger.info(f"批量处理进度: {min(i + self.batch_size, total)}/{total}")
        
        return results


def cached_result(cache: LRUCache, key_func: Optional[Callable] = None):
    """
    缓存装饰器
    
    Args:
        cache: LRU缓存实例
        key_func: 键生成函数（可选）
    
    Example:
        @cached_result(cache, lambda date: f"breadth_{date}")
        def get_breadth_data(date: str):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = f"{func.__name__}_{args}_{kwargs}"
            
            # 检查缓存
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # 执行函数
            result = func(*args, **kwargs)
            
            # 缓存结果
            if result is not None:
                cache.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator


class PerformanceMonitor:
    """
    性能监控器
    
    监控函数执行时间，识别性能瓶颈
    """
    
    def __init__(self):
        """初始化监控器"""
        self.stats: Dict[str, List[float]] = {}
        self.lock = threading.Lock()
    
    def time_function(self, func_name: str):
        """
        函数执行时间装饰器
        
        Args:
            func_name: 函数名称
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    elapsed = time.time() - start_time
                    with self.lock:
                        if func_name not in self.stats:
                            self.stats[func_name] = []
                        self.stats[func_name].append(elapsed)
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """
        获取性能统计
        
        Returns:
            {func_name: {"count": N, "avg": X, "max": Y, "min": Z}}
        """
        result = {}
        with self.lock:
            for func_name, times in self.stats.items():
                if times:
                    result[func_name] = {
                        "count": len(times),
                        "avg": np.mean(times),
                        "max": np.max(times),
                        "min": np.min(times),
                        "total": np.sum(times),
                    }
        return result
    
    def print_stats(self):
        """打印性能统计"""
        stats = self.get_stats()
        print("\n" + "="*60)
        print("性能统计")
        print("="*60)
        print(f"{'函数名':<30} {'调用次数':<10} {'平均耗时':<12} {'最大耗时':<12} {'总耗时':<12}")
        print("-"*60)
        for func_name, data in sorted(stats.items(), key=lambda x: x[1]["total"], reverse=True):
            print(f"{func_name:<30} {data['count']:<10} {data['avg']:<12.3f} {data['max']:<12.3f} {data['total']:<12.3f}")
        print("="*60)
    
    def clear_stats(self):
        """清空统计"""
        with self.lock:
            self.stats.clear()


# ============ 全局实例 ============

# 全局缓存实例
_global_cache = LRUCache(max_size=500)

# 全局性能监控器
_global_monitor = PerformanceMonitor()


def get_global_cache() -> LRUCache:
    """获取全局缓存实例"""
    return _global_cache


def get_global_monitor() -> PerformanceMonitor:
    """获取全局性能监控器"""
    return _global_monitor
