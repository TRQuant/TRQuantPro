# 9步工作流问题诊断报告

> 创建时间: 2025-12-22  
> 状态: 调研完成，问题定位

---

## 🔍 调研结果

### 1. 网络搜索发现

**FastMCP框架模式**：
- 使用 `asyncio.run()` 自动管理事件循环
- 通过装饰器定义工具
- 标准化MCP协议通信

**标准MCP服务器模式**：
- 使用 `mcp.server.stdio.stdio_server()` 处理stdio通信
- 通过 `asyncio.run(main())` 启动
- 自动处理JSON-RPC协议

### 2. 当前架构测试结果

✅ **事件循环测试通过**：
- `asyncio.run()` 可以正常工作
- 手动管理事件循环也可以工作
- 但有一个DeprecationWarning（在subprocess中）

✅ **模块导入正常**：
- 所有MCP服务器模块都能正确导入
- 工作流适配器正常注册

⚠️ **潜在问题**：
- 在subprocess中，`get_event_loop()` 可能返回None
- 需要显式创建新的事件循环

---

## 🎯 问题定位

### 问题1: 事件循环管理（已确认）

**位置**: `extension/python/bridge.py:262-274`

**当前代码**：
```python
try:
    loop = asyncio.get_event_loop()  # ⚠️ 在subprocess中可能返回None
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

result = loop.run_until_complete(_handle_tool(tool_name, arguments))
```

**问题**：
- `get_event_loop()` 在Python 3.10+中已弃用
- 在subprocess中，可能没有事件循环
- 多个调用可能共享同一个事件循环

**解决方案**：
```python
# 使用asyncio.run()（推荐）
result = asyncio.run(_handle_tool(tool_name, arguments))
```

### 问题2: 错误信息不完整

**位置**: `extension/python/bridge.py:284-293`

**当前代码**：
```python
except Exception as e:
    error_msg = f'Workflow9工具调用失败: {str(e)}'
    return {
        'ok': False, 
        'error': error_msg,
        'traceback': traceback.format_exc(),
        'hint': '请检查：1) workflow_9steps_server 模块是否可用 2) 依赖是否安装完整'
    }
```

**问题**：
- 错误信息可能不够详细
- 没有区分不同类型的错误
- traceback可能包含敏感信息

### 问题3: 超时时间可能不够

**位置**: `extension/src/views/unifiedDashboard.ts:152-160`

**当前代码**：
```typescript
const timeout = setTimeout(() => {
    proc.kill();
    resolve({ 
        ok: false, 
        error: '调用超时(30秒)',
    });
}, 30000);  // 30秒
```

**问题**：
- 数据源检查可能需要更长时间（网络请求）
- 30秒可能不够
- 强制kill可能导致资源泄漏

---

## 💡 解决方案

### 方案1: 改进事件循环管理（立即实施）

**修改 `extension/python/bridge.py`**：

```python
def call_workflow9_tool(tool_name: str, arguments: dict) -> dict:
    """调用9步工作流工具（改进版）"""
    import traceback
    import asyncio
    
    try:
        # 添加路径
        mcp_servers_path = os.path.join(TRQUANT_ROOT, 'mcp_servers')
        if mcp_servers_path not in sys.path:
            sys.path.insert(0, mcp_servers_path)
        if TRQUANT_ROOT not in sys.path:
            sys.path.insert(0, TRQUANT_ROOT)
        
        # 导入
        from workflow_9steps_server import _handle_tool
        
        # ✅ 使用asyncio.run()（Python 3.7+推荐方式）
        # 自动创建和管理事件循环，避免冲突
        result = asyncio.run(_handle_tool(tool_name, arguments))
        
        # 格式化返回
        if isinstance(result, dict):
            if 'success' not in result:
                result['success'] = True
            return {
                'ok': result.get('success', True), 
                'data': result, 
                'error': result.get('error')
            }
        else:
            return {'ok': True, 'data': result}
            
    except Exception as e:
        import traceback
        error_msg = f'Workflow9工具调用失败: {str(e)}'
        logger.error(f'{error_msg}\n{traceback.format_exc()}')
        return {
            'ok': False, 
            'error': error_msg,
            'error_type': type(e).__name__,
            'traceback': traceback.format_exc(),
            'hint': '请检查：1) workflow_9steps_server 模块是否可用 2) 依赖是否安装完整'
        }
```

