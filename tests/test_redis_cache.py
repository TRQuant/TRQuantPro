"""Redis缓存测试"""
import pytest


class TestRedisCache:
    def test_redis_module_import(self, redis_cache):
        """测试Redis模块导入"""
        assert redis_cache is not None
    
    def test_redis_stats(self, redis_cache):
        """测试Redis统计"""
        if not redis_cache.available:
            pytest.skip("Redis未运行")
        stats = redis_cache.stats()
        assert stats["available"] == True
    
    def test_redis_set_get(self, redis_cache):
        """测试设置和获取"""
        if not redis_cache.available:
            pytest.skip("Redis未运行")
        redis_cache.set("test", "pytest_key", {"value": 123})
        result = redis_cache.get("test", "pytest_key")
        assert result == {"value": 123}
        redis_cache.delete("test", "pytest_key")
