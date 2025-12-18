# MCP工具命名规范

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中所有MCP工具的命名规范，确保工具名称的一致性、可读性和可维护性。

## 🎯 命名原则

1. **一致性**: 所有工具遵循统一的命名格式
2. **可读性**: 名称清晰表达工具的功能
3. **可维护性**: 名称便于分类和管理
4. **简洁性**: 避免过长的名称

---

## 📝 工具名称格式

### 基本格式

```
{模块}.{动作}[.{子动作}]
```

### 格式说明

- **模块**: 工具所属的功能模块（小写，使用点分隔）
- **动作**: 工具执行的主要操作（小写，使用点分隔）
- **子动作**: 可选，用于细化操作（小写，使用点分隔）

### 命名规则

1. **全部小写**: 使用小写字母
2. **点分隔**: 使用点（`.`）分隔各部分
3. **动词优先**: 动作部分优先使用动词
4. **避免缩写**: 除非是广泛认知的缩写（如 `api`, `id`）
5. **避免下划线**: 不使用下划线（`_`）分隔

---

## 🏷️ 模块命名规范

### 标准模块列表

| 模块 | 说明 | 示例工具 |
|------|------|----------|
| `kb` | 知识库（Knowledge Base） | `kb.query`, `kb.stats` |
| `engineering` | 工程管理 | `engineering.plan`, `engineering.work` |
| `data` | 数据源 | `data.query`, `data.list_sources` |
| `backtest` | 回测 | `backtest.run`, `backtest.report` |
| `strategy` | 策略 | `strategy.generate`, `strategy.optimize` |
| `factor` | 因子 | `factor.calculate`, `factor.list` |
| `trading` | 交易 | `trading.order`, `trading.position` |
| `workflow` | 工作流 | `workflow.run`, `workflow.status` |
| `code` | 代码分析 | `code.search`, `code.analyze` |
| `spec` | 规范文档 | `spec.read`, `spec.validate` |
| `task` | 任务管理 | `task.create`, `task.list` |
| `optimizer` | 优化器 | `optimizer.run`, `optimizer.results` |
| `evidence` | 证据记录 | `evidence.record`, `evidence.query` |
| `docs` | 文档管理 | `docs.generate`, `docs.update` |
| `config` | 配置管理 | `config.get`, `config.set` |
| `lint` | 代码检查 | `lint.check`, `lint.fix` |
| `adr` | 架构决策记录 | `adr.create`, `adr.list` |
| `report` | 报告生成 | `report.generate`, `report.list` |
| `schema` | 模式管理 | `schema.validate`, `schema.generate` |
| `secrets` | 密钥管理 | `secrets.get`, `secrets.set` |
| `data_quality` | 数据质量 | `data_quality.check`, `data_quality.report` |
| `data_collector` | 数据采集 | `data_collector.crawl`, `data_collector.schedule` |
| `manual_generator` | 手册生成 | `manual_generator.create`, `manual_generator.update` |
| `strategy_kb` | 策略知识库 | `strategy_kb.query`, `strategy_kb.add` |
| `strategy_template` | 策略模板 | `strategy_template.list`, `strategy_template.get` |
| `strategy_optimizer` | 策略优化器 | `strategy_optimizer.run`, `strategy_optimizer.results` |

### 模块命名规则

1. **单一职责**: 每个模块代表一个明确的功能领域
2. **简洁明了**: 使用简洁的单词或常见缩写
3. **避免冲突**: 确保模块名称不重复
4. **一致性**: 相关模块使用统一的命名风格

---

## ⚙️ 动作命名规范

### 标准动作列表

