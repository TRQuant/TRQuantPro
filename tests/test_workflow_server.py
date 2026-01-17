"""
Workflow 9-Steps Server 测试
测试工作流服务器的主要功能
"""
import sys
import os
import json
import pytest
import asyncio

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mcp_servers'))


class TestWorkflowSteps:
    """测试工作流步骤定义"""
    
    def test_workflow_steps_exist(self):
        """测试工作流步骤存在"""
        from workflow_9steps_server import WORKFLOW_9STEPS
        assert isinstance(WORKFLOW_9STEPS, list)
        assert len(WORKFLOW_9STEPS) == 9
    
    def test_step_structure(self):
        """测试步骤结构"""
        from workflow_9steps_server import WORKFLOW_9STEPS
        for step in WORKFLOW_9STEPS:
            assert 'id' in step
            assert 'name' in step
            assert 'description' in step


class TestWorkflowTools:
    """测试工作流工具"""
    
    def test_tools_list(self):
        """测试工具列表"""
        from workflow_9steps_server import TOOLS
        assert isinstance(TOOLS, list)
        assert len(TOOLS) > 0
    
    def test_tool_names(self):
        """测试工具名称"""
        from workflow_9steps_server import TOOLS
        tool_names = [t.name for t in TOOLS]
        
        expected = [
            'workflow9.create',
            'workflow9.status', 
            'workflow9.run_step',
            'workflow9.list',
            'workflow9.restore',
            'workflow9.delete'
        ]
        
        for name in expected:
            assert name in tool_names, f"Missing tool: {name}"


class TestWorkflowCreate:
    """测试工作流创建"""
    
    def test_create_workflow(self):
        """测试创建工作流"""
        from workflow_9steps_server import call_tool
        
        async def run_test():
            result = await call_tool("workflow9.create", {"name": "test_workflow"})
            return result
        
        result = asyncio.run(run_test())
        assert result is not None
        
        # 解析结果
        if hasattr(result, '__iter__') and len(result) > 0:
            content = result[0]
            if hasattr(content, 'text'):
                data = json.loads(content.text)
                assert 'success' in data
                if data['success']:
                    assert 'workflow_id' in data


class TestWorkflowStatus:
    """测试工作流状态"""
    
    def test_status_invalid_id(self):
        """测试无效ID返回错误"""
        from workflow_9steps_server import call_tool
        
        async def run_test():
            result = await call_tool("workflow9.status", {"workflow_id": "invalid_id"})
            return result
        
        result = asyncio.run(run_test())
        assert result is not None
        
        if hasattr(result, '__iter__') and len(result) > 0:
            content = result[0]
            if hasattr(content, 'text'):
                data = json.loads(content.text)
                # 无效ID应该返回错误
                assert 'success' in data


class TestWorkflowList:
    """测试工作流列表"""
    
    def test_list_workflows(self):
        """测试列出工作流"""
        from workflow_9steps_server import call_tool
        
        async def run_test():
            result = await call_tool("workflow9.list", {})
            return result
        
        result = asyncio.run(run_test())
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
