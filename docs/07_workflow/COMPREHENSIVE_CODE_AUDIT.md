# TRQuant 代码全面审计报告

> 审计日期: 2025-12-19 | 审计版本: v2.0

---

## 一、项目规模总览

### 1.1 代码统计

| 模块 | 文件数 | 代码行数 | 主要功能 |
|------|--------|----------|----------|
| MCP服务器 | 39 | 13,432 | 后端业务逻辑 |
| 工具模块 | 47 | 14,174 | 核心算法引擎 |
| Extension视图 | 15 | 11,553 | Cursor面板UI |
| Extension命令 | 7 | 2,166 | VS Code命令 |
| Python桥接 | 7 | 1,890 | TS↔Python通信 |
| **总计** | **115+** | **43,215+** | - |

### 1.2 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cursor Extension (TypeScript)               │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ workflowPanel │  │ tenbaggerDash │  │ stockDetail   │       │
│  │   (2164行)    │  │   (701行)     │  │   (662行)     │       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
│          │                  │                  │                │
│          └──────────────────┼──────────────────┘                │
│                             │                                   │
│              ┌──────────────▼──────────────┐                   │
│              │  Python Bridge (bridge.py)  │                   │
│              │        (1890行)             │                   │
│              └──────────────┬──────────────┘                   │
└─────────────────────────────┼───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                     MCP Server Layer (Python)                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │workflow_9steps  │  │trquant_core     │  │backtest_server  │ │
│  │  (614行)        │  │  (1132行)       │  │  (943行)        │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │           │
│  ┌────────▼────────────────────▼────────────────────▼────────┐ │
│  │                    Utils Layer (14,174行)                  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │ tenbagger_   │  │ scorecard    │  │ stage_       │     │ │
│  │  │ evaluator    │  │  (541行)     │  │ machine      │     │ │
│  │  │  (465行)     │  │              │  │  (341行)     │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │ candidate_   │  │ industry_    │  │ datasource_  │     │ │
│  │  │ pool (269行) │  │ chain(324行) │  │ manager      │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、核心模块详解

### 2.1 九步投资工作流

**文件**: `mcp_servers/workflow_9steps_server.py` (614行)

| 步骤 | ID | 调用服务器 | 功能 |
|------|-----|-----------|------|
| 1 | data_source | data_source_server_v2 | 数据源健康检查 |
| 2 | market_trend | market_server_v2 | 市场趋势分析 |
| 3 | mainline | market_server_v2 | 投资主线识别 |
| 4 | candidate_pool | data_source_server_v2 | 候选池筛选 |
| 5 | factor | factor_server | 因子构建推荐 |
| 6 | strategy | strategy_template_server | 策略生成 |
| 7 | backtest | backtest_server | 回测验证 |
| 8 | optimization | optimizer_server | 策略优化 |
| 9 | report | report_server | 报告生成 |

**相关工具文件**:
- `utils/workflow_storage.py` (189行) - 工作流持久化
- `utils/workflow_context.py` (297行) - 上下文管理
- `utils/workflow_batch.py` (257行) - 批量执行

### 2.2 十倍股识别系统

**核心文件** (共20个):

| 文件 | 行数 | 功能 |
|------|------|------|
| `utils/tenbagger_evaluator.py` | 465 | 综合评估引擎 |
| `utils/tenbagger_tools.py` | 232 | 工具函数 |
| `utils/scorecard.py` | 541 | 7维评分卡 |
| `utils/stage_machine.py` | 341 | S0-S5阶段状态机 |
| `utils/candidate_pool.py` | 269 | L0-L3分层候选池 |
| `utils/industry_chain.py` | 324 | 产业链图谱 |
| `utils/event_extractor.py` | 437 | 事件抽取 |
| `utils/altdata_tier2.py` | 438 | Tier2另类数据 |
| `utils/altdata_tools.py` | 249 | AltData工具 |
| `utils/datasource_manager.py` | 598 | 数据源管理 |
| `extension/python/tenbagger_commands.py` | 348 | Python命令 |
| `extension/src/views/tenbaggerDashboard.ts` | 701 | 仪表盘面板 |
| `extension/src/views/stockDetailPanel.ts` | 662 | 个股详情面板 |
| `extension/src/views/industryChainPanel.ts` | 684 | 产业链面板 |

