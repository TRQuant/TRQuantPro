# 避免搜索ope文件夹 - 完整解决方案

> **更新时间**: 2025-01-03  
> **问题**: Cursor仍然会自动搜索ope文件夹

## 🔍 问题原因

### 为什么还会搜索ope？

1. **ope目录仍然存在**
   - 即使说"已删除"，但目录可能还在
   - 需要实际检查：`ls -la ~/.cursor/worktrees/TRQuant/ | grep ope`

2. **Git worktree引用未清理**
   - Git仍然认为ope是有效的worktree
   - 查看：`git worktree list`
   - 如果显示`prunable`，说明引用还在但目录可能已删除

3. **Cursor的索引机制**
   - Cursor会索引worktrees目录下的所有子目录
   - 即使禁用了worktrees创建，已有的目录仍会被索引

## ✅ 完整解决方案

### 步骤1：清理Git worktree引用

```bash
cd /home/taotao/dev/QuantTest/TRQuant

# 移除worktree引用
git worktree remove ~/.cursor/worktrees/TRQuant/ope
git worktree remove ~/.cursor/worktrees/TRQuant/abd

# 清理已删除的引用
git worktree prune

# 验证
git worktree list
# 应该只显示主仓库，没有ope和abd
```


### 目录类型说明

**沙盒目录**（需要清理）：
- `ope/`, `abd/` 等 - Cursor沙盒模式创建的Git worktree
- `[a-z][a-z][a-z]/` - 三字母目录（沙盒创建的临时worktree）

**项目开发目录**（必须保留）：
- `gui/` - GUI开发目录
- `web/` - Web开发目录
- 其他项目目录

⚠️ **重要**：清理时只删除沙盒目录，不要删除项目开发目录！

### 步骤2：删除目录（如果还存在）

```bash
cd ~/.cursor/worktrees/TRQuant

# 删除ope目录（如果存在）
rm -rf ope/

# 删除其他不需要的子目录
rm -rf abd/ gui/ web/

# 删除所有三字母目录
find . -maxdepth 1 -type d -name "[a-z][a-z][a-z]" -exec rm -rf {} +
```

### 步骤3：验证清理结果

参考完整文档获取详细步骤。

## 🔄 如果要开启沙盒模式

参考 `docs/SANDBOX_MODE_BEST_PRACTICES.md` 了解最佳实践。

## 💡 建议

**推荐：保持当前配置（禁用worktrees）**

理由：
- ✅ 当前配置已经工作良好
- ✅ 在worktrees根目录工作，路径清晰
- ✅ 无需额外的worktree管理
- ✅ 性能更好，资源占用更少

*最后更新: 2025-01-03*
