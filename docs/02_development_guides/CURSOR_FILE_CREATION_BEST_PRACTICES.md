# Cursor文件创建最佳实践

> **更新时间**: 2025-01-03  
> **目的**: 确保文件在正确位置创建，避免创建到沙盒目录

## ✅ 测试结果

### 当前状态

1. **ope目录**: 已删除（不存在）
2. **Git worktree引用**: 已清理（无ope引用）
3. **新沙盒目录**: 未创建（配置已禁用worktrees）

### 文件创建行为

- ✅ **绝对路径**: 文件创建在指定位置
- ✅ **相对路径（当前工作目录正确时）**: 文件创建在当前目录

## 📋 最佳实践

### 1. 文件创建位置规范

#### ✅ 推荐：使用绝对路径

```python
# ✅ 正确
file_path = "/home/taotao/.cursor/worktrees/TRQuant/docs/myfile.md"

# ⚠️ 相对路径（需要确认当前工作目录正确）
file_path = "docs/myfile.md"
```

#### ✅ 工作目录

当前工作目录：`/home/taotao/.cursor/worktrees/TRQuant/`

所有文件操作应该基于此目录。

### 2. 文件创建检查清单

在创建文件前，检查：

- [ ] 是否使用了绝对路径？
- [ ] 路径是否包含 `worktrees/TRQuant/`？
- [ ] 路径中是否没有三字母子目录（如 `ope/`, `abd/`等）？
- [ ] 是否确认了当前工作目录？

### 3. 沙盒模式使用

**默认行为（当前配置）**：
- ✅ worktrees自动创建已禁用
- ✅ 文件创建在worktrees根目录
- ✅ 不会创建新的沙盒目录

**如果需要沙盒模式**：
- 明确指定使用沙盒
- 文件会创建在沙盒目录中
- 完成后需要手动复制到正确位置

### 4. 验证文件位置

创建文件后，验证：

```bash
# 检查文件是否在正确位置
ls -lh /home/taotao/.cursor/worktrees/TRQuant/docs/myfile.md

# 检查是否在错误的沙盒目录中（不应该存在）
find ~/.cursor/worktrees/TRQuant/[a-z][a-z][a-z]/ -name "myfile.md" 2>/dev/null
```

## ⚠️ 注意事项

### 1. 相对路径的风险

使用相对路径时：
- 取决于当前工作目录
- 如果工作目录是worktrees根目录，相对路径可以工作
- 但如果工作目录改变，可能创建到错误位置

### 2. 沙盒目录识别

如果发现文件创建在以下位置，说明创建在了沙盒目录：
- `~/.cursor/worktrees/TRQuant/xxx/docs/...` (xxx是三字母目录)
- 应该创建在: `~/.cursor/worktrees/TRQuant/docs/...`

### 3. Cursor配置

当前配置（`settings.json`）：
```json
{
  "cursor.codebaseIndexing.enableWorktrees": false,
  "cursor.workspace.useWorktrees": false,
  "agent.autoRunMode": "everything"
}
```

这些配置确保了：
- ✅ 不会自动创建worktrees
- ✅ 文件创建在正确位置
- ✅ 不会创建新的沙盒目录

## 📝 建议

### 立即执行

1. ✅ **使用绝对路径创建所有文件**
2. ✅ **验证文件创建位置**
3. ✅ **监控是否有新沙盒目录创建**

### 长期维护

1. ✅ 保持当前配置（禁用worktrees自动创建）
2. ✅ 所有文件操作使用绝对路径
3. ✅ 定期检查是否有新的沙盒目录

---

*最后更新: 2025-01-03*