**评估维度** (7维):
1. **Stage** (20%) - 发展阶段 S0-S5
2. **ScoreCard** (25%) - 财务评分
3. **Growth** (15%) - 成长性
4. **Industry** (15%) - 行业地位
5. **AltData** (10%) - 另类数据信号
6. **Momentum** (10%) - 市场动量
7. **Risk** (5%) - 风险调整

### 2.3 MCP工具注册 (132个)

**按类别**:
```
strategy    : 11个  │  scorecard   : 10个  │  portfolio   : 10个
experiment  : 9个   │  chain       : 9个   │  altdata     : 9个
stage       : 8个   │  datasource  : 8个   │  event       : 7个
pool        : 7个   │  tenbagger   : 7个   │  market      : 5个
workflow9   : 5个   │  其他        : 27个
```

---

## 三、Cursor Extension 结构

### 3.1 视图面板 (15个)

| 面板 | 文件 | 行数 | 状态 | 功能 |
|------|------|------|------|------|
| 工作流面板 | workflowPanel.ts | 2164 | ⚠️ 按钮问题 | 9步工作流+十倍股 |
| 十倍股仪表盘 | tenbaggerDashboard.ts | 701 | ✅ | 候选池+排名 |
| 个股详情 | stockDetailPanel.ts | 662 | ✅ | 评分卡+时间线 |
| 产业链图谱 | industryChainPanel.ts | 684 | ✅ | 产业链可视化 |
| 主仪表盘 | mainDashboard.ts | 2707 | ✅ | 系统入口 |
| 回测面板 | backtestPanel.ts | 699 | ✅ | 策略回测 |
| 策略生成器 | strategyGeneratorPanel.ts | 781 | ✅ | 策略生成 |
| 策略管理器 | strategyManagerPanel.ts | 553 | ✅ | 策略管理 |
| 优化器面板 | optimizerPanel.ts | 742 | ✅ | 策略优化 |
| 报告面板 | reportPanel.ts | 617 | ✅ | 报告查看 |
| 市场面板 | marketPanel.ts | 252 | ✅ | 市场状态 |
| 结果管理器 | resultManagerPanel.ts | 638 | ✅ | 回测结果 |
| 监控面板 | monitoringPanel.ts | 479 | ✅ | 系统监控 |

### 3.2 消息通信流程

```
[Webview HTML]
    │
    │ onclick="runStep('data_source')"
    │
    ▼
[JavaScript函数]
    │
    │ vscode.postMessage({ command: 'runStep', stepId: 'data_source' })
    │
    ▼
[Extension _handleMessage()]
    │
    │ case 'runStep': this._runStep(message.stepId)
    │
    ▼
[Python Bridge]
    │
    │ proc.stdin.write(JSON.stringify(request))
    │
    ▼
[MCP Server]
    │
    │ workflow9.run_step
    │
    ▼
[返回结果]
```

---

## 四、当前问题诊断

### 4.1 工作流面板按钮失效

**症状**: 点击"执行"按钮无响应

**已验证**:
- ✅ MCP后端正常 (`workflow9.run_step` 返回正确结果)
- ✅ Python Bridge正常 (命令行测试通过)
- ❌ Webview JavaScript未执行
- ❌ `acquireVsCodeApi()` 未被调用

**根因分析**:
1. CSP (Content-Security-Policy) 限制
2. 外部脚本加载阻塞
3. HTML结构或脚本语法错误

### 4.2 修复尝试记录

| 尝试 | 修改 | 结果 |
|------|------|------|
| v0.2.14 | 添加CSP meta标签 | ❌ |
| v0.2.15 | 添加诊断fetch日志 | ❌ |
| v0.2.16 | 移除echarts+放宽CSP | ❌ |

