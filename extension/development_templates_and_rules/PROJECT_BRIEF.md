# 项目概要 (Project Brief)

## 项目整体目标

- **TRQuant Cursor Extension（韬睿量化扩展）**是一个VS Code扩展，旨在为A股量化投资提供完整的开发、回测和实盘交易支持。项目采用TypeScript + Python混合架构，通过Python Bridge实现与量化引擎的通信，提供策略开发、回测、优化等全流程功能。

- 项目遵循**单人高效开发**原则，充分利用Cursor + Claude Opus 4.5进行AI辅助开发，确保代码质量和一致性，同时控制token成本。

- **核心价值**：将量化策略开发从传统Web平台迁移到IDE环境，提供更好的开发体验、代码补全、实时反馈和策略优化能力。

*(提供此概要有助于为AI助手提供项目高层信息，避免其逐文件推断架构导致的高代价"运行时调研"。这相当于为AI提供新成员入项指南，从一开始就了解项目架构。)*

## 系统架构设计

### 三层架构

```
┌─────────────────────────────────────────┐
│  VS Code Extension (TypeScript)        │
│  - Commands (命令)                      │
│  - Views (WebView面板)                  │
│  - Services (服务层)                    │
│  - Providers (数据提供者)               │
└──────────────┬──────────────────────────┘
               │ stdin/stdout JSON
               │ (Python Bridge)
┌──────────────▼──────────────────────────┐
│  Python Bridge (bridge.py)             │
│  - 协议转换 (JSON ↔ Python对象)        │
│  - 错误处理                             │
│  - 子进程管理                           │
└──────────────┬──────────────────────────┘
               │ 调用
┌──────────────▼──────────────────────────┐
│  Python Core (core/)                   │
│  - 工作流编排器                         │
│  - 数据源管理                           │
│  - 因子计算                             │
│  - 回测引擎                             │
│  - 策略生成器                           │
└─────────────────────────────────────────┘
```

### 核心组件

1. **VS Code Extension (TypeScript)**
   - 位置：`extension/src/`
   - 职责：提供用户界面、命令注册、WebView面板、与Python通信
   - 技术栈：TypeScript, VS Code API, WebView API

2. **Python Bridge**
   - 位置：`extension/python/bridge.py`
   - 职责：作为TypeScript和Python之间的通信桥梁，处理JSON协议转换
   - 通信方式：stdin/stdout JSON消息

3. **Python Core**
   - 位置：`core/` (项目根目录)
   - 职责：核心业务逻辑，包括工作流、数据源、因子、回测等
   - 技术栈：Python 3.8+, pandas, numpy等

4. **策略优化器**
   - 位置：`extension/src/services/strategyOptimizer/`
   - 职责：代码分析、平台转换、报告生成、学习引擎
   - 特色：支持从A股实操手册实时学习

## 模块职责概述

### Extension模块 (`extension/src/`)

- **Commands (`commands/`)**：用户命令实现，如`getMarketStatus`、`runBacktest`等
- **Services (`services/`)**：核心服务，如`TRQuantClient`（Python通信）、`BacktestManager`（回测管理）、`StrategyOptimizer`（策略优化）
- **Views (`views/`)**：WebView面板，如`MainDashboard`（主工作台）、`BacktestConfigPanel`（回测配置）等
- **Providers (`providers/`)**：TreeView数据提供者，如`ProjectExplorer`（项目树）、`QuickActionsProvider`（快捷操作）
- **Utils (`utils/`)**：工具函数，如`logger`（日志）、`config`（配置）、`errors`（错误处理）

### Python模块

- **Bridge (`extension/python/bridge.py`)**：通信桥梁，处理JSON协议
- **Tools (`extension/python/tools/`)**：工具模块，如`backtest_engine.py`（回测引擎）
- **Core (`core/`)**：核心业务逻辑（在项目根目录）

### 配置文件

- **`extension/package.json`**：扩展清单，定义命令、视图、激活事件
- **`extension/tsconfig.json`**：TypeScript配置
- **`extension/webpack.config.js`**：打包配置

## 接口与调用关系

### 1. 命令调用流程

```
用户操作 (Ctrl+Shift+P)
  ↓
VS Code命令注册 (extension.ts)
  ↓
Command Handler (commands/*.ts)
  ↓
TRQuantClient (services/trquantClient.ts)
  ↓
Python Bridge (python/bridge.py)
  ↓
Python Core (core/*.py)
  ↓
返回结果 (JSON)
  ↓
显示给用户 (WebView/Notification)
```

### 2. WebView通信流程

```
WebView Panel (views/*.ts)
  ↓
postMessage (WebView → Extension)
  ↓
handleMessage (Extension处理)
  ↓
TRQuantClient调用
  ↓
postMessage (Extension → WebView)
  ↓
更新UI
```

### 3. Python Bridge协议

- **请求格式**：`{"action": "get_market_status", "params": {...}}`
- **响应格式**：`{"ok": true, "data": {...}, "error": null}`
- **通信方式**：stdin/stdout，JSON编码

## 关键设计原则

1. **单一职责**：每个模块只负责一个明确的功能
2. **依赖注入**：服务通过构造函数注入，便于测试
3. **统一错误处理**：使用`ErrorHandler`统一处理异常
4. **类型安全**：TypeScript严格模式，Python使用类型提示
5. **DRY原则**：避免重复代码，提取公共逻辑

## 开发工作流

1. **功能开发**：在`commands/`或`views/`中实现新功能
2. **服务封装**：复杂逻辑封装到`services/`中
3. **Python集成**：如需Python功能，在`bridge.py`中添加action
4. **测试**：编写单元测试和集成测试
5. **文档**：更新相关文档和类型定义

（详细模块列表参见`MODULE_INDEX.md`以获取每个模块的职责、接口和入口定义。）

