# TRQuant MCP服务器完整列表

> **版本**: v1.0  
> **更新**: 2026-01-16  
> **目的**: 列出TRQuant系统中所有MCP服务器及其功能说明

---

## 📊 统计信息

- **总服务器数量**: 49个
- **核心服务器**: 6个（推荐配置）
- **业务服务器**: 20+个
- **开发工具服务器**: 10+个
- **官方参考服务器**: 多个（在official_servers目录）

---

## 🔧 核心服务器（推荐配置）

这些是最常用的服务器，建议在Windows上优先配置：

| # | 服务器名称 | 文件名 | 工具前缀 | 功能说明 |
|---|-----------|--------|----------|----------|
| 1 | **trquant-core** | `trquant_core_server.py` | `trquant-core.*` | 核心业务服务器（整合数据源、市场、因子、策略、回测、优化） |
| 2 | **trquant-dev** | `unified_dev_server.py` | `trquant-dev.*` | 统一开发工具服务器（任务管理、开发日志、进度跟踪） |
| 3 | **trquant-workflow** | `workflow_9steps_server.py` | `workflow9.*` | 9步骤投资工作流服务器 |
| 4 | **trquant-kb** | `kb_server.py` | `kb.*` | 知识库服务器（RAG搜索、向量索引管理） |
| 5 | **xuanyuan** | `xuanyuan_server.py` | `xuanyuan.*` | 轩辕剑灵开发助手（提示词管理、错误处理、命令助手） |
| 6 | **trquant-backtest** | `backtest_server_v2.py` | `backtest.*` | 回测服务器（策略回测执行和分析） |

---

## 📊 业务服务器（按功能分类）

### 数据源相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 7 | **trquant-data** | `data_source_server_v2.py` | 数据源管理（JQData、AKShare等） |
| 8 | **data-collector** | `data_collector_server.py` | 数据收集服务器 |
| 9 | **data-quality** | `data_quality_server.py` | 数据质量检查服务器 |

### 市场分析相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 10 | **trquant-market** | `market_server_v2.py` | 市场趋势分析服务器 |
| 11 | **market** | `market_server.py` | 市场分析服务器（旧版） |

### 因子相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 12 | **factor** | `factor_server.py` | 因子推荐和计算服务器 |

### 策略相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 13 | **strategy** | `strategy_server.py` | 策略开发和管理服务器 |
| 14 | **strategy-optimizer** | `strategy_optimizer_server.py` | 策略优化服务器 |
| 15 | **strategy-kb** | `strategy_kb_server.py` | 策略知识库服务器 |
| 16 | **strategy-template** | `strategy_template_server.py` | 策略模板服务器 |
| 17 | **bull-market-strategy** | `bull_market_strategy_server.py` | 牛市策略服务器 |

### 回测相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 18 | **backtest** | `backtest_server.py` | 回测服务器（旧版） |
| 19 | **backtest-v2** | `backtest_server_v2.py` | 回测服务器（新版，推荐） |

### 优化相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 20 | **optimizer** | `optimizer_server.py` | 策略参数优化服务器 |

### 交易相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 21 | **trading** | `trading_server.py` | 交易执行服务器 |

### 图表相关

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 22 | **chart** | `chart_server.py` | 图表生成服务器 |

---

## 🛠️ 开发工具服务器

### 任务和工作流管理

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 23 | **trquant-dev** | `unified_dev_server.py` | 统一开发工具服务器（推荐） |
| 24 | **dev-task** | `dev_task_server.py` | 开发任务管理服务器 |
| 25 | **task** | `task_server.py` | 任务管理服务器 |
| 26 | **task-optimizer** | `task_optimizer_server.py` | 任务优化服务器 |
| 27 | **enhanced-dev-workflow** | `enhanced_dev_workflow_server.py` | 增强开发工作流服务器 |
| 28 | **workflow** | `workflow9_server.py` | 工作流服务器（9步骤） |

### 代码和文档管理

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 29 | **code** | `code_server.py` | 代码管理服务器 |
| 30 | **docs** | `docs_server.py` | 文档管理服务器 |
| 31 | **lint** | `lint_server.py` | 代码检查服务器 |

