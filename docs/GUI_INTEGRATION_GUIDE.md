# GUI 整合指南 - 去重后模块的使用位置

**更新时间**: 2025-12-07  
**状态**: ✅ 去重完成，准备整合

---

## 📍 一、VS Code Extension 中的打开位置

### 1.1 策略管理 (`StrategyVersionControl`)

**打开方式**:
1. **命令面板** (Ctrl+Shift+P / Cmd+Shift+P):
   - 输入: `TRQuant: 打开策略管理`
   - 命令ID: `trquant.openStrategyManager` (需要添加)

2. **侧边栏**:
   - 在 `workflowProvider.ts` 中添加策略管理入口
   - 或创建独立的策略管理面板

3. **主控制台**:
   - 在 `mainDashboard.ts` 中添加策略管理卡片

**当前状态**: 
- ❌ 命令未注册
- ✅ 模块已可用 (`core/strategy_manager.py`)

**需要添加的文件**:
```typescript
// extension/src/views/strategyManagerPanel.ts
// 使用 StrategyVersionControl 管理策略版本
```

---

### 1.2 Broker 管理 (`PTradeBroker`, `QMTBroker`)

**打开方式**:
1. **命令面板**:
   - 输入: `TRQuant: 打开券商管理`
   - 命令ID: `trquant.openBrokerManager` (需要添加)

2. **工作流步骤面板**:
   - 在 `workflowStepPanel.ts` 中的 `trading-center` 步骤
   - 命令ID: `trquant.openTradingCenter` (已注册)

3. **主控制台**:
   - 在 `mainDashboard.ts` 中添加 Broker 状态卡片

**当前状态**:
- ✅ 工作流步骤已注册 (`trquant.openTradingCenter`)
- ✅ 模块已可用 (`core/broker/ptrade_broker.py`, `core/broker/qmt_broker.py`)

**现有集成点**:
```typescript
// extension/src/views/workflowStepPanel.ts (行 2380)
{ id: 'trquant.openTradingCenter', step: 'trading-center' }
```

---

### 1.3 数据中心 (`DataCenter`)

**打开方式**:
1. **命令面板**:
   - 输入: `TRQuant: 打开数据中心`
   - 命令ID: `trquant.openDataCenter` (已注册)

2. **工作流步骤面板**:
   - 在 `workflowStepPanel.ts` 中的 `data-center` 步骤
   - 命令ID: `trquant.openDataCenter` (已注册)

3. **主控制台**:
   - 在 `mainDashboard.ts` 中添加数据源状态卡片

**当前状态**:
- ✅ 命令已注册 (`trquant.openDataCenter`)
- ✅ 模块已可用 (`core/data_center.py`)

**现有集成点**:
```typescript
// extension/src/views/workflowStepPanel.ts (行 2373)
{ id: 'trquant.openDataCenter', step: 'data-center' }
```

---

### 1.4 A股工具 (`AShareTradingRules`)

**打开方式**:
1. **命令面板**:
   - 输入: `TRQuant: 打开A股工具`
   - 命令ID: `trquant.openAShareTools` (需要添加)

2. **工作流步骤面板**:
   - 在 `workflowStepPanel.ts` 中的相关步骤
   - 或在策略开发步骤中使用

**当前状态**:
- ❌ 命令未注册
- ✅ 模块已可用 (`utils/a_share_tools.py`)

**需要添加的文件**:
```typescript
// extension/src/views/ashareToolsPanel.ts
// 使用 AShareTradingRules 等工具类
```

---

### 1.5 AI 助手 (`AIAssistant`)

**打开方式**:
1. **命令面板**:
   - 输入: `TRQuant: 打开AI助手`
   - 命令ID: `trquant.openAIAssistant` (需要添加)

2. **策略优化器**:
   - 在 `strategyOptimizerPanel.ts` 中已集成
   - 命令ID: `trquant.optimizeStrategy` (已注册)

3. **主控制台**:
   - 在 `mainDashboard.ts` 中添加 AI 助手卡片

**当前状态**:
- ✅ 策略优化器已集成 (`trquant.optimizeStrategy`)
- ✅ 模块已可用 (`utils/ai_assistant.py`)

**现有集成点**:
```typescript
// extension/src/views/strategyOptimizerPanel.ts
// 已使用 AIAssistant 进行策略优化
```

---

## 📍 二、PyQt6 GUI 中的打开位置

### 2.1 策略管理

**文件位置**: `gui/widgets/strategy_manager_panel.py`

**打开方式**:
1. **主窗口菜单**: 工具 → 策略管理
2. **侧边栏**: 策略管理标签页
3. **快捷键**: Ctrl+S (如果配置)

**当前状态**:
- ✅ 文件已存在 (`gui/widgets/strategy_manager_panel.py`)
- ✅ 模块已可用 (`core/strategy_manager.py`)

---

### 2.2 Broker 管理

**文件位置**: `gui/widgets/trading_panel.py`

**打开方式**:
1. **主窗口菜单**: 交易 → Broker 管理
2. **侧边栏**: 交易标签页
3. **工作流面板**: 交易中心步骤

**当前状态**:
- ✅ 文件已存在 (`gui/widgets/trading_panel.py`)
- ✅ 模块已可用 (`core/broker/ptrade_broker.py`, `core/broker/qmt_broker.py`)

---

### 2.3 数据中心

**文件位置**: `gui/widgets/data_source_panel.py`, `gui/widgets/data_manager_panel.py`

**打开方式**:
1. **主窗口菜单**: 数据 → 数据源管理
2. **侧边栏**: 数据管理标签页
3. **工作流面板**: 数据源步骤

