# 适配器使用指南

> **创建时间**: 2025-12-21  
> **主项目路径**: `/home/taotao/dev/QuantTest/TRQuant`

---

## 📋 概述

本文档说明如何在GUI层使用适配器来调用MCP服务，实现功能模块与GUI设计的解耦。

---

## 🎯 使用适配器的优势

1. **版本独立性**: GUI不依赖具体MCP工具名称
2. **向后兼容**: 适配器自动处理版本降级
3. **统一接口**: 所有服务使用相同的调用方式
4. **易于测试**: 可以mock适配器进行单元测试

---

## 📚 TypeScript端（React Webview）

### Tenbagger适配器

```typescript
import { TenbaggerAdapter } from '../adapters/tenbaggerAdapter';
import { MCPClient } from '../services/mcp/client';

// 创建适配器
const mcpClient = new MCPClient();
const adapter = new TenbaggerAdapter(mcpClient);

// 评估股票
const result = await adapter.evaluate({
    symbol: "000001.XSHE",
    name: "平安银行",
    version: "v2"  // 可选，默认v2
});

// 批量评估
const batchResult = await adapter.batchEvaluate({
    symbols: ["000001.XSHE", "000002.XSHE"],
    max_count: 10
});

// 获取排名
const rankings = await adapter.getRankings({
    top_n: 20,
    min_level: "A"
});

// 生成报告
const report = await adapter.generateReport(
    "html",  // format: markdown/json/html
    "A",     // min_level
    undefined, // output_path (可选)
    "v2"     // version (可选)
);
```

### Workflow适配器

```typescript
import { WorkflowAdapter } from '../adapters/workflowAdapter';
import { MCPClient } from '../services/mcp/client';

// 创建适配器
const mcpClient = new MCPClient();
const adapter = new WorkflowAdapter(mcpClient);

// 获取步骤定义
const steps = await adapter.getSteps();

// 创建工作流
const workflow = await adapter.createWorkflow("我的工作流");

// 执行步骤
const result = await adapter.runStep(
    workflow.workflow_id!,
    "data_source",
    {}  // args
);

// 获取状态
const status = await adapter.getStatus(workflow.workflow_id!);

// 执行所有步骤
const allResults = await adapter.runAll(workflow.workflow_id!);
```

---

## 📚 Python端（PyQt6 GUI）

### Tenbagger适配器

```python
from gui.adapters.tenbagger_adapter import get_tenbagger_gui_adapter

# 获取适配器
adapter = get_tenbagger_gui_adapter()

# 评估股票
result = adapter.evaluate(
    symbol="000001.XSHE",
    name="平安银行",
    version="v2"  # 可选
)

# 批量评估
batch_result = adapter.batch_evaluate(
    symbols=["000001.XSHE", "000002.XSHE"],
    max_count=10
)

# 获取排名
rankings = adapter.get_rankings(
    top_n=20,
    min_level="A"
)

# 生成报告
report = adapter.generate_report(
    format="html",
    min_level="A",
    output_path="/path/to/report.html"
)
```

### Workflow适配器

```python
from gui.adapters.workflow_adapter import get_workflow_gui_adapter

# 获取适配器
adapter = get_workflow_gui_adapter()

# 获取步骤定义
steps = adapter.get_steps()

# 创建工作流
workflow = adapter.create_workflow("我的工作流")

# 执行步骤
result = adapter.run_step(
    workflow_id=workflow["workflow_id"],
    step_id="data_source",
    args={}
)

# 获取状态
status = adapter.get_status(workflow["workflow_id"])

# 执行所有步骤
all_results = adapter.run_all(workflow["workflow_id"])
```

---

## 🔄 版本管理

### 获取可用版本

```typescript
// TypeScript
const versions = await adapter.getAvailableVersions();
console.log("可用版本:", versions);
```

```python
# Python
versions = adapter.get_available_versions()
print("可用版本:", versions)
```

### 设置默认版本

```typescript
// TypeScript
adapter.setDefaultVersion("v3");
```

```python
# Python
adapter.set_default_version("v3")
```

---

## ⚠️ 错误处理

适配器会自动处理错误并返回统一的响应格式：

```typescript
const result = await adapter.evaluate({ symbol: "000001.XSHE" });

if (result.success) {
    // 处理成功结果
    console.log(result.report);
} else {
    // 处理错误
    console.error(result.error);
}
```

---

## 📝 最佳实践

1. **使用适配器而非直接调用MCP工具**
   - ✅ `adapter.evaluate({ symbol: "000001.XSHE" })`
   - ❌ `mcpClient.callTool("tenbagger_v2.evaluate", { symbol: "000001.XSHE" })`

2. **处理版本兼容性**
   - 适配器自动处理版本降级
   - 可以指定版本，但通常使用默认版本即可

3. **错误处理**
   - 始终检查 `result.success`
   - 使用 `result.error` 获取错误信息

4. **类型安全**
   - TypeScript适配器提供完整的类型定义
   - Python适配器使用类型注解

---

*文档更新时间: 2025-12-21 16:02*

