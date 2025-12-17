# TRQuant MCP服务器整合方案

## 一、当前状态分析

### 1.1 已启用的MCP服务器 (mcp.json)

| # | 服务器名称 | 文件 | 工具数 | 功能 |
|---|-----------|------|-------|------|
| 1 | filesystem | (官方) | ~15 | 文件系统操作 |
| 2 | trquant | mcp_server.py | ~20 | 主扩展服务 |
| 3 | trquant-workflow9 | workflow_9steps_server.py | 6 | 9步投资工作流 |
| 4 | trquant-project-manager | project_manager_server.py | 17 | 项目规划管理 |
| 5 | trquant-dev-task | dev_task_server.py | 8 | 开发任务管理 |
| 6 | trquant-dev-unified | unified_utils_server.py | 45 | 统一工具集(空壳) |
| 7 | trquant-dev-test | test_server.py | 3 | 测试运行 |
| 8 | trquant-trading | trading_server.py | 5 | 交易执行 |

**总计: 8个服务器, ~119个工具**

### 1.2 未启用但存在的服务器文件

```
mcp_servers/
├── data_source_server_v2.py    # 数据源 (9 tools)
├── market_server_v2.py         # 市场分析 (11 tools)
├── backtest_server.py          # 回测 (12 tools)
├── optimizer_server.py         # 优化 (6 tools)
├── factor_server.py            # 因子 (? tools)
├── strategy_server.py          # 策略 (? tools)
├── report_server.py            # 报告 (? tools)
└── ... (30+ 其他文件)
```

### 1.3 发现的问题

#### 🔴 严重问题

1. **工具重复**: `task.*` 在3个服务器中重复定义
   - `trquant-dev-task`: task.list, task.create, task.update, task.complete
   - `trquant-project-manager`: task.create, task.update, task.list
   - `trquant-dev-unified`: task.analyze_complexity, task.recommend_mode

2. **空壳实现**: `unified_utils_server.py` 定义了45个工具但全是占位符

3. **版本混乱**: 存在v1/v2两套服务器，但只用了一部分

#### 🟡 中等问题

4. **启用不完整**: 核心服务器(data_source, market, backtest)未在mcp.json中启用
5. **功能分散**: 相关功能分散在多个服务器中

---

## 二、整合方案

### 2.1 目标架构 (从8个减少到5个)

```
┌─────────────────────────────────────────────────────────┐
│                    MCP服务器层次架构                      │
├─────────────────────────────────────────────────────────┤
│  L0: 官方服务器                                          │
│      └── filesystem (保留)                               │
├─────────────────────────────────────────────────────────┤
│  L1: 核心量化服务器 (NEW: trquant-core)                  │
│      ├── data.*     数据源 (从data_source_server_v2合并)  │
│      ├── market.*   市场分析 (从market_server_v2合并)     │
│      ├── factor.*   因子库                               │
│      ├── strategy.* 策略管理                             │
│      ├── backtest.* 回测引擎                             │
│      └── optimizer.*参数优化                             │
├─────────────────────────────────────────────────────────┤
│  L2: 工作流服务器                                        │
│      ├── trquant-workflow (保留workflow9)                │
│      └── trquant-project (保留,整合task)                 │
├─────────────────────────────────────────────────────────┤
│  L3: 交易与开发服务器                                    │
│      ├── trquant-trading (保留)                          │
│      └── trquant-dev (合并unified+test)                  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 工具合并映射

#### 删除重复 (减少约30个工具)

| 原工具 | 保留位置 | 删除位置 |
|-------|---------|---------|
| task.create/update/list | trquant-project-manager | trquant-dev-task |
| task.analyze/recommend_mode | trquant-project-manager | unified_utils_server |
| code.analyze/lint/convert | trquant-dev | unified(空壳) |
| spec.*/lint.* | trquant-dev | unified(空壳) |

#### 合并到 trquant-core (新)

```python
# 工具命名空间
data.get_price          # 从 data_source_server_v2
data.get_index_stocks
data.health_check
data.candidate_pool

market.status           # 从 market_server_v2
market.trend
market.mainlines
market.five_dimension_score
market.comprehensive

factor.recommend        # 从 factor_server
factor.calculate
factor.analyze

strategy.generate       # 从 strategy_server
strategy.list_templates
strategy.validate

backtest.run            # 从 backtest_server
backtest.quick
backtest.jqdata
backtest.compare

