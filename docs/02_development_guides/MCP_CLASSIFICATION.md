# MCP服务器分类体系

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中MCP服务器的分类体系，用于组织和管理26个MCP服务器。

## 🎯 分类原则

1. **功能相关性**: 相关功能的服务器归类在一起
2. **调用频率**: 高频和低频服务器分开管理
3. **资源需求**: 计算密集型服务器单独管理
4. **安全隔离**: 安全相关的服务器单独管理

---

## 📁 分类体系

### 1. 业务流程类 (business/)

核心业务逻辑相关的MCP服务器。

| 服务器 | 说明 | 调用频率 |
|--------|------|----------|
| `factor_server.py` | 因子计算和管理 | 高频 |
| `backtest_server.py` | 回测执行 | 高频 |
| `trading_server.py` | 交易执行 | 中频 |
| `optimizer_server.py` | 策略优化 | 中频 |
| `strategy_template_server.py` | 策略模板 | 中频 |
| `strategy_optimizer_server.py` | 策略优化器 | 中频 |
| `report_server.py` | 报告生成 | 中频 |

### 2. 数据类 (data/)

数据相关的MCP服务器。

| 服务器 | 说明 | 调用频率 |
|--------|------|----------|
| `data_source_server.py` | 数据源管理 | 高频 |
| `data_quality_server.py` | 数据质量检查 | 中频 |
| `data_collector_server.py` | 数据采集 | 低频 |
| `kb_server.py` | 知识库 | 高频 |
| `strategy_kb_server.py` | 策略知识库 | 中频 |

### 3. 开发支撑类 (dev/)

开发工具和支撑服务。

| 服务器 | 说明 | 调用频率 |
|--------|------|----------|
| `engineering_server.py` | 工程管理 | 中频 |
| `code_server.py` | 代码分析 | 高频 |
| `lint_server.py` | 代码检查 | 中频 |
| `test_server.py` | 测试服务 | 低频 |
| `task_server.py` | 任务管理 | 中频 |
| `workflow_server.py` | 工作流 | 高频 |
| `docs_server.py` | 文档管理 | 中频 |
| `spec_server.py` | 规范文档 | 中频 |
| `adr_server.py` | 架构决策记录 | 低频 |
| `manual_generator_server.py` | 手册生成 | 低频 |
| `evidence_server.py` | 证据记录 | 高频 |
| `schema_server.py` | 模式管理 | 中频 |
| `config_server.py` | 配置管理 | 中频 |
| `secrets_server.py` | 密钥管理 | 低频 |

---

## 🔄 调用频率分类

### 高频服务器 (>10次/天)

- `data_source_server.py`
- `kb_server.py`
- `code_server.py`
- `workflow_server.py`
- `factor_server.py`
- `backtest_server.py`
- `evidence_server.py`

### 中频服务器 (1-10次/天)

- `trading_server.py`
- `optimizer_server.py`
- `strategy_optimizer_server.py`
- `data_quality_server.py`
- `engineering_server.py`
- `lint_server.py`
- `task_server.py`
- `docs_server.py`
- `spec_server.py`
- `schema_server.py`
- `config_server.py`
- `report_server.py`
- `strategy_template_server.py`
- `strategy_kb_server.py`

### 低频服务器 (<1次/天)

- `data_collector_server.py`
- `test_server.py`
- `adr_server.py`
- `manual_generator_server.py`
- `secrets_server.py`

---

## 🔒 安全隔离分类

### 需要安全隔离的服务器

- `trading_server.py` - 交易执行，需要严格安全控制
- `secrets_server.py` - 密钥管理，需要加密存储
- `data_collector_server.py` - 爬虫服务，需要网络隔离

### 需要资源隔离的服务器

- `backtest_server.py` - 计算密集型，需要独立资源
- `data_collector_server.py` - 网络密集型，需要独立资源

---

## 📖 相关文档

- [MCP目录结构设计](./MCP_DIRECTORY_STRUCTURE.md)
- [MCP服务合并策略](./MCP_MERGE_STRATEGY.md)

---

**最后更新**: 2025-12-14