---

## 五、重新开发方案

### 5.1 方案对比

| 方案 | 优点 | 缺点 | 推荐度 |
|------|------|------|--------|
| 修复现有Webview | 保留现有代码 | 调试困难,原因不明 | ⭐⭐ |
| 重构为简化Webview | 从零开始,控制复杂度 | 需要重写 | ⭐⭐⭐⭐ |
| Webview + React | 现代化,工具链成熟 | 增加构建复杂度 | ⭐⭐⭐ |
| Streamlit独立GUI | 开发快,Python原生 | 不在Cursor内 | ⭐⭐⭐ |

### 5.2 推荐方案: 渐进式重构

**Phase 1**: 创建最小可用Webview (MVP)
- 只有基本HTML+CSS+JS
- 无外部依赖
- 验证消息通信

**Phase 2**: 逐步添加9步工作流UI
- 步骤列表
- 执行按钮
- 结果显示

**Phase 3**: 添加十倍股功能
- 候选池统计
- 潜力排名
- 个股评估

**Phase 4**: 添加可视化
- 图表组件
- 产业链图谱
- 时间线

**Phase 5**: 整合报告和回测
- 报告生成
- 回测结果
- 导出功能

---

## 六、文件清单

### 6.1 十倍股系统完整文件 (20个)

**Python后端**:
```
mcp_servers/utils/tenbagger_evaluator.py    # 评估引擎
mcp_servers/utils/tenbagger_tools.py        # 工具函数
mcp_servers/utils/scorecard.py              # 评分卡
mcp_servers/utils/stage_machine.py          # 阶段状态机
mcp_servers/utils/candidate_pool.py         # 候选池
mcp_servers/utils/industry_chain.py         # 产业链
mcp_servers/utils/event_extractor.py        # 事件抽取
mcp_servers/utils/altdata_tier2.py          # Tier2数据
mcp_servers/utils/altdata_tools.py          # AltData工具
mcp_servers/utils/datasource_manager.py     # 数据源管理
mcp_servers/utils/experiment.py             # 实验跟踪
mcp_servers/utils/strategy_pack.py          # 策略包
mcp_servers/utils/strategy_tools.py         # 策略工具
mcp_servers/trquant_core_server.py          # 核心服务器
mcp_servers/crawlers/pipeline.py            # 爬虫管道
extension/python/tenbagger_commands.py      # Python命令
```

**TypeScript前端**:
```
extension/src/views/workflowPanel.ts        # 工作流面板
extension/src/views/tenbaggerDashboard.ts   # 仪表盘
extension/src/views/stockDetailPanel.ts     # 个股详情
extension/src/views/industryChainPanel.ts   # 产业链
extension/src/views/registerPanels.ts       # 面板注册
extension/src/pythonBridge.ts               # Python桥接
extension/src/views/index.ts                # 视图导出
```

### 6.2 九步工作流完整文件 (10个)

**Python后端**:
```
mcp_servers/workflow_9steps_server.py       # 主服务器
mcp_servers/workflow_server_strategy_integration.py  # 策略集成
mcp_servers/utils/workflow_storage.py       # 存储
mcp_servers/utils/workflow_context.py       # 上下文
mcp_servers/utils/workflow_batch.py         # 批量执行
mcp_servers/data_source_server_v2.py        # 数据源
mcp_servers/market_server_v2.py             # 市场分析
mcp_servers/factor_server.py                # 因子服务
mcp_servers/backtest_server.py              # 回测服务
mcp_servers/optimizer_server.py             # 优化服务
mcp_servers/report_server.py                # 报告服务
mcp_servers/strategy_template_server.py     # 策略模板
```

**TypeScript前端**:
```
extension/src/views/workflowPanel.ts        # 工作流面板 (共用)
extension/python/bridge.py                  # Python桥接
extension/python/workflow_direct.py         # 直接调用
```

---

*审计完成时间: 2025-12-19 08:00*
