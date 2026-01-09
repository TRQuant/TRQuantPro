# 轩辕剑灵MCP集成问题分析

## 🔍 问题诊断

### 当前状态
1. ✅ xuanyuan工具已添加到TOOL_SERVER_MAP（18个工具）
2. ✅ MCPClient可以调用工具（返回success=True）
3. ❌ 创建模板返回的数据结构不正确（template_id为None）

### 根本原因

**xuanyuan_server.py使用的是官方MCP SDK**，通过`stdio_server`进行通信，需要JSON-RPC over stdio协议。

**MCPClient._call_mcp_server()使用的是简单的subprocess调用**，直接发送JSON到stdin，期望JSON响应。

这两个机制不兼容！

## 📋 解决方案

### 方案A：修改xuanyuan_server使用自定义JSON-RPC（推荐）
参考其他服务器的实现方式（如trquant_core_server），使用简单的JSON-RPC协议。

### 方案B：修改MCPClient支持官方MCP SDK
实现完整的MCP协议支持（复杂，需要大量工作）。

### 方案C：使用workflow9的直接调用方式
参考`_call_workflow9_direct`方法，直接在Python中调用xuanyuan_server的函数。

## 🎯 推荐方案

**方案C（直接调用）** + **方案A（简化协议）**

理由：
1. 性能更好（无需subprocess）
2. 错误处理更容易
3. 与其他服务器保持一致
4. 实现简单

## 📝 下一步行动

1. 检查xuanyuan_server是否有可导入的模块接口
2. 实现类似_call_workflow9_direct的_call_xuanyuan_direct方法
3. 或者修改xuanyuan_server使用简单的JSON-RPC协议

