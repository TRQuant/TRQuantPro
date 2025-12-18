"""
TRQuant Core Server 测试
测试核心MCP服务器的主要功能
"""
import sys
import os
import json
import pytest

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mcp_servers'))


class TestCoreServerTools:
    """测试核心服务器工具列表"""
    
    def test_tools_list_exists(self):
        """测试工具列表存在"""
        from trquant_core_server import TOOLS
        assert isinstance(TOOLS, list)
        assert len(TOOLS) > 0
    
    def test_tools_have_required_fields(self):
        """测试工具有必需字段（Tool对象）"""
        from trquant_core_server import TOOLS
        for tool in TOOLS:
            # MCP SDK Tool对象有 name 和 description 属性
            assert hasattr(tool, 'name')
            assert hasattr(tool, 'description')
            assert tool.name is not None
    
    def test_core_tools_count(self):
        """测试核心工具数量"""
        from trquant_core_server import TOOLS
        # 实际有22个工具
        assert len(TOOLS) >= 20


class TestCacheHandler:
    """测试缓存处理器"""
    
    def test_cache_stats(self):
        """测试缓存统计"""
        from trquant_core_server import call_tool
        import asyncio
        
        async def run_test():
            result = await call_tool("cache.stats", {})
            return result
        
        result = asyncio.run(run_test())
        assert result is not None
        # 检查返回格式
        if hasattr(result, '__iter__') and len(result) > 0:
            content = result[0]
            if hasattr(content, 'text'):
                data = json.loads(content.text)
                assert 'success' in data
    
    def test_cache_clear(self):
        """测试缓存清除"""
        from trquant_core_server import call_tool
        import asyncio
        
        async def run_test():
            result = await call_tool("cache.clear", {})
            return result
        
        result = asyncio.run(run_test())
        assert result is not None


class TestToolHandlers:
    """测试工具处理器映射"""
    
    def test_handlers_exist(self):
        """测试处理器映射存在"""
        from trquant_core_server import TOOL_HANDLERS
        assert isinstance(TOOL_HANDLERS, dict)
        assert len(TOOL_HANDLERS) > 0
    
    def test_market_handlers(self):
        """测试市场处理器"""
        from trquant_core_server import TOOL_HANDLERS
        assert 'market.status' in TOOL_HANDLERS
        assert 'market.trend' in TOOL_HANDLERS
    
    def test_data_handlers(self):
        """测试数据处理器"""
        from trquant_core_server import TOOL_HANDLERS
        # 实际名称是 data.health_check
        assert 'data.health_check' in TOOL_HANDLERS
        assert 'data.get_price' in TOOL_HANDLERS


class TestToolNames:
    """验证所有工具名称"""
    
    def test_expected_tools(self):
        """验证预期的工具存在"""
        from trquant_core_server import TOOLS
        tool_names = [t.name for t in TOOLS]
        
        expected = [
            'data.get_price', 'data.get_index_stocks', 'data.health_check',
            'market.status', 'market.trend', 'market.mainlines',
            'factor.recommend', 'factor.calculate', 'factor.list',
            'strategy.generate', 'strategy.list_templates',
            'backtest.run', 'backtest.quick',
            'optimizer.grid_search', 'optimizer.optuna',
        ]
        
        for name in expected:
            assert name in tool_names, f"Missing tool: {name}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