**优点**：
- ✅ 使用标准 `asyncio.run()`，自动管理事件循环
- ✅ 避免事件循环冲突
- ✅ 代码更简洁
- ✅ 符合Python最佳实践

### 方案2: 增加超时和重试机制

**修改 `extension/src/views/unifiedDashboard.ts`**：

```typescript
private async _callMCP(
    toolName: string, 
    args: Record<string, any> = {},
    timeout: number = 60000  // ✅ 增加到60秒
): Promise<MCPResult> {
    // 根据工具类型设置不同的超时时间
    const toolTimeouts: Record<string, number> = {
        'workflow9.run_step': 120000,  // 2分钟（数据源检查可能需要更长时间）
        'workflow9.run_all': 300000,   // 5分钟（执行所有步骤）
        'data_source.health_check': 60000,  // 1分钟
    };
    
    const actualTimeout = toolTimeouts[toolName] || timeout;
    
    // ... 现有代码 ...
}
```

### 方案3: 改进错误处理

**统一错误格式**：

```python
def format_error_response(error: Exception, context: str = "") -> dict:
    """格式化错误响应"""
    import traceback
    return {
        'ok': False,
        'error': str(error),
        'error_type': type(error).__name__,
        'context': context,
        'traceback': traceback.format_exc() if logger.level <= logging.DEBUG else None,
        'timestamp': datetime.now().isoformat()
    }
```

---

## 📋 实施计划

### 阶段1: 立即修复（高优先级）

1. ✅ **改进事件循环管理**
   - 使用 `asyncio.run()` 替代手动管理
   - 避免DeprecationWarning
   - 提高可靠性

2. ✅ **增加超时时间**
   - 数据源检查：60秒
   - 单步执行：120秒
   - 全部执行：300秒

### 阶段2: 优化改进（中优先级）

3. **改进错误处理**
   - 统一错误格式
   - 增加错误类型
   - 优化错误信息

4. **增加重试机制**
   - 网络错误自动重试
   - 超时重试
   - 指数退避

### 阶段3: 长期优化（低优先级）

5. **性能优化**
   - 缓存结果
   - 并行执行
   - 资源池管理

6. **监控和日志**
   - 详细日志记录
   - 性能监控
   - 错误统计

---

## 🧪 测试验证

### 测试1: 事件循环管理

```bash
cd /home/taotao/dev/QuantTest/TRQuant
./venv/bin/python -c "
import sys
import asyncio
sys.path.insert(0, 'mcp_servers')
from workflow_9steps_server import _handle_tool

# 测试asyncio.run()
result = asyncio.run(_handle_tool('workflow9.get_steps', {}))
print(f'✅ 成功: {result.get(\"success\")}')
"
```

### 测试2: 完整工作流

```bash
# 通过bridge.py测试
cd /home/taotao/dev/QuantTest/TRQuant
echo '{"action": "call_mcp_tool", "params": {"tool_name": "workflow9.run_step", "arguments": {"workflow_id": "test", "step_id": "data_source", "args": {}}}}' | ./venv/bin/python extension/python/bridge.py
```

---

## 📝 总结

### 已确认的问题

1. ✅ 事件循环管理可以改进（使用asyncio.run()）
2. ✅ 超时时间可能需要增加
3. ✅ 错误处理可以更完善

### 推荐方案

**立即实施**：
- 使用 `asyncio.run()` 替代手动事件循环管理
- 增加超时时间到60-120秒

**后续优化**：
- 改进错误处理
- 增加重试机制
- 性能优化

---

*创建时间: 2025-12-22*




























































