# MCP服务器开关指南

> **更新时间**: 2024-12-16  
> **目标**: 明确告知应该打开哪些服务器，关闭哪些服务器

---

## ✅ 应该打开的服务器（6个）

### 1. filesystem（官方服务器）
- **状态**: ✅ **必须打开**
- **功能**: 文件系统操作
- **工具数**: ~15个
- **说明**: Cursor官方提供的文件系统MCP服务器

### 2. trquant-core（新建，核心量化服务器）
- **状态**: ✅ **必须打开**
- **文件**: `mcp_servers/trquant_core_server.py`
- **工具数**: 35个
- **功能**: 
  - `data.*` - 数据源（9个工具）
  - `market.*` - 市场分析（5个工具）
  - `factor.*` - 因子库（3个工具）
  - `strategy.*` - 策略管理（3个工具）
  - `backtest.*` - 回测引擎（3个工具）
  - `optimizer.*` - 参数优化（3个工具）
  - `core.metrics` - 性能监控（1个工具）
- **说明**: **新建服务器**，整合了数据源、市场、因子、策略、回测、优化功能

### 3. trquant-workflow（工作流服务器）
- **状态**: ✅ **必须打开**
- **文件**: `mcp_servers/workflow_9steps_server.py`
- **工具数**: 6个
- **功能**: 9步投资工作流编排
- **说明**: 重命名自 `trquant-workflow9`

### 4. trquant-project（项目规划管理服务器）
- **状态**: ✅ **必须打开**
- **文件**: `mcp_servers/project_manager_server.py`
- **工具数**: 17个
- **功能**: 
  - `task.*` - 任务管理（4个工具）
  - `progress.*` - 进度跟踪（2个工具）
  - `devlog.*` - 开发日志（2个工具）
  - `experience.*` - 经验总结（3个工具）
  - `issue.*` - 问题追踪（3个工具）
  - `milestone.*` - 里程碑管理（2个工具）
  - `risk.*` - 风险评估（2个工具）
- **说明**: 重命名自 `trquant-project-manager`，已整合任务管理功能

### 5. trquant-trading（交易执行服务器）
- **状态**: ✅ **必须打开**
- **文件**: `mcp_servers/trading_server.py`
- **工具数**: 5个
- **功能**: 实盘交易执行（PTrade/QMT）
- **说明**: 保持不变

### 6. trquant-dev（开发工具服务器）
- **状态**: ✅ **必须打开**
- **文件**: `mcp_servers/test_server.py`
- **工具数**: 3个（当前）
- **功能**: 测试运行
- **说明**: 临时使用test_server，后续应整合更多开发工具

---

## ❌ 应该关闭的服务器（旧配置）

### 1. trquant（主扩展服务）
- **状态**: ❌ **应该关闭**
- **文件**: `extension/python/mcp_server.py`
- **原因**: 功能已分散到其他服务器，避免重复

### 2. trquant-workflow9（旧名称）
- **状态**: ❌ **应该关闭**
- **文件**: `mcp_servers/workflow_9steps_server.py`
- **原因**: 已重命名为 `trquant-workflow`，使用新名称

### 3. trquant-project-manager（旧名称）
- **状态**: ❌ **应该关闭**
- **文件**: `mcp_servers/project_manager_server.py`
- **原因**: 已重命名为 `trquant-project`，使用新名称

### 4. trquant-dev-task（任务管理服务器）
- **状态**: ❌ **应该关闭**
- **文件**: `mcp_servers/dev_task_server.py`
- **原因**: 任务管理功能已整合到 `trquant-project`，避免重复

### 5. trquant-dev-unified（统一工具服务器）
- **状态**: ❌ **应该关闭**
- **文件**: `mcp_servers/unified_utils_server.py`
- **原因**: 45个工具全是空壳实现，无实际功能

### 6. trquant-dev-test（测试服务器）
- **状态**: ⚠️ **暂时保留，后续整合**
- **文件**: `mcp_servers/test_server.py`
- **原因**: 当前作为 `trquant-dev` 使用，后续应整合更多开发工具

---

## 📋 最终配置清单

### 正确的 `.cursor/mcp.json` 配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/taotao/dev/QuantTest/TRQuant"]
    },
    "trquant-core": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": ["/home/taotao/dev/QuantTest/TRQuant/mcp_servers/trquant_core_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant",
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant:/home/taotao/dev/QuantTest/TRQuant/mcp_servers"
      }
    },
    "trquant-workflow": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": ["/home/taotao/dev/QuantTest/TRQuant/mcp_servers/workflow_9steps_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant",
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant:/home/taotao/dev/QuantTest/TRQuant/mcp_servers"
      }
    },
    "trquant-project": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": ["/home/taotao/dev/QuantTest/TRQuant/mcp_servers/project_manager_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant",
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant:/home/taotao/dev/QuantTest/TRQuant/mcp_servers"
      }
    },
    "trquant-trading": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": ["/home/taotao/dev/QuantTest/TRQuant/mcp_servers/trading_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant",
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant:/home/taotao/dev/QuantTest/TRQuant/mcp_servers"
      }
    },
    "trquant-dev": {
      "command": "/home/taotao/dev/QuantTest/TRQuant/venv/bin/python",
      "args": ["/home/taotao/dev/QuantTest/TRQuant/mcp_servers/test_server.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "TRQUANT_ROOT": "/home/taotao/dev/QuantTest/TRQuant",
        "PYTHONPATH": "/home/taotao/dev/QuantTest/TRQuant:/home/taotao/dev/QuantTest/TRQuant/mcp_servers"
      }
    }
  }
}
```

---

## 🔄 迁移对照表

| 旧服务器名称 | 新服务器名称 | 状态 | 说明 |
|------------|------------|------|------|
| `trquant` | ❌ 关闭 | ❌ 删除 | 功能已分散 |
| `trquant-workflow9` | `trquant-workflow` | ✅ 重命名 | 使用新名称 |
| `trquant-project-manager` | `trquant-project` | ✅ 重命名 | 使用新名称 |
| `trquant-dev-task` | ❌ 关闭 | ❌ 删除 | 已整合到trquant-project |
| `trquant-dev-unified` | ❌ 关闭 | ❌ 删除 | 空壳实现 |
| `trquant-dev-test` | `trquant-dev` | ⚠️ 临时 | 后续整合更多工具 |
| `trquant-trading` | `trquant-trading` | ✅ 保留 | 保持不变 |
| - | `trquant-core` | ✅ 新建 | **新增核心服务器** |

---

## ✅ 验证步骤

1. **检查配置文件**:
   ```bash
   cat .cursor/mcp.json | python3 -m json.tool
   ```

2. **确认服务器列表**:
   - 应该只有6个服务器：filesystem, trquant-core, trquant-workflow, trquant-project, trquant-trading, trquant-dev

3. **重启Cursor**:
   - `Ctrl+Shift+P` → `Developer: Reload Window`

4. **验证工具可用**:
   - 测试 `data.get_price`
   - 测试 `market.status`
   - 测试 `backtest.run`

---

## 📊 整合效果

| 指标 | 整合前 | 整合后 | 改进 |
|------|--------|--------|------|
| **服务器数量** | 8个 | 6个 | ⬇️ 减少25% |
| **工具总数** | ~119个 | ~93个 | ⬇️ 减少22% |
| **重复工具** | 30+个 | 0个 | ✅ 消除重复 |
| **空壳工具** | 45个 | 0个 | ✅ 清理空壳 |

---

**文档维护**: TRQuant Team  
**最后更新**: 2024-12-16

