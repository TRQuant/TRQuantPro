"""
Pytest配置文件
设置项目路径和共享fixtures
"""
import sys
import os

# 添加项目根目录到路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MCP_SERVERS = os.path.join(ROOT, 'mcp_servers')

# 确保路径在最前面
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
if MCP_SERVERS not in sys.path:
    sys.path.insert(0, MCP_SERVERS)

import pytest


@pytest.fixture
def project_root():
    """返回项目根目录"""
    return ROOT


@pytest.fixture
def redis_cache():
    """Redis缓存fixture"""
    # 直接导入模块避免__init__.py的问题
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "redis_cache", 
        os.path.join(MCP_SERVERS, 'utils', 'redis_cache.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_redis_cache()


@pytest.fixture
def system_registry():
    """系统注册表fixture"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "system_registry", 
        os.path.join(MCP_SERVERS, 'utils', 'system_registry.py')
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_registry()