| 动作 | 说明 | 示例 |
|------|------|------|
| `query` | 查询 | `kb.query`, `data.query` |
| `list` | 列出 | `data.list_sources`, `task.list` |
| `get` | 获取单个 | `config.get`, `spec.get` |
| `create` | 创建 | `task.create`, `adr.create` |
| `update` | 更新 | `docs.update`, `config.update` |
| `delete` | 删除 | `task.delete`, `evidence.delete` |
| `run` | 运行/执行 | `backtest.run`, `workflow.run` |
| `generate` | 生成 | `report.generate`, `docs.generate` |
| `validate` | 验证 | `spec.validate`, `schema.validate` |
| `analyze` | 分析 | `code.analyze`, `data.analyze` |
| `optimize` | 优化 | `strategy.optimize`, `factor.optimize` |
| `calculate` | 计算 | `factor.calculate`, `backtest.calculate` |
| `check` | 检查 | `lint.check`, `data_quality.check` |
| `fix` | 修复 | `lint.fix`, `code.fix` |
| `record` | 记录 | `evidence.record`, `workflow.record` |
| `search` | 搜索 | `code.search`, `spec.search` |
| `stats` | 统计 | `kb.stats`, `backtest.stats` |
| `report` | 报告 | `backtest.report`, `data_quality.report` |
| `order` | 下单 | `trading.order`, `trading.cancel_order` |
| `position` | 持仓 | `trading.position`, `trading.list_positions` |

### 动作命名规则

1. **动词优先**: 使用动词表达操作
2. **标准动作**: 优先使用标准动作列表中的动词
3. **明确性**: 动作名称清晰表达操作意图
4. **避免歧义**: 避免使用容易产生歧义的动词

---

## 📚 命名示例

### ✅ 正确示例

```python
# 知识库工具
"kb.query"              # 查询知识库
"kb.stats"              # 获取统计信息
"kb.index.build"        # 构建索引

# 工程管理工具
"engineering.plan"      # 制定计划
"engineering.work"       # 执行工作
"engineering.review"    # 审查代码

# 数据源工具
"data.query"            # 查询数据
"data.list_sources"     # 列出数据源
"data.validate"         # 验证查询

# 回测工具
"backtest.run"          # 运行回测
"backtest.report"        # 生成报告
"backtest.list_results" # 列出结果

# 策略工具
"strategy.generate"      # 生成策略
"strategy.optimize"     # 优化策略
"strategy.list"         # 列出策略
```

### ❌ 错误示例

```python
# 使用下划线分隔
"kb_query"              # ❌ 应使用点分隔
"data_list_sources"     # ❌ 应使用点分隔

# 使用大写字母
"KB.Query"               # ❌ 应全部小写
"Data.Query"             # ❌ 应全部小写

# 动作不明确
"kb.get"                # ❌ 应使用更具体的动作，如 query
"data.do"               # ❌ 应使用明确的动作

# 模块名称过长
"knowledge_base.query"  # ❌ 应使用缩写 kb
"data_source.query"     # ❌ 应使用 data
```

---

## 🔄 迁移指南

### 现有工具名称映射

对于现有不符合规范的工具名称，需要进行迁移：

| 旧名称 | 新名称 | 说明 |
|--------|--------|------|
| `trquant_mainlines` | `mainline.identify` | 主线识别 |
| `trquant_market_status` | `market.status` | 市场状态 |
| `trquant_generate_strategy` | `strategy.generate` | 策略生成 |
| `trquant_recommend_factors` | `factor.recommend` | 因子推荐 |
| `trquant_analyze_backtest` | `backtest.analyze` | 回测分析 |

### 迁移步骤

1. **更新工具定义**: 在MCP服务器中更新工具名称
2. **更新调用代码**: 更新所有调用该工具的代码
3. **更新文档**: 更新相关文档和示例
4. **保持兼容**: 在过渡期保持旧名称的兼容性（可选）

---

## 📖 相关文档

- [MCP参数结构规范](./MCP_PARAMETER_SCHEMA.md)
- [MCP工具调用流程规范](./CURSOR_MCP_CALL_FLOW.md)
- [MCP错误码体系](./ERROR_CODE_SYSTEM.md)

---

**最后更新**: 2025-12-14  
**维护者**: 轩辕剑灵（AI Assistant）
