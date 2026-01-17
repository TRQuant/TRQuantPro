# 策略优化模块

根据《策略优化模块设计方案》实现的策略自动优化功能。

## 📋 模块概述

策略优化模块作为八步投资流程中的关键环节，负责将策略从验证阶段进一步打磨优化，确保最终提交实盘的是经过迭代改进和验证的稳健策略。

## 🏗️ 架构组成

### 1. 优化决策引擎 (`StrategyOptimizationEngine`)

核心组件，根据评估结果决定如何调整策略。

**位置**: `optimizer/index.ts`

**功能**:
- 管理多种优化算法
- 协调回测、分析、版本管理等组件
- 提供统一的优化接口

### 2. 优化算法 (`algorithms/`)

支持多种优化算法：

- ✅ **网格搜索** (`gridSearch.ts`): 穷举法遍历参数空间
- ✅ **随机搜索** (`randomSearch.ts`): 随机采样参数组合
- ⏳ **贝叶斯优化**: 智能选择参数测试（待实现）
- ⏳ **遗传算法**: 进化算法优化（待实现）
- ⏳ **强化学习**: 深度强化学习优化（待实现）

### 3. 回测接口组件 (`backtest/`)

与回测系统对接，批量提交候选策略方案。

**位置**: `backtest/backtestInterface.ts`

**功能**:
- 执行单个回测
- 批量回测（支持并行）
- 任务状态查询

### 4. 结果分析与记录组件 (`analyzer/`)

收集、对比、记录优化结果。

**位置**: `analyzer/resultAnalyzer.ts`

**功能**:
- 分析回测结果（优势、劣势、风险、建议）
- 对比不同策略版本
- 生成优化报告

### 5. 版本管理 (待实现)

管理策略版本，支持版本对比和回滚。

### 6. AI辅助 (待实现)

使用AI辅助改写策略逻辑。

## 📊 类型定义

所有类型定义在 `types.ts` 中：

- `OptimizationConfig`: 优化配置
- `StrategyConfig`: 策略配置
- `OptimizationTarget`: 优化目标
- `BacktestResult`: 回测结果
- `OptimizationResult`: 优化结果
- `OptimizationProgress`: 优化进度

## 🚀 使用示例

```typescript
import { getOptimizationEngine } from './optimizer';
import { GridSearchAlgorithm } from './optimizer/algorithms';

// 获取优化引擎
const engine = getOptimizationEngine();

// 注册算法
engine.registerAlgorithm('grid_search', new GridSearchAlgorithm());

// 设置回测接口
engine.setBacktestInterface(new BacktestInterfaceImpl(client));

// 设置结果分析器
engine.setResultAnalyzer(new ResultAnalyzerImpl());

// 执行优化
const result = await engine.optimize(
    strategyConfig,
    optimizationConfig,
    target,
    context,
    (progress) => {
        console.log(`进度: ${progress.currentIteration}/${progress.totalIterations}`);
    }
);
```

## 📝 待实现功能

根据设计方案，以下功能待实现：

1. **优化算法**:
   - [ ] 贝叶斯优化
   - [ ] 遗传算法
   - [ ] 强化学习
   - [ ] 模拟退火
   - [ ] 粒子群优化

2. **版本管理**:
   - [ ] 版本保存和查询
   - [ ] 版本对比
   - [ ] 版本回滚

3. **AI辅助**:
   - [ ] AI策略改写
   - [ ] 自然语言解释生成
   - [ ] 代码质量检查

4. **可视化**:
   - [ ] 参数空间图谱
   - [ ] 优化迭代曲线
   - [ ] 绩效对比图

5. **协同机制**:
   - [ ] 与策略模板协同
   - [ ] 与数据模块协同
   - [ ] 与主线模块协同

6. **防过拟合**:
   - [ ] Walk-Forward分析
   - [ ] 样本外验证
   - [ ] 稳健性度量

## 🔗 相关文档

- [策略优化模块设计方案](../../../docs/03_modules/策略优化模块设计方案.pdf)
- [策略优化器服务架构文档](../README.md)























