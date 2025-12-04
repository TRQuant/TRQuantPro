# TRQuant Extension 最终任务列表

> 基于完整代码审查后的精确任务列表
> 更新时间: 2025-12-03

---

## 📊 总体状态

| 类别 | 完成 | 待完成 | 完成率 |
|------|------|--------|--------|
| 核心架构 | 8 | 0 | 100% |
| 命令实现 | 7 | 0 | 100% |
| 视图实现 | 4 | 3 | 57% |
| MCP工具 | 5 | 7 | 42% |
| 文档 | 5 | 0 | 100% |

---

## ✅ 已完成模块（无需修改）

### 核心架构
- [x] Extension入口 (`extension.ts`)
- [x] TypeScript客户端 (`trquantClient.ts`)
- [x] MCP注册器 (`mcpRegistrar.ts`)
- [x] 配置管理 (`projectConfig.ts`)
- [x] 回测管理 (`backtestManager.ts`)
- [x] 日志系统 (`logger.ts`)
- [x] 错误处理 (`errors.ts`)
- [x] 配置工具 (`config.ts`)

### 命令实现
- [x] 获取市场状态 (`getMarketStatus.ts`)
- [x] 获取投资主线 (`getMainlines.ts`)
- [x] 推荐因子 (`recommendFactors.ts`)
- [x] 生成策略 (`generateStrategy.ts`)
- [x] 分析回测 (`analyzeBacktest.ts`)
- [x] 创建项目 (`createProject.ts`)
- [x] 运行回测 (`runBacktest.ts`)

### 视图实现
- [x] 市场面板 (`marketPanel.ts`)
- [x] Dashboard面板 (`dashboardPanel.ts`)
- [x] 欢迎面板 (`welcomePanel.ts`)
- [x] 项目资源管理器 (`projectExplorer.ts`)

### Python后端
- [x] Bridge通信 (`bridge.py`)
- [x] MCP Server (`mcp_server.py`)
- [x] 策略生成器 (`strategy_generator.py`)
- [x] 回测引擎 (`backtest_engine.py`)

### 文档
- [x] 系统设计 (`DESIGN.md`)
- [x] 安装指南 (`INSTALLATION.md`)
- [x] 使用教程 (`USAGE.md`)
- [x] README (`README.md`)
- [x] 快速开始 (`QUICK_START.md`)

---

## 🔴 紧急任务（立即执行）

### Task-001: 编译并打包
```
优先级: 🔴 紧急
预计时间: 10分钟
状态: ⏳ 待执行

执行命令:
cd /home/taotao/dev/QuantTest/TRQuant/extension
rm -rf dist
npm run compile
npx @vscode/vsce package --allow-missing-repository --no-dependencies
```

### Task-002: 安装测试
```
优先级: 🔴 紧急
预计时间: 5分钟
状态: ⏳ 待执行

执行命令:
cursor --install-extension trquant-cursor-extension-0.1.0.vsix
# 重启Cursor
# 测试: Ctrl+Shift+P -> TRQuant
```

---

## 🟡 短期任务（本周）

### Task-003: 实现市场状态TreeView
```
优先级: 🟡 重要
预计时间: 2小时
文件: src/views/marketTreeView.ts

功能:
- 显示当前Regime (Risk On/Off/Neutral)
- 显示主要指数趋势
- 显示风格轮动状态
- 定时自动刷新
```

### Task-004: 实现投资主线TreeView
```
优先级: 🟡 重要
预计时间: 2小时
文件: src/views/mainlinesTreeView.ts

功能:
- 显示TOP20投资主线
- 评分和排名
- 相关行业展示
- 点击查看详情
```

### Task-005: 实现策略管理TreeView
```
优先级: 🟡 重要
预计时间: 2小时
文件: src/views/strategiesTreeView.ts

功能:
- 列出项目中所有策略文件
- 显示平台类型(PTrade/QMT)
- 右键菜单: 运行、编辑、删除
- 策略状态指示
```

### Task-006: 扩展MCP工具集
```
优先级: 🟡 重要
预计时间: 1天
文件: python/mcp_server.py

新增工具:
- trquant_create_project
- trquant_run_backtest
- trquant_optimize_params
- trquant_get_realtime_data
- trquant_deploy_strategy
- trquant_get_portfolio
- trquant_compare_strategies
```

---

## 🟢 中期任务（下周）

### Task-007: 集成ECharts图表
```
优先级: 🟢 一般
预计时间: 3天
文件: src/views/chartPanel.ts

功能:
- K线图
- 收益曲线
- 回撤曲线
- 因子热力图
```

### Task-008: 参数优化器
```
优先级: 🟢 一般
预计时间: 3天
文件: src/commands/optimizeStrategy.ts

功能:
- 参数空间定义
- 网格搜索
- 并行优化
- 结果可视化
```

### Task-009: 报告导出系统
```
优先级: 🟢 一般
预计时间: 2天
文件: python/tools/report_generator.py

功能:
- HTML报告
- PDF导出
- Excel数据导出
```

---

## 🔵 长期任务（后续版本）

### Task-010: PTrade实盘部署
```
文件: src/commands/deployToPTrade.ts
功能: 一键部署到PTrade客户端
```

### Task-011: QMT实盘部署
```
文件: src/commands/deployToQMT.ts
功能: 一键部署到QMT客户端
```

### Task-012: 实时数据订阅
```
文件: python/data_service.py
功能: WebSocket实时行情推送
```

### Task-013: 多数据源管理
```
文件: src/services/dataService.ts
功能: JQData/AKShare/Baostock统一接口
```

---

## 📁 需要创建的文件清单

### 立即需要
```
(无 - 当前代码已完整，只需编译)
```

### 本周需要
```
src/views/marketTreeView.ts
src/views/mainlinesTreeView.ts  
src/views/strategiesTreeView.ts
```

### 下周需要
```
src/views/chartPanel.ts
src/commands/optimizeStrategy.ts
python/tools/report_generator.py
```

---

## 🎯 执行优先级

```
今天:
  1. Task-001: 编译打包
  2. Task-002: 安装测试

本周:
  3. Task-003: 市场状态TreeView
  4. Task-004: 投资主线TreeView
  5. Task-005: 策略管理TreeView
  6. Task-006: MCP工具扩展

下周:
  7. Task-007: ECharts图表
  8. Task-008: 参数优化器
  9. Task-009: 报告导出
```

---

## ✅ 验收标准

### 今日验收
- [ ] vsix文件成功生成
- [ ] 扩展成功安装到Cursor
- [ ] 侧边栏图标显示
- [ ] 命令面板显示所有TRQuant命令
- [ ] 欢迎界面正常显示

### 本周验收
- [ ] 所有TreeView正常显示
- [ ] MCP工具扩展到12个
- [ ] AI可调用所有工具

### 最终验收
- [ ] 完整QuantConnect式工作流
- [ ] 专业图表可视化
- [ ] 策略优化器可用
- [ ] 报告导出功能

---

*文档版本: v1.0*
*创建日期: 2025-12-03*







