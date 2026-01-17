#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Redis缓存模块
============

为TRQuant提供高性能Redis缓存支持。

特点:
    - 自动序列化/反序列化JSON
    - TTL自动过期
    - 连接池管理
    - 优雅降级(Redis不可用时跳过缓存)
"""

import json
import logging
from typing import Any, Optional
from datetime import timedelta
import hashlib

logger = logging.getLogger(__name__)

# 尝试导入redis
try:
    import redis
    from redis import ConnectionPool
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    logger.warning("redis包未安装，Redis缓存将被禁用")


class RedisCache:
    """Redis缓存管理器"""
    
    # 默认TTL配置 (秒)
    DEFAULT_TTL = {
        "market_status": 300,      # 市场状态 5分钟
        "mainlines": 1800,         # 投资主线 30分钟
        "factors": 3600,           # 因子推荐 1小时
        "candidate_pool": 1800,    # 候选池 30分钟
        "health_check": 60,        # 健康检查 1分钟
    }
    
    # 键前缀
    KEY_PREFIX = "trquant:"
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: str = None,
        socket_timeout: float = 2.0
    ):
        self.host = host
        self.port = port
        self.db = db
        self._client = None
        self._pool = None
        self._available = False
        
        if REDIS_AVAILABLE:
            self._connect(host, port, db, password, socket_timeout)
    
    def _connect(self, host, port, db, password, socket_timeout):
        """建立连接"""
        try:
            self._pool = ConnectionPool(
                host=host,
                port=port,
                db=db,
                password=password,
                socket_timeout=socket_timeout,
                decode_responses=True
            )
            self._client = redis.Redis(connection_pool=self._pool)
            self._client.ping()
            self._available = True
            logger.info(f"✅ Redis连接成功: {host}:{port}")
        except Exception as e:
            logger.warning(f"⚠️ Redis连接失败: {e}")
            self._available = False
    
    @property
    def available(self) -> bool:
        """检查Redis是否可用"""
        return self._available
    
    def _make_key(self, category: str, key: str) -> str:
        """生成缓存键"""
        return f"{self.KEY_PREFIX}{category}:{key}"
    
    def _hash_args(self, args: dict) -> str:
        """将参数哈希为键"""
        args_str = json.dumps(args, sort_keys=True, default=str)
        return hashlib.md5(args_str.encode()).hexdigest()[:12]
    
    def get(self, category: str, key: str) -> Optional[Any]:
        """获取缓存"""
        if not self._available:
            return None
        
        try:
            full_key = self._make_key(category, key)
            value = self._client.get(full_key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.warning(f"Redis get失败: {e}")
            return None
    
    def set(
        self, 
        category: str, 
        key: str, 
        value: Any, 
        ttl: int = None
    ) -> bool:
        """设置缓存"""
        if not self._available:
            return False
        
        try:
            full_key = self._make_key(category, key)
            
            # 确定TTL
            if ttl is None:
                ttl = self.DEFAULT_TTL.get(category, 300)
            
            # 序列化并存储
            serialized = json.dumps(value, ensure_ascii=False, default=str)
            self._client.setex(full_key, ttl, serialized)
            return True
        except Exception as e:
            logger.warning(f"Redis set失败: {e}")
            return False
    
    def delete(self, category: str, key: str) -> bool:
        """删除缓存"""
        if not self._available:
            return False
        
        try:
            full_key = self._make_key(category, key)
            self._client.delete(full_key)
            return True
        except Exception as e:
            logger.warning(f"Redis delete失败: {e}")
            return False
    
    def clear_category(self, category: str) -> int:
        """清空某类缓存"""
        if not self._available:
            return 0
        
        try:
            pattern = f"{self.KEY_PREFIX}{category}:*"
            keys = self._client.keys(pattern)
            if keys:
                return self._client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Redis clear失败: {e}")
            return 0
    
    def clear_all(self) -> int:
        """清空所有TRQuant缓存"""
        if not self._available:
            return 0
        
        try:
            pattern = f"{self.KEY_PREFIX}*"
            keys = self._client.keys(pattern)
            if keys:
                return self._client.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Redis clear_all失败: {e}")
            return 0
    
    def stats(self) -> dict:
        """获取缓存统计"""
        if not self._available:
            return {"available": False}
        
        try:
            info = self._client.info()
            
            # 统计各类键数量
            categories = {}
            for cat in self.DEFAULT_TTL.keys():
                pattern = f"{self.KEY_PREFIX}{cat}:*"
                categories[cat] = len(self._client.keys(pattern))
            
            return {
                "available": True,
                "host": self.host,
                "port": self.port,
                "redis_version": info.get("redis_version"),
                "used_memory": info.get("used_memory_human"),
                "connected_clients": info.get("connected_clients"),
                "total_keys": info.get("db0", {}).get("keys", 0) if isinstance(info.get("db0"), dict) else 0,
                "categories": categories
            }
        except Exception as e:
            return {"available": False, "error": str(e)}
    
    def cached(self, category: str, ttl: int = None):
        """缓存装饰器"""
        def decorator(func):
            async def wrapper(*args, **kwargs):
                # 生成缓存键
                cache_key = self._hash_args(kwargs)
                
                # 尝试获取缓存
                cached = self.get(category, cache_key)
                if cached is not None:
                    logger.debug(f"Redis缓存命中: {category}:{cache_key}")
                    return cached
                
                # 执行函数
                result = await func(*args, **kwargs)
                
                # 存储缓存
                if result and isinstance(result, dict) and result.get("success"):
                    self.set(category, cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator


# 全局实例
_redis_cache = None

def get_redis_cache() -> RedisCache:
    """获取Redis缓存实例"""
    global _redis_cache
    if _redis_cache is None:
        _redis_cache = RedisCache()
    return _redis_cache