### 知识和证据管理

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 32 | **trquant-kb** | `kb_server.py` | 知识库服务器（推荐） |
| 33 | **kb-grounding** | `kb_grounding_server.py` | 知识库基础服务器 |
| 34 | **evidence** | `evidence_server.py` | 证据记录服务器 |
| 35 | **strategy-kb** | `strategy_kb_server.py` | 策略知识库服务器 |

### 项目和管理

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 36 | **project-manager** | `project_manager_server.py` | 项目管理服务器 |
| 37 | **engineering** | `engineering_server.py` | 工程管理服务器 |
| 38 | **config** | `config_server.py` | 配置管理服务器 |
| 39 | **secrets** | `secrets_server.py` | 密钥管理服务器 |

### 平台和报告

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 40 | **platform-api** | `platform_api_server.py` | 平台API服务器 |
| 41 | **report** | `report_server.py` | 报告生成服务器 |

### 其他工具服务器

| # | 服务器名称 | 文件名 | 功能说明 |
|---|-----------|--------|----------|
| 42 | **xuanyuan** | `xuanyuan_server.py` | 轩辕剑灵开发助手（推荐） |
| 43 | **adr** | `adr_server.py` | ADR（架构决策记录）服务器 |
| 44 | **schema** | `schema_server.py` | 模式管理服务器 |
| 45 | **spec** | `spec_server.py` | 规范服务器 |
| 46 | **test** | `test_server.py` | 测试服务器 |

---

## 📚 辅助模块（非独立服务器）

这些文件是辅助模块，不独立运行，但被其他服务器使用：

| 文件名 | 功能说明 |
|--------|----------|
| `knowledge_hybrid_search.py` | 混合知识搜索（被kb_server使用） |
| `knowledge_search_api.py` | 知识搜索API（被kb_server使用） |
| `knowledge_search_enhanced.py` | 增强知识搜索（被kb_server使用） |
| `knowledge_vector_index.py` | 知识向量索引（被kb_server使用） |

---

## 🌐 官方参考服务器

位于 `mcp_servers/official_servers/` 目录：

| 服务器 | 路径 | 功能说明 |
|--------|------|----------|
| **filesystem** | `official_servers/src/filesystem/` | 文件系统操作（参考实现） |
| **git** | `official_servers/src/git/` | Git操作（参考实现） |
| **memory** | `official_servers/src/memory/` | 记忆管理（参考实现） |
| **time** | `official_servers/src/time/` | 时间管理（参考实现） |
| **sequentialthinking** | `official_servers/src/sequentialthinking/` | 顺序思考（参考实现） |
| **fetch** | `official_servers/src/fetch/` | 网页抓取（参考实现） |
| **everything** | `official_servers/src/everything/` | 综合测试服务器（参考实现） |

**注意**: 这些官方服务器主要用于参考和学习，通常不直接使用。

---

## 🎯 服务器分类统计

### 按用途分类

| 类别 | 数量 | 服务器 |
|------|------|--------|
| **核心业务** | 6 | trquant-core, trquant-kb, trquant-workflow, trquant-backtest, trquant-dev, xuanyuan |
| **数据源** | 3 | data-source, data-collector, data-quality |
| **市场分析** | 2 | market, market-v2 |
| **因子计算** | 1 | factor |
| **策略开发** | 5 | strategy, strategy-optimizer, strategy-kb, strategy-template, bull-market-strategy |
| **回测验证** | 2 | backtest, backtest-v2 |
| **参数优化** | 1 | optimizer |
| **交易执行** | 1 | trading |
| **图表生成** | 1 | chart |
| **开发工具** | 16 | unified-dev, dev-task, task, task-optimizer, enhanced-dev-workflow, code, docs, lint, project-manager, engineering, config, secrets, platform-api, report, adr, schema, spec, test |
| **知识管理** | 3 | kb, kb-grounding, evidence, strategy-kb |
| **官方参考** | 7 | filesystem, git, memory, time, sequentialthinking, fetch, everything |

### 按推荐程度分类

