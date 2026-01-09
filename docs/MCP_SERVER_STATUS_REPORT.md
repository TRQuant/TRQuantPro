# MCP Server 状态报告

> **生成时间**: 2026-01-09  
> **目的**: 确认所有MCP server可用性，特别是kb-server

---

## 📊 当前状态

### ✅ 已确认可用的服务器

#### 1. **kb-server** ✅
- **状态**: ✅ 可用
- **文件**: `mcp_servers/kb_server.py`
- **工具数量**: 5个
- **工具列表**:
  - `kb.search` - 搜索知识库
  - `kb.get_strategy` - 获取策略详情
  - `kb.get_api` - 获取API文档
  - `kb.best_practices` - 获取最佳实践
  - `kb.add` - 添加知识库条目
- **MCP配置**: ✅ 已注册（`~/.cursor/mcp.json`）

#### 2. **unified-dev** ✅
- **状态**: ✅ 可用
- **文件**: `mcp_servers/unified_dev_server.py`
- **工具数量**: 57个
- **包含知识库工具**: ✅
  - `knowledge.add` - 添加知识库条目
  - `knowledge.search` - 搜索知识库（混合检索）
  - `knowledge.get` - 获取知识详情
  - `knowledge.update` - 更新知识库
  - `knowledge.mark_useful` - 标记有用
  - `knowledge.stats` - 知识库统计
- **MCP配置**: ✅ 已注册

#### 3. **trquant-core** ✅
- **状态**: ✅ 已注册
- **工具数量**: 132个
- **MCP配置**: ✅ 已注册

#### 4. **其他服务器** ✅
- `xuanyuan` - 轩辕剑灵开发助手
- `trquant-workflow` - 9步投资工作流
- `kb-grounding` - KB Grounding服务器
- `quantconnect` - QuantConnect MCP服务器
- `filesystem` - 文件系统操作
- `git` - Git版本控制

---

## 🔍 测试结果

### 测试1: 模块导入测试
```
✅ kb_server模块: 可导入
✅ kb_server.server: 存在（服务器名称: kb-server）
✅ kb_server.TOOLS: 存在（5个工具）
```

### 测试2: 工具调用测试
```
✅ unified_dev_server: 可用
   - knowledge_search: True
   - knowledge_add: True
✅ knowledge_hybrid_search: 可用
   - vector_search: True
✅ knowledge_search_api: 可用
   - search: True
✅ MCPClient: 可用
✅ knowledge_search调用成功: True
   找到 1 条结果
```

---

## ⚠️ 发现的问题

### 问题1: `list_mcp_resources()` 返回空
- **现象**: `list_mcp_resources()` 返回 "No MCP resources found"
- **原因**: 
  - Cursor的MCP资源列表功能可能不支持所有类型的服务器
  - 或者某些服务器没有正确暴露资源接口
- **影响**: ⚠️ 不影响工具调用，只是资源列表为空
- **解决方案**: 使用工具调用方式，而不是资源列表方式

### 问题2: 工具数量统计
- **unified-dev**: 57个工具
- **trquant-core**: 132个工具
- **kb-server**: 5个工具
- **总计**: 可能超过200个工具

**Cursor工具数量限制**:
- Cursor通常没有严格的工具数量限制
- 但过多的工具可能影响性能
- 建议：按需使用，不需要的服务器可以暂时禁用

---

## ✅ 解决方案

### 方案1: 确认kb-server已正确配置（推荐）

kb-server已经在MCP配置中注册，但需要确认Cursor已加载：

1. **检查MCP配置**:
   ```bash
   cat ~/.cursor/mcp.json | grep -A 10 "kb-server"
   ```

2. **重启Cursor**:
   - 完全关闭Cursor
   - 重新打开
   - 检查MCP服务器状态（Cursor设置 → MCP Servers）

3. **测试工具调用**:
   ```
   在Cursor Chat中测试：
   "请调用 kb.search，参数：{'query': '动量策略'}"
   ```

### 方案2: 使用unified-dev的知识库工具（备选）

如果kb-server不可用，可以使用unified-dev的知识库工具：

```
✅ knowledge.search - 混合检索（向量+关键词）
✅ knowledge.add - 添加知识库条目
✅ knowledge.get - 获取知识详情
```

这些工具已经测试可用，功能更强大（支持向量检索）。

### 方案3: 工具数量优化（如果遇到性能问题）

如果工具数量过多导致性能问题：

1. **禁用不需要的服务器**:
   - 在 `~/.cursor/mcp.json` 中注释掉不需要的服务器
   - 只保留必要的服务器

2. **合并服务器**:
   - 将功能相似的服务器合并
   - 例如：kb-server的功能已经包含在unified-dev中

3. **按需加载**:
   - 使用多个配置文件
   - 根据项目需要切换配置

---

## 📋 推荐配置

### 最小配置（核心功能）
```json
{
  "mcpServers": {
    "unified-dev": {
      "command": "/home/taotao/.cursor/worktrees/TRQuant/ope/venv/bin/python",
      "args": ["/home/taotao/.cursor/worktrees/TRQuant/ope/mcp_servers/unified_dev_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/.cursor/worktrees/TRQuant/ope"
      }
    }
  }
}
```

### 完整配置（所有功能）
保持当前配置，包含所有服务器。

---

## 🧪 验证步骤

### 步骤1: 检查MCP配置
```bash
cat ~/.cursor/mcp.json | python3 -m json.tool
```

### 步骤2: 测试kb-server
```python
# 在Python中测试
from mcp_servers.kb_server import server, TOOLS
print(f"工具数量: {len(TOOLS)}")
for tool in TOOLS:
    print(f"  - {tool.name}")
```

### 步骤3: 在Cursor中测试
```
在Cursor Chat中：
"请调用 kb.search，查询'动量策略'"
```

### 步骤4: 检查Cursor日志
- 打开Cursor设置
- 查看MCP服务器状态
- 检查是否有错误日志

---

## 📝 总结

1. **kb-server可用**: ✅ 模块可导入，工具已定义，MCP配置已注册
2. **unified-dev可用**: ✅ 包含更强大的知识库工具（混合检索）
3. **工具调用成功**: ✅ knowledge_search测试成功
4. **资源列表为空**: ⚠️ 不影响使用，只是资源列表功能不支持

**建议**:
- 优先使用 `unified-dev` 的 `knowledge.*` 工具（功能更强大）
- 如果需要kb-server的特定功能，确保Cursor已重启并加载配置
- 如果遇到性能问题，可以禁用不需要的服务器

---

*生成时间: 2026-01-09*
