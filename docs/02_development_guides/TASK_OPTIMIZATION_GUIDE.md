# TRQuant 任务优化与Max Mode使用方案

> **创建时间**: 2025-12-14  
> **目的**: 优化Max mode使用，节省token和调用次数

---

## 📊 任务复杂度分析标准

### 复杂度等级

| 等级 | 特征 | 推荐模式 | 示例 |
|------|------|----------|------|
| **SIMPLE** | 单个文件修改、简单修复、文档更新 | **auto** | 修复语法错误、更新文档、格式调整 |
| **MEDIUM** | 多个文件修改、需要理解业务逻辑 | **max** | 功能增强、bug修复、代码重构 |
| **COMPLEX** | 架构变更、新功能开发、多轮迭代 | **max** | 新模块开发、系统集成、性能优化 |
| **CRITICAL** | 系统重构、核心功能、大规模变更 | **max** | 数据库迁移、架构重构、核心引擎开发 |

### 判断因素

1. **文件数量**: 
   - 1个文件 → SIMPLE (auto)
   - 2-5个文件 → MEDIUM (max)
   - 5+个文件 → COMPLEX (max)

2. **任务类型关键词**:
   - 简单: fix, update, modify, change, edit, 文档, 注释, 格式
   - 复杂: refactor, 重构, architecture, 架构, design, 设计, implement, 实现
   - 关键: system, 系统, core, 核心, engine, 引擎, framework, 框架

3. **预计时间**:
   - < 1小时 → SIMPLE (auto)
   - 1-4小时 → MEDIUM (max)
   - 4-8小时 → COMPLEX (max)
   - > 8小时 → CRITICAL (max)

4. **依赖关系**:
   - 无依赖 → SIMPLE (auto)
   - 1-3个依赖 → MEDIUM (max)
   - 3+个依赖 → COMPLEX (max)

---

## 🎯 当前项目任务分析

### 第一阶段：MCP规范标准化（1-3周）

#### 1.4 MCP服务器集成修复
- **复杂度**: MEDIUM → COMPLEX
- **推荐模式**: **max**
- **原因**: 涉及多个文件修改，需要理解MCP规范，有依赖关系
- **优化建议**: 
  - 使用`task.optimize_workflow`分析需要读取的文件
  - 缓存已修复服务器的模式作为参考
  - 批量处理相似结构的服务器

#### 1.5 Cursor扩展MCP调用流程规范
- **复杂度**: COMPLEX
- **推荐模式**: **max**
- **原因**: 涉及架构设计和系统集成

#### 1.6 MCP类型组织与结果归档
- **复杂度**: MEDIUM
- **推荐模式**: **max**
- **原因**: 需要理解现有结构，设计新的组织方式

### 第二阶段：GUI前端优化（4-5周）

#### 2.1 MVC/MVVM开发模式
- **复杂度**: CRITICAL
- **推荐模式**: **max**
- **原因**: 架构重构，涉及整个前端系统

#### 2.2 任务触发与异步
- **复杂度**: COMPLEX
- **推荐模式**: **max**
- **原因**: 需要理解现有架构，设计异步机制

#### 2.3 图表展示库
- **复杂度**: MEDIUM
- **推荐模式**: **max**
- **原因**: 需要集成第三方库，理解数据流

### 第三阶段：工作流编排优化（6-7周）

#### 3.1 工作流状态持久化
- **复杂度**: COMPLEX
- **推荐模式**: **max**
- **原因**: 涉及数据库设计和状态管理

#### 3.2 错误处理与恢复机制
- **复杂度**: COMPLEX
- **推荐模式**: **max**
- **原因**: 需要理解错误场景，设计恢复策略

#### 3.3 工作流可视化
- **复杂度**: MEDIUM
- **推荐模式**: **max**
- **原因**: 需要设计可视化界面

### 第四阶段：数据库实施（8-10周）

#### 4.1-4.3 PostgreSQL/时序库/对象存储部署
- **复杂度**: CRITICAL
- **推荐模式**: **max**
- **原因**: 系统级变更，涉及数据迁移

---

## 💡 Max Mode优化策略

### 1. 上下文缓存管理

**使用场景**: 避免重复读取相同文件

**使用方法**:
```python
# 1. 检查是否有缓存
result = task.get_context(file_path="docs/PROJECT_TASK_LIST.md")
if result["cached"]:
    # 使用缓存
    context = result["context"]
else:
    # 读取文件
    content = read_file("docs/PROJECT_TASK_LIST.md")
    # 缓存上下文（摘要、关键信息）
    task.cache_context(
        file_path="docs/PROJECT_TASK_LIST.md",
        context={
            "summary": "项目任务列表，包含15个主要阶段",
            "key_tasks": [...],
            "last_updated": "2025-12-14"
        }
    )
```

**节省效果**: 
- 每个文件缓存可节省约10k-50k tokens
- 如果10个文件都有缓存，可节省100k-500k tokens

