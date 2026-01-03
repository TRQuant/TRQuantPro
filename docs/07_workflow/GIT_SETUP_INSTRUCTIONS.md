# Git仓库初始化说明

> **新仓库**: https://github.com/TRQuant/TRQuant_ope.git

---

## 🚀 快速开始

### 方法1: 使用脚本（推荐）

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope
bash setup_new_git.sh
```

### 方法2: 手动执行

```bash
cd /home/taotao/.cursor/worktrees/TRQuant/ope

# 1. 清理旧配置（如果有）
rm -rf .git .git*

# 2. 初始化Git
git init

# 3. 配置Remote
git remote add origin https://github.com/TRQuant/TRQuant_ope.git

# 4. 验证
git remote -v
```

---

## 📋 后续步骤

### 1. 添加核心文件

```bash
# 添加核心代码和配置
git add .gitignore
git add core/ config/ strategies/ data_sources/
git add notebooks/ docs/ scripts/ utils/
git add requirements.txt requirements-dev.txt pyproject.toml
git add README.md README.txt VERSION

# 或添加所有（.gitignore会过滤敏感文件）
git add .
```

### 2. 查看将要提交的内容

```bash
# 查看状态
git status

# 查看将要提交的文件
git diff --cached --name-only
```

### 3. 提交

```bash
git commit -m "Initial commit: 核心代码和配置文件"
```

### 4. 推送（首次）

```bash
# 如果分支是main
git push -u origin main

# 如果分支是master
git push -u origin master
```

---

## 🔒 安全注意事项

### .gitignore已配置排除：

- ✅ 敏感信息：`*.token`, `*.key`, `github_token.txt`, `.env`
- ✅ 可重新构建：`venv/`, `node_modules/`, `build/`, `dist/`
- ✅ 数据文件：`data/`, `*.csv`, `*.db`, `logs/`
- ✅ 测试结果：`backtest_results/`, `results/`, `output/`

### 提交前检查：

```bash
# 检查是否有敏感文件被添加
git status | grep -E "token|key|password|secret|\.env"

# 如果有，从暂存区移除
git reset HEAD <文件路径>
```

---

## ✅ 验证清单

- [ ] Git已初始化（`.git`目录/文件存在）
- [ ] Remote配置正确（`git remote -v`）
- [ ] .gitignore文件存在
- [ ] 敏感文件已排除
- [ ] 核心文件已添加
- [ ] 提交成功
- [ ] 推送成功

---

*创建时间: 2025-01-03*




