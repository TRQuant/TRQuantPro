# Cursor Worktrees 问题分析与解决方案

## 问题描述

在使用 Cursor IDE 开发 TRQuant 项目时，会出现大量 `[composer] No code blocks found` 错误，错误路径指向 `~/.cursor/worktrees/TRQuant/xxx`，而不是主项目路径。

## 问题根源

### 1. Cursor Worktrees 机制

Cursor IDE 内部使用 **worktrees**（工作树）机制来管理多个工作区或临时工作空间。这些 worktrees 位于：
```
~/.cursor/worktrees/TRQuant/
├── obb/
├── jjb/
├── kbl/
└── ...
```

### 2. 问题原因

当代码使用 `vscode.workspace.workspaceFolders?.[0]?.uri.fsPath` 获取工作区路径时：
- **正常情况**：返回主项目路径
- **worktrees 情况**：返回 worktrees 路径 `~/.cursor/worktrees/TRQuant/obb`

这导致：
1. 文件路径解析错误
2. Composer 工具在错误的路径中查找代码块
3. Python 脚本执行失败
4. 各种功能异常

## 解决方案

### 1. 统一使用智能项目路径检测（可移植）

**核心原则**：使用智能检测机制，支持跨机器部署，避免依赖 `vscode.workspace.workspaceFolders`。

#### 实现方式

在 `extension/src/utils/config.ts` 中添加了 `getProjectRoot()` 方法，支持多种检测方式：

**检测顺序（优先级从高到低）：**

1. **环境变量 `TRQUANT_ROOT`**（最高优先级，用户可配置）
   - 适用于所有机器，推荐使用
   - 设置方法见下方"跨机器部署配置"

2. **从 extensionPath 推断**（最可靠的方法）
   - 如果扩展安装在 `xxx/extension`，自动识别项目根为 `xxx`
   - 适用于开发模式和标准安装

3. **工作区路径**（需要过滤 worktrees）
   - 使用 VS Code/Cursor 工作区路径
   - 自动过滤掉 `.cursor/worktrees` 路径
   - 验证路径有效性

4. **硬编码路径**（仅开发环境）
   - 仅作为最后回退，其他机器会跳过

#### 项目根目录验证

通过 `_isValidProjectRoot()` 方法验证路径是否为有效的 TRQuant 项目根目录：

- 检查关键目录/文件：`mcp_servers`, `core`, `extension`, `.git`, `docs`, `requirements.txt`
- 至少满足 2 个条件才确认为项目根目录
- 避免误判其他目录为项目根

### 2. 跨机器部署配置

#### 方法1：环境变量（推荐）

在不同机器上设置环境变量：

**Linux/macOS:**
```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export TRQUANT_ROOT=/path/to/your/TRQuant

# 重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc
```

**Windows:**
```powershell
# 在 PowerShell 中设置（临时）
$env:TRQUANT_ROOT = "C:\path\to\your\TRQuant"

# 或在系统环境变量中设置（永久）
# 控制面板 → 系统 → 高级系统设置 → 环境变量
```

#### 方法2：自动检测（默认）

如果不设置环境变量，系统会按以下顺序自动检测：

1. **从 extensionPath 推断**（最可靠）
   - 如果扩展安装在 `xxx/extension`，自动识别项目根为 `xxx`
   - 适用于开发模式和标准安装

2. **工作区路径**（过滤 worktrees）
   - 使用 VS Code/Cursor 工作区路径
   - 自动过滤掉 `.cursor/worktrees` 路径

3. **硬编码路径**（仅开发环境）
   - 仅作为最后回退，其他机器会跳过

#### 验证配置

在扩展日志中查看使用的路径：
- `使用TRQUANT_ROOT环境变量: xxx` - ✅ 环境变量配置成功
- `使用推断的项目路径: xxx` - ✅ 自动检测成功
- `使用工作区路径: xxx` - ✅ 工作区路径有效
- `使用回退路径（可能不正确）: xxx` - ⚠️ 需要配置环境变量

### 3. 修复所有使用工作区路径的代码

