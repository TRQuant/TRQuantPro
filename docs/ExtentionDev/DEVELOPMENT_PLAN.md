# TRQuant Cursor Extension 开发方案

## 一、项目概述

### 1.1 背景回顾
- **美股场景**: QuantConnect插件 → 策略代码生成 → 回测 → 代码迭代 → 分析报告（完整流程）
- **A股场景**: TRQuant系统已有完整工作流框架，需要开发Cursor插件实现类似体验

### 1.2 目标
开发 TRQuant Cursor Extension，实现：
1. 在Cursor IDE中直接调用TRQuant功能
2. 通过MCP协议让Cursor AI自动调用TRQuant工具
3. 通过规则文件指导AI生成符合TRQuant规范的策略代码

---

## 二、技术架构

### 2.1 整体架构
```
┌─────────────────────────────────────────────────────────────┐
│                     Cursor IDE                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ TRQuant         │  │ Cursor AI       │  │ .cursor/    │ │
│  │ Extension       │  │ (Composer/Chat) │  │ rules/      │ │
│  │ (TypeScript)    │  │                 │  │ (mdc files) │ │
│  └────────┬────────┘  └────────┬────────┘  └─────────────┘ │
│           │                    │                            │
│           │    ┌───────────────┴───────────────┐           │
│           │    │        MCP Protocol           │           │
│           │    └───────────────┬───────────────┘           │
│           │                    │                            │
└───────────┼────────────────────┼────────────────────────────┘
            │                    │
            ▼                    ▼
┌───────────────────────────────────────────────────────────┐
│              TRQuant MCP Server (Python)                   │
├───────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│  │ MCP Tools   │ │ Bridge API  │ │ TRQuant Core        │ │
│  │             │ │             │ │ ├── TrendAnalyzer   │ │
│  │ • market    │ │ JSON/stdio  │ │ ├── CandidatePool   │ │
│  │ • mainlines │ │ HTTP/REST   │ │ ├── FactorManager   │ │
│  │ • factors   │ │             │ │ ├── StrategyGen     │ │
│  │ • strategy  │ │             │ │ └── BacktestEngine  │ │
│  └─────────────┘ └─────────────┘ └─────────────────────┘ │
└───────────────────────────────────────────────────────────┘
```

### 2.2 通信方案
| 场景 | 方案 | 说明 |
|------|------|------|
| Extension命令 | JSON over stdio | 子进程调用bridge.py |
| AI对话调用 | MCP Protocol | Cursor AI自动调用MCP工具 |
| 后端HTTP服务 | REST API | 可选，用于Dashboard等 |

---

## 三、项目结构

```
trquant-cursor-extension/
├── package.json                    # Extension配置
├── tsconfig.json
├── src/
│   ├── extension.ts               # 入口，注册命令和MCP
│   ├── commands/
│   │   ├── getMarketStatus.ts     # 获取市场状态
│   │   ├── getMainlines.ts        # 获取投资主线
│   │   ├── recommendFactors.ts    # 推荐因子
│   │   ├── generateStrategy.ts    # 生成策略
│   │   ├── analyzeBacktest.ts     # 分析回测（进阶）
│   │   └── riskAssessment.ts      # 风险评估（进阶）
│   ├── services/
│   │   ├── trquantClient.ts       # Python后端通信
│   │   └── mcpRegistrar.ts        # MCP Server注册
│   ├── views/
│   │   ├── marketPanel.ts         # 市场状态WebView
│   │   ├── strategyPanel.ts       # 策略预览面板
│   │   └── backtestPanel.ts       # 回测结果面板
│   └── utils/
│       ├── promptBuilder.ts       # Prompt构建器
│       └── config.ts              # 配置管理
├── python/
│   ├── __init__.py
│   ├── bridge.py                  # Extension桥接（stdio）
│   ├── mcp_server.py              # MCP Server主程序
│   ├── tools/                     # MCP工具实现
│   │   ├── market_tools.py
│   │   ├── factor_tools.py
│   │   └── strategy_tools.py
│   └── adapters/                  # TRQuant核心适配器
│       └── trquant_adapter.py
├── rules/                         # Cursor规则文件模板
│   ├── trquant-architecture.mdc
│   ├── trquant-prompts.mdc
│   └── trquant-style.mdc
└── README.md
```

---

## 四、MCP工具定义

