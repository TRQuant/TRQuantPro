# 文件操作指南 - 避免 Worktrees 问题

## ⚠️ 重要警告

**所有文件操作必须使用主项目路径的绝对路径！**

Cursor IDE 会在 `~/.cursor/worktrees/TRQuant/xxx` 中创建临时工作区，如果使用相对路径或工作区路径，文件可能会被创建到错误的位置。

## 问题示例

### ❌ 错误做法

```typescript
// 错误：使用相对路径
const filePath = 'docs/myfile.md';
fs.writeFileSync(filePath, content);

// 错误：使用工作区路径
const workspacePath = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
const filePath = path.join(workspacePath, 'docs/myfile.md');
```

**问题**：如果 Cursor 在 worktrees 中执行，文件会被创建到 `~/.cursor/worktrees/TRQuant/xxx/docs/myfile.md`，而不是主项目路径。

### ✅ 正确做法

```typescript
import { ConfigManager } from '../utils/config';

// 正确：使用 ConfigManager 获取主项目路径
const configManager = ConfigManager.getInstance();
const projectRoot = configManager.getProjectRoot(extensionPath);
const filePath = path.join(projectRoot, 'docs/myfile.md');
fs.writeFileSync(filePath, content);
```

## 统一工具函数

### TypeScript/JavaScript

```typescript
import { ConfigManager } from '../utils/config';
import * as path from 'path';

// 获取项目根目录（绝对路径）
const configManager = ConfigManager.getInstance();
const projectRoot = configManager.getProjectRoot(extensionPath);

// 构建文件路径（使用绝对路径）
const filePath = path.join(projectRoot, 'docs', 'myfile.md');

// 验证路径
if (!filePath.startsWith(projectRoot)) {
    throw new Error('文件路径必须在项目根目录内');
}
```

### Python

```python
import os
from pathlib import Path

# 从环境变量获取项目根目录
project_root = os.environ.get('TRQUANT_ROOT', '/home/taotao/dev/QuantTest/TRQuant')

# 构建文件路径（使用绝对路径）
file_path = Path(project_root) / 'docs' / 'myfile.md'

# 验证路径
if not str(file_path).startswith(project_root):
    raise ValueError('文件路径必须在项目根目录内')
```

## 文件操作检查清单

在创建或修改文件前，检查：

- [ ] 是否使用了 `ConfigManager.getProjectRoot()` 获取项目根路径？
- [ ] 文件路径是否是绝对路径？
- [ ] 路径是否以项目根目录开头？
- [ ] 是否过滤了 worktrees 路径？

## 常见错误场景

### 1. 使用 `write` 工具创建文件

**问题**：`write` 工具可能使用相对路径，导致文件创建到 worktrees。

**解决**：使用绝对路径，或使用 `cat heredoc` 命令：

```bash
cd /home/taotao/dev/QuantTest/TRQuant
cat > docs/myfile.md << 'EOF'
文件内容
EOF
```

### 2. 使用 `vscode.workspace.workspaceFolders`

**问题**：工作区路径可能指向 worktrees。

**解决**：使用 `ConfigManager.getProjectRoot()` 替代。

### 3. 使用相对路径

**问题**：相对路径基于当前工作目录，可能在 worktrees 中。

**解决**：始终使用绝对路径，从项目根目录开始构建。

## 验证方法

### 检查文件位置

```bash
# 检查文件是否在主项目路径中
ls -la /home/taotao/dev/QuantTest/TRQuant/docs/myfile.md

# 检查是否在 worktrees 中（不应该存在）
ls -la ~/.cursor/worktrees/TRQuant/*/docs/myfile.md
```

### 检查日志

在扩展日志中查找：
- `使用TRQUANT_ROOT环境变量` - ✅ 正确
- `使用推断的项目路径` - ✅ 正确
- `检测到 worktrees 路径，已跳过` - ✅ 已过滤

## 相关文档

- `docs/CURSOR_WORKTREES_ISSUE.md` - Worktrees 问题详细分析
- `extension/src/utils/config.ts` - `getProjectRoot()` 方法实现

## 更新记录

- **2025-12-19**: 创建本文档，规范文件操作流程

