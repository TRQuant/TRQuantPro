# Cursor 默认工作目录机制

## 🔍 检查结果

### 当前状态

1. **Cursor配置**：
   ```json
   "cursor.codebaseIndexing.enableWorktrees": false
   "cursor.workspace.useWorktrees": false
   ```
   - ✅ 已禁用worktrees自动创建

2. **Git worktree状态**：
   ```
   /home/taotao/dev/QuantTest/TRQuant          e81133c5 [main]
   /home/taotao/.cursor/worktrees/TRQuant/abd  43d88ea2 (detached HEAD) prunable
   /home/taotao/.cursor/worktrees/TRQuant/ope  43d88ea2 (detached HEAD)
   ```
   - `ope` 是注册的Git worktree
   - `abd` 标记为prunable（可删除）

3. **worktrees目录结构**：
   - 根目录：完整的Git仓库（不是worktree引用）
   - `ope/`：Git worktree（通过.git文件引用）
   - `gui/`, `web/`：其他目录

## ❌ 系统不会默认在ope工作

### Cursor的worktree机制

1. **自动创建**：
   - Cursor会创建**随机的三字母目录**（如 `fpc`, `obb`, `jjb`等）
   - 每次创建都是新的随机名称
   - **不会固定使用ope**

2. **手动打开**：
   - 如果用户手动打开某个目录，Cursor会在那个目录工作
   - 但不会默认选择ope

3. **当前配置**：
   - 已禁用worktrees自动创建
   - 但可能仍会在worktrees目录工作（如果打开了worktrees下的目录）

## ✅ 实际情况

### 如果Cursor在worktrees目录工作

Cursor会：
1. 创建新的随机三字母目录（如 `abc`, `xyz`等）
2. 或者使用已存在的目录（如果手动打开）
3. **不会默认使用ope**

### 如果Cursor在根目录工作

从检查看，worktrees根目录是**完整的Git仓库**，不是worktree引用：
- ✅ 有完整的`.git`目录
- ✅ 可以直接工作
- ✅ 有remote配置

## 🎯 建议

### 方案1：在worktrees根目录工作（推荐）

**优势**：
- ✅ 文件完整（173,950个文件）
- ✅ Git配置完整
- ✅ Cursor默认会在这里工作（如果打开了这个目录）
- ✅ 包含运行时环境

**操作**：
```bash
# 在Cursor中手动打开worktrees根目录
# File -> Open Folder -> ~/.cursor/worktrees/TRQuant
```

### 方案2：删除ope，使用根目录

如果确定在根目录工作：
```bash
cd ~/.cursor/worktrees/TRQuant
rm -rf ope/  # 删除ope目录
# 然后清理Git worktree引用
cd /home/taotao/dev/QuantTest/TRQuant
git worktree remove ~/.cursor/worktrees/TRQuant/ope
git worktree prune
```

### 方案3：配置Cursor使用固定目录

虽然Cursor不会默认使用ope，但可以：
1. 在Cursor中手动打开worktrees根目录
2. 保存为工作区（Workspace）
3. 下次直接打开工作区文件

## 📝 总结

**回答你的问题**：
- ❌ **系统不会默认在ope工作**
- ✅ Cursor会创建随机三字母目录，或使用手动打开的目录
- ✅ **推荐在worktrees根目录工作**（文件完整，Git配置好）
- ⚠️ ope可以删除（如果不在那里工作）

**最佳实践**：
1. 在Cursor中打开worktrees根目录
2. 删除ope目录（如果不需要）
3. 直接在根目录开发










