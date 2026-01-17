# 禁用 Cursor Worktrees 完整指南

## ⚠️ 重要：文件操作必须使用绝对路径

**在创建或修改文件时，必须使用绝对路径！**

**❌ 错误示例**：
```
请创建文件：docs/DISABLE_CURSOR_WORKTREES.md
```

**✅ 正确示例**：
```
请创建文件：/home/taotao/dev/QuantTest/TRQuant/docs/DISABLE_CURSOR_WORKTREES.md
```

**原因**：Cursor 的 `write` 工具使用当前工作区路径作为基础路径。如果当前工作区是 worktrees（`~/.cursor/worktrees/TRQuant/xxx`），相对路径会被解析到错误的位置。

**详细说明**：请参考 `docs/ABSOLUTE_PATH_REQUIREMENT.md`


## ⚠️ 问题严重性

**当前状态**：
- worktrees 目录占用：**99GB**
- worktrees 子目录数量：**92+ 个**
- 导致的问题：
  - 文件被错误创建到 worktrees 中
  - 路径混淆，代码无法找到正确文件
  - Composer 工具在错误路径中查找代码块
  - 磁盘空间浪费

## Worktrees 的作用

Cursor IDE 使用 `~/.cursor/worktrees/TRQuant/` 来创建 Git 工作树，用于：
- **沙盒模式（Sandbox Mode）**：在隔离环境中运行代码，防止意外修改主项目
- **并行开发**：支持多个工作区同时开发

**但对我们来说**：
- ❌ 造成路径混淆
- ❌ 文件被创建到错误位置
- ❌ 占用大量磁盘空间（99GB）
- ❌ 没有实际价值（我们已经有 Git 版本控制）

## 禁用方法

### 方法1：禁用沙盒模式（推荐）

1. **打开 Cursor 设置**
   - `Ctrl+,` (Windows/Linux) 或 `Cmd+,` (macOS)
   - 或点击左下角齿轮图标 → Settings

2. **搜索 "Auto-Run Mode"**
   - 在设置搜索框中输入：`agent.autoRunMode`

3. **修改设置**
   - 找到 `Agent > Auto-Run Mode`
   - 将值从 `sandbox` 改为 `everything`
   - 或直接设置为 `disabled`（完全禁用自动运行）

4. **重启 Cursor**
   - 完全关闭并重新打开 Cursor IDE

### 方法2：通过 settings.json 配置

1. **打开 settings.json**
   - `Ctrl+Shift+P` → 输入 "Preferences: Open User Settings (JSON)"

2. **添加配置**
   ```json
   {
     "agent.autoRunMode": "everything",
     "cursor.general.enableSandbox": false
   }
   ```

3. **保存并重启**

### 方法3：清理现有 worktrees（可选）

**⚠️ 警告**：在禁用沙盒模式后再执行此操作！

```bash
# 备份（可选）
mv ~/.cursor/worktrees/TRQuant ~/.cursor/worktrees/TRQuant.backup

# 删除 worktrees 目录
rm -rf ~/.cursor/worktrees/TRQuant

# 验证删除
ls ~/.cursor/worktrees/TRQuant 2>&1 || echo "✅ worktrees 已删除"
```

**注意**：删除后可以释放约 99GB 磁盘空间。

## 验证禁用是否成功

### 1. 检查设置

```bash
# 查看 Cursor 配置
cat ~/.config/Cursor/User/settings.json | grep -i "autorun\|sandbox"
```

应该看到：
```json
"agent.autoRunMode": "everything"
```

### 2. 检查工作区路径

在 Cursor 中：
- 打开终端
- 运行：`pwd`
- 应该显示主项目路径：`/home/taotao/dev/QuantTest/TRQuant`
- **不应该**显示：`~/.cursor/worktrees/TRQuant/xxx`

### 3. 测试文件创建

创建一个测试文件，检查位置：
```bash
# 在 Cursor 终端中
echo "test" > test_worktrees.txt
ls -la test_worktrees.txt
# 应该显示在主项目路径中
```

### 4. 监控 worktrees 目录

```bash
# 监控是否有新的 worktrees 创建
watch -n 5 'ls -la ~/.cursor/worktrees/TRQuant/ 2>/dev/null | wc -l'
```

如果禁用成功，不应该有新的 worktrees 创建。

## 代码层面的保护措施

即使禁用了 worktrees，我们仍然需要在代码中强制使用主项目路径：

### 1. 使用 ConfigManager.getProjectRoot()

```typescript
import { ConfigManager } from '../utils/config';

const configManager = ConfigManager.getInstance();
const projectRoot = configManager.getProjectRoot(extensionPath);
// 始终使用绝对路径
const filePath = path.join(projectRoot, 'docs', 'myfile.md');
```

### 2. 验证路径

```typescript
// 验证路径是否在主项目中
if (!filePath.startsWith(projectRoot)) {
    throw new Error(`文件路径必须在项目根目录内: ${filePath}`);
}
```

### 3. 使用绝对路径

**❌ 错误**：
```typescript
const filePath = 'docs/myfile.md';  // 相对路径
```

**✅ 正确**：
```typescript
const projectRoot = configManager.getProjectRoot(extensionPath);
const filePath = path.join(projectRoot, 'docs', 'myfile.md');  // 绝对路径
```

## 清理脚本

创建一个清理脚本（在禁用沙盒模式后使用）：

```bash
#!/bin/bash
# cleanup_worktrees.sh

echo "=== 清理 Cursor Worktrees ==="
echo ""

# 检查是否已禁用沙盒模式
if [ -f ~/.config/Cursor/User/settings.json ]; then
    if grep -q '"agent.autoRunMode": "everything"' ~/.config/Cursor/User/settings.json; then
        echo "✅ 沙盒模式已禁用"
    else
        echo "⚠️  警告：请先禁用沙盒模式！"
        echo "   设置: agent.autoRunMode = everything"
        exit 1
    fi
else
    echo "⚠️  无法找到 Cursor 配置文件"
fi

# 计算 worktrees 大小
SIZE=$(du -sh ~/.cursor/worktrees/TRQuant 2>/dev/null | cut -f1)
echo "当前 worktrees 大小: $SIZE"
echo ""

# 确认删除
read -p "是否删除 worktrees 目录？(y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在删除..."
    rm -rf ~/.cursor/worktrees/TRQuant
    echo "✅ 已删除 worktrees 目录"
    echo "释放空间: $SIZE"
else
    echo "已取消"
fi
```

## 注意事项

1. **备份重要数据**：在删除 worktrees 前，确保没有重要文件在其中
2. **Git 状态**：worktrees 是 Git 工作树，删除不会影响主项目
3. **重启 Cursor**：修改设置后必须重启 Cursor 才能生效
4. **监控空间**：定期检查 worktrees 目录，确保没有重新创建

## 相关文档

- `docs/CURSOR_WORKTREES_ISSUE.md` - Worktrees 问题详细分析
- `docs/FILE_OPERATIONS_GUIDE.md` - 文件操作规范

## 更新记录

- **2025-12-19**: 创建本文档，提供禁用 worktrees 的完整方案

