# 模块索引 (Module Index)

列出项目主要模块及其文件路径、职责说明、对外接口和调用入口：

## Extension核心模块 (`extension/src/`)

### 入口模块 (`extension.ts`)

- **路径**：`extension/src/extension.ts`
- **职责**：扩展激活入口，注册所有命令、视图、提供者；初始化全局服务（TRQuantClient、ConfigManager等）
- **对外接口**：VS Code扩展激活函数`activate(context)`，导出供VS Code调用
- **调用入口**：VS Code加载扩展时自动调用`activate`函数

### 命令模块 (`commands/`)

- **路径**：`extension/src/commands/`
- **职责**：实现用户命令的具体逻辑，如获取市场状态、运行回测、生成策略等
- **对外接口**：通过`vscode.commands.registerCommand`注册的命令ID（如`trquant.getMarketStatus`）
- **调用入口**：用户在命令面板执行命令时触发，或在WebView中通过`vscode.postMessage`调用
- **主要文件**：
  - `getMarketStatus.ts` - 获取市场状态
  - `getMainlines.ts` - 获取投资主线
  - `recommendFactors.ts` - 推荐因子
  - `generateStrategy.ts` - 生成策略代码
  - `runBacktest.ts` - 运行回测
  - `createProject.ts` - 创建项目
  - `analyzeBacktest.ts` - 分析回测结果

### 服务模块 (`services/`)

- **路径**：`extension/src/services/`
- **职责**：封装核心业务逻辑，提供可复用的服务类
- **对外接口**：导出服务类供Commands和Views使用
- **主要服务**：
  - **TRQuantClient** (`trquantClient.ts`)
    - 职责：与Python Bridge通信的客户端
    - 接口：`getMarketStatus()`, `getMainlines()`, `runBacktest()`等
    - 调用：Commands和Views通过依赖注入使用
  - **BacktestManager** (`backtestManager.ts`)
    - 职责：管理回测任务队列、状态跟踪
    - 接口：`addTask()`, `getStatus()`, `cancelTask()`
  - **StrategyOptimizer** (`strategyOptimizer/`)
    - 职责：策略代码分析、平台转换、报告生成、学习引擎
    - 接口：`analyzeStrategy()`, `convertToPlatform()`, `generateReport()`
  - **ProjectConfig** (`projectConfig.ts`)
    - 职责：项目配置管理
    - 接口：`loadConfig()`, `saveConfig()`, `validateConfig()`
  - **MCPRegistrar** (`mcpRegistrar.ts`)
    - 职责：注册MCP服务器，与Cursor AI集成
    - 接口：`registerMCP()`, `unregisterMCP()`

### 视图模块 (`views/`)

- **路径**：`extension/src/views/`
- **职责**：实现WebView面板，提供图形化用户界面
- **对外接口**：通过`vscode.window.createWebviewPanel`创建的面板，通过`postMessage`与Extension通信
- **调用入口**：通过命令或TreeView节点点击触发
- **主要视图**：
  - `mainDashboard.ts` - 主工作台（8步骤工作流入口）
  - `backtestConfigPanel.ts` - 回测配置面板
  - `backtestReportPanel.ts` - 回测报告展示
  - `strategyOptimizerPanel.ts` - 策略优化器面板
  - `marketTrendPanel.ts` - 市场趋势分析面板
  - `mainlinePanel.ts` - 投资主线面板
  - `factorPanel.ts` - 因子构建面板
  - `workflowPanel.ts` - 工作流面板

### 提供者模块 (`providers/`)

- **路径**：`extension/src/providers/`
- **职责**：实现TreeView数据提供者，在侧边栏显示树形结构
- **对外接口**：实现`vscode.TreeDataProvider`接口
- **调用入口**：VS Code自动调用`getChildren()`等方法
- **主要提供者**：
  - `projectExplorer.ts` - 项目资源管理器
  - `quickActionsProvider.ts` - 快捷操作
  - `strategyCompletionProvider.ts` - 策略代码补全
  - `strategyDiagnosticProvider.ts` - 策略代码诊断

### 工具模块 (`utils/`)

- **路径**：`extension/src/utils/`
- **职责**：提供通用工具函数和类
- **对外接口**：导出函数和类供其他模块使用
- **主要工具**：
  - `logger.ts` - 统一日志系统
  - `config.ts` - 配置管理
  - `errors.ts` - 错误处理和类型定义
  - `projectNameGenerator.ts` - 项目名生成器

### 类型定义 (`types/`)

- **路径**：`extension/src/types/`
- **职责**：定义TypeScript类型和接口
- **对外接口**：导出类型供其他模块使用
- **主要文件**：`index.ts` - 所有类型定义

## Python模块

### Bridge模块 (`extension/python/bridge.py`)

- **路径**：`extension/python/bridge.py`
- **职责**：作为TypeScript和Python之间的通信桥梁，处理JSON协议转换、子进程管理
- **对外接口**：通过stdin接收JSON请求，通过stdout返回JSON响应
- **调用入口**：由`TRQuantClient`通过子进程启动，持续监听stdin
- **协议格式**：
  - 请求：`{"action": "get_market_status", "params": {...}}`
  - 响应：`{"ok": true, "data": {...}, "error": null}`

### Python工具模块 (`extension/python/tools/`)

- **路径**：`extension/python/tools/`
- **职责**：提供Python工具函数，如回测引擎
- **主要文件**：
  - `backtest_engine.py` - 本地回测引擎

### Python核心模块 (`core/`)

- **路径**：项目根目录`core/`
- **职责**：核心业务逻辑，包括工作流编排、数据源管理、因子计算等
- **调用方式**：由`bridge.py`导入并调用
- **主要模块**：
  - `workflow_orchestrator.py` - 工作流编排器
  - `data_source_manager.py` - 数据源管理
  - `factors/` - 因子计算模块
  - `trading/` - 交易接口模块

## 配置文件

### Extension配置

- **`extension/package.json`**
  - 职责：定义扩展清单、命令、视图、激活事件
  - 关键字段：`contributes.commands`, `contributes.views`, `activationEvents`

- **`extension/tsconfig.json`**
  - 职责：TypeScript编译配置
  - 关键设置：严格模式、模块解析、目标版本

- **`extension/webpack.config.js`**
  - 职责：打包配置，将TypeScript编译为单个JS文件
  - 输出：`extension/dist/extension.js`

### Python配置

- **`extension/python/requirements.txt`**
  - 职责：Python依赖列表
  - 使用：在虚拟环境中安装依赖

## 模块调用关系图

```
extension.ts (激活)
  ├── 注册 Commands
  │   └── commands/*.ts
  │       └── services/trquantClient.ts
  │           └── python/bridge.py
  │               └── core/*.py
  ├── 注册 Views
  │   └── views/*.ts
  │       └── services/trquantClient.ts
  └── 注册 Providers
      └── providers/*.ts
          └── utils/*.ts
```

## 数据流

1. **用户操作** → Command/View
2. **Command/View** → Service (TRQuantClient)
3. **Service** → Python Bridge (stdin/stdout)
4. **Bridge** → Python Core
5. **Python Core** → 返回结果
6. **Bridge** → Service (JSON响应)
7. **Service** → Command/View
8. **Command/View** → 显示给用户