optimizer.grid_search   # 从 optimizer_server
optimizer.optuna
optimizer.best_params
```

### 2.3 整合后的服务器列表

| # | 服务器 | 工具数 | 职责 |
|---|-------|-------|------|
| 1 | filesystem | 15 | 文件操作(官方) |
| 2 | **trquant-core** | 35 | 数据+市场+因子+策略+回测+优化 |
| 3 | trquant-workflow | 6 | 9步工作流 |
| 4 | trquant-project | 17 | 项目+任务+经验+日志 |
| 5 | trquant-trading | 5 | 交易执行 |
| 6 | trquant-dev | 15 | 代码+lint+测试+文档 |

**整合后: 6个服务器, ~93个工具 (减少22%)**

---

## 三、改进建议

### 3.1 统一命名规范

```
# 命名格式: <领域>.<动作>
data.get_price      ✅ 好
getData             ❌ 避免
get-price           ❌ 避免
```

### 3.2 统一参数格式

```python
# 标准化日期参数
"start_date": {"type": "string", "format": "date", "example": "2024-01-01"}
"end_date": {"type": "string", "format": "date", "example": "2024-12-31"}

# 标准化股票代码
"securities": {"type": "array", "items": {"type": "string"}, "example": ["000001.XSHE"]}
```

### 3.3 统一返回格式

```python
# 成功响应
{
    "success": True,
    "data": {...},
    "timestamp": "2024-12-16T10:00:00",
    "tool": "market.status"
}

# 错误响应
{
    "success": False,
    "error": "错误描述",
    "error_code": "DATA_NOT_FOUND",
    "timestamp": "2024-12-16T10:00:00"
}
```

### 3.4 添加性能监控

```python
# 每个工具调用自动记录
{
    "tool": "backtest.run",
    "duration_ms": 1234,
    "input_size": 100,
    "output_size": 50
}
```

### 3.5 添加缓存层

```python
# 对频繁调用的工具添加缓存
@cached(ttl=300)  # 5分钟缓存
async def _handle_market_status(args):
    ...
```

---

## 四、实施步骤

### Phase 1: 清理 (1天)
- [ ] 删除未使用的v1服务器文件
- [ ] 删除unified_utils_server中的空壳工具
- [ ] 统一mcp.json配置

### Phase 2: 合并 (2天)
- [ ] 创建trquant-core服务器
- [ ] 合并task.*到project_manager
- [ ] 合并dev相关工具

### Phase 3: 优化 (1天)
- [ ] 统一返回格式
- [ ] 添加性能监控
- [ ] 添加缓存层

### Phase 4: 测试 (1天)
- [ ] 编写整合测试
- [ ] 验证GUI兼容性
- [ ] 文档更新

---

## 五、即时可执行的清理

### 5.1 删除冗余文件

```bash
# 可安全删除的v1版本
rm mcp_servers/data_source_server.py  # 保留v2
rm mcp_servers/market_server.py       # 保留v2
rm mcp_servers/backtest_server_v2.py  # 与backtest_server重复

# 未使用的单独服务器(已合并到unified)
rm mcp_servers/code_server.py
rm mcp_servers/lint_server.py
rm mcp_servers/spec_server.py
rm mcp_servers/docs_server.py
rm mcp_servers/schema_server.py
rm mcp_servers/secrets_server.py
rm mcp_servers/evidence_server.py
rm mcp_servers/adr_server.py
rm mcp_servers/data_collector_server.py
rm mcp_servers/data_quality_server.py
rm mcp_servers/strategy_kb_server.py
rm mcp_servers/strategy_optimizer_server.py
rm mcp_servers/task_optimizer_server.py
rm mcp_servers/platform_api_server.py
rm mcp_servers/kb_server.py
```

### 5.2 更新mcp.json

```json
{
  "mcpServers": {
    "filesystem": { ... },
    "trquant-core": {
      "command": "python",
      "args": ["mcp_servers/trquant_core_server.py"]
    },
    "trquant-workflow": {
      "command": "python", 
      "args": ["mcp_servers/workflow_9steps_server.py"]
    },
    "trquant-project": {
      "command": "python",
      "args": ["mcp_servers/project_manager_server.py"]
    },
    "trquant-trading": {
      "command": "python",
      "args": ["mcp_servers/trading_server.py"]
    },
    "trquant-dev": {
      "command": "python",
      "args": ["mcp_servers/dev_server.py"]
    }
  }
}
```

---

## 六、风险评估

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| 工具名变更导致GUI失效 | 高 | 保持工具名不变，只合并服务器 |
| 性能下降 | 中 | 使用异步加载，按需导入 |
| 功能丢失 | 低 | 先测试后删除 |

---

*创建时间: 2024-12-16*
*作者: TRQuant Dev Team*

