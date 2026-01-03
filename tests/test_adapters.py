"""
适配器功能测试

测试Tenbagger和Workflow适配器的功能。

Author: TRQuant Team
Date: 2025-12-21
"""

import pytest
import sys
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class TestTenbaggerAdapter:
    """Tenbagger适配器测试"""
    
    def test_adapter_creation(self):
        """测试适配器创建"""
        from mcp_servers.utils.adapters.tenbagger_adapter import get_tenbagger_adapter
        
        adapter = get_tenbagger_adapter()
        assert adapter is not None
        assert hasattr(adapter, 'handle_evaluate')
        assert hasattr(adapter, 'handle_batch')
        assert hasattr(adapter, 'get_available_versions')
    
    def test_version_manager(self):
        """测试版本管理器"""
        from core.mcp.versioning.version_manager import get_version_manager
        
        vm = get_version_manager()
        versions = vm.list_versions()
        assert 'v2' in versions
    
    def test_service_interface(self):
        """测试服务接口"""
        from mcp_servers.utils.services.tenbagger_service_v2 import TenbaggerServiceV2
        from core.mcp.interfaces.tenbagger_interface import TenbaggerRequest
        
        service = TenbaggerServiceV2()
        assert service.get_version() == "v2"
        
        # 测试接口方法存在
        assert hasattr(service, 'evaluate')
        assert hasattr(service, 'batch_evaluate')
        assert hasattr(service, 'get_report')
        assert hasattr(service, 'get_rankings')
        assert hasattr(service, 'generate_report')


class TestWorkflowAdapter:
    """Workflow适配器测试"""
    
    def test_adapter_creation(self):
        """测试适配器创建"""
        from mcp_servers.utils.adapters.workflow_adapter import get_workflow_adapter
        
        adapter = get_workflow_adapter()
        assert adapter is not None
        assert hasattr(adapter, 'handle_get_steps')
        assert hasattr(adapter, 'handle_create')
        assert hasattr(adapter, 'handle_run_step')
        assert hasattr(adapter, 'get_available_versions')
    
    def test_service_interface(self):
        """测试服务接口"""
        from mcp_servers.utils.services.workflow_service_v1 import WorkflowServiceV1
        
        service = WorkflowServiceV1()
        assert service.get_version() == "v1"
        
        # 测试接口方法存在
        assert hasattr(service, 'get_steps')
        assert hasattr(service, 'create_workflow')
        assert hasattr(service, 'get_status')
        assert hasattr(service, 'run_step')
        assert hasattr(service, 'run_all')
        assert hasattr(service, 'get_context')


class TestVersionManager:
    """版本管理器测试"""
    
    def test_version_registration(self):
        """测试版本注册"""
        from core.mcp.versioning.version_manager import get_version_manager
        from mcp_servers.utils.services.tenbagger_service_v2 import TenbaggerServiceV2
        from mcp_servers.utils.services.workflow_service_v1 import WorkflowServiceV1
        
        vm = get_version_manager()
        
        # 注册服务
        vm.register("v2", TenbaggerServiceV2, is_default=True)
        vm.register("v1", WorkflowServiceV1, is_default=False)
        
        # 验证注册
        versions = vm.list_versions()
        assert 'v1' in versions
        assert 'v2' in versions
    
    def test_version_routing(self):
        """测试版本路由"""
        from core.mcp.versioning.version_manager import get_version_manager
        from mcp_servers.utils.services.tenbagger_service_v2 import TenbaggerServiceV2
        
        vm = get_version_manager()
        vm.register("v2", TenbaggerServiceV2, is_default=True)
        
        # 获取服务
        service = vm.get_service("v2")
        assert service is not None
        assert service.get_version() == "v2"
        
        # 测试默认版本
        default_service = vm.get_service()
        assert default_service is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

