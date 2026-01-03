# MCP服务器修复总结

## 📊 当前进度

### ✅ 已完成并测试通过 (3/10 - 30%)

1. **schema_server.py** - 4个工具 ✅
   - 全部使用process_mcp_tool_call
   - 语法检查通过
   - 所有检查通过

2. **factor_server.py** - 6个工具 ✅
   - 全部使用process_mcp_tool_call
   - 语法检查通过
   - 所有检查通过

3. **kb_server.py** - 3个工具 ✅
   - 全部使用process_mcp_tool_call
   - 语法检查通过
   - 所有检查通过（类格式，不需要适配函数）

### 🚧 进行中 (1/10 - 10%)

4. **report_server.py** - 6个工具
   - report.list: ✅ 已修复
   - report.get: ✅ 已修复
   - report.generate: ⚠️  已修复但可能有缩进问题
   - report.export: ⚠️  已修复但可能有缩进问题
   - report.compare: ⚠️  已修复但可能有缩进问题
   - report.archive: ❌ 结构复杂，需要手动修复（else块位置问题）

**问题**: report.archive的handler函数内，if mode == "dry_run"的else块被放在了handler函数外面，导致语法错误。

### ⏳ 待修复 (6/10 - 60%)

5. **data_quality_server.py** - 4个工具（使用异步辅助函数）
6. **engineering_server.py** - 8个工具
7. **strategy_kb_server.py** - 8个工具
8. **strategy_template_server.py** - 6个工具（有适配函数）
9. **trading_server.py** - 5个工具（使用异步辅助函数）
10. **workflow_server.py** - 7个工具

## 🔧 修复方法

### 标准格式服务器（有适配函数）

参考 `schema_server.py` 和 `factor_server.py`：

```python
if name == "tool_name":
    def handler(args):
        # 原有的处理逻辑，将arguments改为args
        return {"result": ...}
    
    result = process_mcp_tool_call(
        tool_name=name,
        arguments=arguments,
        tools_list=await list_tools(),
        tool_handler_func=handler,
        server_name="server-name",
        version="1.0.0"
    )
    return _adapt_mcp_result_to_text_content(result)
```

### 类格式服务器

参考 `kb_server.py`：

```python
if name == "tool_name":
    def handler(args):
        # 原有的处理逻辑
        return {"result": ...}
    
    result = process_mcp_tool_call(
        tool_name=name,
        arguments=arguments,
        tools_list=MCP_TOOLS,
        tool_handler_func=handler,
        server_name="server-name",
        version="1.0.0"
    )
    return result  # 直接返回Dict，不需要适配函数
```

## 📝 下一步建议

1. **先修复简单的服务器**（strategy_template_server.py等）
2. **然后修复report_server.py的report.archive**
3. **最后修复使用异步辅助函数的服务器**（需要特殊处理）

## ⚠️ 注意事项

- 代码很长时，使用Python脚本直接修改文件，避免search_replace超时
- 修复后立即测试，确保语法正确
- 注意缩进一致性
- 确保handler函数内的所有代码都在handler内
