# 🧠 TRQuant 知识库和自学习系统

## 一、调用方式总览

### 🔴 自动调用（无需手动操作）

| 触发时机 | 自动行为 |
|----------|----------|
| `issue.resolve()` | 解决问题后**自动**提取知识到知识库 |
| `experience.mark_useful()` | 标记经验有用后**自动**提取知识 |
| `session.init()` | 会话初始化时**自动**检查待学习内容 |

### 🟡 手动调用（按需使用）

| 工具 | 用途 |
|------|------|
| `knowledge.search()` | 搜索已有知识 |
| `knowledge.add()` | 直接添加新知识 |
| `learn.suggest()` | 根据上下文智能推荐 |
| `learn.auto_extract()` | 批量提取所有待学习内容 |

---

## 二、自动学习流程图

```
┌─────────────────────────────────────────────────────────────┐
│                   自动学习触发点                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐                                        │
│  │ issue.resolve() │ ─── 自动 ──→ learn.from_issue()       │
│  │  (解决问题)     │              │                         │
│  └─────────────────┘              ↓                         │
│                              ┌─────────┐                    │
│  ┌─────────────────┐         │ 知识库  │                    │
│  │ experience.     │ ─ 自动 →│         │                    │
│  │ mark_useful()   │         │ 持久化  │                    │
│  │ (标记有用)      │         │ 存储    │                    │
│  └─────────────────┘         └────┬────┘                    │
│                                   │                         │
│  ┌─────────────────┐              ↓                         │
│  │ session.init()  │ ─── 检查 ──→ 显示待学习数量           │
│  │  (会话初始化)   │              提示执行auto_extract      │
│  └─────────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 三、具体使用示例

### 示例1: 解决问题（自动学习）

```python
# 创建问题
issue.create(title="CSP配置错误", description="Webview脚本无法执行")

# 解决问题 - 自动触发学习！
issue.resolve(
    issue_id="issue_xxx",
    solution="添加 unsafe-inline 到 CSP script-src"
)
# 返回: {..., "auto_learned": true, "knowledge_id": "kb_xxx"}

# 知识已自动添加到知识库，下次可以搜索到
knowledge.search("CSP")
```

### 示例2: 记录经验（自动学习）

```python
# 添加经验
exp = experience.add(
    content="使用绝对路径可以避免worktrees问题",
    category="file_operation"
)

# 标记有用 - 自动触发学习！
experience.mark_useful(exp["experience_id"])
# 返回: {..., "auto_learned": true, "knowledge_id": "kb_xxx"}
```

### 示例3: 会话初始化（自动检查）

```python
# 每次新对话开始
result = session.init()

# 返回中包含待学习内容统计:
# {
#   "pending_learning": {
#     "unlearned_issues": 2,
#     "unlearned_experiences": 3,
#     "total": 5
#   },
#   "recommendations": [
#     "有 5 条待学习内容，建议执行 learn.auto_extract"
#   ],
#   "knowledge_stats": {
#     "total": 10,
#     "types": {"practice": 5, "error": 3, "lesson": 2}
#   }
# }

# 如果有待学习内容，可以批量学习
learn.auto_extract()
```

### 示例4: 主动搜索知识

```python
# 遇到问题时，先搜索知识库
result = knowledge.search("webview 不工作")

# 或使用智能建议
suggest = learn.suggest("Webview按钮点击没有响应")
# 返回相关知识、错误模式、最佳实践
```

### 示例5: 主动添加知识

```python
# 直接添加经验教训
knowledge.add(
    title="MCP调用超时处理",
    content="MCP调用超时时，检查服务器进程是否正常...",
    type="lesson",
    tags=["mcp", "timeout"]
)

# 添加错误模式
error_pattern.add(
    error_type="ImportError",
    pattern="cannot import name 'xxx' from 'module'",
    solution="检查模块版本和导入路径",
    prevention="使用requirements.txt锁定版本"
)

# 添加最佳实践
practice.add(
    title="文件操作使用绝对路径",
    description="所有文件操作必须使用绝对路径...",
    category="file_operation"
)
```

---

## 四、知识类型说明

| 类型 | 代码 | 说明 | 示例 |
|------|------|------|------|
| 错误模式 | `error` | 错误的模式和解决方案 | worktrees问题 |
| 最佳实践 | `practice` | 推荐的做法 | 使用绝对路径 |
| 经验教训 | `lesson` | 从问题中学到的 | 某次调试经验 |
| 开发技巧 | `tip` | 实用技巧 | 快捷键、命令 |
| 设计模式 | `pattern` | 代码模式 | 单例模式实现 |
| 开发规则 | `rule` | 强制规则 | 必须session.init |

---

## 五、数据存储

```
.trquant/dev/knowledge/
└── knowledge_base.json    # 所有知识存储在这里
```

知识结构:
```json
{
  "id": "kb_20251219_xxx",
  "title": "标题",
  "content": "详细内容",
  "type": "lesson",
  "tags": ["tag1", "tag2"],
  "source": "issue_xxx",  // 来源（自动学习时记录）
  "useful_count": 5,       // 被标记有用的次数
  "created": "...",
  "updated": "..."
}
```

---

## 六、最佳实践

### ✅ 推荐做法

1. **遇问题先搜索**: `knowledge.search()` 或 `learn.suggest()`
2. **解决问题记录solution**: `issue.resolve(issue_id, solution="详细解决方案")`
3. **有用的经验标记**: `experience.mark_useful(exp_id)`
4. **定期执行批量学习**: `learn.auto_extract()`

### ❌ 避免做法

1. 不记录solution就关闭问题
2. 不标记有用的经验
3. 重复遇到相同问题但不搜索知识库

---

*必读文档 5/5 | 更新时间: 2025-12-19*