#### 已修复的文件

1. **`extension/src/views/workflowPanel.ts`**
   - `_getProjectRoot()` 方法已改用 `ConfigManager.getProjectRoot()`

2. **`extension/src/services/dataUpdateService.ts`**
   - `executePythonScript()` 方法已改用 `ConfigManager.getProjectRoot()`

3. **`extension/src/pythonBridge.ts`**
   - 需要更新为使用 `ConfigManager.getProjectRoot()`

#### 需要修复的文件

以下文件仍在使用 `vscode.workspace.workspaceFolders`，需要逐步修复：

- `extension/src/utils/config.ts` - `getPythonPath()` 方法
- `extension/src/views/mainDashboard.ts` - 多处使用
- `extension/src/views/strategyManagerPanel.ts`
- `extension/src/views/strategyGeneratorPanel.ts`
- `extension/src/views/resultManagerPanel.ts`
- `extension/src/services/trquantClient.ts`

### 4. 使用统一工具函数

**推荐做法**：所有需要获取项目根路径的地方，统一使用：

```typescript
import { ConfigManager } from '../utils/config';

const configManager = ConfigManager.getInstance();
const projectRoot = configManager.getProjectRoot(extensionPath);
```

## 验证方法

### 1. 检查 worktrees 目录

```bash
ls -la ~/.cursor/worktrees/TRQuant/
```

如果存在多个子目录，说明 Cursor 正在使用 worktrees。

### 2. 检查日志

在扩展日志中查找：
- `使用TRQUANT_ROOT环境变量` - ✅ 正确（推荐）
- `使用推断的项目路径` - ✅ 正确
- `检测到 worktrees 路径，已跳过` - ✅ 已过滤
- `使用工作区路径` - ⚠️ 需要检查是否指向 worktrees
- `使用回退路径（可能不正确）` - ❌ 需要配置环境变量

### 3. 测试功能

确保以下功能正常工作：
- 9步工作流执行
- 十倍股识别系统
- Python 脚本执行
- 文件读写操作

## 预防措施

### 1. 代码审查检查清单

在代码审查时，检查：
- [ ] 是否使用了 `vscode.workspace.workspaceFolders?.[0]?.uri.fsPath`？
- [ ] 是否优先使用 `ConfigManager.getProjectRoot()`？
- [ ] 是否过滤了 worktrees 路径？
- [ ] 是否验证了路径有效性？

### 2. 开发规范

**强制规则**：
1. ❌ **禁止**直接使用 `vscode.workspace.workspaceFolders` 获取项目路径
2. ✅ **必须**使用 `ConfigManager.getProjectRoot()` 获取项目路径
3. ✅ **必须**在获取路径后验证路径有效性
4. ✅ **推荐**设置 `TRQUANT_ROOT` 环境变量以支持跨机器部署

### 3. 新机器部署步骤

1. **克隆项目**
   ```bash
   git clone <repository-url> /path/to/TRQuant
   ```

2. **设置环境变量**（推荐）
   ```bash
   export TRQUANT_ROOT=/path/to/TRQuant
   ```

3. **验证配置**
   - 打开 VS Code/Cursor
   - 查看扩展日志，确认使用了正确的路径

## 相关文件

- `extension/src/utils/config.ts` - 统一路径获取工具
- `extension/src/views/workflowPanel.ts` - 已修复示例
- `extension/src/services/dataUpdateService.ts` - 已修复示例

## 更新记录

- **2025-12-19**: 创建本文档，分析 worktrees 问题并制定解决方案
- **2025-12-19**: 在 `config.ts` 中添加可移植的 `getProjectRoot()` 方法
- **2025-12-19**: 修复 `workflowPanel.ts` 和 `dataUpdateService.ts` 使用统一路径获取方法
- **2025-12-19**: 添加跨机器部署配置说明

## 参考

- [VS Code Workspace API](https://code.visualstudio.com/api/references/vscode-api#workspace)
- [Cursor IDE 内部机制](https://cursor.sh/docs)（官方文档可能不包含 worktrees 说明）

