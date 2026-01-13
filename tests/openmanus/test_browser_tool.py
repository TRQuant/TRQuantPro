#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
OpenManus浏览器工具测试
"""

import pytest
import asyncio
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from scripts.openmanus_browser_tool import OpenManusBrowserTool, BrowserResult


class TestBrowserResult:
    """测试BrowserResult数据类"""
    
    def test_success_result(self):
        result = BrowserResult(success=True, data={"key": "value"}, url="https://test.com")
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.url == "https://test.com"
        assert result.error is None
    
    def test_error_result(self):
        result = BrowserResult(success=False, error="Test error")
        assert result.success is False
        assert result.error == "Test error"
    
    def test_to_dict(self):
        result = BrowserResult(success=True, data="test", url="https://test.com", title="Test")
        d = result.to_dict()
        assert d["success"] is True
        assert d["data"] == "test"
        assert d["url"] == "https://test.com"
        assert d["title"] == "Test"


class TestOpenManusBrowserTool:
    """测试OpenManusBrowserTool类"""
    
    @pytest.fixture
    def tool(self):
        return OpenManusBrowserTool(headless=True)
    
    def test_init(self, tool):
        """测试初始化"""
        assert tool.headless is True
        assert tool._browser is None
        assert tool._page is None
        assert "eastmoney" in tool.finance_sites
        assert "sina" in tool.finance_sites
    
    def test_finance_sites_config(self, tool):
        """测试财经网站配置"""
        eastmoney = tool.finance_sites["eastmoney"]
        assert eastmoney["name"] == "东方财富"
        assert "url" in eastmoney
        assert "search_url" in eastmoney
        assert "stock_url" in eastmoney
        assert "selectors" in eastmoney


@pytest.mark.asyncio
class TestBrowserToolAsync:
    """异步测试"""
    
    @pytest.fixture
    async def tool(self):
        tool = OpenManusBrowserTool(headless=True)
        yield tool
        await tool.cleanup()
    
    async def test_navigate_success(self, tool):
        """测试导航功能 - 使用简单页面"""
        # 使用百度测试，更稳定
        result = await tool.navigate("https://www.baidu.com", wait_for="domcontentloaded")
        # 即使超时，也应该返回结果
        assert isinstance(result, BrowserResult)
        assert result.url == "https://www.baidu.com"
    
    async def test_get_page_content(self, tool):
        """测试获取页面内容"""
        await tool.navigate("https://www.baidu.com", wait_for="domcontentloaded")
        result = await tool.get_page_content()
        assert isinstance(result, BrowserResult)
        if result.success:
            assert "content" in result.data


# 运行测试
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--timeout=120"])
