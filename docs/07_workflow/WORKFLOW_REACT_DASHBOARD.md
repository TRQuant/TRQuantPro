# React仪表盘9步投资工作流实现文档

> 创建时间: 2025-12-22  
> 状态: 开发完成，待测试

---

## 📋 功能概述

实现了React仪表盘的9步投资工作流功能，包括：

1. **状态展示**：每个步骤的运行状态（运行中/成功/失败）
2. **数据源检查详情**：显示每个数据源的具体状态（JQData/AKShare/Tushare）
3. **结果详情面板**：可展开查看每个步骤的详细执行结果

---

## 🎨 UI组件

### 1. DataSourceStatus组件

**位置**: `extension/webview-ui/src/components/DataSourceStatus.tsx`

**功能**：
- 显示数据源健康检查的详细结果
- 展示每个数据源的状态、延迟、成功率、错误次数等
- 统计信息：可用数据源数量、可用率、检查方法

**数据格式**：
```typescript
interface DataSourceStatus {
  available: boolean;
  latency_ms?: number;
  last_check?: string;
  error_count?: number;
  success_rate?: number;
  error?: string;
  message?: string;
}

interface DataSourceHealthStatus {
  [key: string]: DataSourceStatus;  // key: jqdata, akshare, tushare
}
```

**显示内容**：
- 数据源名称（聚宽数据/AKShare/Tushare）
- 状态标签（可用/不可用）
- 延迟（ms，颜色编码：<100ms绿色，<500ms黄色，>500ms红色）
- 成功率（%，颜色编码：≥95%绿色，≥80%黄色，<80%红色）
- 错误次数
- 最后检查时间
- 备注信息（成功消息或错误信息）

### 2. Workflow页面改进

**位置**: `extension/webview-ui/src/pages/Workflow.tsx`

**改进内容**：

#### 2.1 步骤状态可视化
- 使用Ant Design Steps组件显示9个步骤
- 状态图标：
  - 运行中：`LoadingOutlined`（蓝色）
  - 成功：`CheckCircleOutlined`（绿色）
  - 失败：`CloseCircleOutlined`（红色）
  - 未执行：无图标（灰色）

#### 2.2 步骤按钮
- 每个步骤有独立的执行按钮
- 按钮状态：
  - 运行中：显示loading图标
  - 成功：显示绿色对勾
  - 失败：显示红色错误图标，按钮为danger类型
  - 未执行：显示播放图标

#### 2.3 结果详情面板
- 使用Collapse组件，可展开查看每个步骤的详细结果
- 数据源检查步骤（步骤1）：
  - 使用DataSourceStatus组件显示详细的数据源状态
  - 显示检查方法、摘要信息
  - 如有错误，显示错误信息Alert
- 其他步骤：
  - 使用Descriptions组件显示结构化信息
  - 显示状态、摘要、执行方法、错误信息等
  - 完整结果数据以JSON格式展示（可折叠）

---

## 🔄 数据流

### 1. 步骤执行流程

```
用户点击步骤按钮
  ↓
runWorkflowStep(step)
  ↓
callMCP('workflow9.run_step', { workflow_id, step_id })
  ↓
后端执行步骤（workflow_9steps_server.py）
  ↓
返回结果：{ success, step_id, step_result }
  ↓
更新store：stepResults[step] = result
  ↓
UI更新：显示状态和结果
```

### 2. 数据源检查特殊处理

数据源检查步骤返回的数据结构：
```json
{
  "success": true,
  "step_id": "data_source",
  "step_result": {
    "success": true,
    "health_status": {
      "jqdata": {
        "available": true,
        "latency_ms": 123.45,
        "last_check": "2025-12-22T...",
        "error_count": 0,
        "success_rate": 100.0
      },
      "akshare": {...},
      "tushare": {...}
    },
    "summary": "数据源检查完成（直接导入函数）",
    "method": "direct_import",
    "available_count": 2,
    "total_count": 3
  }
}
```

---

## 📁 文件结构

```
extension/webview-ui/
├── src/
│   ├── components/
│   │   └── DataSourceStatus.tsx      # 数据源状态组件（新增）
│   ├── pages/
│   │   └── Workflow.tsx               # 工作流页面（改进）
│   └── store/
│       └── index.ts                   # 状态管理（更新）
```

---

## 🎯 9步工作流定义

| 步骤 | step_id | 名称 | MCP工具 | 描述 |
|------|---------|------|---------|------|
| 1 | data_source | 信息获取 | data_source.health_check | 检查数据源连接状态 |
| 2 | market_trend | 市场趋势 | market.status | 分析当前市场状态 |
| 3 | mainline | 投资主线 | market.mainlines | 识别投资主线 |
| 4 | candidate_pool | 候选池构建 | data_source.candidate_pool | 构建候选股票池 |
| 5 | factor | 因子构建 | factor.recommend | 推荐量化因子 |
| 6 | strategy | 策略生成 | template.generate | 生成策略代码 |
| 7 | backtest | 回测验证 | backtest.quick | 执行回测验证 |
| 8 | optimization | 策略优化 | optimizer.grid_search | 参数优化 |
| 9 | report | 报告生成 | report.generate | 生成研究报告 |

---

## ✅ 已完成功能

- [x] 创建DataSourceStatus组件
- [x] 改进Workflow页面状态展示
- [x] 添加结果详情面板
- [x] 数据源检查步骤特殊处理
- [x] 更新store以支持详细结果数据
- [x] 错误处理和显示

---

## 🧪 测试建议

1. **数据源检查测试**：
   - 点击步骤1，查看数据源状态是否正确显示
   - 验证每个数据源的状态、延迟、成功率等信息
   - 测试错误情况下的显示

2. **状态展示测试**：
   - 依次执行各个步骤，验证状态图标和按钮状态
   - 验证成功/失败状态的正确显示

3. **结果详情测试**：
   - 展开各个步骤的结果面板
   - 验证数据源检查步骤的特殊展示
   - 验证其他步骤的通用展示

4. **错误处理测试**：
   - 模拟网络错误
   - 模拟步骤执行失败
   - 验证错误信息的正确显示

---

## 📝 后续优化建议

1. **性能优化**：
   - 结果数据量大时，考虑虚拟滚动
   - 添加结果缓存机制

2. **用户体验**：
   - 添加步骤执行进度条
   - 添加步骤执行时间显示
   - 支持批量执行步骤

3. **功能扩展**：
   - 支持步骤依赖关系检查
   - 支持步骤重试
   - 支持步骤结果导出

---

*创建时间: 2025-12-22*



























































