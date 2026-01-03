# MCP 服务器组织架构

## 📋 概述

TRQuant 的 MCP 服务器分为两大类：
1. **投资工作流服务器** - 核心业务功能
2. **开发工具服务器** - 开发辅助功能

## 📊 投资工作流服务器

### 1. `trquant` (核心业务服务器)
**路径**: `extension/python/mcp_server.py`

**功能**: TRQuant 核心投资工作流
- `trquant_market_status` - 获取市场状态
- `trquant_mainlines` - 获取投资主线
- `trquant_recommend_factors` - 推荐量化因子
- `trquant_generate_strategy` - 生成策略代码
- `trquant_analyze_backtest` - 分析回测结果

**用途**: 9步投资工作流的核心功能

### 2. `trquant-trading` (交易服务器)
**路径**: `mcp_servers/trading_server.py`

**功能**: 交易执行和账户管理
- 账户状态查询
- 持仓查询
- 订单管理
- 模拟交易

**用途**: 策略执行和交易管理

---

## 🛠️ 开发工具服务器

### 1. `trquant-dev-task` (任务管理服务器) ⭐ 合并版
**路径**: `mcp_servers/dev_task_server.py`

**功能**: 开发任务管理和优化
- **任务管理**: `task.list`, `task.create`, `task.get`, `task.update`, `task.complete`
- **任务优化**: `task.analyze`, `task.recommend_mode`, `task.cache_context`

**说明**: 合并了原来的 `task_server.py` 和 `task_optimizer_server.py`

### 2. `trquant-dev-unified` (统一开发工具)
**路径**: `mcp_servers/unified_utils_server.py`

**功能**: 综合开发工具（已合并多个小服务器）
- 代码分析、检查、转换
- 规范检查
- 工程工具（测试、构建、部署）
- 文档管理
- 数据模型验证
- 密钥管理
- 证据管理
- ADR管理
- 数据采集
- 数据质量检查
- 策略知识库
- 策略优化
- 平台API转换

**说明**: 包含 42+ 个工具，整合了多个小服务器

### 3. `trquant-dev-code` (代码服务器)
**路径**: `mcp_servers/code_server.py`

**功能**: 代码分析工具
- `code.analyze` - 分析策略代码
- `code.lint` - 检查代码规范
- `code.convert` - 转换代码格式

### 4. `trquant-dev-lint` (代码检查服务器)
**路径**: `mcp_servers/lint_server.py`

**功能**: 代码质量检查
- `lint.check` - 检查代码质量
- `lint.fix` - 自动修复问题
- `lint.rules` - 列出检查规则

### 5. `trquant-dev-spec` (规范服务器)
**路径**: `mcp_servers/spec_server.py`

**功能**: 规范管理
- `spec.list` - 列出所有规范
- `spec.get` - 获取规范详情
- `spec.check` - 检查是否符合规范

### 6. `trquant-dev-test` (测试服务器)
**路径**: `mcp_servers/test_server.py`

**功能**: 测试工具
- `test.run` - 运行pytest测试
- `test.report` - 生成测试报告
- `test.coverage` - 获取代码覆盖率

---

## 📁 其他服务器

### 1. `filesystem` (文件系统服务器)
**功能**: 文件读写操作

### 2. `git` (Git服务器)
**功能**: Git版本控制操作

---

## 🔄 合并历史

### 已合并的服务器
- `task_server.py` + `task_optimizer_server.py` → `dev_task_server.py`
- 15个小服务器 → `unified_utils_server.py` (42+ 工具)

### 保留的独立服务器
- `trquant` - 核心业务，保持独立
- `trquant-trading` - 交易功能，保持独立
- `trquant-dev-code`, `trquant-dev-lint`, `trquant-dev-spec`, `trquant-dev-test` - 专业工具，保持独立

---

## 📝 配置建议

### 最小配置（仅核心功能）
```json
{
  "mcpServers": {
    "trquant": { ... },
    "trquant-trading": { ... },
    "trquant-dev-task": { ... },
    "trquant-dev-unified": { ... }
  }
}
```

### 完整配置（包含所有开发工具）
```json
{
  "mcpServers": {
    "trquant": { ... },
    "trquant-trading": { ... },
    "trquant-dev-task": { ... },
    "trquant-dev-unified": { ... },
    "trquant-dev-code": { ... },
    "trquant-dev-lint": { ... },
    "trquant-dev-spec": { ... },
    "trquant-dev-test": { ... },
    "filesystem": { ... },
    "git": { ... }
  }
}
```

---

## 🎯 使用建议

1. **投资工作流**: 使用 `trquant` 和 `trquant-trading`
2. **任务管理**: 使用 `trquant-dev-task`
3. **代码开发**: 使用 `trquant-dev-unified`（包含大部分工具）
4. **专业工具**: 根据需要启用 `trquant-dev-code`, `trquant-dev-lint` 等

---

## 📊 工具统计

- **投资工作流工具**: ~10 个
- **开发工具**: ~60+ 个
- **总工具数**: ~70+ 个















