### 2. 工作流优化

**使用场景**: 开始新任务前，分析需要读取的文件

**使用方法**:
```python
result = task.optimize_workflow(
    task_title="修复MCP服务器集成",
    file_paths=[
        "mcp_servers/schema_server.py",
        "mcp_servers/factor_server.py",
        "mcp_servers/report_server.py",
        "docs/MCP_INTEGRATION_BEST_PRACTICES.md"
    ]
)

# 结果会显示：
# - 哪些文件有缓存可以复用
# - 哪些文件需要读取
# - 预计节省的tokens
```

### 3. 任务模式推荐

**使用场景**: 开始任务前，判断应该用Max mode还是auto模式

**使用方法**:
```python
# 分析单个任务
result = task.analyze_complexity(
    task_title="修复report_server.py的report.archive工具",
    task_description="修复handler函数内else块的位置问题",
    file_count=1,
    code_complexity="medium"
)

# 结果：
# {
#   "complexity": "medium",
#   "recommended_mode": "max",
#   "reason": "任务需要理解上下文和业务逻辑，建议使用Max mode"
# }
```

### 4. 批量任务分析

**使用场景**: 分析整个项目阶段的任务

**使用方法**:
```python
result = task.recommend_mode(
    tasks=[
        {
            "id": "task1",
            "title": "修复MCP服务器",
            "file_count": 6,
            "code_complexity": "medium"
        },
        {
            "id": "task2",
            "title": "更新文档",
            "file_count": 1,
            "code_complexity": "low"
        }
    ]
)

# 结果会显示：
# - 每个任务的推荐模式
# - 总体统计（多少任务用max，多少用auto）
# - 预计节省的tokens
```

---

## 📈 预期效果

### Token节省

假设：
- 每个任务平均需要读取5个文件
- 每个文件平均20k tokens
- 使用缓存后，每个文件节省15k tokens（只读取摘要）

**节省计算**:
- 单个任务: 5个文件 × 15k = 75k tokens
- 10个任务: 750k tokens
- 100个任务: 7.5M tokens

### 调用次数优化

- **不使用缓存**: 每个任务需要多次Max mode调用（读取文件、理解代码、修改代码）
- **使用缓存**: 减少文件读取调用，直接使用缓存的上下文

**预计减少**: 30-50%的Max mode调用次数

---

## 🚀 实施建议

### 立即开始

1. **配置MCP服务器**
   - 将`task_optimizer_server.py`添加到MCP配置
   - 测试所有工具是否正常工作

2. **分析当前任务**
   - 使用`task.analyze_complexity`分析当前进行中的任务
   - 使用`task.recommend_mode`分析待处理任务列表

3. **建立缓存**
   - 对常用文档建立缓存（PROJECT_TASK_LIST.md, DEVELOPMENT_PLAN.md等）
   - 对已修复的服务器建立缓存（作为参考模式）

### 持续优化

1. **任务开始前**
   - 使用`task.optimize_workflow`分析需要读取的文件
   - 检查缓存，复用已有上下文

2. **任务进行中**
   - 读取新文件后，立即缓存上下文
   - 使用`task.analyze_complexity`判断是否需要切换到Max mode

3. **任务完成后**
   - 更新任务状态
   - 清理过期缓存（使用`task.clear_cache`）

---

## 📝 使用示例

### 示例1: 开始新任务前

```python
# 1. 分析任务复杂度
complexity = task.analyze_complexity(
    task_title="修复MCP服务器集成",
    file_count=6,
    code_complexity="medium"
)

# 2. 优化工作流
workflow = task.optimize_workflow(
    task_title="修复MCP服务器集成",
    file_paths=[
        "mcp_servers/schema_server.py",
        "mcp_servers/factor_server.py",
        "docs/MCP_INTEGRATION_BEST_PRACTICES.md"
    ]
)

# 3. 根据结果决定：
# - 如果workflow["file_analysis"]["cached_count"] > 0，使用缓存
# - 如果需要读取新文件，读取后立即缓存
```

### 示例2: 批量分析任务

```python
# 从PROJECT_TASK_LIST.md提取任务
tasks = extract_tasks_from_markdown("docs/PROJECT_TASK_LIST.md")

# 批量分析
result = task.recommend_mode(tasks=tasks)

# 根据结果：
# - 将SIMPLE任务标记为auto模式
# - 将MEDIUM/COMPLEX/CRITICAL任务标记为max模式
# - 优先处理auto模式任务（节省Max mode调用）
```

---

## ⚠️ 注意事项

1. **缓存时效性**: 缓存默认24小时有效，文件修改后会自动失效
2. **缓存大小**: 定期清理过期缓存，避免占用过多空间
3. **缓存准确性**: 缓存的是摘要和关键信息，不是完整文件内容
4. **模式切换**: 如果auto模式无法完成任务，及时切换到Max mode

---

**文档维护**: 根据实际使用情况持续优化  
**最后更新**: 2025-12-14
