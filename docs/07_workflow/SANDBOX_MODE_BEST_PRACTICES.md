# Cursor 沙盒模式最佳开发实践

> **更新时间**: 2025-01-03  
> **目的**: 如果启用沙盒模式，如何避免worktrees目录问题

---

## 🎯 核心问题
### 关于ope目录的搜索问题

**问题原因**：
- 即使已经"删除"ope目录，如果Git worktree引用还存在，Cursor仍可能搜索它
- ope目录可能仍然存在于文件系统中
- Git worktree引用没有清理

**解决方案**：
1. 清理Git worktree引用：`git worktree prune`
2. 删除目录：`rm -rf ~/.cursor/worktrees/TRQuant/ope`
3. 验证清理：`git worktree list`



即使已经删除了ope目录，Cursor在沙盒模式下仍然可能：
1. 自动搜索worktrees目录下的其他文件夹
2. 创建新的三字母worktree目录
3. 导致路径混淆

---

## ✅ 推荐方案：禁用沙盒模式（当前状态）

### 当前配置

```json
{
  "cursor.codebaseIndexing.enableWorktrees": false,
  "cursor.workspace.useWorktrees": false,
  "agent.autoRunMode": "everything"  // 或 "disabled"
}
```

### 优势

- ✅ 直接在worktrees根目录工作（无额外worktree创建）
- ✅ 路径清晰，不会混淆
- ✅ 性能更好（无需创建额外目录）
- ✅ 避免磁盘空间浪费

---

## 🔄 如果要开启沙盒模式

### 沙盒模式的作用

- **隔离执行**: 在隔离环境中运行代码，防止意外修改主项目
- **安全测试**: 可以在不修改主项目的情况下测试代码

### 最佳实践


### 一键清理脚本

已创建清理脚本 `cleanup_worktrees.sh`：

```bash
# 执行清理
/tmp/cleanup_worktrees.sh

# 或手动执行步骤
cd /home/taotao/dev/QuantTest/TRQuant
git worktree remove ~/.cursor/worktrees/TRQuant/ope
git worktree remove ~/.cursor/worktrees/TRQuant/abd
git worktree prune
cd ~/.cursor/worktrees/TRQuant
rm -rf ope/ abd/ gui/ web/ [a-z][a-z][a-z]/
```

#### 目录类型说明
**⚠️ 重要**：只删除沙盒目录（ope, abd, 三字母目录），不要删除项目开发目录（gui, web等）！

#### 1. 清理现有worktree引用

```bash
# 清理Git worktree引用
cd /home/taotao/dev/QuantTest/TRQuant
git worktree remove ~/.cursor/worktrees/TRQuant/ope
git worktree remove ~/.cursor/worktrees/TRQuant/abd
git worktree prune

# 删除沙盒目录（只删除沙盒创建的目录）
cd ~/.cursor/worktrees/TRQuant
rm -rf ope/ abd/  # 沙盒目录

# 删除三字母目录（沙盒创建的worktree）
# ⚠️ 注意：gui和web是项目开发目录，不要删除！
find . -maxdepth 1 -type d -name "[a-z][a-z][a-z]" ! -name "gui" ! -name "web" -exec rm -rf {} +
```

#### 2. 配置工作目录排除

在 `.gitignore` 或 Cursor 配置中排除worktrees子目录：

```gitignore
# .gitignore
.cursor/worktrees/*/
!.cursor/worktrees/TRQuant/
```

#### 3. 使用绝对路径（强制）

**所有文件操作必须使用绝对路径**：

```python
# ✅ 正确
file_path = "/home/taotao/.cursor/worktrees/TRQuant/docs/file.md"

# ❌ 错误
file_path = "docs/file.md"  # 会被解析到worktree子目录
```

#### 4. 在代码中验证路径

```python
import os
from pathlib import Path

# 验证路径是否在正确位置
def validate_path(path: str) -> bool:
    project_root = Path("/home/taotao/.cursor/worktrees/TRQuant")
    resolved = Path(path).resolve()
    return resolved.is_relative_to(project_root) and "worktrees/TRQuant/" not in str(resolved.parents)
```

#### 5. 使用环境变量

```bash
# 设置环境变量
export TRQUANT_ROOT=/home/taotao/.cursor/worktrees/TRQuant

# 在代码中使用
import os
PROJECT_ROOT = os.environ.get('TRQUANT_ROOT', '/home/taotao/.cursor/worktrees/TRQuant')
```

---

## 🛡️ 防护措施

### 1. 代码层面的保护

在代码中检查路径：

```python
def ensure_main_directory(path: Path) -> Path:
    """确保路径指向主工作目录，而不是worktree子目录"""
    worktrees_pattern = "/worktrees/TRQuant/"
    if worktrees_pattern in str(path):
        parts = str(path).split(worktrees_pattern)
        if len(parts) > 1 and parts[1]:
            # 如果在worktree子目录中，转换到主目录
            main_dir = Path("/home/taotao/.cursor/worktrees/TRQuant")
            return main_dir / parts[1]
    return path
```

### 2. 监控worktrees目录

```bash
# 定期检查是否有新的worktree创建
watch -n 60 'ls -d ~/.cursor/worktrees/TRQuant/[a-z][a-z][a-z] 2>/dev/null | wc -l'
```

### 3. 清理脚本

```bash
#!/bin/bash
# cleanup_worktrees.sh

WORKTREES_ROOT=~/.cursor/worktrees/TRQuant

# 清理所有三字母目录（保留根目录）
find "$WORKTREES_ROOT" -maxdepth 1 -type d -name "[a-z][a-z][a-z]" -exec rm -rf {} +

# 清理Git worktree引用
cd /home/taotao/dev/QuantTest/TRQuant
git worktree prune

echo "✅ Worktrees已清理"
```

---

## 📋 检查清单

如果启用沙盒模式，定期检查：

- [ ] worktrees目录下是否有新的三字母目录
- [ ] Git worktree列表是否干净
- [ ] 代码中的路径是否使用绝对路径
- [ ] 文件操作是否在正确位置
- [ ] 磁盘空间使用是否正常

---

## 💡 建议

### 推荐：保持当前配置（禁用worktrees）

**理由**：
1. ✅ 当前配置已经工作良好
2. ✅ 在worktrees根目录工作，路径清晰
3. ✅ 无需额外的worktree管理
4. ✅ 性能更好，资源占用更少

### 如果必须使用沙盒模式

1. **定期清理**: 每天或每周清理worktrees子目录
2. **路径验证**: 代码中验证路径正确性
3. **监控脚本**: 使用脚本监控新目录创建
4. **文档记录**: 记录worktree使用情况

---

## 🔗 相关文档

- `docs/DISABLE_CURSOR_WORKTREES.md` - 禁用worktrees指南
- `docs/WORKTREE_FOLDER_EXPLANATION.md` - worktree机制说明
- `docs/CURSOR_DEFAULT_WORKDIRECTORY.md` - 默认工作目录机制

---

*最后更新: 2025-01-03*
