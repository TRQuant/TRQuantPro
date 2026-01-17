"""系统注册表测试"""
import pytest


class TestSystemRegistry:
    def test_registry_exists(self, system_registry):
        """测试注册表存在"""
        assert system_registry is not None
    
    def test_list_modules(self, system_registry):
        """测试列出模块"""
        modules = system_registry.list_modules()
        assert isinstance(modules, list)
    
    def test_get_status(self, system_registry):
        """测试获取系统状态"""
        status = system_registry.get_current_status()
        assert "modules" in status
        assert "databases" in status
    
    def test_list_changes(self, system_registry):
        """测试列出变更"""
        changes = system_registry.list_changes()
        assert isinstance(changes, list)