| 推荐程度 | 数量 | 服务器 |
|----------|------|--------|
| **⭐ 强烈推荐** | 6 | trquant-core, trquant-dev, trquant-workflow, trquant-kb, xuanyuan, trquant-backtest |
| **⭐ 推荐** | 10+ | data-source-v2, market-v2, factor, strategy, optimizer, trading, chart, etc. |
| **可选** | 20+ | 其他专用服务器 |
| **参考** | 7 | official_servers目录下的参考实现 |

---

## 📋 完整列表（按字母顺序）

1. `adr_server.py` - ADR服务器
2. `backtest_server.py` - 回测服务器（旧版）
3. `backtest_server_v2.py` - 回测服务器（新版）⭐
4. `bull_market_strategy_server.py` - 牛市策略服务器
5. `chart_server.py` - 图表生成服务器
6. `code_server.py` - 代码管理服务器
7. `config_server.py` - 配置管理服务器
8. `data_collector_server.py` - 数据收集服务器
9. `data_quality_server.py` - 数据质量检查服务器
10. `data_source_server.py` - 数据源服务器（旧版）
11. `data_source_server_v2.py` - 数据源服务器（新版）
12. `dev_task_server.py` - 开发任务管理服务器
13. `docs_server.py` - 文档管理服务器
14. `engineering_server.py` - 工程管理服务器
15. `enhanced_dev_workflow_server.py` - 增强开发工作流服务器
16. `evidence_server.py` - 证据记录服务器
17. `factor_server.py` - 因子推荐和计算服务器
18. `kb_grounding_server.py` - 知识库基础服务器
19. `kb_server.py` - 知识库服务器 ⭐
20. `lint_server.py` - 代码检查服务器
21. `market_server.py` - 市场分析服务器（旧版）
22. `market_server_v2.py` - 市场趋势分析服务器
23. `optimizer_server.py` - 策略参数优化服务器
24. `platform_api_server.py` - 平台API服务器
25. `project_manager_server.py` - 项目管理服务器
26. `report_server.py` - 报告生成服务器
27. `schema_server.py` - 模式管理服务器
28. `secrets_server.py` - 密钥管理服务器
29. `spec_server.py` - 规范服务器
30. `strategy_kb_server.py` - 策略知识库服务器
31. `strategy_optimizer_server.py` - 策略优化服务器
32. `strategy_server.py` - 策略开发和管理服务器
33. `strategy_template_server.py` - 策略模板服务器
34. `task_optimizer_server.py` - 任务优化服务器
35. `task_server.py` - 任务管理服务器
36. `test_server.py` - 测试服务器
37. `trading_server.py` - 交易执行服务器
38. `trquant_core_server.py` - 核心业务服务器 ⭐
39. `unified_dev_server.py` - 统一开发工具服务器 ⭐
40. `unified_utils_server.py` - 统一工具服务器
41. `workflow_9steps_server.py` - 9步骤工作流服务器 ⭐
42. `workflow_server_strategy_integration.py` - 工作流策略集成服务器
43. `workflow9_server.py` - 工作流服务器（9步骤）
44. `xuanyuan_server.py` - 轩辕剑灵开发助手 ⭐

---

## 🚀 快速配置指南

### 最小配置（3个核心服务器）

对于Windows用户，推荐先配置这3个核心服务器：

```json
{
  "mcpServers": {
    "trquant-core": { ... },
    "trquant-dev": { ... },
    "trquant-kb": { ... }
  }
}
```

### 完整配置（6个推荐服务器）

```json
{
  "mcpServers": {
    "trquant-core": { ... },
    "trquant-dev": { ... },
    "trquant-workflow": { ... },
    "trquant-kb": { ... },
    "xuanyuan": { ... },
    "trquant-backtest": { ... }
  }
}
```

### 使用自动配置脚本

在Windows上运行：
```powershell
.\scripts\setup_mcp_config.ps1
```

---

## 📝 相关文档

- `docs/WINDOWS_MCP_SERVER_SETUP_GUIDE.md` - Windows MCP配置完整指南
- `docs/07_workflow/MCP配置指南.md` - 通用MCP配置指南
- `docs/XUANYUAN_MCP_SETUP.md` - 轩辕剑灵服务器配置

---

**最后更新**: 2026-01-16  
**维护者**: TRQuant Team
