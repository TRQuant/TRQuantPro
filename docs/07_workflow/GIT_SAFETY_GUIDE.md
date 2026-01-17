# Git 安全使用指南

## ⚠️ 今天发生的问题

**时间**: 2025-12-13 早上
**问题**: 执行 `git restore` 命令覆盖了未提交的更改
**原因**: `git restore` 会直接恢复文件到HEAD状态，不会自动备份未提交的更改

## 🛡️ 已设置的安全措施

### 1. Git Pre-Restore Hook
位置: `.git/hooks/pre-restore`
功能: 在执行restore前自动stash当前更改

### 2. 安全恢复脚本
位置: `scripts/safe_restore.sh`
使用方法:
```bash
./scripts/safe_restore.sh <文件路径>
```

### 3. Git 安全别名
使用方法:
```bash
git safe-restore <文件路径>  # 会自动备份后恢复
```

## 📋 最佳实践

### 在执行任何可能覆盖更改的命令前：

1. **先检查未提交的更改**:
   ```bash
   git status
   git diff
   ```

2. **先保存更改**:
   ```bash
   git stash push -m "描述性信息"
   ```

3. **再执行恢复**:
   ```bash
   git restore <文件>
   ```

4. **或者使用安全命令**:
   ```bash
   git safe-restore <文件>
   # 或
   ./scripts/safe_restore.sh <文件>
   ```

## 🔄 恢复丢失的更改

如果更改被覆盖了：

1. **检查stash**:
   ```bash
   git stash list
   git stash show -p stash@{0}
   ```

2. **检查dangling objects**:
   ```bash
   git fsck --lost-found
   ```

3. **如果记得内容，重新实现**

## ⚡ 紧急情况处理

如果发现更改被覆盖：

1. **立即停止所有git操作**
2. **检查是否有自动备份**
3. **检查编辑器历史**
4. **检查stash列表**
5. **如果可能，使用文件恢复工具**

## 📝 预防措施

1. **定期提交**: 不要长时间保持未提交状态
2. **使用安全命令**: 优先使用 `git safe-restore`
3. **配置编辑器自动保存**: 确保编辑器有本地历史功能
4. **设置自动备份**: 考虑使用定时备份脚本

