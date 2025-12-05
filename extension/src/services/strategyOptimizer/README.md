# 策略优化器服务架构文档

## 📋 概述

策略优化器是 TRQuant Extension 的核心服务之一，提供策略代码分析、优化建议、平台转换等功能。

## 🏗️ 架构结构

```
strategyOptimizer/
├── index.ts                    # 主入口，StrategyOptimizerService 单例
├── types.ts                    # 类型定义
├── analyzer/                   # 分析器模块
│   ├── index.ts               # 分析器导出
│   ├── codeAnalyzer.ts        # 代码分析器（旧版）
│   ├── strategyAnalyzer.ts    # 策略分析器（新版，深度分析）
│   └── optimizationAdvisor.ts # 优化建议生成器
├── adapters/                   # 平台适配器
│   └── platformAdapter.ts     # 平台转换适配器
├── generator/                  # 报告生成器
│   └── reportGenerator.ts     # 报告生成器
└── learner/                    # 学习引擎
    ├── index.ts               # 学习器导出
    ├── strategyLearner.ts     # 策略学习器
    ├── manualLearner.ts       # 手册学习器
    └── knowledgeStore.ts     # 知识库存储
```

## 🔧 核心组件

### 1. StrategyOptimizerService（主服务类）

**位置**: `index.ts`

**功能**:
- 单例模式，统一管理所有子模块
- 提供策略分析、优化、转换、报告生成等核心功能
- 整合学习引擎和知识库

**主要方法**:
- `analyzeStrategy(code, filename)` - 分析策略代码（旧版）
- `analyzeStrategyDeep(code, fileName)` - 深度分析策略（新版）
- `generateOptimizationReport(code, fileName)` - 生成优化报告
- `convertToPlatform(code, targetPlatform)` - 平台转换
- `optimizeStrategy(code, targetPlatform)` - 一键优化
- `getStrategyScore(code)` - 获取策略评分
- `quickOptimizationCheck(code)` - 快速优化检查

### 2. StrategyAnalyzer（策略分析器）

**位置**: `analyzer/strategyAnalyzer.ts`

**功能**:
- 深度分析策略代码
- 提取因子、风控、选股、交易等信息
- 检测策略问题

**输出**: `StrategyAnalysis` 接口
```typescript
{
    name: string;
    platform: 'ptrade' | 'qmt' | 'joinquant' | 'unknown';
    factors: FactorInfo[];
    riskControl: RiskControlInfo;
    stockSelection: StockSelectionInfo;
    trading: TradingInfo;
    issues: StrategyIssue[];
}
```

### 3. OptimizationAdvisor（优化建议生成器）

**位置**: `analyzer/optimizationAdvisor.ts`

**功能**:
- 基于分析结果生成优化建议
- 从知识库获取最佳实践
- 计算策略评分

**输出**: `OptimizationReport` 接口
```typescript
{
    strategyName: string;
    platform: string;
    overallScore: number;  // 0-100
    scoreBreakdown: {
        risk: number;
        factor: number;
        selection: number;
        code: number;
    };
    advices: OptimizationAdvice[];
    summary: string;
}
```

### 4. PlatformAdapter（平台适配器）

**位置**: `adapters/platformAdapter.ts`

**功能**:
- 在不同平台间转换策略代码
- 支持 JoinQuant ↔ PTrade ↔ QMT
- API 映射和参数转换

### 5. ReportGenerator（报告生成器）

**位置**: `generator/reportGenerator.ts`

**功能**:
- 生成 JSON/Markdown/HTML 格式报告
- 包含投资理念、代码架构、兼容性分析等

### 6. Learner（学习引擎）

**位置**: `learner/`

**功能**:
- 从文档和历史策略学习
- 提取成功模式和最佳实践
- 知识库存储和管理

## 📦 导出接口

### 主服务
```typescript
import { strategyOptimizer, StrategyOptimizerService } from './services/strategyOptimizer';
```

### 子模块
```typescript
import { codeAnalyzer } from './services/strategyOptimizer';
import { platformAdapter } from './services/strategyOptimizer';
import { reportGenerator } from './services/strategyOptimizer';
import { createStrategyAnalyzer, StrategyAnalyzer } from './services/strategyOptimizer';
import { createOptimizationAdvisor, OptimizationAdvisor } from './services/strategyOptimizer';
```

### 类型
```typescript
import {
    StrategyAnalysis,
    OptimizationReport,
    OptimizationAdvice,
    FactorInfo,
    RiskControlInfo,
    // ... 更多类型
} from './services/strategyOptimizer';
```

## 🔍 使用示例

### 1. 分析策略
```typescript
const optimizer = strategyOptimizer;
const analysis = optimizer.analyzeStrategyDeep(code, 'my_strategy.py');
console.log('因子数量:', analysis.factors.length);
console.log('风控参数:', analysis.riskControl);
```

### 2. 生成优化报告
```typescript
const report = optimizer.generateOptimizationReport(code, 'my_strategy.py');
console.log('总体评分:', report.overallScore);
console.log('优化建议:', report.advices);
```

### 3. 平台转换
```typescript
const result = optimizer.convertToPlatform(code, 'ptrade');
if (result.success) {
    console.log('转换后的代码:', result.convertedCode);
}
```

### 4. 获取策略评分
```typescript
const score = optimizer.getStrategyScore(code);
console.log('风险评分:', score.risk);
console.log('因子评分:', score.factor);
```

## ⚠️ 当前状态

### ✅ 已完成
- [x] 策略分析器（深度分析）
- [x] 优化建议生成器
- [x] 平台适配器（基础）
- [x] 报告生成器
- [x] 学习引擎框架
- [x] 类型定义完整

### ⚠️ 待完善
- [ ] `registerStrategyOptimizer` 函数缺失（在 extension.ts 中被注释）
- [ ] 知识库集成（当前未完全集成）
- [ ] 手册学习器初始化（需要手动路径）
- [ ] 部分 API 映射需要补充

### 🔧 需要补充的功能

1. **注册函数**
   - 需要在 `index.ts` 或单独文件中添加 `registerStrategyOptimizer` 函数
   - 用于在 extension.ts 中注册命令和服务

2. **初始化逻辑**
   - 学习引擎的初始化路径配置
   - 知识库存储路径配置

3. **集成测试**
   - 各模块的单元测试
   - 端到端测试

## 📝 下一步开发建议

1. **补充注册函数**
   ```typescript
   export function registerStrategyOptimizer(
       context: vscode.ExtensionContext,
       client: TRQuantClient
   ): void {
       // 注册命令
       // 初始化服务
       // 设置存储路径
   }
   ```

2. **完善知识库集成**
   - 自动加载知识库
   - 从历史策略学习
   - 用户反馈收集

3. **增强平台转换**
   - 补充更多 API 映射
   - 处理复杂场景
   - 错误处理优化

4. **优化建议增强**
   - 基于回测结果的建议
   - 市场状态适配建议
   - 个性化优化建议

