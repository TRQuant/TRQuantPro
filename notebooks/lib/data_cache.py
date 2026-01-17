"""
数据缓存模块
============

提供数据获取的缓存功能，避免重复API调用，提高性能。

特性：
- 基于 joblib 的内存缓存
- 可配置的缓存有效期
- 支持缓存清理和失效
- 自动检测数据变化

使用方式:
    from notebooks.lib.data_cache import cached_get_price, clear_cache
    
    df = cached_get_price(jq, 'AAPL', '2024-01-01', '2024-12-31')
"""

import os
import hashlib
import logging
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Callable, Optional, Dict
from functools import wraps

logger = logging.getLogger(__name__)

# 尝试导入 joblib
try:
    from joblib import Memory
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False
    logger.warning("joblib 未安装，将使用简化缓存")


class SimpleCache:
    """简化的文件缓存（当 joblib 不可用时）"""
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_path(self, key: str) -> Path:
        """获取缓存文件路径"""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.pkl"
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        # 检查是否过期
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if datetime.now() - mtime > self.ttl:
            cache_path.unlink()
            return None
        
        try:
            import warnings
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=DeprecationWarning,
                                        module='pandas.compat.pickle_compat')
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.warning(f"缓存读取失败: {e}")
            return None
    
    def set(self, key: str, value: Any):
        """设置缓存"""
        cache_path = self._get_cache_path(key)
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(value, f)
        except Exception as e:
            logger.warning(f"缓存写入失败: {e}")
    
    def clear(self):
        """清除所有缓存"""
        for f in self.cache_dir.glob("*.pkl"):
            f.unlink()
        logger.info("缓存已清除")


class DataCache:
    """
    数据缓存管理器
    
    支持两种模式：
    1. joblib Memory 缓存（推荐）
    2. 简化的文件缓存（备用）
    """
    
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        ttl_hours: int = 24,
        enabled: bool = True
    ):
        """
        初始化数据缓存
        
        Args:
            cache_dir: 缓存目录
            ttl_hours: 缓存有效期（小时）
            enabled: 是否启用缓存
        """
        self.enabled = enabled
        self.ttl_hours = ttl_hours
        
        # 设置缓存目录
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            from .research_init import get_project_root
            self.cache_dir = get_project_root() / 'notebooks' / 'research' / '.cache'
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化缓存后端
        if HAS_JOBLIB:
            self.memory = Memory(str(self.cache_dir), verbose=0)
            self._simple_cache = None
            logger.info(f"✅ 使用 joblib 缓存: {self.cache_dir}")
        else:
            self.memory = None
            self._simple_cache = SimpleCache(self.cache_dir, ttl_hours)
            logger.info(f"✅ 使用简化缓存: {self.cache_dir}")
        
        # 统计信息
        self.stats = {"hits": 0, "misses": 0}
    
    def cached(self, func: Callable) -> Callable:
        """
        缓存装饰器
        
        Args:
            func: 要缓存的函数
            
        Returns:
            带缓存的函数
        """
        if not self.enabled:
            return func
        
        if self.memory:
            # 使用 joblib
            return self.memory.cache(func)
        else:
            # 使用简化缓存
            @wraps(func)
            def wrapper(*args, **kwargs):
                # 生成缓存键
                key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
                
                # 尝试从缓存获取
                result = self._simple_cache.get(key)
                if result is not None:
                    self.stats["hits"] += 1
                    return result
                
                # 执行函数并缓存结果
                self.stats["misses"] += 1
                result = func(*args, **kwargs)
                self._simple_cache.set(key, result)
                return result
            
            return wrapper
    
    def clear(self):
        """清除所有缓存"""
        if self.memory:
            self.memory.clear()
        if self._simple_cache:
            self._simple_cache.clear()
        self.stats = {"hits": 0, "misses": 0}
        logger.info("✅ 缓存已清除")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total if total > 0 else 0
        
        # 计算缓存大小
        cache_size = sum(f.stat().st_size for f in self.cache_dir.rglob("*") if f.is_file())
        
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": hit_rate,
            "cache_size_mb": cache_size / (1024 * 1024),
            "cache_dir": str(self.cache_dir),
            "enabled": self.enabled,
        }
    
    def print_stats(self):
        """打印缓存统计"""
        stats = self.get_stats()
        print("=" * 50)
        print("数据缓存统计")
        print("=" * 50)
        print(f"缓存命中: {stats['hits']}")
        print(f"缓存未命中: {stats['misses']}")
        print(f"命中率: {stats['hit_rate']:.1%}")
        print(f"缓存大小: {stats['cache_size_mb']:.2f} MB")
        print(f"缓存目录: {stats['cache_dir']}")
        print("=" * 50)


