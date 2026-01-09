# 轩辕剑灵智能Prompt优化工具使用指南

> **日期**: 2026-01-03  
> **状态**: ✅ 完整实现  
> **版本**: 1.0.0

---

## 📋 功能概述

`xuanyuan.prompt.optimize` 是一个智能prompt优化工具，能够根据开发任务需求自动生成符合Cursor方法论的结构化prompt。

### 核心特性

1. **结构化生成**：自动生成包含目标、约束、范围、验收标准的完整prompt
2. **类型支持**：支持多种prompt类型（新功能开发、重构、Bug修复等）
3. **智能约束**：根据上下文和技术栈自动生成约束条件
4. **模板参考**：可选参考已有prompt模板和最佳实践
5. **MCP集成**：可通过MCP在Cursor Chat中直接调用
6. **GUI界面**：提供独立的图形界面，支持可视化操作
7. **反馈机制**：支持用户反馈，持续优化工具本身

### 使用方式

#### 方式1：通过GUI界面（推荐）

启动轩辕剑灵GUI：
```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
venv/bin/python gui/xuanyuan_main_window.py
```

或使用桌面快捷方式。

#### 方式2：通过Cursor Chat

在Cursor Chat中直接调用MCP工具：
```
@xuanyuan 优化我的prompt：实现用户登录功能
```

#### 方式3：通过Python代码

```python
from core.mcp.client import get_mcp_client
client = get_mcp_client()
result = client.call('xuanyuan.prompt.optimize', {
    'task_description': '实现用户登录功能，使用JWT认证',
    'context': 'Python Flask项目',
    'prompt_type': 'feature_development'
})
```

---

## 🚀 使用方法

### 在Cursor Chat中调用

```
@xuanyuan.prompt.optimize
任务描述: 实现用户登录功能，使用JWT认证
上下文: Python Flask项目，已有用户模型
类型: feature_development
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| `task_description` | string | ✅ | 开发任务描述，描述要实现什么功能或解决什么问题 | - |
| `context` | string | ❌ | 上下文信息：相关文件、模块、技术栈等 | "" |
| `prompt_type` | string | ❌ | Prompt类型 | "feature_development" |
| `include_template` | boolean | ❌ | 是否参考已有模板 | true |

### Prompt类型

- `feature_development` - 新功能开发
- `refactoring` - 代码重构
- `bug_fix` - Bug修复
- `code_review` - 代码审查
- `testing` - 测试编写
- `documentation` - 文档编写

---

## 📝 使用示例

### 示例1: 新功能开发

**输入**:
```json
{
  "task_description": "添加用户注册功能，包含邮箱验证",
  "context": "Flask应用，使用SQLAlchemy",
  "prompt_type": "feature_development"
}
```

**输出结构**:
- 目标：添加用户注册功能，包含邮箱验证
- 约束：遵循项目规范、使用Python 3.x、不引入新依赖等
- 范围：涉及文件、只修改必要部分
- 验收标准：功能实现、通过测试、通过lint、更新文档

### 示例2: Bug修复

**输入**:
```json
{
  "task_description": "修复登录接口的SQL注入漏洞",
  "context": "Flask应用，使用SQLAlchemy ORM",
  "prompt_type": "bug_fix"
}
```

**输出结构**:
- 问题描述：修复登录接口的SQL注入漏洞
- 约束：修复问题同时不引入新bug、添加回归测试等
- 修复范围：涉及文件、只修改必要部分
- 验收标准：问题已修复、通过回归测试、添加测试用例等

### 示例3: 代码重构

**输入**:
```json
{
  "task_description": "重构用户服务模块，提升可维护性",
  "context": "Python项目，使用依赖注入",
  "prompt_type": "refactoring"
}
```

**输出结构**:
- 重构目标：提升可维护性
- 约束：行为保持一致、不改变公开API、最小化diff等
- 范围：涉及文件、只改必要部分
- 验收标准：功能行为一致、可读性提升、通过现有测试等

---

## 🎯 生成的结构化要素

根据Cursor方法论，生成的prompt包含以下结构化要素：

### 1. 目标（Goal）
- 明确要实现什么功能或解决什么问题
- 包含任务描述和上下文信息

### 2. 约束（Constraints）
- 技术栈约束（Python、TypeScript等）
- 项目规范约束
- 类型特定约束（重构、Bug修复等）

### 3. 范围（Scope）
- 涉及的文件和模块
- 修改范围限制

### 4. 验收标准（Acceptance Criteria）
- 功能验证
- 测试要求
- 代码质量要求
- 文档要求

---

## 🔧 实现细节

### 生成逻辑

1. **解析任务描述**：提取关键信息和上下文
2. **选择模板**：根据prompt_type选择对应的模板结构
3. **生成约束**：基于上下文和技术栈生成约束条件
4. **生成范围**：从任务描述中提取文件/模块信息
5. **生成验收标准**：根据prompt_type生成对应的验收标准
6. **参考模板**：如果启用，参考已有的prompt模板

### 约束生成规则

- **通用约束**：项目规范、API兼容性、注释文档
- **技术栈约束**：根据context识别Python/TypeScript/React等
- **类型特定约束**：
  - 重构：行为一致、最小diff
  - Bug修复：不引入新bug、回归测试
  - 新功能：不引入新依赖、考虑性能

---

## 📊 返回数据格式

```json
{
  "success": true,
  "prompt": "生成的完整prompt文本",
  "category": "feature_development",
  "tags": ["has_goal", "has_constraint", "python"],
  "prompt_type": "feature_development",
  "structure": {
    "has_goal": true,
    "has_constraint": true,
    "has_scope": true,
    "has_acceptance": true
  }
}
```

---

## 💡 最佳实践

1. **明确任务描述**：提供清晰的任务描述，包含关键需求
2. **提供上下文**：提供技术栈、相关文件等上下文信息
3. **选择合适类型**：根据任务性质选择合适的prompt_type
4. **启用模板参考**：默认启用，可参考已有的最佳实践

---

## 🔗 相关文档

- [Cursor Prompt Engineering方法论](XUANYUAN_EXTRACT_PROMPT_REDESIGN.md)
- [轩辕剑灵MCP服务器文档](XUANYUAN_MCP_SETUP.md)
- [Prompt模板管理](XUANYUAN_GUI_IMPLEMENTATION_PLAN.md)

---

## ✅ 测试验证

工具已通过以下测试：
- ✅ 新功能开发prompt生成
- ✅ Bug修复prompt生成
- ✅ 代码重构prompt生成
- ✅ MCP路由和调用
- ✅ 结构化要素识别

---

**最后更新**: 2026-01-03