### 4.1 核心工具列表
| 工具名称 | 功能 | 参数 | 返回 |
|----------|------|------|------|
| `trquant_get_market_status` | 获取市场状态 | universe, as_of | regime, trends, style_rotation |
| `trquant_get_mainlines` | 获取投资主线 | top_n, time_horizon | mainlines[], scores |
| `trquant_recommend_factors` | 推荐因子 | market_regime, mainlines | factors[], weights |
| `trquant_generate_strategy` | 生成策略代码 | factors, style, risk_params | ptrade_code, explanation |
| `trquant_analyze_backtest` | 分析回测结果 | backtest_file | metrics, diagnosis |
| `trquant_risk_assessment` | 风险评估 | portfolio | risk_metrics, suggestions |

### 4.2 JSON协议示例
```json
// 请求
{
  "action": "get_market_status",
  "params": {
    "universe": "CN_EQ",
    "as_of": "2025-12-02",
    "lookback_days": 60
  }
}

// 响应
{
  "ok": true,
  "data": {
    "regime": "risk_on",
    "index_trend": {
      "SH000300": {"zscore": 1.2, "trend": "up"},
      "SZ399006": {"zscore": -0.5, "trend": "flat"}
    },
    "style_rotation": [
      {"style": "growth", "score": 0.8},
      {"style": "value", "score": -0.3}
    ],
    "summary": "当前市场风险偏好回升，成长风格占优..."
  }
}
```

---

## 五、开发路线图

### Phase 0: 项目初始化（1周）
- [ ] 创建Extension项目骨架
- [ ] 配置TypeScript/Webpack构建
- [ ] 验证在Cursor中安装运行
- [ ] 创建Python MCP Server骨架

### Phase 1: MVP实现（2-3周）
- [ ] 实现bridge.py与TRQuant Core对接
- [ ] 实现4个核心命令
  - [ ] TRQuant: Get Market Status
  - [ ] TRQuant: Get Mainlines  
  - [ ] TRQuant: Recommend Factors
  - [ ] TRQuant: Generate Strategy
- [ ] 实现简单WebView展示
- [ ] 实现StatusBar状态显示

### Phase 2: MCP集成（2-4周）
- [ ] 实现完整MCP Server
- [ ] 注册MCP工具到Cursor
- [ ] 编写.cursor/rules规则文件
- [ ] 验证Cursor Composer调用MCP工具
- [ ] 优化Prompt生成逻辑

### Phase 3: 进阶功能（3-6周）
- [ ] 回测分析命令
- [ ] 风险评估命令
- [ ] 策略对比命令
- [ ] 回测可视化面板
- [ ] 因子分析面板

### Phase 4: 发布优化（1-2周）
- [ ] 打包VSIX
- [ ] 编写用户文档
- [ ] 发布到Open VSX（可选）

---

## 六、.cursor/rules 规则文件内容

### trquant-architecture.mdc
```markdown
---
description: TRQuant量化系统架构说明
globs: ["**/*.py", "**/*.ts"]
---

# TRQuant 系统模块

## 核心模块
- TrendAnalyzer: 市场趋势分析，输出regime(风险偏好)和style(风格轮动)
- CandidatePoolBuilder: 候选池构建，基于投资主线筛选股票
- FactorManager: 因子计算和管理
- StrategyGenerator: PTrade策略代码生成

## PTrade策略规范
- 入口函数: initialize(), handle_data()
- 必须包含风控逻辑: 止损、仓位控制
- 支持的订单类型: order_value(), order_target_percent()
```

### trquant-prompts.mdc  
```markdown
---
description: TRQuant AI交互指南
globs: ["**/*.py"]
---

# 使用TRQuant MCP工具的指南

当用户请求量化策略相关任务时：
1. 首先调用 trquant_get_market_status 了解当前市场状态
2. 然后调用 trquant_get_mainlines 获取投资主线
3. 基于以上信息调用 trquant_recommend_factors 获取因子建议
4. 最后调用 trquant_generate_strategy 生成策略代码

生成策略时必须：
- 包含完整的风控逻辑
- 注明策略适用的市场环境
- 提供参数说明和调优建议
```

---

## 七、下一步行动

### 立即开始
1. **创建Extension项目目录**
2. **编写package.json和基础配置**
3. **实现bridge.py连接TRQuant Core**
4. **实现第一个命令: Get Market Status**

### 需要确认
- Extension项目放在TRQuant内部还是独立仓库？
- 建议放在: `/home/taotao/dev/QuantTest/TRQuant/extension/`

---

*文档版本: v1.0*
*创建日期: 2025-12-02*

