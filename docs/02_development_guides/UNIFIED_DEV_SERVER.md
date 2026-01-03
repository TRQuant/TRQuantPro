# TRQuant 统一开发工具服务器

> 更新日期: 2025-12-19
> 文件: `mcp_servers/unified_dev_server.py`

---

## 概述

整合所有开发流程相关工具到一个统一服务器，支持自学习和知识积累。

**总计: 91个工具 (27个分类)**

---

## 工具分类总览

| 类别 | 工具数 | 说明 |
|------|--------|------|
| 核心开发 | 33 | 任务、日志、问题等 |
| 代码质量 | 24 | 代码分析、测试等 |
| GUI开发 | 11 | Webview、面板等 |
| 会话快捷 | 7 | 会话管理、快捷操作 |
| **知识自学习** | **16** | 知识库、自学习系统 ⭐新增 |

---

## ⭐ 知识库和自学习系统 (16个工具)

### 知识库 (knowledge.*) - 6个

| 工具 | 说明 |
|------|------|
| `knowledge.add` | 添加知识条目 |
| `knowledge.search` | 搜索知识库 |
| `knowledge.get` | 获取知识详情 |
| `knowledge.update` | 更新知识 |
| `knowledge.mark_useful` | 标记有用 (提高权重) |
| `knowledge.stats` | 知识库统计 |

### 错误模式库 (error_pattern.*) - 3个

| 工具 | 说明 |
|------|------|
| `error_pattern.add` | 添加错误模式 |
| `error_pattern.search` | 搜索匹配的错误模式 |
| `error_pattern.list` | 列出所有错误模式 |

### 最佳实践库 (practice.*) - 3个

| 工具 | 说明 |
|------|------|
| `practice.add` | 添加最佳实践 |
| `practice.search` | 搜索最佳实践 |
| `practice.list` | 列出最佳实践 |

### 自学习系统 (learn.*) - 4个

| 工具 | 说明 |
|------|------|
| `learn.from_issue` | 从已解决问题学习 |
| `learn.from_experience` | 从经验学习 |
| `learn.auto_extract` | 自动提取所有知识 |
| `learn.suggest` | 智能建议 (根据上下文推荐) |

---

## 自学习流程

### 1. 解决问题时自动学习

```python
# 解决问题
issue.resolve(issue_id, solution="解决方案")

# 自动从问题中提取知识
learn.from_issue(issue_id)
```

### 2. 记录经验时自动学习

```python
# 记录经验
experience.add("经验内容", category="xxx")
experience.mark_useful(exp_id)

# 自动从经验中提取知识
learn.from_experience(exp_id)
```

### 3. 批量自动学习

```python
# 自动从所有未处理的经验和已解决问题中提取知识
learn.auto_extract()
```

### 4. 智能建议

```python
# 根据上下文推荐相关知识
result = learn.suggest("CSP配置问题")

# 返回:
# - 相关知识
# - 匹配的错误模式
# - 相关最佳实践
```

---

## 知识类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `pattern` | 设计模式和代码模式 | 单例模式实现 |
| `error` | 错误模式和解决方案 | worktrees问题 |
| `practice` | 最佳实践 | 使用绝对路径 |
| `lesson` | 经验教训 | 从某次问题中学到的 |
| `tip` | 开发技巧 | 快捷操作技巧 |
| `rule` | 开发规则 | 必须执行session.init |

---

## 数据存储位置

```
.trquant/dev/
├── knowledge/
│   └── knowledge_base.json    # 知识库数据
├── tasks/
├── devlog/
├── issues/
├── experience/
└── ...
```

---

## 相关文档

- `docs/MUST_READ/` - 必读文档目录
- `docs/MCP_STANDARD_DEV_WORKFLOW.md` - 完整开发流程
- `.cursorrules` - Cursor规则配置 v4.0

---

*文档版本: 5.0 | 更新时间: 2025-12-19*
