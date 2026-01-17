"""
增强功能模块测试
"""
import sys
import os
import pytest
import asyncio
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mcp_servers'))


class TestEnhancementModule:
    """测试增强功能模块"""
    
    def test_retry_decorator(self):
        """测试重试装饰器"""
        from utils.enhancements import retry_on_failure
        
        call_count = 0
        
        @retry_on_failure(max_retries=2, delay=0.1)
        def failing_func():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("模拟失败")
            return "success"
        
        result = failing_func()
        assert result == "success"
        assert call_count == 3
    
    def test_performance_metrics(self):
        """测试性能指标收集"""
        from utils.enhancements import PerformanceMetrics
        
        metrics = PerformanceMetrics()
        metrics.record("test_func", 100, True)
        metrics.record("test_func", 200, True)
        metrics.record("test_func", 150, False)
        
        stats = metrics.get_stats("test_func")
        assert stats["calls"] == 3
        assert stats["errors"] == 1
        assert stats["min_ms"] == 100
        assert stats["max_ms"] == 200
    
    def test_cache_warmer(self):
        """测试缓存预热器"""
        from utils.enhancements import CacheWarmer
        
        warmer = CacheWarmer()
        results = []
        
        def task1():
            results.append("task1")
        
        def task2():
            results.append("task2")
        
        warmer.register(task1)
        warmer.register(task2)
        
        # 同步预热（简化测试）
        assert len(warmer.warmup_tasks) == 2


class TestEnhancementTools:
    """测试增强功能工具"""
    
    def test_perf_detailed_stats(self):
        """测试详细性能统计工具"""
        from trquant_core_server import call_tool
        
        async def run_test():
            result = await call_tool("perf.detailed_stats", {})
            content = result[0].text if result else "{}"
            data = json.loads(content)
            assert data.get("success") == True
            return data
        
        asyncio.run(run_test())
    
    def test_perf_reset_stats(self):
        """测试重置性能统计工具"""
        from trquant_core_server import call_tool
        
        async def run_test():
            result = await call_tool("perf.reset_stats", {})
            content = result[0].text if result else "{}"
            data = json.loads(content)
            assert data.get("success") == True
            assert "message" in data.get("data", {})
            return data
        
        asyncio.run(run_test())
    
    def test_tools_count(self):
        """测试工具总数"""
        from trquant_core_server import TOOLS
        # 应该有25个工具（22 + 3新增）
        assert len(TOOLS) == 25


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
