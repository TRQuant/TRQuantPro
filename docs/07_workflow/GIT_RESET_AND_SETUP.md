# Git清理和重新配置步骤

> **目标**: 清理旧的Git配置，重新配置到新仓库 `TRQuant_ope`

---

## 📋 操作步骤

### 步骤1: 清理旧的Git相关文件和配置

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 删除.git目录或.git文件
rm -rf .git
rm -f .git*

# 或者更彻底的清理（如果需要）
find . -name ".git*" -not -path "./.gitignore" -delete
```

**清理的内容**：
- `.git/` 目录（如果是独立仓库）
- `.git` 文件（如果是worktree）
- 其他Git相关隐藏文件（保留`.gitignore`）

---

### 步骤2: 重新初始化Git仓库

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 初始化新的Git仓库
git init

# 验证初始化成功
ls -la .git
```

---

### 步骤3: 配置Remote到新仓库

```bash
# 添加新仓库作为origin
git remote add origin https://github.com/TRQuant/TRQuant_ope.git

# 验证Remote配置
git remote -v

# 应该显示：
# origin  https://github.com/TRQuant/TRQuant_ope.git (fetch)
# origin  https://github.com/TRQuant/TRQuant_ope.git (push)
```

---

### 步骤4: 验证配置

```bash
# 检查Git状态
git status

# 检查Remote
git remote -v

# 检查分支
git branch
```

---

## 🔒 注意事项

### .gitignore已配置

- ✅ 敏感文件已排除（密码、token等）
- ✅ 可重新构建的文件已排除（venv、node_modules等）
- ✅ 数据文件已排除（data、logs、results等）
- ✅ 核心代码和配置文件会保留

### 提交前检查

```bash
# 查看将要添加的文件
git status

# 检查是否有敏感文件
git status | grep -E "token|key|password|secret|\.env"

# 如果有敏感文件，确保.gitignore已正确配置
```

---

## ✅ 完成后的操作

1. **添加文件**：
   ```bash
   git add .
   ```

2. **提交**：
   ```bash
   git commit -m "Initial commit: 核心代码和配置文件"
   ```

3. **推送**（首次）：
   ```bash
   git push -u origin main
   # 或者
   git push -u origin master
   ```

---

*创建时间: 2025-01-03*




