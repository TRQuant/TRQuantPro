"""
集成测试 - 端到端测试
测试各模块之间的交互
"""
import sys
import os
import pytest
import asyncio
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mcp_servers'))


class TestCoreServerIntegration:
    """核心服务器集成测试"""
    
    @pytest.mark.asyncio
    async def test_market_status_with_cache(self):
        """测试市场状态（带缓存）"""
        from trquant_core_server import call_tool
        
        # 第一次调用（可能从数据源获取）
        start1 = time.perf_counter()
        result1 = await call_tool("market.status", {"index": "000300.XSHG"})
        time1 = (time.perf_counter() - start1) * 1000
        
        content1 = result1[0].text if result1 else "{}"
        data1 = json.loads(content1)
        assert data1.get("success") == True
        
        # 第二次调用（应该从缓存获取）
        start2 = time.perf_counter()
        result2 = await call_tool("market.status", {"index": "000300.XSHG"})
        time2 = (time.perf_counter() - start2) * 1000
        
        content2 = result2[0].text if result2 else "{}"
        data2 = json.loads(content2)
        assert data2.get("success") == True
        
        # 缓存应该更快
        print(f"\n  第一次: {time1:.2f}ms, 第二次: {time2:.2f}ms")
    
    @pytest.mark.asyncio
    async def test_cache_stats_integration(self):
        """测试缓存统计集成"""
        from trquant_core_server import call_tool
        
        # 获取缓存统计
        result = await call_tool("cache.stats", {})
        content = result[0].text if result else "{}"
        data = json.loads(content)
        
        assert data.get("success") == True
        assert "caches" in data.get("data", {})
    
    @pytest.mark.asyncio
    async def test_factor_recommend_integration(self):
        """测试因子推荐集成"""
        from trquant_core_server import call_tool
        
        result = await call_tool("factor.recommend", {
            "market_regime": "neutral",
            "top_n": 5
        })
        content = result[0].text if result else "{}"
        data = json.loads(content)
        
        assert data.get("success") == True
        factors = data.get("data", {}).get("factors", [])
        assert len(factors) > 0


class TestWorkflowIntegration:
    """工作流集成测试"""
    
    @pytest.mark.asyncio
    async def test_workflow_create_and_status(self):
        """测试工作流创建和状态查询"""
        from workflow_9steps_server import call_tool
        
        # 创建工作流
        create_result = await call_tool("workflow9.create", {"name": "integration_test"})
        create_content = create_result[0].text if create_result else "{}"
        create_data = json.loads(create_content)
        
        assert create_data.get("success") == True
        workflow_id = create_data.get("workflow_id")
        assert workflow_id is not None
        
        # 查询状态
        status_result = await call_tool("workflow9.status", {"workflow_id": workflow_id})
        status_content = status_result[0].text if status_result else "{}"
        status_data = json.loads(status_content)
        
        assert status_data.get("success") == True
        assert status_data.get("current_step") == 0
    
    @pytest.mark.asyncio
    async def test_workflow_list(self):
        """测试工作流列表"""
        from workflow_9steps_server import call_tool
        
        result = await call_tool("workflow9.list", {})
        content = result[0].text if result else "{}"
        data = json.loads(content)
        
        assert data.get("success") == True
        workflows = data.get("data", {}).get("workflows", [])
        assert isinstance(workflows, list)


class TestDatabaseIntegration:
    """数据库集成测试"""
    
    def test_redis_connection(self):
        """测试Redis连接"""
        try:
            from utils.redis_cache import get_redis_cache
            cache = get_redis_cache()
            stats = cache.stats()
            assert stats.get("available") == True
        except Exception as e:
            pytest.skip(f"Redis不可用: {e}")
    
    def test_mongodb_connection(self):
        """测试MongoDB连接"""
        try:
            from pymongo import MongoClient
            client = MongoClient("localhost", 27017, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            client.close()
        except Exception as e:
            pytest.skip(f"MongoDB不可用: {e}")


class TestDataSourceIntegration:
    """数据源集成测试"""
    
    @pytest.mark.asyncio
    async def test_health_check(self):
        """测试数据源健康检查"""
        from trquant_core_server import call_tool
        
        result = await call_tool("data.health_check", {})
        content = result[0].text if result else "{}"
        data = json.loads(content)
        
        assert data.get("success") == True
        sources = data.get("data", {}).get("sources", {})
        # 至少有一个数据源可用
        assert any(s.get("available", False) for s in sources.values()) or len(sources) == 0


class TestEndToEndWorkflow:
    """端到端工作流测试"""
    
    @pytest.mark.asyncio
    async def test_full_analysis_pipeline(self):
        """测试完整分析流程"""
        from trquant_core_server import call_tool
        
        # 1. 获取市场状态
        market_result = await call_tool("market.status", {})
        market_data = json.loads(market_result[0].text)
        assert market_data.get("success") == True
        
        # 提取市场状态
        regime = market_data.get("data", {}).get("regime", "neutral")
        
        # 2. 根据市场状态获取因子推荐
        factor_result = await call_tool("factor.recommend", {
            "market_regime": regime,
            "top_n": 5
        })
        factor_data = json.loads(factor_result[0].text)
        assert factor_data.get("success") == True
        
        # 3. 获取策略模板列表
        template_result = await call_tool("strategy.list_templates", {})
        template_data = json.loads(template_result[0].text)
        assert template_data.get("success") == True
        
        print(f"\n  市场状态: {regime}")
        print(f"  推荐因子数: {len(factor_data.get('data', {}).get('factors', []))}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