# 全局缓存实例
_global_cache: Optional[DataCache] = None


def get_data_cache() -> DataCache:
    """获取全局数据缓存实例"""
    global _global_cache
    if _global_cache is None:
        _global_cache = DataCache()
    return _global_cache


def clear_cache():
    """清除全局缓存"""
    cache = get_data_cache()
    cache.clear()


# ==========================================
# 便捷缓存函数
# ==========================================

def cached_get_price(
    jq_client,
    security: str,
    start_date: str,
    end_date: str,
    frequency: str = "daily",
    fields: list = None,
    use_cache: bool = True
):
    """
    带缓存的价格数据获取
    
    Args:
        jq_client: JQData 客户端
        security: 证券代码
        start_date: 开始日期
        end_date: 结束日期
        frequency: 频率
        fields: 字段列表
        use_cache: 是否使用缓存
        
    Returns:
        价格数据 DataFrame
    """
    cache = get_data_cache()
    
    if not use_cache or not cache.enabled:
        return jq_client.get_price(
            security, start_date=start_date, end_date=end_date,
            frequency=frequency, fields=fields
        )
    
    # 生成缓存键
    cache_key = f"price_{security}_{start_date}_{end_date}_{frequency}_{fields}"
    
    if cache._simple_cache:
        # 使用简化缓存
        result = cache._simple_cache.get(cache_key)
        if result is not None:
            cache.stats["hits"] += 1
            logger.debug(f"缓存命中: {cache_key}")
            return result
        
        cache.stats["misses"] += 1
        result = jq_client.get_price(
            security, start_date=start_date, end_date=end_date,
            frequency=frequency, fields=fields
        )
        cache._simple_cache.set(cache_key, result)
        return result
    else:
        # 使用 joblib 缓存
        @cache.memory.cache
        def _get_price(sec, start, end, freq, flds):
            return jq_client.get_price(sec, start_date=start, end_date=end,
                                       frequency=freq, fields=flds)
        return _get_price(security, start_date, end_date, frequency, fields)


def cached_get_fundamentals(
    jq_client,
    query,
    date: str = None,
    use_cache: bool = True
):
    """
    带缓存的基本面数据获取
    
    Args:
        jq_client: JQData 客户端
        query: 查询对象
        date: 日期
        use_cache: 是否使用缓存
        
    Returns:
        基本面数据 DataFrame
    """
    cache = get_data_cache()
    
    if not use_cache or not cache.enabled:
        return jq_client.get_fundamentals(query, date=date)
    
    # 生成缓存键
    cache_key = f"fundamentals_{str(query)}_{date}"
    
    if cache._simple_cache:
        result = cache._simple_cache.get(cache_key)
        if result is not None:
            cache.stats["hits"] += 1
            return result
        
        cache.stats["misses"] += 1
        result = jq_client.get_fundamentals(query, date=date)
        cache._simple_cache.set(cache_key, result)
        return result
    else:
        @cache.memory.cache
        def _get_fundamentals(q, d):
            return jq_client.get_fundamentals(q, date=d)
        return _get_fundamentals(query, date)


if __name__ == '__main__':
    # 测试
    cache = DataCache()
    
    @cache.cached
    def expensive_operation(x):
        import time
        time.sleep(0.5)  # 模拟耗时操作
        return x * 2
    
    print("第一次调用（未缓存）:")
    result1 = expensive_operation(10)
    print(f"结果: {result1}")
    
    print("\n第二次调用（缓存）:")
    result2 = expensive_operation(10)
    print(f"结果: {result2}")
    
    cache.print_stats()

