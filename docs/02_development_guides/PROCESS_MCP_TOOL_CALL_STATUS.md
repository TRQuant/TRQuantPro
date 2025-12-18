# process_mcp_tool_call 说明与修复状态

## 什么是 process_mcp_tool_call？

`process_mcp_tool_call` 是TRQuant系统中统一的MCP工具调用处理函数，位于 `mcp_servers/utils/mcp_integration_helper.py`。

### 核心作用

它封装了MCP工具调用的标准化流程，包括：

1. **trace_id追踪** (阶段1.2要求) - 自动提取和设置trace_id
2. **参数验证** (阶段1.1要求) - 根据工具schema自动验证参数
3. **错误处理** (阶段1.3要求) - 统一的错误码体系和错误响应格式
4. **结果包装** - 统一的结果格式，自动添加trace_id

## 当前完成状态

- ✅ 26/26 服务器已导入 process_mcp_tool_call
- ✅ 16/26 服务器已完全集成（使用process_mcp_tool_call）
- ⚠️  10/26 服务器已导入但未使用

## 待修复的10个服务器

1. kb_server.py (3工具, 类格式)
2. factor_server.py (6工具, 标准格式)
3. data_quality_server.py (4工具, 标准格式, 有适配函数)
4. engineering_server.py (8工具, 标准格式, 有适配函数)
5. report_server.py (6工具, 标准格式, 有适配函数)
6. schema_server.py (4工具, 标准格式, 有适配函数)
7. strategy_kb_server.py (8工具, 标准格式, 有适配函数)
8. strategy_template_server.py (6工具, 标准格式, 有适配函数)
9. trading_server.py (5工具, 标准格式, 有适配函数)
10. workflow_server.py (7工具, 标准格式, 有适配函数)

## 修复方案

由于每个服务器结构不同，建议：
1. 使用lint.fix_mcp_integration工具逐个修复
2. 或参考data_source_server.py的实现方式手动重构

参考示例（data_source_server.py）：
- 将每个工具的处理逻辑包装在handler函数中
- 调用process_mcp_tool_call
- 使用_adapt_mcp_result_to_text_content转换结果
