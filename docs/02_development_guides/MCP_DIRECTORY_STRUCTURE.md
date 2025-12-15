# MCP服务器目录结构设计

> **版本**: v1.0.0  
> **制定时间**: 2025-12-14  
> **适用范围**: 所有TRQuant MCP服务器

---

## 📋 概述

本文档定义了TRQuant系统中MCP服务器的目录组织结构，按照功能分类组织26个MCP服务器。

## 🎯 设计原则

1. **功能分类**: 按功能模块分类组织
2. **清晰层次**: 目录结构清晰，易于查找
3. **易于维护**: 便于添加新服务器和维护
4. **向后兼容**: 保持现有导入路径兼容

---

## 📁 目录结构

```
mcp_servers/
├── business/              # 业务流程类MCP
│   ├── factor_server.py
│   ├── backtest_server.py
│   ├── trading_server.py
│   ├── optimizer_server.py
│   ├── strategy_template_server.py
│   ├── strategy_optimizer_server.py
│   └── report_server.py
├── data/                  # 数据类MCP
│   ├── data_source_server.py
│   ├── data_quality_server.py
│   ├── data_collector_server.py
│   ├── kb_server.py
│   └── strategy_kb_server.py
├── dev/                   # 开发支撑类MCP
│   ├── engineering_server.py
│   ├── code_server.py
│   ├── lint_server.py
│   ├── test_server.py
│   ├── task_server.py
│   ├── workflow_server.py
│   ├── docs_server.py
│   ├── spec_server.py
│   ├── adr_server.py
│   ├── manual_generator_server.py
│   ├── evidence_server.py
│   ├── schema_server.py
│   ├── config_server.py
│   └── secrets_server.py
└── utils/                 # 工具类（保持不变）
    ├── parameter_validator.py
    ├── trace_manager.py
    ├── error_handler.py
    ├── artifacts.py
    └── ...
```

---

## 🔄 迁移计划

### 阶段1: 创建新目录结构

```bash
mkdir -p mcp_servers/business
mkdir -p mcp_servers/data
mkdir -p mcp_servers/dev
```

### 阶段2: 迁移服务器文件

按照分类迁移文件到对应目录。

### 阶段3: 更新导入路径

更新所有引用MCP服务器的代码，使用新的导入路径。

### 阶段4: 更新配置文件

更新`.cursor/mcp.json`等配置文件中的路径。

---

## 📖 相关文档

- [MCP服务器分类体系](./MCP_CLASSIFICATION.md)
- [MCP服务合并策略](./MCP_MERGE_STRATEGY.md)

---

**最后更新**: 2025-12-14
