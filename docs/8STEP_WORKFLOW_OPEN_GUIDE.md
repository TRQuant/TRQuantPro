# 8步骤投资工作流打开指南

**更新时间**: 2025-12-07

---

## 📍 8步骤工作流的打开位置

### ✅ 方式 1: 侧边栏树视图（推荐）

**位置**: VS Code 左侧活动栏 → `TRQuant 工作流` 视图

**打开步骤**:
1. 在 VS Code 左侧活动栏找到 `TRQuant 工作流` 图标
2. 展开可以看到 8 个步骤：
   - 📡 1. 数据中心
   - 📈 2. 市场分析
   - 🔥 3. 投资主线
   - 📦 4. 候选池
   - 📊 5. 因子中心
   - 🛠️ 6. 策略开发
   - 🔄 7. 回测中心
   - 🚀 8. 交易中心
3. 点击任意步骤即可打开对应的详细面板

**视图ID**: `trquant-workflow`  
**注册位置**: `extension/src/providers/workflowProvider.ts` (行 340)

---

### ✅ 方式 2: 主控制台（Dashboard）

**位置**: 主控制台面板

**打开步骤**:
1. 命令面板: `Ctrl+Shift+P` → `TRQuant: 量化工作台`
2. 在主控制台中可以看到 8 步骤工作流的快捷入口
3. 点击任意步骤卡片即可打开

**命令ID**: `trquant.openDashboard`  
**文件位置**: `extension/src/views/mainDashboard.ts`

---

### ✅ 方式 3: 命令面板直接打开

**打开步骤**:
1. 按 `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)
2. 输入对应的命令：

| 步骤 | 命令 | 命令ID |
|------|------|--------|
| 1. 数据中心 | `TRQuant: 📡 数据中心 (步骤1)` | `trquant.openDataCenter` |
| 2. 市场分析 | `TRQuant: 📈 市场趋势 (步骤2)` | `trquant.openMarketAnalysis` |
| 3. 投资主线 | `TRQuant: 🔥 投资主线 (步骤3)` | `trquant.openMainlines` |
| 4. 候选池 | `TRQuant: 📦 候选池 (步骤4)` | `trquant.openCandidatePool` |
| 5. 因子中心 | `TRQuant: 📊 因子构建 (步骤5)` | `trquant.openFactorCenter` |
| 6. 策略开发 | `TRQuant: 🛠️ 策略开发 (步骤6)` | `trquant.openStrategyDev` |
| 7. 回测中心 | `TRQuant: 🔄 回测验证 (步骤7)` | `trquant.openBacktestCenter` |
| 8. 交易中心 | `TRQuant: 🚀 实盘交易 (步骤8)` | `trquant.openTradingCenter` |

**注册位置**: `extension/src/views/workflowStepPanel.ts` (行 2372-2380)

---

### ✅ 方式 4: 桌面系统（完整版）

**打开步骤**:
1. 命令面板: `Ctrl+Shift+P` → `TRQuant: 🖥️ 打开桌面系统（完整工作流）`
2. 或: `TRQuant: 🐉 韬睿量化桌面系统`

**命令ID**: 
- `trquant.openWorkflowPanel` (启动桌面系统)
- `trquant.launchDesktopSystem` (启动桌面系统)

**说明**: 这会启动 PyQt6 桌面系统，包含完整的 8 步骤工作流界面

---

### ✅ 方式 5: WebView 简化版（6步骤）

**打开步骤**:
1. 命令面板: `Ctrl+Shift+P` → `TRQuant: 🖥️ 打开桌面系统（WebView版）`

**命令ID**: `trquant.openWorkflowPanelWebview`

**说明**: 这是在 VS Code 中打开的简化版工作流面板（6步骤，与桌面系统一致）

---

## 🔗 8步骤与去重后模块的对应关系

| 步骤 | 模块 | 打开命令 | 状态 |
|------|------|---------|------|
| 1. 数据中心 | `DataCenter` | `trquant.openDataCenter` | ✅ 已集成 |
| 2. 市场分析 | - | `trquant.openMarketAnalysis` | ✅ 已注册 |
| 3. 投资主线 | - | `trquant.openMainlines` | ✅ 已注册 |
| 4. 候选池 | - | `trquant.openCandidatePool` | ✅ 已注册 |
| 5. 因子中心 | - | `trquant.openFactorCenter` | ✅ 已注册 |
| 6. 策略开发 | `StrategyVersionControl` | `trquant.openStrategyDev` | ✅ 已注册 |
| 7. 回测中心 | - | `trquant.openBacktestCenter` | ✅ 已注册 |
| 8. 交易中心 | `PTradeBroker`, `QMTBroker` | `trquant.openTradingCenter` | ✅ 已集成 |

---

## 🎯 推荐使用方式

### 日常使用:
1. **侧边栏树视图** - 最直观，可以展开查看子功能
2. **主控制台** - 适合快速访问和查看整体状态

### 快速操作:
1. **命令面板** - 直接输入步骤名称快速打开

### 完整功能:
1. **桌面系统** - 启动 PyQt6 GUI，包含所有完整功能

---

## 📝 代码位置总结

### 侧边栏树视图:
- **注册**: `extension/src/providers/workflowProvider.ts` (行 337)
- **视图ID**: `trquant-workflow`
- **8步骤定义**: 行 33-275

### 步骤面板:
- **注册**: `extension/src/views/workflowStepPanel.ts` (行 2367)
- **8个命令**: 行 2372-2380
- **面板实现**: `WorkflowStepPanel` 类

### 主控制台:
- **文件**: `extension/src/views/mainDashboard.ts`
- **8步骤入口**: 行 120-129
- **一键执行**: 行 396-421

---

## ✅ 验证方法

### 检查侧边栏是否显示:
1. 打开 VS Code
2. 查看左侧活动栏是否有 `TRQuant 工作流` 视图
3. 如果没有，检查 `package.json` 中的 `views` 配置

### 检查命令是否注册:
1. 按 `Ctrl+Shift+P`
2. 输入 `TRQuant:`
3. 应该能看到所有 8 个步骤的命令

---

**总结**: 8步骤工作流可以通过**侧边栏树视图**、**主控制台**、**命令面板**或**桌面系统**打开。所有命令已注册，可以直接使用。




