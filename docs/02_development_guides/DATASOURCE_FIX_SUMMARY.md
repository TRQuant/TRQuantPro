# 数据源检查功能修复总结

## 🎯 问题根源

数据源检查是最简单的功能，但一直无法正常工作，主要原因是：

1. **模块导入错误**: 使用了不存在的 `core.data.data_provider.get_data_provider`
2. **异步事件循环冲突**: MCPClient在已有循环中创建新循环
3. **协程未await**: 适配器中调用异步函数但未正确处理

## ✅ 修复内容

### 1. 修复模块导入错误

**文件**: `mcp_servers/workflow_9steps_server.py`

```python
# ❌ 错误
from core.data.data_provider import get_data_provider
provider = get_data_provider()

# ✅ 正确
from core.data.unified_data_provider_v2 import get_data_provider_v2
provider = get_data_provider_v2()
```

### 2. 修复MCPClient异步事件循环冲突

**文件**: `core/mcp/client.py`

```python
def _call_workflow9_direct(self, tool_name: str, arguments: Dict[str, Any]) -> Dict:
    """直接调用workflow9服务器（避免subprocess问题）"""
    try:
        loop = asyncio.get_running_loop()
        # 如果已有循环，使用线程池执行
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self._run_async_in_thread, _handle_tool, tool_name, arguments)
            result = future.result(timeout=60)
            return result
    except RuntimeError:
        # 没有运行中的循环，创建新循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_handle_tool(tool_name, arguments))
            return result
        finally:
            loop.close()
```

### 3. 修复适配器中的协程处理

**文件**: `mcp_servers/utils/services/workflow_service_v1.py`

```python
def run_step(self, request: WorkflowRequest) -> WorkflowResponse:
    """执行指定步骤"""
    import asyncio
    try:
        from mcp_servers.workflow_9steps_server import _handle_tool
        
        # 检查是否已有事件循环
        try:
            loop = asyncio.get_running_loop()
            # 使用线程池执行
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    lambda: asyncio.run(_handle_tool(...))
                )
                result = future.result(timeout=60)
        except RuntimeError:
            # 没有运行中的循环，直接使用asyncio.run
            result = asyncio.run(_handle_tool(...))
        
        return WorkflowResponse(...)
```

### 4. 修复虚拟环境路径查找

**文件**: `core/mcp/client.py`

```python
def _find_python_path(self) -> str:
    """查找Python解释器路径，优先使用工作区venv"""
    # 1. 检查项目根目录下的 venv（主虚拟环境）
    venv_path = self.project_root / "venv"
    if platform.system() == "Windows":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python3"
    if python_exe.exists():
        return str(python_exe)
    
    # 2. 检查环境变量TRQUANT_ROOT下的venv
    # 3. 检查extension/venv（备用）
    # 4. 回退到sys.executable
```

## 🚀 快速测试方案

### 方案1: 简单验证（推荐）

```bash
cd /home/taotao/dev/QuantTest/TRQuant
venv/bin/python3 scripts/test_datasource_simple.py
```

### 方案2: F5调试模式（前端代码）

1. 在Cursor中打开 `extension` 文件夹
2. 按 `F5` 启动调试
3. 新窗口自动加载最新代码

### 方案3: 直接测试Python

```python
from core.data.unified_data_provider_v2 import get_data_provider_v2
provider = get_data_provider_v2()
health_status = provider.health_check()
print(health_status)
```

## 📋 测试结果

- ✅ 直接调用数据提供者: 成功
- ✅ 工作流步骤执行: 成功
- ✅ 模块导入: 成功
- ✅ 虚拟环境路径: 正确找到 `/home/taotao/dev/QuantTest/TRQuant/venv/bin/python3`

## 📚 相关文档

- [快速测试指南](./QUICK_TEST_GUIDE.md)
- [数据源检查代码路径分析](./DATASOURCE_CHECK_ANALYSIS.md)

---

*修复完成时间: 2025-12-22*



























































