**当前状态**:
- ✅ 文件已存在 (`gui/widgets/data_source_panel.py`)
- ✅ 模块已可用 (`core/data_center.py`)

---

### 2.4 A股工具

**文件位置**: `gui/widgets/` (可能需要创建新组件)

**打开方式**:
1. **主窗口菜单**: 工具 → A股工具
2. **侧边栏**: 工具标签页

**当前状态**:
- ⚠️ 可能需要创建新组件
- ✅ 模块已可用 (`utils/a_share_tools.py`)

---

### 2.5 AI 助手

**文件位置**: `gui/widgets/ai_assistant_panel.py`

**打开方式**:
1. **主窗口菜单**: 工具 → AI 助手
2. **侧边栏**: AI 助手标签页
3. **策略开发面板**: 集成在策略开发流程中

**当前状态**:
- ✅ 文件已存在 (`gui/widgets/ai_assistant_panel.py`)
- ✅ 模块已可用 (`utils/ai_assistant.py`)

---

## 🚀 三、快速打开方式总结

### VS Code Extension

| 功能 | 命令 | 快捷键 | 状态 |
|------|------|--------|------|
| 策略管理 | `trquant.openStrategyManager` | - | ❌ 需添加 |
| Broker 管理 | `trquant.openTradingCenter` | - | ✅ 已注册 |
| 数据中心 | `trquant.openDataCenter` | - | ✅ 已注册 |
| A股工具 | `trquant.openAShareTools` | - | ❌ 需添加 |
| AI 助手 | `trquant.optimizeStrategy` | - | ✅ 已注册 |
| 主控制台 | `trquant.openDashboard` | - | ✅ 已注册 |

### PyQt6 GUI

| 功能 | 菜单路径 | 文件位置 | 状态 |
|------|---------|---------|------|
| 策略管理 | 工具 → 策略管理 | `gui/widgets/strategy_manager_panel.py` | ✅ 已存在 |
| Broker 管理 | 交易 → Broker 管理 | `gui/widgets/trading_panel.py` | ✅ 已存在 |
| 数据中心 | 数据 → 数据源管理 | `gui/widgets/data_source_panel.py` | ✅ 已存在 |
| A股工具 | 工具 → A股工具 | - | ⚠️ 需创建 |
| AI 助手 | 工具 → AI 助手 | `gui/widgets/ai_assistant_panel.py` | ✅ 已存在 |

---

## 📝 四、需要添加的集成点

### 4.1 VS Code Extension

1. **策略管理面板** (`extension/src/views/strategyManagerPanel.ts`)
   ```typescript
   // 使用 StrategyVersionControl
   import { StrategyVersionControl } from '../../../core/strategy_manager';
   ```

2. **A股工具面板** (`extension/src/views/ashareToolsPanel.ts`)
   ```typescript
   // 使用 AShareTradingRules
   import { AShareTradingRules } from '../../../utils/a_share_tools';
   ```

3. **Broker 管理面板** (`extension/src/views/brokerManagerPanel.ts`)
   ```typescript
   // 使用 PTradeBroker, QMTBroker
   import { PTradeBroker } from '../../../core/broker/ptrade_broker';
   import { QMTBroker } from '../../../core/broker/qmt_broker';
   ```

### 4.2 命令注册

在 `extension/src/extension.ts` 的 `registerCommands` 函数中添加:

```typescript
{
  id: 'trquant.openStrategyManager',
  handler: async () => {
    const { StrategyManagerPanel } = await import('./views/strategyManagerPanel');
    StrategyManagerPanel.createOrShow(context.extensionUri, client);
  },
},
{
  id: 'trquant.openAShareTools',
  handler: async () => {
    const { AShareToolsPanel } = await import('./views/ashareToolsPanel');
    AShareToolsPanel.createOrShow(context.extensionUri, client);
  },
},
{
  id: 'trquant.openBrokerManager',
  handler: async () => {
    const { BrokerManagerPanel } = await import('./views/brokerManagerPanel');
    BrokerManagerPanel.createOrShow(context.extensionUri, client);
  },
},
```

---

## 🎯 五、推荐打开流程

### 对于策略管理:
1. **VS Code**: `Ctrl+Shift+P` → `TRQuant: 打开策略管理` (需添加)
2. **PyQt6**: 主窗口 → 工具 → 策略管理

### 对于 Broker 管理:
1. **VS Code**: `Ctrl+Shift+P` → `TRQuant: 打开交易中心`
2. **PyQt6**: 主窗口 → 交易 → Broker 管理

### 对于数据中心:
1. **VS Code**: `Ctrl+Shift+P` → `TRQuant: 打开数据中心`
2. **PyQt6**: 主窗口 → 数据 → 数据源管理

### 对于 AI 助手:
1. **VS Code**: `Ctrl+Shift+P` → `TRQuant: 优化策略`
2. **PyQt6**: 主窗口 → 工具 → AI 助手

---

## ✅ 六、当前可用功能

### 立即可用 (无需修改):
- ✅ 数据中心: `trquant.openDataCenter`
- ✅ Broker 管理: `trquant.openTradingCenter`
- ✅ AI 助手: `trquant.optimizeStrategy`
- ✅ 主控制台: `trquant.openDashboard`

### 需要添加:
- ❌ 策略管理面板 (`trquant.openStrategyManager`)
- ❌ A股工具面板 (`trquant.openAShareTools`)
- ❌ Broker 管理独立面板 (`trquant.openBrokerManager`)

---

**总结**: 大部分功能已集成，只需添加策略管理和A股工具的面板即可完整使用所有去重后的模块。



