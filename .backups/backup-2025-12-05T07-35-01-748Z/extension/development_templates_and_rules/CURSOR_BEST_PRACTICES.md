# Cursor + Claude Opus 4.5 开发最佳实践

> **基于深度研究和TRQuant项目实践**

本文档结合了《深度研究：使用 Cursor 编辑器和 Claude Opus 4.5 开发复杂项目的最佳实践》的研究成果和TRQuant项目的实际经验，制定了一套完整的开发规则和最佳实践。

---

## 📋 目录

1. [项目规划与上下文管理](#项目规划与上下文管理)
2. [Token成本控制策略](#token成本控制策略)
3. [代码生成与质量保证](#代码生成与质量保证)
4. [模块化开发原则](#模块化开发原则)
5. [上下文缓存机制](#上下文缓存机制)
6. [结构化提示模板](#结构化提示模板)

---

## 项目规划与上下文管理

### 1. 单一事实源（Single Source of Truth）

**原则**：项目必须有一个权威的架构文档作为"黄金标准"。

**实践**：
- ✅ **PROJECT_BRIEF.md** 作为项目架构的单一事实源
- ✅ **MODULE_INDEX.md** 记录所有模块的职责和接口
- ✅ **DECISIONS.md** 记录所有架构决策
- ✅ 所有新功能开发前，先更新或引用这些文档

**操作流程**：
```
1. 新功能开发前 → 查阅 PROJECT_BRIEF.md 和 MODULE_INDEX.md
2. 确认模块位置 → 询问AI "该文件位置是否符合架构设计？"
3. 更新文档 → 功能完成后更新相关文档
4. 验证一致性 → 让AI对照文档验证实现
```

### 2. 上下文重建机制

**问题**：Cursor对话历史无法在会话间永久保存，导致上下文丢失。

**解决方案**：

#### 方案A：主动提供项目概要
每次新对话开始时，提供：
```markdown
项目：TRQuant Cursor Extension
架构：VS Code Extension + Python Bridge
主要模块：
- commands/ - 用户命令
- services/ - 核心服务（TRQuantClient, StrategyOptimizer等）
- views/ - WebView面板
- providers/ - TreeView提供者
当前任务：[具体任务描述]
相关文件：[列出相关文件路径]
```

#### 方案B：使用Cursor内存文件
- 利用Cursor Claude 4的"内存文件"功能
- 定期让AI总结项目状态写入备忘文档
- 在`development_templates_and_rules/`目录维护项目状态快照

#### 方案C：文档引用
在提示中明确引用：
```
请参考 extension/development_templates_and_rules/PROJECT_BRIEF.md
当前项目架构为：VS Code Extension + Python Bridge
```

### 3. 避免上下文遗失

**关键实践**：
- ✅ 重要讨论内容保存到文档（更新README或注释）
- ✅ 架构决策记录到`DECISIONS.md`
- ✅ 模块接口变更更新`MODULE_INDEX.md`
- ✅ 定期生成项目状态快照

**禁止行为**：
- ❌ 依赖对话历史作为唯一信息源
- ❌ 在对话中做出重要决策但不记录
- ❌ 让AI凭空猜测项目结构

---

## Token成本控制策略

### 1. 上下文缓存与重用

**问题**：重复分析代码库导致Token浪费（分析→编写→验证，同一上下文被分析3次）

**解决方案**：

#### 实现上下文缓存
```typescript
// 缓存结构示例
interface ContextCache {
    id: string;
    timestamp: string;
    analysis: {
        fileDependencies: string[];
        architecturePoints: string[];
        testPlan: string[];
    };
    relatedFiles: string[];
}

// 使用缓存
// 首次分析
const cache = await analyzeContext(files);
saveCache('feature-x', cache);

// 后续步骤复用
const cached = loadCache('feature-x');
prompt = `请使用缓存上下文（ID: feature-x），勿重复分析已知部分。
已知信息：${cached.analysis}
现在请实现功能...`;
```

**预期效果**：
- 后续步骤减少约30%的上下文Token
- 每个功能总体Token消耗降低约20%

#### 缓存管理
- 缓存位置：`extension/.cursor/cache/`
- 缓存格式：JSON文件
- 缓存清理：定期清理过期缓存（>7天）

### 2. 精简上下文与结构化提示

**原则**：只提供任务相关的必要文件，避免全量上下文。

**实践**：

#### 文件选择策略
```
❌ 错误：让Cursor自动选择所有文件
✅ 正确：手动指定相关文件
  - 编辑函数 → 只提供该文件和接口定义
  - 添加功能 → 提供相关模块和依赖
  - 修复Bug → 提供问题文件和测试文件
```

#### 结构化提示模板
使用`TASK_TEMPLATE.md`中的模板，包含：
- **任务**：明确描述
- **背景**：相关代码和上下文
- **要求**：具体验收标准
- **约束**：技术限制
- **输出**：期望格式

**示例**：
```
任务：在StrategyOptimizer中添加新的API映射规则

背景：
- 文件：extension/src/services/strategyOptimizer/adapters/platformAdapter.ts
- 当前已有映射：get_price → get_history
- 需要添加：get_fundamentals → get_financial_data

要求：
- 遵循现有映射格式
- 添加参数转换逻辑
- 更新API_MAPPINGS数组
- 添加单元测试

约束：
- 不得修改现有映射
- 必须保持向后兼容

输出：
- 修改后的platformAdapter.ts代码片段
- 新增的测试用例
```

### 3. 上下文分块与渐进提供

**策略**：将长任务拆分为逻辑块，分块处理。

**流程**：
```
100K Token任务
  ↓
[步骤1] 分析概要（10K Token）
  → 保存概要到缓存
  ↓
[步骤2] 模块A细节（20K Token）
  → 引用缓存概要
  → 保存模块A分析
  ↓
[步骤3] 模块B细节（20K Token）
  → 引用缓存概要
  → 保存模块B分析
  ↓
[步骤4] 整合实现（30K Token）
  → 引用所有缓存
```

**实践**：
- 复杂功能先让AI分析概要
- 分段深入各模块细节
- 各段分析结果写入缓存
- 最后整合时引用缓存

### 4. 按需调用与成本控制

**原则**：合理使用Auto模式和高级模型。

**策略**：
- ✅ **简单任务**：使用精简模型或快速编辑模式
- ✅ **复杂任务**：使用Opus 4.5，但提供清晰上下文
- ✅ **批量操作**：先规划，再执行，避免重复调用
- ❌ **避免**：Auto模式无脑运行，导致超额成本

**成本控制检查清单**：
- [ ] 是否真的需要Opus 4.5？（简单任务用Claude 3.5即可）
- [ ] 上下文是否精简？（只包含必要文件）
- [ ] 是否使用了缓存？（避免重复分析）
- [ ] 提示是否结构化？（减少来回沟通）

---

## 代码生成与质量保证

### 1. 模块化任务输入

**原则**：明确指定修改范围，避免AI生成不需要的模块。

**实践**：

#### 明确任务边界
```
❌ 错误提示：
"添加用户登录功能"

✅ 正确提示：
"在 services/authService.ts 中添加 login() 方法
  - 调用现有的 validateUser() 函数
  - 使用现有的 tokenManager 生成token
  - 不要创建新的用户模型（已有 User 类）"
```

#### 接口约定
- 明确新组件与现有系统的集成关系
- 提供相关代码片段和接口定义
- 说明禁止新建的模块

### 2. 代码审查流程

**流程**：
```
1. AI生成代码
  ↓
2. 开发者审查
  - 是否符合架构设计？
  - 是否遵循编码规范？
  - 是否有重复代码？
  ↓
3. 如有偏差
  - 在提示中明确强调规则
  - 引用相关规范文档
  - 要求重新生成
  ↓
4. 验证通过
  - 运行测试
  - 更新文档
  - 提交代码
```

### 3. 避免重复生成

**问题**：AI可能重复生成已有模块。

**解决方案**：
- ✅ 提供文件列表：`ls extension/src/services/`
- ✅ 明确禁止：`不要创建新的XXX服务，已有XXXService`
- ✅ 引用现有代码：`请参考 services/trquantClient.ts 的实现方式`

---

## 模块化开发原则

### 1. 任务拆分

**原则**：将复杂功能拆分为小任务，逐步集成。

**实践**：
```
复杂功能：策略优化器
  ↓
任务1：代码分析器（analyzer/）
  → 完成并测试
  ↓
任务2：平台适配器（adapters/）
  → 基于分析器结果
  → 完成并测试
  ↓
任务3：报告生成器（generator/）
  → 基于分析器和适配器
  → 完成并测试
  ↓
任务4：学习引擎（learner/）
  → 整合所有模块
  → 完成并测试
```

### 2. 接口约定

**原则**：每个模块都有清晰的接口定义。

**实践**：
- 在`MODULE_INDEX.md`中记录接口
- 使用TypeScript类型定义接口
- 提供接口文档和示例

### 3. 集成测试

**原则**：每完成一个模块，立即编写集成测试。

**实践**：
- 模块完成后 → 编写单元测试
- 模块集成后 → 编写集成测试
- 功能完成后 → 端到端测试

---

## 上下文缓存机制

### 1. 缓存结构

```typescript
interface ContextCache {
    // 基本信息
    id: string;                    // 缓存ID（如 'feature-strategy-optimizer'）
    timestamp: string;             // 创建时间
    version: string;                // 项目版本
    
    // 分析结果
    analysis: {
        fileDependencies: string[]; // 文件依赖关系
        architecturePoints: string[]; // 架构要点
        testPlan: string[];        // 测试计划
        apiInterfaces: Record<string, any>; // API接口定义
    };
    
    // 相关文件
    relatedFiles: {
        modified: string[];         // 修改的文件
        referenced: string[];      // 引用的文件
        created: string[];         // 新建的文件
    };
    
    // 决策记录
    decisions: Array<{
        question: string;
        answer: string;
        reason: string;
    }>;
}
```

### 2. 缓存使用流程

```
[开发阶段1] 需求分析
  → AI分析项目结构
  → 生成缓存 cache-v1.json
  → 保存到 .cursor/cache/
  
[开发阶段2] 代码实现
  → 加载 cache-v1.json
  → 提示："使用缓存上下文 cache-v1，已知信息：..."
  → AI基于缓存实现代码
  
[开发阶段3] 测试验证
  → 加载 cache-v1.json
  → 提示："基于缓存 cache-v1 编写测试"
  → AI生成测试用例
```

### 3. 缓存管理

**位置**：`extension/.cursor/cache/`

**命名规则**：`{feature-name}-{version}.json`

**清理策略**：
- 保留最近7天的缓存
- 功能完成后归档到`extension/.cursor/cache/archive/`
- 定期清理过期缓存

---

## 结构化提示模板

### 标准提示结构

```markdown
## 任务
[简要描述任务]

## 背景
- 相关文件：[列出文件路径]
- 当前实现：[描述现状]
- 问题/需求：[说明问题或需求]

## 上下文缓存
- 缓存ID：[如果有]
- 已知信息：[从缓存中提取的关键信息]

## 要求
1. [具体要求1]
2. [具体要求2]
3. [具体要求3]

## 约束
- [约束1]
- [约束2]

## 参考文档
- PROJECT_BRIEF.md - 项目架构
- MODULE_INDEX.md - 模块索引
- ENGINEERING_RULES.md - 编码规范

## 输出
- [期望的输出格式]
- [需要包含的内容]
```

### TRQuant专用提示模板

#### 模板1：添加新命令
```markdown
任务：添加新的TRQuant命令

背景：
- 命令ID格式：trquant.{commandName}
- 注册位置：extension/src/extension.ts
- 实现位置：extension/src/commands/{commandName}.ts
- 相关服务：[列出依赖的服务]

要求：
- 遵循命令命名规范
- 使用TRQuantClient进行Python通信
- 添加错误处理
- 更新package.json注册命令

约束：
- 不得修改现有命令
- 必须通过TRQuantClient调用Python

输出：
- commands/{commandName}.ts 完整实现
- extension.ts 中的注册代码
- package.json 中的命令定义
```

#### 模板2：添加新WebView面板
```markdown
任务：添加新的WebView面板

背景：
- 面板类命名：{Name}Panel
- 实现位置：extension/src/views/{name}Panel.ts
- 单例模式：使用静态 currentPanel
- 消息处理：handleMessage方法

要求：
- 实现单例模式
- 实现dispose方法清理资源
- 使用postMessage与Extension通信
- 支持本地资源引用

约束：
- 必须实现vscode.Disposable接口
- 消息格式统一为 {command, data}

输出：
- views/{name}Panel.ts 完整实现
- 注册代码（在extension.ts中）
```

#### 模板3：Python Bridge新功能
```markdown
任务：在Python Bridge中添加新功能

背景：
- Bridge文件：extension/python/bridge.py
- 协议格式：{"action": "...", "params": {...}}
- 响应格式：{"ok": true, "data": {...}}
- 相关Core模块：[列出]

要求：
- 添加新的action处理函数
- 实现参数验证
- 添加错误处理
- 返回标准JSON格式

约束：
- 不得修改现有action
- 必须处理异常并返回错误

输出：
- bridge.py 中的新函数
- TypeScript端的调用代码（TRQuantClient）
- 错误处理逻辑
```

---

## 开发工作流

### 标准开发流程

```
1. 需求分析
   ├── 查阅 PROJECT_BRIEF.md
   ├── 查阅 MODULE_INDEX.md
   ├── 确认模块位置
   └── 生成上下文缓存

2. 设计讨论（Chat模式）
   ├── 使用结构化提示
   ├── 与AI讨论实现方案
   ├── 确认接口设计
   └── 记录决策到 DECISIONS.md

3. 代码实现（Agent模式）
   ├── 加载上下文缓存
   ├── 提供相关代码片段
   ├── AI生成代码
   └── 开发者审查

4. 测试验证
   ├── 运行单元测试
   ├── 运行集成测试
   └── 手动验证功能

5. 文档更新
   ├── 更新 MODULE_INDEX.md
   ├── 更新相关注释
   └── 提交代码
```

### 快速开发流程（简单功能）

```
1. 明确任务
   └── 使用TASK_TEMPLATE.md

2. 直接实现
   ├── 提供相关文件
   ├── AI生成代码
   └── 快速审查

3. 测试提交
   ├── 运行测试
   └── 提交代码
```

---

## Token使用监控

### 成本控制检查点

每次使用AI前，检查：

- [ ] **是否真的需要AI？**
  - 简单修改 → 手动完成
  - 复杂逻辑 → 使用AI

- [ ] **是否使用了缓存？**
  - 首次分析 → 生成缓存
  - 后续步骤 → 使用缓存

- [ ] **上下文是否精简？**
  - 只包含必要文件
  - 避免全量代码库

- [ ] **提示是否结构化？**
  - 使用模板
  - 明确要求

- [ ] **是否选择了合适的模型？**
  - 简单任务 → Claude 3.5
  - 复杂任务 → Opus 4.5

### Token使用记录

建议在`.cursor/token-usage.log`中记录：
```
[2025-12-04] 功能：策略优化器学习引擎
- 分析阶段：15K tokens（生成缓存）
- 实现阶段：8K tokens（使用缓存，节省30%）
- 测试阶段：5K tokens（使用缓存）
- 总计：28K tokens（无缓存预计35K，节省20%）
```

---

## 质量保证检查清单

### 代码生成后检查

- [ ] **架构一致性**
  - 文件位置是否符合MODULE_INDEX.md？
  - 是否遵循PROJECT_BRIEF.md的架构？

- [ ] **编码规范**
  - 是否符合ENGINEERING_RULES.md？
  - 命名是否遵循规范？
  - 错误处理是否完善？

- [ ] **接口设计**
  - 接口是否在MODULE_INDEX.md中记录？
  - 参数和返回值类型是否定义？

- [ ] **测试覆盖**
  - 是否编写了单元测试？
  - 是否编写了集成测试？

- [ ] **文档更新**
  - 是否更新了相关文档？
  - 注释是否完善？

---

## 常见问题与解决方案

### Q1: AI生成了重复的模块

**原因**：上下文不完整，AI不知道已有模块。

**解决**：
- 提供文件列表：`ls extension/src/services/`
- 明确禁止：`不要创建XXXService，已有`
- 引用现有代码

### Q2: Token消耗过高

**原因**：上下文过大，重复分析。

**解决**：
- 使用上下文缓存
- 精简相关文件
- 使用结构化提示

### Q3: AI偏离架构设计

**原因**：没有引用架构文档。

**解决**：
- 在提示中引用PROJECT_BRIEF.md
- 让AI对照MODULE_INDEX.md验证
- 明确架构约束

### Q4: 跨会话上下文丢失

**原因**：依赖对话历史。

**解决**：
- 主动提供项目概要
- 使用内存文件功能
- 更新文档作为信息源

---

## 参考资源

### 内部文档
- `PROJECT_BRIEF.md` - 项目架构
- `MODULE_INDEX.md` - 模块索引
- `ENGINEERING_RULES.md` - 编码规范
- `DECISIONS.md` - 架构决策
- `TASK_TEMPLATE.md` - 任务模板

### 外部资源
- [Cursor Community Forum](https://forum.cursor.com/)
- [Vibe Coding with Cursor Guide](https://medium.com/@aaabulkhair/vibe-coding-with-cursor-a-survival-guide-for-10x-speed-without-10x-disasters-50e25edaf3d9)
- [Token Cost Reduction Guide](https://medium.com/@sun.raphael/how-to-reduce-30-40-of-ai-token-costs-with-context-cache-snippets-and-structured-prompts-01fe6bbebb37)

---

## 持续改进

### 定期审查
- 每月审查Token使用情况
- 评估缓存效果
- 优化提示模板
- 更新最佳实践

### 经验积累
- 记录成功案例
- 总结失败教训
- 更新本文档
- 分享给团队

---

**文档版本**：1.0.0  
**最后更新**：2025-12-04  
**维护者**：TRQuant Team

