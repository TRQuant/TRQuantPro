# TRQuant Cursor Extension 系统设计文档

## 1. 系统概述

TRQuant Cursor Extension 是一个专为A股量化投资设计的 Cursor IDE 插件。它将韬睿量化系统的核心能力封装为可视化命令和 MCP 工具，使用户能够在 Cursor 中直接进行市场分析、因子选择和策略生成。

### 1.1 设计目标

- **易用性**: 通过命令面板和快捷键快速访问量化功能
- **可视化**: 使用 WebView 展示专业的分析报告和策略代码
- **AI 增强**: 通过 MCP 协议让 Cursor AI 直接调用量化工具
- **跨平台**: 支持 Linux、macOS 和 Windows

### 1.2 核心价值

1. **市场洞察**: 实时获取市场状态（Regime）和投资主线
2. **智能选股**: 基于市场环境推荐量化因子
3. **策略生成**: 自动生成 PTrade/QMT 策略代码
4. **回测分析**: 分析回测结果，提供优化建议

## 2. 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Cursor IDE                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐    ┌────────────────┐                   │
│  │   Commands     │    │    Views       │                   │
│  │ (TypeScript)   │    │   (WebView)    │                   │
│  └───────┬────────┘    └───────┬────────┘                   │
│          │                     │                             │
│          ▼                     ▼                             │
│  ┌─────────────────────────────────────────┐                │
│  │           TRQuantClient                  │                │
│  │     (TypeScript Service Layer)          │                │
│  └───────────────────┬─────────────────────┘                │
│                      │                                       │
│                      │ JSON over stdio                       │
│                      ▼                                       │
│  ┌─────────────────────────────────────────┐                │
│  │           bridge.py                      │                │
│  │     (Python Backend Bridge)             │                │
│  └───────────────────┬─────────────────────┘                │
│                      │                                       │
└──────────────────────┼──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   TRQuant Core                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Trend     │  │   Factor    │  │  Strategy   │         │
│  │  Analyzer   │  │   Manager   │  │  Generator  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  FiveDim    │  │  Candidate  │  │  Workflow   │         │
│  │  Scorer     │  │   Pool      │  │ Orchestrator│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 分层设计

| 层级 | 组件 | 职责 |
|------|------|------|
| **表现层** | Commands, Views | 用户交互、WebView渲染 |
| **服务层** | TRQuantClient, MCPRegistrar | 通信管理、配置管理 |
| **桥接层** | bridge.py | TypeScript-Python 通信 |
| **核心层** | TRQuant Core | 量化分析、策略生成 |

### 2.2 通信机制

**JSON over stdio**:
```
TypeScript                    Python
    │                            │
    │  {"action": "xxx", ...}    │
    ├──────────────────────────►│
    │                            │
    │  {"ok": true, "data": ...} │
    │◄──────────────────────────┤
```

## 3. 模块设计

### 3.1 命令模块 (Commands)

| 命令 | 功能 | 文件 |
|------|------|------|
| `trquant.getMarketStatus` | 获取市场状态 | `getMarketStatus.ts` |
| `trquant.getMainlines` | 获取投资主线 | `getMainlines.ts` |
| `trquant.recommendFactors` | 推荐因子 | `recommendFactors.ts` |
| `trquant.generateStrategy` | 生成策略 | `generateStrategy.ts` |
| `trquant.analyzeBacktest` | 回测分析 | `analyzeBacktest.ts` |
| `trquant.enableMCP` | 启用MCP | `extension.ts` |
| `trquant.showPanel` | 打开面板 | `extension.ts` |

### 3.2 服务模块 (Services)

**TRQuantClient**:
- 封装与 Python 后端通信
- 提供类型安全的 API
- 处理超时和错误

**MCPRegistrar**:
- 注册 MCP Server 到 Cursor
- 管理 MCP 配置文件
- 跨平台路径处理

### 3.3 工具模块 (Utils)

**Logger**:
- 多级别日志（DEBUG/INFO/WARN/ERROR）
- 输出到 VS Code Output Channel
- 错误级别自动弹窗通知

**Config**:
- 集中配置管理
- 支持用户自定义
- 配置变更监听

