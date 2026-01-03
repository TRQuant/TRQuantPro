# Worktrees 问题解决方案状态

## ✅ 已完成的措施

### 1. 规则配置

**`.cursorrules`** - 已添加强制规则：
- ✅ 文件操作必须使用绝对路径
- ✅ 禁止使用相对路径
- ✅ 路径转换规则

**`.cursor-prompt-template.md`** - 已创建提示模板：
- ✅ 每次对话开始时的提醒
- ✅ 路径检查清单

### 2. 文档

所有文档都在主项目路径 `/home/taotao/dev/QuantTest/TRQuant/docs/`：
- ✅ `ABSOLUTE_PATH_REQUIREMENT.md` - 绝对路径要求详细说明
- ✅ `DISABLE_CURSOR_WORKTREES.md` - 禁用 worktrees 指南
- ✅ `CURSOR_WORKTREES_ISSUE.md` - 问题分析
- ✅ `FILE_OPERATIONS_GUIDE.md` - 文件操作规范

## ⚠️ 重要说明

### 规则是否生效？

**`.cursorrules` 规则**：
- ✅ 已添加到文件中
- ⚠️ **但是**：Cursor 的 `write` 工具本身仍然会基于当前工作区路径解析相对路径
- ⚠️ **关键**：即使 AI 遵循规则，如果用户或 AI 提供了相对路径，`write` 工具仍然会解析到 worktrees

### 当前工作区状态

Cursor 仍然在 worktrees 中运行：
- 工作区路径：`file:///home/taotao/.cursor/worktrees/TRQuant/fpc`
- 这意味着相对路径仍然会被解析到 worktrees

### 解决方案

#### 方案1：强制使用绝对路径（已实施）

**规则已设置**，但需要：
1. AI 助手必须严格遵循规则
2. 用户提供路径时也必须使用绝对路径
3. 在代码中验证路径

**验证方法**：
```bash
# 检查文件是否在主项目路径
ls -la /home/taotao/dev/QuantTest/TRQuant/docs/myfile.md

# 检查是否在 worktrees 中（不应该存在）
find ~/.cursor/worktrees/TRQuant -name "myfile.md" 2>/dev/null
```

#### 方案2：禁用 worktrees（推荐）

**这是根本解决方案**，按照 `docs/DISABLE_CURSOR_WORKTREES.md` 中的步骤：

1. 打开 Cursor 设置
2. 搜索 `agent.autoRunMode`
3. 设置为 `everything` 或 `disabled`
4. 重启 Cursor

**效果**：
- ✅ Cursor 直接在主项目路径中运行
- ✅ 相对路径会解析到主项目路径
- ✅ 不再创建 worktrees

## 后续操作建议

### 立即行动

1. **测试规则是否生效**
   - 让 AI 创建一个新文件（使用相对路径）
   - 检查文件是否在主项目路径中

2. **如果规则不生效**
   - 执行方案2：禁用 worktrees
   - 这是最可靠的解决方案

### 长期方案

1. **禁用 worktrees**（推荐）
   - 从根本上解决问题
   - 释放 99GB 磁盘空间

2. **代码层面保护**
   - 所有代码中的路径操作使用 `ConfigManager.getProjectRoot()`
   - 验证路径有效性

## 验证清单

- [ ] `.cursorrules` 包含绝对路径规则
- [ ] `.cursor-prompt-template.md` 存在
- [ ] 所有文档在主项目路径中
- [ ] 测试：创建新文件是否在主项目路径中
- [ ] （可选）禁用 worktrees

## 更新记录

- **2025-12-19**: 创建本文档，记录解决方案状态
- **2025-12-19**: 添加规则到 `.cursorrules`
- **2025-12-19**: 创建提示模板

