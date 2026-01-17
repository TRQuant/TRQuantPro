# 绝对路径要求 - 文件操作规范

## ⚠️ 强制要求

**所有文件操作必须使用绝对路径！**

## 问题说明

### Cursor Worktrees 机制

Cursor IDE 会在 `~/.cursor/worktrees/TRQuant/xxx` 中创建临时工作区。当使用 `write` 工具创建文件时：

- **相对路径**：`docs/myfile.md`
  - 会被解析为：`当前工作区路径 + docs/myfile.md`
  - 如果当前工作区是 worktrees：`~/.cursor/worktrees/TRQuant/xxx/docs/myfile.md` ❌
  - 如果当前工作区是主项目：`/home/taotao/dev/QuantTest/TRQuant/docs/myfile.md` ✅

- **绝对路径**：`/home/taotao/dev/QuantTest/TRQuant/docs/myfile.md`
  - 始终创建到正确位置 ✅

## 规范要求

### 1. 创建新文件

**❌ 错误**：
```
请创建文件：docs/myfile.md
```

**✅ 正确**：
```
请创建文件：/home/taotao/dev/QuantTest/TRQuant/docs/myfile.md
```

### 2. 修改现有文件

**❌ 错误**：
```
请修改文件：extension/src/utils/config.ts
```

**✅ 正确**：
```
请修改文件：/home/taotao/dev/QuantTest/TRQuant/extension/src/utils/config.ts
```

### 3. 使用工具函数（代码中）

在 TypeScript/JavaScript 代码中：

```typescript
import { ConfigManager } from '../utils/config';
import * as path from 'path';

// 获取项目根目录（绝对路径）
const configManager = ConfigManager.getInstance();
const projectRoot = configManager.getProjectRoot(extensionPath);

// 构建文件路径（使用绝对路径）
const filePath = path.join(projectRoot, 'docs', 'myfile.md');
// filePath 现在是：/home/taotao/dev/QuantTest/TRQuant/docs/myfile.md
```

在 Python 代码中：

```python
import os
from pathlib import Path

# 从环境变量获取项目根目录
project_root = os.environ.get('TRQUANT_ROOT', '/home/taotao/dev/QuantTest/TRQuant')

# 构建文件路径（使用绝对路径）
file_path = Path(project_root) / 'docs' / 'myfile.md'
# file_path 现在是：/home/taotao/dev/QuantTest/TRQuant/docs/myfile.md
```

## 检查清单

在创建或修改文件前，检查：

- [ ] 是否使用了绝对路径？
- [ ] 路径是否以 `/home/taotao/dev/QuantTest/TRQuant` 开头？
- [ ] 是否避免了相对路径（如 `docs/`, `extension/` 等）？

## 快速参考

### 常用目录的绝对路径

```bash
# 项目根目录
/home/taotao/dev/QuantTest/TRQuant

# 文档目录
/home/taotao/dev/QuantTest/TRQuant/docs

# 扩展目录
/home/taotao/dev/QuantTest/TRQuant/extension

# 扩展源码目录
/home/taotao/dev/QuantTest/TRQuant/extension/src

# MCP 服务器目录
/home/taotao/dev/QuantTest/TRQuant/mcp_servers

# 核心代码目录
/home/taotao/dev/QuantTest/TRQuant/core
```

### 跨机器部署

如果项目在其他机器上，使用环境变量：

```bash
export TRQUANT_ROOT=/path/to/your/TRQuant
```

然后在代码中使用：
```typescript
const projectRoot = process.env.TRQUANT_ROOT || '/home/taotao/dev/QuantTest/TRQuant';
```

## 验证方法

### 1. 检查文件位置

```bash
# 检查文件是否在主项目路径中
ls -la /home/taotao/dev/QuantTest/TRQuant/docs/myfile.md

# 检查是否在 worktrees 中（不应该存在）
find ~/.cursor/worktrees/TRQuant -name "myfile.md" 2>/dev/null
```

### 2. 检查文件内容

```bash
# 查看文件内容，确认路径正确
head -5 /home/taotao/dev/QuantTest/TRQuant/docs/myfile.md
```

## 相关文档

- `docs/DISABLE_CURSOR_WORKTREES.md` - 禁用 worktrees 的完整指南
- `docs/CURSOR_WORKTREES_ISSUE.md` - Worktrees 问题详细分析
- `docs/FILE_OPERATIONS_GUIDE.md` - 文件操作规范

## 更新记录

- **2025-12-19**: 创建本文档，强制要求使用绝对路径