**Errors**:
- 自定义错误类型
- 错误码枚举
- 用户友好的错误消息

### 3.4 类型定义 (Types)

```typescript
// 市场状态
interface MarketStatus {
    regime: 'risk_on' | 'risk_off' | 'neutral';
    index_trend: Record<string, IndexTrend>;
    style_rotation: StyleScore[];
    summary: string;
}

// 投资主线
interface Mainline {
    name: string;
    score: number;
    industries: string[];
    logic: string;
}

// 量化因子
interface Factor {
    name: string;
    category: FactorCategory;
    weight: number;
    reason: string;
}

// 策略
interface Strategy {
    code: string;
    name: string;
    platform: 'ptrade' | 'qmt';
    style: StrategyStyle;
    risk_params: RiskParams;
}
```

## 4. MCP 集成

### 4.1 MCP 工具列表

| 工具 | 描述 |
|------|------|
| `trquant_market_status` | 获取市场状态和Regime |
| `trquant_mainlines` | 获取投资主线TOP N |
| `trquant_recommend_factors` | 推荐量化因子 |
| `trquant_generate_strategy` | 生成策略代码 |
| `trquant_analyze_backtest` | 分析回测结果 |

### 4.2 使用示例

在 Cursor AI 对话中：
```
用户: 帮我生成一个适合当前市场的PTrade策略

AI: 我来调用TRQuant工具分析市场并生成策略...
[调用 trquant_market_status]
[调用 trquant_recommend_factors]
[调用 trquant_generate_strategy]
```

## 5. 软件工程原则

### 5.1 SOLID 原则

- **S**ingle Responsibility: 每个模块单一职责
- **O**pen-Closed: 对扩展开放，对修改关闭
- **L**iskov Substitution: 类型安全的接口设计
- **I**nterface Segregation: 接口按功能分离
- **D**ependency Inversion: 依赖注入模式

### 5.2 代码质量

- TypeScript 严格类型检查
- ESLint 代码规范
- 完整的 JSDoc 注释
- 统一的错误处理

### 5.3 测试覆盖

- `test_bridge.py`: Python 后端测试
- `test_mcp.py`: MCP Server 测试
- 所有测试用例通过

## 6. 目录结构

```
extension/
├── package.json          # 扩展配置
├── tsconfig.json         # TypeScript配置
├── webpack.config.js     # 打包配置
├── src/
│   ├── extension.ts      # 入口文件
│   ├── commands/         # 命令实现
│   │   ├── getMarketStatus.ts
│   │   ├── getMainlines.ts
│   │   ├── recommendFactors.ts
│   │   ├── generateStrategy.ts
│   │   └── analyzeBacktest.ts
│   ├── services/         # 服务层
│   │   ├── trquantClient.ts
│   │   └── mcpRegistrar.ts
│   ├── views/            # WebView
│   │   └── marketPanel.ts
│   ├── types/            # 类型定义
│   │   └── index.ts
│   └── utils/            # 工具模块
│       ├── logger.ts
│       ├── config.ts
│       └── errors.ts
├── python/
│   ├── bridge.py         # Python桥接
│   ├── mcp_server.py     # MCP Server
│   ├── test_bridge.py    # Bridge测试
│   ├── test_mcp.py       # MCP测试
│   └── tools/
│       └── strategy_generator.py
├── docs/
│   ├── DESIGN.md         # 设计文档
│   └── INSTALLATION.md   # 安装指南
├── scripts/
│   ├── setup.sh          # Linux安装脚本
│   └── setup.bat         # Windows安装脚本
└── rules/                # Cursor规则
    ├── trquant-architecture.mdc
    ├── trquant-prompts.mdc
    └── trquant-style.mdc
```

## 7. 版本规划

| 版本 | 功能 |
|------|------|
| v1.0 | MVP - 市场分析、因子推荐、策略生成 |
| v1.1 | MCP集成、回测分析 |
| v1.2 | 实时数据、股票筛选 |
| v2.0 | 回测引擎、持仓管理 |

## 8. 参考资料

- [VS Code Extension API](https://code.visualstudio.com/api)
- [Cursor MCP 文档](https://docs.cursor.com/context/model-context-protocol)
- [TRQuant 核心文档](../docs/)
